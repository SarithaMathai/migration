# Measurement — Migration Stories

> **Domain:** `measurement` (+ `measurementTemplate`) · **Target DGS:** `plm-measurement`
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

Story IDs: `SPARK-MEAS-{Phase}{NN}`.
Severity: 🔴 critical · 🟡 enrichment / findings · 🔵 platform · 🟢 perf / trivial.
Complexity per [USAGE.md §7](fedMigrationScripts/USAGE.md): Trivial (<1d) · Small (1–2d) · Medium (3–5d) · Large (5–8d) · X-Large (8–13d). +20% buffer applied per-phase.

---

## Phase F — Foundation (DGS scaffolding)

| ID | Title | Severity | Complexity |
|---|---|---|---|
| **SPARK-MEAS-F01** | Bootstrap `plm-measurement` Kotlin DGS module · Medium (3–5d) | 🔵 | M |
| **SPARK-MEAS-F02** | Wire HTTP client for `enterprise_product_development_products/measurements/v1` + `/measurement/templates/v1` + master-data endpoints · Small (1–2d) | 🔵 | S |
| **SPARK-MEAS-F03** | Port `deepToCamelCase` / `deepToSnakeCase` converters or use Jackson naming strategy · Small (1–2d) | 🔵 | S |
| **SPARK-MEAS-F04** | Port ACL JWT helper (`getUserPermissionsJWT`) — sentinel-aware (handle `SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY` literal) · Small (1–2d) | 🔵 | S |
| **SPARK-MEAS-F05** | Add federation v2.3 directives + Hive Gateway composition wiring · Small (1–2d) | 🔵 | S |
| **SPARK-MEAS-F06** | Configure relationship-service client (for `getMeasurements` parentId resolution) · Small (1–2d) | 🔵 | S |
| **SPARK-MEAS-F07** | DataLoader infra: BatchLoaders for `measurementSetsByIds`, `measurementTemplatesByIds`, `unitsOfMeasure` · Medium (3–5d) | 🔵 | M |
| **SPARK-MEAS-F08** | Elastic search client for `getMeasurementSetsElastic` · Small (1–2d) | 🔵 | S |

**Phase F raw 13–22d → buffered 16–27d**

---

## Phase Q — Query Resolvers

| ID | Title | Severity | Complexity | Blocks |
|---|---|---|---|---|
| **SPARK-MEAS-Q01** | `measurementSetsByIds` (ports `getMeasurementByIds`) · Small (1–2d) | — | S | F02, F04, F07 |
| **SPARK-MEAS-Q02** | `measurementSets(parentId)` — relationship-tree pre-walk + ACL JWT + client-side sort moved to backend · Medium (3–5d) | 🟡 | M | F06, Q01 |
| **SPARK-MEAS-Q03** | `measurementSetsElastic(parentId)` — sanitize `parentId` interpolation (injection-risk fix) · Small (1–2d) | 🟡 | S | F08 |
| **SPARK-MEAS-Q04** | `unitsOfMeasure(ids)` + caching · Small (<1d) | 🟢 | T | F02 |
| **SPARK-MEAS-Q05** | `thicknessUnitsOfMeasure` + caching · Small (<1d) | 🟢 | T | F02 |
| **SPARK-MEAS-Q06** | `measurementSetStatuses` + caching · Small (<1d) | 🟢 | T | F02 |
| **SPARK-MEAS-Q07** | `sampleMeasurement(sampleId)` — **fix latent bug**: ensure JWT passed correctly to service · Medium (3–5d) | 🔴 | M | F04 |
| **SPARK-MEAS-Q08** | `measurementTemplates(page, size)` — remove dead array-join code or add missing filter args (PO decision) · Small (1–2d) | 🟡 | S | F02 |
| **SPARK-MEAS-Q09** | `measurementTemplatesByIds(ids)` · Small (<1d) | — | T | F02 |

**Phase Q raw 11–19d → buffered 14–23d**

---

## Phase M — Mutation Resolvers

| ID | Title | Severity | Complexity | Blocks |
|---|---|---|---|---|
| **SPARK-MEAS-M01** | `addMeasurementSet` — typed error mapping replaces `validationErrors \|\| message` sniff · Medium (3–5d) | 🟡 | M | F02 |
| **SPARK-MEAS-M02** | `updateMeasurementSet` — atomic strategy for workspace-association + body write (decide saga vs reject) · Large (5–8d) | 🔴 | L | M01, F04 |
| **SPARK-MEAS-M03** | `updateMeasurementSetAccess` with tagged `MeasurementAccessInput` (refactor polymorphic body) · Medium (3–5d) | 🟡 | M | F04 |
| **SPARK-MEAS-M04** | `lockMeasurementSet` · Small (<1d) | — | T | F04 |
| **SPARK-MEAS-M05** | `unlockMeasurementSet` · Small (<1d) | — | T | F04 |
| **SPARK-MEAS-M06** | `putSampleMeasurementSet` — multi-resource ACL seed (measurementSetId + sampleId) · Medium (3–5d) | 🟡 | M | F04 |
| **SPARK-MEAS-M07** | `deleteSampleMeasurementSet` — return shape upgrade (`String → SampleMeasurementSet`) · Small (1–2d) | 🟢 | S | F04 |
| **SPARK-MEAS-M08** | `updateMeasurementComponentStatus` — **add JWT** (closes cross-domain finding shared with bom/product) · Small (1–2d) | 🟡 | S | F04 |
| **SPARK-MEAS-M09** | `addMeasurementTemplate` — clarify `SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY` sentinel · Medium (3–5d) | 🟡 | M | F04 |
| **SPARK-MEAS-M10** | `updateMeasurementTemplate` — same sentinel concern as M09 · Medium (3–5d) | 🟡 | M | M09 |
| **SPARK-MEAS-M11** | `deleteMeasurementTemplate` — **replace `purgeTestMeasurementTemplateData` endpoint** with production-safe delete; add JWT; fix closure shadowing · Medium (3–5d) | 🔴 | M | F04 |

**Phase M raw 28–46d → buffered 34–56d**

---

## Phase C — Field Resolvers

| ID | Title | Severity | Complexity | Blocks |
|---|---|---|---|---|
| **SPARK-MEAS-C01** | `MeasurementSet.access` + `currentUserPermissions` via federation entity refs · Small (1–2d) | — | S | F05 |
| **SPARK-MEAS-C02** | `MeasurementSet.product` via federation; remove inline lookup; migrate to `parentId` (away from deprecated `resourceId`) · Small (1–2d) | 🟡 | S | F05, Q01 |
| **SPARK-MEAS-C03** | `MeasurementSet.workspaces / businessPartners / createdBy / updatedBy / participantDetails` via federation references · Medium (3–5d) | — | M | F05 |
| **SPARK-MEAS-C04** | `MeasurementSet.measurementTemplates` (same-subgraph fetch) · Small (1–2d) | — | S | Q09 |
| **SPARK-MEAS-C05** | `MeasurementSet.sizeTemplate` + `tightFitTemplate` via federation (composite `@key id version` for TightFit) · Small (1–2d) | — | S | F05 |
| **SPARK-MEAS-C06** | `MeasurementSet.updatedFromResource` — polymorphism handling (currently only `'sample'` case) · Small (1–2d) | 🟡 | S | F05 |
| **SPARK-MEAS-C07** | `MeasurementSet.status` synthetic (statusId + statusName projection) · Small (<1d) | 🟢 | T | — |
| **SPARK-MEAS-C08** | `SampleMeasurementSet.createdBy` + synthetic `measurementSizeId` · Small (<1d) | 🟢 | T | F05 |
| **SPARK-MEAS-C09** | `MeasurementTemplatesPaged` paging/content/pageable projections · Small (<1d) | 🟢 | T | — |
| **SPARK-MEAS-C10** | `MeasurementTemplate.createdBy / updatedBy / departments / divisions` via federation; preserve `loadManyIncludeEmptyResponse` partial-results tolerance · Medium (3–5d) | — | M | F05 |
| **SPARK-MEAS-C11** | `MeasurementTemplate.brands` — **fix `await ctx.loaders.brand.getBrand` latent bug** (awaiting loader reference); clarify `brandIds !== -1` sentinel · Medium (3–5d) | 🔴 | M | F05 |

**Phase C raw 14–24d → buffered 17–29d**

---

## Phase E — Federation Contributions

| ID | Title | Severity | Complexity | Blocks |
|---|---|---|---|---|
| **SPARK-MEAS-E01** | Extend `Product` with `measurementSets(...)` field; replaces `getMeasurements(resourceId)` from product subgraph's perspective · Medium (3–5d) | 🔵 | M | Q02 |
| **SPARK-MEAS-E02** | Extend `SampleV2` with `sampleMeasurement` field · Small (1–2d) | 🔵 | S | Q07 |
| **SPARK-MEAS-E03** | Declare shared scalars (`UnitOfMeasure`, `Pom`, `CodeDescription`, `SizeCodeDescription`, `Pageable`, `Paging`) with `@shareable`; reconcile ownership with sibling subgraphs · Medium (3–5d) | 🔵 | M | F05 |

**Phase E raw 5–9d → buffered 6–11d**

---

## Phase V — Validation, Tests, Cutover

| ID | Title | Severity | Complexity |
|---|---|---|---|
| **SPARK-MEAS-V01** | Port unit tests for resolvers + services · Medium (3–5d) | 🟢 | M |
| **SPARK-MEAS-V02** | Contract tests against backend (`measurements/v1` + `measurement/templates/v1` + master-data) · Medium (3–5d) | 🟢 | M |
| **SPARK-MEAS-V03** | Federation composition + introspection diff vs spark-internal-graphql · Small (1–2d) | 🟢 | S |
| **SPARK-MEAS-V04** | Performance baseline: `measurementSetsByIds`, `measurementSets(parentId)`, master-data caching · Small (1–2d) | 🟢 | S |
| **SPARK-MEAS-V05** | Gateway cutover with weighted rollout + rollback plan · Medium (3–5d) | 🔵 | M |
| **SPARK-MEAS-V06** | Decommission `SPARK_Measurement.js`, `SPARK_MeasurementTemplate.js`, `Measurement.js`, `MeasurementTemplate.js` from spark-internal-graphql · Small (1–2d) | 🔵 | S |

**Phase V raw 11–19d → buffered 14–23d**

---

## Risk Register

| Risk | Severity | Stories | Mitigation |
|---|---|---|---|
| `getSampleMeasurement` resolver-vs-service signature mismatch → JWT header contains sampleId literal | 🔴 | Q07 | Audit production token-header values immediately; ship Q07 fix first |
| `purgeTestMeasurementTemplateData` endpoint used as production delete | 🔴 | M11 | Confirm with backend; consider hold on delete until safe endpoint exists |
| `MeasurementTemplate.brands` awaits loader reference instead of load call | 🔴 | C11 | Quick fix; verify if brands currently return null in production |
| `updateMeasurementSet` non-atomic workspace + body write | 🔴 | M02 | Saga pattern or compensating action; document in arch decision record |
| ACL sentinel `SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY` semantic | 🟡 | M09, M10 | Confirm with access-control team |
| `updateMeasurementComponentStatus` missing JWT (cross-domain pattern w/ bom & product) | 🟡 | M08 | Either add JWT or document backend-enforced ACL |
| Polymorphic input `updateMeasurementAccess(systemTeamIds \| systemTeamDto)` | 🟡 | M03 | Tagged `MeasurementAccessInput` |
| Schema casing anomaly `Spark_MeasurementRowInput` | 🟡 | F05, M01, M02 | Rename in port; coordinate with UI |
| Elastic query string interpolation injection risk | 🟡 | Q03 | Sanitize parentId; use parameterized elastic client |
| `updatedFromResource` polymorphism only handles `'sample'` | 🟡 | C06 | Confirm with backend, plan union if needed |

---

## Critical Path

```
F01 → F02 → F04 → Q01 → Q07 (🔴 SampleMeasurement JWT bug)
                       ↘ M02 (🔴 atomic updateMeasurementSet) → M11 (🔴 safe delete endpoint)
                                                              ↘ C11 (🔴 brands loader bug)
```

Recommend **Sprint 1** ships F01–F08 + Q07 + C11 quick-fix backports if hot-fixable to source first.

---

## Effort Roll-Up

| Phase | Raw days | Buffered days |
|---|---|---|
| F Foundation | 13–22 | 16–27 |
| Q Queries | 11–19 | 14–23 |
| M Mutations | 28–46 | 34–56 |
| C Field resolvers | 14–24 | 17–29 |
| E Federation | 5–9 | 6–11 |
| V Validation/cutover | 11–19 | 14–23 |
| **Total (40 stories)** | **82–139** | **101–169** |

---

## Sprint Sequencing (suggested)

| Sprint | Stories | Goal |
|---|---|---|
| **S1** | F01, F02, F03, F04, F05, Q07, C11 | Scaffolding + critical bug fixes |
| **S2** | F06, F07, F08, Q01, Q02, Q03, Q04, Q05, Q06, Q08, Q09 | All queries online |
| **S3** | M01, M03, M04, M05, M06, M07, M08, M09, M10 | Bulk of mutations |
| **S4** | M02, M11, E01, E02, E03 | Risky mutations + federation contributions |
| **S5** | C01, C02, C03, C04, C05, C06, C07, C08, C09, C10 | Field resolvers + entity refs |
| **S6** | V01, V02, V03, V04, V05, V06 | Validate, cutover, decommission |

---

**Phase Completed:** Phase 4 — Story Generation
**Companion:** [04-po-summary.md](output/measurement/04-po-summary.md)
