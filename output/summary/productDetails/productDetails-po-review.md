# Product Details — Migration to the `plm-product` DGS (PO view)

> 🏷️ **Tags:** `dgs-migration` · `po-page` · `domain-productDetails` · `pipeline-v2`  —  **Confluence location:** *Federation Graph Migration ▸ Domains ▸ productDetails*

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.  
> Deep dives: migration approach & schema · field inventory · engineering stories.  
> Create tickets from `../finalOutput/jira/productDetails.csv`. Effort is **AI-estimated — confirm in refinement.**

---

## What are we building?

We are moving the **ProductDetails** domain — the product's "construction" sets (build/assembly detail rows,
their attachments, and per-partner access) — off the `spark-internal-graphql` gateway into the
**`plm-product`** DGS. It is **mid-sized and mid-low risk**: 2 queries, 6 mutations, 12 field resolvers on a
129-line resolver, with **no polymorphism**. (In the backend this domain is called *construction* —
`construction/v1`; the GraphQL names stay `productDetails`.)

The one genuinely harder piece is **`updateProductDetailsSet`**, a multi-step write — workspace
associations, then bulk-archive removed attachments, then the body — with no rollback today.

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive step in `updateProductDetailsSet`) use **Mid-Request ACL Update** before the downstream call.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one by-ids (internal), one elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateProductDetailsSet` (multi-step) |
| Field-resolver type blocks | 3 | `ProductDetails` (10), item (2), category (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

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


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateProductDetailsSet` failure strategy | E-01 | Tech Lead + PO |
| 2 | `updateProductDetailComponentStatus` no token — backend-enforced? | D-05 | PO |
| 3 | `getProductDetailsElastic.types` — add to schema or drop? | C-01 | Backend Eng |
| 4 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Migration approach (summary)

**B** Core Reads; **C** Search & Listing; **D** Mutations (simple); **E** Complex (`updateProductDetailsSet`); **F** Federation (Product, internal); **G** Field Resolvers & Tests. Full detail: `be-03-schema-analysis.md §Migration Approach`.

## Sequencing & capacity

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | D-01–D-05 | simple mutations |
| 3 | E-01 + F-01 | multi-step write + Product field |
| 4 | G-01–G-03 | field resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

---
*PO review assembled from the `productDetails` analysis. Jira tickets: `finalOutput/jira/productDetails.csv`. Full engineering detail: `productDetails-comprehensive.md` (same folder).*