## PRODUCT-FE-011 — Migrate TechPack count queries (facade-then-federate)
Queries in scope: getProductTechPackCountV1, getProductTechPackBulkCountV1 · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-E-03, PRODUCT-BE-E-04, PRODUCT-BE-F-06, PRODUCT-BE-F-08, PRODUCT-BE-G-08, PRODUCT-BE-H-01, PRODUCT-BE-H-02, PRODUCT-BE-H-03, PRODUCT-BE-H-05

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getProductTechPackBulkCountV1 | PRODUCT-BE-E-04 | — | — | No | getProductTechPackBulkCountV1 |  |
| getProductTechPackCountV1 | PRODUCT-BE-E-03 | — | — | No | getProductTechPackCountV1 |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|

## PRODUCT-FE-011 — Readiness
All 12 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
