## PRODUCT-FE-002 — Migrate `getProducts` documents (list/search/bulk-create)
Queries in scope: getProducts · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-S-02

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getProducts | PRODUCT-BE-S-02 | — | — | No | getProducts |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|

## PRODUCT-FE-002 — Readiness
All 1 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
