# Phase 1: Schema Inventory — BOM

> **Domain:** `bom`
> **Target DGS:** `BomService` → `plm-product` (Kotlin / Netflix DGS / Spring Boot)
> **Pipeline Version:** 2.0
> **Generated:** 2026-06-26
> **Source of truth:** `code/schemas/SPARK_Bom.txt` (988-line SDL) + `code/resolvers/product/SPARK_Bom.txt` + `code/services/product/Bom.txt` + `code/utils/bomUtils.txt`
> **Depends on:** None (entry phase)
> **DGS Target Status:** Green-field (no existing DGS schema)

---

## 1. Context Registration

There is no `context.js` in the snapshot. The backend endpoint is built in the **service constructor**
(`code/services/product/Bom.txt:9-13`):

```js
constructor (endpoint, headers, logContext) {
  this.endpoint = `${endpoint}/enterprise_product_development_products/bom/v1`
  this.masterDataEndpoint = `${endpoint}/masterData`
  const bomMaterialTypeEndpoint = `${endpoint}/enterprise_product_development_products/master_data/bom_material_types`
}
```

| Setting | Value |
|---|---|
| Loader key | `bom` |
| Service class | `BomService` |
| Backend base (`${endpoint}`) | `https://spark-product.dev.target.com` (repo `spark-product`) |
| BOM base path | `${endpoint}/enterprise_product_development_products/bom/v1` |
| Master-data path | `${endpoint}/masterData` and `.../master_data/*` |
| Auth pattern | base `Authorization` header + per-call `SPARK-Capability-Token: {permissionJWT}` on ACL-scoped calls |
| Target DGS | `plm-product` (co-located with product/measurement/impression/packaging) |

---

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `code/schemas/SPARK_Bom.txt` | 988 | the source SDL — 13 queries, 6 mutations, `Bom`/`Bom_Unified`/material+impression interfaces, inputs |
| `code/resolvers/product/SPARK_Bom.txt` | 735 | All BOM resolvers: 13 queries, 6 mutations, 20 type blocks (incl. 2 `__resolveType`) + 3 module-level helpers |
| `code/services/product/Bom.txt` | 184 | REST client — 17 methods against `bom/v1` + master-data |
| `code/utils/bomUtils.txt` | 325 | Trim size/caption dispatchers (15 `TRIM_TYPES`), field-resolver helpers, material dispatcher |
| `code/resolvers/activityLogUtilities/bomActivityModifiedDataHelper.txt` | 31 | Activity-log diff helper (referenced cross-domain) |
| **Total** | **2,263** | No file > 1000 lines — no chunked reading required |

Schema: **`code/schemas/SPARK_Bom.txt` (988 lines)** — target schema in [03-schema.graphql](./03-schema.graphql) translated from it (nullability/return-types from the SDL).

## 3. Import Graph

```
SPARK_Bom.txt (resolver)
├── utils/commonLoaders            → getUserPermissionsJWT (ACL capability token)
├── utils/workspaceAssociationHelper → workspaceAssociationHelper, ValidWorkspaceAssociationTypes
├── utils/bomUtils                 → getTrimSizeValue, getBomSizeCaption, getBusinessPartners,
│                                     getCurrentUserPermissions, getCreatedBy, getProduct, getWorkspaces,
│                                     getUpdatedBy, getBomAccess, getMaterialLibraryUom, getBomMaterial,
│                                     getCountryOfOrigin
├── utils/Product/userGroupUtils   → getUserGroup
├── resolvers/SPARK_Combination    → searchFabricSpecCombos (EXT call, cross-resolver import)
├── resolvers/VMM_BusinessPartner  → getRelatedFabricSuppliersByMerchVendors (EXT)
├── utils/vmmUtils                 → getRelatedSuppliersForMVs (EXT)
├── config/businessPartner         → BusinessPartnerRole   ⚠️ config not in snapshot — see note
└── config/constants               → VMM_ROLE_IDS          ⚠️ config not in snapshot — see note

bomUtils.txt
├── utils/materialsConstants       → TRIM_SUB_TYPES, TRIM_TYPES
├── utils/commonLoaders            → getUserPermissionsJWT
├── resolvers/product/SPARK_Bom    → MATERIAL_CATEGORY_ID  ⚠️ circular import (resolver ↔ util)
├── resolvers/SPARK_WorkspaceV2    → getWorkspacesByIdsV2 (EXT)
├── resolvers/commonResolvers/Teams→ loadBusinessPartners
├── utils/Product/userGroupUtils   → getUserGroup
└── utils/userAttributesUtils      → getUser
```

> **Config note:** `config/businessPartner` and `config/constants` are imported but are **not present**
> in the snapshot. The values used (`BusinessPartnerRole.TRIM_SUPPLIER.code`, `VMM_ROLE_IDS.*`) are role
> ID constants — port them as Kotlin enums; confirm exact codes against the real config during A06.

## 4. Cross-Domain Reference Table

| Operation / Field | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `BomMaterial.libraryResource`, `getMaterialWeight`, `getBomMaterialTypes` | `materialHub` | MaterialHubService | sibling federation | 🟡 |
| `BomTrimMaterial.*`, `getMaterialLibraryUom` | `trim` | TrimService | sibling federation | 🟡 |
| `BomWashMaterial.libraryResource` | `wash` | WashService | sibling federation | 🟡 |
| `BomFabricSpecMaterial.libraryResource` | `fabric` | FabricService | sibling federation | 🟡 |
| `BomCombinationMaterial.libraryResource` | `combination` | CombinationService | sibling federation | 🟡 |
| `getBomElastic`, `searchMaterialsBom`, impression `libraryResource`, search-result fields | `search` | SearchService (elastic) | sibling federation | 🔴 |
| `access`, `currentUserPermissions`, `getUserPermissionsJWT` | `accessControl` | AccessControlService | sibling federation | 🔴 |
| `countryOfOrigin` | `tag` | TagService | sibling federation | 🔵 |
| `product` field | `product` | ProductService (same DGS) | **internal call** | — |
| `workspaces`, `manageBomWorkspaces`, `updateBom` workspace branch | `workspaceV2` | WorkspaceService | sibling federation | 🟡 |
| `searchMaterialsBom` supplier lookup, `getComboSupplierForBom`, `facilityName` | `vmm` / `location` | VMM platform | **Gateway stitch** | 🔵 |
| `participantDetails`, `createdBy`, `updatedBy` | userGroup / userAttributes | UserProfileService | sibling federation | 🔵 |

## 5. Co-located Siblings (share `plm-product`)
`product`, `measurement`, `impression`, `packaging`, `productDetails` — all build the same
`enterprise_product_development_products/...` base. Federation (CAT-4) stories may be shared.

## 6. Hot Spots (drive complexity)

1. **`SPARK_BomMaterialInterface.__resolveType`** (`:315-347`) — 21-case switch over `MATERIAL_CATEGORY_ID`
   routing to **7 concrete material types** (Trim/Wash/Fabric/Combination/FabricSpec/Packaging/Base).
   Needs `@DgsTypeResolver`; default → `SPARK_BomMaterial`. **+1 complexity** on every material field.
2. **`SPARK_BomImpressionDetailsInterface.__resolveType`** (`:517-532`) — 4-case + default impression type.
3. **Internal vs external user branch** — `SPARK_BomImpressionDetails_Unified.libraryResource` (`:533-555`)
   and 3 sibling impression types branch on `ctx.currentUser.internal`. External path uses
   `searchMaterialsByProxyIds(permissionJWT)`. **+1 complexity**; needs parity test per branch.
4. **JWT-curried hot path** — 9 of 13 queries and 3 of 6 mutations call `getUserPermissionsJWT(ids, ctx)`
   before the service call.
5. **`SPARK_BomTrimMaterial`** (`:426-502`) — largest material subtype: `sizeValue`/`sizeCaption` run the
   15-case `getTrimSizeValue`/`getBomSizeCaption` dispatchers from `bomUtils`; `facilityName` does a
   2-level supplier→facility→VMM-location lookup; 3 fields each re-load the same trim via `getTrimBatch`.
6. **`getBomMaterialTypes`** (`:112-130`) — merges REST bom types with Material Hub types, synthesizing
   `code: 9, libraryLink: true, freeText: true` per hub type.
7. **Circular import** — `bomUtils` imports `MATERIAL_CATEGORY_ID` from the resolver (`bomUtils.txt:6`).
   Move constants to a `BomConstants.kt`.
8. **Module-level helpers in the resolver** — `getMaterialWeight`/`getValueWithMaterialHubUom`/
   `getCodedOptions` (`:710-735`) belong in utils.
9. **Latent bug** — `getHubMaterial` (`bomUtils.txt:268-278`) calls `getUserPermissionsJWT` **without
   `await`** then passes the promise to the loader; other call sites `await` it. Fix on port.

## 7. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 13 |
| Mutations | 6 |
| Object types (resolver keys) | 18 |
| Interfaces (`__resolveType`) | 2 |
| Concrete material variants | 7 |
| Service methods | 17 |
| Utils functions used | ~20 |
| Cross-domain loader keys | 12 |
| EXT calls (RED/YELLOW/BLUE) | 2 🔴 · 6 🟡 · 4 🔵 (by loader key) |
| Large files (>1000 lines) | 0 |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `bom` · **Files Analyzed:** 5 (2,263 lines incl. 988-line SDL)
**Next:** Phase 2 — Resolver Dependency Analysis.
