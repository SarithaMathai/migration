# Phase 2D — Service Class + Utility Function Analysis (`product` domain)

> Scope: [services/Product.js](spark-internal-graphql/packages/data-source-spark/src/services/Product.js) (589 lines, 42 methods) + utility modules called from `SPARK_Product.js`.
> Severity legend: 🔴 critical · 🟡 important · 🔵 platform

---

## D1. `ProductService` class — REST clients (HTTP-level concern)

`ProductService` is **REST plumbing**, not business logic. Every method is a thin wrapper around `loadOne` / `loadListing` / `postOne` / `putOne` / `deleteOne` HOFs that produce JWT-curried, batched, request-scoped DataLoaders against the Java/Spring `enterprise_product_development_products` service.

**In DGS, all 42 methods collapse into ~10 Kotlin service interfaces:**
- `ProductReadService` (queries), `ProductWriteService` (mutations), `ProductElasticSearchService`, `ProductCopyService`, `ProductRuleService`, `ProductComponentStatusService`, `ProductVersionService`, `RatingClient` (external), `RelationshipClient` (cross-domain helper), `ApexClient` (cross-domain).
- All current `loadOne`/`loadListing` HOFs **disappear** — replaced by Spring `@FeignClient` or `RestTemplate` + DGS `@DgsDataLoader` for batching.

### D1.1 Configuration
| Field | Source | DGS equivalent |
|---|---|---|
| `endpoint` | `process.env.PRODUCT_ENDPOINT` | Application property `product.endpoint` (already same JVM in plm-product → **internal call, no HTTP**) |
| `endpointv1` | `${endpoint}/enterprise_product_development_products/v1` | Internal Kotlin service method |
| `endpointv2` | `${endpoint}/enterprise_product_development_products/v2` | Internal Kotlin service method |
| `elasticSearchEndpoint` | `process.env.PRODUCT_SEARCH_ENDPOINT` | `search.endpoint` (separate Feign client to Elasticsearch service) |
| `endpointCopy` | `${SEARCH_ENDPOINT}/requests/v1` | Internal Copy service |
| `ratingEndpoint` | `process.env.RATING_ENDPOINT` | External Feign client `RatingClient`. **🔵 BLUE — stays Hive-stitched** |
| `ratingKey` | `SPARK_GATEWAY_API_KEY` | Spring config secret |

### D1.2 Method Inventory (all 42)

> **Important**: ~30 of these become internal Kotlin method calls inside `plm-product` after migration (the GraphQL gateway → DGS hop is removed and the DGS calls its own service code directly). Only `getRatingByTcin` (external rating service) and `searchProductDeptRules / searchProductBPRules / searchProductRules` (calls to `spark_rules` legacy endpoint) remain HTTP calls.

| # | Method | HOF | Endpoint | Verb | Purpose | Used by (Phase 2A/B/C) | DGS notes |
|---|---|---|---|---|---|---|---|
| 1 | `getPage` | `loadListing` | `${v1}?productId=…&page&size&sort` | GET | Paged product list with `getByID` priming | Q1, Q9 | Replace with JPA paged query + DataLoader registry |
| 2 | `getByID` | `loadOne` | `${v1}?productId=ID&size=N` | GET | Bulk get by IDs (filters JSON response) | Many Q+F | Native `findAllById` |
| 3 | `getCopyStatus` | `loadOne` (no batch) | `${v2}/count/resource-type?copyId=…` | GET | Copy job status | Q7 | Direct service call |
| 4 | `createBulk` | `postOne` | `${v1}/bulk` | POST | Bulk product create | M2 | Service method |
| 5 | `bulkUpdate` | `putOne` | `${v1}/mass_update` | PUT | Bulk product update | M3 | Service method |
| 6 | `addTeams` | `postOne` | `${v1}/{productId}/resources/bulk` | POST | Add teams (resources) to product | M5 | Service method |
| 7 | `updateBusinessPartnerStatuses` | `putOne` | `${v1}/{productId}/status_update/bulk` | PUT | Update BP statuses | M11 | Service method |
| 8 | `dropUndropProductBusinessPartner` | `permissionJWT → postOne` | `${v2}/{productId}/drop-undrop-partner` | POST | Combined drop/undrop with JWT | M11 | **Keep JWT pattern → DGS `@DgsContext` capability token header** |
| 9 | `dropProductBusinessPartner` | `postOne` | `${v1}/{productId}/drop-partner/{partnerId}` | POST | Legacy drop | (schema-drift wrapper) | Same service method but no JWT — legacy, mark for deprecation |
| 10 | `unDropProductBusinessPartner` | `postOne` | `${v1}/{productId}/undrop-partner/{partnerId}` | POST | Legacy undrop | (schema-drift wrapper) | Same — mark deprecated |
| 11 | `updateProduct` | `putOne` | `${v1}/{id}` | PUT | Update single product | M9 | Service method |
| 12 | `carryForwardProduct` | `putOne` | `${v1}/{productId}/carry_forward/{workspaceId}` | PUT | Copy product into a workspace | M10 | Service method |
| 13 | `removeProductResources` | `deleteOne` | `${v1}/{productId}/resources/bulk?resourceList=…` | DELETE | Remove resources (teams/etc.) | M6 | Service method |
| 14 | `removeProductBusinessPartner` | `permissionJWT → deleteOne` | `${v2}/{productId}/partners/bulk?partnerList=…` | DELETE | Remove BP (JWT-protected) | (schema-drift wrapper) | Keep JWT, service method |
| 15 | `deletePartnerWorkspaceStatuses` | `deleteOne` | `${v1}/{productId}/workspaceAttributes/{workspaceId}` | DELETE | Drop a workspace attribute row | M16 | Service method |
| 16 | `getFilteredProducts` | `loadListing` | `${elastic}/search?resourceType=…` | GET | Returns just `human_id` list | (internal) | Elasticsearch client |
| 17 | `getFilteredProductsListing` | `loadListing` | `${elastic}/search?…many flags` | GET | Returns full page of elastic content | Q1 (with hydration flags) | Elasticsearch client — preserve all `include*` flags |
| 18 | `getFilteredSamples` | `loadListing` | `${elastic}/search?…buildSampleURLParam` | GET | Reduces to flat `humanId` list | Field `samples`, `sampleIds` | Elasticsearch client |
| 19 | `getProductCategories` | `loadListing` | `${elastic}/search/{snake_type}?…` | GET | Right-rail facet aggregations | Q12 → `categories` field | Elasticsearch aggregation query |
| 20 | `getByIdList` | `loadListing` | `${v1}?productId=csv&size=10000` | GET | Bulk fetch by ID list (primes `getByID`) | Field `ancestryProducts` | `findAllById` |
| 21 | `addProduct` | `postOne` | `${v1}` | POST | Create single product | M1 | Service method |
| 22 | `getStatus` | `loadListing` | `${v1}/masterData/status` | GET | Master product status list | Q11 | Reference data — consider caching |
| 23 | `updateViewToggle` | `putOne` | `${v1}/{productId}/workspaceAttributes/{workspaceId}` | PUT | Toggle visibility | M14 | Service method |
| 24 | `updateWorkspaceAttributes` | `putOne` | `${v1}/{productId}/workspaceAttributes/{humanId}` | PUT | Update workspace attrs payload | M15 | Service method |
| 25 | `getWorkspaceProducts` | `loadListing` | `${elastic}/search?resourceType=workspaces&…` | GET | Workspace-scoped product listing | Q2 | Elasticsearch client |
| 26 | `copyProduct` | `permissionJWT → postOne` | `${v2}/copy-details` | POST | JWT-protected copy job | M7 | Keep JWT pattern |
| 27 | `addBusinessPartnersWithType` | `postOne` | `${v1}/{productId}/partners-add/bulk` | POST | Add BPs (typed) | M11 add-bp case | Service method |
| 28 | `updateProductTeamsWorkspaceContext` | `putOne` | `${v1}/{productId}/manage_workspace_teams` | PUT | Reassign teams across workspaces | M12 | Service method |
| 29 | `getVersions` | `loadListing` | `${v1}/{id}/versions?page&size` | GET | Product version history | Q8 | Service method |
| 30 | `linkProduct` | `putOne` (`throwOnError: true`) | `${v1}/{childProductId}/link_product` | PUT | Establish parent/child link | M21 | **`throwOnError: true` is unusual — port as a checked exception** |
| 31 | `unlinkProduct` | `putOne` | `${v1}/{childProductId}/unlink_product` | PUT | Remove parent/child link | M22 | Service method |
| 32 | `getRatingByTcin` | `loadOne` (`batch:false`, `skipJsonParse:true`) | `${rating}?reviewType=product&includes=statistics&reviewedId={tcin}&key={key}` | GET | External rating fetch | Field `rating`, Q? `getRating` | **🔵 External Feign client. JSON.parse done in resolver — preserve.** |
| 33 | `getAllRules` | `loadListing` | `${endpoint}/spark_rules/v1` | GET | All product rules | Q `getRules` (impl in 2A) | Service method — note **separate `spark_rules` service** |
| 34 | `getAllInsightsRules` | `loadListing` | `${endpoint}/spark_rules/v1/insights` | GET | Insights-flavored rules | Q `getInsightsRules` | Same |
| 35 | `getRuleById` | `loadOne` (`batch:false`) | `${endpoint}/spark_rules/v1/{id}` | GET | Single rule | Q `getRuleById` | Same |
| 36 | `addRule` | `postOne` (`rulesRequestTransformer`) | `${endpoint}/spark_rules/v1` | POST | Create rule | M `addRule` | Same — uses `productUtils.rulesRequestTransformer` |
| 37 | `updateRule` | `putOne` | `${endpoint}/spark_rules/v1/{id}` | PUT | Update rule | M `updateRule` | Same |
| 38 | `deleteRule` | `deleteOne` | `${endpoint}/spark_rules/v1/{id}` | DELETE | Delete rule | M `deleteRule` | Same |
| 39 | `getAvailableRules` | `loadListing` | `${endpoint}/spark_rules/v1/rules` | GET | Available rule catalog | Q `getAvailableRules` | Same |
| 40 | `searchProductDeptRules` | `loadListing` | `${endpoint}/spark_rules/v1/search?productIds&departmentIds&activeOnly` | GET | Legacy (only if `USE_NEW_RULES_API=false`) | Q `getProductRules` (legacy) | **Conditionally registered — flag drift** |
| 41 | `searchProductBPRules` | `loadListing` | `${endpoint}/spark_rules/v1/search?productIds&businessPartnerIds&activeOnly` | GET | Legacy | Q `getProductRulesByBP` (legacy) | Conditionally registered |
| 42 | `searchProductRules` | `loadListing` | `${endpoint}/spark_rules/v1/search_mapped?…` | GET | Legacy (mapped) | Q `getProductRulesMapped` (legacy) | Conditionally registered; uses `productRuleResponseTransformer` |
| 43 | `updateComponentStatus` | `putOne` | `${v1}/component_status_update/bulk` | PUT | Bulk component status update | M20 | Service method |

### D1.3 Cross-cutting Service Patterns (preserve in DGS)
1. **`primeKey: product => product.productId`** — every write returning a product re-primes the `getByID` cache. DGS port: after-write callback that updates the request-scoped DataLoader cache.
2. **`getDataLoader: () => this.getByID`** — write methods reference the read loader for cache invalidation. DGS port: shared `DataLoaderRegistry`.
3. **JWT-curried writes** (`permissionJWT => postOne(...)`) for 3 methods (#8, #14, #26): the JWT is acquired *before* the call and passed as `SPARK-Capability-Token` header. DGS port: forward the capability token via `DgsRequestData` headers; do not regress to ad-hoc per-call signing.
4. **`USE_NEW_RULES_API`** env flag gates registration of methods #40–42. DGS port: Spring `@ConditionalOnProperty` — but ideally **delete the legacy branch** as part of this migration (it's already dormant in most environments per the Q phase notes).
5. **`throwOnError: true`** on `linkProduct` (#30) is the **only** method that surfaces backend errors as thrown exceptions; all others swallow → null. Port as checked exception in DGS; mention in Phase 4 cross-cutting findings.
6. **`skipJsonParse: true`** + `transform: rating => JSON.parse(rating)` in `getRatingByTcin` indicates the rating service returns text/plain. Preserve in Feign client config.

---

## D2. Utility Modules Called from `SPARK_Product.js`

### D2.1 [utils/Product/attachmentUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/attachmentUtils.js)

The single most-touched util — supplies the merge engine for `attachmentsWithMetaData`, `attachmentsV3`, and `components`.

| Export | Purpose | Severity | DGS port |
|---|---|---|---|
| `initialCountsByBp` | Frozen array `[{ bpType:'targetOnly', counts:0 }, { bpType:'totalCount', counts:0 }]` — seed for per-resolver counters | low | Kotlin `data class AttachmentCountSeed` |
| `orderAttachmentsByType(attachments)` | Sort: product-related first (rank 0), others (rank 1); within rank by `createdAt` DESC | low | Comparator |
| `orderComponentsByDate(components)` | Sort by `createdAt` DESC | low | Comparator |
| `convertV2AccessToV3(partners)` | Wrap a flat partner-id list into `{ locked:false, fabSuppliers:[], designPartners:[], merchVendors:[], external:false, bps:partners }` | low | Tiny mapper |
| **`resolveRelationIds(relations, countsByBp, resourceId, ctx, onlyProductPacketFiles, primaryThumbnailId)`** | Partitions `relations[0].nodes` into 4 buckets, fetches 2 attachment JWTs, fetches v2 + v3 attachments (or single elastic call if `attachmentElasticResponseFeatureFlag`), fetches discussions/threads in batches of `CHUNK_SIZE`, fetches ACL in batches of 250, delegates to `createAttachmentPaged`. | 🔴 **High** | Kotlin service method `AttachmentRelationResolver` — preserve flag branch as **`@DgsData` feature toggle** |
| `get3DmodelFile(attachment, ctx)` | If FBX + valid gallery + not Showdog: fetch renders, find GLB, return `{ fileId, fileName }` | medium | One DGS data fetcher on attachment type |
| `addPartnersToCountObject(partners, countsByBp)` | **Mutates** `countsByBp`: bumps per-bp counts (creates entry if missing), increments `totalCount` always, increments `targetOnly` when no partners | low | Pure helper, but the **mutation across closures is the source of `cloneDeep`** in the resolver — port as immutable accumulator |
| **`createAttachmentPaged(attachments, permissions, discussionThreads, discussions, resourceId, countsByBp, onlyProductPacketFiles, primaryThumbnailIdToInclude, ctx)`** | The merge engine: for each attachment, extract bps/dps/MerchVendor grantees, link to its discussion or thread head (for ACL-discovered draft suppression), filter productPacketFiles, build normalized shape with **v2/v3 dual-naming fallback** (`document_id || documentId`, etc.) | 🔴 **High** | Kotlin `AttachmentPagedAssembler` |
| `filterAttachmentsOrComponents(items, args, primaryThumbnailToInclude)` | Filters by `workspaceId`, `partnerId` (with `'targetOnly'` sentinel), `tags`, `type`, `archived`, `onlyProductPacketFiles` | medium | DGS `@DgsData` filter |
| `getProductOrWorkSpaceAttachments(resourceId, countsByBp, args, ctx, onlyProductPacketFiles, resourceThumbnailId)` | Calls `searchAttachmentsByRelatedResource`, gathers all discussions + discussionReplies (loop, swallows errors), gathers ACL by resourceIds, calls `createAttachmentPaged`, then filters. **N+1 discussion replies** | 🔴 **High** | Same — batch the reply loop |

**Cross-cutting concern** in this module: **camelCase/snake_case dual-naming fallback** (`document_id || documentId`, `human_id || humanId`, etc.) appears in every attachment mapper. DGS port: single normalization layer at the Elasticsearch client boundary.

---

### D2.2 [utils/Product/partnerUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/partnerUtils.js)

| Export | Purpose | Severity | DGS port |
|---|---|---|---|
| `getAreStatusesEqual(statuses)` (internal) | All statuses share same `statusId` | low | Pure |
| `VARIES_STATUS` / `DEFAULT_STATUS` constants | `{id:0, name:'Varies'}` and `{id:100, name:'Prototype'}` | low | Kotlin objects |
| `filterOutDesignPartners({partnerType})` | `partnerType !== 5` (drops Design Partners) | low | Pure |
| `getProductStatus(product, args)` | Iterates BPs (filtered to non-DP). If statuses vary across BPs OR within a BP → returns `VARIES_STATUS`. If `workspaceIdFilter`: only count statuses for that workspace. Default `DEFAULT_STATUS`. | medium | Pure Kotlin function |
| `getFinalPartnerStatuses(product, args)` | Per-BP status summary used by `vendorAttributes`. With `workspaceIdFilter` returns workspace-specific status; without, returns 'Varies' synthetic when statuses disagree. | medium | Pure Kotlin function |

Both methods are **pure** — perfect for direct Kotlin port. No external calls.

---

### D2.3 [utils/Product/productUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/productUtils.js)

| Export | Purpose | Severity | DGS port |
|---|---|---|---|
| `getNotRemovableWorkspaceIds(product, args, ctx)` | Calls `samples` + `components` field resolvers reflectively, then unions workspace IDs from teams-bearing `productWorkspaceInfo/Attributes` rows + each sample's `workspaceContext` + each component's `workspaceContext`. | 🟡 medium | Replace reflective field-resolver call with direct service-method call |
| `rulesRequestTransformer(rule)` | Camel → snake transform for rule create/update payloads | low | Mapper / `@JsonProperty` |
| `productRuleResponseTransformer(response)` | Flattens `{ product_rules: { id: rule, … } }` → `[ { ...rule, product_id: id }, … ]` | low | Mapper |
| `sanitizedProductDescription(description)` | Strip non-printable characters (regex `/[^\x20-\x7E\xA0-\xFF]/g`) and trim | low | Pure |

---

### D2.4 [utils/Product/teamUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/teamUtils.js)

| Export | Purpose | DGS port |
|---|---|---|
| `filterTeamsByPartnerOrWorkspaceId(teams, product, args)` | Two filters: by `workspaceId` (cross-reference into `product.productWorkspaceAttributes`) and by `partnerId` with `'targetOnly'` sentinel. | Pure Kotlin function |

---

### D2.5 [utils/Product/getReservedDpcisFromApex.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/getReservedDpcisFromApex.js)

| Export | Purpose | Severity | DGS port |
|---|---|---|---|
| `calculateDpciStatus(item, productId)` | Returns `'reserved' | 'locked' | null`. Reserved = `systemStatusValue === 'New' && !itemSetup && dpci && sparkPids contains productId && bpId`. Locked = `itemSetup && (same commonFieldsCheck)`. | low | Pure |
| `getReservedDpcisFromApex(product, ctx)` | **🔵 APEX platform call** with `bpId` (all BPs), filter `section_data.item.spark_pids = productId`, sort by `create_time DESC`. Reduces to per-BP grouped map; if both 'reserved' and 'locked' present for same DPCI, **'locked' wins** (overrides earlier 'reserved'). HTML-entity-decode the description. | 🔵 **Platform — must stay Hive-stitched** | External call retained; consider DGS Feign client to APEX |

---

### D2.6 [utils/removePartnerUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/removePartnerUtils.js)

| Export | Purpose | Severity | DGS port |
|---|---|---|---|
| `getPartnersFromAccess(accesses)` | Walks ACL `permissions[*].abstractAccessGroup.grantees` to extract BP IDs | low | Pure |
| `getDiscussionPartners(discussions)` | Unions `partnerId + droppedPartnerIds + designPartnerId` per discussion | low | Pure |
| `getWorkspacePartnersNotRemovable(ctx, workspace)` | Workspace variant — calls `discussionsV2` + `attachmentsWithMetaData` field resolvers on workspace | 🟡 | Service-method port |
| `getProductPartnersNotRemovable(ctx, product, info)` | **For Phase 2C field `notRemovablePartnerIds`.** Calls 4 field resolvers (`discussionsV2`, `attachmentsV3`, `components`, `samples`), then fetches watchlist by elastic query (`parentId:{pid} AND workspaceContext:{wsid} AND statusId:501`), then ACL-batches all detail IDs (250 chunk), unions all BP IDs + `owningPartnerId`. | 🔴 **High — fan-out of all heavy field resolvers** | Refactor in DGS to call underlying services directly (not field resolvers); same logical union |

---

### D2.7 [utils/ProductAskUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/ProductAskUtils.js)

| Export | Purpose | Severity | DGS port |
|---|---|---|---|
| `getProductAsksForWorkspace(ctx, { workspaceId, productIds, page, size })` | Fetches workspace → if no `setDateRange` returns empty page → else extracts `from/to`, flattens `departments[*].classId[*]` into `classIds`, calls `productAsk.searchProductAsks`. | medium | Service-method port; **uses CommonJS `module.exports` — the only file in the read set that does** |

---

### D2.8 [utils/Product/userGroupUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/Product/userGroupUtils.js)

| Export | Purpose | DGS port |
|---|---|---|
| `getUserGroup(ctx, id)` | Wrapper around `SPARK_UserGroup.Query.getUserGroups` returning `participantDetails` or `{teams:[], users:[]}` | Service-method port |

Not called by `SPARK_Product.js` directly; included for completeness — likely used by Discussion sibling.

---

### D2.9 [utils/accessControlUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/accessControlUtils.js)

| Export | Purpose | DGS port |
|---|---|---|
| `getToken(ids, headers, logContext)` | Standalone fetch against ACL service — used inside loader definitions (not from resolvers directly) | Spring `RestTemplate` call inside Feign interceptor |
| **`getAccessControlBatch(resourceIds, chunkSize, ctx)`** | Chunks `resourceIds` by `chunkSize`, sequential `Promise` loop calling `accessControl.getPermissionsByPost`, concatenates. **Sequential, not parallel.** Used by `components`, `attachmentsWithMetaData`, `getProductPartnersNotRemovable`. | 🔴 **High — performance hot-spot.** DGS port should parallelize chunks |

---

### D2.10 [utils/commonLoaders.js](spark-internal-graphql/packages/data-source-spark/src/utils/commonLoaders.js) — selected exports

The file is large; the exports referenced from `SPARK_Product.js` (directly or transitively) are:

| Export | Purpose | DGS port |
|---|---|---|
| `loadTags(ids, ctx)` | Single tag fetch with size=10000 | Tag service call |
| `makeTagFromBp(bpId)` | Stringify BP id (for ACL tag) | Pure |
| `getACLGroupFromPermissions(perms, type, dropped, partnerIds)` | Find a specific ACL group type, filter dropped if requested, return cleaned `abstractAccessGroup` | Pure |
| `getDroppedPartnersFromACL(perms)` | Extract dropped MerchVendor/bps/dps grantees with type tag | Pure |
| `addRelationship` / `addBulkRelationShip` / `removeRelationship` / `deleteRelationshipResource` | Relationship CRUD wrappers (swallow errors) | RelationshipClient |
| **`getUserPermissionsJWT(ids, ctx)`** | If empty → `''`. Else `accessControl.getUserAccess.load(ids)`. **Used by:** `teams`, `attachments`, `associateProductsAsks`, `variations`, `attachmentsWithMetaData`. | 🔴 **High** — JWT pattern central to ACL-gated DGS port |
| `getUserPermissionsJWTHelper(ids, ctx)` | Same but switches to `getUserAccessByPost` when ids > 50 (GET URL length limit) | Same |
| `getUserPermissionsJWTByProxy / Unencoded` | Proxy-permission variants | Same |
| `associateAttachmentResourcesV3` | Attachment relation + attribute update via JWT | Service method |
| `removeAccessControlPermissionsV2` / `addAccessControlPermissionsV2` | Team-aware bulk ACL grant/revoke | Service method |
| `getPermissions / hasSecurity / getACLPermissions / getACLPermissionsForResource` | Read helpers | Service method |
| `getDroppedACLGroups / getAccessUserGroup` | Specialized ACL extractors | Pure mappers |
| `createAccessControl / createAccessControlWithExistingGroup` | ACL creation for new resources | Service method |
| `addPartnerToGroup / deletePartnerFromGroup / addAccessControlDiscussionAttachment / getAccessBPGroup` | Grant management | Service method |
| `addBulkPermissionToAttachments` (continues beyond 500-line read) | Bulk discussion-style permissions | Service method |

**DGS implications:** every JWT-curried loader currently in the gateway becomes an **`@DgsContext` capability token** passed through Hive Gateway to plm-product. The DGS service uses it to call accessControl's `getPermissions` once and caches per-request.

---

### D2.11 [utils/vmmUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/vmmUtils.js)

| Export | Purpose | DGS port |
|---|---|---|
| `getRelatedSuppliersForMVs(ctx, merchVendorIds, roles)` | Per-MV fetch from VMM, filter `relationship[]` by relatedBpRole + status='Approved', intersect across all MVs | 🔵 VMM platform call — stays Hive-stitched |
| **`loadManyIncludeEmptyResponse(loader, keys)`** | `Promise.all(keys.map(key => loader.load(key).then(res => Array.isArray(res) && res.length===0 ? null : res)))` — **used pervasively by the categories switch in Phase 2C** | Pure helper |
| `handleMissingBp(id, ctx)` (internal) | Fallback to `getPartnersFromUserProfileBackup` when VMM returns nothing; returns `{ bpId, bpName: 'MISSING_PARTNER' or backup name }` | Same logic |
| **`loadBps(ctx, ids)`** | Per-id `vmm.getByID` with `handleMissingBp` fallback, then `sortBpByName`. **Used by:** `businessPartners`, `droppedPartners`, `vendorAttributes`, `ProductRules.businessPartners`, categories `businessPartners` case. | 🔵 VMM — stays stitched. DGS DataLoader |
| `loadBp(ctx, id)` | Singular variant | Same |
| `loadLaundries(ctx, ids)` | Location service loop | Location platform — stays stitched |
| **`loadBpsWithType(partners, ctx)`** | Load bps + attach `associatedPartnerType` (default 8) by matching original `partnerId` | Same |
| `loadBpWithType(ctx, id)` | Singular | Same |
| `getCapabilityIdsByType / getFilteredLocations` | Capability matching for laundry filter | Pure |

---

### D2.12 [utils/discussionUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/discussionUtils.js) — selected

| Export | Purpose | DGS port |
|---|---|---|
| `CHUNK_SIZE = 250` | Default batch size for discussion fetches | Constant |
| `makeTagFromResource(resourceId)` | `Discussion-{id}` ACL tag string | Pure |
| `createDiscussionAccessControl` / `createDiscussionThreadsAccessControl` / `updateDiscussionAccessControl` | ACL creation for discussion entities (used by sample/thread mutations) | Service method |
| `setSecurityForSampleDiscussionAttachment` | Cascade ACL from sample to thread to attachment | Service method |
| `createSampleAttachmentRelationship` + helpers | Relationship payload builders for sample → attachment | Pure mappers |
| `createSampleDiscussionRelationships` + helpers | Sample → discussion → thread relationship cascade | Pure mappers |
| `createDiscussionThreadRelationship` + helper | Discussion → thread cascade | Pure mapper |
| `createSampleDiscussionSecurity` | Bulk ACL for sample discussion + thread | Service method |
| `createSampleDiscussionThread` / `createSampleDiscussions` / `bulkAddSampleDiscussionsUtil` | Discussion creation orchestrators (with relationship + ACL + attachment update fan-out) | Service method |
| `getDiscussionResource(discussion, ctx)` | Polymorphic: based on `resources.mappings` key (product/workspace/sample/palette/artworks/…) calls the right Query resolver. Falls through ~10 cases. | DGS `@DgsTypeResolver` over `DiscussionResource` union — calls per-domain DGS |
| `getDiscussionsBatch / getDiscussionThreadsBatch / getDiscussionRepliesV2` (referenced from attachmentUtils) | Batched discussion fetches | Service method |

The discussion utils module is shared with several siblings (claims, samples) — **not a product-only port**. Migration story: keep in shared util library.

---

### D2.13 [utils/componentStatusUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/componentStatusUtils.js)

| Export | Purpose | DGS port |
|---|---|---|
| `getCountByComponents(components)` | Group components by `type`, sum counts, recurse into per-status counts | Pure |
| `getCountByComponentStatus(component, initialCounts)` | Per-`workspaceId` and `'ALL'` aggregate of status codes; **the `incrementAllContextCounter` logic looks fragile** — it's set false on the first 'ALL' miss and never reset, so subsequent 'ALL' matches don't increment. Document as expected behavior or fix during port. | Pure (flag the logic) |

---

### D2.14 [utils/convertFunctions.js](spark-internal-graphql/packages/data-source-spark/src/utils/convertFunctions.js) — selected

| Export | Purpose | DGS port |
|---|---|---|
| `deepToCamelCase(object)` / `deepToSnakeCase(object)` | Recursive key transforms with `resources.mappings` carve-out | Jackson `@JsonNaming` strategy |
| `doCamelCaseConversion(key, value)` | Returns `false` only for `resources` keys that have `mappings` — keeps the polymorphic resource map intact | Custom serializer |
| **`getStatusName(id)`** | Hardcoded 5-entry table (100=Prototype, 101=Production, 102=Dropped, 103=PreProduction, 104=NotRequested) — **`// must be removed once we have status name in Elastic`** comment present | Move to enum + reference table; **flag for cleanup** |
| **`getTrackingStatusName(id)`** | Hardcoded 5-entry table (107–111) — same comment | Enum |
| **`getEvalStatusName(id)`** | Hardcoded 6-entry table (100,101,102,103,131,132) — same comment | Enum |
| `buildURLParam / buildSampleURLParam / buildSampleQuery / buildCommaSeparatedString / buildFilterQueryParam / buildString / appendAndOperator / additionalParams` | URL construction helpers | Replaced by Feign / Elasticsearch query builder |
| `findRolesById(roleIds, ctx)` | Role lookup | Service call |
| `transformDiscussionMutateV2 / transformDiscussionsMutateV2 / transformUpdateParticipantsV2` | Participant → partnerIds/designPartnerIds derivation | Service method (shared) |
| `transformKeyValues / batchedSingleDeepToCamelCase / singleDeepToCamelCase / singleDeepToSnakeCase / formatQueryResults / toQueryString` | Generic transforms | Replaced by Jackson |

---

### D2.15 [utils/resolvePaging.js](spark-internal-graphql/packages/data-source-spark/src/utils/resolvePaging.js)

| Export | Purpose | DGS port |
|---|---|---|
| `CONNECTIONS_PER_PAGE = 200` | Default page size | Constant |
| `resolvePaging(fields)` | Maps Spring `Page` shape (`totalPages`, `totalElements`, `first`, `numberOfElements`, `size`, `number`, `last`, `sort`) onto GraphQL `Paging` type. Used by every `SPARK_*Paged` wrapper resolver. | Direct mapper — DGS already speaks Spring's `Page<T>` natively, so this becomes a tiny `Page → PagingDto` extension function |
| `NO_RESULTS` | Empty-page constant | Constant |

---

### D2.16 [config/businessPartner.js](spark-internal-graphql/packages/data-source-spark/src/config/businessPartner.js)

Single-class enum-like file. Defines `BusinessPartnerRole` with 8 static instances (DESIGN_PARTNER=5, MERCHANDISE_VENDOR=8, FABRIC_SUPPLIER=7, TRIM_SUPPLIER=10, PACKAGING_SUPPLIER=27, FRAGRANCE_SUPPLIER=311, FOOTWEAR_SUPPLIER=312, YARN_SUPPLIER=313) and 3 lookup methods (`getByCode`, `getByVMMPartnerTypeAndMatrixPlacement`, `getSparkRolesByVMMPartnerType`).

**DGS port:** Kotlin `enum class BusinessPartnerRole(val code: Int, val description: String, val vmmPartnerTypeCode: Int, val vmmMatrixPlacementCodes: List<Int>?)`. Replace static lookups with companion functions.

---

## D3. Cross-Cutting Patterns to Carry Into Phase 3 / Phase 4

| Pattern | Frequency | DGS guidance |
|---|---|---|
| **JWT-curried loaders** (`permissionJWT => loader(...)`) | 3 service methods, 6+ resolver call sites | Hive Gateway forwards capability token via header; DGS verifies once per request and caches |
| **camelCase/snake_case dual reads** (`a.document_id || a.documentId`) | ~30 attachment field accesses | Eliminate at the Feign client boundary with Jackson naming strategy |
| **Mutating `countsByBp` accumulators across closures** | 3 resolvers + 2 utils | Replace with immutable accumulators or a builder |
| **Sequential ACL chunking** (`getAccessControlBatch` and `getProductOrWorkSpaceAttachments`) | 3 hot resolvers | Parallelize chunks in Kotlin (`Flow.flatMapMerge`) |
| **Reflective field-resolver calls from utils** (`Product.SPARK_Product.samples(...)` inside `getNotRemovableWorkspaceIds`, `getProductPartnersNotRemovable`) | 2 utils | Replace with direct service-method calls in DGS; field resolvers should be presentation-only |
| **Hardcoded status-name tables** (`getStatusName`, `getTrackingStatusName`, `getEvalStatusName`) | 3 categories cases + 1 query | Migrate to enums + Elasticsearch-sourced labels (per long-standing TODO in source) |
| **`USE_NEW_RULES_API` env flag** | Conditionally registers 3 service methods + their queries | Delete legacy branch as part of migration if all envs are on the new API |
| **`throwOnError: true` only on `linkProduct`** | 1 method | Port as Kotlin checked exception; document the inconsistency vs other mutations that swallow errors |
| **CommonJS `module.exports` in one file** (`ProductAskUtils.js`) — all others use ES module syntax | 1 file | Cosmetic; DGS rewrite removes the distinction |

---

## D4. Cross-Cutting Findings (Service + Util)

1. **`spark_rules` is a separate Java service** (`${endpoint}/spark_rules/v1`, not `enterprise_product_development_products`). It is **not part of `plm-product`** and likely belongs to its own DGS (`plm-product-rules` or similar). Confirm during Phase 3 federation schema derivation — may require its own DGS or co-location decision.
2. **Rating service** is fully external (different domain, different auth via API key). Stays Hive-stitched (🔵). Migrate as a separate Feign client.
3. **APEX integration** (`getReservedDpcisFromApex`) is a 🔵 platform call — keep stitched.
4. **Sequential ACL chunking is a measurable performance regression source** — three hot resolvers loop `await` on chunks. Should be `Promise.all` in JS today; will be `Flow.flatMapMerge(concurrency=4)` in Kotlin.
5. **`getNotRemovableWorkspaceIds` and `getProductPartnersNotRemovable` call into 4–5 sibling field resolvers** — this triggers entire elasticsearch chains for what is logically a single workspace-id union. Refactor to use underlying services in DGS port.
6. **3 hardcoded status-name tables** in `convertFunctions.js` with "must be removed" comments since at least 2 release cycles. Migration is the right moment to fix these.
7. **`incrementAllContextCounter` logic in `getCountByComponentStatus` looks buggy** (`false` is never reset). Suggest verifying intended behavior; may be the cause of an existing count-mismatch bug.
8. **No retry/circuit-breaker config on ProductService methods** — relies on `utils/circuitBreaker.js` wrapping at a different layer. DGS port should use Spring Cloud Circuit Breaker (Resilience4j).
9. **CommonJS straggler** (`ProductAskUtils.js`) — non-issue for the migration since the whole module is being rewritten in Kotlin.

---

## D5. Complexity Roll-Up (Service + Utils)

| Tier | Items | Days (un-buffered) |
|---|---|---|
| Very High | `attachmentUtils.resolveRelationIds` + `createAttachmentPaged` + `getProductOrWorkSpaceAttachments` (treat as a unit) | 8–13 |
| High | `accessControlUtils.getAccessControlBatch` parallelization, `removePartnerUtils.getProductPartnersNotRemovable`, `commonLoaders` JWT pattern port | 12–20 |
| Medium | `ProductService` REST → service-method port (42 methods, mostly mechanical), `discussionUtils` shared port, `convertFunctions` cleanup, `getProductAsksForWorkspace`, `getNotRemovableWorkspaceIds`, `vmmUtils.loadBps*` chain port | 24–40 |
| Low | `partnerUtils`, `teamUtils`, `productUtils` (3 transforms), `componentStatusUtils`, `resolvePaging`, `BusinessPartnerRole` enum, `addPartnersToCountObject`, ordering helpers, `convertFunctions` URL builders | 8–14 |
| **Total (Services + Utils)** | | **52–87 days** |

Apply +20% buffer per [USAGE.md §7](fedMigrationScripts/USAGE.md): **~62–104 days for Services + Utils.**

---

## Phase 2 Grand Total (Resolvers + Services + Utils)

| Sub-phase | Days (un-buffered) | Days (+20% buffer) |
|---|---|---|
| 2A — Queries | 44–76 | 53–91 |
| 2B — Mutations | 45–79 | 54–95 |
| 2C — Field resolvers | 126–221 | 151–265 |
| 2D — Services + Utils | 52–87 | 62–104 |
| **Total Phase 2** | **267–463 days** | **320–555 days** |

> Roughly **1.3 to 2.3 person-years of engineering** for the product domain alone — consistent with it being the largest single domain in the system.

---

**Phase 2D complete — Services + Utils.** Reply `next` to proceed to **Phase 3** (federation schema derivation: produce `03-schema.graphql` + `03-schema-analysis.md`).
