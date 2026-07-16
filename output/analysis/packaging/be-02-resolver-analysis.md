# Phase 2: Resolver Dependency Analysis — Packaging

> **Domain:** `packaging` · **Target DGS:** `PackagingService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_Packaging.graphqls` (SDL), `resolvers/product/SPARK_Packaging.js`, `services/product/Packaging.js`
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full

Implementation spec. ACL/JWT usage is **context-only** (ignored in impl). Base path `packaging/v1`.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 7 |
| Mutation resolvers | 10 |
| Field resolvers | 17 (4 type blocks) |
| Service methods | ~16 |
| EXT loaders | 7 (2 🔴 · 3 🟡 · 2 🔵) + accessControl context-only + 3 internal |
| High complexity | 2 (`updatePackaging` multi-step, `suggestedRetailPriceByDPCI`) |

---

## Query Resolvers (7)

| # | Query | Complexity | Pseudo-logic (REST + EXT) |
|---|-------|-----------|---------------------------|
| Q1 | `getPackagings(page,size,packagingIds,parentIds,workspaceIds,partnerIds,statusIds): PackagingPaged` | Low | (own) `packaging.getPackagings().load({...filters})` → paged. |
| Q2 | `getPackagingById(packagingId): Packaging` | Low | (ACL context) token → (own) `getPackagingById.load(packagingId)`. |
| Q3 | `getDielines(page,size,packagingIds,parentIds,printerIds,statusIds): [Dieline]` | Low | (own) `getDielines.load({...})` → `.dielines`. |
| Q4 | `getPackagingFieldValuesByType(type, ids): [PackagingFieldValues]` | Low | (own) `getPackagingFieldValuesByType(type, ids)`. |
| Q5 | `getDielineEvaluationStatuses: [CodeDescription]` | Low · cacheable | (own) `getDielineEvaluationStatuses()`. |
| Q6 | `getCountries(codes): [Countries]` | Low · cacheable | (own) `getCountries(codes)`. |
| Q7 | `getPackagingElastic(parentHumanId): [Packaging]` | Medium | (🔴 search) `search.getPackagingElastic.load({ q:"parentId: {parentHumanId}" })` → `.content`. |

## Mutation Resolvers (10)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `addPackaging(sparkPackaging): Packaging` | Medium | (own) `addPackaging` `POST packaging/v1`. **Throw on `validationErrors`/`message`.** |
| M2 | `updatePackaging(packagingId, sparkPackaging): Packaging` | **High** | **multi-step:** 1) token; set `humanId=packagingId`; `PUT packaging/v1` (body); 2) if `attachmentsToRemove` → (🔴 attachment) `archiveAttachmentBulkV2` + (🟡 relationship) `removeRelationship`; 3) if `attachmentsToAdd` → (🟡 relationship) `addBulkRelationShip` (**reject on status≥400**) then (🔴 attachment) `bulkUpdateAttributes`; 4) **throw on `validationErrors`/`message`**. No rollback. |
| M3 | `evaluateDieline(dielineId, dielineEvaluation): Dieline` | Low | (own) `PUT packaging/v1/dielines/{dielineId}/evaluate`. |
| M4 | `bulkAddPackagings(bulkPackagingInput): PackagingBulk` | Medium | (own) `bulkAddPackagings`. **Throw on `validationErrors`/`message`.** |
| M5 | `bulkUpdatePackagings(bulkPackagingInput): PackagingBulk` | Medium | token for `packaging[].humanId` → (own) `bulkUpdatePackagings`. **Throw on error.** |
| M6 | `exportPackaging(workspaceId, workspaceDescription, ids): String` | Low | token → (own) `requestPackagingExport({workspace_id, workspace_description, product_ids})` → request id. |
| M7 | `lockPackaging(packagingId): Packaging` | Low | token → (own) `PUT packaging/v1/{id}/lock`. |
| M8 | `unlockPackaging(packagingId): Packaging` | Low | token → (own) `PUT packaging/v1/{id}/unlock`. |
| M9 | `cloneFilesForDielines(attachmentIds, cloneReferences): [Attachment]` | Medium | token → `Promise.all(attachmentIds.map(id => (🔴 attachment) cloneAttachmentV3({cloneReferences}, id)))`, flatten. No rollback. |
| M10 | `updatePackagingComponentStatus(productId, ids, status): PackagingPagedForStatus` | Low | (own) `updatePackagingComponentStatus({productId, ids, status})`. **No JWT — confirm.** |

## Field Resolvers (17)

**`Packaging` (12):**
- `access` (ACL context) — `accessControl.getPermissions([humanId])[0]`.
- `businessPartner` (🔵 vmm) — `loadBpsWithType([businessPartner])[0]`.
- `retailPrice` (deprecated) — `() => 0`.
- `suggestedRetailPriceByDPCI` (🔵 apex/pricing) — printers→`getDielines(printerIds)`→dpcis→`getRetailPriceByDpci`; gated on `requiresSuggestedRetailPrice` + bpId; else `[]`.
- `waveDescription` (🟡 tag) — `tag.getTag(wave).name` if `wave`, else `waveDescription`.
- `dielineEvaluators` (🟡 user-profile) — map `userAttributes.getUserByID`.
- `createdBy`/`updatedBy` (🟡 user-profile) — `getUser`.
- `product` (internal) — only if `parentId` starts `'PID'` → `product.getByID(parentId)`, else null.
- `workspaces` (🔴 search) — `getWorkspacesPagedV3({ q:"id:(...)" })` → `.content` (elastic, not the workspace service).
- `attachments` (🔴 search) — `searchAttachmentsByRelatedResource(humanId)`.
- `participantDetails` (🔵 user-profile) — `getUserGroup(humanId||id)`.

**`Dieline` (3):** `evaluatedBy` (🟡 user-profile), `attachments` (🔴 search), `attachment` (🔴 attachment `getAttachmentsV3([attachmentId])[0]`).
**`PrinterDieline` (1):** `dielines(statusIdFilter)` (own) — `getDielines({printerIds:[printerId], statusIds:statusIdFilter})`.
**`PackagingElement` (1):** `packagingLibrary` (internal fileLibrary) — `getPackageLibrary(packagingLibrary.id)`.

## Service Classes
- `PackagingService` base `packaging/v1`.
- Methods incl.
- `addPackaging` (POST), `updatePackaging` (PUT), `evaluateDieline` (PUT `/dielines/{id}/evaluate`), `manageWorkspaceAssociations` (PUT `/{id}/workspace_associations`), `bulkAddPackagings`/`bulkUpdatePackagings`, `getPackagings`, `getDielines`, `getPackagingById`, `getPackagingFieldValuesByType`, `getDielineEvaluationStatuses`, `getCountries`, `requestPackagingExport` (POST `/export`), `lockPackaging`/`unlockPackaging`, `updatePackagingComponentStatus` (PUT `/component_status_update`).

## EXT Service Call Inventory (summary)
- 7 EXT keys — **2 🔴** (search, attachment) · **3 🟡** (relationship, userAttributes, tag) · **2 🔵** (vmm, apex/pricing) · accessControl **context-only**.
- **Internal (same DGS):** product, fileLibrary, packaging (own).

## Key Findings
- **Highest risk:** `updatePackaging` (M2) — body + attachment remove/add (relationship + archive +
  attribute-update), no rollback; `suggestedRetailPriceByDPCI` (multi-hop pricing).
- **Latent / confirm:** `updatePackagingComponentStatus` has **no auth token**; the add-attachment branch
  rejects on `relationship.status>=400` but the remove branch does not.
- **Refactors:** attachment-by-search field resolvers → shared helper; clone fan-out → batch.
- **Quick wins:** the 6 simple reads, evaluateDieline, lock/unlock, export.
- **Preserve:** deprecated `retailPrice → 0`; `@deprecated` SDL fields; `waveDescription` tag fallback.

---
**Phase Completed:** Phase 2 · **Domain:** `packaging` · **EXT:** 7 keys (2🔴 · 3🟡 · 2🔵).
