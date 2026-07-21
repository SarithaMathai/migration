# Phase 3: Schema Analysis — Product

> **Domain:** `product`
> **Target DGS:** `ProductService` (repo: `plm-product`, url: `https://spark-product.dev.target.com`)
> **Pipeline Version:** 1.1
> **Generated:** 2026-05-01
> **Depends on:** [be-01-schema-inventory.md](./be-01-schema-inventory.md), [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field (no existing DGS schema)

---

## Existing DGS Scan

> **Status:** Green-field migration — no existing DGS schema found in workspace.
> Target repo `plm-product` is not present locally. All operations classified as 🔜 (Needs migration).
> No commented-out fields to inherit. Naming conventions derived from source schema with `SPARK_` prefix dropped.

---

## Naming Convention Decisions

| Source Name | DGS Name | Rule |
|-------------|----------|------|
| `SPARK_Product` | `Product` | Drop `SPARK_` prefix |
| `SPARK_ProductStatus` | `ProductStatus` | Drop prefix |
| `SPARK_ProductsPaged` | `ProductsPaged` | Drop prefix |
| `SPARK_ProductTemplatesList` | `ProductTemplatesList` | Drop prefix |
| `SPARK_MasterProductStatus` | `MasterProductStatus` | Drop prefix |
| `SPARK_ProductRules` | `ProductRules` | Drop prefix |
| `SPARK_AvailableRules` | `AvailableRules` | Drop prefix |
| `SPARK_ResourcesCount` | `ResourcesCount` | Drop prefix |
| `SPARK_AttachmentSummary` | `AttachmentSummary` | Drop prefix |
| `SPARK_ProductCopy` | `ProductCopy` | Drop prefix |
| `SPARK_ProductBulkType` | `ProductBulkType` | Drop prefix |
| `SPARK_ProductsCategories` | `ProductsCategories` | Drop prefix |
| `SPARK_AncestryProducts` | `AncestryProducts` | Drop prefix |
| `SPARK_ChildProducts` | `ChildProducts` | Drop prefix |
| `CORONA_ItemDetails` | `CoronaItemDetails` | Drop `CORONA_` prefix; document as gateway stitch |
| `VMM_BusinessPartner` | `VMM_BusinessPartner` | Keep VMM prefix — external platform |
| `VMM_Brand` | `VMM_Brand` | Keep VMM prefix — external platform |
| `IG_Department` | `IG_Department` | Keep IG prefix — external platform |
| `IG_Division` | `IG_Division` | Keep IG prefix — external platform |
| `IG_Clazz` | `IG_Clazz` | Keep IG prefix — external platform |
| `DateTime` | `DateTime` | DGS extended scalar |
| `Bulk_CarryForwardProductInput` | `BulkCarryForwardProductInput` | Normalize naming convention |

---

## Type Classification Table

| Type | Category | Federation Key | Owning Service | Notes |
|------|----------|----------------|----------------|-------|
| `Product` | **Owned** | `@key(fields: "id")` | plm-product | Primary entity; `id` maps to `productId` in REST response |
| `ProductStatus` | **Owned** | none | plm-product | Embedded value object |
| `MasterProductStatus` | **Owned** | none | plm-product | Master data; no independent lookup needed |
| `ProductVendorAttributes` | **Owned** | none | plm-product | Embedded; computed from product + VMM data |
| `CarryForwardProductStatus` | **Owned** | none | plm-product | Embedded |
| `CarryForwardProductAllStatus` | **Owned** | none | plm-product | Embedded |
| `ProductBulkType` | **Owned** | none | plm-product | Response wrapper |
| `ProductsPaged` | **Owned** | none | plm-product | Response wrapper |
| `ProductTemplatesList` | **Owned** | none | plm-product | Response wrapper (type=101 products) |
| `ProductsCategories` | **Owned** | none | plm-product | Filter facets response |
| `ResourcesCount` | **Owned** | `@key(fields: "productId partnerId")` | plm-product | Composite key entity — Product defines the type and stub resolver; Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, and Watchlist subgraphs each `extend` it to resolve their own fields via `@requires`. See `reference/federation-patterns.md` §9 and `reference/techpack-migration-options.md`. |
| `AttachmentSummary` | **Owned** | none | plm-product | Embedded summary |
| `ProductCopy` | **Owned** | none | plm-product | Copy operation response |
| `ProductCopyResources` | **Owned** | none | plm-product | Embedded in ProductCopy |
| `ProductWorkspaceAttributes` | **Owned** | none | plm-product | Embedded; resolved from product data |
| `ProductWorkspaceInfo` | **Owned** | none | plm-product | Embedded; extended workspace info |
| `WorkspaceInfoPartner` | **Owned** | none | plm-product | Embedded |
| `Rating` | **Owned** | none | plm-product | Bazaarvoice rating — fetched by product service |
| `ChildProducts` | **Owned** | none | plm-product | Embedded in Product |
| `AncestryProducts` | **Owned** | none | plm-product | Embedded; includes parent + sibling products |
| `PartnerTcins` | **Owned** | none | plm-product | Embedded; TCINs per partner |
| `PartnerReservedDpci` | **Owned** | none | plm-product | Embedded; DPCI data from APEX |
| `Tcin` | **Owned** | none | plm-product | Embedded; references CoronaItemDetails (gateway stub) |
| `CoronaItemDetails` | **Owned** | none | plm-product | Fetched by Corona loader; returned as embedded value |
| `ReservedDpci` | **Owned** | none | plm-product | Embedded in PartnerReservedDpci |
| `CodeName` | **Owned** | none | plm-product | Embedded value |
| `ProductMaterials` | **Owned** | none | plm-product | Embedded |
| `ProductLibraryResource` | **Owned** | none | plm-product | Embedded |
| `PackagingAttribute` | **Owned** | none | plm-product | Embedded; `spg` field uses FileLibrary (internal) |
| `ProductRules` | **Owned** | none | plm-product | Rules data; departments/bps are gateway-stitched |
| `AvailableRules` | **Owned** | none | plm-product | Master data |
| `DopplerDepartment` | **Owned** | none | plm-product | Computed from Doppler data; IG fields gateway-stitched |
| `ProductTemplateAttachments` | **Owned** | none | plm-product | Embedded; references Attachment stubs |
| `ProductTemplateStatus` | **Owned** | none | plm-product | Embedded computed value |
| `ProductComponentsCounts` | **Owned** | none | plm-product | Embedded count |
| `PurchaseOrderDetails` | **Owned** | none | plm-product | Embedded in Tcin |
| `VMM_BusinessPartnerCategory` | **Owned** | none | plm-product | Filter category; id/name from VMM |
| `ProductComponentStatus` | **Owned** | none | plm-product | Embedded status |
| `AttachmentWithMetaData` | **Owned** | none | plm-product | Enriched attachment wrapper |
| `VMM_BusinessPartner` | **External stub** | `@key(fields: "bpId")` | VMM Gateway | Gateway-only; Product DGS returns `bpId` key only |
| `VMM_Brand` | **External stub** | `@key(fields: "brandId")` | VMM Gateway | Gateway-only |
| `IG_Department` | **External stub** | `@key(fields: "id")` | IG Gateway | Gateway-only |
| `IG_Division` | **External stub** | `@key(fields: "id")` | IG Gateway | Gateway-only |
| `IG_Clazz` | **External stub** | `@key(fields: "id")` | IG Gateway | Gateway-only |
| `Tag` | **External stub** | `@key(fields: "id")` | Tag DGS | Co-located DGS in plm-product; federation |
| `Attachment` | **External stub** | `@key(fields: "id")` | Attachment DGS | EXT domain |
| `SampleV2` | **External stub** | `@key(fields: "id")` | Sample DGS | EXT domain |
| `WorkspaceV2` | **External stub** | `@key(fields: "id")` | Workspace DGS | EXT domain |
| `TeamV2` | **External stub** | `@key(fields: "teamId")` | UserProfile DGS | EXT domain |
| `UserProfileAttributes` | **External stub** | `@key(fields: "id")` | UserProfile DGS | EXT domain |
| All `*Input` types (30) | **Input** | n/a | plm-product | Input types |
| `Paging`, `Pageable` | **Shared** | n/a (shared) | plm-product | `@shareable` — utility across domains |
| `CodeDescription`, `CodeDescriptionOrder` | **Shared** | n/a (shared) | plm-product | `@shareable` — used in many domains |

---

## Query Gap Analysis

Summary: 0 ✅ | 18 🔜 | 0 ⏭ — 18 total

| # | Source Operation | DGS Status | Notes |
|---|-----------------|-----------|-------|
| 1 | `getProducts(page, size, q, filter, ...): ProductsPaged` | 🔜 | Dual elastic+REST call; elastic for IDs, REST for hydration |
| 2 | `getProductTemplates(page, size, q, filter, types, ...): ProductTemplatesList` | 🔜 | Elastic-only; returns products of type=101 |
| 3 | `getProduct(id: ID!): Product` | 🔜 | Single DataLoader call; straightforward |
| 4 | `getCopyStatus(id: ID!): ProductCopy` | 🔜 | Single non-batched REST call |
| 5 | `getCategories(type, resourceId, resourceType, productType): ProductsCategories` | 🔜 | Elastic facet search; complex categories resolver with 16 switch cases |
| 6 | `getProductsByIds(ids: [ID]!): ProductsPaged` | 🔜 | Batch REST call by ID list |
| 7 | `getProductStatus: [MasterProductStatus]` | 🔜 | Simple master data call |
| 8 | `getProductTechPackCountV1(productId, partnerId, workspaceContext, parentProductId): ResourcesCount` | 🔜 | Very High — 10+ parallel elastic queries + ACL; returns composite key entity `ResourcesCount`. Decomposes into: 1 CAT-1 schema story + 1 Phase E stub+facade story (Product subgraph) + 8 CAT-4 placeholder stories (one per owning subgraph: Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist). See `reference/techpack-migration-options.md` Option D. |
| 9 | `getProductTechPackBulkCountV1(bulkTechPackCountResource): [ResourcesCount]` | 🔜 | Very High — parallel calls to Q8 logic; same `ResourcesCount` composite key entity. Decomposes identically to Q8; bulk wrapper story added in Phase E. |
| 10 | `getProductVersions(id: ID!): ProductsPaged` | 🔜 | Single REST call to versions endpoint |
| 11 | `getRatingByTcin(tcin: String): Rating` | 🔜 | Bazaarvoice external call; silent null on error |
| 12 | `getProductRules: [ProductRules]` | 🔜 | GET all rules — simple listing |
| 13 | `getProductRulesById(id: ID!): ProductRules` | 🔜 | Non-batched GET by ID |
| 14 | `getAllAvailableRules: [AvailableRules]` | 🔜 | Simple listing |
| 15 | `getProductDeptRules(productIds, departmentIds, activeOnly): [ProductRules]` | 🔜 | Feature-flag: routes to RuleLibrary or Product API |
| 16 | `getProductBPRules(productIds, businessPartnerIds, activeOnly): [ProductRules]` | 🔜 | Same flag dispatch as Q15 |
| 17 | `searchProductRules(productIds, departmentIds, businessPartnerIds, activeOnly): [ProductRules]` | 🔜 | Same flag dispatch; uses search_mapped endpoint |
| 18 | `getProductTemplateById(id: ID!): Product` | 🔜 | Delegates to same DataLoader as getProduct |

---

## Mutation Gap Analysis

Summary: 0 ✅ | 22 🔜 | 1 ⏭ — 23 total

| # | Source Operation | DGS Status | Notes |
|---|-----------------|-----------|-------|
| 1 | `addProduct(workspaceId, sparkProduct, copyProduct): Product` | 🔜 | Create + workspace + optional copy |
| 2 | `updateProduct(input, copyProduct): Product` | 🔜 | Update + archive attachments + optional copy |
| 3 | `carryForwardProduct(productId, carryForwardProductInput): Product` | 🔜 | PUT carry_forward endpoint |
| 4 | `bulkUpdateProducts(products): ProductBulkType` | 🔜 | Bulk PUT via mass_update |
| 5 | `addProducts(workspaceId, products): ProductBulkType` | 🔜 | Bulk create + attachment linking + workspace add |
| 6 | `addTeamsToProduct(productId, teamIds, workspaceIds, newPartners): Product` | 🔜 | Add teams/partners + workspace context update |
| 7 | `addBusinessPartnersToProductWithType(productId, partners): Product` | 🔜 | POST partners-add/bulk |
| 8 | `removeProductResources(productId, resourceIds): Product` | 🔜 | DELETE resources/bulk |
| 9 | `removeProductBusinessPartner(productId, partnerId): Product` | ⏭ | Internal sub-op — expose only via actionType=REMOVE_PARTNER |
| 10 | `updateBusinessPartnerStatuses(productId, statusInput): Product` | 🔜 | PUT status_update/bulk |
| 11 | `productBusinessPartnerActions(actionType, values): Product` | 🔜 | Very High — DROP_UNDROP + relationship tree + ACL + samples |
| 12 | `updateViewToggle(toggleInput): Product` | 🔜 | PUT view toggle |
| 13 | `updateWorkspaceAttributes(productId, workspaceAttributesInput): Product` | 🔜 | PUT workspace attributes |
| 14 | `dropProductBusinessPartner(productId, partnerId): Product` | 🔜 | POST partner drop |
| 15 | `unDropProductBusinessPartner(productId, partnerId): Product` | 🔜 | POST partner undrop |
| 16 | `updateProductTeamsWorkspaceContext(productId, ...): Product` | 🔜 | Update team-workspace context |
| 17 | `linkProduct(parentProductId, childProductId): Product` | 🔜 | Link child to parent |
| 18 | `unlinkProduct(parentProductId, childProductId): Product` | 🔜 | Unlink child from parent |
| 19 | `addProductRule(rule): ProductRules` | 🔜 | POST new rule |
| 20 | `updateProductRule(rule): ProductRules` | 🔜 | PUT update rule |
| 21 | `deleteProductRule(ruleId): Boolean` | 🔜 | DELETE rule |
| 22 | `updateComponentStatus(productComponents): Product` | 🔜 | Bulk component status update |
| 23 | `updateComponentStatuses(productId, ids, status): Product` | 🔜 | Component status by IDs |

---

## External Type Stubs (Gateway-Only)

These types are never migrated to DGS — Hive Gateway resolves them via stitching.

| Stub Type | Owned By | @key | Pattern |
|-----------|---------|------|---------|
| `VMM_BusinessPartner` | VMM platform | `bpId` | Product returns `bpId` only; gateway fetches full type |
| `VMM_Brand` | VMM platform | `brandId` | Product returns `brandId` only |
| `IG_Department` | Item Groups | `id` | Product returns `id` only |
| `IG_Division` | Item Groups | `id` | Product returns `id` only |
| `IG_Clazz` | Item Groups | `id` | Product returns `id` only |

---

## Risks and Recommendations

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| `productBusinessPartnerActions DROP_UNDROP` partial failure leaves products in inconsistent state | Medium | High | Define rollback strategy before Phase E | Tech Lead |
| `division` resolver BUG in source calls wrong loader | High | Medium | Fix in DGS (do not replicate bug); document for gateway team | Backend Eng |
| `USE_NEW_RULES_API` flag creates dual-code-path in DGS | High | Medium | Decide flag default before Phase F | PO |
| `components` cross-domain aggregation complexity | High | High | Validate federation strategy; see `reference/stitching-patterns.md` | Architects |
| TechPack orchestration migration approach | High | High | Confirm Option B/C/D in `reference/techpack-migration-options.md` before Phase E stories start; Option D (facade now, federate per-subgraph later) is recommended. `ResourcesCount` must use `@key(fields: "productId partnerId")` composite key. | Tech Lead |
| Hive Gateway federation v2.3 support | Medium | High | Confirm before Phase H | Platform |

---

**Phase Completed:** Phase 3 — Federation Schema Derivation
**Domain:** `product`
**Analysis Mode:** Full
**DGS Target:** Green-field
**Skills Applied:** federation-candidate-detection, federation-schema-derivation
**Files Analyzed:** 18 files (Phase 1+2 output)
**Target Service:** `ProductService` (plm-product)
**EXT Service Calls Found:** 29 (from Phase 2)
**Output Files Written:**
- `output/product/be-03-schema.graphql`
- `output/product/be-03-schema-analysis.md`
**Next Phase:** Phase 4 — Migration Story Generation: `Generate migration stories for product — Phases 1, 2, and 3 are done.`
**Open Questions:**
- Confirm TechPack migration option (B/C/D) before Phase E story generation. `ResourcesCount` @key and sub-story decomposition are documented in `reference/federation-patterns.md` §9.
- Confirm `removeProductBusinessPartner` exposure decision (⏭ or standalone mutation)
