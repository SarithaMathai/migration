# Phase 2: Resolver Dependency Analysis — BOM

> **Domain:** `bom`
> **Target DGS:** `BomService` → `plm-product` (co-located; the draft's `plm-bom` label is superseded — see catalog)
> **Pipeline Version:** 2.0
> **Generated:** 2026-06-26
> **Source of truth:** `code/schemas/SPARK_Bom.txt` (SDL), `code/resolvers/product/SPARK_Bom.txt`, `code/services/product/Bom.txt`, `code/utils/bomUtils.txt`
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md)
> **DGS Target Status:** Green-field · **Analysis Mode:** Full

This is the implementation spec. A junior engineer implements each operation from the pseudo-logic here
without opening the `.txt` resolver. Every cross-domain call is tagged 🔴/🟡/🔵.

## Summary Statistics

| Metric | Count |
|--------|-------|
| Query resolvers | 13 |
| Mutation resolvers | 6 |
| Field resolvers (non-trivial) | ~46 across 18 type blocks |
| Field resolvers (trivial pass-through) | 6 |
| Interfaces (`__resolveType`) | 2 (7 material variants, 5 impression variants) |
| Helper functions (module-level) | 5 |
| Service methods (`BomService`) | 17 |
| Utils functions used (`bomUtils` + shared) | ~20 |
| EXT loader keys | 12 (2 🔴 · 6 🟡 · 4 🔵) |
| Very High complexity ops | 1 (updateBom) |
| High complexity ops | 2 (BomTrimMaterial, ImpressionDetails_Unified) |

> **Estimates:** complexity tiers only (per Pipeline 2.0). Rough day-ranges live in `04-po-summary.md`.

---

## Helper Functions (module-level, `SPARK_Bom.txt:710-735` + `:63-80`)

### H1 · `getMaterialWeight(material, ctx)` — `:710-719`
Used by every material type's `weight` field. If `material.weight` set: load `materialHub.getHubUnitsOfMeasure`,
find UoM by `weightUomId` (fallback code **23** = grams), return `{value, unitOfMeasure}`. Else `null`.
**EXT:** 🟡 `materialHub`. **DGS:** `MaterialWeightService.resolve(material)` with cached UoM table.

### H2 · `getValueWithMaterialHubUom(value, uomCode, ctx)` — `:721-728`
Same shape as H1 for arbitrary value+uom; used by `BomMaterial.sizeUnitOfMeasure`. **EXT:** 🟡 `materialHub`.

### H3 · `getCodedOptions(type, ctx)` — `:730-735`
Loads `materialHub.getHubCodedOptions(type)` → `Map<code, description>`. Used by `origins`/`certifications`.
**EXT:** 🟡 `materialHub`. **DGS:** cache per request (`@Cacheable` keyed on type).

### H4 · `searchMaterialById(varName, detail, ctx)` — `:63-69`
`id = detail[varName].id`; if present → `search.getMaterialByIds.load(id)`. Used by all impression color fields.
**EXT:** 🔴 `search`. **DGS:** `MaterialDataLoader` keyed on id.

### H5 · `getMaterialHubResource(material, ctx)` — `:71-80`
`matId = material.libraryResource.id`; if present → `permissionJWT = await getUserPermissionsJWT(matId)` →
`materialHub.getHubMaterial(permissionJWT).load(matId)`. **EXT:** 🔴 `accessControl` + 🟡 `materialHub`.

---

## Query Resolvers (12)

### Q1 · `getBomByIds(ids: [String!]): [Bom]` — Low
1. If `ids` empty → return `[]`.
2. `permissionJWT = await getUserPermissionsJWT(ids, ctx)`.
3. Return `ctx.loaders.bom.getBomByIds(permissionJWT, ids)`.
**Service:** `GET {base}/enterprise_product_development_products/bom/v1?ids={ids}` + `SPARK-Capability-Token`.
**Transform:** `deepToCamelCase`. **Error:** empty-array short-circuit; otherwise REST passthrough.
**Note:** not DataLoader-batched at resolver level — one REST call per invocation. Add a request DataLoader in DGS.

### Q2 · `getBomDataV2(ids: [String!]): [Bom_Unified]` — Low
Identical REST call to Q1; **only the return type differs** (`Bom_Unified` is a smaller projection of `Bom`).
Confirm `Bom_Unified` ⊆ `Bom`. Share one Kotlin service call; two `@DgsQuery` methods.

### Q3 · `getBomStatus: [CodeDescription]` — Low · *master data, cacheable*
`ctx.loaders.bom.getBomStatus()` → `GET {base}/masterData?name=BomStatus`. Transform `{key:value}` map →
`[{code, description}]`. **No JWT.** **DGS:** `@Cacheable("bomMasterData", key="'status'")`.

### Q4 · `getBomByParentId(parentId: String!): BomPaged` — Low
1. `permissionJWT = await getUserPermissionsJWT(parentId, ctx)`.
2. `boms = await ctx.loaders.bom.getActiveBomsByProductId(permissionJWT, parentId)`
   → `GET {base}/.../bom/v1/byProductId/{parentId}`.
3. Return `{ content: orderBy(boms, b => new Date(b.createdAt), 'desc') }` — **client-side sort**.
**Finding 🟡:** sort happens in the gateway. PO decision B03: push sort to backend to remove the hop.

### Q5 · `getBomMaterialTypes(ids: [String]): [BomMaterialType]` — Medium
1. `bomMaterialTypes = await ctx.loaders.bom.getBomMaterialTypes(ids)`
   → `GET {base}/.../master_data/bom_material_types[?ids={ids}]`.
2. `materialHubTypes = await ctx.loaders.materialHub.getHubMaterialTypes.load()`. **EXT** 🟡 `materialHub`.
3. Concat; map each hub type → `{code:9, description:type, bomType:{code:1,description:'Product'}, libraryLink:true, freeText:true}`.
**Finding 🟢 perf:** the two `await`s are independent — parallelize (`coroutineScope`/`Promise.all`) in port.

### Q6 · `getBomPackagingMaterialTypes: [BomMaterialType]` — Low · *master data, cacheable*
`GET {base}/.../master_data/packaging_bom_material_types`.

### Q7 · `getBomPackagingSubstrates: [BomPackagingSubstrate]` — Low · *master data, cacheable*
`GET {base}/.../master_data/packaging_bom_substrate_types`.

### Q8 · `getBomPackagingUnitOfMeasure: [UnitsOfMeasure]` — Low · *master data, cacheable*
`GET {base}/.../master_data/packaging_unit_of_measure`.

### Q9 · `getBomElastic(query): [Bom]` — Low
`{content: boms} = await ctx.loaders.search.getBomElastic.load(query)` → return `boms`. **EXT** 🔴 `search`.
**Finding 🟡:** the **entire `query` object** is passed to elastic, not just `q`. Document the exact field set.

### Q10 · `searchMaterialsBom(searchString, materialType, partnerIds, internalOnly, excludedTypes, size, sortField, sortDirection, nestedSearchFilters): BomMaterialSearch` — Medium
1. `fabricSuppliers = await VMM_BusinessPartner.Query.getRelatedFabricSuppliersByMerchVendors(null, {merchVendorIds: partnerIds}, ctx)` — **EXT** 🔵 `vmm` (reached via cross-resolver import — anti-pattern; use service call in DGS).
2. Build `queryPayload` from the args.
3. If `nestedSearchFilters.length`: for each `[i]`, flatten into 5 query-string keys
   `nestedSearchFilters[i].{type|fieldPath|nestedFieldPath|operator|values}`; then `delete queryPayload.nestedSearchFilters`.
4. Return `ctx.loaders.search.searchMaterialsBom.load(queryPayload)`. **EXT** 🔴 `search`.
**Finding 🟡:** the flatten is fragile (PO decision C02 — keep flatten vs structured DTO).

### Q11 · `getValidTrimSuppliersForBom(merchVendorIds: [ID]): [Int]` — Low
`return getRelatedSuppliersForMVs(ctx, merchVendorIds, [BusinessPartnerRole.TRIM_SUPPLIER.code])`. **EXT** 🔵 `vmm`.

### Q12 · `getValidRawMaterialSuppliersForBom(merchVendorIds: [ID]): [Int]` — Low
Same as Q11 with roles `[RAW_MATERIAL_SUPPLIER, FABRIC_SUPPLIER, TRIM_SUPPLIER]` (`VMM_ROLE_IDS`). **EXT** 🔵 `vmm`.

### Q13 · `getComboSupplierForBom(comboId: String, partnerIds: [ID]): [BomComboSupplier]` — Medium
1. `fabricSpecCombos = await SPARK_Combination.Query.searchFabricSpecCombos(null, {q:`parentComboId:${comboId}`, page:0, size:100}, ctx)` — **EXT** 🟡 `combination` (cross-resolver import → use service/federation in DGS).
2. Filter combos: keep where `fsId` set AND (`partnerIds` non-empty & `mvIds.length===1` & `partnerIds.includes(mvIds[0])`) OR `partnerIds` empty.
3. For each filtered (in `Promise.all`): `fs = await ctx.loaders.vmm.getByID.load(fsId)`; if `fs.bpName`, push `{fabricSupplier:{id:fsId, name:fs.bpName}, fabricSpecCombo}`. **EXT** 🔵 `vmm`.
**Finding 🟡:** `mvIds.length === 1` silently drops multi-MV combos — document; may be intentional.

---

## Mutation Resolvers (5)

### M1 · `addBom(sparkBom: SparkBomInput): Bom` — Medium
1. `bom = await ctx.loaders.bom.addBom(sparkBom)` → `POST {base}/.../bom/v1` (`transformRequest: deepToSnakeCase`, `transform: deepToCamelCase`, `primeKey: bom.humanId`).
2. If `bom.validationErrors || bom.message` → `throw Error('Error creating bom\n' + JSON.stringify(bom))`.
3. Return `bom`. **No JWT** (new resource). **DGS:** typed `BomValidationException`; `dataLoader.prime(humanId, bom)` after success.

### M2 · `updateBom(sparkBom: UpdateBomInput): Bom` — **Very High** (+1 for 3-step non-atomic write)
1. `permissionJWT = await getUserPermissionsJWT(sparkBom.humanId, ctx)`.
2. **If** `workspaceContext` and (`addWorkspaces.length` or `removeWorkspaces.length`): `await workspaceAssociationHelper(BOM, humanId, add, remove, ctx)` → PUT `.../{bomId}/{associate|dissociate}_workspace`. **(commits first)**
3. `bom = await ctx.loaders.bom.updateBom(permissionJWT, sparkBom)` → `PUT {base}/.../bom/v1/{humanId}` (`omitParamsInBody: true`).
4. If `validationErrors || message` → throw.
5. **If** `sparkBom.businessPartners`: `await ctx.loaders.bom.updatePermissions(permissionJWT).load(sparkBom)` → PUT `.../{humanId}/permission`.
6. Return `bom`.
**Finding 🔴 atomicity:** three sequential writes, **no rollback**. Step-2 workspace change persists even if step 3 fails; step-3 ACL can go stale if step 5 fails. **PO decision E (saga / compensation log / best-effort).**

### M3 · `manageBomWorkspaces(bomId, workspacesToAdd, workspacesToRemove): Bom` — Low
If either array non-empty → `result = await workspaceAssociationHelper(BOM, bomId, toAdd, toRemove, ctx)`; return `result` (else `undefined`).
**Finding 🟡:** returns `undefined` when both empty — document for clients.

### M4 · `lockBom(bomId: String!): Bom` — Low
`permissionJWT = await getUserPermissionsJWT(bomId)` → `ctx.loaders.bom.lockBom(jwt, bomId)` → `PUT .../{bomId}/lock`.

### M5 · `unlockBom(bomId: String!): Bom` — Low
Identical to M4 → `PUT .../{bomId}/unlock`.

### M6 · `updateBomComponentStatus(productId, ids, status): BomPaged` — Low
`return ctx.loaders.bom.updateBomComponentStatus({productId, ids, status})` → `PUT .../bom/v1/component_status_update`.
**Finding 🟡:** **no JWT** — the only write without one. **PO decision D05** (intentional or gap?).

---

## Field Resolvers (by type block)

### C1 · `Bom` + `Bom_Unified` — 9 fields each, **identical** → one Kotlin impl backs both — Medium
| Field | Backing | Call / EXT |
|---|---|---|
| `humanId` | inline | `bom.humanId ?? bom.id` — Direct/Computed |
| `access` | `getBomAccess` | `accessControl.getPermissions.load({resourceIds:[id]})`→`[0]` · 🔴 `accessControl` |
| `businessPartners` | `getBusinessPartners` | `loadBusinessPartners(id)` (Teams util) · 🔵 |
| `currentUserPermissions` | `getCurrentUserPermissions` | `accessControl.getUserAccessUnencoded.load(id)`→`resourcePermissions[0]` · 🔴 |
| `createdBy` | `getCreatedBy` | `getUser(bom.createdBy)` · 🔵 user-profile |
| `updatedBy` | `getUpdatedBy` | `getUser(bom.updatedBy)` · 🔵 |
| `product` | `getProduct` | if `parentId.startsWith('PID')` → `product.getByID.load(parentId)` else null · **internal** |
| `workspaces` | `getWorkspaces` | `WorkspaceV2.getWorkspacesByIdsV2({ids: workspaceContext})` · 🟡 `workspaceV2` |
| `participantDetails` | `getUserGroup` | userGroup loader · 🔵 |
**Finding 🟡:** `getProduct` only follows `PID*` parents — PO Q confirm no other prefixes.

### C2 · `BomMaterial_Unified` — 3 fields — Low
`libraryResourceId` (Direct), `libraryResource`=`getBomMaterial(material)` (4-case dispatcher: TRIM→`getTrimMaterial`,
WASH→`getWashMaterial`, FABRIC→`getFabricMaterial`, HUB→`getHubMaterial`, default→null), `materialLibraryUom`=`getMaterialLibraryUom` (resolves only when category=TRIM).

### C3 · `BomMaterialInterface.__resolveType` — 21-case dispatcher → 7 types — Low (+1 → Medium for polymorphism)
TRIM(4)→`BomTrimMaterial` · WASH(6)→`BomWashMaterial` · FABRIC(2)→`BomFabricMaterial` · COMBINATION(15)→`BomCombinationMaterial` ·
FABRIC_SPEC(16)→`BomFabricSpecMaterial` · PACKAGING+others(10,11,12,13,14,17–24)→`BomPackagingMaterial` ·
default(1 COMPONENT, 5 OTHER, **9 HUB**)→`BomMaterial`. **Preserve the HUB-falls-through default.** DGS: `@DgsTypeResolver`.

### C4 · `BomMaterial` — 8 fields — Medium
`impressionDetails`=`material.impressions` (rename) · `libraryResourceId` (Direct) · `libraryResource`=`getMaterialHubResource` (H5, 🔴+🟡) ·
`genericMaterialType` (loads hub; if `baseMaterial.relatedMaterialType` ≠ local → hub's value) · `countryOfOrigin`=`getCountryOfOrigin` (🔵 `tag`) ·
`parentLibraryResourceId` (Direct) · `origins`/`certifications` (H3 coded-options filter+enrich, 🟡) · `weight`=H1 (🟡) · `sizeUnitOfMeasure`=H2 (🟡).
**Finding 🟡:** hub resource loaded twice (`libraryResource`+`genericMaterialType`) — DataLoader-memoized; consolidate.

### C5 · `BomPackagingMaterial` — 2 fields — Low
`impressionDetails` (rename), `countryOfOrigin` (🔵 `tag`).

### C6 · `BomFabricMaterial` — 4 fields — Low
`libraryResource`: `search.searchFabricSpecCombos.load({q:`id:${fscId}`,page:0,size:1})`→`content[0] ?? {id:fscId}` (🔴 `search`) · `weight`(H1) · `countryOfOrigin` · `impressionDetails`.

### C7 · `BomFabricSpecMaterial` — 4 fields — Low
`libraryResource`: `fabric.getSpecificationByID.load(fabricSpecId)`→`?? {id}` (🟡 `fabric`) · `weight` · `countryOfOrigin` · `impressionDetails`.

### C8 · `BomCombinationMaterial` — 4 fields — Low
`libraryResource`: `combination.getById.load(combinationId)`→`?? {id}` (🟡 `combination`) · `weight` · `countryOfOrigin` · `libraryResourceId`.

### C9 · `BomTrimMaterial` — 7 fields — **High** (largest material subtype)
`libraryResource`: `trim.getTrimBatch.load(trimId)` (🟡 `trim`) · `materialLibraryUom`: trim UoMs, find by `materialLibraryUomId.toString()` ·
`sizeValue`: reload trim → match size by `librarySizeId` → `getTrimSizeValue(trimType, trimSubType, size)` (**15-case TRIM_TYPES**) ·
`sizeCaption`: reload trim → `getBomSizeCaption(trim, size)` (**15-case**, returns `{edit, view}`) ·
`facilityName`: if `material.facilityName` set → return; else reload trim → find supplier by `supplierId` → facility by `facilityId` → `location.getLocationById(facilityId).load()` → `vmmFacility.name` (🔵 `location`) ·
`weight` · `countryOfOrigin`.
**Finding 🔵 perf:** `getTrimBatch` hit 3× per material (memoized) — consolidate into one `TrimEnrichmentService.enrich(material)`.
**Finding 🟡:** preserve int→string `materialLibraryUomId.toString()` coercion.

### C10 · `BomWashMaterial` — 4 fields — Low
`libraryResource`: `permissionJWT = await getUserPermissionsJWT(washId)` → `wash.getWash(jwt).load(washId)`→`?? {id}` (🔴 `accessControl` + 🟡 `wash`) · `weight` · `countryOfOrigin` · `impressionDetails`.

### C11 · `BomImpressionDetailsInterface.__resolveType` — 5-case — Low
TRIM(603)→`BomTrimLibraryImpressionDetails` · TRIM_ZIPPER(605)→`BomTrimZipperLibraryImpressionDetails` ·
WASH(604)→`BomWashLibraryImpressionDetails` · FABRIC(602)→`BomFabricLibraryImpressionDetails` · default(601 BASE)→`BomBaseImpressionDetails`.

### C12 · `BomImpressionDetails_Unified` — 6 fields — **High** (+1 for internal/external branch)
`libraryResource`:
- **internal** (`ctx.currentUser.internal`): `searchMaterialById('libraryResource', detail, ctx)` (🔴 `search`).
- **external**: `bomIds = args.ids`; `libraryResourceId = detail.libraryResource.id`; if none → null; `permissionJWT = await getUserPermissionsJWT(bomIds)`; `search.searchMaterialsByProxyIds(jwt).load({q:`id:(${libraryResourceId})`, proxyIds: bomIds, page:0, size:1})` → `content[0] ?? {id}` (🔴 `search`, 🔴 `accessControl`).
`groundColor`/`textColor`/`sliderColor`/`tapeColor`/`teethColor`: `searchMaterialById(name, detail, ctx)` (5 separate loader calls).
**Finding 🔴:** `args.ids` is read off the field args — only present when the parent query carried an `ids` arg. Fragile contract. **DGS:** pass `bomIds` via `DgsDataFetchingEnvironment` local context, not field args.

### C13 · `BomFabricLibraryImpressionDetails` — 1 field — Low (+1 branch → Medium)
`libraryResource` — same internal/external branch as C12.

### C14 · `BomTrimLibraryImpressionDetails` — 3 fields — Low (+1 branch → Medium)
`libraryResource` (same branch) + `groundColor`, `textColor` via `searchMaterialById`.

### C15 · `BomTrimZipperLibraryImpressionDetails` — 3 fields — Low
`sliderColor`, `tapeColor`, `teethColor` via `searchMaterialById` (🔴 `search`).

### C16 · `BomMaterialType.id` — 1 synthetic field — Low (trivial)
`id = `${detail.code}_${detail.description}``. Computed.

### C17 · `BomMaterialSearch.paging` — 1 field — Low (trivial)
`paging = searchResults` (whole-object passthrough).

### C18 · `BomMaterialSearchResult` — 5 fields — Medium
`description`=`detail.description ?? detail.name` · `status`=`detail.status?.description ?? detail.status` ·
`fabricSpec`: if `type==='fabric_spec_combo'` & `fabricSpecId` → `fabric.getSpecificationByID.load(id)` (🟡) ·
`fabric`: if `type==='combination'` & `fabricRecordHumanId` → `permissionJWT` → `fabric.getByID(jwt).load(id)` (🔴+🟡) ·
`fabricId`: if `type==='combination'` → `fabricRecordHumanId` ·
`relatedMaterials`: 2-branch (internal/external) elastic search by `relatedAssetIds` buckets (🔴 `search`).
**Finding 🟡:** external branch does `proxyIds.push(detail.parentComboId)` — **mutates the args array**. Defensive-copy in port.

### Trivial Pass-Through Resolvers (bundle into one story)
| Resolver | Returns |
|---|---|
| `BomMaterial.impressionDetails` (+ Fabric/FabricSpec/Trim/Wash/Packaging variants) | `material.impressions` (rename) |
| `*.libraryResourceId` (all material types) | `get(material,'libraryResource.id', null)` |
| `BomMaterial.parentLibraryResourceId` | `get(material,'parentLibraryResource.id', null)` |

---

## Service Classes (1)

### S1 · `BomService` — base `…/enterprise_product_development_products/bom/v1` — `services/product/Bom.txt` (184 lines)
| # | Method | HTTP | Path | JWT | Notes |
|---|---|---|---|---|---|
| 1 | `getBomByIds(jwt, ids)` | GET | `/v1?ids={ids}` | ✓ | listing transform |
| 2 | `getActiveBomsByProductId(jwt, id)` | GET | `/v1/byProductId/{id}` | ✓ | |
| 3 | `getActiveBomsByProductIdAndBomType(jwt, id, type)` | GET | `/v1/byProductId/{id}?type={type}` | ✓ | **unused by bom resolvers** — product domain caller |
| 4 | `getBomVersionsById(jwt, id)` | GET | `/v1/{id}/versions` | ✓ | **unused** |
| 5 | `getBomVersion({id, version})` | GET | `/v1/{id}/versions/{version}` | aclToken | **unused** |
| 6 | `getBomStatus()` | GET | `/masterData?name=BomStatus` | ✗ | cacheable |
| 7 | `addBom(bom)` | POST | `/v1` | ✗ | `primeKey: humanId` |
| 8 | `updateBom(jwt, bom)` | PUT | `/v1/{humanId}` | ✓ | `omitParamsInBody: true`; primes cache |
| 9 | `updatePermissions(jwt)` | PUT | `/v1/{humanId}/permission` | ✓ | returns DataLoader callable |
| 10 | `getBomMaterialTypes(ids)` | GET | `/master_data/bom_material_types[?ids]` | ✗ | cacheable |
| 11 | `getBomPackagingMaterialTypes()` | GET | `/master_data/packaging_bom_material_types` | ✗ | cacheable |
| 12 | `getBomPackagingSubstrates()` | GET | `/master_data/packaging_bom_substrate_types` | ✗ | cacheable |
| 13 | `getBomPackagingUnitOfMeasure()` | GET | `/master_data/packaging_unit_of_measure` | ✗ | cacheable |
| 14 | `manageWorkspaceAssociations(bomId, action, jwt)` | PUT | `/v1/{bomId}/{associate\|dissociate}_workspace` | ✓ | via workspaceAssociationHelper |
| 15 | `lockBom(jwt, bomId)` | PUT | `/v1/{bomId}/lock` | ✓ | |
| 16 | `unlockBom(jwt, bomId)` | PUT | `/v1/{bomId}/unlock` | ✓ | |
| 17 | `updateBomComponentStatus(input)` | PUT | `/v1/component_status_update` | ✗ | **missing JWT** |

**Findings:** (D-S1) methods 3/4/5 unused by bom — confirm cross-domain callers before deleting; all master-data methods cacheable; preserve `prime()`/`omitParamsInBody`.

---

## Referenced Utils

| U# | `bomUtils` fn | Purpose | DGS equivalent |
|---|---|---|---|
| U1 | `getTrimSizeValue` (15-case) | size string per trim type | Kotlin `TrimSizePresentation` table |
| U2 | `getBomSizeCaption` (15-case) | `{edit,view}` caption per trim type | same table (co-locate with U1) |
| U3 | `getSizeOptions`/`getBomUomOptions` | size/uom option lists | service helpers |
| U4 | `getSuppliers` | builds size/color/finish id arrays — **mutates input** | defensive-copy in port |
| U5 | `getBomAccess`/`getCurrentUserPermissions` | ACL load → first element | `accessControl` calls |
| U6 | `getBomMaterial` (4-case) + `getTrim/Fabric/Hub/WashMaterial` | material summary dispatcher | `BomMaterialEnrichmentService` |
| U7 | `getCountryOfOrigin` | tag lookup by `countryOfOriginIds` | `tag` call |
| U8 (shared) | `commonLoaders.getUserPermissionsJWT` | ACL capability token | `@DgsContext` header forwarding |
| U9 (shared) | `workspaceAssociationHelper` | associate/dissociate | service method |

**Latent bugs to fix on port:** `getHubMaterial` missing `await` on `getUserPermissionsJWT` (`bomUtils.txt:271`);
`getFabricMaterial` reads `fabricSpec.humanId` after a `... || null` (TypeError if no content) (`:250-251`);
`getSuppliers` mutates input (`:46-55`).

---

## EXT Service Call Inventory

**By loader key — 12 keys (2 🔴 · 6 🟡 · 4 🔵):**

| # | Loader key | Owning DGS/platform | HTTP / via | Severity | Called from |
|---|---|---|---|---|---|
| 1 | `accessControl` | AccessControlService | JWT + permissions | 🔴 | Q1/Q4, M2/M4/M5, C1/C10/C12/C18, H5 |
| 2 | `search` | SearchService (elastic) | elastic | 🔴 | Q9, Q10, C6, C12–C15, C18, H4 |
| 3 | `materialHub` | MaterialHubService | loader | 🟡 | Q5, C4, H1/H2/H3/H5 |
| 4 | `trim` | TrimService | `getTrimBatch`/UoMs | 🟡 | C9, `getMaterialLibraryUom` |
| 5 | `wash` | WashService | JWT loader | 🟡 | C10 |
| 6 | `fabric` | FabricService | `getSpecificationByID`/`getByID` | 🟡 | C7, C18 |
| 7 | `combination` | CombinationService | `getById`/search | 🟡 | Q13, C8 |
| 8 | `workspaceV2` | WorkspaceService | `getWorkspacesByIdsV2`/assoc | 🟡 | C1, M2, M3 |
| 9 | `vmm` | VMM platform | `getByID`/supplier roles | 🔵 | Q10, Q11, Q12, Q13 |
| 10 | `location` | VMM platform | `getLocationById` | 🔵 | C9 facilityName |
| 11 | `tag` | TagService | `getTags` | 🔵 | C4/C5 countryOfOrigin |
| 12 | userGroup/userAttributes | UserProfileService | `getUser`/`getUserGroup` | 🔵 | C1 |

`product` loader (Bom.product) is an **internal** same-DGS call — not EXT.

---

## Complexity Assessment

| Operation | Type | EXT | Complexity |
|---|---|---|---|
| updateBom | Mutation | 🔴 acl + 🟡 ws | **Very High** (3-step non-atomic) |
| BomTrimMaterial (C9) | Field block | 🟡 trim + 🔵 loc | **High** |
| BomImpressionDetails_Unified (C12) | Field block | 🔴 search/acl | **High** (internal/external branch) |
| getBomMaterialTypes, searchMaterialsBom, getComboSupplierForBom, addBom, BomMaterial(C4), BomMaterialSearchResult(C18) | mixed | varies | **Medium** |
| all master-data queries, lock/unlock, simple material blocks | mixed | varies | **Low** |

Bump rules applied: `__resolveType` (+1 → C3 Medium); `isExternal` branch (+1 → C12/C13/C14, C18).

## Key Findings

**Highest risk:** (1) `updateBom` 3-step atomicity 🔴; (2) `BomImpressionDetails_Unified.libraryResource` `args.ids` contract 🔴; (3) `BomTrimMaterial` 15-case trim dispatcher × 2.
**Migration blockers:** field resolvers need sibling stubs (materialHub/trim/wash/fabric/combination) published before they resolve full types via gateway.
**Refactor recommendations:** circular `MATERIAL_CATEGORY_ID` import → `BomConstants.kt`; module-level helpers → `BomMaterialHelpers.kt`; single impl for `Bom`/`Bom_Unified`; consolidate 3× trim load.
**Quick wins:** 4 master-data queries (`@Cacheable`); lock/unlock; trivial pass-throughs.
**Latent bugs:** `getHubMaterial` missing await; `getFabricMaterial` null-guard; `getSuppliers`/`relatedMaterials` array mutation.

---
**Phase Completed:** Phase 2 — Resolver Dependency Analysis · **Domain:** `bom` · **Files:** 3 (1,244 lines)
**EXT:** 12 keys (2 🔴 · 6 🟡 · 4 🔵) · **Next:** Phase 3 — Schema Derivation.
