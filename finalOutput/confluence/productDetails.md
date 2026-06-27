# ProductDetails — Migration to the `plm-product` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../productDetails/03-schema-analysis.md) ·
> [field inventory](../productDetails/05-attribute-inventory.md) · [engineering stories](../productDetails/04-stories.md).
> Create tickets from [`../jira/productDetails.csv`](../jira/productDetails.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving **ProductDetails** — the product's "construction" sets (build/assembly detail rows, their
attachments, and per-partner access) — off the `spark-internal-graphql` gateway into the **`plm-product`**
DGS. (In the backend this domain is called *construction* — `construction/v1`; the GraphQL names stay
`productDetails`.) It is **mid-sized and mid-low risk**: 2 queries, 6 mutations, 12 field resolvers on a
129-line resolver, with **no polymorphism**.

The one genuinely harder piece is **`updateProductDetailsSet`**, a multi-step write — workspace
associations, then bulk-archive removed attachments, then the body — with no rollback today.

**ACL note:** the current code obtains per-resource capability tokens via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one by-ids (internal), one elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateProductDetailsSet` (multi-step) |
| Field-resolver type blocks | 3 | `ProductDetails` (10), item (2), category (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **17** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 7–11d |
| B | Core Reads | 1 | 1–2d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateProductDetailsSet`) | 1 | 4–7d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **17** | **31–53d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateProductDetailsSet` multi-step write | 🟡 Medium | Needs a decision (E01) on recovering from a mid-write failure |
| `updateProductDetailComponentStatus` has no auth token | 🟢 Low | Confirm the backend enforces it |
| Attachment-by-search field resolvers | 🟢 Low | Shared search helper; batch where possible |
| `getProductDetailsElastic.types` arg not in schema | 🟢 Low | Drop or add to the schema |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateProductDetailsSet` failure strategy | E01 | Tech Lead + PO |
| 2 | `updateProductDetailComponentStatus` no token — backend-enforced? | D05 | PO |
| 3 | `getProductDetailsElastic.types` — add to schema or drop? | C01 | Backend Eng |

## Migration approach (summary)

Phase **A** schema + `ProductDetailsService` port (base `construction/v1`); **B/C** the 2 reads; **D** the
simple mutations; **E** the multi-step `updateProductDetailsSet`; **F** `Product.productDetails` (internal,
co-located); **G** the field resolvers (ACL/permissions, attachment-by-search, partners/workspaces/users) +
tests. Full detail: [03-schema-analysis.md §Migration Approach](../productDetails/03-schema-analysis.md).

## Sequencing & capacity

One engineer ≈ 6–11 sprints; 2 engineers ≈ 4–6. Full plan: [04-po-summary.md](../productDetails/04-po-summary.md).

---
*PO page assembled from the productDetails analysis. Tickets:
[`../jira/productDetails.csv`](../jira/productDetails.csv) · [`../jira/productDetails-stories.md`](../jira/productDetails-stories.md).*
