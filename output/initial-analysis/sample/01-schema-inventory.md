# Phase 1: Schema Inventory — Sample

> **Domain:** `sample`
> **Target DGS:** `SampleServiceV2` → **separate `plm-sample` subgraph**
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_SampleV2.graphqls` (513-line SDL) + `resolvers/SPARK_SampleV2.js` (430) + `services/SampleV2.js` (309)
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

No `context.js`. `SampleServiceV2 extends SparkService` builds its endpoint in the constructor
(`services/SampleV2.js:14`):

```js
this.endpoint = `${endpoint}/enterprise_product_development_samples/v2`
this.exportEndpoint = `${endpoint}/enterprise_product_development_samples/export`
```

> The base path is `enterprise_product_development_**samples**` (distinct from the product family's
> `_products` base), so sample is its **own backend / subgraph** → **`plm-sample`** (per platform direction).

| Setting | Value |
|---|---|
| Loader key | `sampleV2` |
| Service class | `SampleServiceV2 extends SparkService` |
| Backend / DGS | **`plm-sample`** (separate subgraph + backend) |
| Auth | base `Authorization` + per-call `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | **separate `plm-sample` subgraph** (referenced by product `samples`, measurement, workspace) |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `schemas/SPARK_SampleV2.graphqls` | 513 | the source SDL — 23 queries, 12 mutations, `SampleV2` + ~25 value types, ~10 inputs, 1 union |
| `resolvers/SPARK_SampleV2.js` | 430 | 23 queries, 9 mutations, `SampleV2` (~35 field resolvers) + a `__resolveType` union + 6 sub-type blocks |
| `services/SampleV2.js` | 309 | ~30 REST methods (`samples/v2` + export) |
| **Total** | **1,252** | mid-large domain — no chunked reading needed |

Schema: **`schemas/SPARK_SampleV2.graphqls` (513 lines)** — target schema in [03-schema.graphql](./03-schema.graphql)
translated from it (nullability from the SDL).

## 3. Import Graph
```
resolvers/SPARK_SampleV2.js imports:
  resolvers/SPARK_WorkspaceV2 (getWorkspaceV2), SPARK_Material (getMaterialByIdFromService)
  utils/commonLoaders (getUserPermissionsJWT[Helper]), vmmUtils (loadBps, loadBpWithType),
  sampleUtils (bulkEvaluateSampleUtil), discussionUtils (createSampleAttachmentRelationship),
  materials/colorUtils (isColorId), userGroupUtils (getParticipantsByUserGroup), userAttributesUtils (systemUser),
  batchingUtils (batchParallelOperation)
SampleServiceV2 extends SparkService; uses loadListing/loadOne/postOne/putOne/convertFunctions
```

## 4. Cross-Domain Reference Table (all cross-subgraph — sample is its own DGS)

| Field / op | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `attachments`, rfid (`searchLatestRfidLocations`) | `search` | SearchService (elastic) | federation | 🔴 |
| `product` (+ parents) | `product` | ProductService | federation | 🟡 |
| `workspace` | `workspaceV2` | WorkspaceService | federation | 🟡 |
| `sampleMeasurementSet` | `measurement` | MeasurementService | federation | 🟡 |
| relationship tree (`getSamplesByParentId`, create rel) | `relationship` | RelationshipService | federation | 🟡 |
| `bulkUpdateAttributes` (create), `cloneAttachmentV3` (bulkClone) | `attachment` | AttachmentService | federation | 🟡 |
| notification errors / retry | `notification` | NotificationService | federation | 🟡 |
| created/updated/evaluated users, evaluators, participant users | `userAttributes` / `userGroup` | UserProfileService | federation | 🟡 |
| `trim`/`colorArchroma`/`color`/`combination`/`fabric`/`artwork`/`asset(material)`/`clmPackage`/`role` | various | material/color/fabric/artwork/role/tgtColorEvaluator DGSs | federation | 🟡/🔵 |
| business/fabric/merch partners, `brand`, `department`, `designCycle` | `vmm`/`brand`/`ig`/`tag` | platforms | Gateway stitch | 🔵 |
| `addRecentlyViewed` (getSamplesByIdsV2 side-effect) | `recentlyViewed` | UserProfileService | federation | 🔵 |
| reads/writes capability tokens | `accessControl` | AccessControlService | **context only** | n/a |

## 5. Co-located Siblings
**None** — `sample` is its **own DGS** (`plm-sample`). It is **referenced as an entity** by product
(`Product.samples`, `sampleIds`), measurement (`SampleV2.sampleMeasurement` — F02), and workspace
(drop/undrop samples, sampleReport). All its outbound calls (above) are cross-subgraph.

## 6. Hot Spots
1. **Polymorphism** — `SPARK_SampleAsset.__resolveType` (`:200-209`) union → `SPARK_Color` | `SPARK_Artwork`
   (by humanId prefix). **+1 complexity tier**; needs a `@DgsTypeResolver`.
2. **Wide entity** — `SPARK_SampleV2` has **~35 field resolvers** with **prefix-gated parent hydration**
   (`product` PID, `colorArchroma` ARCCLR/TARARCCLR/REFARCCLR, `fabricSpecCombo` FSC, `fabricSpec` FAS,
   `artwork` ART, `asset` via material) — the bulk of the work.
3. **`bulkEvaluateSamples`** (`:163-166`) — delegates to `bulkEvaluateSampleUtil` (eval + new rounds). Complex.
4. **`updateSamplesV2`** (`:167-176`) — multi-id token + evaluation.
5. **`createSamplesV2`** (`:127-153`) — create + (relationship) attachment relationship + (attachment)
   `bulkUpdateAttributes` for uploaded files. No rollback.
6. **`getSamplesByIdsV2`** (`:23-39`) — **batched** (`batchParallelOperation`, chunk size) + side-effect
   `addRecentlyViewed` when exactly one sample.
7. **RFID** — `getSampleLocationByIds`/`getSamplesByRfidTagIds`/`rfidLocationInfo`/`currentLocations` resolve
   latest RFID locations via (🔴 search) with a `lastSeen` reduce.
8. **`sampleMeasurementSet`** (`:329-337`) — calls (🟡 measurement) `getSampleMeasurement` — the sample side of
   the measurement/product sample-measurement federation (`SPARK-MEAS-F02` / `SPARK-PROD-F03`).
9. **Schema-drift mutations** — `updateSampleEvaluations`, `dropSamples`, `undropSamples` are in the SDL but
   have **no top-level resolver** (drop/undrop are called as service methods inside the workspace dispatcher).
   Deferred ⏭.
10. **System-user branch** — `createdBy`/`updatedBy`/participant users special-case `systemGenerated`/`systemUser`.

## 7. Operation Lists
**Queries (23):** by-id/parent (`getSampleById`, `getSamplesByIdsV2`, `getSamplesByParentId`,
`getColorSamplesByParentId`, `getSampleRounds`); rfid (`getSampleLocationByIds`, `getSamplesByRfidTagIds`);
ops (`getSampleNotificationErrors`, `getSampleExports`); master-data (`getSampleMaterialTypesV2`,
`getSampleTypesV2`, `getFabricSampleTypesV2`, `getSampleProductTypesV2`, `getSampleTrackingTypesV2`,
`getSampleLateReasonTypesV2`, `getColorSamplePurposesV2`, `getMaterialSampleEvaluationTypesV2`,
`getProductSampleEvaluationTypesV2`, `getWashSampleTypesV2`, `getSampleFormats`, `getMaterialSampleFormats`,
`getSampleEvaluationPurposes`, `getSampleTypeFormatMappings`).
**Mutations (9 impl + 3 schema-drift):** createSamplesV2, updateSamplesV2, updateSampleWorkspaceAssociation,
- createSampleRoundV2, bulkEvaluateSamples, requestSampleExport, retrySampleNotificationError, retryAllSampleNotificationErrors, bulkCloneFilesForEvaluate.
- **Deferred ⏭:** updateSampleEvaluations, dropSamples, undropSamples.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | 23 (incl. ~13 cacheable master-data) |
| Mutations | 9 (+3 schema-drift) |
| Object types | ~25 (`SampleV2`, rounds/colors/aesthetics/library-color/participants/department/…) |
| Field resolvers | ~45 (35 on `SampleV2` + 6 sub-type blocks) |
| Unions (`__resolveType`) | 1 (`SampleAsset` → Color/Artwork) |
| Service methods | ~30 |
| Cross-domain loader keys | ~20 (all cross-subgraph) |
| EXT calls | 1 🔴 (search) · ~13 🟡 · ~6 🔵 · accessControl context |
| Large files | 0 (largest 513) |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `sample` · **Files:** 3 (1,252 lines: schema 513 + resolver 430 + service 309).
