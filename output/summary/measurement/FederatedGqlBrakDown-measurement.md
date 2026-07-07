# Federated GraphQL Breakdown — Measurement

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **M** |
| **Total Stories** | 20 |
| **Complexity** | 🔴 0 Very High · 🟠 1 High · 🟡 6 Medium · 🟢 13 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Measurement** domain — measurement sets (the size/point-of-measure specs for a product), their sample measurements, and the master-data unit lists — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **mid-sized and mid-low risk**: 7 queries, 8 mutations, 15 field resolvers on a 175-line resolver, with **no polymorphism**.
- The one genuinely harder piece is `updateMeasurement`, a 2-step write (workspace association, then body) with no rollback today.

`getMeasurements` depends on the **relationship** service to find a product's measurement-set ids, and the
template/size/tight-fit references are **separate sibling domains** we only reference (not migrate here).

**ACL note:** the current code obtains per-resource capability tokens via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

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

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `SPARK-MEAS-E01` — `updateMeasurement` — 2-step orchestrated write | `SPARK-SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

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


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~8–14 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel |
| 3 engineers | ~4–6 sprints | critical path A → E01 → G01 → G03 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C01/C02 + D01–D04 | listing + simple mutations |
| 3 | D05–D07 + E01 | remaining mutations + `updateMeasurement` |
| 4 | G01–G02 | field resolvers |
| 5 | G03 | tests & parity |
| post-launch | F01, F02 | federation contributions |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-MEAS-B01`<br>`getMeasurementByIds` data fetcher | 🟢 Low `XS` | Query | — | **Intent —** Fetch measurement sets by id.<br>**Today —** GET … → camelCase. ignored in DGS<br>**Done when:**<br>• Returns measurements for ids with `calculated` flag forwarded<br>• Empty ids → `[]`<br>• snake→camel mapping |
| 🔷 `SPARK-MEAS-B02`<br>`getUnitsOfMeasure` (cacheable) | 🟢 Low `XS` | Query | B01 | **Intent —** Return the unit-of-measure lookup list (cached).<br>**Today —** GET … → units_of_measure camelCase<br>**Done when:**<br>• Returns UoM list (optionally filtered by ids)<br>• Cached |
| 🔷 `SPARK-MEAS-B03`<br>`getThicknessUnitsOfMeasure` (cacheable) | 🟢 Low `XS` | Query | B01 | **Intent —** Return the thickness unit-of-measure lookup (cached).<br>**Today —** GET … → units_of_measure<br>**Done when:**<br>• Returns thickness UoM list<br>• Cached |
| 🔷 `SPARK-MEAS-B04`<br>`getMeasurementSetStatus` (cacheable) | 🟢 Low `XS` | Query | B01 | **Intent —** Return the measurement-set status lookup (cached).<br>**Today —** GET … → {key:value} map → [{code, description}]<br>**Done when:**<br>• Returns statuses<br>• Cached<br>• key→code, value→description |
| 🔷 `SPARK-MEAS-B05`<br>`getSampleMeasurement` data fetcher | 🟢 Low `XS` | Query | B01 | **Intent —** Fetch the measurement set for a sample.<br>**Today —** GET … → camelCase. ignored in DGS<br>**Done when:**<br>• Returns the sample measurement set for `sampleId`<br>• Not found → `null` |

> **`SPARK-MEAS-B01`** — **Note — DGS Module Init (this PR only):** Creates `measurement.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql.


### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-MEAS-C01`<br>`getMeasurements` data fetcher (relationship + listing) | 🟡 Medium `M` | Query<br>Calls: `relationship` | B01 | **Intent —** List a resource's measurement sets (resolves the relationship first).<br>**Today —** relationships = relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0}). 2. ids = relationships.map(n => n.id); if empty → [].…<br>**Done when:**<br>• Resolves ids via relationship then fetches measurements<br>• No ids → `{content:[]}` (no measurement call)<br>• Sorted `createdAt DESC` (location documented) |
| 🔷 `SPARK-MEAS-C02`<br>`getMeasurementsElastic` data fetcher | 🟢 Low `XS` | Query<br>Calls: `search` | B01 | **Intent —** Search a product's measurement sets via elastic.<br>**Today —** {content} = search.getMeasurementSets → sort createdAt DESC → {content}. - EXT Service Calls: EXT → key: search · severity: — elastic measurement-set index<br>**Done when:**<br>• Returns elastic content for `parentId`<br>• Sorted `createdAt DESC`<br>• Empty → `{content:[]}` |


### ✏️ Phase D — Mutations (7 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `SPARK-MEAS-D01`<br>`addMeasurement` mutation | 🟡 Medium `M` | Mutation | B01 | **Intent —** Create a measurement set.<br>**Today —** POST … (snake_case request, primeKey: humanId); on validationErrors\\|\\|message → throw. No ACL (new resource)<br>**Done when:**<br>• POST creates + returns mapped `Measurement`<br>• `validationErrors`/`message` → exception<br>• Cache primed with `humanId` |
| 🔶 `SPARK-MEAS-D02`<br>`updateMeasurementAccess` mutation | 🟢 Low `XS` | Mutation | B01 | **Intent —** Change who can access a measurement set.<br>**Today —** PUT …/{id}/permission body {systemTeamIds} or {systemTeamDto} (whichever provided). ignored in DGS<br>**Done when:**<br>• Sends `{systemTeamIds}` when provided, else `{systemTeamDto}`<br>• Returns updated measurement<br>• Input-shape decision recorded |
| 🔶 `SPARK-MEAS-D03`<br>`lockMeasurementSet` mutation | 🟢 Low `XS` | Mutation | B01 | **Intent —** Lock a measurement set from edits.<br>**Today —** PUT …/{id}/lock. ignored in DGS<br>**Done when:**<br>• PUT `/lock` returns locked set<br>• 404 → null |
| 🔶 `SPARK-MEAS-D04`<br>`unlockMeasurementSet` mutation | 🟢 Low `XS` | Mutation | B01 | **Intent —** Unlock a measurement set.<br>**Today —** PUT …/{id}/unlock<br>**Done when:**<br>• PUT `/unlock` returns unlocked set<br>• 404 → null |
| 🔶 `SPARK-MEAS-D05`<br>`updateMeasurementComponentStatus` mutation | 🟢 Low `XS` | Mutation | B01 | **Intent —** Update the component status on measurement sets.<br>**Today —** PUT …/component_status_update body {productId, ids, status}. No ACL token — confirm backend enforces (like BOM D05)<br>**Done when:**<br>• PUT sends `{productId, ids, status}` snake_case<br>• Returns `MeasurementPaged{content}`<br>• Auth decision recorded |
| 🔶 `SPARK-MEAS-D06`<br>`putSampleMeasurementSet` mutation | 🟡 Medium `M` | Mutation | B01 | **Intent —** Create or replace a sample's measurement set.<br>**Today —** PUT …/sample (primeKey: sampleId); token for [measurementSetId, sampleId]; on validationErrors\\|\\|message → throw<br>**Done when:**<br>• PUT upserts the sample set<br>• `validationErrors`/`message` → exception<br>• Cache primed by `sampleId` |
| 🔶 `SPARK-MEAS-D07`<br>`deleteSampleMeasurementSet` mutation | 🟢 Low `XS` | Mutation | B01 | **Intent —** Delete a sample's measurement set.<br>**Today —** DELETE …/sample/{sampleId}. ignored in DGS<br>**Done when:**<br>• DELETE removes the sample set; returns the deleted/empty result<br>• 404 → null |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `SPARK-MEAS-E01`<br>`updateMeasurement` — 2-step orchestrated write<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `workspaceV2` | SPARK-SPIKE-01, B01 | **Intent —** Edit a measurement set — a 2-step write (workspace + body) that has no rollback today.<br>**Today —** workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations \\|\\| {}. token for [humanId]. 2. If add/remove workspaces → workspaceAssociationHelper(MEASUREMENT…<br>**Done when:**<br>• Parity for 3 fixtures: body-only; body+workspace-add; body+workspace-remove<br>• Workspace step runs before body PUT<br>• Body PUT omits `humanId`<br>• Chosen failure strategy implemented<br>• `validationErrors`/`message` → exception | ☐ Unit: order workspace→body<br>☐ Unit: no-workspace skip<br>☐ Unit: body-failure path<br>☐ Parity: 3 fixtures |


### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-MEAS-F01`<br>Implement `Product.measurementSets` (internal) | 🟡 Medium `M` | Field Resolver<br>Calls: `relationship` | B01 | **Intent —** Expose a product's measurement sets on the Product type.<br>**Today —** product navigates to measurement sets via the relationship + getMeasurements flow<br>**Done when:**<br>• `Product.measurementSets` resolves internally via `measurementService`<br>• no gateway hop<br>• Parity vs current product resolver |
| 🔸 `SPARK-MEAS-F02`<br>Contribute `sampleMeasurement` to the `SampleV2` entity | 🟢 Low `XS` | Field Resolver | B01 | **Intent —** Contribute a sample's measurement set to the Sample entity.<br>**Today —** sample navigates to its measurement set via getSampleMeasurement<br>**Done when:**<br>• `SampleV2.sampleMeasurement` resolves<br>• Parity vs current |


### 🧪 Phase G — Field Resolvers & Tests (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-MEAS-G01`<br>`Measurement` field resolvers (13 fields) | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `sampleV2`, `measurementTemplate`, `sizeTemplate`, `tightFit`, `vmm`, `userAttributes` | B01 | **Intent —** Resolve the everyday measurement fields (people, product, partners).<br>**Today —** access/currentUserPermissions , businessPartners (loadBps), createdBy/updatedBy (getUserByIDOrNullIfNotFound), product (PID-prefixed → internal product.getByID)…<br>**Done when:**<br>• All 13 fields resolve<br>• `product` null when `resourceId` not `PID*`<br>• `status` = `{statusId, statusName}`<br>• `workspaces` empty → null<br>• `updatedFromResource` resolves only for `type==='sample'` |
| 🔸 `SPARK-MEAS-G02`<br>`SampleMeasurementSet` field resolvers (2 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | B01 | **Intent —** Resolve the sample-measurement-set fields.<br>**Today —** 2 @DgsData fields<br>**Done when:**<br>• `createdBy` resolves by user id (null id → null)<br>• `measurementSizeId` = `measurementSize.code` |
| 📄 `SPARK-MEAS-G03`<br>Test coverage & parity | 🟡 Medium `M` | Tests | B01, C01, E01, G01 | **Intent —** Prove the measurement subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity fixtures for the 7 queries + 8 mutations + updateMeasurement 3 fixtures + the relationship path<br>**Done when:**<br>• Unit ≥80%<br>• Parity green for reads/writes incl. `getMeasurements` relationship path<br>• `updateMeasurement` failure path covered |

