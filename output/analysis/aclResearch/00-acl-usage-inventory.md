# ACL Research — Usage Inventory (Program Roll-Up)

> **Scope:** 8 phase-1 domains · **Generated:** 2026-07-17 · **Pipeline Version:** 1.0
> Aggregates each domain's `be-07-acl-usage-analysis.md`. Regenerate via `python fedMigrationScripts/generatescripts/generate_acl_analysis.py`.

## Key Finding

Every domain's `be-03-schema.graphql` header and `be-04-stories.md` currently state: *"capability-token (JWT) usage in source is context-only; ACL is IGNORED in the DGS implementation (no ACL plumbing story)"*. This research finds that is only true for **permission-check** and **own-domain-token** call sites. **Downstream-token** call sites mint a capability token specifically to call another domain's API — ACL is load-bearing there, and **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) is the recommended resolution: refresh the current thread's security context with the newly-fetched token instead of re-authenticating per downstream call.

**This is a proposed supersession, not yet applied to be-03/be-04** — those docs are edited in a separate follow-up once these findings are reviewed.

## Program Totals

| Metric | Value |
|---|---|
| Total ACL call sites | 73 |
| Permission-check | 15 |
| Own-domain token | 35 |
| **Downstream-token (Mid-Request ACL Update candidates)** | **23** |
| Unresolved (manual check) | 0 |

## By Domain

| Domain | Total sites | Permission-check | Own-domain token | Downstream-token | Unresolved |
|---|---|---|---|---|---|
| [Product](../product/be-07-acl-usage-analysis.md) | 18 | 8 | 1 | **9** | 0 |
| [BOM](../bom/be-07-acl-usage-analysis.md) | 12 | 0 | 6 | **6** | 0 |
| [Measurement](../measurement/be-07-acl-usage-analysis.md) | 10 | 2 | 8 | **0** | 0 |
| [Product Details](../productDetails/be-07-acl-usage-analysis.md) | 9 | 2 | 5 | **2** | 0 |
| [Packaging](../packaging/be-07-acl-usage-analysis.md) | 11 | 1 | 6 | **4** | 0 |
| [Watchlist](../watchlist/be-07-acl-usage-analysis.md) | 5 | 0 | 3 | **2** | 0 |
| [Impression](../impression/be-07-acl-usage-analysis.md) | 3 | 0 | 3 | **0** | 0 |
| [Claims](../claims/be-07-acl-usage-analysis.md) | 5 | 2 | 3 | **0** | 0 |
| **TOTAL** | **73** | **15** | **35** | **23** | **0** |

## All Downstream-Token Call Sites (Mid-Request ACL Update candidates)

| Domain | Resolver | Target domain | Recommendation |
|---|---|---|---|
| product | `Mutation.addProducts` | `workspaceV2` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `workspaceV2`, avoiding re-authentication |
| product | `Mutation.addProducts` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| product | `Mutation.addProduct` | `workspaceV2` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `workspaceV2`, avoiding re-authentication |
| product | `Mutation.updateProduct` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| product | `Mutation.updateProduct` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| product | `Mutation.productBusinessPartnerActions` | `sampleV2` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `sampleV2`, avoiding re-authentication |
| product | `SPARK_Product.associateProductsAsks` | `productAsk` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `productAsk`, avoiding re-authentication |
| product | `SPARK_Product.variations` | `productVariation` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `productVariation`, avoiding re-authentication |
| product | `SPARK_Product.teams` | `teamV2` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `teamV2`, avoiding re-authentication |
| bom | `SPARK_BomWashMaterial.libraryResource` | `wash` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `wash`, avoiding re-authentication |
| bom | `SPARK_BomImpressionDetails_Unified.libraryResource` | `search` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `search`, avoiding re-authentication |
| bom | `SPARK_BomFabricLibraryImpressionDetails.libraryResource` | `search` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `search`, avoiding re-authentication |
| bom | `SPARK_BomTrimLibraryImpressionDetails.libraryResource` | `search` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `search`, avoiding re-authentication |
| bom | `SPARK_BomMaterialSearchResult.fabric` | `fabric` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `fabric`, avoiding re-authentication |
| bom | `SPARK_BomMaterialSearchResult.relatedMaterials` | `search` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `search`, avoiding re-authentication |
| productDetails | `Mutation.updateProductDetailsSet` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| productDetails | `Mutation.cloneFilesForProductDetails` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| packaging | `Mutation.updatePackaging` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| packaging | `Mutation.updatePackaging` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| packaging | `Mutation.cloneFilesForDielines` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| packaging | `SPARK_Dieline.attachment` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| watchlist | `Mutation.updateWatchlistEntries` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| watchlist | `Mutation.cloneFilesForWatchlist` | `attachment` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |

---
*Program roll-up · generated 2026-07-17 from each domain's `be-07-acl-usage-analysis.md`.*