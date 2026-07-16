# Frontend Migration Stories — Phase-1 Domains

> Phase 8 deliverable · Hand-authored source of truth (parsed by `generate_frontend.py` for Jira CSVs, the dependency matrix and traceability) · 2026-07-16
> Story id format: `<DOMAIN>-FE-<NNN>` (domain tokens match the backend ids: PRODUCT, BOM, MST, PDTL, PKG, WATCHLIST, IMPRESSION, CLAIM).
> Rule: a frontend story is Done only after every backend story it depends on has been delivered.
> Platform enablement (former PLATFORM-FE-001…005: router flag, codegen, cache remap, fragment sweep, dynamic-gql expansion) is **complete** — it is an assumed baseline, not a dependency, for every story below.

---

## Product

### PRODUCT-FE-001 · Migrate `getProduct` documents in product-queries

- **Type:** Query migration · **Impact:** High · **Domain:** product
- **Depends on:** PRODUCT-BE-B-01
- **Operations:** `getProduct`

- **Business objective:**
  - Product detail, scaffolding, files and team screens read from the federated graph with unchanged behaviour.
- **Technical objective:**
  - Re-point every `getProduct`-rooted document in `product-queries` (detail, scaffolding, workspaces, status-update info, files/components, teams) to federated shapes.
- **Background / current implementation:**
  - 10+ documents in `src/libs/product-queries/src/queries/ProductQueries.tsx`, `ProductFilesQueries.tsx`, `TeamTabQueries.ts`, `WorkspaceFilesQueries.ts` share the `getProduct` resolver; widest selections in the estate (`getProductScaffolding` 131 fields).
- **Required changes:**
  - Fragment re-targeting; nested-entity selections for `createdBy`/`brand`/`department`.
  - TypeScript model and hook generic updates; mock/snapshot regeneration.
  - Attachment/discussion sub-selections stay entity-stitched — no document split.

#### Acceptance Criteria

1. Product detail, files, teams and scaffolding screens render identically under the flag.
2. No selection requests a field absent from the federated `Product` type.
3. Cache normalizes one `Product` entity across all migrated documents.

#### Testing

- Side-by-side JSON diff of legacy vs federated responses per document; full product-screen integration suite under the flag.

- **Risk:** High — largest regression surface in phase 1.
- **Estimated effort:** 10–15 days

### PRODUCT-FE-002 · Migrate shared-library `getProduct` consumers

- **Type:** Query migration · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-B-01, PRODUCT-BE-B-04, PRODUCT-FE-001
- **Operations:** `getProduct`, `getProductVersions`

- **Business objective:**
  - Breadcrumbs, discussion panes, admin views and packaging DPCI lookups keep working after product cutover.
- **Technical objective:**
  - Migrate `getProduct`-rooted documents outside `product-queries`: `spark-legacy` breadcrumbs, `core-discussions`/`LegacyDiscussionQueries` team reads, `spark-ui-admin` (`getProductById`, `getProductVersions`), `product-packaging` (`getDpciInfo`).
- **Background / current implementation:**
  - 8 documents across 4 libraries duplicate slim `getProduct` selections.
- **Required changes:**
  - Same re-pointing pattern as PRODUCT-FE-001; consolidate duplicate slim selections onto a shared base fragment where identical.

#### Acceptance Criteria

1. Breadcrumb, discussion team pane, admin product view and DPCI lookup render identically under the flag.
2. Duplicate selections reduced to shared fragments where shapes match.

#### Testing

- Component tests per consumer library; snapshot regeneration.

- **Risk:** Medium — many small consumers, low individual complexity.
- **Estimated effort:** 5–8 days

### PRODUCT-FE-003 · Migrate product list and bulk reads

- **Type:** Query migration · **Impact:** High · **Domain:** product
- **Depends on:** PRODUCT-BE-S-02, PRODUCT-BE-B-02
- **Operations:** `getProducts`, `getProductsByIds`

- **Business objective:**
  - Workspace product listings and bulk flows read from the federated graph without pagination or filter regressions.
- **Technical objective:**
  - Migrate `getProducts` (list/search, 88-field document) and `getProductsByIds` (bulk discussion data, file metadata) documents.
- **Background / current implementation:**
  - `product-queries/ProductQueries.tsx`, `product-common/WorkspaceProductsQueries.ts`, `workspaces/BulkDiscussionQueries.ts`, `spark-legacy` vendor merge.
- **Required changes:**
  - Await the search-cutover decision carried by PRODUCT-BE-S-02 (elastic read-hub) — list shapes must not be migrated twice.
  - `getBulkDiscussionData` also selects an access-control root (out of scope): keep that document on the legacy gateway until the access-control phase, or split (decision recorded in-story at grooming).

#### Acceptance Criteria

1. List pagination, sorting and filters behave identically under the flag.
2. The cross-domain document's routing decision is implemented and documented.

#### Testing

- List-screen integration tests with pagination fixtures; bulk-flow smoke tests.

- **Risk:** High — blocked by the search spike outcome.
- **Estimated effort:** 8–12 days

### PRODUCT-FE-004 · Migrate product status and workspace-context reads

- **Type:** Query migration · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-B-03
- **Operations:** `getProductStatus`

- **Business objective:**
  - Status chips, workspace metrics and connected-component status views stay accurate per workspace.
- **Technical objective:**
  - Migrate the 4 `getProductStatus`-rooted documents (form data, status-update info, connected components, workspace metrics report count).
- **Background / current implementation:**
  - `getFormData` (132 fields, 5 root fields) is the widest multi-root document in the estate; also selects a tags root (out of scope).
- **Required changes:**
  - Migrate product roots; hold `getFormData` on the legacy gateway until its tags root migrates, or split into two documents (per [fe-07-network-call-analysis.md §2.1](./fe-07-network-call-analysis.md)).
  - Workspace-filter arguments (`workspaceIdFilter`, `partnerIdFilter`) unchanged — verify against federated `ProductStatus`.

#### Acceptance Criteria

1. Status values match legacy per workspace/partner filter combination.
2. `getFormData` routing decision implemented and documented.

#### Testing

- Fixture matrix across workspace/partner filters; form-screen integration test.

- **Risk:** Medium.
- **Estimated effort:** 5–8 days

### PRODUCT-FE-005 · Migrate template library and categories reads

- **Type:** Query migration · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-C-02, PRODUCT-BE-C-03
- **Operations:** `getProductTemplates`, `getCategories`

- **Business objective:**
  - Template library browsing and template-driven creation keep working, including the claim/measurement/size template composition.
- **Technical objective:**
  - Migrate `getProductTemplates` (3 documents, one selecting 208 fields via 12 fragments) and `getCategories` (3 documents).
- **Background / current implementation:**
  - `spark-legacy/templateLibrary/ProductTemplateQueries.tsx`, `claims/ClaimQueries.ts`, `product-common/WorkspaceProductsQueries.ts`.
  - The wide template document embeds fragments defined outside the inventoried libraries (`sizeTemplateFragmentWithRows`, `measurementTemplateFragment`) — locate and inventory them during implementation.
- **Required changes:**
  - Fragment re-target + document re-point; close the fragment inventory gap.

#### Acceptance Criteria

1. Template library lists, previews and clone-from-template flows render identically.
2. The two externally defined fragments are located, inventoried and migrated.

#### Testing

- Template library integration suite; clone-flow smoke test.

- **Risk:** Medium — widest fragment composition in phase 1.
- **Estimated effort:** 5–8 days

### PRODUCT-FE-006 · Migrate product rules administration

- **Type:** Query + mutation migration · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-B-07, PRODUCT-BE-B-08, PRODUCT-BE-B-09, PRODUCT-BE-B-10, PRODUCT-BE-B-11, PRODUCT-BE-C-05, PRODUCT-BE-D-15, PRODUCT-BE-D-16, PRODUCT-BE-D-17
- **Operations:** `getProductRules`, `getProductRulesById`, `getAllAvailableRules`, `getProductDeptRules`, `getProductBPRules`, `searchProductRules`, `addProductRule`, `updateProductRule`, `deleteProductRule`

- **Business objective:**
  - Rules administration (admin console) is fully functional on the federated graph.
- **Technical objective:**
  - Migrate the 9 rules operations in `spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` as one vertical slice.
- **Background / current implementation:**
  - Self-contained admin flow; shared `PRODUCT_RULES_FIELDS_FRAGMENT`.
  - `SPARK_ProductRules.businessPartners` is deprecated ("use rule attribute") and still selected.
- **Required changes:**
  - Replace the deprecated `businessPartners` selection with the rule-attribute shape before cutover.
  - Re-point all 9 documents together (single flag scope).

#### Acceptance Criteria

1. Rule list, search, create, update and delete work end-to-end under the flag.
2. No selection references `businessPartners` on the rules type.

#### Testing

- Admin rules CRUD integration test; search fixture tests.

- **Risk:** Low — isolated admin surface.
- **Estimated effort:** 4–6 days

### PRODUCT-FE-007 · Migrate simple product mutations

- **Type:** Mutation migration · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-D-01, PRODUCT-BE-D-02, PRODUCT-BE-D-03, PRODUCT-BE-D-04, PRODUCT-BE-D-05, PRODUCT-BE-D-10, PRODUCT-BE-D-13, PRODUCT-BE-D-14
- **Operations:** `addProduct`, `addProducts`, `updateProduct`, `bulkUpdateProducts`, `carryForwardProduct`, `updateViewToggle`, `linkProduct`, `unlinkProduct`

- **Business objective:**
  - Product create, edit, bulk-edit, carry-forward and link flows write through the federated graph.
- **Technical objective:**
  - Migrate the 8 single-step product mutations and their cache updates.
- **Background / current implementation:**
  - Spread across `product-queries`, `product-common`, `spark-legacy`; several rely on `refetchQueries` after thin responses.
- **Required changes:**
  - Input type renames (`SPARK_*Input` → federated inputs); response selections aligned to returned entities.
  - Replace blanket `refetchQueries` with `update`-function cache writes where the mutation returns the entity (per [fe-07-network-call-analysis.md §2.3](./fe-07-network-call-analysis.md)).

#### Acceptance Criteria

1. Each flow completes and the UI reflects the write without a manual refresh.
2. No migrated mutation triggers a full-document refetch that its response payload makes redundant.

#### Testing

- Mutation unit tests with cache assertions; create/edit/link E2E happy paths.

- **Risk:** Medium.
- **Estimated effort:** 6–10 days

### PRODUCT-FE-008 · Migrate team and partner assignment mutations

- **Type:** Mutation migration · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-D-06, PRODUCT-BE-D-07, PRODUCT-BE-D-12, PRODUCT-FE-001
- **Operations:** `addTeamsToProduct`, `addBusinessPartnersToProductWithType`, `updateProductTeamsWorkspaceContext`

- **Business objective:**
  - Team-tab management (add teams/partners, workspace context) writes through the federated graph.
- **Technical objective:**
  - Migrate the 3 team/partner mutations in `product-queries/TeamTabQueries.ts` with their team-tab read dependencies.
- **Background / current implementation:**
  - Mutations return slim payloads; team tab refetches `getProductWithTeams` after each write.
- **Required changes:**
  - Align response selections with federated team entities (`TeamV2.teamId` key).
  - Cache write on mutation response; keep one guarded refetch only where the payload is insufficient.

#### Acceptance Criteria

1. Add-team, add-partner and workspace-context flows work under the flag.
2. Team tab updates without a full refetch where the response carries the change.

#### Testing

- Team-tab integration suite; cache assertion tests.

- **Risk:** Medium.
- **Estimated effort:** 4–6 days

### PRODUCT-FE-009 · Migrate partner drop/undrop orchestration

- **Type:** Mutation migration (complex) · **Impact:** High · **Domain:** product
- **Depends on:** PRODUCT-BE-S-03, PRODUCT-BE-D-09
- **Operations:** `productBusinessPartnerActions`, `updateBusinessPartnerStatuses`

- **Business objective:**
  - Partner drop/undrop keeps its business guarantees (status cascades, not-removable rules) on the federated graph.
- **Technical objective:**
  - Migrate the orchestrated partner-action mutations once the backend orchestration design lands (ADR-012 — 🟠 draft, ratification pending; not-removable aggregation per ADR-016 — 🟠 draft).
- **Background / current implementation:**
  - `workspaces/workspaceMutations.ts` and `product-common/WorkspaceProductsQueries.ts`; today's dispatcher has un-awaited promise chains backend-side — response timing is unreliable and the UI compensates with refetches.
- **Required changes:**
  - Adopt the ratified mutation contract (single orchestrated mutation vs saga-status payload).
  - Explicit partial-failure UI: per-partner success/failure rendering instead of all-or-nothing toasts.
  - Remove compensating refetch logic tied to legacy timing behaviour.

#### Acceptance Criteria

1. Drop and undrop flows match the ratified contract, including partial-failure display.
2. Not-removable/undroppable partners are blocked client-side per the aggregated flags returned by the backend.

#### Testing

- Contract tests against the new mutation; E2E drop/undrop with induced partial failure.

- **Risk:** High — blocked on two draft ADR ratifications.
- **Estimated effort:** 8–12 days

### PRODUCT-FE-010 · Migrate TechPack count queries (facade-then-federate)

- **Type:** Query migration (staged) · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-E-03, PRODUCT-BE-E-04
- **Operations:** `getProductTechPackCountV1`, `getProductTechPackBulkCountV1`

- **Business objective:**
  - TechPack readiness counts remain correct on product list and detail screens through both migration steps.
- **Technical objective:**
  - Step 1 (facade): keep the current document shapes, re-point to the router (facade preserves the contract — ADR-015 Option B, 🟠 draft; facade-then-federate).
  - Step 2 (federate): replace the dedicated count queries with count fields selected on `Product` in existing documents.
- **Background / current implementation:**
  - `product-queries/ProductQueries.tsx` and `product-common/WorkspaceProductsQueries.ts`; the backend aggregates 7 sequential elastic queries per count.
- **Required changes:**
  - Step 1 is endpoint-only; Step 2 deletes 2 documents and extends `getProduct`/`getProducts` selections.

#### Acceptance Criteria

1. Counts identical to legacy in step 1 (facade parity check).
2. Step 2 removes the standalone count round trips on the product list screen.

#### Testing

- Parity fixtures step 1; screen-level request-count assertion step 2.

- **Risk:** Medium — two-step delivery, second step gated on federation of the counts.
- **Estimated effort:** 4–6 days (step 1) + 4–6 days (step 2)

### PRODUCT-FE-011 · Migrate component status rollups

- **Type:** Query + mutation migration · **Impact:** Medium · **Domain:** product
- **Depends on:** PRODUCT-BE-B-01, PRODUCT-BE-D-18, PRODUCT-BE-E-02
- **Operations:** `getProduct`, `updateComponentStatus`, `updateComponentStatuses`

- **Business objective:**
  - Component status counts and bulk status updates behave identically on the federated graph.
- **Technical objective:**
  - Migrate `getProductComponentStatusCounts` (rooted on `getProduct`) and the two component-status mutations under the counts-rollup design (ADR-014 — 🟠 draft, ratification pending).
- **Background / current implementation:**
  - `product-queries/ProductFilesQueries.tsx` reads rollup counts; `spark-legacy` connected-components flows write statuses singly and in bulk.
- **Required changes:**
  - Adopt the ratified rollup field shapes; align bulk mutation payload with per-item results.

#### Acceptance Criteria

1. Rollup counts equal legacy values across fixture products.
2. Bulk status update renders per-item outcomes.

#### Testing

- Rollup parity fixtures; bulk-update integration test.

- **Risk:** Medium — gated on ADR-014 ratification.
- **Estimated effort:** 4–6 days

---

## BOM

### BOM-FE-001 · Statically expand BOM fragment factories (pre-cutover)

- **Type:** Refactor · **Impact:** High · **Domain:** bom
- **Depends on:** —
- **Operations:** —

- **Business objective:**
  - Unblock codegen and validation for every BOM document before cutover work starts.
- **Technical objective:**
  - Land the BOM share of the dynamic-gql static expansion (delivered platform pattern: `BUILD_FILES_FRAGMENT`, `BOM_FABRIC_SPEC_COMBO_DETAILS`) and regenerate all embedding documents in `product-queries/BomQueries.ts`.
- **Background / current implementation:**
  - The factories are embedded in the widest BOM read documents (`getBomByIds` variants); every downstream BOM story depends on their static form.
- **Required changes:**
  - Behaviour-neutral expansion on the legacy schema; document-text snapshot proves equivalence.

#### Acceptance Criteria

1. `BomQueries.ts` contains only static documents; codegen validates all of them.

#### Testing

- Document-text snapshots; existing BOM screen tests unchanged.

- **Risk:** Medium.
- **Estimated effort:** 3–4 days

### BOM-FE-002 · Migrate BOM core reads

- **Type:** Query migration · **Impact:** High · **Domain:** bom
- **Depends on:** BOM-BE-B-01, BOM-BE-B-03, BOM-BE-B-04, BOM-FE-001
- **Operations:** `getBomByIds`, `getBomByParentId`, `getBomStatus`, `getBomComponentStatus`

- **Business objective:**
  - BOM detail and status views read from the federated graph with unchanged behaviour.
- **Technical objective:**
  - Migrate the by-id/by-parent reads and status reads (3 `getBomByIds` variants with different selection widths).
- **Background / current implementation:**
  - `product-queries/BomQueries.ts` + `spark-ui-admin`; heavy fragment composition (`BomDetails`, `MaterialDetails`, supplier/combo fragments).
- **Required changes:**
  - Fragment re-target; nested entity selections for material/supplier references per the federated `Bom` schema.

#### Acceptance Criteria

1. BOM detail renders identically under the flag across fixture BOMs (fabric, trim, packaging component mixes).
2. One `Bom` cache entity is shared across all migrated documents.

#### Testing

- Response JSON diff per variant; BOM screen integration suite.

- **Risk:** High — widest fragment graph after product.
- **Estimated effort:** 6–10 days

### BOM-FE-003 · Migrate BOM search and elastic reads

- **Type:** Query migration · **Impact:** High · **Domain:** bom
- **Depends on:** BOM-BE-C-01, BOM-BE-S-03
- **Operations:** `getBomElastic`, `searchMaterialsBom`

- **Business objective:**
  - BOM listing and material search inside BOM keep parity through the search cutover.
- **Technical objective:**
  - Migrate `getBomElastic` and `searchMaterialsBom` after the elastic read-hub decision lands (BOM-BE-S-03 carries the spike outcome).
- **Background / current implementation:**
  - List screens page through elastic-backed results; `MAX_BOM_SEARCH_SIZE` constant caps page size client-side.
- **Required changes:**
  - Adopt ratified search shapes; verify paging/caps unchanged.

#### Acceptance Criteria

1. Search results, ordering and paging match legacy fixtures.

#### Testing

- Search fixture parity tests; list-screen pagination tests.

- **Risk:** High — blocked on the search spike.
- **Estimated effort:** 5–8 days

### BOM-FE-004 · Migrate BOM master-data reads

- **Type:** Query migration · **Impact:** Low · **Domain:** bom
- **Depends on:** BOM-BE-B-05, BOM-BE-B-06, BOM-BE-B-07, BOM-BE-B-08
- **Operations:** `getBomMaterialTypes`, `getBomPackagingMaterialTypes`, `getBomPackagingSubstrates`, `getBomPackagingUnitOfMeasure`

- **Business objective:**
  - BOM editors keep their dropdown/master data.
- **Technical objective:**
  - Re-point the 4 master-data queries (`getBomPackagingMasterData` document bundles several of them).
- **Background / current implementation:**
  - Static reference data, cached client-side per session.
- **Required changes:**
  - Endpoint re-point + type regeneration only; `cache-first` policy retained.

#### Acceptance Criteria

1. Dropdown contents identical; one fetch per session per master-data set.

#### Testing

- Fixture equality tests.

- **Risk:** Low.
- **Estimated effort:** 2–3 days

### BOM-FE-005 · Migrate BOM supplier reads

- **Type:** Query migration · **Impact:** Medium · **Domain:** bom
- **Depends on:** BOM-BE-C-03, BOM-BE-C-04, BOM-BE-C-05
- **Operations:** `getComboSupplierForBom`, `getValidTrimSuppliersForBom`, `getValidRawMaterialSuppliersForBom`

- **Business objective:**
  - Supplier pickers in the BOM editor stay accurate.
- **Technical objective:**
  - Migrate the 3 supplier-lookup queries (`getValidSuppliersForBom` document).
- **Background / current implementation:**
  - Supplier results join VMM business-partner data — flat partner fields may become `VMM_BusinessPartner` stubs.
- **Required changes:**
  - Selection updates for partner entity nesting; picker component model updates.

#### Acceptance Criteria

1. Picker options and disabled states match legacy fixtures.

#### Testing

- Picker component tests across fixture partner sets.

- **Risk:** Medium.
- **Estimated effort:** 3–5 days

### BOM-FE-006 · Migrate BOM mutations including `updateBom` saga handling

- **Type:** Mutation migration (complex) · **Impact:** High · **Domain:** bom
- **Depends on:** BOM-BE-D-01, BOM-BE-D-03, BOM-BE-D-04, BOM-BE-D-05, BOM-BE-S-01
- **Operations:** `addBom`, `lockBom`, `unlockBom`, `updateBom`, `updateBomComponentStatus`

- **Business objective:**
  - BOM create/edit/lock flows write through the federated graph with explicit partial-failure behaviour.
- **Technical objective:**
  - Migrate the 5 BOM mutations; adopt the saga contract for `updateBom` (3-step write, no rollback today — ADR-013, 🟠 draft; BOM-BE-S-01 carries the decision).
- **Background / current implementation:**
  - `updateBom` failures today can leave partial state that the UI cannot detect; the editor refetches after every save.
- **Required changes:**
  - Saga-status rendering on save (per-step success/failure); retry affordance per the ratified contract.
  - Lock/unlock and component-status mutations are single-step re-points with cache writes.

#### Acceptance Criteria

1. Save surfaces per-step outcomes; a partial failure is visible and actionable, never silent.
2. Lock state renders from the mutation response without refetch.

#### Testing

- Induced step-failure tests against the saga contract; editor E2E save flows.

- **Risk:** High — blocked on ADR-013 ratification.
- **Estimated effort:** 8–12 days

---

## Measurement

### MST-FE-001 · Migrate measurement reads and retire `humanId`

- **Type:** Query migration · **Impact:** Medium · **Domain:** measurement
- **Depends on:** MST-BE-B-01, MST-BE-B-04
- **Operations:** `getMeasurementByIds`, `getMeasurementSetStatus`, `getMeasurementComponentStatus`

- **Business objective:**
  - Measurement set views read from the federated graph; the deprecated identifier is gone before cutover.
- **Technical objective:**
  - Migrate the by-id and status reads; replace every `SPARK_Measurements.humanId` selection with `parentId` (deprecated: "Use parentId").
- **Background / current implementation:**
  - `product-common/MeasurementQueries.tsx` + `spark-ui-admin`; fragments `MEASUREMENT_FIELDS_FRAGMENT`, `SAMPLE_MEASUREMENT_FRAGMENT`.
  - `getMeasurementsMetaData` also selects a POM root (out of scope) — routing decision at grooming.
- **Required changes:**
  - `humanId` → `parentId` in selections, models and any UI rendering the id.
  - Fragment re-target; document re-point.

#### Acceptance Criteria

1. No document selects `humanId` on measurements.
2. Measurement views render identically under the flag.

#### Testing

- Selection-level lint (no `humanId`); measurement screen integration tests.

- **Risk:** Medium.
- **Estimated effort:** 4–6 days

### MST-FE-002 · Migrate measurement list/search reads

- **Type:** Query migration · **Impact:** Medium · **Domain:** measurement
- **Depends on:** MST-BE-C-01, MST-BE-C-02
- **Operations:** `getMeasurements`, `getMeasurementsElastic`

- **Business objective:**
  - Measurement listings keep parity through the search cutover.
- **Technical objective:**
  - Migrate the list and elastic-search documents after the read-hub decision.
- **Required changes:**
  - Adopt ratified search shapes; pagination fixtures verified.

#### Acceptance Criteria

1. List results and paging match legacy fixtures.

#### Testing

- Fixture parity tests.

- **Risk:** Medium — search-cutover dependency.
- **Estimated effort:** 3–5 days

### MST-FE-003 · Migrate measurement master-data reads

- **Type:** Query migration · **Impact:** Low · **Domain:** measurement
- **Depends on:** MST-BE-B-02, MST-BE-B-03
- **Operations:** `getUnitsOfMeasure`, `getThicknessUnitsOfMeasure`

- **Business objective:**
  - Unit pickers keep their data.
- **Technical objective:**
  - Re-point the units-of-measure queries.
- **Required changes:**
  - Endpoint + types only.

#### Acceptance Criteria

1. Unit lists identical; session-cached.

#### Testing

- Fixture equality tests.

- **Risk:** Low.
- **Estimated effort:** 1–2 days

### MST-FE-004 · Migrate measurement mutations

- **Type:** Mutation migration · **Impact:** Medium · **Domain:** measurement
- **Depends on:** MST-BE-D-03, MST-BE-D-04, MST-BE-D-06, MST-BE-D-07
- **Operations:** `lockMeasurementSet`, `unlockMeasurementSet`, `putSampleMeasurementSet`, `deleteSampleMeasurementSet`

- **Business objective:**
  - Measurement editing, locking and sample-set management write through the federated graph.
- **Technical objective:**
  - Migrate the 4 mutations; `putSampleMeasurementSet` follows the 2-step `updateMeasurement` write pattern (master-data cache backend-side).
- **Required changes:**
  - Input renames; cache writes from responses; partial-failure surface on the 2-step write per the ratified contract.

#### Acceptance Criteria

1. Lock/unlock reflect immediately from the response.
2. Sample-set save surfaces step outcomes.

#### Testing

- Mutation unit tests with cache assertions; editor E2E save.

- **Risk:** Medium.
- **Estimated effort:** 4–6 days

---

## Product Details

### PDTL-FE-001 · Migrate product-details reads

- **Type:** Query migration · **Impact:** Low · **Domain:** productDetails
- **Depends on:** PDTL-BE-B-01
- **Operations:** `getProductDetailsById`, `getProductDetailComponentStatus`

- **Business objective:**
  - Specification screens read from the federated graph unchanged.
- **Technical objective:**
  - Migrate the 2 read documents in `product-details/SpecificationQueries.ts` (fragment `PRODUCT_DETAILS_DATA_FRAGMENT`).
- **Required changes:**
  - Fragment re-target; document re-point; model regeneration.

#### Acceptance Criteria

1. Specification screens render identically under the flag.

#### Testing

- Screen integration tests; snapshot regeneration.

- **Risk:** Low.
- **Estimated effort:** 2–3 days

### PDTL-FE-002 · Migrate product-details simple mutations

- **Type:** Mutation migration · **Impact:** Medium · **Domain:** productDetails
- **Depends on:** PDTL-BE-D-01, PDTL-BE-D-03, PDTL-BE-D-04, PDTL-BE-D-05
- **Operations:** `createProductDetailsSet`, `productDetailLockUnlock`, `cloneFilesForProductDetails`, `updateProductDetailComponentStatus`

- **Business objective:**
  - Specification create, lock and clone flows write through the federated graph.
- **Technical objective:**
  - Migrate the 4 single-step mutations with cache writes.
- **Required changes:**
  - Input renames; response-driven cache updates.

#### Acceptance Criteria

1. Each flow completes and reflects in the UI without manual refresh.

#### Testing

- Mutation unit tests; clone-flow smoke test.

- **Risk:** Low.
- **Estimated effort:** 3–4 days

### PDTL-FE-003 · Migrate `updateProductDetailsSet` saga handling

- **Type:** Mutation migration (complex) · **Impact:** Medium · **Domain:** productDetails
- **Depends on:** PDTL-BE-E-01
- **Operations:** `updateProductDetailsSet`

- **Business objective:**
  - Specification saves surface partial failures explicitly.
- **Technical objective:**
  - Adopt the multi-step write contract (elastic-search step included — ADR-013 scope, 🟠 draft).
- **Required changes:**
  - Saga-status rendering; remove compensating refetch.

#### Acceptance Criteria

1. Partial failure is visible and actionable on save.

#### Testing

- Induced step-failure contract tests; save E2E.

- **Risk:** Medium — ADR-013 ratification dependency.
- **Estimated effort:** 3–5 days

---

## Packaging

### PKG-FE-001 · Migrate packaging reads

- **Type:** Query migration · **Impact:** Medium · **Domain:** packaging
- **Depends on:** PKG-BE-B-01, PKG-BE-B-02
- **Operations:** `getPackagings`, `getPackagingById`, `getPackagingComponentStatus`

- **Business objective:**
  - Packaging detail and listing screens read from the federated graph unchanged.
- **Technical objective:**
  - Migrate the 3 `getPackagings` variants and 2 `getPackagingById` documents across `product-packaging` and `spark-packaging-base` (fragment factories `GET_PACKAGING_DETAIL_FRAGMENT(...)` become static per the delivered platform dynamic-gql expansion pattern).
- **Background / current implementation:**
  - Duplicate `PackagingDetailsQueries` files exist in `product-packaging` and `spark-packaging-base` — consolidation candidate.
- **Required changes:**
  - Static fragment expansion; document re-point; consolidate duplicate documents where selections match.

#### Acceptance Criteria

1. Packaging screens render identically under the flag.
2. Duplicate documents consolidated or explicitly justified.

#### Testing

- Response JSON diffs; packaging screen integration suite.

- **Risk:** Medium.
- **Estimated effort:** 5–8 days

### PKG-FE-002 · Migrate packaging master-data reads and retire deprecated fields

- **Type:** Query migration · **Impact:** Low · **Domain:** packaging
- **Depends on:** PKG-BE-B-04, PKG-BE-B-06
- **Operations:** `getCountries`, `getPackagingFieldValuesByType`

- **Business objective:**
  - Packaging editors keep their reference data; deprecated selections are gone before cutover.
- **Technical objective:**
  - Re-point the 2 master-data queries; drop the deprecated `SPARK_PackagingFieldValues.resourceType` selection.
- **Required changes:**
  - Endpoint + types; remove `resourceType` from selections and models.

#### Acceptance Criteria

1. Reference data identical; no `resourceType` selection remains.

#### Testing

- Fixture equality tests; selection lint.

- **Risk:** Low.
- **Estimated effort:** 2–3 days

### PKG-FE-003 · Migrate dieline flows

- **Type:** Query + mutation migration · **Impact:** Medium · **Domain:** packaging
- **Depends on:** PKG-BE-B-03, PKG-BE-B-05, PKG-BE-D-02
- **Operations:** `getDielines`, `getDielineEvaluationStatuses`, `evaluateDieline`

- **Business objective:**
  - Dieline browsing and evaluation keep working end-to-end.
- **Technical objective:**
  - Migrate the 2 dieline reads and the evaluation mutation; replace the deprecated `SPARK_Dieline.attachments` selection with attachment entity selections.
- **Required changes:**
  - Attachment selections move to the stitched entity shape; evaluation status polling unchanged.

#### Acceptance Criteria

1. Dieline list, preview and evaluation statuses match legacy.
2. No `attachments` selection remains on the dieline type.

#### Testing

- Dieline flow integration tests; evaluation E2E.

- **Risk:** Medium.
- **Estimated effort:** 4–6 days

### PKG-FE-004 · Migrate packaging simple mutations and export

- **Type:** Mutation migration · **Impact:** Medium · **Domain:** packaging
- **Depends on:** PKG-BE-D-01, PKG-BE-D-03, PKG-BE-D-04, PKG-BE-D-05, PKG-BE-D-06, PKG-BE-D-07, PKG-BE-D-09
- **Operations:** `addPackaging`, `bulkAddPackagings`, `bulkUpdatePackagings`, `exportPackaging`, `lockPackaging`, `unlockPackaging`, `updatePackagingComponentStatus`

- **Business objective:**
  - Packaging create, bulk, lock and export flows write through the federated graph.
- **Technical objective:**
  - Migrate the 7 single-step mutations with response-driven cache updates.
- **Required changes:**
  - Input renames; per-item results rendered on bulk paths; export request/ack flow unchanged.

#### Acceptance Criteria

1. Each flow completes with UI reflecting the write; bulk flows show per-item outcomes.

#### Testing

- Mutation unit tests; bulk-path fixtures; export smoke test.

- **Risk:** Medium — bulk surface.
- **Estimated effort:** 5–8 days

### PKG-FE-005 · Migrate `updatePackaging` saga handling and packet information

- **Type:** Mutation migration (complex) · **Impact:** High · **Domain:** packaging
- **Depends on:** PKG-BE-E-01
- **Operations:** `updatePackaging`, `getPackagingPacketsInformation`, `getPackagingPacketInformation`

- **Business objective:**
  - Packaging saves surface partial failures explicitly; packet information stays consistent after saves.
- **Technical objective:**
  - Adopt the multi-step write contract for `updatePackaging` (elastic step included — ADR-013 scope, 🟠 draft); migrate the packet-information reads that render post-save state.
- **Required changes:**
  - Saga-status rendering; packet reads re-pointed with the save flow to avoid mixed-endpoint reads of just-written data.

#### Acceptance Criteria

1. Partial failure visible and actionable; packet info reflects the save without endpoint mixing.

#### Testing

- Induced step-failure tests; save-then-read consistency test.

- **Risk:** High — write-then-read consistency across the cutover boundary.
- **Estimated effort:** 5–8 days

---

## Watchlist

### WATCHLIST-FE-001 · Migrate watchlist reads

- **Type:** Query migration · **Impact:** Low · **Domain:** watchlist
- **Depends on:** WATCHLIST-BE-B-01, WATCHLIST-BE-C-01
- **Operations:** `getWatchlistByIds`, `getWatchlistByFilter`

- **Business objective:**
  - Watchlist screens read from the federated graph unchanged — the pilot cutover candidate.
- **Technical objective:**
  - Migrate the 2 read documents in `watchlist/WatchlistQueries.ts` (fragments `WATCHLIST_FRAGMENT`, `WATCHLIST_PARTICIPANT_FRAGMENT`, shared `PRODUCT_BASE_INFO_FRAGMENT`).
- **Required changes:**
  - Fragment re-target (product base fragment shared with product domain); document re-point.

#### Acceptance Criteria

1. Watchlist list and detail render identically under the flag.

#### Testing

- Screen integration tests; shared-fragment cache assertion with product entities.

- **Risk:** Low — smallest isolated domain; run first to validate the platform stack.
- **Estimated effort:** 2–3 days

### WATCHLIST-FE-002 · Migrate watchlist create and clone mutations

- **Type:** Mutation migration · **Impact:** Low · **Domain:** watchlist
- **Depends on:** WATCHLIST-BE-D-01, WATCHLIST-BE-D-02
- **Operations:** `createWatchlistEntries`, `cloneFilesForWatchlist`

- **Business objective:**
  - Watchlist creation and file cloning write through the federated graph.
- **Technical objective:**
  - Migrate the 2 single-step mutations with cache writes.
- **Required changes:**
  - Input renames; response-driven list update.

#### Acceptance Criteria

1. Created entries appear without refetch; clone completes.

#### Testing

- Mutation unit tests; create E2E.

- **Risk:** Low.
- **Estimated effort:** 2–3 days

### WATCHLIST-FE-003 · Migrate `updateWatchlistEntries` saga handling

- **Type:** Mutation migration (complex) · **Impact:** Medium · **Domain:** watchlist
- **Depends on:** WATCHLIST-BE-E-01
- **Operations:** `updateWatchlistEntries`

- **Business objective:**
  - Bulk watchlist updates surface partial failures explicitly.
- **Technical objective:**
  - Adopt the multi-step write contract (`getWatchlistForBulkUpdate` feeds this flow).
- **Required changes:**
  - Per-entry outcome rendering; remove compensating refetch.

#### Acceptance Criteria

1. Bulk update shows per-entry outcomes; partial failure actionable.

#### Testing

- Induced step-failure tests; bulk-update E2E.

- **Risk:** Medium — ADR-013 ratification dependency.
- **Estimated effort:** 3–4 days

---

## Impression

### IMPRESSION-FE-001 · Migrate `getBomDataAndImpressions` (with BOM wave)

- **Type:** Query migration · **Impact:** Low · **Domain:** impression
- **Depends on:** IMPRESSION-BE-B-01, BOM-BE-B-01, BOM-FE-002
- **Operations:** `searchImpressionsByProductId`, `getBomByIds`

- **Business objective:**
  - The combined BOM + impressions view keeps one round trip and identical data.
- **Technical objective:**
  - Migrate the cross-domain document when both roots are on the router (per [fe-07-network-call-analysis.md §2.1](./fe-07-network-call-analysis.md) — no interim split).
- **Background / current implementation:**
  - One document selects `getBomByIds` and `searchImpressionsByProductId`; impression sub-type polymorphism (5 types) needs the regenerated `possibleTypes` map (ADR-017 — 🟠 draft).
- **Required changes:**
  - Re-point after BOM-FE-002 lands; inline-fragment selections verified against federated impression sub-types.

#### Acceptance Criteria

1. Combined view renders identically in one request under the flag.
2. All 5 impression sub-types resolve correctly in cache.

#### Testing

- Fixtures covering each sub-type; view integration test.

- **Risk:** Low.
- **Estimated effort:** 2–3 days

### IMPRESSION-FE-002 · Migrate `getCarryForwardFormData` (with Product wave)

- **Type:** Query migration · **Impact:** Low · **Domain:** impression
- **Depends on:** IMPRESSION-BE-B-01, PRODUCT-BE-B-01, PRODUCT-FE-001
- **Operations:** `searchImpressionsByProductId`, `getProduct`

- **Business objective:**
  - Carry-forward form keeps its combined product + impressions data.
- **Technical objective:**
  - Migrate the cross-domain document when both roots are on the router.
- **Required changes:**
  - Re-point after PRODUCT-FE-001; sub-type handling as IMPRESSION-FE-001.

#### Acceptance Criteria

1. Carry-forward form renders identically in one request under the flag.

#### Testing

- Carry-forward flow E2E.

- **Risk:** Low.
- **Estimated effort:** 1–2 days

---

## Claims

### CLAIM-FE-001 · Split the claim fragment factory and re-target claim fragments

- **Type:** Refactor · **Impact:** Medium · **Domain:** claims
- **Depends on:** —
- **Operations:** —

- **Business objective:**
  - Claim documents become statically valid before the first cross-subgraph cutover.
- **Technical objective:**
  - Land the claims share of the dynamic-gql static expansion (delivered platform pattern): `FULL_CLAIM_DETAILS(includeWorkspaces)` → two static fragments; re-target `CLAIM_DETAILS_FRAGMENT` / `CLAIM_WORKSPACE_PRODUCT_FRAGMENT`.
- **Background / current implementation:**
  - The factory is consumed from `claims` and `spark-legacy` template-library flows.
- **Required changes:**
  - Behaviour-neutral expansion; call sites select the with/without-workspaces variant explicitly.

#### Acceptance Criteria

1. No runtime-composed claim documents remain; codegen validates all claim documents.

#### Testing

- Document-text snapshots; claim screen tests unchanged.

- **Risk:** Low.
- **Estimated effort:** 2–3 days

### CLAIM-FE-002 · Migrate claim reads (first cross-subgraph cutover)

- **Type:** Query migration · **Impact:** High · **Domain:** claims
- **Depends on:** CLAIM-BE-B-01, CLAIM-BE-B-02, CLAIM-BE-B-03, CLAIM-BE-B-04, CLAIM-FE-001
- **Operations:** `getClaims`, `getClaimByIds`, `getCommunicationChannels`, `getAllClaimsAbout`, `getClaimComponentStatus`

- **Business objective:**
  - Claim views read from the `spark-claims` subgraph through the router — the program's first cross-subgraph entity resolution in production.
- **Technical objective:**
  - Migrate the 5 read operations; the claim → product entity hop (`Claims.product`) exercises `Product @key` resolution across subgraphs.
- **Background / current implementation:**
  - `claims/ClaimQueries.ts` + `spark-legacy` template library + `spark-ui-admin`; `getWorkspaceV2` inside ClaimQueries is a workspace-service call (out of scope — stays on its current endpoint).
- **Required changes:**
  - Fragment re-target; error-policy `all` (claim screens must render if the product subgraph is degraded).

#### Acceptance Criteria

1. Claim list/detail render identically under the flag; product data inside claims resolves via entity reference.
2. Product-subgraph failure yields partial claim render, not a blank screen.

#### Testing

- Cross-subgraph fixture tests incl. induced product-subgraph failure; claim screen integration suite.

- **Risk:** High — first cross-subgraph dependency in production.
- **Estimated effort:** 6–10 days

### CLAIM-FE-003 · Migrate claim simple mutations and export

- **Type:** Mutation migration · **Impact:** Medium · **Domain:** claims
- **Depends on:** CLAIM-BE-D-01, CLAIM-BE-D-02, CLAIM-BE-D-03, CLAIM-BE-D-04, CLAIM-BE-D-05
- **Operations:** `createClaim`, `bulkUpdateClaim`, `lockClaim`, `unlockClaim`, `requestClaimExport`

- **Business objective:**
  - Claim create, bulk-update, lock and export flows write through the federated graph.
- **Technical objective:**
  - Migrate the 5 single-step mutations with response-driven cache updates.
- **Required changes:**
  - Input renames; per-item outcomes on bulk update; export request/ack unchanged.

#### Acceptance Criteria

1. Each flow completes with the UI reflecting the write; bulk shows per-item outcomes.

#### Testing

- Mutation unit tests; create/lock E2E.

- **Risk:** Medium.
- **Estimated effort:** 4–6 days

### CLAIM-FE-004 · Migrate `updateClaim` multi-step write handling

- **Type:** Mutation migration (complex) · **Impact:** High · **Domain:** claims
- **Depends on:** CLAIM-BE-E-01
- **Operations:** `updateClaim`

- **Business objective:**
  - Claim edits keep their guarantees through the proxy-ACL multi-step write, with correct response shapes.
- **Technical objective:**
  - Adopt the ratified write contract; do not codify the legacy camelCase response bug — the federated response is the corrected shape.
- **Background / current implementation:**
  - `claims` + `spark-fabric` utils + `spark-legacy` template edit all call `updateClaim`; some client code compensates for the camelCase bug.
- **Required changes:**
  - Remove bug-compensation mapping; saga-status rendering; shared handling across the 3 call sites.

#### Acceptance Criteria

1. Claim edit succeeds from all 3 call sites with the corrected response shape.
2. Partial failure visible and actionable.

#### Testing

- Contract tests per call site; induced step-failure test.

- **Risk:** High — behavioural change (bug removal) across multiple libraries.
- **Estimated effort:** 5–8 days
