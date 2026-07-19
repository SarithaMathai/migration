## BOM-FE-002 — Migrate BOM core reads
Queries in scope: getBomByIds, getBomByParentId, getBomStatus, getBomComponentStatus · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-A-04, BOM-BE-B-01, BOM-BE-B-03, BOM-BE-B-04, BOM-BE-G-01

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getBomByIds | BOM-BE-B-01 | — | No | getBomByIds, getBomComponentStatus |  |
| getBomByParentId | BOM-BE-B-04 | — | No | getBomByParentId |  |
| getBomStatus | BOM-BE-B-03 | — | No | getBomStatus |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| access | BOM-BE-G-01 | — | No | getBomByIds | via `...BomDetails` |
| businessPartners | BOM-BE-G-01 | vmm | No | getBomByIds | via `...BomDetails` |
| createdBy | BOM-BE-G-01 | user-profile | No | getBomByIds | via `...BomDetails` |
| currentUserPermissions | BOM-BE-G-01 | — | No | getBomByIds | via `...BomDetails` |
| humanId | BOM-BE-G-01 | — | No | getBomByIds, getBomComponentStatus | via `...BomDetails` |
| materials | BOM-BE-A-04 | — | No | getBomByIds | via `...BomDetails` |
| participantDetails | BOM-BE-G-01 | user-profile | No | getBomByIds | via `...BomDetails` |
| product | BOM-BE-G-01 | — | No | getBomByIds |  |
| updatedBy | BOM-BE-G-01 | user-profile | No | getBomByIds | via `...BomDetails` |
| workspaces | BOM-BE-G-01 | workspaceV2 | No | getBomByIds | via `...BomDetails` |

## BOM-FE-002 — Readiness
All 13 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
