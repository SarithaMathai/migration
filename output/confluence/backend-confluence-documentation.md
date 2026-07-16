# Federated GraphQL Migration — Backend Documentation

> Confluence-ready page · 2026-07-16 · Scope: the 8 phase-1 domains
> Companion page: [Frontend Documentation](./frontend-confluence-documentation.md)
> Backend stories are referenced here, never duplicated — the per-domain breakdown pages are the source of truth.

## Purpose

- Index page for the spark-internal-graphql → Netflix DGS federated migration backend deliverables.
- Audience: Engineers implementing backend stories; Product Owner tracking scope and sequencing.

## Program shape

- 200 build stories across 8 domains + 7 program spikes, under the single epic "Federate BreakDown Product".
- Subgraph targets: `plm-product` hosts product, bom, measurement, productDetails, packaging, watchlist, impression; `spark-claims` is a separate subgraph for claims.
- Story id format: `<DOMAIN>-BE-<phase>-<NN>` (phases B core reads · C search/listing · D mutations · E complex · F federation contributions · G field resolvers & tests).

## Per-domain breakdown pages (source of truth)

| Domain | Breakdown page | Stories source |
|---|---|---|
| Product | `output/summary/product/FederatedGqlBrakDown-product.md` (+ .docx) | `output/initial-analysis/product/04-stories.md` |
| BOM | `output/summary/bom/FederatedGqlBrakDown-bom.md` | `output/initial-analysis/bom/04-stories.md` |
| Measurement | `output/summary/measurement/FederatedGqlBrakDown-measurement.md` | `output/initial-analysis/measurement/04-stories.md` |
| Product Details | `output/summary/productDetails/FederatedGqlBrakDown-productDetails.md` | `output/initial-analysis/productDetails/04-stories.md` |
| Packaging | `output/summary/packaging/FederatedGqlBrakDown-packaging.md` | `output/initial-analysis/packaging/04-stories.md` |
| Watchlist | `output/summary/watchlist/FederatedGqlBrakDown-watchlist.md` | `output/initial-analysis/watchlist/04-stories.md` |
| Impression | `output/summary/impression/FederatedGqlBrakDown-impression.md` | `output/initial-analysis/impression/04-stories.md` |
| Claims | `output/summary/claims/FederatedGqlBrakDown-claims.md` | `output/initial-analysis/claims/04-stories.md` |

- Program overview (all domains, effort, sequencing): `output/summary/00-program-overview.md`.
- Global breakdown: `output/summary/Federated+Graphql+Stories+-+BreakDown.md` (+ .docx).

## Frontend dependency view

- 43 frontend stories depend on backend stories; the frontend is not Done until its backend dependencies deliver.
- Which backend story blocks which frontend story: [09-story-dependency-matrix.md](../frontend-analysis/09-story-dependency-matrix.md) (reverse index included).
- Backend root fields with **no frontend caller** (deprecation-review candidates): [03-merged-inventory.md §Unused backend operations](../frontend-analysis/03-merged-inventory.md).
- Phase-1 schema fields never selected by the frontend (consolidation input for federated schema derivation): same document, §Unused schema fields.

## Open decisions (program spikes)

- SPIKE-01…SPIKE-06b track the program-level decisions; scenario ADRs are drafted per complex case under `output/complexStories/`.
- Status convention: 🟠 Draft ADR proposed — ratification pending (06a remains 🔴 Open).
- Frontend stories gated on these decisions are listed in [10-migration-sequencing.md §External gates](../frontend-analysis/10-migration-sequencing.md).

## Jira import

- Per-domain CSVs: `output/jira/{domain}.csv`.
- Full import: `output/jira/all-stories.csv` (epic + 200 stories + 7 program spikes).

## Regeneration

- All backend summary/Jira artifacts rebuild via `python fedMigrationScripts/generatescripts/generate_all.py`.
- Source repo: `https://github.com/XXX`.
