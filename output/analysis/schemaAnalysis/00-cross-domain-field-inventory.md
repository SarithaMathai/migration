# Schema Analysis — Cross-Domain Field Inventory (Program Roll-Up)

> **Scope:** 8 phase-1 domains · **Generated:** 2026-07-21 · **Pipeline Version:** 1.0
> Aggregates each domain's `be-06-cross-domain-field-analysis.md`. Regenerate via `python fedMigrationScripts/generatescripts/generate_schema_analysis.py`.

## Program Totals

| Metric | Value |
|---|---|
| Total resolvers scanned | 359 |
| Cross-domain/EXT dependent resolvers | 128 |
| Cross-domain fields with no client usage found | 107 |

## By Domain

| Domain | Resolvers | Cross-domain | 🔴 Very High | 🟠 High | 🟡 Medium | 🟢 Low | Unused (no client match) |
|---|---|---|---|---|---|---|---|
| [Product](../product/be-06-cross-domain-field-analysis.md) | 105 | 45 | 2 | 2 | 4 | 37 | 37 |
| [BOM](../bom/be-06-cross-domain-field-analysis.md) | 92 | 19 | 0 | 0 | 1 | 18 | 15 |
| [Measurement](../measurement/be-06-cross-domain-field-analysis.md) | 56 | 19 | 0 | 0 | 0 | 19 | 17 |
| [Product Details](../productDetails/be-06-cross-domain-field-analysis.md) | 20 | 10 | 0 | 0 | 0 | 10 | 8 |
| [Packaging](../packaging/be-06-cross-domain-field-analysis.md) | 35 | 12 | 0 | 0 | 0 | 12 | 11 |
| [Watchlist](../watchlist/be-06-cross-domain-field-analysis.md) | 15 | 10 | 0 | 0 | 2 | 8 | 6 |
| [Impression](../impression/be-06-cross-domain-field-analysis.md) | 9 | 3 | 0 | 0 | 0 | 3 | 3 |
| [Claims](../claims/be-06-cross-domain-field-analysis.md) | 27 | 10 | 0 | 0 | 0 | 10 | 10 |
| **TOTAL** | **359** | **128** | **2** | **2** | **7** | **117** | **107** |

## Unused Cross-Domain Fields (candidates for deferral)

Fields that hydrate from another domain but were not matched to any operation in `ClientCallingGqlQueries/` — candidates to defer or drop rather than build federation for.

### Product

| Resolver | Requires | Complexity |
|---|---|---|
| `DopplerDepartment.clazzes` | `ig` (Item Groups (IG)) | Low |
| `DopplerDepartment.department` | `ig` (Item Groups (IG)) | Low |
| `DopplerDepartment.division` | `ig` (Item Groups (IG)) | Low |
| `DopplerDepartment.primaryCapacityTypeName` | `doppler` (External platforms) | Low |
| `DopplerDepartment.secondaryCapacityTypeName` | `doppler` (External platforms) | Low |
| `ProductComponentStatus.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_PackagingAttribute.spg` | `fileLibrary` (FileLibraryService) | Low |
| `SPARK_Product.associateProductsAsks` | `productAsk` (ProductAskService) | Low |
| `SPARK_Product.attachmentSummary` | `search` (SearchService (elastic)) | Low |
| `SPARK_Product.attachments` | `attachment` (separate DGS (plm-attachment)), `relationship` (RelationshipService) | Medium |
| `SPARK_Product.attachmentsData` | `relationship` (RelationshipService) | Low |
| `SPARK_Product.attachmentsWithMetaData` | `attachment` (separate DGS (plm-attachment)), `relationship` (RelationshipService), `sampleV2` (SampleService) | High |
| `SPARK_Product.brand` | `brand` (VMM platform) | Low |
| `SPARK_Product.brands` | `brand` (VMM platform) | Low |
| `SPARK_Product.businessPartners` | `workspaceV2` (WorkspaceService) | Low |
| `SPARK_Product.clazz` | `ig` (Item Groups (IG)) | Low |
| `SPARK_Product.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Product.department` | `ig` (Item Groups (IG)) | Low |
| `SPARK_Product.designCycle` | `tag` (TagService) | Low |
| `SPARK_Product.discussionsCount` | `discussion` (separate DGS (plm-discussion)) | Low |
| `SPARK_Product.discussionsV2` | `search` (SearchService (elastic)) | Low |
| `SPARK_Product.division` | `ig` (Item Groups (IG)) | Low |
| `SPARK_Product.divisions` | `ig` (Item Groups (IG)) | Low |
| `SPARK_Product.elasticSamplesList` | `search` (SearchService (elastic)) | Low |
| `SPARK_Product.productTemplateDepartments` | `ig` (Item Groups (IG)) | Low |
| `SPARK_Product.productWorkspaceAttributes` | `search` (SearchService (elastic)), `tag` (TagService) | Medium |
| `SPARK_Product.productWorkspaceInfo` | `search` (SearchService (elastic)), `tag` (TagService) | Medium |
| `SPARK_Product.samples` | `relationship` (RelationshipService) | Low |
| `SPARK_Product.teams` | `teamV2` (TeamService) | Low |
| `SPARK_Product.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Product.variations` | `productVariation` (ProductVariationService) | Low |
| `SPARK_Product.versionCreatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Product.workspaces` | `search` (SearchService (elastic)) | Low |
| `SPARK_ProductRules.departments` | `ig` (Item Groups (IG)) | Low |
| `SPARK_ProductRules.insightsClassExclusion` | `ig` (Item Groups (IG)) | Low |
| `SPARK_ProductsCategories.categories` | `brand` (VMM platform), `ig` (Item Groups (IG)), `packaging` (Packaging), `tag` (TagService) | High |
| `SPARK_Tcin.itemDetails` | `coronaItems` (External platforms) | Low |

### BOM

| Resolver | Requires | Complexity |
|---|---|---|
| `SPARK_BomCombinationMaterial.libraryResource` | `combination` (CombinationService) | Low |
| `SPARK_BomFabricLibraryImpressionDetails.libraryResource` | `search` (SearchService (elastic)) | Low |
| `SPARK_BomFabricMaterial.libraryResource` | `search` (SearchService (elastic)) | Low |
| `SPARK_BomFabricSpecMaterial.libraryResource` | `fabric` (FabricService) | Low |
| `SPARK_BomImpressionDetails_Unified.libraryResource` | `search` (SearchService (elastic)) | Low |
| `SPARK_BomMaterialSearchResult.fabric` | `fabric` (FabricService) | Low |
| `SPARK_BomMaterialSearchResult.fabricSpec` | `fabric` (FabricService) | Low |
| `SPARK_BomMaterialSearchResult.relatedMaterials` | `search` (SearchService (elastic)) | Low |
| `SPARK_BomTrimLibraryImpressionDetails.libraryResource` | `search` (SearchService (elastic)) | Low |
| `SPARK_BomTrimMaterial.facilityName` | `location` (VMM platform), `trim` (TrimService) | Medium |
| `SPARK_BomTrimMaterial.libraryResource` | `trim` (TrimService) | Low |
| `SPARK_BomTrimMaterial.materialLibraryUom` | `trim` (TrimService) | Low |
| `SPARK_BomTrimMaterial.sizeCaption` | `trim` (TrimService) | Low |
| `SPARK_BomTrimMaterial.sizeValue` | `trim` (TrimService) | Low |
| `SPARK_BomWashMaterial.libraryResource` | `wash` (WashService) | Low |

### Measurement

| Resolver | Requires | Complexity |
|---|---|---|
| `SPARK_MeasurementTemplate.brands` | `brand` (VMM platform) | Low |
| `SPARK_MeasurementTemplate.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_MeasurementTemplate.departments` | `ig` (Item Groups (IG)) | Low |
| `SPARK_MeasurementTemplate.divisions` | `ig` (Item Groups (IG)) | Low |
| `SPARK_MeasurementTemplate.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Measurements.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Measurements.product` | `product` (Product) | Low |
| `SPARK_Measurements.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Measurements.updatedFromResource` | `sampleV2` (SampleService) | Low |
| `SPARK_SampleMeasurementSet.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_SizeTemplate.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_SizeTemplate.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_TightFit.brands` | `brand` (VMM platform) | Low |
| `SPARK_TightFit.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_TightFit.departments` | `ig` (Item Groups (IG)) | Low |
| `SPARK_TightFit.divisions` | `ig` (Item Groups (IG)) | Low |
| `SPARK_TightFit.updatedBy` | `userAttributes` (UserProfileService) | Low |

### Product Details

| Resolver | Requires | Complexity |
|---|---|---|
| `Query.getProductDetailsElastic` | `search` (SearchService (elastic)) | Low |
| `SPARK_ProductDetails.attachment` | `search` (SearchService (elastic)) | Low |
| `SPARK_ProductDetails.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_ProductDetails.product` | `product` (Product) | Low |
| `SPARK_ProductDetails.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_ProductDetailsCategoryWithSection.subCategories` | `specificationsTemplate` (SpecificationsTemplateService) | Low |
| `SPARK_ProductDetailsItem.attachment` | `search` (SearchService (elastic)) | Low |
| `SPARK_ProductDetailsItem.constructionSetAttachments` | `search` (SearchService (elastic)) | Low |

### Packaging

| Resolver | Requires | Complexity |
|---|---|---|
| `Mutation.cloneFilesForDielines` | `attachment` (separate DGS (plm-attachment)) | Low |
| `Query.getPackagingElastic` | `search` (SearchService (elastic)) | Low |
| `SPARK_Dieline.attachment` | `attachment` (separate DGS (plm-attachment)) | Low |
| `SPARK_Dieline.attachments` | `search` (SearchService (elastic)) | Low |
| `SPARK_Dieline.evaluatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Packaging.attachments` | `search` (SearchService (elastic)) | Low |
| `SPARK_Packaging.dielineEvaluators` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Packaging.product` | `product` (Product) | Low |
| `SPARK_Packaging.waveDescription` | `tag` (TagService) | Low |
| `SPARK_Packaging.workspaces` | `search` (SearchService (elastic)) | Low |
| `SPARK_PackagingElement.packagingLibrary` | `fileLibrary` (FileLibraryService) | Low |

### Watchlist

| Resolver | Requires | Complexity |
|---|---|---|
| `Query.parentId` | `search` (SearchService (elastic)) | Low |
| `SPARK_Watchlist.attachments` | `search` (SearchService (elastic)) | Low |
| `SPARK_Watchlist.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Watchlist.product` | `product` (Product) | Low |
| `SPARK_Watchlist.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_WatchlistPartner.partnerName` | `vmm` (VMM platform) | Low |

### Impression

| Resolver | Requires | Complexity |
|---|---|---|
| `SPARK_Impression.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Impression.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_ImpressionCount.counts` | `product` (Product) | Low |

### Claims

| Resolver | Requires | Complexity |
|---|---|---|
| `Query.getClaimsElastic` | `search` (SearchService (elastic)) | Low |
| `SPARK_ClaimSubstantiate.substantiatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Claims.businessPartner` | `vmm` (VMM platform) | Low |
| `SPARK_Claims.createdBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_Claims.designPartner` | `vmm` (VMM platform) | Low |
| `SPARK_Claims.parentDetails` | `product` (Product) | Low |
| `SPARK_Claims.product` | `product` (Product) | Low |
| `SPARK_Claims.updatedBy` | `userAttributes` (UserProfileService) | Low |
| `SPARK_ParentDetails.otherClaimBps` | `search` (SearchService (elastic)) | Low |
| `SPARK_ParentDetails.systemTeams` | `search` (SearchService (elastic)) | Low |

---
*Program roll-up · generated 2026-07-21 from each domain's `be-06-cross-domain-field-analysis.md`.*