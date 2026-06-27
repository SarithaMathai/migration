# Phase 5: Attribute (Field) Inventory — Product

> **Domain:** `product` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`code/schemas/SPARK_Product.txt`). `Product` is
> wide (~90 fields); this lists the **non-trivial** field resolvers and groups the direct pass-throughs.

Resolution kinds: `Direct` · `Computed` · `Field-resolver` (internal) · `EXT` (severity) · `Polymorphic`.

## Table 1 — `Product` non-trivial field resolvers

| Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|-----------|--------------|------------|-----------|------------|-------|
| `attachmentsWithMetaData` | `[AttachmentWithMetaData]` | EXT (5-source merge, ~150 ln) | 🔴 attachment + relationship | Very High | G01 |
| `components` | `SearchComponentsPaged` | EXT (4 elastic + N+1 ACL, ~190 ln) | 🔴 search + acl(context) | Very High | G02 |
| `attachments` / `attachmentsV3` / `attachmentSummary` | attachment types | EXT | 🔴 attachment/search | High | G03 |
| `ProductsCategories.categories` | `[Categories]` | Polymorphic (12-case) | 🔵 IG/VMM/tag | Medium | G04 |
| `samples` / `sampleIds` / `elasticSamplesList` | sample types | EXT | 🟡 sampleV2 / 🔴 search | Medium | G05 |
| `teams` / `teamsV2` | team types | EXT | 🟡 teamV2 | Medium | G06 |
| `discussionsV2` / `discussionsCount` | discussion types | EXT | 🟡 discussion / 🔴 search | Medium | G06 |
| `workspaces` / `productWorkspaceAttributes` / `productWorkspaceInfo` | workspace types | EXT | 🔴 workspaceV2 / 🔴 search | Medium | G09 |
| `vendorAttributes` / `businessPartners` / `droppedPartners` / `unDroppablePartners` | VMM types | EXT | 🔵 vmm | Medium | G07 |
| `measurementSets` / `claims` / `bom` / `productBom` / `packagingBom` / `productDetails` / `variations` / `associateProductsAsks` | sibling types | Field-resolver (internal) | — same DGS | Medium | G08 |
| `ancestryProducts` / `childProducts` | relationship types | EXT | 🟡 relationship | Medium | G10 |
| `rating` | `Rating` | EXT (external SaaS) | 🔵 rating (api-key) | Low | G10 |
| `reservedDpcis` | `[PartnerReservedDpci]` | EXT (APEX) | 🔵 apex | Low | G10 |
| `notRemovablePartnerIds` / `notRemovableWorkspaceIds` | `[ID]` | EXT (reflective→service) | 🔵 vmm/workspace | Medium | G11 |
| `department` / `departments` / `clazz` / `brand` / `brands` / `divisions` / `productTemplateDepartments` | IG/VMM/Doppler | EXT | 🔵 ig/brand/doppler | Low | G13 |
| `division` | `IG_Division` | EXT **(latent bug — calls department loader)** | 🔵 ig | Low | G12 |
| `tags` | `[Tag]` | EXT | 🟡 tag | Low | G13 |
| `tcins` / `SPARK_Tcin.itemDetails` | tcin/CORONA | EXT | 🔵 corona | Low | G13 |
| `createdBy` / `updatedBy` / `versionCreatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G14 |
| `status` | `ProductStatus` | EXT (merge partner/workspace) | 🔵 vmm | Medium | G07 |
| `SPARK_PackagingAttribute.spg` | `SpgFileLibrary` | Field-resolver (internal) | — fileLibrary | Low | G13 |
| `DopplerDepartment.primary/secondaryCapacityTypeName` | `String` | EXT | 🔵 doppler | Low | G04 |
| `ProductComponentStatus.updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G14 |
| `SPARK_ResourcesCount.productThumbnailId` | `String` | Field-resolver (re-fetch product) | — internal | Low | G14 |
| `Categories.__resolveType` | — | Polymorphic | — | Medium | A04 |

**Direct/Computed pass-throughs (~60 fields):** `id, humanId, type, description, comments, internalNotes,
vendorStyleNumber, primaryMaterial, secondaryMaterial, thumbnailId, parentProductId, copyId, numberOfPieces,
developmentCost, presentation*, archived, movable, editable, preferredStyle, fbDpci, version, createdAt,
updatedAt, parentTcins, designPartnerId, droppedPartnerIds`, plus all value-type scalar fields — DTO-mapped.
Bundled into **G14**.

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `ProductInput` | `type` | `Int` | No | 100 product / 101 template / 102 brand-compliance — drives branches |
| `ProductInput` | `businessPartners` | `[ProductPartnerInput]` | No | initial partner assignment |
| `ProductUpdateInput` | `id` | `ID!` | Yes | |
| `ProductUpdateInput` | `carryForwardProduct` | `BulkCarryForwardProductInput` | No | carry-forward branch |
| `ProductUpdateInput` | `removedProductTemplateAttachments` | `[…]` | No | drives template attachment archival (M4) |
| `ProductPartnerActionInput` | `dropped` | `Boolean` | No | REMOVE/DROP/UNDROP routing (M10) |
| `ProductTechPackCountInput` | `productId`/`partnerId`/`workspaceContext`/`parentProductId` | mixed | productId yes | TechPack key + context |
| `ComponentIdsInput` | `bomIds`/`claimIds`/`measurementSetIds`/`packagingIds`/`constructionSetIds` | `[String]` | No | fan-out targets (M20) |
| `CarryForwardProductInput` | many | mixed | No | every field used by `carryForwardProduct` (M5) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~60 | Free — schema + DTO mapping (G14) |
| Field-resolver (internal, same DGS) | ~10 | sibling/internal calls — cheap (G08, fileLibrary) |
| EXT (cross-domain) | ~30 | federated references; 2 X-Large (G01/G02) |
| Polymorphic | 1 union (`Categories`) | `@DgsTypeResolver` (A04) |

**Signal:** Product is **wide and deep**. The bulk of fields are direct, but the long tail of **~30 EXT field
resolvers** plus the **two X-Large** (`attachmentsWithMetaData`, `components`) and the **TechPack composite-key
aggregate** are where the migration cost and risk concentrate. The `division` field carries a **latent bug**
(wrong loader) to fix on port.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `product`.
