# Phase 1: Schema Inventory — Discussion

> **Domain:** `discussion`
> **Target DGS:** `DiscussionService` (+ V3) → **separate `plm-discussion` subgraph**
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_Discussion.graphqls` (334) + `resolvers/SPARK_DiscussionV3.js` (133) + resolvers `resolvers/SPARK_Discussion.js` (902) + `resolvers/SPARK_DiscussionV3.js` (543) + services `services/Discussion.js` (319) + `services/DiscussionV3.js` (87)
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

No `context.js`. `DiscussionService` builds its endpoint in the constructor (`services/Discussion.js:15-16`):
```js
this.endpointv1 = endpoint + '/enterprise_product_development_discussions/v1'
this.endpointv2 = endpoint + '/enterprise_product_development_discussions/v2'
```
- The `_discussions` base is a **distinct backend** → **`plm-discussion`** (per platform direction).
- The domain spans two GraphQL files (`SPARK_Discussion` legacy/V2 + `SPARK_DiscussionV3`) — both compile into this subgraph.

| Setting | Value |
|---|---|
| Loader key | `discussion` |
| Service classes | `DiscussionService` (v1/v2) + `DiscussionV3Service` |
| Backend / DGS | **`plm-discussion`** (separate subgraph + backend) |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | **separate `plm-discussion` subgraph** (referenced by product/workspace/sample; provides TechPack `discussions`) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Discussion.graphqls` | 334 | V2/legacy SDL — 9 queries, 17 mutations, `Discussion`/`FullDiscussion`/`Reply`/participants + `Resource` union |
| `schemas/SPARK_DiscussionV3.graphqls` | 133 | V3 SDL — 2 queries, 12 mutations (incl. `core*` twins), versioned types |
| `resolvers/SPARK_Discussion.js` | 902 ⚠️ | V2 resolvers + ~9 field-resolver type blocks (incl. `Resource.__resolveType`) |
| `resolvers/SPARK_DiscussionV3.js` | 543 | V3 resolvers + 3 field-resolver type blocks |
| `services/Discussion.js` + `services/DiscussionV3.js` | 319 + 87 | REST clients (`discussions/v1` + `/v2`) |
| **⚠️ Large file** | 902 | V2 resolver read in windows |

Schema: **`schemas/SPARK_Discussion.graphqls` + `resolvers/SPARK_DiscussionV3.js` (467 lines)** — target schema in
[03-schema.graphql](./03-schema.graphql) translated from both (nullability from the SDLs).

## 3. Import Graph
```
resolvers/SPARK_Discussion(.V3).js
├── utils/commonLoaders            → getUserPermissionsJWT (ACL — context only)
├── utils/discussionUtils          → batching / attachment relationship helpers
├── utils/userGroupUtils           → participants
└── resolvers/SPARK_Attachment, SPARK_UserAttributes, SPARK_UserGroup (enrichment)
DiscussionService builds endpointv1/v2; DiscussionV3Service its own; postOne/putOne/loadListing/loadOne
```

## 4. Cross-Domain Reference Table (all cross-subgraph — discussion is its own DGS)

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `getDiscussionsV2`/`searchDiscussionsElastic` | `search` | SearchService (elastic) | federation | 🔴 |
| add/reply/bulk **attachments**, clone files | `attachment` | AttachmentService | federation | 🟡 |
| participants (users/teams), `*Participants*` ops | `userGroup` / `userAttributes` | UserProfileService | federation | 🟡 |
| participant/partner business partners | `vmm` | VMM platform | Gateway stitch | 🔵 |
| `tags` / `updateTagExisting` | `tag` | TagService | federation | 🔵 |
| reads/writes capability tokens | `accessControl` | AccessControlService | **context only** | n/a |

## 5. Co-located Siblings
**None** — `discussion` is its **own DGS** (`plm-discussion`). It is **referenced as an entity / via fields**
- by product (`discussionsCount`, `discussionsV2`), workspace (`discussionsV2`, drop/undrop in the partner dispatcher), and sample.
- It **contributes** the TechPack `ResourcesCount.discussions` count (`SPARK-PROD-F02`).

## 6. Hot Spots
1. **`core*` twins** — V3 has `add/coreAdd`, `addBulk/coreAddBulk`, `update/coreUpdate`,
   `updateParticipants/coreUpdateParticipants`, `coreDeleteParticipants` — the `core*` variants are
   **system/internal-context** versions of the public ops (same logic, different auth context). Pair them per story.
2. **Polymorphism** — `SPARK_Resource.__resolveType` union (the discussion's parent resource). +1 tier.
3. **Participant management** — `updateParticipantsV2/V3`, `deleteParticipantV2/V3`, `coreDeleteParticipantsV3`
   (users/teams/partners/design-partners) — the richest writes.
4. **Sample discussions** — `addSampleDiscussionV2`/`V3`/`bulkAddSampleDiscussions` (sample-scoped).
5. **Attachments on write** — add/reply/bulk accept `[SPARK_BulkAttachmentInput]` (🟡 attachment) +
   `cloneFilesForBulkDiscussion`.
6. **Schema-drift mutations (no top-level resolver):** `dropPartnerFromDiscussionIds`,
   `unDropPartnerFromDiscussionIds` (run as service methods inside `workspaceBusinessPartnerActionsV2`), and
   `coreAddBulkDiscussionV3`. Deferred ⏭.
7. **`discussionReadByUsers`** — read-receipts across discussions + threads.
8. **Two API versions** — v1 (`discussion_message`) + v2 (`/discussion`) + V3; the port consolidates.

## 7. Operation Lists
**Queries (11):** getDiscussionsCount, getDiscussionV2, coreGetDiscussionV2, getDiscussionByIdsV2,
getDiscussionsV2, getUnsentDiscussions, getSampleDiscussion, getDiscussionOnResource, getDiscussionsByThread,
getVersionedDiscussions, getVersionedDiscussionThreads.
**Mutations (26 impl + 3 schema-drift):** addDiscussionV2, addDiscussionReplyV2, updateDiscussionV2,
- deleteDiscussionV2, updateParticipantsV2, deleteParticipantV2, deleteDiscussionPartnersV2, updateDiscussionReplyV2, deleteDiscussionReplyV2, addSampleDiscussionV2, addSampleDiscussionV3, bulkAddSampleDiscussions, updateAsCritical, updateDiscussionEditable, updateTagExisting, addDiscussionV3, coreAddDiscussionV3, addBulkDiscussionV3, updateDiscussionV3, coreUpdateDiscussionV3, updateParticipantsV3, coreUpdateParticipantsV3, coreDeleteParticipantsV3, deleteParticipantV3, cloneFilesForBulkDiscussion, discussionReadByUsers.
- **Drift ⏭:** dropPartnerFromDiscussionIds, unDropPartnerFromDiscussionIds, coreAddBulkDiscussionV3.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 11 |
| Mutations | 26 (+3 schema-drift) |
| Object types | ~20 (`Discussion`, `FullDiscussion`, `DiscussionReply`, participants/team, versioned, sample) |
| Field resolvers | ~12 type blocks (incl. `Resource.__resolveType`) |
| Unions (`__resolveType`) | 1 (`Resource`) |
| Service methods | ~30 (v1 + v2 + V3) |
| Cross-domain loader keys | 6 (+ accessControl context) |
| EXT calls | 1 🔴 (search) · 3 🟡 (attachment, user-profile, relationship) · 2 🔵 (vmm, tag) |
| Large files | 1 ⚠️ (V2 resolver 902) |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `discussion` · **Files:** 6 (2,318 lines across V2+V3 schema/resolver/service).
