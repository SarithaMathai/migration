## PDTL-FE-001 — Migrate product-details reads
Queries in scope: getProductDetailsById, getProductDetailComponentStatus · Mutations excluded: 0

**Must complete first:** BE — PDTL-BE-B-01, PDTL-BE-G-01, PDTL-BE-G-02, PDTL-BE-G-03

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getProductDetailsById | PDTL-BE-B-01 | — | No | getProductDetailComponentStatus, getProductDetailsById |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| access | PDTL-BE-G-01 | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| attachment | PDTL-BE-G-03 | search | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| businessPartners | PDTL-BE-G-02 | vmm | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| createdBy | PDTL-BE-G-02 | user-profile | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| currentUserPermissions | PDTL-BE-G-01 | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| participantDetails | PDTL-BE-G-01 | user-profile | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| product | PDTL-BE-G-02 | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| status | PDTL-BE-B-01 | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| statuses | PDTL-BE-B-01 | — | No | getProductDetailComponentStatus |  |
| updatedBy | PDTL-BE-G-02 | user-profile | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| workspaces | PDTL-BE-G-02 | workspaceV2 | No | getProductDetailsById | via `...ProductDetailsDataFragment` |

## PDTL-FE-001 — Readiness
All 12 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
