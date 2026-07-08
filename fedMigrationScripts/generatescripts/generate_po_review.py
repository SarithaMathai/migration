#!/usr/bin/env python3
"""
Generate {domain}-po-review.md for every domain.

Artifact: Executive / PO-facing review for stakeholder prioritization.
Concise: scope, effort, risks, decisions, migration approach, sprint capacity,
and complex story breakdowns (where applicable). No per-story engineering detail.

Format mirrors the confluence pages — Confluence-paste ready.

Source priority:
  1. output/initial-analysis/{domain}/  (updated, Phase A dissolved where applicable)
  2. migration/finalOutput/{domain}/         (fallback; used for search)

Output → migration/finalOutput/oneStopDoc/{domain}-po-review.md

Run:
    cd migration/finalOutput/oneStopDoc
    python generate_po_review.py              # all domains
    python generate_po_review.py product bom  # specific domain(s)
"""

import re
import sys
from pathlib import Path
from datetime import date

# ─── Path setup ──────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
UPDATED_SOURCE = HERE.parent.parent / "output" / "initial-analysis"
FALLBACK_SOURCE = HERE.parent.parent / "output" / "initial-analysis"
OUT_DIR = HERE.parent.parent / "output" / "summary"

# ─── Domain catalogue ─────────────────────────────────────────────────────────
# thirdAttempt scope: all 13 domains — the 8 phase-1 domains plus attachment,
# discussion, sample, search and workspace.
ALL_DOMAINS = [
    "attachment", "bom", "claims", "discussion", "impression",
    "measurement", "packaging", "product", "productDetails",
    "sample", "search", "watchlist", "workspace",
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

DGS_KIND = {
    "product":        "host",
    "bom":            "co-located in plm-product",
    "measurement":    "co-located in plm-product",
    "packaging":      "co-located in plm-product",
    "impression":     "co-located in plm-product",
    "productDetails": "co-located in plm-product",
    "watchlist":      "co-located in plm-product",
    "workspace":      "separate subgraph",
    "sample":         "separate subgraph",
    "discussion":     "separate subgraph",
    "attachment":     "separate subgraph",
    "search":         "separate subgraph",
    "claims":         "separate subgraph",
}

# ─── Complex story breakdowns (Phase 2) ───────────────────────────────────────
# Mirrors STORY-BREAKDOWN-GUIDE.md. Domains not listed here have no breakdowns.
PHASE2_BREAKDOWNS: dict[str, dict] = {
    "product": {
        "intro": (
            "Four stories in this domain (2 Very High + 2 High) were broken into "
            "**M-size (≤5 day) sub-tasks** in Jira. Two additional Very High stories "
            "are delegated to dedicated complex cases."
        ),
        "rows": [
            ("SPARK-PROD-E01", "productBusinessPartnerActions (drop/undrop)", "Very High",
             "E01-1 orchestrator + fan-out · E01-2 ACL drop + user-profile · E01-3 saga + parity harness"),
            ("SPARK-PROD-G01", "Product.attachmentsWithMetaData", "Very High",
             "G01-1 per-domain service call + merge · G01-2 metadata hydration + counts"),
            ("SPARK-PROD-E02", "updateComponentStatuses (5-loader fan-out)", "High",
             "E02-1 loader scaffold + status updates · E02-2 parity + count validation"),
            ("SPARK-PROD-G03", "Product.attachments / attachmentsV3 / attachmentSummary", "High",
             "G03-1 attachments + attachmentsV3 · G03-2 attachmentSummary + draft filtering"),
        ],
        "delegated_note": (
            "> `SPARK-PROD-E03/E04` (TechPack) and `SPARK-PROD-G02` (components) are delegated to "
            "complex cases — those provide the full cross-domain breakdown; the Jira stubs point there."
        ),
    },
    "bom": {
        "intro": "Two stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "rows": [
            ("SPARK-BOM-E01", "updateBom — 3-step orchestrated write", "Very High",
             "E01-1 workspace-assoc + body PUT · E01-2 permissions PUT + rollback framework"),
            ("SPARK-BOM-G08", "BomTrimMaterial field resolvers (dispatcher + 7 types)", "High",
             "G08-1 dispatcher scaffold + type resolution · G08-2 7 TrimMaterial field resolvers"),
        ],
        "delegated_note": (
            "> `SPARK-BOM-E01` is also the home stub for the **non-atomic-write-saga** complex case. "
            "See `complexStories/non-atomic-write-saga/`."
        ),
    },
    "workspace": {
        "intro": (
            "Three stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira. "
            "One additional Very High story is delegated to a complex case."
        ),
        "rows": [
            ("SPARK-WS-E01", "workspaceBusinessPartnerActionsV2 (5-case dispatcher)", "Very High",
             "E01-1 dispatcher scaffold + sample/discussion/claims cases · E01-2 engagement/team/ACL removal + saga"),
            ("SPARK-WS-G01", "WorkspaceV2.attachmentsWithMetaData (hub rollup)", "Very High",
             "G01-1 per-domain services + merge · G01-2 metadata + draft filtering + counts"),
        ],
        "delegated_note": (
            "> `SPARK-WS-G02` (counts — dashboard rollup + increment) is delegated to "
            "`complexStories/components-and-counts-rollups/`. "
            "In Jira, sub-tasks appear nested under their parent story."
        ),
    },
    "attachment": {
        "intro": "One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "rows": [
            ("SPARK-ATCH-G01", "Attachment field resolvers (cross-domain)", "High",
             "G01-1 access/users · G01-2 businessPartnersFull + snake/camel"),
        ],
    },
    "claims": {
        "intro": "One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "rows": [
            ("SPARK-CLM-E01", "updateClaim (proxy ACL + workspace + body)", "High",
             "E01-1 body PUT + workspace call · E01-2 ACL proxy + orchestration"),
        ],
    },
    "discussion": {
        "intro": "Two stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "rows": [
            ("SPARK-DISC-E02", "Participants V3 (4 bundled mutations)", "High",
             "E02-1 updateParticipantsV3 + coreUpdate · E02-2 coreDelete + deleteParticipantV3"),
            ("SPARK-DISC-G01", "Discussion field resolvers (3 main types)", "High",
             "G01-1 Discussion + Content · G01-2 FullDiscussion + participants"),
        ],
    },
    "packaging": {
        "intro": "One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "rows": [
            ("SPARK-PKG-E01", "updatePackaging (body + attachment add/remove, branching)", "High",
             "E01-1 body + attachment add · E01-2 attachment remove + pricing"),
        ],
    },
    "sample": {
        "intro": "Three stories in this domain were broken into **M-size (≤5 day) sub-tasks** in Jira.",
        "rows": [
            ("SPARK-SMPL-E02", "bulkEvaluateSamples (evaluation + new-rounds utility)", "High",
             "E02-1 evaluation orchestrator · E02-2 new-rounds utility"),
            ("SPARK-SMPL-G02", "Prefix-gated parents (5 prefixes + union)", "High",
             "G02-1 prefix→loader table + DataLoader · G02-2 parent field resolvers + union"),
        ],
    },
}

# ─── Source file resolution ───────────────────────────────────────────────────
def get_domain_dir(domain: str) -> Path:
    for src in [FALLBACK_SOURCE / domain]:
        if (src / "04-po-summary.md").exists():
            return src
    raise FileNotFoundError(
        f"No source found for '{domain}'. Checked: "
        f"{UPDATED_SOURCE / domain}, {FALLBACK_SOURCE / domain}"
    )


def extract_section(text: str, header: str) -> str:
    """Extract content under a ## or ### header, stopping at the next ##."""
    pattern = rf"## {re.escape(header)}.*?\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else ""


def strip_relative_links(text: str) -> str:
    """Confluence/Jira-safe: relative markdown links become plain text (they break once hosted).
    http(s) links and in-page #anchors stay clickable."""
    def repl(m: "re.Match") -> str:
        label, url = m.group(1), m.group(2)
        return m.group(0) if url.startswith(("http://", "https://", "#")) else label
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def build_migration_approach(po_text: str, domain: str) -> str:
    """
    Build a one-paragraph migration approach summary from the phase table.
    Preserves original case of phase descriptions.
    """
    # Try explicit migration approach section first
    m = re.search(r"## Migration Approach.*?\n(.*?)(?=\n## |\Z)", po_text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Build from phase table rows (columns: Phase | Name | Stories | Effort | ...)
    phase_rows = re.findall(
        r"^\|\s*([A-G])\s*\|\s*([^|*\n]+?)\s*\|",
        po_text, re.MULTILINE
    )
    # Filter out header rows, total rows, and Phase A (dissolved)
    filtered = [
        (p.strip(), n.strip())
        for p, n in phase_rows
        if p.strip() in "BCDEFG" and "Phase" not in n and "Name" not in n
    ]
    if not filtered:
        return f"See [`03-schema-analysis.md §Migration Approach`](../finalOutput/{domain}/03-schema-analysis.md)."

    parts = [f"**{p}** {n.rstrip(';')}" for p, n in filtered]
    return (
        "; ".join(parts) + ". "
        f"Full detail: [`03-schema-analysis.md §Migration Approach`]"
        f"(../finalOutput/{domain}/03-schema-analysis.md)."
    )


def build_phase2_section(domain: str) -> list[str]:
    data = PHASE2_BREAKDOWNS.get(domain)
    if not data:
        return []

    lines: list[str] = [
        "## Phase 2 Story Breakdowns",
        "",
        data["intro"],
        "",
        "| Parent milestone | Original size | Sub-tasks |",
        "|---|---|---|",
    ]
    for sid, name, size, subtasks in data["rows"]:
        lines.append(f"| `{sid}` {name} | {size} | {subtasks} |")

    lines.append("")
    if "delegated_note" in data:
        lines.append(data["delegated_note"])
        lines.append("")

    lines += [
        "> In Jira, sub-tasks appear **nested under** their parent story. "
        "Sprint capacity: each sub-task = M (3–5 days).",
        "",
    ]
    return lines


# ─── Document builder ─────────────────────────────────────────────────────────
def build_po_review(domain: str) -> str:
    label   = DOMAIN_LABELS.get(domain, domain.title())
    dgs     = DGS_MAP.get(domain, "")
    kind    = DGS_KIND.get(domain, "")
    src_dir = get_domain_dir(domain)
    today   = date.today().isoformat()

    po_text = (src_dir / "04-po-summary.md").read_text(encoding="utf-8")
    # Strip the trailing "*Pipeline 2.0 ...*" colophon and any stray "Pipeline Version:" line —
    # these are internal pipeline bookkeeping, not PO-facing content, and used to leak through
    # into whichever section happened to be last in the source file (Capacity Planning).
    po_text = re.sub(r"\n---\s*\n\*Pipeline \d[^\n]*\*\s*$", "", po_text.rstrip())
    po_text = re.sub(r"^>.*\*\*Pipeline Version:\*\*[^\n]*\n?", "", po_text, flags=re.MULTILINE)

    lines: list[str] = []

    # ── Title & Header ────────────────────────────────────────────────────────
    lines += [
        f"# {label} — Migration to the `{dgs}` DGS (PO view)",
        "",
        f"> 🏷️ **Tags:** `dgs-migration` · `po-page` · `domain-{domain}` · `pipeline-v2`  —  "
        f"**Confluence location:** *Federation Graph Migration ▸ Domains ▸ {domain}*",
        "",
        f"> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.  ",
        f"> Deep dives: [migration approach & schema](../finalOutput/{domain}/03-schema-analysis.md) · "
        f"[field inventory](../finalOutput/{domain}/05-attribute-inventory.md) · "
        f"[engineering stories](../finalOutput/{domain}/04-stories.md).  ",
        f"> Create tickets from [`../finalOutput/jira/{domain}.csv`](../finalOutput/jira/{domain}.csv). "
        f"Effort is **AI-estimated — confirm in refinement.**",
        "",
        "---",
        "",
    ]

    # ── What are we building? ─────────────────────────────────────────────────
    lines += ["## What are we building?", ""]
    what = extract_section(po_text, "What Are We Building?")
    lines += [what if what else f"Migration of the **{label}** domain to the `{dgs}` DGS ({kind}).", ""]

    # ── Scope ─────────────────────────────────────────────────────────────────
    lines += ["## Scope", ""]
    scope = extract_section(po_text, "Migration Scope")
    lines += [scope if scope else "_Scope table not available._", ""]

    # ── Deployment model (ship on green, per story) ───────────────────────────
    deploy = extract_section(po_text, "Deployment model — ship on green, per story") \
        or extract_section(po_text, "Deployment model")
    if deploy:
        lines += ["## Deployment model — ship on green, per story", "", deploy, ""]

    # ── Effort by phase ───────────────────────────────────────────────────────
    lines += ["## Effort by phase (AI-estimated, +20% buffer)", ""]
    phase_block = extract_section(po_text, "Story Summary by Phase")
    if phase_block:
        phase_block = re.sub(r"^Story Summary by Phase.*\n", "", phase_block).strip()
        # Keep the legit Phase-A (A04) row; strip only dissolved-note + pipeline noise
        phase_block = re.sub(r"^>.*[Pp]hase A dissolved[^\n]*\n?", "", phase_block, flags=re.MULTILINE)
        phase_block = re.sub(r"^>.*No separate Phase A[^\n]*\n?", "", phase_block, flags=re.MULTILINE)
        phase_block = re.sub(r"^\*Pipeline 2\.0[^\n]*\n?", "", phase_block, flags=re.MULTILINE)
        phase_block = phase_block.strip()
        lines += [phase_block, ""]
    else:
        lines += ["_Phase effort not available._", ""]

    # ── Decisions required (Key risks intentionally omitted) ──────────────────
    lines += ["## Decisions required", ""]
    decisions = extract_section(po_text, "Decisions Required")
    lines += [decisions if decisions else "_No decisions documented._", ""]
    if "Phase 0" in decisions or "SPIKE" in decisions:
        lines += [
            f"> 🔬 Open decisions marked **Spike** are tracked as real, estimable Phase 0 stories — "
            f"see *Phase 0 — Spikes* in [`../finalOutput/{domain}/04-stories.md`](../finalOutput/{domain}/04-stories.md) "
            f"and [`{domain}/FederatedGqlBrakDown-{domain}.md`](./{domain}/FederatedGqlBrakDown-{domain}.md) "
            f"for the full write-up (unknowns, candidate patterns, examples).",
            "",
        ]

    # ── Migration approach ────────────────────────────────────────────────────
    lines += ["## Migration approach (summary)", ""]
    approach = build_migration_approach(po_text, domain)
    lines += [approach, ""]

    # ── Sequencing & capacity ─────────────────────────────────────────────────
    lines += ["## Sequencing & capacity", ""]
    seq = extract_section(po_text, "Recommended Sprint Sequencing")
    cap = extract_section(po_text, "Capacity Planning")
    if cap:
        lines += [cap, ""]
    if seq:
        lines += [seq, ""]

    # ── Phase 2 story breakdowns ──────────────────────────────────────────────
    p2 = build_phase2_section(domain)
    if p2:
        lines += p2

    # ── Footer (name references only — relative links break once hosted in Confluence) ──
    lines += [
        "---",
        f"*PO review assembled from the `{domain}` analysis. "
        f"Jira tickets: `finalOutput/jira/{domain}.csv`. "
        f"Full engineering detail: `{domain}-comprehensive.md` (same folder).*",
    ]

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
            content  = build_po_review(domain)
            domain_dir = OUT_DIR / domain
            domain_dir.mkdir(parents=True, exist_ok=True)
            out_file = domain_dir / f"{domain}-po-review.md"
            out_file.write_text(content, encoding="utf-8")
            print(f"  OK {out_file.relative_to(REPO_ROOT)} ({len(content):,} chars)")
        except FileNotFoundError as e:
            print(f"  FAIL {domain}: {e}")
        except Exception as e:
            print(f"  FAIL {domain}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
