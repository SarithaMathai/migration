# Phase 4: PO Sprint Planning Summary — Claims

> **Domain:** `claims` · **Target DGS:** separate `claims` subgraph (repo `spark-claims`) · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [be-04-stories.md](./be-04-stories.md)
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
Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites — where a resolver hands its token to a *different* domain's loader — use **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before the downstream call.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateClaim` (proxy-ACL multi-step) |
| Field-resolver type blocks | 4 | `Claims` (11), `ParentDetails` (3), substantiate (1), claimDetails (1) |
| External dependencies | 6 keys (1 🔴 · 3 🟡 · 2 🔵) | search 🔴; product/user-profile/workspace 🟡 |
| Federation contributions | 2 (Product.claims, ResourcesCount.claims) | BLOCKED-BY product |
| **Total stories** | **21** | green-field; separate subgraph (G-06 added by federation review) |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 5 | 5–9d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateClaim`) | 1 | 4–7d |
| G | Field Resolvers & Tests | 6 | 14–23d |
| H | Entity Resolution (cross-subgraph) | 2 | 4–7d (BLOCKED-BY `PRODUCT-BE-F-14` + product deploy) |
| **Total** | | **21** | **38–65d** (buffered) |

> **Phase H note.** H-01 (`Product.claims`) and H-02 (`ResourcesCount.claims`) are cross-subgraph
> contributions — they cannot ship until `plm-product` is deployed and `PRODUCT-BE-F-14` (contract
> alignment) has landed. They are sequenced post-launch.

> One engineer ≈ **8–13 sprints**.

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B-01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateClaim` proxy-ACL multi-step write | 🟡 Medium | Needs a decision (E-01) on recovering from a mid-write failure |
| `bulkUpdateClaim` snake-cases its response (likely bug) | 🟡 Medium | Fix to camelCase on the port; parity test |
| `businessPartner` 3-way fallback (incl. a "Target" id-0 case) | 🟢 Low | Preserve exactly; unit-test each branch |
| `ParentDetails` elastic team/BP lookups | 🟢 Low | Preserve empty handling; paginate |
| Federation contributions wait on product | 🟢 Low | H-01/H-02 post-launch; not on the critical path |
| DataLoader missing on H-01 entity fetcher | 🟡 Medium | N+1 at gateway level; add `claimByIdLoader` MappedBatchLoader to H-01 AC |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateClaim` failure strategy (proxy ACL + workspace + body) | E-01 | Tech Lead + PO |
| 2 | `bulkUpdateClaim` — confirm response should be camelCase | D-02 | Backend Eng |
| 3 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Dependency Map
```
claims subgraph (spark-claims) depends on:
 spark-claims backend REST claim base (create/search/export/lock/...)
 cross-subgraph (federation): product, search 🔴, workspace, user-profile, team
 Hive Gateway → VMM (business/design partners)
 cross-domain blockers:
   E-01 (updateClaim) depends on PRODUCT-BE-E-00 (WriteSaga shared module)
   H-01/H-02 BLOCKED-BY PRODUCT-BE-F-14 (contract alignment) + plm-product deploy
 contributes → plm-product: Product.claims (H-01) ; ResourcesCount.claims (H-02, TechPack PRODUCT-BE-H-04)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-05 | search + simple mutations |
| 3 | E-01 + G-01/G-02 | `updateClaim` + ACL/partner field resolvers |
| 4 | G-03/G-04 + G-06 | parent/elastic + misc fields + shared value-type alignment |
| post-launch | H-01, H-02 | federation contributions (unblocked by product) |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~9–15 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel after B-01 |

---
*Pipeline 2.0 — Phase 4 complete. Claims artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Separate `claims` subgraph.*
