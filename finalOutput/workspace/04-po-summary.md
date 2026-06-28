# Phase 4: PO Sprint Planning Summary — Workspace

> **Domain:** `workspace` · **Target DGS:** separate `plm-workspace` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

We are moving the **Workspace** domain — the seasonal/working containers that group products, samples,
teams, partners, attachments and discussions — off the `spark-internal-graphql` gateway into its **own
`plm-workspace` DGS subgraph**. Workspace is a **hub**: nearly every product-family domain references a
`WorkspaceV2`, and workspace itself reaches into product, search, discussion, sample, combination,
attachment, relationship and access-control.

It is **large and high-risk**: 8 queries, 10 mutations (+2 schema-drift wrappers), ~25 field resolvers on a
1,060-line resolver. The cost and risk concentrate in three places: the **`workspaceBusinessPartnerActionsV2`**
drop/undrop dispatcher (5 cases, manual compensation, and **un-awaited promise chains** to fix), and the two
heavy field resolvers **`attachmentsWithMetaData`** and **`counts`** (the workspace product dashboard).

**ACL note:** ACL authorization is ignored in the DGS implementation; **but** the drop/undrop **resource
bookkeeping** (which resources get dropped/undropped) IS real build work — it is data maintenance, not auth.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 8 | 2 paged elastic; product/search-backed lookups |
| Mutations | 10 (+2 deferred) | incl. the partner-action dispatcher + 3 exports |
| Field-resolver type blocks | ~3 | `WorkspaceV2` (~22), `WorkspaceDepartmentV2`, paged |
| External dependencies | 14 keys (all cross-subgraph) | search/product/attachment 🔴 |
| Federation role | provides `WorkspaceV2` entity | every product-family domain references it |
| **Total stories** | **32** | green-field; separate subgraph |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 4 | 12–20d |
| B | Core Reads | 6 | 8–14d |
| C | Search & Listing | 2 | 5–9d |
| D | Mutations (simple) | 9 | 16–27d |
| E | Complex (partner-action dispatcher) | 1 | 8–13d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 8 | 34–56d |
| **Total** | | **32** | **87–146d** (buffered) |

> One engineer ≈ **17–29 sprints**. Heavily parallelizable after A; 2–3 engineers recommended.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| Partner-action dispatcher (E01) | 🔴 High | 5-case drop/undrop with manual compensation + **un-awaited chains** (real bug); needs a failure strategy |
| `attachmentsWithMetaData` / `counts` (G01/G02) | 🟡 Medium-High | Large, performance-sensitive; budget X-Large |
| Cross-subgraph coupling to product | 🟡 Medium | `products`/`addResources` call product directly today; needs entity refs / a product client |
| Schema-drift drop/undrop wrappers | 🟢 Low | Survey live consumers before deleting |
| `WORKSPACE_PACKAGING_TAG_ID` env dependency | 🟢 Low | Move to config; fail fast if unset |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `workspaceBusinessPartnerActionsV2` failure strategy + await the fire-and-forget chains | E01 | Tech Lead + PO |
| 2 | Delete or `@deprecated` the 2 drop/undrop drift wrappers | F02 | PO |
| 3 | `products`/`addResources` — federated entity reference vs a product client | D04/G04 | Architect |

## Dependency Map
```
plm-workspace (Workspace subgraph) depends on (all cross-subgraph):
  search 🔴 (paged/elastic, discussions/teams/combinations/samples, exports)
  product 🔴 (workspace products, page, view-toggle, status cleanup)
  attachment 🔴 ; discussion, sampleV2, combination, relationship, tag, user-profile 🟡
  Hive Gateway → VMM, IG, Brand ; exportHub, favorite ; access-control (drop/undrop bookkeeping)
  provides → WorkspaceV2 entity for product/bom/measurement/impression/productDetails/packaging/claims/watchlist
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | A01–A04 + B01–B06 | schema, service port, reads |
| 3 | C01/C02 + D06–D09 | paged search + teams + exports |
| 4 | D01–D05 | create/update/change + resource add/remove |
| 5–6 | E01 | partner-action dispatcher (focused) |
| 7–8 | G01–G04 | the heavy field resolvers (X-Large) |
| 9 | G05–G07 | partners/hierarchy/users/computed |
| 10 | F01/F02 + G08 | entity fetcher + drift decision + tests |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~17–29 sprints | sequential — not recommended |
| 2 engineers | ~10–17 sprints | B/C/D parallel after A |
| 3 engineers | ~7–11 sprints | critical path A → E01 → G01/G02 → G08 |

---
*Pipeline 2.0 — Phase 4 complete. Workspace artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Separate `plm-workspace` subgraph.*
