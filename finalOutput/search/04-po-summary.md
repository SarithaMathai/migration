# Phase 4: PO Sprint Planning Summary — Search

> **Domain:** `search` · **Target DGS:** separate `plm-elastic-search` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

We are moving the **Search** domain — the elastic-backed read layer that powers every search box, listing,
suggestion, count and report across the PLM app — off the `spark-internal-graphql` gateway into its **own
`plm-elastic-search` DGS subgraph**. Search is the **read hub**: nearly every other domain calls it (the
🔴 `search` dependency you see throughout product/bom/measurement/packaging/productDetails/claims/watchlist/
workspace).

It is **breadth-dominated**: ~48 mostly-thin elastic-wrapper queries + 1 mutation, but a **large result-type
surface** (~50 types) and heavy **enrichment field resolvers** that re-hydrate hits from product, vmm, ig,
tag, brand, workspace, user, attachment, fabric and color. Low orchestration risk; the cost is surface area.

**ACL note:** a few proxy reads curry capability tokens; **ACL is ignored in the DGS implementation** — context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | ~48 | grouped into 10 search-family stories (Phase C) |
| Mutations | 1 | `sendBulkCombinationUpdates` |
| Result/value types | ~50 | the biggest single task (A02) |
| Field-resolver type blocks | ~12 | `SearchAttachment`, `Material`, combination/palette/watchlist/component, access/report/paging |
| External dependencies | ~14 keys | all cross-subgraph enrichment |
| Federation role | the program **read hub** | every domain calls it |
| **Total stories** | **25** | green-field; separate subgraph |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 4 | 14–24d |
| B | Core Reads | 3 | 3–6d |
| C | Search & Listing (by family) | 10 | 24–40d |
| D | Mutations | 1 | 1–2d |
| F | Federation & ownership | 1 | 3–5d |
| G | Field Resolvers & Tests | 6 | 28–46d |
| **Total** | | **25** | **73–123d** (buffered) |

> One engineer ≈ **15–25 sprints**. Parallelizable by family after A.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| Type-surface breadth (A02) | 🟡 Medium-High | ~50 result types — easy to under-scope; guard with schema-conformance CI |
| Enrichment field resolvers (G01/G02) | 🟡 Medium | Fan out to many subgraphs; needs DataLoader batching |
| Read-hub cutover | 🔴 High | Every domain depends on search — migrate early or dual-run; sequence dependents |
| Ownership drift | 🟢 Low | A few queries have no resolver / are resolved in workspace — reconcile (F01) |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Read-hub migration ordering (early vs dual-run during dependents' cutover) | all | Tech Lead + Platform |
| 2 | `searchProducts` (no resolver) vs `searchProductsES` (not in SDL) — which to keep | F01/C06 | Architect |
| 3 | Owner for `searchSPG/Users/TeamsSuggestions` (no resolver) + the 2 workspace-resolved suggestions | F01/C09 | Architect |
| 4 | Scope of A02 — expand all `JSON`-placeholder value types to concrete SDL types | A02 | Architect |

## Dependency Map
```
plm-elastic-search (Search subgraph) is the READ HUB. It enriches elastic hits from (cross-subgraph):
  product, bom, workspace, sample, attachment, user-profile, user-group, fabric, color, adminTools
  Hive Gateway → VMM, IG, Brand, Tag
  consumed by → product, bom, measurement, packaging, productDetails, claims, watchlist, workspace (their `search` calls)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | A01–A04 | schema (type surface) + service port |
| 3 | B01–B03 + C01 | by-id/counts + attachments |
| 4 | C02/C03 | material + sample families |
| 5 | C04–C06 | team/template/product families |
| 6 | C07–C10 + D01 | combination/palette/misc/suggestions/reports + mutation |
| 7 | G01/G02 | the two heavy enrichment blocks |
| 8 | G03–G05 + F01 | remaining enrichment + gateway/ownership |
| 9 | G06 | tests, parity, conformance CI |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~15–25 sprints | sequential |
| 2 engineers | ~9–15 sprints | families parallel after A |
| 3 engineers | ~6–10 sprints | A02/A04 → families → enrichment in parallel |

---
*Pipeline 2.0 — Phase 4 complete. Search artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Separate `plm-elastic-search` subgraph — the program read hub.*
