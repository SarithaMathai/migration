## IMPRESSION-FE-001 — Migrate `getBomDataAndImpressions` (with BOM wave)
Queries in scope: searchImpressionsByProductId, getBomByIds · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-A-04, BOM-BE-B-01, BOM-BE-G-01, IMPRESSION-BE-B-01, IMPRESSION-BE-G-01, PRODUCT-BE-B-01 · New — NEW-BOM-BE-G-??, NEW-IMPRESSION-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getBomByIds | BOM-BE-B-01 | — | No | getBomByIds, searchImpressionsByProductId |  |
| getProduct | PRODUCT-BE-B-01 | — | No | searchImpressionsByProductId |  |
| searchImpressionsByProductId | IMPRESSION-BE-B-01 | — | No | searchImpressionsByProductId |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| components | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| department | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| departments | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| description | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| designPartnerId | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| droppedPartnerIds | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| droppedPartners | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| ImpressionFragment | NEW-BOM-BE-G-?? | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| productWorkspaceInfo | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| teams | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| thumbnailId | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| access | BOM-BE-G-01 | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| businessPartners | IMPRESSION-BE-G-01 | vmm | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| createdBy | BOM-BE-G-01 | user-profile | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| currentUserPermissions | BOM-BE-G-01 | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| humanId | BOM-BE-G-01 | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| materials | BOM-BE-A-04 | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| participantDetails | BOM-BE-G-01 | user-profile | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| product | BOM-BE-G-01 | — | No | getBomByIds |  |
| updatedBy | BOM-BE-G-01 | user-profile | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| workspaces | BOM-BE-G-01 | workspaceV2 | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |

## IMPRESSION-FE-001 — Readiness
13 of 24 distinct fields/entities resolve to existing backend stories. 11 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored.
