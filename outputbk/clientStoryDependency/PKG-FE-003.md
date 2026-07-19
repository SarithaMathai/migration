## PKG-FE-003 — Migrate dieline flows
Queries in scope: getDielines, getDielineEvaluationStatuses · Mutations excluded: 1

**Must complete first:** BE — PKG-BE-B-03, PKG-BE-B-05, PKG-BE-G-05

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getDielineEvaluationStatuses | PKG-BE-B-05 | — | No | getDielineEvaluationStatuses |  |
| getDielines | PKG-BE-B-03 | — | No | getDielines |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| attachment | PKG-BE-G-05 | attachment | No | getDielines |  |
| attachments | PKG-BE-G-05 | search | No | getDielines |  |
| evaluatedBy | PKG-BE-G-05 | user-profile | No | getDielines |  |

## PKG-FE-003 — Readiness
All 5 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
