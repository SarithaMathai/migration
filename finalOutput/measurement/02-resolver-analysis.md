# Phase 2: Resolver Dependency Analysis — Measurement

> **Domain:** `measurement` · **Target DGS:** `MeasurementService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `code/schemas/SPARK_Measurement.txt` (SDL), `code/resolvers/product/SPARK_Measurement.txt`, `code/services/product/Measurement.txt`
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 7 |
| Mutation resolvers | 8 |
| Field resolvers | 15 |
| Service methods | 18 |
| EXT loader keys | 11 (2 🔴 · 6 🟡 · 3 🔵) + accessControl context-only |
| Very High / High | 0 / 1 (`updateMeasurement`) |

---

## Query Resolvers (7)

### Q1 · `getMeasurementByIds(ids, calculated): MeasurementPaged` — Low
(ACL context) token for `ids` → `measurement.getMeasurementByIds(jwt, ids, calculated)` →
`GET {base}/…/measurements/v1?ids=&calculated=&mustHaveRows=` → camelCase.

### Q2 · `getMeasurements(businessPartnerIds, calculated, mustHaveRows, resourceId): MeasurementPaged` — Medium
1. `relationships = relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0})` — **EXT 🔴 relationship**.
2. `measurementSetIds = relationships.map(n => n.id)`; if empty → `[]`.
3. (ACL context) token for `measurementSetIds`.
4. `{content} = getMeasurementByIds(jwt, ids, calculated, businessPartnerIds, mustHaveRows)`.
5. Return `{content: orderBy(content, createdAt DESC)}` — client-side sort (PO decision: push to backend).

### Q3 · `getMeasurementsElastic(resourceId): MeasurementPaged` — Low
`{content} = search.getMeasurementSets.load({q:`parentId: ${resourceId}`})` → sort `createdAt DESC` → `{content}`. **EXT 🔴 search**.

### Q4 · `getUnitsOfMeasure(ids): [UnitOfMeasure]` — Low · *cacheable master data*
`measurement.getUnitsOfMeasure(ids)` → `GET {base}/…/master_data/unit_of_measure[?ids=]` → `units_of_measure` camelCase.

### Q5 · `getThicknessUnitsOfMeasure: [UnitOfMeasure]` — Low · *cacheable*
`GET {base}/…/master_data/thickness_uom` → `units_of_measure`.

### Q6 · `getMeasurementSetStatus: [CodeDescription]` — Low · *cacheable*
`GET {base}/masterData?name=MeasurementSetStatus` → `{key:value}` map → `[{code, description}]`.

### Q7 · `getSampleMeasurement(sampleId): SampleMeasurementSet` — Low
(ACL context) token for `sampleId` → `GET {base}/…/measurements/v1/sample/{sampleId}` → camelCase.

## Mutation Resolvers (8)

### M1 · `addMeasurement(sparkMeasurement): Measurement` — Medium
`POST {base}/…/measurements/v1` (`transformRequest: deepToSnakeCase`, `primeKey: humanId`); on `validationErrors||message` → throw. No ACL (new resource). DGS: typed `MeasurementValidationException` + cache prime.

### M2 · `updateMeasurementComponentStatus(productId, ids, status): MeasurementPaged` — Low
`PUT {base}/…/measurements/v1/component_status_update` body `{productId, ids, status}`. **No ACL token** (like BOM M6) — confirm backend enforces.

### M3 · `updateMeasurement(sparkMeasurement): Measurement` — **High** (2-step non-atomic)
1. `workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations || {}`. (ACL context) token for `[humanId]`.
2. **If** add/remove workspaces → `workspaceAssociationHelper(MEASUREMENT, humanId, add, remove)`; on its `validationErrors||message` → throw. **(commits first)**
3. `measurement = measurement.updateMeasurement(jwt, sparkMeasurement)` → `PUT …/measurements/v1/{humanId}` (`omitParamsInBody: true`).
4. On `validationErrors||message` → throw. Return measurement.
**Finding 🟡:** 2-step write — workspace change persists if body PUT fails. PO decision: rollback strategy (lighter than BOM's 3-step).

### M4 · `updateMeasurementAccess(measurementSetId, systemTeamIds, systemTeamDto): Measurement` — Low
(ACL context) token → `measurement.updateMeasurementAccess(jwt, id, systemTeamIds, systemTeamDto)` →
`PUT …/{id}/permission` with body `{systemTeamIds}` **or** `{systemTeamDto}` (whichever is provided).
**Finding 🟡:** polymorphic input — recommend a single tagged `MeasurementAccessInput`.

### M5 · `lockMeasurementSet(measurementSetId): Measurement` — Low
(ACL context) → `PUT …/{id}/lock`.

### M6 · `unlockMeasurementSet(measurementSetId): Measurement` — Low
(ACL context) → `PUT …/{id}/unlock`.

### M7 · `putSampleMeasurementSet(sampleMeasurementSet): SampleMeasurementSet` — Medium
(ACL context) token for `[measurementSetId, sampleId]` → `PUT …/sample` (`primeKey: sampleId`); on `validationErrors||message` → throw.

### M8 · `deleteSampleMeasurementSet(sampleId): SampleMeasurementSet` — Low
(ACL context) token for `sampleId` → `DELETE …/sample/{sampleId}`.

## Field Resolvers

### Measurement set (`SPARK_Measurements`, 13 fields)
| Field | Logic | EXT |
|---|---|---|
| `access` | `accessControl.getPermissions.load({resourceIds:[humanId]})` → `[0]` | accessControl (context) |
| `currentUserPermissions` | `accessControl.getUserAccessUnencoded.load(humanId)` → `resourcePermissions[0]` | accessControl (context) |
| `businessPartners` | `businessPartnerIds && loadBps(businessPartnerIds)` | 🔵 vmm |
| `createdBy`/`updatedBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(...)` | 🔵 user-profile |
| `product` | if `resourceId.indexOf('PID')===0` → `product.getByID.load(resourceId)` else null | — internal |
| `workspaces` | `workspaceContext.length ? getWorkspacesByIdsV2(...) : null` | 🟡 workspaceV2 |
| `status` | `{code: statusId, description: statusName}` (Computed) | — |
| `updatedFromResource` | switch `type`: `'sample'` → `sampleV2.getSampleById.load(id)`; else null | 🟡 sampleV2 |
| `measurementTemplates` | `templateIds.length ? measurementTemplate.getMeasurementTemplatesByIds(ids).content : []` | 🟡 measurementTemplate |
| `sizeTemplate` | `sizeTemplate ? sizeTemplate.getSizeTemplates([id])[0] : undefined` | 🟡 sizeTemplate |
| `tightFitTemplate` | `tightFit.getTightFitByIdAndVersion.load({id, version})` | 🟡 tightFit |
| `participantDetails` | `getUserGroup(ctx, humanId)` | 🔵 user-profile |

### `SampleMeasurementSet` (2 fields)
| Field | Logic | EXT |
|---|---|---|
| `createdBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(createdBy)` | 🔵 user-profile |
| `measurementSizeId` | `measurementSize && measurementSize.code` (Computed) | — |

## Service Classes (1)

### S1 · `MeasurementService` — base `…/measurements/v1`
| Method | HTTP | Path | JWT | Notes |
|---|---|---|---|---|
| `getMeasurementByIds(jwt, ids, calculated, bpIds, mustHaveRows)` | GET | `/v1?ids=&calculated=&businessPartnerIds=&mustHaveRows=` | ✓ | qs.stringify |
| `getMeasurementSetVersionsById(jwt, id)` | GET | `/v1/{id}/versions` | ✓ | **unused by resolvers** |
| `getMeasurementSetVersion({id, version})` | GET | `/v1/{id}/versions/{version}` | aclToken | **unused** |
| `getUnitsOfMeasure(ids)` | GET | `/master_data/unit_of_measure[?ids=]` | ✗ | cacheable |
| `getThicknessUnitsOfMeasure()` | GET | `/master_data/thickness_uom` | ✗ | cacheable |
| `getMeasurementSetStatus()` | GET | `/masterData?name=MeasurementSetStatus` | ✗ | cacheable |
| `getSampleMeasurement(jwt, sampleId)` | GET | `/v1/sample/{sampleId}` | ✓ | |
| `addMeasurement(m)` | POST | `/v1` | ✗ | `primeKey: humanId` |
| `updateMeasurement(jwt, m)` | PUT | `/v1/{humanId}` | ✓ | `omitParamsInBody`; primes |
| `putSampleMeasurementSet(jwt, m)` | PUT | `/v1/sample` | ✓ | `primeKey: sampleId` |
| `deleteSampleMeasurementSet(jwt, sampleId)` | DELETE | `/v1/sample/{sampleId}` | ✓ | |
| `updateMeasurementAccess(jwt, id, teamIds, dto)` | PUT | `/v1/{id}/permission` | ✓ | body `{systemTeamIds}` or `{systemTeamDto}` |
| `lockMeasurementSet(jwt, id)` | PUT | `/v1/{id}/lock` | ✓ | |
| `unlockMeasurementSet(jwt, id)` | PUT | `/v1/{id}/unlock` | ✓ | |
| `manageWorkspaceAssociations(id, action, jwt)` | PUT | `/v1/{id}/{associate\|dissociate}_workspace` | ✓ | via helper |
| `updateMeasurementComponentStatus(input)` | PUT | `/v1/component_status_update` | ✗ | **no JWT** |

## EXT Service Call Inventory

> **Monorepo correction:** `measurementTemplate`, `sizeTemplate`, `tightFit` (and `product`) are **co-located
> in the same `plm-product` subgraph** — their field resolvers (`measurementTemplates`, `sizeTemplate`,
> `tightFitTemplate`) are **internal** in-process calls, **not** gateway federation. They appear in the table
> below for traceability but require no CAT-4 stub. **Genuinely external:** `relationship`, `search`,
> `workspaceV2`, `sampleV2`, `userAttributes`/userGroup, `accessControl` (context-only) + platform `vmm`.

**11 keys — 2 🔴 · 6 🟡 (3 of which are co-located/internal) · 3 🔵** (+ accessControl context-only):

| # | Loader key | Owning DGS / platform | Severity | Called from |
|---|---|---|---|---|
| 1 | `relationship` | RelationshipService | 🔴 | Q2 |
| 2 | `search` | SearchService | 🔴 | Q3 |
| 3 | `workspaceV2` | WorkspaceService | 🟡 | workspaces, M3 |
| 4 | `sampleV2` | SampleService | 🟡 | updatedFromResource |
| 5 | `measurementTemplate` | MeasurementTemplateService | 🟡 | measurementTemplates |
| 6 | `sizeTemplate` | SizeTemplateService | 🟡 | sizeTemplate |
| 7 | `tightFit` | TightFitService | 🟡 | tightFitTemplate |
| 8 | `vmm` | VMM platform | 🔵 | businessPartners |
| 9 | `userAttributes` | UserProfileService | 🔵 | createdBy/updatedBy |
| 10 | userGroup | UserProfileService | 🔵 | participantDetails |
| 11 | `product` | ProductService (same DGS) | — internal | product field |

## Complexity Assessment
`updateMeasurement` **High** (2-step). `getMeasurements`, `addMeasurement`, `putSampleMeasurementSet` **Medium**. Everything else **Low**.

## Key Findings
- **Highest risk:** `updateMeasurement` 2-step workspace+body write.
- **Refactor:** `updateMeasurementAccess` polymorphic input → tagged `MeasurementAccessInput`; client-side sorts (Q2/Q3) → backend.
- **Confirm:** `updateMeasurementComponentStatus` no JWT (like BOM M6); 2 unused version methods.
- **Quick wins:** 3 cacheable master-data queries; lock/unlock; delete-sample.

---
**Phase Completed:** Phase 2 · **Domain:** `measurement` · **EXT:** 11 keys (2🔴·6🟡·3🔵).
