## PKG-FE-003 — Migrate dieline flows
Queries in scope: getDielines, getDielineEvaluationStatuses · Mutations excluded: 1

**Must complete first:** BE — PKG-BE-B-03, PKG-BE-B-05, PKG-BE-G-05

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getDielineEvaluationStatuses | PKG-BE-B-05 | — | — | No | getDielineEvaluationStatuses |  |
| getDielines | PKG-BE-B-03 | — | — | No | getDielines |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| attachment | PKG-BE-G-05 | attachment | — | No | getDielines |  |
| attachments | PKG-BE-G-05 | search | — | No | getDielines |  |
| evaluatedBy | PKG-BE-G-05 | user-profile | — | No | getDielines |  |

## PKG-FE-003 — Readiness
All 5 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
