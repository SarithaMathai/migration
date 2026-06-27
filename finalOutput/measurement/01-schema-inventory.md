# Phase 1: Schema Inventory — Measurement

> **Domain:** `measurement`
> **Target DGS:** `MeasurementService` → `plm-product` (co-located)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `code/schemas/SPARK_Measurement.txt` (219-line SDL) + `code/resolvers/product/SPARK_Measurement.txt` + `code/services/product/Measurement.txt`
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

Endpoint built in the service constructor (`services/product/Measurement.txt:15-19`):
```js
this.endpoint = `${endpoint}/enterprise_product_development_products/measurements/v1`
this.masterDataEndpoint = `${endpoint}/masterData`
// + /master_data/unit_of_measure , /master_data/thickness_uom
```
| Setting | Value |
|---|---|
| Loader key | `measurement` |
| Service class | `MeasurementService` |
| Backend base | `https://spark-product.dev.target.com` (repo `spark-product`) |
| Base path | `${endpoint}/enterprise_product_development_products/measurements/v1` |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | `plm-product` |

> **Scope note:** this domain covers `SPARK_Measurement.txt` only. `MeasurementTemplate` is a **separate
> sibling resolver/domain** — referenced here (`measurementTemplates` field) but not migrated by these stories.

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `code/schemas/SPARK_Measurement.txt` | 219 | the source SDL — 7 queries, 8 mutations, `Measurements`/`SampleMeasurementSet`/`UnitsOfMeasure`/row types, inputs |
| `code/resolvers/product/SPARK_Measurement.txt` | 175 | 7 queries, 8 mutations, 2 type blocks (15 field resolvers) |
| `code/services/product/Measurement.txt` | 181 | 18 REST methods (`measurements/v1` + master data) |
| **Total** | **575** | no chunked reading |

Schema: **`code/schemas/SPARK_Measurement.txt` (219 lines)** — target schema in [03-schema.graphql](./03-schema.graphql) is translated from it (nullability/return-types from the SDL).

## 3. Import Graph
```
SPARK_Measurement.txt
├── utils/commonLoaders            → getUserPermissionsJWT (ACL — context only)
├── utils/workspaceAssociationHelper → workspaceAssociationHelper, ValidWorkspaceAssociationTypes
├── utils/Product/userGroupUtils   → getUserGroup
├── utils/vmmUtils                 → loadBps
└── resolvers/SPARK_WorkspaceV2    → getWorkspacesByIdsV2
```

## 4. Cross-Domain Reference Table

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `getMeasurements` resource tree | `relationship` | RelationshipService | sibling federation | 🔴 |
| `getMeasurementsElastic` | `search` | SearchService (elastic) | sibling federation | 🔴 |
| `access`, `currentUserPermissions`, JWT | `accessControl` | AccessControlService | **context only — ACL ignored** | n/a |
| `businessPartners` | `vmm` (loadBps) | VMM platform | Gateway stitch | 🔵 |
| `createdBy`, `updatedBy` | `userAttributes` | UserProfileService | sibling federation | 🔵 |
| `product` | `product` | ProductService (same DGS) | **internal** | — |
| `workspaces`, `updateMeasurement` assoc | `workspaceV2` | WorkspaceService | sibling federation | 🟡 |
| `updatedFromResource` (sample) | `sampleV2` | SampleService | sibling federation | 🟡 |
| `measurementTemplates` | `measurementTemplate` | MeasurementTemplateService | sibling federation | 🟡 |
| `sizeTemplate` | `sizeTemplate` | SizeTemplateService | sibling federation | 🟡 |
| `tightFitTemplate` | `tightFit` | TightFitService | sibling federation | 🟡 |
| `participantDetails` | userGroup | UserProfileService | sibling federation | 🔵 |

## 5. Co-located Siblings
`product`, `bom`, `impression`, `packaging`, `productDetails`, plus the template siblings (`measurementTemplate`, `sizeTemplate`, `tightFit`) — share `plm-product`.

## 6. Hot Spots
1. **`getMeasurements`** (`:14-28`) — 2-hop: `relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0})` → ids → `getMeasurementByIds`; empty ids short-circuit; client-side `createdAt DESC` sort. 🔴 relationship.
2. **`updateMeasurement`** (`:50-67`) — 2-step write: optional `workspaceAssociationHelper` (throws on its own error) **then** body PUT. Less risky than BOM's 3-step but still non-atomic.
3. **`updateMeasurementAccess`** (`:68-71`) — polymorphic input: `systemTeamIds` **or** `systemTeamDto` (the service picks the body shape). Recommend a tagged input.
4. **`updatedFromResource`** (`:132-141`) — switch on `type` with only `'sample'` realized → `sampleV2.getSampleById`. Future polymorphism.
5. **JWT-curried** — most ops curry a capability token (ACL — context only).
6. **Client-side sort** in `getMeasurements` + `getMeasurementsElastic` — push to backend (PO decision).

## 7. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 7 |
| Mutations | 8 |
| Object types | 2 (`Measurement` set, `SampleMeasurementSet`) + value types |
| Field resolvers | 15 (13 on Measurement, 2 on SampleMeasurementSet) |
| Service methods | 18 |
| Cross-domain loader keys | 11 (+ accessControl context-only) |
| EXT calls | 2 🔴 · 6 🟡 · 3 🔵 |
| Large files | 0 |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `measurement` · **Files:** 3 (575 lines: schema 219 + resolver 175 + service 181).
