## MST-FE-001 — Migrate measurement reads and retire `humanId`
Queries in scope: getMeasurementByIds, getMeasurementSetStatus, getMeasurementComponentStatus · Mutations excluded: 0

**Must complete first:** BE — MST-BE-B-01, MST-BE-B-04

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getMeasurementByIds | MST-BE-B-01 | — | No | getMeasurementByIds, getMeasurementComponentStatus |  |
| getMeasurementSetStatus | MST-BE-B-04 | — | No | getMeasurementSetStatus |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| content | MST-BE-B-01 | — | No | getMeasurementByIds, getMeasurementComponentStatus |  |

## MST-FE-001 — Readiness
All 3 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
