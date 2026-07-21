## IMPRESSION-FE-002 — Migrate `getCarryForwardFormData` (with Product wave)
Queries in scope: searchImpressionsByProductId, getProduct · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-A-04, BOM-BE-B-01, BOM-BE-B-03, BOM-BE-G-01, BOM-BE-G-03, BOM-BE-G-08, BOM-BE-G-12, BOM-BE-G-13, BOM-BE-G-17, IMPRESSION-BE-B-01, IMPRESSION-BE-G-01, PRODUCT-BE-B-01, PRODUCT-BE-G-01, PRODUCT-BE-G-02, PRODUCT-BE-G-03, PRODUCT-BE-G-06, PRODUCT-BE-G-07, PRODUCT-BE-G-08, PRODUCT-BE-G-09, PRODUCT-BE-G-10, PRODUCT-BE-G-13, PRODUCT-BE-S-01 · Spikes — SPIKE-04, SPIKE-05 · New — NEW-BOM-BE-G-??, NEW-IMPRESSION-BE-G-??, NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getBomByIds | BOM-BE-B-01 | — | — | No | searchImpressionsByProductId |  |
| getProduct | PRODUCT-BE-B-01 | — | — | No | getProduct, searchImpressionsByProductId |  |
| searchImpressionsByProductId | IMPRESSION-BE-B-01 | — | — | No | searchImpressionsByProductId |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| additionalMaterialDetails | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| BomFabricSpecComboSlimDetails | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| BOMTrimDetailsFragment | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| BomWashDetailsFragment | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| criticalToQuality | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| designPartnerId | NEW-IMPRESSION-BE-G-?? | — | — | Yes | searchImpressionsByProductId |  |
| ImpressionFragment | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| isResourceCritical | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct | via `...AttachmentsWithMetaData` |
| linkedResourceId | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct | via `...AttachmentsWithMetaData` |
| primaryMaterialAttachmentId | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| quantityUom | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| recycledContent | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| resourcePermissions | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct |  |
| resourceTitle | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct | via `...AttachmentsWithMetaData` |
| sectionId | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| sectionName | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| sizeUom | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | via `...BomDetails` |
| SPARK_FabricSpecification_Files | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| ancestryProducts | PRODUCT-BE-G-10 | relationship | — | No | getProduct |  |
| attachments | PRODUCT-BE-G-03 | attachment | — | No | getProduct |  |
| attachmentsV3 | PRODUCT-BE-G-03 | attachment | — | No | getProduct |  |
| attachmentsWithMetaData | PRODUCT-BE-G-01 | attachment | — | No | getProduct |  |
| blue | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment` |
| brand | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| businessPartners | IMPRESSION-BE-G-01 | vmm | — | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |
| certifications | BOM-BE-G-03 | materialHub | — | No | searchImpressionsByProductId | via `...BomDetails` |
| childProducts | PRODUCT-BE-G-10 | relationship | — | No | getProduct |  |
| clazz | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| components | PRODUCT-BE-G-02 | search | — | No | getProduct, searchImpressionsByProductId | 🔬 SPIKE-05 (gated) |
| countryOfOrigin | BOM-BE-G-03 | tag | — | No | searchImpressionsByProductId | via `...BomDetails` |
| createdBy | BOM-BE-G-01 | user-profile | — | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |
| department | PRODUCT-BE-G-13 | ig | — | No | getProduct, searchImpressionsByProductId |  |
| departments | PRODUCT-BE-G-13 | ig | — | No | getProduct, searchImpressionsByProductId |  |
| discussionsV2 | PRODUCT-BE-G-06 | discussion | — | No | getProduct |  |
| division | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| droppedPartners | PRODUCT-BE-G-07 | vmm | — | No | getProduct, searchImpressionsByProductId | 🔬 SPIKE-04 (gated) |
| fabricRecord | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BomComboSlimDetails` |
| fabricRecordDetail | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BomFabricSpecDetails` |
| fabricRecordHumanId | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BomComboSlimDetails` |
| fabricSpecCombos | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BomComboSlimDetails` |
| green | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment` |
| groundColor | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | via `...TrimLibraryImpressionDetails` |
| libraryResource | BOM-BE-G-03 | materialHub | — | No | searchImpressionsByProductId | via `...BomDetails` |
| materialLibraryUom | BOM-BE-G-08 | trim | — | No | searchImpressionsByProductId | via `...BomDetails` |
| origin | BOM-BE-G-03 | materialHub | — | No | searchImpressionsByProductId | external via `origins`; via `...MaterialOrigins` |
| origins | BOM-BE-G-03 | materialHub | — | No | searchImpressionsByProductId | via `...BomDetails` |
| parentHumanId | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BomFabricSpecDetails` |
| participantDetails | BOM-BE-G-01 | user-profile | — | No | searchImpressionsByProductId | via `...BomDetails` |
| percentage | BOM-BE-G-03 | materialHub | — | No | searchImpressionsByProductId | external via `origins`; via `...MaterialOrigins` |
| productWorkspaceInfo | PRODUCT-BE-G-09 | workspaceV2 | — | No | getProduct, searchImpressionsByProductId |  |
| red | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment` |
| sizeCaption | BOM-BE-G-08 | trim | — | No | searchImpressionsByProductId | via `...BomDetails` |
| sizeValue | BOM-BE-G-08 | trim | — | No | searchImpressionsByProductId | via `...BomDetails` |
| sliderColor | BOM-BE-G-13 | search | — | No | searchImpressionsByProductId | via `...TrimZipperLibraryImpressionDetails` |
| tags | PRODUCT-BE-G-13 | tag | — | No | getProduct |  |
| tapeColor | BOM-BE-G-13 | search | — | No | searchImpressionsByProductId | via `...TrimZipperLibraryImpressionDetails` |
| teams | BOM-BE-G-01 | user-profile | — | No | searchImpressionsByProductId | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| teethColor | BOM-BE-G-13 | search | — | No | searchImpressionsByProductId | via `...TrimZipperLibraryImpressionDetails` |
| textColor | BOM-BE-G-12 | search | — | No | searchImpressionsByProductId | via `...TrimLibraryImpressionDetails` |
| thumbnailId | BOM-BE-G-12 | search | — | No | getProduct, searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment`; via `...BomFabricSpecDetails` |
| updatedBy | BOM-BE-G-01 | user-profile | — | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |
| users | BOM-BE-G-01 | user-profile | — | No | searchImpressionsByProductId | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| workspaces | BOM-BE-G-01 | workspaceV2 | — | No | getProduct, searchImpressionsByProductId | via `...BomDetails` |

## IMPRESSION-FE-002 — Readiness
60 of 78 distinct fields/entities resolve to existing backend stories. 18 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored. 2 field(s) sit behind an unresolved spike (SPIKE-04, SPIKE-05) and cannot be built past the spike's decision.
