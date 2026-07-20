# Claims — Migration to the `spark-claims` DGS (PO view)

> 🏷️ **Tags:** `dgs-migration` · `po-page` · `domain-claims` · `pipeline-v2`  —  **Confluence location:** *Federation Graph Migration ▸ Domains ▸ claims*

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.  
> Deep dives: migration approach & schema · field inventory · engineering stories.  
> Create tickets from `../finalOutput/jira/claims.csv`. Effort is **AI-estimated — confirm in refinement.**

---

## What are we building?

We are moving the **Claims** domain — a product's marketing/technical claims (claim details, guest-facing
copy, substantiation, per-partner access, exports) — off the `spark-internal-graphql` gateway into its
**own `claims` DGS subgraph**. Unlike BOM/Measurement/ProductDetails, claims is **not** part of the
plm-product monorepo, so its links to Product, search, workspace, user-profile and VMM are all
**cross-subgraph** (federation / gateway stitch), and it **contributes** the `Product.claims` field and the
TechPack `ResourcesCount.claims` count back to plm-product.

It is **mid-sized and mid-risk**: 7 queries, 6 mutations, 17 field resolvers on a 164-line resolver, with
**no polymorphism**. The one genuinely harder piece is **`updateClaim`**, a multi-step write that uses the
**proxy/external ACL** path plus workspace association, with no rollback today.

**ACL note:** the current code obtains capability tokens via ACL (including the proxy variant for update);
Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites — where a resolver hands its token to a *different* domain's loader — use **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before the downstream call.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateClaim` (proxy-ACL multi-step) |
| Field-resolver type blocks | 4 | `Claims` (11), `ParentDetails` (3), substantiate (1), claimDetails (1) |
| External dependencies | 6 keys (1 🔴 · 3 🟡 · 2 🔵) | search 🔴; product/user-profile/workspace 🟡 |
| Federation contributions | 2 (Product.claims, ResourcesCount.claims) | BLOCKED-BY product |
| **Total stories** | **20** | green-field; separate subgraph |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 5 | 5–9d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateClaim`) | 1 | 4–7d |
| F | Federation Contributions | 2 | 4–7d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 5 | 12–20d |
| **Total** | | **20** | **36–62d** (buffered) |

> One engineer ≈ **8–13 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateClaim` failure strategy (proxy ACL + workspace + body) | E-01 | Tech Lead + PO |
| 2 | `bulkUpdateClaim` — confirm response should be camelCase | D-02 | Backend Eng |
| 3 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Migration approach (summary)

**B** Core Reads; **C** Search & Listing; **D** Mutations (simple); **E** Complex (`updateClaim`); **F** Federation Contributions; **G** Field Resolvers & Tests. Full detail: `be-03-schema-analysis.md §Migration Approach`.

## Sequencing & capacity

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~9–15 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel after B-01 |

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-05 | search + simple mutations |
| 3 | E-01 + G-01/G-02 | `updateClaim` + ACL/partner field resolvers |
| 4 | G-03/G-04 + G-06 | parent/elastic + misc fields + shared value-type alignment |
| post-launch | H-01, H-02 | federation contributions (unblocked by product) |

## Phase 2 Story Breakdowns

One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.

| Parent milestone | Original size | Sub-tasks |
|---|---|---|
| `CLAIM-BE-E-01` updateClaim (proxy ACL + workspace + body) | High | E-01-1 body PUT + workspace call · E-01-2 ACL proxy + orchestration |

> In Jira, sub-tasks appear **nested under** their parent story. Sprint capacity: each sub-task = M (3–5 days).

---
*PO review assembled from the `claims` analysis. Jira tickets: `finalOutput/jira/claims.csv`. Full engineering detail: `claims-comprehensive.md` (same folder).*