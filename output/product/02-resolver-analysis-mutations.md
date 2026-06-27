# Phase 2B — Resolver Analysis: Mutations (`product` domain)

> Source:    [resolvers/SPARK_Product.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/SPARK_Product.js) lines 538–1102
> Service:   [services/Product.js](spark-internal-graphql/packages/data-source-spark/src/services/Product.js)
> Scope:     All 23 schema-declared Mutation operations.
> Severity legend: 🔴 critical · 🟡 important enrichment · 🔵 platform/optional

---

## ⚠️ Schema-vs-Resolver Drift (must address before Phase 4)

The schema declares **3 mutations** as top-level fields that have **no dedicated resolver function** in `SPARK_Product.js`:

| Schema-declared mutation | Implementation location | Notes |
|---|---|---|
| `removeProductBusinessPartner(productId, partnerId)` | `productBusinessPartnerActions` switch — `REMOVE_PARTNER` case | Top-level call would throw "field not implemented" |
| `dropProductBusinessPartner(productId, partnerId)` | `productBusinessPartnerActions` switch — `DROP_UNDROP_PARTNER` (`dropped=true`) | Same |
| `unDropProductBusinessPartner(productId, partnerId)` | `productBusinessPartnerActions` switch — `DROP_UNDROP_PARTNER` (`dropped=false`) | Same |

**Migration decision needed:** In DGS, either (a) **add** the missing top-level data fetchers as thin wrappers around the orchestration, or (b) **remove** the un-implemented fields from `.graphqls` (breaking change). Recommend (a) for client parity.

The numbered sections below describe the **22 actually-implemented** resolvers (counting `productBusinessPartnerActions` once).

---

## M1. `addProducts(workspaceId: ID!, products: [SPARK_ProductInput])` → `SPARK_ProductBulkType`
**Resolver:** lines 539–637. **Complexity:** **High (Large, 5–8 days)** — multi-service orchestration.

### Pseudo-logic
1. **(EXT 🔴 accessControl)** `workspaceResourcePermissionJWT = await getUserPermissionsJWT(getWorkspaceResourceString(workspaceId), ctx)`.
2. **(Internal)** `productList = await ctx.loaders.product.createBulk.load(products.map(p => ({...p, thumbnailId: p.attachmentId})))`.
   - HTTP: `POST ${endpointv1}/bulk`, body `{ products: deepToSnakeCase(...) }`.
3. Initialize `attachmentList=[]`, `promiseList=[]`, `relationshipNodes=[]`, `attachmentAttributes=[]`.
4. For each `productInput`:
   - Match its created product via `_.find(productList.products, { thumbnailId: productInput.attachmentId })`.
   - If `attachmentId` present:
     - Push `{ documentId, resource: { id: product.productId, type: 'product' } }` onto `attachmentList`.
     - Push a relationship node `{ root: product.productId, rootResourceType: 'product', node: attachmentId, nodeResourceType: 'attachments_v3' }`.
     - If `businessPartners.length > 0`: push `attachmentAttributes` with `productPacketProps` (`partnerId`, `critical: 'true'`) and `managePermissionsRequest.partnersToAdd`.
     - Else push `attachmentAttributes` with just `relatedResources` + `documentId`.
5. If `attachmentAttributes.length`, **(EXT 🔴 attachment)** call `SPARK_Attachment.Mutation.bulkUpdateAttachmentsV2(null, { attachments: attachmentAttributes }, ctx)` (delegates into sibling resolver).
6. If `relationshipNodes.length`, **(EXT 🟡 relationship)** `addBulkRelationShip(ctx, relationshipNodes)` → if `status >= 400`, **return `Promise.reject(error)`** (whole mutation fails after products already created).
7. `await Promise.all(promiseList)` — currently always empty (dead code).
8. If `attachmentList.length`:
   - **(EXT 🔴 accessControl)** `permissionJWT = await getUserPermissionsJWT(attachmentList.map(a => a.documentId), ctx)`.
   - **(EXT 🔴 attachment)** `ctx.loaders.attachment.bulkUpdateResource(permissionJWT).load(attachmentList)` — fire-and-forget (no `await`).
9. **(EXT 🔴 workspaceV2)** `await ctx.loaders.workspaceV2.addResourcesToWorkspaceV2(workspaceResourcePermissionJWT).load(productList.products.map(p => p.productId), { workspaceId })`.
10. Return `productList` (shape: `{ products: [...] }`).

**Risks flagged:**
- **No rollback** on partial failure between step 2 (products created) and step 6 (relationships rejected) — products exist orphaned.
- **Fire-and-forget** `bulkUpdateResource` in step 8 swallows errors.
- **Dead code:** `promiseList` is never appended to.

**EXT services:** `accessControl` 🔴, `attachment` 🔴 (×2 paths), `relationship` 🟡, `workspaceV2` 🔴.

---

## M2. `updateProductTeamsWorkspaceContext(productId, teamWorkspacesToAdd, teamWorkspacesToRemove)` → `SPARK_Product`
**Resolver:** lines 639–640. **Complexity:** **Low (Small, 1–2 days)**.

1. `return ctx.loaders.product.updateProductTeamsWorkspaceContext.load(body)` → `PUT ${endpointv1}/{productId}/manage_workspace_teams`, body deep-snake-cased.

---

## M3. `addBusinessPartnersToProductWithType(productId: ID!, partners: [SPARK_ProductPartnerInput])` → `SPARK_Product`
**Resolver:** lines 641–663. **Complexity:** **Low**.

1. **(Internal)** `response = await ctx.loaders.product.addBusinessPartnersWithType.load(partners, { productId })` → `POST` partner-add.
2. If `response.product_id && !response.status_code` → return `response`.
3. Else log error with `status_code`/`message` and **return** `new Error(...)` (not throw — error becomes a value in the response).

**Note:** Returning an `Error` instead of throwing causes GraphQL to serialize it as `__typename`-broken; the field returns `null` to the client with no `errors[]` entry. Migration should use proper exception → `errors[]` mapping.

---

## M4. `addProduct(workspaceId, sparkProduct, copyProduct)` → `SPARK_Product`
**Resolver:** lines 664–691. **Complexity:** **Medium (Medium, 3–5 days)**.

1. **(Internal)** `product = await ctx.loaders.product.addProduct.load(sparkProduct)` → `POST ${endpointv1}`.
2. If `workspaceId`:
   - **(EXT 🔴 accessControl)** `jwt = await getUserPermissionsJWT(getWorkspaceResourceString(workspaceId), ctx)`.
   - **(EXT 🔴 workspaceV2)** `await ctx.loaders.workspaceV2.addResourcesToWorkspaceV2(jwt).load([product.productId], { workspaceId })`.
3. If `!_.isEmpty(copyProduct)`:
   - Set `copyProduct.targetProductId = product.productId`.
   - Call helper `copyProductToProduct(copyProduct, ctx)` (see Phase 2A §0.1 — calls `ctx.loaders.product.copyProduct(jwt).load(copyProduct)`).
   - Mutate `product.copyId`, `product.copyProductRequest`, `product.copyProductResources` onto the return value.
4. Return `product`.

**EXT services:** `accessControl` 🔴, `workspaceV2` 🔴.

---

## M5. `updateProduct(input: SPARK_ProductUpdateInput!, copyProduct)` → `SPARK_Product`
**Resolver:** lines 692–737. **Complexity:** **Medium**.

1. `product = {}`.
2. If `input` has any key other than `id` → **(Internal)** `product = await ctx.loaders.product.updateProduct.load(input)` → `PUT` update.
3. `copyProductRedirect = await copyProductToProduct(copyProduct, ctx)` (may be undefined).
4. If `copyProductRedirect`: set `product.copyId`, `.copyProductRequest`, `.copyProductResources`.
5. If `input.removedProductTemplateAttachments?.length`:
   - Partition into `v2Attachments` (have `documentId`) vs `v3Attachments` (have `humanId`).
   - If v2 non-empty: **(EXT 🔴 accessControl + 🔴 attachment)** get JWT for documentIds, then `attachment.archiveAttachmentBulkV2(jwt).load({ attachments: v2Attachments })`.
   - If v3 non-empty: same with `humanId`s and `archiveAttachmentBulkV3`.
6. Return `product`.

**Edge case:** If `input` only has `id` and no `copyProduct`, returns `{}` — client gets an empty `SPARK_Product` (no fields). Preserve in parity test.

---

## M6. `carryForwardProduct(productId, carryForwardProductInput)` → `SPARK_Product`
**Resolver:** lines 738–760. **Complexity:** **Low–Medium**.

1. **(Internal)** `response = await ctx.loaders.product.carryForwardProduct.load({ ...carryForwardProductInput, productId })` → `PUT ${endpointv1}/{productId}/carry_forward` (URL pattern in service line ~173).
2. If `!response || response.statusCode`: log error, **return** `new Error(...)` (same pattern as M3 — value, not thrown).
3. Else return `response`.

---

## M7. `bulkUpdateProducts(products: [SPARK_ProductUpdateInput])` → `SPARK_ProductBulkType`
**Resolver:** lines 761–762. **Complexity:** **Low**.

1. `return ctx.loaders.product.bulkUpdate.load(products)` → `PUT ${endpointv1}/mass_update`.

---

## M8. `removeProductResources(productId: ID!, resourceIds: [ID])` → `SPARK_Product`
**Resolver:** lines 763–767. **Complexity:** **Low**.

1. `return ctx.loaders.product.removeProductResources.load({ productId, resourceIds })` → `DELETE`.

---

## M9. `updateBusinessPartnerStatuses(productId, statusInput: [SPARK_ProductPartnerStatusInput])` → `SPARK_Product`
**Resolver:** lines 769–773. **Complexity:** **Low**.

1. `return ctx.loaders.product.updateBusinessPartnerStatuses.load({ productId, statusInput })` → `PUT`.

---

## M10. `addTeamsToProduct(productId, teamIds, workspaceIds, newPartners)` → `SPARK_Product`
**Resolver:** lines 774–821. **Complexity:** **Medium**.

1. If `newPartners?.length > 0`:
   - **(Internal)** `response = await ctx.loaders.product.addBusinessPartnersWithType.load(newPartners, { productId })`.
   - If `response.status_code`: log + **return** `new Error(...)` (same value-error pattern).
2. **(Internal)** `addTeamsResult = await ctx.loaders.product.addTeams.load(teamIds, { productId })` → `POST` add teams.
3. If `workspaceIds?.length > 0`:
   - Build `teamWorkspacesToAdd = workspaceIds.flatMap(ws => teamIds.map(t => ({ workspaceId: ws, teamId: t })))`.
   - **(Internal)** Return `ctx.loaders.product.updateProductTeamsWorkspaceContext.load({ productId, teamWorkspacesToAdd })`.
4. Else return `addTeamsResult`.

**Note:** Two different return shapes depending on `workspaceIds` — both shaped like `SPARK_Product` but produced by different backend endpoints. Pin in parity tests.

---

## M11. `productBusinessPartnerActions(actionType: String!, values: SPARK_ProductPartnerActionInput)` → `SPARK_Product`
**Resolver:** lines 822–1042. **Complexity:** **Very High (X-Large, 8–13 days)** — orchestrates across 6+ services; switch-on-string is brittle.

> This single resolver implements the schema-declared `removeProductBusinessPartner`, `dropProductBusinessPartner`, and `unDropProductBusinessPartner` flows (see drift note above).

### Top-level shape
`switch (actionType)` over 3 cases. No `default` — unknown `actionType` silently returns `undefined`.

### Case `'REMOVE_TEAM'` (lines 829–833)
1. **(Internal)** `ctx.loaders.product.removeProductResources.load({ productId: values.productId, resourceIds: values.teamIds })`.
2. Done.

### Case `'REMOVE_PARTNER'` (lines 834–867)
1. **(Internal)** `removeProductResources` with `resourceIds: values.teamIds`.
2. **(EXT 🔵 recentlyViewed)** `recentlyViewed.deleteRecentlyViewedByPartner({ resourceType:'product', partnerId, resourceIds: productId })`.
3. **(EXT 🔵 todo)** `todo.deleteToDoByBusinessPartner({ resourceType:'product', partnerId, resourceIds: productId })`.
4. **(EXT 🔵 favorite)** `favorite.deleteFavoritesByBusinessPartner({ resourceType:'product', resourceId: productId, partnerId })`.
5. **(EXT 🔴 accessControl)** `capabilityToken = await getUserPermissionsJWT(values.productId, ctx)`.
6. **(Internal)** `product.removeProductBusinessPartner(capabilityToken).load({ productId, partnerId })` → `DELETE`.

**Order matters** — partner-derived data (3 EXT cleanups) is deleted BEFORE the partner is removed from the product. **No rollback** if step 6 fails: ghost cleanups remain.

### Case `'DROP_UNDROP_PARTNER'` (lines 868–1039)
The most complex single block. Inputs: `{ productId, partnerId, dropped (bool), partnerType, workspaceId }`.

1. Build `dropUndropBody = { partnerId, dropped, partnerType, workspaceId }`.
2. Init `allResourcePermissions = {}`, `toBePermissionsMap = {}`, `allIds = []`.
3. **(EXT 🟡 relationship)** `relationShip = await ctx.loaders.relationship.searchByIds.load({ id: productId, includeBranches: ['product','sample','discussions','discussionThreads','claim'], includeNodeTypes: ['attachments','sample','discussions','discussionThreads','attachments_v3'] })`.
4. `relationShipMap = _.groupBy(relationShip[0].nodes, 'type')`.
5. Extract 5 id lists by type from the map: `discussionList`, `attachmentList`, `discussionThreadsList`, `sampleList`, `claimList` (each `?.map(({id})=>id) || []`).
6. `allIds = [...discussionList, ...attachmentList, ...discussionThreadsList, ...sampleList, productId, ...claimList]`.
7. If `allIds.length > 0`:
   - **(EXT 🔴 accessControl × N)** `allResourcePermissions = await filterResourcesByPartner(ctx, allIds, parseInt(partnerId), true, !dropped)` (batched ACL filter — see [utils/commonLoaders.js](spark-internal-graphql/packages/data-source-spark/src/utils/commonLoaders.js)).
   - For each of the 5 id lists: `_.remove(list, id => !(id in allResourcePermissions) || allResourcePermissions[id].permissions.length === 0)` — i.e., drop resources the user can't act on.
   - `toBePermissionsMap = getPermissionMapForBulkACLCall(allResourcePermissions, partnerId)`.
8. **(EXT 🔴 accessControl)** `capabilityToken = await getUserPermissionsJWT([productId, ...discussionList, ...discussionThreadsList, ...sampleList, ...claimList, SAMPLE_EVALUTION], ctx)`.
9. `sampleCallNeeded = sampleList?.length > 0`.
10. Conditional sample call:
    - If `partnerType !== DESIGN_PARTNER && sampleCallNeeded`:
      - `sampleCall = dropped ? sampleV2.dropSamples(token).load(sampleList) : sampleV2.unDropSamples(token).load(sampleList)`.
    - Else `sampleCall = false`.
11. **`Promise.all([` parallel `])`:**
    - **(Internal)** `product.dropUndropProductBusinessPartner(token).load(dropUndropBody, { productId })`.
    - `sampleCall` (🟡 sampleV2, may be `false` truthy-ish but `Promise.all` accepts non-promises).
12. `.then(async () => { … })`:
    - If `dropped`: **(EXT 🔴 accessControl)** `accessControl.dropPartnerFromResources.load(toBePermissionsMap)`.
    - Else: `accessControl.unDropPartnerFromResources.load(toBePermissionsMap)`.
    - If `dropped`: **(EXT 🟡 userAttributes)** `await UserProfileAttributes.Mutation.deleteAllUserProfileDataForAPartner(null, { partnerId, resourceId: productId, resourceType:'product', discussionIds, sampleIds }, ctx)` (delegates to sibling resolver).

**Returns:** `undefined` — schema says `SPARK_Product`, but resolver returns nothing in any case. Client likely gets `null`. Latent contract violation.

**EXT services:** `relationship` 🟡, `accessControl` 🔴 (×3 calls + batched ACL filter), `sampleV2` 🟡 (conditional), `userAttributes` 🟡 (conditional), plus 3× 🔵 (`recentlyViewed`, `todo`, `favorite`) in REMOVE_PARTNER.

---

## M12. `updateViewToggle(toggleInput: SPARK_ToggleInput)` → `SPARK_Product`
**Resolver:** lines 1043–1044. **Complexity:** **Low**.

1. `return ctx.loaders.product.updateViewToggle.load(toggleInput)` → `PUT`.

---

## M13. `updateWorkspaceAttributes(productId: ID!, workspaceAttributesInput: SPARK_ProductWorkspaceAttributesInput)` → `SPARK_Product`
**Resolver:** lines 1045–1053. **Complexity:** **Low**.

1. `return ctx.loaders.product.updateWorkspaceAttributes.load({ productId, workspaceAttributesInput })` → `PUT`.

---

## M14. `linkProduct(parentProductId, childProductId)` → `SPARK_Product`
**Resolver:** lines 1054–1055. **Complexity:** **Low**.

1. `return ctx.loaders.product.linkProduct.load(body)` → `PUT ${endpointv1}/{childProductId}/link_product` (`throwOnError: true`).

---

## M15. `unlinkProduct(parentProductId, childProductId)` → `SPARK_Product`
**Resolver:** lines 1056–1057. **Complexity:** **Low**.

1. `return ctx.loaders.product.unlinkProduct.load(body)` → `PUT ${endpointv1}/{childProductId}/unlink_product`.

---

## M16. `addProductRule(rule: SPARK_ProductRuleCreateInput)` → `SPARK_ProductRules`
**Resolver:** lines 1058–1064. **Complexity:** **Low**.

1. `result = await ctx.loaders.product.addRule.load(body.rule)` → `POST ${endpoint}/spark_rules/v1`, body transformed via `rulesRequestTransformer`.
2. If `result.statusCode`: **throw** `Error(...)` (this one actually throws — consistency violation vs M3/M6).
3. Return `result`.

---

## M17. `updateProductRule(rule: SPARK_ProductRuleUpdateInput)` → `SPARK_ProductRules`
**Resolver:** lines 1065–1071. **Complexity:** **Low**.

1. `result = await ctx.loaders.product.updateRule.load(body.rule)` → `PUT ${endpoint}/spark_rules/v1/{rule.id}`.
2. If `result.statusCode`: **throw**.
3. Return `result`.

---

## M18. `deleteProductRule(ruleId: ID!)` → `Boolean`
**Resolver:** lines 1072–1079. **Complexity:** **Low**.

1. `result = await ctx.loaders.product.deleteRule.load(body.ruleId)` → `DELETE`.
2. **Inverted logic (latent bug):** `if (result) { throw ... }` — comment says "We normally return nothing on success." So success path = falsy `result`. If the backend ever returns truthy on success, this throws.
3. Return `true`.

---

## M19. `updateComponentStatus(productComponents: [ProductComponentStatusUpdateInput])` → `SPARK_Product`
**Resolver:** lines 1080–1081. **Complexity:** **Low**.

1. `return ctx.loaders.product.updateComponentStatus.load({ productComponents })` → `PUT ${endpointv1}/component_status_update/bulk`.

---

## M20. `updateComponentStatuses(productId, ids: SPARK_ComponentIdsInput!, status: SPARK_ComponentStatusInput)` → `SPARK_Product`
**Resolver:** lines 1082–1101. **Complexity:** **High** — fans out to 5 co-located loaders in parallel.

### Pseudo-logic
1. `promises = []`.
2. If `ids.bomIds?.length`: **(Internal — co-located)** `promises.push(ctx.loaders.bom.updateBomComponentStatus({ productId, ids: ids.bomIds, status: { ...status, type: 'PRODUCT_BOM_STATUS' } }))`.
3. If `ids.measurementSetIds?.length`: **(Internal — co-located)** `promises.push(ctx.loaders.measurement.updateMeasurementComponentStatus({ productId, ids: ids.measurementSetIds, status }))`.
4. If `ids.constructionSetIds?.length`: **(Internal — co-located)** `promises.push(ctx.loaders.ProductDetails.updateProductDetailComponentStatus({ productId, ids: ids.constructionSetIds, status }))`.
5. If `ids.claimIds?.length`:
   - Build `sparkClaim = ids.claimIds.map((claimId, index) => ({ humanId: ids.claimIds[index], statuses: [{ ...status, claimIds: ids.claimIds }], parentId: productId }))`.
     - **Note:** `claimId` parameter is shadowed but unused; `ids.claimIds[index]` is the value. Refactor opportunity.
   - **(EXT 🟡 claim)** `promises.push(ctx.loaders.claim.bulkUpdateClaim({ updateClaimDtoList: sparkClaim }))`.
6. If `ids.packagingIds?.length`: **(Internal — co-located)** `promises.push(ctx.loaders.packaging.updatePackagingComponentStatus({ productId, ids: ids.packagingIds, status }))`.
7. `await Promise.all(promises)`.
8. **Returns `undefined`** — schema says `SPARK_Product`, resolver returns nothing. Latent contract violation. Client gets `null`.

**EXT services:** `claim` 🟡 (the only non-co-located call). 4 of the 5 fan-outs become a single `plm-product` Kotlin service method.

---

## EXT Service Call Summary (Mutations only)

| Loader | Severity | Touched From | Notes |
|---|---|---|---|
| `accessControl` (JWT + ACL filter) | 🔴 RED | M1, M4, M5, M11 (×3 calls) | Most mutations need workspace or product JWT |
| `attachment` (bulkUpdate, archive v2/v3, bulkUpdateResource) | 🔴 RED | M1, M5 | JWT-curried loaders |
| `workspaceV2.addResourcesToWorkspaceV2` | 🔴 RED | M1, M4 | JWT-curried |
| `relationship.searchByIds` | 🟡 YELLOW | M1 (bulk), M11 (drop/undrop) | Tree walk |
| `sampleV2.dropSamples / unDropSamples` | 🟡 YELLOW | M11 (conditional) | JWT-curried |
| `userAttributes.deleteAllUserProfileDataForAPartner` | 🟡 YELLOW | M11 (drop only) | Via sibling resolver delegation |
| `claim.bulkUpdateClaim` | 🟡 YELLOW | M20 | Only non-co-located fan-out |
| `recentlyViewed.deleteRecentlyViewedByPartner` | 🔵 BLUE | M11 (REMOVE_PARTNER) | Pure cleanup |
| `todo.deleteToDoByBusinessPartner` | 🔵 BLUE | M11 (REMOVE_PARTNER) | Pure cleanup |
| `favorite.deleteFavoritesByBusinessPartner` | 🔵 BLUE | M11 (REMOVE_PARTNER) | Pure cleanup |
| `bom`, `measurement`, `ProductDetails`, `packaging` | — Internal (co-located) | M20 | Become same-service Kotlin calls |
| `product` self | — Internal | All | Becomes Feign client to spark-product |

---

## Complexity Roll-Up (Mutations only, 22 implemented)

| Tier | Operations | Count | Days (un-buffered) |
|---|---|---|---|
| Very High | `productBusinessPartnerActions` (M11) | 1 | 8–13 |
| High | `addProducts` (M1), `updateComponentStatuses` (M20) | 2 | 10–16 |
| Medium | `addProduct` (M4), `updateProduct` (M5), `addTeamsToProduct` (M10), `carryForwardProduct` (M6) | 4 | 12–20 |
| Low | M2, M3, M7, M8, M9, M12, M13, M14, M15, M16, M17, M18, M19, M21*, M22*, M23* | 15 | 15–30 |
| **Total (Mutations)** | | **22 implemented + 3 schema-only stubs** | **45–79 days** |

\* M21–M23 = the 3 missing wrapper data fetchers needed to satisfy schema-declared `removeProductBusinessPartner`, `dropProductBusinessPartner`, `unDropProductBusinessPartner`. Estimate ~1 day each.

Apply +20% buffer: **~54–95 days for Mutation work alone.**

---

## Cross-Cutting Findings (Mutations)

1. **Inconsistent error handling.** M3, M6, M10 **return** `new Error(...)` (value); M16, M17 **throw** `new Error(...)`; M11, M20 swallow errors silently and return `undefined`. DGS migration should standardize on thrown `DgsException` / `DataFetcherExceptionHandler`.
2. **Schema-vs-resolver drift** (top of doc) for 3 partner mutations — must resolve.
3. **No rollback / saga** for multi-step mutations (M1, M11). Currently products can be created with orphaned attachments/relationships. Consider compensating actions in DGS or move to backend transactional endpoint.
4. **Fire-and-forget** loader calls in M1 step 8 (`bulkUpdateResource`) — don't migrate this pattern; await for parity.
5. **Latent ordering / typing bugs:**
   - M18 inverted-logic delete check.
   - M20 unused `claimId` shadow var.
   - M11 `sampleCall = false` mixed with promises in `Promise.all` (works in JS, but fragile).
6. **Sibling-resolver direct delegation** (`SPARK_Attachment.Mutation.bulkUpdateAttachmentsV2`, `UserProfileAttributes.Mutation.deleteAllUserProfileDataForAPartner`) — in DGS these become **Feign client calls into other DGS services**, not GraphQL resolver calls. They are EXT 🔴.
7. **Co-location wins** in M20: 4 of 5 fan-outs collapse to one Kotlin service in `plm-product`.

---

**Phase 2B complete — Mutations.** Reply `next` to proceed to Phase 2C (50+ field resolvers on `SPARK_Product`, plus the polymorphic `SPARK_Categories.__resolveType`).
