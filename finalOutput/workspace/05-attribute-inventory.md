# Phase 5: Attribute (Field) Inventory — Workspace

> **Domain:** `workspace` · **Target DGS:** separate `plm-workspace` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`code/schemas/SPARK_WorkspaceV2.txt`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — `WorkspaceV2` non-trivial field resolvers

| Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|-----------|--------------|------------|-----------|------------|-------|
| `attachmentsWithMetaData` | `[AttachmentWithMetaData]` | EXT (relationship→attachment→discussion merge, ~75 ln) | 🔴 attachment + 🟡 relationship/discussion | Very High | G01 |
| `counts` | `WorkspaceCountsV2` | EXT (search+product+discussion+sample rollup, ~85 ln) | 🔴 search/product + 🟡 discussion | Very High | G02 |
| `attachmentsV3` | `SearchAttachmentsPaged` | EXT (relationship→attachment, per-BP counts) | 🔴 attachment + 🟡 relationship | High | G03 |
| `products` | `ProductsPaged` | EXT (calls product getProducts) | 🔴 product | High | G04 |
| `productsCount` | `Int` | EXT (product getPage totalElements) | 🔴 product | Medium | G04 |
| `combinations` | `CombinationSourcePaged` | EXT (search + combination getByIds) | 🔴 search + 🟡 combination | High | G04 |
| `sampleReport` | `WorkspaceReportV2` | EXT (search samples + sampleV2 + round filter) | 🔴 search + 🟡 sampleV2 | High | G04 |
| `businessPartners` / `droppedPartners` | `[VMM_BusinessPartner]` | EXT | 🔵 vmm | Medium | G05 |
| `notRemovablePartnerIds` / `unDroppablePartners` | `[ID]` | EXT (util + ACL) | 🔵 (acl context) | Medium | G05 |
| `divisions` / `clazzes` | `[IG_Division]` / `[IG_Clazz]` | EXT | 🔵 ig | Medium | G06 |
| `brands` | `[VMM_Brand]` | EXT | 🔵 brand | Medium | G06 |
| `designCycles` / `tags` | `[Tag]` | EXT | 🟡 tag | Medium | G06 |
| `departments` (`WorkspaceDepartmentV2.node`/`clazzes`) | `[WorkspaceDepartmentV2]` | EXT | 🔵 ig | Medium | G06 |
| `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Medium | G07 |
| `discussionsV2` / `teams` | discussion / team types | EXT (elastic) | 🔴 search | Medium | G07 |
| `id` / `status` / `workspaceTypeElastic` / `createdAt` / `updatedAt` | mixed | Computed (from record) | — | Low | G07 |

**Direct pass-throughs:** `WorkspaceV2.{workspaceType, description, setDates, protoApprovalDueDate,
setDateRange, version, enableDateRule, productsCount(scalar), resources}`; all of `WorkspaceCountsV2`,
`WorkspaceProductDashboard(StatusCount)`, `StatusCount`, `WorkspaceReportV2`, `WorkspaceTypeCount`,
`WorkspaceExportReceipt`, `WorkspaceContentResult`/`WorkspaceProductResult`, `DateRange`, and the
`WorkspacesPagedV2/V3` content/paging/pageable (computed) — DTO-mapped. Covered by A02 + B01.

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `CreateWorkspaceInputV2` | `departmentIds` / `brandIds` | `[DepartmentInputV2]!` / `[ID]!` | Yes | required on create |
| `UpdateWorkspaceInputV2` | `id` | `ID!` | Yes | |
| `WorkspaceTeamInput` | `teamId` / `existingGroups` | `String!` / `AccessPermission!` | Yes | team grant map |
| `WorkspacePartnerActionInputV2` | `dropped` / `partnerType` / `teamInput` | mixed | No | drive the E01 dispatcher cases |
| `WorkspaceExportOptions` | `userProfileId`/`workspaceId`/`workspaceDescription` | `String!` | Yes | Excel export (D08) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~30 | Free — schema + DTO mapping (A02/B01) |
| Field-resolver (internal) | 0 | workspace is its own subgraph — nothing co-located |
| EXT (cross-domain) | ~18 | federation/elastic; 2 Very-High (attachmentsWithMetaData, counts) + cross-subgraph product |
| Polymorphic | 0 | none |

**Signal:** Workspace is **wide and federation-heavy** — as a standalone hub every reference is
cross-subgraph. Cost concentrates in the partner-action dispatcher (E01) and the two Very-High field
resolvers (`attachmentsWithMetaData`, `counts`); the cross-subgraph coupling to **product** is the main
architectural decision. No polymorphism.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `workspace`.
