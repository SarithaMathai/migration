# Phase 5: Attribute (Field) Inventory — BOM

> **Domain:** `bom` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source:** [be-03-schema.graphql](./be-03-schema.graphql) + [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> GraphQL types/nullability are taken from the source SDL (`schemas/SPARK_Bom.graphqls`).

Every field, classified by **how it is resolved** and tied to the story that delivers it.
**Resolution kinds:** `Direct` (from parent) · `Computed` (parent-only, no I/O) · `Field-resolver`
(own-backend call) · `EXT` (cross-domain call, severity tagged) · `Polymorphic` (interface/union).

> **`Bom_Unified` deprecated** (see [be-04-stories.md](./be-04-stories.md)'s Phases Overview): dropped as a
> parallel type — field selection on `Bom` covers the same ground. `BomMaterial_Unified` (story `G-02`) and
> `BomImpressionDetails_Unified` were removed entirely (not merely renamed) along with it. Their fields' real
> equivalents are already listed under `G-08` (`BomTrimMaterial`) and `G-11`/`G-12`/`G-13`
> (`BomFabricLibraryImpressionDetails`/`BomTrimLibraryImpressionDetails`/`BomTrimZipperLibraryImpressionDetails`)
> below. `G-10` survives as its own story, rescoped to just the shared internal/external branch-resolution
> logic + `MaterialDataLoader` those three real types still depend on — not a schema type of its own.

---

## Table 1 — Object-type attributes (non-trivial; trivial scalars summarized at end)

| Type | Attribute | GraphQL Type | Resolution | Resolver Loc | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|--------------|-----------|------------|-------|
| `Bom` | `humanId` | `String` | Computed | `resolvers/SPARK_Bom.js:281` | — | Low | G01 |
| `Bom` | `materials` | `[BomMaterialInterface]` | Polymorphic | `:315` | — | Very High | A04 |
| `Bom` | `access` | `AccessControl` | EXT | `:282` | accessControl (context-only) | Medium | G01 |
| `Bom` | `currentUserPermissions` | `ResourcePermissions` | EXT | `:285` | accessControl (context-only) | Medium | G01 |
| `Bom` | `businessPartners` | `[VMM_BusinessPartner]` | EXT | `:283` | 🔵 vmm/teams | Medium | G01 |
| `Bom` | `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | `:287,290` | 🔵 user-profile | Low | G01 |
| `Bom` | `product` | `Product` | Field-resolver (internal) | `:288` | — (same DGS) | Low | G01 |
| `Bom` | `workspaces` | `[WorkspaceV2]` | EXT | `:289` | 🟡 workspaceV2 | Medium | G01 |
| `Bom` | `participantDetails` | `UserGroup_Participants` | EXT | `:291` | 🔵 user-profile | Low | G01 |
| `BomMaterialInterface` | `__resolveType` | — | Polymorphic | `:315-347` | — | Medium | A04 |
| `BomMaterial` | `libraryResource` | `HubMaterialInterface` | EXT | `:351` | 🟡 materialHub (+acl context) | Medium | G03 |
| `BomMaterial` | `genericMaterialType` | `String` | EXT (hub-precedence) | `:352-363` | 🟡 materialHub | Medium | G03 |
| `BomMaterial` | `origins` | `[MaterialOriginV2!]` | EXT (coded-options enrich) | `:366-372` | 🟡 materialHub | Medium | G03 |
| `BomMaterial` | `certifications` | `[CodeDescription]` | EXT (coded-options) | `:373-378` | 🟡 materialHub | Low | G03 |
| `BomMaterial` | `weight` | `ValueWithUnit` | EXT (H1) | `:379` | 🟡 materialHub | Low | G03 |
| `BomMaterial` | `sizeUnitOfMeasure` | `UnitOfMeasure` | EXT (H2) | `:380` | 🟡 materialHub | Low | G03 |
| `BomMaterial` | `countryOfOrigin` | `[Tag]` | EXT | `:364` | 🔵 tag | Low | G03 |
| `BomFabricMaterial` | `libraryResource` | `FabricSpecCombo` | EXT | `:389-397` | 🔴 search | Low | G05 |
| `BomFabricSpecMaterial` | `libraryResource` | `FabricSpecification` | EXT | `:404-410` | 🟡 fabric | Low | G06 |
| `BomCombinationMaterial` | `libraryResource` | `Combination` | EXT | `:416-422` | 🟡 combination | Low | G07 |
| `BomTrimMaterial` | `libraryResource` | `Trim` | EXT | `:429-435` | 🟡 trim | Medium | G08 |
| `BomTrimMaterial` | `materialLibraryUom` | `CodeDescription` | EXT | `:436-446` | 🟡 trim | Low | G08 |
| `BomTrimMaterial` | `sizeValue` | `String` | EXT + 15-case dispatcher | `:447-465` | 🟡 trim | High | G08 |
| `BomTrimMaterial` | `sizeCaption` | `BomSizeCaption` | EXT + 15-case dispatcher | `:466-476` | 🟡 trim | High | G08 |
| `BomTrimMaterial` | `facilityName` | `String` | EXT (2-level lookup) | `:477-499` | 🔵 location | Medium | G08 |
| `BomWashMaterial` | `libraryResource` | `Wash` | EXT | `:506-513` | 🟡 wash (+acl context) | Low | G09 |
| `BomImpressionDetailsInterface` | `__resolveType` | — | Polymorphic | `:517-532` | — | Low | A04 |
| `BomFabricLibraryImpressionDetails` | `libraryResource` | `Material` | EXT (branch) | `:567-589` | 🔴 search | Medium | G11 |
| `BomTrimLibraryImpressionDetails` | `libraryResource`,`groundColor`,`textColor` | `Material` | EXT (branch) | `:591-618` | 🔴 search | Medium | G12 |
| `BomTrimZipperLibraryImpressionDetails` | `sliderColor`,`tapeColor`,`teethColor` | `Material` | EXT (H4) | `:620-627` | 🔴 search | Low | G13 |
| `BomMaterialType` | `id` | `String` | Computed | `:629-631` | — | Low | G14 |
| `BomMaterialSearch` | `paging` | `Paging` | Direct (whole-object) | `:633-635` | — | Low | G14 |
| `BomMaterialSearchResult` | `description` | `String` | Computed | `:638` | — | Low | G15 |
| `BomMaterialSearchResult` | `status` | `String` | Computed (object\|string) | `:639-640` | — | Low | G15 |
| `BomMaterialSearchResult` | `fabricSpec` | `FabricSpecification` | EXT (conditional) | `:641-646` | 🟡 fabric | Medium | G15 |
| `BomMaterialSearchResult` | `fabric` | `Fabric` | EXT (conditional) | `:647-653` | 🟡 fabric (+acl context) | Medium | G15 |
| `BomMaterialSearchResult` | `fabricId` | `String` | Computed (conditional) | `:654-659` | — | Low | G15 |
| `BomMaterialSearchResult` | `relatedMaterials` | `MaterialsPaged` | EXT (internal/external branch) | `:660-707` | 🔴 search | High | G15 |

**Trivial scalar pass-throughs (Direct):** every material type's `rowId, notes, quantity, size,
- componentLocation, supplierArticleNumber, sectionId/Name, level, attachmentIds, weight*, thickness*, length*, width*, tcin*` etc. come straight from the parent material record (~30 fields × 7 types).
- `*.libraryResourceId` = `get(parent,'libraryResource.id')` (Computed).
- `*.impressionDetails` = `parent.impressions` (Direct rename).
- Bundled into **G14**.

## Table 2 — Input-object attributes (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `BomInput` | `name` | `String!` | Yes | |
| `BomInput` | `parentId` | `String!` | Yes | product/template id |
| `BomInput` | `materials` | `[BomMaterialInput]` | No | the material rows |
| `BomInput` | `workspaceContext` | `[ID]` | No | initial workspace assoc |
| `UpdateBomInput` | `humanId` | `String` | No | primeKey for the read cache; absent on create |
| `UpdateBomInput` | `workspaceContext` | `PartialWorkspaceAssociationsInput` | No | drives the workspace step of `updateBom` (E01) |
| `UpdateBomInput` | `businessPartners` | `[BomPartnerInput]` | No | triggers the 3rd (permissions) call in `updateBom` |
| `BomMaterialInput` | `materialCategoryId` | `Int` | No | drives `__resolveType` after read-back |
| `BomMaterialInput` | `librarySizeId` | `Int` | No | used by trim `sizeValue`/`sizeCaption` |
| `BomMaterialInput` | `origins` | `[MaterialOriginInput!]` | No | `{origin:Int, percentage:Float}` |
| `MaterialNestedSearchFilter` | `type/fieldPath/nestedFieldPath/operator/values` | mixed | No | flattened to query-string keys in `searchMaterialsBom` |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~210 (scalar pass-throughs across 7 material types + entity scalars) | Free — schema + DTO mapping only (G14) |
| Field-resolver (own backend) | 1 (`Bom.product` internal) | thin |
| EXT (cross-domain) | ~38 distinct field resolvers | each needs a federated reference or service call |
| Polymorphic | 2 interfaces (7 + 5 impls) | `@DgsTypeResolver` + per-variant tests (A04) |

**Reading the signal:** the BOM schema is *wide but shallow* — the overwhelming majority of attributes
- are direct pass-throughs (cheap).
- Migration risk concentrates in **~38 EXT field resolvers** (material library + impression color lookups) and the **2 polymorphic interfaces**.
- Trim (`G08`) and the impression `libraryResource` internal/external branch (`G10`) are the two hardest field-resolver stories.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `bom`
