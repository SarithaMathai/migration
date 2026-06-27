# Watchlist — Migration to the `plm-product` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../watchlist/03-schema-analysis.md) ·
> [field inventory](../watchlist/05-attribute-inventory.md) · [engineering stories](../watchlist/04-stories.md).
> Create tickets from [`../jira/watchlist.csv`](../jira/watchlist.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Watchlist** domain — quality watchlist entries on a product (reasons, statuses,
inspections, partners, attachments) — off the `spark-internal-graphql` gateway into the **`plm-product`**
DGS. It is **small and mid-low risk**: 4 queries, 3 mutations, 13 field resolvers on a 129-line resolver,
with **no polymorphism**. It is **co-located** in the product family, so `Product.watchlists` and the
TechPack `ResourcesCount.watchlists` count resolve **internally** (not across the federation gateway).

> **Note:** this corrects a prior inconsistency — product's `SPARK-PROD-F08` (the TechPack `watchlists`
> count) was labelled a *separate-subgraph* federation contribution; watchlist is **co-located**, so it's an
> **internal** contribution like bom and measurement. Product's artifacts have been updated.

The one genuinely harder piece is **`updateWatchlistEntries`**, a multi-step write (user-group upsert, then
the body, then attachment archival) that today **does not await** its per-entry user-group updates — a race
to fix on the port.

**ACL note:** the current code obtains per-resource capability tokens via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 4 | 2 cacheable master-data; 1 four-step filtered read |
| Mutations | 3 | 2 simple + `updateWatchlistEntries` (multi-step) |
| Field-resolver type blocks | 3 | `Watchlist` (10), inspection (2), partner (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 2 (Product, ResourcesCount) | **internal** (co-located) |
| **Total stories** | **17** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 7–11d |
| B | Core Reads | 3 | 3–6d |
| C | Search & Listing | 1 | 3–5d |
| D | Mutations (simple) | 2 | 4–7d |
| E | Complex (`updateWatchlistEntries`) | 1 | 4–7d |
| F | Federation (Product + TechPack, internal) | 2 | 2–4d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **17** | **32–55d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateWatchlistEntries` un-awaited user-group update (race) | 🟡 Medium-High | Real bug today; fix to await on the port + decide failure strategy |
| `getWatchlistByFilter` 4-step chain | 🟡 Medium | Performance-sensitive; cache the product lookup |
| Product `SPARK-PROD-F08` mislabelled watchlist as a separate subgraph | 🟢 Low | Corrected — it's an **internal** contribution (like bom/measurement) |
| Attachment/search field resolvers | 🟢 Low | Shared search helper |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateWatchlistEntries` — await user-group upserts + failure strategy | E01 | Tech Lead + PO |
| 2 | Are the 2 unused version service methods needed cross-domain? | A04 | Tech Lead |

## Migration approach (summary)

Phase **A** schema + `WatchlistService` port (base `watchlist/v1`); **B** the 3 simple reads (2 cacheable);
**C** the 4-step `getWatchlistByFilter`; **D** create + clone-files; **E** the multi-step
`updateWatchlistEntries` (fix the await race); **F** `Product.watchlists` + `ResourcesCount.watchlists`
(internal); **G** field resolvers (computed flatteners, users/workspace/participants/partner, attachments,
product) + tests. Full detail:
[03-schema-analysis.md §Migration Approach](../watchlist/03-schema-analysis.md).

## Sequencing & capacity

One engineer ≈ 6–11 sprints; 2 engineers ≈ 4–6. Full plan: [04-po-summary.md](../watchlist/04-po-summary.md).

---
*PO page assembled from the watchlist analysis. Tickets:
[`../jira/watchlist.csv`](../jira/watchlist.csv) · [`../jira/watchlist-stories.md`](../jira/watchlist-stories.md).*
