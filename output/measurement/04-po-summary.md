# Measurement — PO Summary

> **Domain:** `measurement` (+ `measurementTemplate`) · **Target DGS:** `plm-measurement`
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

Executive-level summary of the `measurement` DGS migration scope. Companion to [04-stories.md](output/measurement/04-stories.md).

---

## TL;DR

| Metric | Value |
|---|---|
| Source files | 6 production (+ 1 cross-domain activity helper, out of scope) |
| Lines of code | 772 in-scope (+ 29 out of scope) |
| Stories | **40** across 6 phases |
| Estimated effort (buffered +20%) | **101–169 days** (~5–8 sprints) |
| Critical findings (🔴) | **4** |
| Domain size tier | **Mid-small** (larger than impression, smaller than bom) |

---

## What is Migrating

Two related sub-domains merged into one Kotlin DGS:

- **Measurement Sets** — central PLM measurement data attached to products. 7 queries, 9 mutations.
- **Measurement Templates** — reusable template library used by measurement sets. 2 queries, 3 mutations.
- **Sample Measurements** — sub-resource (per-sample row overrides) addressable by `sampleId`.

---

## Why This Matters

Measurement sets are a primary PLM artifact for Materials/Apparel teams. The DGS port:

1. **Closes 4 critical bugs** found during analysis:
   - JWT header corruption on `getSampleMeasurement` (sampleId sent as token)
   - Production usage of `purgeTestMeasurementTemplateData` endpoint
   - Brand-loader misuse on `MeasurementTemplate.brands` (likely returns null)
   - Non-atomic 2-step write on `updateMeasurement` (workspace + body)
2. **Cleans schema hygiene** — drops `Spark_MeasurementRowInput` casing anomaly, removes misplaced `@deprecated`, migrates `resourceId → parentId`.
3. **Refactors polymorphic input** for `updateMeasurementAccess` to a tagged shape.
4. **Adds federation entity contributions** (`Product.measurementSets`, `SampleV2.sampleMeasurement`) and reduces inline cross-domain lookups (Workspace, BusinessPartner, User, ACL, SizeTemplate, TightFit).
5. **Documents the JWT sentinel** (`SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY`) used for template mutations.

---

## Top Risks

| Risk | Stories | Mitigation |
|---|---|---|
| 🔴 `getSampleMeasurement` token-header corruption | Q07 | Ship S1; consider hot-fix in source first |
| 🔴 `deleteMeasurementTemplate` calls test-purge endpoint in prod | M11 | Confirm safe endpoint with backend before S4 |
| 🔴 `MeasurementTemplate.brands` awaits loader reference (likely null in prod) | C11 | Quick fix in source + DGS port |
| 🔴 `updateMeasurement` 2-step non-atomic write | M02 | Architecture decision: saga, idempotent retry, or reject |
| 🟡 Schema/UI fan-out from `Spark_` casing rename + `MeasurementAccessInput` refactor | F05, M01, M03 | Coordinate with UI; provide compatibility layer if needed |
| 🟡 Cross-domain JWT-omission pattern on `updateXxxComponentStatus` | M08 | Decide whether to add JWT here OR document backend enforcement (consistent w/ bom + product) |

---

## Dependencies on Sibling Subgraphs

Confirmed federation references (must be available at gateway):

| Subgraph | Entity / Field |
|---|---|
| plm-product | `Product` (parent of MeasurementSet) |
| plm-workspace | `Workspace` |
| plm-sample-v2 | `SampleV2` (updatedFromResource source) |
| plm-relationship | service call (not federation) for `getMeasurements(parentId)` |
| plm-user-profile | `UserProfileAttributes` (createdBy / updatedBy) |
| plm-team | `UserGroupParticipants` |
| plm-access-control | `AccessControl`, `ResourcePermissions` |
| plm-size-template | `SizeTemplate` |
| plm-tight-fit | `TightFit` (composite key `id + version`) |
| Hive → VMM | `BusinessPartner`, `Brand` |
| Hive → IG | `Division`, `Department` (template-only) |

---

## Effort by Phase

| Phase | Stories | Buffered days |
|---|---|---|
| F — Foundation | 8 | 16–27 |
| Q — Queries | 9 | 14–23 |
| M — Mutations | 11 | 34–56 |
| C — Field resolvers | 11 | 17–29 |
| E — Federation contributions | 3 | 6–11 |
| V — Validation & cutover | 6 | 14–23 |
| **Total** | **40** | **101–169** |

---

## Recommended Sequencing

| Sprint | Theme | Headline outcome |
|---|---|---|
| S1 | Scaffolding + critical bug fixes (F01–F05, Q07, C11) | Two hot bugs landed; DGS module deployable |
| S2 | All queries online (F06–F08, Q01–Q09 except Q07) | Read parity with spark-internal-graphql |
| S3 | Bulk mutations (M01, M03–M10) | Non-risky mutations cut over |
| S4 | Risky mutations + federation contributions (M02, M11, E01–E03) | Atomic write + safe delete + product/sampleV2 fields |
| S5 | Field resolvers (C01–C10) | Entity refs in place; cross-domain lookups removed |
| S6 | Validate + cutover (V01–V06) | Decommission source resolvers |

---

## Open Decisions for PO/Architecture

1. **Atomic-write policy** for `updateMeasurementSet` (saga vs reject vs compensating action).
2. **Schema rename coordination** with UI: `Measurements → MeasurementSet`, `resourceId → parentId`, `Spark_MeasurementRowInput → MeasurementRowInput`.
3. **Polymorphism** for `MeasurementSet.updatedFromResource` (union vs single type).
4. **JWT policy** for `updateMeasurementComponentStatus`, `deleteMeasurementTemplate` (cross-domain consistency).
5. **Template `delete` endpoint** — replace `purgeTestMeasurementTemplateData` before S4.
6. **`brandIds === -1` sentinel** meaning (all brands? none? legacy?).
7. **Master-data caching** — confirm TTL with backend for UoM + status endpoints.

---

## Out of Scope

- `resolvers/activityLogUtilities/measurementsActivityModifiedDataHelper.js` (29 lines) — owned by activity-log subsystem.
- 3 unused service methods in `MeasurementService` (`getMeasurementSetVersionsById`, `getMeasurementSetVersion`, standalone `manageWorkspaceAssociations`) — confirm cross-domain callers, then delete.

---

**Phase Completed:** Phase 4 — PO Summary
**Companion:** [04-stories.md](output/measurement/04-stories.md)
