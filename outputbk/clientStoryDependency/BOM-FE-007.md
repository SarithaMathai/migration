## BOM-FE-007 — Adopt BOM `supplier` entity references (optional, PO-gated)
Queries in scope: getBomByIds, getBomByParentId, searchMaterialsBom · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-A-04, BOM-BE-B-01, BOM-BE-B-04, BOM-BE-G-01, BOM-BE-G-14, BOM-BE-S-03

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getBomByIds | BOM-BE-B-01 | — | No | getBomByIds |  |
| getBomByParentId | BOM-BE-B-04 | — | No | getBomByParentId |  |
| searchMaterialsBom | BOM-BE-S-03 | — | No | searchMaterialsBom |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| access | BOM-BE-G-01 | — | No | getBomByIds | via `...BomDetails` |
| businessPartners | BOM-BE-G-01 | vmm | No | getBomByIds | via `...BomDetails` |
| createdBy | BOM-BE-G-01 | user-profile | No | getBomByIds | via `...BomDetails` |
| currentUserPermissions | BOM-BE-G-01 | — | No | getBomByIds | via `...BomDetails` |
| humanId | BOM-BE-G-01 | — | No | getBomByIds | via `...BomDetails` |
| materials | BOM-BE-A-04 | — | No | getBomByIds | via `...BomDetails` |
| paging | BOM-BE-G-14 | — | No | searchMaterialsBom |  |
| participantDetails | BOM-BE-G-01 | user-profile | No | getBomByIds | via `...BomDetails` |
| product | BOM-BE-G-01 | — | No | getBomByIds |  |
| updatedBy | BOM-BE-G-01 | user-profile | No | getBomByIds | via `...BomDetails` |
| workspaces | BOM-BE-G-01 | workspaceV2 | No | getBomByIds | via `...BomDetails` |

## BOM-FE-007 — Readiness
All 14 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
