## MST-FE-003 — Migrate measurement master-data reads
Queries in scope: getUnitsOfMeasure, getThicknessUnitsOfMeasure · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-G-15, MST-BE-B-02, MST-BE-B-03, MST-BE-B-04 · New — NEW-MST-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getThicknessUnitsOfMeasure | MST-BE-B-03 | — | — | No | getThicknessUnitsOfMeasure |  |
| getUnitsOfMeasure | MST-BE-B-02 | — | — | No | getThicknessUnitsOfMeasure, getUnitsOfMeasure |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| shortDescription | NEW-MST-BE-G-?? | — | — | Yes | getThicknessUnitsOfMeasure, getUnitsOfMeasure |  |

## MST-FE-003 — Readiness
4 of 5 distinct fields/entities resolve to existing backend stories. 1 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
