# Confluence publication inventory

The complete list of pages the migration program publishes to Confluence, with the exact title, source
file, and parent location for each. This is the checklist the publish prompts (see
[`PUSH-TO-JIRA-CONFLUENCE.md`](../docs/PUSH-TO-JIRA-CONFLUENCE.md)) work through; formatting is
preserved per the rules in that runbook. Pages update in place by exact title on re-sync — never
duplicated.

**Scope note:** phase 1 covers **8 domains** — product, bom, measurement, packaging, impression,
productDetails, watchlist, claims. The remaining domains (attachment, discussion, sample, search,
workspace) join in a later phase and are out of scope for this inventory until then.

**Totals: 22 core pages** — 1 space home · 2 program roll-ups (overview + sequencing) · 16 domain
pages (8 domains × 2: breakdown + FE-readiness graph) · 3 optional deep-dive tiers (PO review,
comprehensive, complex-case ADRs) published on request, not by default.

**Audience map** — who each tier is for:

| Tier | Pages | Audience |
|---|---|---|
| 1. Program orientation | Space home, Program Overview, Migration Sequencing | Everyone — architects, PO, stakeholders, new engineers |
| 2. Per-domain default | Breakdown page, FE-Readiness graph (×8 domains) | Engineers (BE+FE) implementing that domain, tech leads reviewing scope |
| 3. Deep-dive (opt-in) | PO review, Comprehensive, Complex-case ADRs | PO ratifying a decision, an engineer who needs full pseudo-logic, an architect reviewing a cross-domain design |

---

## 1. Space home

| Title | Source | Content |
|---|---|---|
| Spark → Federated GraphQL Migration — Program Overview | `finalArtifacts/00-overview.md` | What/why, program totals, domain-at-a-glance table, DGS service groupings, phase legend |

## 2. Federation Graph Migration ▸ Program — roll-ups (2)

| Title | Source | Content |
|---|---|---|
| Migration Sequencing & Roadmap | `finalArtifacts/00-sequencing.md` | Domain build order + why, per-domain BE/FE roadmap and step tables, full story sequence, external gates, effort summary |
| Federated GraphQL Stories — Breakdown (All Domains) | `output/summary/Federated+Graphql+Stories+-+BreakDown.md` | The global page: program spike register, spike details, all-domain story roll-up (bigger and more detailed than the overview — publish alongside it, not instead of it) |

## 3. Federation Graph Migration ▸ Domains — two pages per domain (16)

Titles follow one convention: `{Domain} — Federated GraphQL Breakdown` (engineering/PO story
breakdown) and `{Domain} — FE Readiness`. Each domain page nests both as children.

| Domain | Breakdown page (source) | FE-Readiness page (source) |
|---|---|---|
| Product | `finalArtifacts/summary/product/FederatedGqlBreakDown-product.md` | `finalArtifacts/summary/product/story-dependency-graph-product.md` |
| BOM | `finalArtifacts/summary/bom/FederatedGqlBreakDown-bom.md` | `finalArtifacts/summary/bom/story-dependency-graph-bom.md` |
| Measurement | `finalArtifacts/summary/measurement/FederatedGqlBreakDown-measurement.md` | `finalArtifacts/summary/measurement/story-dependency-graph-measurement.md` |
| Packaging | `finalArtifacts/summary/packaging/FederatedGqlBreakDown-packaging.md` | `finalArtifacts/summary/packaging/story-dependency-graph-packaging.md` |
| Impression | `finalArtifacts/summary/impression/FederatedGqlBreakDown-impression.md` | `finalArtifacts/summary/impression/story-dependency-graph-impression.md` |
| Product Details | `finalArtifacts/summary/productDetails/FederatedGqlBreakDown-productDetails.md` | `finalArtifacts/summary/productDetails/story-dependency-graph-productDetails.md` |
| Watchlist | `finalArtifacts/summary/watchlist/FederatedGqlBreakDown-watchlist.md` | `finalArtifacts/summary/watchlist/story-dependency-graph-watchlist.md` |
| Claims | `finalArtifacts/summary/claims/FederatedGqlBreakDown-claims.md` | `finalArtifacts/summary/claims/story-dependency-graph-claims.md` |

Each **breakdown** page contains: the domain's story list by phase (A–H) with acceptance criteria,
spike-gated stories flagged with their program spike, complexity/T-shirt sizing, and the BE+FE
sections merged onto one page. Each **FE-Readiness** page contains: one small diagram per frontend
story showing exactly which backend stories must ship before it can start — this is new since the
last inventory pass and was previously not published anywhere.

## 4. Deep-dive tier — published on request, not by default (per domain, 2 each = 16 optional)

These exist under `output/summary/{domain}/` but only after a `generate_all.py --full` run, and are
**not** copied into `finalArtifacts/` — they're the working-detail tier, one step short of
`be-04-stories.md` itself. Publish only when a specific reader needs this level of depth (a PO
ratifying a scope decision, an engineer who needs the full pseudo-logic before implementing).

| Title | Source | When to publish |
|---|---|---|
| `{Domain} — PO Review` | `output/summary/{domain}/{domain}-po-review.md` | PO needs the decisions-required list without the engineering detail |
| `{Domain} — Comprehensive` | `output/summary/{domain}/{domain}-comprehensive.md` | An engineer needs full pseudo-logic / schema detail beyond the breakdown page — large (largest domain, product, is 2500+ lines) |

## 5. Federation Graph Migration ▸ Architecture ▸ Complex Cases — ADRs (9, on request)

Each complex case's ADR lives inside its case folder as `01-adr-*.md`, not as a standalone top-level
`adrs/ADR-0NN-*.md` file — the previous version of this inventory pointed at file paths that never
existed. Page title = the ADR's own H1. Publish once a case is actually being reviewed for
ratification, not preemptively.

| Case | ADR source | Status (check `output/complexStories/{case}/00-overview.md`) |
|---|---|---|
| ACL mid-request update | `output/complexStories/acl/01-adr-acl-mid-request-update.md` | — |
| Non-atomic write saga | `output/complexStories/non-atomic-write-saga/01-adr-non-atomic-write-saga.md` | — |
| TechPack aggregate | `output/complexStories/techpack/01-adr-techpack.md` | — |
| Partner drop/undrop write | `output/complexStories/partner-drop-undrop-write/01-adr-partner-drop-undrop.md` | — |
| Not-removable / undroppable partners | `output/complexStories/notRemovable-undroppable-partners/01-adr-notremovable-undroppable-partners.md` | — |
| Attachments enrichment | `output/complexStories/attachments-enrichment/01-adr-attachments-enrichment.md` | — |
| Components & counts rollups | `output/complexStories/components-and-counts-rollups/01-adr-components-counts-rollups.md` | — |
| Polymorphic type resolution | `output/complexStories/polymorphic-type-resolution/01-adr-polymorphic-type-resolution.md` | — |
| Cross-domain association & hydration | `output/complexStories/cross-domain-association/01-adr-cross-domain-association.md` | — |

> Check each case's `00-overview.md` for current ratification status before publishing/re-syncing —
> this table intentionally doesn't cache a status column since it drifts fast; read it live.

## 6. Deliberately not published to Confluence

| Artifact | Destination instead |
|---|---|
| `finalArtifacts/jira/{domain}.csv`, `all-stories.csv` | Jira, via the Jira publish prompts |
| `output/analysis/**` (`be-01`…`be-07`, `be-04-stories.md`) | Source of truth — stays in GitHub; every published page links back to it there, never duplicates its content |
| `.docx` variants | Distribution copies; attach to a page only if a stakeholder specifically needs Word |
| `output/complexStories/**/01-stories.md`, `implementation/`, case CSVs | Engineering working files; the case CSV imports to Jira under its home stub story |
| `output/clientStoryDependency/*.md` (per-FE-story field-dependency reports) | Working detail behind `story-dependency-graph-{domain}.md` — link to it on GitHub from the FE-Readiness page if a reader needs the field-level detail |

## Publication rules (summary)

1. Update by exact title — never create duplicates; keep titles stable across re-syncs.
2. Formatting preserved end-to-end: tables, headings, emphasis, code, checklists, quotes, emoji,
   mermaid diagrams (as a code macro carrying the full diagram source, not a prose description).
3. Repository references become GitHub links (`https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/...`)
   — never a local file path. Story IDs stay as plain text.
4. Publish order: space home → Program roll-ups → Domains (breakdown, then FE-readiness) → deep-dive
   tier and Architecture ADRs on request only.
5. After each domain's breakdown page is published, record its URL in
   `finalArtifacts/jira/confluence-page-map.csv` — the Jira publish prompts read this file to link
   each story back to its domain's Confluence page. Publish Confluence before Jira for a first import.
