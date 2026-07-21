# Measurement — Comprehensive Migration Documentation

> **Domain:** `measurement` · **Target DGS:** `plm-product (co-located)` · **Generated:** 2026-07-19
> **Confluence location:** *Federation Graph Migration ▸ Domains ▸ measurement*

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Migration Scope](#migration-scope)
- [Story Summary by Phase](#story-summary-by-phase)
- [Decisions Required](#decisions-required)
- [Recommended Sprint Sequencing](#recommended-sprint-sequencing)
- [Capacity Planning](#capacity-planning)
- [All Stories — Detailed Engineering Breakdown](#all-stories--detailed-engineering-breakdown)
  - [Phase B — Core Reads](#phase-b--core-reads)
  - [Phase C — Search & Listing](#phase-c--search-listing)
  - [Phase D — Mutations (Simple)](#phase-d--mutations-simple)
  - [Phase E — Complex Operations](#phase-e--complex-operations)
  - [Phase F — Federation & Stitching](#phase-f--federation-stitching)
  - [Phase G — Field Resolvers, Bug-fixes & Tests](#phase-g--field-resolvers-bug-fixes-tests)
  - [Phase H — Phase H](#phase-h--phase-h)
- [Story Reference Table](#story-reference-table)

---

## Executive Summary

- We are moving the **Measurement** domain — measurement sets (the size/point-of-measure specs for a product), their sample measurements, and the master-data unit lists — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **mid-sized and mid-low risk**: 7 queries, 8 mutations, 15 field resolvers on a 175-line resolver, with **no polymorphism**.
- The one genuinely harder piece is `updateMeasurement`, a 2-step write (workspace association, then body) with no rollback today.

`getMeasurements` depends on the **relationship** service to find a product's measurement-set ids, and the
template/size/tight-fit references are **separate sibling domains** we only reference (not migrate here).

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); measurement has zero downstream-token sites.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 3 cacheable master-data |
| Mutations | 8 | 6 simple + `updateMeasurement` (2-step) + add |
| Field-resolver type blocks | 2 | `Measurement` (13), `SampleMeasurementSet` (2) |
| External dependencies | 11 keys (2 🔴 · 6 🟡 · 3 🔵) | relationship/search 🔴; templates 🟡 |
| Federation contributions | 2 (Product, SampleV2) | BLOCKED-BY product/sample |
| **Total stories** | **20** | green-field |

---

## Story Summary by Phase

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 5 | 5–9d |
| C | Listing | 2 | 4–7d |
| D | Mutations (simple) | 7 | 8–14d |
| E | Complex (`updateMeasurement`) | 1 | 4–7d |
| F | Federation | 2 | 3–5d (BLOCKED-BY product/sample) |
| G | Field Resolvers & Tests | 3 | 8–13d |
| **Total** | | **20** | **32–55d** (buffered) |

> One engineer ≈ **7–11 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

---

## Decisions Required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateMeasurement` failure strategy | E-01 | Tech Lead + PO |
| 2 | `updateMeasurementComponentStatus` no auth token — backend-enforced? | D-05 | PO |
| 3 | Adopt tagged `MeasurementAccessInput`? | D-02 | Product Owner |
| 4 | Push `getMeasurements`/`getMeasurementsElastic` sort to backend? | C-01/C-02 | Backend Eng |
| 5 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-04 | listing + simple mutations |
| 3 | D-05–D-07 + E-01 | remaining mutations + `updateMeasurement` |
| 4 | G-01–G-02, G-04 | field resolvers (G-04 recommended, PO-gated). Test coverage/parity tracked outside this Jira pipeline, created manually. |
| post-launch | F-01, H-01 | federation contributions |

---

## Capacity Planning

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~8–14 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel |
| 3 engineers | ~4–6 sprints | critical path A → E-01 → G-01 → G-04 |

---
*Pipeline 2.0 — Phase 4 complete. Measurement artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*

---

## All Stories — Detailed Engineering Breakdown

> Each story is self-contained. Read: **Current Behaviour → Target → Acceptance Criteria**.
> Test cases are included only for **High** and **Very High** complexity stories.

### Phases Overview

| Phase | Name | Stories |
|---|---|---|
| B | Core Reads | B-01–B-05 (measurement) + B-06–B-09 (sub-domains: measurementTemplate, sizeTemplate, tightFit, sizes) |
| C | Listing (relationship/elastic) | C-01–C-02 |
| D | Mutations (simple) | D-01–D-07 (measurement) + D-08–D-10 (sub-domains) |
| E | Complex (`updateMeasurement`) | E-01 |
| F | Federation Contributions (internal) | F-01 |
| G | Field Resolvers | G-01–G-02, G-04 (measurement) + G-05–G-07 (sub-domains: MeasurementTemplate, SizeTemplate, TightFit) (G-04 recommended, PO-gated — federation review) |
| H | Entity Resolution — cross-subgraph contribution (BLOCKED-BY sample) | H-01 |

> **Self-contained story model.** The Netflix-DGS-on-REST framework already exists, so **every operation story below is end-to-end in a single PR**: it adds the schema (query/mutation + the GraphQL type definitions it returns), the DGS data fetcher, the Kotlin REST service method (read or write) that calls the backend, and pushes the schema change to the **Hive** registry. There is **no separate service-layer story** — the former `*Service` Kotlin-port story has been dissolved into the operation stories.

---

### Phase B — Core Reads

#### MST-BE-B-01 · `getMeasurementByIds` data fetcher

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Fetch measurement sets by id.

> **Note — DGS Module Init (this PR only):** Creates `measurement.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.
- **Current Behaviour (Q1):** `GET {base}/…/measurements/v1?ids=&calculated=&mustHaveRows=` → camelCase. **ACL note (context):** token for `ids`; ignored in DGS.
- **Target DGS Implementation:** `@DgsQuery getMeasurementByIds(ids, calculated): MeasurementPaged` (SDL: paged `{content}`, not a bare list) → `measurementService.getByIds(ids, calculated)`. Add a `MeasurementDataLoader` keyed on id.
- **Files:** `dataFetcher/MeasurementQueryDataFetcher.kt`.

**Acceptance Criteria:**

1. Returns measurements for ids with `calculated` flag forwarded
2. Empty ids → `[]`
3. snake→camel mapping

---

#### MST-BE-B-02 · `getUnitsOfMeasure` (cacheable)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the unit-of-measure lookup list (cached).

- **Current Behaviour (Q4):** `GET {base}/…/master_data/unit_of_measure[?ids=]` → `units_of_measure` camelCase.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` service method returning `[UnitOfMeasure]`.

**Acceptance Criteria:**

1. Returns UoM list (optionally filtered by ids)
2. Cached

---

#### MST-BE-B-03 · `getThicknessUnitsOfMeasure` (cacheable)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the thickness unit-of-measure lookup (cached).

- **Current Behaviour (Q5):** `GET {base}/…/master_data/thickness_uom` → `units_of_measure`.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` returning `[UnitOfMeasure]`.

**Acceptance Criteria:**

1. Returns thickness UoM list
2. Cached

---

#### MST-BE-B-04 · `getMeasurementSetStatus` (cacheable)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the measurement-set status lookup (cached).

- **Current Behaviour (Q6):** `GET {base}/masterData?name=MeasurementSetStatus` → `{key:value}` map → `[{code, description}]`.
- **Target DGS Implementation:** `@DgsQuery` → `@Cacheable` mapping the map to the list.

**Acceptance Criteria:**

1. Returns statuses
2. Cached
3. key→code, value→description

---

#### MST-BE-B-05 · `getSampleMeasurement` data fetcher

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01, B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01, B-01

- **In plain terms:** Fetch the measurement set for a sample.

- **Current Behaviour (Q7):** `GET {base}/…/measurements/v1/sample/{sampleId}` → camelCase. **ACL note (context):** token for `sampleId`; ignored in DGS.
- **Target DGS Implementation:** `@DgsQuery getSampleMeasurement(sampleId): SampleMeasurementSet` (SDL: a single object, not a list).

**Acceptance Criteria:**

1. Returns the sample measurement set for `sampleId`
2. Not found → `null`

---

#### MST-BE-B-06 · `getMeasurementTemplates` + `getMeasurementTemplatesByIds` data fetchers

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** List or look up measurement templates.

- **Current Behaviour (Q8/Q9):** `getMeasurementTemplates(page, size)` → `GET {base}/…/measurement/templates/v1?…&sort=createdAt,desc` (falsy params stripped, array params comma-joined) → camelCase, paged. `getMeasurementTemplatesByIds(ids)` → `GET {base}/…/measurement/templates/v1?ids=` → camelCase, paged.
- **Target DGS Implementation:** `@DgsQuery getMeasurementTemplates(page, size): MeasurementTemplatesPaged`; `@DgsQuery getMeasurementTemplatesByIds(ids): MeasurementTemplatesPaged` → `measurementTemplateService.getTemplates(...)` / `getByIds(ids)`.
- **Files:** `dataFetcher/MeasurementTemplateQueryDataFetcher.kt`.

**Acceptance Criteria:**

1. `getMeasurementTemplates` returns a sorted, paged list honoring `page`/`size`
2. `getMeasurementTemplatesByIds` returns templates for the given ids
3. Empty ids → empty paged content

---

#### MST-BE-B-07 · `getSizeTemplates` + `getSizeCategories` + `getMaterialTypes` data fetchers

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Look up size templates and their master-data lookups (size category, material type).

- **Current Behaviour (Q10/Q11/Q12):** `getSizeTemplates(ids)` → `POST {base}/…/size_templates/v1/search` (id+version pairs) → camelCase. `getSizeCategories(ids)` → `GET {masterDataBase}/size_category[?ids=]` → `size_categories` camelCase (*cacheable*). `getMaterialTypes(ids)` → `GET {masterDataBase}/material_type[?ids=]` → `material_types` camelCase (*cacheable*).
- **Target DGS Implementation:** `@DgsQuery getSizeTemplates(ids: [VersionableIdInput]!): [SizeTemplate]`; `@DgsQuery getSizeCategories(ids): [CodeDescription]` and `getMaterialTypes(ids): [CodeDescription]` → `@Cacheable` service methods.
- **Files:** `dataFetcher/SizeTemplateQueryDataFetcher.kt`.

**Acceptance Criteria:**

1. `getSizeTemplates` resolves by id+version pairs
2. `getSizeCategories`/`getMaterialTypes` return the lookup lists, optionally filtered by ids, cached

---

#### MST-BE-B-08 · `getTightFits` + `getTightFitByIdAndVersion` data fetchers

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Search or look up tight-fit templates.

- **Current Behaviour (Q13/Q14):** `getTightFits(ids, name, statusIds, brandIds, divisionIds, departmentIds)` → `GET {base}/…/tightfit/v1/search?…` (qs-stringified) → camelCase, wrapped `{tightFits}`. `getTightFitByIdAndVersion(id, version)` → `GET {base}/…/tightfit/v1/{id}/versions/{version}` (non-batching DataLoader) → camelCase.
- **Target DGS Implementation:** `@DgsQuery getTightFits(...): TightFitsResponse`; `@DgsQuery getTightFitByIdAndVersion(id, version): TightFit` (composite key `id version`).
- **Files:** `dataFetcher/TightFitQueryDataFetcher.kt`.

**Acceptance Criteria:**

1. `getTightFits` filters by any combination of the given params
2. `getTightFitByIdAndVersion` resolves the exact version; not found → `null`

---

#### MST-BE-B-09 · `searchSparkSizes` data fetcher (NEXUS + Tag fan-out)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |
| **EXT** | 🔵 `NEXUS_Attributes` (platform) |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `NEXUS_Attributes` (platform)

- **In plain terms:** Search sizes across both the Nexus platform and Spark's own tag-based sizes.

- **Current Behaviour (Q15):** Fans out in parallel: `NEXUS_Attributes.Query.searchSizes(nameFilter, page:0, size)` (🔵 platform, gateway stitch) tagged `source:'Nexus'`, and `SPARK_Tag.Query.searchTags(type:'SIZE', archived:false, search:nameFilter, page:0, size)` (co-located `tag` sub-domain) tagged `source:'Spark'`; results concatenated and sliced to `size`. **No own REST endpoint.**
- **EXT Service Calls:** **EXT** → key: `NEXUS_Attributes` · severity: 🔵 — gateway-stitched platform size lookup.
- **Target DGS Implementation:** `@DgsQuery searchSparkSizes(nameFilter, size): [Sizes]` → parallel call to the NEXUS gateway stub + the co-located `tag` service; merge and slice.
- **Files:** `dataFetcher/SizesQueryDataFetcher.kt`.

**Acceptance Criteria:**

1. Returns up to `size` results, Nexus + Spark tag sizes combined
2. Each result tagged with its `source`
3. Empty/no-match → `[]`

---

### Phase C — Search & Listing

#### MST-BE-C-01 · `getMeasurements` data fetcher (relationship + listing)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟡 Medium |
| **Phase** | C |
| **Depends on** | B-01 |
| **EXT** | 🔴 `relationship` |

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

**Acceptance Criteria:**

1. Resolves ids via relationship then fetches measurements
2. No ids → `{content:[]}` (no measurement call)
3. Sorted `createdAt DESC` (location documented)

---

#### MST-BE-C-02 · `getMeasurementsElastic` data fetcher

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | C |
| **Depends on** | B-01 |
| **EXT** | 🔴 `search` |

- **Type:** Query · **Phase:** C · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search`

- **In plain terms:** Search a product's measurement sets via elastic.

- **Current Behaviour (Q3):** `{content} = search.getMeasurementSets.load({q:`parentId: ${resourceId}`})` → sort `createdAt DESC` → `{content}`.
- **EXT Service Calls:** **EXT** → key: `search` · severity: 🔴 — elastic measurement-set index.
- **Target DGS Implementation:** `@DgsQuery getMeasurementsElastic(resourceId): MeasurementPaged` → `searchClient.measurementSets("parentId: $resourceId")`; sort `createdAt DESC` (or backend).

**Acceptance Criteria:**

1. Returns elastic content for `parentId`
2. Sorted `createdAt DESC`
3. Empty → `{content:[]}`

---

### Phase D — Mutations (Simple)

#### MST-BE-D-01 · `addMeasurement` mutation

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Create a measurement set.

- **Current Behaviour (M1):** `POST {base}/…/measurements/v1` (snake_case request, `primeKey: humanId`); on `validationErrors||message` → throw. No ACL (new resource).
- **Target DGS Implementation:** `@DgsMutation addMeasurement(sparkMeasurement): Measurement` → typed `MeasurementValidationException`; prime read cache.

**Acceptance Criteria:**

1. POST creates + returns mapped `Measurement`
2. `validationErrors`/`message` → exception
3. Cache primed with `humanId`

---

#### MST-BE-D-02 · `updateMeasurementAccess` mutation

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Change who can access a measurement set.

- **Current Behaviour (M4):** `PUT …/{id}/permission` body `{systemTeamIds}` **or** `{systemTeamDto}` (whichever provided). **ACL note (context):** token for `id`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation updateMeasurementAccess(measurementSetId, systemTeamIds, systemTeamDto): Measurement`. **PO decision:** adopt tagged `MeasurementAccessInput` (keep wire format).

**Acceptance Criteria:**

1. Sends `{systemTeamIds}` when provided, else `{systemTeamDto}`
2. Returns updated measurement
3. Input-shape decision recorded

---

#### MST-BE-D-03 · `lockMeasurementSet` mutation

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Lock a measurement set from edits.

- **Current Behaviour (M5):** `PUT …/{id}/lock`. **ACL note (context):** token for `id`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation lockMeasurementSet(measurementSetId): Measurement`.

**Acceptance Criteria:**

1. PUT `/lock` returns locked set
2. 404 → null

---

#### MST-BE-D-04 · `unlockMeasurementSet` mutation

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Unlock a measurement set.

- **Current Behaviour (M6):** `PUT …/{id}/unlock`. ACL note as D-03.
- **Target DGS Implementation:** `@DgsMutation unlockMeasurementSet(measurementSetId): Measurement`.

**Acceptance Criteria:**

1. PUT `/unlock` returns unlocked set
2. 404 → null

---

#### MST-BE-D-05 · `updateMeasurementComponentStatus` mutation

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Update the component status on measurement sets.

- **Current Behaviour (M2):** `PUT …/component_status_update` body `{productId, ids, status}`. **No ACL token** — confirm backend enforces (like BOM D-05).
- **Target DGS Implementation:** `@DgsMutation updateMeasurementComponentStatus(productId, ids, status): MeasurementPaged`; wrap result `{content}`.

**Acceptance Criteria:**

1. PUT sends `{productId, ids, status}` snake_case
2. Returns `MeasurementPaged{content}`
3. Auth decision recorded

---

#### MST-BE-D-06 · `putSampleMeasurementSet` mutation

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Create or replace a sample's measurement set.

- **Current Behaviour (M7):** `PUT …/sample` (`primeKey: sampleId`); token for `[measurementSetId, sampleId]`; on `validationErrors||message` → throw.
- **Target DGS Implementation:** `@DgsMutation putSampleMeasurementSet(sampleMeasurementSet): SampleMeasurementSet` → typed exception; prime by `sampleId`.

**Acceptance Criteria:**

1. PUT upserts the sample set
2. `validationErrors`/`message` → exception
3. Cache primed by `sampleId`

---

#### MST-BE-D-07 · `deleteSampleMeasurementSet` mutation

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Delete a sample's measurement set.

- **Current Behaviour (M8):** `DELETE …/sample/{sampleId}`. **ACL note (context):** token for `sampleId`; ignored in DGS.
- **Target DGS Implementation:** `@DgsMutation deleteSampleMeasurementSet(sampleId): SampleMeasurementSet`.

**Acceptance Criteria:**

1. DELETE removes the sample set; returns the deleted/empty result
2. 404 → null

---

#### MST-BE-D-08 · `addMeasurementTemplate` + `updateMeasurementTemplate` + `deleteMeasurementTemplate` mutations

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-06 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-06

- **In plain terms:** Create, update, or delete a measurement template.

- **Current Behaviour (M9/M10/M11):** `addMeasurementTemplate` — (ACL context) token `[SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY]` → `POST {base}/…/measurement/templates/v1` (snake_case request); on `validationErrors||message` → throw. `updateMeasurementTemplate` — same token → `PUT {base}/…/measurement/templates/v1/{templateId}`; same error handling. `deleteMeasurementTemplate(ids)` → `DELETE {endpoint}/purgeTestMeasurementTemplateData?ids=`. **No ACL token on delete** — confirm backend enforces (like measurement's own D-05).
- **Target DGS Implementation:** `@DgsMutation addMeasurementTemplate/updateMeasurementTemplate(measurementTemplate): MeasurementTemplate`; `@DgsMutation deleteMeasurementTemplate(ids): Boolean` → typed `MeasurementTemplateValidationException` on add/update.
- **Files:** `dataFetcher/MeasurementTemplateMutationDataFetcher.kt`.

**Acceptance Criteria:**

1. `add`/`update` POST/PUT create or replace the template; `validationErrors`/`message` → exception
2. `delete` removes the templates for the given ids
3. Delete auth decision recorded (no JWT today)

---

#### MST-BE-D-09 · `addSizeTemplate` + `updateSizeTemplate` mutations

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-07 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-07

- **In plain terms:** Create or update a size template.

- **Current Behaviour (M12/M13):** (ACL context) token `[SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY]` → `POST {base}/…/size_templates/v1` (add) / `PUT {base}/…/size_templates/v1/{id}` (update), both snake_case request/camelCase response; on `validationErrors||message` → throw.
- **Target DGS Implementation:** `@DgsMutation addSizeTemplate/updateSizeTemplate(sizeTemplate): SizeTemplate` → typed `SizeTemplateValidationException`.
- **Files:** `dataFetcher/SizeTemplateMutationDataFetcher.kt`.

**Acceptance Criteria:**

1. `add`/`update` POST/PUT create or replace the size template
2. `validationErrors`/`message` → exception

---

#### MST-BE-D-10 · `addTightFit` + `updateTightFit` mutations

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-08 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-08

- **In plain terms:** Create or update a tight-fit template.

- **Current Behaviour (M14/M15):** (ACL context) token `[SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY]` → `POST {base}/…/tightfit/v1` (add) / `PUT {base}/…/tightfit/v1/{tightFitId}` (update), both snake_case request/camelCase response; on `validationErrors||message` → throw.
- **Target DGS Implementation:** `@DgsMutation addTightFit/updateTightFit(tightFit): TightFit` → typed `TightFitValidationException`.
- **Files:** `dataFetcher/TightFitMutationDataFetcher.kt`.

**Acceptance Criteria:**

1. `add`/`update` POST/PUT create or replace the tight fit
2. `validationErrors`/`message` → exception

---

### Phase E — Complex Operations

#### MST-BE-E-01 · `updateMeasurement` — 2-step orchestrated write

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟠 High |
| **Phase** | E |
| **Depends on** | B-01 |
| **EXT** | 🟡 `workspaceV2` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |
| **Blocked by** | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |

- **Type:** Mutation · **Phase:** E · **Complexity:** 🔶 High · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🟡 `workspaceV2` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module)

> **Draft ADR-013, ratification pending.** This is the program's **pilot** saga adoption (smallest real case,
> ADR-013 §5 build order) against the shared `WriteSaga` module built in `PRODUCT-BE-E-00`: workspace assoc
> `COMPENSATE` → body PUT = point of no return; injected step-2 failure must yield `COMPENSATED` (set not
> moved) with per-step detail.

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

**Acceptance Criteria:**

1. Parity for 3 fixtures: body-only; body+workspace-add; body+workspace-remove
2. Workspace step runs before body PUT
3. Body PUT omits `humanId`
4. Chosen failure strategy implemented
5. `validationErrors`/`message` → exception

**Test Cases:**

- [ ] Unit: order workspace→body
- [ ] Unit: no-workspace skip
- [ ] Unit: body-failure path
- [ ] Parity: 3 fixtures

---

### Phase F — Federation & Stitching

#### MST-BE-F-01 · Implement `Product.measurementSets` (internal)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | F |
| **Depends on** | B-01 |
| **EXT** | 🔴 `relationship` |

- **Type:** Field Resolver · **Phase:** F · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `relationship`

- **In plain terms:** Expose a product's measurement sets on the Product type.

- **Current Behaviour:** product navigates to measurement sets via the relationship + getMeasurements flow.
- **Target DGS Implementation:** plain `@DgsData measurementSets(...)` on the internal `Product` type (same
subgraph) reusing the C-01 relationship+listing logic. **No** `@DgsEntityFetcher`/`@extends @external`.
Depends on `Product` existing (product A-02), not on a separate deployment.

**Acceptance Criteria:**

1. `Product.measurementSets` resolves internally via `measurementService`
2. no gateway hop
3. Parity vs current product resolver

---

### Phase G — Field Resolvers, Bug-fixes & Tests

#### MST-BE-G-01 · `Measurement` field resolvers (13 fields)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01, B-01, B-06, B-07, B-08 |
| **EXT** | 🟡 `workspaceV2` · 🟡 `sampleV2` · 🔵 `vmm` · 🔵 `userAttributes` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01, B-01, B-06, B-07, B-08 · **EXT:** 🟡 `workspaceV2` · 🟡 `sampleV2` · 🔵 `vmm` · 🔵 `userAttributes`

- **In plain terms:** Resolve the everyday measurement fields (people, product, partners, templates).

- **Current Behaviour (field table in 02):** `access`/`currentUserPermissions`
(ACL — context only), `businessPartners` (loadBps), `createdBy`/`updatedBy` (`getUserByIDOrNullIfNotFound`),
`product` (PID-prefixed → internal `product.getByID`), `workspaces` (`getWorkspacesByIdsV2` or null),
`status` (`{code:statusId, description:statusName}` computed), `updatedFromResource` (switch type='sample' →
`sampleV2.getSampleById`), `measurementTemplates` (`measurementTemplate.getMeasurementTemplatesByIds(...).content`),
`sizeTemplate` (`sizeTemplate.getSizeTemplates([id])[0]`), `tightFitTemplate` (`tightFit.getTightFitByIdAndVersion({id,version})`),
`participantDetails` (`getUserGroup`).
- **EXT:** 🟡 workspaceV2/sampleV2; 🔵 vmm/user-profile. (`measurementTemplates`/`sizeTemplate`/`tightFitTemplate`
**reclassified internal 2026-07-19** — plain in-process calls to this domain's own B-06/B-07/B-08 data
fetchers, no longer counted as EXT; depends-on updated to require those stories exist first.)
- **Target DGS Implementation:** one `@DgsData` set; `workspaceV2`/`sampleV2` → federated references;
`measurementTemplates`/`sizeTemplate`/`tightFitTemplate` → plain internal calls to the co-located
`MeasurementTemplateService`/`SizeTemplateService`/`TightFitService` (B-06/B-07/B-08), **not**
`@DgsEntityFetcher`; `product` internal; `status` computed; `updatedFromResource` switch preserved (only
`sample` realized).
- **Files:** `dataFetcher/MeasurementFieldDataFetcher.kt`.

**Acceptance Criteria:**

1. All 13 fields resolve
2. `product` null when `resourceId` not `PID*`
3. `status` = `{statusId, statusName}`
4. `workspaces` empty → null
5. `updatedFromResource` resolves only for `type==='sample'`

---

#### MST-BE-G-02 · `SampleMeasurementSet` field resolvers (2 fields)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-01, B-01 |
| **EXT** | 🔵 `userAttributes` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01, B-01 · **EXT:** 🔵 `userAttributes`

- **In plain terms:** Resolve the sample-measurement-set fields.

- **Current Behaviour (`:165-174`):** `createdBy` (`getUserByIDOrNullIfNotFound`), `measurementSizeId` (`measurementSize && measurementSize.code` — computed).
- **Target DGS Implementation:** 2 `@DgsData` fields.

**Acceptance Criteria:**

1. `createdBy` resolves by user id (null id → null)
2. `measurementSizeId` = `measurementSize.code`

---

#### MST-BE-G-05 · `MeasurementTemplate` field resolvers (5 fields)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-06 |
| **EXT** | 🔵 `ig` · 🔵 `vmm` · 🔵 `userAttributes` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-06 · **EXT:** 🔵 `ig` · 🔵 `vmm` · 🔵 `userAttributes`

- **In plain terms:** Resolve a measurement template's people and item-group fields.

- **Current Behaviour (field table in 02):** `createdBy`/`updatedBy`
(`getUserByIDOrNullIfNotFound`), `departments`/`divisions` (`ig.department|division.getByID`, empty-tolerant),
`brands` (`brand.getBrand`, skipped when `brandIds === -1`).
- **Target DGS Implementation:** 5 `@DgsData` fields; `departments`/`divisions` → `ig` gateway stitch;
`brands` → `vmm`/`brand` gateway stitch; `createdBy`/`updatedBy` → `userAttributes` entity reference.
- **Files:** `dataFetcher/MeasurementTemplateFieldDataFetcher.kt`.

**Acceptance Criteria:**

1. All 5 fields resolve
2. `departments`/`divisions` null-tolerant on empty ids
3. `brands` skipped (null) when `brandIds === -1`

---

#### MST-BE-G-06 · `SizeTemplate` field resolvers (3 fields)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-07 |
| **EXT** | 🔵 `userAttributes` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-07 · **EXT:** 🔵 `userAttributes`

- **In plain terms:** Resolve a size template's computed id and people fields.

- **Current Behaviour (field table in 02):** `humanId` (`humanId || id` —
computed fallback), `createdBy`/`updatedBy` (`getUserByIDOrNullIfNotFound`).
- **Target DGS Implementation:** 3 `@DgsData` fields; `humanId` computed; `createdBy`/`updatedBy` →
`userAttributes` entity reference.
- **Files:** `dataFetcher/SizeTemplateFieldDataFetcher.kt`.

**Acceptance Criteria:**

1. All 3 fields resolve
2. `humanId` falls back to `id` when the record has no `humanId`

---

#### MST-BE-G-07 · `TightFit` field resolvers (5 fields)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-08 |
| **EXT** | 🔵 `ig` · 🔵 `vmm` · 🔵 `userAttributes` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-08 · **EXT:** 🔵 `ig` · 🔵 `vmm` · 🔵 `userAttributes`

- **In plain terms:** Resolve a tight-fit template's people and item-group fields.

- **Current Behaviour (field table in 02):** `departments`/`divisions`
(`ig.department|division.getByID`, empty-tolerant), `brands` (`brand.getBrand`, skipped when
`brandIds === -1`), `createdBy`/`updatedBy` (`getUserByIDOrNullIfNotFound`).
- **Target DGS Implementation:** 5 `@DgsData` fields; same pattern as G-05 (`ig`/`vmm` gateway stitch,
`userAttributes` entity reference).
- **Files:** `dataFetcher/TightFitFieldDataFetcher.kt`.

**Acceptance Criteria:**

1. All 5 fields resolve
2. `departments`/`divisions` null-tolerant on empty ids
3. `brands` skipped (null) when `brandIds === -1`

---

#### MST-BE-G-04 · `SampleMeasurementSet.sample` forward reference (recommended, PO-gated)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-02 (carries B-05 `getSampleMeasurement`, grouped-XS merged) |
| **EXT** | 🟡 `sample` |
| **Status** | Recommended (PO-gated — federation-review/03 §2 REC-4) |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-02 (carries B-05 `getSampleMeasurement`, grouped-XS merged) · **EXT:** 🟡 `sample`
- **Status:** Recommended (PO-gated — federation-review/03 §2 REC-4)

- **In plain terms:** Adds `sample { … }` on the sample measurement set — the forward twin of the existing
reverse extension (`SampleV2.sampleMeasurement`, **MST-BE-H-01**).

- **Context:** `SampleMeasurementSet` is keyed on `sampleId` but exposes no way to walk to the sample entity;
sample screens re-query by id today. `sampleId` stays — it is the `@key`.
- **Target DGS Implementation:** schema adds `sample: SampleV2` on `SampleMeasurementSet`; resolver emits
`{id: sampleId}` — zero extra backend calls; hydrated by the sample subgraph (phase 2; stitched gateway
until then).

**Acceptance Criteria:**

1. PO approval recorded (OQ-5) before implementation starts
2. `sample { id }` resolves as a stub; `sampleId` unchanged
3. Pairs cleanly with MST-BE-H-01 (no circular resolution at the gateway — verified by a two-hop smoke query)

---

### Phase H — Phase H

#### MST-BE-H-01 · Contribute `sampleMeasurement` to the `SampleV2` entity

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | H |
| **Depends on** | B-01 |
| **Blocked by** | sample |

- **Type:** Field Resolver · **Phase:** H · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** B-01 · **Blocked by:** sample

- **In plain terms:** Contribute a sample's measurement set to the Sample entity.

- **Current Behaviour:** sample navigates to its measurement set via `getSampleMeasurement`.
- **Target DGS Implementation:** `extend type SampleV2 @key(fields:"id")` with `@DgsData sampleMeasurement` → `getSampleMeasurement(sampleId)`. **BLOCKED-BY** sample domain Phase 3.

**Acceptance Criteria:**

1. `SampleV2.sampleMeasurement` resolves
2. Parity vs current

---

---

## Story Reference Table

| Story ID | Title | Phase | Complexity | Depends On |
|---|---|---|---|---|
| `MST-BE-B-01` | `getMeasurementByIds` data fetcher | B | 🟢 Low | — |
| `MST-BE-B-02` | `getUnitsOfMeasure` (cacheable) | B | 🟢 Low | B-01 |
| `MST-BE-B-03` | `getThicknessUnitsOfMeasure` (cacheable) | B | 🟢 Low | B-01 |
| `MST-BE-B-04` | `getMeasurementSetStatus` (cacheable) | B | 🟢 Low | B-01 |
| `MST-BE-B-05` | `getSampleMeasurement` data fetcher | B | 🟢 Low | B-01, B-01 |
| `MST-BE-B-06` | `getMeasurementTemplates` + `getMeasurementTemplatesByIds` data fetchers | B | 🟢 Low | — |
| `MST-BE-B-07` | `getSizeTemplates` + `getSizeCategories` + `getMaterialTypes` data fetchers | B | 🟢 Low | — |
| `MST-BE-B-08` | `getTightFits` + `getTightFitByIdAndVersion` data fetchers | B | 🟢 Low | — |
| `MST-BE-B-09` | `searchSparkSizes` data fetcher (NEXUS + Tag fan-out) | B | 🟢 Low | — |
| `MST-BE-C-01` | `getMeasurements` data fetcher (relationship + listing) | C | 🟡 Medium | B-01 |
| `MST-BE-C-02` | `getMeasurementsElastic` data fetcher | C | 🟢 Low | B-01 |
| `MST-BE-D-01` | `addMeasurement` mutation | D | 🟡 Medium | B-01 |
| `MST-BE-D-02` | `updateMeasurementAccess` mutation | D | 🟢 Low | B-01 |
| `MST-BE-D-03` | `lockMeasurementSet` mutation | D | 🟢 Low | B-01 |
| `MST-BE-D-04` | `unlockMeasurementSet` mutation | D | 🟢 Low | B-01 |
| `MST-BE-D-05` | `updateMeasurementComponentStatus` mutation | D | 🟢 Low | B-01 |
| `MST-BE-D-06` | `putSampleMeasurementSet` mutation | D | 🟡 Medium | B-01 |
| `MST-BE-D-07` | `deleteSampleMeasurementSet` mutation | D | 🟢 Low | B-01 |
| `MST-BE-D-08` | `addMeasurementTemplate` + `updateMeasurementTemplate` + `deleteMeasurementTemplate` mutations | D | 🟢 Low | B-06 |
| `MST-BE-D-09` | `addSizeTemplate` + `updateSizeTemplate` mutations | D | 🟢 Low | B-07 |
| `MST-BE-D-10` | `addTightFit` + `updateTightFit` mutations | D | 🟢 Low | B-08 |
| `MST-BE-E-01` | `updateMeasurement` — 2-step orchestrated write | E | 🟠 High | B-01 |
| `MST-BE-F-01` | Implement `Product.measurementSets` (internal) | F | 🟡 Medium | B-01 |
| `MST-BE-H-01` | Contribute `sampleMeasurement` to the `SampleV2` entity | H | 🟢 Low | B-01 |
| `MST-BE-G-01` | `Measurement` field resolvers (13 fields) | G | 🟡 Medium | B-01, B-01, B-06, B-07, B-08 |
| `MST-BE-G-02` | `SampleMeasurementSet` field resolvers (2 fields) | G | 🟢 Low | B-01, B-01 |
| `MST-BE-G-05` | `MeasurementTemplate` field resolvers (5 fields) | G | 🟢 Low | B-06 |
| `MST-BE-G-06` | `SizeTemplate` field resolvers (3 fields) | G | 🟢 Low | B-07 |
| `MST-BE-G-07` | `TightFit` field resolvers (5 fields) | G | 🟢 Low | B-08 |
| `MST-BE-G-04` | `SampleMeasurementSet.sample` forward reference (recommended, PO-gated) | G | 🟢 Low | B-02 (carries B-05 `getSampleMeasurement`, grouped-XS merged) |