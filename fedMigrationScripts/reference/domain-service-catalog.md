---
description: "Single source of truth for the Spark GraphQL → Netflix DGS migration. Domain Service Catalog (37+ domains), context.js wiring rules, utils infrastructure, and lessons learned. Read this any time you need to look up a loader key, target DGS, source files, EXT classification, or util-to-DGS mapping."
applyTo: "**/spark-migration/**,**/spark-internal-graphql/**"
---

# Domain Service Catalog & Migration Reference

> This file is the **single source of truth** for per-domain facts the migration framework depends on.
> Agent definitions live in `agents/`. Phase procedures live in `skills/`. Output formats live in `templates/`.

---

## 1. Source System Overview

`spark-internal-graphql` is a centralized Node.js GraphQL gateway that proxies 37+ backend microservices. It contains:

- **80 schema files** defining types, queries, and mutations
- **60+ resolver files** implementing field resolution, transformation, and orchestration
- **50+ service files** wrapping REST calls to domain backends
- **40+ utility files** providing shared infrastructure: DataLoader patterns, case conversion, access control, workspace management, circuit breakers, caching, batching
- **`context.js`** — the central wiring file registering ALL microservices with endpoints and auth tokens

### Source Locations

```
spark-internal-graphql/packages/
└── data-source-spark/src/
    ├── schemas/             # 80 .graphql files
    ├── resolvers/           # 60+ .js resolver files + subdirectories
    │   ├── activityLogUtilities/
    │   ├── commonResolvers/
    │   ├── material/
    │   ├── product/
    │   ├── productplan/
    │   └── reporting/
    ├── services/            # 50+ .js service files + subdirectories
    │   ├── batchers/
    │   ├── material/
    │   ├── product/
    │   ├── productAsk/
    │   ├── productplan/
    │   └── reporting/
    ├── utils/               # 40+ shared utility files
    │   ├── Product/
    │   ├── Reporting/
    │   ├── ValueAssessment/
    │   ├── logging/
    │   ├── materials/
    │   ├── packaging/
    │   └── search/
    ├── config/              # Constants, business partner config
    └── context.js           # Service wiring — ALL microservice registration
```

### Context Registration Format

The **canonical source of truth** for service endpoints is `context.js`. Each entry:

```json
"{loaderKey}": { "service": "{ServiceClassName}", "url": "{baseUrl}", "repo": "{gitRepoName}" }
```

When analyzing any domain:
- Use the `loaderKey` to locate how the service is loaded in resolvers
- Use `url` as the backend base URL (replaces all `*_ENDPOINT` env var references)
- Use `repo` as the owning git repository name
- If a resolver calls a service **not owned by the current domain**, tag that call with **EXT Service**

---

## 2. Domain Service Catalog

### 2a. Services Targeting `spark-product` Backend
**URL:** `https://spark-product.dev.target.com` | **Repo:** `spark-product` | **Target DGS:** `plm-product`

| Loader Key | Service Class | Schema File | Resolver File |
|-----------|--------------|------------|--------------|
| `product` | `ProductService` | `SPARK_Product.graphql` | `SPARK_Product.js` |
| `bom` | `BomService` | `SPARK_Bom.graphql` | `product/SPARK_Bom.js` |
| `impression` | `ImpressionService` | `SPARK_Impression.graphql` | `product/SPARK_Impression.js` |
| `measurement` | `MeasurementService` | `SPARK_Measurement.graphql` | `product/SPARK_Measurement.js` |
| `packaging` | `PackagingService` | `SPARK_Packaging.graphql` | `product/SPARK_Packaging.js` |
| `productDetails` | `ProductDetailsService` | `SPARK_ProductDetail.graphql` | `product/SPARK_ProductDetail.js` |
| `sizeTemplate` | `SizeTemplateService` | `SPARK_SizeTemplate.graphql` | `product/SPARK_SizeTemplate.js` |
| `tightFit` | `TightFitService` | `SPARK_TightFit.graphql` | `product/SPARK_TightFit.js` |
| `watchlist` | `WatchlistService` | `SPARK_Watchlist.graphql` | `product/SPARK_Watchlist.js` |
| `fileLibrary` | `FileLibraryService` | `SPARK_FileLibrary.graphql` | `SPARK_FileLibrary.js` |
| `pom` | `PomService` | `SPARK_Pom.graphql` | `SPARK_Pom.js` |
| `specificationsTemplate` | `SpecificationsTemplateService` | `SPARK_SpecificationTemplate.graphql` | `SPARK_SpecificationsTemplate.js` |
| `productPlan` | `ProductPlanService` | `SPARK_ProductPlan.graphql` | `productplan/SPARK_ProductPlan.js` |
| `productAsk` | `ProductAskService` | *(part of ProductPlan)* | *(part of ProductPlan)* |
| `productVariation` | `ProductVariationService` | `SPARK_Variation.graphql` | `product/SPARK_Variation.js` |
| `measurementTemplate` | `MeasurementTemplateService` | `SPARK_MeasurementTemplate.graphql` | `SPARK_MeasurementTemplate.js` |
| `ruleLibrary` | `RuleLibraryService` | `SPARK_RuleLibrary.graphql` | `SPARK_RuleLibrary.js` |

### 2b. Independent Domain Services (Each Gets Own DGS)

| Loader Key | Service Class | Schema File | Target DGS |
|-----------|--------------|------------|-----------|
| `accessControl` | `AccessControlService` | `SPARK_AccessControl.graphql` | **AccessControlService** |
| `activity` | `ActivityCenterService` | `SPARK_ActivityCenter.graphql` | **ActivityService** |
| `artwork` | `ArtworkService` | `SPARK_Artwork.graphql` | **ArtworkService** |
| `attachment` | `AttachmentService` | `SPARK_Attachment.graphql` | **AttachmentService** |
| `color` | `ColorService` | `SPARK_Color.graphql` | **ColorService** |
| `colorArchroma` | `ColorArchromaService` | `SPARK_ColorArchroma.graphql` | **ColorService** |
| `combination` | `CombinationService` | `SPARK_Combination.graphql` | **CombinationService** |
| `discussion` | `DiscussionService` | `SPARK_Discussion.graphql` | **DiscussionService** |
| `discussionV3` | `DiscussionV3Service` | `SPARK_DiscussionV3.graphql` | **DiscussionService** |
| `fabric` | `FabricService` | `SPARK_Fabric.graphql` | **FabricService** |
| `materialHub` | `MaterialHubService` | `SPARK_MaterialHub.graphql` | **MaterialHubService** |
| `palette` | `PaletteService` | `SPARK_Palette.graphql` | **PaletteService** |
| `pdf` | `PdfService` | `SPARK_Pdf.graphql` | **PdfService** |
| `relationship` | `RelationshipService` | `SPARK_Relationship.graphql` | **RelationshipService** |
| `RFID` | `RFIDService` | `SPARK_RFID.graphql` | **RFIDService** |
| `sampleV2` | `SampleServiceV2` | `SPARK_SampleV2.graphql` | **SampleService** |
| `search` | `SearchService` | `SPARK_Search.graphql` | **SearchService** |
| `tag` | `TagService` | `SPARK_Tag.graphql` | **TagService** |
| `trim` | `TrimService` | `SPARK_Trim.graphql` | **TrimService** |
| `wash` | `WashService` | `SPARK_Wash.graphql` | **WashService** |
| `workspaceV2` | `WorkspaceServiceV2` | `SPARK_WorkspaceV2.graphql` | **WorkspaceService** |
| `claim` | `ClaimService` | `SPARK_Claims.graphql` | **ClaimService** |
| `notification` | `NotificationService` | `SPARK_Notification.graphql` | **NotificationService** |
| `exportHub` | `ExportHubService` | *(none)* | **ExportHubService** |
| `training` | `TrainingService` | `CONFLUENCE_Training.graphql` | **TrainingService** |
| `gallery` | `GalleryService` | *(none)* | **GalleryService** |
| `tgtColorEvaluator` | `TGTColorEvaluator` | `SPARK_AsapTGTColorEvaluator.graphql` | **CLMService** |
| `valueAssessment` | `ValueAssessmentService` | `SPARK_ValueAssessment.graphql` | **ValueAssessmentService** |

### 2c. User Profile Composite
**URL:** `https://spark-user-profile.dev.target.com` | **Repo:** `spark-user-profile` | **Target DGS:** `UserProfileService`

| Loader Key | Service Class | URL (context.js) | Schema File |
|-----------|--------------|-----------------|------------|
| `favorite` | `FavoriteService` | `.../favorites` | `SPARK_Favorite.graphql` |
| `teamV2` | `TeamServiceV2` | base URL | `SPARK_TeamV2.graphql` |
| `role` | `RoleService` | `spark-access-control.dev.target.com` | `SPARK_Role.graphql` |
| `userAttributes` | `UserAttributesService` | base URL | `SPARK_UserAttributes.graphql` |
| `todo` | `ToDoService` | `.../to_do` | `SPARK_ToDo.graphql` |
| `recentlyViewed` | `RecentlyViewedService` | `.../recentlyviewed` | `SPARK_RecentlyViewed.graphql` |
| `byotemplate` | `ByoTemplateService` | `stgapi-internal.target.com/bi_reporting_assets/...` | `SPARK_ByoTemplate.graphql` |

### 2d. External Platform Services — Gateway Only (Never DGS)

These services are **never migrated to DGS**. Always Hive Gateway stitch. Classify all references as 🔵 BLUE unless business-critical.

| Loader Key | Service Class | URL | Schema File | Strategy |
|-----------|--------------|-----|------------|---------|
| `clazz` | `IgClazzService` | `stgapi-internal.target.com/item_groups/v1` | `IG_Clazz.graphql` | Gateway Stitch |
| `department` | `IgDepartmentService` | `stgapi-internal.target.com/item_groups/v1` | `IG_Department.graphql` | Gateway Stitch |
| `division` | `IgDivisionService` | `stgapi-internal.target.com/item_groups/v1` | `IG_Division.graphql` | Gateway Stitch |
| `brand` | `VmmBrandService` | `stgapi-internal.target.com` | `VMM_Brand.graphql` | Gateway Stitch |
| `vmm` | `VmmBusinessPartnerService` | `stgapi-internal.target.com` | `VMM_BusinessPartner.graphql` | Gateway Stitch |
| `location` | `VmmLocationService` | `spark-rfid-middleware.dev.target.com` | `VMM_Location.graphql` | Gateway Stitch |
| `doppler` | `DopplerService` | `stgapi-internal.target.com/supply_plans_details/v1` | `Doppler.graphql` | Gateway Stitch |
| `nexusAttributes` | `NexusAttributesService` | `stgapi-internal.target.com` | `NEXUS_Attributes.graphql` | Gateway Stitch |
| `ldap` | `LdapDirectoryService` | `stgapi-internal.target.com/ldap_directory_items/v1` | `LDAP_Directory.graphql` | Gateway Stitch |
| `coronaItems` | `CoronaItemService` | `stgapi-internal.target.com/items/v4/graphql/...` | *(none)* | Gateway Stitch |
| `apex` | `ApexService` | `stgapi-internal.target.com` | `APEX_ProductPlan.graphql` | Gateway Stitch |
| `assortmentItem` | `AssortmentItemService` | `stgapi-internal.target.com/items/v4/...` | `AssortmentItem.graphql` | Gateway Stitch |
| `negotiatorBids` | `NegotiatorBids` | `obcmedge.dev.target.com` | `SPARK_Negotiator.graphql` | Gateway Stitch |
| `brandCompliance` | `BrandComplianceService` | `stgapi-internal.target.com/brand_compliance_data/v1` | `OBDP_BrandCompliance.graphql` | Gateway Stitch |

### 2e. Reporting Services

| Loader Key | Service Class | URL | Schema File | Target DGS |
|-----------|--------------|-----|------------|-----------|
| `greenfield` | `GreenfieldService` | `stgapi-internal.target.com/bi_reporting_assets/v3/...` | `SPARK_Greenfield.graphql` | **ReportingService** |
| `insightsIntegration` | `InsightsIntegrationService` | `spark-insights-integration.dev.target.com` | `SPARK_InsightsIntegration.graphql` | **InsightsService** |

---

## 3. Utils Infrastructure — Analysis Requirements

When analyzing any domain (Phase 1 + 2), always analyze the utils files it references.

### Core HTTP Patterns (Referenced by Every Service)

| File | Purpose | DGS Equivalent |
|------|---------|----------------|
| `loadOne.js` | DataLoader GET with ACL, batching, transform | `@DgsDataLoader` + `MappedBatchLoaderWithContext` |
| `loadListing.js` | Parameterized listing loader | Spring `@Cacheable` or Feign client |
| `postOne.js` | POST with transform, DataLoader priming | Service method + Feign POST |
| `putOne.js` | PUT with transform | Service method + Feign PUT |
| `deleteOne.js` | DELETE builder | Service method + Feign DELETE |
| `convertFunctions.js` | `deepToCamelCase`/`deepToSnakeCase`, URL builders | Jackson ObjectMapper / DTO annotations |

### Shared Logic (Analyze When Referenced)

| File | Lines | Purpose |
|------|-------|---------|
| `commonLoaders.js` | 885 | ACL resolution, tag loading, relationship CRUD, bulk permissions |
| `accessControlUtils.js` | 54 | ACL JWT token, chunked permission loading |
| `workspaceAssociationHelper.js` | 78 | Manage workspace associations for BOM/Measurement/etc. |
| `batchingUtils.js` | 18 | Parallel/sequential batch chunking |
| `circuitBreaker.js` | — | Resilience patterns → Resilience4j |
| `cache.js` / `lruCache.js` | — | Caching → Spring Cache / Redis |
| `resolvePaging.js` | — | Pagination helpers → Spring Pageable |

### Domain-Specific Utils (Analyze With Owning Domain)

| File | Domain |
|------|--------|
| `bomUtils.js` | BOM |
| `ProductAskUtils.js` | Product Ask |
| `Product/productUtils.js` | Product |
| `Product/attachmentUtils.js` | Product/Attachment |
| `Product/partnerUtils.js` | Product |
| `Product/teamUtils.js` | Product |
| `Product/userGroupUtils.js` | Product |
| `Product/getReservedDpcisFromApex.js` | Product/APEX |
| `materials/colorUtils.js` | Color |
| `materials/resourceLinkUtils.js` | Materials |
| `Reporting/queryUtil.js` | Reporting |
| `packaging/getRetailPriceByDpci.js` | Packaging |
| `variantIdFunctions.js` | Product |
| `vmmUtils.js` | VMM |
| `discussionUtils.js` | Discussion |
| `sampleUtils.js` | Sample |
| `sortBpByName.js` | BusinessPartner |

---

## 4. Output Organization

```
output/
├── SHARED_FINDINGS.md              # Cross-domain shared investigation findings
├── product/
│   ├── 01-schema-inventory.md
│   ├── 02-resolver-analysis.md
│   ├── 03-schema.graphql
│   ├── 03-schema-analysis.md
│   ├── 04-stories.md
│   └── 04-po-summary.md
├── bom/
│   └── ...
└── {domain}/
    └── ...
```

**Directory naming:** kebab-case matching the loader key: `product`, `bom`, `product-details`, `product-variation`, `access-control`, etc.

---

## 5. Lessons Learned

Apply these patterns to every domain investigation.

### Large Resolver Files (1000+ Lines)

- Read in 500-line windows
- Track progress by resolver type: queries first, then mutations, then field resolvers
- Expect 50+ field resolvers in large domains — budget analysis time accordingly
- Product domain: 2,629 lines, ~60 min for full Phase 2

### Polymorphic Type Resolution (`__resolveType`)

- BOM has a `BomMaterial` interface with 7 concrete variants
- Document each concrete type and its resolution condition
- DGS equivalent: `@DgsTypeResolver` on the interface class
- Count each variant as a separate test case

### Internal vs External User Bifurcation

- Some domains branch on `context.user.isExternal`
- Document BOTH code paths explicitly in Phase 2
- This is a +1 complexity bump — always apply

### Cross-Domain Component Aggregation

- Product's `components` resolver pulls from BOM, Measurement, Claim, ProductDetail, Packaging
- Always HIGH complexity — budget 8–13 days
- Requires batched ACL permission checking
- Elastic search queries may differ from backend queries

### Story ID Convention

- `SPARK-{DOMAIN_ABBREV}-{PHASE_LETTER}{SEQUENCE}` (e.g., `SPARK-PROD-A01`, `SPARK-BOM-B02`)
- Phase-letter grouping (A–G) maps directly to sprints
- Technical category (CAT-1–5) is metadata on each story, not the grouping key

### Effort Calibration (From Real Analysis)

- Simple query/mutation (single REST call): 1–3 days
- Medium resolver (2–3 service calls, some transformation): 3–5 days
- Complex orchestration (4+ services, parallel calls, ACL): 5–8 days
- Very High (cross-domain aggregation, 10+ steps): 8–13 days
- Always add +20% buffer to domain totals
