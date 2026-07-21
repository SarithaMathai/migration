## MST-FE-002 — Migrate measurement list/search reads
Queries in scope: getMeasurements, getMeasurementsElastic · Mutations excluded: 0

**Must complete first:** BE — MST-BE-B-01, MST-BE-C-01, MST-BE-C-02, MST-BE-G-01, MST-BE-G-07 · New — NEW-MST-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getMeasurements | MST-BE-C-01 | — | — | No | getMeasurements |  |
| getMeasurementsElastic | MST-BE-C-02 | — | — | No | getMeasurementsElastic |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| measurementTemplateFragment | NEW-MST-BE-G-?? | — | — | Yes | getMeasurements | fragment body not found in snapshot |
| sizeTemplateFragmentWithRows | NEW-MST-BE-G-?? | — | — | Yes | getMeasurements | fragment body not found in snapshot |
| brands | MST-BE-G-07 | vmm | — | No | getMeasurements | via `...tightFitFragment` |
| businessPartners | MST-BE-G-01 | vmm | — | No | getMeasurements | via `...measurementFieldsFragment` |
| createdBy | MST-BE-G-07 | user-profile | — | No | getMeasurements | via `...measurementFieldsFragment`; via `...tightFitFragment` |
| departments | MST-BE-G-07 | ig | — | No | getMeasurements | via `...tightFitFragment` |
| divisions | MST-BE-G-07 | ig | — | No | getMeasurements | via `...tightFitFragment` |
| participantDetails | MST-BE-G-01 | user-profile | — | No | getMeasurements | via `...measurementFieldsFragment` |
| teams | MST-BE-G-01 | user-profile | — | No | getMeasurements | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| updatedBy | MST-BE-G-07 | user-profile | — | No | getMeasurements | via `...measurementFieldsFragment`; via `...tightFitFragment` |
| updatedFromResource | MST-BE-G-01 | sampleV2 | — | No | getMeasurements | via `...measurementFieldsFragment` |
| users | MST-BE-G-01 | user-profile | — | No | getMeasurements | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| workspaces | MST-BE-G-01 | workspaceV2 | — | No | getMeasurements | via `...measurementFieldsFragment` |

## MST-FE-002 — Readiness
21 of 23 distinct fields/entities resolve to existing backend stories. 2 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
