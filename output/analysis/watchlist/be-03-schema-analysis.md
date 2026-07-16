# Phase 3: Federation Schema Analysis — Watchlist

> **Domain:** `watchlist` · **Target DGS:** `WatchlistService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [be-03-schema.graphql](./be-03-schema.graphql) · **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 7 🔜 | 0 ⏭ — 7 operations**

The target schema is translated from the source SDL (`schemas/SPARK_Watchlist.graphqls`), verified against
the resolver. **Watchlist is co-located in the `plm-product` monorepo** (see §3).

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `Watchlist` (key `humanId`) |
| Owned value types | 3 | `WatchlistInspection`, `WatchlistInspectionAction`, `WatchlistPartner` |
| `@shareable` | 1 | `CodeDescription` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — sibling DGS | 5 | `Attachment`, `SearchAttachment`, `WorkspaceV2`, `UserProfileAttributes`, `UserGroup_Participants` |
| Internal (same subgraph) | 1 | `Product` |
| Inputs | 4 | `WatchlistInput`, `WatchlistPartnerInput`, `WatchlistInspectionInput`, `WatchlistAttachmentCloneRef` |

No interfaces / unions — no `@DgsTypeResolver` needed.

## 2. Client Contract Verification
4 queries + 3 mutations preserved (`0 ✅ | 7 🔜 | 0 ⏭`). `SPARK_` prefixes dropped; `VMM_` kept.
**Entity key:** `Watchlist` is keyed on **`humanId`** (`humanId: String!`; the SDL exposes no `id`).
**Computed fields:** `statusId`/`statusName`/`reasonIds`/`reasons` and `WatchlistInspection.actionId`/`action`
are flattened from `{code, description}` objects on the record (declared in the SDL — keep as field resolvers).

## 3. Federation Boundaries

> **Monorepo:** `watchlist` is the **same `plm-product` subgraph** as product/bom/measurement/packaging/
> productDetails. References among them are **internal types**, not federation. See
> [reference-federation-patterns.md §0](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

- **Owns** `Watchlist` + the 3 value types.
- **Internal (same subgraph — NOT federation):** `Product` (`product` field + `getWatchlistByFilter`'s
  `getWorkspaceProducts`).
- **External (true federation stubs):** `attachment` (search-by-related + clone + archive), `search`
  (elastic watchlist), `workspace`, `user-profile` (`createdBy`/`updatedBy`), `user-group` (participants);
  **gateway stitch:** `VMM` (`WatchlistPartner.partnerName`).
- **Contributes back** to `Product` → **internal** field resolvers (co-located, Phase F): `Product.watchlists`
  and the TechPack `ResourcesCount.watchlists` count.

> **⚠ Cross-domain correction:** the product analysis's `PRODUCT-BE-F-08` (`ResourcesCount.watchlists`)
> currently labels watchlist as a **separate-subgraph** federation contribution (`category: CAT-4`,
> `blocked_by: watchlist`). Watchlist is **co-located**, so F-08 is **internal** (`CAT-2`, `blocked_by: none`),
> exactly like `BOM-BE-F-06` and `MST-BE-F-04`. This has been corrected in product's artifacts.

## 4. Migration Approach  *(Confluence approach page)*

Watchlist is a **small, mid-low-risk** co-located domain — no polymorphism.

1. **Phase A:** schema + `WatchlistService` port (base `watchlist/v1`). Preserve the create/update
   throw-on-error contracts.
2. **Phase B:** the 3 simple reads (`getWatchlistByIds` + 2 cacheable master-data lists).
3. **Phase C:** `getWatchlistByFilter` — the 4-step read (product → search → ACL → watchlist).
4. **Phase D:** `createWatchlistEntries` (create + user-group per entry) and `cloneFilesForWatchlist`
   (🔴 attachment).
5. **Phase E:** `updateWatchlistEntries` — the **multi-step** write (user-group upsert → body → attachment
   archive). **Fix the un-awaited user-group map** (race) and choose a failure strategy.
6. **Phase F:** `Product.watchlists` + `ResourcesCount.watchlists` — **internal** field resolvers
   (co-located), not gateway federation.
7. **Phase G:** field resolvers (computed flatteners, users/workspace/participants/partner, attachments,
   product) + the test/parity harness.

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `updateWatchlistEntries` un-awaited user-group map (race) (E-01) | Medium | Medium-High | Await/`Promise.all`; choose failure strategy | Backend Eng + Tech Lead |
| `updateWatchlistEntries` multi-step partial failure (E-01) | Medium | Medium | Saga / compensation — decision | Tech Lead + PO |
| `getWatchlistByFilter` 4-step chain (perf) (C-01) | Low | Medium | Cache product lookup; paginate | Backend Eng |
| Product `PRODUCT-BE-F-08` mislabel (separate vs internal) | — | Low | Reclassified to internal (CAT-2) | Product Owner |
| Sibling refs (attachment/search/workspace/user-profile/VMM) need gateway stubs | Medium | Low | Standard federation sequencing | Platform |

## 6. ACL Handling
Reads/writes curry capability tokens via `getUserPermissionsJWT` (resource-scoped). **ACL is ignored in the
DGS implementation** (no ACL story) — context only.

## 7. Open Questions
1. `updateWatchlistEntries` — confirm the user-group upserts should complete before the watchlist update
   (current code does not await them); failure strategy?
2. Are the 2 unused version service methods needed cross-domain?

---
**Phase Completed:** Phase 3 · **Domain:** `watchlist`.
