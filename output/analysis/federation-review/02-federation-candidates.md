# 02 · Federation Candidates — Cross-Domain Identifier Inventory

> Phase 2 of the federation review · 2026-07-17
> Every output-type field that references another business domain by primitive identifier, with a verdict.
> Verdicts: **KEEP** (stays primitive — justified) · **DUAL** (id kept, object field already exists) · **ADD** (recommended/optional new object field — see [03](./03-proposed-schema-changes.md)) · **FIX** (required contract fix — see [03 §1](./03-proposed-schema-changes.md)).

## 0. Global rules applied

- **Input types keep primitive IDs.** GraphQL input types cannot reference entities; every `*Id` in an input is correct as-is. Inputs are therefore excluded below.
- **Local identifiers stay.** `id`, `humanId`, `rowId`, `sectionId`, `parentRowId`, `copyId`, `placeholderId`, master-data code ids (`*UomId`, `statusId`, `reasonIds`, `substrateTypeId`, `formatId`, …) are within-domain and are not federation candidates.
- **Dual pairs are the house pattern.** Where the schema already exposes `xId` *and* `x: Entity`, both stay — the id preserves the client contract (thumbnails, cache keys, gating logic), the object is the federated path.
- **Denormalized display pairs** (`supplierId`+`supplierName`, `facilityId`+`facilityName`, `laundryId`+`laundryName`, `printerId`+`printer*`) may be *snapshots* taken at authoring time, not live lookups — converting them to live entity refs can change displayed data. Flagged per-row; PO question OQ-3 in [08](./08-risks-assumptions-questions.md).

## 1. BOM (owner: `plm-product` / bom)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `Bom.parentId` | product | `String` | keep + existing `Bom.product: Product` | DUAL |
| `Bom.workspaceContext` | workspace | `[ID]` | keep + existing `workspaces: [WorkspaceV2]` | DUAL |
| `Bom.selectedProductImpressionIds` | impression (co-located) | `[String]` | + `selectedProductImpressions: [Impression]` (internal resolver) | ADD (optional) |
| `BomMaterialInterface.supplierId` / `supplierName` (7 impls) | business-partner (VMM) | `String` | + `supplier: VMM_BusinessPartner` | ADD (recommended) |
| `BomMaterial/BomTrimMaterial.facilityId` / `facilityName` | VMM location | `String` | + `facility: VMM_Location` *(needs VMM_Location stub)* | ADD (optional) |
| `BomWashMaterial.laundryId` / `laundryName` | VMM location | `String` | keep (same pattern as facility; fold into facility decision) | ADD (optional) |
| `BomMaterialInterface.attachmentIds` / `primaryMaterialAttachmentId` | attachment (phase 2) | `[String]` | + `attachments: [Attachment]` post-phase-2 | ADD (optional, deferred) |
| `BomMaterialInterface.tcinIds` / `tcinDpcis` | CORONA item | `[String]` | keep — item detail joins live on `Product.tcins[].itemDetails` | KEEP |
| `Bom*Material.libraryResourceId` | material DGSs | `String` | keep + existing `libraryResource: <Hub/Fabric/Trim/Wash/Combination>` | DUAL |
| `BomMaterialSearchResult.thumbnailId` | attachment | `String` | keep — search projection, perf-sensitive | KEEP |
| `BomMaterialSearchResult.fabricId/fabricSpecId/parentComboId` | material DGSs | `String` | keep + existing `fabric`/`fabricSpec`/`relatedMaterials` objects | DUAL |
| `Bom*ImpressionDetails.*RowId` (finish/color/slider/tape/teeth) | trim rows (material DGS) | `String` | keep + existing `textColor`/`groundColor`/… `Material` objects | DUAL |

## 2. Product (owner: `plm-product` / product)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `Product.thumbnailId` | attachment | `String` | keep (clients build image URLs from the id) + optional `thumbnail: Attachment` | ADD (optional) |
| `Product.parentProductId` | product (self) | `String` | keep + existing `ancestryProducts` projection | KEEP |
| `Product.copyId` / `copyProductRequest` | product copy op (local) | `String` | local — feeds `getCopyStatus(id)` | KEEP |
| `Product.brandComplianceRecordId` | OBDP (no subgraph) | `String` | keep — service fetched server-side by API key, no federation stub | KEEP |
| `Product.notRemovablePartnerIds` / `droppedPartnerIds` / `designPartnerId` / `unDroppablePartners` | business-partner | `[ID]` | keep — UI gating sets; display objects already on `businessPartners`/`droppedPartners` | KEEP |
| `Product.sampleIds` | sample | `[ID]` | keep + existing `samples: [SampleV2]` | DUAL |
| `Product.notRemovableWorkspaceIds` | workspace | `[String]` | keep — gating set; `workspaces` object list exists | DUAL |
| `ProductVendorAttributes.partnerId` | business-partner | `ID` | + `partner: VMM_BusinessPartner` (removes client-side join) | ADD (recommended) |
| `WorkspaceInfoPartner.partnerId` | business-partner | `ID` | + `partner: VMM_BusinessPartner` | ADD (recommended) |
| `PartnerTcins.partnerId` / `PartnerReservedDpci.partnerId` | business-partner | `ID` | keep — grouping key only, name never displayed here | KEEP |
| `ProductWorkspaceAttributes.workspaceId` / `ProductWorkspaceInfo.workspaceId` / `CarryForwardProduct*Status.workspaceId` | workspace | `String` | + optional `workspace: WorkspaceV2` (phase-2 workspace subgraph) | ADD (optional, deferred) |
| `AncestryProducts.id` / `ChildProducts.id` | product (self) | `String!` | keep — lineage projections carry `removable` context; optional `product: Product` | ADD (optional) |
| `ResourcesCount.*` stub lists (`productAttachments`…`watchlists`) | 8 domains | `[ID]` | **keep by design** — TechPack count pattern; owning subgraphs fill via `@requires` (federation-patterns-condensed §9) | KEEP |
| `ResourcesCount.productThumbnailId` | attachment | `String` | keep — same as `Product.thumbnailId` | KEEP |
| `ProductRules.productId` | product (self) | `String` | local | KEEP |
| `Component.*` (search projection: `relatedResources`, `materials`, …) | mixed | `[String]` | keep — elastic projection, typed by `type` discriminator | KEEP |
| `AccessV3.fabSuppliers/designPartners/merchVendors/bps` | business-partner | `[ID]` | keep — ACL context lists (ACL ignored in impl) | KEEP |

## 3. Measurement (owner: `plm-product` / measurement)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `Measurement.parentId` / `resourceId` | product | `String` | keep + existing `product: Product` | DUAL |
| `Measurement.workspaceContext` | workspace | `[ID]` | keep + existing `workspaces` | DUAL |
| `SampleMeasurementSet.sampleId` | sample | `String!` | it is the `@key` — keep; + `sample: SampleV2` forward ref | ADD (recommended) |
| `SampleMeasurementSet.measurementSetId` | measurement (self) | `String` | local | KEEP |
| `Measurement.updatedFromResource` | sample | already `SampleV2` | — | ✅ done |

## 4. Impression (owner: `plm-product` / impression)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `Impression.owningPartnerId` | business-partner | `ID` | keep + existing `owningBusinessPartner` | DUAL |
| `Impression.workspaceContext` | workspace | `[ID]` | keep + existing `workspaces` | DUAL |
| `Impression.attachmentId` | attachment | `String` | + `attachment: Attachment` (client selects `attachmentId` today and resolves the file separately) | ADD (recommended) |
| `Impression.associatedBomIds` | bom (co-located) | `[String]` | + `associatedBoms: [Bom]` (internal resolver) | ADD (optional) |
| `Impression.relatedResources` | mixed resource types | `[ID]` | keep — polymorphic; would need a union of 6+ types (OQ-4) | KEEP |
| `Impression.parentId` | product | `ID` | keep — product link contributed by Phase F `Product.impressions` | KEEP |

## 5. Packaging (owner: `plm-product` / packaging)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `Packaging.parentId` | product | `String` | keep + existing `product: Product` | DUAL |
| `Packaging.workspaceIds` | workspace | `[String]` | keep + existing `workspaces` | DUAL |
| `PackagingInternalData.attachmentIds` / `PrinterDieline.attachmentIds` | attachment (phase 2) | `[String]` | + `attachments: [SearchAttachment]` post-phase-2 | ADD (optional, deferred) |
| `Dieline.attachmentId` | attachment | `String` | keep + existing `attachment: Attachment` | DUAL |
| `Dieline.printerId` / `PrinterDieline.printerId` + `printer*` denormals | VMM location/partner | `String` | keep — printer master data has no phase-1 subgraph; snapshot semantics (OQ-3) | KEEP |
| `PrinterDieline.sizeIds` / `Dieline.sizeIds` | sizes master data | `[String]` | master-data codes | KEEP |
| `Packaging.claimId` (input pass-through only) | claims | `String` | input — keep | KEEP |

## 6. Product Details (owner: `plm-product` / productDetails)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `ProductDetails.parentId` | product | `String` | keep + existing `product: Product` | DUAL |
| `ProductDetails.workspaceContext` | workspace | `[String]` | keep + existing `workspaces` | DUAL |
| `ProductDetails.relatedResources` | mixed | `[String]` | keep — polymorphic (OQ-4) | KEEP |
| `ProductDetailsItem.templateId` | specificationTemplate (co-located) | `String` | + optional `template` ref once spec-template types land in the merged schema | ADD (optional) |
| `ProductDetails.constructionTemplate` | template | already `[VersionableId]` | — | ✅ done |

## 7. Watchlist (owner: `plm-product` / watchlist)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `Watchlist.parentId` | product | `String!` | keep + existing `product: Product` | DUAL |
| `WatchlistPartner.partnerId` / `partnerName` | business-partner | `ID` | + `partner: VMM_BusinessPartner` (`partnerName` is already a live VMM lookup — same call) | ADD (recommended) |
| `Watchlist.workspaceContext` | workspace | `String` | keep + existing `workspaces` | DUAL |
| `WatchlistPartner.systemTeamId` | team (phase 2) | `String` | keep until team subgraph lands | KEEP |

## 8. Claims (owner: separate `spark-claims` subgraph)

| Field | References | Current type | Expected federated type | Verdict |
|---|---|---|---|---|
| `Claims.parentId` | product | `String` | keep + existing `product: Product` (cross-subgraph — needs the Product entity fetcher, see [04 §4](./04-entity-analysis.md)) | DUAL |
| `Claims.workspaceContext` | workspace | `[String]` | keep + existing `workspaces` | DUAL |
| `ClaimDetails.claimId` / `guestFacingClaimId` | claims library (own domain) | `String`/`ID` | local master data | KEEP |
| `ParentDetails.droppedPartnerIds` / `otherClaimBps` | business-partner | `[Int]` | keep — UI gating sets from the parent product record | KEEP |
| `ClaimExport.requestId` | export op (local) | `String` | local | KEEP |

## 9. Summary counts

- 62 identifier fields reviewed (output types only) → **34 KEEP · 17 DUAL (already federated) · 11 ADD candidates** (6 recommended, 5 optional/deferred) · **0 fields require removal**.
- The 5 **FIX** items are not field-level ID conversions but cross-subgraph contract mismatches — see [03 §1](./03-proposed-schema-changes.md).
