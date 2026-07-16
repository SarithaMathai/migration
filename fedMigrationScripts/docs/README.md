# Migration Docs — README & User Guide

This is the **file inventory + navigation guide** for the `spark-internal-graphql` → Netflix DGS migration
deliverables under `output/`. Two parts:

- **Part A — File Inventory:** every file under `output/`, its purpose, audience, and whether it's source
  / generated / regenerable.
- **Part B — Navigate by Role:** which files to open, in what order, for who you are.

> **Golden rule:** the **source of truth** is `analysis/{domain}/be-04-stories.md` + `be-04-po-summary.md`.
> Everything in `summary/` and `../jira/*.csv` is **generated** from it by `fedMigrationScripts/generatescripts/generate_*.py` — never
> hand-edit a generated file (it's overwritten on the next run).

> **Traceability:** every story maps to **one `spark-internal-graphql` operation** — the story *title* is that
> gateway operation, its *Current Behaviour* describes the operation's logic today (DataLoader + REST call), and
> the `(Qn/Mn)` tag points into `analysis/{domain}/be-02-resolver-analysis.md`.

---

# Part A — File Inventory (everything under `output/`)

### `analysis/{domain}/` — SOURCE analysis (inputs; edit `04-*` here)

| File | Purpose | Audience | Regenerable? |
|---|---|---|---|
| `be-01-schema-inventory.md` | Every GraphQL type/field in the domain — the surface being migrated | Architect / Eng | source (hand/analysis) |
| `be-02-resolver-analysis.md` | Per-resolver logic of the **spark-internal-graphql** gateway (what each op does today) — the migration reference | Eng | source |
| `be-03-schema-analysis.md` | Migration approach + federation notes | Architect | source |
| `be-03-schema.graphql` | Target **federated SDL** (the DGS schema) | Eng / Architect | source |
| `be-04-stories.md` | **The migration stories** — source of truth for all generation | Eng | source ✍️ **edit here** |
| `be-04-po-summary.md` | PO planning summary — source for the po-review | PO / Lead | source ✍️ **edit here** |
| `be-05-attribute-inventory.md` | Field-by-field attribute mapping | Eng | source |

### `summary/{domain}/` — GENERATED deliverables (do not edit)

| File | Purpose | Audience | Regenerable? |
|---|---|---|---|
| `FederatedGqlBreakDown-BE-{domain}.md` | **Confluence breakdown** — phase tables (1 row/story), spikes, deployment model, **§5b complex breakdowns**, risks, decisions, dep map | PO + Eng | ✅ generated |
| `FederatedGqlBreakDown-BE-{domain}.docx` | Same, Word format | Word/Confluence upload | ✅ generated |
| `{domain}-comprehensive.md` | **Heavy** eng doc — every story's full body (CB, examples, pseudocode, target, AC, tests) + **§8b complex breakdowns** | Engineers | ✅ generated |
| `{domain}-po-review.md` | Executive review — scope, deployment, risks, **decisions**, capacity, **Phase-2 complex breakdowns** | PO / Stakeholders | ✅ generated |

### `summary/` root — GENERATED program-level + scripts + guides

| File | Purpose | Audience | Regenerable? |
|---|---|---|---|
| `00-program-overview.md` | All 13 domains: totals, per-domain table, DGS groupings, risks, decisions, sequencing, cross-domain blockers | Program leads / PO | ✅ generated |
| `Federated+Graphql+Stories+-+BreakDown.md`/`.docx` | **Global** — all 13 domains, one overview | All | ✅ generated |
| `Federated+Graphql+Stories+-+BreakDown_custom.md`/`.docx` | **Scoped overview** — 7 selected modules only (product, bom, claims, productDetails, packaging, watchlist, measurement). The global page above is untouched. | All | ✅ generated |
| the generators live in `../generatescripts/` (`generate_all.py` + `generate_*.py`) | run these to rebuild everything | 🛠️ Script Runner | scripts |
| `README.md` | This guide — inventory + Script-Runner how-to | Everyone / Script Runner | hand-authored |
| `README-PO.md` | Navigation guide for PO / Stakeholder / Reviewer | PO | hand-authored |
| `README-ENGINEER.md` | Navigation guide for Engineer / Architect | Engineer | hand-authored |
| `PUSH-TO-JIRA-CONFLUENCE.md` | MCP prompts to push stories→Jira and pages→Confluence | Delivery | hand-authored |

### `../jira/` — GENERATED Jira import

| File | Purpose | Audience | Regenerable? |
|---|---|---|---|
| `{domain}.csv` | One row/story+spike (+Epic): size, depends-on, status, Description (CB, target, AC, tests, **complex-case ref**) | Scrum / Delivery | ✅ generated |
| `all-stories.csv` | All 13 domains' stories in one import file | Scrum | ✅ generated |

### `../complexStories/{case}/` — cross-domain hard cases (separate; referenced by the summary)

| File | Purpose | Audience |
|---|---|---|
| `00-overview.md` | What/why of the case + the ADR/decision | PO / Architect |
| `ARCHITECTURE.md` | The federation/orchestration design | Architect / Eng |
| `01-stories.md` | Detailed sub-task breakdown | Eng |
| `{case}.csv` | Jira import for the case's sub-tasks | Scrum |
| `implementation/` | Engineer-facing pseudo-code + SDL per cross-service op | Eng |

> The 7 cases: `techpack`, `partner-drop-undrop-write`, `attachments-enrichment`, `non-atomic-write-saga`,
> `components-and-counts-rollups`, `notRemovable-undroppable-partners`, `polymorphic-type-resolution`.

### `../reference/` + `../CHANGELOG.md`

| File | Purpose | Audience |
|---|---|---|
| `reference/*.md` | Methodology + federation-pattern guides (`RUN-NEW-DOMAIN.md`, `reference-federation-patterns.md`, …) | Eng / Architect |
| `CHANGELOG.md` | History of tracked changes | Everyone |

---

# Part B — Navigate by Role

> **Role-specific navigation lives in its own short guide** (each contains *only* how that role moves through
> the artifacts):
> - **Product Owner / Stakeholder / Reviewer** → [`README-PO.md`](./README-PO.md)
> - **Architect / Tech Lead** → [`README-ARCHITECT.md`](./README-ARCHITECT.md)
> - **Engineer** → [`README-ENGINEER.md`](./README-ENGINEER.md)
> - **🛠️ Script Runner / Maintainer** → the **§Script Runner** section below (regenerate, Jira, Confluence).

### How to read a story row
```
BOM-BE-B-04 · getBomByParentId · 🔷 Query · 🟢 Low [XS] · Depends On: — · ⬜ Not Started
```
`ID` (stable ref) · `Phase` 🔬0 🧱A 📖B 🔍C ✏️D ⚙️E 🔗F 🧪G · `Type` 🔷Query 🔶Mutation 🔸Resolver ·
`Complexity→size` 🟢XS 🟡M 🟠L 🔴XL · `Depends On` (real story-to-story only) · `Status`.

### Conventions
- **Counts:** BOM **39**, Product **70** (incl. Phase-0 spikes; BOM incl. `A-04`).
- **`B-01` isn't a per-story dependency** — it lands the one-time DGS module scaffold; assumed once (in the
  dependency graph), not repeated per row.
- **Thin wrappers:** model + REST (GET/POST/PUT) + service already exist; each story adds only the DGS layer.
- **Ship on green, per story** — except cross-subgraph entity extensions (marked **BLOCKED-BY**).
- **Cross-refs are by ID/name, not file path** (so they survive Confluence/Jira).

---

## 🛠️ Script Runner — regenerate & publish

```bash
cd migration
python fedMigrationScripts/generatescripts/generate_all.py                 # ALL domains → output/summary/{domain}/* + output/jira/*.csv + 00-program-overview.md
python fedMigrationScripts/generatescripts/generate_all.py bom product     # just these domains
python fedMigrationScripts/generatescripts/generate_breakdown.py --global  # refresh the all-domains breakdown page
python fedMigrationScripts/generatescripts/generate_breakdown.py --custom  # refresh the scoped (7-module) BreakDown_custom.md
python fedMigrationScripts/generatescripts/generate_word.py --custom       # the same, as .docx
```
> A no-arg `generate_breakdown.py` / `generate_word.py` builds **both** the global and the `_custom` pages.
> Change the 7 modules by editing `CUSTOM_DOMAINS` in `generatescripts/generate_breakdown.py` + `generate_word.py`.
- **Setup:** `pip install python-docx` (only for the `.docx`). Output is deterministic (re-runs = byte-identical).
- **Edit → regen loop:** edit `analysis/{domain}/04-*.md` → `python fedMigrationScripts/generatescripts/generate_all.py {domain}`.
- **Push to Jira / Confluence:** follow the prompts in `PUSH-TO-JIRA-CONFLUENCE.md` (imports `jira/{domain}.csv`,
  wires `Depends On` links, publishes the breakdown + po-review pages).

*Push detail: `PUSH-TO-JIRA-CONFLUENCE.md`. Program rollup: `00-program-overview.md`.*
