## PRODUCT-FE-005 — Migrate template library and categories reads
Queries in scope: getProductTemplates, getCategories · Mutations excluded: 0

**Must complete first:** BE — CLAIM-BE-B-01, CLAIM-BE-G-01, CLAIM-BE-G-02, CLAIM-BE-G-03, CLAIM-BE-G-04, PRODUCT-BE-C-02, PRODUCT-BE-C-03, PRODUCT-BE-G-03, PRODUCT-BE-G-04, PRODUCT-BE-G-06, PRODUCT-BE-G-08, PRODUCT-BE-G-13, PRODUCT-BE-H-07, PRODUCT-BE-S-02 · New — NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getCategories | PRODUCT-BE-C-03 | — | — | No | getCategories |  |
| getProductTemplates | PRODUCT-BE-C-02 | — | — | No | getProductTemplates |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| access | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProductTemplates |  |
| additionalInfo | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProductTemplates | via `...FullClaimDetailsFragment` |
| claimDetails | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProductTemplates | via `...FullClaimDetailsFragment` |
| claimNotes | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProductTemplates | via `...FullClaimDetailsFragment` |
| parentId | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProductTemplates | via `...FullClaimDetailsFragment` |
| users | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProductTemplates | via `...LegacyComponentDiscussionParticipantsFragment` |
| attachmentsV3 | PRODUCT-BE-G-03 | attachment | — | No | getProductTemplates |  |
| brands | PRODUCT-BE-G-13 | ig | — | No | getProductTemplates | via `...productTemplateDetails` |
| businessPartner | CLAIM-BE-G-02 | vmm | — | No | getProductTemplates | cross-domain: `Claims` owned by `claims`; via `...FullClaimDetailsFragment` |
| categories | PRODUCT-BE-G-04 | IG | — | No | getCategories |  |
| createdBy | CLAIM-BE-G-02 | user-profile | — | No | getProductTemplates | cross-domain: `Claims` owned by `claims`; via `...FullClaimDetailsFragment` |
| designPartner | CLAIM-BE-G-02 | vmm | — | No | getProductTemplates | cross-domain: `Claims` owned by `claims`; via `...FullClaimDetailsFragment` |
| divisions | PRODUCT-BE-G-13 | ig | — | No | getProductTemplates | via `...productTemplateDetails` |
| IG_Clazz_Filter | PRODUCT-BE-H-07 | ig | PRODUCT-BE-H-07 | No | getCategories | newly authored — PRODUCT-BE-H-07 |
| parentDetails | CLAIM-BE-G-03 | product | — | No | getProductTemplates | cross-domain: `Claims` owned by `claims`; via `...FullClaimDetailsFragment` |
| participantDetails | CLAIM-BE-G-01 | user-profile | — | No | getProductTemplates | cross-domain: `Claims` owned by `claims`; via `...FullClaimDetailsFragment` |
| product | CLAIM-BE-G-03 | product | — | No | getProductTemplates | cross-domain: `Claims` owned by `claims`; via `...FullClaimDetailsFragment` |
| productTemplateDepartments | PRODUCT-BE-G-13 | ig | — | No | getProductTemplates | via `...productTemplateDetails` |
| tags | PRODUCT-BE-G-13 | tag | — | No | getProductTemplates | via `...productTemplateDetails` |
| teams | PRODUCT-BE-G-06 | teamV2 | — | No | getProductTemplates | via `...LegacyComponentDiscussionParticipantsFragment` |
| updatedBy | CLAIM-BE-G-02 | user-profile | — | No | getProductTemplates | cross-domain: `Claims` owned by `claims`; via `...FullClaimDetailsFragment` |

## PRODUCT-FE-005 — Readiness
28 of 34 distinct fields/entities resolve to existing backend stories. 6 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
