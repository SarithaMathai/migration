# Phase 6: Cross-Domain Field Analysis — Product

> **Domain:** `product`
> **Target DGS:** `plm-product (host)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-18
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · [be-03-schema.graphql](./be-03-schema.graphql)
> **DGS Target Status:** Green-field

For every query/mutation/field resolver that hydrates from another domain or service, this identifies the dependency, whether the field is used by a real frontend client operation (cross-checked against `ClientCallingGqlQueries/`), complexity, and a federation recommendation.

## Summary

| Metric | Count |
|---|---|
| Total resolvers scanned | 105 |
| Resolvers with cross-domain/EXT dependency | 45 |
| Very High complexity | 2 |
| High complexity | 2 |
| Medium complexity | 4 |
| Low complexity | 37 |
| Cross-domain fields with no client usage found | 37 |

## Cross-Domain Field Dependencies

| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |
|---|---|---|---|---|
| `DopplerDepartment.clazzes` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `DopplerDepartment.department` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `DopplerDepartment.division` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `DopplerDepartment.primaryCapacityTypeName` | `doppler` (External platforms) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `DopplerDepartment.secondaryCapacityTypeName` | `doppler` (External platforms) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `Mutation.addProduct` | `workspaceV2` (WorkspaceService) | `addProduct` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Mutation.addProducts` | `attachment` (separate DGS (plm-attachment)), `workspaceV2` (WorkspaceService) | `addProducts` | Medium | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Mutation.productBusinessPartnerActions` | `favorite` (Dashboard services), `recentlyViewed` (Dashboard services), `relationship` (RelationshipService), `sampleV2` (SampleService), `todo` (Dashboard services) | `productBusinessPartnerActions` | Very High | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Mutation.updateComponentStatuses` | `ProductDetails` (Product Details), `bom` (BOM), `claim` (Claims), `measurement` (Measurement), `packaging` (Packaging) | `updateComponentStatuses` | Very High | Co-locate + @requires — multiple phase-1 domains, same plm-product subgraph, order dependency |
| `Mutation.updateProduct` | `attachment` (separate DGS (plm-attachment)) | `updateProduct`; `updateProduct`; `updateProduct` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `ProductComponentStatus.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.getProductBPRules` | `ruleLibrary` (RuleLibraryService) | `getProductBPRules` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.getProductDeptRules` | `ruleLibrary` (RuleLibraryService) | `getProductDeptRules` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.searchProductRules` | `ruleLibrary` (RuleLibraryService) | `searchProductRules` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_PackagingAttribute.spg` | `fileLibrary` (FileLibraryService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.associateProductsAsks` | `productAsk` (ProductAskService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.attachmentSummary` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.attachments` | `attachment` (separate DGS (plm-attachment)), `relationship` (RelationshipService) | ⏭ not found in ClientCallingGqlQueries | Medium | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.attachmentsData` | `relationship` (RelationshipService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.attachmentsWithMetaData` | `attachment` (separate DGS (plm-attachment)), `relationship` (RelationshipService), `sampleV2` (SampleService) | ⏭ not found in ClientCallingGqlQueries | High | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.brand` | `brand` (VMM platform) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Product.brands` | `brand` (VMM platform) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Product.businessPartners` | `workspaceV2` (WorkspaceService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.clazz` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Product.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.department` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Product.designCycle` | `tag` (TagService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.discussionsCount` | `discussion` (separate DGS (plm-discussion)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.discussionsV2` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.division` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Product.divisions` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Product.elasticSamplesList` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.productTemplateDepartments` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Product.productWorkspaceAttributes` | `search` (SearchService (elastic)), `tag` (TagService) | ⏭ not found in ClientCallingGqlQueries | Medium | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.productWorkspaceInfo` | `search` (SearchService (elastic)), `tag` (TagService) | ⏭ not found in ClientCallingGqlQueries | Medium | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.samples` | `relationship` (RelationshipService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.teams` | `teamV2` (TeamService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.variations` | `productVariation` (ProductVariationService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.versionCreatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Product.workspaces` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_ProductRules.departments` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_ProductRules.insightsClassExclusion` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_ProductsCategories.categories` | `brand` (VMM platform), `ig` (Item Groups (IG)), `packaging` (Packaging), `tag` (TagService) | ⏭ not found in ClientCallingGqlQueries | High | Co-locate + @requires — multiple phase-1 domains, same plm-product subgraph, order dependency |
| `SPARK_Tcin.itemDetails` | `coronaItems` (External platforms) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |

## Recommendation Legend

- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); compose via Federation `@requires`, no gateway hop.
- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, sequence the `@requires` chain, document ordering.
- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS subgraph; needs a federation entity fetcher on the owning side.
- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS migration, the gateway resolves the stub directly.
- **No cross-domain dependency** — resolves locally; no federation work needed.

---
**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `product` · **Cross-domain fields:** 45/105
