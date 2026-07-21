## BOM-FE-004 — Migrate BOM master-data reads
Queries in scope: getBomMaterialTypes, getBomPackagingMaterialTypes, getBomPackagingSubstrates, getBomPackagingUnitOfMeasure · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-B-05, BOM-BE-B-06, BOM-BE-B-07, BOM-BE-B-08, BOM-BE-G-14 · New — NEW-BOM-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getBomMaterialTypes | BOM-BE-B-05 | — | — | No | getBomMaterialTypes |  |
| getBomPackagingMaterialTypes | BOM-BE-B-06 | — | — | No | getBomPackagingMaterialTypes, getBomPackagingUnitOfMeasure |  |
| getBomPackagingSubstrates | BOM-BE-B-07 | — | — | No | getBomPackagingSubstrates |  |
| getBomPackagingUnitOfMeasure | BOM-BE-B-08 | — | — | No | getBomPackagingMaterialTypes, getBomPackagingUnitOfMeasure |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| shortDescription | NEW-BOM-BE-G-?? | — | — | Yes | getBomPackagingMaterialTypes, getBomPackagingUnitOfMeasure |  |

## BOM-FE-004 — Readiness
5 of 6 distinct fields/entities resolve to existing backend stories. 1 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
