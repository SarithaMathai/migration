# Phase 5: Attribute (Field) Inventory — Attachment

> **Domain:** `attachment` · **Target DGS:** separate `plm-attachment` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`schemas/SPARK_Attachment.graphqls`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — non-trivial field resolvers

| Type | Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|-----------|------------|-------|
| `Attachment` | `access` | `AccessControl` | EXT | acl (context) | Medium | G01 |
| `Attachment` | `businessPartnersFull` | `[VMM_BusinessPartner]` | EXT | 🔵 vmm | Medium | G01 |
| `Attachment` | `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Medium | G01 |
| `Attachment` | `tags` | `[Tag]` | EXT | 🟡 tag | Medium | G02 |
| `Attachment` | `modelFile` | `ThreeDFile` | Computed (`get3DmodelFile`) | — | Low | G02 |
| `Attachment` | `id`/`documentId`/`humanId`/`attachmentId` | ID | **Computed (snake/camel coalesce + derive)** | — | Medium | G01 |
| `Attachment` | `createdAt`/`updatedAt` | DateTime | Computed (coalesce + Date parse) | — | Low | G01 |
| `Attachment` | `documentType`/`documentSize`/`documentName`/`mediaType`/`relatedResources`/`productPacketProps`/`galleryDetails`/`versionNumber`/`canShareWithGallery`/`attachmentCanShowdog`/`canOpenInShowDog`/`sharedWithGallery`/`finalVirtualFile` | mixed | Computed (snake/camel coalesce) | — | Low | G01 |
| `GalleryDetails` | `publishedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G02 |
| `GalleryDetails` | `fileTypes` | `[String]` | EXT | 🔵 gallery | Low | G02 |
| `GalleryDetails` | `assetId`/`publishedAt`/`fileValid` | mixed | Computed (coalesce) | — | Low | G02 |
| `GalleryFile` | `canOpenInShowDog` | Boolean | Computed (coalesce) | — | Low | G02 |
| `ThreeDFile` | `fileId`/`fileName` | String | Computed (null-safe) | — | Low | G02 |
| `ProductPacketProps` | `partnerId`/`critical` | mixed | Computed (coalesce) | — | Low | G02 |

**Direct pass-throughs:** `Attachment.{resource, businessPartners, tcins, parentResource, resources,
- relationshipMetadata, previewable}` and the remaining scalar value-type fields — DTO-mapped.
- **Once A02 normalizes the dual record shape, most "Computed coalesce" fields above become plain Direct fields.**

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `CopyAttachmentInputV3` | `humanIds` | `[ID]!` | Yes | copy targets (D03) |
| `AssociateResourceAttachmentInput` | `humanIds` | `[String]!` | Yes | associate/remove (D04/D05) |
| `BulkAttachmentTagsInput` | `addTagIds`/`removeTagIds`/`id` | `[String]`/`String` | No | bulk tag update (D08) |
| `ManagePermissionsRequest` | `partnersToAdd`/`partnersToDelete`/`locked`/`globalMvAccess` | mixed | No | per-attachment ACL (D11) |
| `AttachmentAttributesUpdateInput` | `documentId`/`productPacketProps`/`finalVirtualFile` | mixed | No | attributes update (D09/D10) |
| `UpdateAttachmentV2` | `documentId`/`tags`/`managePermissionsRequest`/`relatedResources` | mixed | No | bulk v2 (D11) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~24 | Most are **snake/camel coalesce** today → become Direct after A02's canonical DTO |
| Field-resolver (internal) | 0 | attachment is its own subgraph |
| EXT (cross-domain) | ~8 | access/users/tags/businessPartnersFull/gallery (G01/G02) |
| Polymorphic | 0 | none |

**Signal:** Attachment is **CRUD + field-coalescing heavy**, not orchestration. The decisive task is the
**dual record-shape normalization** (A02) which collapses ~18 coalescing field resolvers into Direct fields;
the EXT enrichment (access/users/tags/gallery) is the rest. No polymorphism, no multi-step writes.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `attachment`.
