# Phase 2: Resolver Dependency Analysis — Discussion

> **Domain:** `discussion` · **Target DGS:** `DiscussionService` (+ V3) → separate `plm-discussion` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `SPARK_Discussion(.V3)` SDLs + resolvers (902 + 543) + services (319 + 87)
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full (V2 resolver in windows)

Implementation spec. ACL/JWT usage is **context-only**. `discussion` is its **own subgraph** (V2 + V3 surfaces).

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 11 |
| Mutation resolvers | 26 (+3 schema-drift) |
| Field resolvers | ~12 type blocks (incl. 1 union) |
| Service methods | ~30 (v1 + v2 + V3) |
| EXT loaders | 6 (1 🔴 · 3 🟡 · 2 🔵) + accessControl context |
| High complexity | participant V3 ops; bulk V3; the field-resolver surface |

---

## Query Resolvers (11)

| # | Query | Complexity | Pseudo-logic |
|---|-------|-----------|--------------|
| Q1 | `getDiscussionV2(id)` / `coreGetDiscussionV2(id)` | Low | (own) `GET discussions/v2?ids={id}` → `FullDiscussion` (core = system context). |
| Q2 | `getDiscussionByIdsV2(ids)` | Low | (own) `GET /v2?ids={csv}`. |
| Q3 | `getDiscussionsCount(resourceId, resourceType)` | Low | (own) count by resource → `[ResourceCount]`. |
| Q4 | `getDiscussionOnResource(resourceId)` | Low | (own) discussions for a resource. |
| Q5 | `getDiscussionsByThread(id)` | Low | (own) discussions in a thread. |
| Q6 | `getUnsentDiscussions` | Low | (own) `GET /api/admin/unsent`. |
| Q7 | `getDiscussionsV2(resourceId, resourceType, partnerId)` | Medium | (🔴 search) elastic discussions (partner-filtered) → `DiscussionElastic`. |
| Q8 | `getSampleDiscussion(resourceId, resourceType, partnerId)` | Medium | (own) sample-scoped discussions. |
| Q9 | `getVersionedDiscussions(id)` / `getVersionedDiscussionThreads(id)` | Medium | (own V3) version history for a discussion / its threads. |

## Mutation Resolvers (26 + 3 drift)

| Group | Mutations | Complexity | Notes |
|-------|-----------|-----------|-------|
| **Add discussion** | `addDiscussionV2` (+attachments), `addDiscussionV3` / `coreAddDiscussionV3` | Medium | create + (🟡 attachment) bulk attachment input. |
| **Bulk add** | `addBulkDiscussionV3` (+ `coreAddBulkDiscussionV3` ⏭ drift) | High | bulk create across resources. |
| **Update discussion** | `updateDiscussionV2`, `updateDiscussionV3` / `coreUpdateDiscussionV3` | Medium | body update. |
| **Delete** | `deleteDiscussionV2`, `deleteDiscussionReplyV2`, `deleteDiscussionPartnersV2` | Low | id-scoped deletes. |
| **Replies** | `addDiscussionReplyV2`, `updateDiscussionReplyV2` (+attachments, `isAttachmentsV3`) | Medium | thread replies. |
| **Participants V2** | `updateParticipantsV2`, `deleteParticipantV2` | Medium | add/remove participants (team/user/partner). |
| **Participants V3** | `updateParticipantsV3` / `coreUpdateParticipantsV3`, `coreDeleteParticipantsV3`, `deleteParticipantV3` | High | richer participant model (users/teams/partners/design-partners). |
| **Sample discussions** | `addSampleDiscussionV2`, `addSampleDiscussionV3`, `bulkAddSampleDiscussions` | Medium | sample-scoped create. |
| **Flags** | `updateAsCritical`, `updateDiscussionEditable`, `updateTagExisting` | Low | share one `DiscussionAsCritical` input shape. |
| **Files** | `cloneFilesForBulkDiscussion` (🟡 attachment) | Medium | per-attachment clone fan-out. |
| **Read receipts** | `discussionReadByUsers` | Medium | mark read across discussions + threads. |
| **⏭ Drift** | `dropPartnerFromDiscussionIds`, `unDropPartnerFromDiscussionIds` | — | **no top-level resolver** — service methods called inside `workspaceBusinessPartnerActionsV2`. |

## Polymorphism · `SPARK_Resource.__resolveType`
Union → the discussion's parent resource type (product/sample/workspace/etc., by id prefix). **DGS:**
`@DgsTypeResolver(name="Resource")` mirroring the prefix mapping.

## Field Resolvers (~12 type blocks)
- `SPARK_Discussion` / `SPARK_FullDiscussion` / `SPARK_DiscussionContent` — discussion bodies, content,
  created/updated users, resource link.
- `SPARK_DiscussionReply` — reply bodies, attachments, author, notification status.
- `SPARK_Discussion_Participants` / `_Team` / `_Participant` — participant hydration (🟡 user-profile, 🔵 vmm).
- `SPARK_Resource` — the union (`__resolveType`).
- `SPARK_NotificationStatus` — per-reply notification state.
- V3: `SPARK_VersionedDiscussion` / `SPARK_VersionedDiscussionThread` (`updatedBy` 🟡 user, `updatedAt` parse),
  `SPARK_DiscussionReadByUsers` (`discussions`/`discussionThreads`).

## Service Classes
`DiscussionService` base `discussions/v1` (+ `discussion_message`, `/bulk`) and `discussions/v2` (`/discussion`),
admin `/api/admin/unsent`. `DiscussionV3Service` base its own. ~30 methods total.

## EXT Service Call Inventory (summary)
6 keys — **1 🔴** (search) · **3 🟡** (attachment, user-profile/userGroup, relationship) · **2 🔵** (vmm, tag) ·
accessControl **context**.

## Key Findings
- **Highest cost:** the participant-management writes (V2 + V3 + core twins) and the field-resolver surface
  (incl. the `Resource` union); bulk V3.
- **Schema-drift:** `dropPartnerFromDiscussionIds`/`unDropPartnerFromDiscussionIds` (owned by workspace
  dispatcher) + `coreAddBulkDiscussionV3` (no resolver).
- **`core*` twins:** pair each with its public op in one story (system vs user context).
- **Federation provider:** discussion provides `discussionsCount`/`discussionsV2` for product/workspace and
  the TechPack `ResourcesCount.discussions` count.
- **Quick wins:** the simple by-id/by-resource/by-thread reads, the flag mutations, deletes.

---
**Phase Completed:** Phase 2 · **Domain:** `discussion` · **EXT:** 6 keys (1🔴 · 3🟡 · 2🔵).
