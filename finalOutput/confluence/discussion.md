# Discussion — Migration to a dedicated `plm-discussion` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../discussion/03-schema-analysis.md) ·
> [field inventory](../discussion/05-attribute-inventory.md) · [engineering stories](../discussion/04-stories.md).
> Create tickets from [`../jira/discussion.csv`](../jira/discussion.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Discussion** domain — threaded discussions/replies on products, samples and workspaces,
their participants, sample discussions, flags (critical/editable/tag), read-receipts and bulk operations — off
the `spark-internal-graphql` gateway into its **own `plm-discussion` DGS subgraph**. Discussion is referenced
by **product** and **workspace** (it provides `discussionsCount`/`discussionsV2` and the TechPack
`ResourcesCount.discussions` count, `SPARK-PROD-F02`).

It is **large**: it consolidates **three API versions** (v1/v2/V3) into one subgraph — **11 queries + 26
mutations** (plus 3 schema-drift ops), ~12 field-resolver type blocks, and the **`Resource` union** (`Product`
| `SampleV2` | `WorkspaceV2`, resolved by id prefix). The defining wrinkles are the **`core*` twins**
(system-context versions of public ops — paired per story) and the **participant-management** surface (V2 + V3
+ core delete over users/teams/partners/design-partners).

**ACL note:** read/write tokens are context-only; the drop/undrop partner bookkeeping is **driven by the
workspace dispatcher** (`workspaceBusinessPartnerActionsV2`), so it is a deferred drift decision, not build work
here.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 11 | by-id/by-resource/by-thread, version history (V3), elastic (🔴 search), sample |
| Mutations | 26 (+3 deferred drift) | add/update/delete, replies, sample, flags, files clone, read-receipts, participants V2/V3 + core twins |
| Field-resolver type blocks | ~12 | `Discussion`/`FullDiscussion`/`DiscussionReply`/participants/team + the `Resource` union + versioned |
| Polymorphism | 1 union (`Resource`) | A04 (`@DgsTypeResolver` by id prefix) |
| External dependencies | 6 keys | search 🔴; attachment/user-profile/user-group 🟡; vmm/tag 🔵 |
| Federation role | provides `Discussion` entity + `ResourcesCount.discussions` | product/workspace |
| **Total stories** | **37** | green-field; separate subgraph |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 5 | 12–20d |
| B | Core Reads | 7 | 9–15d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations | 13 | 22–37d |
| E | Participant management | 2 | 6–10d |
| F | Federation & decisions | 3 | 4–7d |
| G | Field Resolvers & Tests | 5 | 13–22d |
| **Total** | | **37** | **70–118d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| Three API versions (v1/v2/V3) + `core*` twins | 🟡 Medium | Consolidate in the service port; pair each twin (system vs user context) |
| Participant-management correctness (V2/V3) | 🟡 Medium | Per-op parity over users/teams/partners/design-partners |
| `Resource` union correctness | 🟡 Medium | `@DgsTypeResolver` + per-member tests (product/sample/workspace by prefix) |
| Drop/undrop drift owned by workspace | 🟢 Low | Coordinate ownership; decide delete vs keep `@deprecated` |
| Attachment coupling on write (bulk input + clone) | 🟢 Low | Attachment client / entity refs |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Consolidate v1/v2/V3 into one surface, or preserve all three? | A05 | Architect |
| 2 | `core*` twins — separate ops or one op with a context flag? | A05/D11/D13/E02 | Backend Eng |
| 3 | Delete or `@deprecated`-keep the 3 drift ops (drop/undrop + `coreAddBulkDiscussionV3`); drop/undrop ownership with workspace | F03 | Architect |

## Migration approach (summary)

Phase **A** schema (~20 types + the `Resource` `@DgsTypeResolver` + ~12 inputs) + service port consolidating
`DiscussionService` v1/v2 + V3; **B** by-id/by-resource/by-thread/version reads; **C** elastic
`getDiscussionsV2` + `getSampleDiscussion`; **D** the create/update/delete/reply/sample/flag/files/read-receipt
writes (V2 + V3 + core twins); **E** participant management (V2 + V3 + core delete); **F** expose `Discussion`
as a federated entity + the TechPack count + the 3-drift decision; **G** the field-resolver surface (incl. the
`Resource` union) + tests. Full detail: [03-schema-analysis.md §Migration Approach](../discussion/03-schema-analysis.md).

## Sequencing & capacity

Parallelizable after A; **2 engineers recommended** (~8–14 sprints for two vs ~14–24 for one). Reads,
mutations and participant management run in parallel after the schema + service port land. Full plan:
[04-po-summary.md](../discussion/04-po-summary.md).

---
*PO page assembled from the discussion analysis. Tickets:
[`../jira/discussion.csv`](../jira/discussion.csv) · [`../jira/discussion-stories.md`](../jira/discussion-stories.md).*
