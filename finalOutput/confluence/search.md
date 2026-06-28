# Search — Migration to a dedicated `plm-elastic-search` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../search/03-schema-analysis.md) ·
> [field inventory](../search/05-attribute-inventory.md) · [engineering stories](../search/04-stories.md).
> Create tickets from [`../jira/search.csv`](../jira/search.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Search** domain — the elastic-backed read layer behind every search box, listing,
suggestion, count and report — off the `spark-internal-graphql` gateway into its **own `plm-elastic-search`
DGS subgraph**. Search is the program **read hub**: nearly every other domain calls it (the 🔴 `search`
dependency across product/bom/measurement/packaging/productDetails/claims/watchlist/workspace).

It is **breadth-dominated**: ~48 mostly-thin elastic-wrapper queries + 1 mutation, but a **large result-type
surface** (~50 types) and heavy **enrichment field resolvers** that re-hydrate hits from product, vmm, ig,
tag, brand, workspace, user, attachment, fabric and color. Low orchestration risk; the cost is surface area.

**ACL note:** a few proxy reads curry capability tokens; **ACL is ignored in the DGS implementation** — context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | ~48 | grouped into 10 search-family stories (Phase C) |
| Mutations | 1 | `sendBulkCombinationUpdates` |
| Result/value types | ~50 | the biggest single task (A02) |
| Field-resolver type blocks | ~12 | `SearchAttachment`, `Material`, combination/palette/watchlist/component, access/report/paging |
| External dependencies | ~14 keys | all cross-subgraph enrichment |
| Federation role | the program **read hub** | every domain calls it |
| **Total stories** | **25** | green-field; separate subgraph |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 14–24d |
| B | Core Reads | 3 | 3–6d |
| C | Search & Listing (by family) | 10 | 24–40d |
| D | Mutations | 1 | 1–2d |
| F | Federation & ownership | 1 | 3–5d |
| G | Field Resolvers & Tests | 6 | 28–46d |
| **Total** | | **25** | **73–123d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| Read-hub cutover | 🔴 High | Every domain depends on search — migrate early or dual-run; sequence dependents |
| Type-surface breadth (A02) | 🟡 Medium-High | ~50 result types — easy to under-scope; guard with schema-conformance CI |
| Enrichment field resolvers (G01/G02) | 🟡 Medium | Fan out to many subgraphs; needs DataLoader batching |
| Ownership drift | 🟢 Low | A few queries have no resolver / are resolved in workspace — reconcile (F01) |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Read-hub migration ordering (early vs dual-run during dependents' cutover) | all | Tech Lead + Platform |
| 2 | `searchProducts` (no resolver) vs `searchProductsES` (not in SDL) — which to keep | F01/C06 | Architect |
| 3 | Owner for `searchSPG/Users/TeamsSuggestions` + the 2 workspace-resolved suggestions | F01/C09 | Architect |
| 4 | Scope of A02 — expand all `JSON`-placeholder value types to concrete SDL types | A02 | Architect |

## Migration approach (summary)

Phase **A** schema (the ~50-type surface is the biggest task) + `SearchService` port (~80 elastic builders →
grouped clients); **B** by-id/counts; **C** the search families (one story each: attachments, materials,
samples, teams, templates, products, combinations/palettes, misc, suggestions, reports); **D** the bulk
combination mutation; **F** gateway composition + ownership reconciliation; **G** the per-result-type
enrichment field resolvers + tests/conformance CI. Full detail:
[03-schema-analysis.md §Migration Approach](../search/03-schema-analysis.md).

## Sequencing & capacity

Families parallelize after A. One engineer ≈ 15–25 sprints; 3 engineers ≈ 6–10. **Sequence the read-hub
cutover** so dependents' search calls keep resolving. Full plan: [04-po-summary.md](../search/04-po-summary.md).

---
*PO page assembled from the search analysis. Tickets:
[`../jira/search.csv`](../jira/search.csv) · [`../jira/search-stories.md`](../jira/search-stories.md).*
