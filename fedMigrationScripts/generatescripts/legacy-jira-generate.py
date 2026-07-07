#!/usr/bin/env python3
"""
Generate Jira-ready artifacts (CSV bulk-import + per-issue Markdown) from the
per-domain migration stories.

It is DOMAIN-AGNOSTIC: it auto-discovers every `finalOutput/<domain>/04-stories-index.yaml`,
so when a new domain (claims, productDetails, watchlist, search, ...) is analyzed and its
folder appears, just re-run this script — no code change needed.

    python finalOutput/jira/generate.py

Outputs (into finalOutput/jira/):
  - <domain>.csv            one row per story (+ an Epic row), per domain
  - all-stories.csv         every domain concatenated (epics + stories)
  - <domain>-stories.md     one clean block per story, for pasting a single Jira issue

Story metadata comes from 04-stories-index.yaml (the authoritative story list).
The issue Description is pulled from the matching `### <ID>` block in 04-stories.md;
if a story has no dedicated block (e.g. a bundled F01..F08 section), the summary is used
with a pointer to the bundled section.
"""
import csv
import re
import sys
from pathlib import Path

import yaml

# finalOutput/ is the parent of this script's folder (finalOutput/jira/).
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "jira"

# Preferred domain ordering for the combined file (others appended alphabetically).
DOMAIN_ORDER = ["impression", "measurement", "bom", "product"]

# Complexity -> T-shirt size. Engineers estimate size after reading the story.
# See jira/README.md §A for the T-shirt index (size → day-range).
TSHIRT = {"Low": "XS", "Medium": "M", "High": "L", "Very High": "XL"}

CSV_HEADER = [
    "Issue Type", "Story ID", "Summary", "Epic Name", "Epic Link",
    "Phase", "T-shirt size",
    "Labels", "Labels", "Labels", "Parent Link", "Depends On", "Description",
]

STORY_ID_RE = re.compile(r"^###\s+(SPARK-[A-Z]+-[A-Za-z0-9]+)", re.MULTILINE)
YAML_FENCE_RE = re.compile(r"```ya?ml.*?```", re.DOTALL)
TYPE_RE = re.compile(r"\btype:\s*([a-z][a-z-]*)")


def parse_story_md(md_path: Path):
    """Return {story_id: {"desc": str, "type": str|None}} from a 04-stories.md file."""
    if not md_path.exists():
        return {}
    text = md_path.read_text(encoding="utf-8")
    matches = list(STORY_ID_RE.finditer(text))
    out = {}
    for i, m in enumerate(matches):
        sid = m.group(1)
        # start after the rest of the header line (drop the "· <title>" remainder)
        nl = text.find("\n", m.end())
        start = nl + 1 if nl != -1 else m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        # capture `type:` from the leading yaml front-matter before stripping it
        ftype = None
        fence = YAML_FENCE_RE.search(block)
        if fence:
            tm = TYPE_RE.search(fence.group(0))
            if tm:
                ftype = tm.group(1)
        body = YAML_FENCE_RE.sub("", block)
        body = body.strip().strip("-").strip()
        out.setdefault(sid, {"desc": body, "type": ftype})
    return out


def type_label(story, md_entry):
    if md_entry and md_entry.get("type"):
        return md_entry["type"]
    cat = (story.get("category") or "").upper()
    return {
        "CAT-1": "schema", "CAT-3": "service", "CAT-4": "federation", "CAT-5": "tests",
    }.get(cat, "story")


def deps_str(story):
    return ", ".join(story.get("depends_on") or [])


def load_domain(index_path: Path):
    data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    domain = data.get("domain") or index_path.parent.name
    epic = data.get("epic") or f"{domain} migration"
    labels_common = data.get("labels_common") or ["dgs-migration", domain]
    stories = data.get("stories") or []
    md = parse_story_md(index_path.parent / "04-stories.md")
    return {"domain": domain, "epic": epic, "labels_common": labels_common,
            "stories": stories, "md": md}


def domain_rows(dm):
    """Yield CSV rows (list) for one domain: an Epic row then one row per story.

    Handles parent/substory structure:
    - Parent stories are emitted as regular Stories (milestone marker, no size).
    - Substories are emitted with Parent Link set.
    """
    domain, epic, lc = dm["domain"], dm["epic"], dm["labels_common"]
    l1 = lc[0] if len(lc) > 0 else "dgs-migration"
    l2 = lc[1] if len(lc) > 1 else domain
    rows = []
    rows.append(["Epic", "", epic, epic, "", "", "", "", l1, l2, "epic", "", "",
                 f"Epic for the {domain} domain migration to the plm-product DGS."])
    for s in dm["stories"]:
        sid = s["id"]
        summary = s.get("summary", sid)
        md_entry = dm["md"].get(sid)
        desc = md_entry["desc"] if md_entry else (
            f"{summary}\n\n(Full detail is in finalOutput/{domain}/04-stories.md — "
            f"phase {s.get('phase','?')} section.)")

        # Determine if this is a parent or substory
        parent_id = s.get("parent")
        substories = s.get("substories", [])

        if parent_id:
            # Substory: include Parent Link
            rows.append([
                "Sub-task", sid, f"{sid} · {summary}", "", epic,
                s.get("phase", ""), TSHIRT.get(s.get("complexity"), "?"),
                l1, l2, type_label(s, md_entry), parent_id, deps_str(s), desc,
            ])
        elif substories:
            # Parent: no T-shirt size (milestone), no depends (deps are on substories)
            rows.append([
                "Story", sid, f"{sid} · {summary} [MILESTONE]", "", epic,
                s.get("phase", ""), "",  # Empty T-shirt size for parent
                l1, l2, "epic", "",  # No Parent Link, "epic" label
                f"Parent story (milestone). Breakdown: {', '.join(substories)}. " + desc,
            ])
        else:
            # Regular story (no parent, no substories)
            rows.append([
                "Story", sid, f"{sid} · {summary}", "", epic,
                s.get("phase", ""), TSHIRT.get(s.get("complexity"), "?"),
                l1, l2, type_label(s, md_entry), "", deps_str(s), desc,
            ])
    return rows


def write_csv(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(CSV_HEADER)
        w.writerows(rows)


def write_stories_md(path: Path, dm):
    domain, epic, lc = dm["domain"], dm["epic"], dm["labels_common"]
    l1 = lc[0] if len(lc) > 0 else "dgs-migration"
    l2 = lc[1] if len(lc) > 1 else domain
    lines = [f"# {domain} — Jira stories (paste one block per issue)",
             "",
             # Tag line — keeps the artifact identifiable (mirrors the Confluence tag scheme).
             # See jira/README.md §D. `dgs-migration` is the shared program label across Jira + Confluence.
             (f"> 🏷️ **Jira labels (on every story below):** `{l1}` · `{l2}` · `<type>`  —  "
              f"**Epic:** {domain} → DGS migration  ·  **Bulk import:** `{domain}.csv`"),
             "",
             f"> **Epic:** {epic}  ·  **Labels:** `{l1}`, `{l2}`, `<type>`",
             "> Create the Epic first, then paste each block below as a new Story's description.",
             "> Estimate T-shirt size after reading the story (confirm in refinement). See "
             "[README.md](./README.md) for the T-shirt index.",
             ""]
    for s in dm["stories"]:
        sid = s["id"]
        summary = s.get("summary", sid)
        md_entry = dm["md"].get(sid)
        desc = md_entry["desc"] if md_entry else (
            f"{summary}\n\n_(Full detail bundled in "
            f"../{domain}/04-stories.md — phase {s.get('phase','?')} section.)_")
        deps = deps_str(s) or "—"
        lines += [
            f"## {sid} · {summary}",
            (f"**Type:** Story  ·  **Phase:** {s.get('phase','')}  ·  "
             f"**T-shirt size:** {TSHIRT.get(s.get('complexity'),'?')}  ·  "
             f"**Depends on:** {deps}"),
            f"**Labels:** `{l1}`, `{l2}`, `{type_label(s, md_entry)}`",
            "",
            desc,
            "",
            "---",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index_paths = sorted(ROOT.glob("*/04-stories-index.yaml"))
    if not index_paths:
        print("No */04-stories-index.yaml found under", ROOT)
        return 1

    domains = [load_domain(p) for p in index_paths]
    order = {d: i for i, d in enumerate(DOMAIN_ORDER)}
    domains.sort(key=lambda dm: (order.get(dm["domain"], len(DOMAIN_ORDER)), dm["domain"]))

    all_rows = []
    total_stories = 0
    for dm in domains:
        rows = domain_rows(dm)
        write_csv(OUT / f"{dm['domain']}.csv", rows)
        write_stories_md(OUT / f"{dm['domain']}-stories.md", dm)
        all_rows.extend(rows)
        n = len(dm["stories"])
        total_stories += n
        print(f"  {dm['domain']:14s} epic + {n:3d} stories")
    write_csv(OUT / "all-stories.csv", all_rows)

    print(f"\nDomains: {len(domains)}  ·  Stories: {total_stories}  ·  "
          f"all-stories.csv rows: {len(all_rows)} ({len(domains)} epics + {total_stories} stories)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
