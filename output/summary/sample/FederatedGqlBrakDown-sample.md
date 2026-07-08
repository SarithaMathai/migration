# Federated GraphQL Breakdown — Sample

| | |
|---|---|
| **Target DGS** | `plm-sample (separate)` |
| **T-Shirt Size** | **XL** |
| **Total Stories** | 28 |
| **Complexity** | 🔴 0 Very High · 🟠 5 High · 🟡 11 Medium · 🟢 12 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Sample** domain — physical/virtual samples, their rounds, evaluations, RFID locations and master-data — off the `spark-internal-graphql` gateway into its **own `plm-sample` DGS subgraph**.
- Sample is referenced by **product** (`Product.samples`/`sampleIds`), **measurement** (`SampleV2.sampleMeasurement`) and
**workspace** (sample report + drop/undrop).

- It is **large and mid-high risk**: 23 queries, 9 mutations **(+3 schema-drift)**, ~45 field resolvers on a 430-line resolver.
- The cost concentrates in the **wide `SampleV2` entity** with **prefix-gated polymorphic parent hydration** (product / trim / color / fabric / artwork / asset), the **`SampleAsset` union**, and two evaluation writes (`updateSamplesV2`, `bulkEvaluateSamples`).
- A long master-data tail (~13 cacheable lookups) is cheap.

**ACL note:** reads/writes curry capability tokens; drop/undrop bookkeeping lives in the workspace dispatcher.
**ACL is ignored in the DGS implementation** (no ACL story) — context only.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 23 | ~13 cacheable master-data + by-id/parent + 2 RFID |
| Mutations | 9 (+3 deferred) | create/round/update/workspace-assoc/export/retry/clone + 2 evaluation writes |
| Field-resolver type blocks | ~7 | `SampleV2` (~35) + 6 sub-types |
| Polymorphism | 1 union (`SampleAsset`) | B01 |
| External dependencies | ~20 keys (all cross-subgraph) | search 🔴; product/workspace/measurement/material/… 🟡 |
| Federation role | provides `SampleV2` entity | product/measurement/workspace reference it |
| **Total stories** | **33** | green-field; separate subgraph |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `SPARK-SMPL-B01` — `getSampleById(id)` | `SPARK-SPIKE-05` | Polymorphic Type Resolution |
| 🔴🔬 `SPARK-SMPL-E01` — `updateSamplesV2` | `SPARK-SPIKE-01` | Non-Atomic Write Saga |
| 🔴🔬 `SPARK-SMPL-E02` — `bulkEvaluateSamples` | `SPARK-SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 8 | 8–14d |
| C | RFID Reads | 2 | 4–7d |
| D | Mutations (simple) | 7 | 11–18d |
| E | Complex (evaluation writes) | 2 | 9–15d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 7 | 31–51d |
| **Total** | | **33** | **70–116d** (buffered) |

> One engineer ≈ **14–24 sprints**. Parallelizable after B01; 2–3 engineers recommended.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories; the `SampleAsset` union `@DgsTypeResolver` remains a dedicated story.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~16–27 sprints | sequential |
| 2 engineers | ~10–16 sprints | reads + mutations parallel after B01 |
| 3 engineers | ~6–11 sprints | critical path A → G02 → G07; E in parallel |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | B01 (DGS module init + service wiring + first resolver) | schema, union resolver, service port, reads + master-data |
| 3 | C01/C02 + D02–D06 | RFID + simple mutations |
| 4 | D01/D07 + E01/E02 | create(+files), clone, evaluation writes |
| 5 | G01/G02 | users + the prefix-gated parents/union (X-Large) |
| 6 | G03–G06 | partners/assoc/attachments/participants |
| 7 | F01/F02 + G07 | entity fetcher + drift decision + tests |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (8 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔴🔬 🔷 `SPARK-SMPL-B01`<br>`getSampleById(id)`<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-05` (Polymorphic Type Resolution) — see global Spike Detail_ | 🟢 Low `XS` | Query | SPARK-SPIKE-05 | **Intent —** Fetch one sample by id.<br>**Today —** getSampleById<br>**Done when:**<br>• returns sample; miss→null |
| 🔷 `SPARK-SMPL-B02`<br>`getSamplesByIdsV2(ids)` (batched) | 🟡 Medium `M` | Query<br>Calls: `recentlyViewed` | B01 | **Intent —** Fetch several samples by ids (batched); records 'recently viewed'.<br>**Today —** batchParallelOperation(chunk) → token per batch → getSamplesByIdsV2ByPost. Side-effect: exactly-one → (recentlyViewed) addRecentlyViewed<br>**Done when:**<br>• batched by chunk size<br>• single → recentlyViewed |
| 🔷 `SPARK-SMPL-B03`<br>`getSamplesByParentId(humanId)` | 🟡 Medium `M` | Query<br>Calls: `relationship` | B01 | **Intent —** List a product's samples.<br>**Today —** (relationship) getByID({id, type:'sample', maxDepth:0}) → ids → token → getSamplesByIdsV2; empty → []<br>**Done when:**<br>• relationship→ids→samples chain |
| 🔷 `SPARK-SMPL-B04`<br>`getColorSamplesByParentId(id)` | 🟢 Low `XS` | Query | B01 | **Intent —** List a product's colour samples.<br>**Today —** getColorSamplesByParentId<br>**Done when:**<br>• returns color samples |
| 🔷 `SPARK-SMPL-B05`<br>`getSampleRounds(humanId)` | 🟢 Low `XS` | Query | B01 | **Intent —** List the evaluation rounds on a sample.<br>**Today —** token → getSampleRounds<br>**Done when:**<br>• returns rounds |
| 🔷 `SPARK-SMPL-B06`<br>`getSampleExports` | 🟢 Low `XS` | Query | B01 | **Intent —** List sample export jobs.<br>**Today —** getSampleExports<br>**Done when:**<br>• returns exports |
| 🔷 `SPARK-SMPL-B07`<br>`getSampleNotificationErrors` | 🟢 Low `XS` | Query<br>Calls: `notification` | B01 | **Intent —** List failed sample notifications.<br>**Today —** (notification) getSampleNotificationErrors<br>**Done when:**<br>• returns errors |
| 🔷 `SPARK-SMPL-B08`<br>Master-data type/format/purpose queries (cacheable bundle) | 🟢 Low `XS` | Query | B01 | **Intent —** Return the sample type / format / purpose lookups (cached).<br>**Today —** thin master-data loads<br>**Done when:**<br>• each returns its list; cached |

> **`SPARK-SMPL-B01`** — **Note — DGS Module Init (this PR only):** Creates `sample.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql.


### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔷 `SPARK-SMPL-C01`<br>`getSampleLocationByIds(ids)` | 🟠 High `L` | Query<br>Calls: `search` | B01 | **Intent —** Find each sample's latest physical location via its RFID tags.<br>**Today —** batched samples → for each with rfidTagIds → (search) searchLatestRfidLocations({q: tagIds OR-joined}) → reduce to latest lastSeen → {id, locationDescription…<br>**Done when:**<br>• latest-location reduce correct<br>• no tags → [] | ☐ latest reduce<br>☐ no-tags<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔷 `SPARK-SMPL-C02`<br>`getSamplesByRfidTagIds(ids)` | 🟡 Medium `M` | Query | B01 | **Intent —** Find samples by their RFID tag ids.<br>**Today —** token → getSamplesByRfidTagIds<br>**Done when:**<br>• returns tag→sample pairs | — |


### ✏️ Phase D — Mutations (7 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `SPARK-SMPL-D01`<br>`createSamplesV2` | 🟡 Medium `M` | Mutation<br>Calls: `relationship`, `attachment` | B01 | **Intent —** Create samples (and link any attachment files).<br>**Today —** createSamplesV2; if first new sample has files → (relationship) createSampleAttachmentRelationship + token + (attachment) bulkUpdateAttributes (stamp…<br>**Done when:**<br>• creates<br>• file-relationship + attribute side-effects when files present |
| 🔶 `SPARK-SMPL-D02`<br>`createSampleRoundV2` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Create a new evaluation round on a sample.<br>**Today —** token [sampleId, SAMPLE_EVALUTION] → createSampleRoundV2<br>**Done when:**<br>• creates a round |
| 🔶 `SPARK-SMPL-D03`<br>`updateSampleWorkspaceAssociation` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Add / remove a sample's workspace links.<br>**Today —** token [sampleId, workspaceId] → updateSampleWorkspaceAssociation<br>**Done when:**<br>• associates sample to workspace |
| 🔶 `SPARK-SMPL-D04`<br>`requestSampleExport` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Kick off a sample export.<br>**Today —** requestSampleExport<br>**Done when:**<br>• returns request id |
| 🔶 `SPARK-SMPL-D05`<br>`retrySampleNotificationError` | 🟢 Low `XS` | Mutation<br>Calls: `notification` | B01 | **Intent —** Retry one failed sample notification.<br>**Today —** (notification) retrySampleNotificationError(failedMessageId)<br>**Done when:**<br>• retries one |
| 🔶 `SPARK-SMPL-D06`<br>`retryAllSampleNotificationErrors` | 🟢 Low `XS` | Mutation<br>Calls: `notification` | B01 | **Intent —** Retry all failed sample notifications.<br>**Today —** (notification) retryAllSampleNotificationErrors<br>**Done when:**<br>• retries all |
| 🔶 `SPARK-SMPL-D07`<br>`bulkCloneFilesForEvaluate` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B01 | **Intent —** Copy attachment files for sample evaluation.<br>**Today —** token → Promise.all(attachmentIds.map(id => (attachment) cloneAttachmentV3({cloneReferences}, id))), flatten<br>**Done when:**<br>• clones each id |


### ⚙️ Phase E — Complex Operations (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `SPARK-SMPL-E01`<br>`updateSamplesV2`<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation | SPARK-SPIKE-01, B01 | **Intent —** Update samples (the evaluation write).<br>**Today —** token for all updateSamples[].id + SAMPLE_EVALUTION → updateSamplesV2<br>**Done when:**<br>• bulk-updates samples (eval-scoped token) | ☐ update<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔴🔬 🔶 `SPARK-SMPL-E02`<br>`bulkEvaluateSamples`<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `attachment` | SPARK-SPIKE-01, B01 | **Intent —** Apply evaluations to many samples and create new rounds.<br>**Today —** delegates to bulkEvaluateSampleUtil(ctx, updateSamples, newSampleRounds) — applies evaluations and creates new sample rounds<br>**Done when:**<br>• evaluations + new rounds applied<br>• partial-failure handling decided | ☐ evaluate<br>☐ new rounds<br>☐ partial<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-SMPL-F01`<br>`SampleV2` federated entity fetcher | 🟡 Medium `M` | Field Resolver | B01 | **Intent —** Let other subgraphs resolve a Sample by key.<br>**Today —** @DgsEntityFetcher(name="SampleV2") resolving by id, so product (`Product<br>**Done when:**<br>• entity resolves by key<br>• `Product { samples { id } }` cross-subgraph smoke test |
| 📄 `SPARK-SMPL-F02`<br>Deferred drift mutation decision | 🟢 Low `XS` | Schema | E02 | **Intent —** Decide the fate of superseded / drift sample mutations.<br>**Today —** updateSampleEvaluations (no resolver — superseded by bulkEvaluateSamples), dropSamples/undropSamples (no resolver — run inside workspaceBusinessPartnerActionsV2)<br>**Done when:**<br>• decision + traffic survey |


### 🧪 Phase G — Field Resolvers & Tests (7 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `SPARK-SMPL-G01`<br>Users (created/updated/evaluated + evaluators + primary roles) | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `role` | B01 | **Intent —** Resolve the created / updated / evaluated-by people and evaluator roles.<br>**Done when:**<br>• each resolves; system-user branch preserved | — |
| 🔸 `SPARK-SMPL-G02`<br>Prefix-gated parents + `SampleAsset` union | 🟠 High `L` | Field Resolver<br>Calls: `product`, `trim`, `colorArchroma`, `combination`, `fabric`, `artwork`, `material` | B01 | **Intent —** Resolve a sample's parent (product / colour / fabric…) by id-prefix into the right type.<br>**Today —** prefix-gated hydration — product (PID, product), colorArchroma (ARCCLR/TARARCCLR/REFARCCLR, colorArchroma), fabricSpecCombo (FSC, combination), fabricSpec (FAS…<br>**Done when:**<br>• each prefix routes to the right loader<br>• `asset` union resolves<br>• non-matching → null | ☐ each prefix<br>☐ union<br>☐ null |
| 🔸 `SPARK-SMPL-G03`<br>Partners (`businessPartner`/`fabricSupplier`/`merchandiseVendors`/`brand`/`designPartnerId`) | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm`, `brand` | B01 | **Intent —** Resolve the business / fabric / vendor / brand partner fields.<br>**Done when:**<br>• each resolves; empty → [] | — |
| 🔸 `SPARK-SMPL-G04`<br>`workspace` + `sampleMeasurementSet` + `designCycle` + `clmPackage` | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `measurement`, `tag`, `tgtColorEvaluator` | B01 | **Intent —** Resolve workspace, measurement, design-cycle and package fields.<br>**Done when:**<br>• each resolves; gates preserved | — |
| 🔸 `SPARK-SMPL-G05`<br>`attachments` + `rfidLocationInfo` + `currentLocations` | 🟡 Medium `M` | Field Resolver<br>Calls: `search` | B01 | **Intent —** Resolve attachment and RFID-location fields.<br>**Done when:**<br>• attachments via elastic<br>• rfid latest-location preserved | — |
| 🔸 `SPARK-SMPL-G06`<br>participants + sub-types (+ library color + department) | 🟡 Medium `M` | Field Resolver<br>Calls: `userGroup`, `vmm`, `color`, `ig` | B01 | **Intent —** Resolve participant and related sub-type fields (library colour, department).<br>**Done when:**<br>• each resolves; Target-0 + system-user preserved | — |
| 📄 `SPARK-SMPL-G07`<br>Tests, parity harness, load test | 🟠 High `L` | Tests | B02, E02, G02 | **Intent —** Prove the sample subgraph matches the old gateway (incl. load test).<br>**Today —** ≥80% unit coverage; parity harness (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green<br>• load p95 parity<br>• schema-diff intentional | ☐ Parity: DGS response matches spark-internal-graphql baseline<br>☐ Load: p95 latency is within spark-internal-graphql baseline<br>☐ contract |

