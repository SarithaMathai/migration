# Phase 6: Cross-Domain Field Analysis — Claims

> **Domain:** `claims`
> **Target DGS:** `spark-claims (separate)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-21
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · [be-03-schema.graphql](./be-03-schema.graphql)
> **DGS Target Status:** Green-field

For every query/mutation/field resolver that hydrates from another domain or service, this identifies the dependency, whether the field is used by a real frontend client operation (cross-checked against `ClientCallingGqlQueries/`), complexity, and a federation recommendation.

## Summary

| Metric | Count |
|---|---|
| Total resolvers scanned | 27 |
| Resolvers with cross-domain/EXT dependency | 10 |
| Low complexity | 10 |
| Cross-domain fields with no client usage found | 10 |

## Cross-Domain Field Dependencies

| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |
|---|---|---|---|---|
| `Query.getClaimsElastic` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_ClaimSubstantiate.substantiatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Claims.businessPartner` | `vmm` (VMM platform) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Claims.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Claims.designPartner` | `vmm` (VMM platform) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |
| `SPARK_Claims.parentDetails` | `product` (Product) | ⏭ not found in ClientCallingGqlQueries | Low | @requires field composition — single co-located phase-1 domain, same plm-product subgraph |
| `SPARK_Claims.product` | `product` (Product) | ⏭ not found in ClientCallingGqlQueries | Low | @requires field composition — single co-located phase-1 domain, same plm-product subgraph |
| `SPARK_Claims.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_ParentDetails.otherClaimBps` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_ParentDetails.systemTeams` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |

## Recommendation Legend

- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); compose via Federation `@requires`, no gateway hop.
- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, sequence the `@requires` chain, document ordering.
- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS subgraph; needs a federation entity fetcher on the owning side.
- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS migration, the gateway resolves the stub directly.
- **No cross-domain dependency** — resolves locally; no federation work needed.

---
**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `claims` · **Cross-domain fields:** 10/27
