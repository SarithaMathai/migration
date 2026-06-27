# Phase 2: Resolver Dependency Analysis — Impression

> **Domain:** `impression` · **Target DGS:** `ImpressionService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `code/schemas/SPARK_Impression.txt` (SDL), `code/resolvers/product/SPARK_Impression.txt`, `code/services/product/Impression.txt`
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full

## Summary Statistics

| Metric | Count |
|--------|-------|
| Query resolvers | 2 |
| Mutation resolvers | 1 |
| Field resolvers | 6 |
| Service methods | 2 |
| EXT loader keys | 4 (1 🟡 · 3 🔵) + accessControl (context only) |
| Very High / High ops | 0 / 0 |

---

## Query Resolvers (2)

### Q1 · `searchImpressionsByProductId(id, partnerIds, workspaceIds, enableWorkspaceContextFiltering): [Impression]` — Low
1. (ACL context) capability token for `id` — backend authorizes per-product impression read; ignored in DGS.
2. `ctx.loaders.impression.searchImpressionsByProductId(jwt, id, partnerIds, workspaceIds, enableWorkspaceContextFiltering)`.
**Service:** `GET {base}/…/impressions/product/{id}?workspaceIds=&partnerIds=` (repeated query params built by looping the arrays). Transform `deepToCamelCase`.
**Note:** `enableWorkspaceContextFiltering` is accepted by the resolver but **not forwarded** to the service method (only id/partnerIds/workspaceIds are). Confirm intended.

### Q2 · `getImpressionCountsByProductId(id): ImpressionCount` — Low
1. (ACL context) capability token for `id`.
2. Returns `searchImpressionsByProductId(jwt, id)` — **the same REST call**, returning the impressions list.
   The `ImpressionCount.counts` field resolver (F6) does the aggregation; the query's return value is the impressions array typed as `ImpressionCount`.

## Mutation Resolvers (1)

### M1 · `updateImpressions(productId, productImpression): [Impression]` — Medium
1. (ACL context) capability token for `productId`.
2. `impression = impressionService.updateImpressions(jwt, productId, productImpression)` → `PUT {base}/…/impressions/product/{productId}` (`transformRequest: deepToSnakeCase`, response `deepToCamelCase`).
3. If `impression.validationErrors || impression.message` → `throw Error('Error updating impression set\n' + JSON.stringify(...))`.
4. Return `impression`.
**Input:** `productImpression: { impressionsToDelete: [String], impressionsToUpdate: [ImpressionInput] }`.
**DGS:** typed `ImpressionValidationException` replaces the shape-sniff.

## Field Resolvers

### F1–F5 · `Impression` (5 fields) — Low
| Field | Logic | EXT |
|---|---|---|
| `businessPartners` | `partnerIds && loadBpsWithType(partnerIds.map(p=>({partnerId:p})), ctx)` | 🔵 vmm |
| `owningBusinessPartner` | `owningPartnerId && loadBp(ctx, owningPartnerId)` | 🔵 vmm |
| `workspaces` | `workspaceContext.length ? getWorkspacesByIdsV2({ids}) : []` | 🟡 workspaceV2 |
| `createdBy` | `createdBy && userAttributes.getUserByID.load(createdBy)` | 🔵 user-profile |
| `updatedBy` | `updatedBy && userAttributes.getUserByID.load(updatedBy)` | 🔵 user-profile |

### F6 · `ImpressionCount.counts: [CountsByBp]` — Medium
Parent = the **impressions array**.
1. `parentId = impressions[0].parentId`.
2. `product = ctx.loaders.product.getByID.load(parentId)` — **internal** same-DGS call.
3. `partners = (product.businessPartners||[]).map(p => p.partnerId)`.
4. For each partner: `{bpType: partnerId, counts: impressions.filter(i => i.partnerIds.includes(partnerId)).length}`.
5. Append `{bpType:'totalCount', counts: impressions.length}`.
6. **On any error** → log + return `[{bpType:'totalCount', counts:0}]`.

## Service Classes (1)

### S1 · `ImpressionService` — base `…/impressions/product`
| Method | HTTP | Path | JWT | Notes |
|---|---|---|---|---|
| `searchImpressionsByProductId(jwt, productId, partnerIds, workspaceIds)` | GET | `/{productId}?workspaceIds=&partnerIds=` | ✓ | repeated query params; camelCase |
| `updateImpressions(jwt, productId, productImpression)` | PUT | `/{productId}` | ✓ | snake_case request, camelCase response |

## EXT Service Call Inventory

**4 keys — 0 🔴 · 1 🟡 · 3 🔵** (+ accessControl context-only):

| # | Loader key | Owning DGS / platform | Severity | Called from |
|---|---|---|---|---|
| 1 | `workspaceV2` | WorkspaceService | 🟡 | F3 workspaces |
| 2 | `vmm` | VMM platform | 🔵 | F1, F2 |
| 3 | `userAttributes` | UserProfileService | 🔵 | F4, F5 |
| 4 | `product` | ProductService (same DGS) | — internal | F6 counts |

## Complexity Assessment
All Low except M1 `updateImpressions` (Medium — write + validation) and F6 `counts` (Medium — aggregation + error fallback).

## Key Findings
- **Highest risk:** none High/VH — this is a small, low-risk domain.
- **Refactor:** `ImpressionCount` count contract is awkward (parent is an array). Recommend a typed
  `ImpressionCountResult` (PO decision in 03-analysis).
- **Confirm:** `enableWorkspaceContextFiltering` accepted but not forwarded to the service (Q1).
- **Quick wins:** both queries + all field resolvers.

---
**Phase Completed:** Phase 2 · **Domain:** `impression` · **EXT:** 4 keys (0🔴·1🟡·3🔵).
