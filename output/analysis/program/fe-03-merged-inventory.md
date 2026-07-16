# Merged GraphQL Inventory — Frontend Usage × Backend Schema

> Authoritative migration-planning inventory · Generated: 2026-07-16
> One row per frontend operation × backend root field. FE story ids resolve in fe-08-frontend-stories.md; BE story ids in output/analysis/{{domain}}/be-04-stories.md.

## Summary

| Bucket | Operation-to-root-field rows |
|---|---|
| Phase-1 domains (8) — in scope | 153 |
| Later-phase / shared domains — out of scope | 577 |
| No mapping in spark-internal-graphql — out of scope | 257 |

- Program scope: only phase-1 domain queries/mutations and their fields are inventoried below.
- Out-of-scope rows are counted for completeness; they migrate with their own subgraph phase.

## Phase-1 domains

### Product (`product`) — 66 rows · DGS: `plm-product (host)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `addBusinessPartnersToProductWithType` | mutation | PRODUCT-BE-D-07 | `addBusinessPartnersToProductWithType` | `ADD_PARTNERS_PRODUCT_WITH_TYPE` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | 0 | 2 | — | — |
| `addProduct` | mutation | PRODUCT-BE-D-01 | `addProduct` | `ADD_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 2 | 7 | — | — |
| `addProductRule` | mutation | PRODUCT-BE-D-15 | `addProductRule` | `ADD_PRODUCT_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `addProducts` | mutation | PRODUCT-BE-D-02 | `addProducts` | `PRODUCT_BULK` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 1 | 4 | — | — |
| `addTeamsToProduct` | mutation | PRODUCT-BE-D-06 | `addTeams` | `ADD_TEAMS_PRODUCT` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | 1 | 2 | — | — |
| `bulkUpdateProducts` | mutation | PRODUCT-BE-D-03 | `bulkUpdateProducts` | `PRODUCT_BULK_UPDATE` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 1 | 4 | — | — |
| `carryForwardProduct` | mutation | PRODUCT-BE-D-05 | `carryForwardProduct` | `CARRY_FORWARD_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 2 | 2 | — | — |
| `deleteProductRule` | mutation | PRODUCT-BE-D-17 | `deleteProductRule` | `DELETE_PRODUCT_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | — |
| `getAllAvailableRules` | query | PRODUCT-BE-B-09 | `getAllAvailableRules` | `GET_ALL_AVAILABLE_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 3 | — | — |
| `getCategories` | query | PRODUCT-BE-C-03 | `getCategories` | `GET_PRODUCT_TEMPLATE_CATEGORY` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 1 | 6 | — | — |
| `getCategories` | query | PRODUCT-BE-C-03 | `getCategories` | `GET_WORKSPACE_CATEGORY` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 2 | 6 | — | — |
| `getCategories` | query | PRODUCT-BE-C-03 | `getCategories` | `GET_WORKSPACE_CATEGORY_CLAZZ` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 1 | 9 | — | — |
| `getProduct` | query | PRODUCT-BE-B-01 | `getCarryForwardFormData` | `GET_CARRY_FORWARD_FORM_DATA` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 3 | 32 | — | multi-root op (2 root fields); 6 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProduct` | `GET_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 2 | 111 | — | 2 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductWorkspaces` | `GET_PRODUCT_AND_WORKSPACES` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 3 | 27 | — | multi-root op (2 root fields); 4 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductWorkspaces` | `GET_PRODUCT_AND_WORKSPACES_WITH_STATUS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 1 | 12 | — | multi-root op (2 root fields); 4 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductById` | `GET_PRODUCT_BY_ID` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | 0 | 17 | — | — |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductComponentStatusCounts` | `GET_PRODUCT_COMPONENT_STATUS_COUNTS` | `src/libs/product-queries/src/queries/ProductFilesQueries.tsx` | 3 | 10 | — | — |
| `getProduct` | query | PRODUCT-BE-B-01 | `breadcrumbProduct` | `GET_PRODUCT_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/graphql/BreadcrumbQueries.ts` | 1 | 3 | — | — |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductStatusUpdateInfo` | `GET_PRODUCT_FOR_STATUS_UPDATE` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 1 | 15 | — | multi-root op (2 root fields); 4 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProduct` | `GET_PRODUCT_MINIMAL` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 0 | 32 | — | 2 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getTeams` | `GET_PRODUCT_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` | 0 | 15 | — | multi-root op (2 root fields); 2 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getTeams` | `GET_PRODUCT_TEAMS` | `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` | 0 | 15 | — | multi-root op (2 root fields); 2 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductWithAttachmentsAndComponents` | `GET_PRODUCT_WITH_ATTACHMENTS_AND_COMPONENTS` | `src/libs/product-queries/src/queries/ProductFilesQueries.tsx` | 0 | 52 | — | 6 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProduct` | `GET_PRODUCT_WITH_META_DATA` | `src/libs/product-queries/src/queries/WorkspaceFilesQueries.ts` | 0 | 15 | — | multi-root op (2 root fields); 2 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductWithTeams` | `GET_PRODUCT_WITH_TEAMS` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | 2 | 35 | — | 4 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProduct` | `GET_SPARK_PRODUCT_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` | 1 | 4 | — | 2 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProduct` | `GET_SPARK_PRODUCT_BP` | `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` | 1 | 4 | — | 2 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProductScaffolding` | `GET_SPARK_PRODUCT_SCAFFOLDING` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 0 | 131 | — | 6 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProduct` | `GET_SPARK_PRODUCT_V2` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` | 1 | 7 | — | 4 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getProduct` | `GET_SPARK_PRODUCT_V2` | `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` | 1 | 7 | — | 4 fragment(s) |
| `getProduct` | query | PRODUCT-BE-B-01 | `getDpciInfo` | `USE_DPCI_INFO` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 16 | — | — |
| `getProductBPRules` | query | PRODUCT-BE-B-11 | `getProductBPRules` | `GET_PRODUCT_BUSINESS_PARTNER_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `getProductDeptRules` | query | PRODUCT-BE-B-10 | `getProductDeptRules` | `GET_PRODUCT_DEPARTMENT_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `getProductRules` | query | PRODUCT-BE-B-07 | `getProductRules` | `GET_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `getProductRulesById` | query | PRODUCT-BE-B-08 | `getProductRule` | `GET_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `getProductStatus` | query | PRODUCT-BE-B-03 | `getFormData` | `GET_PRODUCTS_BY_ID_LIST` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 1 | 132 | — | multi-root op (5 root fields); 2 fragment(s) |
| `getProductStatus` | query | PRODUCT-BE-B-03 | `getProductStatusUpdateInfo` | `GET_PRODUCT_FOR_STATUS_UPDATE` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 1 | 15 | — | multi-root op (2 root fields); 4 fragment(s) |
| `getProductStatus` | query | PRODUCT-BE-B-03 | `getStatus` | `GET_PRODUCT_STATUS` | `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsQueries.ts` | 0 | 9 | — | multi-root op (3 root fields) |
| `getProductStatus` | query | PRODUCT-BE-B-03 | `getProductWorkspaceMetricsReportCount` | `GET_PRODUCT_WORKSPACES_METRICS_REPORT_COUNT` | `src/libs/product-queries/src/queries/workspaceQueries.tsx` | 1 | 22 | — | multi-root op (3 root fields) |
| `getProductTechPackBulkCountV1` | query | PRODUCT-BE-E-04 | `getTechPackBulkCount` | `BULK_TECHPACK_COUNTS` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 2 | 13 | — | — |
| `getProductTechPackCountV1` | query | PRODUCT-BE-E-03 | `getTechPackCountV1` | `GET_COUNT_V1` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 2 | 12 | — | — |
| `getProductTemplates` | query | PRODUCT-BE-C-02 | `getProductTemplates` | `GET_ALL_PRODUCTS_TEMPLATES` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 2 | 34 | — | — |
| `getProductTemplates` | query | PRODUCT-BE-C-02 | `getProductTemplates` | `GET_PRODUCTS_WITH_IDS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 1 | 112 | — | — |
| `getProductTemplates` | query | PRODUCT-BE-C-02 | `getProductTemplates` | `GET_PRODUCT_TEMPLATE` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 3 | 208 | `SPARK_Claims.includeWorkspaces`; `SPARK_SizeTemplate.…sizeTemplateFragmentWithRows (fragment defined outside snapshot)`; `SPARK_MeasurementTemplate.…measurementTemplateFragment (fragment defined outside snapshot)` | 12 fragment(s) |
| `getProductVersions` | query | PRODUCT-BE-B-04 | `getProductVersions` | `GET_PRODUCT_VERSIONS` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | 0 | 37 | — | — |
| `getProducts` | query | PRODUCT-BE-S-02 | `getProducts` | `GET_ALL_PRODUCTS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 0 | 88 | — | — |
| `getProducts` | query | PRODUCT-BE-S-02 | `getProducts` | `GET_PRODUCTS_WITH_SAMPLE_DETAILS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 1 | 16 | — | — |
| `getProducts` | query | PRODUCT-BE-S-02 | `getProducts` | `PID_AND_WRK_ID_SEARCH` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/graphql/VendorMergeQueries.ts` | 1 | 8 | — | multi-root op (2 root fields) |
| `getProductsByIds` | query | PRODUCT-BE-B-02 | `getBulkDiscussionData` | `GET_BULK_DISCUSSION_DATA` | `src/libs/workspaces/src/graphql/BulkDiscussionQueries.ts` | 1 | 33 | — | multi-root op (2 root fields) |
| `getProductsByIds` | query | PRODUCT-BE-B-02 | `getFilesWithMetaData` | `GET_FILES_WITH_METADATA` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 0 | 12 | — | 2 fragment(s) |
| `getProductsByIds` | query | PRODUCT-BE-B-02 | `getFormData` | `GET_PRODUCTS_BY_ID_LIST` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 1 | 132 | — | multi-root op (5 root fields); 2 fragment(s) |
| `getProductsByIds` | query | PRODUCT-BE-B-02 | `getTeamsProductAndWorkspace` | `GET_TEAMS_PRODUCT_AND_WORKSPACE` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 2 | 22 | — | multi-root op (2 root fields) |
| `linkProduct` | mutation | PRODUCT-BE-D-13 | `linkProduct` | `LINK_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 1 | 1 | — | 2 fragment(s) |
| `productBusinessPartnerActions` | mutation | PRODUCT-BE-S-03 | `productBusinessPartnerActions` | `BUSINESS_PARTNER_ACTIONS_PRODUCT` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | 1 | 2 | — | — |
| `searchProductRules` | query | PRODUCT-BE-C-05 | `searchProductRules` | `GET_SEARCH_PRODUCT_DEPARTMENT_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `unlinkProduct` | mutation | PRODUCT-BE-D-14 | `unlinkProduct` | `UNLINK_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 2 | 1 | — | 2 fragment(s) |
| `updateBusinessPartnerStatuses` | mutation | PRODUCT-BE-D-09 | `updateBusinessPartnerStatuses` | `UPDATE_PRODUCT_STATUSES` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 3 | 2 | — | — |
| `updateComponentStatus` | mutation | PRODUCT-BE-D-18 | `updateComponentStatus` | `UPDATE_COMPONENT_STATUS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 1 | 2 | — | — |
| `updateComponentStatuses` | mutation | PRODUCT-BE-E-02 | `updateComponentStatuses` | `UPDATE_COMPONENT_STATUSES` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 1 | 2 | — | — |
| `updateProduct` | mutation | PRODUCT-BE-D-04 | `updateProduct` | `UPDATE_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 0 | 7 | — | — |
| `updateProduct` | mutation | PRODUCT-BE-D-04 | `updateProduct` | `UPDATE_PRODUCT` | `(local) ClientCallingGqlQueries/spark-legacy__carouselMutations.txt` | 0 | 2 | — | — |
| `updateProduct` | mutation | PRODUCT-BE-D-04 | `updateProduct` | `UPDATE_PRODUCT_TEMPLATE` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 1 | 2 | — | — |
| `updateProductRule` | mutation | PRODUCT-BE-D-16 | `updateProductRule` | `UPDATE_PRODUCT_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `updateProductTeamsWorkspaceContext` | mutation | PRODUCT-BE-D-12 | `updateProductTeamsWorkspaceContext` | `MANAGE_TEAMS_WORKSPACES` | `src/libs/spark-legacy/routes/teams/graphql/TeamsQueries.tsx` | 1 | 6 | — | — |
| `updateViewToggle` | mutation | PRODUCT-BE-D-10 | `updateViewToggle` | `TOGGLE_VIEW_SWITCH` | `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsMutations.ts` | 1 | 2 | — | — |

### BOM (`bom`) — 21 rows · DGS: `plm-product (co-located)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `addBom` | mutation | BOM-BE-D-01 | `addBom` | `ADD_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | 2 | 2 | — | — |
| `getBomByIds` | query | BOM-BE-B-01 | `getBomByIds` | `GET_BOMS_BY_IDS` | `src/libs/product-queries/src/queries/BomQueries.ts` | 1 | 1 | `SPARK_FabricSpecCombo.…BomFabricSpecComboSlimDetails (fragment defined outside snapshot)`; `SPARK_FabricSpecification.…SPARK_FabricSpecification_Files (fragment defined outside snapshot)` | 2 fragment(s) |
| `getBomByIds` | query | BOM-BE-B-01 | `getBomByIds` | `GET_BOMS_BY_IDS_WITH_PRODUCT_INFO` | `src/libs/product-queries/src/queries/BomQueries.ts` | 1 | 3 | `SPARK_FabricSpecCombo.…BomFabricSpecComboSlimDetails (fragment defined outside snapshot)`; `SPARK_FabricSpecification.…SPARK_FabricSpecification_Files (fragment defined outside snapshot)` | 4 fragment(s) |
| `getBomByIds` | query | BOM-BE-B-01 | `getBomByIds` | `GET_BOM_BY_ID` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | 0 | 14 | — | — |
| `getBomByIds` | query | BOM-BE-B-01 | `getBomComponentStatus` | `GET_BOM_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | 0 | 8 | — | — |
| `getBomByIds` | query | BOM-BE-B-01 | `getBomDataAndImpressions` | `GET_BOM_TEMPLATES_AND_IMPRESSIONS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 1 | 5 | `SPARK_FabricSpecCombo.…BomFabricSpecComboSlimDetails (fragment defined outside snapshot)`; `SPARK_FabricSpecification.…SPARK_FabricSpecification_Files (fragment defined outside snapshot)`; `SPARK_Impression.…ImpressionFragment (fragment defined outside snapshot)` | multi-root op (2 root fields); 4 fragment(s) |
| `getBomByParentId` | query | BOM-BE-B-04 | `getBomByParentId` | `GET_BOMS_BY_PARENT_ID` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 27 | `SPARK_FabricSpecCombo.…BomFabricSpecComboDetails (fragment defined outside snapshot)` | 2 fragment(s) |
| `getBomElastic` | query | BOM-BE-C-01 | `getBomElastic` | `GET_BOMS_FROM_ES_BY_PARENT_IDS` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 4 | — | — |
| `getBomMaterialTypes` | query | BOM-BE-B-05 | `getBomMaterialTypes` | `GET_BOM_MATERIAL_TYPES` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 11 | — | — |
| `getBomPackagingMaterialTypes` | query | BOM-BE-B-06 | `getBomPackagingMasterData` | `GET_BOM_PACKAGING_MASTER_DATA` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 16 | — | multi-root op (2 root fields) |
| `getBomPackagingSubstrates` | query | BOM-BE-B-07 | `getBomPackagingSubstrates` | `GET_BOM_PACKAGING_SUBSTRATES` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 9 | — | — |
| `getBomPackagingUnitOfMeasure` | query | BOM-BE-B-08 | `getBomPackagingMasterData` | `GET_BOM_PACKAGING_MASTER_DATA` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 16 | — | multi-root op (2 root fields) |
| `getBomStatus` | query | BOM-BE-B-03 | `getBomStatus` | `GET_BOM_STATUS` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 3 | — | — |
| `getComboSupplierForBom` | query | BOM-BE-C-03 | `getComboSupplierForBom` | `GET_COMBINATION_SUPPLIER_FOR_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `getValidRawMaterialSuppliersForBom` | query | BOM-BE-C-05 | `getValidSuppliersForBom` | `GET_VALID_SUPPLIERS_FOR_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | 2 | 2 | — | multi-root op (2 root fields) |
| `getValidTrimSuppliersForBom` | query | BOM-BE-C-04 | `getValidSuppliersForBom` | `GET_VALID_SUPPLIERS_FOR_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | 2 | 2 | — | multi-root op (2 root fields) |
| `lockBom` | mutation | BOM-BE-D-03 | `lockBom` | `LOCK_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | 1 | 1 | — | 2 fragment(s) |
| `searchMaterialsBom` | query | BOM-BE-S-03 | `searchMaterialsBom` | `BOM_SEARCH_MATERIALS` | `src/libs/product-queries/src/queries/BomQueries.ts` | 0 | 59 | `SPARK_BaseMaterial.…SPARK_BaseMaterial_Files (fragment defined outside snapshot)`; `SPARK_FabricSpecification.…SPARK_FabricSpecification_Files (fragment defined outside snapshot)` | 7 fragment(s) |
| `unlockBom` | mutation | BOM-BE-D-04 | `unlockBom` | `UNLOCK_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | 1 | 1 | — | 2 fragment(s) |
| `updateBom` | mutation | BOM-BE-S-01 | `updateBom` | `UPDATE_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | 1 | 2 | — | — |
| `updateBomComponentStatus` | mutation | BOM-BE-D-05 | `updateBomComponentStatus` | `UPDATE_BOM_COMPONENT_STATUS` | `src/libs/product-queries/src/queries/BomQueries.ts` | 1 | 3 | — | — |

### Measurement (`measurement`) — 13 rows · DGS: `plm-product (co-located)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `deleteSampleMeasurementSet` | mutation | MST-BE-D-07 | `deleteSampleMeasurementSet` | `DELETE_SAMPLE_MEASUREMENT` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 2 | 1 | — | — |
| `getMeasurementByIds` | query | MST-BE-B-01 | `getMeasurementByIds` | `GET_MEASUREMENT_BY_IDS` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 0 | 2 | `SPARK_SizeTemplate.…sizeTemplateFragmentWithRows (fragment defined outside snapshot)`; `SPARK_MeasurementTemplate.…measurementTemplateFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `getMeasurementByIds` | query | MST-BE-B-01 | `getMeasurementComponentStatus` | `GET_MEASUREMENT_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | 0 | 8 | — | — |
| `getMeasurementByIds` | query | MST-BE-B-01 | `getMeasurementByIds` | `GET_MEASUREMENT_SET_BY_ID` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | 0 | 18 | — | — |
| `getMeasurementSetStatus` | query | MST-BE-B-04 | `getMeasurementSetStatus` | `GET_MEASUREMENT_SET_STATUS` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 1 | 3 | — | — |
| `getMeasurements` | query | MST-BE-C-01 | `getMeasurements` | `GET_MEASUREMENTS` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 1 | 2 | `SPARK_SizeTemplate.…sizeTemplateFragmentWithRows (fragment defined outside snapshot)`; `SPARK_MeasurementTemplate.…measurementTemplateFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `getMeasurementsElastic` | query | MST-BE-C-02 | `getMeasurementsElastic` | `GET_PRODUCT_TEMPLATE_MEASUREMENTS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 0 | 77 | `SPARK_SizeTemplate.…sizeTemplateFragmentWithRows (fragment defined outside snapshot)`; `SPARK_MeasurementTemplate.…measurementTemplateFragment (fragment defined outside snapshot)` | 6 fragment(s) |
| `getThicknessUnitsOfMeasure` | query | MST-BE-B-03 | `getMeasurementsMetaData` | `GET_MEASUREMENTS_META_DATA` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 0 | 15 | — | multi-root op (3 root fields) |
| `getUnitsOfMeasure` | query | MST-BE-B-02 | `getMeasurementsMetaData` | `GET_MEASUREMENTS_META_DATA` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 0 | 15 | — | multi-root op (3 root fields) |
| `getUnitsOfMeasure` | query | MST-BE-B-02 | `getUnitsOfMeasure` | `GET_UNITS_OF_MEASURE` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 0 | 5 | — | — |
| `lockMeasurementSet` | mutation | MST-BE-D-03 | `lockMeasurementSet` | `LOCK_MEASUREMENT_SET` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 1 | 1 | `SPARK_SizeTemplate.…sizeTemplateFragmentWithRows (fragment defined outside snapshot)`; `SPARK_MeasurementTemplate.…measurementTemplateFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `putSampleMeasurementSet` | mutation | MST-BE-D-06 | `putSampleMeasurementSet` | `PUT_SAMPLE_MEASUREMENT` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 4 | 1 | `SPARK_Pom.…PomFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `unlockMeasurementSet` | mutation | MST-BE-D-04 | `unlockMeasurementSet` | `UNLOCK_MEASUREMENT_SET` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 1 | 1 | `SPARK_SizeTemplate.…sizeTemplateFragmentWithRows (fragment defined outside snapshot)`; `SPARK_MeasurementTemplate.…measurementTemplateFragment (fragment defined outside snapshot)` | 2 fragment(s) |

### Product Details (`productDetails`) — 7 rows · DGS: `plm-product (co-located)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `cloneFilesForProductDetails` | mutation | PDTL-BE-D-04 | `cloneFilesForProductDetails` | `CLONE_PDTL_ATTACHMENTS` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | 1 | 3 | — | — |
| `createProductDetailsSet` | mutation | PDTL-BE-D-01 | `createProductDetailsSet` | `CREATE_PRODUCT_DETAILS_SET` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | 2 | 3 | — | — |
| `getProductDetailsById` | query | PDTL-BE-B-01 | `getProductDetailsById` | `GET_PRODUCT_DETAILS_SET_BY_IDS` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `getProductDetailsById` | query | PDTL-BE-B-01 | `getProductDetailComponentStatus` | `GET_PROUCT_DETAIL_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | 0 | 7 | — | — |
| `productDetailLockUnlock` | mutation | PDTL-BE-D-03 | `productDetailLockUnlock` | `PRODUCT_DETAILS_LOCK_UNLOCK` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | 1 | 3 | — | — |
| `updateProductDetailComponentStatus` | mutation | PDTL-BE-D-05 | `updateProductDetailComponentStatus` | `UPDATE_PRODUCT_DETAIL_COMPONENT_STATUS` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | 1 | 3 | — | — |
| `updateProductDetailsSet` | mutation | PDTL-BE-E-01 | `updateProductDetailsSet` | `UPDATE_PRODUCT_DETAILS_SET` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | 2 | 3 | — | — |

### Packaging (`packaging`) — 21 rows · DGS: `plm-product (co-located)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `addPackaging` | mutation | PKG-BE-D-01 | `addPackaging` | `ADD_PACKAGING_DETAIL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 2 | 2 | — | — |
| `bulkAddPackagings` | mutation | PKG-BE-D-03 | `bulkAddPackagings` | `BULK_ADD_PACKAGING_DETAILS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 3 | — | — |
| `bulkUpdatePackagings` | mutation | PKG-BE-D-04 | `bulkUpdatePackagings` | `BULK_UPDATE_PACKAGING_DETAILS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 3 | — | — |
| `evaluateDieline` | mutation | PKG-BE-D-02 | `evaluateDieline` | `EVALUATE_DIELINE` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 3 | — | — |
| `exportPackaging` | mutation | PKG-BE-D-05 | `exportPackaging` | `PACKAGING_EXCEL_EXPORT` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 1 | 1 | — | — |
| `getCountries` | query | PKG-BE-B-06 | `getCountries` | `GET_PACKAGING_COUNTRIES` | `src/libs/spark-packaging-base/src/graphql/PackagingCountryQueries.ts` | 0 | 4 | — | — |
| `getDielineEvaluationStatuses` | query | PKG-BE-B-05 | `getDielineEvaluationStatuses` | `GET_DIELINE_STATUS_LIST` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 3 | — | — |
| `getDielines` | query | PKG-BE-B-03 | `getDielines` | `GET_DIELINES` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 56 | — | — |
| `getPackagingById` | query | PKG-BE-B-02 | `getPackagingComponentStatus` | `GET_PACKAGING_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | 0 | 7 | — | — |
| `getPackagingById` | query | PKG-BE-B-02 | `getPackagingById` | `GET_PACKAGING_DETAIL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 1 | `SPARK_Packaging.…PackagingDetailsFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `getPackagingById` | query | PKG-BE-B-02 | `getPackagingById` | `GET_PACKAGING_DETAIL_WITH_INTERNAL_DATA` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 1 | `SPARK_Packaging.…PackagingDetailsFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `getPackagingById` | query | PKG-BE-B-02 | `getPackagingPacketInformation` | `GET_PACKAGING_PACKET_INFORMATION` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 1 | — | 2 fragment(s) |
| `getPackagingFieldValuesByType` | query | PKG-BE-B-04 | `getPackagingFieldValuesByType` | `GET_PACKAGING_FIELD_VALUES_BY_TYPE` | `src/libs/spark-packaging-base/src/graphql/PackagingDetailsQueries.ts` | 0 | 5 | — | — |
| `getPackagings` | query | PKG-BE-B-01 | `getPackagings` | `GET_PACKAGING_DETAILS_BY_PARENTS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 2 | `SPARK_Packaging.…PackagingDetailsFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `getPackagings` | query | PKG-BE-B-01 | `getPackagings` | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 0 | 2 | `SPARK_Packaging.…PackagingDetailsFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `getPackagings` | query | PKG-BE-B-01 | `getPackagings` | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `src/libs/spark-packaging-base/src/graphql/PackagingDetailsQueries.ts` | 0 | 2 | `SPARK_Packaging.…PackagingDetailsBaseFragment (fragment defined outside snapshot)` | 2 fragment(s) |
| `getPackagings` | query | PKG-BE-B-01 | `getPackagingPacketsInformation` | `GET_PACKAGING_PACKETS_INFORMATION` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 2 | — | 2 fragment(s) |
| `lockPackaging` | mutation | PKG-BE-D-06 | `lockPackaging` | `LOCK_PACKAGING` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 3 | — | — |
| `unlockPackaging` | mutation | PKG-BE-D-07 | `unlockPackaging` | `UNLOCK_PACKAGING` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 3 | — | — |
| `updatePackaging` | mutation | PKG-BE-E-01 | `updatePackaging` | `UPDATE_PACKAGING_DETAIL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 2 | — | — |
| `updatePackagingComponentStatus` | mutation | PKG-BE-D-09 | `updatePackagingComponentStatus` | `UPDATE_PACKAGING_COMPONENT_STATUS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 1 | 3 | — | — |

### Watchlist (`watchlist`) — 5 rows · DGS: `plm-product (co-located)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `cloneFilesForWatchlist` | mutation | WATCHLIST-BE-D-02 | `cloneFilesForWatchlist` | `CLONE_WATCHLIST_ATTACHMENTS` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | 1 | 3 | — | — |
| `createWatchlistEntries` | mutation | WATCHLIST-BE-D-01 | `createWatchlistEntries` | `CREATE_WATCHLIST_ENTRIES` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | 0 | 2 | — | — |
| `getWatchlistByFilter` | query | WATCHLIST-BE-C-01 | `getWatchlistForBulkUpdate` | `GET_WATCHLIST_FOR_BULK_UPDATE` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | 1 | 18 | — | multi-root op (2 root fields); 5 fragment(s) |
| `getWatchlistByIds` | query | WATCHLIST-BE-B-01 | `getWatchlistByIds` | `GET_WATCHLIST_BY_IDS` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | 3 | 1 | — | 5 fragment(s) |
| `updateWatchlistEntries` | mutation | WATCHLIST-BE-E-01 | `updateWatchlistEntries` | `UPDATE_WATCHLIST_ENTRIES` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | 2 | 2 | — | — |

### Impression (`impression`) — 2 rows · DGS: `plm-product (co-located)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `searchImpressionsByProductId` | query | IMPRESSION-BE-B-01 | `getBomDataAndImpressions` | `GET_BOM_TEMPLATES_AND_IMPRESSIONS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 1 | 5 | `SPARK_FabricSpecCombo.…BomFabricSpecComboSlimDetails (fragment defined outside snapshot)`; `SPARK_FabricSpecification.…SPARK_FabricSpecification_Files (fragment defined outside snapshot)`; `SPARK_Impression.…ImpressionFragment (fragment defined outside snapshot)` | multi-root op (2 root fields); 4 fragment(s) |
| `searchImpressionsByProductId` | query | IMPRESSION-BE-B-01 | `getCarryForwardFormData` | `GET_CARRY_FORWARD_FORM_DATA` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 3 | 32 | — | multi-root op (2 root fields); 6 fragment(s) |

### Claims (`claims`) — 18 rows · DGS: `spark-claims (separate)`

| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client constant | Client file | Components | Fields req. | Missing fields | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `bulkUpdateClaim` | mutation | CLAIM-BE-D-02 | `bulkUpdateClaim` | `BULK_UPDATE_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 1 | 2 | — | — |
| `createClaim` | mutation | CLAIM-BE-D-01 | `createClaim` | `ADD_CLAIMS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 2 | 4 | — | — |
| `getAllClaimsAbout` | query | CLAIM-BE-B-04 | `getClaims` | `GET_CLAIMS_AND_CHANNELS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 2 | 9 | — | multi-root op (3 root fields); 2 fragment(s) |
| `getAllClaimsAbout` | query | CLAIM-BE-B-04 | `getClaimByIds` | `GET_CLAIM_BY_ID` | `(local) ClientCallingGqlQueries/claims__ClaimQueries.txt` | 0 | 9 | `SPARK_Claims.includeWorkspaces` | multi-root op (3 root fields); 2 fragment(s) |
| `getClaimByIds` | query | CLAIM-BE-B-02 | `getClaimByIds` | `GET_CLAIM_BY_ID` | `(local) ClientCallingGqlQueries/claims__ClaimQueries.txt` | 0 | 9 | `SPARK_Claims.includeWorkspaces` | multi-root op (3 root fields); 2 fragment(s) |
| `getClaimByIds` | query | CLAIM-BE-B-02 | `getClaimComponentStatus` | `GET_CLAIM_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | 0 | 7 | — | — |
| `getClaimByIds` | query | CLAIM-BE-B-02 | `breadcrumbClaims` | `GET_CLAIM_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/graphql/BreadcrumbQueries.ts` | 1 | 3 | — | — |
| `getClaimByIds` | query | CLAIM-BE-B-02 | `getClaimByIds` | `GET_CLAIM_TEMPLATE_BY_ID` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 2 | 1 | `SPARK_Claims.includeWorkspaces` | 2 fragment(s) |
| `getClaims` | query | CLAIM-BE-B-01 | `getClaims` | `GET_CLAIMS_AND_CHANNELS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 2 | 9 | — | multi-root op (3 root fields); 2 fragment(s) |
| `getClaims` | query | CLAIM-BE-B-01 | `getClaims` | `GET_PRODUCT_TEMPLATE_CLAIMS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 1 | 33 | — | 2 fragment(s) |
| `getCommunicationChannels` | query | CLAIM-BE-B-03 | `getClaims` | `GET_CLAIMS_AND_CHANNELS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 2 | 9 | — | multi-root op (3 root fields); 2 fragment(s) |
| `getCommunicationChannels` | query | CLAIM-BE-B-03 | `getClaimByIds` | `GET_CLAIM_BY_ID` | `(local) ClientCallingGqlQueries/claims__ClaimQueries.txt` | 0 | 9 | `SPARK_Claims.includeWorkspaces` | multi-root op (3 root fields); 2 fragment(s) |
| `getCommunicationChannels` | query | CLAIM-BE-B-03 | `getComponentVersion` | `GET_CLAIM_VERSION` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 0 | 6 | `SPARK_Claims.includeWorkspaces` | multi-root op (2 root fields); 2 fragment(s) |
| `getCommunicationChannels` | query | CLAIM-BE-B-03 | `getCommunicationChannels` | `GET_COMMUNICATION_CHANNELLS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 0 | 5 | — | — |
| `lockClaim` | mutation | CLAIM-BE-D-04 | `lockClaim` | `LOCK_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 1 | 3 | — | — |
| `requestClaimExport` | mutation | CLAIM-BE-D-03 | `requestClaimExport` | `REQUEST_REPORT` | `src/libs/spark-ui-admin/src/graphql/uiAdminMutations.ts` | 0 | 1 | — | — |
| `unlockClaim` | mutation | CLAIM-BE-D-05 | `unlockClaim` | `UNLOCK_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 1 | 3 | — | — |
| `updateClaim` | mutation | CLAIM-BE-E-01 | `updateClaim` | `UPDATE_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 2 | 3 | — | — |

## Unused backend operations on phase-1 schemas (no frontend caller)

- Candidates for deprecation review, or callers outside pdex-ui-react (service-to-service, exports, jobs).

| Root field | Kind | Schema file | Domain |
|---|---|---|---|
| `getBomDataV2` | query | `schemas/SPARK_Bom.graphqls` | BOM |
| `getClaimExports` | query | `schemas/SPARK_Claims.graphqls` | Claims |
| `getClaimsElastic` | query | `schemas/SPARK_Claims.graphqls` | Claims |
| `getCopyStatus` | query | `schemas/SPARK_Product.graphqls` | Product |
| `getImpressionCountsByProductId` | query | `schemas/SPARK_Impression.graphqls` | Impression |
| `getPackagingElastic` | query | `schemas/SPARK_Packaging.graphqls` | Packaging |
| `getProductDetailsElastic` | query | `schemas/SPARK_ProductDetail.graphqls` | Product Details |
| `getProductTemplateById` | query | `schemas/SPARK_Product.graphqls` | Product |
| `getRatingByTcin` | query | `schemas/SPARK_Product.graphqls` | Product |
| `getSampleMeasurement` | query | `schemas/SPARK_Measurement.graphqls` | Measurement |
| `getWatchlistInspectionActions` | query | `schemas/SPARK_Watchlist.graphqls` | Watchlist |
| `getWatchlistReasons` | query | `schemas/SPARK_Watchlist.graphqls` | Watchlist |
| `searchGuestFacing` | query | `schemas/SPARK_Claims.graphqls` | Claims |
| `addMeasurement` | mutation | `schemas/SPARK_Measurement.graphqls` | Measurement |
| `cloneFilesForDielines` | mutation | `schemas/SPARK_Packaging.graphqls` | Packaging |
| `dropProductBusinessPartner` | mutation | `schemas/SPARK_Product.graphqls` | Product |
| `manageBomWorkspaces` | mutation | `schemas/SPARK_Bom.graphqls` | BOM |
| `removeProductBusinessPartner` | mutation | `schemas/SPARK_Product.graphqls` | Product |
| `removeProductResources` | mutation | `schemas/SPARK_Product.graphqls` | Product |
| `unDropProductBusinessPartner` | mutation | `schemas/SPARK_Product.graphqls` | Product |
| `updateImpressions` | mutation | `schemas/SPARK_Impression.graphqls` | Impression |
| `updateMeasurement` | mutation | `schemas/SPARK_Measurement.graphqls` | Measurement |
| `updateMeasurementAccess` | mutation | `schemas/SPARK_Measurement.graphqls` | Measurement |
| `updateMeasurementComponentStatus` | mutation | `schemas/SPARK_Measurement.graphqls` | Measurement |
| `updateProductDetailAccess` | mutation | `schemas/SPARK_ProductDetail.graphqls` | Product Details |
| `updateWorkspaceAttributes` | mutation | `schemas/SPARK_Product.graphqls` | Product |

## Unused schema fields on phase-1 types

- Fields defined on phase-1 object types that no frontend selection ever requests.
- Input: consolidation candidates when deriving the federated schema.

| Type | Unused fields |
|---|---|
| `CORONA_ItemDetails` | `alternateImages`, `colorFamily`, `colorName` |
| `DopplerDepartment` | `divisionId` |
| `ProductComponentStatus` | `updatedAt`, `updatedBy` |
| `SPARK_Bom` | `archived`, `bomBaseType`, `libraryLinked`, `type`, `workspaceContext` |
| `SPARK_BomCombinationMaterial` | `additionalMaterialDetails`, `attachmentIds`, `componentLocation`, `criticalToQuality`, `defaultTcin`, `description`, `genericMaterialType`, `length`, `lengthInMillimeters`, `lengthUom`, `lengthUomId`, `materialCategory`, `notes`, `primaryMaterialAttachmentId`, `quantity`, `quantityUom`, `recycledContent`, `rowId`, `sectionId`, `sectionName`, `size`, `sizeUom`, `supplierArticleNumber`, `supplierId`, `supplierName`, `tcinDpcis`, `tcinIds`, `thickness`, `thicknessInMillimeters`, `thicknessUom`, `thicknessUomId`, `weight`, `weightInGrams`, `weightUomId`, `width`, `widthInMillimeters`, `widthUom`, `widthUomId`, `yieldConsumptionUom` |
| `SPARK_BomFabricMaterial` | `additionalMaterialDetails`, `attachmentIds`, `componentLocation`, `criticalToQuality`, `defaultTcin`, `description`, `genericMaterialType`, `length`, `lengthInMillimeters`, `lengthUom`, `lengthUomId`, `materialCategory`, `notes`, `primaryMaterialAttachmentId`, `quantity`, `quantityUom`, `recycledContent`, `rowId`, `sectionId`, `sectionName`, `size`, `sizeUom`, `supplierArticleNumber`, `supplierId`, `supplierName`, `tcinDpcis`, `tcinIds`, `thickness`, `thicknessInMillimeters`, `thicknessUom`, `thicknessUomId`, `weight`, `weightInGrams`, `weightUomId`, `width`, `widthInMillimeters`, `widthUom`, `widthUomId`, `yieldConsumptionUom` |
| `SPARK_BomFabricSpecMaterial` | `additionalMaterialDetails`, `attachmentIds`, `componentLocation`, `criticalToQuality`, `defaultTcin`, `description`, `genericMaterialType`, `length`, `lengthInMillimeters`, `lengthUom`, `lengthUomId`, `materialCategory`, `notes`, `primaryMaterialAttachmentId`, `quantity`, `quantityUom`, `recycledContent`, `rowId`, `sectionId`, `sectionName`, `size`, `sizeUom`, `supplierArticleNumber`, `supplierId`, `supplierName`, `tcinDpcis`, `tcinIds`, `thickness`, `thicknessInMillimeters`, `thicknessUom`, `thicknessUomId`, `weight`, `weightInGrams`, `weightUomId`, `width`, `widthInMillimeters`, `widthUom`, `widthUomId`, `yieldConsumptionUom` |
| `SPARK_BomImpressionDetails_Unified` | *(entire type unreferenced by FE selections)* |
| `SPARK_BomMaterial` | `additionalMaterialDetails`, `attachmentIds`, `componentLocation`, `criticalToQuality`, `cuttableWidth`, `defaultTcin`, `description`, `genericMaterialType`, `length`, `lengthInMillimeters`, `lengthUom`, `lengthUomId`, `materialCategory`, `notes`, `parentLibraryResourceId`, `primaryMaterialAttachmentId`, `quantity`, `quantityUom`, `recycledContent`, `rowId`, `sectionId`, `sectionName`, `size`, `sizeUnitOfMeasure`, `sizeUom`, `supplierArticleNumber`, `supplierId`, `supplierName`, `tcinDpcis`, `tcinIds`, `thickness`, `thicknessInMillimeters`, `thicknessUom`, `thicknessUomId`, `weight`, `weightInGrams`, `weightUomId`, `width`, `widthInMillimeters`, `widthUom`, `widthUomId`, `yieldConsumption`, `yieldConsumptionUom` |
| `SPARK_BomMaterial_Library_Unified` | *(entire type unreferenced by FE selections)* |
| `SPARK_BomMaterial_Unified` | *(entire type unreferenced by FE selections)* |
| `SPARK_BomPackagingMaterial` | `additionalMaterialDetails`, `attachmentIds`, `componentLocation`, `criticalToQuality`, `defaultTcin`, `description`, `genericMaterialType`, `length`, `lengthInMillimeters`, `lengthUom`, `lengthUomId`, `materialCategory`, `notes`, `primaryMaterialAttachmentId`, `quantity`, `quantityUom`, `recycledContent`, `rowId`, `sectionId`, `sectionName`, `size`, `sizeUom`, `supplierArticleNumber`, `supplierId`, `supplierName`, `tcinIds`, `thickness`, `thicknessInMillimeters`, `thicknessUom`, `thicknessUomId`, `weight`, `weightInGrams`, `weightUomId`, `width`, `widthInMillimeters`, `widthUom`, `widthUomId` |
| `SPARK_BomTrimLibraryImpressionDetails` | `finishId`, `groundFinishRowId`, `rowId`, `textFinishRowId` |
| `SPARK_BomTrimMaterial` | `additionalMaterialDetails`, `attachmentIds`, `componentLocation`, `criticalToQuality`, `cuttableWidth`, `defaultTcin`, `description`, `genericMaterialType`, `length`, `lengthInMillimeters`, `lengthUom`, `lengthUomId`, `materialCategory`, `notes`, `primaryMaterialAttachmentId`, `quantity`, `quantityUom`, `recycledContent`, `rowId`, `sectionId`, `sectionName`, `size`, `sizeUom`, `supplierArticleNumber`, `supplierName`, `tcinDpcis`, `tcinIds`, `thickness`, `thicknessInMillimeters`, `thicknessUom`, `thicknessUomId`, `weight`, `weightInGrams`, `weightUomId`, `width`, `widthInMillimeters`, `widthUom`, `widthUomId`, `yieldConsumption`, `yieldConsumptionUom` |
| `SPARK_BomWashMaterial` | `additionalMaterialDetails`, `attachmentIds`, `componentLocation`, `criticalToQuality`, `cuttableWidth`, `defaultTcin`, `description`, `genericMaterialType`, `length`, `lengthInMillimeters`, `lengthUom`, `lengthUomId`, `materialCategory`, `materialLibraryUom`, `notes`, `primaryMaterialAttachmentId`, `quantity`, `quantityUom`, `recycledContent`, `rowId`, `sectionId`, `sectionName`, `size`, `sizeUom`, `supplierArticleNumber`, `supplierId`, `supplierName`, `tcinDpcis`, `tcinIds`, `thickness`, `thicknessInMillimeters`, `thicknessUom`, `thicknessUomId`, `weight`, `weightInGrams`, `weightUomId`, `width`, `widthInMillimeters`, `widthUom`, `widthUomId`, `yieldConsumption`, `yieldConsumptionUom` |
| `SPARK_Bom_Type` | *(entire type unreferenced by FE selections)* |
| `SPARK_Bom_Unified` | *(entire type unreferenced by FE selections)* |
| `SPARK_ClaimDetails` | `claimCategory`, `technicalClaim` |
| `SPARK_ClaimExport` | *(entire type unreferenced by FE selections)* |
| `SPARK_ClaimPackagingCopy` | `descriptor`, `warningsAndCaution` |
| `SPARK_Claims` | `partners`, `workspaces` |
| `SPARK_CodeName` | *(entire type unreferenced by FE selections)* |
| `SPARK_ContactInformation` | *(entire type unreferenced by FE selections)* |
| `SPARK_Dieline` | `attachmentId`, `printerLocationId`, `sizeIds` |
| `SPARK_Guest_Facing` | *(entire type unreferenced by FE selections)* |
| `SPARK_Impression` | `associatedBomIds`, `createdAt`, `createdBy`, `deletable`, `owningBusinessPartner`, `owningPartnerId`, `owningPartnerType`, `parentId`, `relatedResources`, `sortOrder`, `updatedAt`, `updatedBy`, `version`, `workspaceContext`, `workspaces` |
| `SPARK_ImpressionCount` | *(entire type unreferenced by FE selections)* |
| `SPARK_LibraryMaterial` | *(entire type unreferenced by FE selections)* |
| `SPARK_MeasurementBaseType` | *(entire type unreferenced by FE selections)* |
| `SPARK_Measurements` | `baseType` |
| `SPARK_Packaging` | `access`, `archived`, `attachments`, `contactInformation`, `copyWriterEditAndApproved`, `createdAt`, `createdBy`, `creativePath`, `creativePathName`, `descriptionDisplayText`, `dielineDueDate`, `dielineEvaluators`, `fulfillmentTypeId`, `fulfillmentTypeName`, `group`, `groupName`, `handoffDueDate`, `illustrationRequired`, `notes`, `orderCode`, `packagingInternalData`, `participantDetails`, `photoRequired`, `placeholderId`, `projectItemType`, `projectItemTypeName`, `projectLevel`, `projectLevelName`, `projectType`, `projectTypeName`, `requiresSuggestedRetailPrice`, `resolvedSelectedComponents`, `retailPrice`, `selectedComponents`, `status`, `suggestedRetailPriceByDPCI`, `updatedAt`, `updatedBy`, `version`, `warningsAndCautions`, `warningsAndCautionsList`, `wave`, `waveDescription`, `workspaceIds` |
| `SPARK_PackagingElement` | `id`, `selectedComponentId`, `selectedComponentName` |
| `SPARK_PackagingInternalData` | *(entire type unreferenced by FE selections)* |
| `SPARK_PackagingPaged` | `pageable`, `paging` |
| `SPARK_PomSizes` | `displayValue` |
| `SPARK_PrinterDieline` | `dielineContactName`, `dielineEmail`, `fileDeliveryEmailList`, `isPrintInformationReviewed`, `printerAddress`, `printerCity`, `printerCode`, `printerCompanyName`, `printerContactEmail`, `printerCountry`, `printerCountryName`, `printerId`, `printerLocationId`, `printerPhoneNumber`, `printerSoftproofing`, `printerState`, `printerZipcode`, `printingProcess`, `reservedDpcis`, `shippingAddressSameAsPrinterAddress`, `shippingDestination`, `sizeIds` |
| `SPARK_PrintingProcess` | *(entire type unreferenced by FE selections)* |
| `SPARK_PrintingProcessSubstrate` | *(entire type unreferenced by FE selections)* |
| `SPARK_Product` | `associateProductsAsks`, `discussionsCount`, `elasticSamplesList`, `fbDpci`, `hasNotEvaluatedReceivedSamples`, `hasSamplesUpcomingDue`, `productWorkspaceAttributes`, `receivedNotEvaluatedCount`, `sampleIds`, `teamsV2`, `type`, `variations`, `versionCreatedAt`, `versionCreatedBy` |
| `SPARK_ProductCopy` | *(entire type unreferenced by FE selections)* |
| `SPARK_ProductDetails` | `constructionTemplate`, `type`, `workspaceContext` |
| `SPARK_ProductTemplateStatus` | `description` |
| `SPARK_ProductTemplatesList` | `pageable` |
| `SPARK_ProductWorkspaceAttributes` | *(entire type unreferenced by FE selections)* |
| `SPARK_ProductWorkspaceInfo` | `archived`, `isHidden` |
| `SPARK_ProductsPaged` | `pageable` |
| `SPARK_PurchaseOrderDetails` | *(entire type unreferenced by FE selections)* |
| `SPARK_ResourcesCount` | `boms`, `partnerId`, `workspaceContext` |
| `SPARK_ShippingDestination` | *(entire type unreferenced by FE selections)* |
| `SPARK_Softproofing` | *(entire type unreferenced by FE selections)* |
| `SPARK_SuggestedRetailPriceByDPCI` | *(entire type unreferenced by FE selections)* |
| `SPARK_Tcin` | `launchedAt`, `parentTcins`, `purchaseOrders`, `relationshipType` |
| `SPARK_WarningsAndCautions` | *(entire type unreferenced by FE selections)* |
| `SPARK_WatchlistInspectionAction` | *(entire type unreferenced by FE selections)* |
| `SPARK_WorkspaceInfoPartner` | `archived`, `preProdStatusAt`, `preferred`, `prodStatusAt` |
| `VMM_BusinessPartnerCategory` | *(entire type unreferenced by FE selections)* |
