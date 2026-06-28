# Phase 5: Attribute (Field) Inventory — Discussion

> **Domain:** `discussion` · **Target DGS:** separate `plm-discussion` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDLs (`code/schemas/SPARK_Discussion.txt` + `SPARK_DiscussionV3.txt`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — non-trivial field resolvers

| Type | Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|-----------|------------|-------|
| `Discussion` | `resource` | `Resource` | **Polymorphic** (`@DgsTypeResolver` by id prefix) | — | High | A04/G01 |
| `Discussion` | `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Medium | G01 |
| `Discussion` | `tags` | `[Tag]` | EXT | 🔵 tag | Low | G01 |
| `Discussion` | `participants` | `Discussion_Participants` | Field-resolver | — | Medium | G01 |
| `Discussion` | `replies` | `[DiscussionReply]` | Field-resolver | — | Medium | G01 |
| `Discussion` | `attachments` | `[Attachment]` | EXT | 🟡 attachment | Medium | G01 |
| `Discussion` | `content` | `DiscussionContent` | Field-resolver (text/html) | — | Low | G01 |
| `Discussion` | `createdAt`/`updatedAt` | DateTime | Computed (Date parse) | — | Low | G01 |
| `FullDiscussion` | `resource`/`participants`/`replies` | mixed | Field-resolver (shared with `Discussion`) | — | Medium | G01 |
| `DiscussionReply` | `createdBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Medium | G02 |
| `DiscussionReply` | `attachments` | `[Attachment]` | EXT | 🟡 attachment | Medium | G02 |
| `DiscussionReply` | `notificationStatus` | `NotificationStatus` | Field-resolver | — | Low | G02 |
| `Discussion_Team` | `businessPartner` | `VMM_BusinessPartner` | EXT | 🔵 vmm | Medium | G03 |
| `Discussion_Participant` | `userDetails` | `UserProfileAttributes` | EXT | 🟡 user-profile | Medium | G03 |
| `VersionedDiscussion` / `…Thread` | `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G04 |
| `VersionedDiscussion` / `…Thread` | `updatedAt` | String | Computed (parse) | — | Low | G04 |
| `DiscussionReadByUsers` | `discussions`/`discussionThreads` | `[JsonNode]` | Computed | — | Low | G04 |

**Direct pass-throughs:** `Discussion.{discussionId, discussionThreadId, subject, resourceId, resourceType,
partnerId, critical, draft, editable}`, `DiscussionContent.{text, html}`, `DiscussionReply.{message, critical,
editable}`, `ResourceCount.{resourceId, count}`, `SampleDiscussion.*`, `UnsentDiscussions.{count}` — DTO-mapped.

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `DiscussionInput` | `resourceId`/`resourceType`/`subject`/`content`/`participants` | mixed | No | V2 create (D01/D07) |
| `DiscussionInputV3` | `discussionId`/`attachmentId`/`resourceId`/`subject`/`content`/`participants` | mixed | No | V3 create (D11) |
| `BulkDiscussionInputV3` | `discussionDtoList` | `[DiscussionInputV3]` | No | bulk create (D12) |
| `DiscussionReplyInput` | `discussionId`/`message`/`critical` | `ID!`/String/Boolean | id Yes | reply add/update (D02) |
| `AddParticipantInput` | `teams`/`users`/`partnerIds` | `[String]`/`[ID]` | No | participants V2 (E01) |
| `ParticipantsInput` | `teams`/`users` | `[String]` | No | participants V3 (E02) |
| `DiscussionAsCritical` | `discussionId`/`discussionThreadId`/`value`/`tagId` | mixed | No | flags — critical/editable/tag (D08) |
| `BulkAttachmentInput` | `documentId`/`resource`/`relatedResources` | mixed | No | attachment association on create (D01/D02/D11) |
| `BulkDiscussionAttachCloneRef` | `resourceId`/`businessPartner`/`relatedResources` | mixed | No | clone references (D09) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~26 | scalar bodies + Date/JSON parse — straightforward DTO mapping |
| Field-resolver (internal) | ~6 | content/replies/participants/notificationStatus links |
| EXT (cross-domain) | ~9 | users/attachments (🟡), tags/vmm (🔵), search (🔴 elastic read) |
| Polymorphic | 1 | `Resource` union (`@DgsTypeResolver` by id prefix) — +1 complexity tier |

**Signal:** Discussion is **write- and orchestration-heavy** (participants V2/V3 + core twins, replies, sample,
bulk) on top of a wide field-resolver surface. The decisive tasks are the **v1/v2/V3 consolidation** (A05), the
**participant-management** writes (E01/E02), and the **`Resource` union** (A04/G01); the EXT enrichment
(users/attachments/tags/vmm) is the remainder.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `discussion`.
