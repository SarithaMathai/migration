# Phase 2: Resolver Dependency Analysis — Attachment

> **Domain:** `attachment` · **Target DGS:** `AttachmentService` → separate `plm-attachment` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `code/schemas/SPARK_Attachment.txt` (SDL), `code/resolvers/SPARK_Attachment.txt` (318), `code/services/Attachment.txt` (403)
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full

Implementation spec. ACL/JWT usage is **context-only** (ACL *writes* are build work). Own subgraph.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 8 (+1 schema-drift) |
| Mutation resolvers | 15 |
| Field resolvers | ~32 (4 sub-type blocks) |
| Service methods | ~30 |
| EXT loaders | 6 (1 🔴 · 3 🟡 · 2 🔵) + accessControl context |
| High complexity | core field coalescing (G01); ACL bulk writes |

---

## Query Resolvers (8 + 1 drift)

| # | Query | Complexity | Pseudo-logic |
|---|-------|-----------|--------------|
| Q1 | `getAttachmentsV3(ids)` | Low | (ACL) token → (own) `getAttachmentsV3` `GET /attachments/v3?humanIds=`; empty ids → []. |
| Q2 | `getAttachmentsByResource(resourceId)` | Medium | (🟡 relationship) `searchByIds({id, includeNodeTypes:['attachments','attachments_v3'], maxDepth:0})` → ids → (accessControl) `getUserAccessByPost` → (own) `getAttachmentsByPostV3`. |
| Q3 | `getAttachmentsByResourceAndOwner(resourceId)` | Medium | (🟡 relationship) ids → (own) `getAttachmentsByIdsAndAuthorByPostV3`. |
| Q4 | `getRendersForAttachmentIds(ids, betaMode)` | Medium | `Promise.all(ids.map(id → (own) getRendersForAttachmentIds(betaMode).load(id)))`, compact. (@deprecated, still resolved.) |
| Q5 | `getRendersForAttachmentV3Ids(ids, betaMode)` | Medium | as Q4 with V3 loader. |
| Q6 | `getRendersForAttachmentIdsByPost(ids, betaMode)` | Medium | (ACL) token → (own) `getRendersForAttachmentIdsByPost`. |
| Q7 | `getAttachmentsfromRelatedResource(relatedResourceId, parentResourceId)` | Medium | (🔴 search) `searchAttachmentsByParentAndRelatedResource` (if both) or `searchAttachmentsByRelatedResource`; else []. |
| Q8 | `getAttachmentsfromRelatedResources(relatedResourceIds)` | Medium | (🔴 search) `searchAttachmentsByRelatedResources({resourceIds})` → `.content` or []. |
| ⏭ | `getAttachments(resourceId, resourceType)` | — | **schema-drift** — `@deprecated("Use v3")`, no resolver. |

## Mutation Resolvers (15)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `archiveAttachmentV3(id)` | Low | (ACL) token → (own) `archiveAttachmentV3`. |
| M2 | `deleteAttachmentV3(humanId)` | Low | (ACL) token → (own) `deleteAttachmentV3` → String. |
| M3 | `copyAttachmentsV3(attachmentInput)` | Medium | (ACL) token for `humanIds` → (own) `copyAttachmentsV3`. |
| M4 | `associateResourcesV3(input)` | Low | (ACL) token → (own) `associateResourcesV3`. |
| M5 | `removeResourcesV3(input)` | Low | (ACL) token → (own) `removeResourcesV3`. |
| M6 | `updateAttachmentsACLPermissions(partnerId, adminIds, readIds)` | Medium | build bulk `{resourceId, dps:[{permissionLevel:ADMIN/READ, grantees:[partnerId]}]}` → (accessControl) `updateAccessControl`. |
| M7 | `updateAttachmentTags` / M8 `updateAttachmentTagsV3` | Low | (ACL) token → (own) `updateTagsV3({attachmentId, tags})`. **Identical impl** — same story. |
| M9 | `bulkUpdateAttachments(tags, permissions)` | Medium | if tags → (own) `bulkUpdateTags`; if permissions → (accessControl) `bulkUpdateAttachmentPermissions`. **Fire-and-forget; returns undefined** (verify). |
| M10 | `updateAttributes(attachment)` | Low | (ACL) token → (own) `updateAttributes`. |
| M11 | `bulkUpdateAttributes(attachments)` | Medium | (ACL) token for `documentId||humanId` → (own) `bulkUpdateAttributes`. |
| M12 | `bulkUpdateAttachmentsV2(attachments)` | Medium | (ACL) token → (own) `bulkUpdateAttachmentsV2`. |
| M13 | `publishAttachmentToGallery(attachmentId)` | Medium | **branch on `ATC-` prefix** → V3 or legacy publish; void → return `true`. |
| M14 | `unpublishAttachmentToGallery(attachmentId)` | Medium | as M13, unpublish. |
| M15 | `associateAttachmentTeams(parentId, files, teamsToUpdate, relatedResourceIds)` | Medium | build dto → (ACL) token → (own) `associateAttachmentTeams`. |

## Field Resolvers (`SPARK_Attachment` ~25 + 4 sub-types)
- **Snake/camel coalescing (the bulk):** `documentId`/`humanId`/`attachmentId`/`documentType`/`documentSize`/
  `documentName`/`mediaType`/`relatedResources`/`productPacketProps`/`galleryDetails`/`versionNumber`/
  `canShareWithGallery`/`attachmentCanShowdog`/`canOpenInShowDog`/`sharedWithGallery`/`finalVirtualFile`/
  `createdAt`/`updatedAt` (coalesce + Date parse); `id` = `human_id||humanId||document_id||documentId`.
- **EXT:** `access` (accessControl `getPermissionsForResource`), `businessPartnersFull` (🔵 vmm),
  `createdBy`/`updatedBy` (🟡 user `getUser`), `tags` (🟡 tag `getTags`), `modelFile` (`get3DmodelFile`).
- **Sub-types:** `GalleryFile.canOpenInShowDog` (coalesce); `3d_File.fileId`/`fileName` (null-safe);
  `ProductPacketProps.partnerId`/`critical` (coalesce); `GalleryDetails.assetId`/`publishedAt`/`fileValid`
  (coalesce), `publishedBy` (🟡 user), `fileTypes` (🔵 gallery `getAssetFiles`).

## Service Classes
`AttachmentService` base = `plm-attachment`. ~30 methods: `getAttachmentsV3`/`byPostV3`/`byIdsAndAuthor`,
renders (ids/V3/byPost), archive/delete, copy, associate/removeResourcesV3, updateTagsV3/bulkUpdateTags,
updateAttributes/bulk(V2), publish/unpublish gallery (V3 + legacy), associateAttachmentTeams.

## EXT Service Call Inventory (summary)
6 keys — **1 🔴** (search) · **3 🟡** (relationship, tag, userAttributes) · **2 🔵** (vmm, gallery) ·
accessControl **context** (its ACL *writes* — `updateAccessControl`/`bulkUpdateAttachmentPermissions` — ARE build work).

## Key Findings
- **Highest cost:** the dual-shape **snake/camel coalescing** across ~25 field resolvers (G01) — normalize at
  the Feign/DTO boundary so the schema fields are clean.
- **Latent:** `bulkUpdateAttachments` returns undefined (fire-and-forget tags + permissions) — confirm contract.
- **Branches:** gallery publish/unpublish V3-vs-legacy by `ATC-` prefix.
- **Federation provider:** attachment provides `SPARK_Attachment` for product/productDetails/packaging/
  workspace/sample/claims; search returns a separate `SearchAttachment` shape.
- **Quick wins:** the simple V3 reads + single-resource mutations (archive/delete/associate/tags/attributes).

---
**Phase Completed:** Phase 2 · **Domain:** `attachment` · **EXT:** 6 keys (1🔴 · 3🟡 · 2🔵).
