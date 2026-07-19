## MST-FE-002 — Migrate measurement list/search reads
Queries in scope: getMeasurements, getMeasurementsElastic · Mutations excluded: 0

**Must complete first:** BE — MST-BE-B-01, MST-BE-C-01, MST-BE-C-02

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getMeasurements | MST-BE-C-01 | — | No | getMeasurements |  |
| getMeasurementsElastic | MST-BE-C-02 | — | No | getMeasurementsElastic |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| content | MST-BE-B-01 | — | No | getMeasurements, getMeasurementsElastic |  |

## MST-FE-002 — Readiness
All 3 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
