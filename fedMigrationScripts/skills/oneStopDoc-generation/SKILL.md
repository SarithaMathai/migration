# Skill: oneStopDoc Generation

**Purpose:** Regenerate all per-domain publication artifacts from the analyzed source files.

---

## What this skill produces

For each of the 13 domains, running this skill produces **five files** inside `finalOutput/oneStopDoc/{domain}/`:

| Output file | Audience | Contents |
|---|---|---|
| `FederatedGqlBrakDown-{domain}.docx` | PO + Engineers · **Open in Word / paste into Confluence** | **Primary artifact** — Microsoft Word with full formatting: navy blue title, light-blue metrics banner, colored table headers, complexity-coded text (🔴🟠🟡🟢), type icons (🔷🔶🔸), phase icons, all 8 sections as Word content. Ready to copy-paste into Confluence or share as a Word doc. |
| `FederatedGqlBrakDown-{domain}.md` | PO + Engineers · Confluence paste (Markdown) | Markdown fallback — same content and table format as the Word doc; use this when pasting raw Markdown into Confluence. |
| `{domain}-comprehensive.md` | Engineers + Tech Leads | Full engineering doc — executive summary, scope, phase effort table, risks, decisions, dependency map, sprint sequencing, capacity planning, complex story breakdowns (§8b), **all stories** with AC + test cases (High/VH only), and story reference table |
| `{domain}-po-review.md` | Product Owner + Stakeholders | Concise PO review — what we're building, scope, effort by phase, key risks, decisions required, migration approach summary, sprint capacity, and Phase 2 story breakdowns |
| `{domain}.csv` | Jira admin | Jira-import CSV — one Epic + per-story rows; schema init excluded (it is a B-01 checklist item, not a story); test cases included only for High/VH stories |

Plus program-level files at `finalOutput/oneStopDoc/`:
- `Federated+Graphql+Stories+-+BreakDown.docx` — All domains in one Word doc: domain index table + per-domain story tables; fully formatted (primary)
- `Federated+Graphql+Stories+-+BreakDown.md` — Same content as Markdown (Confluence fallback)
- `00-executive-summary.md` — Cross-domain scope, risk register, sequencing, per-domain quick reference
- `00-portfolio.md` — Program portfolio table for Confluence space home
- `jira/all-stories.csv` — All 325 stories in a single Jira import file

---

## When to run

Run any time the source analysis files are updated:
- After running any of the domain analysis phases (Phase 1–5) for a domain
- After resolving a key architecture decision that changes story scope or complexity
- After Phase 2 story breakdowns are added or revised
- Before a stakeholder review session — to ensure docs reflect the latest state

---

## How to run

```bash
cd migration/finalOutput/oneStopDoc

# Regenerate all 13 domains + all global docs (recommended)
python generate_all.py

# Regenerate a single domain (all 5 artifacts)
python generate_all.py impression

# Regenerate only Word docs (.docx — the primary artifact)
python generate_word.py
python generate_word.py attachment   # single domain
python generate_word.py --global     # global Word doc only

# Regenerate only breakdown Markdown docs (Confluence raw paste)
python generate_breakdown.py
python generate_breakdown.py attachment   # single domain
python generate_breakdown.py --global    # global doc only

# Regenerate only comprehensive docs
python generate_comprehensive.py

# Regenerate only PO review docs
python generate_po_review.py

# Regenerate only Jira CSVs
python generate_jira.py

# Skip executive summary / portfolio (useful when iterating on a single domain)
python generate_all.py bom product --no-summary
```

**Python requirements:** Python 3.10+. `python-docx` package required for Word generation (`pip install python-docx`).

---

## Source files (what gets read)

The generators look for source files in this priority order:

| Priority | Location | Status |
|---|---|---|
| 1 (preferred) | `finslDocSomeRevision/domain/{domain}/` | Updated versions — schema/service init is a B-01 checklist item (not a story) |
| 2 (fallback) | `migration/finalOutput/{domain}/` | Original pipeline output — used only for `search` |

**Key source files per domain:**
- `04-stories.md` → all stories (comprehensive §9, breakdown story tables, Jira CSV)
- `04-po-summary.md` → scope, effort, sprint sequencing, risks, decisions (used by all four artifacts)

---

## Format rules

### Breakdown doc (`FederatedGqlBrakDown-{domain}.md`)
- **Table format for stories** — each story is one row: `Story ID | Operation | Type | Complexity | Depends On | AC`; no card-style headers
- **Phase grouping** — each phase gets its own `###` heading with icon and story count, then a single table for all stories in that phase
- **Complexity icons** — 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low; size badge (`XS`/`M`/`L`/`XL`) in the complexity cell
- **Type icons** — 🔷 Query · 🔶 Mutation · 🔸 Field Resolver; inferred from metadata or phase when source says "Story"
- **DGS init notes** — B-01 notes shown as blockquotes beneath the table, not inline
- **Tests** — shown only for High/VH stories, as a checklist beneath the phase table
- **No Phase A** — schema/service init is a B-01 checklist item; no Phase A rows appear anywhere
- **Sections** — §1 What We're Building · §2 Scope · §3 Effort + Capacity · §4 Sprint Sequencing · §5 Stories by Phase · §6 Risks · §7 Decisions · §8 Dependency Map

### Comprehensive doc
- **Schema/service init** is a one-time checklist inside B-01 — no Phase A stories or rows appear in any output
- **Test cases:** shown **only for High and Very High** complexity stories. Low and Medium stories show acceptance criteria only
- **Complex story callouts:** domains with broken-down stories get a §8b section listing parent milestones → sub-tasks
- **Story IDs** are linkable: `SPARK-{DOMAIN}-{phase}{nn}` format throughout
- **Confluence-paste ready:** no HTML, no unsupported macros — headings, tables, and mermaid blocks only

### PO review doc
- **No engineering detail** — no file paths, no DGS annotations, no per-story breakdown
- **Phase 2 breakdowns** appear for the 8 domains that have them (product, bom, workspace, attachment, claims, discussion, packaging, sample)
- **Tags and Confluence location** in the header for easy page organization
- Concise: typically 1–2 Confluence pages

### Jira CSV
- One Epic row per domain + one Story row per story
- Tests in description only for High/VH stories
- `Labels` column maps phase to Jira label (e.g., `dgs-migration-phase-B`)

---

## Adding a new domain

1. Run the full analysis pipeline for the new domain (Phases 1–5) — outputs to `finslDocSomeRevision/domain/{new-domain}/`
2. Add the domain to `ALL_DOMAINS`, `DOMAIN_LABELS`, `DGS_MAP` in all four generators (`generate_comprehensive.py`, `generate_po_review.py`, `generate_jira.py`, `generate_breakdown.py`)
3. If the domain has complex/split stories, add an entry to `COMPLEX_STORIES` (in `generate_comprehensive.py`) and `PHASE2_BREAKDOWNS` (in `generate_po_review.py`)
4. Add domain metadata to `DOMAIN_META` and `TSHIRT_DATA` in `generate_all.py` and `generate_breakdown.py`
5. Run `python generate_all.py {new-domain}`

---

## Relationship to other skills

| Skill | Feeds into oneStopDoc? |
|---|---|
| `migration-story-generation` | Yes — produces `04-stories.md` which is the source for comprehensive §9 |
| `graphql-schema-inventory` | No — produces `01-schema-inventory.md` (engineer reference, not in oneStopDoc) |
| `resolver-dependency-analysis` | No — produces `02-resolver-analysis.md` (deep engineering reference, linked but not embedded) |
| `federation-schema-derivation` | No — produces `03-schema.graphql` (linked in PO review deep-dive links) |
| `federation-candidate-detection` | No — produces `03-schema-analysis.md` (linked in PO review deep-dive links) |

---

*fedMigrationScripts — oneStopDoc Generation Skill · Pipeline 2.0*
