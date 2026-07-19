## PRODUCT-FE-005 — Migrate template library and categories reads
Queries in scope: getProductTemplates, getCategories · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-C-02, PRODUCT-BE-C-03, PRODUCT-BE-G-04

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getCategories | PRODUCT-BE-C-03 | — | No | getCategories |  |
| getProductTemplates | PRODUCT-BE-C-02 | — | No | getProductTemplates |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| categories | PRODUCT-BE-G-04 | IG | No | getCategories |  |

## PRODUCT-FE-005 — Readiness
All 3 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
