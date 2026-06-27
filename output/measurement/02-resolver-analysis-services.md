# Measurement — Resolver Analysis: Services + Utils

> **Domain:** `measurement` (+ `measurementTemplate`) · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## D1. `MeasurementService` (14 methods, 181 lines)

| # | Method | HTTP | Path | JWT | Notes |
|---|---|---|---|---|---|
| 1 | `getMeasurementByIds(jwt, ids, calculated, businessPartnerIds, mustHaveRows)` | GET | `/v1?ids=&calculated=&businessPartnerIds=&mustHaveRows=` | ✓ | qs.stringify |
| 2 | `getMeasurementSetVersionsById(jwt, id)` | GET | `/v1/{id}/versions` | ✓ | **Unused** |
| 3 | `getMeasurementSetVersion({id, version})` | GET | `/v1/{id}/versions/{version}` | `fetchAclToken:true` | **Unused** |
| 4 | `getUnitsOfMeasure(ids)` | GET | `/master_data/unit_of_measure[?ids=]` | ✗ | Master data; cacheable |
| 5 | `getThicknessUnitsOfMeasure()` | GET | `/master_data/thickness_uom` | ✗ | Master data; cacheable |
| 6 | `getMeasurementSetStatus()` | GET | `/masterData?name=MeasurementSetStatus` | ✗ | Master data; cacheable |
| 7 | `getSampleMeasurement(jwt, sampleId)` | GET | `/v1/sample/{sampleId}` | ✓ | **Bug: resolver passes sampleId where jwt expected** (Phase 2A Q7) |
| 8 | `addMeasurement(measurement)` | POST | `/v1` | ✗ | primeKey humanId |
| 9 | `updateMeasurement(jwt, measurement)` | PUT | `/v1/{humanId}` | ✓ | omitParamsInBody; primeKey humanId |
| 10 | `putSampleMeasurementSet(jwt, m)` | PUT | `/v1/sample` | ✓ | primeKey sampleId |
| 11 | `deleteSampleMeasurementSet(jwt, sampleId)` | DELETE | `/v1/sample/{sampleId}` | ✓ | |
| 12 | `updateMeasurementAccess(jwt, msId, systemTeamIds, systemTeamDto)` | PUT | `/v1/{msId}/permission` | ✓ | Polymorphic body |
| 13 | `lockMeasurementSet(jwt, msId)` / `unlockMeasurementSet(jwt, msId)` | PUT | `/v1/{msId}/{lock\|unlock}` | ✓ | primeKey humanId |
| 14 | `manageWorkspaceAssociations(msId, action, jwt)` | PUT | `/v1/{msId}/{associate\|dissociate}_workspace` | ✓ | Called via `workspaceAssociationHelper` |
| 15 | `updateMeasurementComponentStatus(input)` | PUT | `/v1/component_status_update` | ✗ | **Missing JWT** (M8 finding) |

### Findings (D1)

| # | Finding | Severity |
|---|---|---|
| 1 | 3 unused methods (#2, #3, #14 stand-alone) — confirm cross-domain callers before delete | 🟢 |
| 2 | Q7 `getSampleMeasurement` resolver-vs-service signature mismatch (latent bug) | 🔴 |
| 3 | `updateMeasurementComponentStatus` missing JWT | 🟡 |
| 4 | Manual qs.stringify on Q1 — replace with Feign multi-param | 🟢 |

---

## D2. `MeasurementTemplateService` (5 methods, 53 lines)

| # | Method | HTTP | Path | JWT | Notes |
|---|---|---|---|---|---|
| 1 | `getMeasurementTemplates` | GET | `/v1?{params}&sort=createdAt,desc` | ✗ | Pagination; pre-bound DataLoader |
| 2 | `getMeasurementTemplatesByIds(ids)` | GET | `/v1?ids=` | ✗ | |
| 3 | `addMeasurementTemplate(jwt, template)` | POST | `/v1` | ✓ | |
| 4 | `updateMeasurementTemplate(jwt, template)` | PUT | `/v1/{templateId}` | ✓ | |
| 5 | `deleteTemplates(ids)` | DELETE | `${endpoint}/purgeTestMeasurementTemplateData?ids=` | ✗ | **Production safety issue** (M11 finding) |

### Findings (D2)

| # | Finding | Severity |
|---|---|---|
| 1 | `deleteTemplates` endpoint is `purgeTestMeasurementTemplateData` — production-safety question | 🔴 |
| 2 | `deleteTemplates` closure shadowing of `endpoint` (uses constructor `endpoint` arg, not `this.endpoint`) | 🟡 |
| 3 | `deleteTemplates` has no JWT | 🟡 |
| 4 | `getMeasurementTemplates` is pre-bound `loadListing` (not a method) — unusual pattern; preserve as factory in DGS | 🟢 |

---

## D3. No Dedicated Utils

All cross-cutting helpers are shared:

| Util | Owner | Usage |
|---|---|---|
| `commonLoaders.getUserPermissionsJWT` | shared | 7 queries + 7 mutations + ... |
| `workspaceAssociationHelper` | workspace utils | M2 |
| `vmmUtils.loadBps` / `loadManyIncludeEmptyResponse` | vmm | C1, C4 |
| `Product/userGroupUtils.getUserGroup` | product | C1 participantDetails |
| `constants.SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY` | shared | M9, M10 ACL JWT seed |
| `resolvers/SPARK_WorkspaceV2` | workspace | C1 workspaces |

---

## D4. `measurementsActivityModifiedDataHelper.js` (29 lines)

Activity-log diff helper. **Out of scope** for measurement DGS — owned by activity-log subsystem.

---

## D5. Phase 2 Grand Total

| Sub-phase | Days |
|---|---|
| 2A Queries | 9–16 |
| 2B Mutations | 26–43 |
| 2C Field resolvers | 7–12 |
| 2D Service + utils | 5–9 |
| **Phase 2 raw** | **47–80** |
| **+20% buffer** | **57–96** |

---

**Phase Completed:** Phase 2D — Services + Utils
