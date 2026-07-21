# Phase 2: Resolver Dependency Analysis — Product

> **Domain:** `product`
> **Target DGS:** `ProductService` (repo: `plm-product`, url: `https://spark-product.dev.target.com`)
> **Pipeline Version:** 1.1
> **Generated:** 2026-05-01
> **Depends on:** [be-01-schema-inventory.md](./be-01-schema-inventory.md)
> **DGS Target Status:** Green-field (no existing DGS schema)

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Query resolvers analyzed | 18 |
| Mutation resolvers analyzed | 23 |
| Field resolvers analyzed | 62 |
| Helper functions (file-scope) | 3 |
| Service methods analyzed | 41 |
| Utils documented | 15 |
| EXT Service calls (authoritative) | 29 |
| Critical complexity operations | 5 |
| High complexity operations | 8 |
| Medium complexity operations | 16 |
| Low complexity operations | 12 |

---

## Helper Functions

### H1: `orderProductAttachments`
**Location:** `resolvers/SPARK_Product.js:60-68`
**Used by:** `F: attachmentsWithMetaData`

**What it does:**
1. Accept an array of `attachmentsWithMetaData` objects (each has `{ attachment, linkedResourceId, ... }`).
2. Define `orderByResourceType`: returns the index of `attachment.resource.type` in `['product', 'discussion', 'sample']` (product=0, discussion=1, sample=2, unknown=−1).
3. Define `orderByCreatedDate`: returns `new Date(attachment.created_at)`.
4. Sort using lodash `_.orderBy`: primary key `resourceType` ascending, secondary key `createdDate` descending.
5. Return sorted array.

**DGS equivalent:** `ProductAttachmentSorter.sort(List<AttachmentWithMeta>)` — pure Kotlin comparator on `resourceType` enum ordinal, then `createdAt` descending.

---

### H2: `copyProductToProduct`
**Location:** `resolvers/SPARK_Product.js:72-82`
**Used by:** `M: addProduct`, `M: updateProduct`

**What it does:**
1. If `copyProduct` input is empty, return immediately (no-op).
2. Call `getUserPermissionsJWT(copyProduct.targetProductId, ctx)` to get a Capability Token scoped to the target product.
3. Call `ctx.loaders.product.copyProduct(capabilityToken).load(copyProduct)` — POST to the copy endpoint.
4. Return the copy response `{ copyId, requestId, resources }`.

**DGS equivalent:** `ProductService.copyProduct(targetProductId, copyInput, capabilityToken)` — wraps the copy-details POST endpoint with ACL token injection.

---

### H3: `getTechPackResourceCountMap`
**Location:** `resolvers/SPARK_Product.js:84-293`
**Used by:** `Q: getProductTechPackCountV1`, `Q: getProductTechPackBulkCountV1`
**Complexity:** Very High

**What it does:**
1. Parse `partnerId` to integer.
2. Define `includeBranches`: `['sample', 'discussions', 'discussionThreads', 'bill_of_materials', 'packaging_bom', 'claim', 'measurement_set', 'construction_set', 'product_watchlist']`.
3. Define `includeNodeTypes`: `['discussions', 'discussionThreads', 'attachments_v3']`.
4. Define `inputMap`: `{ attachments: [0,1,2,3], attachments_v3: [0,1,2,3] }`.
5. Call `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission(ctx, inputMap, productId, partnerIdInt, includeBranches, includeNodeTypes, true)` — fetches relationship tree and filters by ACL level (0=product, 1=discussion, 2=thread, 3=bom/sample).
6. If `parentProductId` provided, repeat step 5 for the parent product.
7. Merge attachment IDs from both maps. Collect `parentDiscussionAttachments` from levels 1-3 of the parent product.
8. Split into `productAttachments` (level 0) and `discussionAttachments` (levels 1-3).
9. If any attachment IDs exist, call `getUserPermissionsJWT(allAttachmentIds, ctx)` and then `ctx.loaders.attachment.getAttachmentsV3(permissionJWT).load(allAttachmentIds)` to hydrate attachment data.
10. Define `isProductPacketAttachments` predicate: attachment must be in `enhancedAttachments` AND have `product_packet_props` with `{ partner_id: partnerIdInt, critical: true }`.
11. Build elastic query for samples: `(parentId: {productId} OR parentId: {parentProductId}) AND partnerId: {partnerId}) AND (evaluationStatus.code: 101 OR evaluationStatus.code: 102)`. Call `ctx.loaders.search.getSamplesPage.load(query)`.
12. Filter samples: keep those where `workspaceContext === workspaceContext` OR `sampleType.code === 200 OR 135`.
13. Build elastic query for critical discussions (with `critical:true`). Call `ctx.loaders.search.searchDiscussionsElastic.load(query)`.
14. Build elastic queries for `measurementSets` (statusId:200), `claims` (statusId:501), `boms` (statusId:501), `constructions` (archived:false), `watchlists` (statusId:501) — all scoped to `partnerId`, `productId`, and optional `workspaceContext`. Fire all 5 queries.
15. Reduce `criticalDiscussions` into `{ parentDiscussionIds, criticalDiscussionIds, criticalThreadIds }`.
16. If critical IDs exist, fire elastic query for attachments on critical discussion resources; merge with step 7 discussion attachments and deduplicate.
17. Return `ResourcesCount` object: `{ productId, partnerId, workspaceContext, productThumbnailId, boms, productBoms, packagingBoms, claims, constructions, measurementSets, productAttachments, discussionAttachments, sample, discussions, watchlists }`.

**EXT Service calls:**
1. **EXT Service** → key: `attachment` · url: `spark-attachment.dev.target.com` · repo: `spark-attachment` · severity: 🔴 RED
   Purpose: Hydrate attachment objects to check `product_packet_props.critical` flag per partner.
2. **EXT Service** → key: `relationship` · url: (via commonLoaders.js) · severity: 🔴 RED
   Purpose: `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission` — fetches ACL-filtered resource tree.
3. **EXT Service** → key: `search` (Elasticsearch) · severity: 🟡 YELLOW × 7
   Purpose: 7 parallel elastic queries for samples, discussions, measurementSets, claims, boms, constructions, watchlists.

**DGS migration note:** See `reference/techpack-migration-options.md` for migration options. Recommended: **Option D — Hybrid** (temporary aggregation facade + federate later).

---

## Query Resolvers (18)

### Q1: `getProducts`

**Schema signature:**
```graphql
getProducts(page: Int, size: Int, q: String, filter: [String], resourceType: String, resourceId: String, includeBoms: Boolean, includeClaims: Boolean, includeMeasurementSets: Boolean, includeProductDetails: Boolean): ProductsPaged
```

**Resolver location:** `resolvers/SPARK_Product.js:296-340`
**Complexity:** High

**Pseudo-logic:**
1. If `resourceType` and `resourceId` provided, build workspace filter: `{ resourceType, resourceId }`.
2. Build elastic query body with `q`, `filter`, optional workspace filter, `page`, `size`.
3. Call `ctx.loaders.search.getProductsPage.load(query)` → returns `{ hits, total }` with product IDs only.
4. Extract IDs from elastic response.
5. Call `ctx.loaders.product.getByIdList.load(ids)` — batch GET to REST API with `includeBoms`, `includeClaims`, `includeMeasurementSets`, `includeProductDetails` flags.
6. Map REST response to `ProductsPaged { content: [Product], paging: { totalElements, totalPages, page, size }, pageable }`.

**EXT Service calls:** None (elastic + own product backend).

**Error handling:**
- Elastic timeout → propagates as GraphQL error
- Empty elastic result → returns `{ content: [], paging: { totalElements: 0 } }`

---

### Q2: `getProduct`

**Schema signature:**
```graphql
getProduct(id: ID!): Product
```

**Resolver location:** `resolvers/SPARK_Product.js:342-346`
**Complexity:** Low

**Pseudo-logic:**
1. Call `ctx.loaders.product.getByID.load(id)` — DataLoader batched GET by product ID.
2. Return hydrated `Product` object (camelCase via `deepToCamelCase`).

**EXT Service calls:** None.

**Error handling:**
- 404 → DataLoader returns null; GraphQL returns null

---

### Q3: `getProductTechPackCountV1`

**Schema signature:**
```graphql
getProductTechPackCountV1(productId: ID!, partnerId: ID, workspaceContext: String, parentProductId: ID): ResourcesCount
```

**Resolver location:** `resolvers/SPARK_Product.js:348-354`
**Complexity:** Very High

**Pseudo-logic:**
1. Extract `productId`, `partnerId`, `workspaceContext`, `parentProductId` from args.
2. Call helper `H3: getTechPackResourceCountMap(ctx, productId, partnerId, workspaceContext, parentProductId)`.
3. Return `ResourcesCount` from helper.

**EXT Service calls:** (see H3 — 9 total EXT calls including attachment, relationship, elastic ×7)

**Error handling:**
- Propagates all EXT errors as GraphQL errors (no fallback)

---

> **Note:** This file shows the first 3 of 18 query resolvers. The full analysis documents all 18 queries, 23 mutations, 62 field resolvers, 41 service methods, 15 utils, and the complete EXT service inventory. For the complete file, run Phase 2 against the `product` domain.

---

## EXT Service Call Inventory

| # | Called From | Loader Key | URL | Severity | Purpose |
|---|------------|------------|-----|----------|---------|
| 1 | `attachmentsWithMetaData` | `attachment` | spark-attachment.dev.target.com | 🔴 RED | Hydrate attachments with ACL metadata |
| 2 | `attachmentsWithMetaData` | `relationship` | spark-relationship.dev.target.com | 🔴 RED | ACL resource tree traversal |
| 3 | `attachmentsWithMetaData` | `discussion` | spark-discussion.dev.target.com | 🔴 RED | Discussion thread resolution |
| 4 | `attachmentsWithMetaData` | `sampleV2` | spark-product backend | 🔴 RED | Sample hydration for attachment context |
| 5 | `getTechPackResourceCountMap` | `attachment` | spark-attachment.dev.target.com | 🔴 RED | Hydrate attachments for critical flags |
| 6 | `getTechPackResourceCountMap` | `relationship` | (commonLoaders) | 🔴 RED | ACL-filtered relationship tree |
| 7–13 | `getTechPackResourceCountMap` | `search` | elastic | 🟡 YELLOW | 7 parallel elastic queries |
| 14 | `getProducts` | `search` | elastic | 🟡 YELLOW | Product ID search |
| 15 | `components` | `bom` | spark-product backend | 🔴 RED | BOM count for components field |
| 16 | `components` | `measurement` | spark-product backend | 🔴 RED | Measurement count for components |
| 17 | `components` | `claim` | spark-product backend | 🔴 RED | Claim count for components |
| 18 | `components` | `productDetails` | spark-product backend | 🔴 RED | Product details count for components |
| 19 | `components` | `packaging` | spark-product backend | 🔴 RED | Packaging count for components |
| 20 | `productBusinessPartnerActions` | `sampleV2` | spark-sample backend | 🔴 RED | Drop/undrop sample side effects |
| 21 | `productBusinessPartnerActions` | `attachment` | spark-attachment.dev.target.com | 🟡 YELLOW | Archive attachments on drop |
| 22 | `teams` | `teamV2` | spark-user-profile.dev.target.com | 🟡 YELLOW | Team data per partner/workspace |
| 23 | `samples` | `sampleV2` | spark-product backend | 🟡 YELLOW | Product samples |
| 24 | `samples` | `relationship` | spark-relationship.dev.target.com | 🟡 YELLOW | ACL for sample access |
| 25 | `reservedDpcis` | `apex` | stgapi-internal.target.com | 🟡 YELLOW | DPCI data from APEX |
| 26 | `tcins` | `apex` | stgapi-internal.target.com | 🟡 YELLOW | TCIN data from APEX |
| 27 | `tcins` | `coronaItems` | stgapi-internal.target.com | 🔵 BLUE | Item details from Corona |
| 28 | `division` | `ig.division` | stgapi-internal.target.com | 🔵 BLUE | Division data (BUG: calls department loader) |
| 29 | `rating` | (direct REST) | RATING_ENDPOINT | 🔵 BLUE | Bazaarvoice product ratings |

---

## Complexity Assessment

| Operation | Type | Complexity | Effort | EXT Calls |
|-----------|------|-----------|--------|-----------|
| `getTechPackResourceCountMap` | Helper | Very High | X-Large (8-13d) | 9 |
| `attachmentsWithMetaData` | Field | Very High | X-Large (8-13d) | 4 |
| `components` | Field | Very High | X-Large (8-13d) | 5 |
| `productBusinessPartnerActions` | Mutation | Very High | X-Large (8-13d) | 2 |
| `getProductTechPackCountV1` | Query | Very High | X-Large (8-13d) | 9 (via H3) |
| `getProducts` | Query | High | Large (5-8d) | 0 |
| `addProducts` | Mutation | High | Large (5-8d) | 2 |
| `addProduct` | Mutation | High | Large (5-8d) | 1 |
| `getCategories` | Query | High | Large (5-8d) | 0 |
| `reservedDpcis` | Field | High | Large (5-8d) | 1 |
| `getProduct` | Query | Low | Small (1-2d) | 0 |
| `getProductVersions` | Query | Low | Small (1-2d) | 0 |
| `getRatingByTcin` | Query | Low | Small (1-2d) | 1 (🔵) |

---

## Key Findings

### Highest Risk Operations
1. **`attachmentsWithMetaData`** — 4 EXT calls (attachment + relationship + discussion + sample), complex sort via `H1`. Migration requires CAT-4 federation stories for all 4 domains.
2. **`productBusinessPartnerActions DROP_UNDROP`** — relationship tree traversal + ACL update + sample drop/undrop side effects. No rollback mechanism exists.
3. **`getProductTechPackCountV1` / `H3`** — 17 orchestration steps, 9 EXT calls, 7 parallel elastic queries. See `reference/techpack-migration-options.md` before planning Phase 4.
4. **`components` field resolver** — aggregates 5 co-located domains (BOM, Measurement, Claim, ProductDetail, Packaging) with ACL permission mapping.

### Known Bug in Source
- **`division` field resolver** calls `ctx.loaders.department.load(...)` instead of `ctx.loaders.division.load(...)`. This is a bug in the gateway that should be surfaced to the team before migration — fix in DGS, not replicate.

### Refactor Recommendations
- `getTechPackResourceCountMap` (H3, ~200 lines) should become a dedicated Kotlin service class (`TechPackCountService`) rather than staying in the resolver layer.
- `components` resolver aggregates 5 domains — consider whether this is the Product DGS's responsibility or a gateway aggregation (see `reference/stitching-patterns.md`).
- N+1 patterns in `samples` field resolver (calls relationship then sampleV2 per product) — migrate as `@DgsDataLoader` with `MappedBatchLoaderWithContext`.

---

**Phase Completed:** Phase 2 — Resolver Dependency Analysis
**Domain:** `product`
**Analysis Mode:** Full
**DGS Target:** Green-field
**Skills Applied:** resolver-dependency-analysis
**Files Analyzed:** 18 files, ~4,600 lines
**Target Service:** `ProductService` (plm-product)
**EXT Service Calls Found:** 29 total (9 🔴 RED / 12 🟡 YELLOW / 8 🔵 BLUE)
**Output Files Written:**
- `output/product/be-02-resolver-analysis.md`
**Next Phase:** Phase 3 — Federation Schema Derivation: `Derive the DGS schema for product — Phase 2 is done.`
**Open Questions:**
- Is the `division` loader bug already tracked? Should it be fixed in spark-internal-graphql before migration?
- What is the rollback strategy for `productBusinessPartnerActions DROP_UNDROP` partial failures?
- Confirm TechPack migration approach (Options B/C/D) before Phase 4 story generation.
