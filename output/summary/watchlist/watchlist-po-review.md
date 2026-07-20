# Watchlist — Migration to the `plm-product` DGS (PO view)

> 🏷️ **Tags:** `dgs-migration` · `po-page` · `domain-watchlist` · `pipeline-v2`  —  **Confluence location:** *Federation Graph Migration ▸ Domains ▸ watchlist*

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.  
> Deep dives: migration approach & schema · field inventory · engineering stories.  
> Create tickets from `../finalOutput/jira/watchlist.csv`. Effort is **AI-estimated — confirm in refinement.**

---

## What are we building?

- We are moving the **Watchlist** domain — quality watchlist entries on a product (reasons, statuses, inspections, partners, attachments) — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **small and mid-low risk**: 4 queries, 3 mutations, 13 field resolvers on a 129-line resolver, with **no polymorphism**.
- It is **co-located** in the product family, so `Product.watchlists` and the TechPack `ResourcesCount.watchlists` count resolve **internally** (not across the federation gateway).

The one genuinely harder piece is **`updateWatchlistEntries`**, a multi-step write (user-group upsert, then
the body, then attachment archival) that today **does not await** its per-entry user-group updates — a race
to fix on the port.

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive step in `updateWatchlistEntries`) use **Mid-Request ACL Update** before the downstream call.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 4 | 2 cacheable master-data; 1 four-step filtered read |
| Mutations | 3 | 2 simple + `updateWatchlistEntries` (multi-step) |
| Field-resolver type blocks | 3 | `Watchlist` (10), inspection (2), partner (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 2 (Product, ResourcesCount) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

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


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateWatchlistEntries` — await user-group upserts + failure strategy | E-01 | Tech Lead + PO |
| 2 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Migration approach (summary)

**B** Core Reads; **C** Search & Listing; **D** Mutations (simple); **E** Complex (`updateWatchlistEntries`); **F** Federation (Product + TechPack, internal); **G** Field Resolvers & Tests. Full detail: `be-03-schema-analysis.md §Migration Approach`.

## Sequencing & capacity

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01 + D-01/D-02 | filtered read + simple mutations |
| 3 | E-01 + F-01/F-02 | multi-step update + Product/TechPack internal contributions |
| 4 | G-01–G-03, G-05 (recommended, PO-gated) | field resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

---
*PO review assembled from the `watchlist` analysis. Jira tickets: `finalOutput/jira/watchlist.csv`. Full engineering detail: `watchlist-comprehensive.md` (same folder).*