# Impression — Schema Inventory

> **Domain:** `impression` · **Target DGS:** `plm-impression` (green-field) — but see note below
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## 1. Context Registration

| Setting | Value |
|---|---|
| Context key | `impression` |
| Service class | `ImpressionService extends SparkService` (`services/product/Impression.js`) |
| Backend endpoint | `${config.endpoints.product}/enterprise_product_development_products/impressions/product` |
| Loader registration | `context.js` line 187 |

> **Domain-sizing note:** This is a single-collection sub-resource of Product (`/impressions/product/{productId}`). Strong candidate for **co-location inside `plm-product`** rather than its own DGS subgraph. Flagged as PO decision #1.

---

## 2. File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Impression.graphql` | 59 | Schema |
| `resolvers/product/SPARK_Impression.js` | 66 | Resolvers |
| `services/product/Impression.js` | 44 | REST client (2 methods) |
| **Total** | **169** | |

---

## 3. Dependencies

| Sibling DGS / platform | Usage |
|---|---|
| VMM | `VMM_BusinessPartner` (businessPartners, owningBusinessPartner) |
| `plm-workspace` | `getWorkspacesByIdsV2` |
| `plm-user-profile` | `userAttributes.getUserByID` for createdBy/updatedBy |
| `plm-product` | `product.getByID` for `SPARK_ImpressionCount.counts` |
| `plm-access-control` | `getUserPermissionsJWT` on both queries + mutation |

---

## 4. Surface Summary

- 2 queries (`searchImpressionsByProductId`, `getImpressionCountsByProductId`)
- 1 mutation (`updateImpressions`)
- 2 types (`SPARK_Impression`, `SPARK_ImpressionCount`)
- 2 inputs (`SPARK_ProductImpressionInput`, `SPARK_ImpressionInput`)
- 5 field resolvers on `SPARK_Impression`
- 1 field resolver on `SPARK_ImpressionCount`

---

## 5. Hot Spots / Flags

| # | Finding | Severity |
|---|---|---|
| 1 | `enableWorkspaceContextFiltering` arg is **declared in schema and passed by resolver** but `ImpressionService.searchImpressionsByProductId` **signature drops the 4th arg** → bug, never reaches backend | 🔴 |
| 2 | `getImpressionCountsByProductId` schema returns `SPARK_ImpressionCount` but resolver returns `[SPARK_Impression]` — relies on `counts` field-resolver receiving the array as parent. Schema-shape mismatch (works but fragile) | 🔴 |
| 3 | `SPARK_ImpressionCount.counts` uses `try/catch` and silently returns dummy `[{bpType: 'totalCount', counts: 0}]` on failure (no `null` from upstream → swallowed error) | 🟡 |
| 4 | `counts` resolver indexes `impressions[0].parentId` — TypeError if empty array | 🟡 |
| 5 | `bpType` mixes integer partnerIds and the string literal `'totalCount'` — type ambiguity | 🟡 |
| 6 | `updateImpressions` shape-sniffs errors (`validationErrors \|\| message`) | 🟢 |
| 7 | No bulk read by IDs; all reads are per-product. Confirm gateway doesn't need an `Impression @key` entity | 🟡 |

---

**Phase Completed:** Phase 1 — Schema Inventory
**Output:** [output/impression/01-schema-inventory.md](output/impression/01-schema-inventory.md)
