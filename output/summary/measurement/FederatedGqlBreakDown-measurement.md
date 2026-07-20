## Backend

### Federated GraphQL Breakdown — Measurement

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **M** |
| **Total Stories** | 30 |
| **Complexity** | 🔴 0 Very High · 🟠 1 High · 🟡 5 Medium · 🟢 24 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H |
| **Generated** | 2026-07-19 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H

---

#### What Are We Building?

- We are moving the **Measurement** domain — measurement sets (the size/point-of-measure specs for a product), their sample measurements, and the master-data unit lists — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **mid-sized and mid-low risk**: 7 queries, 8 mutations, 15 field resolvers on a 175-line resolver, with **no polymorphism**.
- The one genuinely harder piece is `updateMeasurement`, a 2-step write (workspace association, then body) with no rollback today.

`getMeasurements` depends on the **relationship** service to find a product's measurement-set ids, and the
template/size/tight-fit references are **separate sibling domains** we only reference (not migrate here).

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** ([`complexStories/acl/01-adr-acl-mid-request-update.md`](https://github.com/XXX/blob/main/output/complexStories/acl/01-adr-acl-mid-request-update.md)), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); measurement has zero downstream-token sites.

---

#### Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 3 cacheable master-data |
| Mutations | 8 | 6 simple + `updateMeasurement` (2-step) + add |
| Field-resolver type blocks | 2 | `Measurement` (13), `SampleMeasurementSet` (2) |
| External dependencies | 11 keys (2 🔴 · 6 🟡 · 3 🔵) | relationship/search 🔴; templates 🟡 |
| Federation contributions | 2 (Product, SampleV2) | BLOCKED-BY product/sample |
| **Total stories** | **20** | green-field |

---

#### Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `MST-BE-E-01` — `updateMeasurement` — 2-step orchestrated write | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

#### Effort Snapshot

| Phase | Name | Stories | Effort (est., +20% buffer) |
|-------|------|---------|----------------------------|
| B | Core Reads | 9 | 11–22d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations | 10 | 14–29d |
| E | Complex Operations | 1 | 5–8d |
| F | Federation & Stitching | 1 | 2–5d |
| G | Field Resolvers & Tests | 6 | 8–17d |
| H | Entity Resolution | 1 | 1–2d |
| **Total** | | **30** | **45–90d** (buffered) |

> Computed live from `be-04-stories.md` (phase + complexity per story) — always reconciles with the story tables below and the program overview. Effort = sum of per-story nominal day-ranges (Low 1–2 · Medium 2–4 · High 4–7 · Very High 7–12) × 1.2 buffer, AI-estimated — confirm in refinement. See each story's **Depends On** column for real sequencing.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~8–14 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel |
| 3 engineers | ~4–6 sprints | critical path A → E-01 → G-01 → G-04 |

---

#### Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-04 | listing + simple mutations |
| 3 | D-05–D-07 + E-01 | remaining mutations + `updateMeasurement` |
| 4 | G-01–G-02, G-04 | field resolvers (G-04 recommended, PO-gated). Test coverage/parity tracked outside this Jira pipeline, created manually. |
| post-launch | F-01, H-01 | federation contributions |

---

#### Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `B-09`, 🟡 `C-01`, 🟢 `C-02`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟡 `D-06`, 🟢 `D-07`, 🟠 `E-01`, 🟡 `F-01`, 🟢 `G-02`, 🟢 `H-01` | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)<br>`H-01` → ⛔ BLOCKED-BY sample | Fan-out — 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests · 🧬 Entity Resolution |
| 3 | 🟢 `D-08`, 🟢 `D-09`, 🟢 `D-10`, 🟡 `G-01`, 🟢 `G-04`, 🟢 `G-05`, 🟢 `G-06`, 🟢 `G-07` | — | ✏️ Mutations · 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `B-06` → `D-08` — 3 sequential stories; everything else hangs off this chain in parallel.

---

#### Recommended Story Graph — 1 Backend Engineer

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 1 backend engineer** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 |
|---|---|
| 1 | 🟢 `B-01` (1–2d) |
| 2 | 🟠 `E-01` (4–7d) 🔬 ⛔ |
| 3 | 🟢 `B-06` (1–2d) |
| 4 | 🟢 `B-07` (1–2d) |
| 5 | 🟢 `B-08` (1–2d) |
| 6 | 🟢 `B-02` (1–2d) |
| 7 | 🟢 `B-05` (1–2d) |
| 8 | 🟡 `C-01` (2–4d) |
| 9 | 🟡 `D-01` (2–4d) |
| 10 | 🟡 `D-06` (2–4d) |
| 11 | 🟡 `F-01` (2–4d) |
| 12 | 🟡 `G-01` (2–4d) |
| 13 | 🟢 `B-03` (1–2d) |
| 14 | 🟢 `B-04` (1–2d) |
| 15 | 🟢 `B-09` (1–2d) |
| 16 | 🟢 `C-02` (1–2d) |
| 17 | 🟢 `D-02` (1–2d) |
| 18 | 🟢 `D-03` (1–2d) |
| 19 | 🟢 `D-04` (1–2d) |
| 20 | 🟢 `D-05` (1–2d) |
| 21 | 🟢 `D-07` (1–2d) |
| 22 | 🟢 `D-08` (1–2d) |
| 23 | 🟢 `D-09` (1–2d) |
| 24 | 🟢 `D-10` (1–2d) |
| 25 | 🟢 `G-02` (1–2d) |
| 26 | 🟢 `G-04` (1–2d) |
| 27 | 🟢 `G-05` (1–2d) |
| 28 | 🟢 `G-06` (1–2d) |
| 29 | 🟢 `G-07` (1–2d) |
| 30 | 🟢 `H-01` (1–2d) ⛔ |

**BE-1:** `B-01` → `E-01` → `B-06` → `B-07` → `B-08` → `B-02` → `B-05` → `C-01` → `D-01` → `D-06` → `F-01` → `G-01` → `B-03` → `B-04` → `B-09` → `C-02` → `D-02` → `D-03` → `D-04` → `D-05` → `D-07` → `D-08` → `D-09` → `D-10` → `G-02` → `G-04` → `G-05` → `G-06` → `G-07` → `H-01`

**Elapsed (nominal midpoints):** ~56 working days.

---

#### Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

##### 📖 Phase B — Core Reads (9 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `MST-BE-B-01`<br>`getMeasurementByIds` data fetcher | 🟢 Low `XS` | Query | — | **Intent —** Fetch measurement sets by id.<br>**Today —** GET … → camelCase. ignored in DGS<br>**Done when:**<br>• Returns measurements for ids with `calculated` flag forwarded<br>• Empty ids → `[]`<br>• snake→camel mapping |
| 🔷 `MST-BE-B-02`<br>`getUnitsOfMeasure` (cacheable) | 🟢 Low `XS` | Query | B-01 | **Intent —** Return the unit-of-measure lookup list (cached).<br>**Today —** GET … → units_of_measure camelCase<br>**Done when:**<br>• Returns UoM list (optionally filtered by ids)<br>• Cached |
| 🔷 `MST-BE-B-03`<br>`getThicknessUnitsOfMeasure` (cacheable) | 🟢 Low `XS` | Query | B-01 | **Intent —** Return the thickness unit-of-measure lookup (cached).<br>**Today —** GET … → units_of_measure<br>**Done when:**<br>• Returns thickness UoM list<br>• Cached |
| 🔷 `MST-BE-B-04`<br>`getMeasurementSetStatus` (cacheable) | 🟢 Low `XS` | Query | B-01 | **Intent —** Return the measurement-set status lookup (cached).<br>**Today —** GET … → {key:value} map → [{code, description}]<br>**Done when:**<br>• Returns statuses<br>• Cached<br>• key→code, value→description |
| 🔷 `MST-BE-B-05`<br>`getSampleMeasurement` data fetcher | 🟢 Low `XS` | Query | B-01 | **Intent —** Fetch the measurement set for a sample.<br>**Today —** GET … → camelCase. ignored in DGS<br>**Done when:**<br>• Returns the sample measurement set for `sampleId`<br>• Not found → `null` |
| 🔷 `MST-BE-B-06`<br>`getMeasurementTemplates` + `getMeasurementTemplatesByIds` data fetchers | 🟢 Low `XS` | Query | — | **Intent —** List or look up measurement templates.<br>**Today —** getMeasurementTemplates(page, size) → GET …,desc (falsy params stripped, array params comma-joined) → camelCase, paged. getMeasurementTemplatesByIds(ids) → GET … →…<br>**Done when:**<br>• `getMeasurementTemplates` returns a sorted, paged list honoring `page`/`size`<br>• `getMeasurementTemplatesByIds` returns templates for the given ids<br>• Empty ids → empty paged content |
| 🔷 `MST-BE-B-07`<br>`getSizeTemplates` + `getSizeCategories` + `getMaterialTypes` data fetchers | 🟢 Low `XS` | Query | — | **Intent —** Look up size templates and their master-data lookups (size category, material type).<br>**Today —** getSizeTemplates(ids) → POST … (id+version pairs) → camelCase. getSizeCategories(ids) → GET … → size_categories camelCase (cacheable). getMaterialTypes(ids) → GET … →…<br>**Done when:**<br>• `getSizeTemplates` resolves by id+version pairs<br>• `getSizeCategories`/`getMaterialTypes` return the lookup lists, optionally filtered by ids, cached |
| 🔷 `MST-BE-B-08`<br>`getTightFits` + `getTightFitByIdAndVersion` data fetchers | 🟢 Low `XS` | Query | — | **Intent —** Search or look up tight-fit templates.<br>**Today —** getTightFits(ids, name, statusIds, brandIds, divisionIds, departmentIds) → GET … (qs-stringified) → camelCase, wrapped {tightFits}. getTightFitByIdAndVersion(id…<br>**Done when:**<br>• `getTightFits` filters by any combination of the given params<br>• `getTightFitByIdAndVersion` resolves the exact version; not found → `null` |
| 🔷 `MST-BE-B-09`<br>`searchSparkSizes` data fetcher (NEXUS + Tag fan-out) | 🟢 Low `XS` | Query<br>Calls: `NEXUS_Attributes` | — | **Intent —** Search sizes across both the Nexus platform and Spark's own tag-based sizes.<br>**Today —** Fans out in parallel: NEXUS_Attributes.Query.searchSizes(nameFilter, page:0, size) (platform, gateway stitch) tagged source:'Nexus', and…<br>**Done when:**<br>• Returns up to `size` results, Nexus + Spark tag sizes combined<br>• Each result tagged with its `source`<br>• Empty/no-match → `[]` |

> **`MST-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `measurement.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.


##### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `MST-BE-C-01`<br>`getMeasurements` data fetcher (relationship + listing) | 🟡 Medium `M` | Query<br>Calls: `relationship` | B-01 | **Intent —** List a resource's measurement sets (resolves the relationship first).<br>**Today —** relationships = relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0}). 2. ids = relationships.map(n => n.id); if empty → [].…<br>**Done when:**<br>• Resolves ids via relationship then fetches measurements<br>• No ids → `{content:[]}` (no measurement call)<br>• Sorted `createdAt DESC` (location documented) |
| 🔷 `MST-BE-C-02`<br>`getMeasurementsElastic` data fetcher | 🟢 Low `XS` | Query<br>Calls: `search` | B-01 | **Intent —** Search a product's measurement sets via elastic.<br>**Today —** {content} = search.getMeasurementSets → sort createdAt DESC → {content}. - EXT Service Calls: EXT → key: search · severity: — elastic measurement-set index<br>**Done when:**<br>• Returns elastic content for `parentId`<br>• Sorted `createdAt DESC`<br>• Empty → `{content:[]}` |


##### ✏️ Phase D — Mutations (10 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `MST-BE-D-01`<br>`addMeasurement` mutation | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create a measurement set.<br>**Today —** POST … (snake_case request, primeKey: humanId); on validationErrors\\|\\|message → throw. No ACL (new resource)<br>**Done when:**<br>• POST creates + returns mapped `Measurement`<br>• `validationErrors`/`message` → exception<br>• Cache primed with `humanId` |
| 🔶 `MST-BE-D-02`<br>`updateMeasurementAccess` mutation | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Change who can access a measurement set.<br>**Today —** PUT …/{id}/permission body {systemTeamIds} or {systemTeamDto} (whichever provided). ignored in DGS<br>**Done when:**<br>• Sends `{systemTeamIds}` when provided, else `{systemTeamDto}`<br>• Returns updated measurement<br>• Input-shape decision recorded |
| 🔶 `MST-BE-D-03`<br>`lockMeasurementSet` mutation | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Lock a measurement set from edits.<br>**Today —** PUT …/{id}/lock. ignored in DGS<br>**Done when:**<br>• PUT `/lock` returns locked set<br>• 404 → null |
| 🔶 `MST-BE-D-04`<br>`unlockMeasurementSet` mutation | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Unlock a measurement set.<br>**Today —** PUT …/{id}/unlock<br>**Done when:**<br>• PUT `/unlock` returns unlocked set<br>• 404 → null |
| 🔶 `MST-BE-D-05`<br>`updateMeasurementComponentStatus` mutation | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Update the component status on measurement sets.<br>**Today —** PUT …/component_status_update body {productId, ids, status}. No ACL token — confirm backend enforces (like BOM D-05)<br>**Done when:**<br>• PUT sends `{productId, ids, status}` snake_case<br>• Returns `MeasurementPaged{content}`<br>• Auth decision recorded |
| 🔶 `MST-BE-D-06`<br>`putSampleMeasurementSet` mutation | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create or replace a sample's measurement set.<br>**Today —** PUT …/sample (primeKey: sampleId); token for [measurementSetId, sampleId]; on validationErrors\\|\\|message → throw<br>**Done when:**<br>• PUT upserts the sample set<br>• `validationErrors`/`message` → exception<br>• Cache primed by `sampleId` |
| 🔶 `MST-BE-D-07`<br>`deleteSampleMeasurementSet` mutation | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Delete a sample's measurement set.<br>**Today —** DELETE …/sample/{sampleId}. ignored in DGS<br>**Done when:**<br>• DELETE removes the sample set; returns the deleted/empty result<br>• 404 → null |
| 🔶 `MST-BE-D-08`<br>`addMeasurementTemplate` + `updateMeasurementTemplate` + `deleteMeasurementTemplate` mutations | 🟢 Low `XS` | Mutation | B-06 | **Intent —** Create, update, or delete a measurement template.<br>**Today —** addMeasurementTemplate — token [SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY] → POST … (snake_case request); on validationErrors\\|\\|message → throw. updateMeasurementTemplate…<br>**Done when:**<br>• `add`/`update` POST/PUT create or replace the template; `validationErrors`/`message` → exception<br>• `delete` removes the templates for the given ids<br>• Delete auth decision recorded (no JWT today) |
| 🔶 `MST-BE-D-09`<br>`addSizeTemplate` + `updateSizeTemplate` mutations | 🟢 Low `XS` | Mutation | B-07 | **Intent —** Create or update a size template.<br>**Today —** token [SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY] → POST … (add) / PUT … (update), both snake_case request/camelCase response; on validationErrors\\|\\|message → throw<br>**Done when:**<br>• `add`/`update` POST/PUT create or replace the size template<br>• `validationErrors`/`message` → exception |
| 🔶 `MST-BE-D-10`<br>`addTightFit` + `updateTightFit` mutations | 🟢 Low `XS` | Mutation | B-08 | **Intent —** Create or update a tight-fit template.<br>**Today —** token [SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY] → POST … (add) / PUT … (update), both snake_case request/camelCase response; on validationErrors\\|\\|message → throw<br>**Done when:**<br>• `add`/`update` POST/PUT create or replace the tight fit<br>• `validationErrors`/`message` → exception |


##### ⚙️ Phase E — Complex Operations (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `MST-BE-E-01`<br>`updateMeasurement` — 2-step orchestrated write<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `workspaceV2` | SPIKE-01, B-01 | **Intent —** Edit a measurement set — a 2-step write (workspace + body) that has no rollback today.<br>**Today —** workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations \\|\\| {}. token for [humanId]. 2. If add/remove workspaces → workspaceAssociationHelper(MEASUREMENT…<br>**Done when:**<br>• Parity for 3 fixtures: body-only; body+workspace-add; body+workspace-remove<br>• Workspace step runs before body PUT<br>• Body PUT omits `humanId`<br>• Chosen failure strategy implemented<br>• `validationErrors`/`message` → exception | ☐ Unit: order workspace→body<br>☐ Unit: no-workspace skip<br>☐ Unit: body-failure path<br>☐ Parity: 3 fixtures |


##### 🔗 Phase F — Federation & Stitching (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `MST-BE-F-01`<br>Implement `Product.measurementSets` (internal) | 🟡 Medium `M` | Field Resolver<br>Calls: `relationship` | B-01 | **Intent —** Expose a product's measurement sets on the Product type.<br>**Today —** product navigates to measurement sets via the relationship + getMeasurements flow<br>**Done when:**<br>• `Product.measurementSets` resolves internally via `measurementService`<br>• no gateway hop<br>• Parity vs current product resolver |


##### 🧪 Phase G — Field Resolvers & Tests (6 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `MST-BE-G-01`<br>`Measurement` field resolvers (13 fields) | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `sampleV2`, `vmm`, `userAttributes` | B-01, B-06, B-07, B-08 | **Intent —** Resolve the everyday measurement fields (people, product, partners, templates).<br>**Today —** access/currentUserPermissions , businessPartners (loadBps), createdBy/updatedBy (getUserByIDOrNullIfNotFound), product (PID-prefixed → internal product.getByID)…<br>**Done when:**<br>• All 13 fields resolve<br>• `product` null when `resourceId` not `PID*`<br>• `status` = `{statusId, statusName}`<br>• `workspaces` empty → null<br>• `updatedFromResource` resolves only for `type==='sample'` |
| 🔸 `MST-BE-G-02`<br>`SampleMeasurementSet` field resolvers (2 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | B-01 | **Intent —** Resolve the sample-measurement-set fields.<br>**Today —** 2 @DgsData fields<br>**Done when:**<br>• `createdBy` resolves by user id (null id → null)<br>• `measurementSizeId` = `measurementSize.code` |
| 🔸 `MST-BE-G-05`<br>`MeasurementTemplate` field resolvers (5 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `ig`, `vmm`, `userAttributes` | B-06 | **Intent —** Resolve a measurement template's people and item-group fields.<br>**Today —** createdBy/updatedBy (getUserByIDOrNullIfNotFound), departments/divisions (ig.department\\|division.getByID, empty-tolerant), brands (brand.getBrand, skipped when…<br>**Done when:**<br>• All 5 fields resolve<br>• `departments`/`divisions` null-tolerant on empty ids<br>• `brands` skipped (null) when `brandIds === -1` |
| 🔸 `MST-BE-G-06`<br>`SizeTemplate` field resolvers (3 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | B-07 | **Intent —** Resolve a size template's computed id and people fields.<br>**Today —** humanId (humanId \\|\\| id — computed fallback), createdBy/updatedBy (getUserByIDOrNullIfNotFound)<br>**Done when:**<br>• All 3 fields resolve<br>• `humanId` falls back to `id` when the record has no `humanId` |
| 🔸 `MST-BE-G-07`<br>`TightFit` field resolvers (5 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `ig`, `vmm`, `userAttributes` | B-08 | **Intent —** Resolve a tight-fit template's people and item-group fields.<br>**Today —** departments/divisions (ig.department\\|division.getByID, empty-tolerant), brands (brand.getBrand, skipped when brandIds === -1), createdBy/updatedBy…<br>**Done when:**<br>• All 5 fields resolve<br>• `departments`/`divisions` null-tolerant on empty ids<br>• `brands` skipped (null) when `brandIds === -1` |
| 🔸 `MST-BE-G-04`<br>`SampleMeasurementSet.sample` forward reference (recommended, PO-gated) | 🟢 Low `XS` | Field Resolver<br>Calls: `sample` | B-02 (carries B-05 `getSampleMeasurement`, grouped-XS merged) | **Intent —** Adds `sample { … }` on the sample measurement set — the forward twin of the existing<br>**Today —** schema adds sample: SampleV2 on SampleMeasurementSet; resolver emits<br>**Done when:**<br>• PO approval recorded (OQ-5) before implementation starts<br>• `sample { id }` resolves as a stub; `sampleId` unchanged<br>• Pairs cleanly with MST-BE-H-01 (no circular resolution at the gateway — verified by a two-hop smoke query) |


##### 🧬 Phase H — Entity Resolution (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `MST-BE-H-01`<br>Contribute `sampleMeasurement` to the `SampleV2` entity | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Contribute a sample's measurement set to the Sample entity.<br>**Today —** sample navigates to its measurement set via getSampleMeasurement<br>**Done when:**<br>• `SampleV2.sampleMeasurement` resolves<br>• Parity vs current |



---

## Frontend

### Federated GraphQL Breakdown — Measurement · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 4 |
| **Impact** | 🔴 0 High · 🟡 3 Medium · 🟢 1 Low |
| **Estimated effort** | 12–19 days (single-engineer) |
| **Phase-1 surface** | 16 operation-to-root-field rows · 5 client files · 8 components |
| **Generated** | 2026-07-19 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

#### What Are We Changing?

- Point the **Measurement** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

#### Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `MST-FE-001` | Migrate measurement reads and retire `humanId` | Query migration | 🟡 Medium | 4–6 days | `MST-BE-B-01`, `MST-BE-B-04` | `getMeasurementByIds`, `getMeasurementSetStatus`, `getMeasurementComponentStatus` |
| `MST-FE-002` | Migrate measurement list/search reads | Query migration | 🟡 Medium | 3–5 days | `MST-BE-C-01`, `MST-BE-C-02` | `getMeasurements`, `getMeasurementsElastic` |
| `MST-FE-003` | Migrate measurement master-data reads | Query migration | 🟢 Low | 1–2 days | `MST-BE-B-02`, `MST-BE-B-03` | `getUnitsOfMeasure`, `getThicknessUnitsOfMeasure` |
| `MST-FE-004` | Migrate measurement mutations | Mutation migration | 🟡 Medium | 4–6 days | `MST-BE-D-03`, `MST-BE-D-04`, `MST-BE-D-06`, `MST-BE-D-07` | `lockMeasurementSet`, `unlockMeasurementSet`, `putSampleMeasurementSet`, `deleteSampleMeasurementSet` |

---

#### Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟡 `MST-FE-001`, 🟢 `MST-FE-003` | `MST-FE-001` → `MST-BE-B-01`, `MST-BE-B-04`<br>`MST-FE-003` → `MST-BE-B-02`, `MST-BE-B-03` | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `MST-FE-002` | `MST-FE-002` → `MST-BE-C-01`, `MST-BE-C-02` | Search & listing — needs backend phase C |
| 3 | 🟡 `MST-FE-004` | `MST-FE-004` → `MST-BE-D-03`, `MST-BE-D-04`, `MST-BE-D-06`, `MST-BE-D-07` | Writes — needs backend phase D mutations |

**Cutover flow:** `MST-FE-001` → `MST-FE-003` → `MST-FE-002` → `MST-FE-004`.

---

#### Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 1 | 🟡 `MST-FE-001` (4–6d)<br>🟢 `MST-FE-003` (1–2d) | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `MST-FE-002` (3–5d) | Search & listing — needs backend phase C |
| 3 | 🟡 `MST-FE-004` (4–6d) | Writes — needs backend phase D mutations |

**Elapsed (nominal midpoints):** ~16 FE build days — calendar time is set by the backend gates, not FE capacity.

---

#### References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-measurement.md — the combined Backend + Frontend breakdown this section lives in.

