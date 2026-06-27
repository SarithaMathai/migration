# Phase 1: Schema Inventory — Product

> **Domain:** `product`
> **Target DGS:** `ProductService` (repo: `plm-product`, url: `https://spark-product.dev.target.com`)
> **Pipeline Version:** 1.1
> **Generated:** 2026-05-01
> **Depends on:** None (entry phase)
> **DGS Target Status:** Green-field (no existing DGS schema)

---

## Context Registration

```js
// from spark-internal-graphql/packages/data-source-spark/src/context.js
product: new Proxy({ ServiceClass: ProductService, serviceArgs: [config.endpoints.product, headers, logContext] }, lazyLoadService),
```

**Auth pattern:** SPARK-Capability-Token V1 (injected at runtime via `getUserPermissionsJWT`; most reads use standard bearer headers)

### Co-located Domains (same backend URL `config.endpoints.product`)

| Loader Key | Service Class | Schema File |
|-----------|--------------|------------|
| `product` | `ProductService` | `SPARK_Product.graphql` |
| `pom` | `PomService` | `SPARK_Pom.graphql` |
| `measurement` | `MeasurementService` | `SPARK_Measurement.graphql` |
| `bom` | `BomService` | `SPARK_Bom.graphql` |
| `impression` | `ImpressionService` | `SPARK_Impression.graphql` |
| `measurementTemplate` | `MeasurementTemplateService` | `SPARK_MeasurementTemplate.graphql` |
| `sizeTemplate` | `SizeTemplateService` | `SPARK_SizeTemplate.graphql` |
| `specificationsTemplate` | `SpecificationsTemplateService` | `SPARK_SpecificationTemplate.graphql` |
| `ProductDetails` | `ProductDetailsService` | `SPARK_ProductDetail.graphql` |
| `watchlist` | `WatchlistService` | `SPARK_Watchlist.graphql` |
| `tightFit` | `TightFitService` | `SPARK_TightFit.graphql` |
| `packaging` | `PackagingService` | `SPARK_Packaging.graphql` |
| `productPlan` | `ProductPlanService` | `SPARK_ProductPlan.graphql` |
| `productAsk` | `ProductAskService` | *(part of ProductPlan)* |
| `productVariation` | `ProductVariationService` | `SPARK_Variation.graphql` |
| `fileLibrary` | `FileLibraryService` | `SPARK_FileLibrary.graphql` |

All co-located domains will eventually share the **`plm-product`** DGS service.

---

## Source File Manifest

### Schema Files

| File | Path | Lines | Types | Inputs | Enums | Queries | Mutations |
|------|------|-------|-------|--------|-------|---------|-----------|
| `SPARK_Product.graphql` | `spark-internal-graphql/packages/data-source-spark/src/schemas/SPARK_Product.graphql` | 781 | 33 | 30 | 0 | 18 | 23 |

**Type list:** `SPARK_Product`, `SPARK_Rating`, `SPARK_ChildProducts`, `SPARK_AncestryProducts`, `SPARK_PartnerTcins`, `SPARK_PartnerReservedDpci`, `CORONA_ItemDetails`, `SPARK_Tcin`, `SPARK_ReservedDpci`, `SPARK_CodeName`, `SPARK_ProductMaterials`, `SPARK_ProductLibraryResource`, `SPARK_PackagingAttribute`, `ProductVendorAttributes`, `SPARK_ProductStatus`, `SPARK_CarryForwardProductStatus`, `SPARK_CarryForwardProductAllStatus`, `SPARK_MasterProductStatus`, `SPARK_ProductBulkType`, `SPARK_ProductsPaged`, `SPARK_ProductsCategories`, `SPARK_ResourcesCount`, `SPARK_AttachmentSummary`, `SPARK_ProductRules`, `SPARK_AvailableRules`, `DopplerDepartment`, `SPARK_ProductTemplatesList`, `SPARK_ProductTemplateAttachments`, `SPARK_ProductTemplateStatus`, `SPARK_ProductComponentsCounts`, `SPARK_PurchaseOrderDetails`, `VMM_BusinessPartnerCategory`, `ProductComponentStatus`

**Input list (30):** `SPARK_ComponentStatusInput`, `SPARK_ComponentIdsInput`, `ProductComponentStatusUpdateInput`, `SPARK_CopyProductInput`, `SPARK_ProductTeamInput`, `SPARK_BombsWithMaterialInput`, `Spark_bomMaterialDtosInput`, `SPARK_ToggleInput`, `SPARK_ProductPartnerActionInput`, `CarryForwardProductInput`, `Bulk_CarryForwardProductInput`, `SPARK_ProductPartnerStatusInput`, `SPARK_ProductInput`, `SPARK_ProductPartnerInput`, `SPARK_ProductUpdateInput`, `SPARK_ProductMaterialsInput`, `SPARK_ProductLibraryResourceInput`, `SPARK_PackagingAttributeInput`, `SPARK_ProductTemplateRemovedAttachments`, `SPARK_VendorAttributeInput`, `SPARK_ProductTechPackCountInput`, `SPARK_ProductWorkspaceAttributesInput`, `SPARK_ProductWorkspaceInfoInput`, `WorkspaceTeamPair`, `WorkspaceTeamContextInput`, `WorkspaceStatusPairInput`, `DopplerDepartmentInput`, `SPARK_ProductRuleCreateInput`, `SPARK_ProductRuleUpdateInput`, `SPARK_WorkspaceInfoPartnerInput`

**Cross-domain type references in schema:** `VMM_BusinessPartner`, `VMM_Brand`, `IG_Department`, `IG_Division`, `IG_Clazz`, `SPARK_Tag`, `SPARK_Attachment`, `SPARK_Attachment_With_Meta_Data`, `SPARK_SampleV2`, `SPARK_MeasurementsPaged`, `SPARK_Claims`, `SPARK_ProductDetails`, `SPARK_BomPaged`, `SPARK_SearchAttachmentsPaged`, `SPARK_SearchComponentsPaged`, `SPARK_DiscussionElastic`, `SPARK_TeamPaged`, `SPARK_TeamPagedV2`, `SPARK_WorkspacesPagedV2`, `SPARK_ProductVariation`, `SPARK_ProductAsk`, `SPARK_SpgFileLibrary`

### Resolver Files

| File | Path | Lines | Query Resolvers | Mutation Resolvers | Field Resolvers | Imports |
|------|------|-------|-----------------|--------------------|-----------------|---------|
| `SPARK_Product.js` | `spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js` | 2629 | 18 | 23 | 60+ | 8 services, 14 utils |

**Exported helper functions (file scope, used by multiple resolvers):**
- `orderProductAttachments` (line ~60) — sorts `attachmentsWithMetaData` by resource type then created date
- `copyProductToProduct` (line ~72) — calls `getUserPermissionsJWT` + `product.copyProduct` loader; used by `addProduct` and `updateProduct`
- `getTechPackResourceCountMap` (line ~83) — large helper (~200 lines); called by `getProductTechPackCountV1` and `getProductTechPackBulkCountV1`

### Service Files

| File | Path | Lines | Methods | Base URL | Auth |
|------|------|-------|---------|----------|------|
| `Product.js` | `spark-internal-graphql/packages/data-source-spark/src/services/Product.js` | 589 | 41 | `process.env.PRODUCT_ENDPOINT` + `/enterprise_product_development_products/v1\|v2` | SPARK-Capability-Token V1 |

**All 41 service methods:**
`getPage`, `getByID`, `getCopyStatus`, `createBulk`, `bulkUpdate`, `addTeams`, `updateBusinessPartnerStatuses`, `dropUndropProductBusinessPartner`, `dropProductBusinessPartner`, `unDropProductBusinessPartner`, `updateProduct`, `carryForwardProduct`, `removeProductResources`, `removeProductBusinessPartner`, `deletePartnerWorkspaceStatuses`, `getFilteredProducts`, `getFilteredProductsListing`, `getFilteredSamples`, `getProductCategories`, `getByIdList`, `addProduct`, `getStatus`, `updateViewToggle`, `updateWorkspaceAttributes`, `getWorkspaceProducts`, `copyProduct`, `addBusinessPartnersWithType`, `updateProductTeamsWorkspaceContext`, `getVersions`, `linkProduct`, `unlinkProduct`, `getRatingByTcin`, `getAllRules`, `getAllInsightsRules`, `getRuleById`, `addRule`, `updateRule`, `deleteRule`, `getAvailableRules`, `searchProductDeptRules`*, `searchProductBPRules`*, `searchProductRules`*, `updateComponentStatus`

> *conditional: these three methods are only registered when `USE_NEW_RULES_API === false`; when the flag is `true`, the resolver delegates to `ctx.loaders.ruleLibrary.searchRuleLibrary`.

**Additional REST endpoints used in `Product.js`:**
- `process.env.PRODUCT_SEARCH_ENDPOINT` — elastic search, used by `getFilteredProducts`, `getFilteredProductsListing`, `getFilteredSamples`, `getProductCategories`, `getWorkspaceProducts`
- `process.env.SEARCH_ENDPOINT + '/requests/v1'` — copy request endpoint (`copyProduct`)
- `process.env.RATING_ENDPOINT` — bazaarvoice ratings (`getRatingByTcin`)
- `process.env.PRODUCT_ENDPOINT + '/spark_rules/v1'` — product rules CRUD

### Utils Files Referenced

| File | Path | Lines | Functions | Scope |
|------|------|-------|-----------|-------|
| `attachmentUtils.js` | `utils/Product/attachmentUtils.js` | 329 | `initialCountsByBp`, `orderAttachmentsByType`, `orderComponentsByDate`, `convertV2AccessToV3`, `resolveRelationIds`, `get3DmodelFile`, `addPartnersToCountObject`, `createAttachmentPaged`, `filterAttachmentsOrComponents`, `getProductOrWorkSpaceAttachments` | domain-specific |
| `partnerUtils.js` | `utils/Product/partnerUtils.js` | 108 | `getFinalPartnerStatuses`, `filterOutDesignPartners`, `getProductStatus` | domain-specific |
| `productUtils.js` | `utils/Product/productUtils.js` | 58 | `getNotRemovableWorkspaceIds`, `rulesRequestTransformer`, `productRuleResponseTransformer`, `sanitizedProductDescription` | domain-specific |
| `teamUtils.js` | `utils/Product/teamUtils.js` | 30 | `filterTeamsByPartnerOrWorkspaceId` | domain-specific |
| `getReservedDpcisFromApex.js` | `utils/Product/getReservedDpcisFromApex.js` | 115 | `calculateDpciStatus`, `getReservedDpcisFromApex` | domain-specific |
| `userGroupUtils.js` | `utils/Product/userGroupUtils.js` | 10 | *(referenced but not directly imported in resolver)* | domain-specific |
| `commonLoaders.js` | `utils/commonLoaders.js` | 884 | `getUserPermissionsJWT`, `filterResourcesByPartner`, `addBulkRelationShip`, `getPermissionMapForBulkACLCall`, `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission`, `getUnDroppablePartners`, and many others | core |
| `convertFunctions.js` | `utils/convertFunctions.js` | ~350 (est.) | `deepToCamelCase`, `deepToSnakeCase`, `buildURLParam`, `buildSampleURLParam`, `buildCommaSeparatedString`, `getStatusName`, `getTrackingStatusName`, `getEvalStatusName` | core |
| `vmmUtils.js` | `utils/vmmUtils.js` | 124 | `loadManyIncludeEmptyResponse`, `loadBps`, `loadBpsWithType` | core |
| `accessControlUtils.js` | `utils/accessControlUtils.js` | 53 | `getAccessControlBatch` | core |
| `discussionUtils.js` | `utils/discussionUtils.js` | 720 | `CHUNK_SIZE`, `getDiscussionThreadsBatch`, `getDiscussionsBatch`, `getDiscussionRepliesV2` | core |
| `removePartnerUtils.js` | `utils/removePartnerUtils.js` | ~50 (est.) | `getProductPartnersNotRemovable` | core |
| `componentStatusUtils.js` | `utils/componentStatusUtils.js` | ~40 (est.) | `getCountByComponents` | core |
| `ProductAskUtils.js` | `utils/ProductAskUtils.js` | ~80 (est.) | `getProductAsksForWorkspace` | domain-specific |
| `resolvePaging.js` | `utils/resolvePaging.js` | ~20 (est.) | `resolvePaging` | core |

### Config Files

| File | Path | Purpose |
|------|------|---------|
| `constants.js` | `utils/constants.js` | `SAMPLE_EVALUTION` constant (evaluation status code), `RESOURCE_TYPES`, `RESOURCE_TYPE_PREFIXES` |
| `businessPartner.js` | `config/businessPartner.js` | `BusinessPartnerRole.DESIGN_PARTNER.code` (= 5) — used to skip design partners from sample drop/undrop |
| `constants.js` | `config/constants.js` | `SPARK_GATEWAY_API_KEY` — used as `ratingKey` for Bazaarvoice ratings |

---

## Target DGS — Existing Files

**Repo:** `plm-product`
**Schema dir:** `plm-product/apps/app/src/main/resources/schema/`
**Code root:** `plm-product/apps/app/src/main/kotlin/`

> **Status:** Green-field migration — no existing DGS code found in workspace. Target repo `plm-product` is not present locally.

### Existing Schemas

| File | Path | Lines | Defined Types | Defined Queries | Defined Mutations | Commented-out fields |
|------|------|-------|---------------|----------------|-------------------|---------------------|
| _(no existing files — green-field migration)_ | | | | | | |

### Existing Data Fetchers

| File | Path | Lines | Operations Wired |
|------|------|-------|------------------|
| _(no existing files — green-field migration)_ | | | |

---

## Import Graph

```text
SPARK_Product.js
├── services/Product.js                                          (primary)
├── resolvers/product/SPARK_Measurement.js                       (EXT — measurement domain)
├── resolvers/SPARK_SampleV2.js                                  (EXT — sample domain)
├── resolvers/product/SPARK_Claims.js                            (EXT — claim domain)
├── resolvers/product/SPARK_Bom.js                               (EXT — bom domain)
├── resolvers/product/SPARK_ProductDetail.js                     (EXT — productDetails domain)
├── resolvers/SPARK_Attachment.js                                (EXT — attachment domain)
├── resolvers/product/SPARK_Packaging.js                         (EXT — packaging domain)
├── resolvers/SPARK_WorkspaceV2.js                               (EXT — workspace domain)
├── resolvers/SPARK_UserAttributes.js                            (EXT — user profile domain)
├── utils/Product/attachmentUtils.js
├── utils/Product/partnerUtils.js
├── utils/Product/teamUtils.js
├── utils/Product/productUtils.js
├── utils/Product/getReservedDpcisFromApex.js
├── utils/ProductAskUtils.js
├── utils/commonLoaders.js
├── utils/convertFunctions.js
├── utils/vmmUtils.js
├── utils/accessControlUtils.js
├── utils/discussionUtils.js
├── utils/removePartnerUtils.js
├── utils/componentStatusUtils.js
├── utils/resolvePaging.js
├── services/batchers/getTagsBatched.js                          (batching util)
└── config/businessPartner.js

services/Product.js
├── utils/convertFunctions.js          (deepToCamelCase, deepToSnakeCase, build* helpers)
├── utils/deleteOne.js
├── utils/loadListing.js
├── utils/loadOne.js
├── utils/postOne.js
├── utils/putOne.js
├── utils/Product/productUtils.js      (productRuleResponseTransformer, rulesRequestTransformer)
├── config/constants.js                (SPARK_GATEWAY_API_KEY)
└── services/SparkService.js           (base class)
```

---

## Cross-Domain Reference Table

| Source Type | Field | Referenced Type | Referenced Domain | Loader Key | URL | Strategy | Severity |
|------------|-------|----------------|-------------------|------------|-----|----------|----------|
| `SPARK_Product` | `businessPartners` | `VMM_BusinessPartner` | VMM (external platform) | `vmm` | stgapi-internal.target.com | Gateway Stitch | 🟡 |
| `SPARK_Product` | `droppedPartners` | `VMM_BusinessPartner` | VMM | `vmm` | stgapi-internal.target.com | Gateway Stitch | 🟡 |
| `SPARK_Product` | `brand` | `VMM_Brand` | VMM (external platform) | `brand` | stgapi-internal.target.com | Gateway Stitch | 🔵 |
| `SPARK_Product` | `brands` | `[VMM_Brand]` | VMM | `brand` | stgapi-internal.target.com | Gateway Stitch | 🔵 |
| `SPARK_Product` | `department` | `IG_Department` | Item Groups (external platform) | `ig.department` | stgapi-internal.target.com | Gateway Stitch | 🔵 |
| `SPARK_Product` | `departments` | `[DopplerDepartment]` | Doppler (external platform) | `doppler` | stgapi-internal.target.com | Gateway Stitch | 🟡 |
| `SPARK_Product` | `division` | `IG_Division` | Item Groups | `ig.division` | stgapi-internal.target.com | Gateway Stitch | 🔵 |
| `SPARK_Product` | `clazz` | `IG_Clazz` | Item Groups | `ig.clazz` | stgapi-internal.target.com | Gateway Stitch | 🔵 |
| `SPARK_Product` | `tags` | `[SPARK_Tag]` | Tag domain | `tag` | spark-tag endpoint | EXT Service | 🔵 |
| `SPARK_Product` | `workspaces` | `SPARK_WorkspacesPagedV2` | Workspace domain | `search` | elastic | EXT Service | 🟡 |
| `SPARK_Product` | `attachments` | `[SPARK_Attachment]` | Attachment domain | `attachment` | spark-attachment endpoint | EXT Service | 🔴 |
| `SPARK_Product` | `attachmentsWithMetaData` | `[SPARK_Attachment_With_Meta_Data]` | Attachment + Discussion + Sample | multiple | multiple | EXT Service | 🔴 |
| `SPARK_Product` | `attachmentsV3` | `SPARK_SearchAttachmentsPaged` | Attachment domain | `search` + `attachment` | elastic | EXT Service | 🔴 |
| `SPARK_Product` | `attachmentSummary` | `SPARK_AttachmentSummary` | Attachment domain | `search` | elastic | EXT Service | 🟡 |
| `SPARK_Product` | `samples` | `[SPARK_SampleV2]` | Sample domain | `sampleV2` / `relationship` | multiple | EXT Service | 🟡 |
| `SPARK_Product` | `measurementSets` | `SPARK_MeasurementsPaged` | Measurement domain | `measurement` | spark-product backend | Internal |  |
| `SPARK_Product` | `claims` | `[SPARK_Claims]` | Claim domain | `claim` | spark-product backend | Internal |  |
| `SPARK_Product` | `bom` | `SPARK_BomPaged` | BOM domain | `bom` | spark-product backend | Internal |  |
| `SPARK_Product` | `components` | `SPARK_SearchComponentsPaged` | BOM+Measurement+Claims+PD+PKG | multiple | multiple | EXT Service | 🔴 |
| `SPARK_Product` | `teams` | `SPARK_TeamPaged` | TeamV2 domain | `teamV2` | spark-user-profile | EXT Service | 🟡 |
| `SPARK_Product` | `discussionsCount` | `Int` | Discussion domain | `discussion` | spark-discussion | EXT Service | 🔵 |
| `SPARK_Product` | `tcins` | `[SPARK_PartnerTcins]` | APEX/Corona | `apex` / `coronaItems` | stgapi-internal.target.com | Gateway Stitch | 🟡 |
| `SPARK_Product` | `reservedDpcis` | `[SPARK_PartnerReservedDpci]` | APEX | `apex` | stgapi-internal.target.com | Gateway Stitch | 🟡 |
| `SPARK_Product` | `variations` | `[SPARK_ProductVariation]` | ProductVariation domain | `productVariation` | spark-product backend | Internal |  |
| `SPARK_Product` | `rating` | `SPARK_Rating` | Bazaarvoice (external) | product.getRatingByTcin | `RATING_ENDPOINT` | EXT Service | 🔵 |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Schema files | 1 |
| Resolver files | 1 |
| Service files | 1 |
| Utils files | 15 (6 domain-specific, 9 core) |
| Config files | 3 |
| Total source lines | ~4,600 (resolver 2629 + service 589 + schema 781 + utils ~600 est.) |
| Query operations | 18 |
| Mutation operations | 23 |
| Field resolvers | 60+ |
| Cross-domain references | 40 |
| EXT Service calls (provisional) | 29 |
| Existing DGS schemas | 0 (green-field) |
| Existing DGS data fetchers | 0 (green-field) |

---

*Generated by spark-migration pipeline v1.1 — Phase 1 complete. Proceed to [02-resolver-analysis.md](./02-resolver-analysis.md).*
