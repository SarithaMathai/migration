# Phase 2C — Resolver Analysis: Field Resolvers (`product` domain)

> Source: [resolvers/SPARK_Product.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js) lines 1104–2629
> Scope: 16 type-level resolver blocks · ~75 field implementations · 1 polymorphic `__resolveType`.
> Severity legend: 🔴 critical · 🟡 important enrichment · 🔵 platform/optional

---

## Index of Type Blocks

| # | Type | Starting line | Field count | Notes |
|---|---|---|---|---|
| C1 | `SPARK_ResourcesCount` | 1104 | 1 | TechPack count payload |
| C2 | `SPARK_Product` | 1112 | ~50 | The main entity — bulk of work |
| C3 | `SPARK_AncestryProducts` | 2127 | 4 | Pure passthroughs |
| C4 | `SPARK_ProductBulkType` | 2134 | 1 | Wrapper |
| C5 | `SPARK_ProductsPaged` | 2138 | 3 | Wrapper |
| C6 | `SPARK_ProductTemplatesList` | 2144 | 3 | Wrapper |
| C7 | `SPARK_ProductsCategories` | 2150 | 2 | `categories` is a 17-case switch (polymorphic dispatch) |
| C8 | `SPARK_Categories` | 2467 | `__resolveType` | Union — 17 type tags |
| C9 | `SPARK_MasterProductStatus` | 2510 | 2 | Pure transforms |
| C10 | `SPARK_Tcin` | 2514 | 2 | One CORONA platform call |
| C11 | `SPARK_ProductRules` | 2519 | 6 | Mixed IG/VMM + recursive insights mapping |
| C12 | `DopplerDepartment` | 2554 | 5 | Doppler platform |
| C13 | `ProductComponentStatus` | 2599 | 2 | userAttributes lookup |
| C14 | `SPARK_PackagingAttribute` | 2609 | 1 | File library lookup |
| C15 | `VMM_BusinessPartnerCategory` | 2625 | 2 | Extension stub for VMM type |

---

## C1. `SPARK_ResourcesCount`

### `productThumbnailId(parent, args, ctx)` — lines 1105–1110 · **Low**
1. If `!parent.productId` → `return null`.
2. **(Internal)** `product = await ctx.loaders.product.getByID.load(parent.productId)`.
3. Return `product?.thumbnailId ?? null`.

**EXT:** none (self-loader). Returns piggy-backed thumbnail when TechPack payload is consumed by clients that need it for previews.

---

## C2. `SPARK_Product` — the main entity (~50 field resolvers)

### Trivial pass-through resolvers — **Low** (1 day group total to migrate)

| Resolver | Returns |
|---|---|
| `id` | `product.productId` |
| `humanId` | `product.humanId` |
| `createdAt` | `new Date(product.createdDate)` |
| `updatedAt` | `new Date(product.updatedDate)` |
| `versionCreatedAt` | `product.versionCreatedAt && new Date(product.versionCreatedAt)` |
| `resources` | `product.resources` |
| `primaryMaterial` | `product.primaryMaterial` |
| `secondaryMaterial` | `product.secondaryMaterial` |
| `vendorStyleNumber` | `product.vendorStyleNumber` |
| `internalNotes` | `product.internalNotes` |
| `thumbnailId` | `product.thumbnailId` |
| `designPartnerId` | `product.businessPartners.filter(p => p.partnerType === 5).map(bp => bp.partnerId)` |
| `tcins` | `product.businessPartners.filter(bp => bp.tcin && bp.tcin.length > 0)` |
| `parentProductId` | `product.parentProductId` |
| `productTemplateStatus` | `statusName === 'inactive' ? { code: 502 } : { code: 501 }` (template only) |
| `description` | `productTemplate.description` (template only — same field as on regular product) |
| `productBom` | `{ content: product.productBoms || [] }` |
| `packagingBom` | `{ content: product.packagingBoms || [] }` |

### Single-loader user lookups — **Low**

| Resolver | Lines | Loader | Severity |
|---|---|---|---|
| `createdBy` | 1116–1121 | `userAttributes.getUserByIDOrNullIfNotFound(product.createdUser \|\| product.createdBy)` | 🟡 |
| `updatedBy` | 1122–1124 | `userAttributes.getUserByIDOrNullIfNotFound(product.updatedUser)` | 🟡 |
| `versionCreatedBy` | 1127–1129 | `userAttributes.getUserByIDOrNullIfNotFound(product.versionCreatedBy)` | 🟡 |

All three guard on `parent.X &&` before loading — DGS port should preserve the null-short-circuit.

### Single-loader IG / VMM lookups — **Low (🔵 Platform stitch in DGS)**

| Resolver | Lines | Behavior |
|---|---|---|
| `department` | 1310–1314 | If `departmentId && != -1`: `ig.department.getByID(departmentId)`. Else null. |
| `division` | 1315–1319 | **Same call as `department`** — uses `departmentId`, not a separate divisionId. Likely a latent bug but pinned by clients. |
| `clazz` | 1320–1328 | If `classId && departmentId && both != -1`: `ig.clazz.getByClassByDeptId({ department, id: classId })`. Else null. |
| `brand` | 1329–1333 | If `brandId && != -1`: `brand.getBrand(brandId)`. Else null. |

**Migration note:** `division` calls the department loader — preserve exactly to avoid client breakage. Flag for product review post-migration.

### Helper-based / module-import resolvers — **Low/Medium**

| Resolver | Lines | Delegates to |
|---|---|---|
| `status` | 1138 | `getProductStatus(product, args)` from `utils/Product/partnerUtils.js` |
| `notRemovablePartnerIds` | 1187–1188 | `getProductPartnersNotRemovable(ctx, product, info, args)` from `utils/removePartnerUtils.js` (uses `info` — must be plumbed in DGS) |
| `notRemovableWorkspaceIds` | 1929–1930 | `getNotRemovableWorkspaceIds(product, args, ctx)` from `utils/Product/productUtils.js` |
| `reservedDpcis` | 1933 | `getReservedDpcisFromApex(product, ctx)` — APEX platform 🔵 |
| `tags` | 1481 | `getTagsBatched(ctx, product.tags)` — `services/batchers/getTagsBatched.js` 🟡 |
| `unDroppablePartners(isDesignPartner)` | 1130–1137 | If `args.isDesignPartner`: `getUnDroppablePartners(ctx, product.productId)`. Else `[]`. |

### `vendorAttributes(workspaceIdFilter)` — lines 1139–1172 · **Medium**
1. Pull `businessPartners` from product.
2. `merchPartners = businessPartners.filter(filterOutDesignPartners)`.
3. `allStatuses = getFinalPartnerStatuses(product, args)` (pure).
4. **(EXT 🔵 VMM)** `allVmmData = await loadBpsWithType(merchPartners, ctx)` (batches VMM).
5. For each merch partner: find matching `statusData` and `vmm` (by `bpId === partnerId`).
6. Compose `{ partnerId, partnerType, name: vmm?.bpName || partnerName || '', status, statusCount, allStatuses }`.

**Note:** Int-parse normalization to avoid string/number id mismatch.

### `businessPartners(workspaceIdFilter)` — lines 1173–1184 · **Medium**
1. If `args.workspaceIdFilter`:
   - **(EXT 🔴 workspaceV2)** `workspace = workspaceV2.getWorkspaceByIdV2(workspaceIdFilter)`.
   - Filter `businessPartners` to those present in `workspace.businessPartners`.
2. **(EXT 🔵 VMM)** Return `loadBpsWithType(filtered_or_all, ctx)`.

### `droppedPartners` — lines 1185–1186 · **Low**
1. **(EXT 🔵 VMM)** `loadBpsWithType(droppedPartners, ctx)`.

### `elasticSamplesList(query, page, size)` — lines 1189–1218 · **High**
1. **(EXT 🔴 search)** `samplesPaged = search.searchSamplesByParentId({ parentIds: productId, query: args.query ?? '*', page: args.page ?? 0, size: args.size ?? 20 })`.
2. `elasticSamples = samplesPaged.content || []`. If empty → return `samplesPaged` as-is.
3. `sampleIds = elasticSamples.map(s => s.id)`.
4. **(Sibling resolver)** `samples = await SPARK_SampleV2.Query.getSamplesByIdsV2({}, { ids, recentlyViewed: false }, ctx)` (→ EXT 🟡 `sampleV2`).
5. Return `{ ...samplesPaged, content: samples.map(s => ({ ...elasticSample[s.id], ...s })) }` — sample-API fields override elastic where overlapping.

**Comment from source:** "rfidTagId not on sample in elastic so double network call."

### `samples(parent, args, ctx, info)` — lines 1219–1257 · **High**
Reads `info.variableValues` (top-level query vars) to branch:

1. If top-level var `id` starts with `'WRK'` **OR** both `q` and `filter` present:
   - **(Internal)** `sampleIds = ctx.loaders.product.getFilteredSamples({ resourceType:'workspaces', resourceId: info.variableValues.id, filter, q, productId })` — elastic search wrapper.
   - If non-empty: **(Sibling/EXT 🟡)** `SPARK_SampleV2.Query.getSamplesByIdsV2`.
2. Else:
   - **(EXT 🟡 relationship)** `relationship.getByID({ id: productId, type:'sample', maxDepth: 0 })`. Catch errors → `[]` (silent 404).
   - If `nodes.length > 0`: `sampleIds = nodes.map(n => n.id)` → call `getSamplesByIdsV2`.
3. Else `[]`.

**Risk:** Depends on `info.variableValues` — fragile coupling to query-document variable names. Reproduce in DGS via `DgsDataFetchingEnvironment.getArguments()` or explicit `@DgsContext` propagation.

### `sampleIds(parent, args, ctx, info)` — lines 1258–1270 · **Low**
1. If `product.sampleIds` already present → return it.
2. Else **(Internal)** `product.getFilteredSamples({ resourceType:'products', resourceId:[productId], filter: info.vars.filter, q: info.vars.q, productId })`.

### `associateProductsAsks(workspaceIdFilter)` — lines 1271–1289 · **Medium**
1. If `!product.productId` → `[]`.
2. If `args.workspaceIdFilter`:
   - **(Internal co-located)** `getProductAsksForWorkspace(ctx, { workspaceId, productIds:[productId], page:0, size:50 })`.
   - Return `results?.content || []`.
3. Else:
   - **(EXT 🔴 accessControl)** `permissionJWT = getUserPermissionsJWT(productId, ctx)`.
   - **(Internal co-located)** `productAsk.getAssociateProductAsks(permissionJWT, productId)`.

### `variations(partnerId, workspaceId)` — lines 1290–1302 · **Medium**
1. If `!product.productId` → `[]`.
2. **(EXT 🔴 accessControl)** Get JWT.
3. **(Internal co-located)** `productVariation.getProductVariations(jwt, productId, 'ACTIVE', args.partnerId, args.workspaceId).load()`.

### `productWorkspaceAttributes(elasticVerify)` — lines 1339–1387 · **Medium**
Defines local `mapAttribute(attributes)` that returns a shape with `designCycle` as a deferred async resolver (`async () => { tag.getTag(...).catch(()=>null) }` 🟡).

1. If `args.elasticVerify`:
   - **(EXT 🔴 search)** `workspaces = search.getWorkspacesPagedV3({ size:10000, page:0, q:'resources.mappings.product:{productId}' }).content`.
   - Return `product.productWorkspaceAttributes.filter(!archived).filter(humanId in workspaces).map(mapAttribute)`.
2. Else: same filter chain without the elastic verification.

**Note:** Returning async functions as field values (`designCycle: async () => …`) is GraphQL-legal — DGS will need a nested `@DgsData` on the wrapper type.

### `productWorkspaceInfo` — lines 1388–1428 · **Medium**
Near-identical to above but **always** performs the elastic verification (no `elasticVerify` arg). Wrapper includes `businessPartners` field. Returns shape with deferred `designCycle`.

### `teams(partnerId, workspaceId)` — lines 1429–1473 · **Medium**
1. `ids = product.resources?.mappings?.team || []`. If empty → `{ content: [] }`.
2. **(EXT 🔴 accessControl)** `jwt = getUserPermissionsJWT(ids, ctx)`.
3. **(EXT 🟡 teamV2)** `teams = teamV2.getByIDs(jwt).load({ ids })`.
4. Sort case-insensitively by `teamName`. (Comment: "elastic will sort for us soon".)
5. `content = filterTeamsByPartnerOrWorkspaceId(teams, product, args)` (pure util).
6. Return `{ content, paging: { totalElements: content.length } }`.

### `discussionsV2(partnerId)` — lines 1466–1473 · **Low**
Note: `args.partnerId` is declared in schema but **unused** in the resolver.
1. **(EXT 🔴 search)** `search.searchDiscussionsElastic({ q: '(relatedResources:{productId} AND _index:discussion)' })`.
2. Return raw response.

### `discussionsCount` — lines 1474–1480 · **Low**
1. **(EXT 🟡 discussion)** `discussion.getDiscussionsCount({ resourceId: productId, resourceType:'product' })`.
2. Return `_.get(response, 'discussionsCount[0].discussionCount', 0)`.

### `workspaces` — lines 1482–1487 · **Low**
1. **(EXT 🔴 search)** `search.getWorkspacesPagedV3({ size:10000, page:0, q: 'resources.mappings.product:{productId}' })`.

### `attachments` — lines 1488–1506 · **Medium**
1. **(EXT 🟡 relationship)** `attachmentsIds = relationship.searchByIds({ id: productId, includeNodeTypes:['attachments','attachments_v3'], maxDepth: 0 })`.
2. If non-empty:
   - **(EXT 🔴 accessControl)** `aclJWT = accessControl.getUserAccessByPost(nodeIds)`.
   - **(EXT 🔴 attachment)** `attachment.getAttachmentsByPost(aclJWT).load(nodeIds)`.
3. Return `attachments` (or `[]`).

### `attachmentsWithMetaData(partnerId, type, tags, onlyProductPacketFiles)` — lines 1507–1656 · **Very High (X-Large)**
The single largest field resolver. ~150 lines.

1. **(EXT 🟡 relationship)** `relations = relationship.searchByIds({ id: productId, includeBranches:['product','sample','discussions','discussionThreads','bill_of_materials','packaging_bom','claim','measurement_set','construction_set','product_watchlist'], includeNodeTypes:['attachments','sample','discussions','discussionThreads','attachments_v3'] })`.
2. If no nodes → `[]`.
3. Partition `nodes` by `type` into 5 lists: `attachmentV2Ids`, `attachmentV3Ids`, `discussionIds`, `discussionThreadIds`, `sampleIds`.
4. If both attachment lists empty → `[]`.
5. `attachmentIds = v2 ∪ v3`.
6. **(EXT 🔴 accessControl ×2)** `attachmentsJWT = getUserAccessByPost(attachmentIds)`; `samplesJWT = getUserAccessByPost(sampleIds)` (each guarded for empty → `''`).
7. **(EXT 🔴 attachment)** `attachments = attachment.getAttachmentsV3(attachmentsJWT).load(attachmentIds)`. If empty → `[]`.
8. **(EXT 🔴 accessControl)** `currentUserPermissions = accessControl.getUserAccessUnencoded(attachmentIds).resourcePermissions`.
9. Conditional batch fetches:
   - If `discussionIds.length`: **(EXT 🟡 discussion via util)** `getDiscussionsBatch(discussionIds, CHUNK_SIZE, ctx)`.
   - If `discussionThreadIds.length`: `getDiscussionThreadsBatch(...)`.
   - If `sampleIds.length`: **(EXT 🟡 sampleV2)** `sampleV2.getSamplesByIdsV2(samplesJWT).load(sampleIds)`.
10. For each attachment, find `relatedDiscussion`, `relatedDiscussionThread`, `relatedSample` by id. Build `relatedResource`:
    - Thread → use parent discussion's `linkedResourceId` (sample mapping if `sampleDiscussion`, else `discussionId`), subject, critical/draft flags.
    - Discussion → same shape from itself.
    - Sample → `{ linkedResourceId: id, isResourceCritical, resourceTitle: description }`.
11. Compose `{ attachment, ...relatedResource, currentUserPermissions: find(currentUserPermissions, { resourceId: attachment.document_id }) }`.
12. Filter out: `attachment.resource.type === 'discussion' && (!linkedResourceId || isResourceDraft)` — comment: "TODO: ACL should be doing this".
13. **Sort** via `orderProductAttachments(...)` (defined at top of file lines 60–69): orders by resource type rank (`product`, `discussion`, `sample`) ascending, then by `created_at` descending.

### `attachmentSummary` — lines 1657–1685 · **Medium**
1. **(EXT 🔴 search)** `search.searchAttachmentsByRelatedResource(productId)`.
2. `primaryAttachment = find(attachments, { id: thumbnailId }) || find(attachments, { documentId: thumbnailId })`.
3. Return `{ isThumbnailPreviewable: primary?.previewable ?? false, totalAttachmentCount: attachments.length }`.

### `attachmentsV3(partnerId, type, tags, onlyProductPacketFiles)` — lines ~1670–1685 · **High**
1. `countsByBp = _.cloneDeep(initialCountsByBp)` (from `attachmentUtils`).
2. For each `product.businessPartners`: push `{ bpType: partnerId, counts: 0 }` onto `countsByBp` (**mutation; cloneDeep prevents cross-request bleed**).
3. **(EXT 🔴 multiple)** `attachments = await getProductOrWorkSpaceAttachments((productId || humanId), countsByBp, args, ctx, onlyProductPacketFiles, thumbnailId)` — see `utils/Product/attachmentUtils.js` (Phase 2D).
4. Return `{ content: attachments, counts: countsByBp }`.

### `components(workspaceId, partnerId, type, tags, archived, types)` — lines 1686–1879 · **Very High (X-Large)**
~190 lines. The other heavyweight field resolver.

1. Init `boms = product.boms || []`, `measurements = product.measurementSets || []`, `claims = product.claims || []`, `productDetails = product.productDetails || []`, `packagingDetail = []`.
2. If none of those 4 are pre-hydrated on `product`:
   - **(Sibling/EXT 🔴 search ×4 in parallel)** `Promise.all([...])`:
     - `SPARK_Measurement.Query.getMeasurementsElastic(product, { resourceId: productId }, ctx)`
     - `SPARK_Claims.Query.getClaimsElastic(product, { parentHumanId: productId }, ctx)`
     - `SPARK_Bom.Query.getBomElastic(product, { q: 'parentId:{productId}' }, ctx)`
     - `SPARK_ProductDetail.Query.getProductDetailsElastic(product, { resourceId, types: args?.types || [100] }, ctx)`
   - Re-assign each variable from its `.content` (or raw for `bomElastic`).
3. **(Sibling EXT 🔴 search)** `packagingElastic = SPARK_Packaging.Query.getPackagingElastic(product, { parentHumanId: productId }, ctx)`. If present, map → `name = (promoDescription ? '{p} ' : '') + description`.
4. If claims non-empty, **(EXT 🔴 accessControl per-claim, sequential loop)** for each claim: `getUserAccessUnencoded(claim.id || claim.humanId)` → attach `currentUserClaimPermissions`. **Performance hot-spot — N+1 ACL calls** (worth flagging in Phase 4).
5. Build `countsByBp = cloneDeep(initialCountsByBp)`; push partner entries (same as `attachmentsV3`).
6. `allHumanIds = union of all 5 component arrays' ids`.
7. If empty → return `{ content:[], counts: countsByBp, archivedCount: 0 }`.
8. **(EXT 🔴 accessControl batched)** `permissions = getAccessControlBatch(allHumanIds, 100, ctx)` — chunked at 100.
9. Define `mapComponent(component)`:
   - Determine partners list:
     - If `componentId` starts with `'PKG-'`: `partners = [parseInt(component.businessPartner?.partnerId)]`.
     - Else: find `access = permissions[resourceId]`; **throw** `Error('no permissions object found for resourceId: ...')` if missing. Iterate `access.permissions[*].abstractAccessGroup.grantees` — if locked, set `isLocked`; union grantees into `partners`.
   - `addPartnersToCountObject(partners, countsByBp)` (mutates `countsByBp`).
   - Return component shape with normalized `{ id, name, type, createdBy, updatedBy, createdAt, updatedAt, parentResource, additionalDescription, relatedResources:[], workspaceContext, access: convertV2AccessToV3(partners, isLocked), archived, libraryLinked, materials, status (synth if missing), statuses, rows, currentUserClaimPermissions? }`.
10. Compose `components = [...measurements:type='measurement', ...claims:type='claim', ...boms:type=(bom.type===2?'packagingBom':'bom'), ...productDetails:type='productDetail', ...packagingDetail:type='packaging'].map(mapComponent)`.
11. `archivedCount = filterAttachmentsOrComponents(components, { ...args, archived: true }).length`.
12. `filteredComponents = filterAttachmentsOrComponents(components, args)`.
13. Return `{ content: orderComponentsByDate(filteredComponents), counts: countsByBp, archivedCount, countByComponents: getCountByComponents(filteredComponents) }`.

### `measurementSets(businessPartnerIds, calculated, mustHaveRows, includeMeasurements)` — lines 1880–1904 · **Medium**
1. Build `queryParams = { businessPartnerIds, calculated, mustHaveRows, resourceId: productId }`.
2. **(Sibling)** `measurementSets = SPARK_Measurement.Query.getMeasurements(product, queryParams, ctx)` (not awaited — Promise returned).
3. If `mustHaveRows`: filter to sets with non-empty `rows`.
4. If `includeMeasurements`: return `{ content: product.measurementSets || [] }` (skip the API call result entirely).
5. Else return the Promise.

**Note:** Boolean branching combined with un-awaited Promise leak is fragile. Step 3 awaits implicitly; step 4 ignores step 2 entirely. Pin in parity tests.

### `claims(partnerIds, includeClaims)` — lines 1905–1913 · **Low**
1. If `args.includeClaims`: return `product.claims` (pre-hydrated).
2. Else **(Sibling)** `SPARK_Claims.Query.getClaims(product, { parentHumanId: productId, partnerIds }, ctx)`.

### `bom(includeBoms)` — lines 1914–1922 · **Low**
1. If `args.includeBoms`: `{ content: product.boms || [] }`.
2. Else **(Sibling)** `SPARK_Bom.Query.getBomByParentId(product, { parentId: productId }, ctx)`.

### `ancestryProducts` — lines 1935–1996 · **Medium**
1. `ids=[]; ancestryProductsResult=[]; parentProduct=null`.
2. If `parentProductId`:
   - **(Internal)** `parentProduct = product.getByID(parentProductId)`.
   - Augment `{ ...parent, type: 'parent' }` (strip `childProducts`); push to result.
   - For each `parentProduct.childProducts` where `id !== productId`: push id onto `ids`.
3. Else if `product.childProducts` non-empty: push each child id onto `ids`.
4. If `ids.length > 0`:
   - **(Internal)** `response = product.getByIdList(ids)`.
   - For each fetched product, find matching `childProductSnippet` in either `parentProduct.childProducts` or `product.childProducts` to get `removable`; push as `{ ...product, removable, type: 'otherChild' | 'child' }`.
5. Return `ancestryProductsResult`.

### `rating` — lines 1997–2019 · **Medium (🔵 external rating service, looped)**
1. If `parentTcins` non-empty: for each tcin, **(External Rating)** `product.getRatingByTcin(tcin)` → JSON.parse; first successful one breaks loop.
2. If statistics found: `{ averageRating: rating.average ?? 0.0, reviewCount: reviewCount ?? 0 }`.
3. Else implicit `undefined` (→ `null` to client).

**Risk:** Serial loop over parentTcins — could be slow if many; consider parallel with `Promise.any` in DGS.

### `productTemplateDepartments` (template only) — lines 2020–2034 · **Low**
1. If `departmentIds?.length > 0`: **(EXT 🔵 IG)** parallel `ig.department.getByID(id)` for each; filter falsy.
2. Else `[]`.

### `brands` (template only) — lines 2036–2050 · **Low**
1. If `brandIds?.length > 0`: **(EXT 🔵 VMM)** parallel `brand.getBrand(id)`; filter falsy.

### `divisions` (template only) — lines 2051–2067 · **Low**
1. If `divisionIds?.length > 0`: **(EXT 🔵 IG)** parallel `ig.division.getByID(id)`; filter falsy.

### `attachmentsData` (template only) — lines 2071–2126 · **High**
> TODO comment: "SPARK-26829 relationship for attachments will be cleaned up"
1. **(EXT 🟡 relationship)** `relations = relationship.searchByIds({ id: productTemplate.humanId, includeNodeTypes:['attachments','attachments_v3'], maxDepth: 0 })`.
2. Partition nodes:
   - `attachments` type and id **does NOT** contain `'ATC-'` → v2 list.
   - Else → v3 list. (Heuristic: v3 ids contain `ATC-`.)
3. If v2 non-empty: **(Sibling EXT 🔴 attachment)** `SPARK_Attachment.Query.getAttachmentsV3(_, { ids: v2Ids }, ctx)`.
4. If v3 non-empty: same call.
5. `finalAttachmentInfo = [...v3, ...v2]`.
6. Return `{ attachmentIds: finalAttachmentInfo.map(a => a.human_id || a.document_id), attachments: finalAttachmentInfo }`.

---

## C3. `SPARK_AncestryProducts` — lines 2127–2133 · **Low**
Four trivial passthroughs: `id` (`response.productId`), `removable`, `description`, `thumbnailId`. No logic.

---

## C4. `SPARK_ProductBulkType` — line 2135 · **Low**
`products: response => response.products`. Wrapper.

---

## C5. `SPARK_ProductsPaged` — lines 2138–2142 · **Low**
`paging: resolvePaging`, `content`, `pageable` — all wrappers.

---

## C6. `SPARK_ProductTemplatesList` — lines 2144–2148 · **Low**
Identical to C5.

---

## C7. `SPARK_ProductsCategories.categories(type)` — lines 2151–2466 · **Very High (X-Large, +1 polymorphic bump)**

A single ~315-line `switch(args.type)` over **17 cases**. Each case loads a category list of a different type and tags it with `type` for `__resolveType` (C8). Behavior summary:

| `args.type` | Source field | Loader | EXT |
|---|---|---|---|
| `brands` | `productCategories.brands` (filter `>0`) | `loadManyIncludeEmptyResponse(brand.getBrand, ids, ctx.logContext)` | 🔵 VMM |
| `brandIds` | `productCategories.brandIds` (filter `>0`) | same; rewrites `type` to `'brands'` for `__resolveType` | 🔵 VMM |
| `departments` | `productCategories.departments` (filter `>0`) | `loadManyIncludeEmptyResponse(ig.department.getByID, ids)` | 🔵 IG |
| `departmentIds` | `productCategories.departmentIds` (filter `>0`) | same; rewrites `type` to `'departments'` | 🔵 IG |
| `divisions` | `productCategories.divisions` | `loadManyIncludeEmptyResponse(ig.division.getByID, ids)` | 🔵 IG |
| `divisionIds` | `productCategories.divisionIds` | same; rewrites `type` to `'divisions'` | 🔵 IG |
| `clazz` | walks `productCategories.departments[*].classId[*]` | `ig.clazz.getByClassByDeptId({ department, id })` flatten + tag | 🔵 IG |
| `businessPartners` | `productCategories.businessPartners` | `loadBps(ctx, ids)` (vmmUtils) | 🔵 VMM |
| `setDates` | `productCategories.setDates` | local: format each via `moment(date).format('YYYY-MM-DD')` → `{ id, name, type }` | none |
| `productStatus` | `productCategories.productStatus` | local: `getStatusName(id)` (convertFunctions) | none |
| `trackingStatus` | `productCategories.trackingStatus` | `getTrackingStatusName(id)` | none |
| `evaluationStatus` | `productCategories.evaluationStatus` | `getEvalStatusName(id)` | none |
| `tags` | `productCategories.tags` | `tag.getTags({ page:0, size:10000, ids })` | 🟡 tag |
| `sampleType` | `productCategories.sampleType` | `SPARK_SampleV2.Query.getSampleProductTypesV2()` then match by `code` | 🟡 sampleV2 sibling |
| `sampleFormat` | `productCategories.sampleFormat` | `SPARK_SampleV2.Query.getSampleFormats()` then match | 🟡 sampleV2 sibling |
| `packagingFormat` | `productCategories.packagingFormat` | `packaging.getPackagingFieldValuesByType('PACKAGING_COMPONENTS', ids)` | Internal co-located |
| `packagingGroup` | `productCategories.packagingGroup` | `packaging.getPackagingFieldValuesByType('PACKAGING_GROUP', ids)` | Internal co-located |
| `packagingWave` | `productCategories.packagingWave` | `tag.getTags({ page:0, size:1000, ids })` | 🟡 tag |
| `fulfillmentType` | `productCategories.fulfillmentType` | `packaging.getPackagingFieldValuesByType('fulfillment_type', ids)` | Internal co-located |
| `designCycle` | `productCategories.designCycle` | `tag.getTags({ page:0, size:10000, ids })` | 🟡 tag |

Default: no return → `undefined`.

Each case tags `result.type = args.type` (some override to a different tag, see C8 mapping).

**Migration approach:** Build one `@DgsData` per category branch, or a single dispatcher that calls per-type Kotlin services. Keep the dispatch logic in one place but split implementations for testability.

---

## C8. `SPARK_Categories.__resolveType(category)` — lines 2467–2509 · **High (+1 polymorphic complexity tier)**

```
switch (category.type) {
  'brands' | 'brandIds'             → 'VMM_Brand'
  'departments' | 'departmentIds'   → 'IG_Department'
  'divisions' | 'divisionIds'       → 'IG_Division'
  'clazz'                            → 'IG_Clazz_Filter'
  'productStatus'                    → 'SPARK_ProductStatus'
  'businessPartners'                 → 'VMM_BusinessPartnerCategory'
  'tags'                             → 'SPARK_Tag_Elastic'
  'setDates'                         → 'SPARK_Filter_SetDates'
  'trackingStatus' | 'evaluationStatus' → 'SPARK_Status'
  'sampleType'                       → 'SPARK_FilterSampleType'
  'sampleFormat'                     → 'SPARK_FilterSampleFormat'
  'designCycle' | 'packagingWave'    → 'SPARK_Tag_Elastic'
  'packagingFormat' | 'packagingGroup' | 'fulfillmentType' → 'SPARK_Packaging_Field'
  default                            → 'IG_Clazz_Filter'
}
```

**Migration:** In DGS, use `@DgsTypeResolver(name = "SPARK_Categories")` mapping `category.type` → concrete type. Keep the default branch — clients may rely on it.

---

## C9. `SPARK_MasterProductStatus` — lines 2510–2513 · **Low**
- `id: status.statusCode`
- `name: status.description`

---

## C10. `SPARK_Tcin` — lines 2514–2518 · **Low**
- `createdAt: parent.createdAt && new Date(parent.createdAt)`
- `itemDetails: ctx.loaders.coronaItems.getItemDetails(parent.tcinId)` — **🔵 CORONA platform**.

---

## C11. `SPARK_ProductRules` — lines 2519–2553 · **Medium**

| Field | Behavior |
|---|---|
| `id` | `parent.ruleId` |
| `active` | `parent.active` |
| `departments` | If `criteria.departmentIds`: parallel `ig.department.getByID(id)` 🔵 IG. Else `[]`. |
| `businessPartners` | If `criteria.businessPartnerIds`: `loadBps(ctx, ids)` 🔵 VMM. Else `[]`. |
| `rules` | `parent.rules` (passthrough) |
| `insightsClassExclusion` | `parent.insightsClassExclusion?.departmentClass.map(pair => pair.classIds.map(id => ({ d:pair.departmentId, c:id }))).flat().map(p => ig.clazz.getByClassByDeptId({ department:p.d, id:p.c }))` 🔵 IG. Else `null`. |

---

## C12. `DopplerDepartment` — lines 2554–2598 · **Medium (Doppler platform)**

| Field | Behavior |
|---|---|
| `department` | If `id && != -1`: `ig.department.getByID(parent.id)` 🔵 IG. Else `null`. **Uses department id (not divisionId)**. |
| `division` | **Same call as `department`** (lines 2559–2562). Identical latent issue as `SPARK_Product.division`. |
| `clazzes` | If `id != -1` and `classIds` non-empty: filter `classId !== -1 \|\| === 0`, then per-id `ig.clazz.getByClassByDeptId({ department: parent.id, id: clazzId })` 🔵 IG. |
| `primaryCapacityTypeName` | If `primaryCapacityTypeId`: `doppler.getCapacityTypesByDepartmentAndPrimaryId({ id, primaryCapacityId })` 🔵 Doppler; return `[0].capacityTypePrimaryName \|\| ''`. |
| `secondaryCapacityTypeName` | Same Doppler call; find element whose `capacityTypeSecondaryId === parent.secondaryCapacityTypeId` and return its `capacityTypeSecondaryName`. **N.B.:** `primary` and `secondary` resolvers both make the same call — DataLoader memoizes within a request, but the duplicate fetch is worth removing in DGS. |

---

## C13. `ProductComponentStatus` — lines 2599–2608 · **Low**
- `updatedAt: new Date(status.updatedAt)`
- `updatedBy: status.updatedBy && userAttributes.getUserByIDOrNullIfNotFound(status.updatedBy)` 🟡

---

## C14. `SPARK_PackagingAttribute.spg` — lines 2609–2624 · **Low**
1. `spgId = parent.spgLibraryId`.
2. If present: try `fileLibrary.getPackageLibrary(spgId)` (Internal co-located). On error: log + return `null`.
3. Else `null`.

---

## C15. `VMM_BusinessPartnerCategory` — lines 2625–2628 · **Low**
- `id: businessPartner.bpId`
- `name: businessPartner.bpName`
Extension type stub for VMM_BusinessPartner — preserves the gateway-stitched VMM type.

---

## EXT Service Call Summary (Field Resolvers only)

| Loader | Severity | Touched From | Notes |
|---|---|---|---|
| `accessControl` (JWT + ACL by post + unencoded + batch) | 🔴 RED | `attachments`, `attachmentsWithMetaData` ×2, `components` (N+1 per claim + batch of 100), `teams`, `associateProductsAsks`, `variations` | The hottest path |
| `search.*` | 🔴 RED | `elasticSamplesList`, `workspaces`, `discussionsV2`, `attachmentSummary`, `productWorkspaceAttributes` (verify), `productWorkspaceInfo`, `components` (×5 sibling elastic queries) | |
| `attachment.getAttachmentsByPost / getAttachmentsV3` | 🔴 RED | `attachments`, `attachmentsWithMetaData`, `attachmentsV3`, `attachmentsData` | JWT-curried |
| `workspaceV2.getWorkspaceByIdV2` | 🔴 RED | `businessPartners(workspaceIdFilter)` | |
| `relationship.searchByIds / getByID` | 🟡 YELLOW | `samples`, `attachments`, `attachmentsWithMetaData`, `attachmentsData` | |
| `userAttributes.getUserByIDOrNullIfNotFound` | 🟡 YELLOW | `createdBy`, `updatedBy`, `versionCreatedBy`, `ProductComponentStatus.updatedBy` | |
| `teamV2.getByIDs` | 🟡 YELLOW | `teams` | JWT-curried |
| `discussion.getDiscussionsCount` + `getDiscussions/Threads/Batch` (via util) | 🟡 YELLOW | `discussionsCount`, `attachmentsWithMetaData` | |
| `sampleV2.getSamplesByIdsV2` | 🟡 YELLOW | `samples`, `elasticSamplesList`, `attachmentsWithMetaData` | JWT-curried |
| `tag.getTag / getTags` | 🟡 YELLOW | `tags`, `productWorkspaceAttributes/Info` (designCycle), categories switch (tags/designCycle/packagingWave) | |
| `ig.department / division / clazz` | 🔵 PLATFORM | `department`, `division`, `clazz`, `DopplerDepartment.*`, `ProductRules`, categories | |
| `brand.getBrand` (VMM) | 🔵 PLATFORM | `brand`, `brands`, categories | |
| `loadBps / loadBpsWithType` (VMM batch) | 🔵 PLATFORM | `businessPartners`, `droppedPartners`, `vendorAttributes`, `ProductRules.businessPartners` | |
| `coronaItems.getItemDetails` | 🔵 PLATFORM | `SPARK_Tcin.itemDetails` | |
| `doppler.getCapacityTypesByDepartmentAndPrimaryId` | 🔵 PLATFORM | `DopplerDepartment.primary/secondaryCapacityTypeName` | |
| `getReservedDpcisFromApex` | 🔵 PLATFORM | `reservedDpcis` | APEX |
| `productAsk`, `productVariation`, `fileLibrary`, `packaging` | Internal (co-located) | `associateProductsAsks`, `variations`, `SPARK_PackagingAttribute.spg`, categories packaging branches | All become same-service in `plm-product` |
| `bom`, `measurement`, `ProductDetails`, `claim`, `packaging` (via sibling Query resolvers) | Internal + 🟡 claim | `components` parallel elastic | |
| External Rating service | 🔵 PLATFORM | `rating` | API-key auth |

---

## Complexity Roll-Up (Field Resolvers only)

| Tier | Resolvers | Count | Days (un-buffered) |
|---|---|---|---|
| Very High | `attachmentsWithMetaData`, `components`, `SPARK_ProductsCategories.categories` (+1 polymorphic via C8) | 3 | 24–39 |
| High | `elasticSamplesList`, `samples`, `attachmentsV3`, `attachmentsData` | 4 | 20–32 |
| Medium | `vendorAttributes`, `businessPartners`, `productWorkspaceAttributes`, `productWorkspaceInfo`, `teams`, `attachments`, `attachmentSummary`, `measurementSets`, `ancestryProducts`, `rating`, `associateProductsAsks`, `variations`, `SPARK_ProductRules.*`, `DopplerDepartment.*` (treat as block) | 14 | 42–70 |
| Low | All trivial passthroughs, single-loader IG/VMM/user lookups, `claims`, `bom`, `productBom`, `packagingBom`, `discussionsCount`, `discussionsV2`, `workspaces`, `tags`, `notRemovablePartnerIds`, `notRemovableWorkspaceIds`, `reservedDpcis`, `unDroppablePartners`, `sampleIds`, `productTemplateDepartments`, `brands`, `divisions`, `productTemplateStatus`, C3–C6 wrappers, C9, C10, C13, C14, C15 | ~40 | 40–80 |
| **Total (Field Resolvers)** | | **~61 individual fields** | **126–221 days** |

Apply +20% buffer (per [USAGE.md §7](fedMigrationScripts/USAGE.md)): **~151–265 days for Field Resolver work alone.**

> This is the largest single phase of the migration. Most of the cost lives in 3 resolvers (`attachmentsWithMetaData`, `components`, `categories`) plus the ~20 medium ones.

---

## Cross-Cutting Findings (Field Resolvers)

1. **`SPARK_Product.division` calls the department loader, not division.** Same bug in `DopplerDepartment.division`. Pinned by clients today — preserve behavior, document, then fix in a separate ticket post-migration.
2. **N+1 ACL calls in `components`** (per-claim `getUserAccessUnencoded` loop). Refactor to a batched call in the DGS port — both faster and simpler.
3. **`SPARK_ProductsCategories.categories` is effectively a 17-resolver-in-one.** Either split into 17 `@DgsData` methods on the wrapper type or keep as a single dispatcher with helper methods. Splitting gives better DataLoader reuse and easier per-branch testing.
4. **Polymorphic `__resolveType`** (C8) maps `category.type` strings to 11+ concrete types. +1 complexity tier per [USAGE.md §7](fedMigrationScripts/USAGE.md) is already applied to C7.
5. **`samples` reads `info.variableValues`** — relies on the calling query's top-level variable names. Reproduce explicitly in DGS via `DataFetchingEnvironment.getArguments()` on a parent context, **not** by introspecting variable names. Document the contract.
6. **Deferred `designCycle` in `productWorkspaceAttributes/Info`** returns a Promise-producing function as the field value. DGS handles this via nested `@DgsData` resolvers on the wrapper type — straightforward port.
7. **TODO comments left in code:**
   - `attachmentsData` — "SPARK-26829 relationship for attachments will be cleaned up".
   - `attachmentsWithMetaData` discussion-draft filter — "TODO: ACL should be doing this".
   - Capture both as separate clean-up tickets after the migration completes.
8. **External Rating service** is hit twice from this file (`rating` field + `getRatingByTcin` query). Single DGS Feign client should back both.
9. **DataLoader memoization saves duplicate calls** in `DopplerDepartment` (primary/secondary capacity types) — DGS port must keep request-scoped caching to preserve performance parity.

---

**Phase 2C complete — Field Resolvers.** Reply `next` to proceed to Phase 2D (Service class methods + util functions; final piece of Phase 2 before Phase 3 schema derivation).
