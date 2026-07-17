# Federated GraphQL Breakdown — Measurement

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **M** |
| **Total Stories** | 14 |
| **Complexity** | 🔴 0 Very High · 🟠 1 High · 🟡 8 Medium · 🟢 5 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-17 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Measurement** domain — measurement sets (the size/point-of-measure specs for a product), their sample measurements, and the master-data unit lists — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **mid-sized and mid-low risk**: 7 queries, 8 mutations, 15 field resolvers on a 175-line resolver, with **no polymorphism**.
- The one genuinely harder piece is `updateMeasurement`, a 2-step write (workspace association, then body) with no rollback today.

`getMeasurements` depends on the **relationship** service to find a product's measurement-set ids, and the
template/size/tight-fit references are **separate sibling domains** we only reference (not migrate here).

**ACL note:** the current code obtains per-resource capability tokens via ACL; Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs ([`complexStories/*/02-adr-noacl-*.md`](https://github.com/XXX/blob/main/output/complexStories/*/02-adr-noacl-*.md)) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

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
| 🔴🔬 `MST-BE-E-01` — `updateMeasurement` — 2-step orchestrated write | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

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
| 3 engineers | ~4–6 sprints | critical path A → E-01 → G-01 → G-03 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-04 | listing + simple mutations |
| 3 | D-05–D-07 + E-01 | remaining mutations + `updateMeasurement` |
| 4 | G-01–G-02 | field resolvers |
| 5 | G-03 | tests & parity |
| post-launch | F-01, F-02 | federation contributions |

---

## Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟡 `B-02`, 🟡 `C-01`, 🟢 `C-02`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-06`, 🟢 `D-07`, 🟠 `E-01`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟢 `G-02` | `E-01` → 🔬 SPIKE-01<br>`F-02` → ⛔ BLOCKED-BY sample | Fan-out — 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests |
| 3 | 🟡 `G-03` | — | 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `E-01` → `G-03` — 3 sequential stories; everything else hangs off this chain in parallel.

---

## Recommended Story Graph — 2 Backend Engineers

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 2 backend engineers** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 | 👤 BE-2 |
|---|---|---|
| 1 | 🟢 `B-01` (1–2d) | ⏳ after `B-01` → 🟡 `C-01` (2–4d) |
| 2 | 🟠 `E-01` (4–7d) 🔬 | 🟡 `G-01` (2–4d) |
| 3 | 🟡 `B-02` (2–4d) *(grouped XS: +`B-03`, `B-04`, `B-05`)* | 🟡 `D-01` (2–4d) |
| 4 | 🟡 `D-02` (2–4d) *(grouped XS: +`D-03`, `D-04`, `D-05`)* | 🟡 `D-06` (2–4d) |
| 5 | 🟡 `F-01` (2–4d) | 🟡 `G-03` (2–4d) |
| 6 | 🟢 `C-02` (1–2d) | 🟢 `D-07` (1–2d) |
| 7 | 🟢 `F-02` (1–2d) ⛔ | 🟢 `G-02` (1–2d) |

**BE-1:** `B-01` → `E-01` → `B-02` → `D-02` → `F-01` → `C-02` → `F-02`<br>**BE-2:** `C-01` → `G-01` → `D-01` → `D-06` → `G-03` → `D-07` → `G-02`

**Elapsed (nominal midpoints):** ~20 working days with 2 engineers vs ~37 days sequential.

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `MST-BE-B-01`<br>`getMeasurementByIds` data fetcher | 🟢 Low `XS` | Query | — | **Intent —** Fetch measurement sets by id.<br>**Today —** GET … → camelCase. ignored in DGS<br>**Done when:**<br>• Returns measurements for ids with `calculated` flag forwarded<br>• Empty ids → `[]`<br>• snake→camel mapping |
| 🔷 `MST-BE-B-02`<br>`getUnitsOfMeasure` · `getThicknessUnitsOfMeasure` · `getMeasurementSetStatus` · `getSampleMeasurement` data fetcher | 🟡 Medium `M` | Query | B-01 | **Grouped XS story —** combines former `B-03`, `B-04`, `B-05` (one PR train)<br>**Intent —** Return the unit-of-measure lookup list (cached); Return the thickness unit-of-measure lookup (cached); Return the measurement-set status lookup (cached); Fetch the measurement set for a sample<br>**Today —** GET … → units_of_measure camelCase. ; GET … → units_of_measure. ; GET … → {key:value} map → [{code, description}]. ; GET … → camelCase. ignored in DGS<br>**Done when:**<br>• `getUnitsOfMeasure`: Returns UoM list (optionally filtered by ids)<br>• `getUnitsOfMeasure`: Cached<br>• `getThicknessUnitsOfMeasure`: Returns thickness UoM list<br>• `getThicknessUnitsOfMeasure`: Cached<br>• `getMeasurementSetStatus`: Returns statuses<br>• `getMeasurementSetStatus`: Cached<br>• `getMeasurementSetStatus`: key→code, value→description<br>• `getSampleMeasurement` data fetcher: Returns the sample measurement set for `sampleId`<br>• `getSampleMeasurement` data fetcher: Not found → `null` |

> **`MST-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `measurement.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.


### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `MST-BE-C-01`<br>`getMeasurements` data fetcher (relationship + listing) | 🟡 Medium `M` | Query<br>Calls: `relationship` | B-01 | **Intent —** List a resource's measurement sets (resolves the relationship first).<br>**Today —** relationships = relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0}). 2. ids = relationships.map(n => n.id); if empty → [].…<br>**Done when:**<br>• Resolves ids via relationship then fetches measurements<br>• No ids → `{content:[]}` (no measurement call)<br>• Sorted `createdAt DESC` (location documented) |
| 🔷 `MST-BE-C-02`<br>`getMeasurementsElastic` data fetcher | 🟢 Low `XS` | Query<br>Calls: `search` | B-01 | **Intent —** Search a product's measurement sets via elastic.<br>**Today —** {content} = search.getMeasurementSets → sort createdAt DESC → {content}. - EXT Service Calls: EXT → key: search · severity: — elastic measurement-set index<br>**Done when:**<br>• Returns elastic content for `parentId`<br>• Sorted `createdAt DESC`<br>• Empty → `{content:[]}` |


### ✏️ Phase D — Mutations (4 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `MST-BE-D-01`<br>`addMeasurement` mutation | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create a measurement set.<br>**Today —** POST … (snake_case request, primeKey: humanId); on validationErrors\\|\\|message → throw. No ACL (new resource)<br>**Done when:**<br>• POST creates + returns mapped `Measurement`<br>• `validationErrors`/`message` → exception<br>• Cache primed with `humanId` |
| 🔶 `MST-BE-D-02`<br>`updateMeasurementAccess` mutation · `lockMeasurementSet` mutation · `unlockMeasurementSet` mutation · `updateMeasurementComponentStatus` mutation | 🟡 Medium `M` | Mutation | B-01 | **Grouped XS story —** combines former `D-03`, `D-04`, `D-05` (one PR train)<br>**Intent —** Change who can access a measurement set; Lock a measurement set from edits; Unlock a measurement set; Update the component status on measurement sets<br>**Today —** PUT …/{id}/permission body {systemTeamIds} or {systemTeamDto} (whichever provided). ignored in DGS. ; PUT …/{id}/lock. ignored in DGS. ; PUT …/{id}/unlock. ; PUT…<br>**Done when:**<br>• `updateMeasurementAccess` mutation: Sends `{systemTeamIds}` when provided, else `{systemTeamDto}`<br>• `updateMeasurementAccess` mutation: Returns updated measurement<br>• `updateMeasurementAccess` mutation: Input-shape decision recorded<br>• `lockMeasurementSet` mutation: PUT `/lock` returns locked set<br>• `lockMeasurementSet` mutation: 404 → null<br>• `unlockMeasurementSet` mutation: PUT `/unlock` returns unlocked set<br>• `unlockMeasurementSet` mutation: 404 → null<br>• `updateMeasurementComponentStatus` mutation: PUT sends `{productId, ids, status}` snake_case<br>• `updateMeasurementComponentStatus` mutation: Returns `MeasurementPaged{content}`<br>• `updateMeasurementComponentStatus` mutation: Auth decision recorded |
| 🔶 `MST-BE-D-06`<br>`putSampleMeasurementSet` mutation | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create or replace a sample's measurement set.<br>**Today —** PUT …/sample (primeKey: sampleId); token for [measurementSetId, sampleId]; on validationErrors\\|\\|message → throw<br>**Done when:**<br>• PUT upserts the sample set<br>• `validationErrors`/`message` → exception<br>• Cache primed by `sampleId` |
| 🔶 `MST-BE-D-07`<br>`deleteSampleMeasurementSet` mutation | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Delete a sample's measurement set.<br>**Today —** DELETE …/sample/{sampleId}. ignored in DGS<br>**Done when:**<br>• DELETE removes the sample set; returns the deleted/empty result<br>• 404 → null |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `MST-BE-E-01`<br>`updateMeasurement` — 2-step orchestrated write<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `workspaceV2` | SPIKE-01, B-01 | **Intent —** Edit a measurement set — a 2-step write (workspace + body) that has no rollback today.<br>**Today —** workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations \\|\\| {}. token for [humanId]. 2. If add/remove workspaces → workspaceAssociationHelper(MEASUREMENT…<br>**Done when:**<br>• Parity for 3 fixtures: body-only; body+workspace-add; body+workspace-remove<br>• Workspace step runs before body PUT<br>• Body PUT omits `humanId`<br>• Chosen failure strategy implemented<br>• `validationErrors`/`message` → exception | ☐ Unit: order workspace→body<br>☐ Unit: no-workspace skip<br>☐ Unit: body-failure path<br>☐ Parity: 3 fixtures |


### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `MST-BE-F-01`<br>Implement `Product.measurementSets` (internal) | 🟡 Medium `M` | Field Resolver<br>Calls: `relationship` | B-01 | **Intent —** Expose a product's measurement sets on the Product type.<br>**Today —** product navigates to measurement sets via the relationship + getMeasurements flow<br>**Done when:**<br>• `Product.measurementSets` resolves internally via `measurementService`<br>• no gateway hop<br>• Parity vs current product resolver |
| 🔸 `MST-BE-F-02`<br>Contribute `sampleMeasurement` to the `SampleV2` entity | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Contribute a sample's measurement set to the Sample entity.<br>**Today —** sample navigates to its measurement set via getSampleMeasurement<br>**Done when:**<br>• `SampleV2.sampleMeasurement` resolves<br>• Parity vs current |


### 🧪 Phase G — Field Resolvers & Tests (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `MST-BE-G-01`<br>`Measurement` field resolvers (13 fields) | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `sampleV2`, `measurementTemplate`, `sizeTemplate`, `tightFit`, `vmm`, `userAttributes` | B-01 | **Intent —** Resolve the everyday measurement fields (people, product, partners).<br>**Today —** access/currentUserPermissions , businessPartners (loadBps), createdBy/updatedBy (getUserByIDOrNullIfNotFound), product (PID-prefixed → internal product.getByID)…<br>**Done when:**<br>• All 13 fields resolve<br>• `product` null when `resourceId` not `PID*`<br>• `status` = `{statusId, statusName}`<br>• `workspaces` empty → null<br>• `updatedFromResource` resolves only for `type==='sample'` |
| 🔸 `MST-BE-G-02`<br>`SampleMeasurementSet` field resolvers (2 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | B-01 | **Intent —** Resolve the sample-measurement-set fields.<br>**Today —** 2 @DgsData fields<br>**Done when:**<br>• `createdBy` resolves by user id (null id → null)<br>• `measurementSizeId` = `measurementSize.code` |
| 📄 `MST-BE-G-03`<br>Test coverage & parity | 🟡 Medium `M` | Tests | B-01, C-01, E-01, G-01 | **Intent —** Prove the measurement subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity fixtures for the 7 queries + 8 mutations + updateMeasurement 3 fixtures + the relationship path<br>**Done when:**<br>• Unit ≥80%<br>• Parity green for reads/writes incl. `getMeasurements` relationship path<br>• `updateMeasurement` failure path covered |

