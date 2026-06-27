# Phase 2A — Resolver Analysis: Queries (`product` domain)

> Source:    [resolvers/SPARK_Product.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js) lines 297–536
> Service:   [services/Product.js](spark-internal-graphql/packages/data-source-spark/src/services/Product.js)
> Scope:     All 18 Query operations. Helper `getTechPackResourceCountMap` documented in §0.
> Severity legend: 🔴 critical · 🟡 important enrichment · 🔵 platform/optional

---

## 0. Shared Helpers (used by Query resolvers)

### 0.1 `copyProductToProduct(copyProduct, ctx)`  — lines 70–82
Used by `addProduct` / `updateProduct` mutations (covered in Phase 2B). Listed here because it lives in the same module head.

1. If `copyProduct` is non-empty:
   1. Call `getUserPermissionsJWT(copyProduct.targetProductId, ctx)` → ACL JWT for target resource.
   2. Call `ctx.loaders.product.copyProduct(permissionJWT).load(copyProduct)` → POSTs the copy request.
2. Return the copy response.

### 0.2 `getTechPackResourceCountMap(productId, partnerId, workspaceContext, parentProductId, ctx)` — lines 84–293
The single most complex operation in the system. Backs `getProductTechPackCountV1` and `getProductTechPackBulkCountV1`.

**Inputs:** `productId`, `partnerId`, `workspaceContext` (workspace humanId), optional `parentProductId`.

**Constants used:**
```
inputMap        = { attachments:[0,1,2,3], attachments_v3:[0,1,2,3] }
includeBranches = ['sample','discussions','discussionThreads','bill_of_materials','packaging_bom',
                   'claim','measurement_set','construction_set','product_watchlist']
includeNodeTypes= ['discussions','discussionThreads','attachments_v3']
```

**Steps:**
1. **(EXT 🔴 accessControl + 🔴 search)** Call `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission(ctx, inputMap, productId, partnerIdInt, includeBranches, includeNodeTypes, true)` to walk the child-tree and return ACL-filtered `commonLoaderOutputMaps`.
2. If `parentProductId` is set, repeat step 1 for the parent → `parentProductOutputMaps`; capture its `attachments_v3` levels 1/2/3 into `parentDiscussionAttachments`.
3. Normalize: ensure every level (0/1/2/3) exists in both maps; default missing levels to `[]`.
4. Merge the child product's `attachments` and `attachments_v3` levels with `_.mergeWith(...concat)` → `[productAttachments, ...discussionAttachments]`.
5. Build `discussionAttachments` = parent discussion attachments ∪ self-product discussion attachments (levels 1/2/3 only — level 0 is the product itself).
6. Combine `allAttachmentIds = productAttachments + discussionAttachments`.
7. **(EXT 🔴 accessControl)** `getUserPermissionsJWT(allAttachmentIds, ctx)` → JWT scoped to these IDs.
8. **(EXT 🔴 attachment)** `ctx.loaders.attachment.getAttachmentsV3(permissionJWT).load(allAttachmentIds)` → enriched attachments.
9. Define predicate `isProductPacketAttachments(attachmentId)`:
   - true iff some `enhancedAttachment` matches the id (by `document_id` OR `human_id`) and has a `product_packet_props` entry with `partner_id == partnerIdInt AND critical == true`.
10. **(EXT 🔴 search)** Run **7 parallel elastic queries** (each via a `ctx.loaders.search.*` loader) with the `q` strings shown:

    | Query | Loader |
    |---|---|
    | `(((parentId:X OR parentId:Y) AND partnerId:P) AND (evaluationStatus.code:101 OR 102))` | `search.getSamplesPage` |
    | `((relatedResources:X OR relatedResources:Y) AND (security.merchVendors:P OR security.bps:P) AND (critical:true))` | `search.searchDiscussionsElastic` |
    | `((security.merchVendors:P OR security.bps:P) AND (parentId:X) [AND workspaceContext:W] AND (statusId:200))` | `search.getMeasurementSets` |
    | …same shape, `statusId:501` | `search.getClaimsElastic` |
    | …same shape, `statusId:501` | `search.getBomElastic` |
    | …same shape, `archived:false` | `search.getProductDetailsElastic` |
    | …same shape, `statusId:501` | `search.searchWatchlist` |

    Filter `samples` further to those whose `workspaceContext` matches OR whose `sampleType.code ∈ {200, 135}`.
11. From critical discussions, derive 3 dedup'd id lists: `parentDiscussionIds`, `criticalDiscussionIds`, `criticalThreadIds` (reduce + filter unique).
12. If any critical IDs exist, **(EXT 🔴 search)** call `search.searchAttachmentsByParentResources.load(allCriticalIds)` → `criticalDiscussionAttachments`.
13. Filter `discussionAttachments` through `isProductPacketAttachments` → `filteredProductPacketDiscussionAttachments`.
14. Build & return:

    ```json
    {
      "productId": …, "partnerId": …, "workspaceContext": …,
      "productAttachments":  productAttachments.filter(isProductPacketAttachments),
      "discussionAttachments": union(criticalDiscussionAttachmentsIds, filteredProductPacketDiscussionAttachments),
      "discussions": union(parentDiscussionIds, criticalDiscussionIds),
      "sample": filteredSamples.map(id),
      "measurementSets": measurementSets.map(id),
      "claims": claims.map(id),
      "productBoms": boms where type === 1,
      "packagingBoms": boms where type === 2,
      "constructions": constructions.map(id),
      "watchlists": watchlists.map(id)
    }
    ```

**EXT services invoked:** `accessControl` 🔴 (1–2×), `attachment.getAttachmentsV3` 🔴, `search.*` 🔴 ×8 distinct loaders.
**Complexity:** **Very High (X-Large, 8–13 days)** — apply +0 polymorphic bump (none here) but stitch design required (CAT-4).
**See:** `fedMigrationScripts/reference/stitching-patterns.md` + `techpack-migration-options.md` (Option D recommended).

---

## 1. `getProducts(page, size, q, filter, resourceType, resourceId, includeBoms, includeClaims, includeMeasurementSets, includeProductDetails)` → `SPARK_ProductsPaged`
**Resolver:** lines 297–366. **Complexity:** **High (Large, 5–8 days)**.

### Pseudo-logic
1. **(EXT 🔴 search via product loader)** Call `ctx.loaders.product.getFilteredProductsListing.load({ resourceType: resourceType ?? 'products', resourceId: resourceId ?? '', includeBoms: includeBoms ?? true, includeClaims: includeClaims ?? true, includeMeasurementSets: includeMeasurementSets ?? true, includeProductDetails: includeProductDetails ?? true, filter: filter ?? [], q: q ?? '', page, size })`.
   - HTTP: `GET ${PRODUCT_SEARCH_ENDPOINT}/search?…` (elastic). Response transformed `deepToCamelCase`.
2. Extract `productHumanIds = elasticResponse.content.map(p => p.humanId)`.
3. **(Internal)** Call `ctx.loaders.product.getPage.load({ products: productHumanIds, page: 0, size, additionalParams: '' })`.
   - HTTP: `GET ${endpointv1}?productId={ids}&page=0&size={size}&sort=createdDate,desc`.
4. Build `elasticProducts = reduce(content, (acc,p) => ({...acc, [p.humanId]: p}))`.
5. Return `{ ...elasticResponse, content: productsPaged.content.map(product => mergeWith elasticProducts[product.productId] picking { boms, productDetails, claims, measurementSets, samples, sampleIds (samples.humanId[]), hasSamplesUpcomingDue, hasNotEvaluatedReceivedSamples, receivedNotEvaluatedCount }) }`.

**EXT services:** `search` 🔴 (via the product loader's elastic endpoint).
**Notes:** Two-stage hydration — elastic first (gives the IDs + flags), then product API (gives canonical record). Boolean defaults are **truthy** (`|| true`) — a future change to `false` would be backwards-incompatible.

---

## 2. `getProductTemplates(page, size, q, filter, resourceId, resourceType, types, includeBoms, includeClaims, includeMeasurementSets, includeProductDetails, includeClaimTemplates, includeMeasurementSetTemplates, includeProductDetailTemplates, includeProductComponentsCount, includeBomTemplates)` → `SPARK_ProductTemplatesList`
**Resolver:** lines 367–409. **Complexity:** **Medium (Medium, 3–5 days)**.

### Pseudo-logic
1. **(EXT 🔴 search)** `ctx.loaders.product.getFilteredProductsListing.load({ resourceType: resourceType ?? 'product', resourceId: resourceId ?? '', includeBoms: false, includeClaims: includeClaims ?? false, includeMeasurementSets: includeMeasurementSets ?? false, includeProductDetails: false, filter: filter ?? [], q: q ?? '', page, size, types, includeProductComponentsCount: …, includeBomTemplates: …, includeClaimTemplates: …, includeMeasurementSetTemplates: …, includeProductDetailTemplates: … })`.
2. Return `elasticResponse || {}`. **No** secondary product-API hydration.

**EXT services:** `search` 🔴.

---

## 3. `getProduct(id: ID!)` → `SPARK_Product`
**Resolver:** lines 410–413. **Complexity:** **Low (Small, 1–2 days)**.

1. `return ctx.loaders.product.getByID.load(id)` → `GET ${endpointv1}?productId={id}&size={id.length}`.
2. Response: `deepToCamelCase(json.content[matching])` or `null`. Batched via DataLoader.

---

## 4. `getCopyStatus(id: ID!)` → `SPARK_ProductCopy`
**Resolver:** lines 414–417. **Complexity:** **Low**.

1. `return ctx.loaders.product.getCopyStatus.load(id)` → `GET ${endpointv2}/count/resource-type?copyId={id}` (not batched).

---

## 5. `getCategories(type: String!, resourceId, resourceType, productType)` → `SPARK_ProductsCategories`
**Resolver:** lines 418–428. **Complexity:** **Medium** (categories are then resolved polymorphically — see Phase 2C `SPARK_ProductsCategories.categories` and `SPARK_Categories.__resolveType`).

1. Default `productType = productType ?? 100`.
2. **(EXT 🔴 search)** `ctx.loaders.product.getProductCategories.load({ type, resourceId, resourceType, productType })` → `GET ${elasticSearchEndpoint}/search/${snake_case(type)}?resourceType=…&resourceId=…&productType=…`.
3. Return as-is.

---

## 6. `getProductsByIds(ids: [ID]!)` → `SPARK_ProductsPaged`
**Resolver:** lines 429–430. **Complexity:** **Low**.

1. `return ctx.loaders.product.getByIdList.load(ids)` → `GET ${endpointv1}?productId={csv}&page=0&size=10000&sort=createdDate,desc`. Primes the per-id `getByID` loader.

---

## 7. `getProductStatus()` → `[SPARK_MasterProductStatus]`
**Resolver:** lines 431–432. **Complexity:** **Low**.

1. `return ctx.loaders.product.getStatus.load()` → fetch master status list (page-listing loader, no args).

---

## 8. `getProductTechPackCountV1(productId: ID!, partnerId, workspaceContext, parentProductId)` → `SPARK_ResourcesCount`
**Resolver:** lines 433–445. **Complexity:** **Very High** — delegates to §0.2.

1. `return getTechPackResourceCountMap(productId, partnerId, workspaceContext, parentProductId, ctx)`.

---

## 9. `getProductTechPackBulkCountV1(bulkTechPackCountResource: [SPARK_ProductTechPackCountInput])` → `[SPARK_ResourcesCount]`
**Resolver:** lines 446–467. **Complexity:** **Very High** (fans out per-item).

### Pseudo-logic
1. `outputMapList = []`.
2. `Promise.all( bulkTechPackCountResource.map(input => getTechPackResourceCountMap(input.productId, input.partnerId, input.workspaceContext, input.parentProductId, ctx).then(r => outputMapList.push(r))) )`.
3. After all settle, return `outputMapList`.

**Performance note:** Each item triggers the full §0.2 pipeline (8+ EXT search calls + ACL + attachment). For N items: ~9N EXT calls. **Order of results is non-deterministic** (push order = completion order, not input order). This is a latent bug worth flagging in Phase 4.

---

## 10. `getProductVersions(id: ID!)` → `SPARK_ProductsPaged`
**Resolver:** lines 468–469. **Complexity:** **Low**.

1. `return ctx.loaders.product.getVersions.load({ id })` → `GET ${endpointv1}/{id}/versions?page=0&size=10000`. Primes `getByID` per version.

---

## 11. `getRatingByTcin(tcin: String)` → `SPARK_Rating`
**Resolver:** lines 470–486. **Complexity:** **Medium** (uses an **external rating service**, not a Spark backend).

### Pseudo-logic
1. `response = await ctx.loaders.product.getRatingByTcin.load(tcin)` → `GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={SPARK_GATEWAY_API_KEY}`. `skipJsonParse: true` (raw text returned).
2. `try { parsed = JSON.parse(response); if (parsed?.statistics) return { averageRating: parsed.statistics.rating?.average ?? 0.0, reviewCount: parsed.statistics.reviewCount ?? 0 } }`.
3. `catch { return null }` (silent failure on 404 / non-JSON).

**EXT services:** Rating service (external SaaS, gateway-only). 🔵 BLUE.
**Auth:** API key (`SPARK_GATEWAY_API_KEY`) — **secret must be migrated to DGS config**.

---

## 12. `getProductRules()` → `[SPARK_ProductRules]`
**Resolver:** lines 487–489. **Complexity:** **Low**.

1. `return ctx.loaders.product.getAllRules.load()` → `GET ${endpoint}/spark_rules/v1`, return `result.content` deep-camelCased.

---

## 13. `getProductRulesById(id: ID!)` → `SPARK_ProductRules`
**Resolver:** lines 490–492. **Complexity:** **Low**.

1. `return ctx.loaders.product.getRuleById.load(id)` → `GET ${endpoint}/spark_rules/v1/{id}` (not batched).

---

## 14. `getAllAvailableRules()` → `[SPARK_AvailableRules]`
**Resolver:** lines 493–495. **Complexity:** **Low**.

1. `return ctx.loaders.product.getAvailableRules.load()` → `GET ${endpoint}/spark_rules/v1/rules`.

---

## 15. `getProductDeptRules(productIds, departmentIds, activeOnly)` → `[SPARK_ProductRules]`
**Resolver:** lines 496–507. **Complexity:** **Low** (default `activeOnly = true`).

### Pseudo-logic
1. `loader = USE_NEW_RULES_API ? ctx.loaders.ruleLibrary.searchRuleLibrary : ctx.loaders.product.searchProductDeptRules.load`.
2. `return loader({ productIds, departmentIds, activeOnly })`.
   - When false: `GET ${endpoint}/spark_rules/v1/search?productIds=…&departmentIds=…&activeOnly=…`.
   - When true: ruleLibrary loader (different backend — `spark-tag`).

**Feature-flag risk:** Two divergent code paths; parity tests in Phase 4 must cover both.

---

## 16. `getProductBPRules(productIds, businessPartnerIds, activeOnly)` → `[SPARK_ProductRules]`
**Resolver:** lines 508–519. **Complexity:** **Low**.

Same shape as §15 but with `businessPartnerIds`. URL: `…/search?productIds=…&businessPartnerIds=…&activeOnly=…`.

---

## 17. `searchProductRules(productIds, departmentIds, businessPartnerIds, activeOnly)` → `[SPARK_ProductRules]`
**Resolver:** lines 520–532. **Complexity:** **Medium** (server-side response transformer).

1. Same loader-switch pattern as §15/§16.
2. Legacy path uses `searchProductRules` loader → `GET ${endpoint}/spark_rules/v1/search_mapped?…`.
3. Legacy response runs through `productRuleResponseTransformer` then `deepToCamelCase` (see [utils/Product/productUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/productUtils.js)).

---

## 18. `getProductTemplateById(id: ID!)` → `SPARK_Product`
**Resolver:** lines 533–536. **Complexity:** **Low**.

1. `response = await ctx.loaders.product.getByID.load(id)`.
2. `return response || {}` (returns empty object on miss instead of null — schema contract subtle).

---

## EXT Service Call Summary (Queries only)

| Loader | Severity | Touched From | Notes |
|---|---|---|---|
| `search.*` (≥8 distinct loaders) | 🔴 RED | §1, §2, §5, §8/9 (techpack ×7) | Bulk of latency budget |
| `accessControl` (getUserPermissionsJWT + ACL batch) | 🔴 RED | §8/9 (techpack) | Required for JWT-scoped attachment fetch |
| `attachment.getAttachmentsV3` | 🔴 RED | §8/9 (techpack) | JWT-curried loader |
| `ruleLibrary.searchRuleLibrary` | 🔵 BLUE | §15/§16/§17 (flag) | Different DGS owner |
| External Rating service | 🔵 BLUE | §11 | Non-Spark SaaS, API-key auth |
| `product` self loader | — Internal | All ops | Becomes the Feign client in `plm-product` |

## Complexity Roll-Up (Queries only)

| Tier | Operations | Count | Days (un-buffered) |
|---|---|---|---|
| Very High | `getProductTechPackCountV1`, `getProductTechPackBulkCountV1` | 2 | 16–26 |
| High | `getProducts` | 1 | 5–8 |
| Medium | `getProductTemplates`, `getCategories`, `getRatingByTcin`, `searchProductRules` | 4 | 12–20 |
| Low | `getProduct`, `getCopyStatus`, `getProductsByIds`, `getProductStatus`, `getProductVersions`, `getProductRules`, `getProductRulesById`, `getAllAvailableRules`, `getProductDeptRules`, `getProductBPRules`, `getProductTemplateById` | 11 | 11–22 |
| **Total (Queries)** | | **18** | **44–76 days** |

Apply +20% buffer (per [USAGE.md §7](fedMigrationScripts/USAGE.md)): **~53–91 days for Query work alone.**

## Key Findings (Queries)

1. **TechPack** is the single largest migration cost. Two operations alone consume ~⅓ of the query effort.
2. **TechPack bulk version has a latent ordering bug** — output array order is completion order, not input order. Flag for Phase 4 acceptance criteria (parity test should sort or key by `productId`).
3. **Feature-flag fork** (`USE_NEW_RULES_API`) covers 3 operations and crosses a DGS boundary (rules → `spark-tag` DGS). Decide cutover strategy before Phase 4.
4. **Two-stage elastic + canonical pattern** in `getProducts` is reusable across siblings; consider extracting into a shared `plm-product` Kotlin helper.
5. **External Rating service** (`RATING_ENDPOINT`, `SPARK_GATEWAY_API_KEY`) is the only non-Spark backend called directly from product queries. Migrate as a gateway stitch or a thin Feign client with secret in Vault.
6. **Boolean defaults `?? true`** in `getProducts` are easy to mis-port. Tests must pin the existing behavior.

---

**Phase 2A complete — Queries.** Reply `next` to proceed to Phase 2B (Mutations).
