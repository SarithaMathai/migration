# Traceability Matrix — Domain → Schema → Resolver → Client → Impact → Stories

> Generated: 2026-07-16 · One row per phase-1 frontend operation × backend root field.
> Chain: Business Domain → Backend Schema → Resolver → Frontend Query → Client Component → FE story → BE story.

## Product

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_Product.graphqls` | `addBusinessPartnersToProductWithType` | `addBusinessPartnersToProductWithType` | `ADD_PARTNERS_PRODUCT_WITH_TYPE` | — | PRODUCT-FE-008 | PRODUCT-BE-D-07 |
| `schemas/SPARK_Product.graphqls` | `addProduct` | `addProduct` | `ADD_PRODUCT` | `ProductNew.tsx`<br>`ProductTemplateNew.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-01 |
| `schemas/SPARK_Product.graphqls` | `addProductRule` | `addProductRule` | `ADD_PRODUCT_RULE` | — | PRODUCT-FE-006 | PRODUCT-BE-D-15 |
| `schemas/SPARK_Product.graphqls` | `addProducts` | `addProducts` | `PRODUCT_BULK` | `ProductBulkCreate.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-02 |
| `schemas/SPARK_Product.graphqls` | `addTeamsToProduct` | `addTeams` | `ADD_TEAMS_PRODUCT` | `BPSelector.tsx` | PRODUCT-FE-008 | PRODUCT-BE-D-06 |
| `schemas/SPARK_Product.graphqls` | `bulkUpdateProducts` | `bulkUpdateProducts` | `PRODUCT_BULK_UPDATE` | `ProductBulkUpdate.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-03 |
| `schemas/SPARK_Product.graphqls` | `carryForwardProduct` | `carryForwardProduct` | `CARRY_FORWARD_PRODUCT` | `ProductCarryForwardModal.tsx`<br>`WorkspacePlanGrid.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-05 |
| `schemas/SPARK_Product.graphqls` | `deleteProductRule` | `deleteProductRule` | `DELETE_PRODUCT_RULE` | — | PRODUCT-FE-006 | PRODUCT-BE-D-17 |
| `schemas/SPARK_Product.graphqls` | `getAllAvailableRules` | `getAllAvailableRules` | `GET_ALL_AVAILABLE_RULES` | — | PRODUCT-FE-006 | PRODUCT-BE-B-09 |
| `schemas/SPARK_Product.graphqls` | `getCategories` | `getCategories` | `GET_PRODUCT_TEMPLATE_CATEGORY` | `ProductTemplateSideFilterForm.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-03 |
| `schemas/SPARK_Product.graphqls` | `getCategories` | `getCategories` | `GET_WORKSPACE_CATEGORY` | `ProductListSideFilterForm.tsx`<br>`UserListSideFilterForm.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-03 |
| `schemas/SPARK_Product.graphqls` | `getCategories` | `getCategories` | `GET_WORKSPACE_CATEGORY_CLAZZ` | `ProductListSideFilterForm.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-03 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getCarryForwardFormData` | `GET_CARRY_FORWARD_FORM_DATA` | `ProductQueries.testHelper.tsx`<br>`ProductCarryForwardModal.tsx`<br>`WorkspaceCarryForwardSpecsForm.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `GET_PRODUCT` | `ImportProductDetailsModal.tsx`<br>`ProductEdit.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWorkspaces` | `GET_PRODUCT_AND_WORKSPACES` | `ReleaseProductPacket.tsx`<br>`WatchlistForm.tsx`<br>`WatchlistViewTemplate.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWorkspaces` | `GET_PRODUCT_AND_WORKSPACES_WITH_STATUS` | `ReleaseTechPackModal.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductById` | `GET_PRODUCT_BY_ID` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductComponentStatusCounts` | `GET_PRODUCT_COMPONENT_STATUS_COUNTS` | `BomViewTemplate.tsx`<br>`ProductFilesQueries.testHelper.tsx`<br>`SpecsContainer.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `breadcrumbProduct` | `GET_PRODUCT_CRUMB` | `BreadcrumbProduct.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductStatusUpdateInfo` | `GET_PRODUCT_FOR_STATUS_UPDATE` | `ProductQueries.testHelper.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `GET_PRODUCT_MINIMAL` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getTeams` | `GET_PRODUCT_TEAMS` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getTeams` | `GET_PRODUCT_TEAMS` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWithAttachmentsAndComponents` | `GET_PRODUCT_WITH_ATTACHMENTS_AND_COMPONENTS` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `GET_PRODUCT_WITH_META_DATA` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWithTeams` | `GET_PRODUCT_WITH_TEAMS` | `BPSelector.tsx`<br>`Teams.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `GET_SPARK_PRODUCT_BP` | `ImportProductDetailsSection.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `GET_SPARK_PRODUCT_BP` | `ImportProductDetailsSection.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductScaffolding` | `GET_SPARK_PRODUCT_SCAFFOLDING` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `GET_SPARK_PRODUCT_V2` | `ProductsListItem.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `GET_SPARK_PRODUCT_V2` | `ProductsListItem.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getDpciInfo` | `USE_DPCI_INFO` | `useDpciInformation.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProductBPRules` | `getProductBPRules` | `GET_PRODUCT_BUSINESS_PARTNER_RULES` | — | PRODUCT-FE-006 | PRODUCT-BE-B-11 |
| `schemas/SPARK_Product.graphqls` | `getProductDeptRules` | `getProductDeptRules` | `GET_PRODUCT_DEPARTMENT_RULES` | — | PRODUCT-FE-006 | PRODUCT-BE-B-10 |
| `schemas/SPARK_Product.graphqls` | `getProductRules` | `getProductRules` | `GET_RULES` | — | PRODUCT-FE-006 | PRODUCT-BE-B-07 |
| `schemas/SPARK_Product.graphqls` | `getProductRulesById` | `getProductRule` | `GET_RULE` | — | PRODUCT-FE-006 | PRODUCT-BE-B-08 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getFormData` | `GET_PRODUCTS_BY_ID_LIST` | `ProductBulkUpdate.tsx` | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getProductStatusUpdateInfo` | `GET_PRODUCT_FOR_STATUS_UPDATE` | `ProductQueries.testHelper.tsx` | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getStatus` | `GET_PRODUCT_STATUS` | — | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getProductWorkspaceMetricsReportCount` | `GET_PRODUCT_WORKSPACES_METRICS_REPORT_COUNT` | `WorkspaceOverview.tsx` | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductTechPackBulkCountV1` | `getTechPackBulkCount` | `BULK_TECHPACK_COUNTS` | `BulkGenerateProductPacketModal.tsx`<br>`BulkGenerateReleasePacketModal.tsx` | PRODUCT-FE-010 | PRODUCT-BE-E-04 |
| `schemas/SPARK_Product.graphqls` | `getProductTechPackCountV1` | `getTechPackCountV1` | `GET_COUNT_V1` | `GenerateTechPackModal.tsx`<br>`ReleaseTechPackModal.tsx` | PRODUCT-FE-010 | PRODUCT-BE-E-03 |
| `schemas/SPARK_Product.graphqls` | `getProductTemplates` | `getProductTemplates` | `GET_ALL_PRODUCTS_TEMPLATES` | `ProductTemplateQueries.testHelper.tsx`<br>`TemplateLibraryContainer.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-02 |
| `schemas/SPARK_Product.graphqls` | `getProductTemplates` | `getProductTemplates` | `GET_PRODUCTS_WITH_IDS` | `ClaimBulkUpdate.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-02 |
| `schemas/SPARK_Product.graphqls` | `getProductTemplates` | `getProductTemplates` | `GET_PRODUCT_TEMPLATE` | `ProductTemplatePDTLExpandedView.tsx`<br>`ProductTemplateEdit.tsx`<br>`ProductTemplateOverviewContainer.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-02 |
| `schemas/SPARK_Product.graphqls` | `getProductVersions` | `getProductVersions` | `GET_PRODUCT_VERSIONS` | — | PRODUCT-FE-002 | PRODUCT-BE-B-04 |
| `schemas/SPARK_Product.graphqls` | `getProducts` | `getProducts` | `GET_ALL_PRODUCTS` | — | PRODUCT-FE-003 | PRODUCT-BE-S-02 |
| `schemas/SPARK_Product.graphqls` | `getProducts` | `getProducts` | `GET_PRODUCTS_WITH_SAMPLE_DETAILS` | `SampleCompare.tsx` | PRODUCT-FE-003 | PRODUCT-BE-S-02 |
| `schemas/SPARK_Product.graphqls` | `getProducts` | `getProducts` | `PID_AND_WRK_ID_SEARCH` | `PIDOrWRKIDSelectAutoComplete.tsx` | PRODUCT-FE-003 | PRODUCT-BE-S-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getBulkDiscussionData` | `GET_BULK_DISCUSSION_DATA` | `DiscussionBulkCreate.tsx` | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getFilesWithMetaData` | `GET_FILES_WITH_METADATA` | — | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getFormData` | `GET_PRODUCTS_BY_ID_LIST` | `ProductBulkUpdate.tsx` | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getTeamsProductAndWorkspace` | `GET_TEAMS_PRODUCT_AND_WORKSPACE` | `ProductQueries.testHelper.tsx`<br>`ReplaceWorkspaceFieldset.tsx` | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `linkProduct` | `linkProduct` | `LINK_PRODUCT` | `ProductActionsDropDown.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-13 |
| `schemas/SPARK_Product.graphqls` | `productBusinessPartnerActions` | `productBusinessPartnerActions` | `BUSINESS_PARTNER_ACTIONS_PRODUCT` | `Teams.tsx` | PRODUCT-FE-009 | PRODUCT-BE-S-03 |
| `schemas/SPARK_Product.graphqls` | `searchProductRules` | `searchProductRules` | `GET_SEARCH_PRODUCT_DEPARTMENT_RULES` | `useSearchProductRules.tsx` | PRODUCT-FE-006 | PRODUCT-BE-C-05 |
| `schemas/SPARK_Product.graphqls` | `unlinkProduct` | `unlinkProduct` | `UNLINK_PRODUCT` | `Links.tsx`<br>`ProductLinkRailListItem.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-14 |
| `schemas/SPARK_Product.graphqls` | `updateBusinessPartnerStatuses` | `updateBusinessPartnerStatuses` | `UPDATE_PRODUCT_STATUSES` | `BPSelector.tsx`<br>`ProductsGridItem.tsx`<br>`ProductsListItemHeader.tsx` | PRODUCT-FE-009 | PRODUCT-BE-D-09 |
| `schemas/SPARK_Product.graphqls` | `updateComponentStatus` | `updateComponentStatus` | `UPDATE_COMPONENT_STATUS` | `ComponentStatusDropdown.tsx` | PRODUCT-FE-011 | PRODUCT-BE-D-18 |
| `schemas/SPARK_Product.graphqls` | `updateComponentStatuses` | `updateComponentStatuses` | `UPDATE_COMPONENT_STATUSES` | `ProductComponentSetStatusesDropdown.tsx` | PRODUCT-FE-011 | PRODUCT-BE-E-02 |
| `schemas/SPARK_Product.graphqls` | `updateProduct` | `updateProduct` | `UPDATE_PRODUCT` | — | PRODUCT-FE-007 | PRODUCT-BE-D-04 |
| `schemas/SPARK_Product.graphqls` | `updateProduct` | `updateProduct` | `UPDATE_PRODUCT` | — | PRODUCT-FE-007 | PRODUCT-BE-D-04 |
| `schemas/SPARK_Product.graphqls` | `updateProduct` | `updateProduct` | `UPDATE_PRODUCT_TEMPLATE` | `ProductTemplateEdit.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-04 |
| `schemas/SPARK_Product.graphqls` | `updateProductRule` | `updateProductRule` | `UPDATE_PRODUCT_RULE` | — | PRODUCT-FE-006 | PRODUCT-BE-D-16 |
| `schemas/SPARK_Product.graphqls` | `updateProductTeamsWorkspaceContext` | `updateProductTeamsWorkspaceContext` | `MANAGE_TEAMS_WORKSPACES` | `ManageTeamWorkspacesModal.tsx` | PRODUCT-FE-008 | PRODUCT-BE-D-12 |
| `schemas/SPARK_Product.graphqls` | `updateViewToggle` | `updateViewToggle` | `TOGGLE_VIEW_SWITCH` | `ToggleViewFilter.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-10 |

## BOM

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_Bom.graphqls` | `addBom` | `addBom` | `ADD_BOM` | `BomCloneTemplate.tsx`<br>`BomCreateTemplate.tsx` | BOM-FE-006 | BOM-BE-D-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomByIds` | `GET_BOMS_BY_IDS` | `BomCloneTemplate.tsx`<br>`useBomsByIds.ts` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomByIds` | `GET_BOMS_BY_IDS_WITH_PRODUCT_INFO` | `BomViewTemplate.tsx` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomByIds` | `GET_BOM_BY_ID` | — | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomComponentStatus` | `GET_BOM_COMPONENT_STATUS` | `useComponentStatus.ts` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomDataAndImpressions` | `GET_BOM_TEMPLATES_AND_IMPRESSIONS` | `ProductTemplateBomExpandedView.tsx` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByParentId` | `getBomByParentId` | `GET_BOMS_BY_PARENT_ID` | `useBomsByParentId.ts` | BOM-FE-002 | BOM-BE-B-04 |
| `schemas/SPARK_Bom.graphqls` | `getBomElastic` | `getBomElastic` | `GET_BOMS_FROM_ES_BY_PARENT_IDS` | `useBomsByParentIdsFromES.ts` | BOM-FE-003 | BOM-BE-C-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomMaterialTypes` | `getBomMaterialTypes` | `GET_BOM_MATERIAL_TYPES` | `useBomMaterialTypes.ts` | BOM-FE-004 | BOM-BE-B-05 |
| `schemas/SPARK_Bom.graphqls` | `getBomPackagingMaterialTypes` | `getBomPackagingMasterData` | `GET_BOM_PACKAGING_MASTER_DATA` | `useBomMaterialTypes.ts` | BOM-FE-004 | BOM-BE-B-06 |
| `schemas/SPARK_Bom.graphqls` | `getBomPackagingSubstrates` | `getBomPackagingSubstrates` | `GET_BOM_PACKAGING_SUBSTRATES` | — | BOM-FE-004 | BOM-BE-B-07 |
| `schemas/SPARK_Bom.graphqls` | `getBomPackagingUnitOfMeasure` | `getBomPackagingMasterData` | `GET_BOM_PACKAGING_MASTER_DATA` | `useBomMaterialTypes.ts` | BOM-FE-004 | BOM-BE-B-08 |
| `schemas/SPARK_Bom.graphqls` | `getBomStatus` | `getBomStatus` | `GET_BOM_STATUS` | — | BOM-FE-002 | BOM-BE-B-03 |
| `schemas/SPARK_Bom.graphqls` | `getComboSupplierForBom` | `getComboSupplierForBom` | `GET_COMBINATION_SUPPLIER_FOR_BOM` | — | BOM-FE-005 | BOM-BE-C-03 |
| `schemas/SPARK_Bom.graphqls` | `getValidRawMaterialSuppliersForBom` | `getValidSuppliersForBom` | `GET_VALID_SUPPLIERS_FOR_BOM` | `BomForm.tsx`<br>`PackagingBomForm.tsx` | BOM-FE-005 | BOM-BE-C-05 |
| `schemas/SPARK_Bom.graphqls` | `getValidTrimSuppliersForBom` | `getValidSuppliersForBom` | `GET_VALID_SUPPLIERS_FOR_BOM` | `BomForm.tsx`<br>`PackagingBomForm.tsx` | BOM-FE-005 | BOM-BE-C-04 |
| `schemas/SPARK_Bom.graphqls` | `lockBom` | `lockBom` | `LOCK_BOM` | `BomViewHeader.tsx` | BOM-FE-006 | BOM-BE-D-03 |
| `schemas/SPARK_Bom.graphqls` | `searchMaterialsBom` | `searchMaterialsBom` | `BOM_SEARCH_MATERIALS` | — | BOM-FE-003 | BOM-BE-S-03 |
| `schemas/SPARK_Bom.graphqls` | `unlockBom` | `unlockBom` | `UNLOCK_BOM` | `BomViewHeader.tsx` | BOM-FE-006 | BOM-BE-D-04 |
| `schemas/SPARK_Bom.graphqls` | `updateBom` | `updateBom` | `UPDATE_BOM` | `BomViewTemplate.tsx` | BOM-FE-006 | BOM-BE-S-01 |
| `schemas/SPARK_Bom.graphqls` | `updateBomComponentStatus` | `updateBomComponentStatus` | `UPDATE_BOM_COMPONENT_STATUS` | `BomViewTemplate.tsx` | BOM-FE-006 | BOM-BE-D-05 |

## Measurement

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_Measurement.graphqls` | `deleteSampleMeasurementSet` | `deleteSampleMeasurementSet` | `DELETE_SAMPLE_MEASUREMENT` | `SampleCompare.tsx`<br>`Sample.tsx` | MST-FE-004 | MST-BE-D-07 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementByIds` | `getMeasurementByIds` | `GET_MEASUREMENT_BY_IDS` | — | MST-FE-001 | MST-BE-B-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementByIds` | `getMeasurementComponentStatus` | `GET_MEASUREMENT_COMPONENT_STATUS` | `useComponentStatus.ts` | MST-FE-001 | MST-BE-B-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementByIds` | `getMeasurementByIds` | `GET_MEASUREMENT_SET_BY_ID` | — | MST-FE-001 | MST-BE-B-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementSetStatus` | `getMeasurementSetStatus` | `GET_MEASUREMENT_SET_STATUS` | `TightFitTemplateEditLayout.tsx` | MST-FE-001 | MST-BE-B-04 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurements` | `getMeasurements` | `GET_MEASUREMENTS` | `ImportMeasurementSet.tsx` | MST-FE-002 | MST-BE-C-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementsElastic` | `getMeasurementsElastic` | `GET_PRODUCT_TEMPLATE_MEASUREMENTS` | — | MST-FE-002 | MST-BE-C-02 |
| `schemas/SPARK_Measurement.graphqls` | `getThicknessUnitsOfMeasure` | `getMeasurementsMetaData` | `GET_MEASUREMENTS_META_DATA` | — | MST-FE-003 | MST-BE-B-03 |
| `schemas/SPARK_Measurement.graphqls` | `getUnitsOfMeasure` | `getMeasurementsMetaData` | `GET_MEASUREMENTS_META_DATA` | — | MST-FE-003 | MST-BE-B-02 |
| `schemas/SPARK_Measurement.graphqls` | `getUnitsOfMeasure` | `getUnitsOfMeasure` | `GET_UNITS_OF_MEASURE` | — | MST-FE-003 | MST-BE-B-02 |
| `schemas/SPARK_Measurement.graphqls` | `lockMeasurementSet` | `lockMeasurementSet` | `LOCK_MEASUREMENT_SET` | `MeasurementSetTemplate.tsx` | MST-FE-004 | MST-BE-D-03 |
| `schemas/SPARK_Measurement.graphqls` | `putSampleMeasurementSet` | `putSampleMeasurementSet` | `PUT_SAMPLE_MEASUREMENT` | `SampleCompare.tsx`<br>`SampleNew.tsx`<br>`Sample.tsx`<br>`SampleMeasurementEditTemplate.tsx` | MST-FE-004 | MST-BE-D-06 |
| `schemas/SPARK_Measurement.graphqls` | `unlockMeasurementSet` | `unlockMeasurementSet` | `UNLOCK_MEASUREMENT_SET` | `MeasurementSetTemplate.tsx` | MST-FE-004 | MST-BE-D-04 |

## Product Details

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_ProductDetail.graphqls` | `cloneFilesForProductDetails` | `cloneFilesForProductDetails` | `CLONE_PDTL_ATTACHMENTS` | `ProductDetailClone.tsx` | PDTL-FE-002 | PDTL-BE-D-04 |
| `schemas/SPARK_ProductDetail.graphqls` | `createProductDetailsSet` | `createProductDetailsSet` | `CREATE_PRODUCT_DETAILS_SET` | `ProductDetailsSetNew.tsx`<br>`ProductDetailClone.tsx` | PDTL-FE-002 | PDTL-BE-D-01 |
| `schemas/SPARK_ProductDetail.graphqls` | `getProductDetailsById` | `getProductDetailsById` | `GET_PRODUCT_DETAILS_SET_BY_IDS` | — | PDTL-FE-001 | PDTL-BE-B-01 |
| `schemas/SPARK_ProductDetail.graphqls` | `getProductDetailsById` | `getProductDetailComponentStatus` | `GET_PROUCT_DETAIL_COMPONENT_STATUS` | `useComponentStatus.ts` | PDTL-FE-001 | PDTL-BE-B-01 |
| `schemas/SPARK_ProductDetail.graphqls` | `productDetailLockUnlock` | `productDetailLockUnlock` | `PRODUCT_DETAILS_LOCK_UNLOCK` | `ProductDetailsViewTemplate.tsx` | PDTL-FE-002 | PDTL-BE-D-03 |
| `schemas/SPARK_ProductDetail.graphqls` | `updateProductDetailComponentStatus` | `updateProductDetailComponentStatus` | `UPDATE_PRODUCT_DETAIL_COMPONENT_STATUS` | `ProductDetailsViewTemplate.tsx` | PDTL-FE-002 | PDTL-BE-D-05 |
| `schemas/SPARK_ProductDetail.graphqls` | `updateProductDetailsSet` | `updateProductDetailsSet` | `UPDATE_PRODUCT_DETAILS_SET` | `ProductDetailsViewTemplate.tsx`<br>`ProductTemplateProductDetailsEdit.tsx` | PDTL-FE-003 | PDTL-BE-E-01 |

## Packaging

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_Packaging.graphqls` | `addPackaging` | `addPackaging` | `ADD_PACKAGING_DETAIL` | `PackagingDetailsCloneTemplate.tsx`<br>`PackagingDetailsNewTemplate.tsx` | PKG-FE-004 | PKG-BE-D-01 |
| `schemas/SPARK_Packaging.graphqls` | `bulkAddPackagings` | `bulkAddPackagings` | `BULK_ADD_PACKAGING_DETAILS` | `PackagingBulkCreate.tsx` | PKG-FE-004 | PKG-BE-D-03 |
| `schemas/SPARK_Packaging.graphqls` | `bulkUpdatePackagings` | `bulkUpdatePackagings` | `BULK_UPDATE_PACKAGING_DETAILS` | `PackagingBulkUpdate.tsx` | PKG-FE-004 | PKG-BE-D-04 |
| `schemas/SPARK_Packaging.graphqls` | `evaluateDieline` | `evaluateDieline` | `EVALUATE_DIELINE` | `PackagingEvaluationButton.tsx` | PKG-FE-003 | PKG-BE-D-02 |
| `schemas/SPARK_Packaging.graphqls` | `exportPackaging` | `exportPackaging` | `PACKAGING_EXCEL_EXPORT` | `WorkspaceDownloadDropdown.tsx` | PKG-FE-004 | PKG-BE-D-05 |
| `schemas/SPARK_Packaging.graphqls` | `getCountries` | `getCountries` | `GET_PACKAGING_COUNTRIES` | `usePackagingCountries.ts` | PKG-FE-002 | PKG-BE-B-06 |
| `schemas/SPARK_Packaging.graphqls` | `getDielineEvaluationStatuses` | `getDielineEvaluationStatuses` | `GET_DIELINE_STATUS_LIST` | `useFetchDielineStatusList.tsx` | PKG-FE-003 | PKG-BE-B-05 |
| `schemas/SPARK_Packaging.graphqls` | `getDielines` | `getDielines` | `GET_DIELINES` | `useFetchDielines.ts` | PKG-FE-003 | PKG-BE-B-03 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingComponentStatus` | `GET_PACKAGING_COMPONENT_STATUS` | `useComponentStatus.ts` | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingById` | `GET_PACKAGING_DETAIL` | — | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingById` | `GET_PACKAGING_DETAIL_WITH_INTERNAL_DATA` | `usePackagingDetail.tsx` | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingPacketInformation` | `GET_PACKAGING_PACKET_INFORMATION` | — | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingFieldValuesByType` | `getPackagingFieldValuesByType` | `GET_PACKAGING_FIELD_VALUES_BY_TYPE` | `usePackagingDetailsEnums.ts` | PKG-FE-002 | PKG-BE-B-04 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagings` | `GET_PACKAGING_DETAILS_BY_PARENTS` | — | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagings` | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `usePackagingDetailsByParent.tsx` | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagings` | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `usePackagingDetailsByParent.tsx` | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagingPacketsInformation` | `GET_PACKAGING_PACKETS_INFORMATION` | `BulkGeneratePackagingPacketModal.tsx` | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `lockPackaging` | `lockPackaging` | `LOCK_PACKAGING` | `PackagingDetailsTemplate.tsx` | PKG-FE-004 | PKG-BE-D-06 |
| `schemas/SPARK_Packaging.graphqls` | `unlockPackaging` | `unlockPackaging` | `UNLOCK_PACKAGING` | `PackagingDetailsTemplate.tsx` | PKG-FE-004 | PKG-BE-D-07 |
| `schemas/SPARK_Packaging.graphqls` | `updatePackaging` | `updatePackaging` | `UPDATE_PACKAGING_DETAIL` | `PackagingDetailsTemplate.tsx` | PKG-FE-005 | PKG-BE-E-01 |
| `schemas/SPARK_Packaging.graphqls` | `updatePackagingComponentStatus` | `updatePackagingComponentStatus` | `UPDATE_PACKAGING_COMPONENT_STATUS` | `PackagingDetailsTemplate.tsx` | PKG-FE-004 | PKG-BE-D-09 |

## Watchlist

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_Watchlist.graphqls` | `cloneFilesForWatchlist` | `cloneFilesForWatchlist` | `CLONE_WATCHLIST_ATTACHMENTS` | `WatchlistCloneTemplate.tsx` | WATCHLIST-FE-002 | WATCHLIST-BE-D-02 |
| `schemas/SPARK_Watchlist.graphqls` | `createWatchlistEntries` | `createWatchlistEntries` | `CREATE_WATCHLIST_ENTRIES` | — | WATCHLIST-FE-002 | WATCHLIST-BE-D-01 |
| `schemas/SPARK_Watchlist.graphqls` | `getWatchlistByFilter` | `getWatchlistForBulkUpdate` | `GET_WATCHLIST_FOR_BULK_UPDATE` | `WatchlistBulkUpdate.tsx` | WATCHLIST-FE-001 | WATCHLIST-BE-C-01 |
| `schemas/SPARK_Watchlist.graphqls` | `getWatchlistByIds` | `getWatchlistByIds` | `GET_WATCHLIST_BY_IDS` | `WatchlistCloneTemplate.tsx`<br>`WatchlistEditTemplate.tsx`<br>`WatchlistViewTemplate.tsx` | WATCHLIST-FE-001 | WATCHLIST-BE-B-01 |
| `schemas/SPARK_Watchlist.graphqls` | `updateWatchlistEntries` | `updateWatchlistEntries` | `UPDATE_WATCHLIST_ENTRIES` | `WatchlistBulkUpdate.tsx`<br>`WatchlistEditTemplate.tsx` | WATCHLIST-FE-003 | WATCHLIST-BE-E-01 |

## Impression

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_Impression.graphqls` | `searchImpressionsByProductId` | `getBomDataAndImpressions` | `GET_BOM_TEMPLATES_AND_IMPRESSIONS` | `ProductTemplateBomExpandedView.tsx` | IMPRESSION-FE-002 | IMPRESSION-BE-B-01 |
| `schemas/SPARK_Impression.graphqls` | `searchImpressionsByProductId` | `getCarryForwardFormData` | `GET_CARRY_FORWARD_FORM_DATA` | `ProductQueries.testHelper.tsx`<br>`ProductCarryForwardModal.tsx`<br>`WorkspaceCarryForwardSpecsForm.tsx` | IMPRESSION-FE-002 | IMPRESSION-BE-B-01 |

## Claims

| Backend schema | Resolver | Frontend operation | Client constant | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|---|
| `schemas/SPARK_Claims.graphqls` | `bulkUpdateClaim` | `bulkUpdateClaim` | `BULK_UPDATE_CLAIM` | `ClaimBulkUpdate.tsx` | CLAIM-FE-003 | CLAIM-BE-D-02 |
| `schemas/SPARK_Claims.graphqls` | `createClaim` | `createClaim` | `ADD_CLAIMS` | `ClaimNewTemplate.tsx`<br>`ProductTemplateClaimClone.tsx` | CLAIM-FE-003 | CLAIM-BE-D-01 |
| `schemas/SPARK_Claims.graphqls` | `getAllClaimsAbout` | `getClaims` | `GET_CLAIMS_AND_CHANNELS` | `ClaimNewTemplate.tsx`<br>`ImportProductDetailsSection.tsx` | CLAIM-FE-002 | CLAIM-BE-B-04 |
| `schemas/SPARK_Claims.graphqls` | `getAllClaimsAbout` | `getClaimByIds` | `GET_CLAIM_BY_ID` | — | CLAIM-FE-002 | CLAIM-BE-B-04 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `getClaimByIds` | `GET_CLAIM_BY_ID` | — | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `getClaimComponentStatus` | `GET_CLAIM_COMPONENT_STATUS` | `useComponentStatus.ts` | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `breadcrumbClaims` | `GET_CLAIM_CRUMB` | `BreadcrumbClaim.tsx` | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `getClaimByIds` | `GET_CLAIM_TEMPLATE_BY_ID` | `ProductTemplateClaimClone.tsx`<br>`ProductTemplateClaimEdit.tsx` | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaims` | `getClaims` | `GET_CLAIMS_AND_CHANNELS` | `ClaimNewTemplate.tsx`<br>`ImportProductDetailsSection.tsx` | CLAIM-FE-002 | CLAIM-BE-B-01 |
| `schemas/SPARK_Claims.graphqls` | `getClaims` | `getClaims` | `GET_PRODUCT_TEMPLATE_CLAIMS` | `ProductTemplateClaimExpandedView.tsx` | CLAIM-FE-002 | CLAIM-BE-B-01 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getClaims` | `GET_CLAIMS_AND_CHANNELS` | `ClaimNewTemplate.tsx`<br>`ImportProductDetailsSection.tsx` | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getClaimByIds` | `GET_CLAIM_BY_ID` | — | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getComponentVersion` | `GET_CLAIM_VERSION` | `useClaimQuery.ts` | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getCommunicationChannels` | `GET_COMMUNICATION_CHANNELLS` | — | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `lockClaim` | `lockClaim` | `LOCK_CLAIM` | `ClaimViewTemplate.tsx` | CLAIM-FE-003 | CLAIM-BE-D-04 |
| `schemas/SPARK_Claims.graphqls` | `requestClaimExport` | `requestClaimExport` | `REQUEST_REPORT` | — | CLAIM-FE-003 | CLAIM-BE-D-03 |
| `schemas/SPARK_Claims.graphqls` | `unlockClaim` | `unlockClaim` | `UNLOCK_CLAIM` | `ClaimViewTemplate.tsx` | CLAIM-FE-003 | CLAIM-BE-D-05 |
| `schemas/SPARK_Claims.graphqls` | `updateClaim` | `updateClaim` | `UPDATE_CLAIM` | `ClaimViewTemplate.tsx`<br>`ProductTemplateClaimEdit.tsx` | CLAIM-FE-004 | CLAIM-BE-E-01 |
