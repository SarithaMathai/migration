## IMPRESSION-FE-001 — Migrate `getBomDataAndImpressions` (with BOM wave)
Queries in scope: searchImpressionsByProductId, getBomByIds · Mutations excluded: 0

**Must complete first:** BE — BOM-BE-A-04, BOM-BE-B-01, BOM-BE-B-03, BOM-BE-G-01, BOM-BE-G-03, BOM-BE-G-08, BOM-BE-G-12, BOM-BE-G-13, BOM-BE-G-17, IMPRESSION-BE-B-01, IMPRESSION-BE-G-01, PRODUCT-BE-B-01, PRODUCT-BE-G-07, PRODUCT-BE-G-10, PRODUCT-BE-G-13 · Spikes — SPIKE-04 · New — NEW-BOM-BE-G-??, NEW-IMPRESSION-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getBomByIds | BOM-BE-B-01 | — | — | No | getBomByIds, searchImpressionsByProductId |  |
| getProduct | PRODUCT-BE-B-01 | — | — | No | searchImpressionsByProductId |  |
| searchImpressionsByProductId | IMPRESSION-BE-B-01 | — | — | No | searchImpressionsByProductId |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| additionalMaterialDetails | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| BomFabricSpecComboSlimDetails | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | fragment body not found in snapshot |
| BOMTrimDetailsFragment | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | fragment body not found in snapshot |
| BomWashDetailsFragment | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | fragment body not found in snapshot |
| components | NEW-IMPRESSION-BE-G-?? | — | — | Yes | searchImpressionsByProductId |  |
| criticalToQuality | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| department | NEW-IMPRESSION-BE-G-?? | — | — | Yes | searchImpressionsByProductId |  |
| departments | NEW-IMPRESSION-BE-G-?? | — | — | Yes | searchImpressionsByProductId |  |
| designPartnerId | NEW-IMPRESSION-BE-G-?? | — | — | Yes | searchImpressionsByProductId |  |
| droppedPartnerIds | NEW-IMPRESSION-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...ProductBaseInfoFragment` |
| editable | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| ImpressionFragment | NEW-BOM-BE-G-?? | — | — | Yes | searchImpressionsByProductId | fragment body not found in snapshot |
| owningPartnerType | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| packagingAttributes | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| preferredStyle | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| primaryMaterial | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| primaryMaterialAttachmentId | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| productMaterials | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| productWorkspaceInfo | NEW-IMPRESSION-BE-G-?? | — | — | Yes | searchImpressionsByProductId |  |
| quantityUom | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| recycledContent | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| secondaryMaterial | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| sectionId | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| sectionName | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| sizeUom | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| SPARK_FabricSpecification_Files | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds, searchImpressionsByProductId | fragment body not found in snapshot |
| vendorStyleNumber | NEW-BOM-BE-G-?? | — | — | Yes | getBomByIds | via `...ProductBaseInfoFragment` |
| blue | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment` |
| brand | PRODUCT-BE-G-13 | ig | — | No | getBomByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| businessPartners | IMPRESSION-BE-G-01 | vmm | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails`; via `...ProductBaseInfoFragment` |
| certifications | BOM-BE-G-03 | materialHub | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| countryOfOrigin | BOM-BE-G-03 | tag | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| createdBy | BOM-BE-G-01 | user-profile | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| droppedPartners | PRODUCT-BE-G-07 | vmm | — | No | getBomByIds, searchImpressionsByProductId | 🔬 SPIKE-04 (gated); cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| fabricRecord | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BomComboSlimDetails` |
| fabricRecordDetail | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BomFabricSpecDetails` |
| fabricRecordHumanId | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BomComboSlimDetails` |
| fabricSpecCombos | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BomComboSlimDetails` |
| green | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment` |
| groundColor | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | via `...TrimLibraryImpressionDetails` |
| libraryResource | BOM-BE-G-03 | materialHub | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| materialLibraryUom | BOM-BE-G-08 | trim | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| origin | BOM-BE-G-03 | materialHub | — | No | getBomByIds, searchImpressionsByProductId | external via `origins`; via `...MaterialOrigins` |
| origins | BOM-BE-G-03 | materialHub | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| parentHumanId | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BomFabricSpecDetails` |
| participantDetails | BOM-BE-G-01 | user-profile | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| percentage | BOM-BE-G-03 | materialHub | — | No | getBomByIds, searchImpressionsByProductId | external via `origins`; via `...MaterialOrigins` |
| red | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment` |
| reservedDpcis | PRODUCT-BE-G-10 | apex | — | No | getBomByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| sizeCaption | BOM-BE-G-08 | trim | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| sizeValue | BOM-BE-G-08 | trim | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| sliderColor | BOM-BE-G-13 | search | — | No | getBomByIds, searchImpressionsByProductId | via `...TrimZipperLibraryImpressionDetails` |
| tags | PRODUCT-BE-G-13 | tag | — | No | getBomByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| tapeColor | BOM-BE-G-13 | search | — | No | getBomByIds, searchImpressionsByProductId | via `...TrimZipperLibraryImpressionDetails` |
| tcins | PRODUCT-BE-G-13 | corona | — | No | getBomByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| teams | BOM-BE-G-01 | user-profile | — | No | getBomByIds, searchImpressionsByProductId | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment`; via `...ProductBaseInfoFragment` |
| teethColor | BOM-BE-G-13 | search | — | No | getBomByIds, searchImpressionsByProductId | via `...TrimZipperLibraryImpressionDetails` |
| textColor | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | via `...TrimLibraryImpressionDetails` |
| thumbnailId | BOM-BE-G-12 | search | — | No | getBomByIds, searchImpressionsByProductId | external via `libraryResource`; via `...BOMColorDetailsFragment`; via `...BomFabricSpecDetails`; via `...ProductBaseInfoFragment` |
| updatedBy | BOM-BE-G-01 | user-profile | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails` |
| users | BOM-BE-G-01 | user-profile | — | No | getBomByIds, searchImpressionsByProductId | external via `participantDetails`; via `...LegacyComponentDiscussionParticipantsFragment` |
| workspaces | BOM-BE-G-01 | workspaceV2 | — | No | getBomByIds, searchImpressionsByProductId | via `...BomDetails`; via `...ProductBaseInfoFragment` |

## IMPRESSION-FE-001 — Readiness
49 of 76 distinct fields/entities resolve to existing backend stories. 27 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored. 1 field(s) sit behind an unresolved spike (SPIKE-04) and cannot be built past the spike's decision.
