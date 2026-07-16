# Federated GraphQL Breakdown — Packaging

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **L** |
| **Total Stories** | 24 |
| **Complexity** | 🔴 0 Very High · 🟠 2 High · 🟡 9 Medium · 🟢 13 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-16 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Packaging** domain — packaging records, their dielines (print artwork specs), printers, elements, and exports — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is
**mid-sized with a wide schema** (24 object types, 20 inputs): 7 queries, 10 mutations, 17 field resolvers
on a 273-line resolver, but **no polymorphism**.

Two pieces carry the real work: **`updatePackaging`**, a multi-step write (body, then attachment
remove via archive + relationship, then attachment add via relationship + attribute update) with no
rollback; and **`suggestedRetailPriceByDPCI`**, a multi-hop pricing field (printers → dielines → DPCIs →
pricing service).

**ACL note:** the current code obtains per-resource capability tokens via ACL; Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs ([`complexStories/*/02-adr-noacl-*.md`](https://github.com/XXX/blob/main/output/complexStories/*/02-adr-noacl-*.md)) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 10 | 9 simple + `updatePackaging` (multi-step) |
| Field-resolver type blocks | 4 | `Packaging` (12), `Dieline` (3), `PrinterDieline` (1), `PackagingElement` (1) |
| External dependencies | 7 keys (2 🔴 · 3 🟡 · 2 🔵) | search/attachment 🔴; relationship/user-profile/tag 🟡 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **24** | green-field |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `PKG-BE-E-01` — `updatePackaging` (multi-step write) | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 6 | 6–11d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 9 | 13–22d |
| E | Complex (`updatePackaging`) | 1 | 5–8d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 6 | 15–25d |
| **Total** | | **24** | **42–72d** (buffered) |

> One engineer ≈ **9–15 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~10–17 sprints | sequential |
| 2 engineers | ~6–10 sprints | reads + mutations parallel after B-01 |
| 3 engineers | ~4–7 sprints | critical path A → E-01 → G-04 → G-06 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, core reads |
| 2 | B-04–B-06 + C-01 + D-02/D-05–D-07 | master-data + search + simple mutations |
| 3 | D-01/D-03/D-04/D-08/D-09 | create/bulk/clone/component-status |
| 4 | E-01 + F-01 | multi-step update + Product links |
| 5 | G-01–G-03 | ACL/users/refs field resolvers |
| 6 | G-04/G-05 + G-06 | pricing + dieline resolvers + tests |

---

## Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step |
|---|---|---|
| 1 | 🟢 `B-01` | — |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟡 `C-01`, 🟡 `D-01`, 🟢 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟢 `D-05`, 🟢 `D-06`, 🟢 `D-07`, 🟡 `D-08`, 🟢 `D-09`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟢 `G-02`, 🟡 `G-03`, 🟠 `G-04`, 🟡 `G-05` | `E-01` → 🔬 SPIKE-01 |
| 3 | 🟡 `G-06` | — |

**Critical path:** `B-01` → `G-03` → `G-06` — 3 sequential stories; everything else hangs off this chain in parallel.

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (6 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PKG-BE-B-01`<br>`getPackagings(...)` | 🟢 Low `XS` | Query | — | **Intent —** List packagings with paging and filters.<br>**Today —** getPackagings() → paged<br>**Done when:**<br>• all 7 filter args forwarded; defaults page=0/size=10000 |
| 🔷 `PKG-BE-B-02`<br>`getPackagingById(packagingId)` | 🟢 Low `XS` | Query | B-01 | **Intent —** Fetch one packaging by id.<br>**Today —** token → getPackagingById<br>**Done when:**<br>• returns packaging; miss→null |
| 🔷 `PKG-BE-B-03`<br>`getDielines(...)` | 🟢 Low `XS` | Query | B-01 | **Intent —** List dielines (print layouts) for a packaging.<br>**Today —** getDielines → .dielines<br>**Done when:**<br>• filters forwarded; returns the `dielines` array |
| 🔷 `PKG-BE-B-04`<br>`getPackagingFieldValuesByType(type, ids)` | 🟢 Low `XS` | Query | B-01 | **Intent —** Return packaging field-value lookups by type.<br>**Today —** getPackagingFieldValuesByType(type, ids)<br>**Done when:**<br>• by type (+optional ids) |
| 🔷 `PKG-BE-B-05`<br>`getDielineEvaluationStatuses` (cacheable) | 🟢 Low `XS` | Query | B-01 | **Intent —** Return the dieline evaluation-status lookup (cached).<br>**Today —** getDielineEvaluationStatuses()<br>**Done when:**<br>• returns statuses; cached |
| 🔷 `PKG-BE-B-06`<br>`getCountries(codes)` (cacheable) | 🟢 Low `XS` | Query | B-01 | **Intent —** Return the country lookup (cached).<br>**Today —** getCountries(codes)<br>**Done when:**<br>• returns countries (optionally filtered by codes) |

> **`PKG-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `packaging.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.


### 🔍 Phase C — Search & Listing (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PKG-BE-C-01`<br>`getPackagingElastic(parentHumanId)` | 🟡 Medium `M` | Query<br>Calls: `search` | B-01 | **Intent —** Search a product's packagings via elastic.<br>**Today —** (search) search.getPackagingElastic → .content. EXT: search<br>**Done when:**<br>• `parentId:` elastic query built; returns content |


### ✏️ Phase D — Mutations (9 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `PKG-BE-D-01`<br>`addPackaging` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create a packaging.<br>**Today —** POST packaging/v1. Throw on validationErrors/message<br>**Done when:**<br>• creates<br>• validation error → exception |
| 🔶 `PKG-BE-D-02`<br>`evaluateDieline` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Trigger evaluation of a dieline.<br>**Today —** PUT packaging/v1/dielines/{dielineId}/evaluate<br>**Done when:**<br>• evaluates the dieline |
| 🔶 `PKG-BE-D-03`<br>`bulkAddPackagings` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create many packagings at once.<br>**Today —** bulkAddPackagings. Throw on validationErrors/message<br>**Done when:**<br>• bulk creates<br>• error → throw |
| 🔶 `PKG-BE-D-04`<br>`bulkUpdatePackagings` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Update many packagings at once.<br>**Today —** token for packaging[].humanId → bulkUpdatePackagings. Throw on error<br>**Done when:**<br>• bulk updates<br>• error → throw |
| 🔶 `PKG-BE-D-05`<br>`exportPackaging` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Kick off a packaging export.<br>**Today —** token → requestPackagingExport({workspace_id, workspace_description, product_ids}) → request id<br>**Done when:**<br>• returns the export request id |
| 🔶 `PKG-BE-D-06`<br>`lockPackaging` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Lock a packaging from edits.<br>**Today —** token → PUT packaging/v1/{id}/lock<br>**Done when:**<br>• locks |
| 🔶 `PKG-BE-D-07`<br>`unlockPackaging` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Unlock a packaging.<br>**Today —** token → PUT packaging/v1/{id}/unlock<br>**Done when:**<br>• unlocks |
| 🔶 `PKG-BE-D-08`<br>`cloneFilesForDielines` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B-01 | **Intent —** Copy attachment files for dielines.<br>**Today —** token → Promise.all(attachmentIds.map(id => (attachment) cloneAttachmentV3({cloneReferences}, id))), flatten. EXT: attachment<br>**Done when:**<br>• clones each id with the shared `cloneReferences` |
| 🔶 `PKG-BE-D-09`<br>`updatePackagingComponentStatus` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Update component status on packagings.<br>**Today —** updatePackagingComponentStatus({productId, ids, status}). No JWT — confirm backend-enforced<br>**Done when:**<br>• updates statuses<br>• no-token behaviour documented |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `PKG-BE-E-01`<br>`updatePackaging` (multi-step write)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `attachment`, `relationship` | SPIKE-01, B-01 | **Intent —** Edit a packaging — a multi-step write (body + attachments + relationships) with no rollback today.<br>**Today —** token; set humanId=packagingId; PUT packaging/v1 (body); 2) if attachmentsToRemove → (attachment) archiveAttachmentBulkV2 + (relationship) removeRelationship; 3) if…<br>**Done when:**<br>• all branches in order<br>• add rejects on status≥400; remove error handling decided<br>• partial-failure strategy | ☐ body-only<br>☐ remove<br>☐ add<br>☐ status≥400<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PKG-BE-F-01`<br>Product packaging links (internal, same subgraph) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Expose a product's packagings on the Product type (same subgraph).<br>**Today —** Product references packaging (e.g. components(...packaging), packaging attributes) from the co-located packaging service<br>**Done when:**<br>• resolves in-process; no gateway hop |


### 🧪 Phase G — Field Resolvers & Tests (6 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `PKG-BE-G-01`<br>`access` + `businessPartner` + `participantDetails` | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm`, `userGroup` | B-01 | **Intent —** Resolve a packaging's access / partner / participant fields.<br>**Done when:**<br>• each resolves; null-safe | — |
| 🔸 `PKG-BE-G-02`<br>`createdBy` + `updatedBy` + `dielineEvaluators` | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | B-01 | **Intent —** Resolve the people fields on a packaging.<br>**Done when:**<br>• each resolves; null id → null | — |
| 🔸 `PKG-BE-G-03`<br>`product` + `workspaces` + `attachments` | 🟡 Medium `M` | Field Resolver<br>Calls: `search` | B-01 | **Intent —** Resolve a packaging's product, workspaces and attachments.<br>**Done when:**<br>• `product` null when not `PID*`<br>• workspaces/attachments via elastic | — |
| 🔸 `PKG-BE-G-04`<br>`suggestedRetailPriceByDPCI` + `waveDescription` + `retailPrice` | 🟠 High `L` | Field Resolver<br>Calls: `tag`, `apex` | B-01 | **Intent —** Resolve pricing fields (the dieline→DPCI→price chain).<br>**Today —** suggestedRetailPriceByDPCI — gated on requiresSuggestedRetailPrice + a BP id: - collect printer ids from packagingElements → getDielines(printerIds) → unique dpcis →…<br>**Done when:**<br>• price chain matches source; gate honored<br>• wave tag fallback<br>• `retailPrice`→0 | ☐ price chain<br>☐ gate<br>☐ wave<br>☐ retailPrice |
| 🔸 `PKG-BE-G-05`<br>`Dieline` + `PrinterDieline` + `PackagingElement` field resolvers | 🟡 Medium `M` | Field Resolver<br>Calls: `attachment`, `search`, `userAttributes` | B-01 | **Intent —** Resolve the dieline / printer-dieline / element sub-type fields.<br>**Done when:**<br>• each field resolves to the right source | — |
| 📄 `PKG-BE-G-06`<br>Tests, parity harness | 🟡 Medium `M` | Tests | B-01, E-01, G-03, G-04 | **Intent —** Prove the packaging subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity fixtures (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green<br>• schema-diff intentional | — |

