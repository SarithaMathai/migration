# Phase 1: Schema Inventory — Measurement

> **Domain:** `measurement`
> **Target DGS:** `MeasurementService` → `plm-product` (co-located)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `schemas/SPARK_Measurement.graphqls` (219-line SDL) + `resolvers/product/SPARK_Measurement.js` + `services/product/Measurement.js`
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

Endpoint built in the service constructor (`services/product/Measurement.js:15-19`):
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

> **Scope note:** this domain covers `resolvers/SPARK_Measurement.js` only. `MeasurementTemplate` is a **separate
> sibling resolver/domain** — referenced here (`measurementTemplates` field) but not migrated by these stories.

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Measurement.graphqls` | 219 | the source SDL — 7 queries, 8 mutations, `Measurements`/`SampleMeasurementSet`/`UnitsOfMeasure`/row types, inputs |
| `resolvers/product/SPARK_Measurement.js` | 175 | 7 queries, 8 mutations, 2 type blocks (15 field resolvers) |
| `services/product/Measurement.js` | 181 | 18 REST methods (`measurements/v1` + master data) |
| `schemas/SPARK_MeasurementTemplate.graphqls` | 57 | sub-domain — 2 queries, 3 mutations, `MeasurementTemplate`/`MeasurementTemplatesPaged` |
| `resolvers/SPARK_MeasurementTemplate.js` | 87 | 2 queries, 3 mutations, 1 paged block, 1 type block (3 field resolvers) |
| `services/MeasurementTemplate.js` | 53 | 5 REST methods (`measurement/templates/v1`) |
| `schemas/SPARK_SizeTemplate.graphqls` | 137 | sub-domain — 3 queries, 2 mutations, `SizeTemplate` + row/grade/tolerance value types |
| `resolvers/product/SPARK_SizeTemplate.js` | 39 | 3 queries, 2 mutations, 1 type block (2 field resolvers) |
| `services/product/SizeTemplate.js` | 58 | 5 REST methods (`size_templates/v1` + master data: size_category, material_type) |
| `schemas/SPARK_TightFit.graphqls` | 40 | sub-domain — 2 queries, 2 mutations, `TightFit`/`TightFitsResponse` |
| `resolvers/product/SPARK_TightFit.js` | 51 | 2 queries, 2 mutations, 1 type block (5 field resolvers) |
| `services/product/TightFit.js` | 54 | 4 REST methods (`tightfit/v1`) |
| `schemas/SPARK_Sizes.graphqls` | 11 | sub-domain — 1 query (`searchSparkSizes`), `Sizes` value type |
| `resolvers/product/SPARK_Sizes.js` | 20 | 1 query, fans out to `NEXUS_Attributes` + `SPARK_Tag` |
| **Total** | **1,182** | no chunked reading |

Schema: **`schemas/SPARK_Measurement.graphqls` (219 lines)** — target schema in [be-03-schema.graphql](./be-03-schema.graphql) is translated from it (nullability/return-types from the SDL).

> **Scope correction (2026-07-19):** `MeasurementTemplate`, `SizeTemplate`, `TightFit`, and `Sizes` are
> **co-located sub-domains of `measurement`**, not external services — all four service classes build
> their endpoint from the SAME `enterprise_product_development_products` base as `MeasurementService`
> (`measurement/templates/v1`, `size_templates/v1`, `tightfit/v1` respectively; `Sizes` has no own
> endpoint, it only fans out to `NEXUS_Attributes`/`SPARK_Tag`), confirmed against
> `services/{MeasurementTemplate,product/SizeTemplate,product/TightFit}.js`. This corrects the previous
> "separate sibling resolver/domain" scope note below (superseded) and the `measurementTemplate`/
> `sizeTemplate`/`tightFit` rows in `domain-service-catalog.md`, which incorrectly tagged them EXT 🟡
> sibling-DGS. Their own operations (`getMeasurementTemplates`, `getSizeTemplates`, `getTightFits`,
> `searchSparkSizes`, and their mutations) are now first-class `measurement` stories — see
> [be-04-stories.md](./be-04-stories.md) Phase B/D/G.
>
> ~~**Scope note (superseded):** this domain covers `resolvers/SPARK_Measurement.js` only.
> `MeasurementTemplate` is a **separate sibling resolver/domain** — referenced here (`measurementTemplates`
> field) but not migrated by these stories.~~

## 3. Import Graph
```
resolvers/SPARK_Measurement.js
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
| `measurementTemplates` | `measurementTemplate` | MeasurementTemplate (co-located `measurement` sub-domain) | **internal** — own `MST-BE-B/D/G` stories | — |
| `sizeTemplate` | `sizeTemplate` | SizeTemplate (co-located `measurement` sub-domain) | **internal** — own `MST-BE-B/D/G` stories | — |
| `tightFitTemplate` | `tightFit` | TightFit (co-located `measurement` sub-domain) | **internal** — own `MST-BE-B/D/G` stories | — |
| `participantDetails` | userGroup | UserProfileService | sibling federation | 🔵 |
| `TightFit.divisions`/`.departments` | `ig` | Item Groups (IG) | Gateway stitch | 🔵 |
| `TightFit.brands`, `MeasurementTemplate.brands` | `vmm`/`brand` | VMM platform | Gateway stitch | 🔵 |
| `SizeTemplate.createdBy`/`.updatedBy`, `MeasurementTemplate.createdBy`/`.updatedBy` | `userAttributes` | UserProfileService | sibling federation | 🔵 |
| `searchSparkSizes` | (fan-out, no own loader key) | NEXUS_Attributes (platform) + `SPARK_Tag` (co-located) | Gateway stitch (NEXUS) + internal (Tag) | 🔵 |

## 5. Co-located Siblings
`product`, `bom`, `impression`, `packaging`, `productDetails`, plus the template sub-domains
(`measurementTemplate`, `sizeTemplate`, `tightFit`, `sizes`) — share `plm-product`. The template
sub-domains are folded into THIS domain's own stories (not a separate `output/analysis/` folder) since
they only exist to hydrate `Measurement` fields and have no independent frontend surface of their own
beyond that.

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
| Queries | 7 (measurement) + 8 (sub-domains: 2 measurementTemplate, 3 sizeTemplate, 2 tightFit, 1 sizes) = **15** |
| Mutations | 8 (measurement) + 7 (sub-domains: 3 measurementTemplate, 2 sizeTemplate, 2 tightFit) = **15** |
| Object types | 2 (`Measurement` set, `SampleMeasurementSet`) + 4 sub-domain owned types (`MeasurementTemplate`, `SizeTemplate`, `TightFit`, `Sizes`) + value types |
| Field resolvers | 15 (13 on Measurement, 2 on SampleMeasurementSet) + 10 sub-domain (3 MeasurementTemplate, 2 SizeTemplate, 5 TightFit) |
| Service methods | 18 (measurement) + 14 (sub-domains: 5 measurementTemplate, 5 sizeTemplate, 4 tightFit) = **32** |
| Cross-domain loader keys | 11 (+ accessControl context-only) — `measurementTemplate`/`sizeTemplate`/`tightFit` **reclassified internal** (2026-07-19), no longer counted as cross-domain |
| EXT calls | 2 🔴 · 3 🟡 · 3 🔵 (measurement) + 🔵 `ig`/`vmm`/`userAttributes`/NEXUS on the sub-domains' own field resolvers |
| Large files | 0 |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `measurement` · **Files:** 14 (1,182 lines: measurement schema/resolver/service 575 + measurementTemplate 197 + sizeTemplate 234 + tightFit 145 + sizes 31).
