## MST-FE-001 — Migrate measurement reads and retire `humanId`
Queries in scope: getMeasurementByIds, getMeasurementSetStatus, getMeasurementComponentStatus · Mutations excluded: 0

**Must complete first:** BE — MST-BE-B-01, MST-BE-B-04, MST-BE-G-01, MST-BE-G-07 · New — NEW-MST-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getMeasurementByIds | MST-BE-B-01 | — | — | No | getMeasurementByIds, getMeasurementComponentStatus |  |
| getMeasurementSetStatus | MST-BE-B-04 | — | — | No | getMeasurementSetStatus |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| measurementTemplateFragment | NEW-MST-BE-G-?? | — | — | Yes | getMeasurementByIds | fragment body not found in snapshot |
| sizeTemplateFragmentWithRows | NEW-MST-BE-G-?? | — | — | Yes | getMeasurementByIds | fragment body not found in snapshot |
| brands | MST-BE-G-07 | vmm | — | No | getMeasurementByIds | via `...tightFitFragment` |
| businessPartners | MST-BE-G-01 | vmm | — | No | getMeasurementByIds | via `...measurementFieldsFragment` |
| createdBy | MST-BE-G-07 | user-profile | — | No | getMeasurementByIds | via `...measurementFieldsFragment`; via `...tightFitFragment` |
| departments | MST-BE-G-07 | ig | — | No | getMeasurementByIds | via `...tightFitFragment` |
| divisions | MST-BE-G-07 | ig | — | No | getMeasurementByIds | via `...tightFitFragment` |
| measurementTemplates | MST-BE-G-01 | measurementTemplate | — | No | getMeasurementByIds | via `...measurementFieldsFragment` |
| participantDetails | MST-BE-G-01 | user-profile | — | No | getMeasurementByIds | via `...measurementFieldsFragment` |
| sizeTemplate | MST-BE-G-01 | sizeTemplate | — | No | getMeasurementByIds | via `...measurementFieldsFragment` |
| teams | MST-BE-G-01 | user-profile | — | No | getMeasurementByIds | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| tightFitTemplate | MST-BE-G-01 | tightFit | — | No | getMeasurementByIds | via `...measurementFieldsFragment` |
| updatedBy | MST-BE-G-07 | user-profile | — | No | getMeasurementByIds | via `...measurementFieldsFragment`; via `...tightFitFragment` |
| updatedFromResource | MST-BE-G-01 | sampleV2 | — | No | getMeasurementByIds | via `...measurementFieldsFragment` |
| users | MST-BE-G-01 | user-profile | — | No | getMeasurementByIds | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| workspaces | MST-BE-G-01 | workspaceV2 | — | No | getMeasurementByIds | via `...measurementFieldsFragment` |

## MST-FE-001 — Readiness
21 of 23 distinct fields/entities resolve to existing backend stories. 2 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
