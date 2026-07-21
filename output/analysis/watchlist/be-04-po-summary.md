# Phase 4: PO Sprint Planning Summary — Watchlist

> **Domain:** `watchlist` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [be-04-stories.md](./be-04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

- We are moving the **Watchlist** domain — quality watchlist entries on a product (reasons, statuses, inspections, partners, attachments) — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **small and mid-low risk**: 4 queries, 3 mutations, 13 field resolvers on a 129-line resolver, with **no polymorphism**.
- It is **co-located** in the product family, so `Product.watchlists` and the TechPack `ResourcesCount.watchlists` count resolve **internally** (not across the federation gateway).

The one genuinely harder piece is **`updateWatchlistEntries`**, a multi-step write (user-group upsert, then
the body, then attachment archival) that today **does not await** its per-entry user-group updates — a race
to fix on the port.

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive step in `updateWatchlistEntries`) use **Mid-Request ACL Update** before the downstream call.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 4 | 2 cacheable master-data; 1 four-step filtered read |
| Mutations | 3 | 2 simple + `updateWatchlistEntries` (multi-step) |
| Field-resolver type blocks | 3 | `Watchlist` (10), inspection (2), partner (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 2 (Product, ResourcesCount) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 3 | 3–6d |
| C | Search & Listing | 1 | 3–5d |
| D | Mutations (simple) | 2 | 4–7d |
| E | Complex (`updateWatchlistEntries`) | 1 | 4–7d |
| F | Federation (Product + TechPack, internal) | 2 | 2–4d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **13** | **25–44d** (buffered) |

> One engineer ≈ **5–9 sprints**.

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B-01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateWatchlistEntries` un-awaited user-group update (race) | 🟡 Medium-High | Real bug today; fix to await on the port + decide failure strategy |
| `getWatchlistByFilter` 4-step chain | 🟡 Medium | Performance-sensitive; cache the product lookup |
| Product `PRODUCT-BE-F-08` mislabelled watchlist as a separate subgraph | 🟢 Low | Corrected — it's an **internal** contribution (like bom/measurement) |
| Attachment/search field resolvers | 🟢 Low | Shared search helper |
| DataLoader missing on F-01 field resolver | 🟡 Medium | N+1 risk when parent returns list; add `watchlistByProductIdLoader` to F-01 AC |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateWatchlistEntries` — await user-group upserts + failure strategy | E-01 | Tech Lead + PO |
| 2 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Dependency Map
```
plm-product (Watchlist subgraph) depends on:
 spark-product backend REST .../watchlist/v1
 sibling DGS (federation): attachment, search 🔴, workspace, user-profile, user-group
 Hive Gateway → VMM (partner names)
 internal (same DGS): product
 cross-domain blockers:
   E-01 (updateWatchlistEntries) depends on PRODUCT-BE-E-00 (WriteSaga shared module)
 product domain F-01 Product.watchlists ; F-02 ResourcesCount.watchlists (both internal)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01 + D-01/D-02 | filtered read + simple mutations |
| 3 | E-01 + F-01/F-02 | multi-step update + Product/TechPack internal contributions |
| 4 | G-01–G-03, G-05 (recommended, PO-gated) | field resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

---
*Pipeline 2.0 — Phase 4 complete. Watchlist artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*
