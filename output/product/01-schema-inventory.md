# Phase 1 — Schema Inventory: `product` Domain

> Source:    `spark-internal-graphql/packages/data-source-spark/src/`
> Target DGS: `plm-product` (green-field)
> Generated: Phase 1 of 4 — Schema Inventory only. No pseudo-logic yet.

---

## 1. Context Registration

From [context.js](spark-internal-graphql/packages/data-source-spark/src/context.js#L172):

```js
product: new Proxy(
  { ServiceClass: ProductService,
    serviceArgs: [config.endpoints.product, headers, logContext] },
  lazyLoadService,
)
```

| Field | Value |
|---|---|
| Loader key | `product` |
| Service class | `ProductService` ([services/Product.js](spark-internal-graphql/packages/data-source-spark/src/services/Product.js)) |
| Backend URL config | `config.endpoints.product` (env: `PRODUCT_ENDPOINT`) |
| Repo | `spark-product` |
| Target DGS | `plm-product` |
| Auth | `X-AUTH-TOKEN` (Spark capability token) + `Authorization: Bearer …` + `X-Api-Id` + `X-Tracing-ID` |

### Service-internal endpoints (constructed in [Product.js#L23-L36](spark-internal-graphql/packages/data-source-spark/src/services/Product.js#L23-L36))

| Field | Value |
|---|---|
| `endpointv1` | `${PRODUCT_ENDPOINT}/enterprise_product_development_products/v1` |
| `endpointv2` | `${PRODUCT_ENDPOINT}/enterprise_product_development_products/v2` |
| `elasticSearchEndpoint` | `process.env.PRODUCT_SEARCH_ENDPOINT` |
| `endpointCopy` | `${SEARCH_ENDPOINT}/requests/v1` |
| `ratingEndpoint` | `process.env.RATING_ENDPOINT` (external rating service) |
| `ratingKey` | `SPARK_GATEWAY_API_KEY` (from `config/constants`) |

---

## 2. Co-Located Domains (Same `spark-product` Backend → Same DGS `plm-product`)

All loaders below are wired with `config.endpoints.product` in [context.js](spark-internal-graphql/packages/data-source-spark/src/context.js):

| Loader Key | Service Class | Notes |
|---|---|---|
| `product` | `ProductService` | **This domain** |
| `pom` | `PomService` | Points of Measure |
| `fileLibrary` | `FileLibraryService` | Asset/document library |
| `measurement` | `MeasurementService` | Measurement sets |
| `bom` | `BomService` | Bill of Materials |
| `impression` | `ImpressionService` | Visual impressions |
| `measurementTemplate` | `MeasurementTemplateService` | Measurement templates |
| `sizeTemplate` | `SizeTemplateService` | Size templates |
| `specificationsTemplate` | `SpecificationsTemplateService` | Spec templates |
| `ProductDetails` | `ProductDetailsService` | Construction sets |
| `watchlist` | `WatchlistService` | Product watchlist |
| `tightFit` | `TightFitService` | Tight-fit calculator |
| `packaging` | `PackagingService` | Packaging BOMs |
| `productPlan` | `ProductPlanService` | Product plans |
| `productAsk` | `ProductAskService` | Vendor asks |
| `productVariation` | `ProductVariationService` | Product variations |

> **Federation implication:** All 16 services migrate into the **same `plm-product` DGS module**. Sibling field resolvers that today live in the `SPARK_Product` resolver (e.g., `bom`, `claims`, `measurementSets`, `productBom`, `packagingBom`) become **same-service @DgsData fetchers**, not federation entity references.

---

## 3. Source File Manifest

### 3a. Schema

| File | Path | Lines | Queries | Mutations | Subs | Types | Inputs |
|---|---|---|---|---|---|---|---|
| `SPARK_Product.graphql` | [schemas/SPARK_Product.graphql](spark-internal-graphql/packages/data-source-spark/src/schemas/SPARK_Product.graphql) | 800 | 18 | 23 | 0 | ~35 | ~25 |

### 3b. Resolvers

| File | Path | Lines | Queries | Mutations | Field Resolvers |
|---|---|---|---|---|---|
| `SPARK_Product.js` | [resolvers/SPARK_Product.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js) | 2,629 | 18 | 23 | 60+ (across 14 type-level resolver blocks) |

**Type-level resolver blocks in `SPARK_Product.js`:**

| Block | Starting Line | Purpose |
|---|---|---|
| `Query` | [296](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js#L296) | 18 query resolvers |
| `Mutation` | [538](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js#L538) | 23 mutation resolvers |
| `SPARK_ResourcesCount` | [1104](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js#L1104) | 1 field (`productThumbnailId`) |
| `SPARK_Product` | [1112](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js#L1112) | ~50 field resolvers — the main entity |
| `SPARK_AncestryProducts` | 2127 | 1 field |
| `SPARK_ProductBulkType` | 2134 | passthrough wrapper |
| `SPARK_ProductsPaged` | 2138 | passthrough wrapper |
| `SPARK_ProductTemplatesList` | 2144 | passthrough wrapper |
| `SPARK_ProductsCategories` | 2150 | nested category resolution |
| `SPARK_Categories` | 2467 | `__resolveType` union resolution |
| `SPARK_MasterProductStatus` | 2510 | 1 field |
| `SPARK_Tcin` | 2514 | 2 fields (`itemDetails` via CORONA) |
| `SPARK_ProductRules` | 2519 | 4 fields (`departments`, `businessPartners`, `insightsClassExclusion`) |
| `DopplerDepartment` | 2554 | 5 fields (Doppler ext platform) |
| `ProductComponentStatus` | 2599 | 1 field (`updatedBy`) |
| `SPARK_PackagingAttribute` | 2609 | 1 field (`spg`) |
| `VMM_BusinessPartnerCategory` | 2625 | extension of VMM type (gateway-stitched) |

### 3c. Service

| File | Path | Lines | Public Methods (loaders) |
|---|---|---|---|
| `Product.js` | [services/Product.js](spark-internal-graphql/packages/data-source-spark/src/services/Product.js) | 589 | 42 |

**Complete method roster (all assigned in constructor as DataLoaders):**

| Group | Methods |
|---|---|
| Reads | `getPage`, `getByID`, `getByIdList`, `getCopyStatus`, `getFilteredProducts`, `getFilteredProductsListing`, `getFilteredSamples`, `getProductCategories`, `getStatus`, `getWorkspaceProducts`, `getVersions`, `getRatingByTcin` |
| Mutations — product CRUD | `addProduct`, `createBulk`, `bulkUpdate`, `updateProduct`, `carryForwardProduct`, `removeProductResources` |
| Mutations — partners | `addBusinessPartnersWithType`, `updateBusinessPartnerStatuses`, `dropProductBusinessPartner`, `unDropProductBusinessPartner`, `dropUndropProductBusinessPartner` (JWT-curried), `removeProductBusinessPartner` (JWT-curried), `deletePartnerWorkspaceStatuses` |
| Mutations — teams | `addTeams`, `updateProductTeamsWorkspaceContext` |
| Mutations — workspace attrs | `updateViewToggle`, `updateWorkspaceAttributes` |
| Mutations — relationships | `linkProduct`, `unlinkProduct`, `copyProduct` (JWT-curried) |
| Mutations — components | `updateComponentStatus` |
| Rules | `getAllRules`, `getAllInsightsRules`, `getRuleById`, `addRule`, `updateRule`, `deleteRule`, `getAvailableRules`, `searchProductDeptRules`, `searchProductBPRules`, `searchProductRules` |

### 3d. Utilities (imported by `SPARK_Product.js`)

| Util File | Path | Imported Functions | Cross-Domain? |
|---|---|---|---|
| `commonLoaders.js` | [utils/commonLoaders.js](spark-internal-graphql/packages/data-source-spark/src/utils/commonLoaders.js) | `getUserPermissionsJWT`, `filterResourcesByPartner`, `addBulkRelationShip`, `getPermissionMapForBulkACLCall`, `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission`, `getUnDroppablePartners` | Shared infra |
| `convertFunctions.js` | [utils/convertFunctions.js](spark-internal-graphql/packages/data-source-spark/src/utils/convertFunctions.js) | `getStatusName`, `getTrackingStatusName`, `getEvalStatusName`, `deepToCamelCase`, `deepToSnakeCase`, `buildURLParam` | Shared infra |
| `resolvePaging.js` | [utils/resolvePaging.js](spark-internal-graphql/packages/data-source-spark/src/utils/resolvePaging.js) | `resolvePaging` | Shared infra |
| `vmmUtils.js` | [utils/vmmUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/vmmUtils.js) | `loadManyIncludeEmptyResponse`, `loadBps`, `loadBpsWithType` | **VMM EXT** |
| `removePartnerUtils.js` | [utils/removePartnerUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/removePartnerUtils.js) | `getProductPartnersNotRemovable` | Domain-specific |
| `Product/attachmentUtils.js` | [utils/Product/attachmentUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/attachmentUtils.js) | `convertV2AccessToV3`, `addPartnersToCountObject`, `filterAttachmentsOrComponents`, `orderComponentsByDate`, `initialCountsByBp`, `getProductOrWorkSpaceAttachments` | Domain-specific |
| `accessControlUtils.js` | [utils/accessControlUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/accessControlUtils.js) | `getAccessControlBatch` | Shared infra (ACL EXT) |
| `Product/partnerUtils.js` | [utils/Product/partnerUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/partnerUtils.js) | `filterOutDesignPartners`, `getFinalPartnerStatuses`, `getProductStatus` | Domain-specific |
| `Product/teamUtils.js` | [utils/Product/teamUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/teamUtils.js) | `filterTeamsByPartnerOrWorkspaceId` | Domain-specific |
| `Product/productUtils.js` | [utils/Product/productUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/productUtils.js) | `getNotRemovableWorkspaceIds`, `productRuleResponseTransformer`, `rulesRequestTransformer` | Domain-specific |
| `componentStatusUtils.js` | [utils/componentStatusUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/componentStatusUtils.js) | `getCountByComponents` | Shared (used across components) |
| `discussionUtils.js` | [utils/discussionUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/discussionUtils.js) | `CHUNK_SIZE`, `getDiscussionThreadsBatch`, `getDiscussionsBatch` | **Discussion EXT** |
| `Product/getReservedDpcisFromApex.js` | [utils/Product/getReservedDpcisFromApex.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/getReservedDpcisFromApex.js) | `getReservedDpcisFromApex` | **APEX EXT (Platform)** |
| `ProductAskUtils.js` | [utils/ProductAskUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/ProductAskUtils.js) | `getProductAsksForWorkspace` | Co-located domain |
| `logger.js` | [utils/logger.js](spark-internal-graphql/packages/data-source-spark/src/utils/logger.js) | `logger` | Shared infra |
| `constants.js` | [utils/constants.js](spark-internal-graphql/packages/data-source-spark/src/utils/constants.js) | `SAMPLE_EVALUTION` | Shared constants |

### 3e. Sibling Resolvers Re-Exported (delegated field implementations)

| File | Path | Purpose |
|---|---|---|
| `product/SPARK_Measurement.js` | [resolvers/product/SPARK_Measurement.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_Measurement.js) | Provides `measurementSets` field logic |
| `SPARK_SampleV2.js` | [resolvers/SPARK_SampleV2.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_SampleV2.js) | Provides `samples` field logic |
| `SPARK_WorkspaceV2.js` | [resolvers/SPARK_WorkspaceV2.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_WorkspaceV2.js) | Exports `getWorkspaceResourceString` |
| `SPARK_UserAttributes.js` | [resolvers/SPARK_UserAttributes.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_UserAttributes.js) | Default-imported as `UserProfileAttributes` |
| `product/SPARK_Claims.js` | [resolvers/product/SPARK_Claims.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_Claims.js) | `claims` field logic |
| `product/SPARK_Bom.js` | [resolvers/product/SPARK_Bom.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_Bom.js) | `bom` / `productBom` field logic |
| `product/SPARK_ProductDetail.js` | [resolvers/product/SPARK_ProductDetail.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_ProductDetail.js) | `productDetails` field logic |
| `SPARK_Attachment.js` | [resolvers/SPARK_Attachment.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Attachment.js) | `attachments` field logic |
| `product/SPARK_Packaging.js` | [resolvers/product/SPARK_Packaging.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_Packaging.js) | `packagingBom` field logic |
| `services/batchers/getTagsBatched.js` | [services/batchers/getTagsBatched.js](spark-internal-graphql/packages/data-source-spark/src/services/batchers/getTagsBatched.js) | Tag batching utility |

### 3f. Config

| File | Path | Purpose |
|---|---|---|
| `businessPartner.js` | [config/businessPartner.js](spark-internal-graphql/packages/data-source-spark/src/config/businessPartner.js) | `BusinessPartnerRole` constants |
| `constants.js` | [config/constants.js](spark-internal-graphql/packages/data-source-spark/src/config/constants.js) | `SPARK_GATEWAY_API_KEY` |

### 3g. Feature flags

| Flag | Default | Effect |
|---|---|---|
| `USE_NEW_RULES_API` | `false` | When `true`, swaps `RULE_SERVICE_URL` from `config.endpoints.product` to `config.endpoints.tag` and uses `ctx.loaders.ruleLibrary` for rules search instead of `ctx.loaders.product.searchProduct{Dept,BP,}Rules`. |

---

## 4. Cross-Domain Reference Table (Loaders Called From Product Resolver)

Legend: **Internal** = same `plm-product` DGS · **EXT** = different DGS or backend · **Platform** = external SaaS, always Hive-Gateway-stitched (🔵)

| Loader (ctx.loaders.X) | Backend / DGS Owner | Classification | Severity | Used For |
|---|---|---|---|---|
| `product` | `spark-product` → `plm-product` | Internal (self) | — | All Query/Mutation reads & writes |
| `bom` | `spark-product` → `plm-product` | **Internal (co-located)** | — | `updateComponentStatuses` mutation, sibling BOM field resolution |
| `measurement` | `spark-product` → `plm-product` | **Internal (co-located)** | — | `updateComponentStatuses` mutation |
| `ProductDetails` | `spark-product` → `plm-product` | **Internal (co-located)** | — | `updateComponentStatuses` mutation |
| `packaging` | `spark-product` → `plm-product` | **Internal (co-located)** | — | `updateComponentStatuses`, packaging field formatting |
| `productAsk` | `spark-product` → `plm-product` | **Internal (co-located)** | — | `associateProductsAsks` field |
| `productVariation` | `spark-product` → `plm-product` | **Internal (co-located)** | — | `variations` field |
| `fileLibrary` | `spark-product` → `plm-product` | **Internal (co-located)** | — | `SPARK_PackagingAttribute.spg` field |
| `claim` | `spark-claims` | EXT | 🟡 YELLOW | `updateComponentStatuses` for claims |
| `attachment` | `spark-attachment` | EXT | 🔴 RED | `getTechPackResourceCountMap`, `attachments`, `attachmentsWithMetaData`, copy/carry-forward flows |
| `workspaceV2` | `spark-workspace` | EXT | 🔴 RED | `addProduct`, `updateProduct`, `productWorkspaceAttributes`/`productWorkspaceInfo` field resolvers |
| `search` | `spark-elastic-search` | EXT | 🔴 RED | All elastic queries: `getProducts`, `getProductTemplates`, `getTechPackResourceCountMap`, `discussionsV2`, `attachmentSummary`, `components`, `workspaces` |
| `accessControl` | `spark-access-control` | EXT | 🔴 RED | `getUserPermissionsJWT`, `getAccessControlBatch`, `dropPartnerFromResources`, `unDropPartnerFromResources` — gates almost every read |
| `relationship` | `spark-relationship` | EXT | 🟡 YELLOW | `searchByIds` for attachment/sample/template relationships |
| `userAttributes` | `spark-userprofile` | EXT | 🟡 YELLOW | `createdBy`, `updatedBy`, `versionCreatedBy`, status `updatedBy` fields |
| `teamV2` | `spark-userprofile` | EXT | 🟡 YELLOW | `teams` field |
| `role` | `spark-userprofile` | EXT (not directly used in resolver, via permissions) | 🟡 YELLOW | — |
| `discussion` | `spark-discussion` | EXT | 🟡 YELLOW | `discussionsCount`, `discussionsV2` |
| `sampleV2` | `spark-sample-v2` | EXT | 🟡 YELLOW | `samples`, `sampleIds` fields, partner-action sample updates |
| `tag` | `spark-tag` | EXT | 🟡 YELLOW | `tags` field, design-cycle tag resolution |
| `recentlyViewed` | `spark-recentlyviewed` | EXT | 🔵 BLUE | `productBusinessPartnerActions` cleanup on partner drop |
| `todo` | `spark-todo` | EXT | 🔵 BLUE | `productBusinessPartnerActions` cleanup |
| `favorite` | `spark-favorite` | EXT | 🔵 BLUE | `productBusinessPartnerActions` cleanup |
| `ruleLibrary` | `spark-tag` (when `USE_NEW_RULES_API`) | EXT | 🔵 BLUE | Rules search, behind feature flag |
| `ig.department` / `ig.division` / `ig.clazz` | **Item Groups platform** | **Platform** | 🔵 BLUE | `department`, `division`, `clazz`, `productTemplateDepartments`, `divisions` fields; categories resolution |
| `brand` (VmmBrandService) | **VMM platform** | **Platform** | 🔵 BLUE | `brand`, `brands` fields; category resolution |
| `vmm` (VmmBusinessPartnerService) | **VMM platform** | **Platform** | 🔵 BLUE | `businessPartners`, `droppedPartners` fields (via `vmmUtils`) |
| `coronaItems` | **CORONA platform** | **Platform** | 🔵 BLUE | `SPARK_Tcin.itemDetails` |
| `doppler` | **Doppler platform** | **Platform** | 🔵 BLUE | `DopplerDepartment.primaryCapacityTypeName` / `secondaryCapacityTypeName` |
| `apex` (via `getReservedDpcisFromApex`) | **APEX platform** | **Platform** | 🔵 BLUE | `reservedDpcis` field |

---

## 5. Import Dependency Graph (top-level only)

```
SPARK_Product.js (resolver)
├── utils/commonLoaders (ACL + JWT)            → spark-access-control EXT
├── utils/convertFunctions (status mapping)    → pure
├── utils/resolvePaging                        → pure
├── utils/vmmUtils                             → VMM Platform 🔵
├── utils/removePartnerUtils                   → pure (uses ctx)
├── utils/Product/attachmentUtils              → pure transforms over attachment shape
├── utils/Product/partnerUtils                 → pure
├── utils/Product/teamUtils                    → pure
├── utils/Product/productUtils                 → pure transforms (request/response)
├── utils/Product/getReservedDpcisFromApex     → APEX Platform 🔵
├── utils/ProductAskUtils                      → co-located productAsk
├── utils/accessControlUtils                   → spark-access-control EXT
├── utils/componentStatusUtils                 → pure (works over ctx loaders)
├── utils/discussionUtils                      → spark-discussion EXT
├── utils/logger, utils/constants              → infra
├── config/businessPartner                     → constants
├── resolvers/product/SPARK_Measurement        → measurementSets field
├── resolvers/product/SPARK_Claims             → claims field
├── resolvers/product/SPARK_Bom                → bom / productBom fields
├── resolvers/product/SPARK_ProductDetail      → productDetails field
├── resolvers/product/SPARK_Packaging          → packagingBom field
├── resolvers/SPARK_SampleV2                   → samples (sibling EXT spark-sample-v2)
├── resolvers/SPARK_WorkspaceV2                → workspaces (sibling EXT)
├── resolvers/SPARK_UserAttributes             → userprofile (EXT)
├── resolvers/SPARK_Attachment                 → attachments (EXT)
└── services/batchers/getTagsBatched           → spark-tag EXT
```

---

## 6. Operation Lists (names only — pseudo-logic is Phase 2)

### 6a. Queries (18)
1. `getProducts`
2. `getProductTemplates`
3. `getProduct`
4. `getCopyStatus`
5. `getCategories`
6. `getProductsByIds`
7. `getProductStatus`
8. `getProductTechPackCountV1` ⚠️ flagged Very High complexity
9. `getProductTechPackBulkCountV1` ⚠️ wraps the above per item
10. `getProductVersions`
11. `getRatingByTcin` (external rating service)
12. `getProductRules`
13. `getProductRulesById`
14. `getAllAvailableRules`
15. `getProductDeptRules` (feature-flagged routing)
16. `getProductBPRules` (feature-flagged routing)
17. `searchProductRules` (feature-flagged routing)
18. `getProductTemplateById`

### 6b. Mutations (23)
1. `addProduct`
2. `updateProduct`
3. `carryForwardProduct`
4. `bulkUpdateProducts`
5. `addProducts`
6. `addTeamsToProduct`
7. `addBusinessPartnersToProductWithType`
8. `removeProductResources`
9. `removeProductBusinessPartner` *(declared in schema; resolver implemented inside `productBusinessPartnerActions`)*
10. `updateBusinessPartnerStatuses`
11. `productBusinessPartnerActions` ⚠️ orchestrates partner drop/undrop across 6+ services
12. `updateViewToggle`
13. `updateWorkspaceAttributes`
14. `dropProductBusinessPartner` *(via `productBusinessPartnerActions`)*
15. `unDropProductBusinessPartner` *(via `productBusinessPartnerActions`)*
16. `updateProductTeamsWorkspaceContext`
17. `linkProduct`
18. `unlinkProduct`
19. `addProductRule`
20. `updateProductRule`
21. `deleteProductRule`
22. `updateComponentStatus`
23. `updateComponentStatuses` ⚠️ fans out to bom/measurement/ProductDetails/claim/packaging loaders in parallel

### 6c. Field resolvers on `SPARK_Product` (50+)

Grouped by complexity tier (final ratings come in Phase 2):

**Likely trivial pass-throughs** (return `product.X` directly): `parentProductId`, `notRemovablePartnerIds`, `designPartnerId`, `tcins`

**Single-loader lookups** (low complexity): `createdBy`, `updatedBy`, `versionCreatedBy`, `department`, `division`, `clazz`, `brand`, `status`, `tags`, `workspaces`, `bom`, `productBom`, `packagingBom`, `claims`, `productDetails`, `discussionsCount`, `notRemovableWorkspaceIds`, `reservedDpcis`, `rating`, `productTemplateDepartments`, `brands`, `divisions`, `attachmentsData`

**Medium complexity** (multi-step / merging): `vendorAttributes`, `businessPartners`, `droppedPartners`, `unDroppablePartners`, `productWorkspaceAttributes`, `productWorkspaceInfo`, `teams`, `discussionsV2`, `measurementSets`, `attachments`, `samples`, `sampleIds`, `ancestryProducts`, `associateProductsAsks`, `variations`

**High / Very High** (large orchestration): `attachmentsWithMetaData`, `attachmentSummary`, `components`, `elasticSamplesList`

### 6d. Other type-level resolvers
- `SPARK_ResourcesCount.productThumbnailId` (re-fetch product by id)
- `SPARK_AncestryProducts` (1 field)
- Passthrough wrappers: `SPARK_ProductBulkType`, `SPARK_ProductsPaged`, `SPARK_ProductTemplatesList`, `SPARK_ProductsCategories`
- `SPARK_Categories.__resolveType` (polymorphic union)
- `SPARK_MasterProductStatus` (1 field)
- `SPARK_Tcin.itemDetails` (CORONA)
- `SPARK_ProductRules` (4 fields: departments / businessPartners / insightsClassExclusion)
- `DopplerDepartment` (5 fields, Doppler platform)
- `ProductComponentStatus.updatedBy`
- `SPARK_PackagingAttribute.spg`
- `VMM_BusinessPartnerCategory` (type extension — VMM gateway-stitched)

---

## 7. Summary Statistics

| Metric | Value |
|---|---|
| Schema lines | 800 |
| Resolver lines | **2,629 — Large File Protocol active for Phase 2** |
| Service lines | 589 |
| Total LOC in scope (schema + resolver + service + util touchpoints) | ~5,000+ |
| Queries | **18** |
| Mutations | **23** |
| Field resolvers (`SPARK_Product` block alone) | **~50** |
| Distinct service loaders called | **26** |
| Co-located sibling domains (same DGS) | **15** |
| **EXT services** (different DGS) | **12** |
| **Platform services** (always 🔵, Hive-Gateway-stitched) | **6** (VMM, IG, Doppler, CORONA, APEX, Brand Compliance) |
| Polymorphic `__resolveType` blocks | **1** (`SPARK_Categories`) — applies +1 complexity tier per USAGE §7 |
| Operations behind feature flag | 3 (rules search routes via `USE_NEW_RULES_API`) |

---

## 8. Migration Hot-Spots Flagged for Phase 2

1. **`getProductTechPackCountV1` / `getProductTechPackBulkCountV1`** — single most complex operation in the system. 17-step orchestration of 9+ services (search × 7, accessControl, attachment). See `reference/stitching-patterns.md` and `reference/techpack-migration-options.md` before Phase 4.
2. **`productBusinessPartnerActions`** — large mutation orchestrating drop/undrop with cleanup against `recentlyViewed`, `todo`, `favorite`, `sampleV2`, `accessControl`, plus product partner update. JWT permissioning required.
3. **`updateComponentStatuses`** — fans out to 5 co-located loaders in parallel (`bom`, `measurement`, `ProductDetails`, `claim`, `packaging`). Maps cleanly to a single `plm-product` DGS service method.
4. **`SPARK_Product.attachmentsWithMetaData`** and **`SPARK_Product.components`** — ~150-line field resolvers each, heavy access-control + multi-source merge.
5. **Categories union resolver** (`SPARK_Categories`, `SPARK_ProductsCategories.categories`) — polymorphic over `IG_Clazz`, `IG_Department`, `VMM_BusinessPartner` etc. Apply +1 complexity tier.

---

**Phase 1 complete.** Proceeding to Phase 2A — Query resolvers.
