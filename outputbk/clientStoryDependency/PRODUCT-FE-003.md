## PRODUCT-FE-003 — Migrate product list and bulk reads
Queries in scope: getProducts, getProductsByIds · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-B-02, PRODUCT-BE-B-03, PRODUCT-BE-G-13, PRODUCT-BE-S-02 · New — NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getProducts | PRODUCT-BE-S-02 | — | No | getProducts |  |
| getProductsByIds | PRODUCT-BE-B-02 | — | No | getProductsByIds |  |
| getProductStatus | PRODUCT-BE-B-03 | — | No | getProductsByIds |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| roles | NEW-PRODUCT-BE-G-?? | — | Yes | getProductsByIds |  |
| departments | PRODUCT-BE-G-13 | ig | No | getProductsByIds |  |

## PRODUCT-FE-003 — Readiness
4 of 5 distinct fields/entities resolve to existing backend stories. 1 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
