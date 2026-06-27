# Bom — Resolver Analysis: Services + Utils

> **Domain:** `bom` · **Source:** [services/product/Bom.js](spark-internal-graphql/packages/data-source-spark/src/services/product/Bom.js), [utils/bomUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/bomUtils.js)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## D1. `BomService` (16 methods, 184 lines)

| # | Method | HTTP | Path | JWT | Notes |
|---|---|---|---|---|---|
| 1 | `getBomByIds(jwt, ids)` | GET | `/v1?ids={ids}` | ✓ | Listing transform |
| 2 | `getActiveBomsByProductId(jwt, id)` | GET | `/v1/byProductId/{id}` | ✓ | |
| 3 | `getActiveBomsByProductIdAndBomType(jwt, id, bomType)` | GET | `/v1/byProductId/{id}?type={bomType}` | ✓ | **Unused by Bom resolvers** — likely called from product domain |
| 4 | `getBomVersionsById(jwt, id)` | GET | `/v1/{id}/versions` | ✓ | **Unused** — no schema query exposes this |
| 5 | `getBomVersion({id, version})` | GET | `/v1/{id}/versions/{version}` | `fetchAclToken: true` | **Unused** — uses single-record loader; possibly future |
| 6 | `getBomStatus()` | GET | `/masterData?name=BomStatus` | ✗ | Master data; cacheable |
| 7 | `addBom(bom)` | POST | `/v1` | ✗ | `primeKey: bom.humanId`, primes read cache |
| 8 | `updateBom(jwt, bom)` | PUT | `/v1/{humanId}` | ✓ | `omitParamsInBody: true`; primes read cache |
| 9 | `updatePermissions(jwt)` | PUT | `/v1/{humanId}/permission` | ✓ | Returns DataLoader (caller `.load(bom)`) |
| 10 | `getBomMaterialTypes(ids)` | GET | `/master_data/bom_material_types[?ids={ids}]` | ✗ | Master data |
| 11 | `getBomPackagingMaterialTypes()` | GET | `/master_data/packaging_bom_material_types` | ✗ | Master data |
| 12 | `getBomPackagingSubstrates()` | GET | `/master_data/packaging_bom_substrate_types` | ✗ | Master data |
| 13 | `getBomPackagingUnitOfMeasure()` | GET | `/master_data/packaging_unit_of_measure` | ✗ | Master data |
| 14 | `manageWorkspaceAssociations(bomId, action, jwt)` | PUT | `/v1/{bomId}/{associate\|dissociate}_workspace` | ✓ | Called by `workspaceAssociationHelper` |
| 15 | `lockBom(jwt, bomId)` | PUT | `/v1/{bomId}/lock` | ✓ | |
| 16 | `unlockBom(jwt, bomId)` | PUT | `/v1/{bomId}/unlock` | ✓ | |
| 17 | `updateBomComponentStatus(input)` | PUT | `/v1/component_status_update` | ✗ | **Missing JWT** — flagged in Phase 2B M6 |

### Findings

| # | Finding | Severity |
|---|---|---|
| 1 | Methods 3/4/5 (`getActiveBomsByProductIdAndBomType`, `getBomVersionsById`, `getBomVersion`) appear unused by bom resolvers — confirm cross-domain callers (likely `Product.bom` / `Product.productBom` / `Product.packagingBom`) | 🟡 |
| 2 | `updateBomComponentStatus` (#17) is the only write without JWT — confirm intentional | 🟡 |
| 3 | `addBom` (#7) primes the read DataLoader after success (`primeKey: bom.humanId`) — preserve via DGS `dataLoader.prime()` | 🟢 |
| 4 | All master-data methods (6, 10, 11, 12, 13) are cacheable — apply `@Cacheable("bomMasterData", key=...)` in DGS | 🟢 perf |
| 5 | `updatePermissions` returns a DataLoader-shaped callable — DGS port should expose a regular method | 🟢 |
| 6 | `omitParamsInBody: true` on `updateBom` — verify Feign serializer strips path-arg from body | 🟢 |
| 7 | Endpoint naming inconsistency: `bom_material_types` vs `packaging_bom_material_types` (positional swap). Document | 🟢 |

---

## D2. `bomUtils.js` (325 lines)

### D2.1 Pure trim-presentation helpers

- `getSizeOptions(trim)` — returns size options filtered by `gvs` flag or approved-size membership; uses `getTrimSizeValue`
- `getBomUomOptions(trim)` — flattens supplier→facility→sizes→uom
- `getSuppliers(trimSuppliers)` — **mutates input** (adds `sizeIds`/`approvedColorRowIds`/`approvedFinishRowIds` arrays to each facility). **Defensive-copy in port.**
- `getTrimSizeValue(trimType, trimSubType, size, includeHelperLabel)` — **15-case TRIM_TYPES dispatcher** returning size string
- `createThreadSizeOption` / `createLabelSizeOption` / `buildMultipleFieldLabel` — internal helpers for above
- `getBomSizeCaption(trim, chosenSize)` — **15-case TRIM_TYPES dispatcher** returning `{edit, view}` caption pair
- `buildMultiFieldCaptionLabel` — caption assembly helper

### D2.2 Bom field-resolver helpers (used by `SPARK_Bom.js`)

| Helper | Calls |
|---|---|
| `getBomAccess` | `accessControl.getPermissions.load({resourceIds:[id]})` → `[0]` |
| `getBusinessPartners` | `loadBusinessPartners(id, ctx)` |
| `getCurrentUserPermissions` | `accessControl.getUserAccessUnencoded.load(id)` → `resourcePermissions[0]` |
| `getCreatedBy` | `getUser(bom.createdBy, ctx)` |
| `getProduct` | `if parentId.startsWith('PID') → product.getByID.load(parentId)` |
| `getWorkspaces` | `SPARK_WorkspaceV2.Query.getWorkspacesByIdsV2({}, {ids: workspaceContext}, ctx)` |
| `getUpdatedBy` | `getUser(bom.updatedBy, ctx)` |
| `getParticipantDetails` | `getUserGroup(ctx, id)` |
| `getBomMaterial` | 4-case dispatcher: TRIM/WASH/FABRIC/HUB → matching sub-helper |
| `getFabricMaterial` | `search.searchFabricSpecCombos.load(...)` → return `{humanId, description}` |
| `getTrimMaterial` | `trim.getTrimBatch.load(id)` → build trim summary + size + caption |
| `getHubMaterial` | JWT-curried `materialHub.getHubMaterial(jwt).load(id)` → build hub summary |
| `getWashMaterial` | JWT-curried `wash.getWash(jwt).load(id)` → build wash summary |
| `getTrimSize` / `getSizeCaption` | Inline of trim-batch + matching-size lookup |
| `getMaterialLibraryUom` | `trim.getTrimUnitOfMeasures.load()` → find by code |
| `getCountryOfOrigin` | `tag.getTags.load({ids: countryOfOriginIds})` → `content` |

### D2.3 Findings

| # | Finding | Severity |
|---|---|---|
| 1 | **Circular import smell:** `bomUtils.js` imports `MATERIAL_CATEGORY_ID` from `resolvers/product/SPARK_Bom.js`. Should move constant to `config/bomConstants.js` | 🟡 |
| 2 | `getSuppliers` mutates input arrays (`facility.sizeIds = ...`). Defensive-copy in Kotlin port | 🟡 |
| 3 | `getHubMaterial` uses `getUserPermissionsJWT(matId, ctx)` **without `await`** — pseudo-promise leaks into `materialHub.getHubMaterial(promise).load(id)`. Verify whether the loader handles promise inputs; likely a latent bug | 🟡 |
| 4 | `getFabricMaterial` does `fabricSpec.humanId` after `... || null` — if first call returns no content, this throws TypeError. Add null-guard in port | 🟡 |
| 5 | `getTrimMaterial` builds nested object with 13 properties — likely should return the full trim record and let GraphQL filter | 🟢 |
| 6 | 15-case TRIM_TYPES switch duplicated between `getTrimSizeValue` and `getBomSizeCaption` — co-locate in a single trim-size table in Kotlin | 🟢 |
| 7 | All field-resolver helpers expect `(parent, args, ctx)` shape — Kotlin port should accept a `BomMaterialEnvelope` data class to avoid losing intent | 🟢 |

---

## D3. `bomActivityModifiedDataHelper.js` (31 lines)

Cross-domain helper (lives outside `bom` folder) used by **activity-log** subsystem to diff bom snapshots. Not invoked from `SPARK_Bom.js` resolvers directly. Tracked here for completeness:

- Exports `BOM_ACTIVITY_MODIFIED_FIELDS` and `bomActivityModifiedDataHelper(oldBom, newBom)` returning a diff object.
- Used by the audit/activity feed.
- **Migration ownership:** activity-log subsystem, not the bom DGS. **Out of scope** for this domain's Phase 4. Track as a separate ticket if activity-log is migrated.

---

## D4. Cross-Cutting Utilities Used by Bom

These do **not** belong to bom; bom is just a consumer.

| Util | Owner | Used by |
|---|---|---|
| `commonLoaders.getUserPermissionsJWT` | shared | Q1/Q4, M2/M4/M5, C2/C4/C9/C10/C12/C13/C14, util helpers |
| `workspaceAssociationHelper` | workspace utils | M2, M3 |
| `vmmUtils.getRelatedSuppliersForMVs` | vmm | Q11, Q12 |
| `Product/userGroupUtils.getUserGroup` | product | `participantDetails` |
| `userAttributesUtils.getUser` | user-profile | createdBy, updatedBy |
| `resolvers/commonResolvers/Teams.loadBusinessPartners` | teams | `businessPartners` |
| `resolvers/SPARK_Combination.Query.searchFabricSpecCombos` | combination | Q13 |
| `resolvers/SPARK_WorkspaceV2.Query.getWorkspacesByIdsV2` | workspace | `getWorkspaces` |
| `resolvers/VMM_BusinessPartner.Query.getRelatedFabricSuppliersByMerchVendors` | vmm | Q10 |

**Finding 🟡:** Two cross-resolver imports (Q10 → VMM_BusinessPartner, Q13 → SPARK_Combination). In DGS, replace with native service-method calls or federation entity calls.

---

## D5. Effort Summary

| Bucket | Days |
|---|---|
| BomService Kotlin port (17 methods, mostly thin wrappers) | 5–8 |
| `bomUtils.js` trim-presentation helpers (60% of file) | 4–6 |
| `bomUtils.js` field-resolver helpers (40% of file) | 4–6 |
| Refactor circular `MATERIAL_CATEGORY_ID` import | 1 |
| Fix latent bugs (D2.3 #2, #3, #4) | 1–2 |
| **Subtotal services + utils** | **15–23** |

---

## D6. Phase 2 Grand Total

| Sub-phase | Days |
|---|---|
| 2A Queries | 17–29 |
| 2B Mutations | 11–19 |
| 2C Field resolvers | 26–47 |
| 2D Services + utils | 15–23 |
| **Phase 2 raw** | **69–118** |
| **+20% buffer** | **83–142** |

---

**Phase Completed:** Phase 2D — Services + Utils
**Output:** [output/bom/02-resolver-analysis-services.md](output/bom/02-resolver-analysis-services.md)
