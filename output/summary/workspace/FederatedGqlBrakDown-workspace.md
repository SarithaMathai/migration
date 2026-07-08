# Federated GraphQL Breakdown — Workspace

| | |
|---|---|
| **Target DGS** | `plm-workspace (separate)` |
| **T-Shirt Size** | **XL** |
| **Total Stories** | 28 |
| **Complexity** | 🔴 3 Very High · 🟠 3 High · 🟡 13 Medium · 🟢 9 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Workspace** domain — the seasonal/working containers that group products, samples, teams, partners, attachments and discussions — off the `spark-internal-graphql` gateway into its **own `plm-workspace` DGS subgraph**.
- Workspace is a **hub**: nearly every product-family domain references a `WorkspaceV2`, and workspace itself reaches into product, search, discussion, sample, combination, attachment, relationship and access-control.

- It is **large and high-risk**: 8 queries, 10 mutations (+2 schema-drift wrappers), ~25 field resolvers on a 1,060-line resolver.
- The cost and risk concentrate in three places: the **`workspaceBusinessPartnerActionsV2`** drop/undrop dispatcher (5 cases, manual compensation, and **un-awaited promise chains** to fix), and the two heavy field resolvers **`attachmentsWithMetaData`** and **`counts`** (the workspace product dashboard).

**ACL note:** ACL authorization is ignored in the DGS implementation; **but** the drop/undrop **resource
bookkeeping** (which resources get dropped/undropped) IS real build work — it is data maintenance, not auth.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 8 | 2 paged elastic; product/search-backed lookups |
| Mutations | 10 (+2 deferred) | incl. the partner-action dispatcher + 3 exports |
| Field-resolver type blocks | ~3 | `WorkspaceV2` (~22), `WorkspaceDepartmentV2`, paged |
| External dependencies | 14 keys (all cross-subgraph) | search/product/attachment 🔴 |
| Federation role | provides `WorkspaceV2` entity | every product-family domain references it |
| **Total stories** | **32** | green-field; separate subgraph |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `SPARK-WS-D04` — `addResourcesToWorkspaceV2` | `SPARK-SPIKE-06` | Cross-Domain Association / Hydration |
| 🔴🔬 `SPARK-WS-E01` — `workspaceBusinessPartnerActionsV2` (5-case drop/undrop dispatcher) | `SPARK-SPIKE-03` | Partner Drop/Undrop + Ownership |
| 🔴🔬 `SPARK-WS-G04` — `products` + `productsCount` + `combinations` + `sampleReport` (cross-subgraph) | `SPARK-SPIKE-06` | Cross-Domain Association / Hydration |
| 🔴🔬 `SPARK-WS-G05` — partners (`businessPartners`/`droppedPartners`/`notRemovablePartnerIds`/`unDroppablePartners`) | `SPARK-SPIKE-04` | Not-Removable / Undroppable Partners |

> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 6 | 8–14d |
| C | Search & Listing | 2 | 5–9d |
| D | Mutations (simple) | 9 | 16–27d |
| E | Complex (partner-action dispatcher) | 1 | 8–13d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 8 | 34–56d |
| **Total** | | **32** | **75–126d** (buffered) |

> One engineer ≈ **15–26 sprints**. Heavily parallelizable after B01; 2–3 engineers recommended.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~17–29 sprints | sequential — not recommended |
| 2 engineers | ~10–17 sprints | B/C/D parallel after B01 |
| 3 engineers | ~7–11 sprints | critical path A → E01 → G01/G02 → G08 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | B01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 3 | C01/C02 + D06–D09 | paged search + teams + exports |
| 4 | D01–D05 | create/update/change + resource add/remove |
| 5–6 | E01 | partner-action dispatcher (focused) |
| 7–8 | G01–G04 | the heavy field resolvers (X-Large) |
| 9 | G05–G07 | partners/hierarchy/users/computed |
| 10 | F01/F02 + G08 | entity fetcher + drift decision + tests |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (6 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-WS-B01`<br>`getWorkspaceV2(id, metric)` | 🟢 Low `XS` | Query | — | **Intent —** Fetch one workspace by id.<br>**Today —** getWorkspaceByIdV2 GET …<br>**Done when:**<br>• returns workspace; miss→null |
| 🔷 `SPARK-WS-B02`<br>`getWorkspacesByIdsV2(ids)` | 🟢 Low `XS` | Query | B01 | **Intent —** Fetch several workspaces by ids.<br>**Today —** token → getWorkspacesByIdsV2(jwt)<br>**Done when:**<br>• returns list for ids |
| 🔷 `SPARK-WS-B03`<br>`getWorkspaceTypeCount` | 🟢 Low `XS` | Query<br>Calls: `search` | B01 | **Intent —** Count workspaces by type.<br>**Today —** (search) getWorkspaceTypeCount({})<br>**Done when:**<br>• returns products/combinations/research counts |
| 🔷 `SPARK-WS-B04`<br>`findWorkspaceProductAndSampleIds(workspaceId, q, filter)` | 🟡 Medium `M` | Query<br>Calls: `product` | B01 | **Intent —** List the product and sample ids in a workspace.<br>**Today —** (product) getWorkspaceProducts({workspaceId, filter, q, page:0, size:10000}) → map {id:humanId, sampleIds:[sample.humanId]}<br>**Done when:**<br>• maps products + their sample human ids |
| 🔷 `SPARK-WS-B05`<br>`findWorkspaceClaims(workspaceId, q, filter)` | 🟢 Low `XS` | Query<br>Calls: `search` | B01 | **Intent —** List a workspace's claims (via elastic).<br>**Today —** (search) getClaimsElastic({ q:"workspaceContext:{workspaceId}", page:0, size:10000 }) → .content<br>**Done when:**<br>• elastic query exact |
| 🔷 `SPARK-WS-B06`<br>`getWorkspacePackagingAttachments(workspaceId, bpId)` | 🟡 Medium `M` | Query<br>Calls: `search` | B01 | **Intent —** Find a workspace's packaging attachments by tag.<br>**Today —** env WORKSPACE_PACKAGING_TAG_ID (throws if unset) → (search) searchAttachments({ q:"tags:{tag}[ AND security.bps:{bpId}]", relatedIds:[workspaceId], size:500…<br>**Done when:**<br>• throws if tag config missing<br>• bp filter appended when present |

> **`SPARK-WS-B01`** — **Note — DGS Module Init (this PR only):** Creates `workspace.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql.


### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-WS-C01`<br>`getWorkspacesPagedV2(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | B01 | **Intent —** List workspaces with paging / filters (V2).<br>**Today —** (search) getWorkspacesPagedV2 — array params CSV-joined (except page/size); omitBy drops empties<br>**Done when:**<br>• array→CSV; empties omitted |
| 🔷 `SPARK-WS-C02`<br>`getWorkspacesPagedV3(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | B01 | **Intent —** List workspaces with paging / filters (V3).<br>**Today —** (search) getWorkspacesPagedV3 — CSV-join except q/designPartnerIds; omitBy<br>**Done when:**<br>• CSV-join rules preserved (q/designPartnerIds passthrough) |


### ✏️ Phase D — Mutations (9 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `SPARK-WS-D01`<br>`createWorkspaceV2` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Create a workspace (rejects duplicates).<br>**Today —** default workspaceType=103; POST … (validateUnique). Throw GraphQLError('Workspace already exists') if the response message starts with the dup text<br>**Done when:**<br>• creates; default type<br>• 2. dup → GraphQLError |
| 🔶 `SPARK-WS-D02`<br>`updateWorkspaceV2` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Edit a workspace (rejects duplicates).<br>**Today —** token for workspace.id; default type 103; PUT … → same dup-check throw<br>**Done when:**<br>• updates; dup→throw |
| 🔶 `SPARK-WS-D03`<br>`changeWorkspace` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Move resources from one workspace to another.<br>**Today —** token for Attr-{newWs}-resources → PUT … with {newWorkspaceId, oldWorkspaceId, productHumanId, teams, removeWorkspaceOnly}. Throw on validationErrors/message<br>**Done when:**<br>• moves product between workspaces<br>• error→throw |
| 🔴🔬 🔶 `SPARK-WS-D04`<br>`addResourcesToWorkspaceV2`<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-06` (Cross-Domain Association / Hydration) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `product` | SPARK-SPIKE-06, B01 | **Intent —** Add products / samples to a workspace.<br>**Today —** token; if single product → (product) read Product.workspaces + updateViewToggle (init workspace attrs; firstWorkspace adds designCycle/setDates); POST …<br>**Done when:**<br>• adds resources<br>• single-product init side-effect preserved |
| 🔶 `SPARK-WS-D05`<br>`removeWorkspaceResourcesV2` | 🟡 Medium `M` | Mutation<br>Calls: `product` | B01 | **Intent —** Remove resources from a workspace.<br>**Today —** token; if single product → (product) deletePartnerWorkspaceStatuses cleanup; DELETE …<br>**Done when:**<br>• removes resources<br>• single-product status cleanup |
| 🔶 `SPARK-WS-D06`<br>`addTeamsToWorkspaceV3` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Add teams to a workspace.<br>**Today —** token → POST …<br>**Done when:**<br>• adds teams |
| 🔶 `SPARK-WS-D07`<br>`exportWorkspace` | 🟢 Low `XS` | Mutation<br>Calls: `search` | B01 | **Intent —** Kick off a workspace export.<br>**Today —** (search) requestBulkAttachmentExport({parentResourceId, exportType, includedAttachmentIds, includeOnlyPrimaryThumbnails}, {q, filter})<br>**Done when:**<br>• returns receipt |
| 🔶 `SPARK-WS-D08`<br>`exportWorkspaceExcel` | 🟢 Low `XS` | Mutation<br>Calls: `exportHub` | B01 | **Intent —** Export a workspace to Excel.<br>**Today —** (exportHub) exportWorkspaceExcel(workspaceExportOptions)<br>**Done when:**<br>• returns receipt |
| 🔶 `SPARK-WS-D09`<br>`exportPackagingFiles` | 🟢 Low `XS` | Mutation<br>Calls: `search` | B01 | **Intent —** Export a workspace's packaging files.<br>**Today —** (search) requestPackagingExport({workspaceId, workspaceDescription, exportContext, exportType}, {q, filter})<br>**Done when:**<br>• returns receipt |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `SPARK-WS-E01`<br>`workspaceBusinessPartnerActionsV2` (5-case drop/undrop dispatcher)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-03` (Partner Drop/Undrop + Ownership) — see global Spike Detail_ | 🔴 Very High `XL` | Mutation<br>Calls: `relationship`, `discussion`, `sampleV2`, `favorite` | SPARK-SPIKE-03, B01 | **Intent —** Drop / undrop a partner (or remove team/partner) across a workspace — a 5-case orchestrated write.<br>**Today —** ~310-line switch — REMOVE_TEAM, REMOVE_PARTNER, DROP_PARTNER, - UNDO_DROP_PARTNER, DROP_UNDROP_PARTNER. - Builds a relationship tree (relationship), ACL-filters…<br>**Done when:**<br>• chains awaited; compensation on ACL failure<br>• design-partner skips samples | ☐ REMOVE_TEAM<br>☐ REMOVE_PARTNER<br>☐ DROP<br>☐ UNDO_DROP<br>☐ DROP_UNDROP<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-WS-F01`<br>`WorkspaceV2` federated entity fetcher | 🟡 Medium `M` | Field Resolver | B01 | **Intent —** Let other subgraphs resolve a Workspace by key.<br>**Today —** @DgsEntityFetcher(name="WorkspaceV2") resolving by id, so the product-family subgraphs<br>**Done when:**<br>• entity resolves by key from `_entities`<br>• a cross-subgraph `Product { workspaces { id description } }` smoke test passes |
| 📄 `SPARK-WS-F02`<br>Deferred drop/undrop wrapper decision (drift mutations) | 🟢 Low `XS` | Schema | E01 | **Intent —** Decide the fate of the drop/undrop drift wrappers.<br>**Today —** dropWorkspaceBusinessPartnerV2/unDropWorkspaceBusinessPartnerV2 are schema-drift wrappers; traffic routes through workspaceBusinessPartnerActionsV2<br>**Done when:**<br>• traffic survey complete<br>• decision implemented |


### 🧪 Phase G — Field Resolvers & Tests (8 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `SPARK-WS-G01`<br>`WorkspaceV2.attachmentsWithMetaData` | 🔴 Very High `XL` | Field Resolver<br>Calls: `relationship`, `attachment`, `discussion` | B01 | **Intent —** Resolve a workspace's attachments, enriched with discussion metadata.<br>**Today —** (relationship) tree (attachments_v3/discussions/discussionThreads) → - (attachment) getAttachmentsV3 → (discussion) batch discussions/threads → merge → order by…<br>**Done when:**<br>• parity for mixed attachment/discussion/thread<br>• ordering + draft filter preserved | ☐ merge<br>☐ ordering<br>☐ draft filter<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `SPARK-WS-G02`<br>`WorkspaceV2.counts` (product dashboard rollup) | 🔴 Very High `XL` | Field Resolver<br>Calls: `search`, `product`, `discussion` | B01 | **Intent —** Roll up a workspace's product / sample / discussion counts for the dashboard.<br>**Today —** (search) getFilteredProductsWithSummary → (product) getPage → - (discussion) product discussion counts + (search) sample counts + sample-discussion roll-up into…<br>**Done when:**<br>• parity for the full rollup incl. sample-discussion increment<br>• empty → zeros | ☐ rollup<br>☐ sample-discussion<br>☐ empty<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `SPARK-WS-G03`<br>`WorkspaceV2.attachmentsV3` | 🟠 High `L` | Field Resolver<br>Calls: `relationship`, `attachment` | B01 | **Intent —** Resolve a workspace's attachments (with / without per-partner counts).<br>**Today —** with args → getProductOrWorkSpaceAttachments (per-BP counts via initialCountsByBp); without args → relationship tree → resolveRelationIds → filter<br>**Done when:**<br>• both arg/no-arg paths<br>• per-BP counts | ☐ with args<br>☐ no args<br>☐ counts |
| 🔴🔬 🔸 `SPARK-WS-G04`<br>`products` + `productsCount` + `combinations` + `sampleReport` (cross-subgraph)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-06` (Cross-Domain Association / Hydration) — see global Spike Detail_ | 🟠 High `L` | Field Resolver<br>Calls: `product`, `search`, `combination`, `sampleV2` | SPARK-SPIKE-06, B01 | **Intent —** Resolve a workspace's cross-subgraph product / combination fields.<br>**Today —** products → (product) getProducts(resourceType:'workspaces', resourceId, include*: true); productsCount → (product) getPage totalElements; combinations → (search)…<br>**Done when:**<br>• each resolves; include flags forwarded<br>• sampleReport round counts correct | ☐ products<br>☐ count<br>☐ combinations<br>☐ sampleReport |
| 🔴🔬 🔸 `SPARK-WS-G05`<br>partners (`businessPartners`/`droppedPartners`/`notRemovablePartnerIds`/`unDroppablePartners`)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-04` (Not-Removable / Undroppable Partners) — see global Spike Detail_ | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm` | SPARK-SPIKE-04, B01 | **Intent —** Resolve a workspace's business / dropped / not-removable partner lists.<br>**Done when:**<br>• each resolves; unDroppable gated on `isDesignPartner` | — |
| 🔸 `SPARK-WS-G06`<br>hierarchy/tags (`divisions`/`brands`/`clazzes`/`designCycles`/`tags` + `WorkspaceDepartmentV2`) | 🟡 Medium `M` | Field Resolver<br>Calls: `ig`, `brand`, `tag` | B01 | **Intent —** Resolve a workspace's division / brand / class / design-cycle / tag fields.<br>**Done when:**<br>• each resolves; empty → [] | — |
| 🔸 `SPARK-WS-G07`<br>users/computed (`createdBy`/`updatedBy`/`status`/`id` + `discussionsV2`/`teams` + paged) | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `search` | B01 | **Intent —** Resolve a workspace's people, status and discussion / team fields.<br>**Done when:**<br>• computed mappings correct<br>• users/discussions/teams resolve | — |
| 📄 `SPARK-WS-G08`<br>Tests, parity harness, load test | 🟠 High `L` | Tests | B01, E01, G01, G02 | **Intent —** Prove the workspace subgraph matches the old gateway (incl. load test).<br>**Today —** ≥80% unit coverage; parity harness (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green<br>• load p95 parity<br>• schema-diff intentional | ☐ Parity: DGS response matches spark-internal-graphql baseline<br>☐ Load: p95 latency is within spark-internal-graphql baseline<br>☐ contract |

