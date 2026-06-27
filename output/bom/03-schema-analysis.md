# Bom — Federation Schema Analysis

> **Domain:** `bom` · **Schema:** [03-schema.graphql](output/bom/03-schema.graphql)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## 1. Type Naming Decisions

| Source name | Target name | Rationale |
|---|---|---|
| `SPARK_*` (all) | unprefixed | Per [03-schema-analysis.md product](output/product/03-schema-analysis.md) precedent. Bom owns its types. |
| `VMM_*` | kept | Platform stub (gateway-stitched) |
| `SPARK_Bom_Type` | `Bom_Type` | Kept underscore — distinct from `BomType` enum that may appear elsewhere |
| `SPARK_Bom_Unified` | `Bom_Unified` | Different projection of same entity |
| `SPARK_BomMaterial_Library_Unified` | `BomMaterial_Library_Unified` | Same |
| `MaterialOrigin` (input type with shape `{origin: Int, percentage: Float}`) | output `MaterialOriginV2 {origin: CodeDescription, percentage: Float}` | Source returns enriched shape after looking up `getCodedOptions('Origin')`. Disambiguate from upstream `MaterialOrigin` reference. |

---

## 2. Gap Analysis

### 2.1 Queries

| # | Source query | Status | Notes |
|---|---|---|---|
| Q1 | getBomByIds | 🔜 | |
| Q2 | getBomDataV2 | 🔜 | Same backend call; smaller return shape |
| Q3 | getBomStatus | 🔜 | Cacheable master data |
| Q4 | getBomByParentId | 🔜 | |
| Q5 | getBomMaterialTypes | 🔜 | Merges REST + materialHub types |
| Q6 | getBomPackagingMaterialTypes | 🔜 | Cacheable |
| Q7 | getBomPackagingSubstrates | 🔜 | Cacheable |
| Q8 | getBomPackagingUnitOfMeasure | 🔜 | Cacheable |
| Q9 | getBomElastic | 🔜 | |
| Q10 | searchMaterialsBom | 🔜 | Nested filter flattening preserved |
| Q11 | getValidTrimSuppliersForBom | 🔜 | VMM passthrough |
| Q12 | getValidRawMaterialSuppliersForBom | 🔜 | VMM passthrough |
| Q13 | getComboSupplierForBom | 🔜 | Cross-domain call into Combination |

**Total:** 0✅ / 13🔜 / 0⏭

### 2.2 Mutations

| # | Source mutation | Status | Notes |
|---|---|---|---|
| M1 | addBom | 🔜 | |
| M2 | updateBom | 🔜 | 3-step non-atomic write — saga decision required |
| M3 | manageBomWorkspaces | 🔜 | |
| M4 | lockBom | 🔜 | |
| M5 | unlockBom | 🔜 | |
| M6 | updateBomComponentStatus | 🔜 | Missing JWT — confirm |

**Total:** 0✅ / 6🔜 / 0⏭

### 2.3 Types

| Bucket | Count |
|---|---|
| Owned entities (`@key`) | `Bom`, `Bom_Unified` (2) |
| Owned value types | ~32 (materials, impressions, paging, search results, etc.) |
| Input types | 14 |
| External stubs — platform | 1 (`VMM_BusinessPartner`) |
| External stubs — co-located DGSs | 22 (HubMaterial, Material, FabricSpecCombo, FabricSpecification, Fabric, Trim, Wash, Combination, BaseMaterial, TrimColorRow/FinishRow/Size/Supplier, MaterialOrigin, UnitOfMeasure, Product, WorkspaceV2, UserProfileAttributes, Tag, UserGroup_Participants, ResourcePermissions, AccessControl, ProductComponentStatus, MaterialsPaged) |
| `@shareable` value types | `CodeDescription`, `UnitsOfMeasure`, `Paging`, `ValueWithUnit` |
| Interfaces | `BomMaterialInterface`, `BomImpressionDetailsInterface` |

---

## 3. Material Polymorphism — `@DgsTypeResolver` mapping

| `materialCategory.code` | Concrete DGS type |
|---|---|
| 4 (TRIM) | `BomTrimMaterial` |
| 6 (WASH) | `BomWashMaterial` |
| 2 (FABRIC) | `BomFabricMaterial` |
| 15 (COMBINATION) | `BomCombinationMaterial` |
| 16 (FABRIC_SPEC) | `BomFabricSpecMaterial` |
| 10/11/12/13/14/17/18/19/20/21/22/23/24 (PACKAGING + others) | `BomPackagingMaterial` |
| default (1 COMPONENT, 5 OTHER, 9 HUB, others) | `BomMaterial` |

Impression dispatcher (5-case):
| `impression.type` | Concrete DGS type |
|---|---|
| 603 (TRIM) | `BomTrimLibraryImpressionDetails` |
| 605 (TRIM_ZIPPER) | `BomTrimZipperLibraryImpressionDetails` |
| 604 (WASH) | `BomWashLibraryImpressionDetails` |
| 602 (FABRIC) | `BomFabricLibraryImpressionDetails` |
| default (601 BASE) | `BomBaseImpressionDetails` |

---

## 4. Federation Contributions

### 4.1 Bom contributes to Product entity (sibling subgraph extension)

Per [federation-patterns.md §9](fedMigrationScripts/reference/federation-patterns.md) (multi-subgraph contributions to a shared entity):

```graphql
extend type Product @key(fields: "id") {
  id: ID! @external
  productBoms(includeAttachments: Boolean): [Bom]
  boms(types: [Int]): [Bom]
  packagingBoms: [Bom]
}
```

These three field resolvers are currently defined in the **product** subgraph's `SPARK_Product.js` and call `ctx.loaders.bom.getActiveBomsByProductId(...)`. After migration, the bom DGS owns the entity-extension. This becomes Phase F story **F01** in `04-stories.md` and is **BLOCKED-BY** product domain Phase 3 (publication of `Product @key`).

### 4.2 Bom contributes to TechPack `ResourcesCount` composite-key entity

Per [federation-patterns.md §9](fedMigrationScripts/reference/federation-patterns.md) — `bomsCount` field on the `ResourcesCount @key(fields: "productId partnerId")` entity owned by the product domain.

```graphql
extend type ResourcesCount @key(fields: "productId partnerId") {
  productId: ID! @external
  partnerId: ID! @external
  bomsCount: Int
}
```

This becomes story **F02** (BLOCKED-BY product domain F01–F08 TechPack stub completion).

### 4.3 Bom does NOT own a `Bom` entity extension from any other subgraph

No external subgraph currently contributes fields to `Bom`. Future material-hub or attachment integration could change this — flagged as open question.

---

## 5. Risks

| # | Risk | Severity |
|---|---|---|
| 1 | `updateBom` (M2) 3-step write atomicity (workspace → body → permissions) | 🔴 |
| 2 | `SPARK_BomImpressionDetails_Unified.libraryResource` reads `args.ids` — contract leak | 🔴 |
| 3 | Material-hub / trim / wash / fabric / combination cross-DGS dependencies — 5 sibling domains must federate before B can fully retire stubs | 🟡 |
| 4 | `getHubMaterial` missing `await` before promise-passing — latent bug | 🟡 |
| 5 | `updateBomComponentStatus` missing JWT vs all other writes | 🟡 |
| 6 | Q10 nested-filter flattening fragility | 🟡 |
| 7 | Circular import `bomUtils.js ↔ SPARK_Bom.js` for `MATERIAL_CATEGORY_ID` constant | 🟡 |
| 8 | `Bom` and `Bom_Unified` duplicate ~80% of field resolvers — refactor opportunity | 🟢 |
| 9 | Q13 cross-resolver call into `SPARK_Combination` couples migration order | 🟡 |
| 10 | Polymorphic material types require 7 separate Kotlin classes + a type resolver — ensure schema check on every PR | 🟡 |

---

## 6. Open Questions for PO / Architecture

1. Should `Bom_Unified` survive as a separate type, or be replaced by `@DgsData` field selection on `Bom`?
2. Does `parentId` only ever start with `PID`? (Affects `getProduct` field resolver — confirmed no template-prefixes etc.)
3. Is `updateBomComponentStatus` (M6) JWT-less by design or oversight?
4. `M2` rollback strategy: saga, compensation log, or accept best-effort?
5. Are unused service methods (`getActiveBomsByProductIdAndBomType`, `getBomVersionsById`, `getBomVersion`) needed by cross-domain callers? Confirm before deleting.
6. Material-hub / trim / wash / fabric / combination — what is the federation rollout order? bom needs at least stubs published before its field resolvers can resolve full types via gateway.

---

**Phase Completed:** Phase 3 — Federation Schema Derivation
**Outputs:** [03-schema.graphql](output/bom/03-schema.graphql), [03-schema-analysis.md](output/bom/03-schema-analysis.md)
