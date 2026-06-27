# Phase 5: Attribute (Field) Inventory — Watchlist

> **Domain:** `watchlist` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`code/schemas/SPARK_Watchlist.txt`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` (internal) · `EXT` (severity) · `Polymorphic`.

## Table 1 — non-trivial field resolvers

| Type | Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|-----------|------------|-------|
| `Watchlist` | `statusId` | `Int` | Computed (`status.code`) | — | Low | G01 |
| `Watchlist` | `statusName` | `String` | Computed (`status.description`) | — | Low | G01 |
| `Watchlist` | `reasonIds` | `[Int]` | Computed (`reasons[].code`) | — | Low | G01 |
| `Watchlist` | `reasons` | `[String!]` | Computed (`reasons[].description`) | — | Low | G01 |
| `WatchlistInspection` | `actionId` | `Int` | Computed (`action.code`) | — | Low | G01 |
| `WatchlistInspection` | `action` | `String!` | Computed (`action.description`) | — | Low | G01 |
| `Watchlist` | `attachments` | `[SearchAttachment]` | EXT (elastic by related) | 🔴 search | Medium | G03 |
| `Watchlist` | `product` | `Product` | Field-resolver (internal) | — same DGS (only if `parentId` starts `PID`) | Low | G03 |
| `Watchlist` | `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G02 |
| `Watchlist` | `workspaces` | `[WorkspaceV2]` | EXT | 🟡 workspaceV2 | Low | G02 |
| `Watchlist` | `participantDetails` | `UserGroup_Participants` | EXT | 🔵 user-group | Medium | G02 |
| `WatchlistPartner` | `partnerName` | `String` | EXT (VMM `bpName`) | 🔵 vmm | Low | G02 |

**Direct pass-throughs (from the record):** `Watchlist.{humanId, parentId, workspaceContext,
businessPartners, otherReason, notes, inspections, version, createdAt, updatedAt}`;
`WatchlistInspection.{id, type, instructions}`; `WatchlistPartner.{partnerId, partnerType, systemTeamId}`;
all of `WatchlistInspectionAction` — DTO-mapped, no resolver. Covered by A02 + B01.

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `WatchlistInput` | `parentId` | `String!` | Yes | the product |
| `WatchlistInput` | `attachmentIds` / `removedAttachmentIds` | `[String!]` | No | `removedAttachmentIds` drives the archive step (E01) |
| `WatchlistInput` | `participantDetails` / `relatedResources` | mixed | No | drive the user-group upsert (D01/E01) |
| `WatchlistInspectionInput` | `actionId` | `Int` | No | maps to the action code |
| `WatchlistAttachmentCloneRef` | `relatedResources` / `context` | mixed | No | paired positionally with `attachmentIds` (D02) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~22 | Free — schema + DTO mapping; 6 are simple computed flatteners (G01) |
| Field-resolver (internal, same DGS) | 1 | `product` — cheap |
| EXT (cross-domain) | 6 | federation/elastic; `participantDetails` (user-group), attachments (search) |
| Polymorphic | 0 | none |

**Signal:** Watchlist is **shallow** — most fields are direct or simple computed flatteners. Cost
concentrates in the multi-step `updateWatchlistEntries` write (E01, incl. the await-race fix) and the
4-step `getWatchlistByFilter` read (C01). No polymorphism.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `watchlist`.
