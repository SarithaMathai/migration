# Phase 1: Schema Inventory — Impression

> **Domain:** `impression`
> **Target DGS:** `ImpressionService` → `plm-product` (co-located)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `schemas/SPARK_Impression.graphqls` (59-line SDL) + `resolvers/product/SPARK_Impression.js` + `services/product/Impression.js`
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

Endpoint built in the service constructor (`services/product/Impression.js:10`):

```js
class ImpressionService extends SparkService {
  this.endpoint = endpoint + '/enterprise_product_development_products/impressions/product'
}
```

| Setting | Value |
|---|---|
| Loader key | `impression` |
| Service class | `ImpressionService extends SparkService` |
| Backend base | `https://spark-product.dev.target.com` (repo `spark-product`) |
| Base path | `${endpoint}/enterprise_product_development_products/impressions/product` |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | `plm-product` |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Impression.graphqls` | 59 | the source SDL — 2 queries, 1 mutation, `Impression`/`ImpressionCount` types, 2 inputs |
| `resolvers/product/SPARK_Impression.js` | 66 | 2 queries, 1 mutation, 2 type blocks (6 field resolvers) |
| `services/product/Impression.js` | 44 | 2 REST methods (search GET, update PUT) |
| **Total** | **169** | small domain — no chunked reading |

Schema: **`schemas/SPARK_Impression.graphqls` (59 lines)** — the target schema in [be-03-schema.graphql](./be-03-schema.graphql) is translated from it (nullability from the SDL).

## 3. Import Graph
```
resolvers/SPARK_Impression.js
├── utils/commonLoaders        → getUserPermissionsJWT (ACL token — context only)
├── utils/logger               → logger (counts error fallback)
├── utils/vmmUtils             → loadBp, loadBpsWithType (VMM partner enrichment)
└── resolvers/SPARK_WorkspaceV2→ getWorkspacesByIdsV2 (workspace enrichment)
services/ImpressionService.js extends SparkService; uses putOne, loadListing, convertFunctions
```

## 4. Cross-Domain Reference Table

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `businessPartners`, `owningBusinessPartner` | `vmm` (loadBp/loadBpsWithType) | VMM platform | Gateway stitch | 🔵 |
| `workspaces` | `workspaceV2` | WorkspaceService | sibling federation | 🟡 |
| `createdBy`, `updatedBy` | `userAttributes` | UserProfileService | sibling federation | 🔵 |
| `ImpressionCount.counts` product lookup | `product` | ProductService (same DGS) | **internal** | — |
| all reads/writes | `accessControl` (getUserPermissionsJWT) | AccessControlService | **context only — ACL ignored** | n/a |

## 5. Co-located Siblings
`product`, `bom`, `measurement`, `packaging`, `productDetails` — share `plm-product`.

## 6. Hot Spots
1. **`SPARK_ImpressionCount.counts`** (`:46-65`) — unusual pattern: the parent passed in is the **impressions
- array** (not a wrapper).
- It fetches the product, derives partner ids, counts impressions per partner, and appends a `totalCount` row.
- Wrapped in try/catch → on error returns `[{bpType:'totalCount', counts:0}]`.
2. **`getImpressionCountsByProductId`** reuses `searchImpressionsByProductId` (same REST call) and lets the
   `counts` field do the aggregation — the query returns the impressions list typed as `ImpressionCount`.
3. **Awkward count contract** — recommend restructuring to a typed `ImpressionCountResult` (PO decision; see 03-analysis).
4. **JWT-curried** — both queries and the mutation curry a capability token (ACL — context only).

## 7. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 2 |
| Mutations | 1 |
| Object types | 2 (`Impression`, `ImpressionCount`) |
| Field resolvers | 6 (5 on Impression, 1 on ImpressionCount) |
| Service methods | 2 |
| Cross-domain loader keys | 4 (+ accessControl context-only) |
| EXT calls | 0 🔴 · 1 🟡 · 3 🔵 |
| Large files | 0 |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `impression` · **Files:** 3 (169 lines: schema 59 + resolver 66 + service 44).
