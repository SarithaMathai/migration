## BOM-FE-005 — Migrate BOM supplier reads
Queries in scope: getComboSupplierForBom, getValidTrimSuppliersForBom, getValidRawMaterialSuppliersForBom · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-C-03, BOM-BE-C-04, BOM-BE-C-05

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getComboSupplierForBom | BOM-BE-C-03 | — | — | No | getComboSupplierForBom |  |
| getValidRawMaterialSuppliersForBom | BOM-BE-C-05 | — | — | No | getValidRawMaterialSuppliersForBom, getValidTrimSuppliersForBom |  |
| getValidTrimSuppliersForBom | BOM-BE-C-04 | — | — | No | getValidRawMaterialSuppliersForBom, getValidTrimSuppliersForBom |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|

## BOM-FE-005 — Readiness
All 3 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
