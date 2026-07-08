# Phase 3: Federation Schema Analysis — Attachment

> **Domain:** `attachment` · **Target DGS:** separate `plm-attachment` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 23 🔜 | 1 ⏭ — 24 operations**

- The target schema is translated from the source SDL (`schemas/SPARK_Attachment.graphqls`), verified against the resolver.
- **Attachment is its own subgraph** (`plm-attachment`) — every reference is cross-subgraph.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `Attachment` (key `id`) |
| Owned value types | ~9 | `GalleryAttachment`/`Render`/`File`/`Details`/`Validations`, `CopyAttachment`, `ProductPacketProps`, `ThreeDFile`, `AttachmentAccess` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — other DGS | 6 | `SearchAttachment`, `UserProfileAttributes`, `Tag`, `AccessControl`, `ResourceMapping`, `SingleResourceMapping` |
| Inputs | ~12 | `CopyAttachmentInputV3`, `AssociateResourceAttachmentInput`, `BulkAttachmentTagsInput`, `UpdateAttachmentV2`, … |

No interfaces / unions — no `@DgsTypeResolver` needed.

## 2. Client Contract Verification
- 8 queries + 15 mutations preserved (`0 ✅ | 23 🔜`); **1 schema-drift query deferred ⏭** (`getAttachments`, already `@deprecated "Use v3"`, no resolver).
- `SPARK_`/`V3` naming preserved (client contract); `VMM_` kept.
**Entity key:** `Attachment.id` (derived `human_id||humanId||document_id||documentId`). Several `@deprecated`
SDL ops/fields carried with the directive.

## 3. Federation Boundaries

> **Separate subgraph:** `attachment` is its own DGS. **`Attachment` is referenced as an entity** by product
> (`attachments`, `attachmentsWithMetaData`, copy flows), productDetails, packaging, workspace, sample, claims.
> Note `search` returns its **own** `SearchAttachment` shape (a different elastic projection) — keep distinct.

- **Owns** `Attachment` + ~9 value types.
- **External (federation):** `search` (related-resource lookups), `relationship` (resource→attachment ids),
  `access-control` (perms + ACL writes), `tag`, `user-profile`, `gallery`; **gateway stitch:** `VMM`.
- **Provides** `Attachment` for the product-family + sample/claims subgraphs.

## 4. Migration Approach  *(Confluence approach page)*

Attachment is a **mid-size, mid risk** standalone subgraph — CRUD + heavy field coalescing, no polymorphism,
no multi-step orchestration.

1. **Phase A:** schema (~10 types + ~12 inputs) + `AttachmentService` port. **Normalize the dual record
   shape** (elastic snake_case vs api camelCase) at the DTO/Feign boundary so the schema fields are clean —
   this removes most of the field-resolver coalescing.
2. **Phase B:** the reads — `getAttachmentsV3`, by-resource (relationship+ACL), renders (group), from-related
   (🔴 search).
3. **Phase D:** the 15 mutations — archive/delete/copy/associate/remove, tags, attributes/bulk, gallery
   publish/unpublish (ATC- branch), team association, and the ACL-permission writes.
4. **Phase F:** expose `Attachment` as a federated entity for the consuming subgraphs; decide the deferred
   `getAttachments` drift query.
5. **Phase G:** the remaining field resolvers (access/users/tags/businessPartnersFull/modelFile/gallery
   sub-types) + the test/parity harness.

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Dual record shape (snake/camel) leaks into the schema (A02/G01) | Medium | Medium | Normalize at the DTO boundary; one mapping layer | Backend Eng |
| `bulkUpdateAttachments` fire-and-forget (returns undefined) (D08) | Medium | Medium | Confirm contract; await + return updated | Backend Eng |
| ACL-permission writes (D06/D08) are real build work despite "ACL ignored" | Medium | Medium | Port the ADMIN/READ DTO build; not auth, it's grant data | Tech Lead |
| Gallery publish/unpublish V3-vs-legacy branch (D12/D13) | Low | Low | Preserve the `ATC-` prefix branch | Backend Eng |
| `SearchAttachment` vs `Attachment` shape confusion | Low | Medium | Keep the two types distinct in the supergraph | Product Owner |

## 6. ACL Handling
- Reads curry capability tokens (context).
- **Note:** `updateAttachmentsACLPermissions` and the `permissions` arm of `bulkUpdateAttachments` are **ACL *writes*** (grant ADMIN/READ to partners) — these ARE build work (grant data maintenance), not authorization.
- Everything else's ACL token currying is context only.

## 7. Open Questions
1. `bulkUpdateAttachments` — should it await and return the updated attachments?
2. Delete or `@deprecated`-keep `getAttachments` (drift) and the `@deprecated` renders/tag ops?
3. Confirm the dual-shape normalization target (single canonical DTO)?

---
**Phase Completed:** Phase 3 · **Domain:** `attachment`.
