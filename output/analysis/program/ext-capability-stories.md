# External Capability Stories — Consolidated by Reusable Dependency

> **Generated:** 2026-07-19 · by `generate_ext_capabilities.py`. Auto-generated — regenerate after any `domain-service-catalog.md` or `be-04-stories.md` change; never hand-edit.

> **Why this file exists:** `output/clientStoryDependency/` and `output/analysis/program/ext-dependency-stories.md` correctly identify WHICH fields depend on an external service, but authored a story per (domain, field) — so the SAME external capability (e.g. VMM's business-partner lookup) could get re-authored once per consuming domain. This file re-groups every cross-domain/EXT resolver (`be-06-cross-domain-field-analysis.md`, all 8 domains) by its **owning service/platform** — the real reusable-capability boundary already encoded in `domain-service-catalog.md`'s owner-label column — so there is exactly ONE EXT story per capability, and every consuming domain gets its own lightweight verification story instead of a duplicate implementation story.

**Dependency chain this produces:** `EXT capability (owning service exposes the lookup) → domain implementation (existing be-04 G/H story does the DGS-side fetch) → federation verification (confirm entity stitching / gateway stub resolves end-to-end) → client story`.

- **Sibling DGS** capabilities need a real `@DgsEntityFetcher` (or equivalent client-backed resolver) built ONCE by the owning domain/subgraph; every consumer then just references the entity via `@key` — no per-consumer reimplementation.
- **External platform** capabilities (VMM/IG/Doppler/Corona/...) are gateway-stub (`@extends`) dependencies — no DGS build on our side at all; every consumer's job is only to declare the stub and verify the gateway resolves it.

---

## Summary

| Capability | Kind | Domains | Consuming resolvers |
|---|---|---|---|
| `EXT-SEARCH-01` SearchService (elastic) | Sibling DGS subgraph | 7 | 28 |
| `EXT-USERPROFILE-02` UserProfileService | Sibling DGS subgraph | 7 | 24 |
| `EXT-VMM-03` VMM platform | External platform (gateway stitch) | 5 | 10 |
| `EXT-ATTACHMENT-04` separate DGS (plm-attachment) | Sibling DGS subgraph | 4 | 11 |
| `EXT-FILELIBRARY-05` FileLibraryService | Sibling DGS subgraph | 2 | 2 |
| `EXT-IG-06` Item Groups (IG) | External platform (gateway stitch) | 2 | 15 |
| `EXT-RELATIONSHIP-07` RelationshipService | Sibling DGS subgraph | 2 | 6 |
| `EXT-SAMPLE-08` SampleService | Sibling DGS subgraph | 2 | 3 |
| `EXT-TAG-09` TagService | Sibling DGS subgraph | 2 | 5 |
| `EXT-COMBINATION-10` CombinationService | Sibling DGS subgraph | 1 | 1 |
| `EXT-DASHBOARD-11` Dashboard services | Sibling DGS subgraph | 1 | 3 |
| `EXT-EXTERNAL-12` External platforms | External platform (gateway stitch) | 1 | 3 |
| `EXT-FABRIC-13` FabricService | Sibling DGS subgraph | 1 | 3 |
| `EXT-MATERIALHUB-14` MaterialHubService | Sibling DGS subgraph | 1 | 1 |
| `EXT-PRODUCTASK-15` ProductAskService | Sibling DGS subgraph | 1 | 1 |
| `EXT-PRODUCTVARIATION-16` ProductVariationService | Sibling DGS subgraph | 1 | 1 |
| `EXT-RULELIBRARY-17` RuleLibraryService | Sibling DGS subgraph | 1 | 3 |
| `EXT-SPECIFICATIONSTEMPLATE-18` SpecificationsTemplateService | Sibling DGS subgraph | 1 | 1 |
| `EXT-TEAM-19` TeamService | Sibling DGS subgraph | 1 | 1 |
| `EXT-TRIM-20` TrimService | Sibling DGS subgraph | 1 | 5 |
| `EXT-USERGROUP-21` UserGroupService | Sibling DGS subgraph | 1 | 2 |
| `EXT-WASH-22` WashService | Sibling DGS subgraph | 1 | 1 |
| `EXT-WORKSPACE-23` WorkspaceService | Sibling DGS subgraph | 1 | 3 |
| `EXT-DISCUSSION-24` separate DGS (plm-discussion) | Sibling DGS subgraph | 1 | 1 |

---

### EXT-SEARCH-01 · SearchService (elastic) — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `search` · **Consuming domains:** 7 (bom, claims, measurement, packaging, product, productDetails, watchlist) · **Consuming resolvers:** 28 (4 with confirmed client usage)

- **Owning-side work (build once):** SearchService (elastic) exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if SearchService (elastic) isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| bom | `Query.getBomElastic`, `SPARK_BomFabricMaterial.libraryResource`, `SPARK_BomImpressionDetails_Unified.libraryResource`, `SPARK_BomFabricLibraryImpressionDetails.libraryResource`, `SPARK_BomTrimLibraryImpressionDetails.libraryResource`, `SPARK_BomMaterialSearchResult.relatedMaterials`, `Query.searchMaterialsBom` | ✅ yes | `BOM-BE-C-01`, `BOM-BE-C-02`, `BOM-BE-F-02`, `BOM-BE-G-05`, `BOM-BE-G-10`, `BOM-BE-G-11`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-15` | `BOM-BE-C-01` — verify SearchService (elastic) entity stitching in the bom subgraph |
| claims | `Query.getClaimsElastic`, `SPARK_ParentDetails.otherClaimBps`, `SPARK_ParentDetails.systemTeams` | ⏭ not found in ClientCallingGqlQueries | `CLAIM-BE-C-02`, `CLAIM-BE-G-03` | `CLAIM-BE-C-02` — verify SearchService (elastic) entity stitching in the claims subgraph |
| measurement | `Query.getMeasurementsElastic` | ✅ yes | `MST-BE-C-02` | `MST-BE-C-02` — verify SearchService (elastic) entity stitching in the measurement subgraph |
| packaging | `SPARK_Packaging.attachments`, `SPARK_Dieline.attachments`, `Query.getPackagingElastic`, `SPARK_Packaging.workspaces` | ⏭ not found in ClientCallingGqlQueries | `PKG-BE-C-01`, `PKG-BE-G-03`, `PKG-BE-G-05` | `PKG-BE-C-01` — verify SearchService (elastic) entity stitching in the packaging subgraph |
| product | `SPARK_Product.attachmentSummary`, `SPARK_Product.discussionsV2`, `SPARK_Product.elasticSamplesList`, `SPARK_Product.productWorkspaceAttributes`, `SPARK_Product.productWorkspaceInfo`, `SPARK_Product.workspaces` | ⏭ not found in ClientCallingGqlQueries | `PRODUCT-BE-C-01`, `PRODUCT-BE-C-02`, `PRODUCT-BE-C-03`, `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-G-02`, `PRODUCT-BE-G-03`, `PRODUCT-BE-G-05`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-09` | `PRODUCT-BE-C-01` — verify SearchService (elastic) entity stitching in the product subgraph |
| productDetails | `SPARK_ProductDetails.attachment`, `SPARK_ProductDetailsItem.attachment`, `SPARK_ProductDetailsItem.constructionSetAttachments`, `Query.getProductDetailsElastic` | ⏭ not found in ClientCallingGqlQueries | `PDTL-BE-C-01`, `PDTL-BE-G-03` | `PDTL-BE-C-01` — verify SearchService (elastic) entity stitching in the productDetails subgraph |
| watchlist | `SPARK_Watchlist.attachments`, `Query.getWatchlistByFilter`, `Query.parentId` | ✅ yes | `WATCHLIST-BE-C-01`, `WATCHLIST-BE-G-03` | `WATCHLIST-BE-C-01` — verify SearchService (elastic) entity stitching in the watchlist subgraph |

> ⏭ No confirmed client usage for: `product.elasticSamplesList`, `product.productWorkspaceAttributes`, `product.productWorkspaceInfo`, `product.discussionsV2`, `product.workspaces`, `product.attachmentSummary`, `bom.libraryResource`, `bom.libraryResource`, `bom.libraryResource`, `bom.libraryResource`, `bom.relatedMaterials`, `productDetails.getProductDetailsElastic`, `productDetails.attachment`, `productDetails.attachment`, `productDetails.constructionSetAttachments`, `packaging.getPackagingElastic`, `packaging.workspaces`, `packaging.attachments`, `packaging.attachments`, `watchlist.parentId`, `watchlist.attachments`, `claims.getClaimsElastic`, `claims.otherClaimBps`, `claims.systemTeams` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-USERPROFILE-02 · UserProfileService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `userAttributes` · **Consuming domains:** 7 (claims, impression, measurement, packaging, product, productDetails, watchlist) · **Consuming resolvers:** 24 (0 with confirmed client usage)

- **Owning-side work (build once):** UserProfileService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if UserProfileService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| claims | `SPARK_Claims.createdBy`, `SPARK_ClaimSubstantiate.substantiatedBy`, `SPARK_Claims.updatedBy` | ⏭ not found in ClientCallingGqlQueries | `CLAIM-BE-G-02`, `CLAIM-BE-G-04` | `CLAIM-BE-G-02` — verify UserProfileService entity stitching in the claims subgraph |
| impression | `SPARK_Impression.createdBy`, `SPARK_Impression.updatedBy` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `IMPRESSION-BE-G-VERIFY-USERPROFILE` — verify UserProfileService entity stitching in the impression subgraph |
| measurement | `SPARK_Measurements.createdBy`, `SPARK_SampleMeasurementSet.createdBy`, `SPARK_MeasurementTemplate.createdBy`, `SPARK_SizeTemplate.createdBy`, `SPARK_TightFit.createdBy`, `SPARK_Measurements.updatedBy`, `SPARK_MeasurementTemplate.updatedBy`, `SPARK_SizeTemplate.updatedBy`, `SPARK_TightFit.updatedBy` | ⏭ not found in ClientCallingGqlQueries | `MST-BE-G-01`, `MST-BE-G-02`, `MST-BE-G-05`, `MST-BE-G-06`, `MST-BE-G-07` | `MST-BE-G-01` — verify UserProfileService entity stitching in the measurement subgraph |
| packaging | `SPARK_Packaging.dielineEvaluators`, `SPARK_Dieline.evaluatedBy` | ⏭ not found in ClientCallingGqlQueries | `PKG-BE-G-02`, `PKG-BE-G-05` | `PKG-BE-G-02` — verify UserProfileService entity stitching in the packaging subgraph |
| product | `SPARK_Product.createdBy`, `SPARK_Product.updatedBy`, `ProductComponentStatus.updatedBy`, `SPARK_Product.versionCreatedBy` | ⏭ not found in ClientCallingGqlQueries | `PRODUCT-BE-G-14` | `PRODUCT-BE-G-14` — verify UserProfileService entity stitching in the product subgraph |
| productDetails | `SPARK_ProductDetails.createdBy`, `SPARK_ProductDetails.updatedBy` | ⏭ not found in ClientCallingGqlQueries | `PDTL-BE-G-02` | `PDTL-BE-G-02` — verify UserProfileService entity stitching in the productDetails subgraph |
| watchlist | `SPARK_Watchlist.createdBy`, `SPARK_Watchlist.updatedBy` | ⏭ not found in ClientCallingGqlQueries | `WATCHLIST-BE-G-02` | `WATCHLIST-BE-G-02` — verify UserProfileService entity stitching in the watchlist subgraph |

> ⏭ No confirmed client usage for: `product.createdBy`, `product.updatedBy`, `product.versionCreatedBy`, `product.updatedBy`, `measurement.createdBy`, `measurement.updatedBy`, `measurement.createdBy`, `measurement.createdBy`, `measurement.updatedBy`, `measurement.createdBy`, `measurement.updatedBy`, `measurement.createdBy`, `measurement.updatedBy`, `productDetails.createdBy`, `productDetails.updatedBy`, `packaging.dielineEvaluators`, `packaging.evaluatedBy`, `watchlist.createdBy`, `watchlist.updatedBy`, `impression.createdBy`, `impression.updatedBy`, `claims.createdBy`, `claims.updatedBy`, `claims.substantiatedBy` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-VMM-03 · VMM platform — external lookup/entity resolver
- **Kind:** External platform (gateway stitch) · **Loader key(s):** `brand`, `location`, `vmm` · **Consuming domains:** 5 (bom, claims, measurement, product, watchlist) · **Consuming resolvers:** 10 (1 with confirmed client usage)

- **Owning-side work:** none on our side — VMM platform is an external platform; the gateway resolves an `@extends @external` stub directly. Each consumer only needs to declare the stub correctly and verify the gateway stitch end-to-end.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| bom | `SPARK_BomTrimMaterial.facilityName`, `Query.getComboSupplierForBom` | ✅ yes | `BOM-BE-C-02`, `BOM-BE-C-03`, `BOM-BE-C-04`, `BOM-BE-C-05`, `BOM-BE-G-08`, `BOM-BE-G-17` | `BOM-BE-C-02` — verify VMM platform entity stitching in the bom subgraph |
| claims | `SPARK_Claims.businessPartner`, `SPARK_Claims.designPartner` | ⏭ not found in ClientCallingGqlQueries | `CLAIM-BE-G-02` | `CLAIM-BE-G-02` — verify VMM platform entity stitching in the claims subgraph |
| measurement | `SPARK_MeasurementTemplate.brands`, `SPARK_TightFit.brands` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `MST-BE-G-VERIFY-VMM` — verify VMM platform entity stitching in the measurement subgraph |
| product | `SPARK_Product.brand`, `SPARK_Product.brands`, `SPARK_ProductsCategories.categories` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `PRODUCT-BE-G-VERIFY-VMM` — verify VMM platform entity stitching in the product subgraph |
| watchlist | `SPARK_WatchlistPartner.partnerName` | ⏭ not found in ClientCallingGqlQueries | `WATCHLIST-BE-G-02`, `WATCHLIST-BE-G-05` | `WATCHLIST-BE-G-02` — verify VMM platform entity stitching in the watchlist subgraph |

> ⏭ No confirmed client usage for: `product.brand`, `product.brands`, `product.categories`, `bom.facilityName`, `measurement.brands`, `measurement.brands`, `watchlist.partnerName`, `claims.businessPartner`, `claims.designPartner` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-ATTACHMENT-04 · separate DGS (plm-attachment) — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `attachment` · **Consuming domains:** 4 (packaging, product, productDetails, watchlist) · **Consuming resolvers:** 11 (7 with confirmed client usage)

- **Owning-side work (build once):** separate DGS (plm-attachment) exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if separate DGS (plm-attachment) isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| packaging | `SPARK_Dieline.attachment`, `Mutation.cloneFilesForDielines`, `Mutation.updatePackaging` | ✅ yes | `PKG-BE-D-08`, `PKG-BE-E-01`, `PKG-BE-G-05` | `PKG-BE-D-08` — verify separate DGS (plm-attachment) entity stitching in the packaging subgraph |
| product | `Mutation.addProducts`, `SPARK_Product.attachments`, `SPARK_Product.attachmentsWithMetaData`, `Mutation.updateProduct` | ✅ yes | `PRODUCT-BE-D-01`, `PRODUCT-BE-D-02`, `PRODUCT-BE-D-04`, `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-G-01`, `PRODUCT-BE-G-03` | `PRODUCT-BE-D-01` — verify separate DGS (plm-attachment) entity stitching in the product subgraph |
| productDetails | `Mutation.cloneFilesForProductDetails`, `Mutation.updateProductDetailsSet` | ✅ yes | `PDTL-BE-D-04`, `PDTL-BE-E-01` | `PDTL-BE-D-04` — verify separate DGS (plm-attachment) entity stitching in the productDetails subgraph |
| watchlist | `Mutation.cloneFilesForWatchlist`, `Mutation.updateWatchlistEntries` | ✅ yes | `WATCHLIST-BE-D-02`, `WATCHLIST-BE-E-01` | `WATCHLIST-BE-D-02` — verify separate DGS (plm-attachment) entity stitching in the watchlist subgraph |

> ⏭ No confirmed client usage for: `product.attachments`, `product.attachmentsWithMetaData`, `packaging.cloneFilesForDielines`, `packaging.attachment` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-FILELIBRARY-05 · FileLibraryService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `fileLibrary` · **Consuming domains:** 2 (packaging, product) · **Consuming resolvers:** 2 (0 with confirmed client usage)

- **Owning-side work (build once):** FileLibraryService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if FileLibraryService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| packaging | `SPARK_PackagingElement.packagingLibrary` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `PKG-BE-G-VERIFY-FILELIBRARY` — verify FileLibraryService entity stitching in the packaging subgraph |
| product | `SPARK_PackagingAttribute.spg` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `PRODUCT-BE-G-VERIFY-FILELIBRARY` — verify FileLibraryService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.spg`, `packaging.packagingLibrary` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-IG-06 · Item Groups (IG) — external lookup/entity resolver
- **Kind:** External platform (gateway stitch) · **Loader key(s):** `ig` · **Consuming domains:** 2 (measurement, product) · **Consuming resolvers:** 15 (0 with confirmed client usage)

- **Owning-side work:** none on our side — Item Groups (IG) is an external platform; the gateway resolves an `@extends @external` stub directly. Each consumer only needs to declare the stub correctly and verify the gateway stitch end-to-end.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| measurement | `SPARK_MeasurementTemplate.departments`, `SPARK_TightFit.departments`, `SPARK_MeasurementTemplate.divisions`, `SPARK_TightFit.divisions` | ⏭ not found in ClientCallingGqlQueries | `MST-BE-G-05`, `MST-BE-G-07` | `MST-BE-G-05` — verify Item Groups (IG) entity stitching in the measurement subgraph |
| product | `SPARK_ProductsCategories.categories`, `SPARK_Product.clazz`, `DopplerDepartment.clazzes`, `SPARK_Product.department`, `DopplerDepartment.department`, `SPARK_ProductRules.departments`, `SPARK_Product.division`, `DopplerDepartment.division`, `SPARK_Product.divisions`, `SPARK_ProductRules.insightsClassExclusion`, `SPARK_Product.productTemplateDepartments` | ⏭ not found in ClientCallingGqlQueries | `PRODUCT-BE-G-13` | `PRODUCT-BE-G-13` — verify Item Groups (IG) entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.department`, `product.division`, `product.clazz`, `product.productTemplateDepartments`, `product.divisions`, `product.categories`, `product.departments`, `product.insightsClassExclusion`, `product.department`, `product.division`, `product.clazzes`, `measurement.departments`, `measurement.divisions`, `measurement.departments`, `measurement.divisions` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-RELATIONSHIP-07 · RelationshipService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `relationship` · **Consuming domains:** 2 (measurement, product) · **Consuming resolvers:** 6 (2 with confirmed client usage)

- **Owning-side work (build once):** RelationshipService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if RelationshipService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| measurement | `Query.getMeasurements` | ✅ yes | `MST-BE-C-01`, `MST-BE-F-01` | `MST-BE-C-01` — verify RelationshipService entity stitching in the measurement subgraph |
| product | `SPARK_Product.attachments`, `SPARK_Product.attachmentsData`, `SPARK_Product.attachmentsWithMetaData`, `Mutation.productBusinessPartnerActions`, `SPARK_Product.samples` | ✅ yes | `PRODUCT-BE-G-01`, `PRODUCT-BE-G-10` | `PRODUCT-BE-G-01` — verify RelationshipService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.samples`, `product.attachments`, `product.attachmentsWithMetaData`, `product.attachmentsData` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-SAMPLE-08 · SampleService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `sampleV2` · **Consuming domains:** 2 (measurement, product) · **Consuming resolvers:** 3 (1 with confirmed client usage)

- **Owning-side work (build once):** SampleService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if SampleService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| measurement | `SPARK_Measurements.updatedFromResource` | ⏭ not found in ClientCallingGqlQueries | `MST-BE-G-01` | `MST-BE-G-01` — verify SampleService entity stitching in the measurement subgraph |
| product | `SPARK_Product.attachmentsWithMetaData`, `Mutation.productBusinessPartnerActions` | ✅ yes | `PRODUCT-BE-E-01`, `PRODUCT-BE-G-05` | `PRODUCT-BE-E-01` — verify SampleService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.attachmentsWithMetaData`, `measurement.updatedFromResource` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-TAG-09 · TagService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `tag` · **Consuming domains:** 2 (packaging, product) · **Consuming resolvers:** 5 (0 with confirmed client usage)

- **Owning-side work (build once):** TagService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if TagService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| packaging | `SPARK_Packaging.waveDescription` | ⏭ not found in ClientCallingGqlQueries | `PKG-BE-G-04` | `PKG-BE-G-04` — verify TagService entity stitching in the packaging subgraph |
| product | `SPARK_ProductsCategories.categories`, `SPARK_Product.designCycle`, `SPARK_Product.productWorkspaceAttributes`, `SPARK_Product.productWorkspaceInfo` | ⏭ not found in ClientCallingGqlQueries | `PRODUCT-BE-G-09`, `PRODUCT-BE-G-13` | `PRODUCT-BE-G-09` — verify TagService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.productWorkspaceAttributes`, `product.designCycle`, `product.productWorkspaceInfo`, `product.categories`, `packaging.waveDescription` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-COMBINATION-10 · CombinationService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `combination` · **Consuming domains:** 1 (bom) · **Consuming resolvers:** 1 (0 with confirmed client usage)

- **Owning-side work (build once):** CombinationService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if CombinationService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| bom | `SPARK_BomCombinationMaterial.libraryResource` | ⏭ not found in ClientCallingGqlQueries | `BOM-BE-C-03`, `BOM-BE-G-07` | `BOM-BE-C-03` — verify CombinationService entity stitching in the bom subgraph |

> ⏭ No confirmed client usage for: `bom.libraryResource` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-DASHBOARD-11 · Dashboard services — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `favorite`, `recentlyViewed`, `todo` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 3 (3 with confirmed client usage)

- **Owning-side work (build once):** Dashboard services exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if Dashboard services isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `Mutation.productBusinessPartnerActions`, `Mutation.productBusinessPartnerActions`, `Mutation.productBusinessPartnerActions` | ✅ yes | `PRODUCT-BE-E-01` | `PRODUCT-BE-E-01` — verify Dashboard services entity stitching in the product subgraph |

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-EXTERNAL-12 · External platforms — external lookup/entity resolver
- **Kind:** External platform (gateway stitch) · **Loader key(s):** `coronaItems`, `doppler` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 3 (0 with confirmed client usage)

- **Owning-side work:** none on our side — External platforms is an external platform; the gateway resolves an `@extends @external` stub directly. Each consumer only needs to declare the stub correctly and verify the gateway stitch end-to-end.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `SPARK_Tcin.itemDetails`, `DopplerDepartment.primaryCapacityTypeName`, `DopplerDepartment.secondaryCapacityTypeName` | ⏭ not found in ClientCallingGqlQueries | `PRODUCT-BE-G-04` | `PRODUCT-BE-G-04` — verify External platforms entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.itemDetails`, `product.primaryCapacityTypeName`, `product.secondaryCapacityTypeName` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-FABRIC-13 · FabricService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `fabric` · **Consuming domains:** 1 (bom) · **Consuming resolvers:** 3 (0 with confirmed client usage)

- **Owning-side work (build once):** FabricService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if FabricService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| bom | `SPARK_BomMaterialSearchResult.fabric`, `SPARK_BomMaterialSearchResult.fabricSpec`, `SPARK_BomFabricSpecMaterial.libraryResource` | ⏭ not found in ClientCallingGqlQueries | `BOM-BE-G-06`, `BOM-BE-G-15` | `BOM-BE-G-06` — verify FabricService entity stitching in the bom subgraph |

> ⏭ No confirmed client usage for: `bom.libraryResource`, `bom.fabricSpec`, `bom.fabric` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-MATERIALHUB-14 · MaterialHubService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `materialHub` · **Consuming domains:** 1 (bom) · **Consuming resolvers:** 1 (1 with confirmed client usage)

- **Owning-side work (build once):** MaterialHubService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if MaterialHubService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| bom | `Query.getBomMaterialTypes` | ✅ yes | `BOM-BE-B-05`, `BOM-BE-G-03`, `BOM-BE-G-05`, `BOM-BE-G-06`, `BOM-BE-G-07`, `BOM-BE-G-09` | `BOM-BE-B-05` — verify MaterialHubService entity stitching in the bom subgraph |

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-PRODUCTASK-15 · ProductAskService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `productAsk` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 1 (0 with confirmed client usage)

- **Owning-side work (build once):** ProductAskService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if ProductAskService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `SPARK_Product.associateProductsAsks` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `PRODUCT-BE-G-VERIFY-PRODUCTASK` — verify ProductAskService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.associateProductsAsks` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-PRODUCTVARIATION-16 · ProductVariationService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `productVariation` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 1 (0 with confirmed client usage)

- **Owning-side work (build once):** ProductVariationService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if ProductVariationService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `SPARK_Product.variations` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `PRODUCT-BE-G-VERIFY-PRODUCTVARIATION` — verify ProductVariationService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.variations` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-RULELIBRARY-17 · RuleLibraryService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `ruleLibrary` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 3 (3 with confirmed client usage)

- **Owning-side work (build once):** RuleLibraryService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if RuleLibraryService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `Query.getProductBPRules`, `Query.getProductDeptRules`, `Query.searchProductRules` | ✅ yes | `PRODUCT-BE-B-10`, `PRODUCT-BE-B-11`, `PRODUCT-BE-C-05` | `PRODUCT-BE-B-10` — verify RuleLibraryService entity stitching in the product subgraph |

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-SPECIFICATIONSTEMPLATE-18 · SpecificationsTemplateService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `specificationsTemplate` · **Consuming domains:** 1 (productDetails) · **Consuming resolvers:** 1 (0 with confirmed client usage)

- **Owning-side work (build once):** SpecificationsTemplateService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if SpecificationsTemplateService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| productDetails | `SPARK_ProductDetailsCategoryWithSection.subCategories` | ⏭ not found in ClientCallingGqlQueries | — (none found; needs authoring) | `PDTL-BE-G-VERIFY-SPECIFICATIONSTEMPLATE` — verify SpecificationsTemplateService entity stitching in the productDetails subgraph |

> ⏭ No confirmed client usage for: `productDetails.subCategories` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-TEAM-19 · TeamService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `teamV2` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 1 (0 with confirmed client usage)

- **Owning-side work (build once):** TeamService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if TeamService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `SPARK_Product.teams` | ⏭ not found in ClientCallingGqlQueries | `PRODUCT-BE-G-06` | `PRODUCT-BE-G-06` — verify TeamService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.teams` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-TRIM-20 · TrimService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `trim` · **Consuming domains:** 1 (bom) · **Consuming resolvers:** 5 (0 with confirmed client usage)

- **Owning-side work (build once):** TrimService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if TrimService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| bom | `SPARK_BomTrimMaterial.facilityName`, `SPARK_BomTrimMaterial.libraryResource`, `SPARK_BomTrimMaterial.materialLibraryUom`, `SPARK_BomTrimMaterial.sizeCaption`, `SPARK_BomTrimMaterial.sizeValue` | ⏭ not found in ClientCallingGqlQueries | `BOM-BE-G-08` | `BOM-BE-G-08` — verify TrimService entity stitching in the bom subgraph |

> ⏭ No confirmed client usage for: `bom.libraryResource`, `bom.materialLibraryUom`, `bom.sizeValue`, `bom.sizeCaption`, `bom.facilityName` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-USERGROUP-21 · UserGroupService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `userGroup` · **Consuming domains:** 1 (watchlist) · **Consuming resolvers:** 2 (2 with confirmed client usage)

- **Owning-side work (build once):** UserGroupService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if UserGroupService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| watchlist | `Mutation.createWatchlistEntries`, `Mutation.updateWatchlistEntries` | ✅ yes | `WATCHLIST-BE-D-01`, `WATCHLIST-BE-E-01`, `WATCHLIST-BE-G-02` | `WATCHLIST-BE-D-01` — verify UserGroupService entity stitching in the watchlist subgraph |

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-WASH-22 · WashService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `wash` · **Consuming domains:** 1 (bom) · **Consuming resolvers:** 1 (0 with confirmed client usage)

- **Owning-side work (build once):** WashService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if WashService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| bom | `SPARK_BomWashMaterial.libraryResource` | ⏭ not found in ClientCallingGqlQueries | `BOM-BE-G-09` | `BOM-BE-G-09` — verify WashService entity stitching in the bom subgraph |

> ⏭ No confirmed client usage for: `bom.libraryResource` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-WORKSPACE-23 · WorkspaceService — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `workspaceV2` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 3 (2 with confirmed client usage)

- **Owning-side work (build once):** WorkspaceService exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if WorkspaceService isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `Mutation.addProduct`, `Mutation.addProducts`, `SPARK_Product.businessPartners` | ✅ yes | `PRODUCT-BE-D-01`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-09`, `PRODUCT-BE-G-11-1` | `PRODUCT-BE-D-01` — verify WorkspaceService entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.businessPartners` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---

### EXT-DISCUSSION-24 · separate DGS (plm-discussion) — external lookup/entity resolver
- **Kind:** Sibling DGS subgraph · **Loader key(s):** `discussion` · **Consuming domains:** 1 (product) · **Consuming resolvers:** 1 (0 with confirmed client usage)

- **Owning-side work (build once):** separate DGS (plm-discussion) exposes a federation entity (`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant per federation spec) — OR, if separate DGS (plm-discussion) isn't itself migrating to DGS in this phase, a thin shared client/module every consumer imports rather than each reimplementing its own call. This is the SINGLE piece of work that unblocks every consumer below.

#### Consumers (per domain — verification story, not a duplicate implementation)

| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |
|---|---|---|---|---|
| product | `SPARK_Product.discussionsCount` | ⏭ not found in ClientCallingGqlQueries | `PRODUCT-BE-G-06` | `PRODUCT-BE-G-06` — verify separate DGS (plm-discussion) entity stitching in the product subgraph |

> ⏭ No confirmed client usage for: `product.discussionsCount` — candidates to defer rather than build/verify federation for, pending confirmation against `ClientCallingGqlQueries/`.

#### Acceptance Criteria

1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for every consuming domain listed above, not just one.
2. Every consuming domain's own verification story confirms ITS query returns the hydrated entity correctly — it does not reimplement the lookup.
3. Unknown/missing upstream ids yield `null` without failing the whole response (federation spec null-tolerance).

---
