# Phase 6: Cross-Domain Field Analysis — Watchlist

> **Domain:** `watchlist`
> **Target DGS:** `plm-product (co-located)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-17
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · [be-03-schema.graphql](./be-03-schema.graphql)
> **DGS Target Status:** Green-field

For every query/mutation/field resolver that hydrates from another domain or service, this identifies the dependency, whether the field is used by a real frontend client operation (cross-checked against `ClientCallingGqlQueries/`), complexity, and a federation recommendation.

## Summary

| Metric | Count |
|---|---|
| Total resolvers scanned | 15 |
| Resolvers with cross-domain/EXT dependency | 10 |
| Medium complexity | 2 |
| Low complexity | 8 |
| Cross-domain fields with no client usage found | 6 |

## Cross-Domain Field Dependencies

| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |
|---|---|---|---|---|
| `Mutation.cloneFilesForWatchlist` | `attachment` (separate DGS (plm-attachment)) | `cloneFilesForWatchlist` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Mutation.createWatchlistEntries` | `userGroup` (UserGroupService) | `createWatchlistEntries` | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Mutation.updateWatchlistEntries` | `attachment` (separate DGS (plm-attachment)), `userGroup` (UserGroupService) | `updateWatchlistEntries` | Medium | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `Query.getWatchlistByFilter` | `product` (Product), `search` (SearchService (elastic)) | `getWatchlistForBulkUpdate` | Medium | Co-locate + @requires — multiple phase-1 domains, same plm-product subgraph, order dependency |
| `Query.parentId` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Watchlist.attachments` | `search` (SearchService (elastic)) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Watchlist.createdBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_Watchlist.product` | `product` (Product) | ⏭ not found in ClientCallingGqlQueries | Low | @requires field composition — single co-located phase-1 domain, same plm-product subgraph |
| `SPARK_Watchlist.updatedBy` | `userAttributes` (UserProfileService) | ⏭ not found in ClientCallingGqlQueries | Low | Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required |
| `SPARK_WatchlistPartner.partnerName` | `vmm` (VMM platform) | ⏭ not found in ClientCallingGqlQueries | Low | Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves |

## Recommendation Legend

- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); compose via Federation `@requires`, no gateway hop.
- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, sequence the `@requires` chain, document ordering.
- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS subgraph; needs a federation entity fetcher on the owning side.
- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS migration, the gateway resolves the stub directly.
- **No cross-domain dependency** — resolves locally; no federation work needed.

---
**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `watchlist` · **Cross-domain fields:** 10/15
