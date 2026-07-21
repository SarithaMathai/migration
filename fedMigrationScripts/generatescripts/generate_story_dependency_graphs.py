#!/usr/bin/env python3
"""
Per-domain story dependency graphs — two mermaid diagrams, one file per domain.

Both graphs are rendered from data other generators already compute (compute_implementation_order's
DAG, fe-08's Depends-on lines) — nothing here invents new dependency facts, it only visualizes what
be-04-stories.md / fe-08-frontend-stories.md already declare. Regenerate whenever those change.

  Graph A — BE Story Dependency (intra-domain build order)
    Nodes: this domain's BE-* stories only. Edges: Depends-on, same DAG generate_breakdown.py's
    compute_implementation_order() builds for 02-project-plan.md's step tables. Grouped into
    swimlanes by implementation step so the read order matches the build order.
    Audience: the backend engineer sequencing their own PRs.

  Graph B — FE Readiness (client story dependency)
    Nodes: this domain's FE-* stories + every BE story any of them depends on (which may pull in
    upstream BE stories transitively, via Graph A's own edges, even ones an FE story doesn't name
    directly). Edges: BE -> FE ("must ship before this FE story can start") plus the BE -> BE chain
    behind each gate. Audience: FE engineer or PO checking "is backend far enough along to start."

Output: finalArtifacts/summary/{domain}/story-dependency-graph-{domain}.md

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_story_dependency_graphs.py              # all domains
    python fedMigrationScripts/generatescripts/generate_story_dependency_graphs.py watchlist     # one domain
"""

import re
import sys
from pathlib import Path
from datetime import date

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ANALYSIS = ROOT / "output" / "analysis"
FINAL = ROOT / "finalArtifacts"
TODAY = date.today().isoformat()

from generate_breakdown import (
    parse_stories, get_domain_dir, compute_implementation_order,
    _short_id, PHASE_ICONS, PHASE_NAMES, PHASE_SEQ,
)
from generate_frontend import parse_fe_stories, domain_key_from_token

ALL_DOMAINS = [
    "bom", "claims", "impression", "measurement",
    "packaging", "product", "productDetails", "watchlist",
]
DOMAIN_LABELS = {
    "bom": "BOM", "claims": "Claims", "impression": "Impression",
    "measurement": "Measurement", "packaging": "Packaging", "product": "Product",
    "productDetails": "Product Details", "watchlist": "Watchlist",
}


def _mid(short_id: str) -> str:
    """A mermaid-safe node id — short ids contain '-' which mermaid tolerates in labels but
    not cleanly in bare node ids, so prefix + strip."""
    return "N" + re.sub(r"[^A-Za-z0-9]", "_", short_id)


def _label(short_id: str, title: str, max_len: int = 34) -> str:
    t = re.sub(r"`", "", title).strip()
    if len(t) > max_len:
        t = t[: max_len - 1].rstrip() + "…"
    # mermaid node labels: quote and escape internal quotes
    text = f"{short_id}<br/>{t}".replace('"', "'")
    return f'["{text}"]'


def build_be_graph(domain: str, stories: list[dict]) -> str:
    """Graph A — BE Story Dependency. Swimlaned by implementation step (Graph = subgraph per step)."""
    waves, gates, _crit = compute_implementation_order(stories)
    by_short = {_short_id(s["id"]): s for s in stories}

    lines = ["```mermaid", "flowchart TD"]
    seen_edges = set()
    for step_no, wave in enumerate(waves, 1):
        phases = sorted({s["phase"] for s in wave if s["phase"] in PHASE_SEQ}, key=PHASE_SEQ.find)
        focus = " · ".join(f"{PHASE_ICONS[p]} {PHASE_NAMES[p]}" for p in phases) or "—"
        lines.append(f'  subgraph STEP{step_no}["Step {step_no} — {focus}"]')
        for s in wave:
            sid = _short_id(s["id"])
            lines.append(f"    {_mid(sid)}{_label(sid, s['title'])}")
        lines.append("  end")

    # Edges — recompute from the same source the DAG used, so arrows match the steps exactly.
    for s in stories:
        sid = _short_id(s["id"])
        if sid not in by_short:
            continue
        for m in re.finditer(r"\b(?:[A-Z]+-BE-)?([A-H]-\d+(?:-\d+)?)\b", s.get("depends", "") or ""):
            dep = m.group(1)
            if dep in by_short and dep != sid:
                edge = (dep, sid)
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    lines.append(f"  {_mid(dep)} --> {_mid(sid)}")

    # Gates (spike / cross-subgraph blocks) — shown as dashed edges from an external gate node,
    # not real ordering edges (matches the "entry criteria, not scheduler-enforced" convention
    # used in output/overview/01-architecture-diagrams.md §3).
    gate_nodes_emitted = set()
    for sid, gate_list in gates.items():
        if sid not in by_short:
            continue
        for g in gate_list:
            gnode = "G" + re.sub(r"[^A-Za-z0-9]", "_", g)
            if gnode not in gate_nodes_emitted:
                gate_nodes_emitted.add(gnode)
                label = g.replace('"', "'")
                lines.append(f'  {gnode}{{{{"{label}"}}}}')
            lines.append(f"  {gnode} -.-> {_mid(sid)}")

    lines.append("```")
    return "\n".join(lines)


def build_fe_graph(domain: str, be_stories: list[dict], fe_stories: list[dict]) -> str:
    """Graph B — FE Readiness. Nodes = this domain's FE stories + every BE story gating one of
    them (directly or via that BE story's own upstream chain, so a reader can see the full
    'what must be true' picture without cross-referencing Graph A)."""
    by_short = {_short_id(s["id"]): s for s in be_stories}
    _waves, _gates, _crit = compute_implementation_order(be_stories)
    _by_short2, deps, _gates2, _scaffold = (lambda bs: __import__(
        "generate_breakdown")._dependency_graph(bs))(be_stories)

    dom_fe = [f for f in fe_stories
              if domain_key_from_token(f["id"].rsplit("-FE-", 1)[0]) == domain]
    if not dom_fe:
        return "_No frontend stories recorded for this domain in fe-08-frontend-stories.md._"

    def upstream_chain(short_id: str, acc: set) -> None:
        if short_id in acc or short_id not in deps:
            return
        acc.add(short_id)
        for d in deps[short_id]:
            upstream_chain(d, acc)

    needed_be: set = set()
    fe_edges: list[tuple] = []   # (be_short_id, fe_id)
    for f in dom_fe:
        for full_dep in f["depends"]:
            m = re.search(r"-BE-([A-H]-\d+(?:-\d+)?)$", full_dep)
            if not m:
                continue
            sid = m.group(1)
            if sid in by_short:
                fe_edges.append((sid, f["id"]))
                upstream_chain(sid, needed_be)

    lines = ["```mermaid", "flowchart LR"]
    lines.append('  subgraph BE["Backend — must ship first"]')
    for sid in sorted(needed_be, key=lambda k: (PHASE_SEQ.find(k[0]) if k[0] in PHASE_SEQ else 99, k)):
        s = by_short[sid]
        lines.append(f"    {_mid(sid)}{_label(sid, s['title'])}")
    lines.append("  end")

    lines.append('  subgraph FE["Frontend — this domain\'s cutover stories"]')
    for f in dom_fe:
        lines.append(f'    {_mid(f["id"])}["{f["id"]}<br/>{f["title"][:34].replace(chr(34), chr(39))}"]')
    lines.append("  end")

    # BE -> BE edges within the needed set (the upstream chain a reader would otherwise have
    # to look up in Graph A).
    seen = set()
    for sid in needed_be:
        for d in deps.get(sid, set()):
            if d in needed_be and (d, sid) not in seen:
                seen.add((d, sid))
                lines.append(f"  {_mid(d)} --> {_mid(sid)}")

    # BE -> FE gate edges (the direct "must be done before this FE story can start" edges).
    for sid, fe_id in sorted(set(fe_edges), key=lambda e: (e[1], e[0])):
        lines.append(f"  {_mid(sid)} ==>|gates| {_mid(fe_id)}")

    lines.append("```")
    return "\n".join(lines)


def generate_domain(domain: str) -> None:
    src_dir = get_domain_dir(domain)
    stories = [s for s in parse_stories(src_dir / "be-04-stories.md") if s.get("phase") != "S"]
    if not stories:
        print(f"  ! {domain}: no stories found, skipping")
        return
    fe_stories = parse_fe_stories()

    label = DOMAIN_LABELS.get(domain, domain.title())
    story_link = f"../../../output/analysis/{domain}/be-04-stories.md"

    L = [
        f"# {label} — Story Dependency Graphs",
        "",
        f"> Generated {TODAY} from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via "
        "`generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text "
        f"(Current Behaviour, Target implementation, Acceptance Criteria): [{domain}/be-04-stories.md]({story_link}).",
        "",
        "---",
        "",
        "## Graph A — Backend Story Dependency (build order)",
        "",
        "For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped "
        "into swimlanes by implementation step — everything in one step can be built in parallel once every "
        "step before it is done. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a "
        "cross-subgraph block) — read-only context, not something the scheduler enforces.",
        "",
        build_be_graph(domain, stories),
        "",
        "---",
        "",
        "## Graph B — Frontend Readiness (what must ship before FE can start)",
        "",
        "For the frontend engineer or PO checking whether backend is far enough along: the **bold arrows** "
        "are the actual gate — a frontend story cannot start until every backend story pointing at it (and, "
        "transitively, everything upstream of those) has shipped.",
        "",
        build_fe_graph(domain, stories, fe_stories),
        "",
        "---",
        f"*Story dependency graphs · {domain} · generated {TODAY}.*",
    ]

    out_dir = FINAL / "summary" / domain
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"story-dependency-graph-{domain}.md"
    out_path.write_text("\n".join(L), encoding="utf-8")
    print(f"  OK {out_path.relative_to(ROOT)}")


def main() -> None:
    targets = [a for a in sys.argv[1:] if not a.startswith("--")] or ALL_DOMAINS
    print(f"\n=== Story dependency graphs — {TODAY} ===\n")
    for domain in targets:
        if domain not in ALL_DOMAINS:
            print(f"  UNKNOWN domain '{domain}' — skipping")
            continue
        try:
            generate_domain(domain)
        except Exception as e:
            print(f"  FAIL {domain}: {type(e).__name__}: {e}")
    print("\nDone.\n")


if __name__ == "__main__":
    main()
