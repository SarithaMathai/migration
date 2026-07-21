#!/usr/bin/env python3
"""
Per-domain story dependency graphs — two mermaid diagrams, one file per domain.

Both graphs are rendered from data other generators already compute (compute_implementation_order's
DAG, fe-08's Depends-on lines) — nothing here invents new dependency facts, it only visualizes what
be-04-stories.md / fe-08-frontend-stories.md already declare. Regenerate whenever those change.

  Graph A — BE Story Dependency (intra-domain build order)
    Nodes: this domain's BE-* stories only, swimlaned by PHASE (B/C/D/E/F/G/H) — not by raw DAG
    depth, which collapses to "step 1 = the module-init scaffold, step 2 = almost every other
    story" for any domain where most stories only depend on that one scaffold, rendering as an
    unreadable wall of 40+ nodes in one box. Edges: direct `Depends on:` only.
    Audience: the backend engineer sequencing their own PRs.

  Graph B — FE Readiness (client story dependency)
    One small diagram PER FE story, not one combined diagram for the whole domain — showing only
    that FE story's directly-named BE dependencies, no transitive BE->BE upstream walk (that
    chain is Graph A's job; repeating it here made the shared module-init story fan out to nearly
    every node, producing an illegible crisscross). Audience: FE engineer or PO checking "is
    backend far enough along to start this specific FE story."

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
    """Graph A — BE Story Dependency. Swimlaned by PHASE (B/C/D/E/F/G/H), not raw DAG depth —
    a depth-based grouping collapses to 'step 1 = the module-init scaffold, step 2 = nearly
    every other story' for any domain where most stories only depend on that one scaffold
    story, which renders as one unreadable wall of 40+ nodes. Phase is already meaningful
    (reads vs mutations vs field resolvers) and keeps each swimlane to the size of one phase."""
    _waves, gates, _crit = compute_implementation_order(stories)
    by_short = {_short_id(s["id"]): s for s in stories}
    by_phase: dict[str, list] = {}
    for s in stories:
        by_phase.setdefault(s["phase"], []).append(s)

    lines = ["```mermaid", "flowchart TD"]
    for phase in PHASE_SEQ:
        group = by_phase.get(phase)
        if not group:
            continue
        icon = PHASE_ICONS.get(phase, "")
        name = PHASE_NAMES.get(phase, phase)
        lines.append(f'  subgraph PH{phase}["{icon} Phase {phase} — {name}"]')
        for s in sorted(group, key=lambda s: _short_id(s["id"])):
            sid = _short_id(s["id"])
            lines.append(f"    {_mid(sid)}{_label(sid, s['title'])}")
        lines.append("  end")

    # Edges — direct Depends-on only (no transitive walk); this is what actually shows a reader
    # which specific story unlocks which, without an upstream-chain fan-out from the scaffold story.
    seen_edges = set()
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


def build_fe_graph_section(domain: str, be_stories: list[dict], fe_stories: list[dict]) -> str:
    """Graph B — FE Readiness, rendered as one small diagram PER FE story rather than one big
    diagram for the whole domain. Each diagram shows only that FE story's DIRECTLY named
    Depends-on BE stories — no transitive BE->BE upstream walk. The upstream chain behind any
    one of those BE stories is Graph A's job; repeating it here (as the previous version did)
    made B-01 — which nearly everything in a domain eventually depends on — fan out to almost
    every node, which is exactly the crisscross this format is meant to avoid.
    Returns a markdown string: one '### <FE-ID>' heading + one small mermaid diagram each."""
    by_short = {_short_id(s["id"]): s for s in be_stories}
    dom_fe = [f for f in fe_stories
              if domain_key_from_token(f["id"].rsplit("-FE-", 1)[0]) == domain]
    if not dom_fe:
        return "_No frontend stories recorded for this domain in fe-08-frontend-stories.md._"

    sections = []
    for f in sorted(dom_fe, key=lambda f: f["id"]):
        gate_ids = []
        for full_dep in f["depends"]:
            m = re.search(r"-BE-([A-H]-\d+(?:-\d+)?)$", full_dep)
            if m and m.group(1) in by_short and m.group(1) not in gate_ids:
                gate_ids.append(m.group(1))
        title = f["title"].replace('"', "'")
        lines = [f"### {f['id']} · {title}", "", "```mermaid", "flowchart LR"]
        if not gate_ids:
            lines.append(f'  {_mid(f["id"])}["{f["id"]}<br/>no backend gate — ready to start"]')
        else:
            for sid in sorted(gate_ids, key=lambda k: (PHASE_SEQ.find(k[0]) if k[0] in PHASE_SEQ else 99, k)):
                s = by_short[sid]
                lines.append(f"  {_mid(sid)}{_label(sid, s['title'], max_len=28)}")
            lines.append(f'  {_mid(f["id"])}(["{f["id"]}"])')
            for sid in gate_ids:
                lines.append(f"  {_mid(sid)} ==> {_mid(f['id'])}")
        lines.append("```")
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


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
        "into swimlanes by **phase** (reads, then search, then mutations, then complex/federation/field-"
        "resolver work) — arrows show only the direct `Depends on:` edges. A dashed arrow from a diamond is "
        "a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the "
        "scheduler enforces.",
        "",
        build_be_graph(domain, stories),
        "",
        "---",
        "",
        "## Graph B — Frontend Readiness (what must ship before FE can start)",
        "",
        "For the frontend engineer or PO checking whether backend is far enough along: **one small diagram "
        "per frontend story**, showing only the backend stories it directly depends on. (Any dependency "
        "*those* backend stories have on each other is Graph A's job, not repeated here — that's what kept "
        "the old single combined diagram unreadable.) A frontend story cannot start until every backend "
        "story pointing at it has shipped.",
        "",
        build_fe_graph_section(domain, stories, fe_stories),
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
