# Phase 5: Attribute (Field) Inventory — Search

> **Domain:** `search` · **Target DGS:** separate `plm-elastic-search` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`code/schemas/SPARK_Search.txt`).
> Search has a **large type surface**; this lists the enrichment (non-trivial) field resolvers by result type
> and groups the direct pass-throughs.

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — enrichment field resolvers (by result type)

| Type | Attribute(s) | Resolution | EXT (sev) | Complexity | Story |
|------|--------------|------------|-----------|------------|-------|
| `SearchAttachment` | `relatedProduct` | EXT (PID-prefix) | 🟡 product | High | G01 |
| `SearchAttachment` | `relatedWorkspace` | EXT (WRK-prefix) | 🟡 workspaceV2 | High | G01 |
| `SearchAttachment` | `createdBy`/`updatedBy` | EXT | 🟡 user-profile | Medium | G01 |
| `SearchAttachment` | `renders`/`gallery`/`modelFile` | EXT (gated) | 🟡 attachment | High | G01 |
| `SearchAttachment` | `currentUserFileAccess` | EXT (ACL context) | acl | Medium | G01 |
| `SearchAttachment` | `tags`/`productPacketProps`/`canOpenInShowDog`/`finalVirtualFile` | Computed / delegate | — | Low | G01 |
| `Material` | `supplierName`/`businessPartners`/`droppedPartnerIds`/`teams` | EXT | 🔵 vmm | High | G02 |
| `Material` | `claims` | EXT | 🔵 fabric | Medium | G02 |
| `Material` | `colorLinks` | EXT (**12-prefix gate**) | 🔵 color | High | G02 |
| `Material` | `permissions` | EXT (ACL context) | acl | Medium | G02 |
| `Material` | `attachments` | EXT (own elastic) | — | Medium | G02 |
| `Material` | `tags`/`createdBy` | EXT | 🔵 tag / 🟡 user | Low | G02 |
| `Material` | `baseMaterial`/`referenceId`/`impressionIntent`/`is3D`/`trimSuppliers` | Computed | — | Low | G02 |
| `SearchCombination` | `brands`/`partners`/`department`/`division`/`designCycles`/`materialCategory`/`fabricSpec`/`tags` | EXT | 🔵 brand/vmm/ig/tag/fabric | Medium | G03 |
| `SearchPalette` | `brands`/`tags`/`designCycles`/`departments`/`partners` | EXT | 🔵 brand/tag/ig/vmm | Medium | G03 |
| `SearchWatchlist` | `product`/`workspaces`/`participantDetails`/`attachments`/`partners`/users | EXT | 🟡 product/workspace + 🔵 vmm/userGroup | Medium | G04 |
| `SearchComponent` | `materials` (BOM-prefix)/`workspaces`/users | EXT | 🟡 bom/workspace/user | Medium | G04 |
| `SearchAttachmentAccess` | `bps` (union)/`partnerNamesMap` | Computed / EXT | 🔵 vmm | Medium | G05 |
| `ConnectedBOMGroup(Result)` | `groupBy`/`designCycle` | EXT | 🔵 ig/tag | Medium | G05 |
| `Requested_Evaluated_Samples_By_User` | `user` | EXT | 🟡 user-profile | Medium | G05 |
| `SearchProductDivision/DepartmentCount` | `division`/`department` | EXT | 🔵 ig | Low | G05 |
| paged types (`*Paged`) | `paging`/`counts` | Computed (`MaterialsPaged.counts` → getCounts) | — | Low | G05 |

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `MaterialSearchArguments` | `searchCriteria`/`nestedFilters`/`filters` | lists | No | rich elastic material body (C02) |
| `MaterialSearchCriteria` | `rgbColor` | `MaterialRGBSearchCriteria` | No | RGB color search |
| `MaterialSearchFilter` | `fieldPath`/`values` | `String!`/`[String]!` | Yes | field filter |
| `MaterialNestedSearchFilter` | `type`/`nestedFieldPath`/`fieldPath`/`values` | mixed | Yes | nested filter |
| `UpdateCombinationQueryInput` | `query`/`comboBulkUpdates`/`updateCombinationList` | mixed/JSON | No | bulk combination mutation (D01) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~large (most of ~50 result types) | Free — schema + DTO mapping; **but the type surface itself is the work (A02)** |
| Field-resolver (internal) | 0 | search is its own subgraph |
| EXT (cross-domain enrichment) | ~40 across result types | DataLoader-batched federation/gateway lookups (G01–G05) |
| Polymorphic | 0 | none |

**Signal:** Search is **wide and enrichment-heavy** — the migration cost is the **result-type surface** (A02)
and the per-type **enrichment field resolvers** that re-hydrate from many subgraphs (G01/G02 are the
heaviest). Queries themselves are thin elastic wrappers. No polymorphism, no multi-step writes.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `search`.
