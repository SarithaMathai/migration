# Phase 1: Schema Inventory — Watchlist

> **Domain:** `watchlist`
> **Target DGS:** `WatchlistService` → `plm-product` (co-located)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `code/schemas/SPARK_Watchlist.txt` (98-line SDL) + `code/resolvers/product/SPARK_Watchlist.txt` + `code/services/product/Watchlist.txt`
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

No `context.js` in the snapshot. The endpoint is built in the service constructor
(`services/product/Watchlist.txt:10`):

```js
this.endpoint = `${endpoint}/enterprise_product_development_products/watchlist/v1`
```

> **Co-location correction:** because the service uses the shared
> `enterprise_product_development_products/...` base (like bom/measurement/packaging) and the resolver lives
> under `resolvers/product/`, watchlist is **co-located in the `plm-product` monorepo** (also listed in
> [reference-federation-patterns.md §0](../scripts/reference-federation-patterns.md)). The product analysis's
> `SPARK-PROD-F08` currently labels `watchlists` as a *separate-subgraph* federation contribution — that is
> a mislabel; it should be **internal** (CAT-2), like `bom`'s F06 and `measurement`'s F04. See §5.

| Setting | Value |
|---|---|
| Loader key | `watchlist` |
| Service class | `WatchlistService` |
| Backend base | `https://spark-product.dev.target.com` (repo `spark-product`) |
| Base path | `${endpoint}/enterprise_product_development_products/watchlist/v1` |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | `plm-product` (co-located — internal to the product family) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `code/schemas/SPARK_Watchlist.txt` | 98 | the source SDL — 4 queries, 3 mutations, `Watchlist`/inspection/partner types, inputs |
| `code/resolvers/product/SPARK_Watchlist.txt` | 129 | 4 queries, 3 mutations, 3 type blocks (13 field resolvers) |
| `code/services/product/Watchlist.txt` | 79 | 7 REST methods (`watchlist/v1`) — 2 unused (versions) |
| **Total** | **306** | small domain — no chunked reading |

Schema: **`code/schemas/SPARK_Watchlist.txt` (98 lines)** — target schema in [03-schema.graphql](./03-schema.graphql)
translated from it (nullability from the SDL).

## 3. Import Graph
```
SPARK_Watchlist.txt
├── utils/commonLoaders            → getUserPermissionsJWT (ACL — context only)
├── resolvers/SPARK_WorkspaceV2    → getWorkspacesByIdsV2 (workspace enrichment)
└── resolvers/SPARK_UserGroup      → getUserGroups, updateUserGroup (participants)
WatchlistService.txt uses postOne, putOne, loadListing, loadOne, convertFunctions
```

## 4. Cross-Domain Reference Table

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `getWatchlistByFilter` (searchWatchlist), `attachments` | `search` | SearchService (elastic) | federation | 🔴 |
| `updateWatchlistEntries` (archive), `cloneFilesForWatchlist` | `attachment` | AttachmentService | federation | 🔴 |
| `getWatchlistByFilter` (getWorkspaceProducts), `product` | `product` | ProductService (same DGS) | **internal** | — |
| `createWatchlistEntries`/`updateWatchlistEntries` userGroup, `participantDetails` | `userGroup` / user-profile | UserProfileService | federation | 🔵 |
| `createdBy`/`updatedBy` | `userAttributes` | UserProfileService | federation | 🟡 |
| `workspaces` | `workspaceV2` | WorkspaceService | federation | 🟡 |
| `WatchlistPartner.partnerName` | `vmm` | VMM platform | Gateway stitch | 🔵 |
| all reads/writes | `accessControl` (getUserPermissionsJWT) | AccessControlService | **context only — ACL ignored** | n/a |

## 5. Co-located Siblings
`product`, `bom`, `measurement`, `packaging`, `productDetails`, `impression`, `fileLibrary` — share `plm-product`.
- `Product.watchlists` and the TechPack `ResourcesCount.watchlists` count resolve **internally** (same
  subgraph), **not** cross-subgraph. **Product's `SPARK-PROD-F08` should be reclassified** from CAT-4
  federation (`blocked_by: watchlist`) to **CAT-2 internal** (`blocked_by: none`), matching `SPARK-BOM-F06`
  and `SPARK-MEAS-F04`.

## 6. Hot Spots
1. **`getWatchlistByFilter`** (`:16-24`) — **4-step read**: (internal) `product.getWorkspaceProducts` → product
   ids → (🔴 search) `searchWatchlist` (`parentId:(... OR ...) AND workspaceContext: AND statusId:501`) →
   watchlist ids → (ACL) token → (own) `getWatchlistByIds`.
2. **`updateWatchlistEntries`** (`:44-68`) — **multi-step write**: per-entry user-group upsert, then (own)
   `updateWatchlistEntries`, then (🔴 attachment) bulk-archive `removedAttachmentIds`. **Latent bug:** the
   per-entry `watchlistEntries.map(async …)` is **not awaited** (no `Promise.all`/`await`) before the watchlist
   update — the user-group upserts race with the update. Fix on port.
3. **`createWatchlistEntries`** (`:28-42`) — per-entry `Promise.all`: (own) create + (🔵 user-group)
   `addUserGroup`; **throws** on `validationErrors`/`message` for either.
4. **`cloneFilesForWatchlist`** (`:70-84`) — per-attachment `Promise.all` (🔴 attachment) `cloneAttachmentV3`,
   stamping `parentResource`.
5. **Flattening field resolvers** — `statusId`/`statusName` from `status.{code,description}`;
   `reasonIds`/`reasons` from `reasons[].{code,description}`; `WatchlistInspection.actionId`/`action` from
   `action.{code,description}` (all in the SDL — computed, not record-only).
6. **Entity key** — `SPARK_Watchlist` uses `humanId` (`humanId: String!`, no `id`). `@key` = `humanId`.
7. **2 unused service methods** — `getWatchlistVersionsById`, `getWatchlistVersion`. Confirm before dropping.

## 7. Operation Lists
**Queries (4):** getWatchlistReasons, getWatchlistInspectionActions, getWatchlistByIds, getWatchlistByFilter.
**Mutations (3):** createWatchlistEntries, updateWatchlistEntries, cloneFilesForWatchlist.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 4 |
| Mutations | 3 |
| Object types | 4 (`Watchlist`, `WatchlistInspection`, `WatchlistInspectionAction`, `WatchlistPartner`) |
| Field resolvers | 13 (10 `Watchlist`, 2 inspection, 1 partner) |
| Service methods | 7 (5 used + 2 unused) |
| Cross-domain loader keys | 6 (+ accessControl context-only + product internal) |
| EXT calls | 2 🔴 · 2 🟡 · 2 🔵 |
| Interfaces / unions | 0 |
| Large files | 0 |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `watchlist` · **Files:** 3 (306 lines: schema 98 + resolver 129 + service 79).
