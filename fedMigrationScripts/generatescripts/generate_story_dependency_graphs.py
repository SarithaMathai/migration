#!/usr/bin/env python3
"""
Per-domain story dependency graphs — two mermaid diagrams, one file per domain.

Both graphs are rendered from data other generators already compute (compute_implementation_order's
DAG, fe-08's Depends-on lines) — nothing here invents new dependency facts, it only visualizes what
be-04-stories.md / fe-08-frontend-stories.md already declare. Regenerate whenever those change.

  Graph A — BE Story Dependency (intra-domain build order)
    ONE box per phase (B/C/D/E/F/G/H), not one node per story — a story-level diagram stops being
    readable past a couple dozen nodes, and phase is already a meaningful, size-bounded grouping
    regardless of domain size. Cross-phase arrows are labeled with the story-level dependency
    count they represent; 🔬/⛔ markers flag a phase containing a gated story. A companion table
    (also generated, not hand-maintained) lists every story's phase, direct Depends-on, and gate,
    so the story-level fact isn't lost, just moved out of the diagram.
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


def _phase_dep_counts(stories: list[dict], by_short: dict) -> dict[str, dict[str, int]]:
    """{from_phase: {to_phase: edge_count}} — every direct Depends-on edge, rolled up from
    story-level to phase-level so Graph A can draw one arrow per phase pair (labeled with
    how many story-level edges it represents) instead of one arrow per story pair."""
    counts: dict[str, dict[str, int]] = {}
    for s in stories:
        sid = _short_id(s["id"])
        if sid not in by_short:
            continue
        to_phase = s["phase"]
        for m in re.finditer(r"\b(?:[A-Z]+-BE-)?([A-H]-\d+(?:-\d+)?)\b", s.get("depends", "") or ""):
            dep = m.group(1)
            if dep in by_short and dep != sid:
                from_phase = by_short[dep]["phase"]
                if from_phase != to_phase:
                    counts.setdefault(from_phase, {})
                    counts[from_phase][to_phase] = counts[from_phase].get(to_phase, 0) + 1
    return counts


def build_be_graph(domain: str, stories: list[dict]) -> tuple[str, str]:
    """Graph A — BE Story Dependency. ONE box per phase (B/C/D/E/F/G/H), not one box per story —
    a story-level diagram is unreadable past ~15-20 nodes, and a phase already groups stories
    into a meaningful, bounded-size unit (reads vs mutations vs field resolvers) regardless of
    domain size. Cross-phase arrows are labeled with how many story-level dependencies they
    represent. Gate icons (🔬 spike, ⛔ cross-subgraph block) show on a phase box if ANY story in
    that phase carries one — the specific story is named in the table returned alongside the
    diagram, not spelled out in the diagram itself.
    Returns (mermaid_block, detail_table_markdown)."""
    _waves, gates, _crit = compute_implementation_order(stories)
    by_short = {_short_id(s["id"]): s for s in stories}
    by_phase: dict[str, list] = {}
    for s in stories:
        by_phase.setdefault(s["phase"], []).append(s)

    # Which phases contain a gated story, and which gate(s) — for the box marker + table.
    phase_gates: dict[str, set] = {}
    for sid, gate_list in gates.items():
        if sid in by_short:
            phase_gates.setdefault(by_short[sid]["phase"], set()).update(gate_list)

    phase_counts = _phase_dep_counts(stories, by_short)

    lines = ["```mermaid", "flowchart TD"]
    for phase in PHASE_SEQ:
        group = by_phase.get(phase)
        if not group:
            continue
        icon = PHASE_ICONS.get(phase, "")
        name = PHASE_NAMES.get(phase, phase)
        n = len(group)
        gate_marker = " 🔬" if any(g.startswith("🔬") for g in phase_gates.get(phase, ())) else ""
        gate_marker += " ⛔" if any(g.startswith("⛔") for g in phase_gates.get(phase, ())) else ""
        label = f"{icon} Phase {phase}<br/>{name}<br/>({n} {'story' if n == 1 else 'stories'}){gate_marker}"
        lines.append(f'  PH{phase}["{label}"]')

    for from_phase, targets in phase_counts.items():
        for to_phase, n in targets.items():
            plural = "dep" if n == 1 else "deps"
            lines.append(f"  PH{from_phase} -->|{n} {plural}| PH{to_phase}")

    lines.append("```")
    diagram = "\n".join(lines)

    # Detail table — every story, its phase, and its direct Depends-on, so the story-level fact
    # that used to be in the diagram is still in this file, just not cluttering the picture.
    table = ["| Story | Phase | Depends on | Gate |", "|---|---|---|---|"]
    for phase in PHASE_SEQ:
        for s in sorted(by_phase.get(phase, []), key=lambda s: _short_id(s["id"])):
            sid = _short_id(s["id"])
            dep_ids = sorted({m.group(1) for m in re.finditer(
                r"\b(?:[A-Z]+-BE-)?([A-H]-\d+(?:-\d+)?)\b", s.get("depends", "") or "")
                if m.group(1) in by_short and m.group(1) != sid})
            deps_cell = ", ".join(f"`{d}`" for d in dep_ids) or "—"
            gate_cell = ", ".join(sorted(gates.get(sid, []))) or "—"
            title = re.sub(r"`", "", s["title"]).strip()
            table.append(f"| `{sid}` — {title} | {phase} | {deps_cell} | {gate_cell} |")
    return diagram, "\n".join(table)


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
    be_diagram, be_table = build_be_graph(domain, stories)

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
        "One box per **phase** (reads, search, mutations, complex ops, federation, field resolvers, "
        "entity resolution) — not one box per story, which stops being readable past a couple dozen "
        "stories. An arrow between two phase boxes means at least one story in the target phase "
        "directly depends on a story in the source phase; the label is how many story-level "
        "dependencies that represents. 🔬/⛔ on a box means at least one story in that phase is "
        "spike- or cross-subgraph-gated — see the table below for exactly which one.",
        "",
        be_diagram,
        "",
        "**Story-level detail** (every story in this domain, its phase, its direct `Depends on:`, and "
        "any gate):",
        "",
        be_table,
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
