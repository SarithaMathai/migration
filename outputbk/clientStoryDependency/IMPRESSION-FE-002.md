## IMPRESSION-FE-002 — Migrate `getCarryForwardFormData` (with Product wave)
Queries in scope: searchImpressionsByProductId, getProduct · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-A-04, BOM-BE-B-01, BOM-BE-G-01, IMPRESSION-BE-B-01, IMPRESSION-BE-G-01, PRODUCT-BE-B-01, PRODUCT-BE-G-01, PRODUCT-BE-G-02, PRODUCT-BE-G-03, PRODUCT-BE-G-06, PRODUCT-BE-G-07, PRODUCT-BE-G-08, PRODUCT-BE-G-09, PRODUCT-BE-G-10, PRODUCT-BE-G-13 · Spikes — SPIKE-04, SPIKE-05 · New — NEW-BOM-BE-G-??, NEW-IMPRESSION-BE-G-??, NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getBomByIds | BOM-BE-B-01 | — | No | searchImpressionsByProductId |  |
| getProduct | PRODUCT-BE-B-01 | — | No | getProduct, searchImpressionsByProductId |  |
| searchImpressionsByProductId | IMPRESSION-BE-B-01 | — | No | searchImpressionsByProductId |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| designPartnerId | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| ImpressionFragment | NEW-BOM-BE-G-?? | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| resourcePermissions | NEW-PRODUCT-BE-G-?? | — | Yes | getProduct |  |
| teams | NEW-IMPRESSION-BE-G-?? | — | Yes | searchImpressionsByProductId |  |
| access | BOM-BE-G-01 | — | No | searchImpressionsByProductId | via `...BomDetails` |
| ancestryProducts | PRODUCT-BE-G-10 | relationship | No | getProduct |  |
| attachments | PRODUCT-BE-G-03 | attachment | No | getProduct |  |
| attachmentsV3 | PRODUCT-BE-G-03 | attachment | No | getProduct |  |
| attachmentsWithMetaData | PRODUCT-BE-G-01 | attachment | No | getProduct |  |
| brand | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| businessPartners | IMPRESSION-BE-G-01 | vmm | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |
| childProducts | PRODUCT-BE-G-10 | relationship | No | getProduct |  |
| claims | PRODUCT-BE-G-08 | — | No | getProduct |  |
| clazz | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| components | PRODUCT-BE-G-02 | search | No | getProduct, searchImpressionsByProductId | 🔬 SPIKE-05 (gated) |
| createdBy | BOM-BE-G-01 | user-profile | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |
| currentUserPermissions | BOM-BE-G-01 | — | No | searchImpressionsByProductId | via `...BomDetails` |
| department | PRODUCT-BE-G-13 | ig | No | getProduct, searchImpressionsByProductId |  |
| departments | PRODUCT-BE-G-13 | ig | No | getProduct, searchImpressionsByProductId |  |
| discussionsV2 | PRODUCT-BE-G-06 | discussion | No | getProduct |  |
| division | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| droppedPartners | PRODUCT-BE-G-07 | vmm | No | getProduct, searchImpressionsByProductId | 🔬 SPIKE-04 (gated) |
| humanId | BOM-BE-G-01 | — | No | searchImpressionsByProductId | via `...BomDetails` |
| materials | BOM-BE-A-04 | — | No | searchImpressionsByProductId | via `...BomDetails` |
| participantDetails | BOM-BE-G-01 | user-profile | No | searchImpressionsByProductId | via `...BomDetails` |
| productWorkspaceInfo | PRODUCT-BE-G-09 | workspaceV2 | No | getProduct, searchImpressionsByProductId |  |
| tags | PRODUCT-BE-G-13 | tag | No | getProduct |  |
| updatedBy | BOM-BE-G-01 | user-profile | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |
| workspaces | BOM-BE-G-01 | workspaceV2 | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |

## IMPRESSION-FE-002 — Readiness
28 of 32 distinct fields/entities resolve to existing backend stories. 4 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored. 2 field(s) sit behind an unresolved spike (SPIKE-04, SPIKE-05) and cannot be built past the spike's decision.
