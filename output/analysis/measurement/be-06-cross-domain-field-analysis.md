# Phase 6: Cross-Domain Field Analysis — Measurement

> **Domain:** `measurement`
> **Target DGS:** `plm-product (co-located)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-17
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · [be-03-schema.graphql](./be-03-schema.graphql)
> **DGS Target Status:** Green-field

For every query/mutation/field resolver that hydrates from another domain or service, this identifies the dependency, whether the field is used by a real frontend client operation (cross-checked against `ClientCallingGqlQueries/`), complexity, and a federation recommendation.

## Summary

| Metric | Count |
|---|---|
| Total resolvers scanned | 29 |
| Resolvers with cross-domain/EXT dependency | 10 |
| Low complexity | 10 |
| Cross-domain fields with no client usage found | 8 |

## Cross-Domain Field Dependencies

| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |
|---|---|---|---|---|
| `Query.getMeasurements` | `relationship` (RelationshipService) | `getMeasurements` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.getMeasurementsElastic` | `search` (SearchService (elastic)) | `getMeasurementsElastic` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.measurementTemplates` | `measurementTemplate` (Measurement (templates) services) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.product` | `product` (Product) | ⏭ not found in ClientCallingGqlQueries | Low | @requires field composition — single co-located phase-1 domain, same plm-product subgraph |
| `SPARK_Measurements.sizeTemplate` | `sizeTemplate` (Measurement (templates) services) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.tightFitTemplate` | `tightFit` (Measurement (templates) services) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Measurements.updatedFromResource` | `sampleV2` (SampleService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_SampleMeasurementSet.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |

## Recommendation Legend

- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); compose via Federation `@requires`, no gateway hop.
- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, sequence the `@requires` chain, document ordering.
- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS subgraph; needs a federation entity fetcher on the owning side.
- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS migration, the gateway resolves the stub directly.
- **No cross-domain dependency** — resolves locally; no federation work needed.

---
**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `measurement` · **Cross-domain fields:** 10/29
