# Phase 1: Schema Inventory — Workspace

> **Domain:** `workspace`
> **Target DGS:** `WorkspaceServiceV2` → **separate `plm-workspace` subgraph** — NOT the plm-product monorepo
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `code/schemas/SPARK_WorkspaceV2.txt` (321-line SDL) + `code/resolvers/SPARK_WorkspaceV2.txt` (1,060) + `code/services/WorkspaceV2.txt` (164)
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

No `context.js`. `WorkspaceServiceV2 extends SparkService` takes the base URL **directly**
(`this.endpoint = endpoint`, `WorkspaceV2.txt:15`) — the REST service is **`plm-workspace`** (per platform
direction); there is no `enterprise_product_development_products` path suffix.

| Setting | Value |
|---|---|
| Loader key | `workspaceV2` |
| Service class | `WorkspaceServiceV2 extends SparkService` |
| Backend / DGS | **`plm-workspace`** (separate subgraph + backend) |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | **separate `plm-workspace` subgraph** (referenced by product/bom/measurement/… as an entity) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `code/schemas/SPARK_WorkspaceV2.txt` | 321 | the source SDL — 8 queries, 12 mutations, `WorkspaceV2` + ~14 value types, ~10 inputs |
| `code/resolvers/SPARK_WorkspaceV2.txt` | 1,060 ⚠️ | 8 (+2 non-SDL) queries, 10 mutations, ~25 field resolvers; ~310-line partner-action dispatcher |
| `code/services/WorkspaceV2.txt` | 164 | 13 REST methods (CRUD, resources, teams, drop/undrop) |
| **⚠️ Large file** | 1,060 | resolver read in 3 windows (queries+mutations → dispatcher → field resolvers) |

Schema: **`code/schemas/SPARK_WorkspaceV2.txt` (321 lines)** — target schema in [03-schema.graphql](./03-schema.graphql)
translated from it (nullability from the SDL).

## 3. Import Graph
```
SPARK_WorkspaceV2.txt
├── resolvers/SPARK_Product        → Product.Query.getProducts, Product.SPARK_Product.workspaces (cross-subgraph)
├── resolvers/SPARK_UserAttributes → deleteAllUserProfileDataForAPartner (drop cleanup)
├── utils/commonLoaders            → getUserPermissionsJWT, filterResourcesByPartner, getPermissionMapForBulkACLCall, getUnDroppablePartners
├── utils/vmmUtils                 → loadBpsWithType, loadManyIncludeEmptyResponse
├── utils/removePartnerUtils       → getWorkspacePartnersNotRemovable
├── utils/Product/attachmentUtils  → resolveRelationIds, filterAttachmentsOrComponents, getProductOrWorkSpaceAttachments, initialCountsByBp
├── utils/discussionUtils          → getDiscussionsBatch, getDiscussionThreadsBatch
├── services/batchers/getTagsBatched
└── config/businessPartner
WorkspaceServiceV2 extends SparkService; uses postOne/putOne/deleteOne/loadOne/loadListing
```

## 4. Cross-Domain Reference Table (everything is cross-subgraph — workspace is its own DGS)

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| paged V2/V3, claims/discussions/teams/combinations/samples elastic, type-count, packaging attachments, exports | `search` | SearchService (elastic) | federation | 🔴 |
| `getWorkspaceProducts`, `getProducts`, `getPage`, `updateViewToggle`, `deletePartnerWorkspaceStatuses` | `product` | ProductService (plm-product) | federation | 🔴 |
| `getAttachmentsV3` (attachmentsWithMetaData/V3) | `attachment` | AttachmentService | federation | 🔴 |
| `searchByIds` (drop/undrop trees, attachments) | `relationship` | RelationshipService | federation | 🟡 |
| discussions batch/count, drop/undrop partner | `discussion` | DiscussionService | federation | 🟡 |
| `getSamplesByIdsV2`, drop/undrop samples | `sampleV2` | SampleService | federation | 🟡 |
| `getByIds` (combinations) | `combination` | CombinationService | federation | 🟡 |
| `getTags`/`getTagsBatched` (designCycles/tags) | `tag` | TagService | federation | 🟡 |
| `getUserByID*` (created/updated) | `userAttributes` | UserProfileService | federation | 🟡 |
| `loadBpsWithType` (business/dropped partners) | `vmm` | VMM platform | Gateway stitch | 🔵 |
| division/clazz/department | `ig` | Item Groups | Gateway stitch | 🔵 |
| `getBrand` (brands) | `brand` | VMM/Brand | Gateway stitch | 🔵 |
| `deleteFavoritesByBusinessPartner` | `favorite` | UserProfileService | federation | 🔵 |
| `exportWorkspaceExcel` | `exportHub` | ExportHub | federation | 🔵 |
| ACL drop/undrop, capability tokens | `accessControl` | AccessControlService | **context (drop/undrop noted)** | n/a |

## 5. Co-located Siblings
**None** — `workspace` is its **own DGS** (`plm-workspace`). It is **referenced as an entity** by
product/bom/measurement/impression/etc. (their `workspaces` fields resolve `WorkspaceV2` by `id` over the
gateway). All of its outbound calls (above) are cross-subgraph.

## 6. Hot Spots
1. **`workspaceBusinessPartnerActionsV2`** (`:266-577`) — **~310-line dispatcher**, 5 cases (`REMOVE_TEAM`,
   `REMOVE_PARTNER`, `DROP_PARTNER`, `UNDO_DROP_PARTNER`, `DROP_UNDROP_PARTNER`). Orchestrates ACL drop/undrop
   across discussion/sample/claim/attachment + accessControl + user-profile cleanup, with **manual
   compensation** (un-drop on ACL failure). **Several `Promise.all(...).then(...)` blocks are not awaited**
   (fire-and-forget) — latent races; no transactional rollback.
2. **`SPARK_WorkspaceV2.attachmentsWithMetaData`** (`:678-752`, ~75 ln) — relationship tree → attachment v3
   hydration (ACL) → discussions/threads batch → merge → draft filter.
3. **`SPARK_WorkspaceV2.counts`** (`:910-995`, ~85 ln) — search filtered products + product page + discussion
   counts + sample counts + sample-discussion roll-up into the product dashboard.
4. **`attachmentsV3`** (`:753-790`) — relationship → attachment hydration with per-BP counts.
5. **`products`/`productsCount`/`combinations`/`sampleReport`** — call **into product/sample/combination**
   (cross-subgraph); `products` calls `Product.Query.getProducts` directly today.
6. **Schema-drift mutations** — `dropWorkspaceBusinessPartnerV2` / `unDropWorkspaceBusinessPartnerV2` are in
   the SDL but have **no top-level resolver** (handled inside `workspaceBusinessPartnerActionsV2`). Deferred ⏭.
7. **Resolver-only queries** — `searchWorkspaceSuggestions`, `searchWorkspaceProductsSuggestions` exist in the
   resolver but **not** in this SDL (likely belong to the search schema). Out of scope here.
8. **Entity key** — `WorkspaceV2.id: ID!` (resolver derives it from `workspaceHumanId || humanId`). `@key="id"`.

## 7. Operation Lists
**Queries (8):** getWorkspaceV2, getWorkspacesByIdsV2, getWorkspacesPagedV2, getWorkspacesPagedV3,
findWorkspaceProductAndSampleIds, findWorkspaceClaims, getWorkspaceTypeCount, getWorkspacePackagingAttachments.
**Mutations (10 impl + 2 schema-drift):** createWorkspaceV2, updateWorkspaceV2, changeWorkspace,
addResourcesToWorkspaceV2, removeWorkspaceResourcesV2, addTeamsToWorkspaceV3, workspaceBusinessPartnerActionsV2,
exportWorkspace, exportWorkspaceExcel, exportPackagingFiles. **Deferred ⏭:** dropWorkspaceBusinessPartnerV2,
unDropWorkspaceBusinessPartnerV2.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 8 |
| Mutations | 10 (+2 schema-drift) |
| Object types | ~15 (`WorkspaceV2`, counts/dashboard/report/department/paged/export…) |
| Field resolvers | ~25 (across `WorkspaceV2`, `WorkspaceDepartmentV2`, paged types) |
| Service methods | 13 |
| Cross-domain loader keys | 14 (all cross-subgraph) |
| EXT calls | 3 🔴 (search, product, attachment) · 6 🟡 · 4 🔵 · accessControl context |
| Interfaces / unions | 0 |
| Large files | 1 ⚠️ (resolver 1,060) |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `workspace` · **Files:** 3 (1,545 lines: schema 321 + resolver 1,060 + service 164).
