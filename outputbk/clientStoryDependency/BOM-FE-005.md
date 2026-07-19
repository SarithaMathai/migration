## BOM-FE-005 — Migrate BOM supplier reads
Queries in scope: getComboSupplierForBom, getValidTrimSuppliersForBom, getValidRawMaterialSuppliersForBom · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-C-03, BOM-BE-C-04, BOM-BE-C-05

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getComboSupplierForBom | BOM-BE-C-03 | — | No | getComboSupplierForBom |  |
| getValidRawMaterialSuppliersForBom | BOM-BE-C-05 | — | No | getValidRawMaterialSuppliersForBom, getValidTrimSuppliersForBom |  |
| getValidTrimSuppliersForBom | BOM-BE-C-04 | — | No | getValidRawMaterialSuppliersForBom, getValidTrimSuppliersForBom |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|

## BOM-FE-005 — Readiness
All 3 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
