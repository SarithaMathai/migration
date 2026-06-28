# Phase 4: PO Sprint Planning Summary — Discussion

> **Domain:** `discussion` · **Target DGS:** separate `plm-discussion` subgraph (v1/v2/V3) · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

We are moving the **Discussion** domain — threaded discussions/replies on products, samples and workspaces,
their participants, sample discussions, flags (critical/editable/tag), read-receipts and bulk operations —
off the `spark-internal-graphql` gateway into its **own `plm-discussion` DGS subgraph**. Discussion is
referenced by **product** and **workspace** (it provides `discussionsCount`/`discussionsV2` and the TechPack
`ResourcesCount.discussions` count, `SPARK-PROD-F02`).

It is **large**: it consolidates **three API versions** (v1/v2/V3) into one subgraph — **11 queries + 26
mutations** (plus 3 schema-drift ops), ~12 field-resolver type blocks, and the **`Resource` union**
(`Product` | `SampleV2` | `WorkspaceV2`, resolved by id prefix). The defining wrinkles are the **`core*`
twins** (system-context versions of public ops — paired per story) and the **participant-management** surface
(V2 + V3 + core delete over users/teams/partners/design-partners).

**ACL note:** read/write tokens are context-only. The drop/undrop partner bookkeeping is **driven by the
workspace dispatcher** (`workspaceBusinessPartnerActionsV2`), so it is a deferred drift decision, not build
work here.

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

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 5 | 12–20d |
| B | Core Reads | 7 | 9–15d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations | 13 | 22–37d |
| E | Participant management | 2 | 6–10d |
| F | Federation & decisions | 3 | 4–7d |
| G | Field Resolvers & Tests | 5 | 13–22d |
| **Total** | | **37** | **70–118d** (buffered) |

> One engineer ≈ **14–24 sprints**. Parallelizable after A.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| Three API versions (v1/v2/V3) + `core*` twins | 🟡 Medium | Consolidate in the service port; pair each twin (system vs user context) per story |
| Participant-management correctness (V2/V3) | 🟡 Medium | Per-op parity over users/teams/partners/design-partners |
| `Resource` union correctness | 🟡 Medium | `@DgsTypeResolver` + per-member tests (product/sample/workspace by prefix) |
| Drop/undrop drift owned by workspace | 🟢 Low | Coordinate ownership; decide delete vs keep `@deprecated` |
| Attachment coupling on write (bulk input + clone) | 🟢 Low | Attachment client / entity refs |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Consolidate v1/v2/V3 into one surface, or preserve all three? | A05 | Architect |
| 2 | `core*` twins — separate ops or one op with a context flag? | A05/D11/D13/E02 | Backend Eng |
| 3 | Delete or `@deprecated`-keep the 3 drift ops (drop/undrop + `coreAddBulkDiscussionV3`); drop/undrop ownership with workspace | F03 | Architect |

## Dependency Map
```
plm-discussion (Discussion subgraph) depends on (all cross-subgraph):
  search 🔴 (elastic discussions)
  attachment, user-profile/user-group, relationship 🟡 ; access-control (context + workspace drop/undrop)
  Hive Gateway → VMM ; tag
  Resource union members → Product / SampleV2 / WorkspaceV2 (entity stubs)
  provides → Discussion entity + ResourcesCount.discussions for product/workspace
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | A01–A05 | schema (~20 types + `Resource` resolver + ~12 inputs), service port (v1/v2/V3 consolidate) |
| 3 | B01–B07 + C01–C02 | reads + elastic + sample |
| 4 | D01–D08 | add/update/delete/reply/sample/flags |
| 5 | D09–D13 + E01 | clone/read-receipts, V3 add/bulk/update, participants V2 |
| 6 | E02 + F01–F03 | participants V3 + entity fetcher + TechPack count + drift |
| 7 | G01–G05 | field-resolver surface (incl. `Resource` union) + tests |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~14–24 sprints | sequential |
| 2 engineers | ~8–14 sprints | reads + mutations + participants parallel after A |

---
*Pipeline 2.0 — Phase 4 complete. Discussion artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Separate `plm-discussion` subgraph (v1/v2/V3).*
