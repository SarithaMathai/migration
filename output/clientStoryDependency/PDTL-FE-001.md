## PDTL-FE-001 — Migrate product-details reads
Queries in scope: getProductDetailsById, getProductDetailComponentStatus · Mutations excluded: 0

**Must complete first:** BE — PDTL-BE-B-01, PDTL-BE-G-01, PDTL-BE-G-02, PDTL-BE-G-03

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getProductDetailsById | PDTL-BE-B-01 | — | — | No | getProductDetailComponentStatus, getProductDetailsById |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| attachment | PDTL-BE-G-03 | search | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| businessPartners | PDTL-BE-G-02 | vmm | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| createdBy | PDTL-BE-G-02 | user-profile | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| participantDetails | PDTL-BE-G-01 | user-profile | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| teams | PDTL-BE-G-01 | user-profile | — | No | getProductDetailsById | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| updatedBy | PDTL-BE-G-02 | user-profile | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |
| users | PDTL-BE-G-01 | user-profile | — | No | getProductDetailsById | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| workspaces | PDTL-BE-G-02 | workspaceV2 | — | No | getProductDetailsById | via `...ProductDetailsDataFragment` |

## PDTL-FE-001 — Readiness
All 14 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
