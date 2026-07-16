# Phase 3: Federation Schema Analysis — BOM

> **Domain:** `bom`
> **Target DGS:** `BomService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap summary: **0 ✅ | 19 🔜 | 0 ⏭ — 19 operations**

This is the design view and the **Confluence "approach" page** for BOM. The target schema is translated
from the source SDL (`schemas/SPARK_Bom.graphqls`), verified against the resolver.

---

## 1. Type Classification

| Bucket | Count | Examples |
|--------|-------|----------|
| Owned entities (`@key(fields:"id")`) | 2 | `Bom`, `Bom_Unified` |
| Owned value types | ~32 | 7 material types, 5 impression types, `BomMaterialType`, `BomMaterialSearchResult`, `BomSizeCaption`, `MaterialOriginV2`, `BomComboSupplier`, … |
| Interfaces | 2 | `BomMaterialInterface` (7 impls), `BomImpressionDetailsInterface` (5 impls) |
| `@shareable` value types | 4 | `CodeDescription`, `UnitsOfMeasure`, `Paging`, `ValueWithUnit` |
| External stub — platform (🔵 gateway) | 1 | `VMM_BusinessPartner` |
| External stub — sibling DGS (🔜) | 22 | `Product`, `WorkspaceV2`, `Tag`, `HubMaterialInterface`, `Material`, `Trim`, `Wash`, `Fabric`, `FabricSpecCombo`, `FabricSpecification`, `Combination`, `BaseMaterial`, `MaterialsPaged`, `TrimColorRow/FinishRow/Size/Supplier`, `MaterialOrigin`, `UnitOfMeasure`, `UserProfileAttributes`, `UserGroup_Participants`, `ResourcePermissions`, `AccessControl`, `ProductComponentStatus` |
| Input types | 16 | `BomInput`, `UpdateBomInput`, `BomMaterialInput`, `BomImpressionDetailsInput`, … |
| Enums | 1 | `SortDirection` |

## 2. Polymorphism — `@DgsTypeResolver` mappings (preserve exactly)

**`BomMaterialInterface`** keyed on `materialCategory.code`:

| Code(s) | Concrete type |
|---|---|
| 4 (TRIM) | `BomTrimMaterial` |
| 6 (WASH) | `BomWashMaterial` |
| 2 (FABRIC) | `BomFabricMaterial` |
| 15 (COMBINATION) | `BomCombinationMaterial` |
| 16 (FABRIC_SPEC) | `BomFabricSpecMaterial` |
| 10,11,12,13,14,17,18,19,20,21,22,23,24 (PACKAGING + others) | `BomPackagingMaterial` |
| **default (1 COMPONENT, 5 OTHER, 9 HUB)** | `BomMaterial` |

**`BomImpressionDetailsInterface`** keyed on `type`: 603→Trim, 605→TrimZipper, 604→Wash, 602→Fabric, default 601→Base.

> **Risk:** 7 Kotlin material classes + a type resolver; every new schema field must be added to the
> interface and all impls. Enforce a schema-conformance check in CI (story G-tests).

## 3. Client Contract Verification

- All 13 queries and 6 mutations are **preserved** (`0 ✅ | 19 🔜 | 0 ⏭`).
- No operation is dropped or renamed.
- `SPARK_` prefixes are removed on owned types (`SPARK_Bom` → `Bom`); `VMM_` kept (platform stub).
- `Bom_Unified` is retained as a smaller projection (PO decision: keep vs. replace with field selection).

## 4. Federation Boundaries

> **Monorepo:** `plm-product` is one subgraph hosting `product`, `bom`, `measurement`, `impression`,
> `packaging`, `productDetails`, … — so references **among these are internal types, not federation.**
> See [reference-federation-patterns.md §0](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

- **BOM owns** `Bom`, `Bom_Unified`, all material/impression value types (within the `plm-product` subgraph).
- **Internal (same subgraph — NOT federation stubs):** `Product`, `ProductComponentStatus`. The `Bom.product`
  field is an internal `@DgsData` call to `ProductService` in the same JVM. These need **no** `@extends @external`.
- **External (true federation stubs, `@extends @external`):** `WorkspaceV2` (workspace DGS),
- `UserProfileAttributes`/`UserGroup_Participants` (user-profile), `Tag` (tag), `AccessControl`/ `ResourcePermissions` (access-control — *also ACL-context-only*), and the **material DGSs** — `HubMaterial`/`Material`, `Trim`, `Wash`, `Fabric`/`FabricSpecCombo`/`FabricSpecification`, `Combination`, `BaseMaterial`, `MaterialsPaged`, `TrimColorRow/FinishRow/Size/Supplier`, `MaterialOrigin`, `UnitOfMeasure` — plus the platform `VMM_BusinessPartner`.
- These resolve via the Hive Gateway; BOM emits only the `@key`.
- **BOM contributes back to `Product` and `ResourcesCount` — but those are co-located**, so these are
  **internal field resolvers in the same subgraph**, not cross-subgraph entity extensions:
  - `Product.productBoms` / `boms` / `packagingBoms` → internal `@DgsData` calling `bomService` (F-01).
  - `ResourcesCount.bomsCount` → internal `@DgsData` (F-02). The TechPack `ResourcesCount` type is owned by
- `product` in the same subgraph; only its *externally*-owned fields (attachments/discussions/etc.) need real federation.
- **Neither F-01 nor F-02 is gateway-federated or blocked by a separate deployment** — they just depend on the `Product`/`ResourcesCount` types existing in the merged schema.

## 5. Migration Approach  *(Confluence approach page)*

**Recommended sequence — facade-free, sibling-stub-first:**

1. **Phase A (Foundation):** schema skeleton, owned types, 23 external stubs, the two `@DgsTypeResolver`s,
   and the `BomService` Kotlin port. No ACL plumbing (ACL is ignored in implementation — §7).
2. **Phase B (Core reads):** the 8 read queries, one per story. 4 master-data queries become `@Cacheable`.
   These unblock the UI's read paths first.
3. **Phase C (Search/listing):** elastic + supplier lookups. `searchMaterialsBom` keeps the nested-filter
   flatten unless backend accepts a structured DTO (PO decision C-02).
4. **Phase D (Mutations):** the 4 simple writes (add/lock/unlock/component-status).
5. **Phase E (Complex):** `updateBom` — the one genuinely hard story (3-step non-atomic write). Pick a
   rollback strategy (saga / compensation log / best-effort) before starting.
6. **Phase G (Field resolvers):** one story per type block. Sibling-DGS fields resolve as federated
   entity references once those subgraphs publish stubs; until then they return `{id}` stubs.
7. **Phase F (internal contributions):** `Product.{productBoms,boms,packagingBoms}` and
- `ResourcesCount.bomsCount` are **internal field resolvers** (same `plm-product` subgraph), not gateway federation.
- They depend on the `Product`/`ResourcesCount` types existing but are **not** blocked by a separate deployment.
- BOM can ship and serve its own reads/writes before they land.

**Cross-domain dependency (real federation):** BOM's **material** field resolvers depend on the separate
- material-hub/trim/wash/fabric/combination **DGS subgraphs** being stubbed in the gateway.
- Confirm federation rollout order (PO decision).
- The `Product`/co-located references are internal and need no such sequencing.

## 6. Risks & Recommendations

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| `updateBom` 3-step non-atomic write leaves bom/workspace/ACL inconsistent | Medium | High | Choose saga/compensation/best-effort before E-01 | Tech Lead |
| `BomImpressionDetails_Unified.libraryResource` reads `args.ids` (fragile contract) | Medium | Medium | Pass `bomIds` via DGS local context, not field args (G-10) | Backend Eng |
| 7-variant polymorphism drifts as fields are added | Medium | Medium | CI schema-conformance check across all impls | Backend Eng |
| Sibling material subgraphs not yet federated → material fields return stubs | High | Medium | Sequence material-hub/trim/wash/fabric/combination stubs first | Platform |
| Latent bugs (`getHubMaterial` missing await; `getFabricMaterial` null-guard; array mutations) | Medium | Low | Fix on port; add unit tests | Backend Eng |
| `updateBomComponentStatus` missing JWT vs other writes | Low | Low | Confirm backend enforces ACL server-side (context only) | PO |

## 7. ACL Handling (decision)

- The current gateway calls `getUserPermissionsJWT` to obtain a **capability token** for resource-scoped calls (most reads/writes of a specific bom, plus material-hub/wash lookups).
- **Per stakeholder decision, ACL is ignored in the DGS implementation** — there is **no ACL plumbing story**.
- Each affected operation carries a one-line note explaining *why* ACL is used today (the backend authorizes per-resource access), for reviewer context only.

## 8. Open Questions for Product Owner
1. Keep `Bom_Unified` as a type, or replace with field selection on `Bom`?
2. Does `parentId` only ever start with `PID`? (affects `Bom.product`)
3. `updateBomComponentStatus` JWT-less — backend-enforced or gap?
4. `updateBom` rollback strategy?
5. Are unused service methods (`getActiveBomsByProductIdAndBomType`, `getBomVersionsById`, `getBomVersion`) called cross-domain?
6. Federation rollout order for the 5 sibling material domains?

---
**Phase Completed:** Phase 3 — Schema Derivation · **Domain:** `bom` · **Next:** Phase 4 — Stories.
