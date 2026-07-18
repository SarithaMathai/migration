# Federated GraphQL Breakdown — Watchlist

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **M** |
| **Total Stories** | 12 |
| **Complexity** | 🔴 0 Very High · 🟠 1 High · 🟡 6 Medium · 🟢 5 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-17 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Watchlist** domain — quality watchlist entries on a product (reasons, statuses, inspections, partners, attachments) — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **small and mid-low risk**: 4 queries, 3 mutations, 13 field resolvers on a 129-line resolver, with **no polymorphism**.
- It is **co-located** in the product family, so `Product.watchlists` and the TechPack `ResourcesCount.watchlists` count resolve **internally** (not across the federation gateway).

The one genuinely harder piece is **`updateWatchlistEntries`**, a multi-step write (user-group upsert, then
the body, then attachment archival) that today **does not await** its per-entry user-group updates — a race
to fix on the port.

**ACL note:** the current code obtains per-resource capability tokens via ACL; Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs ([`complexStories/*/02-adr-noacl-*.md`](https://github.com/XXX/blob/main/output/complexStories/*/02-adr-noacl-*.md)) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 4 | 2 cacheable master-data; 1 four-step filtered read |
| Mutations | 3 | 2 simple + `updateWatchlistEntries` (multi-step) |
| Field-resolver type blocks | 3 | `Watchlist` (10), inspection (2), partner (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 2 (Product, ResourcesCount) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `WATCHLIST-BE-E-01` — `updateWatchlistEntries` (multi-step write) | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 3 | 3–6d |
| C | Search & Listing | 1 | 3–5d |
| D | Mutations (simple) | 2 | 4–7d |
| E | Complex (`updateWatchlistEntries`) | 1 | 4–7d |
| F | Federation (Product + TechPack, internal) | 2 | 2–4d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **13** | **25–44d** (buffered) |

> One engineer ≈ **5–9 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01 + D-01/D-02 | filtered read + simple mutations |
| 3 | E-01 + F-01/F-02 | multi-step update + Product/TechPack internal contributions |
| 4 | G-01–G-03 + G-04 | field resolvers + tests |

---

## Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟢 `B-02`, 🟡 `C-01`, 🟡 `D-01`, 🟡 `D-02`, 🟠 `E-01`, 🟢 `F-01`, 🟢 `G-01`, 🟡 `G-02`, 🟡 `G-03` | `E-01` → 🔬 SPIKE-01 | Fan-out — 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests |
| 3 | 🟡 `G-04`, 🟢 `G-05` | — | 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `E-01` → `G-04` — 3 sequential stories; everything else hangs off this chain in parallel.

---

## Recommended Story Graph — 2 Backend Engineers

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 2 backend engineers** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 | 👤 BE-2 |
|---|---|---|
| 1 | 🟢 `B-01` (1–2d) | ⏳ after `B-01` → 🟡 `C-01` (2–4d) |
| 2 | 🟠 `E-01` (4–7d) 🔬 | 🟡 `G-02` (2–4d) |
| 3 | 🟡 `D-01` (2–4d) | 🟡 `D-02` (2–4d) |
| 4 | 🟡 `G-03` (2–4d) | 🟡 `G-04` (2–4d) |
| 5 | 🟢 `B-02` (1–2d) *(grouped XS: +`B-03`)* | 🟢 `F-01` (1–2d) *(grouped XS: +`F-02`)* |
| 6 | 🟢 `G-01` (1–2d) | 🟢 `G-05` (1–2d) |

**BE-1:** `B-01` → `E-01` → `D-01` → `G-03` → `B-02` → `G-01`<br>**BE-2:** `C-01` → `G-02` → `D-02` → `G-04` → `F-01` → `G-05`

**Elapsed (nominal midpoints):** ~16 working days with 2 engineers vs ~31 days sequential.

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `WATCHLIST-BE-B-01`<br>`getWatchlistByIds(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Fetch watchlist entries by id.<br>**Today —** token → GET watchlist/v1?watchlistIds={csv} → camelCase<br>**Done when:**<br>• returns entries for ids; empty → [] |
| 🔷 `WATCHLIST-BE-B-02`<br>`getWatchlistReasons` · `getWatchlistInspectionActions` | 🟢 Low `XS` | Query | B-01 | **Grouped XS story —** combines former `B-03` (one PR train)<br>**Intent —** Return the watchlist-reason lookup (cached); Return the inspection-action lookup (cached)<br>**Today —** GET watchlist/v1/watchlist_reasons. ; GET watchlist/v1/watchlist_inspection_action_types<br>**Done when:**<br>• `getWatchlistReasons`: returns reasons; cached<br>• `getWatchlistInspectionActions`: returns actions; cached |

> **`WATCHLIST-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `watchlist.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.


### 🔍 Phase C — Search & Listing (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `WATCHLIST-BE-C-01`<br>`getWatchlistByFilter(...)` (4-step read) | 🟡 Medium `M` | Query<br>Calls: `search`, `product` | B-01 | **Intent —** List watchlist entries for a workspace's products (a 4-step read).<br>**Today —** (internal) product.getWorkspaceProducts({q,filter,workspaceId,page,size}) → product humanIds → (search) searchWatchlist({ q:"parentId:(... OR ...) AND…<br>**Done when:**<br>• product→search→watchlist chain preserved<br>• elastic query string exact (incl. `statusId: 501`) |


### ✏️ Phase D — Mutations (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `WATCHLIST-BE-D-01`<br>`createWatchlistEntries` | 🟡 Medium `M` | Mutation<br>Calls: `userGroup` | B-01 | **Intent —** Create watchlist entries (and their user-groups).<br>**Today —** Promise.all(entries.map(w => { createWatchlistEntries([w]); throw on validationErrors/message; then (user-group) addUserGroup({resourceId:humanId, participantDetails…<br>**Done when:**<br>• creates each entry + its user group<br>• either failure → exception |
| 🔶 `WATCHLIST-BE-D-02`<br>`cloneFilesForWatchlist` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B-01 | **Intent —** Copy attachment files for watchlist entries.<br>**Today —** token → Promise.all(attachmentIds.map((id,i) => (attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id))), stamp parentResource=id, flatten. EXT…<br>**Done when:**<br>• clones each id with its paired cloneReference; `parentResource` stamped |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `WATCHLIST-BE-E-01`<br>`updateWatchlistEntries` (multi-step write)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `attachment`, `userGroup` | SPIKE-01, B-01 | **Intent —** Edit watchlist entries — a multi-step write (user-groups + body); today the group step isn't awaited (a bug).<br>**Today —** per-entry (currently NOT awaited — bug): getUserGroups([humanId]); if existing participants → updateUserGroup, else (user-group) addUserGroup (throw on error); 2)…<br>**Done when:**<br>• user-group upserts complete before the watchlist update (race fixed)<br>• removed attachments archived<br>• partial-failure strategy | ☐ existing-participants path<br>☐ new-participants path<br>☐ attachment archive<br>☐ ordering/await<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `WATCHLIST-BE-F-01`<br>`Product.watchlists` · `ResourcesCount.watchlists` | 🟢 Low `XS` | Field Resolver | B-01 | **Grouped XS story —** combines former `F-02` (one PR train)<br>**Intent —** Expose a product's watchlists on the Product type; Contribute the watchlists count to the TechPack rollup<br>**Today —** Product exposes watchlists resolved from the co-located watchlist service<br>**Done when:**<br>• `Product.watchlists`: resolves in-process; no gateway hop<br>• `ResourcesCount.watchlists`: count resolves in-process; parity vs the TechPack facade |


### 🧪 Phase G — Field Resolvers & Tests (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `WATCHLIST-BE-G-01`<br>Computed flatteners (status/reasons/inspection action) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Flatten status / reason / inspection-action codes into readable fields.<br>**Today —** statusId=status.code, statusName=status.description, reasonIds=reasons[].code, reasons=reasons[].description; WatchlistInspection.actionId=action.code…<br>**Done when:**<br>• each flattener maps correctly |
| 🔸 `WATCHLIST-BE-G-02`<br>`createdBy` + `updatedBy` + `workspaces` + `participantDetails` + `partnerName` | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `workspaceV2`, `userGroup`, `vmm` | B-01 | **Intent —** Resolve the people, workspace and partner fields.<br>**Done when:**<br>• each resolves; null-safe |
| 🔸 `WATCHLIST-BE-G-03`<br>`attachments` + `product` | 🟡 Medium `M` | Field Resolver<br>Calls: `search` | B-01 | **Intent —** Resolve a watchlist entry's attachments and parent product.<br>**Done when:**<br>• attachments via elastic<br>• `product` null when not `PID*` |
| 📄 `WATCHLIST-BE-G-04`<br>Tests, parity harness | 🟡 Medium `M` | Tests | B-01, C-01, E-01, G-02 | **Intent —** Prove the watchlist subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity fixtures (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green<br>• schema-diff intentional |
| 🔸 `WATCHLIST-BE-G-05`<br>`WatchlistPartner.partner` entity reference (recommended, PO-gated) | 🟢 Low `XS` | Field Resolver<br>Calls: `vmm` | G-02 | **Intent —** Adds `partner { … }` next to `partnerId`/`partnerName` on watchlist partner rows.<br>**Today —** schema adds partner: VMM_BusinessPartner on WatchlistPartner; resolver<br>**Done when:**<br>• PO approval recorded (OQ-5) before implementation starts<br>• `partner { id name }` resolves via the gateway; `partnerName` parity is preserved<br>• No additional VMM calls from the watchlist subgraph (stub emission only) |

