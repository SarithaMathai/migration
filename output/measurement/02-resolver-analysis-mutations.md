# Measurement — Resolver Analysis: Mutations

> **Domain:** `measurement` (+ `measurementTemplate`) · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

12 mutations total (9 measurement + 3 template).

---

## M1 · `addMeasurement(sparkMeasurement) : SPARK_Measurements` — CAT-2 · Medium (3–5d)

```
measurement = await measurement.addMeasurement(sparkMeasurement)
if (validationErrors || message) throw Error
return measurement
```
**Service:** `POST /measurements/v1` with `primeKey: humanId`. **No JWT** on create.

---

## M2 · `updateMeasurement(sparkMeasurement: SPARK_MeasurementsUpdateInput) : SPARK_Measurements` — CAT-2 · Large (5–8d)

```
workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations || {}
permissionJWT = await getUserPermissionsJWT([sparkMeasurement.humanId], ctx)
if ((toAdd?.length) || (toRemove?.length))
  result = await workspaceAssociationHelper(MEASUREMENT, humanId, add, remove, ctx)
  if (result.validationErrors || result.message) throw Error('Error associating measurement set workspaces...')
measurement = await measurement.updateMeasurement(permissionJWT, sparkMeasurement)
if (validationErrors || message) throw Error
return measurement
```

**Finding 🔴:** 2-step non-atomic write (workspace → body). If body update fails, workspaces already committed. Same atomicity question as bom `updateBom` and product `productBusinessPartnerActions`. Decision required.

---

## M3 · `updateMeasurementAccess(measurementSetId, systemTeamIds, systemTeamDto) : SPARK_Measurements` — CAT-2 · Medium (3–5d)

```
permissionJWT = await getUserPermissionsJWT([measurementSetId], ctx)
return measurement.updateMeasurementAccess(permissionJWT, measurementSetId, systemTeamIds, systemTeamDto)
```
**Service:** `PUT /measurements/v1/{measurementSetId}/permission` with body `systemTeamIds ? {systemTeamIds} : {systemTeamDto}` (polymorphic — one OR the other).

**Finding 🟡:** Polymorphic input. In DGS, prefer a single tagged input type or two separate mutations.

---

## M4 · `lockMeasurementSet(measurementSetId) : SPARK_Measurements` — CAT-2 · Small (<1d)

`PUT /measurements/v1/{measurementSetId}/lock` with JWT.

---

## M5 · `unlockMeasurementSet(measurementSetId) : SPARK_Measurements` — CAT-2 · Small (<1d)

`PUT /measurements/v1/{measurementSetId}/unlock` with JWT.

---

## M6 · `putSampleMeasurementSet(sampleMeasurementSet: SPARK_SampleMeasurementSetInput) : SPARK_SampleMeasurementSet` — CAT-2 · Medium (3–5d)

```
permissionJWT = await getUserPermissionsJWT([sampleMeasurementSet.measurementSetId, sampleMeasurementSet.sampleId], ctx)
measurement = await measurement.putSampleMeasurementSet(permissionJWT, sampleMeasurementSet)
if (validationErrors || message) throw Error
return measurement
```
**Service:** `PUT /measurements/v1/sample` with `primeKey: sampleId`. JWT seeded by both the measurementSet AND sample IDs (multi-resource permission).

---

## M7 · `deleteSampleMeasurementSet(sampleId) : String` — CAT-2 · Small (1–2d)

```
permissionJWT = await getUserPermissionsJWT(sampleId, ctx)
return measurement.deleteSampleMeasurementSet(permissionJWT, sampleId)
```
**Service:** `DELETE /measurements/v1/sample/{sampleId}` with JWT.

**Finding 🟢:** Return type is `String` — what string? Confirm backend response shape (typical: success/ID).

---

## M8 · `updateMeasurementComponentStatus(productId, ids, status) : SPARK_MeasurementsPaged` — CAT-2 · Small (1–2d)

```
return measurement.updateMeasurementComponentStatus({productId, ids, status})
```
**Service:** `PUT /measurements/v1/component_status_update`. **No JWT.**

**Finding 🟡:** Missing JWT — same pattern observed in bom M6 (`updateBomComponentStatus`) and product domain. Confirm whether intentional (backend enforces) or oversight.

---

## M9 · `addMeasurementTemplate(measurementTemplate) : SPARK_MeasurementTemplate` — CAT-2 · Medium (3–5d)

```
permissionJWT = await getUserPermissionsJWT([SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY], ctx)
template = await measurementTemplate.addMeasurementTemplate(permissionJWT, measurementTemplate)
if (validationErrors || message) throw Error
return template
```

**Finding 🟡:** ACL JWT seeded with constant `SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY` (not a real resource ID). Confirm what this sentinel means in the ACL system — typically a "library write" capability stand-in. Document the sentinel ID.

---

## M10 · `updateMeasurementTemplate(measurementTemplate) : SPARK_MeasurementTemplate` — CAT-2 · Medium (3–5d)

Same JWT-sentinel pattern as M9. `PUT /measurement/templates/v1/{templateId}`.

---

## M11 · `deleteMeasurementTemplate(ids: [ID]) : Boolean` — CAT-2 · Medium (3–5d)

```
return measurementTemplate.deleteTemplates.load(ids)
```
**Service path:** `${endpoint}/purgeTestMeasurementTemplateData?ids=` — **uses test-data-purge endpoint in production?**

**Finding 🔴:** Endpoint name `purgeTestMeasurementTemplateData` suggests this is a non-production cleanup tool repurposed as the delete mutation. Verify with backend team. Also, no JWT (template service deleteTemplates skips ACL — confirm intentional). DGS port should use a proper delete endpoint.

**Finding 🟡:** Closure-shadowing bug in service: `deleteTemplates = deleteOne(ids => `${endpoint}/...`)` — `endpoint` here refers to the constructor arg, not `this.endpoint`. Works because constructor still binds `endpoint` from outer scope, but fragile.

---

## Cross-Cutting Findings

| # | Finding | Severity |
|---|---|---|
| 1 | M2 `updateMeasurement` 2-step non-atomic write — rollback decision | 🔴 |
| 2 | M11 `deleteMeasurementTemplate` calls `purgeTestMeasurementTemplateData` — production safety question | 🔴 |
| 3 | M3 polymorphic input (`systemTeamIds` XOR `systemTeamDto`) — refactor in DGS | 🟡 |
| 4 | M8 missing JWT (consistent with bom M6 and product pattern) | 🟡 |
| 5 | M9/M10 JWT-sentinel pattern — document `SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY` semantic | 🟡 |
| 6 | M11 closure-shadowing on `endpoint` reference | 🟡 |
| 7 | M11 no JWT on template delete | 🟡 |
| 8 | M1, M6, M9, M10 all use shape-sniff error detection (`validationErrors \|\| message`) — typed exceptions in port | 🟢 |
| 9 | M1, M2, M4, M5, M6 `primeKey` preservation in DataLoader cache | 🟢 |

---

## Effort

| Tier | Mutations | Days |
|---|---|---|
| Small | M4, M5, M7, M8 (4) | 3–5 |
| Medium | M1, M3, M6, M9, M10, M11 (6) | 18–30 |
| Large | M2 (1) | 5–8 |
| **Subtotal mutations** | **11** (+ delete is part of M11) | **26–43** |

---

**Phase Completed:** Phase 2B — Mutation Resolvers
