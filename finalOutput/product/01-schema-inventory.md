# Phase 1: Schema Inventory — Product

> **Domain:** `product`
> **Target DGS:** `ProductService` → `plm-product` (the flagship co-located DGS)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source of truth:** `code/schemas/SPARK_Product.txt` (802-line SDL) + `code/resolvers/SPARK_Product.txt` (2,629) + `code/services/Product.txt` (589) + utils
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

There is no `context.js`/config in the snapshot (the schema SDL *is* present — see manifest below). The
endpoints are built inside `ProductService`'s
constructor (`code/services/Product.txt`): `endpointv1 = ${base}/enterprise_product_development_products/v1`,
`endpointv2 = …/v2`, plus an elastic search endpoint, a copy endpoint, and an external rating endpoint.

| Setting | Value |
|---|---|
| Loader key | `product` |
| Service class | `ProductService` |
| Backend base | `https://spark-product.dev.target.com` (repo `spark-product`) |
| Paths | `…/enterprise_product_development_products/v1` and `/v2`; elastic search; `requests/v1` (copy); external rating service (API-key) |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — **context only, ignored in impl**) |
| Target DGS | `plm-product` (this is the host DGS for all co-located product-family domains) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `code/schemas/SPARK_Product.txt` | 802 | the source SDL — `extend type Query` (18), `extend type Mutation` (23), owned types, ~30 inputs |
| `code/resolvers/SPARK_Product.txt` | 2,629 ⚠️ | 18 queries, 23 mutations (20 with top-level resolvers + 3 schema-drift), ~50 field resolvers across 14 type blocks |
| `code/services/Product.txt` | 589 | 42 REST methods (`v1`/`v2`, elastic, rules, rating) |
| utils touched | — | `commonLoaders`, `convertFunctions`, `resolvePaging`, `vmmUtils`, `accessControlUtils`, `Product/attachmentUtils`, `Product/partnerUtils`, `Product/teamUtils`, `Product/productUtils`, `Product/getReservedDpcisFromApex`, `componentStatusUtils`, `discussionUtils`, `removePartnerUtils`, `ProductAskUtils` |
| **⚠️ Large file** | 2,629 | Phase 2 read in 500-line windows (queries → mutations → fields → service/utils) |

Schema: **`code/schemas/SPARK_Product.txt` (802 lines)** — the federated target schema in
[03-schema.graphql](./03-schema.graphql) is translated from it (nullability taken from the SDL).

## 3. Co-located Siblings (same `plm-product` DGS — sibling field resolvers become same-service `@DgsData`)
`pom`, `fileLibrary`, `measurement`, `bom`, `impression`, `measurementTemplate`, `sizeTemplate`,
`specificationsTemplate`, `productDetails`, `watchlist`, `tightFit`, `packaging`, `productPlan`,
`productAsk`, `productVariation`. **Federation implication:** `bom`, `claims`, `measurementSets`,
`productBom`, `packagingBom`, `productDetails`, `variations`, `associateProductsAsks` resolve **internally**
(same DGS) — not cross-subgraph.

## 4. Cross-Domain Reference Table (loaders called from the resolver)

| Loader key | Owner / DGS | Class | Severity | Used for |
|---|---|---|---|---|
| `product`, `bom`, `measurement`, `productDetails`, `packaging`, `productAsk`, `productVariation`, `fileLibrary` | plm-product (same) | **Internal** | — | reads/writes, `updateComponentStatuses`, sibling fields |
| `attachment` | spark-attachment | EXT | 🔴 | TechPack, `attachments`, `attachmentsWithMetaData`, copy flows |
| `workspaceV2` | spark-workspace | EXT | 🔴 | add/update product, workspace attribute fields |
| `search` | elastic | EXT | 🔴 | `getProducts`, `getProductTemplates`, TechPack ×7, `components`, `discussionsV2`, `attachmentSummary` |
| `accessControl` | spark-access-control | EXT | **context-only (ACL ignored)** | JWT + ACL batch gating |
| `claim` | spark-claims | EXT | 🟡 | `updateComponentStatuses` claims |
| `relationship` | spark-relationship | EXT | 🟡 | `searchByIds` for attachment/sample/template |
| `userAttributes`, `teamV2` | spark-userprofile | EXT | 🟡 | `createdBy`/`updatedBy`/`teams` |
| `discussion` | spark-discussion | EXT | 🟡 | `discussionsCount`, `discussionsV2` |
| `sampleV2` | spark-sample | EXT | 🟡 | `samples`, `sampleIds` |
| `tag` | spark-tag | EXT | 🟡 | `tags`, design-cycle |
| `recentlyViewed`, `todo`, `favorite`, `ruleLibrary` | various | EXT | 🔵 | partner-drop cleanup; rules flag |
| `ig.department/division/clazz`, `brand`, `vmm`, `coronaItems`, `doppler`, `apex` | platforms | **Gateway stitch** | 🔵 | hierarchy/partner/tcin/doppler/dpci fields |

## 5. Hot Spots (drive complexity — full detail in Phase 2)

1. **`getProductTechPackCountV1` / `…BulkCountV1`** — the single most complex operation: a 17-step
   `getTechPackResourceCountMap` orchestrating ACL tree-walk (×2), attachment hydration, **7 parallel elastic
   queries**, critical-discussion→attachment join, building a `ResourcesCount`. Composite-key aggregate →
   facade-then-federate (Option D). **Bulk version has a latent ordering bug** (push order ≠ input order).
2. **`productBusinessPartnerActions`** — ~220-line dispatcher (REMOVE/DROP/UNDROP partner) with cleanup
   across `recentlyViewed`/`todo`/`favorite`/`sampleV2`. No rollback.
3. **`updateComponentStatuses`** — parallel fan-out to 5 loaders (bom/measurement/productDetail/packaging
   co-located + claim EXT). Shadow-var bug noted.
4. **`Product.attachmentsWithMetaData`** + **`Product.components`** — ~150–190-line field resolvers, heavy
   ACL + multi-source merge (N+1 ACL in `components`).
5. **`SPARK_Categories.__resolveType`** — polymorphic union (12 cases, default `IG_Clazz_Filter`). +1 tier.
6. **`Product.division` latent bug** — calls the *department* loader, not division. Fix on port (contract test).
7. **`USE_NEW_RULES_API` feature flag** — 3 rules queries fork to a different DGS (`spark-tag`). Decide cutover.
8. **External rating service** — API-key auth; secret must move to DGS config/Vault.

## 6. Operation Lists
**Queries (18):** getProducts, getProductTemplates, getProduct, getCopyStatus, getCategories,
getProductsByIds, getProductStatus, getProductTechPackCountV1, getProductTechPackBulkCountV1,
getProductVersions, getRatingByTcin, getProductRules, getProductRulesById, getAllAvailableRules,
getProductDeptRules, getProductBPRules, searchProductRules, getProductTemplateById.
**Mutations (20 implemented + 3 deferred wrappers):** addProduct, updateProduct, carryForwardProduct,
bulkUpdateProducts, addProducts, addTeamsToProduct, addBusinessPartnersToProductWithType,
removeProductResources, updateBusinessPartnerStatuses, productBusinessPartnerActions, updateViewToggle,
updateWorkspaceAttributes, updateProductTeamsWorkspaceContext, linkProduct, unlinkProduct, addProductRule,
updateProductRule, deleteProductRule, updateComponentStatus, updateComponentStatuses. **Deferred (⏭):**
removeProductBusinessPartner, dropProductBusinessPartner, unDropProductBusinessPartner (schema-drift wrappers
— routed through `productBusinessPartnerActions`).

## 7. Summary Statistics

| Metric | Value |
|--------|-------|
| Queries | 18 |
| Mutations | 20 (+3 deferred) |
| Field resolvers | ~50 across 14 type blocks |
| Service methods | 42 |
| Internal (same-DGS) loaders | 8 |
| EXT loaders | 12 |
| Platform (gateway) loaders | 6 (VMM, IG, Doppler, CORONA, APEX, Brand Compliance) |
| Polymorphic `__resolveType` | 1 (`Categories`) |
| Composite-key aggregate | 1 (`ResourcesCount` / TechPack) |
| Large files (>1000 lines) | 1 ⚠️ |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `product` · **Files:** 3 (4,020 lines: schema 802 + resolver 2,629 + service 589).
