# Federated GraphQL Migration — Frontend Documentation

> Confluence-ready page · 2026-07-16 · Scope: the 8 phase-1 domains
> Companion page: [Backend Documentation](./backend-confluence-documentation.md)

## Purpose

- Single reference for the pdex-ui-react migration from the spark-internal-graphql gateway to the federated GraphQL router.
- Audience: Engineers implementing frontend stories; Product Owner tracking scope and sequencing.

## Scope

- In scope: every frontend query/mutation whose root field belongs to a phase-1 domain — Product, BOM, Measurement, Product Details, Packaging, Watchlist, Impression, Claims — and the fields those operations select.
- Out of scope: 618 further client operations resolving to later-phase domains or services outside spark-internal-graphql; they migrate with their own subgraph phase.

## Inventory at a glance

| Stat | Value |
|---|---|
| Phase-1 frontend operations | 142 (90 queries, 52 mutations) |
| Fragments on phase-1 types | 22 |
| Client libraries involved | 11 |
| Dynamic (runtime-composed) documents to refactor | 3 |
| Frontend migration stories | 43 (5 platform + 38 domain) |
| Estimated effort | 177–276 engineer-days across 5 waves |

## What changes for the frontend

- Endpoint: one federated router URL replaces the spark-internal-graphql gateway (flag-gated dual-run).
- Type names: owned types drop the `SPARK_` prefix — fragments, generated TypeScript types and Apollo cache identities all change.
- Shapes: flat id fields become entity references (`createdBy`, `brand`, `department`); cross-domain data resolves through `@key`-stitched entities.
- Writes: multi-step backend writes (`updateBom`, `updatePackaging`, `updateClaim`, …) surface saga status — partial failures become explicit UI states.
- Errors: partial data + per-subgraph `errors[]` replaces all-or-nothing responses.

## Deliverables index

| Document | Content |
|---|---|
| [Executive summary](../frontend-analysis/00-executive-summary.md) | Program-level findings and numbers |
| [01 Client inventory](../frontend-analysis/01-client-inventory.md) | Every phase-1 operation: variables, fields, fragments, consumers |
| [02 Backend schema inventory](../frontend-analysis/02-backend-schema-inventory.md) | Phase-1 SDL: types, root fields, deprecations, FE-usage flags |
| [03 Merged inventory](../frontend-analysis/03-merged-inventory.md) | Authoritative operation × resolver × BE-story table |
| [04 Domain analysis](../frontend-analysis/04-domain-analysis.md) | Per-domain grouping, shared fragments/types, cross-domain documents |
| [05 Federation impact](../frontend-analysis/05-federation-impact.md) | Structural schema differences and per-domain impact |
| [06 UI impact](../frontend-analysis/06-ui-impact.md) | Component/hook/cache/test impact per domain with levels |
| [07 Network call analysis](../frontend-analysis/07-network-call-analysis.md) | Request-count and latency changes, caching strategy |
| [08 Frontend stories](../frontend-analysis/08-frontend-stories.md) | The 43 implementation stories (source of truth) |
| [09 Dependency matrix](../frontend-analysis/09-story-dependency-matrix.md) | FE ↔ BE story dependencies, reverse index |
| [10 Sequencing plan](../frontend-analysis/10-migration-sequencing.md) | Waves, gates, rollback posture |
| [11 Traceability matrix](../frontend-analysis/11-traceability-matrix.md) | Domain → schema → resolver → query → component → stories |

## Story waves (summary)

1. **Wave 0 — Platform** (PLATFORM-FE-001…005): router flag, codegen, cache remap, fragment sweep, dynamic-gql expansion.
2. **Wave 1 — Watchlist pilot**: smallest isolated domain proves the stack.
3. **Wave 2 — Product Details, Measurement, Packaging**: parallelizable medium domains.
4. **Wave 3 — BOM, Claims**: saga writes; first cross-subgraph cutover (claims).
5. **Wave 4 — Product (+ Impression riders)**: largest surface, incremental slices.

## Rules of engagement

- A frontend story is Done only after every backend story it depends on has been delivered ([dependency matrix](../frontend-analysis/09-story-dependency-matrix.md)).
- Cross-domain documents migrate with the later of their two domains — no interim splits unless a wave gap forces one.
- Every flag flip is preceded by a dual-run comparison and accompanied by a cache reset.

## Jira import

- Per-domain CSVs: `output/jira/frontend/{domain}-fe.csv`.
- Full import: `output/jira/frontend/all-frontend-stories.csv` (includes the frontend epic).
- All frontend stories hang off the epic "Federate BreakDown Product — Frontend".

## Regeneration

- Generated docs (01–04, 09, 11, Jira CSVs) rebuild via `python fedMigrationScripts/generatescripts/generate_frontend.py` (also runs inside `generate_all.py`).
- Hand-authored docs (00, 05–08, 10, this page) are never overwritten by the pipeline.
- Source repo: `https://github.com/XXX`.
