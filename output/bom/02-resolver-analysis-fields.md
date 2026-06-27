# Bom — Resolver Analysis: Field Resolvers

> **Domain:** `bom` · **Source:** [resolvers/product/SPARK_Bom.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_Bom.js) (lines 317–732) + [utils/bomUtils.js](spark-internal-graphql/packages/data-source-spark/src/utils/bomUtils.js)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

~52 field resolvers across 18 type blocks.

---

## C1 · `SPARK_Bom` + `SPARK_Bom_Unified` (9 fields each, identical) — CAT-2 · Medium (3–5d)

Both types share the same nine field resolvers. Single Kotlin implementation can back both schema types.

| Field | Util backing | Calls |
|---|---|---|
| `humanId` | inline | `bom.humanId ?? bom.id` |
| `access` | `getBomAccess` | `accessControl.getPermissions.load({resourceIds:[id]})` → `[0]` |
| `businessPartners` | `getBusinessPartners` | `loadBusinessPartners(id, ctx)` (shared Teams util) |
| `currentUserPermissions` | `getCurrentUserPermissions` | `accessControl.getUserAccessUnencoded.load(id)` → `resourcePermissions[0]` |
| `createdBy` | `getCreatedBy` | `getUser(bom.createdBy, ctx)` (user-profile) |
| `updatedBy` | `getUpdatedBy` | `getUser(bom.updatedBy, ctx)` |
| `product` | `getProduct` | If `parentId.startsWith('PID')` → `product.getByID.load(parentId)` else `null` |
| `workspaces` | `getWorkspaces` | `SPARK_WorkspaceV2.Query.getWorkspacesByIdsV2({}, {ids: workspaceContext}, ctx)` |
| `participantDetails` | `getUserGroup` (Product/userGroupUtils) | UserGroup loader |

**Finding 🟡:** `getProduct` returns `null` when `parentId` doesn't start with `PID`. Confirm no other prefixes (template ids `PTID*`?) need handling.

**Federation note:** All cross-DGS refs (`product`, `workspaces`, `createdBy`, `updatedBy`, `businessPartners`) become entity-fetcher stubs in federation; only `access`, `currentUserPermissions`, and `participantDetails` stay native.

---

## C2 · `SPARK_BomMaterial_Unified` (3 fields) — CAT-2 · Small (1–2d)

```
libraryResourceId: m -> m.libraryResource?.id
libraryResource: getBomMaterial(material, args, ctx)   // 4-case dispatcher in bomUtils
materialLibraryUom: getMaterialLibraryUom(material, ctx)
```

**`getBomMaterial`** dispatcher (in `bomUtils.js`):
- TRIM → `getTrimMaterial` (trim batch loader + size + caption)
- WASH → `getWashMaterial` (JWT-curried wash loader)
- FABRIC → `getFabricMaterial` (elastic fabricSpecCombo search)
- HUB → `getHubMaterial` (JWT-curried material-hub loader)
- default → `null`

**`getMaterialLibraryUom`** — only resolves when `materialCategory.code === TRIM`; loads trim UoMs and finds by code.

---

## C3 · `SPARK_BomMaterialInterface.__resolveType` (17-case dispatcher) — CAT-1 + CAT-2 · Small (1–2d)

| Material code(s) | Concrete type |
|---|---|
| 4 (TRIM) | `SPARK_BomTrimMaterial` |
| 6 (WASH) | `SPARK_BomWashMaterial` |
| 2 (FABRIC) | `SPARK_BomFabricMaterial` |
| 15 (COMBINATION) | `SPARK_BomCombinationMaterial` |
| 16 (FABRIC_SPEC) | `SPARK_BomFabricSpecMaterial` |
| 10,11,12,13,14,17,18,19,20,21,22,23,24 (PACKAGING + others) | `SPARK_BomPackagingMaterial` |
| default (1 COMPONENT, 5 OTHER, 9 HUB) | `SPARK_BomMaterial` |

**Port:** Kotlin `@DgsTypeResolver(name="SPARK_BomMaterialInterface")` with same enum mapping. Preserve default branch (HUB falls through!) — `SPARK_BomMaterial` is the catch-all.

---

## C4 · `SPARK_BomMaterial` (8 fields) — CAT-2 · Medium (3–5d)

| Field | Implementation |
|---|---|
| `impressionDetails` | `material.impressions` (rename pass-through) |
| `libraryResourceId` | `material.libraryResource?.id ?? null` |
| `libraryResource` | `getMaterialHubResource(material, ctx)` — JWT-curried material-hub loader |
| `genericMaterialType` | Loads hub material → if `baseMaterial.relatedMaterialType` differs from `material.genericMaterialType`, return hub's value; else local |
| `countryOfOrigin` | `getCountryOfOrigin` → tags loader by `countryOfOriginIds` |
| `parentLibraryResourceId` | `material.parentLibraryResource?.id ?? null` |
| `origins` | Loads `getCodedOptions('Origin')` map; filters & enriches each origin row |
| `certifications` | Same pattern with `getCodedOptions('Certification')` |
| `weight` | `getMaterialWeight` (hub UoMs lookup) |
| `sizeUnitOfMeasure` | `getValueWithMaterialHubUom(size, sizeUomId, ctx)` |

**Finding 🟡:** `getMaterialHubResource` is invoked **twice** per material when both `libraryResource` and `genericMaterialType` are selected. DataLoader memoization saves the round-trip; preserve in DGS.
**Finding 🟢:** `getCodedOptions` is called once per `origins`/`certifications` resolution — cache at the materialHub loader level.

---

## C5 · `SPARK_BomPackagingMaterial` (2 fields) — CAT-2 · Small (<1d)

`impressionDetails` (rename `impressions`), `countryOfOrigin` (`getCountryOfOrigin`).

---

## C6 · `SPARK_BomFabricMaterial` (4 fields) — CAT-2 · Small (1–2d)

```
libraryResource: searchFabricSpecCombos.load({q:`id:${fscId}`, page:0, size:1}) -> content[0] || {id: fscId}
weight, countryOfOrigin, impressionDetails: as above
libraryResourceId: m.libraryResource?.id
```

---

## C7 · `SPARK_BomFabricSpecMaterial` (4 fields) — CAT-2 · Small (1–2d)

```
libraryResource: fabric.getSpecificationByID.load(fabricSpecId) || {id: fabricSpecId}
weight, countryOfOrigin, impressionDetails: as above
```

---

## C8 · `SPARK_BomCombinationMaterial` (4 fields) — CAT-2 · Small (1–2d)

```
libraryResource: combination.getById.load(combinationId) || {id: combinationId}
weight, countryOfOrigin
```

---

## C9 · `SPARK_BomTrimMaterial` (7 fields) — CAT-2 · Large (5–8d)

The largest material subtype.

| Field | Implementation |
|---|---|
| `impressionDetails` | `material.impressions` |
| `libraryResourceId` | `material.libraryResource?.id` |
| `libraryResource` | `trim.getTrimBatch.load(trimId)` (DataLoader; memoized below) |
| `materialLibraryUom` | Loads trim UoMs, finds by `materialLibraryUomId.toString()` |
| `sizeValue` | **Reloads trim** (memoized) → find matching trimSize by `librarySizeId` → call `getTrimSizeValue(trimType, trimSubType, matchingSize)` — 15-case TRIM_TYPES switch in `bomUtils.js` |
| `sizeCaption` | **Reloads trim** → `getBomSizeCaption(trim, matchingSize)` — 15-case TRIM_TYPES switch returning `{edit, view}` captions |
| `facilityName` | If `material.facilityName` already set → return it. Else reload trim → find supplier by `material.supplierId` → find facility by `material.facilityId` → `location.getLocationById(facilityId).load() → vmmFacility.name` |
| `weight`, `countryOfOrigin` | shared |

**Finding 🔵 perf:** Same `trim.getTrimBatch` loader hit 3× per material (libraryResource, sizeValue, sizeCaption). DataLoader memoization holds it to one REST call per request, but the in-Kotlin port should still consolidate into a single `TrimEnrichmentService.enrich(material)` call.

**Finding 🟡:** `materialLibraryUomId.toString()` comparison — backend returns string `code`, material has int `materialLibraryUomId`. Preserve type-coercion logic.

---

## C10 · `SPARK_BomWashMaterial` (4 fields) — CAT-2 · Small (1–2d)

```
libraryResource: JWT-curried wash.getWash(jwt).load(washId) || {id: washId}
weight, countryOfOrigin, impressionDetails
```

---

## C11 · `SPARK_BomImpressionDetailsInterface.__resolveType` — CAT-1 · Trivial (<1d)

| Impression type code | Concrete type |
|---|---|
| 603 (TRIM) | `SPARK_BomTrimLibraryImpressionDetails` |
| 605 (TRIM_ZIPPER) | `SPARK_BomTrimZipperLibraryImpressionDetails` |
| 604 (WASH) | `SPARK_BomWashLibraryImpressionDetails` |
| 602 (FABRIC) | `SPARK_BomFabricLibraryImpressionDetails` |
| default (601 BASE) | `SPARK_BomBaseImpressionDetails` |

---

## C12 · `SPARK_BomImpressionDetails_Unified` (6 fields) — CAT-2 · Medium (3–5d)

```
libraryResource:
  if (ctx.currentUser.internal) -> searchMaterialById('libraryResource', detail, ctx)
  else
    bomIds = args.ids   // !!! reads `args.ids` — only present if parent query selected with `ids` arg
    libraryResourceId = detail.libraryResource?.id
    if (!libraryResourceId) return null
    permissionJWT = await getUserPermissionsJWT(bomIds, ctx)
    materials = await search.searchMaterialsByProxyIds(jwt).load({q:`id:(${libraryResourceId})`, proxyIds: bomIds, page:0, size:1})
    return materials.content[0] || {id: libraryResourceId}
groundColor, textColor, sliderColor, tapeColor, teethColor: searchMaterialById(name, detail, ctx)
```

**Finding 🔴:** **`args.ids`** dependency — only set when this field is reached via a parent that has an `ids` argument. Same fragile pattern as `Product.samples` (Phase 2C product domain). In DGS port, pass `bomIds` as part of the resolver context (e.g. through `DgsDataFetchingEnvironment`).

**Finding 🟡:** `searchMaterialById` (top of file) loads each color material individually via `search.getMaterialByIds.load(id)`. 5 separate loader calls per impression detail.

---

## C13 · `SPARK_BomFabricLibraryImpressionDetails` (1 field) — CAT-2 · Small (1–2d)

Same internal/external branch as C12's `libraryResource`. Single field.

---

## C14 · `SPARK_BomTrimLibraryImpressionDetails` (3 fields) — CAT-2 · Small (1–2d)

Same `libraryResource` branch + `groundColor`, `textColor` via `searchMaterialById`.

---

## C15 · `SPARK_BomTrimZipperLibraryImpressionDetails` (3 fields) — CAT-2 · Small (<1d)

3 × `searchMaterialById` (sliderColor, tapeColor, teethColor).

---

## C16 · `SPARK_BomMaterialType.id` (1 synthetic field) — CAT-2 · Trivial (<0.5d)

```
id: detail -> `${detail.code}_${detail.description}`
```

---

## C17 · `SPARK_BomMaterialSearch.paging` (1 field) — CAT-2 · Trivial (<0.5d)

`paging: searchResults -> searchResults` (whole-object passthrough; paging fields are siblings on the result).

---

## C18 · `SPARK_BomMaterialSearchResult` (5 fields) — CAT-2 · Medium (3–5d)

| Field | Implementation |
|---|---|
| `description` | `detail.description \|\| detail.name` |
| `status` | `detail.status?.description \|\| detail.status` (handles both object + string shapes) |
| `fabricSpec` | If `type === 'fabric_spec_combo'` and `fabricSpecId` → `fabric.getSpecificationByID.load(fabricSpecId)` |
| `fabric` | If `type === 'combination'` and `fabricRecordHumanId` → JWT `fabric.getByID(jwt).load(humanId)` |
| `fabricId` | If `type === 'combination'` → `fabricRecordHumanId` |
| `relatedMaterials` | **2-branch (internal vs external) elastic search** by `relatedAssetIds`. External path requires JWT + `searchMaterialsByProxyIds`. ~30 lines. |

**Finding 🟡:** `relatedMaterials.proxyIds.push(detail.parentComboId)` **mutates the args array** before passing to elastic. Defensive-copy in port.

---

## Module-Level Helpers (Exported from `SPARK_Bom.js`)

> These belong in a Kotlin `BomMaterialHelpers` object during port. Phase 2D will track the lift.

| Helper | Purpose |
|---|---|
| `getMaterialWeight` | Joins material weight with hub UoM (fallback code 23 = grams) |
| `getValueWithMaterialHubUom` | Same shape for arbitrary value+uomCode |
| `getCodedOptions` | Loads materialHub coded-options into a `Map<code,description>` |
| `searchMaterialById` (file-scope helper) | Search wrapper for color/material refs |
| `getMaterialHubResource` (file-scope helper) | JWT-curried hub material loader |

---

## Cross-Cutting Findings

| # | Finding | Severity |
|---|---|---|
| 1 | C12 `SPARK_BomImpressionDetails_Unified.libraryResource` reads `args.ids` — fragile contract | 🔴 |
| 2 | C18 `relatedMaterials` mutates `proxyIds` array (`.push`) | 🟡 |
| 3 | C9 `SPARK_BomTrimMaterial` makes 3 DataLoader-memoized trim calls — consolidate in port | 🟢 |
| 4 | C4 `genericMaterialType` triggers second `getMaterialHubResource` call — memoized, but consolidate | 🟢 |
| 5 | Numerous "loader returns `{id}` if missing" fallbacks across 7 material subtypes — extract `withFallback(id)` helper | 🟢 |
| 6 | `SPARK_Bom` and `SPARK_Bom_Unified` have identical 9 field resolvers — single Kotlin impl | 🟢 |
| 7 | Coded-options lookups (`Origin`, `Certification`, hub UoMs) called per material — cache at session scope | 🟢 perf |
| 8 | `materialLibraryUomId` int vs string mismatch — preserve `.toString()` coercion | 🟡 |
| 9 | `getProduct` only follows `PID*`-prefixed parents — confirm no other prefixes | 🟡 |
| 10 | Heavy reliance on cross-DGS resolvers (vmm, materialHub, fabric, trim, wash, combination, tag, user-profile, workspace) — all become federation stubs | 🟢 |

---

## Effort Summary

| Block | Tier | Days |
|---|---|---|
| C1 (Bom + Bom_Unified × 9) | Medium | 3–5 |
| C2 (Material_Unified × 3) | Small | 1–2 |
| C3 (Material __resolveType) | Small | 1–2 |
| C4 (BomMaterial × 8) | Medium | 3–5 |
| C5 (PackagingMaterial × 2) | Small | <1 |
| C6 (FabricMaterial × 4) | Small | 1–2 |
| C7 (FabricSpecMaterial × 4) | Small | 1–2 |
| C8 (CombinationMaterial × 4) | Small | 1–2 |
| C9 (TrimMaterial × 7) | Large | 5–8 |
| C10 (WashMaterial × 4) | Small | 1–2 |
| C11 (Impression __resolveType) | Trivial | <1 |
| C12 (ImpressionDetails_Unified × 6) | Medium | 3–5 |
| C13–C15 (3 Impression subtypes) | Small | 2–4 |
| C16–C17 (Type + Search trivial) | Trivial | <1 |
| C18 (MaterialSearchResult × 5) | Medium | 3–5 |
| **Subtotal field resolvers** | | **26–47** |

---

**Phase Completed:** Phase 2C — Field Resolvers
**Output:** [output/bom/02-resolver-analysis-fields.md](output/bom/02-resolver-analysis-fields.md)
