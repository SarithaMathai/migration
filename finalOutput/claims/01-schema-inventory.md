# Phase 1: Schema Inventory — Claims

> **Domain:** `claims`
> **Target DGS:** `ClaimService` → **separate `claims` subgraph** (repo `spark-claims`) — NOT the plm-product monorepo
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `code/schemas/SPARK_Claims.txt` (157-line SDL) + `code/resolvers/product/SPARK_Claims.txt` + `code/services/Claim.txt`
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

There is no `context.js` in the snapshot. Unlike the product-family services, `ClaimService extends
SparkService` and takes the **base URL directly** (`this.endpoint = endpoint`, `Claim.txt:13`) — there is
**no `/enterprise_product_development_products/...` path suffix** in this file; the claim service base is
injected by the loader registry. Treat the base as the **`spark-claims`** backend.

| Setting | Value |
|---|---|
| Loader key | `claim` |
| Service class | `ClaimService extends SparkService` |
| Backend base | `spark-claims` service base (injected; no path suffix in the file) |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | **separate `claims` subgraph** (contributes to `Product` + TechPack via federation) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `code/schemas/SPARK_Claims.txt` | 157 | the source SDL — 7 queries, 6 mutations, `Claims`/details/substantiate/export types, inputs |
| `code/resolvers/product/SPARK_Claims.txt` | 164 | 7 queries, 6 mutations, 4 type blocks (17 field resolvers) |
| `code/services/Claim.txt` | 151 | 13 REST methods — 2 unused (versions) |
| **Total** | **472** | small/mid domain — no chunked reading |

Schema: **`code/schemas/SPARK_Claims.txt` (157 lines)** — target schema in [03-schema.graphql](./03-schema.graphql)
translated from it (nullability from the SDL).

## 3. Import Graph
```
SPARK_Claims.txt
├── utils/commonLoaders            → getUserPermissionsJWT, getUserPermissionsJWTByProxy (ACL — context only)
├── utils/workspaceAssociationHelper → workspaceAssociationHelper, ValidWorkspaceAssociationTypes
├── utils/Product/userGroupUtils   → getUserGroup (participants)
└── resolvers/SPARK_WorkspaceV2    → getWorkspacesByIdsV2 (workspace enrichment)
ClaimService.txt extends SparkService; uses postOne, putOne, loadListing, loadOne, convertFunctions, qs
```

## 4. Cross-Domain Reference Table

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `getClaimsElastic`, `ParentDetails.otherClaimBps`/`systemTeams` | `search` | SearchService (elastic) | federation | 🔴 |
| `product`, `parentDetails` | `product` | ProductService (**separate subgraph**) | federation | 🟡 |
| `access`, `currentUserPermissions` | `accessControl` | AccessControlService | **context only — ACL ignored** | n/a |
| `createdBy`/`updatedBy`/`substantiatedBy` | `userAttributes` | UserProfileService | federation | 🟡 |
| `workspaces` | `workspaceV2` | WorkspaceService | federation | 🟡 |
| `businessPartner`, `designPartner` | `vmm` | VMM platform | Gateway stitch | 🔵 |
| `participantDetails` | `userGroup` / user-profile | UserProfileService | federation | 🔵 |
| `getClaims`/`getClaimByIds`/`createClaim`/… | `claim` | ClaimService (own) | **owned** | — |

## 5. Co-located Siblings
**None in this subgraph** — `claims` is its **own DGS**. Its references to `Product`, `search`, `workspace`,
`user-profile`, `VMM` are **cross-subgraph** (true federation / gateway stitch). It **contributes** the
`Product.claims` field and the TechPack `ResourcesCount.claims` count back to the `plm-product` subgraph.

## 6. Hot Spots
1. **`updateClaim`** (`:38-52`) — **multi-step + proxy ACL**: `getUserPermissionsJWTByProxy({id:humanId,
   proxyIds:[parentId], basePermissions:true})`, then optional `workspaceAssociationHelper(CLAIM, …)`,
   then `PUT {base}/{humanId}`, **throw on `validationErrors`/`message`**. No rollback.
2. **`createClaim`** (`:31-37`) — throw on `validationErrors`/`message` (preserve).
3. **`bulkUpdateClaim`** (`:53-63`) — unusual error contract: `isArray(result)` → ok; `status_code>400` →
   throw; else throw "unhandled". **Latent bug:** the service `bulkUpdateClaim` uses `deepToSnakeCase` on the
   **response** transform (should be camelCase) — verify on port.
4. **`businessPartner`** (`:98-113`) — 3-way fallback: `partnerId` → else `0` if no `dpPartnerId` → else
   `dpPartnerId`; `0` returns `{bpId:0, bpName:'Target'}`. **Preserve exactly.**
5. **`ParentDetails.systemTeams`** (`:142-150`) — builds an elastic team query from the product's BPs
   (`businessPartner.partnerId:` OR-joined); empty BPs → `{content:[]}`.
6. **Entity key** — `SPARK_Claims` has **`humanId`, no `id`**; the resolver keys everything on `humanId`.
   The federation `@key` is `humanId`.
7. **2 unused service methods** — `getClaimVersionsById`, `getClaimVersion`. Confirm before dropping.

## 7. Operation Lists
**Queries (7):** getClaims, getClaimByIds, searchGuestFacing, getCommunicationChannels, getAllClaimsAbout,
getClaimsElastic, getClaimExports.
**Mutations (6):** createClaim, updateClaim, bulkUpdateClaim, requestClaimExport, lockClaim, unlockClaim.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 7 |
| Mutations | 6 |
| Object types | 8 (`Claims`, `ClaimDetails`, `ParentDetails`, `ClaimSubstantiate`, `ClaimPackagingCopy`, `ClaimExport`, `Guest_Facing`, `CommunicationChannel`) |
| Field resolvers | 17 (11 on `Claims`, 3 `ParentDetails`, 1 substantiate, 1 claimDetails) |
| Service methods | 13 (11 used + 2 unused) |
| Cross-domain loader keys | 6 (+ accessControl context-only) |
| EXT calls | 1 🔴 · 3 🟡 · 2 🔵 |
| Interfaces / unions | 0 |
| Large files | 0 |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `claims` · **Files:** 3 (472 lines: schema 157 + resolver 164 + service 151).
