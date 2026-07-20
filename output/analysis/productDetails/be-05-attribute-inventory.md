# Phase 5: Attribute (Field) Inventory — ProductDetails

> **Domain:** `productDetails` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [be-03-schema.graphql](./be-03-schema.graphql) + [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`schemas/SPARK_ProductDetail.graphqls`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` (internal) · `EXT` (severity) · `Polymorphic`.

## Table 1 — non-trivial field resolvers

| Type | Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|-----------|------------|-------|
| `ProductDetails` | `access` | `AccessControl` | EXT (ACL context) | acl (context) | Medium | G01 |
| `ProductDetails` | `currentUserPermissions` | `ResourcePermissions` | EXT (ACL context) | acl (context) | Medium | G01 |
| `ProductDetails` | `participantDetails` | `UserGroup_Participants` | EXT | 🔵 user-profile | Low | G01 |
| `ProductDetails` | `product` | `Product` | Field-resolver (internal) | — same DGS (only if `parentId` starts `PID`) | Low | G02 |
| `ProductDetails` | `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G02 |
| `ProductDetails` | `businessPartners` | `[VMM_BusinessPartner]` | EXT | 🔵 vmm | Low | G02 |
| `ProductDetails` | `workspaces` | `[WorkspaceV2]` | EXT | 🟡 workspaceV2 | Low | G02 |
| `ProductDetails` | `attachment` | `Attachment` | EXT (elastic; `relatedResources.length<=2`) | 🔴 search | Medium | G03 |
| `ProductDetailsItem` | `attachment` | `Attachment` | EXT (elastic by `templateId`) | 🔴 search | Low | G03 |
| `ProductDetailsItem` | `constructionSetAttachments` | `[Attachment]` | EXT (elastic by `id`) | 🔴 search | Low | G03 |
| `ProductDetailsCategoryWithSection` | `subCategories` | `[CodeDescription]` | Field-resolver (internal) | — specificationsTemplate | Medium | G03 |
| `ProductDetails` | `status` | `CodeDescription` | Direct (from record) | — | Low | B01 |
| `ProductDetails` | `statuses` | `[ProductComponentStatus]` | Direct (from record) | — | Low | B01 |

**Direct pass-throughs (from the record):** `id, humanId, version, type, name, notes, parentId, rows,
- archived, manualLock, relatedResources, workspaceContext, constructionTemplate, createdAt, updatedAt`, plus `ProductDetailsItem.{section, category(code/description), subCategory, detail, critical, criticalFromLibrary, specialInstructions, templateId, id}` — DTO-mapped, no resolver.
- Covered by B01 (no dedicated resolver story — `A02` in earlier drafts of this table referenced a
  foundation-phase story that productDetails' be-04-stories.md never authored; these are plain DTO fields
  on the root query's own response).

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `ProductDetailSetInput` | `workspaceContext` | `[String]` | No | **create**: plain id list |
| `ProductDetailSetUpdateInput` | `workspaceContext` | `PartialWorkspaceAssociationsInput` | No | **update**: add/remove object (drives the multi-step write, E01) |
| `ProductDetailSetUpdateInput` | `deleteAttachmentIds` | `[String]` | No | drives attachment bulk-archive (E01) |
| `ProductDetailsManageAccessRequest` | `resourceId` | `ID!` | Yes | per-resource partner access (D02) |
| `PDTLAttachmentCloneRef` | `relatedResources` / `context` | mixed | No | paired positionally with `attachmentIds` (D04) |
| `ComponentStatusInput` | `workspaceId` | `String!` | Yes | matches `SPARK_ComponentStatusInput` (D05) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~24 | Free — schema + DTO mapping (A02/B01) |
| Field-resolver (internal, same DGS) | 2 | `product`, `subCategories` — cheap |
| EXT (cross-domain) | ~10 | federated/elastic references; 3 via 🔴 search |
| Polymorphic | 0 | none |

**Signal:** ProductDetails is **shallow** — most fields are direct. Cost concentrates in the multi-step
`updateProductDetailsSet` write (E01) and the attachment-by-search field resolvers (G03). No polymorphism.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `productDetails`.
