# Federation Schema Review — Deliverables Index

> Federated GraphQL schema migration analysis (Copilot instruction run) · Generated: 2026-07-17
> Scope: the 8 phase-1 domains (product, bom, measurement, impression, packaging, productDetails, watchlist, claims).
> Companion to the per-domain analyses in `output/analysis/{domain}/` and the program FE docs in `output/analysis/program/`.

| # | Document | Instruction deliverable(s) covered |
|---|----------|-----------------------------------|
| 01 | [Schema validation report](./01-schema-validation-report.md) | Current schema validation report |
| 02 | [Federation candidates](./02-federation-candidates.md) | Cross-domain identifier inventory (owning domain, referenced domain, current/expected type) |
| 03 | [Proposed schema changes](./03-proposed-schema-changes.md) | Proposed federated schema · schema diff report |
| 04 | [Entity analysis](./04-entity-analysis.md) | Federation entity analysis · entity resolver recommendations |
| 05 | [Backend impact](./05-backend-impact.md) | Backend impact analysis · updated Backend Jira stories |
| 06 | [Frontend impact](./06-frontend-impact.md) | Frontend impact analysis · updated Frontend Jira stories |
| 07 | [Story validation & sequencing](./07-story-validation-and-sequencing.md) | Dependency matrix · implementation roadmap · story dispositions |
| 08 | [Risks, assumptions, open questions](./08-risks-assumptions-questions.md) | Risks, assumptions, and unresolved questions |

## Headline findings

- The 8 `be-03-schema.graphql` files are the authoritative federated target schemas; no competing versions exist.
- The schemas already model cross-domain references as entities — **no wholesale ID→entity rewrite is needed**. The remaining primitive IDs are overwhelmingly deliberate (dual id+object pairs, input types, UI gating lists, search projections).
- **5 required fixes** were found — all cross-subgraph contract mismatches that would break supergraph composition, not missing entity conversions (see 03 §1 and 04 §3).
- **6 recommended additive fields** (id kept, object added) and a set of optional ones — all PO-gated (see 03 §2–3).
- 4 new required BE stories + 5 recommended BE stories + 2 FE stories were added to the story inventories; Jira CSVs regenerate from those sources via `fedMigrationScripts/generatescripts/generate_all.py`.
