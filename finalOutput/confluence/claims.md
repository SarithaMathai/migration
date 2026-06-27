# Claims — Migration to a dedicated `claims` DGS subgraph (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../claims/03-schema-analysis.md) ·
> [field inventory](../claims/05-attribute-inventory.md) · [engineering stories](../claims/04-stories.md).
> Create tickets from [`../jira/claims.csv`](../jira/claims.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Claims** domain — a product's marketing/technical claims (claim details, guest-facing
copy, substantiation, per-partner access, exports) — off the `spark-internal-graphql` gateway into its
**own `claims` DGS subgraph**. Unlike BOM/Measurement/ProductDetails/Packaging, claims is **not** part of
the plm-product monorepo, so its links to Product, search, workspace, user-profile and VMM are all
**cross-subgraph**, and it **contributes** the `Product.claims` field and the TechPack
`ResourcesCount.claims` count back to plm-product.

It is **mid-sized and mid-risk**: 7 queries, 6 mutations, 17 field resolvers on a 164-line resolver, with
**no polymorphism**. The one genuinely harder piece is **`updateClaim`**, a multi-step write that uses the
**proxy/external ACL** path plus workspace association, with no rollback today.

**ACL note:** the current code obtains capability tokens via ACL (including the proxy variant for update);
**ACL is ignored in the DGS implementation** (no ACL story) — noted for context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateClaim` (proxy-ACL multi-step) |
| Field-resolver type blocks | 4 | `Claims` (11), `ParentDetails` (3), substantiate (1), claimDetails (1) |
| External dependencies | 6 keys (1 🔴 · 3 🟡 · 2 🔵) | search 🔴; product/user-profile/workspace 🟡 |
| Federation contributions | 2 (Product.claims, ResourcesCount.claims) | BLOCKED-BY product |
| **Total stories** | **24** | green-field; separate subgraph |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 8–13d |
| B | Core Reads | 5 | 5–9d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateClaim`) | 1 | 4–7d |
| F | Federation Contributions | 2 | 4–7d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 5 | 12–20d |
| **Total** | | **24** | **44–75d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateClaim` proxy-ACL multi-step write | 🟡 Medium | Needs a decision (E01) on recovering from a mid-write failure |
| `bulkUpdateClaim` snake-cases its response (likely bug) | 🟡 Medium | Fix to camelCase on the port; parity test |
| `businessPartner` 3-way fallback (incl. a "Target" id-0 case) | 🟢 Low | Preserve exactly; unit-test each branch |
| `ParentDetails` elastic team/BP lookups | 🟢 Low | Preserve empty handling; paginate |
| Federation contributions wait on product | 🟢 Low | F01/F02 post-launch; not on the critical path |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateClaim` failure strategy (proxy ACL + workspace + body) | E01 | Tech Lead + PO |
| 2 | `bulkUpdateClaim` — confirm response should be camelCase | D02 | Backend Eng |
| 3 | Are the 2 unused version service methods needed cross-domain? | A04 | Tech Lead |

## Migration approach (summary)

Phase **A** schema + `ClaimService` port; **B** the 5 simple reads (2 cacheable); **C** guest-facing + elastic
search; **D** simple mutations; **E** the proxy-ACL multi-step `updateClaim`; **F** contribute `Product.claims`
+ TechPack `ResourcesCount.claims` (federation, blocked by product); **G** field resolvers (ACL, users, the
`businessPartner` fallback, `ParentDetails` elastic lookups) + tests. Full detail:
[03-schema-analysis.md §Migration Approach](../claims/03-schema-analysis.md).

## Sequencing & capacity

One engineer ≈ 9–15 sprints; 2 engineers ≈ 5–8. Federation contributions are post-launch. Full plan:
[04-po-summary.md](../claims/04-po-summary.md).

---
*PO page assembled from the claims analysis. Tickets:
[`../jira/claims.csv`](../jira/claims.csv) · [`../jira/claims-stories.md`](../jira/claims-stories.md).*
