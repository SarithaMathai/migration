# Phase 2: Resolver Dependency Analysis — Workspace

> **Domain:** `workspace` · **Target DGS:** `WorkspaceServiceV2` → separate `plm-workspace` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `code/schemas/SPARK_WorkspaceV2.txt` (SDL), `code/resolvers/SPARK_WorkspaceV2.txt` (1,060), `code/services/WorkspaceV2.txt`
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full (large-file protocol)

Implementation spec. ACL/JWT usage is **context-only** (ignored in impl). `workspace` is its **own subgraph**.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 8 |
| Mutation resolvers | 10 (+2 schema-drift) |
| Field resolvers | ~25 |
| Service methods | 13 |
| EXT loaders | 14 (3 🔴 · 6 🟡 · 4 🔵) + accessControl context |
| Very High | 3 (partner-action dispatcher, attachmentsWithMetaData, counts) |

---

## Query Resolvers (8)

| # | Query | Complexity | Pseudo-logic (REST + EXT) |
|---|-------|-----------|---------------------------|
| Q1 | `getWorkspaceV2(id, metric): WorkspaceV2` | Low | (own) `getWorkspaceByIdV2.load(id)` `GET {base}?ids={id}` (ACL token via loader). |
| Q2 | `getWorkspacesByIdsV2(ids): [WorkspaceV2]` | Low | (ACL) token → (own) `getWorkspacesByIdsV2(jwt).load({ids})`. |
| Q3 | `getWorkspacesPagedV2(productIds, description, brandIds, departmentIds, page, size)` | Medium | (🔴 search) `getWorkspacesPagedV2` (array params CSV-joined; `omitBy` empties). |
| Q4 | `getWorkspacesPagedV3(description, brandId, departmentId, designCycle, workspaceType, page, size, q, designPartnerIds)` | Medium | (🔴 search) `getWorkspacesPagedV3` (CSV-join except `q`/`designPartnerIds`). |
| Q5 | `findWorkspaceProductAndSampleIds(workspaceId, q, filter): WorkspaceContentResult` | Medium | (🔴 product) `getWorkspaceProducts({workspaceId, filter, q, page:0, size:10000})` → map `{id:humanId, sampleIds:[sample.humanId]}`. |
| Q6 | `findWorkspaceClaims(workspaceId, q, filter): [Claims]` | Low | (🔴 search) `getClaimsElastic({ q:"workspaceContext:{workspaceId}", page:0, size:10000 })` → `.content`. |
| Q7 | `getWorkspaceTypeCount: WorkspaceTypeCount` | Low | (🔴 search) `getWorkspaceTypeCount({})`. |
| Q8 | `getWorkspacePackagingAttachments(workspaceId, bpId): [SearchAttachment]` | Medium | env `WORKSPACE_PACKAGING_TAG_ID` (throws if unset) → (🔴 search) `searchAttachments({ q:"tags:{tag}[ AND security.bps:{bpId}]", relatedIds:[workspaceId], size:500, sort:createdAt,desc })` → `.content`. |

> Not in this SDL (resolver-only — likely the search schema): `searchWorkspaceSuggestions`,
> `searchWorkspaceProductsSuggestions`. Out of scope for this domain.

## Mutation Resolvers (10 impl + 2 schema-drift)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `createWorkspaceV2(workspace, validateUnique): WorkspaceV2` | Medium | default `workspaceType=103`; (own) `createWorkspaceV2.load(ws, {validateUnique})` `POST {base}`. **Throw `GraphQLError('Workspace already exists')`** if response message starts with the dup text. |
| M2 | `updateWorkspaceV2(workspace, validateUnique): WorkspaceV2` | Medium | (ACL) token for `workspace.id`; default type 103; (own) `PUT {base}/{id}?validateUnique=` → same dup-check throw. |
| M3 | `changeWorkspace(productId, oldWorkspaceId, newWorkspaceId, teams, removeWorkspaceOnly): WorkspaceV2` | Medium | (ACL) token for `Attr-{newWs}-resources` → (own) `PUT {base}/{newWs}/change_resource`. **Throw on validationErrors/message.** |
| M4 | `addResourcesToWorkspaceV2(resourceList, workspaceId, designCycle, setDates): WorkspaceV2` | Medium | (ACL) token; **if single product** → (🔴 product) read `Product.workspaces` + `updateViewToggle` (init workspace attrs, firstWorkspace branch); (own) `POST {base}/{workspaceId}/resources/bulk`. |
| M5 | `removeWorkspaceResourcesV2(workspaceId, resourceType, resourceIds): WorkspaceV2` | Medium | (ACL) token; **if single product** → (🔴 product) `deletePartnerWorkspaceStatuses` cleanup; (own) `DELETE {base}/{workspaceId}/resources/delete/bulk?...`. |
| M6 | `addTeamsToWorkspaceV3(workspaceId, teamInput): WorkspaceV2` | Low | (ACL) token → (own) `POST {base}/{workspaceId}/teams/bulk`. |
| M7 | `workspaceBusinessPartnerActionsV2(actionType, values): WorkspaceV2` | **Very High** | ~310-line dispatcher — see Helper below. |
| M8 | `exportWorkspace(workspaceId, exportType, onlyIncludeAttachmentIds, includeOnlyPrimaryThumbnails, q, filter): WorkspaceExportReceipt` | Low | (🔴 search) `requestBulkAttachmentExport`. |
| M9 | `exportWorkspaceExcel(workspaceExportOptions): WorkspaceExportReceipt` | Low | (🔵 exportHub) `exportWorkspaceExcel`. |
| M10 | `exportPackagingFiles(workspaceId, workspaceDescription, exportContext, exportType, q, filter): WorkspaceExportReceipt` | Low | (🔴 search) `requestPackagingExport`. |
| ⏭ | `dropWorkspaceBusinessPartnerV2` / `unDropWorkspaceBusinessPartnerV2` | — | **schema-drift** — declared in SDL, no top-level resolver; traffic routes through M7 (`DROP_PARTNER`/`UNDO_DROP_PARTNER`). |

## Helper · `workspaceBusinessPartnerActionsV2` dispatcher — Very High
5 cases on `actionType`:
- **`REMOVE_TEAM`** — (ACL) → (own) `removeTeamsFromWorkspaceV3`.
- **`REMOVE_PARTNER`** — optional team removal → (🔵 favorite) `deleteFavoritesByBusinessPartner` → (own) `removeWorkspaceBusinessPartnerV2`.
- **`DROP_PARTNER`** — (🟡 relationship) `searchByIds` tree → partition discussions/attachments/threads →
  `filterResourcesByPartner` (ACL) → `Promise.all([ (own) dropWorkspace, (🟡 discussion) dropPartnerFromDiscussionIds ])`
  → on success (🟡 accessControl) `dropPartnerFromResources` + (user-profile) `deleteAllUserProfileDataForAPartner`;
  **on ACL failure → manual un-drop compensation**. ⚠ the outer `Promise.all().then()` is **not awaited**.
- **`UNDO_DROP_PARTNER`** — mirror of DROP with `unDrop*`; same non-awaited compensation.
- **`DROP_UNDROP_PARTNER`** — unified path; relationship tree incl. sample+claim; optional
  (🟡 sampleV2) drop/undrop (skipped for DESIGN_PARTNER); `await Promise.all([dropUndropWorkspace, sampleCall])`
  then ACL drop/undrop + user-profile cleanup.
**EXT:** relationship 🟡, discussion 🟡, sampleV2 🟡, accessControl (context+drop), favorite 🔵, user-profile.
**Findings:** no transactional rollback; **fire-and-forget `.then()`** in DROP/UNDO_DROP (races); design-partner
sample-skip branch. Needs a failure strategy + await fixes on the port.

## Field Resolvers (~25, on `SPARK_WorkspaceV2` unless noted)
- **Very High:** `attachmentsWithMetaData` (🔴 relationship+attachment + 🟡 discussion + ACL, ~75 ln),
  `counts` (🔴 search+product + 🟡 discussion + sample roll-up, ~85 ln).
- **High:** `attachmentsV3` (🔴 relationship+attachment, per-BP counts).
- **Cross-subgraph (product/sample/combination):** `products` (calls `Product.Query.getProducts`),
  `productsCount` (🔴 product `getPage`), `combinations` (🔴 search + 🟡 combination), `sampleReport`
  (🔴 search + 🟡 sampleV2).
- **Partners:** `businessPartners`/`droppedPartners` (🔵 vmm), `notRemovablePartnerIds`/`unDroppablePartners` (util+ACL).
- **Hierarchy/tags:** `divisions`/`clazzes` (🔵 ig), `brands` (🔵 brand), `designCycles`/`tags` (🟡 tag);
  `WorkspaceDepartmentV2.node`/`clazzes` (🔵 ig).
- **Users/computed:** `createdBy`/`updatedBy` (🟡 user-profile), `id`/`status`/`workspaceTypeElastic`/
  `createdAt`/`updatedAt` (computed), `discussionsV2`/`teams` (🔴 search), `WorkspacesPagedV2/V3` paging (computed).

## Service Classes
`WorkspaceServiceV2` base = `plm-workspace`. Methods: `getWorkspaceByIdV2` (GET `?ids=`), `getWorkspacesByIdsV2`,
`createWorkspaceV2` (POST), `updateWorkspaceV2` (PUT `/{id}?validateUnique=`), `changeWorkspace`
(PUT `/{newWs}/change_resource`), `addResourcesToWorkspaceV2` (POST `/{id}/resources/bulk`),
`removeWorkspaceResourcesV2` (DELETE `/{id}/resources/delete/bulk`), `addTeamsToWorkspaceV3`/
`removeTeamsFromWorkspaceV3` (POST `/{id}/teams[/remove]/bulk`), `removeWorkspaceBusinessPartnerV2`
(DELETE `/{id}/partner/{pid}`), `dropWorkspaceBusinessPartnerV2`/`unDropWorkspaceBusinessPartnerV2`
(POST `/{id}/{drop|undrop}-partner/{pid}`), `dropUndropWorkspaceBusinessPartnerV2` (POST `/{id}/drop-undrop-partner`).

## EXT Service Call Inventory (summary)
14 keys — **3 🔴** (search, product, attachment) · **6 🟡** (relationship, discussion, sampleV2, combination,
tag, userAttributes) · **4 🔵** (vmm, ig, brand/exportHub/favorite) · accessControl **context (+drop/undrop)**.
`workspaceV2` is the owned service.

## Key Findings
- **Highest risk:** `workspaceBusinessPartnerActionsV2` (M7) drop/undrop orchestration — no rollback,
  fire-and-forget `.then()` races; `attachmentsWithMetaData` + `counts` (perf-heavy).
- **Cross-subgraph coupling:** `products`/`addResourcesToWorkspaceV2` call into **product** directly today —
  in federation these become entity references / a thin product client.
- **Schema-drift:** `dropWorkspaceBusinessPartnerV2`/`unDropWorkspaceBusinessPartnerV2` (deferred).
- **Quick wins:** the simple reads (Q1/Q2/Q6/Q7), `addTeamsToWorkspaceV3`, the 3 exports.

---
**Phase Completed:** Phase 2 · **Domain:** `workspace` · **EXT:** 14 keys (3🔴 · 6🟡 · 4🔵).
