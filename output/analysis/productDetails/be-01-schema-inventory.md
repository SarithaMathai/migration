# Phase 1: Schema Inventory — ProductDetails

> **Domain:** `productDetails`
> **Target DGS:** `ProductDetailsService` → `plm-product` (co-located)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_ProductDetail.graphqls` (139-line SDL) + `resolvers/product/SPARK_ProductDetail.js` + `services/product/ProductDetails.js`
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

There is no `context.js` in the snapshot (the schema SDL is present). The endpoint is built in the service
constructor (`services/product/ProductDetails.js:11`):

```js
this.endpoint = `${endpoint}/enterprise_product_development_products/construction/v1`
```

> **Naming note:** in the backend this domain is **"construction"** (`/construction/v1`; mutations use
> `constructionSetId`/`constructionTemplate`). The GraphQL surface calls it **productDetails**. Preserve the
> GraphQL names; the REST path is `construction/v1`.

| Setting | Value |
|---|---|
| Loader key | `ProductDetails` |
| Service class | `ProductDetailsService` |
| Backend base | `https://spark-product.dev.target.com` (repo `spark-product`) |
| Base path | `${endpoint}/enterprise_product_development_products/construction/v1` |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | `plm-product` (co-located — internal to the product family) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_ProductDetail.graphqls` | 139 | the source SDL — 2 queries, 6 mutations, `ProductDetails`/item/category types, 8 inputs |
| `resolvers/product/SPARK_ProductDetail.js` | 129 | 2 queries, 6 mutations, 3 type blocks (12 field resolvers) |
| `services/product/ProductDetails.js` | 102 | 9 REST methods (`construction/v1`) — 2 unused (versions) |
| **Total** | **370** | small domain — no chunked reading |

Schema: **`schemas/SPARK_ProductDetail.graphqls` (139 lines)** — target schema in
[03-schema.graphql](./03-schema.graphql) is translated from it (nullability from the SDL).

## 3. Import Graph
```
resolvers/SPARK_ProductDetail.js
├── utils/vmmUtils                  → loadBpsWithType (VMM partner enrichment)
├── utils/commonLoaders            → getUserPermissionsJWT (ACL — context only)
├── utils/Product/userGroupUtils   → getUserGroup (participants)
├── utils/workspaceAssociationHelper → workspaceAssociationHelper, ValidWorkspaceAssociationTypes
└── resolvers/SPARK_WorkspaceV2    → getWorkspacesByIdsV2 (workspace enrichment)
services/ProductDetailsService.js uses postOne, putOne, loadListing, loadOne, convertFunctions
```

## 4. Cross-Domain Reference Table

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `getProductDetailsElastic`, `attachment`, `ProductDetailsItem.attachment*` | `search` | SearchService (elastic) | sibling DGS (federation) | 🔴 |
| `cloneFilesForProductDetails`, attachment archive (in update) | `attachment` | AttachmentService | sibling DGS (federation) | 🔴 |
| `access`, `currentUserPermissions` | `accessControl` | AccessControlService | **context only — ACL ignored** | n/a |
| `createdBy`, `updatedBy` | `userAttributes` | UserProfileService | sibling DGS (federation) | 🟡 |
| `workspaces` | `workspaceV2` | WorkspaceService | sibling DGS (federation) | 🟡 |
| `businessPartners` | `vmm` (loadBpsWithType) | VMM platform | Gateway stitch | 🔵 |
| `participantDetails` | `userGroup` / user-profile | UserProfileService | sibling DGS (federation) | 🔵 |
| `product` | `product` | ProductService (same DGS) | **internal** | — |
| `ProductDetailsCategoryWithSection.subCategories` | `specificationsTemplate` | SpecificationTemplateService (same DGS) | **internal** | — |
| all reads/writes | `accessControl` (getUserPermissionsJWT) | AccessControlService | **context only — ACL ignored** | n/a |

## 5. Co-located Siblings
- `product`, `bom`, `measurement`, `packaging`, `impression`, `specificationsTemplate` — share `plm-product`.
- `Product.productDetails`, `Component.…(productDetail)` resolve **internally**, not cross-subgraph.

## 6. Hot Spots
1. **`updateProductDetailsSet`** (`:37-55`) — **multi-step write**: (1) workspace associations via
   `workspaceAssociationHelper` (throws on error), (2) bulk-archive `deleteAttachmentIds` (🔴 attachment),
   (3) `PUT construction/v1/{id}`. No rollback across the 3 steps.
2. **`cloneFilesForProductDetails`** (`:56-70`) — per-attachment `Promise.all` fan-out to (🔴 attachment)
   `cloneAttachmentV3`, stamping `parentResource`. No rollback.
3. **`createProductDetailsSet`** (`:19-27`) — throws on `validationErrors`/`message` in the response
   (explicit error contract — preserve).
4. **`updateProductDetailComponentStatus`** (`:71-72`) — **no `getUserPermissionsJWT`** (no auth token —
   confirm backend-enforced). Wraps result as `{content}`.
5. **Attachment-by-search fields** — `ProductDetails.attachment`, `ProductDetailsItem.attachment` /
   `constructionSetAttachments` all hit (🔴 search) `searchAttachments`; `attachment` filters
   `relatedResources.length <= 2`.
6. **2 unused service methods** — `getProductDetailVersionsById`, `getProductDetailVersion` (no query
   wires them). Confirm cross-domain use before dropping.

## 7. Operation Lists
**Queries (2):** getProductDetailsById, getProductDetailsElastic.
**Mutations (6):** createProductDetailsSet, updateProductDetailAccess, productDetailLockUnlock,
updateProductDetailsSet, cloneFilesForProductDetails, updateProductDetailComponentStatus.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 2 |
| Mutations | 6 |
| Object types | 4 (`ProductDetails`, `ProductDetailsItem`, `ProductDetailsCategoryWithSection`, `ProductDetailsPaged`) |
| Field resolvers | 12 (10 on `ProductDetails`, 1 category, 2 item) |
| Service methods | 9 (7 used + 2 unused) |
| Cross-domain loader keys | 8 (+ accessControl context-only) |
| EXT calls | 2 🔴 · 2 🟡 · 2 🔵 (+ 2 internal: product, specificationsTemplate) |
| Interfaces / unions | 0 |
| Large files | 0 |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `productDetails` · **Files:** 3 (370 lines: schema 139 + resolver 129 + service 102).
