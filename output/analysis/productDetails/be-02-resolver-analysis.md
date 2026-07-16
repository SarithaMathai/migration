# Phase 2: Resolver Dependency Analysis — ProductDetails

> **Domain:** `productDetails` · **Target DGS:** `ProductDetailsService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_ProductDetail.graphqls` (SDL), `resolvers/product/SPARK_ProductDetail.js`, `services/product/ProductDetails.js`
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full

Implementation spec. ACL/JWT usage is **context-only** (ignored in impl). Backend path is `construction/v1`.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 2 |
| Mutation resolvers | 6 |
| Field resolvers | 12 (3 type blocks) |
| Service methods | 9 (2 unused) |
| EXT loaders | 6 (2 🔴 · 2 🟡 · 2 🔵) + accessControl context-only + 2 internal |
| High complexity | 1 (`updateProductDetailsSet` multi-step) |

---

## Query Resolvers (2)

| # | Query | Complexity | Pseudo-logic (REST + EXT) |
|---|-------|-----------|---------------------------|
| Q1 | `getProductDetailsById(ids): [ProductDetails]` | Low | (ACL context) token for `ids` → (internal) `ProductDetails.getProductDetailsById(jwt, ids)` `GET construction/v1?ids={csv}` → `deepToCamelCase`. |
| Q2 | `getProductDetailsElastic(resourceId): ProductDetailsPaged` | Medium | (🔴 search) `search.getProductDetailsElastic.load({ q: "parentId: {resourceId}", types })` → paged. **Note:** resolver also reads a `types` arg not declared in the SDL — drop or add to schema. |

## Mutation Resolvers (6)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `createProductDetailsSet(productDetails): ProductDetails` | Medium | (ACL context) token for literal `['SPARK-CONSTRUCTION-CREATE-MODIFY-TARGET-LIBRARY']` → `POST construction/v1` (snake_case body). **If response has `validationErrors` or `message` → throw** (preserve). |
| M2 | `updateProductDetailAccess(updateAccessPermissions): [ProductDetails]` | Low | map `managePermissionsRequest[].resourceId` → (ACL context) token → `PUT construction/v1/manage-permissions`; `primeKey = humanId`. |
| M3 | `productDetailLockUnlock(constructionSetId, isLock): ProductDetails` | Low | (ACL context) token for `[constructionSetId]` → `PUT construction/v1/{id}/{lock|unlock}`. |
| M4 | `updateProductDetailsSet(productDetailsId, productDetails): ProductDetails` | **High** | **multi-step:** 1) if `productDetails.workspaceContext.{add,remove}Workspaces` non-empty → `workspaceAssociationHelper(PRODUCT_DETAIL, id, add, remove)` (throws on error); 2) null out `workspaceContext`; 3) if `deleteAttachmentIds` → (🔴 attachment) `archiveAttachmentBulkV3` (separate ACL token); 4) `PUT construction/v1/{id}` (snake_case). **No rollback across steps.** |
| M5 | `cloneFilesForProductDetails(attachmentIds, cloneReference): [Attachment]` | Medium | (ACL context) token → `Promise.all(attachmentIds.map((id,i) => (🔴 attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id)))`, stamp `parentResource=id`, flatten. No rollback. |
| M6 | `updateProductDetailComponentStatus(productId, ids, status): ProductDetailsPaged` | Low | (internal) `ProductDetails.updateProductDetailComponentStatus({productId, ids, status})` `PUT construction/v1/component_status_update`; wraps as `{content}`. **No JWT — confirm backend-enforced.** |

## Field Resolvers (12)

**`ProductDetails` (10):**
- `access` (ACL context) — `accessControl.getPermissions([humanId||id])`, returns `perms[0]`.
- `currentUserPermissions` (ACL context) — `accessControl.getUserAccessUnencoded(humanId||id)`, `[0]`.
- `product` (internal) — only if `parentId` starts with `'PID'` → `product.getByID(parentId)`, else null.
- `createdBy` / `updatedBy` (🟡 userAttributes) — `getUserByIDOrNullIfNotFound`.
- `businessPartners` (🔵 vmm) — `loadBpsWithType(businessPartners, ctx)`.
- `workspaces` (🟡 workspaceV2) — `SPARK_WorkspaceV2.getWorkspacesByIdsV2({ ids: workspaceContext })` or null.
- `attachment` (🔴 search) — `searchAttachments({ relatedIds:[humanId||id] })`, find `relatedResources.length <= 2`.
- `participantDetails` (🔵 user-profile) — `getUserGroup(ctx, humanId)`.

**`ProductDetailsCategoryWithSection` (1):**
- `subCategories` (internal `specificationsTemplate`) — `getProductDetailsCategorySection()` master data, find by `code`.

**`ProductDetailsItem` (2):**
- `attachment` (🔴 search) — `searchAttachments({ relatedIds:[templateId] })` → `content[0]` or `{}`.
- `constructionSetAttachments` (🔴 search) — `searchAttachments({ relatedIds:[id] })` → `content` or `[]`.

## Service Classes
- `ProductDetailsService` base `construction/v1`.
- Methods: `getProductDetailsById` (GET `?ids=`), `createProductDetailsSet` (POST), `updateProductDetailsSet` (PUT `/{id}`), `manageWorkspaceAssociations` (PUT `/{id}/workspace_associations`), `updateProductDetailAccess` (PUT `/manage-permissions`), `productDetailLockUnlock` (PUT `/{id}/{lock|unlock}`), `updateProductDetailComponentStatus` (PUT `/component_status_update`).
- **Unused:** `getProductDetailVersionsById`, `getProductDetailVersion`.

## EXT Service Call Inventory (summary)
- 6 EXT keys — **2 🔴** (search, attachment) · **2 🟡** (userAttributes, workspaceV2) · **2 🔵** (vmm, user-profile/userGroup) · accessControl **context-only**.
- **Internal (same DGS):** product, specificationsTemplate, ProductDetails (own).

## Key Findings
- **Highest risk:** `updateProductDetailsSet` (M4) multi-step write (workspace + attachment archive + body),
  no rollback — needs a failure strategy (decision).
- **Latent / confirm:** `updateProductDetailComponentStatus` has **no auth token**;
  `getProductDetailsElastic` resolver reads a `types` arg absent from the SDL.
- **Refactors:** 3 attachment-by-search field resolvers → a shared search helper; clone fan-out → batch.
- **Quick wins:** `getProductDetailsById`, `productDetailLockUnlock`, `updateProductDetailAccess`.
- **Unused service methods:** the two version reads — confirm before dropping.

---
**Phase Completed:** Phase 2 · **Domain:** `productDetails` · **EXT:** 6 keys (2🔴 · 2🟡 · 2🔵).
