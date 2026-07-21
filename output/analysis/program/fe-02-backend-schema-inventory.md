# Backend GraphQL Schema Inventory — spark-internal-graphql (Phase-1 Domains)

> Source: `schemas/*.graphqls` (spark-internal-graphql) · Generated: 2026-07-21
> Scope: the 8 phase-1 domain schemas. Cross-referenced against the frontend client inventory (fe-01-client-inventory.md).

## Summary

| Stat | Count |
|---|---|
| Phase-1 schema files | 12 (of 74 total) |
| Object types (phase-1 files) | 128 |
| Input types (phase-1 files) | 101 |
| Interfaces (phase-1 files) | 2 |
| Enums (phase-1 files) | 0 |
| Unions (phase-1 files) | 0 |
| Custom scalars (gateway-wide) | 3 (Date, DateTime, JSON) |
| Phase-1 Query root fields | 68 |
| Phase-1 Mutation root fields | 70 |
| Phase-1 Query fields called by the frontend | 48 |
| Phase-1 Mutation fields called by the frontend | 52 |

## Deprecations (phase-1 schemas)

| Type | Field | Reason | Schema file |
|---|---|---|---|
| `SPARK_Dieline` | `attachments` | deprecated | `schemas/SPARK_Packaging.graphqls` |
| `SPARK_Measurements` | `humanId` | Use parentId | `schemas/SPARK_Measurement.graphqls` |
| `SPARK_Packaging` | `waveDescription` | deprecated | `schemas/SPARK_Packaging.graphqls` |
| `SPARK_PackagingFieldValues` | `resourceType` | deprecated | `schemas/SPARK_Packaging.graphqls` |
| `SPARK_PackagingInput` | `creativePath` | deprecated | `schemas/SPARK_Packaging.graphqls` |
| `SPARK_ProductRules` | `businessPartners` | use rule attribute | `schemas/SPARK_Product.graphqls` |
| `SPARK_ShippingDestination` | `phoneNumber` | Use fileDeliveryEmailList instead | `schemas/SPARK_Packaging.graphqls` |
| `SPARK_ShippingDestinationInput` | `phoneNumber` | Use fileDeliveryEmailList instead | `schemas/SPARK_Packaging.graphqls` |

## Phase-1 domain schemas

✅ = called by the frontend today · ⚠ = no frontend caller found (server-side or dead field)

### `schemas/SPARK_Product.graphqls` — Product · DGS target: `plm-product (host)`

- Object types (38): `CORONA_ItemDetails`, `DopplerDepartment`, `ProductComponentStatus`, `ProductVendorAttributes`, `SPARK_AncestryProducts`, `SPARK_AttachmentSummary`, `SPARK_AvailableRules`, `SPARK_CarryForwardProductAllStatus`, `SPARK_CarryForwardProductStatus`, `SPARK_ChildProducts`, `SPARK_CodeName`, `SPARK_MasterProductStatus`, `SPARK_PackagingAttribute`, `SPARK_PartnerReservedDpci`, `SPARK_PartnerTcins`, `SPARK_Product`, `SPARK_ProductBulkType`, `SPARK_ProductComponentsCounts`, `SPARK_ProductCopy`, `SPARK_ProductCopyResources`, `SPARK_ProductLibraryResource`, `SPARK_ProductMaterials`, `SPARK_ProductRules`, `SPARK_ProductStatus`, `SPARK_ProductTemplateAttachments`, `SPARK_ProductTemplateStatus`, `SPARK_ProductTemplatesList`, `SPARK_ProductWorkspaceAttributes`, `SPARK_ProductWorkspaceInfo`, `SPARK_ProductsCategories`, `SPARK_ProductsPaged`, `SPARK_PurchaseOrderDetails`, `SPARK_Rating`, `SPARK_ReservedDpci`, `SPARK_ResourcesCount`, `SPARK_Tcin`, `SPARK_WorkspaceInfoPartner`, `VMM_BusinessPartnerCategory`
- Input types (32): `Bulk_CarryForwardProductInput`, `BusinessPartnerInput`, `CarryForwardProductInput`, `DopplerDepartmentInput`, `ProductComponentStatusUpdateInput`, `SPARK_BombsWithMaterialInput`, `SPARK_ComponentIdsInput`, `SPARK_ComponentStatusInput`, `SPARK_CopyProductInput`, `SPARK_InitiatedByInput`, `SPARK_PackagingAttributeInput`, `SPARK_ProductInput`, `SPARK_ProductLibraryResourceInput`, `SPARK_ProductMaterialsInput`, `SPARK_ProductPartnerActionInput`, `SPARK_ProductPartnerInput`, `SPARK_ProductPartnerStatusInput`, `SPARK_ProductRuleCreateInput`, `SPARK_ProductRuleUpdateInput`, `SPARK_ProductTeamInput`, `SPARK_ProductTechPackCountInput`, `SPARK_ProductTemplateRemovedAttachments`, `SPARK_ProductUpdateInput`, `SPARK_ProductWorkspaceAttributesInput`, `SPARK_ProductWorkspaceInfoInput`, `SPARK_ToggleInput`, `SPARK_VendorAttributeInput`, `SPARK_WorkspaceInfoPartnerInput`, `Spark_bomMaterialDtosInput`, `WorkspaceStatusPairInput`, `WorkspaceTeamContextInput`, `WorkspaceTeamPair`
- Query fields: `getAllAvailableRules` ✅, `getCategories` ✅, `getCopyStatus` ⚠ unused-by-FE, `getProduct` ✅, `getProductBPRules` ✅, `getProductDeptRules` ✅, `getProductRules` ✅, `getProductRulesById` ✅, `getProductStatus` ✅, `getProductTechPackBulkCountV1` ✅, `getProductTechPackCountV1` ✅, `getProductTemplateById` ⚠ unused-by-FE, `getProductTemplates` ✅, `getProductVersions` ✅, `getProducts` ✅, `getProductsByIds` ✅, `getRatingByTcin` ⚠ unused-by-FE, `searchProductRules` ✅
- Mutation fields: `addBusinessPartnersToProductWithType` ✅, `addProduct` ✅, `addProductRule` ✅, `addProducts` ✅, `addTeamsToProduct` ✅, `bulkUpdateProducts` ✅, `carryForwardProduct` ✅, `deleteProductRule` ✅, `dropProductBusinessPartner` ⚠ unused-by-FE, `linkProduct` ✅, `productBusinessPartnerActions` ✅, `removeProductBusinessPartner` ⚠ unused-by-FE, `removeProductResources` ⚠ unused-by-FE, `unDropProductBusinessPartner` ⚠ unused-by-FE, `unlinkProduct` ✅, `updateBusinessPartnerStatuses` ✅, `updateComponentStatus` ✅, `updateComponentStatuses` ✅, `updateProduct` ✅, `updateProductRule` ✅, `updateProductTeamsWorkspaceContext` ✅, `updateViewToggle` ✅, `updateWorkspaceAttributes` ⚠ unused-by-FE

### `schemas/SPARK_Bom.graphqls` — BOM · DGS target: `plm-product (co-located)`

- Object types (29): `SPARK_Bom`, `SPARK_BomBaseImpressionDetails`, `SPARK_BomCombinationMaterial`, `SPARK_BomComboFabricSupplier`, `SPARK_BomComboSupplier`, `SPARK_BomFabricLibraryImpressionDetails`, `SPARK_BomFabricMaterial`, `SPARK_BomFabricSpecMaterial`, `SPARK_BomImpressionDetails_Unified`, `SPARK_BomMaterial`, `SPARK_BomMaterialSearch`, `SPARK_BomMaterialSearchResult`, `SPARK_BomMaterialType`, `SPARK_BomMaterial_Library_Unified`, `SPARK_BomMaterial_Unified`, `SPARK_BomPackagingMaterial`, `SPARK_BomPackagingSubstrate`, `SPARK_BomPaged`, `SPARK_BomSection`, `SPARK_BomSizeCaption`, `SPARK_BomTrimLibraryImpressionDetails`, `SPARK_BomTrimMaterial`, `SPARK_BomTrimZipperLibraryImpressionDetails`, `SPARK_BomWashLibraryImpressionDetails`, `SPARK_BomWashMaterial`, `SPARK_Bom_Type`, `SPARK_Bom_Unified`, `SPARK_LibraryMaterial`, `SPARK_TcinDpci`
- Input types (9): `SPARK_BomBaseTypeInput`, `SPARK_BomImpressionDetailsInput`, `SPARK_BomInput`, `SPARK_BomMaterialInput`, `SPARK_BomPartnerInput`, `SPARK_BomSectionInput`, `SPARK_MaterialLibraryInput`, `SPARK_TcinDpciInput`, `SPARK_UpdateBomInput`
- Interfaces: `SPARK_BomImpressionDetailsInterface`, `SPARK_BomMaterialInterface`
- Query fields: `getBomByIds` ✅, `getBomByParentId` ✅, `getBomDataV2` ⚠ unused-by-FE, `getBomElastic` ✅, `getBomMaterialTypes` ✅, `getBomPackagingMaterialTypes` ✅, `getBomPackagingSubstrates` ✅, `getBomPackagingUnitOfMeasure` ✅, `getBomStatus` ✅, `getComboSupplierForBom` ✅, `getValidRawMaterialSuppliersForBom` ✅, `getValidTrimSuppliersForBom` ✅, `searchMaterialsBom` ✅
- Mutation fields: `addBom` ✅, `lockBom` ✅, `manageBomWorkspaces` ⚠ unused-by-FE, `unlockBom` ✅, `updateBom` ✅, `updateBomComponentStatus` ✅

### `schemas/SPARK_Measurement.graphqls` — Measurement · DGS target: `plm-product (co-located)`

- Object types (9): `SPARK_MeasurementBaseType`, `SPARK_MeasurementRow`, `SPARK_MeasurementSetCoreSizes`, `SPARK_Measurements`, `SPARK_MeasurementsPaged`, `SPARK_PomSizes`, `SPARK_SampleMeasurementSet`, `SPARK_SampleMeasurementSetRow`, `SPARK_UnitsOfMeasure`
- Input types (9): `SPARK_MeasurementBaseTypeInput`, `SPARK_MeasurementSetCoreSizesInput`, `SPARK_MeasurementsInput`, `SPARK_MeasurementsUpdateInput`, `SPARK_PomSizesInput`, `SPARK_SampleMeasurementSetInput`, `SPARK_SampleMeasurementSetRowInput`, `SPARK_SystemTeamsWithType`, `Spark_MeasurementRowInput`
- Query fields: `getMeasurementByIds` ✅, `getMeasurementSetStatus` ✅, `getMeasurements` ✅, `getMeasurementsElastic` ✅, `getSampleMeasurement` ⚠ unused-by-FE, `getThicknessUnitsOfMeasure` ✅, `getUnitsOfMeasure` ✅
- Mutation fields: `addMeasurement` ⚠ unused-by-FE, `deleteSampleMeasurementSet` ✅, `lockMeasurementSet` ✅, `putSampleMeasurementSet` ✅, `unlockMeasurementSet` ✅, `updateMeasurement` ⚠ unused-by-FE, `updateMeasurementAccess` ⚠ unused-by-FE, `updateMeasurementComponentStatus` ⚠ unused-by-FE

### `schemas/SPARK_MeasurementTemplate.graphqls` — Measurement · DGS target: `plm-product (co-located)`

- Object types (3): `SPARK_MeasurementTemplate`, `SPARK_MeasurementTemplateRow`, `SPARK_MeasurementTemplatesPaged`
- Input types (2): `SPARK_MeasurementTemplateInput`, `SPARK_MeasurementTemplateRowInput`
- Query fields: `getMeasurementTemplates` ⚠ unused-by-FE, `getMeasurementTemplatesByIds` ⚠ unused-by-FE
- Mutation fields: `addMeasurementTemplate` ⚠ unused-by-FE, `deleteMeasurementTemplate` ⚠ unused-by-FE, `updateMeasurementTemplate` ⚠ unused-by-FE

### `schemas/SPARK_SizeTemplate.graphqls` — Measurement · DGS target: `plm-product (co-located)`

- Object types (8): `SPARK_CoreSizes`, `SPARK_GradeInfo`, `SPARK_RowTolerance`, `SPARK_SizeCodeDescription`, `SPARK_SizeGroup`, `SPARK_SizeTemplate`, `SPARK_SizeValues`, `SPARK_Unit_Of_Measure`
- Input types (8): `SPARK_GradeInput`, `SPARK_SizeCodeDescriptionInput`, `SPARK_SizeGroupsInput`, `SPARK_SizeTemplateCoreSizes`, `SPARK_SizeTemplateInput`, `SPARK_SizeTemplateToleranceInput`, `SPARK_SizeTemplateUpdateInput`, `SPARK_SizeValuesInput`
- Query fields: `getMaterialTypes` ⚠ unused-by-FE, `getSizeCategories` ⚠ unused-by-FE, `getSizeTemplates` ⚠ unused-by-FE
- Mutation fields: `addSizeTemplate` ⚠ unused-by-FE, `updateSizeTemplate` ⚠ unused-by-FE

### `schemas/SPARK_Sizes.graphqls` — Measurement · DGS target: `plm-product (co-located)`

- Object types (1): `SPARK_Sizes`
- Query fields: `searchSparkSizes` ⚠ unused-by-FE

### `schemas/SPARK_TightFit.graphqls` — Measurement · DGS target: `plm-product (co-located)`

- Object types (2): `SPARK_TightFit`, `SPARK_TightFitsResponse`
- Input types (1): `SPARK_TightFitInput`
- Query fields: `getTightFitByIdAndVersion` ⚠ unused-by-FE, `getTightFits` ✅
- Mutation fields: `addTightFit` ✅, `updateTightFit` ✅

### `schemas/SPARK_ProductDetail.graphqls` — Product Details · DGS target: `plm-product (co-located)`

- Object types (4): `SPARK_ProductDetails`, `SPARK_ProductDetailsCategoryWithSection`, `SPARK_ProductDetailsItem`, `SPARK_ProductDetailsPaged`
- Input types (8): `PDTLAttachmentCloneRef`, `SPARK_CodeDescriptionInput`, `SPARK_ProductDetailPartnerInput`, `SPARK_ProductDetailsItemInput`, `SPARK_ProductDetailsManageAccessRequest`, `SPARK_ProductDetailsManagePermissionInput`, `productDetailSetInput`, `productDetailSetUpdateInput`
- Query fields: `getProductDetailsById` ✅, `getProductDetailsElastic` ⚠ unused-by-FE
- Mutation fields: `cloneFilesForProductDetails` ✅, `createProductDetailsSet` ✅, `productDetailLockUnlock` ✅, `updateProductDetailAccess` ⚠ unused-by-FE, `updateProductDetailComponentStatus` ✅, `updateProductDetailsSet` ✅

### `schemas/SPARK_Packaging.graphqls` — Packaging · DGS target: `plm-product (co-located)`

- Object types (18): `SPARK_ContactInformation`, `SPARK_Dieline`, `SPARK_DielineReservedDpci`, `SPARK_Dieline_Round`, `SPARK_Packaging`, `SPARK_PackagingBulk`, `SPARK_PackagingElement`, `SPARK_PackagingFieldValues`, `SPARK_PackagingInternalData`, `SPARK_PackagingPaged`, `SPARK_PackagingPagedForStatus`, `SPARK_PrinterDieline`, `SPARK_PrintingProcess`, `SPARK_PrintingProcessSubstrate`, `SPARK_ShippingDestination`, `SPARK_Softproofing`, `SPARK_SuggestedRetailPriceByDPCI`, `SPARK_WarningsAndCautions`
- Input types (20): `DielineAttachmentCloneRef`, `SPARK_ContactInformationInput`, `SPARK_DielineEvaluationInput`, `SPARK_DielineInput`, `SPARK_DielineReservedDpciInput`, `SPARK_PackagingAttachment`, `SPARK_PackagingBulkInput`, `SPARK_PackagingClaimCopyInput`, `SPARK_PackagingClaimInput`, `SPARK_PackagingElementInput`, `SPARK_PackagingInput`, `SPARK_PackagingInternalDataInput`, `SPARK_PackagingLibrary_Input`, `SPARK_PackagingPartnerInput`, `SPARK_PrinterDielineInput`, `SPARK_PrintingProcessInput`, `SPARK_PrintingProcessSubstrateInput`, `SPARK_ShippingDestinationInput`, `SPARK_SoftproofingInput`, `SPARK_WarningsAndCautionsInput`
- Query fields: `getCountries` ✅, `getDielineEvaluationStatuses` ✅, `getDielines` ✅, `getPackagingById` ✅, `getPackagingElastic` ⚠ unused-by-FE, `getPackagingFieldValuesByType` ✅, `getPackagings` ✅
- Mutation fields: `addPackaging` ✅, `bulkAddPackagings` ✅, `bulkUpdatePackagings` ✅, `cloneFilesForDielines` ⚠ unused-by-FE, `evaluateDieline` ✅, `exportPackaging` ✅, `lockPackaging` ✅, `unlockPackaging` ✅, `updatePackaging` ✅, `updatePackagingComponentStatus` ✅

### `schemas/SPARK_Watchlist.graphqls` — Watchlist · DGS target: `plm-product (co-located)`

- Object types (4): `SPARK_Watchlist`, `SPARK_WatchlistInspection`, `SPARK_WatchlistInspectionAction`, `SPARK_WatchlistPartner`
- Input types (4): `SPARK_WatchlistInput`, `SPARK_WatchlistInspectionInput`, `SPARK_WatchlistPartnerInput`, `WatchlistAttachmentCloneRef`
- Query fields: `getWatchlistByFilter` ✅, `getWatchlistByIds` ✅, `getWatchlistInspectionActions` ⚠ unused-by-FE, `getWatchlistReasons` ⚠ unused-by-FE
- Mutation fields: `cloneFilesForWatchlist` ✅, `createWatchlistEntries` ✅, `updateWatchlistEntries` ✅

### `schemas/SPARK_Impression.graphqls` — Impression · DGS target: `plm-product (co-located)`

- Object types (2): `SPARK_Impression`, `SPARK_ImpressionCount`
- Input types (2): `SPARK_ImpressionInput`, `SPARK_ProductImpressionInput`
- Query fields: `getImpressionCountsByProductId` ⚠ unused-by-FE, `searchImpressionsByProductId` ✅
- Mutation fields: `updateImpressions` ⚠ unused-by-FE

### `schemas/SPARK_Claims.graphqls` — Claims · DGS target: `spark-claims (separate)`

- Object types (8): `SPARK_ClaimDetails`, `SPARK_ClaimExport`, `SPARK_ClaimPackagingCopy`, `SPARK_ClaimSubstantiate`, `SPARK_Claims`, `SPARK_CommunicationChannel`, `SPARK_Guest_Facing`, `SPARK_ParentDetails`
- Input types (6): `SPARK_BulkClaimsUpdateInput`, `SPARK_ClaimDetailsInput`, `SPARK_ClaimSubstantiateInput`, `SPARK_ClaimsInput`, `SPARK_ClaimsUpdateInput`, `SPARK_PartnerDetails`
- Query fields: `getAllClaimsAbout` ✅, `getClaimByIds` ✅, `getClaimExports` ⚠ unused-by-FE, `getClaims` ✅, `getClaimsElastic` ⚠ unused-by-FE, `getCommunicationChannels` ✅, `searchGuestFacing` ⚠ unused-by-FE
- Mutation fields: `bulkUpdateClaim` ✅, `createClaim` ✅, `lockClaim` ✅, `requestClaimExport` ✅, `unlockClaim` ✅, `updateClaim` ✅

## Out of scope

- The remaining 62 schema files (later-phase and platform-stitched domains) are excluded per program scope.
