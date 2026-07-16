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
| Product | `output/summary/FederatedGqlBrakDown-BE-product.md` (+ .docx) | `output/analysis/product/be-04-stories.md` |
| BOM | `output/summary/FederatedGqlBrakDown-BE-bom.md` | `output/analysis/bom/be-04-stories.md` |
| Measurement | `output/summary/FederatedGqlBrakDown-BE-measurement.md` | `output/analysis/measurement/be-04-stories.md` |
| Product Details | `output/summary/FederatedGqlBrakDown-BE-productDetails.md` | `output/analysis/productDetails/be-04-stories.md` |
| Packaging | `output/summary/FederatedGqlBrakDown-BE-packaging.md` | `output/analysis/packaging/be-04-stories.md` |
| Watchlist | `output/summary/FederatedGqlBrakDown-BE-watchlist.md` | `output/analysis/watchlist/be-04-stories.md` |
| Impression | `output/summary/FederatedGqlBrakDown-BE-impression.md` | `output/analysis/impression/be-04-stories.md` |
| Claims | `output/summary/FederatedGqlBrakDown-BE-claims.md` | `output/analysis/claims/be-04-stories.md` |

- Program overview (all domains, effort, sequencing): `output/summary/00-program-overview.md`.
- Global breakdown: `output/summary/Federated+Graphql+Stories+-+BreakDown.md` (+ .docx).

## Frontend dependency view

- 38 frontend stories depend on backend stories; the frontend is not Done until its backend dependencies deliver.
- Which backend story blocks which frontend story: [fe-09-story-dependency-matrix.md](../analysis/program/fe-09-story-dependency-matrix.md) (reverse index included).
- Backend root fields with **no frontend caller** (deprecation-review candidates): [fe-03-merged-inventory.md §Unused backend operations](../analysis/program/fe-03-merged-inventory.md).
- Phase-1 schema fields never selected by the frontend (consolidation input for federated schema derivation): same document, §Unused schema fields.

## Open decisions (program spikes)

- SPIKE-01…SPIKE-06b track the program-level decisions; scenario ADRs are drafted per complex case under `output/complexStories/`.
- Status convention: 🟠 Draft ADR proposed — ratification pending (06a remains 🔴 Open).
- Frontend stories gated on these decisions are listed in [fe-10-migration-sequencing.md §External gates](../analysis/program/fe-10-migration-sequencing.md).

## Jira import

- Per-domain CSVs: `output/jira/{domain}.csv` — **combined**: the domain's backend AND frontend stories (both epics) in one file.
- Backend-only full import: `output/jira/all-stories.csv` (epic + 200 stories + 7 program spikes); frontend-only: `output/jira/all-frontend-stories.csv`.
- Per-domain push prompts: `fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md` §1.

## Regeneration

- All backend summary/Jira artifacts rebuild via `python fedMigrationScripts/generatescripts/generate_all.py`.
- Source repo: `https://github.com/XXX`.
