# Phase 4: Migration Plan & Stories — Measurement

> **Domain:** `measurement` · **Target DGS:** `MeasurementService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md), [03-schema.graphql](./03-schema.graphql), [03-schema-analysis.md](./03-schema-analysis.md), [05-attribute-inventory.md](./05-attribute-inventory.md)
> **Index:** `04-stories-index.yaml`

Engineers: read *Current Behaviour → Target → Files → Acceptance → Tests*. **ACL is context-only**
(no ACL work). One operation per story; field resolvers grouped one-story-per-type.

## 1. Phases Overview
| Phase | Name | Stories |
|---|---|---|
| B | Core Reads | B01–B05 |
| C | Listing (relationship/elastic) | C01–C02 |
| D | Mutations (simple) | D01–D07 |
| E | Complex (`updateMeasurement`) | E01 |
| F | Federation Contributions | F01–F02 (BLOCKED-BY product/sample) |
| G | Field Resolvers & Tests | G01–G03 |

> **Self-contained story model.** The Netflix-DGS-on-REST framework already exists, so **every operation story below is end-to-end in a single PR**: it adds the schema (query/mutation + the GraphQL type definitions it returns), the DGS data fetcher, the Kotlin REST service method (read or write) that calls the backend, and pushes the schema change to the **Hive** registry. There is **no separate service-layer story** — the former `*Service` Kotlin-port story has been dissolved into the operation stories.

## 2. Dependency Graph
```mermaid
graph TD
  B01["B01 getMeasurementByIds\n(DGS module init in this PR)"]-->B[B01-B05 Reads]&C[C01-C02 Listing]&D[D01-D07 Mutations]&E01[E01 updateMeasurement]
  B01-->G01[G01 Measurement fields]&G02[G02 SampleSet fields]
  G01-->G03[G03 Tests]
  PROD[product Phase 3]-.->F01[F01 Product.measurementSets]
  SAMP[sample Phase 3]-.->F02[F02 SampleV2.sampleMeasurement]
```

---

## 3. Stories

---

### SPARK-MEAS-B01 · `getMeasurementByIds` data fetcher
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Fetch measurement sets by id.

> **Note — DGS Module Init (this PR only):** Creates `measurement.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: [03-schema.graphql](./03-schema.graphql).
- **Current Behaviour (Q1):** `GET {base}/…/measurements/v1?ids=&calculated=&mustHaveRows=` → camelCase. **ACL note (context):** token for `ids`; ignored in DGS.
- **Target DGS Implementation:** `@DgsQuery getMeasurementByIds(ids, calculated): MeasurementPaged` (SDL: paged `{content}`, not a bare list) → `measurementService.getByIds(ids, calculated)`. Add a `MeasurementDataLoader` keyed on id.
- **Files:** `dataFetcher/MeasurementQueryDataFetcher.kt`.

#### Acceptance Criteria

1. Returns measurements for ids with `calculated` flag forwarded.
2. Empty ids → `[]`.
3. snake→camel mapping.

---

### SPARK-MEAS-B02 · `getUnitsOfMeasure` (cacheable)
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Return the unit-of-measure lookup list (cached).

- **Current Behaviour (Q4):** `GET {base}/…/master_data/unit_of_measure[?ids=]` → `units_of_measure` camelCase.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` service method returning `[UnitOfMeasure]`.

#### Acceptance Criteria

1. Returns UoM list (optionally filtered by ids).
2. Cached.

---

### SPARK-MEAS-B03 · `getThicknessUnitsOfMeasure` (cacheable)
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Return the thickness unit-of-measure lookup (cached).

- **Current Behaviour (Q5):** `GET {base}/…/master_data/thickness_uom` → `units_of_measure`.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` returning `[UnitOfMeasure]`.

#### Acceptance Criteria

1. Returns thickness UoM list.
2. Cached.

---

### SPARK-MEAS-B04 · `getMeasurementSetStatus` (cacheable)
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Return the measurement-set status lookup (cached).

- **Current Behaviour (Q6):** `GET {base}/masterData?name=MeasurementSetStatus` → `{key:value}` map → `[{code, description}]`.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` mapping the map to the list.

#### Acceptance Criteria

1. Returns statuses.
2. Cached.
3. key→code, value→description.

---

### SPARK-MEAS-B05 · `getSampleMeasurement` data fetcher
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01, B01

- **In plain terms:** Fetch the measurement set for a sample.

- **Current Behaviour (Q7):** `GET {base}/…/measurements/v1/sample/{sampleId}` → camelCase. **ACL note (context):** token for `sampleId`; ignored in DGS.
- **Target DGS Implementation:** `@DgsQuery getSampleMeasurement(sampleId): SampleMeasurementSet` (SDL: a single object, not a list).

#### Acceptance Criteria

1. Returns the sample measurement set for `sampleId`.
2. Not found → `null`.

---

### SPARK-MEAS-C01 · `getMeasurements` data fetcher (relationship + listing)
- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B01 · **EXT:** 🔴 `relationship`

- **In plain terms:** List a resource's measurement sets (resolves the relationship first).

- **Current Behaviour (Q2):**
1. `relationships = relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0})`.
2. `ids = relationships.map(n => n.id)`; if empty → `[]`.
3. (ACL context) token for `ids`.
4. `{content} = getMeasurementByIds(ids, calculated, businessPartnerIds, mustHaveRows)`.
5. Return `{content: orderBy(content, createdAt DESC)}` (client-side).
- **EXT Service Calls:** **EXT** → key: `relationship` · severity: 🔴 — resolves the measurement_set ids for a resource.
- **Target DGS Implementation:** `@DgsQuery getMeasurements(resourceId, businessPartnerIds, calculated, mustHaveRows): MeasurementPaged`. Call relationship via `RelationshipClient`/federation, then the service. **PO decision:** push the `createdAt DESC` sort to the backend.
- **Files:** `dataFetcher/MeasurementQueryDataFetcher.kt`.

#### Acceptance Criteria

1. Resolves ids via relationship then fetches measurements.
2. No ids → `{content:[]}` (no measurement call).
3. Sorted `createdAt DESC` (location documented).

---

### SPARK-MEAS-C02 · `getMeasurementsElastic` data fetcher
- **Type:** Query · **Phase:** C · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01 · **EXT:** 🔴 `search`

- **In plain terms:** Search a product's measurement sets via elastic.

- **Current Behaviour (Q3):** `{content} = search.getMeasurementSets.load({q:`parentId: ${resourceId}`})` → sort `createdAt DESC` → `{content}`.
- **EXT Service Calls:** **EXT** → key: `search` · severity: 🔴 — elastic measurement-set index.
- **Target DGS Implementation:** `@DgsQuery getMeasurementsElastic(resourceId): MeasurementPaged` → `searchClient.measurementSets("parentId: $resourceId")`; sort `createdAt DESC` (or backend).

#### Acceptance Criteria

1. Returns elastic content for `parentId`.
2. Sorted `createdAt DESC`.
3. Empty → `{content:[]}`.

---

### SPARK-MEAS-D01 · `addMeasurement` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Create a measurement set.

- **Current Behaviour (M1):** `POST {base}/…/measurements/v1` (snake_case request, `primeKey: humanId`); on `validationErrors||message` → throw. No ACL (new resource).
- **Target DGS Implementation:** `@DgsMutation addMeasurement(sparkMeasurement): Measurement` → typed `MeasurementValidationException`; prime read cache.

#### Acceptance Criteria

1. POST creates + returns mapped `Measurement`.
2. `validationErrors`/`message` → exception.
3. Cache primed with `humanId`.

---

### SPARK-MEAS-D02 · `updateMeasurementAccess` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Change who can access a measurement set.

- **Current Behaviour (M4):** `PUT …/{id}/permission` body `{systemTeamIds}` **or** `{systemTeamDto}` (whichever provided). **ACL note (context):** token for `id`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation updateMeasurementAccess(measurementSetId, systemTeamIds, systemTeamDto): Measurement`. **PO decision:** adopt tagged `MeasurementAccessInput` (keep wire format).

#### Acceptance Criteria

1. Sends `{systemTeamIds}` when provided, else `{systemTeamDto}`.
2. Returns updated measurement.
3. Input-shape decision recorded.

---

### SPARK-MEAS-D03 · `lockMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Lock a measurement set from edits.

- **Current Behaviour (M5):** `PUT …/{id}/lock`. **ACL note (context):** token for `id`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation lockMeasurementSet(measurementSetId): Measurement`.

#### Acceptance Criteria

1. PUT `/lock` returns locked set.
2. 404 → null.

---

### SPARK-MEAS-D04 · `unlockMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Unlock a measurement set.

- **Current Behaviour (M6):** `PUT …/{id}/unlock`. ACL note as D03.
- **Target DGS Implementation:** `@DgsMutation unlockMeasurementSet(measurementSetId): Measurement`.

#### Acceptance Criteria

1. PUT `/unlock` returns unlocked set.
2. 404 → null.

---

### SPARK-MEAS-D05 · `updateMeasurementComponentStatus` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Update the component status on measurement sets.

- **Current Behaviour (M2):** `PUT …/component_status_update` body `{productId, ids, status}`. **No ACL token** — confirm backend enforces (like BOM D05).
- **Target DGS Implementation:** `@DgsMutation updateMeasurementComponentStatus(productId, ids, status): MeasurementPaged`; wrap result `{content}`.

#### Acceptance Criteria

1. PUT sends `{productId, ids, status}` snake_case.
2. Returns `MeasurementPaged{content}`.
3. Auth decision recorded.

---

### SPARK-MEAS-D06 · `putSampleMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Create or replace a sample's measurement set.

- **Current Behaviour (M7):** `PUT …/sample` (`primeKey: sampleId`); token for `[measurementSetId, sampleId]`; on `validationErrors||message` → throw.
- **Target DGS Implementation:** `@DgsMutation putSampleMeasurementSet(sampleMeasurementSet): SampleMeasurementSet` → typed exception; prime by `sampleId`.

#### Acceptance Criteria

1. PUT upserts the sample set.
2. `validationErrors`/`message` → exception.
3. Cache primed by `sampleId`.

---

### SPARK-MEAS-D07 · `deleteSampleMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01

- **In plain terms:** Delete a sample's measurement set.

- **Current Behaviour (M8):** `DELETE …/sample/{sampleId}`. **ACL note (context):** token for `sampleId`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation deleteSampleMeasurementSet(sampleId): SampleMeasurementSet`.

#### Acceptance Criteria

1. DELETE removes the sample set; returns the deleted/empty result.
2. 404 → null.

---

### SPARK-MEAS-E01 · `updateMeasurement` — 2-step orchestrated write
- **Type:** Mutation · **Phase:** E · **Complexity:** 🔶 High · **Category:** CAT-2 · **Depends on:** B01 · **EXT:** 🟡 `workspaceV2`

- **In plain terms:** Edit a measurement set — a 2-step write (workspace + body) that has no rollback today.

- **As a** DGS migration engineer **I want** `updateMeasurement` as an explicit 2-step write with a failure
strategy **so that** workspace and body updates stay consistent.
- **Current Behaviour (M3):**
1. `workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations || {}`. (ACL context) token for `[humanId]`.
2. **If** add/remove workspaces → `workspaceAssociationHelper(MEASUREMENT, humanId, add, remove)`; on its `validationErrors||message` → throw. **(commits first)**
3. `measurement.updateMeasurement(sparkMeasurement)` → `PUT …/measurements/v1/{humanId}` (`omitParamsInBody`).
4. On `validationErrors||message` → throw. Return measurement.
- **Risk 🟡:** 2 sequential writes, no rollback — workspace change persists if body PUT fails.
- **EXT Service Calls:** **EXT** → key: `workspaceV2` · 🟡 (association).
- **Target DGS Implementation:** `MeasurementUpdateOrchestrator`: workspace assoc → body PUT. **PO decision E01:** failure strategy (saga / compensation log / best-effort). Typed exception replaces shape-sniff; prime cache on success.
- **Files:** `service/MeasurementUpdateOrchestrator.kt`, `MeasurementMutationDataFetcher.kt`.

#### Acceptance Criteria

1. Parity for 3 fixtures: body-only; body+workspace-add; body+workspace-remove.
2. Workspace step runs before body PUT.
3. Body PUT omits `humanId`.
4. Chosen failure strategy implemented.
5. `validationErrors`/`message` → exception.

#### Test Cases

- [ ] Unit: order workspace→body
- [ ] Unit: no-workspace skip
- [ ] Unit: body-failure path
- [ ] Parity: 3 fixtures

---

> **Monorepo note:** F01 is **internal** (product+measurement are the same `plm-product` subgraph); F02 is
> **true federation** (sample is a separate DGS). See [reference-federation-patterns.md §0](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

---

### SPARK-MEAS-F01 · Implement `Product.measurementSets` (internal)
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B01 · **EXT:** 🔴 `relationship`

- **In plain terms:** Expose a product's measurement sets on the Product type.

- **Current Behaviour:** product navigates to measurement sets via the relationship + getMeasurements flow.
- **Target DGS Implementation:** plain `@DgsData measurementSets(...)` on the internal `Product` type (same
subgraph) reusing the C01 relationship+listing logic. **No** `@DgsEntityFetcher`/`@extends @external`.
Depends on `Product` existing (product A02), not on a separate deployment.

#### Acceptance Criteria

1. `Product.measurementSets` resolves internally via `measurementService`.
2. no gateway hop.
3. Parity vs current product resolver.

---

### SPARK-MEAS-F02 · Contribute `sampleMeasurement` to the `SampleV2` entity
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** B01 · **Blocked by:** sample

- **In plain terms:** Contribute a sample's measurement set to the Sample entity.

- **Current Behaviour:** sample navigates to its measurement set via `getSampleMeasurement`.
- **Target DGS Implementation:** `extend type SampleV2 @key(fields:"id")` with `@DgsData sampleMeasurement` → `getSampleMeasurement(sampleId)`. **BLOCKED-BY** sample domain Phase 3.

#### Acceptance Criteria

1. `SampleV2.sampleMeasurement` resolves.
2. Parity vs current.

---

### SPARK-MEAS-G01 · `Measurement` field resolvers (13 fields)
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B01, B01 · **EXT:** 🟡 `workspaceV2` · 🟡 `sampleV2` · 🟡 `measurementTemplate` · 🟡 `sizeTemplate` · 🟡 `tightFit` · 🔵 `vmm` · 🔵 `userAttributes`

- **In plain terms:** Resolve the everyday measurement fields (people, product, partners).

- **Current Behaviour (field table in [02](./02-resolver-analysis.md)):** `access`/`currentUserPermissions`
(ACL — context only), `businessPartners` (loadBps), `createdBy`/`updatedBy` (`getUserByIDOrNullIfNotFound`),
`product` (PID-prefixed → internal `product.getByID`), `workspaces` (`getWorkspacesByIdsV2` or null),
`status` (`{code:statusId, description:statusName}` computed), `updatedFromResource` (switch type='sample' →
`sampleV2.getSampleById`), `measurementTemplates` (`measurementTemplate.getMeasurementTemplatesByIds(...).content`),
`sizeTemplate` (`sizeTemplate.getSizeTemplates([id])[0]`), `tightFitTemplate` (`tightFit.getTightFitByIdAndVersion({id,version})`),
`participantDetails` (`getUserGroup`).
- **EXT:** 🟡 workspaceV2/sampleV2/measurementTemplate/sizeTemplate/tightFit; 🔵 vmm/user-profile.
- **Target DGS Implementation:** one `@DgsData` set; sibling fields → federated references; `product` internal; `status` computed; `updatedFromResource` switch preserved (only `sample` realized).
- **Files:** `dataFetcher/MeasurementFieldDataFetcher.kt`.

#### Acceptance Criteria

1. All 13 fields resolve.
2. `product` null when `resourceId` not `PID*`.
3. `status` = `{statusId, statusName}`.
4. `workspaces` empty → null.
5. `updatedFromResource` resolves only for `type==='sample'`.

---

### SPARK-MEAS-G02 · `SampleMeasurementSet` field resolvers (2 fields)
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B01, B01 · **EXT:** 🔵 `userAttributes`

- **In plain terms:** Resolve the sample-measurement-set fields.

- **Current Behaviour (`:165-174`):** `createdBy` (`getUserByIDOrNullIfNotFound`), `measurementSizeId` (`measurementSize && measurementSize.code` — computed).
- **Target DGS Implementation:** 2 `@DgsData` fields.

#### Acceptance Criteria

1. `createdBy` resolves by user id (null id → null).
2. `measurementSizeId` = `measurementSize.code`.

---

### SPARK-MEAS-G03 · Test coverage & parity
- **Type:** Tests · **Phase:** G · **Complexity:** Medium · **Category:** CAT-5 · **Depends on:** B01, C01, E01, G01

- **In plain terms:** Prove the measurement subgraph matches the old gateway.

- **Target DGS Implementation:** ≥80% unit coverage; parity fixtures for the 7 queries + 8 mutations + `updateMeasurement` 3 fixtures + the relationship path.

#### Acceptance Criteria

1. Unit ≥80%.
2. Parity green for reads/writes incl. `getMeasurements` relationship path.
3. `updateMeasurement` failure path covered.

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
- **Stories:** 20 (B:5 · C:2 · D:7 · E:1 · F:2 · G:3).
- **Critical path:** E01; C01.
- **Highest risk:** `updateMeasurement` 2-step write; relationship dependency in `getMeasurements`.
- **Independent of federation:** ships before F01/F02.

---
- **Phase Completed:** Phase 4 · **Domain:** `measurement`.
