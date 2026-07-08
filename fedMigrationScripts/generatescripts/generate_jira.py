#!/usr/bin/env python3
"""
Generate clean Jira-import CSVs for every domain.

Rules applied:
- Source: output/initial-analysis/{domain}/ (updated, Phase A dissolved)
  Fallback: migration/finalOutput/{domain}/ (search only)
- Phase A stories are excluded (they are a one-time B01 checklist, not Jira tickets)
- Test cases included in Description only for High / Very High complexity stories
- AC and test text preserves inline code (backticks) and bold
- Output: migration/finalOutput/jira/{domain}.csv  + jira/all-stories.csv

Run:
    cd migration/finalOutput/oneStopDoc
    python generate_jira.py              # all domains
    python generate_jira.py impression   # specific domain(s)
"""

import csv
import re
import sys
from io import StringIO
from pathlib import Path

# ─── Path setup ──────────────────────────────────────────────────────────────
HERE          = Path(__file__).resolve().parent
REPO_ROOT     = HERE.parent.parent
UPDATED_SRC   = HERE.parent.parent / "output" / "initial-analysis"
FALLBACK_SRC  = HERE.parent.parent / "output" / "initial-analysis"
JIRA_OUT      = HERE.parent.parent / "output" / "jira"

# ─── Domain catalogue ─────────────────────────────────────────────────────────
# Phase 1 scope: the 8 domains in the first production wave. Remaining domains
# (attachment, discussion, sample, search, workspace) join in a later phase —
# add them back here to regenerate their artifacts.
ALL_DOMAINS = [
    "bom", "claims", "impression", "measurement",
    "packaging", "product", "productDetails", "watchlist",
]

DOMAIN_LABELS = {
    "attachment":     "Attachment",
    "bom":            "Bill of Materials (BOM)",
    "claims":         "Claims",
    "discussion":     "Discussion",
    "impression":     "Impression",
    "measurement":    "Measurement",
    "packaging":      "Packaging",
    "product":        "Product",
    "productDetails": "Product Details",
    "sample":         "Sample",
    "search":         "Search",
    "watchlist":      "Watchlist",
    "workspace":      "Workspace",
}

# Short, readable tag prefixed to every story Summary so a domain is identifiable
# under the single shared epic (e.g. "[BOM] SPARK-BOM-S01 · ...").
DOMAIN_TAG = {
    "attachment":     "Attachment",
    "bom":            "BOM",
    "claims":         "Claims",
    "discussion":     "Discussion",
    "impression":     "Impression",
    "measurement":    "Measurement",
    "packaging":      "Packaging",
    "product":        "Product",
    "productDetails": "Product Details",
    "sample":         "Sample",
    "search":         "Search",
    "watchlist":      "Watchlist",
    "workspace":      "Workspace",
}

# All stories/spikes across every domain hang off ONE epic.
GLOBAL_EPIC_NAME = "Federate BreakDown Product"
GLOBAL_EPIC_DESC = (
    "Umbrella epic for the spark-internal-graphql to Netflix DGS federated GraphQL "
    "migration. Holds the stories and spikes for the 8 phase-1 domains (Product, "
    "Impression, BOM, Measurement, Product Details, Packaging, Watchlist, Claims); "
    "each story summary is prefixed with its domain (e.g. [BOM], [Product])."
)

DGS_MAP = {
    "product":        "plm-product",
    "bom":            "plm-product",
    "measurement":    "plm-product",
    "packaging":      "plm-product",
    "impression":     "plm-product",
    "productDetails": "plm-product",
    "watchlist":      "plm-product",
    "workspace":      "plm-workspace",
    "sample":         "plm-sample",
    "discussion":     "plm-discussion",
    "attachment":     "plm-attachment",
    "search":         "plm-elastic-search",
    "claims":         "spark-claims",
}

SIZE_MAP = {
    "low":       "XS",
    "medium":    "M",
    "high":      "L",
    "very high": "XL",
}

PHASE_LABEL = {
    "A": "schema",
    "S": "spike",
    "B": "query",
    "C": "search",
    "D": "mutation",
    "E": "complex",
    "F": "field-resolver",
    "G": "field-resolver",
}
DEFAULT_STATUS = "To Do"

# ─── Story parser ─────────────────────────────────────────────────────────────
STORY_HEADER_RE = re.compile(
    r"^### (SPARK-[A-Z]+-([A-Za-z])(\d+)(?:-\d+)?) · (.+)$", re.MULTILINE
)
METADATA_INLINE_RE = re.compile(
    r"\*\*Type:\*\*\s*([^·\n]+).*?\*\*Complexity:\*\*\s*([^·\n]+)", re.DOTALL
)
PHASE_RE   = re.compile(r"\*\*Phase:\*\*\s*([A-Z])\b")
DEPENDS_RE = re.compile(r"\*\*Depends on:\*\*\s*([^\n*·]+)")
BLOCKED_RE = re.compile(r"\*\*Blocked by:\*\*\s*([^\n]+)")
STATUS_RE  = re.compile(r"\*\*Status:\*\*\s*([^\n*·]+)")


def dedupe_ids(raw: str) -> str:
    """Collapse a comma-separated dependency list to unique ids, preserving order."""
    if not raw:
        return raw
    seen: list[str] = []
    for part in raw.split(","):
        p = part.strip()
        if p and p not in seen:
            seen.append(p)
    return ", ".join(seen)


def get_domain_dir(domain: str) -> Path:
    for src in (FALLBACK_SRC / domain,):
        if (src / "04-stories.md").exists():
            return src
    raise FileNotFoundError(f"No 04-stories.md found for domain '{domain}'")


def extract_named_section(body: str, header: str) -> str:
    pattern = rf"#### {re.escape(header)}\s*\n(.*?)(?=\n####|\n---|\n###|\Z)"
    m = re.search(pattern, body, re.DOTALL)
    return m.group(1).strip() if m else ""


def clean_jira_text(t: str) -> str:
    """Strip markdown links; preserve inline code and bold; collapse whitespace."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\s+", " ", t.replace("\n", " "))
    return t.strip()


def _extract_inline_section(body: str, start_pattern: str, end_pattern: str) -> str:
    """Extract text after an inline bold header until an end pattern."""
    m = re.search(rf"({start_pattern})(.*?)(?={end_pattern}|\Z)", body, re.DOTALL)
    return m.group(2).strip() if m else ""


def parse_stories(stories_path: Path) -> list[dict]:
    if not stories_path.exists():
        return []
    text = stories_path.read_text(encoding="utf-8")
    matches = list(STORY_HEADER_RE.finditer(text))
    stories = []
    for i, m in enumerate(matches):
        sid   = m.group(1)
        phase = m.group(2).upper()
        title = m.group(4).strip()

        # Phase A is a real story now (e.g. BOM A04 type-resolver) — no longer skipped.

        start = m.end()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body  = text[start:end]

        meta = METADATA_INLINE_RE.search(body)
        if meta:
            complexity_raw = meta.group(2).strip()
        else:                                    # YAML `{… complexity: X …}` fallback (matches breakdown parser)
            yaml_c = re.search(r"\bcomplexity:\s*([A-Za-z ]+)", body, re.IGNORECASE)
            complexity_raw = yaml_c.group(1).strip() if yaml_c else "Low"
        complexity = re.sub(r"[⚠️🔶⚪]\s*", "", complexity_raw).strip().lower()

        dep_m    = DEPENDS_RE.search(body)
        depends  = dep_m.group(1).strip() if dep_m else ""
        blocked_m = BLOCKED_RE.search(body)
        blocked  = blocked_m.group(1).strip() if blocked_m else ""
        status_m = STATUS_RE.search(body)
        status   = status_m.group(1).strip() if status_m else DEFAULT_STATUS

        # Build depends list (may include blocked-by), deduped — fixes the 'B01, B01' class of bug
        dep_parts = [d.strip() for d in re.split(r"[,;]", depends) if d.strip() and d.strip() != "—"]
        if blocked:
            dep_parts += [b.strip() for b in re.split(r"[,;]", blocked) if b.strip()]
        dep_str = dedupe_ids(", ".join(dep_parts))

        # Acceptance Criteria — numbered items, preserve code + bold
        ac_sec   = extract_named_section(body, "Acceptance Criteria")
        ac_items = re.findall(r"\d+\.\s*(.+?)(?=\n\d+\.|\Z)", ac_sec, re.DOTALL)
        ac_lines = []
        for idx, item in enumerate(ac_items, 1):
            cleaned = clean_jira_text(item).rstrip(".")
            if cleaned:
                ac_lines.append(f"{idx}. {cleaned}")

        # Test Cases — only for High / Very High
        test_lines = []
        if complexity in ("high", "very high"):
            tests_sec  = extract_named_section(body, "Test Cases")
            test_items = re.findall(r"- \[ \]\s*(.+)", tests_sec)
            for t in test_items:
                cleaned = clean_jira_text(t)
                if cleaned:
                    test_lines.append(f"[ ] {cleaned}")

        # Build description
        desc_parts = []

        # Current Behaviour — handle both inline (**CB:**) and header (#### CB) formats
        cb = (
            extract_named_section(body, "Current Behaviour")
            or _extract_inline_section(body, r"\*\*Current Behaviour[^:*]*:\*\*\s*", r"\*\*Target|\n\n####")
        )
        if cb and cb.lower() not in ("green-field", "—", ""):
            # Strip EXT/ACL footnote lines
            cb_clean = re.sub(r"> \*\*EXT[^\n]*\n?", "", cb)
            cb_clean = re.sub(r"> \*\*ACL[^\n]*\n?", "", cb_clean)
            cb_clean = clean_jira_text(cb_clean).rstrip(" -")
            if cb_clean:
                desc_parts.append(f"*Current Behaviour:*\n* {cb_clean}")

        # Target — handle both formats
        tgt = (
            extract_named_section(body, "Target DGS Implementation")
            or _extract_inline_section(body, r"\*\*Target(?: DGS Implementation)?[:\*]*\*?\s*", r"\n\n\*\*Files|\n\n####")
        )
        if tgt:
            tgt_clean = clean_jira_text(tgt).rstrip(" -")
            if tgt_clean:
                desc_parts.append(f"*Target:*\n* {tgt_clean}")

        # Spike-specific: pull the plain-English summary + the unknowns so the ticket is
        # self-explanatory. The spike analysis reflects the research done so far; the ADR
        # is a later-phase artifact and is deliberately NOT referenced here.
        if phase == "S":
            lay_m = re.search(r"\*\*Layman summary:\*\*\s*(.*?)(?=\n\n|\n\*\*)", body, re.DOTALL)
            if lay_m:
                desc_parts.append("*Summary:*\n* " + clean_jira_text(lay_m.group(1)))
            unk_m = re.search(r"\*\*What's unknown:\*\*\s*(.*?)(?=\n\*\*Candidate|\n\*\*Prior|\n####)", body, re.DOTALL)
            if unk_m:
                desc_parts.append("*What's unknown:*\n* " + clean_jira_text(unk_m.group(1)))

        # One point per line — bullets/numbers, never a paragraph blob.
        if ac_lines:
            desc_parts.append("*Acceptance Criteria:*\n" + "\n".join(ac_lines))

        if test_lines:
            desc_parts.append("*Test Cases:*\n" + "\n".join(f"* {t}" for t in test_lines))

        # Fallback for compact "family" stories (In plain terms / Covers / inline
        # Acceptance) that carry no Current Behaviour / Target / #### sections.
        if not desc_parts:
            plain_m = re.search(r"\*\*In plain terms:?\*\*\s*([^\n]+)", body)
            if plain_m:
                desc_parts.append("*Summary:*\n* " + clean_jira_text(plain_m.group(1)))
            cov_m = re.search(r"\*\*Covers:\*\*\s*(.*?)(?=\*\*Acceptance|\*\*Tests|\Z)", body, re.DOTALL)
            if cov_m:
                desc_parts.append("*Covers:*\n* " + clean_jira_text(cov_m.group(1)))
            acc_m = re.search(r"\*\*Acceptance:\*\*\s*(.*?)(?=\*\*Tests|\Z)", body, re.DOTALL)
            if acc_m:
                items = re.findall(r"\d+\.\s*(.+?)(?=\s*\d+\.|\Z)", acc_m.group(1), re.DOTALL)
                if items:
                    desc_parts.append(
                        "*Acceptance Criteria:*\n"
                        + "\n".join(f"{i}. {clean_jira_text(x).rstrip('.')}" for i, x in enumerate(items, 1))
                    )
                else:
                    desc_parts.append("*Acceptance Criteria:*\n* " + clean_jira_text(acc_m.group(1)))

        description = "\n\n".join(desc_parts)  # real paragraphs, preserved by CSV quoting

        stories.append({
            "id": sid, "title": title, "phase": phase,
            "complexity": complexity, "depends": dep_str,
            "description": description, "status": status,
        })
    return stories


# Complex-story data lives in generate_comprehensive; import it so the Jira ticket points at the
# sub-task breakdown + the detailed cross-domain case CSV.
try:
    from generate_comprehensive import COMPLEX_STORIES
except Exception:
    COMPLEX_STORIES = {}

# Program spikes (the generalized cross-domain buckets) are defined once in generate_breakdown.
# Reuse them so the CSV, the .md and the .docx all agree on ids, titles, steps and mapping.
try:
    from generate_breakdown import (
        spike_for as _spike_for, SPIKE_TITLES, SPIKE_LAYMAN, SPIKE_DECISION,
        SPIKE_STEPS, SPIKE_CASE_FOLDER,
    )
except Exception:                                    # pragma: no cover — fallback keeps CSVs generating
    _spike_for       = lambda s: None
    SPIKE_TITLES     = {}
    SPIKE_LAYMAN     = {}
    SPIKE_DECISION   = {}
    SPIKE_STEPS      = {}
    SPIKE_CASE_FOLDER = {}

_SPIKE_REF_RE = re.compile(r"\b(?:SPARK-[A-Z]+-)?S\d+\b")


def _strip_domain_spike_refs(dep: str) -> str:
    """Drop references to now-removed per-domain spikes (bare `S0x` / `SPARK-*-S0x`)."""
    dep = _SPIKE_REF_RE.sub("", dep)
    dep = re.sub(r"\s*,\s*,\s*", ", ", dep).strip(" ,")
    return dedupe_ids(dep)


def program_spike_rows() -> list[list]:
    """The generalized program spikes (one Jira Spike row per SPIKE_TITLES bucket; all-stories.csv only)."""
    rows = []
    for b in sorted(SPIKE_TITLES):
        # One labelled section per line, steps as a numbered list — points, not a blob.
        steps = "\n".join(f"{i}. {clean_jira_text(s)}" for i, s in enumerate(SPIKE_STEPS.get(b, []), 1))
        case  = SPIKE_CASE_FOLDER.get(b)
        desc_sections = [
            f"*Summary:*\n* {clean_jira_text(SPIKE_LAYMAN.get(b, ''))}",
            f"*Decision to make:*\n* {clean_jira_text(SPIKE_DECISION.get(b, ''))}",
            f"*Intended cross-domain steps:*\n{steps}",
        ]
        if case:
            desc_sections.append(f"*Research so far:*\n* complexStories/{case}/")
        desc = "\n\n".join(desc_sections)
        rows.append([
            "Spike",
            f"SPARK-SPIKE-{b}",
            f"(Program) {SPIKE_TITLES[b]} [SPARK-SPIKE-{b}]",
            "", GLOBAL_EPIC_NAME, "S", "M",
            "dgs-migration", "all-domains", "spike",
            "", "", DEFAULT_STATUS, desc,
        ])
    return rows


def complex_ref_map(domain: str) -> dict:
    """story-id → a Description suffix describing its sub-tasks + cross-domain complex case."""
    data = COMPLEX_STORIES.get(domain, {})
    m: dict[str, str] = {}
    for r in data.get("very_high", []) + data.get("high", []):
        ref = f"*Complex — broken into sub-tasks:* {r['subtasks']}"
        if r.get("complex_case"):
            ref += (f"\n\n*Detailed cross-domain case:* complexStories/{r['complex_case']}/ "
                    f"(import {r['complex_case']}.csv for the sub-tasks)")
        m[r["id"]] = ref
    for r in data.get("delegated", []):
        case = r["case"].rstrip("/").split("/")[-1]
        ids  = r["id"].split("/")
        base = ids[0].rsplit("-", 1)[0]
        full = [ids[0]] + [f"{base}-{x}" for x in ids[1:]]
        for sid in full:
            m[sid] = (f"*Complex — delegated to cross-domain case:* complexStories/{case}/ "
                      f"(problem brief; the task breakdown follows with the spike)")
    return m


def epic_row() -> list:
    """The single shared epic row that every story/spike links to."""
    return [
        "Epic", "", GLOBAL_EPIC_NAME, GLOBAL_EPIC_NAME, "", "", "",
        "dgs-migration", "all-domains", "epic", "", "", "",
        GLOBAL_EPIC_DESC,
    ]


def build_story_rows(domain: str) -> list[list]:
    """Story/spike rows for one domain — summary tagged with the domain, linked to the shared epic."""
    tag     = DOMAIN_TAG.get(domain, domain)
    src_dir = get_domain_dir(domain)
    stories = parse_stories(src_dir / "04-stories.md")
    cref    = complex_ref_map(domain)

    rows = []
    for s in stories:
        # Per-domain spikes are centralized as program spikes (all-stories.csv) — skip them here.
        if s["phase"] == "S":
            continue

        size = SIZE_MAP.get(s["complexity"], "M")
        cat  = PHASE_LABEL.get(s["phase"], "story")
        desc = s["description"]
        if s["id"] in cref:                       # append complex-case breakdown reference
            desc = (desc + "\n\n" + cref[s["id"]]) if desc else cref[s["id"]]

        # Depends On — drop dangling per-domain spike refs; if the story is spike-gated,
        # link it to the program spike and note the requirement in the description.
        dep = _strip_domain_spike_refs(s["depends"])
        b   = _spike_for(s)
        if b:
            spike_id = f"SPARK-SPIKE-{b}"
            dep      = spike_id if not dep else f"{spike_id}, {dep}"
            note     = f"*Requires spike:* {spike_id} ({SPIKE_TITLES.get(b, '')}) — see program spike"
            desc     = (note + "\n\n" + desc) if desc else note

        rows.append([
            "Story",
            s["id"],
            f"({tag}) {s['title'].replace('`', '')} [{s['id']}]",   # (Domain) title [Story ID]
            "",                      # Epic Name (link by name in Jira)
            GLOBAL_EPIC_NAME,        # Epic Link — the one shared epic
            s["phase"],
            size,
            "dgs-migration", domain, cat,
            "",                      # Parent Link
            dep,
            s["status"],
            desc,
        ])

    return rows


def build_csv(domain: str) -> list[list]:
    """A standalone per-domain CSV: the shared epic row + that domain's stories."""
    return [epic_row()] + build_story_rows(domain)


HEADERS = [
    "Issue Type", "Story ID", "Summary", "Epic Name", "Epic Link",
    "Phase", "T-shirt size",
    "Labels", "Labels", "Labels",
    "Parent Link", "Depends On", "Status", "Description",
]


def write_csv(rows: list[list], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(rows)


def generate_domain(domain: str, out_dir: "Path | None" = None) -> int:
    rows    = build_csv(domain)
    dest    = Path(out_dir) if out_dir else JIRA_OUT
    dest.mkdir(parents=True, exist_ok=True)
    out     = dest / f"{domain}.csv"
    write_csv(rows, out)
    story_count = sum(1 for r in rows if r[0] == "Story")
    rel = out.relative_to(HERE) if out.is_relative_to(HERE) else out
    print(f"  OK {rel} ({story_count} stories, {len(rows)} rows)")
    return len(rows)


def generate_all_csv(domains: list[str]) -> None:
    all_rows: list[list] = [epic_row()]          # ONE shared epic for all domains
    all_rows.extend(program_spike_rows())        # the generalized cross-domain spikes (one per bucket)
    for domain in domains:
        all_rows.extend(build_story_rows(domain))
    out = JIRA_OUT / "all-stories.csv"
    write_csv(all_rows, out)
    story_count = sum(1 for r in all_rows if r[0] == "Story")
    spike_count = sum(1 for r in all_rows if r[0] == "Spike")
    print(f"  OK all-stories.csv ({story_count} stories + {spike_count} program spikes)")


# ─── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import datetime
    print(f"=== Jira CSV generation -- {datetime.date.today()} ===\n")

    targets = [a for a in sys.argv[1:] if not a.startswith("--")]
    domains = targets if targets else ALL_DOMAINS

    for d in domains:
        if d not in ALL_DOMAINS:
            print(f"  SKIP '{d}' not in domain list")
            continue
        try:
            generate_domain(d)
        except Exception as e:
            print(f"  FAIL {d}: {e}")

    if not targets:
        generate_all_csv(domains)

    print(f"\nDone. Output: {JIRA_OUT}")
