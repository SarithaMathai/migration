# Phase 2: Resolver Dependency Analysis — Claims

> **Domain:** `claims` · **Target DGS:** `ClaimService` → separate `claims` subgraph (repo `spark-claims`)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_Claims.graphqls` (SDL), `resolvers/product/SPARK_Claims.js`, `services/Claim.js`
> **Depends on:** [be-01-schema-inventory.md](./be-01-schema-inventory.md) · **Mode:** Full

Implementation spec. ACL/JWT usage is **context-only** (ignored in impl). `claims` is its **own subgraph**.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 7 |
| Mutation resolvers | 6 |
| Field resolvers | 17 (4 type blocks) |
| Service methods | 13 (2 unused) |
| EXT loaders | 6 (1 🔴 · 3 🟡 · 2 🔵) + accessControl context-only |
| High complexity | 2 (`updateClaim`, `ParentDetails.systemTeams`/group) |

---

## Query Resolvers (7)

| # | Query | Complexity | Pseudo-logic (REST + EXT) |
|---|-------|-----------|---------------------------|
| Q1 | `getClaims(parentHumanId, claimHumanIds, partnerIds): [Claims]` | Low | (own) `claim.getClaims.load({parentHumanId, claimHumanIds, partnerIds})` `GET {base}` (filtered) → camelCase. No ACL token. |
| Q2 | `getClaimByIds(claimHumanIds): [Claims]` | Low | (ACL context) token for `claimHumanIds` → `GET {base}/search?claimIds={csv}` → camelCase. |
| Q3 | `getCommunicationChannels: [CommunicationChannel]` | Low · cacheable | (own) `GET {base}/communication-channels`. |
| Q4 | `getAllClaimsAbout: [CodeDescription]` | Low · cacheable | (own) `GET {base}/claims-about`. |
| Q5 | `getClaimExports: [ClaimExport]` | Low | (own) `GET {base}/export`. |
| Q6 | `searchGuestFacing(queryParam): [Guest_Facing]` | Medium | (own) `GET {base}/search/guest_facing_claim?{qs(queryParam)}`. |
| Q7 | `getClaimsElastic(parentHumanId): [Claims]` | Medium | (🔴 search) `search.getClaimsElastic.load({ q:"parentId: {parentHumanId}" })`. |

## Mutation Resolvers (6)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `createClaim(sparkClaim): [Claims]` | Medium | (own) `claim.create(sparkClaim)` `POST {base}` (snake_case). **If `validationErrors`/`message` → throw.** |
| M2 | `updateClaim(sparkClaim): Claims` | **High** | **proxy ACL + multi-step:** `getUserPermissionsJWTByProxy({id:humanId, proxyIds:[parentId], basePermissions:true})`; if `workspaceContext.{add,remove}Workspaces` non-empty → `workspaceAssociationHelper(CLAIM, humanId, add, remove)`; `PUT {base}/{humanId}` (snake_case); **throw on `validationErrors`/`message`**. No rollback. |
| M3 | `bulkUpdateClaim(sparkClaim): [Claims]` | Medium | (own) `PUT {base}/bulk-update`. **Error contract:** `isArray(result)`→return; `status_code>400`→throw; else throw "unhandled". **Latent:** response transform uses `deepToSnakeCase` (should be camelCase). |
| M4 | `requestClaimExport: String` | Low | (own) `POST {base}/export` → `response.request_id`. |
| M5 | `lockClaim(claimId): Claims` | Low | (ACL context) token → `PUT {base}/{claimId}/lock`. |
| M6 | `unlockClaim(claimId): Claims` | Low | (ACL context) token → `PUT {base}/{claimId}/unlock`. |

## Field Resolvers (17)

**`Claims` (11):**
- `access` (ACL context) — `accessControl.getPermissions([humanId])[0]`.
- `currentUserPermissions` (ACL context) — `getUserAccessUnencoded(humanId)[0]`.
- `createdBy` / `updatedBy` (🟡 user-profile) — `getUserByIDOrNullIfNotFound`.
- `parentDetails` (🟡 product) — `product.getByID(parentId)` (returns the product; its fields feed `ParentDetails`).
- `product` (🟡 product) — only if `parentId` starts `'PID'` → `product.getByID(parentId)`, else null.
- `businessPartner` (🔵 vmm) — 3-way fallback (`partnerId` || `0`→`{bpId:0,bpName:'Target'}` || `dpPartnerId`).
- `designPartner` (🔵 vmm) — `dpPartnerId` or `{bpId:null,bpName:null}`.
- `workspaces` (🟡 workspaceV2) — `getWorkspacesByIdsV2(workspaceContext)` or null.
- `participantDetails` (🔵 user-profile) — `getUserGroup(humanId)`.

**`ParentDetails` (3):**
- `otherClaimBps` (🔴 search) — `getClaimsElastic({q:"parentId: {productId}"})` → partner ids (filtered).
- `systemTeams` (🔴 search) — build elastic team query from product BPs → `searchTeams({page,size,q})`; empty → `{content:[]}`.
- `droppedPartnerIds` (direct) — `product.droppedPartnerIds`.

**`ClaimSubstantiate` (1):** `substantiatedBy` (🟡 user-profile).
**`ClaimDetails` (1):** `claimName` (computed) — `claimDetails.guestFacingClaim`.

## Service Classes
- `ClaimService` base injected.
- Methods: `create` (POST), `getClaims` (GET listing), `getClaimsByIds` (GET `/search?claimIds=`), `updateClaim` (PUT `/{humanId}`), `bulkUpdateClaim` (PUT `/bulk-update`), `getCommunicationChannels` (GET `/communication-channels`), `manageWorkspaceAssociations` (PUT `/{id}/associate_workspace`|`/dissociate_workspace`), `getClaimExports` (GET `/export`), `requestClaimExport` (POST `/export`→request_id), `searchGuestFacing` (GET `/search/guest_facing_claim`), `lockClaim`/`unlockClaim` (PUT `/{id}/lock`|`/unlock`), `getAllClaimsAbout` (GET `/claims-about`).
**Unused:** `getClaimVersionsById`, `getClaimVersion`.

## EXT Service Call Inventory (summary)
6 EXT keys — **1 🔴** (search) · **3 🟡** (product, userAttributes, workspaceV2) · **2 🔵** (vmm,
user-profile/userGroup) · accessControl **context-only**. `claim` is the owned service.

## Key Findings
- **Highest risk:** `updateClaim` (M2) — proxy ACL + workspace assoc + body + throw, no rollback.
- **Latent bugs:** `bulkUpdateClaim` response transform uses `deepToSnakeCase` (should be camelCase);
  unusual `status_code` error branch — verify on port.
- **Preserve exactly:** `businessPartner` 3-way fallback (incl. `{bpId:0,bpName:'Target'}`); create/update
  throw-on-error contracts.
- **Federation:** claims is a separate subgraph — it **contributes** `Product.claims` + TechPack
  `ResourcesCount.claims` (Phase H — cross-subgraph, blocked until `spark-claims` deploys).
- **Quick wins:** the 5 simple reads (Q1–Q5), lock/unlock, requestClaimExport.

---
**Phase Completed:** Phase 2 · **Domain:** `claims` · **EXT:** 6 keys (1🔴 · 3🟡 · 2🔵).
