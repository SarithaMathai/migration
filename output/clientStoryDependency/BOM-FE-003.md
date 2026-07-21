## BOM-FE-003 — Migrate BOM search and elastic reads
Queries in scope: getBomElastic, searchMaterialsBom · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-C-01, BOM-BE-G-01, BOM-BE-G-14, BOM-BE-S-03

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getBomElastic | BOM-BE-C-01 | — | — | No | getBomElastic |  |
| searchMaterialsBom | BOM-BE-S-03 | — | — | No | searchMaterialsBom |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| businessPartners | BOM-BE-G-01 | vmm | — | No | getBomElastic |  |

## BOM-FE-003 — Readiness
All 5 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
