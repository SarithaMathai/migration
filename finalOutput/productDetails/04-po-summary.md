# Phase 4: PO Sprint Planning Summary — ProductDetails

> **Domain:** `productDetails` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

We are moving the **ProductDetails** domain — the product's "construction" sets (build/assembly detail rows,
their attachments, and per-partner access) — off the `spark-internal-graphql` gateway into the
**`plm-product`** DGS. It is **mid-sized and mid-low risk**: 2 queries, 6 mutations, 12 field resolvers on a
129-line resolver, with **no polymorphism**. (In the backend this domain is called *construction* —
`construction/v1`; the GraphQL names stay `productDetails`.)

The one genuinely harder piece is **`updateProductDetailsSet`**, a multi-step write — workspace
associations, then bulk-archive removed attachments, then the body — with no rollback today.

**ACL note:** the current code obtains per-resource capability tokens via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one by-ids (internal), one elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateProductDetailsSet` (multi-step) |
| Field-resolver type blocks | 3 | `ProductDetails` (10), item (2), category (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **17** | green-field |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 4 | 7–11d |
| B | Core Reads | 1 | 1–2d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateProductDetailsSet`) | 1 | 4–7d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **17** | **31–53d** (buffered) |

> One engineer ≈ **6–11 sprints**.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateProductDetailsSet` multi-step write | 🟡 Medium | Needs a decision (E01) on recovering from a mid-write failure |
| `updateProductDetailComponentStatus` has no auth token | 🟢 Low | Confirm the backend enforces it |
| Attachment-by-search field resolvers | 🟢 Low | Shared search helper; batch where possible |
| `getProductDetailsElastic.types` arg not in schema | 🟢 Low | Drop or add to the schema |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateProductDetailsSet` failure strategy | E01 | Tech Lead + PO |
| 2 | `updateProductDetailComponentStatus` no token — backend-enforced? | D05 | PO |
| 3 | `getProductDetailsElastic.types` — add to schema or drop? | C01 | Backend Eng |
| 4 | Are the 2 unused version service methods needed cross-domain? | A04 | Tech Lead |

## Dependency Map
```
plm-product (ProductDetails subgraph) depends on:
  spark-product backend  REST .../construction/v1
  sibling DGS (federation): attachment, workspace, user-profile, access-control, search 🔴
  Hive Gateway → VMM (business partners)
  internal (same DGS): product, specificationsTemplate
  product domain         F01 Product.productDetails (internal field resolver)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | A01–A04 + B01/C01 | schema, service port, reads |
| 2 | D01–D05 | simple mutations |
| 3 | E01 + F01 | multi-step write + Product field |
| 4 | G01–G03 | field resolvers |
| 5 | G04 | tests & parity |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after A |

---
*Pipeline 2.0 — Phase 4 complete. ProductDetails artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*
