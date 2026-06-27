# Measurement — Resolver Analysis: Field Resolvers

> **Domain:** `measurement` (+ `measurementTemplate`) · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

22 field resolvers across 4 type blocks.

---

## C1 · `SPARK_Measurements` (12 fields) — CAT-2 · Medium (3–5d)

| Field | Implementation |
|---|---|
| `access` | `accessControl.getPermissions.load({resourceIds:[humanId]})` → `[0]` |
| `currentUserPermissions` | `accessControl.getUserAccessUnencoded.load(humanId)` → `resourcePermissions[0]` |
| `businessPartners` | `measurementSet.businessPartnerIds && loadBps(ctx, ids)` (VMM) |
| `createdBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(createdBy)` |
| `updatedBy` | Same as createdBy |
| `product` | If `resourceId.indexOf('PID') === 0` → `product.getByID.load(resourceId)` else `null` |
| `workspaces` | `SPARK_WorkspaceV2.Query.getWorkspacesByIdsV2({}, {ids: workspaceContext}, ctx)` |
| `status` | Synthetic from `statusId` + `statusName` (no I/O) |
| `updatedFromResource` | `if updatedFromResource.type === 'sample' → sampleV2.getSampleById.load(id)` (single-case switch) |
| `measurementTemplates` | If `(measurementTemplates || []).map(t => t.id).length > 0` → `measurementTemplate.getMeasurementTemplatesByIds(ids)` → `.content` |
| `sizeTemplate` | If `sizeTemplate` set → `sizeTemplate.getSizeTemplates([sizeTemplate])` → `[0]` |
| `tightFitTemplate` | If `tightFitTemplate.{id,version}` set → `tightFit.getTightFitByIdAndVersion.load({id, version})` |
| `participantDetails` | `getUserGroup(ctx, humanId)` |

**Findings:**
- 🟡 `product` uses `resourceId` (the `@deprecated` field) instead of `parentId`. Confirm whether to keep or migrate to `parentId` during port.
- 🟡 `updatedFromResource` switch handles only `'sample'` — schema-typed as `SPARK_SampleV2` (single concrete type). If other resource types appear in data, they return `null`. Confirm with backend.
- 🟢 `status` synthetic field — pure projection, no I/O.

---

## C2 · `SPARK_SampleMeasurementSet` (2 fields) — CAT-2 · Small (<1d)

```
createdBy: sampleMeasurementSet.createdBy && userAttributes.getUserByIDOrNullIfNotFound.load(createdBy)
measurementSizeId: ms => ms.measurementSize && ms.measurementSize.code
```

`measurementSizeId` is a synthetic projection from `measurementSize.code` — no I/O.

---

## C3 · `SPARK_MeasurementTemplatesPaged` (3 fields) — CAT-2 · Small (<1d)

```
paging: t => ({totalPages, totalElements, first, numberOfElements, size, number, last, sort})
content: t => t.content
pageable: t => t.pageable
```
Whole-object projection; the parent is the raw paged response shape.

---

## C4 · `SPARK_MeasurementTemplate` (5 fields) — CAT-2 · Medium (3–5d)

| Field | Implementation |
|---|---|
| `createdBy` | `userAttributes.getUserByIDOrNullIfNotFound.load(createdBy)` |
| `updatedBy` | Same |
| `departments` | `(departmentIds && loadManyIncludeEmptyResponse(ig.department.getByID, ids, logContext)) || null` |
| `divisions` | `divisionIds && loadManyIncludeEmptyResponse(ig.division.getByID, ids, logContext)` |
| `brands` | `(brandIds && brandIds !== -1 && loadManyIncludeEmptyResponse(await ctx.loaders.brand.getBrand, brandIds, logContext)) || null` |

**Finding 🔴:** `brands` resolver does `await ctx.loaders.brand.getBrand` — that awaits the **loader function reference** itself, not a load call. This is almost certainly wrong. Likely intended:
```
await loadManyIncludeEmptyResponse(ctx.loaders.brand.getBrand, brandIds, logContext)
```
or
```
loadManyIncludeEmptyResponse(await ctx.loaders.brand.getBrand(...), brandIds, ...)
```
**Confirm behavior and fix during port.**

**Finding 🟡:** `brandIds !== -1` — sentinel for "all brands" or "no brands"? Document.

**Finding 🟢:** `loadManyIncludeEmptyResponse` is shared util — keep parity.

---

## Cross-Cutting Findings

| # | Finding | Severity |
|---|---|---|
| 1 | C4 `brands` field — `await` on loader reference (latent bug) | 🔴 |
| 2 | C1 `product` reads deprecated `resourceId` instead of `parentId` | 🟡 |
| 3 | C1 `updatedFromResource` polymorphism handles only one case (`sample`) | 🟡 |
| 4 | C4 `brandIds !== -1` sentinel — document | 🟡 |
| 5 | Multiple `userAttributes.getUserByIDOrNullIfNotFound.load(...)` calls — DataLoader memoization OK; preserve in port | 🟢 |
| 6 | `getUserGroup`, `loadBps`, `getWorkspacesByIdsV2` cross-utility imports — replace with native service-method calls or federation entity calls | 🟢 |
| 7 | All template field resolvers use `loadManyIncludeEmptyResponse` for partial-results tolerance — preserve | 🟢 |

---

## Effort

| Block | Tier | Days |
|---|---|---|
| C1 (Measurements × 12) | Medium | 3–5 |
| C2 (SampleMeasurementSet × 2) | Small | <1 |
| C3 (TemplatesPaged × 3) | Small | <1 |
| C4 (MeasurementTemplate × 5) | Medium | 3–5 |
| **Subtotal field resolvers** | | **7–12** |

---

**Phase Completed:** Phase 2C — Field Resolvers
