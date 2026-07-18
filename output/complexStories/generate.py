#!/usr/bin/env python3
"""
Generate each complex case's <case>.csv from its 01-stories.md.

Per fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md: a complex case's sub-task
breakdown is imported into Jira SEPARATELY from the domain CSVs, nested under the case's
home-stub story — so these rows never double-count against the 337-story program total
(all-stories.csv / {domain}.csv already carry the same story ids as first-class rows;
this file's job is only to group and re-tag that subset, once per case, for the
sub-task import).

Source of truth: each output/complexStories/<case>/01-stories.md — its own markdown
links (`../../analysis/{domain}/be-04-stories.md#anchor`) are parsed to discover which
story ids belong to that case. This script does not decide case membership; it only
reads what 01-stories.md already declares. Full story content (Current Behaviour,
Target, Acceptance Criteria, Test Cases) is pulled from each domain's real
be-04-stories.md via generate_jira.py's parse_stories() — never duplicated by hand here.

Output: output/complexStories/<case>/<case>.csv (Issue Type "Sub-task", Parent Link =
the case's home stub story id, read from 00-overview.md's "Home stub"/"Stub story" line).

Run:
    python output/complexStories/generate.py              # all cases
    python output/complexStories/generate.py techpack      # one case
"""

import csv
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # output/complexStories/
ROOT = HERE.parent.parent                        # repo root
ANALYSIS = ROOT / "output" / "analysis"
GENSCRIPTS = ROOT / "fedMigrationScripts" / "generatescripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, GENSCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
    spec.loader.exec_module(mod)                          # type: ignore[union-attr]
    return mod


jira_mod = _load("generate_jira")

# Every complex case folder with a 01-stories.md — add a new case here once its folder exists.
ALL_CASES = [
    "techpack",
    "attachments-enrichment",
    "components-and-counts-rollups",
    "cross-domain-association",
    "non-atomic-write-saga",
    "notRemovable-undroppable-partners",
    "partner-drop-undrop-write",
    "polymorphic-type-resolution",
]

# 01-stories.md links look like: ../../analysis/{domain}/be-04-stories.md#{anchor}
LINK_RE = re.compile(r"\[`([A-Z][A-Z0-9]*-BE-[A-Za-z0-9-]+)`\]\(\.\./\.\./analysis/(\w+)/be-04-stories\.md#")

HOME_STUB_RE = re.compile(r"\*\*(?:Home stub|Stub stor(?:y|ies)):?\*\*\s*`?([A-Z][A-Z0-9]*-BE-[A-Za-z0-9/-]+)`?")

HEADERS = [
    "Issue Type", "Story ID", "Summary", "Epic Name", "Epic Link",
    "Phase", "T-shirt size",
    "Labels", "Labels", "Labels",
    "Parent Link", "Depends On", "Status", "Description",
]


def case_dir(case: str) -> Path:
    return HERE / case


def discover_story_refs(case: str) -> dict[str, list[str]]:
    """{domain: [story_id, ...]} — every story id 01-stories.md links to, grouped by
    the domain whose be-04-stories.md it lives in."""
    path = case_dir(case) / "01-stories.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    by_domain: dict[str, list[str]] = {}
    for story_id, domain in LINK_RE.findall(text):
        by_domain.setdefault(domain, [])
        if story_id not in by_domain[domain]:
            by_domain[domain].append(story_id)
    return by_domain


def home_stubs(case: str) -> list[str]:
    """Every home-stub story id 00-overview.md names for this case, in order. Most cases
    declare exactly one (e.g. techpack: PRODUCT-BE-E-03) — some, like non-atomic-write-saga,
    legitimately declare one stub PER DOMAIN (BOM-BE-E-01, MST-BE-E-01, PKG-BE-E-01, ...),
    since each domain's own multi-step write adopts the shared module independently. Returns
    [] if 00-overview.md names no stub at all (e.g. cross-domain-association, whose affected
    stories — D-01/D-02/D-04 — already exist as first-class domain stories; nothing nests
    under another)."""
    path = case_dir(case) / "00-overview.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    m = HOME_STUB_RE.search(text)
    if not m:
        return []
    # "BOM-BE-E-01`, `MST-BE-E-01`, ... `SAMPLE-BE-E-01/E-02` (later phase), `PRODUCT-BE-E-02`"
    # — re-scan the captured group's own line for every backtick-quoted story id, since a
    # single-stub case's HOME_STUB_RE match already IS the id, but a multi-stub case's match
    # is only the first of several the same line lists.
    line_start = text.rfind("\n", 0, m.start()) + 1
    line_end = text.find("\n", m.end())
    line = text[line_start:(line_end if line_end != -1 else len(text))]
    ids = re.findall(r"`([A-Z][A-Z0-9]*-BE-[A-Za-z0-9-]+(?:/[A-Za-z0-9-]+)?)`", line)
    # Expand "SAMPLE-BE-E-01/E-02" shorthand into ["SAMPLE-BE-E-01", "SAMPLE-BE-E-02"] so it
    # matches real story ids elsewhere — same convention generate_jira.py already uses.
    # `rest` ("E-02") already carries its own phase letter — prepend only the "SAMPLE-BE-"
    # domain prefix, not the base id's phase letter too (that would double it up).
    expanded: list[str] = []
    for tok in ids:
        if "/" in tok:
            base, rest = tok.split("/", 1)
            prefix = re.match(r"(.+-BE-)[A-Z]-\d+", base)
            expanded.append(base)
            expanded.append(f"{prefix.group(1)}{rest}" if prefix else rest)
        else:
            expanded.append(tok)
    return expanded or ([m.group(1).strip().strip("`")] if m.group(1) else [])


def stub_for_domain(stubs: list[str], domain: str, domain_ids: set[str]) -> str:
    """Which of this case's home stubs (if any) actually belongs to `domain` — matched by
    checking which stub id is a real story in that domain's own be-04-stories.md. Falls
    back to the first stub if none matches a specific domain (single-stub cases) or to ''
    if the case has no stub at all."""
    for stub in stubs:
        if stub in domain_ids:
            return stub
    return stubs[0] if stubs else ""


def build_case_rows(case: str) -> list[list]:
    by_domain = discover_story_refs(case)
    stubs = home_stubs(case)
    rows: list[list] = []
    for domain, ids in by_domain.items():
        try:
            src_dir = jira_mod.get_domain_dir(domain)
        except FileNotFoundError:
            print(f"  SKIP {case}: domain '{domain}' has no be-04-stories.md")
            continue
        stories = jira_mod.parse_stories(src_dir / "be-04-stories.md")
        by_id = {s["id"]: s for s in stories}
        tag = jira_mod.DOMAIN_TAG.get(domain, domain)
        stub = stub_for_domain(stubs, domain, set(by_id))
        for sid in ids:
            s = by_id.get(sid)
            if s is None:
                print(f"  WARN {case}: {sid} not found in {domain}/be-04-stories.md (renamed since 01-stories.md was written?)")
                continue
            size = jira_mod.SIZE_MAP.get(s["complexity"], "M")
            desc = s["description"]
            src = jira_mod.source_line(domain, s["id"], s["title"]) if hasattr(jira_mod, "source_line") else ""
            if src:
                desc = (desc + "\n\n" + src) if desc else src
            case_note = f"*Complex case:* {case} — see complexStories/{case}/00-overview.md and 01-adr-*.md"
            desc = (case_note + "\n\n" + desc) if desc else case_note
            rows.append([
                "Sub-task",
                s["id"],
                f"({tag}) {s['title'].replace(chr(96), '')} [{s['id']}]",
                "",
                "",                      # no Epic Link — nests under the case's home stub instead
                s["phase"],
                size,
                "dgs-migration", domain, "complex-case",
                stub,                    # Parent Link — the case's home stub
                jira_mod.dedupe_ids(jira_mod._strip_domain_spike_refs(s["depends"])),
                s["status"],
                desc,
            ])
    return rows


def write_csv(rows: list[list], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(rows)


def generate_case(case: str) -> int:
    rows = build_case_rows(case)
    out = case_dir(case) / f"{case}.csv"
    write_csv(rows, out)
    print(f"  OK {case}/{case}.csv ({len(rows)} sub-task rows)")
    return len(rows)


def generate_all(cases: list[str]) -> None:
    for case in cases:
        try:
            generate_case(case)
        except Exception as e:
            print(f"  FAIL {case}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    targets = [a for a in sys.argv[1:] if not a.startswith("--")]
    cases = targets if targets else ALL_CASES
    for c in cases:
        if c not in ALL_CASES:
            print(f"  SKIP '{c}' — no 01-stories.md registered in ALL_CASES")
            continue
    generate_all([c for c in cases if c in ALL_CASES])
