## CLAIM-FE-002 — Migrate claim reads (first cross-subgraph cutover)
Queries in scope: getClaims, getClaimByIds, getCommunicationChannels, getAllClaimsAbout, getClaimComponentStatus · Mutations excluded: 0

**Must complete first:** BE — CLAIM-BE-B-01, CLAIM-BE-B-02, CLAIM-BE-B-03, CLAIM-BE-B-04, CLAIM-BE-G-01, CLAIM-BE-G-02, CLAIM-BE-G-03

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getAllClaimsAbout | CLAIM-BE-B-04 | — | — | No | getAllClaimsAbout, getClaimByIds, getClaims |  |
| getClaimByIds | CLAIM-BE-B-02 | — | — | No | getAllClaimsAbout, getClaimByIds, getClaimComponentStatus |  |
| getClaims | CLAIM-BE-B-01 | — | — | No | getAllClaimsAbout, getClaims |  |
| getCommunicationChannels | CLAIM-BE-B-03 | — | — | No | getAllClaimsAbout, getClaimByIds, getClaims, getCommunicationChannels |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| businessPartner | CLAIM-BE-G-02 | vmm | — | No | getAllClaimsAbout, getClaimByIds | via `...FullClaimDetailsFragment` |
| createdBy | CLAIM-BE-G-02 | user-profile | — | No | getAllClaimsAbout, getClaimByIds, getClaims | via `...FullClaimDetailsFragment` |
| designPartner | CLAIM-BE-G-02 | vmm | — | No | getAllClaimsAbout, getClaimByIds | via `...FullClaimDetailsFragment` |
| parentDetails | CLAIM-BE-G-03 | product | — | No | getAllClaimsAbout, getClaimByIds | via `...FullClaimDetailsFragment` |
| participantDetails | CLAIM-BE-G-01 | user-profile | — | No | getAllClaimsAbout, getClaimByIds | via `...FullClaimDetailsFragment` |
| product | CLAIM-BE-G-03 | product | — | No | getAllClaimsAbout, getClaimByIds | via `...FullClaimDetailsFragment` |
| teams | CLAIM-BE-G-01 | user-profile | — | No | getAllClaimsAbout, getClaimByIds | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| updatedBy | CLAIM-BE-G-02 | user-profile | — | No | getAllClaimsAbout, getClaimByIds, getClaims | via `...FullClaimDetailsFragment` |
| users | CLAIM-BE-G-01 | user-profile | — | No | getAllClaimsAbout, getClaimByIds | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |

## CLAIM-FE-002 — Readiness
All 17 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
