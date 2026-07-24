# Phase 6: Cross-Domain Field Analysis — BOM

> **Domain:** `bom`
> **Target DGS:** `plm-product (co-located)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-24
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · [be-03-schema.graphql](./be-03-schema.graphql)
> **DGS Target Status:** Green-field

For every query/mutation/field resolver that hydrates from another domain or service, this identifies the dependency, whether the field is used by a real frontend client operation (cross-checked against `ClientCallingGqlQueries/`), complexity, and a federation recommendation.

## Summary

| Metric | Count |
|---|---|
| Total resolvers scanned | 92 |
| Resolvers with cross-domain/EXT dependency | 19 |
| Medium complexity | 1 |
| Low complexity | 18 |
| Cross-domain fields with no client usage found | 15 |

## Cross-Domain Field Dependencies

| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |
|---|---|---|---|---|
| `Query.getBomElastic` | `search` (SearchService (elastic)) | `getBomElastic` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.getBomMaterialTypes` | `materialHub` (MaterialHubService) | `getBomMaterialTypes` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.getComboSupplierForBom` | `vmm` (VMM platform) | `getComboSupplierForBom` | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `Query.searchMaterialsBom` | `search` (SearchService (elastic)) | `searchMaterialsBom` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomCombinationMaterial.libraryResource` | `combination` (CombinationService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomFabricLibraryImpressionDetails.libraryResource` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomFabricMaterial.libraryResource` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomFabricSpecMaterial.libraryResource` | `fabric` (FabricService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomImpressionDetails_Unified.libraryResource` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomMaterialSearchResult.fabric` | `fabric` (FabricService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomMaterialSearchResult.fabricSpec` | `fabric` (FabricService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomMaterialSearchResult.relatedMaterials` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomTrimLibraryImpressionDetails.libraryResource` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomTrimMaterial.facilityName` | `location` (VMM platform), `trim` (TrimService) | ⏭ not found in ClientCallingGqlQueries | Medium | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomTrimMaterial.libraryResource` | `trim` (TrimService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomTrimMaterial.materialLibraryUom` | `trim` (TrimService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomTrimMaterial.sizeCaption` | `trim` (TrimService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomTrimMaterial.sizeValue` | `trim` (TrimService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_BomWashMaterial.libraryResource` | `wash` (WashService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |

## Recommendation Legend

- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); compose via Federation `@requires`, no gateway hop.
- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, sequence the `@requires` chain, document ordering.
- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS subgraph; needs a federation entity fetcher on the owning side.
- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS migration, the gateway resolves the stub directly.
- **No cross-domain dependency** — resolves locally; no federation work needed.

---
**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `bom` · **Cross-domain fields:** 19/92
