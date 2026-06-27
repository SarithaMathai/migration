# Measurement — Schema Inventory

> **Domain:** `measurement` (+ `measurementTemplate`) · **Target DGS:** `plm-measurement` (green-field, Kotlin / Netflix DGS)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## 1. Context Registration

| Setting | Value |
|---|---|
| Context keys | `measurement`, `measurementTemplate` |
| Service classes | `MeasurementService`, `MeasurementTemplateService` |
| Measurement endpoint | `${product}/enterprise_product_development_products/measurements/v1` |
| Template endpoint | `${product}/enterprise_product_development_products/measurement/templates/v1` |
| Master data | `${product}/masterData?name=MeasurementSetStatus` + UoM endpoints |
| Registration | `context.js` lines 183, 189 |

This domain has **two related sub-domains** (measurement sets + measurement templates) that share infrastructure but live in separate files. They are unified into one DGS (`plm-measurement`) per the [federation-patterns.md §10](fedMigrationScripts/reference/federation-patterns.md) co-location guidance.

---

## 2. File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Measurement.graphql` | 219 | Measurement sets schema |
| `schemas/SPARK_MeasurementTemplate.graphql` | 57 | Templates schema |
| `resolvers/product/SPARK_Measurement.js` | 175 | Measurement resolvers |
| `resolvers/SPARK_MeasurementTemplate.js` | 87 | Template resolvers |
| `services/product/Measurement.js` | 181 | Measurement REST (14 methods) |
| `services/MeasurementTemplate.js` | 53 | Template REST (5 methods) |
| `resolvers/activityLogUtilities/measurementsActivityModifiedDataHelper.js` | 29 | Activity-log diff helper (cross-domain, **out of scope**) |
| **Total** | **801** | |

---

## 3. Dependencies

| Sibling DGS / platform | Usage |
|---|---|
| `plm-product` | `Measurement.product` field (parent), elastic measurement search |
| `plm-workspace` | `Measurement.workspaces`, `manageWorkspaceAssociations` |
| `plm-user-profile` | createdBy / updatedBy |
| `plm-team` | UserGroup participants |
| `plm-access-control` | ACL JWT on 7 queries + 7 mutations + field resolvers |
| `plm-sample-v2` | `Measurement.updatedFromResource` (when sample-sourced) |
| `plm-relationship` | `getMeasurements` uses relationship tree (`findRelationships`) to discover measurement-set IDs from `resourceId` |
| `plm-size-template` | `Measurement.sizeTemplate` |
| `plm-tight-fit` | `Measurement.tightFitTemplate` |
| Hive Gateway → VMM | `VMM_BusinessPartner`, `VMM_Brand` |
| Hive Gateway → IG | `IG_Department`, `IG_Division` (template-only) |
| Elastic (`getMeasurementSets`) | `getMeasurementsElastic` |

---

## 4. Surface Summary

| | Measurement Sets | Templates |
|---|---|---|
| Queries | 7 | 2 |
| Mutations | 9 | 3 |
| Owned types | ~12 | ~3 |
| Inputs | ~9 | 2 |
| Field resolvers | 12 on `SPARK_Measurements`, 2 on `SPARK_SampleMeasurementSet` | 3 paging + 5 on `SPARK_MeasurementTemplate` |

---

## 5. Resolver Block Locations

### `SPARK_Measurement.js` (175 lines)

| Block | Approx lines | Description |
|---|---|---|
| `Query` | 9–39 | 7 queries |
| `Mutation` | 40–91 | 9 mutations |
| `SPARK_Measurements` | 93–166 | 12 fields (heavy: `measurementTemplates`, `sizeTemplate`, `tightFitTemplate`, `updatedFromResource` polymorphism) |
| `SPARK_SampleMeasurementSet` | 167–175 | 2 fields |

### `SPARK_MeasurementTemplate.js` (87 lines)

| Block | Approx lines | Description |
|---|---|---|
| `Query` | 7–22 | 2 queries (param flattening for arrays) |
| `Mutation` | 23–43 | 3 mutations (JWT uses sentinel constant `SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY`) |
| `SPARK_MeasurementTemplatesPaged` | 44–58 | 3 paging fields |
| `SPARK_MeasurementTemplate` | 60–87 | 5 fields (createdBy/updatedBy/departments/divisions/brands) |

---

## 6. Hot Spots / Flags

| # | Finding | Severity |
|---|---|---|
| 1 | `SPARK_Measurements.resourceId` declared `@deprecated(reason: "Use parentId")` — `parentId` is also in the type. Resolver only reads `resourceId`; field-resolver code still references `resourceId.indexOf('PID') === 0`. Confirm migration to `parentId` is complete | 🟡 |
| 2 | `getMeasurements` requires a `plm-relationship` tree walk (`findRelationships`) before fetching — couples measurement DGS to relationship service availability | 🟡 |
| 3 | `updateMeasurement` (3-step write: workspace association → body → permission), same pattern as bom `updateBom` and product `productBusinessPartnerActions` | 🔴 |
| 4 | `updateMeasurementAccess` accepts either `systemTeamIds` OR `systemTeamDto` — one or the other in the body. Polymorphic input | 🟡 |
| 5 | `updateMeasurementComponentStatus` (Mut 9) missing JWT — same pattern observed in bom M6 and product `updateBomComponentStatuses` | 🟡 |
| 6 | Template mutations use **hardcoded sentinel `SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY`** for ACL JWT seed — confirm value + intent | 🟡 |
| 7 | `MeasurementTemplateService.deleteTemplates` endpoint is `purgeTestMeasurementTemplateData` (test-data-purge path used in production?) | 🔴 |
| 8 | `MeasurementTemplateService.deleteTemplates` references `endpoint` (function arg) but the closure captures `endpoint` from constructor — works but fragile shadowing | 🟡 |
| 9 | `MeasurementTemplate.brands` resolver awaits the LOADER (`await ctx.loaders.brand.getBrand`) instead of awaiting the LOAD CALL — likely no-op or yields the loader itself | 🔴 |
| 10 | `getMeasurementTemplates` query takes `page: Int!` and `size: Int!` but resolver passes the entire `searchParams` object (no extra filterable args declared in schema). The array-join logic in the resolver fires on no fields | 🟡 |
| 11 | `MeasurementService` has 3 unused methods (`getMeasurementSetVersionsById`, `getMeasurementSetVersion`, `manageWorkspaceAssociations` as standalone) | 🟢 |
| 12 | `updatedFromResource` is polymorphic (`type: 'sample'` → fetch from sampleV2 loader) — schema-typed as `SPARK_SampleV2` but resolver only handles 'sample' (single case) | 🟢 |

---

**Phase Completed:** Phase 1 — Schema Inventory
**Output:** [output/measurement/01-schema-inventory.md](output/measurement/01-schema-inventory.md)
