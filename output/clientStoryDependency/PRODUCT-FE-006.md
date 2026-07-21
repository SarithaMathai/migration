## PRODUCT-FE-006 — Migrate `getCategories` documents
Queries in scope: getCategories · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-C-03, PRODUCT-BE-G-04, PRODUCT-BE-H-07, PRODUCT-BE-S-02

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getCategories | PRODUCT-BE-C-03 | — | — | No | getCategories |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| categories | PRODUCT-BE-G-04 | IG | — | No | getCategories |  |
| IG_Clazz_Filter | PRODUCT-BE-H-07 | ig | PRODUCT-BE-H-07 | No | getCategories | newly authored — PRODUCT-BE-H-07 |

## PRODUCT-FE-006 — Readiness
All 4 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
