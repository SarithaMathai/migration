# Domain-Level Analysis — Frontend GraphQL by Business Domain

> Groups every frontend operation by backend business domain (not by client file) · Generated: 2026-07-16

## Phase-1 domains

### Product (`product`)

- Frontend operations: 64 (44 queries, 20 mutations)
- Backend ownership: `plm-product (host)` · schema `schemas/SPARK_Product.graphqls`
- Client ownership (libraries): `claims`, `core-discussions`, `product-common`, `product-packaging`, `product-queries`, `spark-legacy`, `spark-ui-admin`, `workspaces`
- Client domains consuming: Claims, Core — Discussions, Legacy (Spark), Product — Common, Product — Packaging, Product — Queries, UI Admin, Workspaces, spark-legacy
- Shared fragments: `ATTACHMENTS_WITH_META_DATA_FRAGMENT`, `ATTACHMENT_V3_FRAGMENT`, `AttachmentV3Fragment`, `AttachmentsWithMetaData`, `DISCUSSION_LIST_FRAGMENT_V2`, `DISCUSSION_TEAMS_FRAGMENT`, `DiscussionListFragmentV2`, `DiscussionTeamsFragment`, `FULL_CLAIM_DETAILS(true)`, `FullClaimDetailsFragment`, `LEGACY_DISCUSSION_LIST_FRAGMENT_V2`, `LEGACY_DISCUSSION_TEAMS_FRAGMENT`, `LINK_PRODUCT_FRAGMENT`, `LegacyDiscussionListFragmentV2`, `LegacyDiscussionTeamsFragment`, `MEASUREMENT_TEMPLATE_FRAGMENT`, `PRODUCT_BASE_INFO_FRAGMENT`, `PRODUCT_COMPONENT_FRAGMENT`, `PRODUCT_FULL_TEAM_FRAGMENT`, `PRODUCT_RULES_FIELDS_FRAGMENT`, `PRODUCT_TEMPLATE_DETAILS`, `PRODUCT_VENDOR_ATTRIBUTES`, `ProductBaseInfoFragment`, `ProductFullTeamFragment`, `ProductRules`, `ProductVendorAttributesFragment`, `SIZE_TEMPLATE_FRAGMENT_WITH_ROWS`, `TIGHT_FIT_FRAGMENT`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct`, `linkProductFragment`, `measurementTemplateFragment`, `productComponentFragment`, `productTemplateDetails`, `sizeTemplateFragmentWithRows`, `tightFitFragment`
- Cross-domain operations (same document also selects another domain's root field):
  - with **Access Control**: `getBulkDiscussionData`, `getProduct`, `getTeams`
  - with **Tags**: `getFormData`
  - with **Impression**: `getCarryForwardFormData`
- Queries: `getTechPackBulkCount`, `getAllAvailableRules`, `getProducts`, `getProductTemplates`, `getBulkDiscussionData`, `getCarryForwardFormData`, `getTechPackCountV1`, `getFilesWithMetaData`, `getProduct`, `getFormData`, `getProductTemplates`, `getProducts`, `getProductWorkspaces`, `getProductWorkspaces`, `getProductBPRules`, `getProductById`, `getProductComponentStatusCounts`, `breadcrumbProduct`, `getProductDeptRules`, `getProductStatusUpdateInfo`, `getProduct`, `getStatus`, `getTeams`, `getTeams`, `getProductTemplates`, `getCategories`, `getProductVersions`, `getProductWithAttachmentsAndComponents`, `getProduct`, `getProductWithTeams`, `getProductWorkspaceMetricsReportCount`, `getProductRule`, `getProductRules`, `searchProductRules`, `getProduct`, `getProduct`, `getProductScaffolding`, `getProduct`, `getProduct`, `getTeamsProductAndWorkspace`, `getCategories`, `getCategories`, `getProducts`, `getDpciInfo`
- Mutations: `addBusinessPartnersToProductWithType`, `addProduct`, `addProductRule`, `addTeams`, `productBusinessPartnerActions`, `carryForwardProduct`, `deleteProductRule`, `linkProduct`, `updateProductTeamsWorkspaceContext`, `addProducts`, `bulkUpdateProducts`, `updateViewToggle`, `unlinkProduct`, `updateComponentStatus`, `updateComponentStatuses`, `updateProduct`, `updateProduct`, `updateProductRule`, `updateBusinessPartnerStatuses`, `updateProduct`

### BOM (`bom`)

- Frontend operations: 19 (14 queries, 5 mutations)
- Backend ownership: `plm-product (co-located)` · schema `schemas/SPARK_Bom.graphqls`
- Client ownership (libraries): `product-queries`, `spark-legacy`, `spark-ui-admin`
- Client domains consuming: Legacy (Spark), Product — Queries, UI Admin
- Shared fragments: `BOM_ACCESS_FRAGMENT`, `BOM_COMBO_SUPPLIER_FRAGMENT`, `BOM_DETAILS_FRAGMENT`, `BOM_FABRIC_SPEC_COMBO_DETAILS()`, `BUILD_FILES_FRAGMENT('SPARK_BaseMaterial')`, `BUILD_FILES_FRAGMENT('SPARK_FabricSpecification')`, `BomAccessFragment`, `BomComboSupplier`, `BomDetails`, `BomFabricSpecComboDetails`, `IMPRESSION_FRAGMENT()`, `ImpressionFragment`, `MATERIAL_DETAILS`, `MAX_BOM_SEARCH_SIZE`, `MaterialDetails`, `PRODUCT_BASE_INFO_FRAGMENT`, `ProductBaseInfoFragment`, `SPARK_BaseMaterial_Files`, `SPARK_FabricSpecification_Files`
- Cross-domain operations (same document also selects another domain's root field):
  - with **Impression**: `getBomDataAndImpressions`
- Queries: `searchMaterialsBom`, `getBomByIds`, `getBomByIds`, `getBomByParentId`, `getBomElastic`, `getBomByIds`, `getBomComponentStatus`, `getBomMaterialTypes`, `getBomPackagingMasterData`, `getBomPackagingSubstrates`, `getBomStatus`, `getBomDataAndImpressions`, `getComboSupplierForBom`, `getValidSuppliersForBom`
- Mutations: `addBom`, `lockBom`, `unlockBom`, `updateBom`, `updateBomComponentStatus`

### Measurement (`measurement`)

- Frontend operations: 12 (8 queries, 4 mutations)
- Backend ownership: `plm-product (co-located)` · schema `schemas/SPARK_Measurement.graphqls`
- Client ownership (libraries): `product-common`, `spark-legacy`, `spark-ui-admin`
- Client domains consuming: Legacy (Spark), Product — Common, UI Admin
- Shared fragments: `MEASUREMENT_FIELDS_FRAGMENT`, `MEASUREMENT_TEMPLATE_FRAGMENT`, `SAMPLE_MEASUREMENT_FRAGMENT`, `SIZE_TEMPLATE_FRAGMENT_WITH_ROWS`, `SampleMeasurementFragment`, `TIGHT_FIT_FRAGMENT`, `measurementFieldsFragment`, `measurementTemplateFragment`, `sizeTemplateFragmentWithRows`, `tightFitFragment`
- Cross-domain operations (same document also selects another domain's root field):
  - with **Measurement (POM)**: `getMeasurementsMetaData`
- Queries: `getMeasurements`, `getMeasurementsMetaData`, `getMeasurementByIds`, `getMeasurementComponentStatus`, `getMeasurementByIds`, `getMeasurementSetStatus`, `getMeasurementsElastic`, `getUnitsOfMeasure`
- Mutations: `deleteSampleMeasurementSet`, `lockMeasurementSet`, `putSampleMeasurementSet`, `unlockMeasurementSet`

### Product Details (`productDetails`)

- Frontend operations: 7 (2 queries, 5 mutations)
- Backend ownership: `plm-product (co-located)` · schema `schemas/SPARK_ProductDetail.graphqls`
- Client ownership (libraries): `product-details`, `spark-legacy`
- Client domains consuming: Legacy (Spark), Product — Details
- Shared fragments: `PRODUCT_DETAILS_DATA_FRAGMENT`, `ProductDetailsDataFragment`
- Queries: `getProductDetailsById`, `getProductDetailComponentStatus`
- Mutations: `cloneFilesForProductDetails`, `createProductDetailsSet`, `productDetailLockUnlock`, `updateProductDetailsSet`, `updateProductDetailComponentStatus`

### Packaging (`packaging`)

- Frontend operations: 21 (12 queries, 9 mutations)
- Backend ownership: `plm-product (co-located)` · schema `schemas/SPARK_Packaging.graphqls`
- Client ownership (libraries): `product-common`, `product-packaging`, `spark-legacy`, `spark-packaging-base`
- Client domains consuming: Legacy (Spark), Packaging — Base, Product — Common, Product — Packaging
- Shared fragments: `GET_PACKAGING_DETAIL_BASE_FRAGMENT(true)`, `GET_PACKAGING_DETAIL_FRAGMENT()`, `GET_PACKAGING_DETAIL_FRAGMENT(false)`, `GET_PACKAGING_DETAIL_FRAGMENT(true)`, `PACKAGING_PACKET_INFORMATION_FRAGMENT`, `PackagingDetailsBaseFragment`, `PackagingDetailsFragment`, `packagePacketInformation`
- Queries: `getDielines`, `getDielineEvaluationStatuses`, `getPackagingComponentStatus`, `getCountries`, `getPackagingById`, `getPackagings`, `getPackagings`, `getPackagings`, `getPackagingById`, `getPackagingFieldValuesByType`, `getPackagingPacketsInformation`, `getPackagingPacketInformation`
- Mutations: `addPackaging`, `bulkAddPackagings`, `bulkUpdatePackagings`, `evaluateDieline`, `lockPackaging`, `exportPackaging`, `unlockPackaging`, `updatePackagingComponentStatus`, `updatePackaging`

### Watchlist (`watchlist`)

- Frontend operations: 5 (2 queries, 3 mutations)
- Backend ownership: `plm-product (co-located)` · schema `schemas/SPARK_Watchlist.graphqls`
- Client ownership (libraries): `watchlist`
- Client domains consuming: Watchlist
- Shared fragments: `PRODUCT_BASE_INFO_FRAGMENT`, `WATCHLIST_FORM_CONSTANTS`, `WATCHLIST_FRAGMENT`, `WATCHLIST_PARTICIPANT_FRAGMENT`, `WatchlistFields`
- Queries: `getWatchlistByIds`, `getWatchlistForBulkUpdate`
- Mutations: `cloneFilesForWatchlist`, `createWatchlistEntries`, `updateWatchlistEntries`

### Impression (`impression`)

- Frontend operations: 2 (2 queries, 0 mutations)
- Backend ownership: `plm-product (co-located)` · schema `schemas/SPARK_Impression.graphqls`
- Client ownership (libraries): `product-queries`, `spark-legacy`
- Client domains consuming: Legacy (Spark), Product — Queries
- Shared fragments: `BOM_DETAILS_FRAGMENT`, `BomDetails`, `IMPRESSION_FRAGMENT()`, `ImpressionFragment`, `PRODUCT_COMPONENT_FRAGMENT`, `PRODUCT_FULL_TEAM_FRAGMENT`, `ProductFullTeamFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct`, `productComponentFragment`
- Cross-domain operations (same document also selects another domain's root field):
  - with **BOM**: `getBomDataAndImpressions`
  - with **Product**: `getCarryForwardFormData`
- Queries: `getBomDataAndImpressions`, `getCarryForwardFormData`

### Claims (`claims`)

- Frontend operations: 14 (8 queries, 6 mutations)
- Backend ownership: `spark-claims (separate)` · schema `schemas/SPARK_Claims.graphqls`
- Client ownership (libraries): `claims`, `spark-legacy`, `spark-ui-admin`
- Client domains consuming: Claims, Legacy (Spark), UI Admin, claims
- Shared fragments: `CLAIM_DETAILS_FRAGMENT`, `ClaimDetailsFragment`, `FULL_CLAIM_DETAILS(includeWorkspaces)`, `FULL_CLAIM_DETAILS(true)`, `FullClaimDetailsFragment`
- Cross-domain operations (same document also selects another domain's root field):
  - with **Components**: `getComponentVersion`
- Queries: `getClaims`, `getClaimByIds`, `getClaimComponentStatus`, `breadcrumbClaims`, `getClaimByIds`, `getComponentVersion`, `getCommunicationChannels`, `getClaims`
- Mutations: `createClaim`, `bulkUpdateClaim`, `lockClaim`, `requestClaimExport`, `unlockClaim`, `updateClaim`

## Shared object types (phase-1)

- Phase-1 types selected by fragments from more than one client domain — federation `@key` candidates.

| Type | Client domains with fragments on it |
|---|---|
| `SPARK_Claims` | Claims, claims |
| `SPARK_Product` | Claims, Legacy (Spark), Product — Common, Product — Queries |
