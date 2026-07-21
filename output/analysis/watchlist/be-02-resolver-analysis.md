# Phase 2: Resolver Dependency Analysis — Watchlist

> **Domain:** `watchlist` · **Target DGS:** `WatchlistService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_Watchlist.graphqls` (SDL), `resolvers/product/SPARK_Watchlist.js`, `services/product/Watchlist.js`
> **Depends on:** [be-01-schema-inventory.md](./be-01-schema-inventory.md) · **Mode:** Full

Implementation spec. ACL/JWT usage is **context-only** (ignored in impl). Base path `watchlist/v1`.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 4 |
| Mutation resolvers | 3 |
| Field resolvers | 13 (3 type blocks) |
| Service methods | 7 (2 unused) |
| EXT loaders | 6 (2 🔴 · 2 🟡 · 2 🔵) + accessControl context-only + product internal |
| High complexity | 1 (`updateWatchlistEntries` multi-step) |

---

## Query Resolvers (4)

| # | Query | Complexity | Pseudo-logic (REST + EXT) |
|---|-------|-----------|---------------------------|
| Q1 | `getWatchlistByIds(ids): [Watchlist]` | Low | (ACL context) token for `ids` → (own) `getWatchlistByIds(jwt).load(ids)` `GET watchlist/v1?watchlistIds={csv}` → camelCase. |
| Q2 | `getWatchlistReasons: [CodeDescription]` | Low · cacheable | (own) `GET watchlist/v1/watchlist_reasons`. |
| Q3 | `getWatchlistInspectionActions: [WatchlistInspectionAction]` | Low · cacheable | (own) `GET watchlist/v1/watchlist_inspection_action_types`. |
| Q4 | `getWatchlistByFilter(q, filter, workspaceId, page, size): [Watchlist]` | Medium | **4-step:** (internal) `product.getWorkspaceProducts({q,filter,workspaceId,page,size})` → product `humanId`s → (🔴 search) `searchWatchlist({ q:"parentId:(... OR ...) AND workspaceContext: {workspaceId} AND statusId: 501", page, size })` → watchlist ids → (ACL) token → (own) `getWatchlistByIds`. |

## Mutation Resolvers (3)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `createWatchlistEntries(watchlistEntries): [Watchlist]` | Medium | `Promise.all(entries.map(w => { (own) createWatchlistEntries([w]); throw on validationErrors/message; then (🔵 user-group) addUserGroup({resourceId:humanId, participantDetails, relatedResources}); throw on error }))`, flatten. |
| M2 | `updateWatchlistEntries(watchlistEntries): [Watchlist]` | **High** | **multi-step:** 1) **per-entry (NOT awaited — bug):** `getUserGroups([humanId])`; if existing participants → `updateUserGroup`, else `addUserGroup` (throw on error); 2) (own) `updateWatchlistEntries(entries)` (throw on error); 3) collect `removedAttachmentIds` → (ACL) token → (🔴 attachment) `archiveAttachmentBulkV3`. **No rollback.** |
| M3 | `cloneFilesForWatchlist(attachmentIds, cloneReference): [Attachment]` | Medium | (ACL) token → `Promise.all(attachmentIds.map((id,i) => (🔴 attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id)))`, stamp `parentResource=id`, flatten. |

## Field Resolvers (13)

**`Watchlist` (10):**
- `statusId` / `statusName` (computed) — `status.code` / `status.description`.
- `reasonIds` / `reasons` (computed) — `map(reasons,'code')` / `map(reasons,'description')`.
- `attachments` (🔴 search) — `searchAttachmentsByRelatedResource(humanId)`.
- `createdBy` / `updatedBy` (🟡 user-profile) — `getUserByIDOrNullIfNotFound`.
- `workspaces` (🟡 workspaceV2) — `getWorkspacesByIdsV2(workspaceContext)` or null.
- `participantDetails` (🔵 user-group) — `getUserGroups([humanId])[0].participantDetails` or null.
- `product` (internal) — only if `parentId` starts `'PID'` → `product.getByID(parentId)`, else null.

**`WatchlistInspection` (2):** `actionId` (computed `action.code`), `action` (computed `action.description`).
**`WatchlistPartner` (1):** `partnerName` (🔵 vmm) — `vmm.getByID(partnerId).bpName` or null/`''`.

## Service Classes
- `WatchlistService` base `watchlist/v1`.
- Methods: `getWatchlistReasons` (GET `/watchlist_reasons`), `getWatchlistInspectionActions` (GET `/watchlist_inspection_action_types`), `getWatchlistByIds` (GET `?watchlistIds=`), `createWatchlistEntries` (POST), `updateWatchlistEntries` (PUT).
**Unused:** `getWatchlistVersionsById`, `getWatchlistVersion`.

## EXT Service Call Inventory (summary)
- 6 EXT keys — **2 🔴** (search, attachment) · **2 🟡** (userAttributes, workspaceV2) · **2 🔵** (userGroup/ user-profile, vmm) · accessControl **context-only**.
- **Internal (same DGS):** product, watchlist (own).

## Key Findings
- **Highest risk:** `updateWatchlistEntries` (M2) — multi-step (user-group upsert + body + attachment archive);
  **latent bug:** the per-entry user-group `.map(async …)` is **not awaited** before the watchlist update
  (race). Fix on port (await/`Promise.all`).
- **Multi-step read:** `getWatchlistByFilter` (Q4) chains product → search → ACL → watchlist.
- **Quick wins:** `getWatchlistByIds`, the 2 cacheable master-data reads, the computed flatteners.
- **Co-located:** `Product.watchlists` + TechPack `ResourcesCount.watchlists` are **internal** (see 01 §5).
- **Unused service methods:** the two version reads — confirm before dropping.

---
**Phase Completed:** Phase 2 · **Domain:** `watchlist` · **EXT:** 6 keys (2🔴 · 2🟡 · 2🔵).
