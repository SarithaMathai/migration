# Bom — Schema Inventory

> **Domain:** `bom`
> **Source:** `spark-internal-graphql/packages/data-source-spark`
> **Target DGS:** `plm-bom` (Kotlin / Netflix DGS / Spring Boot) — green-field
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## 1. Context Registration

| Setting | Value |
|---|---|
| Context key | `bom` |
| Service class | `BomService` (`services/product/Bom.js`) |
| Backend endpoint | `${config.endpoints.product}/enterprise_product_development_products/bom/v1` |
| Master data endpoint | `${config.endpoints.product}/masterData` |
| BOM material types endpoint | `${config.endpoints.product}/enterprise_product_development_products/master_data/bom_material_types` |
| Loader registration | `context.js` line 186: `bom: new Proxy({ ServiceClass: BomService, ... }, lazyLoadService)` |

---

## 2. File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Bom.graphql` | 988 | Schema (queries + mutations + 30+ types) |
| `resolvers/product/SPARK_Bom.js` | 735 | All BOM resolvers |
| `services/product/Bom.js` | 184 | REST client (16 methods) |
| `utils/bomUtils.js` | 325 | Trim sizes, captions, material library helpers |
| `resolvers/activityLogUtilities/bomActivityModifiedDataHelper.js` | 31 | Activity-log diff helper (cross-domain) |
| **Total** | **2,263** | |

---

## 3. Cross-Domain Sibling Subgraphs Referenced

| Sibling DGS | Purpose | Usage |
|---|---|---|
| `plm-product` | Parent Product entity | `SPARK_Bom.product` field resolver |
| `plm-workspace` | Workspace context | `SPARK_Bom.workspaces`, `manageBomWorkspaces` |
| `plm-team` / `plm-user-profile` | UserGroup participants, createdBy/updatedBy | `participantDetails`, `getUser` |
| `plm-tag` | Country of origin | `getCountryOfOrigin` |
| `plm-access-control` | ACL JWT + permissions | nearly every JWT-curried call |
| `plm-material-hub` | Hub materials (genericMaterialType, weight UoM) | `SPARK_BomMaterial.libraryResource`, `getMaterialWeight` |
| `plm-fabric` | Fabric spec + spec combo lookups | `SPARK_BomFabricMaterial`, `SPARK_BomFabricSpecMaterial` |
| `plm-trim` | Trim batch loader, trim sizes, UoMs | `SPARK_BomTrimMaterial.*` |
| `plm-wash` | Wash material loader | `SPARK_BomWashMaterial.libraryResource` |
| `plm-combination` | Combination material loader | `SPARK_BomCombinationMaterial.libraryResource` |
| `plm-search` (elastic) | Bom elastic, materials search, materials-by-proxy | 6 queries + several field resolvers |
| `plm-vmm` | VMM_BusinessPartner stubs, supplier lookups, location facility | Many field resolvers |
| `plm-product-component-status` | Status updates fan-out target | M6 `updateBomComponentStatus` |

---

## 4. External Platform References (🔵 gateway-stitched)

| Platform | Types referenced | Source |
|---|---|---|
| VMM | `VMM_BusinessPartner`, `getRelatedFabricSuppliersByMerchVendors`, `getRelatedSuppliersForMVs` | Resolver + vmmUtils |
| Material Hub | `getHubMaterial`, `getHubMaterialTypes`, `getHubUnitsOfMeasure`, `getHubCodedOptions` | Resolver |
| Tag | `getTags` | `getCountryOfOrigin` |

---

## 5. Resolver Block Locations (`SPARK_Bom.js`)

| Block | Approx lines | Description |
|---|---|---|
| `Query` | 80–225 | 12 queries |
| `Mutation` | 226–315 | 6 mutations |
| `SPARK_Bom` | 317–333 | 9 field resolvers (entity wrapper) |
| `SPARK_Bom_Unified` | 334–349 | Same 9 fields on unified shape |
| `SPARK_BomMaterial_Unified` | 350–357 | 3 fields (libraryResourceId/libraryResource/materialLibraryUom) |
| `SPARK_BomMaterialInterface` | 358–388 | `__resolveType` 17-case dispatcher |
| `SPARK_BomMaterial` | 389–422 | 8 fields (impressions/libraryResource/genericMaterialType/countryOfOrigin/parentLibraryResourceId/origins/certifications/weight/sizeUnitOfMeasure) |
| `SPARK_BomPackagingMaterial` | 423–427 | 2 fields |
| `SPARK_BomFabricMaterial` | 428–445 | 4 fields |
| `SPARK_BomFabricSpecMaterial` | 446–460 | 4 fields |
| `SPARK_BomCombinationMaterial` | 461–474 | 4 fields |
| `SPARK_BomTrimMaterial` | 475–545 | 7 fields (largest material subtype: sizeValue, sizeCaption, facilityName) |
| `SPARK_BomWashMaterial` | 546–560 | 4 fields |
| `SPARK_BomImpressionDetailsInterface` | 561–579 | `__resolveType` 4-case dispatcher |
| `SPARK_BomImpressionDetails_Unified` | 580–620 | 6 fields (libraryResource + 5 color refs) |
| `SPARK_BomFabricLibraryImpressionDetails` | 621–650 | 1 field |
| `SPARK_BomTrimLibraryImpressionDetails` | 651–680 | 3 fields |
| `SPARK_BomTrimZipperLibraryImpressionDetails` | 681–693 | 3 fields |
| `SPARK_BomMaterialType` | 694–697 | 1 field (synthetic id) |
| `SPARK_BomMaterialSearch` | 698–701 | 1 field (paging passthrough) |
| `SPARK_BomMaterialSearchResult` | 702–732 | 5 fields (description/status/fabricSpec/fabric/fabricId/relatedMaterials) |

---

## 6. Hot Spots

1. **`SPARK_BomMaterialInterface.__resolveType`** — 17 enum cases routing to 7 concrete material types. CAT-2 + CAT-1 union/interface schema work.
2. **`SPARK_BomTrimMaterial.sizeValue` + `sizeCaption` + `facilityName`** — each re-loads the same trim record via DataLoader (memoized) then runs `getTrimSizeValue`/`getBomSizeCaption` trim-type dispatchers from `bomUtils.js` (15+ TRIM_TYPES branches).
3. **`searchMaterialsBom`** — flattens `nestedSearchFilters` array into `nestedSearchFilters[i].field` query-string keys (fragile pattern).
4. **JWT-curried hot path** — 9 of 12 queries and 2 of 6 mutations require `getUserPermissionsJWT(ids, ctx)` before service call.
5. **`SPARK_BomImpressionDetails_Unified.libraryResource`** + 3 other `*ImpressionDetails` types — internal vs external branch with `searchMaterialsByProxyIds(permissionJWT)`. External uses ACL JWT, internal does not.
6. **`getBomMaterialTypes`** — merges REST bom material types with Material Hub types, synthesizing `code: 9, libraryLink: true, freeText: true` for each hub type.
7. **Re-export of internal constants** — `MATERIAL_CATEGORY_ID` is imported by `bomUtils.js` from resolver file. Circular import smell — flag for refactor in Phase 2D.
8. **`getMaterialWeight`/`getValueWithMaterialHubUom`/`getCodedOptions`** — module-level exported helpers in `SPARK_Bom.js` (should live in utils).

---

**Phase Completed:** Phase 1 — Schema Inventory
**Output:** [output/bom/01-schema-inventory.md](output/bom/01-schema-inventory.md)
