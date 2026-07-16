# Phase 4: PO Sprint Planning Summary — ProductDetails

> **Domain:** `productDetails` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

We are moving the **ProductDetails** domain — the product's "construction" sets (build/assembly detail rows,
their attachments, and per-partner access) — off the `spark-internal-graphql` gateway into the
**`plm-product`** DGS. It is **mid-sized and mid-low risk**: 2 queries, 6 mutations, 12 field resolvers on a
129-line resolver, with **no polymorphism**. (In the backend this domain is called *construction* —
`construction/v1`; the GraphQL names stay `productDetails`.)

The one genuinely harder piece is **`updateProductDetailsSet`**, a multi-step write — workspace
associations, then bulk-archive removed attachments, then the body — with no rollback today.

**ACL note:** the current code obtains per-resource capability tokens via ACL; Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs (`complexStories/*/02-adr-noacl-*.md`) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one by-ids (internal), one elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateProductDetailsSet` (multi-step) |
| Field-resolver type blocks | 3 | `ProductDetails` (10), item (2), category (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 1 | 1–2d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateProductDetailsSet`) | 1 | 4–7d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **13** | **24–42d** (buffered) |

> One engineer ≈ **5–9 sprints**.

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B-01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateProductDetailsSet` multi-step write | 🟡 Medium | Needs a decision (E-01) on recovering from a mid-write failure |
| `updateProductDetailComponentStatus` has no auth token | 🟢 Low | Confirm the backend enforces it |
| Attachment-by-search field resolvers | 🟢 Low | Shared search helper; batch where possible |
| `getProductDetailsElastic.types` arg not in schema | 🟢 Low | Drop or add to the schema |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateProductDetailsSet` failure strategy | E-01 | Tech Lead + PO |
| 2 | `updateProductDetailComponentStatus` no token — backend-enforced? | D-05 | PO |
| 3 | `getProductDetailsElastic.types` — add to schema or drop? | C-01 | Backend Eng |
| 4 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Dependency Map
```
plm-product (ProductDetails subgraph) depends on:
 spark-product backend REST .../construction/v1
 sibling DGS (federation): attachment, workspace, user-profile, access-control, search 🔴
 Hive Gateway → VMM (business partners)
 internal (same DGS): product, specificationsTemplate
 product domain F-01 Product.productDetails (internal field resolver)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | D-01–D-05 | simple mutations |
| 3 | E-01 + F-01 | multi-step write + Product field |
| 4 | G-01–G-03 | field resolvers |
| 5 | G-04 | tests & parity |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

---
*Pipeline 2.0 — Phase 4 complete. ProductDetails artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*
