#!/usr/bin/env python3
"""
Generate one consolidated table of every cross-domain `Blocked by:` dependency.

Each domain's be-04-stories.md already carries `**Blocked by:**` on the stories that
need it — but that fact is scattered across 8 files, so there is no single place to see
"what's waiting on what, across domains" at a glance. This script is read-only over the
domain source files; it doesn't invent any new dependency data, it only collects what
`**Blocked by:**` already declares and renders it as one table.

Two categories of Blocked-by target, both included:
  - a shared-infrastructure story in another domain (e.g. "product (`PRODUCT-BE-E-00`,
    the shared `WriteSaga` module)") — the target is a concrete story id, resolvable.
  - a not-yet-live subgraph (e.g. "attachment domain (⛔ cross-subgraph — does not ship
    until `plm-attachment` is live)") — the target is a domain/subgraph name, not a story
    id; these are phase-1/later-phase boundary gates, not sequencing bugs.

Output: output/analysis/program/cross-domain-dependencies.md

Run:
    python fedMigrationScripts/generatescripts/generate_cross_domain_deps.py
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ANALYSIS = ROOT / "output" / "analysis"
OUT = ANALYSIS / "program" / "cross-domain-dependencies.md"

ALL_DOMAINS = [
    "bom", "claims", "impression", "measurement",
    "packaging", "product", "productDetails", "watchlist",
]

STORY_HEADER_RE = re.compile(r"^### ([A-Z][A-Za-z0-9]*-BE-[A-Za-z0-9-]+) · (.+)$", re.MULTILINE)
BLOCKED_RE = re.compile(r"\*\*Blocked by:\*\*\s*([^\n]+)")

# A target story id, if the Blocked-by text names one in backticks — e.g.
# "product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module)" -> PRODUCT-BE-E-00.
# Takes the FIRST backtick-quoted token that looks like a story id (contains "-BE-").
TARGET_ID_RE = re.compile(r"`([A-Z][A-Za-z0-9]*-BE-[A-Za-z0-9-]+)`")


def domain_dir(domain: str) -> Path:
    return ANALYSIS / domain


def find_blocked_stories(domain: str) -> list[dict]:
    path = domain_dir(domain) / "be-04-stories.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    matches = list(STORY_HEADER_RE.finditer(text))
    out = []
    for i, m in enumerate(matches):
        sid, title = m.group(1), m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        blk = BLOCKED_RE.search(body)
        if not blk:
            continue
        raw = blk.group(1).strip()
        target_id_m = TARGET_ID_RE.search(raw)
        target_id = target_id_m.group(1) if target_id_m else None
        out.append({
            "id": sid, "title": title, "domain": domain,
            "raw": raw, "target_id": target_id,
        })
    return out


def target_exists(target_id: str, all_by_domain: dict[str, set[str]]) -> bool:
    for ids in all_by_domain.values():
        if target_id in ids:
            return True
    return False


def build_table() -> str:
    all_by_domain: dict[str, set[str]] = {}
    for dom in ALL_DOMAINS:
        path = domain_dir(dom) / "be-04-stories.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        all_by_domain[dom] = {m.group(1) for m in STORY_HEADER_RE.finditer(text)}

    infra_rows = []    # blocked on a concrete story id in another domain
    subgraph_rows = [] # blocked on a not-yet-live subgraph/domain (no resolvable story id)
    dangling = []      # names a story id that does not exist anywhere

    for dom in ALL_DOMAINS:
        for row in find_blocked_stories(dom):
            if row["target_id"]:
                if target_exists(row["target_id"], all_by_domain):
                    infra_rows.append(row)
                else:
                    dangling.append(row)
            else:
                subgraph_rows.append(row)

    today = __import__("datetime").date.today().isoformat()
    L = [
        "# Cross-Domain Dependencies",
        "",
        f"> **Generated:** {today} · by `generate_cross_domain_deps.py` — collects every "
        "`**Blocked by:**` line already declared in each domain's `be-04-stories.md`; adds "
        "nothing new. Regenerate after any story's `Blocked by:` field changes.",
        "> **`Depends on:` vs `Blocked by:`** — `Depends on:` is an intra-domain build-order "
        "edge the wave scheduler enforces (see each domain's \"Recommended Implementation "
        "Order\"). `Blocked by:` is documentation only: nothing in the generator pipeline "
        "currently treats it as a hard scheduling gate — it's the human-readable record of a "
        "cross-domain or cross-subgraph constraint the *program plan* (sprint sequencing, "
        "not the wave scheduler) has to honor by hand.",
        "",
        "---",
        "",
        "## Blocked on shared infrastructure in another domain",
        "",
        "| Blocked story | Domain | Waits on | Target story |",
        "|---|---|---|---|",
    ]
    for r in sorted(infra_rows, key=lambda r: (r["target_id"], r["domain"], r["id"])):
        L.append(f"| `{r['id']}` — {r['title']} | {r['domain']} | {r['raw']} | `{r['target_id']}` |")
    if not infra_rows:
        L.append("| — | — | — | — |")

    L += [
        "",
        "---",
        "",
        "## Blocked on a not-yet-live subgraph (later-phase domain)",
        "",
        "| Blocked story | Domain | Waits on |",
        "|---|---|---|",
    ]
    for r in sorted(subgraph_rows, key=lambda r: (r["domain"], r["id"])):
        L.append(f"| `{r['id']}` — {r['title']} | {r['domain']} | {r['raw']} |")
    if not subgraph_rows:
        L.append("| — | — | — |")

    if dangling:
        L += [
            "",
            "---",
            "",
            "## ⚠ Dangling references (target story id not found anywhere)",
            "",
            "| Blocked story | Domain | Claims to wait on | Target id (not found) |",
            "|---|---|---|---|",
        ]
        for r in dangling:
            L.append(f"| `{r['id']}` | {r['domain']} | {r['raw']} | `{r['target_id']}` |")

    L += [
        "",
        "---",
        f"*{len(infra_rows)} infrastructure gate(s) · {len(subgraph_rows)} later-phase-subgraph "
        f"gate(s){f' · {len(dangling)} dangling reference(s) — FIX BEFORE SHIP' if dangling else ''}.*",
    ]
    return "\n".join(L)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    content = build_table()
    OUT.write_text(content, encoding="utf-8")
    print(f"  OK {OUT.relative_to(ROOT)} ({len(content):,} chars)")


if __name__ == "__main__":
    main()
