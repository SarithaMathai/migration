# Traceability Matrix — Domain → Schema → Resolver → Client → Impact → Stories

> Generated: 2026-07-16 · One row per phase-1 frontend operation × backend root field.
> Chain: Business Domain → Backend Schema → Resolver → Frontend Query → Client Component → FE story → BE story.

## Product

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_Product.graphqls` | `addBusinessPartnersToProductWithType` | `addBusinessPartnersToProductWithType` | — | PRODUCT-FE-008 | PRODUCT-BE-D-07 |
| `schemas/SPARK_Product.graphqls` | `addProduct` | `addProduct` | `ProductNew.tsx`<br>`ProductTemplateNew.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-01 |
| `schemas/SPARK_Product.graphqls` | `addProductRule` | `addProductRule` | — | PRODUCT-FE-006 | PRODUCT-BE-D-15 |
| `schemas/SPARK_Product.graphqls` | `addProducts` | `addProducts` | `ProductBulkCreate.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-02 |
| `schemas/SPARK_Product.graphqls` | `addTeamsToProduct` | `addTeams` | `BPSelector.tsx` | PRODUCT-FE-008 | PRODUCT-BE-D-06 |
| `schemas/SPARK_Product.graphqls` | `bulkUpdateProducts` | `bulkUpdateProducts` | `ProductBulkUpdate.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-03 |
| `schemas/SPARK_Product.graphqls` | `carryForwardProduct` | `carryForwardProduct` | `ProductCarryForwardModal.tsx`<br>`WorkspacePlanGrid.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-05 |
| `schemas/SPARK_Product.graphqls` | `deleteProductRule` | `deleteProductRule` | — | PRODUCT-FE-006 | PRODUCT-BE-D-17 |
| `schemas/SPARK_Product.graphqls` | `getAllAvailableRules` | `getAllAvailableRules` | — | PRODUCT-FE-006 | PRODUCT-BE-B-09 |
| `schemas/SPARK_Product.graphqls` | `getCategories` | `getCategories` | `ProductTemplateSideFilterForm.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-03 |
| `schemas/SPARK_Product.graphqls` | `getCategories` | `getCategories` | `ProductListSideFilterForm.tsx`<br>`UserListSideFilterForm.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-03 |
| `schemas/SPARK_Product.graphqls` | `getCategories` | `getCategories` | `ProductListSideFilterForm.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-03 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getCarryForwardFormData` | `ProductQueries.testHelper.tsx`<br>`ProductCarryForwardModal.tsx`<br>`WorkspaceCarryForwardSpecsForm.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `ImportProductDetailsModal.tsx`<br>`ProductEdit.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWorkspaces` | `ReleaseProductPacket.tsx`<br>`WatchlistForm.tsx`<br>`WatchlistViewTemplate.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWorkspaces` | `ReleaseTechPackModal.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductById` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductComponentStatusCounts` | `BomViewTemplate.tsx`<br>`ProductFilesQueries.testHelper.tsx`<br>`SpecsContainer.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `breadcrumbProduct` | `BreadcrumbProduct.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductStatusUpdateInfo` | `ProductQueries.testHelper.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getTeams` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getTeams` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWithAttachmentsAndComponents` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductWithTeams` | `BPSelector.tsx`<br>`Teams.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `ImportProductDetailsSection.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `ImportProductDetailsSection.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProductScaffolding` | — | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `ProductsListItem.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getProduct` | `ProductsListItem.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProduct` | `getDpciInfo` | `useDpciInformation.tsx` | PRODUCT-FE-011 | PRODUCT-BE-B-01 |
| `schemas/SPARK_Product.graphqls` | `getProductBPRules` | `getProductBPRules` | — | PRODUCT-FE-006 | PRODUCT-BE-B-11 |
| `schemas/SPARK_Product.graphqls` | `getProductDeptRules` | `getProductDeptRules` | — | PRODUCT-FE-006 | PRODUCT-BE-B-10 |
| `schemas/SPARK_Product.graphqls` | `getProductRules` | `getProductRules` | — | PRODUCT-FE-006 | PRODUCT-BE-B-07 |
| `schemas/SPARK_Product.graphqls` | `getProductRulesById` | `getProductRule` | — | PRODUCT-FE-006 | PRODUCT-BE-B-08 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getFormData` | `ProductBulkUpdate.tsx` | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getProductStatusUpdateInfo` | `ProductQueries.testHelper.tsx` | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getStatus` | — | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductStatus` | `getProductWorkspaceMetricsReportCount` | `WorkspaceOverview.tsx` | PRODUCT-FE-004 | PRODUCT-BE-B-03 |
| `schemas/SPARK_Product.graphqls` | `getProductTechPackBulkCountV1` | `getTechPackBulkCount` | `BulkGenerateProductPacketModal.tsx`<br>`BulkGenerateReleasePacketModal.tsx` | PRODUCT-FE-010 | PRODUCT-BE-E-04 |
| `schemas/SPARK_Product.graphqls` | `getProductTechPackCountV1` | `getTechPackCountV1` | `GenerateTechPackModal.tsx`<br>`ReleaseTechPackModal.tsx` | PRODUCT-FE-010 | PRODUCT-BE-E-03 |
| `schemas/SPARK_Product.graphqls` | `getProductTemplates` | `getProductTemplates` | `ProductTemplateQueries.testHelper.tsx`<br>`TemplateLibraryContainer.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-02 |
| `schemas/SPARK_Product.graphqls` | `getProductTemplates` | `getProductTemplates` | `ClaimBulkUpdate.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-02 |
| `schemas/SPARK_Product.graphqls` | `getProductTemplates` | `getProductTemplates` | `ProductTemplatePDTLExpandedView.tsx`<br>`ProductTemplateEdit.tsx`<br>`ProductTemplateOverviewContainer.tsx` | PRODUCT-FE-005 | PRODUCT-BE-C-02 |
| `schemas/SPARK_Product.graphqls` | `getProductVersions` | `getProductVersions` | — | PRODUCT-FE-002 | PRODUCT-BE-B-04 |
| `schemas/SPARK_Product.graphqls` | `getProducts` | `getProducts` | — | PRODUCT-FE-003 | PRODUCT-BE-S-02 |
| `schemas/SPARK_Product.graphqls` | `getProducts` | `getProducts` | `SampleCompare.tsx` | PRODUCT-FE-003 | PRODUCT-BE-S-02 |
| `schemas/SPARK_Product.graphqls` | `getProducts` | `getProducts` | `PIDOrWRKIDSelectAutoComplete.tsx` | PRODUCT-FE-003 | PRODUCT-BE-S-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getBulkDiscussionData` | `DiscussionBulkCreate.tsx` | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getFilesWithMetaData` | — | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getFormData` | `ProductBulkUpdate.tsx` | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `getProductsByIds` | `getTeamsProductAndWorkspace` | `ProductQueries.testHelper.tsx`<br>`ReplaceWorkspaceFieldset.tsx` | PRODUCT-FE-003 | PRODUCT-BE-B-02 |
| `schemas/SPARK_Product.graphqls` | `linkProduct` | `linkProduct` | `ProductActionsDropDown.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-13 |
| `schemas/SPARK_Product.graphqls` | `productBusinessPartnerActions` | `productBusinessPartnerActions` | `Teams.tsx` | PRODUCT-FE-009 | PRODUCT-BE-S-03 |
| `schemas/SPARK_Product.graphqls` | `searchProductRules` | `searchProductRules` | `useSearchProductRules.tsx` | PRODUCT-FE-006 | PRODUCT-BE-C-05 |
| `schemas/SPARK_Product.graphqls` | `unlinkProduct` | `unlinkProduct` | `Links.tsx`<br>`ProductLinkRailListItem.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-14 |
| `schemas/SPARK_Product.graphqls` | `updateBusinessPartnerStatuses` | `updateBusinessPartnerStatuses` | `BPSelector.tsx`<br>`ProductsGridItem.tsx`<br>`ProductsListItemHeader.tsx` | PRODUCT-FE-009 | PRODUCT-BE-D-09 |
| `schemas/SPARK_Product.graphqls` | `updateComponentStatus` | `updateComponentStatus` | `ComponentStatusDropdown.tsx` | PRODUCT-FE-011 | PRODUCT-BE-D-18 |
| `schemas/SPARK_Product.graphqls` | `updateComponentStatuses` | `updateComponentStatuses` | `ProductComponentSetStatusesDropdown.tsx` | PRODUCT-FE-011 | PRODUCT-BE-E-02 |
| `schemas/SPARK_Product.graphqls` | `updateProduct` | `updateProduct` | — | PRODUCT-FE-007 | PRODUCT-BE-D-04 |
| `schemas/SPARK_Product.graphqls` | `updateProduct` | `updateProduct` | — | PRODUCT-FE-007 | PRODUCT-BE-D-04 |
| `schemas/SPARK_Product.graphqls` | `updateProduct` | `updateProduct` | `ProductTemplateEdit.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-04 |
| `schemas/SPARK_Product.graphqls` | `updateProductRule` | `updateProductRule` | — | PRODUCT-FE-006 | PRODUCT-BE-D-16 |
| `schemas/SPARK_Product.graphqls` | `updateProductTeamsWorkspaceContext` | `updateProductTeamsWorkspaceContext` | `ManageTeamWorkspacesModal.tsx` | PRODUCT-FE-008 | PRODUCT-BE-D-12 |
| `schemas/SPARK_Product.graphqls` | `updateViewToggle` | `updateViewToggle` | `ToggleViewFilter.tsx` | PRODUCT-FE-007 | PRODUCT-BE-D-10 |

## BOM

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_Bom.graphqls` | `addBom` | `addBom` | `BomCloneTemplate.tsx`<br>`BomCreateTemplate.tsx` | BOM-FE-006 | BOM-BE-D-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomByIds` | `BomCloneTemplate.tsx`<br>`useBomsByIds.ts` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomByIds` | `BomViewTemplate.tsx` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomByIds` | — | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomComponentStatus` | `useComponentStatus.ts` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByIds` | `getBomDataAndImpressions` | `ProductTemplateBomExpandedView.tsx` | BOM-FE-002 | BOM-BE-B-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomByParentId` | `getBomByParentId` | `useBomsByParentId.ts` | BOM-FE-002 | BOM-BE-B-04 |
| `schemas/SPARK_Bom.graphqls` | `getBomElastic` | `getBomElastic` | `useBomsByParentIdsFromES.ts` | BOM-FE-003 | BOM-BE-C-01 |
| `schemas/SPARK_Bom.graphqls` | `getBomMaterialTypes` | `getBomMaterialTypes` | `useBomMaterialTypes.ts` | BOM-FE-004 | BOM-BE-B-05 |
| `schemas/SPARK_Bom.graphqls` | `getBomPackagingMaterialTypes` | `getBomPackagingMasterData` | `useBomMaterialTypes.ts` | BOM-FE-004 | BOM-BE-B-06 |
| `schemas/SPARK_Bom.graphqls` | `getBomPackagingSubstrates` | `getBomPackagingSubstrates` | — | BOM-FE-004 | BOM-BE-B-07 |
| `schemas/SPARK_Bom.graphqls` | `getBomPackagingUnitOfMeasure` | `getBomPackagingMasterData` | `useBomMaterialTypes.ts` | BOM-FE-004 | BOM-BE-B-08 |
| `schemas/SPARK_Bom.graphqls` | `getBomStatus` | `getBomStatus` | — | BOM-FE-002 | BOM-BE-B-03 |
| `schemas/SPARK_Bom.graphqls` | `getComboSupplierForBom` | `getComboSupplierForBom` | — | BOM-FE-005 | BOM-BE-C-03 |
| `schemas/SPARK_Bom.graphqls` | `getValidRawMaterialSuppliersForBom` | `getValidSuppliersForBom` | `BomForm.tsx`<br>`PackagingBomForm.tsx` | BOM-FE-005 | BOM-BE-C-05 |
| `schemas/SPARK_Bom.graphqls` | `getValidTrimSuppliersForBom` | `getValidSuppliersForBom` | `BomForm.tsx`<br>`PackagingBomForm.tsx` | BOM-FE-005 | BOM-BE-C-04 |
| `schemas/SPARK_Bom.graphqls` | `lockBom` | `lockBom` | `BomViewHeader.tsx` | BOM-FE-006 | BOM-BE-D-03 |
| `schemas/SPARK_Bom.graphqls` | `searchMaterialsBom` | `searchMaterialsBom` | — | BOM-FE-003 | BOM-BE-S-03 |
| `schemas/SPARK_Bom.graphqls` | `unlockBom` | `unlockBom` | `BomViewHeader.tsx` | BOM-FE-006 | BOM-BE-D-04 |
| `schemas/SPARK_Bom.graphqls` | `updateBom` | `updateBom` | `BomViewTemplate.tsx` | BOM-FE-006 | BOM-BE-S-01 |
| `schemas/SPARK_Bom.graphqls` | `updateBomComponentStatus` | `updateBomComponentStatus` | `BomViewTemplate.tsx` | BOM-FE-006 | BOM-BE-D-05 |

## Measurement

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_Measurement.graphqls` | `deleteSampleMeasurementSet` | `deleteSampleMeasurementSet` | `SampleCompare.tsx`<br>`Sample.tsx` | MST-FE-004 | MST-BE-D-07 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementByIds` | `getMeasurementByIds` | — | MST-FE-001 | MST-BE-B-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementByIds` | `getMeasurementComponentStatus` | `useComponentStatus.ts` | MST-FE-001 | MST-BE-B-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementByIds` | `getMeasurementByIds` | — | MST-FE-001 | MST-BE-B-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementSetStatus` | `getMeasurementSetStatus` | `TightFitTemplateEditLayout.tsx` | MST-FE-001 | MST-BE-B-04 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurements` | `getMeasurements` | `ImportMeasurementSet.tsx` | MST-FE-002 | MST-BE-C-01 |
| `schemas/SPARK_Measurement.graphqls` | `getMeasurementsElastic` | `getMeasurementsElastic` | — | MST-FE-002 | MST-BE-C-02 |
| `schemas/SPARK_Measurement.graphqls` | `getThicknessUnitsOfMeasure` | `getMeasurementsMetaData` | — | MST-FE-003 | MST-BE-B-03 |
| `schemas/SPARK_Measurement.graphqls` | `getUnitsOfMeasure` | `getMeasurementsMetaData` | — | MST-FE-003 | MST-BE-B-02 |
| `schemas/SPARK_Measurement.graphqls` | `getUnitsOfMeasure` | `getUnitsOfMeasure` | — | MST-FE-003 | MST-BE-B-02 |
| `schemas/SPARK_Measurement.graphqls` | `lockMeasurementSet` | `lockMeasurementSet` | `MeasurementSetTemplate.tsx` | MST-FE-004 | MST-BE-D-03 |
| `schemas/SPARK_Measurement.graphqls` | `putSampleMeasurementSet` | `putSampleMeasurementSet` | `SampleCompare.tsx`<br>`SampleNew.tsx`<br>`Sample.tsx`<br>`SampleMeasurementEditTemplate.tsx` | MST-FE-004 | MST-BE-D-06 |
| `schemas/SPARK_Measurement.graphqls` | `unlockMeasurementSet` | `unlockMeasurementSet` | `MeasurementSetTemplate.tsx` | MST-FE-004 | MST-BE-D-04 |

## Product Details

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_ProductDetail.graphqls` | `cloneFilesForProductDetails` | `cloneFilesForProductDetails` | `ProductDetailClone.tsx` | PDTL-FE-002 | PDTL-BE-D-04 |
| `schemas/SPARK_ProductDetail.graphqls` | `createProductDetailsSet` | `createProductDetailsSet` | `ProductDetailsSetNew.tsx`<br>`ProductDetailClone.tsx` | PDTL-FE-002 | PDTL-BE-D-01 |
| `schemas/SPARK_ProductDetail.graphqls` | `getProductDetailsById` | `getProductDetailsById` | — | PDTL-FE-001 | PDTL-BE-B-01 |
| `schemas/SPARK_ProductDetail.graphqls` | `getProductDetailsById` | `getProductDetailComponentStatus` | `useComponentStatus.ts` | PDTL-FE-001 | PDTL-BE-B-01 |
| `schemas/SPARK_ProductDetail.graphqls` | `productDetailLockUnlock` | `productDetailLockUnlock` | `ProductDetailsViewTemplate.tsx` | PDTL-FE-002 | PDTL-BE-D-03 |
| `schemas/SPARK_ProductDetail.graphqls` | `updateProductDetailComponentStatus` | `updateProductDetailComponentStatus` | `ProductDetailsViewTemplate.tsx` | PDTL-FE-002 | PDTL-BE-D-05 |
| `schemas/SPARK_ProductDetail.graphqls` | `updateProductDetailsSet` | `updateProductDetailsSet` | `ProductDetailsViewTemplate.tsx`<br>`ProductTemplateProductDetailsEdit.tsx` | PDTL-FE-003 | PDTL-BE-E-01 |

## Packaging

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_Packaging.graphqls` | `addPackaging` | `addPackaging` | `PackagingDetailsCloneTemplate.tsx`<br>`PackagingDetailsNewTemplate.tsx` | PKG-FE-004 | PKG-BE-D-01 |
| `schemas/SPARK_Packaging.graphqls` | `bulkAddPackagings` | `bulkAddPackagings` | `PackagingBulkCreate.tsx` | PKG-FE-004 | PKG-BE-D-03 |
| `schemas/SPARK_Packaging.graphqls` | `bulkUpdatePackagings` | `bulkUpdatePackagings` | `PackagingBulkUpdate.tsx` | PKG-FE-004 | PKG-BE-D-04 |
| `schemas/SPARK_Packaging.graphqls` | `evaluateDieline` | `evaluateDieline` | `PackagingEvaluationButton.tsx` | PKG-FE-003 | PKG-BE-D-02 |
| `schemas/SPARK_Packaging.graphqls` | `exportPackaging` | `exportPackaging` | `WorkspaceDownloadDropdown.tsx` | PKG-FE-004 | PKG-BE-D-05 |
| `schemas/SPARK_Packaging.graphqls` | `getCountries` | `getCountries` | `usePackagingCountries.ts` | PKG-FE-002 | PKG-BE-B-06 |
| `schemas/SPARK_Packaging.graphqls` | `getDielineEvaluationStatuses` | `getDielineEvaluationStatuses` | `useFetchDielineStatusList.tsx` | PKG-FE-003 | PKG-BE-B-05 |
| `schemas/SPARK_Packaging.graphqls` | `getDielines` | `getDielines` | `useFetchDielines.ts` | PKG-FE-003 | PKG-BE-B-03 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingComponentStatus` | `useComponentStatus.ts` | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingById` | — | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingById` | `usePackagingDetail.tsx` | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingById` | `getPackagingPacketInformation` | — | PKG-FE-001 | PKG-BE-B-02 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagingFieldValuesByType` | `getPackagingFieldValuesByType` | `usePackagingDetailsEnums.ts` | PKG-FE-002 | PKG-BE-B-04 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagings` | — | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagings` | `usePackagingDetailsByParent.tsx` | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagings` | `usePackagingDetailsByParent.tsx` | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `getPackagings` | `getPackagingPacketsInformation` | `BulkGeneratePackagingPacketModal.tsx` | PKG-FE-001 | PKG-BE-B-01 |
| `schemas/SPARK_Packaging.graphqls` | `lockPackaging` | `lockPackaging` | `PackagingDetailsTemplate.tsx` | PKG-FE-004 | PKG-BE-D-06 |
| `schemas/SPARK_Packaging.graphqls` | `unlockPackaging` | `unlockPackaging` | `PackagingDetailsTemplate.tsx` | PKG-FE-004 | PKG-BE-D-07 |
| `schemas/SPARK_Packaging.graphqls` | `updatePackaging` | `updatePackaging` | `PackagingDetailsTemplate.tsx` | PKG-FE-005 | PKG-BE-E-01 |
| `schemas/SPARK_Packaging.graphqls` | `updatePackagingComponentStatus` | `updatePackagingComponentStatus` | `PackagingDetailsTemplate.tsx` | PKG-FE-004 | PKG-BE-D-09 |

## Watchlist

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_Watchlist.graphqls` | `cloneFilesForWatchlist` | `cloneFilesForWatchlist` | `WatchlistCloneTemplate.tsx` | WATCHLIST-FE-002 | WATCHLIST-BE-D-02 |
| `schemas/SPARK_Watchlist.graphqls` | `createWatchlistEntries` | `createWatchlistEntries` | — | WATCHLIST-FE-002 | WATCHLIST-BE-D-01 |
| `schemas/SPARK_Watchlist.graphqls` | `getWatchlistByFilter` | `getWatchlistForBulkUpdate` | `WatchlistBulkUpdate.tsx` | WATCHLIST-FE-001 | WATCHLIST-BE-C-01 |
| `schemas/SPARK_Watchlist.graphqls` | `getWatchlistByIds` | `getWatchlistByIds` | `WatchlistCloneTemplate.tsx`<br>`WatchlistEditTemplate.tsx`<br>`WatchlistViewTemplate.tsx` | WATCHLIST-FE-001 | WATCHLIST-BE-B-01 |
| `schemas/SPARK_Watchlist.graphqls` | `updateWatchlistEntries` | `updateWatchlistEntries` | `WatchlistBulkUpdate.tsx`<br>`WatchlistEditTemplate.tsx` | WATCHLIST-FE-003 | WATCHLIST-BE-E-01 |

## Impression

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_Impression.graphqls` | `searchImpressionsByProductId` | `getBomDataAndImpressions` | `ProductTemplateBomExpandedView.tsx` | IMPRESSION-FE-002 | IMPRESSION-BE-B-01 |
| `schemas/SPARK_Impression.graphqls` | `searchImpressionsByProductId` | `getCarryForwardFormData` | `ProductQueries.testHelper.tsx`<br>`ProductCarryForwardModal.tsx`<br>`WorkspaceCarryForwardSpecsForm.tsx` | IMPRESSION-FE-002 | IMPRESSION-BE-B-01 |

## Claims

| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |
|---|---|---|---|---|---|
| `schemas/SPARK_Claims.graphqls` | `bulkUpdateClaim` | `bulkUpdateClaim` | `ClaimBulkUpdate.tsx` | CLAIM-FE-003 | CLAIM-BE-D-02 |
| `schemas/SPARK_Claims.graphqls` | `createClaim` | `createClaim` | `ClaimNewTemplate.tsx`<br>`ProductTemplateClaimClone.tsx` | CLAIM-FE-003 | CLAIM-BE-D-01 |
| `schemas/SPARK_Claims.graphqls` | `getAllClaimsAbout` | `getClaims` | `ClaimNewTemplate.tsx`<br>`ImportProductDetailsSection.tsx` | CLAIM-FE-002 | CLAIM-BE-B-04 |
| `schemas/SPARK_Claims.graphqls` | `getAllClaimsAbout` | `getClaimByIds` | — | CLAIM-FE-002 | CLAIM-BE-B-04 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `getClaimByIds` | — | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `getClaimComponentStatus` | `useComponentStatus.ts` | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `breadcrumbClaims` | `BreadcrumbClaim.tsx` | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaimByIds` | `getClaimByIds` | `ProductTemplateClaimClone.tsx`<br>`ProductTemplateClaimEdit.tsx` | CLAIM-FE-002 | CLAIM-BE-B-02 |
| `schemas/SPARK_Claims.graphqls` | `getClaims` | `getClaims` | `ClaimNewTemplate.tsx`<br>`ImportProductDetailsSection.tsx` | CLAIM-FE-002 | CLAIM-BE-B-01 |
| `schemas/SPARK_Claims.graphqls` | `getClaims` | `getClaims` | `ProductTemplateClaimExpandedView.tsx` | CLAIM-FE-002 | CLAIM-BE-B-01 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getClaims` | `ClaimNewTemplate.tsx`<br>`ImportProductDetailsSection.tsx` | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getClaimByIds` | — | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getComponentVersion` | `useClaimQuery.ts` | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `getCommunicationChannels` | `getCommunicationChannels` | — | CLAIM-FE-002 | CLAIM-BE-B-03 |
| `schemas/SPARK_Claims.graphqls` | `lockClaim` | `lockClaim` | `ClaimViewTemplate.tsx` | CLAIM-FE-003 | CLAIM-BE-D-04 |
| `schemas/SPARK_Claims.graphqls` | `requestClaimExport` | `requestClaimExport` | — | CLAIM-FE-003 | CLAIM-BE-D-03 |
| `schemas/SPARK_Claims.graphqls` | `unlockClaim` | `unlockClaim` | `ClaimViewTemplate.tsx` | CLAIM-FE-003 | CLAIM-BE-D-05 |
| `schemas/SPARK_Claims.graphqls` | `updateClaim` | `updateClaim` | `ClaimViewTemplate.tsx`<br>`ProductTemplateClaimEdit.tsx` | CLAIM-FE-004 | CLAIM-BE-E-01 |
