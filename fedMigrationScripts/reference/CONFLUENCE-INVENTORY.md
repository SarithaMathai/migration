# Confluence publication inventory

The complete list of pages the migration program publishes to Confluence, with the exact title, source file,
and parent location for each. This is the checklist the MCP push (see
[`PUSH-TO-JIRA-CONFLUENCE.md`](../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md)) works through;
formatting is preserved per the rules in that runbook. Pages update in place by exact title on re-sync.

**Totals: 41 core pages** — 1 space home · 26 domain pages (13 domains × 2) · 2 program pages · 4 ADRs ·
8 complex cases (+ 7 optional per-case architecture children = 48).

## 1. Space home

| Title | Source | Content |
|---|---|---|
| Spark → Federated GraphQL Migration — Program Overview | `output/summary/00-program-overview.md` | Executive summary + portfolio: scope, the 13 domains, the 6 program spikes, sequencing |

## 2. Federation Graph Migration ▸ Domains — two pages per domain (26)

Titles follow one convention: `{Domain} — Federated GraphQL Breakdown` (engineering/PO story breakdown) and
`{Domain} — Migration PO Review` (decision list for the product owner).

| Domain | Breakdown page (source) | PO review page (source) |
|---|---|---|
| Attachment | `output/summary/attachment/FederatedGqlBrakDown-attachment.md` | `output/summary/attachment/attachment-po-review.md` |
| BOM | `output/summary/bom/FederatedGqlBrakDown-bom.md` | `output/summary/bom/bom-po-review.md` |
| Claims | `output/summary/claims/FederatedGqlBrakDown-claims.md` | `output/summary/claims/claims-po-review.md` |
| Discussion | `output/summary/discussion/FederatedGqlBrakDown-discussion.md` | `output/summary/discussion/discussion-po-review.md` |
| Impression | `output/summary/impression/FederatedGqlBrakDown-impression.md` | `output/summary/impression/impression-po-review.md` |
| Measurement | `output/summary/measurement/FederatedGqlBrakDown-measurement.md` | `output/summary/measurement/measurement-po-review.md` |
| Packaging | `output/summary/packaging/FederatedGqlBrakDown-packaging.md` | `output/summary/packaging/packaging-po-review.md` |
| Product | `output/summary/product/FederatedGqlBrakDown-product.md` | `output/summary/product/product-po-review.md` |
| Product Details | `output/summary/productDetails/FederatedGqlBrakDown-productDetails.md` | `output/summary/productDetails/productDetails-po-review.md` |
| Sample | `output/summary/sample/FederatedGqlBrakDown-sample.md` | `output/summary/sample/sample-po-review.md` |
| Search | `output/summary/search/FederatedGqlBrakDown-search.md` | `output/summary/search/search-po-review.md` |
| Watchlist | `output/summary/watchlist/FederatedGqlBrakDown-watchlist.md` | `output/summary/watchlist/watchlist-po-review.md` |
| Workspace | `output/summary/workspace/FederatedGqlBrakDown-workspace.md` | `output/summary/workspace/workspace-po-review.md` |

Each breakdown page contains: the domain's story list by phase (A–G) with acceptance criteria, the spike-gated
stories flagged with their program spike, complexity/T-shirt sizing, and dependency mapping. Each PO review
contains: scope summary, key risk areas, and the decisions the PO owns.

## 3. Federation Graph Migration ▸ Program — the roll-up pages (2)

| Title | Source | Content |
|---|---|---|
| Federated GraphQL Stories — Breakdown (All Domains) | `output/summary/Federated+Graphql+Stories+-+BreakDown.md` | The global page: program spike register (with ADR-012…015 status), spike details, all-domain story roll-up |
| Federated GraphQL Stories — Breakdown (Selected Modules) | `output/summary/Federated+Graphql+Stories+-+BreakDown_custom.md` | The same page scoped to the eight selected modules: product, bom, claims, productDetails, packaging, watchlist, measurement, impression |

## 4. Federation Graph Migration ▸ Architecture — decision records (4)

| Title | Source |
|---|---|
| ADR-012 — Non-Atomic Write Failure Strategy | `adrs/ADR-012-non-atomic-write-failure-strategy.md` |
| ADR-013 — Partner Drop/Undrop Write Orchestration | `adrs/ADR-013-partner-drop-undrop-write-orchestration.md` |
| ADR-014 — Cross-Domain Association & Hydration | `adrs/ADR-014-cross-domain-association-hydration.md` |
| ADR-015 — Polymorphic Type Resolution Playbook | `adrs/ADR-015-polymorphic-type-resolution-playbook.md` |

The earlier decision documents (ADR-010, ADR-011, TechPack, Color-on-Fabric, PLM Federation Architecture) are
PDF/DOC attachments — attach to the Architecture parent rather than converting.

## 5. Federation Graph Migration ▸ Architecture ▸ Complex Cases (8, + 7 optional children)

Page title = the case's `00-overview.md` H1. Optional child page per case from its `ARCHITECTURE.md`
(seven carry an explicit Confluence-location tag; cross-domain-association's is a companion note).

| Title (from H1) | Case folder | Optional architecture child |
|---|---|---|
| Complex Story — Non-atomic multi-step writes (the saga / compensation pattern) | `output/complexStories/non-atomic-write-saga/` | ✓ |
| Complex Story — Product Tech Pack (getProductTechPack) | `output/complexStories/techpack/` | ✓ |
| Complex Story — Partner DROP / UNDROP / REMOVE write (productBusinessPartnerActions / workspaceBusinessPartnerActionsV2) | `output/complexStories/partner-drop-undrop-write/` | ✓ |
| Complex Story — notRemovablePartnerIds & unDroppablePartners | `output/complexStories/notRemovable-undroppable-partners/` | ✓ |
| Complex Story — attachmentsWithMetaData enrichment (Product + Workspace) | `output/complexStories/attachments-enrichment/` | ✓ |
| Complex Story — Product.components + WorkspaceV2.counts rollups | `output/complexStories/components-and-counts-rollups/` | ✓ |
| Complex Story — Polymorphic type resolution (@DgsTypeResolver + per-variant + prefix-gated parents) | `output/complexStories/polymorphic-type-resolution/` | ✓ |
| Complex Story — Cross-domain association & hydration (SPIKE-06) | `output/complexStories/cross-domain-association/` | companion note only |

## 6. Deliberately not published to Confluence

| Artifact | Destination instead |
|---|---|
| `output/jira/*.csv` (343 issues) | Jira, via the push runbook |
| `output/summary/{domain}/{domain}-comprehensive.md` | Working reference — publish on request only (large; the breakdown page is the Confluence face) |
| `output/initial-analysis/**` | Source analyses — remain in the repository (pages link to them on GitHub) |
| `.docx` variants | Distribution copies; attach to pages only if a stakeholder needs Word |
| `output/complexStories/**/01-stories.md`, `implementation/`, case CSVs | Engineering working files; the case CSV imports to Jira under its home stub |

## Publication rules (summary)

1. Update by exact title — never create duplicates; keep titles stable across re-syncs.
2. Formatting preserved end-to-end: tables, headings, emphasis, code, checklists, quotes, emoji.
3. Repository references become GitHub links; story IDs stay as text (Jira macro links them by label).
4. Publish order: space home → Domains → Program → Architecture (ADRs, then cases).
