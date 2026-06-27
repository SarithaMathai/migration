# Phase 3 — Federation Schema Analysis (`product` domain)

> **Domain:** `product`
> **Target DGS:** `plm-product` (Kotlin / Netflix DGS, Spring Boot)
> **Mode:** Green-field (no existing DGS schema)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18
> **Depends on:** [01-schema-inventory.md](output/product/01-schema-inventory.md), [02-resolver-analysis.md](output/product/02-resolver-analysis.md), [02-resolver-analysis-mutations.md](output/product/02-resolver-analysis-mutations.md), [02-resolver-analysis-fields.md](output/product/02-resolver-analysis-fields.md), [02-resolver-analysis-services.md](output/product/02-resolver-analysis-services.md)
> **Output:** [03-schema.graphql](output/product/03-schema.graphql)

---

## 1. Existing-DGS Scan

| Item | Result |
|---|---|
| Target repo `plm-product` present in workspace? | **No** — green-field migration |
| Existing DGS schema files | **None** |
| Commented-out / placeholder fields to inherit | **None** |
| Conflicting type definitions | **None** |

All 90+ types in the derived schema are tagged 🔜 (needs migration). No ✅ (already-in-DGS) entries.

---

## 2. Naming-Convention Decisions

| Source name | DGS name | Rule |
|---|---|---|
| `SPARK_Product`, `SPARK_ProductStatus`, `SPARK_ProductBulkType`, `SPARK_ProductsPaged`, `SPARK_ProductsCategories`, `SPARK_ProductTemplatesList`, `SPARK_MasterProductStatus`, `SPARK_ProductRules`, `SPARK_AvailableRules`, `SPARK_ResourcesCount`, `SPARK_AttachmentSummary`, `SPARK_ProductCopy`, `SPARK_AncestryProducts`, `SPARK_ChildProducts`, `SPARK_Rating`, `SPARK_Tcin`, `SPARK_PartnerTcins`, `SPARK_PartnerReservedDpci`, `SPARK_ReservedDpci`, `SPARK_PackagingAttribute`, `SPARK_ProductMaterials`, `SPARK_ProductLibraryResource`, `SPARK_CodeName`, `SPARK_PurchaseOrderDetails`, `SPARK_ProductCopyResources`, `SPARK_ProductWorkspaceAttributes`, `SPARK_ProductWorkspaceInfo`, `SPARK_WorkspaceInfoPartner`, `SPARK_CarryForwardProductStatus`, `SPARK_CarryForwardProductAllStatus`, `SPARK_ProductTemplateAttachments`, `SPARK_ProductTemplateStatus`, `SPARK_ProductComponentsCounts`, `SPARK_Attachment_With_Meta_Data`, `SPARK_SearchSamplesPaged`, `SPARK_SearchAttachmentsPaged`, `SPARK_SearchComponentsPaged`, `SPARK_DiscussionElastic`, `SPARK_TeamPaged`, `SPARK_TeamPagedV2`, `SPARK_WorkspacesPagedV2`, `SPARK_Tag_Elastic`, `SPARK_Filter_SetDates`, `SPARK_Status`, `SPARK_FilterSampleType`, `SPARK_FilterSampleFormat`, `SPARK_Packaging_Field`, `SPARK_Categories` (union), `SPARK_Paging`, `SPARK_Pageable`, `SPARK_CodeDescription`, `SPARK_CodeDescriptionOrder` | Drop `SPARK_` prefix | Convention |
| `CORONA_ItemDetails` | `CORONA_ItemDetails` | **Keep** — external platform stub |
| `VMM_*`, `IG_*`, `DOPPLER*` | unchanged | **Keep** — external platform stubs |
| `Bulk_CarryForwardProductInput` | `BulkCarryForwardProductInput` | Normalize naming |
| `Spark_bomMaterialDtosInput` | `BomMaterialDtosInput` | Drop prefix, normalize casing |
| `Attachment_With_Meta_Data` (after prefix drop) | `AttachmentWithMetaData` | PascalCase normalization |

---

## 3. Type Classification

### 3.1 Owned types (Product subgraph) — 40+
`Product` (primary), `ResourcesCount` (composite-key), `ProductStatus`, `ProductVendorAttributes`, `CarryForwardProductStatus`, `CarryForwardProductAllStatus`, `MasterProductStatus`, `ProductWorkspaceAttributes`, `ProductWorkspaceInfo`, `WorkspaceInfoPartner`, `ProductBulkType`, `ProductsPaged`, `ProductTemplatesList`, `ProductsCategories`, `ProductCopy`, `ProductCopyResources`, `Rating`, `ChildProducts`, `AncestryProducts`, `PartnerTcins`, `PartnerReservedDpci`, `Tcin`, `ReservedDpci`, `PurchaseOrderDetails`, `CodeName`, `ProductMaterials`, `ProductLibraryResource`, `PackagingAttribute`, `SpgFileLibrary`, `AttachmentSummary`, `AttachmentWithMetaData`, `Component`, `SearchAttachmentsPaged`, `SearchComponentsPaged`, `SearchSamplesPaged`, `BpCount`, `CountByComponent`, `CountByComponentStatus`, `Tag_Elastic`, `Filter_SetDates`, `Status`, `FilterSampleType`, `FilterSampleFormat`, `Packaging_Field`, `DopplerDepartment`, `ProductTemplateAttachments`, `ProductTemplateStatus`, `ProductComponentsCounts`, `VMM_BusinessPartnerCategory`, `ProductComponentStatus`, `ProductRules`, `AvailableRules`.

### 3.2 Composite-key entity — 1
| Type | Key | Owner of stub | Extending subgraphs |
|---|---|---|---|
| `ResourcesCount` | `@key(fields: "productId partnerId")` | Product subgraph (with workspaceContext + parentProductId as carried context) | attachment, discussion, sample, measurement, claim, bom, construction, watchlist (**N=8**) |

Per [federation-patterns.md §9](fedMigrationScripts/reference/federation-patterns.md) — Product defines the type; each owning subgraph adds `extend type ResourcesCount @key(fields: "productId partnerId") { … }` with `@requires` for non-key context fields. See §6 of this doc for story decomposition.

### 3.3 External-stub types (gateway-stitched, 🔵 BLUE)
| Stub | `@key` | Owner |
|---|---|---|
| `VMM_BusinessPartner` | `bpId` | VMM platform |
| `VMM_Brand` | `brandId` | VMM platform |
| `IG_Department` / `IG_Division` / `IG_Clazz` / `IG_Clazz_Filter` | `id` | Item Groups platform |
| `DopplerCapacityType` | `id` | Doppler platform |
| `CORONA_ItemDetails` | `tcinId` | Corona platform |

### 3.4 Co-located sibling-DGS stubs (same `plm-product` deployable, separate subgraphs)
| Stub | `@key` | Owner subgraph |
|---|---|---|
| `Attachment` | `id` | attachment |
| `SampleV2` | `id` | sample |
| `Tag` | `id` | tag |
| `WorkspaceV2` | `id` | workspace |
| `TeamV2` | `teamId` | team / user-profile |
| `UserProfileAttributes` | `id` | user-profile |
| `Discussion` | `discussionId` | discussion |
| `DiscussionThread` | `discussionThreadId` | discussion |
| `FileLibrary` | `id` | file-library |
| `Bom`, `Claim`, `Measurement`, `ProductDetail`, `Packaging` | `id` | respective component subgraphs |
| `ProductAsk` | `id` | product-ask |
| `ProductVariation` | `id` | product-variation |

### 3.5 Union — 1
| Union | Members |
|---|---|
| `Categories` | `VMM_Brand`, `IG_Department`, `IG_Division`, `IG_Clazz_Filter`, `ProductStatus`, `VMM_BusinessPartnerCategory`, `Tag_Elastic`, `Filter_SetDates`, `Status`, `FilterSampleType`, `FilterSampleFormat`, `Packaging_Field` |

DGS: implement via `@DgsTypeResolver(name = "Categories")` dispatching on `category.type`. **Default branch must return `IG_Clazz_Filter`** to preserve source behavior.

### 3.6 Shared utility types — 5
`Paging`, `Pageable`, `CodeDescription`, `CodeDescriptionOrder`, `AccessV3`, `WorkspaceStatus`, `ResourcePermissions`, `PermissionEntry`, `SpgFileLibrary` — all marked `@shareable` so multiple subgraphs may declare them without composition errors.

### 3.7 Input types — 30+
All input types prefix-stripped; one renamed (`Bulk_CarryForwardProductInput` → `BulkCarryForwardProductInput`). Inputs are never federated, never carry `@key`.

---

## 4. Query Gap Analysis — 18 operations (0 ✅ / 18 🔜 / 0 ⏭)

| # | Operation | Status | Complexity (Phase 2A) | Federation notes |
|---|---|---|---|---|
| Q1 | `getProducts` | 🔜 | High | Elastic listing + REST hydration (Phase 2A §1) |
| Q2 | `getProductTemplates` | 🔜 | Medium | Elastic listing with `includeBomTemplates` etc. flags |
| Q3 | `getProduct(id)` | 🔜 | Low | Single DataLoader call |
| Q4 | `getCopyStatus(id)` | 🔜 | Low | Non-batched REST |
| Q5 | `getCategories(type, …)` | 🔜 | Medium | Elastic facet — works with `ProductsCategories` polymorphic union |
| Q6 | `getProductsByIds(ids)` | 🔜 | Low | Batch REST |
| Q7 | `getProductStatus` | 🔜 | Low | Master data — cache in DGS |
| Q8 | `getProductTechPackCountV1(productId, partnerId, workspaceContext, parentProductId)` | 🔜 | **Very High** | Returns `ResourcesCount`. **Decomposes into:** 1 CAT-1 schema story (Product subgraph) + 1 CAT-3 facade story (aggregation service) + 8 CAT-4 placeholder stories (one per extending subgraph). See §6. |
| Q9 | `getProductTechPackBulkCountV1(bulk[])` | 🔜 | **Very High** | Bulk variant of Q8; same composite-key entity; **shares** CAT-4 stories. Phase 2A noted ordering-bug risk — fix during port. |
| Q10 | `getProductVersions(id)` | 🔜 | Low | Single REST call |
| Q11 | `getRatingByTcin(tcin)` | 🔜 | Low | External Bazaarvoice/Rating; silent null-on-error |
| Q12 | `getProductRules` | 🔜 | Low | **`spark_rules` service — confirm DGS placement** |
| Q13 | `getProductRulesById(id)` | 🔜 | Low | Same |
| Q14 | `getAllAvailableRules` | 🔜 | Low | Master data |
| Q15 | `getProductDeptRules(...)` | 🔜 | Medium | **`USE_NEW_RULES_API` flag** — delete legacy branch in DGS port |
| Q16 | `getProductBPRules(...)` | 🔜 | Medium | Same |
| Q17 | `searchProductRules(...)` | 🔜 | Medium | Same |
| Q18 | `getProductTemplateById(id)` | 🔜 | Low | Same DataLoader as `getProduct` |

---

## 5. Mutation Gap Analysis — 22 implemented + 3 schema-drift wrappers (0 ✅ / 22 🔜 / 3 ⏭)

| # | Operation | Status | Complexity (Phase 2B) | Notes |
|---|---|---|---|---|
| M1 | `addProduct` | 🔜 | Medium | Optional copy + workspace association |
| M2 | `addProducts` (bulk) | 🔜 | Medium | Bulk POST + attachment linking |
| M3 | `bulkUpdateProducts` | 🔜 | Medium | Bulk PUT mass_update |
| M4 | `updateProduct` | 🔜 | Medium | Update + optional copy + archive attachments |
| M5 | `addTeamsToProduct` | 🔜 | Medium | Adds teams/partners + workspace context |
| M6 | `removeProductResources` | 🔜 | Low | DELETE resources/bulk |
| M7 | `carryForwardProduct` | 🔜 | Medium | PUT carry_forward |
| M8 | `addBusinessPartnersToProductWithType` | 🔜 | Low | POST partners-add/bulk |
| M9 | `updateBusinessPartnerStatuses` | 🔜 | Low | PUT status_update/bulk |
| M10 | `updateViewToggle` | 🔜 | Low | PUT toggle |
| M11 | `productBusinessPartnerActions(actionType, values)` | 🔜 | **Very High** | 220-line dispatcher: REMOVE_PARTNER, DROP_PARTNER, UNDROP_PARTNER. JWT-curried writes. **Rollback strategy required.** |
| M12 | `updateWorkspaceAttributes` | 🔜 | Low | PUT workspaceAttributes |
| M13 | `updateProductTeamsWorkspaceContext` | 🔜 | Low | Team-workspace context update |
| M14 | `linkProduct` | 🔜 | Low | **Only mutation with `throwOnError:true`** — port as checked exception |
| M15 | `unlinkProduct` | 🔜 | Low | PUT unlink |
| M16 | `updateComponentStatus` | 🔜 | Low | Bulk component status update |
| M17 | `updateComponentStatuses` | 🔜 | **High** | 5-loader parallel fan-out (4 co-located + 1 claim EXT); shadow-var bug noted in Phase 2B |
| M18 | `addProductRule` | 🔜 | Low | POST `spark_rules/v1` |
| M19 | `updateProductRule` | 🔜 | Low | PUT `spark_rules/v1/{id}` |
| M20 | `deleteProductRule` | 🔜 | Low | DELETE `spark_rules/v1/{id}` |
| M21 (drift) | `removeProductBusinessPartner` | ⏭ | n/a | Declared, no resolver. Mark `@deprecated`; delete from schema if no consumers |
| M22 (drift) | `dropProductBusinessPartner` | ⏭ | n/a | Same |
| M23 (drift) | `unDropProductBusinessPartner` | ⏭ | n/a | Same |

---

## 6. Composite-Key Story Decomposition — `ResourcesCount`

Per [federation-patterns.md §9](fedMigrationScripts/reference/federation-patterns.md) and [techpack-migration-options.md](fedMigrationScripts/reference/techpack-migration-options.md) (Option D recommended):

| Story | Cat | Phase | Where tracked |
|---|---|---|---|
| Define `ResourcesCount` type + `@key(fields: "productId partnerId")` in Product subgraph | CAT-1 | A | `04-stories.md` (Product) |
| Product stub resolver returns key + context fields (productId, partnerId, workspaceContext, parentProductId) | CAT-2 | E | `04-stories.md` (Product) |
| Aggregation facade calls existing 10+ elastic queries (Phase 1) | CAT-3 | E | `04-stories.md` (Product) |
| `extend type ResourcesCount` resolver — attachment subgraph (`productAttachments`, `discussionAttachments`) | CAT-4 | F | Attachment domain `04-stories.md` |
| `extend type ResourcesCount` resolver — discussion subgraph (`discussions`) | CAT-4 | F | Discussion domain `04-stories.md` |
| `extend type ResourcesCount` resolver — sample subgraph (`sample`) | CAT-4 | F | Sample domain `04-stories.md` |
| `extend type ResourcesCount` resolver — measurement subgraph (`measurementSets`) | CAT-4 | F | Measurement domain `04-stories.md` |
| `extend type ResourcesCount` resolver — claim subgraph (`claims`) | CAT-4 | F | Claim domain `04-stories.md` |
| `extend type ResourcesCount` resolver — bom subgraph (`productBoms`, `packagingBoms`, `boms`) | CAT-4 | F | BOM domain `04-stories.md` |
| `extend type ResourcesCount` resolver — construction subgraph (`constructions`) | CAT-4 | F | Construction domain `04-stories.md` |
| `extend type ResourcesCount` resolver — watchlist subgraph (`watchlists`) | CAT-4 | F | Watchlist domain `04-stories.md` |
| Retire aggregation facade after all 8 subgraphs live | CAT-4 | F | `04-stories.md` (Product) |

Until each domain is in scope, add a `BLOCKED-BY: {domain} migration` placeholder CAT-4 story in the **Product** `04-stories.md` (per framework guidance).

---

## 7. Resolver-to-Type Mapping Highlights

| Source field | Type contract | DGS pattern |
|---|---|---|
| `SPARK_Product.businessPartners(workspaceIdFilter)` | `[VMM_BusinessPartner]` | Returns `bpId`-only stubs; Hive Gateway joins VMM full type |
| `SPARK_Product.brand` / `brands` | `VMM_Brand` / `[VMM_Brand]` | Same — `brandId` stubs |
| `SPARK_Product.department` / `division` / `clazz` | IG stubs | `id` stubs; **`division` resolver port fixes the latent bug** (currently calls department loader) |
| `SPARK_Product.attachmentsV3` | `SearchAttachmentsPaged` | DataLoader-backed; ACL JWT forwarded via header |
| `SPARK_Product.components` | `SearchComponentsPaged` | Aggregates 5 sibling subgraphs (measurement/claim/bom/productDetail/packaging) — preserve `cloneDeep(initialCountsByBp)` semantics |
| `SPARK_Product.attachmentsWithMetaData` | `[AttachmentWithMetaData]` | Heaviest field resolver (150 lines); keep as `@DgsData` in Product subgraph backed by `AttachmentRelationResolver` service |
| `SPARK_Product.samples` | `[SampleV2]` | **Stop reading `info.variableValues`** — use explicit `@DgsContext` args |
| `SPARK_ProductsCategories.categories` | `[Categories]` (union) | 18-case switch becomes Kotlin dispatcher + per-branch fetchers |
| `SPARK_Categories.__resolveType` | resolver | `@DgsTypeResolver(name = "Categories")` with default→`IG_Clazz_Filter` |
| `DopplerDepartment.primary/secondaryCapacityTypeName` | `String` | Single Doppler call shared (DataLoader memoization preserves request-scope caching) |

---

## 8. Risks & Open Questions

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `productBusinessPartnerActions` partial failure leaves products inconsistent (M11) | Medium | High | Define rollback or saga before Phase E story start | Tech Lead |
| `division` resolver bug — currently calls department loader for divisions | High | Medium | Fix during DGS port; contract tests for parity | Backend Eng |
| `USE_NEW_RULES_API` flag creates dual-code-path | High | Medium | Decide flag default (assume `true`) and delete legacy branch before Phase F | PO |
| Cross-domain `components` aggregation perf regression vs current parallel elastic | Medium | High | Validate federation latency; consider local aggregation in plm-product since 4 of 5 sources are co-located | Architects |
| TechPack composite-key approach (Option D) requires 8 owning subgraphs to extend `ResourcesCount` | High | High | Confirm Option D; place CAT-4 placeholders for blocked subgraphs | Tech Lead |
| `spark_rules` is a separate Java service — does it co-locate in `plm-product` or land in its own DGS? | Medium | Medium | Decide in Phase 4 kickoff; impacts schema split | Architects |
| `samples` field resolver reads `info.variableValues` — fragile | Medium | Medium | Document contract; switch DGS port to explicit args | Backend Eng |
| Hive Gateway federation v2.3 support / `@requires` on non-key context fields | Medium | High | Confirm before Phase H | Platform |
| `components` N+1 ACL per-claim (Phase 2C) regresses if ported naïvely | Medium | Medium | Refactor to single batched ACL call in DGS port | Backend Eng |
| `getCountByComponentStatus.incrementAllContextCounter` logic appears buggy in source | Low | Low | Verify intent; fix or pin as a test contract | Backend Eng |
| 3 hardcoded status-name tables (`convertFunctions.js`) flagged "must be removed" | High | Low | Replace with enums + Elasticsearch labels during port | Backend Eng |

### Open questions (for Phase 4 kickoff)
1. **TechPack approach:** confirm Option D (facade now + per-subgraph federate later). Alternative options summarized in [techpack-migration-options.md](fedMigrationScripts/reference/techpack-migration-options.md).
2. **`spark_rules` placement:** keep in `plm-product` or new subgraph?
3. **Schema-drift mutations (M21–M23):** delete or keep with `@deprecated`?
4. **`USE_NEW_RULES_API` flag default** and removal timing.
5. **Hive Gateway federation v2.3** compatibility — confirm with platform team.

---

## 9. Federation-Pattern Cheat Sheet (applied)

| Pattern (from [federation-patterns.md](fedMigrationScripts/reference/federation-patterns.md)) | Used by |
|---|---|
| **Owned entity** (`@key(fields:"id")`) | `Product`, `ProductRules` |
| **Composite key** (`@key(fields:"productId partnerId")`) | `ResourcesCount` |
| **External stub** (`@extends`, `@external`) | All 20+ stub types |
| **Gateway-only** | VMM, IG, Doppler, Corona |
| **Shared** (`@shareable`) | `Paging`, `Pageable`, `CodeDescription`, `CodeDescriptionOrder`, `AccessV3`, `WorkspaceStatus`, `ResourcePermissions`, `SpgFileLibrary` |
| **Union with `@DgsTypeResolver`** | `Categories` |
| **`@requires` for non-key context** | All 8 extending subgraphs of `ResourcesCount` |

---

**Phase 3 complete.** Outputs:
- [output/product/03-schema.graphql](output/product/03-schema.graphql) — derived DGS target schema
- [output/product/03-schema-analysis.md](output/product/03-schema-analysis.md) — this document

**Next:** reply `next` to proceed to **Phase 4** (migration stories grouped A–G + PO summary).

**Open questions to resolve before Phase 4 stories are finalized** are listed in §8.
