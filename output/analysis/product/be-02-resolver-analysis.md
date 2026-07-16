# Phase 2: Resolver Dependency Analysis — Product

> **Domain:** `product` · **Target DGS:** `ProductService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `schemas/SPARK_Product.graphqls` (SDL), `resolvers/SPARK_Product.js` (2,629), `services/Product.js` (589), product utils
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full (large-file protocol)

This is the implementation spec for the largest domain. ACL/JWT usage is **context-only** (ignored in impl).

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 18 |
| Mutation resolvers | 20 (+3 deferred) |
| Field resolvers | ~50 (14 type blocks) |
| Service methods | 42 |
| EXT loaders | 12 (4 🔴 · 6 🟡 · 2 🔵) + 6 platform 🔵 + accessControl context-only |
| Very High | 3 (TechPack ×2, productBusinessPartnerActions) |
| High | ~6 (getProducts, components, attachmentsWithMetaData, updateComponentStatuses, …) |

---

## Helper · `getTechPackResourceCountMap(productId, partnerId, workspaceContext, parentProductId, ctx)` — Very High
The most complex logic in the system. Backs Q8/Q9.
1. (🔴 accessControl + 🔴 search) `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission(...)` — ACL-filtered child tree for the product (branches: sample, discussions, discussionThreads, bom, packaging_bom, claim, measurement_set, construction_set, product_watchlist).
2. If `parentProductId`: repeat step 1 for the parent; capture its `attachments_v3` levels 1/2/3.
3. Normalize levels 0–3 in both maps (default `[]`).
4. Merge child `attachments` + `attachments_v3` → `productAttachments` + `discussionAttachments`.
5. `allAttachmentIds = productAttachments + discussionAttachments`.
6. (🔴 attachment) `attachment.getAttachmentsV3(allAttachmentIds)` — hydrate (ACL token, context only).
7. Predicate `isProductPacketAttachments(id)` = matches `document_id`/`human_id` AND `product_packet_props` with `partner_id==partnerId && critical==true`.
8. (🔴 search) **7 elastic slice queries** (independent, but awaited **sequentially** today — perf defect, ADR-015 pin-down 2): samples, criticalDiscussions, measurementSets, claims, boms, constructions, watchlists. Filter samples by workspaceContext or `sampleType.code ∈ {200,135}`.
9. From critical discussions derive `parentDiscussionIds`, `criticalDiscussionIds`, `criticalThreadIds` (dedup).
10. If critical ids exist → (🔴 search) `searchAttachmentsByParentResources(allCriticalIds)`.
11. Filter `discussionAttachments` through the predicate.
12. Build & return `ResourcesCount {productId, partnerId, workspaceContext, productAttachments, discussionAttachments, discussions, sample, measurementSets, claims, productBoms (type==1), packagingBoms (type==2), constructions, watchlists}`.
**EXT:** accessControl 🔴 (context), attachment 🔴, search 🔴 ×8. **Migration:** facade-then-federate (draft ADR-015 Option B; catalogue "Option D (hybrid)") — see `complexStories/techpack/01-adr-techpack.md` §1 for the authoritative 14-step breakdown.

## Query Resolvers (18)

| # | Query | Complexity | Pseudo-logic (REST + EXT) |
|---|-------|-----------|---------------------------|
| Q1 | `getProducts(page,size,q,filter,resourceType,resourceId,includeBoms,includeClaims,includeMeasurementSets,includeProductDetails)` | **High** | (🔴 search) `getFilteredProductsListing` (elastic, defaults `?? true`) → ids → (internal) `getPage({products:ids,...})` `GET ${v1}?productId=&page=0&size=&sort=createdDate,desc` → merge elastic flags (boms/claims/measurementSets/samples/sampleIds/hasSamples* …) onto canonical records. Two-stage hydration. |
| Q2 | `getProductTemplates(...10 includes)` | **Medium** | (🔴 search) `getFilteredProductsListing({resourceType:'product', includeBoms:false, ...flags, types})` → return elastic response, no 2nd hydration. |
| Q3 | `getProduct(id)` | Low | (internal) `getByID.load(id)` `GET ${v1}?productId={id}` → camelCase or null. DataLoader-batched. |
| Q4 | `getCopyStatus(id)` | Low | (internal) `getCopyStatus.load(id)` `GET ${v2}/count/resource-type?copyId={id}` (not batched). |
| Q5 | `getCategories(type,resourceId,resourceType,productType=100)` | Medium | (🔴 search) `getProductCategories` `GET ${elastic}/search/${snake_case(type)}?...` → `ProductsCategories` (polymorphic `categories` resolved in field layer). |
| Q6 | `getProductsByIds(ids)` | Low | (internal) `getByIdList.load(ids)` `GET ${v1}?productId={csv}&page=0&size=10000&sort=createdDate,desc`; primes `getByID`. |
| Q7 | `getProductStatus` | Low · cacheable | (internal) `getStatus.load()` master status list. |
| Q8 | `getProductTechPackCountV1(productId,partnerId,workspaceContext,parentProductId)` | **Very High** | → `getTechPackResourceCountMap(...)` (helper above). |
| Q9 | `getProductTechPackBulkCountV1(bulk[])` | **Very High** | `Promise.all(bulk.map(i => getTechPackResourceCountMap(i...).then(r => out.push(r))))`. **Latent bug:** result order = completion order, not input order — fix on port (key/sort by productId). |
| Q10 | `getProductVersions(id)` | Low | (internal) `getVersions.load({id})` `GET ${v1}/{id}/versions?page=0&size=10000`. |
| Q11 | `getRatingByTcin(tcin)` | Medium | (🔵 external rating) `GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={API_KEY}` (`skipJsonParse`); `JSON.parse`→`{averageRating, reviewCount}`; catch → null. **Secret → Vault.** |
| Q12 | `getProductRules` | Low | (internal) `getAllRules.load()` `GET ${base}/spark_rules/v1` → `content`. |
| Q13 | `getProductRulesById(id)` | Low | (internal) `getRuleById.load(id)` `GET ${base}/spark_rules/v1/{id}`. |
| Q14 | `getAllAvailableRules` | Low | (internal) `getAvailableRules.load()` `GET …/spark_rules/v1/rules`. |
| Q15 | `getProductDeptRules(productIds,departmentIds,activeOnly=true)` | Low | flag fork: `USE_NEW_RULES_API ? ruleLibrary.searchRuleLibrary : product.searchProductDeptRules` `GET …/spark_rules/v1/search?...`. |
| Q16 | `getProductBPRules(productIds,businessPartnerIds,activeOnly)` | Low | same as Q15 with `businessPartnerIds`. |
| Q17 | `searchProductRules(productIds,departmentIds,businessPartnerIds,activeOnly)` | Medium | flag fork; legacy `search_mapped` response → `productRuleResponseTransformer` → camelCase. |
| Q18 | `getProductTemplateById(id)` | Low | (internal) `getByID.load(id)` → `response || {}` (empty object on miss — preserve). |

## Mutation Resolvers (20 implemented + 3 deferred)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `addProduct(workspaceId, sparkProduct, copyProduct)` | Medium | `POST ${v1}` + optional `copyProductToProduct(copyProduct)` (🔴 attachment/workspace) + workspace association (🔴 workspaceV2). |
| M2 | `addProducts(workspaceId, products)` | Medium | bulk `POST ${v1}/bulk` + attachment-link side-effects (no rollback — preserve, flag). |
| M3 | `bulkUpdateProducts(products)` | Medium | `PUT ${v1}/mass_update`. |
| M4 | `updateProduct(input, copyProduct)` | Medium | `PUT ${v1}/{id}` + optional copy + archive removed-template attachments (template branch, 🔴 attachment). |
| M5 | `carryForwardProduct(productId, carryForwardProductInput)` | Medium | `PUT ${v1}/{productId}/carry_forward/{workspaceId}` — uses every field on the input; verify mapping. |
| M6 | `addTeamsToProduct(productId, teamIds, workspaceIds, newPartners)` | Low | `POST ${v1}/{productId}/resources/bulk` + manage_workspace_teams. |
| M7 | `addBusinessPartnersToProductWithType(productId, partners)` | Low | `POST ${v1}/{productId}/partners-add/bulk`. |
| M8 | `removeProductResources(productId, resourceIds)` | Low | `DELETE ${v1}/{productId}/resources/bulk`. |
| M9 | `updateBusinessPartnerStatuses(productId, statusInput)` | Low | `PUT ${v1}/{productId}/status_update/bulk`. |
| M10 | `productBusinessPartnerActions(actionType, values)` | **Very High** | ~220-line dispatcher: `REMOVE_PARTNER` / `DROP_PARTNER` / `UNDROP_PARTNER`. Partner update + cleanup across `recentlyViewed`/`todo`/`favorite`/`sampleV2`/`accessControl` (drop/undrop). No rollback. (ACL token, context.) |
| M11 | `updateViewToggle(toggleInput)` | Low | `PUT ${v1}` view toggle. |
| M12 | `updateWorkspaceAttributes(productId, workspaceAttributesInput)` | Low | `PUT ${v1}/{productId}` workspace attrs. |
| M13 | `updateProductTeamsWorkspaceContext(productId, add, remove)` | Low | `PUT` team-workspace context. |
| M14 | `linkProduct(parent, child)` | Low | `PUT` link — **throws on backend error** (only mutation that does). |
| M15 | `unlinkProduct(parent, child)` | Low | `PUT` unlink. |
| M16 | `addProductRule(rule)` | Low | `POST …/spark_rules/v1`. |
| M17 | `updateProductRule(rule)` | Low | `PUT …/spark_rules/v1/{id}`. |
| M18 | `deleteProductRule(ruleId)` | Low | `DELETE …/spark_rules/v1/{id}` → Boolean. |
| M19 | `updateComponentStatus(productComponents)` | Low | bulk `PUT ${v1}/component_status_update/bulk`. |
| M20 | `updateComponentStatuses(productId, ids, status)` | **High** | parallel fan-out to 5 loaders: `bom`/`measurement`/`productDetail`/`packaging` (internal) + `claim` (🟡 EXT). **Shadow-var bug** — fix on port. |
| ⏭ | `removeProductBusinessPartner`/`dropProductBusinessPartner`/`unDropProductBusinessPartner` | — | schema-drift wrappers; traffic routes through M10. Confirm consumers before deleting. |

## Field Resolvers (grouped by story — see 04-stories G-phase)
`Product` has ~50 field resolvers. Highlights:
- **Very High:** `attachmentsWithMetaData` (G-01, ~150 lines, ACL + 5-source merge), `components` (G-02, ~190 lines, N+1 ACL — batch on port).
- **Medium:** `attachmentsV3`/`attachments`/`attachmentSummary` (G-03), `ProductsCategories.categories` 12-case dispatcher + Doppler (G-04), `samples`/`sampleIds`/`elasticSamplesList` (G-05, stops reading `info.variableValues`), `teams`/`discussionsV2`/`discussionsCount`/`workspaces` (G-06), `vendorAttributes`/`businessPartners`/`droppedPartners`/`unDroppablePartners` (G-07, VMM), `measurementSets`/`claims`/`bom`/`productBom`/`packagingBom` (G-08, internal siblings), `productWorkspaceAttributes`/`productWorkspaceInfo` (G-09, deferred `designCycle`), `ancestryProducts`/`rating`/`reservedDpcis` (G-10, rating+apex), `notRemovablePartnerIds`/`notRemovableWorkspaceIds`/`associateProductsAsks`/`variations` (G-11, replace reflective resolver calls with service methods).
- **Bug fix:** `Product.division` calls the *department* loader — wire to `DivisionService` (G-12).
- **Trivial groups:** `SPARK_ProductRules.*`, `tags`, `tcins`, `SPARK_Tcin.itemDetails` (CORONA), `SPARK_PackagingAttribute.spg`, `ProductComponentStatus.updatedBy`, `VMM_BusinessPartnerCategory.*`, `MasterProductStatus.*`, template fields (G-13); `createdBy`/`updatedBy`/`status`/`department`/`clazz`/`brand` etc. (G-14).
- **Categories polymorphism:** `SPARK_Categories.__resolveType` 12-case + default `IG_Clazz_Filter` (A-04 type resolver).

## EXT Service Call Inventory (summary)
**12 EXT keys + 6 platform** — 4 🔴 (attachment, workspaceV2, search, [accessControl=context]) · 6 🟡 (claim, relationship, userAttributes, teamV2, discussion, sampleV2, tag) · 2 🔵 (recentlyViewed/todo/favorite, ruleLibrary) · 6 platform 🔵 (VMM, IG, Doppler, CORONA, APEX, BrandCompliance). Internal (same DGS): product, bom, measurement, productDetails, packaging, productAsk, productVariation, fileLibrary.

## Key Findings
- **Highest risk:** TechPack (Q8/Q9, composite-key aggregate), `productBusinessPartnerActions` (M10), `components`/`attachmentsWithMetaData` field resolvers.
- **Latent bugs:** TechPack bulk ordering (Q9); `updateComponentStatuses` shadow var (M20); `Product.division` wrong loader (G-12); `componentStatusUtils.incrementAllContextCounter` never resets.
- **Refactors:** N+1 ACL in `components` → batch; reflective resolver calls (G-11) → service methods; two-stage elastic+canonical (Q1) → shared helper; external rating secret → Vault.
- **Decisions:** `USE_NEW_RULES_API` cutover (3 queries cross to spark-tag DGS); deferred partner wrappers (delete vs keep `@deprecated`); TechPack facade option.
- **Quick wins:** `getProduct`, `getProductsByIds`, `getProductStatus`, rules CRUD, lock-like toggles.

---
**Phase Completed:** Phase 2 · **Domain:** `product` · **EXT:** 12 keys + 6 platforms.
