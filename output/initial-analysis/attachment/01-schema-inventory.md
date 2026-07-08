# Phase 1: Schema Inventory — Attachment

> **Domain:** `attachment`
> **Target DGS:** `AttachmentService` → **separate `plm-attachment` subgraph**
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_Attachment.graphqls` (222-line SDL) + `resolvers/SPARK_Attachment.js` (318) + `services/Attachment.js` (403)
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

- No `context.js`.
- `AttachmentService extends SparkService` takes the base URL **directly** (`this.endpoint = endpoint`, `services/Attachment.js:15`); paths are like `/attachments/v3?humanIds=`.
- The REST service is **`plm-attachment`** (per platform direction).

| Setting | Value |
|---|---|
| Loader key | `attachment` |
| Service class | `AttachmentService extends SparkService` |
| Backend / DGS | **`plm-attachment`** (separate subgraph + backend) |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | **separate `plm-attachment` subgraph** (referenced by product/productDetails/packaging/workspace/sample/search/claims) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Attachment.graphqls` | 222 | the source SDL — 9 queries, 15 mutations, `Attachment` + gallery/copy/access types, ~15 inputs |
| `resolvers/SPARK_Attachment.js` | 318 | 8 queries (+1 drift), 15 mutations, `Attachment` (~25 field resolvers) + 4 sub-type blocks |
| `services/Attachment.js` | 403 | ~30 REST methods (`attachments/v3` + renders/gallery/acl) |
| **Total** | **943** | mid domain — no chunked reading |

Schema: **`schemas/SPARK_Attachment.graphqls` (222 lines)** — target schema in [03-schema.graphql](./03-schema.graphql)
translated from it (nullability from the SDL).

## 3. Import Graph
```
resolvers/SPARK_Attachment.js
├── utils/commonLoaders            → getUserPermissionsJWT (ACL — context only)
├── utils/Product/attachmentUtils  → get3DmodelFile (modelFile)
└── utils/userAttributesUtils      → getUser (created/updated)
AttachmentService extends SparkService; uses loadListing/loadOne/postOne/putOne/deleteOne/convertFunctions
```

## 4. Cross-Domain Reference Table (all cross-subgraph — attachment is its own DGS)

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `getAttachmentsfromRelatedResource(s)` | `search` | SearchService (elastic) | federation | 🔴 |
| `getAttachmentsByResource[AndOwner]` (resource→attachment ids) | `relationship` | RelationshipService | federation | 🟡 |
| `access`, ACL perms (`updateAccessControl`, `bulkUpdateAttachmentPermissions`, `getUserAccessByPost`, `getPermissionsForResource`) | `accessControl` | AccessControlService | **context (+ ACL writes are build work)** | n/a |
| `businessPartnersFull` | `vmm` | VMM platform | Gateway stitch | 🔵 |
| `tags` | `tag` | TagService | federation | 🟡 |
| `createdBy`/`updatedBy`/`publishedBy` | `userAttributes` | UserProfileService | federation | 🟡 |
| `galleryDetails.fileTypes` | `gallery` | GalleryService | federation | 🔵 |

## 5. Co-located Siblings
**None** — `attachment` is its **own DGS** (`plm-attachment`). It is **referenced as an entity** by product
- (`attachments`, `attachmentsWithMetaData`, copy flows), productDetails, packaging, workspace, sample, claims, and search (which returns `SearchAttachment`).
- All outbound calls (above) are cross-subgraph.

## 6. Hot Spots
1. **Dual record shape (snake/camel coalescing)** — most `SPARK_Attachment` field resolvers coalesce
   `snake_case` (elastic) vs `camelCase` (api): `documentId`/`humanId`/`createdAt`/`canShareWithGallery`/
   `finalVirtualFile`/`relatedResources`/… The DGS port must normalize both shapes (Jackson + a mapping layer).
2. **Gallery publish/unpublish** — `publishAttachmentToGallery`/`unpublish` branch on `ATC-` prefix (V3 vs
   legacy endpoint); api returns void → resolver returns `true` on no-error.
3. **`getAttachmentsByResource`** — (🟡 relationship) `searchByIds` → ids → (accessControl) `getUserAccessByPost`
   token → (own) `getAttachmentsByPostV3`.
4. **ACL writes** — `updateAttachmentsACLPermissions` builds bulk ADMIN/READ DTOs; `bulkUpdateAttachments`
   fans tags + permissions (**fire-and-forget; returns undefined** — verify intent).
5. **`id` derivation** — `id` = `human_id || humanId || document_id || documentId` (coalesce). `@key` = `id`.
6. **Schema-drift query** — `getAttachments(resourceId, resourceType)` is `@deprecated` in the SDL and has
   **no resolver** ("Use v3"). Deferred ⏭.
7. **3D / model** — `modelFile` via `get3DmodelFile`; `SPARK_3d_File`/`GalleryFile`/`GalleryDetails` sub-types.

## 7. Operation Lists
**Queries (8 impl + 1 drift):** getAttachmentsV3, getAttachmentsByResource, getAttachmentsByResourceAndOwner,
- getRendersForAttachmentIds(⚠@deprecated but resolved), getRendersForAttachmentV3Ids, getRendersForAttachmentIdsByPost, getAttachmentsfromRelatedResource, getAttachmentsfromRelatedResources.
- **Drift ⏭:** getAttachments.
**Mutations (15):** archiveAttachmentV3, deleteAttachmentV3, copyAttachmentsV3, associateResourcesV3,
removeResourcesV3, updateAttachmentsACLPermissions, updateAttachmentTags, updateAttachmentTagsV3,
bulkUpdateAttachments, updateAttributes, bulkUpdateAttributes, bulkUpdateAttachmentsV2,
publishAttachmentToGallery, unpublishAttachmentToGallery, associateAttachmentTeams.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 8 (+1 schema-drift) |
| Mutations | 15 |
| Object types | ~10 (`Attachment`, gallery render/file/details, copy, access, packet-props, 3d) |
| Field resolvers | ~32 (25 on `Attachment` + 4 sub-types) |
| Service methods | ~30 |
| Cross-domain loader keys | 6 (+ accessControl context) |
| EXT calls | 1 🔴 (search) · 3 🟡 (relationship, tag, userAttributes) · 2 🔵 (vmm, gallery) |
| Interfaces / unions | 0 |
| Large files | 0 (largest 403) |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `attachment` · **Files:** 3 (943 lines: schema 222 + resolver 318 + service 403).
