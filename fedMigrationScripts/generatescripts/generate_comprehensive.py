#!/usr/bin/env python3
"""
Generate {domain}-comprehensive.md for every domain.

Artifact: Full engineering doc — executive summary, scope, phase table, risks,
decisions, dependency map, sprint sequencing, capacity planning, complex story
breakdowns (§8b), all stories with AC + test cases (High/VH only), and a
story reference table.

Source priority:
  1. output/analysis/{domain}/  (updated, Phase A dissolved where applicable)
  2. migration/finalOutput/{domain}/         (fallback; used for search)

Output → migration/finalOutput/oneStopDoc/{domain}-comprehensive.md

Run:
    cd migration/finalOutput/oneStopDoc
    python generate_comprehensive.py              # all domains
    python generate_comprehensive.py impression   # specific domain(s)
"""

import re
import sys
from pathlib import Path
from datetime import date

# ─── Path setup ──────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent                   # .../finalOutput/oneStopDoc/
REPO_ROOT = HERE.parent.parent                    # c:\Saritha\jun30\
UPDATED_SOURCE = HERE.parent.parent / "output" / "analysis"
FALLBACK_SOURCE = HERE.parent.parent / "output" / "analysis"       # .../finalOutput/analysis/
OUT_DIR = HERE.parent.parent / "output" / "summary"

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

DGS_MAP = {
    "product":        "plm-product (host)",
    "bom":            "plm-product (co-located)",
    "measurement":    "plm-product (co-located)",
    "packaging":      "plm-product (co-located)",
    "impression":     "plm-product (co-located)",
    "productDetails": "plm-product (co-located)",
    "watchlist":      "plm-product (co-located)",
    "workspace":      "plm-workspace (separate)",
    "sample":         "plm-sample (separate)",
    "discussion":     "plm-discussion (separate)",
    "attachment":     "plm-attachment (separate)",
    "search":         "plm-elastic-search (separate)",
    "claims":         "spark-claims (separate)",
}

# ─── Complex story data ───────────────────────────────────────────────────────
# Per-domain breakdown of Very High (VH) and split High (H) stories.
# This mirrors STORY-BREAKDOWN-GUIDE.md and confluence/{domain}.md §Phase 2.
COMPLEX_STORIES: dict[str, dict] = {
    "product": {
        "intro": (
            "Several stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira. "
            "A number of them are also covered by dedicated complex-case breakdowns — see "
            "each case's `01-stories.md` for the full cross-domain story set."
        ),
        "very_high": [
            {
                "id": "PRODUCT-BE-E-00",
                "name": "WriteSaga shared module (Sprint 0, critical path)",
                "subtasks": "E-00-1 ordered-steps + policy engine · E-00-2 default policy table + compensation inventory",
                "complex_case": "non-atomic-write-saga",
            },
            {
                "id": "PRODUCT-BE-E-01",
                "name": "productBusinessPartnerActions (drop/undrop)",
                "subtasks": "E-01-1 orchestrator + fan-out · E-01-2 ACL drop + user-profile · E-01-3 saga + parity harness",
                "complex_case": "partner-drop-undrop-write",
            },
            {
                "id": "PRODUCT-BE-E-03",
                "name": "TechPack stub + facade (facade-then-federate, draft ADR-015 Option B)",
                "subtasks": "E-03 thin stub + aggregation facade",
                "complex_case": "techpack",
            },
            {
                "id": "PRODUCT-BE-E-04",
                "name": "TechPack bulk wrapper (ordering fix)",
                "subtasks": "E-04 bulk wrapper (input-ordered)",
                "complex_case": "techpack",
            },
            {
                "id": "PRODUCT-BE-G-01",
                "name": "Product.attachmentsWithMetaData",
                "subtasks": "G-01-1 per-domain service call + merge · G-01-2 metadata hydration + counts",
                "complex_case": "attachments-enrichment",
            },
            {
                "id": "PRODUCT-BE-G-02",
                "name": "Product.components (fan-out + rollups)",
                "subtasks": "G-02-1 batched-ACL fan-out · G-02-2 count rollups + type tagging",
                "complex_case": "components-and-counts-rollups",
            },
            {
                "id": "PRODUCT-BE-G-11-1",
                "name": "Product.notRemovablePartnerIds + notRemovableWorkspaceIds",
                "subtasks": "G-11-1-1 lane clients (discussion/attachment/sample/watchlist) · G-11-1-2 union + parallelization",
                "complex_case": "notRemovable-undroppable-partners",
            },
        ],
        "high": [
            {"id": "PRODUCT-BE-E-02", "name": "updateComponentStatuses (5-loader fan-out)", "subtasks": "E-02-1 loader scaffold + status updates · E-02-2 parity + count validation"},
            {"id": "PRODUCT-BE-G-03", "name": "Product.attachments / attachmentsV3 / attachmentSummary", "subtasks": "G-03-1 attachments + attachmentsV3 · G-03-2 attachmentSummary + draft filtering"},
            {
                "id": "PRODUCT-BE-G-07",
                "name": "unDroppablePartners semantics",
                "subtasks": "G-07-1 design-partner gate + dps exclusion · G-07-2 numeric-grantee filter",
                "complex_case": "notRemovable-undroppable-partners",
            },
            {
                "id": "PRODUCT-BE-D-01",
                "name": "addProduct (shared association component)",
                "subtasks": "D-01-1 workspace link via component",
                "complex_case": "cross-domain-association",
            },
            {
                "id": "PRODUCT-BE-D-02",
                "name": "addProducts bulk (shared association component)",
                "subtasks": "D-02-1 workspace link · D-02-2 attachment-metadata client call (replaces cross-resolver import)",
                "complex_case": "cross-domain-association",
            },
            {
                "id": "PRODUCT-BE-D-04",
                "name": "updateProduct (shared association component)",
                "subtasks": "D-04-1 template-attachment archiving via component",
                "complex_case": "cross-domain-association",
            },
        ],
    },
    "bom": {
        "intro": "Several stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "very_high": [
            {"id": "BOM-BE-E-01", "name": "updateBom — 3-step orchestrated write", "subtasks": "E-01-1 workspace-assoc + body PUT · E-01-2 permissions PUT + rollback framework", "complex_case": "non-atomic-write-saga"},
        ],
        "high": [
            {"id": "BOM-BE-G-08", "name": "BomTrimMaterial field resolvers (7 types + dispatcher)", "subtasks": "G-08-1 dispatcher scaffold + type resolution · G-08-2 7 TrimMaterial field resolvers"},
            {
                "id": "BOM-BE-A-05",
                "name": "Shared CI conformance gate + code→type registry",
                "subtasks": "A-05-1 SDL↔enum↔fixture conformance library · A-05-2 code→type registry seeding",
                "complex_case": "polymorphic-type-resolution",
            },
        ],
    },
    "workspace": {
        "intro": "Three stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "very_high": [
            {"id": "WORKSPACE-BE-E-01", "name": "workspaceBusinessPartnerActionsV2 (5-case dispatcher)", "subtasks": "E-01-1 dispatcher scaffold + sample/discussion/claims cases · E-01-2 engagement/team/ACL removal + saga", "complex_case": "partner-drop-undrop-write"},
            {"id": "WORKSPACE-BE-G-01", "name": "WorkspaceV2.attachmentsWithMetaData (hub rollup)", "subtasks": "G-01-1 per-domain services + merge · G-01-2 metadata + draft filtering + counts", "complex_case": "attachments-enrichment"},
        ],
        "delegated": [
            {"id": "WORKSPACE-BE-G-02", "name": "counts (dashboard rollup + increment)", "case": "complexStories/components-and-counts-rollups/"},
        ],
    },
    "attachment": {
        "intro": "One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "high": [
            {"id": "ATTACHMENT-BE-G-01", "name": "Attachment field resolvers (cross-domain)", "subtasks": "G-01-1 access/users · G-01-2 businessPartnersFull + snake/camel"},
        ],
    },
    "claims": {
        "intro": "One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "high": [
            {"id": "CLAIM-BE-E-01", "name": "updateClaim (proxy ACL + workspace + body)", "subtasks": "E-01-1 body PUT + workspace call · E-01-2 ACL proxy + orchestration"},
        ],
    },
    "discussion": {
        "intro": "Two stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "high": [
            {"id": "DISCUSSION-BE-E-02", "name": "Participants V3 (4 bundled mutations)", "subtasks": "E-02-1 updateParticipantsV3 + coreUpdate · E-02-2 coreDelete + deleteParticipantV3"},
            {"id": "DISCUSSION-BE-G-01", "name": "Discussion field resolvers (3 main types)", "subtasks": "G-01-1 Discussion + Content · G-01-2 FullDiscussion + participants"},
        ],
    },
    "packaging": {
        "intro": "One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "high": [
            {"id": "PKG-BE-E-01", "name": "updatePackaging (body + attachment add/remove, branching)", "subtasks": "E-01-1 body + attachment add · E-01-2 attachment remove + pricing"},
        ],
    },
    "sample": {
        "intro": "Three stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "high": [
            {"id": "SAMPLE-BE-E-02", "name": "bulkEvaluateSamples (evaluation + new-rounds utility)", "subtasks": "E-02-1 evaluation orchestrator · E-02-2 new-rounds utility"},
            {"id": "SAMPLE-BE-G-02", "name": "Prefix-gated parents (5 prefixes + union)", "subtasks": "G-02-1 prefix→loader table + DataLoader · G-02-2 parent field resolvers + union"},
        ],
    },
}

# ─── Phase names ──────────────────────────────────────────────────────────────
PHASE_NAMES = {
    "S": "Spikes (Phase 0)",
    "A": "Foundation & Type Resolvers",
    "B": "Core Reads",
    "C": "Search & Listing",
    "D": "Mutations (Simple)",
    "E": "Complex Operations",
    "F": "Federation & Stitching",
    "G": "Field Resolvers, Bug-fixes & Tests",
}

# ─── Complexity badges ────────────────────────────────────────────────────────
COMPLEXITY_BADGE = {
    "low":       "🟢 Low",
    "medium":    "🟡 Medium",
    "high":      "🟠 High",
    "very high": "🔴 Very High",
}

def complexity_badge(c: str) -> str:
    return COMPLEXITY_BADGE.get(c.lower(), f"⚪ {c.title()}")


# ─── Source file resolution ───────────────────────────────────────────────────
def get_domain_dir(domain: str) -> Path:
    for src in [FALLBACK_SOURCE / domain]:
        if (src / "be-04-po-summary.md").exists():
            return src
    raise FileNotFoundError(f"No source found for domain '{domain}'. Checked: {UPDATED_SOURCE / domain}, {FALLBACK_SOURCE / domain}")


# ─── Story parser ─────────────────────────────────────────────────────────────
STORY_HEADER_RE = re.compile(
    r"^### ([A-Z]+-BE-[A-Za-z]-\d+(?:-\d+)?) · (.+)$", re.MULTILINE
)
METADATA_INLINE_RE = re.compile(
    r"\*\*Type:\*\*\s*([^·\n]+).*?\*\*Complexity:\*\*\s*([^·\n]+)", re.DOTALL
)
PHASE_RE   = re.compile(r"\*\*Phase:\*\*\s*([A-Z])\b")
DEPENDS_RE = re.compile(r"\*\*Depends on:\*\*\s*([^\n*·]+)")
EXT_RE     = re.compile(r"\*\*EXT:\*\*\s*([^\n]+)")
BLOCKED_RE = re.compile(r"\*\*Blocked by:\*\*\s*([^\n]+)")
BLOCKS_RE  = re.compile(r"\*\*Blocks:\*\*\s*([^\n*·]+)")
STATUS_RE  = re.compile(r"\*\*Status:\*\*\s*([^\n*·]+)")
ADR_RE     = re.compile(r"\*\*ADR:\*\*\s*([^\n]+)")


def extract_named_section(body: str, header: str) -> str:
    pattern = rf"#### {re.escape(header)}\s*\n(.*?)(?=\n####|\n---|\n###|\Z)"
    m = re.search(pattern, body, re.DOTALL)
    return m.group(1).strip() if m else ""


def clean_text(t: str) -> str:
    """Strip all markdown formatting — used for metadata fields."""
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.strip()


def clean_ac_text(t: str) -> str:
    """Clean AC/test text preserving inline code and bold for readability."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)   # strip links → text
    t = re.sub(r"\s+", " ", t.replace("\n", " "))      # collapse whitespace
    return t.strip().rstrip(".")


def strip_phase_a(text: str) -> str:
    """Remove only genuine noise: 'Phase A dissolved' blockquote notes and pipeline footers.
    Does NOT delete legit Phase-A story rows/refs — BOM's `A-04` type-resolver is a real story."""
    text = re.sub(r"^>.*[Pp]hase A dissolved[^\n]*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^>.*No separate Phase A[^\n]*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\*Pipeline 2\.0[^\n]*\n?", "", text, flags=re.MULTILINE)
    return text.strip()


def strip_relative_links(text: str) -> str:
    """Confluence/Jira-safe: relative markdown links become plain text (they break once hosted).
    http(s) links and in-page #anchors stay clickable."""
    def repl(m: "re.Match") -> str:
        label, url = m.group(1), m.group(2)
        return m.group(0) if url.startswith(("http://", "https://", "#")) else label
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def parse_stories(stories_path: Path) -> list[dict]:
    if not stories_path.exists():
        return []
    text = stories_path.read_text(encoding="utf-8")
    matches = list(STORY_HEADER_RE.finditer(text))
    stories = []
    for i, m in enumerate(matches):
        sid   = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body  = text[start:end]

        meta = METADATA_INLINE_RE.search(body)
        op_type    = meta.group(1).strip() if meta else "Story"
        complexity_raw = meta.group(2).strip() if meta else ""
        if not complexity_raw:
            # YAML format: complexity: High
            yaml_c = re.search(r"\bcomplexity:\s*([A-Za-z ]+)", body, re.IGNORECASE)
            complexity_raw = yaml_c.group(1).strip() if yaml_c else "Low"
        complexity = re.sub(r"[⚠️🔶⚪]\s*", "", complexity_raw).strip()

        # Phase: prefer inline **Phase:** X, then YAML, then extract from story ID
        phase_m = PHASE_RE.search(body)
        if phase_m:
            phase = phase_m.group(1)
        else:
            yaml_p = re.search(r"\bphase:\s*([A-H])\b", body, re.IGNORECASE)
            if yaml_p:
                phase = yaml_p.group(1).upper()
            else:
                id_p = re.search(r"-BE-([A-H])-\d", sid)
                phase = id_p.group(1) if id_p else "?"
        dep_m     = DEPENDS_RE.search(body)
        depends   = dep_m.group(1).strip() if dep_m else "—"
        ext_m     = EXT_RE.search(body)
        ext       = ext_m.group(1).strip() if ext_m else ""
        blocked_m = BLOCKED_RE.search(body)
        blocked   = blocked_m.group(1).strip() if blocked_m else ""
        blocks_m  = BLOCKS_RE.search(body)
        blocks    = blocks_m.group(1).strip() if blocks_m else ""
        status_m  = STATUS_RE.search(body)
        status    = status_m.group(1).strip() if status_m else ""
        adr_m     = ADR_RE.search(body)
        adr       = adr_m.group(1).strip() if adr_m else ""

        # Acceptance Criteria — preserve inline code + bold for readability
        ac_sec  = extract_named_section(body, "Acceptance Criteria")
        ac_items = re.findall(r"\d+\.\s*(.+?)(?=\n\d+\.|\Z)", ac_sec, re.DOTALL)
        ac = [clean_ac_text(x) for x in ac_items if x.strip()]

        # Test Cases — preserve inline code + bold; shown only for High/VH
        tests_sec  = extract_named_section(body, "Test Cases")
        test_items = re.findall(r"- \[ \]\s*(.+)", tests_sec)
        tests = [clean_ac_text(x) for x in test_items]

        stories.append({
            "id": sid, "title": title, "type": op_type,
            "complexity": complexity.lower(), "phase": phase,
            "depends": depends, "ext": ext, "blocked": blocked,
            "blocks": blocks, "status": status, "adr": adr,
            "ac": ac, "tests": tests, "body": body,
        })
    return stories


def group_by_phase(stories: list[dict]) -> dict[str, list]:
    groups: dict[str, list] = {}
    for s in stories:
        groups.setdefault(s["phase"], []).append(s)
    return dict(sorted(groups.items()))


# ─── Complex story section builder ───────────────────────────────────────────
def build_complex_section(domain: str) -> list[str]:
    data = COMPLEX_STORIES.get(domain)
    if not data:
        return []

    lines: list[str] = [
        "## Complex Story Breakdowns",
        "",
        data.get("intro", "Some stories in this domain were broken into M-size sub-tasks."),
        "",
    ]

    vh_rows = data.get("very_high", [])
    h_rows  = data.get("high", [])
    del_rows = data.get("delegated", [])

    if vh_rows or del_rows:
        lines += [
            "### Very High stories (broken into sub-tasks or delegated to a complex case)",
            "",
            "| Parent milestone | Why complex | Sub-tasks / Complex case |",
            "|---|---|---|",
        ]
        for r in vh_rows:
            case_ref = f" · Complex case: [`{r['complex_case']}`](../complexStories/{r['complex_case']}/00-overview.md)" if r.get("complex_case") else ""
            lines.append(f"| `{r['id']}` {r['name']} | see story | {r['subtasks']}{case_ref} |")
        for r in del_rows:
            lines.append(f"| `{r['id']}` {r['name']} | delegated | see [`{r['case']}`](../../finalOutput/{r['case']}00-overview.md) |")
        lines.append("")

    if h_rows:
        lines += [
            "### High stories (split into M-size sub-tasks)",
            "",
            "| Parent milestone | Why split | Sub-tasks |",
            "|---|---|---|",
        ]
        for r in h_rows:
            lines.append(f"| `{r['id']}` {r['name']} | see story | {r['subtasks']} |")
        lines.append("")

    lines += [
        "> Sub-tasks carry T-shirt size **M** (3–5 days). Parent stories are **milestones** (0 points in Jira).",
        "> In Jira sub-tasks appear nested under their parent story.",
        "",
        "---",
        "",
    ]
    return lines


# ─── Document builder ─────────────────────────────────────────────────────────
def build_comprehensive(domain: str) -> str:
    label   = DOMAIN_LABELS.get(domain, domain.title())
    dgs     = DGS_MAP.get(domain, "")
    src_dir = get_domain_dir(domain)
    today   = date.today().isoformat()

    po_text     = (src_dir / "be-04-po-summary.md").read_text(encoding="utf-8")
    stories_path = src_dir / "be-04-stories.md"
    stories      = parse_stories(stories_path)
    phases       = group_by_phase(stories)

    lines: list[str] = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines += [
        f"# {label} — Comprehensive Migration Documentation",
        "",
        f"> **Domain:** `{domain}` · **Target DGS:** `{dgs}` · **Generated:** {today}",
        f"> **Confluence location:** *Federation Graph Migration ▸ Domains ▸ {domain}*",
        "",
        "---",
        "",
    ]

    # ── Table of Contents ─────────────────────────────────────────────────────
    lines += ["## Table of Contents", ""]
    toc_sections = [
        "- [Executive Summary](#executive-summary)",
        "- [Migration Scope](#migration-scope)",
        "- [Story Summary by Phase](#story-summary-by-phase)",
        "- [Decisions Required](#decisions-required)",
        "- [Recommended Sprint Sequencing](#recommended-sprint-sequencing)",
        "- [Capacity Planning](#capacity-planning)",
    ]
    if domain in COMPLEX_STORIES:
        toc_sections.append("- [Complex Story Breakdowns](#complex-story-breakdowns)")
    toc_sections.append("- [All Stories — Detailed Engineering Breakdown](#all-stories--detailed-engineering-breakdown)")
    for phase_key in sorted(phases.keys()):
        pname = PHASE_NAMES.get(phase_key, f"Phase {phase_key}")
        slug  = f"phase-{phase_key.lower()}--{pname.lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '').replace('&', '').replace('--', '-').replace('/', '')}"
        toc_sections.append(f"  - [Phase {phase_key} — {pname}](#{slug})")
    toc_sections.append("- [Story Reference Table](#story-reference-table)")
    lines += toc_sections + ["", "---", ""]

    # ── Executive Summary ─────────────────────────────────────────────────────
    lines += ["## Executive Summary", ""]
    m = re.search(r"## What Are We Building\?\s*\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL)
    lines += [(m.group(1).strip() if m else f"Migration of **{label}** to the Netflix DGS platform."), "", "---", ""]

    # ── Migration Scope ───────────────────────────────────────────────────────
    lines += ["## Migration Scope", ""]
    m = re.search(r"## Migration Scope\s*\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL)
    lines += [(m.group(1).strip() if m else "_Scope data not available._"), "", "---", ""]

    # ── Deployment Model (ship on green, per story) ───────────────────────────
    m = re.search(r"## Deployment model[^\n]*\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL)
    if m:
        lines += ["## Deployment Model — Ship on Green, Per Story", "", m.group(1).strip(), "", "---", ""]

    # ── Story Summary by Phase ────────────────────────────────────────────────
    lines += ["## Story Summary by Phase", ""]
    m = re.search(r"## Story Summary by Phase.*?\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL)
    phase_section = strip_phase_a(m.group(1)) if m else "_Phase summary not available._"
    lines += [phase_section, "", "---", ""]

    # ── Decisions Required (Key Risk Areas and Dependency Map intentionally omitted) ──
    lines += ["## Decisions Required", ""]
    m = re.search(r"## Decisions Required.*?\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL)
    lines += [(m.group(1).strip() if m else "_No decisions documented._"), "", "---", ""]

    # ── Recommended Sprint Sequencing ─────────────────────────────────────────
    lines += ["## Recommended Sprint Sequencing", ""]
    m = re.search(r"## Recommended Sprint Sequencing\s*\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL)
    lines += [(m.group(1).strip() if m else "_Sprint sequencing not documented._"), "", "---", ""]

    # ── Capacity Planning ─────────────────────────────────────────────────────
    lines += ["## Capacity Planning", ""]
    m = re.search(r"## Capacity Planning\s*\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL)
    lines += [(m.group(1).strip() if m else "_Capacity planning not documented._"), "", "---", ""]

    # ── §8b: Complex Story Breakdowns ─────────────────────────────────────────
    lines += build_complex_section(domain)

    # ── §9: All Stories ───────────────────────────────────────────────────────
    lines += [
        "## All Stories — Detailed Engineering Breakdown",
        "",
        "> Each story is self-contained. Read: **Current Behaviour → Target → Acceptance Criteria**.",
        "> Test cases are included only for **High** and **Very High** complexity stories.",
        "",
    ]

    # Phases overview from stories file
    stories_text = stories_path.read_text(encoding="utf-8") if stories_path.exists() else ""
    m = re.search(r"## 1\. Phases Overview\s*\n(.*?)(?=\n## |\n---|\Z)", stories_text, re.DOTALL)
    if m:
        overview = strip_phase_a(m.group(1))
        if overview:
            lines += ["### Phases Overview", "", overview, "", "---", ""]

    # Dependency graph intentionally omitted (dependency map/graph dropped per doc standard)

    for phase_key in sorted(phases.keys()):
        pname = PHASE_NAMES.get(phase_key, f"Phase {phase_key}")
        lines += [f"### Phase {phase_key} — {pname}", ""]

        for s in phases[phase_key]:
            badge = complexity_badge(s["complexity"])
            cl    = s["complexity"].lower()

            lines += [
                f"#### {s['id']} · {s['title']}",
                "",
                "| Field | Value |",
                "|---|---|",
                f"| **Type** | {s['type']} |",
                f"| **Complexity** | {badge} |",
                f"| **Phase** | {phase_key} |",
                f"| **Depends on** | {s['depends']} |",
            ]
            if s.get("blocks"):
                lines.append(f"| **Blocks** | {s['blocks']} |")
            if s["ext"]:
                lines.append(f"| **EXT** | {s['ext']} |")
            if s["blocked"]:
                lines.append(f"| **Blocked by** | {s['blocked']} |")
            if s.get("status"):
                lines.append(f"| **Status** | {s['status']} |")
            lines.append("")

            # Full story body (heavy detail: current behaviour, examples, pseudocode, target, files) —
            # everything up to the Acceptance Criteria, minus the metadata line(s) already shown in the table.
            body = s["body"].strip()
            body_main = re.split(r"\n#### (?:Acceptance Criteria|Test Cases)", body)[0]
            body_main = re.sub(r"^\*\*Type:\*\*[^\n]*\n?",   "", body_main, flags=re.MULTILINE)
            body_main = re.sub(r"^\*\*Status:\*\*[^\n]*\n?", "", body_main, flags=re.MULTILINE)
            body_main = strip_phase_a(body_main).strip()
            # Neutralize the "layman"/"plain English" self-label from source — keep the content.
            body_main = re.sub(r"\*\*(?:Layman summary|Plain[- ]English summary|In plain English):\*\*",
                               "**In summary:**", body_main, flags=re.IGNORECASE)
            if body_main:
                lines += [body_main, ""]

            # Acceptance Criteria (always shown)
            if s["ac"]:
                lines += ["**Acceptance Criteria:**", ""]
                for idx, item in enumerate(s["ac"], 1):
                    lines.append(f"{idx}. {item}")
                lines.append("")

            # Test Cases — only for High / Very High complexity
            if s["tests"] and cl in ("high", "very high"):
                lines += ["**Test Cases:**", ""]
                for t in s["tests"]:
                    lines.append(f"- [ ] {t}")
                lines.append("")

            lines += ["---", ""]

    lines += ["---", ""]

    # ── §10: Story Reference Table ─────────────────────────────────────────────
    lines += [
        "## Story Reference Table",
        "",
        "| Story ID | Title | Phase | Complexity | Depends On |",
        "|---|---|---|---|---|",
    ]
    for s in stories:
        badge = complexity_badge(s["complexity"])
        dep   = s["depends"] if s["depends"] else "—"
        lines.append(f"| `{s['id']}` | {s['title']} | {s['phase']} | {badge} | {dep} |")

    return strip_relative_links("\n".join(lines))


# ─── Runner ───────────────────────────────────────────────────────────────────
def main() -> None:
    targets = sys.argv[1:] if len(sys.argv) > 1 else ALL_DOMAINS
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for domain in targets:
        if domain not in ALL_DOMAINS:
            print(f"  UNKNOWN domain '{domain}' — skipping")
            continue
        try:
            content  = build_comprehensive(domain)
            domain_dir = OUT_DIR / domain
            domain_dir.mkdir(parents=True, exist_ok=True)
            out_file = domain_dir / f"{domain}-comprehensive.md"
            out_file.write_text(content, encoding="utf-8")
            print(f"  OK {out_file.relative_to(REPO_ROOT)} ({len(content):,} chars)")
        except FileNotFoundError as e:
            print(f"  FAIL {domain}: {e}")
        except Exception as e:
            print(f"  FAIL {domain}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
