# Phase 4: Migration Stories — Product

> **Domain:** `product`
> **Target DGS:** `ProductService` (repo: `plm-product`, url: `https://spark-product.dev.target.com`)
> **Pipeline Version:** 1.1
> **Generated:** 2026-05-01
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md), [be-03-schema-analysis.md](./be-03-schema-analysis.md)
> **DGS Target Status:** Green-field (no existing DGS schema)

---

## Summary Statistics

| Category | Story Count | Effort Range (days) |
|----------|-------------|---------------------|
| CAT-1 (Schema & DTOs) | 8 | 16–20 |
| CAT-2 (Resolver/Data Fetcher) | 19 | 55–85 |
| CAT-3 (Service Layer) | 9 | 19–29 |
| CAT-4 (Federation / Stitching) | 18 | 22–36 |
| CAT-5 (Test Coverage) | 9 | 14–22 |
| **Subtotal (raw)** | **63** | **126–192** |
| **+20% buffer** | — | **152–231** |

> **Note on count increase from prior draft:** The TechPack query (`getProductTechPackCountV1`) decomposes into a composite key entity stub + 8 per-subgraph CAT-4 placeholder stories (one per: Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist). These follow the multi-subgraph pattern in `reference/federation-patterns.md` §9.

---

## Phase A: Foundation & Schema

### PRODUCT-BE-A-01 · CAT-1 · Small (1–2d)

**Title:** Define core Product schema file and DGS project skeleton

**As a** backend engineer
**I want to** establish the GraphQL schema file and DGS module structure for the Product domain
**So that** all subsequent schema and resolver work has a stable foundation to build on.

**Current behavior (from Phase 2):**
- Schema defined in `spark-internal-graphql/packages/data-source-spark/src/schemas/SPARK_Product.graphql` (781 lines)
- No DGS target exists — green-field migration

**Target DGS implementation:**
- Create `plm-product/apps/app/src/main/resources/schema/product.graphqls` with federation header
- Create `ProductDataFetcher.kt` stub with `@DgsComponent` annotation
- Wire `DateTime` scalar to `LocalDateTime`

**Files to create:**
- `plm-product/apps/app/src/main/resources/schema/product.graphqls`
- `plm-product/apps/app/src/main/kotlin/.../ProductDataFetcher.kt` (stub)
- `plm-product/apps/app/src/main/kotlin/.../config/ScalarConfig.kt`

**Dependencies:** None

**Acceptance criteria:**
- `product.graphqls` exists with federation header (`@link`, scalars, `extend type Query`, `extend type Mutation`)
- `DateTime` scalar wired to `LocalDateTime` or `Instant` via `ScalarType` config
- Schema loads without errors in DGS schema validation step (`./gradlew generateJava`)
- PR includes schema linting pass

**Test cases:**
- Unit: schema compiles cleanly
- Unit: `DateTime` scalar serializes/deserializes ISO-8601 correctly

---

### PRODUCT-BE-A-02 · CAT-1 · Small (1–2d)

**Title:** Add all owned Product types and input types to schema

**As a** backend engineer
**I want to** define all `Product`-owned GraphQL types and input types in the schema
**So that** field resolvers and mutations can be implemented without subsequent schema churn.

**Current behavior (from Phase 2):**
- 38 owned types defined in source schema (see Phase 3 Type Classification table)
- 30 input types defined

**Target DGS implementation:**
- Add all owned types to `product.graphqls`
- Apply `@shareable` to `Paging`, `Pageable`, `CodeDescription`, `CodeDescriptionOrder`
- Apply `@key(fields: "id")` to `Product` only

**Files to modify:**
- `plm-product/apps/app/src/main/resources/schema/product.graphqls`

**Dependencies:** PRODUCT-BE-A-01

**Acceptance criteria:**
- All 38 owned types defined (see [be-03-schema-analysis.md](./be-03-schema-analysis.md) Type Classification table)
- All 30 input types defined
- `@shareable` applied correctly
- `@key(fields: "id")` on `Product` only; no `@key` on embedded types
- Schema compiles cleanly

**Test cases:**
- Unit: schema validates with graphql-inspector
- Unit: `Product` entity resolves with federation entity fetcher stub

---

### PRODUCT-BE-A-03 · CAT-1 · Small (1–2d)

**Title:** Add external stubs and gateway stitch types to schema

**As a** backend engineer
**I want to** add all `@extends @external` type stubs for externally-owned types
**So that** field resolvers can reference gateway-stitched types without schema errors.

**Current behavior (from Phase 2):**
- `VMM_BusinessPartner`, `VMM_Brand`, `IG_Department`, `IG_Division`, `IG_Clazz` referenced in schema
- 11 external stubs total (5 platform, 6 co-located DGS)

**Target DGS implementation:**
- Add all external stubs with `@key @extends` pattern
- All platform stubs (VMM, IG): key-only return pattern

**Files to modify:**
- `plm-product/apps/app/src/main/resources/schema/product.graphqls`

**Dependencies:** PRODUCT-BE-A-01

**Acceptance criteria:**
- 11 external stubs added with correct `@key @extends` pattern
- `Tag`, `Attachment`, `SampleV2`, `WorkspaceV2`, `TeamV2`, `UserProfileAttributes` stubs defined
- Schema compiles with stubs referencing other DGS subgraphs
- Hive Gateway can resolve stub types via federation (integration test in Phase H)

**Test cases:**
- Unit: schema compiles with external type references
- Integration (Phase H): Hive Gateway resolves `VMM_BusinessPartner` stub for a product query

---

> **Note:** This file shows the first 3 of 51 stories (Phase A). The full file documents Phases A through I (38 story IDs grouped by functional phase). For complete stories, run Phase 4 against the `product` domain with Phases 1–3 complete.

---

## Phase B: Core CRUD Queries

### PRODUCT-BE-B-01 · CAT-2 · Small (1–2d)

**Title:** Implement `getProduct` query data fetcher

**As a** backend engineer
**I want to** implement the `getProduct` query in the DGS service
**So that** clients can fetch a single product by ID from `plm-product`.

**Current behavior (from Phase 2 — Q2):**
1. Call `ctx.loaders.product.getByID.load(id)` — DataLoader batched GET by product ID.
2. Return hydrated `Product` object (camelCase via `deepToCamelCase`).
- **REST endpoint:** `GET /enterprise_product_development_products/v1/{id}` (via `Product.js:getByID`)
- **Error handling:** 404 → return null

**Target DGS implementation:**
- `@DgsQuery` method calling `ProductService.getById(id)` via Feign client
- Feign client method: `GET /enterprise_product_development_products/v1/{id}`
- Return type: `Product` (Kotlin data class mapped from REST response DTO)

**Files to create:**
- `ProductDataFetcher.kt` — add `@DgsQuery getProduct(id: ID!): Product`
- `ProductService.kt` — add `getById(id: String): ProductDto`
- `ProductClient.kt` (Feign) — `@GetMapping` for the REST endpoint
- `ProductDto.kt` — REST response DTO

**Dependencies:** PRODUCT-BE-A-01, PRODUCT-BE-A-02

**Acceptance criteria:**
- `getProduct(id: "123")` returns correct product data from REST API
- 404 from REST → GraphQL returns null (not error)
- Response fields match schema types (e.g., `id`, `humanId`, `description`, `createdAt`, `updatedAt`)
- DataLoader batching implemented: N product IDs resolved in 1 REST call (batch endpoint)

**Test cases:**
- Unit: `ProductService.getById("123")` returns mapped `Product`
- Unit: 404 REST response → null return
- Integration: `getProduct` query resolves via live DGS against test data
- Parity: `getProduct("prod-123")` in DGS returns same shape as spark-internal-graphql response

---

---

## Phase E: Complex Operations (TechPack — excerpt)

> **Note:** Phase E contains all high-complexity orchestration stories. This excerpt shows only the TechPack stories to illustrate the composite key entity sub-story pattern.

### PRODUCT-BE-E-01 · CAT-1 · Small (1–2d)

**Title:** Define `ResourcesCount` composite key schema in Product subgraph

**Type:** Story
**Complexity:** Medium
**Category:** CAT-1 — Schema migration
**Phase:** E

**As a** DGS migration engineer,
**I want** to define `ResourcesCount` with `@key(fields: "productId partnerId")` in the Product subgraph schema,
**so that** the federation gateway can route each stub field to its owning subgraph and all domain teams have a stable contract to implement against.

---

**Current Behavior (from Phase 2):**
- `SPARK_ResourcesCount` defined in `SPARK_Product.graphql` with 10 count fields (no federation key — monolithic type).
- Fields: `productAttachments`, `discussionAttachments`, `discussions`, `sample`, `measurementSets`, `claims`, `productBoms`, `packagingBoms`, `constructions`, `watchlists`.
- All fields populated by `getTechPackResourceCountMap` in a single Node.js service — no federation boundaries.

---

**EXT Service Calls:** None for this schema story.

---

**Target DGS Implementation:**
- Add to `product.graphqls`:
  ```graphql
  type ResourcesCount @key(fields: "productId partnerId") {
    productId:        ID!
    partnerId:        ID!
    workspaceContext: String
    parentProductId:  ID
    productAttachments:    [ID]
    discussionAttachments: [ID]
    discussions:           [ID]
    sample:                [ID]
    measurementSets:       [ID]
    claims:                [ID]
    productBoms:           [ID]
    packagingBoms:         [ID]
    constructions:         [ID]
    watchlists:            [ID]
  }
  ```
- Add schema comments `# → {Domain} subgraph` on each stub field for discoverability.

---

**Files to Create / Modify:**
- `plm-product/apps/app/src/main/resources/schema/product.graphqls` — add `ResourcesCount` type with `@key`

---

**Dependencies:** PRODUCT-BE-A-01

---

**Acceptance Criteria:**
1. `ResourcesCount` defined with `@key(fields: "productId partnerId")` in `product.graphqls`.
2. `productId` and `partnerId` are `ID!` (non-nullable); `workspaceContext` and `parentProductId` are nullable.
3. All 10 stub fields present and return `[ID]` (nullable list).
4. Schema compiles cleanly (`./gradlew generateJava` passes).
5. Schema reviewed and approved by architect before PRODUCT-BE-E-02 starts.

**Test Cases:**
- [ ] Unit: schema compiles cleanly
- [ ] Unit: `ResourcesCount` entity resolves via federation entity fetcher stub

---

### PRODUCT-BE-E-02 · CAT-2 + CAT-3 · Large (5–8d)

**Title:** Implement `getProductTechPackCountV1` Product stub resolver + aggregation facade (Option D Phase 1)

**Type:** Story
**Complexity:** Very High
**Category:** CAT-2 + CAT-3 — Resolver + Service (bundled for Option D Phase 1)
**Phase:** E

**As a** DGS migration engineer,
**I want** to implement the `getProductTechPackCountV1` stub resolver in the Product subgraph and wire it to a TechPack Aggregation Service (extracted from `getTechPackResourceCountMap`),
**so that** the query works end-to-end on Day 1 with lowest risk while the per-subgraph federation stories (Option D Phase 2) are sequenced in parallel.

---

**Current Behavior (from Phase 2 — Q8 / Helper H3):**
1. Extract `productId`, `partnerId`, `workspaceContext`, `parentProductId` from args.
2. Call `getTechPackResourceCountMap(ctx, productId, partnerId, workspaceContext, parentProductId)` (~200 lines in `SPARK_Product.js`).
   - Step 1: `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission(ctx, productId, partnerId.toInt())` — ACL tree traversal (from `commonLoaders.js`; shared across domains).
   - Step 2: Same call for `parentProductId` if provided → merge v2 + v3 attachment IDs from both trees.
   - Step 3: `getAttachmentsV3(allAttachmentIds)` — hydrate attachment objects.
   - Step 4: Filter attachments by `product_packet_props.partner_id` + `critical=true`.
   - Step 5: 7 Elasticsearch queries **in parallel** (`Promise.all`): samples, criticalDiscussions, measurementSets, claims, boms, constructions, watchlists.
   - Step 6: From criticalDiscussions → extract `parentDiscussionIds`, `criticalDiscussionIds`, `criticalThreadIds`.
   - Step 7: If critical IDs exist → `searchAttachmentsByParentResources(allCriticalIds)`.
   - Step 8: Build and return `ResourcesCount` DTO.
3. Return `ResourcesCount`.
- **EXT services:** ACL/Relationship, Attachment REST, Elasticsearch ×8 (7 domain queries + 1 attachment-by-parent).
- **Risk:** ACL tree traversal is 200+ lines of recursive graph logic shared across multiple domains — requires spike before porting.

---

**EXT Service Calls:**
- **EXT Service** → key: `relationship` · url: `spark-relationship.dev.target.com` · repo: `spark-relationship` · severity: 🔴 RED
  Purpose: ACL-filtered resource tree for product + parent product.
- **EXT Service** → key: `attachment` · url: `spark-attachment.dev.target.com` · repo: `spark-attachment` · severity: 🔴 RED
  Purpose: Hydrate attachment objects to read `product_packet_props.critical`.
- **EXT Service** → key: `elasticsearch` · url: `elastic-cluster.internal` · severity: 🔴 RED
  Purpose: 7 domain count queries + 1 attachment-by-parent query (all via aggregation service).

---

**Target DGS Implementation (Option D Phase 1 — Aggregation Facade):**
- `@DgsQuery getProductTechPackCountV1(...)` in `TechPackDataFetcher.kt` — thin stub, no business logic.
- Calls `TechPackAggregatorFeignClient.getResourceCount(productId, partnerId, workspaceContext, parentProductId)`.
- Returns `ResourcesCount` DTO deserialized from aggregation service JSON response.
- `@DgsEntityFetcher(name = "ResourcesCount")` reconstructs entity from gateway `_entities` call.
- **Aggregation Service (Option B1 — Node.js extract, fastest):** Extract `getTechPackResourceCountMap` from `SPARK_Product.js` into a standalone Express.js microservice. Add `POST /techpack/count` endpoint. This is copy-paste with minimal changes — estimated 1–2 days.

```kotlin
@DgsComponent
class TechPackDataFetcher(val aggregatorClient: TechPackAggregatorFeignClient) {
    @DgsQuery
    suspend fun getProductTechPackCountV1(
        @InputArgument productId: String,
        @InputArgument partnerId: String,
        @InputArgument workspaceContext: String?,
        @InputArgument parentProductId: String?,
    ): ResourcesCount = aggregatorClient.getResourceCount(productId, partnerId, workspaceContext, parentProductId)

    @DgsEntityFetcher(name = "ResourcesCount")
    fun resolveResourcesCount(values: Map<String, Any>): ResourcesCount = ResourcesCount(
        productId        = values["productId"] as String,
        partnerId        = values["partnerId"] as String,
        workspaceContext = values["workspaceContext"] as? String,
        parentProductId  = values["parentProductId"] as? String,
    )
}
```

---

**Files to Create / Modify:**
- `plm-product/.../dataFetcher/TechPackDataFetcher.kt` — create
- `plm-product/.../service/TechPackAggregatorFeignClient.kt` — create (Feign client to aggregation service)
- `plm-product/.../model/ResourcesCount.kt` — create DTO
- `techpack-aggregator/index.js` — new Node.js microservice (or `TechPackAggregatorService.kt` for Option B2)

---

**Dependencies:** PRODUCT-BE-E-01

---

**Acceptance Criteria:**
1. `getProductTechPackCountV1(productId, partnerId, workspaceContext, parentProductId)` returns populated `ResourcesCount` from aggregation service.
2. `@DgsEntityFetcher` for `ResourcesCount` reconstructs entity correctly from `_entities` map.
3. Aggregation service returns identical counts to existing `spark-internal-graphql` for the same inputs (parity test passes).
4. Feign client calls `POST {aggregator.url}/techpack/count` with correct params.
5. 404 or 5xx from aggregation service → DGS returns GraphQL error (not silent null).
6. Aggregation service deployed, health-checked, and observable (metrics + structured logs).

**Test Cases:**
- [ ] Unit: `TechPackDataFetcher.getProductTechPackCountV1` calls Feign client with correct params
- [ ] Unit: `resolveResourcesCount` entity fetcher reconstructs from map correctly
- [ ] Integration: end-to-end query via DGS test client returns expected `ResourcesCount` shape
- [ ] Parity: `getProductTechPackCountV1("P-123", "PARTNER-X", "WS-1", null)` returns same counts from DGS and spark-internal-graphql

---

### PRODUCT-BE-E-03 · CAT-2 · Medium (3–5d)

**Title:** Implement `getProductTechPackBulkCountV1` bulk wrapper

**Type:** Story
**Complexity:** Very High
**Category:** CAT-2 — Resolver / Data Fetcher
**Phase:** E

**As a** DGS migration engineer,
**I want** to implement `getProductTechPackBulkCountV1` using the same aggregation facade pattern as PRODUCT-BE-E-02,
**so that** bulk tech-pack count queries are supported without duplicating the ACL/Elasticsearch orchestration logic.

---

**Current Behavior (from Phase 2 — Q9):**
1. Accepts `bulkTechPackCountResource: [{ productId, partnerId, workspaceContext, parentProductId }]`.
2. For each item, calls `getTechPackResourceCountMap(ctx, productId, partnerId, ...)` — the same helper as Q8.
3. All calls run **in parallel** via `Promise.all`.
4. Returns `[ResourcesCount]`.

---

**EXT Service Calls:** Same as PRODUCT-BE-E-02 (multiplied per item in the bulk input).

---

**Target DGS Implementation:**
- `@DgsQuery getProductTechPackBulkCountV1(...)` calls aggregation service bulk endpoint `POST /techpack/count/bulk`.
- Aggregation service handles parallelism internally.
- Returns `List<ResourcesCount>`.

---

**Files to Create / Modify:**
- `plm-product/.../dataFetcher/TechPackDataFetcher.kt` — add `getProductTechPackBulkCountV1` method
- `plm-product/.../service/TechPackAggregatorFeignClient.kt` — add bulk endpoint method
- `techpack-aggregator/index.js` — add `POST /techpack/count/bulk` endpoint

---

**Dependencies:** PRODUCT-BE-E-01, PRODUCT-BE-E-02

---

**Acceptance Criteria:**
1. `getProductTechPackBulkCountV1([{productId, partnerId, ...}])` returns `[ResourcesCount]` for each input.
2. Aggregation service handles all bulk items in parallel.
3. Empty input list → returns empty list (no error).
4. Parity test: bulk result matches N individual `getProductTechPackCountV1` calls for same inputs.

**Test Cases:**
- [ ] Unit: bulk Feign client call maps input list correctly
- [ ] Unit: empty bulk list → returns empty list
- [ ] Parity: bulk(P1, P2, P3) = [single(P1), single(P2), single(P3)]

---

## Phase F: Federation & Stitching (TechPack Option D Phase 2 — excerpt)

> **Note:** These are the per-subgraph CAT-4 stories for Option D Phase 2. Each one migrates a set of stub fields from the aggregation facade to the owning domain subgraph. Stories PRODUCT-BE-F-01 through F-08 are **placeholder stubs** — they will be fully written when each domain is in migration scope. The full story bodies are written in the OWNING domain's `be-04-stories.md`.

### PRODUCT-BE-F-01 · CAT-4 · Medium (2–4d)
**Title:** [PLACEHOLDER] Migrate `productAttachments` + `discussionAttachments` to Attachment subgraph — BLOCKED-BY: attachment migration
**Phase:** F · **Complexity:** Very High · **Category:** CAT-4

**Scope (when unblocked):**
- Attachment subgraph adds `extend type ResourcesCount @key(fields: "productId partnerId")` with `@DgsEntityFetcher` + `@DgsData` for `productAttachments` and `discussionAttachments`.
- Implements ACL tree traversal + `product_packet_props` criticality filter and critical discussion → attachment path.
- Aggregation facade stops populating these two fields.
- Full story in: `output/attachment/be-04-stories.md`.

**Dependencies:** PRODUCT-BE-E-02, Attachment domain Phase 3 complete.

---

### PRODUCT-BE-F-02 · CAT-4 · Small (1–2d)
**Title:** [PLACEHOLDER] Migrate `discussions` to Discussion subgraph — BLOCKED-BY: discussion migration
**Phase:** F · Full story in: `output/discussion/be-04-stories.md`.

---

### PRODUCT-BE-F-03 · CAT-4 · Small (1–2d)
**Title:** [PLACEHOLDER] Migrate `sample` to Sample subgraph — BLOCKED-BY: sample migration
**Phase:** F · Full story in: `output/sample/be-04-stories.md`.

---

### PRODUCT-BE-F-04 · CAT-4 · Small (1–2d)
**Title:** [PLACEHOLDER] Migrate `measurementSets` to Measurement subgraph — BLOCKED-BY: measurement migration
**Phase:** F · Full story in: `output/measurement/be-04-stories.md`.

---

### PRODUCT-BE-F-05 · CAT-4 · Small (1–2d)
**Title:** [PLACEHOLDER] Migrate `claims` to Claims subgraph — BLOCKED-BY: claims migration
**Phase:** F · Full story in: `output/claims/be-04-stories.md`.

---

### PRODUCT-BE-F-06 · CAT-4 · Small (1–2d)
**Title:** [PLACEHOLDER] Migrate `productBoms` + `packagingBoms` to BOM subgraph — BLOCKED-BY: bom migration
**Phase:** F · Full story in: `output/bom/be-04-stories.md`.

---

### PRODUCT-BE-F-07 · CAT-4 · Small (1–2d)
**Title:** [PLACEHOLDER] Migrate `constructions` to Construction subgraph — BLOCKED-BY: construction migration
**Phase:** F · Full story in: `output/construction/be-04-stories.md`.

---

### PRODUCT-BE-F-08 · CAT-4 · Small (1–2d)
**Title:** [PLACEHOLDER] Migrate `watchlists` to Watchlist subgraph — BLOCKED-BY: watchlist migration
**Phase:** F · Full story in: `output/watchlist/be-04-stories.md`.

---

### PRODUCT-BE-F-09 · CAT-4 · Small (1–2d)

**Title:** Retire TechPack aggregation facade once all subgraph extensions are live

**Type:** Story
**Complexity:** Low
**Category:** CAT-4 — Federation / Stitching
**Phase:** F

**As a** DGS migration engineer,
**I want** to decommission the TechPack Aggregation Service and remove the Feign client from `plm-product`,
**so that** `ResourcesCount` is fully federated and the temporary facade has no remaining callers.

---

**Scope:**
- Remove `TechPackAggregatorFeignClient` and aggregation service config from `plm-product`.
- Update `TechPackDataFetcher` to return a pure stub (no Feign call) — gateway fan-out handles all fields via federation.
- Decommission aggregation service (`techpack-aggregator`): remove from infra, CI, and monitoring.

---

**Dependencies:** PRODUCT-BE-F-01 through F-08 all completed and in production.

---

**Acceptance Criteria:**
1. `TechPackAggregatorFeignClient` removed from `plm-product`.
2. `TechPackDataFetcher.getProductTechPackCountV1` returns `ResourcesCount` key fields only; all count fields null (filled by subgraphs).
3. All 10 `ResourcesCount` fields resolve correctly via federation — integration test passes.
4. Aggregation service health-check endpoint returns 404 (decommissioned).
5. No orphaned references to aggregation service URL in config.

**Test Cases:**
- [ ] Integration: all `ResourcesCount` fields populated via federation (no aggregation service hop)
- [ ] Monitoring: no alerts firing from removed aggregation service

---

## Capacity Planning Note

This document contains 63 stories across 9 phases (A–I). For the complete breakdown with all stories, estimated effort per story, and dependency chains, see the full generated output.

**Quick effort reference (with +20% buffer):**
- 1 engineer: ~172–255 days (~35–51 sprints at 5 days/sprint)
- 2 engineers (parallel where unblocked): ~90–130 days (~18–26 sprints)
- 3 engineers (parallel where unblocked): ~65–90 days (~13–18 sprints)

---

**Phase Completed:** Phase 4 — Migration Story Generation
**Domain:** `product`
**Analysis Mode:** Full
**DGS Target:** Green-field
**Skills Applied:** migration-story-generation, stitching-pattern-analysis
**Files Analyzed:** 6 files (Phases 1–3 output)
**Target Service:** `ProductService` (plm-product)
**EXT Service Calls Found:** 29 (from Phase 2)
**Output Files Written:**
- `output/product/be-04-stories.md`
- `output/product/be-04-po-summary.md`
**Next Phase:** Pipeline complete — all 6 artifacts ready.
**Open Questions:** None — see Decisions Required in `be-04-po-summary.md` for PO action items.
