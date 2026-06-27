# measurement — Jira stories (paste one block per issue)

> **Epic:** Measurement → plm-product DGS migration  ·  **Labels:** `dgs-migration`, `measurement`, `<type>`
> Create the Epic first, then paste each block below as a new Story's description.
> Story points are AI-derived from complexity (confirm in refinement). See [README.md](./README.md).

## SPARK-MEAS-A01 · Schema skeleton + DateTime scalar
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** —
**Labels:** `dgs-migration`, `measurement`, `schema`

**As a** DGS migration engineer **I want** the `measurement.graphqls` skeleton + `DateTime` **so that** later
work compiles on a stable base.
**Current Behaviour:** green-field; schema translated from `code/schemas/SPARK_Measurement.txt`.
**Target DGS Implementation:** federation v2.3 header, `scalar DateTime → Instant`, empty `extend type Query`/`Mutation`.
**Files:** `schema/measurement.graphqls`, `config/ScalarConfig.kt`. **Dependencies:** None.
**Acceptance Criteria:** 1. `./gradlew generateJava` passes. 2. `DateTime` round-trips ISO-8601.
**Test Cases:** ☐ Unit: compiles ☐ Unit: DateTime serde.

---

## SPARK-MEAS-A02 · Owned types + inputs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-A01
**Labels:** `dgs-migration`, `measurement`, `schema`

**Current Behaviour:** `Measurement` (set), `SampleMeasurementSet`, 6 value types + ~18 inputs — see [03-schema.graphql](./03-schema.graphql).
**Target DGS Implementation:** add the types; `@key(fields:"id")` on `Measurement`; `@key(fields:"sampleId")` on `SampleMeasurementSet`; `@shareable` on the 5 shared value types.
**Files:** `schema/measurement.graphqls`. **Dependencies:** A01.
**Acceptance Criteria:** 1. All owned types + inputs present. 2. Keys applied as above. 3. Schema validates.
**Test Cases:** ☐ Unit: validates ☐ Unit: both entities resolve via stub.

---

## SPARK-MEAS-A03 · External stubs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A01
**Labels:** `dgs-migration`, `measurement`, `schema`

**Current Behaviour:** references 12 external types incl. `TightFit` (composite key `id version`), `MeasurementTemplate`/`SizeTemplate` (sibling domains), `SampleV2`.
**Target DGS Implementation:** add each stub with the correct `@key`; `TightFit @key(fields:"id version")`.
**Files:** `schema/measurement.graphqls`. **Dependencies:** A01.
**Acceptance Criteria:** 1. 12 stubs compile; gateway composes. 2. `TightFit` composite key correct.
**Test Cases:** ☐ Unit: compiles ☐ Integration: gateway resolves a `MeasurementTemplate` stub.

---

## SPARK-MEAS-A04 · MeasurementService Kotlin port (18 methods)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-A01
**Labels:** `dgs-migration`, `measurement`, `service`

**Current Behaviour (S1):** base `…/measurements/v1` + master data. 18 methods (see [02 §Service Classes](./02-resolver-analysis.md)). `addMeasurement`/`updateMeasurement` prime the read cache; `updateMeasurement` sets `omitParamsInBody`. **ACL note (context):** resource-scoped calls curry a capability token; ignored in DGS.
**Target DGS Implementation:** `MeasurementClient` Feign + `MeasurementService`. Master-data methods (`getUnitsOfMeasure`, `getThicknessUnitsOfMeasure`, `getMeasurementSetStatus`) `@Cacheable`. Build `getMeasurementByIds` query string with `qs`-style params. Confirm fate of 2 unused version methods.
**Files:** `service/MeasurementService.kt`, `client/MeasurementClient.kt`, `model/MeasurementDto.kt`. **Dependencies:** A01.
**Acceptance Criteria:** 1. All 18 method signatures present; verb/path per §Service Classes. 2. Master-data `@Cacheable`. 3. `updateMeasurement` PUT omits `humanId` from body. 4. Jackson snake/camel both ways.
**Test Cases:** ☐ Unit: `getMeasurementByIds` query build ☐ Unit: cache hit ☐ Unit: snake/camel.

---

## SPARK-MEAS-B01 · getMeasurementByIds data fetcher
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A02, SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `query`

**Current Behaviour (Q1):** `GET {base}/…/measurements/v1?ids=&calculated=&mustHaveRows=` → camelCase. **ACL note (context):** token for `ids`; ignored in DGS.
**Target DGS Implementation:** `@DgsQuery getMeasurementByIds(ids, calculated): MeasurementPaged` (SDL: paged `{content}`, not a bare list) → `measurementService.getByIds(ids, calculated)`. Add a `MeasurementDataLoader` keyed on id.
**Files:** `dataFetcher/MeasurementQueryDataFetcher.kt`. **Dependencies:** A02, A04.
**Acceptance Criteria:** 1. Returns measurements for ids with `calculated` flag forwarded. 2. Empty ids → `[]`. 3. snake→camel mapping.
**Test Cases:** ☐ Unit: happy path ☐ Unit: empty ☐ Integration.

---

## SPARK-MEAS-B02 · getUnitsOfMeasure (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `query`

**Current Behaviour (Q4):** `GET {base}/…/master_data/unit_of_measure[?ids=]` → `units_of_measure` camelCase.
**Target DGS Implementation:** `@DgsQuery` → `@Cacheable` service method returning `[UnitOfMeasure]`.
**Acceptance Criteria:** 1. Returns UoM list (optionally filtered by ids). 2. Cached.
**Test Cases:** ☐ Unit: list ☐ Unit: cache hit.

---

## SPARK-MEAS-B03 · getThicknessUnitsOfMeasure (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `query`

**Current Behaviour (Q5):** `GET {base}/…/master_data/thickness_uom` → `units_of_measure`.
**Target DGS Implementation:** `@DgsQuery` → `@Cacheable` returning `[UnitOfMeasure]`.
**Acceptance Criteria:** 1. Returns thickness UoM list. 2. Cached.
**Test Cases:** ☐ Unit: list ☐ Unit: cache hit.

---

## SPARK-MEAS-B04 · getMeasurementSetStatus (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `query`

**Current Behaviour (Q6):** `GET {base}/masterData?name=MeasurementSetStatus` → `{key:value}` map → `[{code, description}]`.
**Target DGS Implementation:** `@DgsQuery` → `@Cacheable` mapping the map to the list.
**Acceptance Criteria:** 1. Returns statuses. 2. Cached. 3. key→code, value→description.
**Test Cases:** ☐ Unit: map→list ☐ Unit: cache hit.

---

## SPARK-MEAS-B05 · getSampleMeasurement data fetcher
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A02, SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `query`

**Current Behaviour (Q7):** `GET {base}/…/measurements/v1/sample/{sampleId}` → camelCase. **ACL note (context):** token for `sampleId`; ignored in DGS.
**Target DGS Implementation:** `@DgsQuery getSampleMeasurement(sampleId): SampleMeasurementSet` (SDL: a single object, not a list).
**Acceptance Criteria:** 1. Returns the sample measurement set for `sampleId`. 2. Not found → `null`.
**Test Cases:** ☐ Unit: happy path ☐ Unit: empty ☐ Integration.

---

## SPARK-MEAS-C01 · getMeasurements (relationship + listing)
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `query`

**Current Behaviour (Q2):**
1. `relationships = relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0})`.
2. `ids = relationships.map(n => n.id)`; if empty → `[]`.
3. (ACL context) token for `ids`.
4. `{content} = getMeasurementByIds(ids, calculated, businessPartnerIds, mustHaveRows)`.
5. Return `{content: orderBy(content, createdAt DESC)}` (client-side).
**EXT Service Calls:** **EXT** → key: `relationship` · severity: 🔴 — resolves the measurement_set ids for a resource.
**Target DGS Implementation:** `@DgsQuery getMeasurements(resourceId, businessPartnerIds, calculated, mustHaveRows): MeasurementPaged`. Call relationship via `RelationshipClient`/federation, then the service. **PO decision:** push the `createdAt DESC` sort to the backend.
**Files:** `dataFetcher/MeasurementQueryDataFetcher.kt`. **Dependencies:** A04.
**Acceptance Criteria:** 1. Resolves ids via relationship then fetches measurements. 2. No ids → `{content:[]}` (no measurement call). 3. Sorted `createdAt DESC` (location documented).
**Test Cases:** ☐ Unit: id resolution ☐ Unit: empty short-circuit ☐ Unit: sort ☐ Integration.

---

## SPARK-MEAS-C02 · getMeasurementsElastic data fetcher
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `query`

**Current Behaviour (Q3):** `{content} = search.getMeasurementSets.load({q:`parentId: ${resourceId}`})` → sort `createdAt DESC` → `{content}`.
**EXT Service Calls:** **EXT** → key: `search` · severity: 🔴 — elastic measurement-set index.
**Target DGS Implementation:** `@DgsQuery getMeasurementsElastic(resourceId): MeasurementPaged` → `searchClient.measurementSets("parentId: $resourceId")`; sort `createdAt DESC` (or backend).
**Acceptance Criteria:** 1. Returns elastic content for `parentId`. 2. Sorted `createdAt DESC`. 3. Empty → `{content:[]}`.
**Test Cases:** ☐ Unit: query build ☐ Unit: sort ☐ Integration.

---

## SPARK-MEAS-D01 · addMeasurement mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**Current Behaviour (M1):** `POST {base}/…/measurements/v1` (snake_case request, `primeKey: humanId`); on `validationErrors||message` → throw. No ACL (new resource).
**Target DGS Implementation:** `@DgsMutation addMeasurement(sparkMeasurement): Measurement` → typed `MeasurementValidationException`; prime read cache.
**Acceptance Criteria:** 1. POST creates + returns mapped `Measurement`. 2. `validationErrors`/`message` → exception. 3. Cache primed with `humanId`.
**Test Cases:** ☐ Unit: happy ☐ Unit: validation → exception ☐ Integration.

---

## SPARK-MEAS-D02 · updateMeasurementAccess mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**Current Behaviour (M4):** `PUT …/{id}/permission` body `{systemTeamIds}` **or** `{systemTeamDto}` (whichever provided). **ACL note (context):** token for `id`; ignored in DGS.
**Target DGS Implementation:** `@DgsMutation updateMeasurementAccess(measurementSetId, systemTeamIds, systemTeamDto): Measurement`. **PO decision:** adopt tagged `MeasurementAccessInput` (keep wire format).
**Acceptance Criteria:** 1. Sends `{systemTeamIds}` when provided, else `{systemTeamDto}`. 2. Returns updated measurement. 3. Input-shape decision recorded.
**Test Cases:** ☐ Unit: teamIds path ☐ Unit: dto path ☐ Integration.

---

## SPARK-MEAS-D03 · lockMeasurementSet mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**Current Behaviour (M5):** `PUT …/{id}/lock`. **ACL note (context):** token for `id`; ignored in DGS.
**Target DGS Implementation:** `@DgsMutation lockMeasurementSet(measurementSetId): Measurement`.
**Acceptance Criteria:** 1. PUT `/lock` returns locked set. 2. 404 → null.
**Test Cases:** ☐ Unit: lock ☐ Unit: 404.

---

## SPARK-MEAS-D04 · unlockMeasurementSet mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**Current Behaviour (M6):** `PUT …/{id}/unlock`. ACL note as D03.
**Target DGS Implementation:** `@DgsMutation unlockMeasurementSet(measurementSetId): Measurement`.
**Acceptance Criteria:** 1. PUT `/unlock` returns unlocked set. 2. 404 → null.
**Test Cases:** ☐ Unit: unlock ☐ Unit: 404.

---

## SPARK-MEAS-D05 · updateMeasurementComponentStatus mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**Current Behaviour (M2):** `PUT …/component_status_update` body `{productId, ids, status}`. **No ACL token** — confirm backend enforces (like BOM D05).
**Target DGS Implementation:** `@DgsMutation updateMeasurementComponentStatus(productId, ids, status): MeasurementPaged`; wrap result `{content}`.
**Acceptance Criteria:** 1. PUT sends `{productId, ids, status}` snake_case. 2. Returns `MeasurementPaged{content}`. 3. Auth decision recorded.
**Test Cases:** ☐ Unit: body shape ☐ Unit: result wrap ☐ Integration.

---

## SPARK-MEAS-D06 · putSampleMeasurementSet mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**Current Behaviour (M7):** `PUT …/sample` (`primeKey: sampleId`); token for `[measurementSetId, sampleId]`; on `validationErrors||message` → throw.
**Target DGS Implementation:** `@DgsMutation putSampleMeasurementSet(sampleMeasurementSet): SampleMeasurementSet` → typed exception; prime by `sampleId`.
**Acceptance Criteria:** 1. PUT upserts the sample set. 2. `validationErrors`/`message` → exception. 3. Cache primed by `sampleId`.
**Test Cases:** ☐ Unit: happy ☐ Unit: validation ☐ Integration.

---

## SPARK-MEAS-D07 · deleteSampleMeasurementSet mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**Current Behaviour (M8):** `DELETE …/sample/{sampleId}`. **ACL note (context):** token for `sampleId`; ignored in DGS.
**Target DGS Implementation:** `@DgsMutation deleteSampleMeasurementSet(sampleId): SampleMeasurementSet`.
**Acceptance Criteria:** 1. DELETE removes the sample set; returns the deleted/empty result. 2. 404 → null.
**Test Cases:** ☐ Unit: delete ☐ Unit: 404.

---

## SPARK-MEAS-E01 · updateMeasurement — 2-step orchestrated write
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `mutation`

**As a** DGS migration engineer **I want** `updateMeasurement` as an explicit 2-step write with a failure
strategy **so that** workspace and body updates stay consistent.
**Current Behaviour (M3):**
1. `workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations || {}`. (ACL context) token for `[humanId]`.
2. **If** add/remove workspaces → `workspaceAssociationHelper(MEASUREMENT, humanId, add, remove)`; on its `validationErrors||message` → throw. **(commits first)**
3. `measurement.updateMeasurement(sparkMeasurement)` → `PUT …/measurements/v1/{humanId}` (`omitParamsInBody`).
4. On `validationErrors||message` → throw. Return measurement.
**Risk 🟡:** 2 sequential writes, no rollback — workspace change persists if body PUT fails.
**EXT Service Calls:** **EXT** → key: `workspaceV2` · 🟡 (association).
**Target DGS Implementation:** `MeasurementUpdateOrchestrator`: workspace assoc → body PUT. **PO decision E01:** failure strategy (saga / compensation log / best-effort). Typed exception replaces shape-sniff; prime cache on success.
**Files:** `service/MeasurementUpdateOrchestrator.kt`, `MeasurementMutationDataFetcher.kt`. **Dependencies:** A04.
**Acceptance Criteria:** 1. Parity for 3 fixtures: body-only; body+workspace-add; body+workspace-remove. 2. Workspace step runs before body PUT. 3. Body PUT omits `humanId`. 4. Chosen failure strategy implemented. 5. `validationErrors`/`message` → exception.
**Test Cases:** ☐ Unit: order workspace→body ☐ Unit: no-workspace skip ☐ Unit: body-failure path ☐ Parity: 3 fixtures.

---

> **Monorepo note:** F01 is **internal** (product+measurement are the same `plm-product` subgraph); F02 is
> **true federation** (sample is a separate DGS). See [reference-federation-patterns.md §0](../scripts/reference-federation-patterns.md).

---

## SPARK-MEAS-F01 · Implement Product.measurementSets (internal, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `field-resolver`

**Current Behaviour:** product navigates to measurement sets via the relationship + getMeasurements flow.
**Target DGS Implementation:** plain `@DgsData measurementSets(...)` on the internal `Product` type (same
subgraph) reusing the C01 relationship+listing logic. **No** `@DgsEntityFetcher`/`@extends @external`.
Depends on `Product` existing (product A02), not on a separate deployment.
**Acceptance Criteria:** 1. `Product.measurementSets` resolves internally via `measurementService`. 2. no gateway hop. 3. Parity vs current product resolver.
**Test Cases:** ☐ Unit: calls measurement service ☐ Integration: `Product { measurementSets { content { id } } }` in-process ☐ Parity.

---

## SPARK-MEAS-F02 · Contribute sampleMeasurement to SampleV2 entity
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `field-resolver`

**Current Behaviour:** sample navigates to its measurement set via `getSampleMeasurement`.
**Target DGS Implementation:** `extend type SampleV2 @key(fields:"id")` with `@DgsData sampleMeasurement` → `getSampleMeasurement(sampleId)`. **BLOCKED-BY** sample domain Phase 3.
**Acceptance Criteria:** 1. `SampleV2.sampleMeasurement` resolves. 2. Parity vs current.
**Test Cases:** ☐ Integration: federated `SampleV2 { sampleMeasurement { sampleId } }`.

---

## SPARK-MEAS-G01 · Measurement field resolvers (13)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-A02, SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `field-resolver`

**Current Behaviour (field table in [02](./02-resolver-analysis.md)):** `access`/`currentUserPermissions`
(ACL — context only), `businessPartners` (loadBps), `createdBy`/`updatedBy` (`getUserByIDOrNullIfNotFound`),
`product` (PID-prefixed → internal `product.getByID`), `workspaces` (`getWorkspacesByIdsV2` or null),
`status` (`{code:statusId, description:statusName}` computed), `updatedFromResource` (switch type='sample' →
`sampleV2.getSampleById`), `measurementTemplates` (`measurementTemplate.getMeasurementTemplatesByIds(...).content`),
`sizeTemplate` (`sizeTemplate.getSizeTemplates([id])[0]`), `tightFitTemplate` (`tightFit.getTightFitByIdAndVersion({id,version})`),
`participantDetails` (`getUserGroup`).
**EXT:** 🟡 workspaceV2/sampleV2/measurementTemplate/sizeTemplate/tightFit; 🔵 vmm/user-profile.
**Target DGS Implementation:** one `@DgsData` set; sibling fields → federated references; `product` internal; `status` computed; `updatedFromResource` switch preserved (only `sample` realized).
**Files:** `dataFetcher/MeasurementFieldDataFetcher.kt`. **Dependencies:** A02, A04.
**Acceptance Criteria:** 1. All 13 fields resolve. 2. `product` null when `resourceId` not `PID*`. 3. `status` = `{statusId, statusName}`. 4. `workspaces` empty → null. 5. `updatedFromResource` resolves only for `type==='sample'`.
**Test Cases:** ☐ Unit: product PID branch ☐ Unit: status computed ☐ Unit: updatedFromResource switch ☐ Unit: empty workspaces ☐ Integration: federated `Measurement { measurementTemplates { id } }`.

---

## SPARK-MEAS-G02 · SampleMeasurementSet field resolvers (2)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-MEAS-A02, SPARK-MEAS-A04
**Labels:** `dgs-migration`, `measurement`, `field-resolver`

**Current Behaviour (`:165-174`):** `createdBy` (`getUserByIDOrNullIfNotFound`), `measurementSizeId` (`measurementSize && measurementSize.code` — computed).
**Target DGS Implementation:** 2 `@DgsData` fields.
**Acceptance Criteria:** 1. `createdBy` resolves by user id (null id → null). 2. `measurementSizeId` = `measurementSize.code`.
**Test Cases:** ☐ Unit: createdBy ☐ Unit: measurementSizeId computed.

---

## SPARK-MEAS-G03 · Test coverage & parity
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-MEAS-B01, SPARK-MEAS-C01, SPARK-MEAS-E01, SPARK-MEAS-G01
**Labels:** `dgs-migration`, `measurement`, `tests`

**Target DGS Implementation:** ≥80% unit coverage; parity fixtures for the 7 queries + 8 mutations + `updateMeasurement` 3 fixtures + the relationship path.
**Acceptance Criteria:** 1. Unit ≥80%. 2. Parity green for reads/writes incl. `getMeasurements` relationship path. 3. `updateMeasurement` failure path covered.
**Test Cases:** ☐ Parity: 15 op fixtures ☐ Unit: updateMeasurement failure ☐ Load: p95 parity for `getMeasurementByIds`, `getMeasurements`.

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `updateMeasurement` 2-step non-atomic write | Medium | Medium | E01 failure strategy | Tech Lead |
| `getMeasurements` relationship dependency 🔴 | Medium | Medium | Sequence relationship federation | Platform |
| `updateMeasurementAccess` polymorphic input | Low | Low | Tagged `MeasurementAccessInput` (D02) | Backend Eng |
| `updateMeasurementComponentStatus` no JWT | Low | Low | Confirm backend enforces | PO |
| F01 internal (same subgraph, depends on Product type); F02 federated (sample DGS) | Low | Low | Sequence F01 after product A02; F02 after sample migrates | Tech Lead |

## 5. Summary
- **Stories:** 24 (A:4 · B:5 · C:2 · D:7 · E:1 · F:2 · G:3).
- **Critical path:** A01→A02→A04→E01; A04→C01.
- **Highest risk:** `updateMeasurement` 2-step write; relationship dependency in `getMeasurements`.
- **Independent of federation:** ships before F01/F02.

---
**Phase Completed:** Phase 4 · **Domain:** `measurement`.

---
