# Phase 2: Resolver Dependency Analysis — Measurement

> **Domain:** `measurement` · **Target DGS:** `MeasurementService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `schemas/SPARK_Measurement.graphqls` (SDL), `resolvers/product/SPARK_Measurement.js`, `services/product/Measurement.js`
> **Depends on:** [be-01-schema-inventory.md](./be-01-schema-inventory.md) · **Mode:** Full

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 7 (measurement) + 8 (sub-domains) = 15 |
| Mutation resolvers | 8 (measurement) + 7 (sub-domains) = 15 |
| Field resolvers | 15 (measurement) + 13 (sub-domains: 5 MeasurementTemplate, 3 SizeTemplate, 5 TightFit) = 28 |
| Service methods | 18 (measurement) + 14 (sub-domains) = 32 |
| EXT loader keys | 11 (2 🔴 · 6 🟡 · 3 🔵) + accessControl context-only — `measurementTemplate`/`sizeTemplate`/`tightFit` reclassified **internal** 2026-07-19 (see Monorepo correction below); sub-domains' own remaining EXT: 🔵 `ig`/`vmm`/`userAttributes` (field resolvers), 🔵 NEXUS (searchSparkSizes) |
| Very High / High | 0 / 1 (`updateMeasurement`) |

---

## Query Resolvers (7 measurement + 8 sub-domain = 15)

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

## Sub-Domain Query Resolvers (8) — MeasurementTemplate, SizeTemplate, TightFit, Sizes

> Co-located `measurement` sub-domains — same `enterprise_product_development_products` service base,
> internal in-process calls from `Measurement.measurementTemplates`/`.sizeTemplate`/`.tightFitTemplate`.
> See the Monorepo correction note in the EXT inventory below.

### Q8 · `getMeasurementTemplates(page, size): MeasurementTemplatesPaged` — Low
`measurementTemplate.getMeasurementTemplates.load(params)` → `GET {base}/…/measurement/templates/v1?…&sort=createdAt,desc` → camelCase. Strips falsy params (`_.omitBy`); array params joined with `,`.

### Q9 · `getMeasurementTemplatesByIds(ids): MeasurementTemplatesPaged` — Low
`measurementTemplate.getMeasurementTemplatesByIds(ids)` → `GET {base}/…/measurement/templates/v1?ids=` → camelCase.

### Q10 · `getSizeTemplates(ids: [VersionableIdInput]): [SizeTemplate]` — Low
`sizeTemplate.getSizeTemplates(ids)` → `POST {base}/…/size_templates/v1/search` (id+version pairs) → camelCase.

### Q11 · `getSizeCategories(ids): [CodeDescription]` — Low · *cacheable master data*
`sizeTemplate.getSizeCategories(ids)` → `GET {masterDataBase}/size_category[?ids=]` → `size_categories` camelCase.

### Q12 · `getMaterialTypes(ids): [CodeDescription]` — Low · *cacheable master data*
`sizeTemplate.getMaterialTypes(ids)` → `GET {masterDataBase}/material_type[?ids=]` → `material_types` camelCase.

### Q13 · `getTightFits(ids, name, statusIds, brandIds, divisionIds, departmentIds): TightFitsResponse` — Low
`tightFit.getTightFits(...)` → `GET {base}/…/tightfit/v1/search?ids=&name=&statusIds=&brandIds=&divisionIds=&departmentIds=` (qs-stringified) → camelCase, wrapped `{tightFits}`.

### Q14 · `getTightFitByIdAndVersion(id, version): TightFit` — Low
`tightFit.getTightFitByIdAndVersion.load({id, version})` → `GET {base}/…/tightfit/v1/{id}/versions/{version}` (non-batching DataLoader) → camelCase.

### Q15 · `searchSparkSizes(nameFilter, size): [Sizes]` — Low
Fans out in parallel: `NEXUS_Attributes.Query.searchSizes(nameFilter, page:0, size)` (🔵 platform) tagged `source:'Nexus'`, and `SPARK_Tag.Query.searchTags(type:'SIZE', archived:false, search:nameFilter, page:0, size)` (co-located `tag` sub-domain) tagged `source:'Spark'`; concatenated and sliced to `size`. **No own REST endpoint** — pure aggregation resolver.

## Mutation Resolvers (8)

### M1 · `addMeasurement(sparkMeasurement): Measurement` — Medium
- `POST {base}/…/measurements/v1` (`transformRequest: deepToSnakeCase`, `primeKey: humanId`); on `validationErrors||message` → throw.
- No ACL (new resource).
- DGS: typed `MeasurementValidationException` + cache prime.

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

## Sub-Domain Mutation Resolvers (7) — MeasurementTemplate, SizeTemplate, TightFit

### M9 · `addMeasurementTemplate(measurementTemplate): MeasurementTemplate` — Low
(ACL context) token `[SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY]` → `POST {base}/…/measurement/templates/v1` (`transformRequest: deepToSnakeCase`); on `validationErrors||message` → throw.

### M10 · `updateMeasurementTemplate(measurementTemplate): MeasurementTemplate` — Low
(ACL context) token → `PUT {base}/…/measurement/templates/v1/{templateId}`; on `validationErrors||message` → throw.

### M11 · `deleteMeasurementTemplate(ids): Boolean` — Low
`measurementTemplate.deleteTemplates.load(ids)` → `DELETE {endpoint}/purgeTestMeasurementTemplateData?ids=`. **No ACL token.**

### M12 · `addSizeTemplate(sizeTemplate): SizeTemplate` — Low
(ACL context) token `[SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY]` → `POST {base}/…/size_templates/v1`; on `validationErrors||message` → throw.

### M13 · `updateSizeTemplate(sizeTemplate): SizeTemplate` — Low
(ACL context) token → `PUT {base}/…/size_templates/v1/{id}`; on `validationErrors||message` → throw.

### M14 · `addTightFit(tightFit): TightFit` — Low
(ACL context) token `[SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY]` → `POST {base}/…/tightfit/v1`; on `validationErrors||message` → throw.

### M15 · `updateTightFit(tightFit): TightFit` — Low
(ACL context) token → `PUT {base}/…/tightfit/v1/{tightFitId}`; on `validationErrors||message` → throw.

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
| `measurementTemplates` | `templateIds.length ? measurementTemplate.getMeasurementTemplatesByIds(ids).content : []` | — internal (co-located `measurement` sub-domain) |
| `sizeTemplate` | `sizeTemplate ? sizeTemplate.getSizeTemplates([id])[0] : undefined` | — internal (co-located `measurement` sub-domain) |
| `tightFitTemplate` | `tightFit.getTightFitByIdAndVersion.load({id, version})` | — internal (co-located `measurement` sub-domain) |
| `participantDetails` | `getUserGroup(ctx, humanId)` | 🔵 user-profile |

### `SampleMeasurementSet` (2 fields)
| Field | Logic | EXT |
|---|---|---|
| `createdBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(createdBy)` | 🔵 user-profile |
| `measurementSizeId` | `measurementSize && measurementSize.code` (Computed) | — |

### `MeasurementTemplate` (3 fields)
| Field | Logic | EXT |
|---|---|---|
| `createdBy`/`updatedBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(...)` | 🔵 user-profile |
| `departments` | `departmentIds && loadManyIncludeEmptyResponse(ig.department.getByID, departmentIds)` | 🔵 ig (platform) |
| `divisions` | `divisionIds && loadManyIncludeEmptyResponse(ig.division.getByID, divisionIds)` | 🔵 ig (platform) |
| `brands` | `brandIds && brandIds!==-1 && loadManyIncludeEmptyResponse(brand.getBrand, brandIds)` | 🔵 vmm (platform) |

### `SizeTemplate` (2 fields)
| Field | Logic | EXT |
|---|---|---|
| `humanId` | `humanId \|\| id` (Computed) | — |
| `createdBy`/`updatedBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(...)` | 🔵 user-profile |

### `TightFit` (5 fields)
| Field | Logic | EXT |
|---|---|---|
| `departments` | `departmentIds && loadManyIncludeEmptyResponse(ig.department.getByID, departmentIds)` | 🔵 ig (platform) |
| `divisions` | `divisionIds && loadManyIncludeEmptyResponse(ig.division.getByID, divisionIds)` | 🔵 ig (platform) |
| `brands` | `brandIds && brandIds!==-1 && loadManyIncludeEmptyResponse(brand.getBrand, brandIds)` | 🔵 vmm (platform) |
| `createdBy`/`updatedBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(...)` | 🔵 user-profile |

> `Sizes` has no field resolvers of its own — `searchSparkSizes` builds the `{id, name, source}` shape
> directly from the NEXUS/Tag responses (Q15).

## Service Classes (1 + 4 sub-domain = 5)

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

> **Monorepo correction (2026-07-19, supersedes the previous note):** `measurementTemplate`, `sizeTemplate`,
> `tightFit` (and `product`) are **co-located in the same `plm-product` subgraph** — confirmed against their
> service classes, which all build their endpoint from the same `enterprise_product_development_products`
> base as `MeasurementService`. Their field resolvers (`measurementTemplates`, `sizeTemplate`,
> `tightFitTemplate`) are **internal** in-process calls, **not** gateway federation, and — unlike the
> earlier pass — they are **no longer counted in the loader-key total below**: they are fully internal
> sub-domains of `measurement` with their OWN operations, service classes, and stories (Phase B/D/G in
> [be-04-stories.md](./be-04-stories.md)), not merely a pass-through field on `Measurement`.
> **Genuinely external to `measurement` (incl. its sub-domains):** `relationship`, `search`, `workspaceV2`,
> `sampleV2`, `userAttributes`/userGroup, `accessControl` (context-only), platform `vmm`/`brand`, platform
> `ig`, platform `NEXUS_Attributes` (searchSparkSizes only).

**11 keys — 2 🔴 · 3 🟡 · 3 🔵** (+ accessControl context-only) on `measurement` itself; the sub-domains add
3 more distinct EXT touchpoints of their own (🔵 `ig`, 🔵 `vmm`/`brand`, 🔵 NEXUS — `userAttributes` already
counted):

| # | Loader key | Owning DGS / platform | Severity | Called from |
|---|---|---|---|---|
| 1 | `relationship` | RelationshipService | 🔴 | Q2 |
| 2 | `search` | SearchService | 🔴 | Q3 |
| 3 | `workspaceV2` | WorkspaceService | 🟡 | workspaces, M3 |
| 4 | `sampleV2` | SampleService | 🟡 | updatedFromResource |
| 5 | `vmm` | VMM platform | 🔵 | businessPartners |
| 6 | `userAttributes` | UserProfileService | 🔵 | createdBy/updatedBy (measurement + all 3 sub-domains) |
| 7 | userGroup | UserProfileService | 🔵 | participantDetails |
| 8 | `product` | ProductService (same DGS) | — internal | product field |
| 9 | `measurementTemplate` | MeasurementTemplate (co-located sub-domain) | — internal | measurementTemplates (Q1/Q8/Q9/M9-M11 own the real ops) |
| 10 | `sizeTemplate` | SizeTemplate (co-located sub-domain) | — internal | sizeTemplate (Q10-Q12/M12-M13 own the real ops) |
| 11 | `tightFit` | TightFit (co-located sub-domain) | — internal | tightFitTemplate (Q13-Q14/M14-M15 own the real ops) |
| 12 | `ig` | Item Groups (IG) platform | 🔵 | TightFit.departments/.divisions, MeasurementTemplate.departments/.divisions |
| 13 | `brand` (vmm) | VMM platform | 🔵 | TightFit.brands, MeasurementTemplate.brands |
| 14 | `NEXUS_Attributes` | Nexus platform | 🔵 | Q15 `searchSparkSizes` |

## Complexity Assessment
`updateMeasurement` **High** (2-step). `getMeasurements`, `addMeasurement`, `putSampleMeasurementSet` **Medium**. Sub-domain ops (Q8-Q15, M9-M15) all **Low** — thin CRUD/search, no orchestration. Everything else **Low**.

## Key Findings
- **Highest risk:** `updateMeasurement` 2-step workspace+body write.
- **Refactor:** `updateMeasurementAccess` polymorphic input → tagged `MeasurementAccessInput`; client-side sorts (Q2/Q3) → backend.
- **Confirm:** `updateMeasurementComponentStatus` no JWT (like BOM M6); 2 unused version methods; `M11 deleteMeasurementTemplate` also has no JWT.
- **Quick wins:** 3 cacheable master-data queries (+ 2 more on SizeTemplate: size categories, material types); lock/unlock; delete-sample.
- **Sub-domain reclassification:** `measurementTemplate`/`sizeTemplate`/`tightFit` were previously tagged EXT 🟡 sibling-DGS in `domain-service-catalog.md` and treated as opaque pass-through fields; they are genuinely co-located and now have first-class stories of their own (2026-07-19 correction).

---
**Phase Completed:** Phase 2 · **Domain:** `measurement` · **EXT:** 11 keys on measurement itself (2🔴·3🟡·3🔵/internal) + 3 sub-domain EXT touchpoints (🔵 ig/vmm/NEXUS).
