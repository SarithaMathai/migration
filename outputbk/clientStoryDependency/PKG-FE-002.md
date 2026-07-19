## PKG-FE-002 — Migrate packaging master-data reads and retire deprecated fields
Queries in scope: getCountries, getPackagingFieldValuesByType · Mutations excluded: 0

**Must complete first:** BE — PKG-BE-B-04, PKG-BE-B-06

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getCountries | PKG-BE-B-06 | — | No | getCountries |  |
| getPackagingFieldValuesByType | PKG-BE-B-04 | — | No | getPackagingFieldValuesByType |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|

## PKG-FE-002 — Readiness
All 2 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
