# Phase 3: Federation Schema Analysis — Discussion

> **Domain:** `discussion` · **Target DGS:** separate `plm-discussion` subgraph (v1/v2/V3)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 37 🔜 | 3 ⏭ — 40 operations**

- The target schema is translated from the two source SDLs (`resolvers/SPARK_Discussion.js` + `resolvers/SPARK_DiscussionV3.js`), verified against the resolvers.
- **Discussion is its own subgraph** (`plm-discussion`) — every reference is cross-subgraph.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `Discussion` (key `discussionId`) |
| Owned value types | ~18 | `FullDiscussion`, `DiscussionReply`, `DiscussionContent`, participants/team, versioned, sample, unsent, bulk output |
| Union (`@DgsTypeResolver`) | 1 | `Resource` (`Product` \| `SampleV2` \| `WorkspaceV2`) |
| `@shareable` | 1 | `ResourceCount` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — other DGS | ~7 | `Attachment`, `SearchAttachment`, `DiscussionElastic`, `UserProfileAttributes`, `UserGroup_Participants`, `Tag` + Resource members (`Product`/`SampleV2`/`WorkspaceV2`) |
| Inputs | ~12 | `DiscussionInput(V3)`, `BulkDiscussionInputV3`, `DiscussionReplyInput`, `AddParticipantInput`, `DiscussionAsCritical`, … |

## 2. Polymorphism — `Resource` union (`@DgsTypeResolver`)
The discussion's **parent resource** (`Product` | `SampleV2` | `WorkspaceV2`, by id prefix). **+1 complexity
tier.** `@DgsTypeResolver(name="Resource")` mirroring the prefix mapping.

## 3. Client Contract Verification
- 11 queries + 26 mutations preserved (`0 ✅ | 37 🔜`); **3 schema-drift mutations deferred ⏭** (`dropPartnerFromDiscussionIds`, `unDropPartnerFromDiscussionIds` — service methods run inside `workspaceBusinessPartnerActionsV2`; `coreAddBulkDiscussionV3` — no resolver).
- `SPARK_`/`V2`/`V3` naming preserved (client contract).
- **`core*` twins** are system-context versions of the public ops — keep both.
**Entity key:** `Discussion.discussionId`.

## 4. Federation Boundaries

> **Separate subgraph:** `discussion` is its own DGS (consolidating v1/v2/V3). **It provides**
> `discussionsCount`/`discussionsV2` for product/workspace and the TechPack `ResourcesCount.discussions`
> count (`SPARK-PROD-F02`); `Discussion` is referenced as an entity by id.

- **Owns** `Discussion` + ~18 value types + the `Resource` union.
- **External (federation):** `search` (elastic discussions), `attachment` (bulk attachment input + clone),
  `user-profile`/`user-group` (participants/authors), `relationship`; **gateway stitch:** `VMM`, `Tag`.
- The `Resource` union members (`Product`/`SampleV2`/`WorkspaceV2`) are entity stubs resolved by their subgraphs.

## 5. Migration Approach  *(Confluence approach page)*

Discussion is **large** — it consolidates three API versions (v1/v2/V3), a wide write surface (participants,
replies, sample discussions, bulk), and the `Resource` union.

1. **Phase A:** schema (~20 types + the `Resource` `@DgsTypeResolver` + ~12 inputs) + service port
   (consolidate `DiscussionService` v1/v2 + `DiscussionV3Service`). Pair each `core*` twin with its public op.
2. **Phase B:** the by-id/by-resource/by-thread/version reads.
3. **Phase C:** elastic `getDiscussionsV2` + `getSampleDiscussion`.
4. **Phase D:** the create/update/delete/reply/sample/flag/files/read-receipt writes (V2 + V3 + core twins).
5. **Phase E:** participant management (V2 + V3 + core delete).
6. **Phase F:** provide `Discussion` as a federated entity + the TechPack `ResourcesCount.discussions` count;
   decide the 3 deferred drift mutations (drop/undrop owned by workspace).
7. **Phase G:** the field-resolver surface (discussion/reply/participants/`Resource` union/versioned/
   read-receipts) + tests.

## 6. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Three API versions (v1/v2/V3) + `core*` twins | Medium | High | Consolidate in the service port; pair twins per story | Tech Lead |
| Participant-management correctness (V2/V3) (E01/E02) | Medium | Medium | Per-op parity (users/teams/partners/design-partners) | Backend Eng |
| `Resource` union correctness (A04) | Medium | Medium | `@DgsTypeResolver` + per-member tests | Backend Eng |
| Schema-drift drop/undrop owned by workspace (F03) | Medium | Low | Coordinate ownership with workspace | Product Owner |
| Attachment coupling on write (bulk attachment input) | Low | Medium | Attachment client / entity refs | Product Owner |

## 7. ACL Handling
Reads/writes curry capability tokens; drop/undrop bookkeeping lives in the workspace dispatcher. **ACL is
ignored in the DGS implementation** (no ACL story) — context only.

## 8. Open Questions
1. Consolidate v1/v2/V3 to one surface, or preserve all three?
2. `core*` twins — keep as separate system-context ops or fold into one with a context flag?
3. `Resource` union members + prefix rules; delete vs keep the 3 drift mutations (drop/undrop ownership)?

---
**Phase Completed:** Phase 3 · **Domain:** `discussion`.
