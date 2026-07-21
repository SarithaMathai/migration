## PRODUCT-FE-003 — Migrate `getProductsByIds` documents (bulk-by-id reads)
Queries in scope: getProductsByIds · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-B-02, PRODUCT-BE-B-03, PRODUCT-BE-G-13 · New — NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getProductsByIds | PRODUCT-BE-B-02 | — | — | No | getProductsByIds |  |
| getProductStatus | PRODUCT-BE-B-03 | — | — | No | getProductsByIds |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| roles | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProductsByIds |  |
| departments | PRODUCT-BE-G-13 | ig | — | No | getProductsByIds |  |

## PRODUCT-FE-003 — Readiness
3 of 4 distinct fields/entities resolve to existing backend stories. 1 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
