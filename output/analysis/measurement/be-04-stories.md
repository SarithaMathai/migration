# Phase 4: Migration Plan & Stories — Measurement

> **Domain:** `measurement` · **Target DGS:** `MeasurementService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md), [be-03-schema.graphql](./be-03-schema.graphql), [be-03-schema-analysis.md](./be-03-schema-analysis.md), [be-05-attribute-inventory.md](./be-05-attribute-inventory.md)
> **Index:** `be-04-stories-index.yaml`

Engineers: read *Current Behaviour → Target → Files → Acceptance → Tests*. **ACL is context-only**
(no ACL work). One operation per story; field resolvers grouped one-story-per-type.

## 1. Phases Overview
| Phase | Name | Stories |
|---|---|---|
| B | Core Reads | B-01–B-05 |
| C | Listing (relationship/elastic) | C-01–C-02 |
| D | Mutations (simple) | D-01–D-07 |
| E | Complex (`updateMeasurement`) | E-01 |
| F | Federation Contributions | F-01–F-02 (BLOCKED-BY product/sample) |
| G | Field Resolvers & Tests | G-01–G-04 (G-04 recommended, PO-gated — federation review) |

> **Self-contained story model.** The Netflix-DGS-on-REST framework already exists, so **every operation story below is end-to-end in a single PR**: it adds the schema (query/mutation + the GraphQL type definitions it returns), the DGS data fetcher, the Kotlin REST service method (read or write) that calls the backend, and pushes the schema change to the **Hive** registry. There is **no separate service-layer story** — the former `*Service` Kotlin-port story has been dissolved into the operation stories.

## 2. Dependency Graph
```mermaid
graph TD
  B01["B-01 getMeasurementByIds\n(DGS module init in this PR)"]-->B[B-01-B-05 Reads]&C[C-01-C-02 Listing]&D[D-01-D-07 Mutations]&E01[E-01 updateMeasurement]
  B01-->G01[G-01 Measurement fields]&G02[G-02 SampleSet fields]
  G01-->G03[G-03 Tests]
  PROD[product Phase 3]-.->F01[F-01 Product.measurementSets]
  SAMP[sample Phase 3]-.->F02[F-02 SampleV2.sampleMeasurement]
```

---

## 3. Stories

---

### MST-BE-B-01 · `getMeasurementByIds` data fetcher
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Fetch measurement sets by id.

> **Note — DGS Module Init (this PR only):** Creates `measurement.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: [be-03-schema.graphql](./be-03-schema.graphql).
- **Current Behaviour (Q1):** `GET {base}/…/measurements/v1?ids=&calculated=&mustHaveRows=` → camelCase. **ACL note (context):** token for `ids`; ignored in DGS.
- **Target DGS Implementation:** `@DgsQuery getMeasurementByIds(ids, calculated): MeasurementPaged` (SDL: paged `{content}`, not a bare list) → `measurementService.getByIds(ids, calculated)`. Add a `MeasurementDataLoader` keyed on id.
- **Files:** `dataFetcher/MeasurementQueryDataFetcher.kt`.

#### Acceptance Criteria

1. Returns measurements for ids with `calculated` flag forwarded.
2. Empty ids → `[]`.
3. snake→camel mapping.

---

### MST-BE-B-02 · `getUnitsOfMeasure` (cacheable)
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the unit-of-measure lookup list (cached).

- **Current Behaviour (Q4):** `GET {base}/…/master_data/unit_of_measure[?ids=]` → `units_of_measure` camelCase.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` service method returning `[UnitOfMeasure]`.

#### Acceptance Criteria

1. Returns UoM list (optionally filtered by ids).
2. Cached.

---

### MST-BE-B-03 · `getThicknessUnitsOfMeasure` (cacheable)
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the thickness unit-of-measure lookup (cached).

- **Current Behaviour (Q5):** `GET {base}/…/master_data/thickness_uom` → `units_of_measure`.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` returning `[UnitOfMeasure]`.

#### Acceptance Criteria

1. Returns thickness UoM list.
2. Cached.

---

### MST-BE-B-04 · `getMeasurementSetStatus` (cacheable)
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the measurement-set status lookup (cached).

- **Current Behaviour (Q6):** `GET {base}/masterData?name=MeasurementSetStatus` → `{key:value}` map → `[{code, description}]`.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` mapping the map to the list.

#### Acceptance Criteria

1. Returns statuses.
2. Cached.
3. key→code, value→description.

---

### MST-BE-B-05 · `getSampleMeasurement` data fetcher
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01, B-01

- **In plain terms:** Fetch the measurement set for a sample.

- **Current Behaviour (Q7):** `GET {base}/…/measurements/v1/sample/{sampleId}` → camelCase. **ACL note (context):** token for `sampleId`; ignored in DGS.
- **Target DGS Implementation:** `@DgsQuery getSampleMeasurement(sampleId): SampleMeasurementSet` (SDL: a single object, not a list).

#### Acceptance Criteria

1. Returns the sample measurement set for `sampleId`.
2. Not found → `null`.

---

### MST-BE-C-01 · `getMeasurements` data fetcher (relationship + listing)
- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `relationship`

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

### MST-BE-C-02 · `getMeasurementsElastic` data fetcher
- **Type:** Query · **Phase:** C · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search`

- **In plain terms:** Search a product's measurement sets via elastic.

- **Current Behaviour (Q3):** `{content} = search.getMeasurementSets.load({q:`parentId: ${resourceId}`})` → sort `createdAt DESC` → `{content}`.
- **EXT Service Calls:** **EXT** → key: `search` · severity: 🔴 — elastic measurement-set index.
- **Target DGS Implementation:** `@DgsQuery getMeasurementsElastic(resourceId): MeasurementPaged` → `searchClient.measurementSets("parentId: $resourceId")`; sort `createdAt DESC` (or backend).

#### Acceptance Criteria

1. Returns elastic content for `parentId`.
2. Sorted `createdAt DESC`.
3. Empty → `{content:[]}`.

---

### MST-BE-D-01 · `addMeasurement` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Create a measurement set.

- **Current Behaviour (M1):** `POST {base}/…/measurements/v1` (snake_case request, `primeKey: humanId`); on `validationErrors||message` → throw. No ACL (new resource).
- **Target DGS Implementation:** `@DgsMutation addMeasurement(sparkMeasurement): Measurement` → typed `MeasurementValidationException`; prime read cache.

#### Acceptance Criteria

1. POST creates + returns mapped `Measurement`.
2. `validationErrors`/`message` → exception.
3. Cache primed with `humanId`.

---

### MST-BE-D-02 · `updateMeasurementAccess` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Change who can access a measurement set.

- **Current Behaviour (M4):** `PUT …/{id}/permission` body `{systemTeamIds}` **or** `{systemTeamDto}` (whichever provided). **ACL note (context):** token for `id`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation updateMeasurementAccess(measurementSetId, systemTeamIds, systemTeamDto): Measurement`. **PO decision:** adopt tagged `MeasurementAccessInput` (keep wire format).

#### Acceptance Criteria

1. Sends `{systemTeamIds}` when provided, else `{systemTeamDto}`.
2. Returns updated measurement.
3. Input-shape decision recorded.

---

### MST-BE-D-03 · `lockMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Lock a measurement set from edits.

- **Current Behaviour (M5):** `PUT …/{id}/lock`. **ACL note (context):** token for `id`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation lockMeasurementSet(measurementSetId): Measurement`.

#### Acceptance Criteria

1. PUT `/lock` returns locked set.
2. 404 → null.

---

### MST-BE-D-04 · `unlockMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Unlock a measurement set.

- **Current Behaviour (M6):** `PUT …/{id}/unlock`. ACL note as D-03.
- **Target DGS Implementation:** `@DgsMutation unlockMeasurementSet(measurementSetId): Measurement`.

#### Acceptance Criteria

1. PUT `/unlock` returns unlocked set.
2. 404 → null.

---

### MST-BE-D-05 · `updateMeasurementComponentStatus` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Update the component status on measurement sets.

- **Current Behaviour (M2):** `PUT …/component_status_update` body `{productId, ids, status}`. **No ACL token** — confirm backend enforces (like BOM D-05).
- **Target DGS Implementation:** `@DgsMutation updateMeasurementComponentStatus(productId, ids, status): MeasurementPaged`; wrap result `{content}`.

#### Acceptance Criteria

1. PUT sends `{productId, ids, status}` snake_case.
2. Returns `MeasurementPaged{content}`.
3. Auth decision recorded.

---

### MST-BE-D-06 · `putSampleMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Create or replace a sample's measurement set.

- **Current Behaviour (M7):** `PUT …/sample` (`primeKey: sampleId`); token for `[measurementSetId, sampleId]`; on `validationErrors||message` → throw.
- **Target DGS Implementation:** `@DgsMutation putSampleMeasurementSet(sampleMeasurementSet): SampleMeasurementSet` → typed exception; prime by `sampleId`.

#### Acceptance Criteria

1. PUT upserts the sample set.
2. `validationErrors`/`message` → exception.
3. Cache primed by `sampleId`.

---

### MST-BE-D-07 · `deleteSampleMeasurementSet` mutation
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Delete a sample's measurement set.

- **Current Behaviour (M8):** `DELETE …/sample/{sampleId}`. **ACL note (context):** token for `sampleId`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation deleteSampleMeasurementSet(sampleId): SampleMeasurementSet`.

#### Acceptance Criteria

1. DELETE removes the sample set; returns the deleted/empty result.
2. 404 → null.

---

### MST-BE-E-01 · `updateMeasurement` — 2-step orchestrated write
- **Type:** Mutation · **Phase:** E · **Complexity:** 🔶 High · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🟡 `workspaceV2`

> **Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — draft ADR-013, ratification pending.** This is the program's **pilot** saga adoption (smallest real case, ADR-013 §5 build order): workspace assoc `COMPENSATE` → body PUT = point of no return; injected step-2 failure must yield `COMPENSATED` (set not moved) with per-step detail.

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
- **Target DGS Implementation:** `MeasurementUpdateOrchestrator`: workspace assoc → body PUT. **PO decision E-01:** failure strategy (saga / compensation log / best-effort). Typed exception replaces shape-sniff; prime cache on success.
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

> **Monorepo note:** F-01 is **internal** (product+measurement are the same `plm-product` subgraph); F-02 is
> **true federation** (sample is a separate DGS). See [reference-federation-patterns.md §0](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

---

### MST-BE-F-01 · Implement `Product.measurementSets` (internal)
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `relationship`

- **In plain terms:** Expose a product's measurement sets on the Product type.

- **Current Behaviour:** product navigates to measurement sets via the relationship + getMeasurements flow.
- **Target DGS Implementation:** plain `@DgsData measurementSets(...)` on the internal `Product` type (same
subgraph) reusing the C-01 relationship+listing logic. **No** `@DgsEntityFetcher`/`@extends @external`.
Depends on `Product` existing (product A-02), not on a separate deployment.

#### Acceptance Criteria

1. `Product.measurementSets` resolves internally via `measurementService`.
2. no gateway hop.
3. Parity vs current product resolver.

---

### MST-BE-F-02 · Contribute `sampleMeasurement` to the `SampleV2` entity
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** B-01 · **Blocked by:** sample

- **In plain terms:** Contribute a sample's measurement set to the Sample entity.

- **Current Behaviour:** sample navigates to its measurement set via `getSampleMeasurement`.
- **Target DGS Implementation:** `extend type SampleV2 @key(fields:"id")` with `@DgsData sampleMeasurement` → `getSampleMeasurement(sampleId)`. **BLOCKED-BY** sample domain Phase 3.

#### Acceptance Criteria

1. `SampleV2.sampleMeasurement` resolves.
2. Parity vs current.

---

### MST-BE-G-01 · `Measurement` field resolvers (13 fields)
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01, B-01 · **EXT:** 🟡 `workspaceV2` · 🟡 `sampleV2` · 🟡 `measurementTemplate` · 🟡 `sizeTemplate` · 🟡 `tightFit` · 🔵 `vmm` · 🔵 `userAttributes`

- **In plain terms:** Resolve the everyday measurement fields (people, product, partners).

- **Current Behaviour (field table in [02](./be-02-resolver-analysis.md)):** `access`/`currentUserPermissions`
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

### MST-BE-G-02 · `SampleMeasurementSet` field resolvers (2 fields)
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01, B-01 · **EXT:** 🔵 `userAttributes`

- **In plain terms:** Resolve the sample-measurement-set fields.

- **Current Behaviour (`:165-174`):** `createdBy` (`getUserByIDOrNullIfNotFound`), `measurementSizeId` (`measurementSize && measurementSize.code` — computed).
- **Target DGS Implementation:** 2 `@DgsData` fields.

#### Acceptance Criteria

1. `createdBy` resolves by user id (null id → null).
2. `measurementSizeId` = `measurementSize.code`.

---

### MST-BE-G-03 · Test coverage & parity
- **Type:** Tests · **Phase:** G · **Complexity:** Medium · **Category:** CAT-5 · **Depends on:** B-01, C-01, E-01, G-01

- **In plain terms:** Prove the measurement subgraph matches the old gateway.

- **Target DGS Implementation:** ≥80% unit coverage; parity fixtures for the 7 queries + 8 mutations + `updateMeasurement` 3 fixtures + the relationship path.

#### Acceptance Criteria

1. Unit ≥80%.
2. Parity green for reads/writes incl. `getMeasurements` relationship path.
3. `updateMeasurement` failure path covered.

---

### MST-BE-G-04 · `SampleMeasurementSet.sample` forward reference (recommended, PO-gated)
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-02 (carries B-05 `getSampleMeasurement`, grouped-XS merged) · **EXT:** 🟡 `sample`
- **Status:** Recommended (PO-gated — federation-review/03 §2 REC-4)

- **In plain terms:** Adds `sample { … }` on the sample measurement set — the forward twin of the existing
reverse extension (`SampleV2.sampleMeasurement`, **MST-BE-F-02**).

- **Context:** `SampleMeasurementSet` is keyed on `sampleId` but exposes no way to walk to the sample entity;
sample screens re-query by id today. `sampleId` stays — it is the `@key`.
- **Target DGS Implementation:** schema adds `sample: SampleV2` on `SampleMeasurementSet`; resolver emits
`{id: sampleId}` — zero extra backend calls; hydrated by the sample subgraph (phase 2; stitched gateway
until then).

#### Acceptance Criteria

1. PO approval recorded (OQ-5) before implementation starts.
2. `sample { id }` resolves as a stub; `sampleId` unchanged.
3. Pairs cleanly with MST-BE-F-02 (no circular resolution at the gateway — verified by a two-hop smoke query).

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `updateMeasurement` 2-step non-atomic write | Medium | Medium | E-01 failure strategy | Tech Lead |
| `getMeasurements` relationship dependency 🔴 | Medium | Medium | Sequence relationship federation | Platform |
| `updateMeasurementAccess` polymorphic input | Low | Low | Tagged `MeasurementAccessInput` (D-02) | Backend Eng |
| `updateMeasurementComponentStatus` no JWT | Low | Low | Confirm backend enforces | PO |
| F-01 internal (same subgraph, depends on Product type); F-02 federated (sample DGS) | Low | Low | Sequence F-01 after product A-02; F-02 after sample migrates | Tech Lead |

## 5. Summary
- **Stories:** 21 (B:5 · C:2 · D:7 · E:1 · F:2 · G:4). G-04 (recommended, PO-gated) added by the federation review.
- **Critical path:** E-01; C-01.
- **Highest risk:** `updateMeasurement` 2-step write; relationship dependency in `getMeasurements`.
- **Independent of federation:** ships before F-01/F-02.

---
- **Phase Completed:** Phase 4 · **Domain:** `measurement`.
