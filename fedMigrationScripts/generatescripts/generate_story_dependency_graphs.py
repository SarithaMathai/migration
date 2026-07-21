#!/usr/bin/env python3
"""
Per-domain frontend-readiness dependency graph — one file per domain.

Rendered from data other generators already compute (fe-08's Depends-on lines) — nothing here
invents new dependency facts, it only visualizes what fe-08-frontend-stories.md already declares.
Regenerate whenever that changes.

  FE Readiness (client story dependency)
    One small diagram PER FE story, not one combined diagram for the whole domain — showing only
    that FE story's directly-named BE dependencies, no transitive BE->BE upstream walk (walking
    the full upstream chain makes the shared module-init story fan out to nearly every node,
    producing an illegible crisscross). Audience: FE engineer or PO checking "is backend far
    enough along to start this specific FE story."

    Pure backend build-order sequencing (which BE story unlocks which within a domain) lives in
    02-project-plan.md / finalArtifacts/00-sequencing.md — deliberately not duplicated here.

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

from generate_breakdown import parse_stories, get_domain_dir, _short_id, PHASE_SEQ
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


def build_fe_graph_section(domain: str, be_stories: list[dict], fe_stories: list[dict]) -> str:
    """FE Readiness, rendered as one small diagram PER FE story rather than one big diagram for
    the whole domain. Each diagram shows only that FE story's DIRECTLY named Depends-on BE
    stories — no transitive BE->BE upstream walk. Walking the full upstream chain makes B-01
    (or whichever story nearly everything in a domain eventually depends on) fan out to almost
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
    sequencing_link = "../../00-sequencing.md"

    L = [
        f"# {label} — Frontend Readiness",
        "",
        f"> Generated {TODAY} from `fe-08-frontend-stories.md` — regenerate via "
        "`generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text "
        f"(Current Behaviour, Target implementation, Acceptance Criteria): [{domain}/be-04-stories.md]({story_link}). "
        f"Backend build-order sequencing: [00-sequencing.md]({sequencing_link}).",
        "",
        "---",
        "",
        "## What must ship before FE can start",
        "",
        "For the frontend engineer or PO checking whether backend is far enough along: **one small diagram "
        "per frontend story**, showing only the backend stories it directly depends on. A frontend story "
        "cannot start until every backend story pointing at it has shipped.",
        "",
        build_fe_graph_section(domain, stories, fe_stories),
        "",
        "---",
        f"*Story dependency graph · {domain} · generated {TODAY}.*",
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
