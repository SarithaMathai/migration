# Phase 1: Schema Inventory — Packaging

> **Domain:** `packaging`
> **Target DGS:** `PackagingService` → `plm-product` (co-located)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_Packaging.graphqls` (453-line SDL) + `resolvers/product/SPARK_Packaging.js` + `services/product/Packaging.js`
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

No `context.js` in the snapshot. The endpoint is built in the service constructor
(`services/product/Packaging.js:10`):

```js
this.endpoint = `${endpoint}/enterprise_product_development_products/packaging/v1`
```

| Setting | Value |
|---|---|
| Loader key | `packaging` |
| Service class | `PackagingService` |
| Backend base | `https://spark-product.dev.target.com` (repo `spark-product`) |
| Base path | `${endpoint}/enterprise_product_development_products/packaging/v1` |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | `plm-product` (co-located — internal to the product family) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_Packaging.graphqls` | 453 | the source SDL — 7 queries, 10 mutations, `Packaging`/`Dieline`/`PrinterDieline`/`PackagingElement` + ~20 value types, ~20 inputs |
| `resolvers/product/SPARK_Packaging.js` | 273 | 7 queries, 10 mutations, 4 type blocks (17 field resolvers) |
| `services/product/Packaging.js` | 164 | REST methods on `packaging/v1` + dielines + export |
| **Total** | **890** | mid domain — no chunked reading |

- Schema: **`schemas/SPARK_Packaging.graphqls` (453 lines)** — target schema in [03-schema.graphql](./03-schema.graphql) translated from it (nullability from the SDL).
- The SDL is **wide** (~24 object types, ~20 inputs).

## 3. Import Graph
```
resolvers/SPARK_Packaging.js
├── utils/vmmUtils                  → loadBpsWithType (VMM partner)
├── utils/commonLoaders            → getUserPermissionsJWT, addBulkRelationShip, removeRelationship (ACL + relationship)
├── utils/Product/userGroupUtils   → getUserGroup (participants)
├── utils/userAttributesUtils      → getUser (created/updated/evaluators)
├── utils/packaging/getRetailPriceByDpci → getRetailPriceByDpci (suggested retail price)
└── resolvers/SPARK_WorkspaceV2    → (imported; workspaces actually resolved via elastic search)
services/PackagingService.js uses postOne, putOne, loadListing, loadOne, convertFunctions
```

## 4. Cross-Domain Reference Table

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `getPackagingElastic`, `workspaces`, `attachments`, `Dieline.attachments` | `search` | SearchService (elastic) | federation | 🔴 |
| `updatePackaging` (archive + bulkUpdateAttributes), `cloneFilesForDielines`, `Dieline.attachment` | `attachment` | AttachmentService | federation | 🔴 |
| `updatePackaging` (addBulkRelationShip / removeRelationship) | `relationship` | RelationshipService | federation | 🟡 |
| `createdBy`/`updatedBy`/`dielineEvaluators`/`Dieline.evaluatedBy` | `userAttributes` | UserProfileService | federation | 🟡 |
| `waveDescription` | `tag` | TagService | federation | 🟡 |
| `businessPartner` | `vmm` | VMM platform | Gateway stitch | 🔵 |
| `suggestedRetailPriceByDPCI` (`getRetailPriceByDpci`) | apex / pricing | APEX/pricing platform | Gateway stitch | 🔵 |
| `participantDetails` | `userGroup` / user-profile | UserProfileService | federation | 🔵 |
| `product` | `product` | ProductService (same DGS) | **internal** | — |
| `PackagingElement.packagingLibrary` | `fileLibrary` | FileLibraryService (same DGS) | **internal** | — |
| `PrinterDieline.dielines`, `suggestedRetailPrice` dieline lookups | `packaging` | PackagingService (own) | **owned** | — |
| `access`, all reads/writes | `accessControl` (getUserPermissionsJWT) | AccessControlService | **context only — ACL ignored** | n/a |

## 5. Co-located Siblings
- `product`, `bom`, `measurement`, `productDetails`, `impression`, `fileLibrary` — share `plm-product`.
- `Product.components(...packaging)` / `Product.packagingAttributes` resolve **internally**, not cross-subgraph.

## 6. Hot Spots
1. **`updatePackaging`** (`:24-87`) — **multi-step write**: 1) `PUT packaging/v1` (body); 2) if
   `attachmentsToRemove` → (🔴 attachment) `archiveAttachmentBulkV2` + (🟡 relationship) `removeRelationship`;
   3) if `attachmentsToAdd` → (🟡 relationship) `addBulkRelationShip` (rejects on status≥400) **then**
   (🔴 attachment) `bulkUpdateAttributes`; 4) throw on `validationErrors`/`message`. No rollback.
2. **`suggestedRetailPriceByDPCI`** (`:189-204`) — only when `requiresSuggestedRetailPrice` and a BP id:
   collect printer ids from `packagingElements` → (own) `getDielines(printerIds)` → dpcis →
   (🔵 apex/pricing) `getRetailPriceByDpci`. Else `[]`.
3. **`cloneFilesForDielines`** (`:129-140`) — per-attachment `Promise.all` (🔴 attachment) `cloneAttachmentV3`.
4. **`updatePackagingComponentStatus`** (`:141-142`) — **no JWT** (no token — confirm backend-enforced).
5. **`waveDescription`** (`:205-212`) — if `wave` set → (🟡 tag) `getTag(wave).name`, else `waveDescription`.
6. **`workspaces`** (`:223-234`) — resolved via (🔴 search) `getWorkspacesPagedV3` elastic `id:(... OR ...)`
   (despite `SPARK_WorkspaceV2` import — it does **not** use the workspace service here).
7. **Entity keys** — `SPARK_Packaging` and `SPARK_Dieline` use `humanId` (no `id` field). `@key` = `humanId`.
8. **Deprecated fields** — `retailPrice` (`() => 0`), several `@deprecated` SDL fields/inputs — preserve.

## 7. Operation Lists
**Queries (7):** getPackagings, getPackagingElastic, getPackagingById, getPackagingFieldValuesByType,
getDielines, getDielineEvaluationStatuses, getCountries.
**Mutations (10):** addPackaging, updatePackaging, evaluateDieline, bulkAddPackagings, bulkUpdatePackagings,
exportPackaging, lockPackaging, unlockPackaging, cloneFilesForDielines, updatePackagingComponentStatus.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 7 |
| Mutations | 10 |
| Object types | ~24 (`Packaging`, `Dieline`, `PrinterDieline`, `PackagingElement`, printing/warnings/contact/…) |
| Field resolvers | 17 (12 `Packaging`, 3 `Dieline`, 1 `PrinterDieline`, 1 `PackagingElement`) |
| Service methods | ~16 |
| Cross-domain loader keys | 8 (+ accessControl context-only + 3 internal) |
| EXT calls | 2 🔴 · 3 🟡 · 2 🔵 |
| Interfaces / unions | 0 |
| Large files | 0 (schema is wide but < 1000 lines) |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `packaging` · **Files:** 3 (890 lines: schema 453 + resolver 273 + service 164).
