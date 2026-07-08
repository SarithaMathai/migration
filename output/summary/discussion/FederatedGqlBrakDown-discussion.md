# Federated GraphQL Breakdown — Discussion

| | |
|---|---|
| **Target DGS** | `plm-discussion (separate)` |
| **T-Shirt Size** | **XL** |
| **Total Stories** | 32 |
| **Complexity** | 🔴 0 Very High · 🟠 4 High · 🟡 15 Medium · 🟢 13 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Discussion** domain — threaded discussions/replies on products, samples and workspaces, their participants, sample discussions, flags (critical/editable/tag), read-receipts and bulk operations — off the `spark-internal-graphql` gateway into its **own `plm-discussion` DGS subgraph**.
- Discussion is referenced by **product** and **workspace** (it provides `discussionsCount`/`discussionsV2` and the TechPack `ResourcesCount.discussions` count, `SPARK-PROD-F02`).

- It is **large**: it consolidates **three API versions** (v1/v2/V3) into one subgraph — **11 queries + 26 mutations** (plus 3 schema-drift ops), ~12 field-resolver type blocks, and the **`Resource` union** (`Product` | `SampleV2` | `WorkspaceV2`, resolved by id prefix).
- The defining wrinkles are the **`core*` twins** (system-context versions of public ops — paired per story) and the **participant-management** surface (V2 + V3 + core delete over users/teams/partners/design-partners).

**ACL note:** read/write tokens are context-only. The drop/undrop partner bookkeeping is **driven by the
workspace dispatcher** (`workspaceBusinessPartnerActionsV2`), so it is a deferred drift decision, not build
work here.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 11 | by-id/by-resource/by-thread, version history (V3), elastic (🔴 search), sample |
| Mutations | 26 (+3 drift) | add/update/delete, replies, sample, flags, files clone, read-receipts, participants V2/V3 + core twins |
| Field-resolver type blocks | ~12 | `Discussion`/`FullDiscussion`/`DiscussionReply`/participants/team + the `Resource` union + versioned |
| Polymorphism | 1 union | `Resource` → `@DgsTypeResolver` (+1 complexity tier) |
| External dependencies | 6 keys | search 🔴; attachment/user-profile/user-group 🟡; vmm/tag 🔵 |
| Federation role | provides `Discussion` entity + `ResourcesCount.discussions` | product / workspace |
| **Total stories** | **37** | green-field; separate subgraph |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `SPARK-DISC-E01` — Participants V2 (`updateParticipantsV2` + `deleteParticipantV2`) | `SPARK-SPIKE-01` | Non-Atomic Write Saga |
| 🔴🔬 `SPARK-DISC-E02` — Participants V3 (`updateParticipantsV3` + `coreUpdate` + `coreDelete` + `deleteParticipantV3`) | `SPARK-SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 7 | 9–15d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations | 13 | 22–37d |
| E | Participant management | 2 | 6–10d |
| F | Federation & decisions | 3 | 4–7d |
| G | Field Resolvers & Tests | 5 | 13–22d |
| **Total** | | **37** | **61–102d** (buffered) |

> One engineer ≈ **13–21 sprints**. Parallelizable after B01.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories; the `Resource` union `@DgsTypeResolver` remains a dedicated story.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~14–24 sprints | sequential |
| 2 engineers | ~8–14 sprints | reads + mutations + participants parallel after B01 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | B01 (DGS module init + service wiring + first resolver) | schema (~20 types + `Resource` resolver + ~12 inputs), service port (v1/v2/V3 consolidate) |
| 3 | B01–B07 + C01–C02 | reads + elastic + sample |
| 4 | D01–D08 | add/update/delete/reply/sample/flags |
| 5 | D09–D13 + E01 | clone/read-receipts, V3 add/bulk/update, participants V2 |
| 6 | E02 + F01–F03 | participants V3 + entity fetcher + TechPack count + drift |
| 7 | G01–G05 | field-resolver surface (incl. `Resource` union) + tests |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (7 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-DISC-B01`<br>`getDiscussionV2` (+ `coreGetDiscussionV2`) | 🟢 Low `XS` | Query | — | **Intent —** Fetch a single discussion (comment thread) by id.<br>**Today —** GET discussions/v2?ids={id} → FullDiscussion; core* = system context<br>**Done when:**<br>• returns discussion; core uses system context |
| 🔷 `SPARK-DISC-B02`<br>`getDiscussionByIdsV2` | 🟢 Low `XS` | Query | B01 | **Intent —** Fetch several discussions by ids.<br>**Today —** GET …<br>**Done when:**<br>• returns by ids |
| 🔷 `SPARK-DISC-B03`<br>`getDiscussionsCount` | 🟢 Low `XS` | Query | B01 | **Intent —** Count discussions per resource.<br>**Today —** count by resourceId/resourceType → [ResourceCount]<br>**Done when:**<br>• returns per-resource counts |
| 🔷 `SPARK-DISC-B04`<br>`getDiscussionOnResource` | 🟢 Low `XS` | Query | B01 | **Intent —** List the discussions on a given resource.<br>**Today —** discussions for a resource<br>**Done when:**<br>• returns discussions |
| 🔷 `SPARK-DISC-B05`<br>`getDiscussionsByThread` | 🟢 Low `XS` | Query | B01 | **Intent —** List the discussions in a thread.<br>**Today —** discussions in a thread<br>**Done when:**<br>• returns thread discussions |
| 🔷 `SPARK-DISC-B06`<br>`getUnsentDiscussions` | 🟢 Low `XS` | Query | B01 | **Intent —** List discussions queued but not yet sent (admin view).<br>**Today —** GET …<br>**Done when:**<br>• returns unsent |
| 🔷 `SPARK-DISC-B07`<br>`getVersionedDiscussions` (+ threads) | 🟡 Medium `M` | Query | B01 | **Intent —** Return a discussion's version history.<br>**Today —** (own V3) version history<br>**Done when:**<br>• both return version history |

> **`SPARK-DISC-B01`** — **Note — DGS Module Init (this PR only):** Creates `discussion.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql.


### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-DISC-C01`<br>`getDiscussionsV2` (elastic) | 🟡 Medium `M` | Query<br>Calls: `search` | B01 | **Intent —** Search discussions for a resource via elastic (partner-filtered).<br>**Today —** (search) elastic discussions by resourceId/resourceType (partner-filtered) → DiscussionElastic<br>**Done when:**<br>• elastic query + partner filter |
| 🔷 `SPARK-DISC-C02`<br>`getSampleDiscussion` | 🟡 Medium `M` | Query | B01 | **Intent —** List discussions scoped to a sample.<br>**Today —** sample-scoped discussions<br>**Done when:**<br>• returns sample discussions |


### ✏️ Phase D — Mutations (13 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔶 `SPARK-DISC-D01`<br>`addDiscussionV2` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B01 | **Intent —** Post a new discussion, optionally with attachments.<br>**Today —** create + (attachment) bulk attachment input<br>**Done when:**<br>• creates; attachments associated | — |
| 🔶 `SPARK-DISC-D02`<br>`addDiscussionReplyV2` + `updateDiscussionReplyV2` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B01 | **Intent —** Add or edit a reply on a discussion.<br>**Today —** add/update reply + (attachment) input (isAttachmentsV3 flag)<br>**Done when:**<br>• add + update reply; v3-attachment flag honored | — |
| 🔶 `SPARK-DISC-D03`<br>`updateDiscussionV2` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Edit a discussion's body.<br>**Today —** PUT discussion body<br>**Done when:**<br>• updates | — |
| 🔶 `SPARK-DISC-D04`<br>`deleteDiscussionV2` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Delete a discussion.<br>**Today —** delete by id → ID<br>**Done when:**<br>• deletes | — |
| 🔶 `SPARK-DISC-D05`<br>`deleteDiscussionReplyV2` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Delete a reply.<br>**Today —** delete reply → ID<br>**Done when:**<br>• deletes reply | — |
| 🔶 `SPARK-DISC-D06`<br>`deleteDiscussionPartnersV2` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Remove partners from a discussion.<br>**Today —** delete partners from a discussion → ID<br>**Done when:**<br>• removes partners | — |
| 🔶 `SPARK-DISC-D07`<br>Sample discussions (V2/V3 + bulk) | 🟡 Medium `M` | Mutation | B01 | **Intent —** Create sample-scoped discussions.<br>**Today —** sample-scoped create<br>**Done when:**<br>• each creates sample discussion(s) | — |
| 🔶 `SPARK-DISC-D08`<br>Flags (critical / editable / tag) | 🟢 Low `XS` | Mutation<br>Calls: `tag` | B01 | **Intent —** Set discussion flags (critical / editable / tag).<br>**Today —** @DgsMutation → DiscussionReply<br>**Done when:**<br>• each flag updates | — |
| 🔶 `SPARK-DISC-D09`<br>`cloneFilesForBulkDiscussion` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B01 | **Intent —** Copy attachments when bulk-creating discussions.<br>**Today —** token → Promise.all(attachmentIds.map(id → (attachment) cloneAttachmentV3({cloneReferences}, id)))<br>**Done when:**<br>• clones each id | — |
| 🔶 `SPARK-DISC-D10`<br>`discussionReadByUsers` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Mark discussions as read for a set of users.<br>**Today —** mark read across discussionIds/discussionThreadIds for readByUserList<br>**Done when:**<br>• records read receipts | — |
| 🔶 `SPARK-DISC-D11`<br>`addDiscussionV3` (+ `coreAddDiscussionV3`) | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B01 | **Intent —** Post a new discussion (V3 model) with attachments.<br>**Today —** (own V3) create + attachments; core* = system context<br>**Done when:**<br>• creates; core uses system context | — |
| 🔶 `SPARK-DISC-D12`<br>`addBulkDiscussionV3` | 🟠 High `L` | Mutation<br>Calls: `attachment` | B01 | **Intent —** Post discussions across many resources at once (V3).<br>**Today —** (own V3) bulk create across resources + attachments → BulkDiscussionOutputV3. - Note: coreAddBulkDiscussionV3 is schema-drift (no resolver — see F03)<br>**Done when:**<br>• bulk creates | ☐ bulk<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔶 `SPARK-DISC-D13`<br>`updateDiscussionV3` (+ `coreUpdateDiscussionV3`) | 🟡 Medium `M` | Mutation | B01 | **Intent —** Edit a discussion (V3 model).<br>**Today —** (own V3) update; core* = system context<br>**Done when:**<br>• updates; core context | — |


### ⚙️ Phase E — Complex Operations (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `SPARK-DISC-E01`<br>Participants V2 (`updateParticipantsV2` + `deleteParticipantV2`)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `userGroup` | SPARK-SPIKE-01, B01 | **Intent —** Add or remove participants on a discussion (V2).<br>**Today —** add participants (AddParticipantInput) / remove a participant (team/user/partner)<br>**Done when:**<br>• add + remove participants | — |
| 🔴🔬 🔶 `SPARK-DISC-E02`<br>Participants V3 (`updateParticipantsV3` + `coreUpdate` + `coreDelete` + `deleteParticipantV3`)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `userGroup` | SPARK-SPIKE-01, B01 | **Intent —** Add / update / remove participants on a discussion with the richer V3 model.<br>**Today —** richer participant model — updateParticipantsV3 / coreUpdateParticipantsV3 - (participants + relatedResources + resourceType), coreDeleteParticipantsV3…<br>**Done when:**<br>• each path updates/removes the right participants | ☐ update<br>☐ coreUpdate<br>☐ coreDelete<br>☐ delete |


### 🔗 Phase F — Federation & Stitching (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-DISC-F01`<br>`Discussion` federated entity fetcher | 🟡 Medium `M` | Field Resolver | B01 | **Intent —** Let other subgraphs resolve a Discussion by key.<br>**Today —** @DgsEntityFetcher(name="Discussion") by discussionId; provides discussionsCount/discussionsV2<br>**Done when:**<br>• entity resolves by key<br>• cross-subgraph smoke |
| 🔸 `SPARK-DISC-F02`<br>`ResourcesCount.discussions` (TechPack — SPARK-PROD-F02) | 🟢 Low `XS` | Field Resolver | B01 | **Intent —** Contribute the discussions count to the TechPack rollup.<br>**Today —** extend type ResourcesCount @key(fields:"productId partnerId") { discussions: [ID] } with a @DgsEntityFetcher; fills the TechPack discussions count (the discussion side…<br>**Done when:**<br>• field resolves; parity vs facade |
| 📄 `SPARK-DISC-F03`<br>Deferred drift decision (drop/undrop + coreAddBulkDiscussionV3) | 🟢 Low `XS` | Schema | B01 | **Intent —** Decide the fate of drop/undrop + a drift bulk query that have no resolvers.<br>**Today —** dropPartnerFromDiscussionIds/unDropPartnerFromDiscussionIds (no resolver — run inside workspaceBusinessPartnerActionsV2); coreAddBulkDiscussionV3 (no resolver)<br>**Done when:**<br>• decision + traffic survey |


### 🧪 Phase G — Field Resolvers & Tests (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `SPARK-DISC-G01`<br>`Discussion` + `FullDiscussion` + `DiscussionContent` field resolvers | 🟠 High `L` | Field Resolver<br>Calls: `userAttributes`, `tag` | B01 | **Intent —** Resolve the core discussion / content fields.<br>**Done when:**<br>• each field resolves | ☐ bodies<br>☐ users<br>☐ resource<br>☐ replies |
| 🔸 `SPARK-DISC-G02`<br>`DiscussionReply` + `NotificationStatus` field resolvers | 🟡 Medium `M` | Field Resolver<br>Calls: `attachment`, `userAttributes` | B01 | **Intent —** Resolve reply and notification-status fields.<br>**Done when:**<br>• each resolves | — |
| 🔸 `SPARK-DISC-G03`<br>Participants + Team + Participant sub-types | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `vmm` | B01 | **Intent —** Resolve participant / team sub-type fields.<br>**Done when:**<br>• teams/users/bp resolve | — |
| 🔸 `SPARK-DISC-G04`<br>`Resource` union members + Versioned + `DiscussionReadByUsers` | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes` | B01 | **Intent —** Resolve the resource-union, versioned and read-by fields.<br>**Done when:**<br>• each resolves | — |
| 📄 `SPARK-DISC-G05`<br>Tests, parity harness | 🟠 High `L` | Tests | B01, D12, E02, G01 | **Intent —** Prove the discussion subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity harness (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green<br>• schema-diff intentional | ☐ Parity: DGS response matches spark-internal-graphql baseline<br>☐ contract |

