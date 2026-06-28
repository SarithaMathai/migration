# discussion — Jira stories (paste one block per issue)

> **Epic:** Discussion → plm-discussion DGS migration  ·  **Labels:** `dgs-migration`, `discussion`, `<type>`
> Create the Epic first, then paste each block below as a new Story's description.
> Story points are AI-derived from complexity (confirm in refinement). See [README.md](./README.md).

## SPARK-DISC-A01 · Schema skeleton + DateTime scalar
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** —
**Labels:** `dgs-migration`, `discussion`, `schema`

**Current Behaviour:** green-field; schema translated from `SPARK_Discussion.txt` + `SPARK_DiscussionV3.txt`.
**Target:** federation v2.3 header, `scalar DateTime → Instant`, `scalar JsonNode`, empty `extend type Query`/`Mutation`. **Acceptance:** 1. `generateJava` passes. **Tests:** ☐ compiles ☐ serde.

---

## SPARK-DISC-A02 · Owned types + inputs (V2+V3 surface)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-DISC-A01
**Labels:** `dgs-migration`, `discussion`, `schema`

**Target:** `Discussion` (`@key(fields:"discussionId")`) + ~18 value types + ~12 inputs per [03-schema.graphql](./03-schema.graphql); reconcile V2 + V3 type shapes. **Acceptance:** 1. all types/inputs present; nullability matches SDLs. 2. validates. **Tests:** ☐ validates ☐ entity stub.

---

## SPARK-DISC-A03 · External stubs (platform + other DGS + Resource members)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A01
**Labels:** `dgs-migration`, `discussion`, `schema`

**Target:** `@extends @external` stubs for `Attachment`/`SearchAttachment`, `DiscussionElastic`,
`UserProfileAttributes`, `UserGroup_Participants`, `Tag`, `VMM_BusinessPartner`, and the `Resource` members
`Product`/`SampleV2`/`WorkspaceV2`. **Acceptance:** 1. compiles; gateway composes. **Tests:** ☐ compiles ☐ stub resolves.

---

## SPARK-DISC-A04 · Resource union @DgsTypeResolver (Product|SampleV2|WorkspaceV2)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A02, SPARK-DISC-A03
**Labels:** `dgs-migration`, `discussion`, `field-resolver`

**Current Behaviour (`__resolveType`):** map the discussion's parent resource id prefix → `Product` | `SampleV2` | `WorkspaceV2`. **Target:** `@DgsTypeResolver(name="Resource")`. **Acceptance:** 1. each member maps by prefix; unknown → null. **Tests:** ☐ product ☐ sample ☐ workspace.

---

## SPARK-DISC-A05 · DiscussionService port (v1/v2 + V3 consolidated)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-DISC-A01
**Labels:** `dgs-migration`, `discussion`, `service`

**Current Behaviour (Phase 2 §Service):** `discussions/v1` (+ `discussion_message`, `/bulk`), `discussions/v2`
(`/discussion`), admin `/unsent`, + V3 service (~30 methods). **Target:** consolidated Kotlin service; map the `core*` system-context twins. **Acceptance:** 1. v1/v2/V3 endpoints present. 2. core twins distinguished. **Tests:** ☐ endpoint build ☐ core context.

---

### Phase B — Core Reads

---

## SPARK-DISC-B01 · getDiscussionV2 (+ coreGetDiscussionV2)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A02, SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (own) `GET discussions/v2?ids={id}` → `FullDiscussion`; `core*` = system context. **Target:** `@DgsQuery → FullDiscussion` (two fields, shared impl). **Acceptance:** 1. returns discussion; core uses system context. **Tests:** ☐ happy ☐ core.

---

## SPARK-DISC-B02 · getDiscussionByIdsV2
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (own) `GET /v2?ids={csv}`. **Target:** `@DgsQuery → [FullDiscussion]`. **Acceptance:** 1. returns by ids. **Tests:** ☐ happy ☐ empty.

---

## SPARK-DISC-B03 · getDiscussionsCount
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (own) count by `resourceId`/`resourceType` → `[ResourceCount]`. **Target:** `@DgsQuery`. **Acceptance:** 1. returns per-resource counts. **Tests:** ☐ counts.

---

## SPARK-DISC-B04 · getDiscussionOnResource
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (own) discussions for a resource. **Target:** `@DgsQuery → [Discussion]`. **Acceptance:** 1. returns discussions. **Tests:** ☐ happy.

---

## SPARK-DISC-B05 · getDiscussionsByThread
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (own) discussions in a thread. **Target:** `@DgsQuery → [Discussion]`. **Acceptance:** 1. returns thread discussions. **Tests:** ☐ happy.

---

## SPARK-DISC-B06 · getUnsentDiscussions
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (own) `GET /api/admin/unsent`. **Target:** `@DgsQuery → UnsentDiscussions`. **Acceptance:** 1. returns unsent. **Tests:** ☐ happy.

---

## SPARK-DISC-B07 · getVersionedDiscussions (+ threads)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Covers:** `getVersionedDiscussions(id)`, `getVersionedDiscussionThreads(id)` (V3). **Current Behaviour:** (own V3) version history. **Target:** `@DgsQuery`. **Acceptance:** 1. both return version history. **Tests:** ☐ discussions ☐ threads.

---

### Phase C — Search & Listing

---

## SPARK-DISC-C01 · getDiscussionsV2 (elastic)
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (🔴 search) elastic discussions by `resourceId`/`resourceType` (partner-filtered) → `DiscussionElastic`. **Target:** `@DgsQuery`. **Acceptance:** 1. elastic query + partner filter. **Tests:** ☐ query ☐ partner filter.

---

## SPARK-DISC-C02 · getSampleDiscussion
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `query`

**Current Behaviour:** (own) sample-scoped discussions. **Target:** `@DgsQuery → [Discussion]`. **Acceptance:** 1. returns sample discussions. **Tests:** ☐ happy.

---

### Phase D — Mutations

---

## SPARK-DISC-D01 · addDiscussionV2 (+ attachments)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own) create + (🟡 attachment) bulk attachment input. **Target:** `@DgsMutation → Discussion`. **Acceptance:** 1. creates; attachments associated. **Tests:** ☐ create ☐ +attachments.

---

## SPARK-DISC-D02 · addDiscussionReplyV2 + updateDiscussionReplyV2
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** add/update reply + (🟡 attachment) input (`isAttachmentsV3` flag). **Target:** `@DgsMutation → DiscussionReply`. **Acceptance:** 1. add + update reply; v3-attachment flag honored. **Tests:** ☐ add ☐ update ☐ attachments.

---

## SPARK-DISC-D03 · updateDiscussionV2
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own) `PUT` discussion body. **Target:** `@DgsMutation → Discussion`. **Acceptance:** 1. updates. **Tests:** ☐ update.

---

## SPARK-DISC-D04 · deleteDiscussionV2
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own) delete by id → ID. **Target:** `@DgsMutation → ID`. **Acceptance:** 1. deletes. **Tests:** ☐ delete.

---

## SPARK-DISC-D05 · deleteDiscussionReplyV2
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own) delete reply → ID. **Target:** `@DgsMutation → ID`. **Acceptance:** 1. deletes reply. **Tests:** ☐ delete.

---

## SPARK-DISC-D06 · deleteDiscussionPartnersV2
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own) delete partners from a discussion → ID. **Target:** `@DgsMutation → ID`. **Acceptance:** 1. removes partners. **Tests:** ☐ delete partners.

---

## SPARK-DISC-D07 · Sample discussions (addSampleDiscussionV2/V3 + bulkAddSampleDiscussions)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Covers:** `addSampleDiscussionV2`, `addSampleDiscussionV3`, `bulkAddSampleDiscussions`. **Current Behaviour:** (own) sample-scoped create. **Target:** `@DgsMutation → SampleDiscussion`/`[…]`. **Acceptance:** 1. each creates sample discussion(s). **Tests:** ☐ v2 ☐ v3 ☐ bulk.

---

## SPARK-DISC-D08 · Flags (updateAsCritical/updateDiscussionEditable/updateTagExisting)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Covers:** `updateAsCritical`, `updateDiscussionEditable`, `updateTagExisting` (share the `DiscussionAsCritical` input). **Target:** `@DgsMutation → DiscussionReply`. **Acceptance:** 1. each flag updates. **Tests:** ☐ critical ☐ editable ☐ tag.

---

## SPARK-DISC-D09 · cloneFilesForBulkDiscussion
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (ACL) token → `Promise.all(attachmentIds.map(id → (🟡 attachment) cloneAttachmentV3({cloneReferences}, id)))`. **Target:** structured-concurrency fan-out. **Acceptance:** 1. clones each id. **Tests:** ☐ clone.

---

## SPARK-DISC-D10 · discussionReadByUsers
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own) mark read across `discussionIds`/`discussionThreadIds` for `readByUserList`. **Target:** `@DgsMutation → DiscussionReadByUsers`. **Acceptance:** 1. records read receipts. **Tests:** ☐ read receipts.

---

## SPARK-DISC-D11 · addDiscussionV3 (+ coreAddDiscussionV3)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own V3) create + attachments; `core*` = system context. **Target:** `@DgsMutation → Discussion` (two fields, shared impl). **Acceptance:** 1. creates; core uses system context. **Tests:** ☐ add ☐ core.

---

## SPARK-DISC-D12 · addBulkDiscussionV3
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own V3) bulk create across resources + attachments → `BulkDiscussionOutputV3`.
**Note:** `coreAddBulkDiscussionV3` is **schema-drift** (no resolver — see F03). **Target:** `@DgsMutation`. **Acceptance:** 1. bulk creates. **Tests:** ☐ bulk ☐ parity.

---

## SPARK-DISC-D13 · updateDiscussionV3 (+ coreUpdateDiscussionV3)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** (own V3) update; `core*` = system context. **Target:** `@DgsMutation → Discussion`. **Acceptance:** 1. updates; core context. **Tests:** ☐ update ☐ core.

---

### Phase E — Participant management

---

## SPARK-DISC-E01 · Participants V2 (updateParticipantsV2 + deleteParticipantV2)
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** add participants (`AddParticipantInput`) / remove a participant (team/user/partner). **Target:** `@DgsMutation → Discussion`. **Acceptance:** 1. add + remove participants. **Tests:** ☐ add ☐ remove.

---

## SPARK-DISC-E02 · Participants V3 (updateParticipantsV3 + coreUpdate + coreDelete + deleteParticipantV3)
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `mutation`

**Current Behaviour:** richer participant model — `updateParticipantsV3` / `coreUpdateParticipantsV3`
(participants + relatedResources + resourceType), `coreDeleteParticipantsV3` (removedUser/team/partners/
designPartners), `deleteParticipantV3` (team/user/partner/designPartner). **Target:** `@DgsMutation → Discussion` (one service, four fields). **Acceptance:** 1. each path updates/removes the right participants. **Tests:** ☐ update ☐ coreUpdate ☐ coreDelete ☐ delete.

---

### Phase F — Federation & decisions

---

## SPARK-DISC-F01 · Discussion entity fetcher (federated reference)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `field-resolver`

**Target:** `@DgsEntityFetcher(name="Discussion")` by `discussionId`; provides `discussionsCount`/`discussionsV2`
for product/workspace over the gateway. **Acceptance:** 1. entity resolves by key. 2. cross-subgraph smoke. **Tests:** ☐ entity ☐ smoke.

---

## SPARK-DISC-F02 · ResourcesCount.discussions (TechPack — SPARK-PROD-F02)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `field-resolver`

**Target:** `extend type ResourcesCount @key(fields:"productId partnerId") { discussions: [ID] }` with a `@DgsEntityFetcher`; fills the TechPack `discussions` count (the discussion side of `SPARK-PROD-F02`). **BLOCKED-BY:** product TechPack facade. **Acceptance:** 1. field resolves; parity vs facade. **Tests:** ☐ field ☐ parity.

---

## SPARK-DISC-F03 · Deferred drift decision (drop/undrop partner + coreAddBulkDiscussionV3)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `schema`

**Current Behaviour:** `dropPartnerFromDiscussionIds`/`unDropPartnerFromDiscussionIds` (no resolver — run inside `workspaceBusinessPartnerActionsV2`); `coreAddBulkDiscussionV3` (no resolver). **Target:** delete or keep `@deprecated`; coordinate drop/undrop ownership with workspace. **Acceptance:** 1. decision + traffic survey. **Tests:** ☐ schema diff intentional.

---

### Phase G — Field Resolvers & Tests

---

## SPARK-DISC-G01 · Discussion + FullDiscussion + Content field resolvers
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-DISC-A02, SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `field-resolver`

**Current Behaviour:** discussion/full/content bodies, `createdBy`/`updatedBy` (🟡 user), `tags` (🔵 tag),
`resource` (union), `replies`/`participants`/`attachments` links. **Acceptance:** 1. each field resolves. **Tests:** ☐ bodies ☐ users ☐ resource ☐ replies.

---

## SPARK-DISC-G02 · DiscussionReply + NotificationStatus field resolvers
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `field-resolver`

**Current Behaviour:** reply body/author (🟡 user), `attachments` (🟡 attachment), `notificationStatus`. **Acceptance:** 1. each resolves. **Tests:** ☐ reply ☐ attachments ☐ notification.

---

## SPARK-DISC-G03 · Participants + Team + Participant sub-types
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `field-resolver`

**Current Behaviour:** `Discussion_Participants.teams`/`users`; `Discussion_Team.businessPartner` (🔵 vmm);
`Discussion_Participant.userDetails` (🟡 user). **Acceptance:** 1. teams/users/bp resolve. **Tests:** ☐ teams ☐ users ☐ bp.

---

## SPARK-DISC-G04 · Resource union members + Versioned + DiscussionReadByUsers field resolvers
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-DISC-A04, SPARK-DISC-A05
**Labels:** `dgs-migration`, `discussion`, `field-resolver`

**Current Behaviour:** `Resource` union resolution (via A04); `VersionedDiscussion`/`Thread.updatedBy` (🟡 user)/`updatedAt` (parse); `DiscussionReadByUsers.discussions`/`discussionThreads` (computed). **Acceptance:** 1. each resolves. **Tests:** ☐ resource ☐ versioned ☐ readBy.

---

## SPARK-DISC-G05 · Tests, parity harness
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-DISC-B01, SPARK-DISC-D12, SPARK-DISC-E02, SPARK-DISC-G01
**Labels:** `dgs-migration`, `discussion`, `tests`

**Target:** ≥80% unit coverage; parity harness (incl. V2/V3 + core twins, participants, bulk, the `Resource`
union, read receipts); contract test (schema diff intentional-only). **Acceptance:** 1. unit ≥80%. 2. parity green. 3. schema-diff intentional. **Tests:** ☐ parity ☐ contract.

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| Three API versions (v1/v2/V3) + `core*` twins | Medium | High | Consolidate in the service port; pair twins | Tech Lead |
| Participant-management correctness (E01/E02) | Medium | Medium | Per-op parity (users/teams/partners/design-partners) | Backend Eng |
| `Resource` union correctness (A04) | Medium | Medium | `@DgsTypeResolver` + per-member tests | Backend Eng |
| Schema-drift drop/undrop owned by workspace (F03) | Medium | Low | Coordinate ownership with workspace | Architect |
| Attachment coupling on write | Low | Medium | Attachment client / entity refs | Architect |

## 5. Summary
- **Stories:** 37 (A:5 · B:7 · C:2 · D:13 · E:2 · F:3 · G:5) covering 11 queries + 26 mutations (+3 drift).
- **Critical path:** A01→A02/A05→A04→G01→G05; E02 + D12 for the heavy writes.
- **Highest cost:** v1/v2/V3 consolidation + participant management + the field-resolver surface (+ `Resource` union).
- **Separate subgraph:** discussion provides `discussionsCount`/`discussionsV2` + the TechPack `discussions` count.

---
**Phase Completed:** Phase 4 — Migration Stories · **Domain:** `discussion` · **Outputs:** 04-stories.md, 04-stories-index.yaml, 04-po-summary.md.

---
