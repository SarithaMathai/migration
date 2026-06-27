# Phase 4: PO Sprint Planning Summary — Claims

> **Domain:** `claims` · **Target DGS:** separate `claims` subgraph (repo `spark-claims`) · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

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
**ACL is ignored in the DGS implementation** (no ACL story) — noted for context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateClaim` (proxy-ACL multi-step) |
| Field-resolver type blocks | 4 | `Claims` (11), `ParentDetails` (3), substantiate (1), claimDetails (1) |
| External dependencies | 6 keys (1 🔴 · 3 🟡 · 2 🔵) | search 🔴; product/user-profile/workspace 🟡 |
| Federation contributions | 2 (Product.claims, ResourcesCount.claims) | BLOCKED-BY product |
| **Total stories** | **24** | green-field; separate subgraph |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 4 | 8–13d |
| B | Core Reads | 5 | 5–9d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateClaim`) | 1 | 4–7d |
| F | Federation Contributions | 2 | 4–7d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 5 | 12–20d |
| **Total** | | **24** | **44–75d** (buffered) |

> One engineer ≈ **9–15 sprints**.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateClaim` proxy-ACL multi-step write | 🟡 Medium | Needs a decision (E01) on recovering from a mid-write failure |
| `bulkUpdateClaim` snake-cases its response (likely bug) | 🟡 Medium | Fix to camelCase on the port; parity test |
| `businessPartner` 3-way fallback (incl. a "Target" id-0 case) | 🟢 Low | Preserve exactly; unit-test each branch |
| `ParentDetails` elastic team/BP lookups | 🟢 Low | Preserve empty handling; paginate |
| Federation contributions wait on product | 🟢 Low | F01/F02 post-launch; not on the critical path |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateClaim` failure strategy (proxy ACL + workspace + body) | E01 | Tech Lead + PO |
| 2 | `bulkUpdateClaim` — confirm response should be camelCase | D02 | Backend Eng |
| 3 | Are the 2 unused version service methods needed cross-domain? | A04 | Tech Lead |

## Dependency Map
```
claims subgraph (spark-claims) depends on:
  spark-claims backend   REST claim base (create/search/export/lock/...)
  cross-subgraph (federation): product, search 🔴, workspace, user-profile, team
  Hive Gateway → VMM (business/design partners)
  contributes → plm-product: Product.claims (F01) ; ResourcesCount.claims (F02, TechPack SPARK-PROD-F05)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | A01–A04 + B01–B05 | schema, service port, reads |
| 2 | C01/C02 + D01–D05 | search + simple mutations |
| 3 | E01 + G01/G02 | `updateClaim` + ACL/partner field resolvers |
| 4 | G03/G04 + G05 | parent/elastic + misc fields + tests |
| post-launch | F01, F02 | federation contributions (unblocked by product) |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~9–15 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel after A |

---
*Pipeline 2.0 — Phase 4 complete. Claims artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Separate `claims` subgraph.*
