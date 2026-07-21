# Phase 6: Cross-Domain Field Analysis — Measurement

> **Domain:** `measurement`
> **Target DGS:** `plm-product (co-located)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-21
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · [be-03-schema.graphql](./be-03-schema.graphql)
> **DGS Target Status:** Green-field

For every query/mutation/field resolver that hydrates from another domain or service, this identifies the dependency, whether the field is used by a real frontend client operation (cross-checked against `ClientCallingGqlQueries/`), complexity, and a federation recommendation.

## Summary

| Metric | Count |
|---|---|
| Total resolvers scanned | 56 |
| Resolvers with cross-domain/EXT dependency | 19 |
| Low complexity | 19 |
| Cross-domain fields with no client usage found | 17 |

## Cross-Domain Field Dependencies

| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |
|---|---|---|---|---|
| `Query.getMeasurements` | `relationship` (RelationshipService) | `getMeasurements` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.getMeasurementsElastic` | `search` (SearchService (elastic)) | `getMeasurementsElastic` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_MeasurementTemplate.brands` | `brand` (VMM platform) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_MeasurementTemplate.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_MeasurementTemplate.departments` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_MeasurementTemplate.divisions` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_MeasurementTemplate.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.product` | `product` (Product) | ⏭ not found in ClientCallingGqlQueries | Low | @requires field composition — single co-located phase-1 domain, same plm-product subgraph |
| `SPARK_Measurements.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.updatedFromResource` | `sampleV2` (SampleService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_SampleMeasurementSet.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_SizeTemplate.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_SizeTemplate.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_TightFit.brands` | `brand` (VMM platform) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_TightFit.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_TightFit.departments` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_TightFit.divisions` | `ig` (Item Groups (IG)) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_TightFit.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |

## Recommendation Legend

- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); compose via Federation `@requires`, no gateway hop.
- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, sequence the `@requires` chain, document ordering.
- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS subgraph; needs a federation entity fetcher on the owning side.
- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS migration, the gateway resolves the stub directly.
- **No cross-domain dependency** — resolves locally; no federation work needed.

---
**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `measurement` · **Cross-domain fields:** 19/56
