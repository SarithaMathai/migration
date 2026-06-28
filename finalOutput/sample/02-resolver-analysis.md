# Phase 2: Resolver Dependency Analysis — Sample

> **Domain:** `sample` · **Target DGS:** `SampleServiceV2` → separate `plm-sample` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `code/schemas/SPARK_SampleV2.txt` (SDL), `code/resolvers/SPARK_SampleV2.txt` (430), `code/services/SampleV2.txt` (309)
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full

Implementation spec. ACL/JWT usage is **context-only**. `sample` is its **own subgraph**. Base `samples/v2`.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | 23 |
| Mutation resolvers | 9 (+3 schema-drift) |
| Field resolvers | ~45 (incl. 1 union `__resolveType`) |
| Service methods | ~30 |
| EXT loaders | ~20 (1 🔴 · ~13 🟡 · ~6 🔵) + accessControl context |
| High complexity | 3 (`bulkEvaluateSamples`, `updateSamplesV2`, polymorphic parent hydration) |

---

## Query Resolvers (23)

| # | Query | Complexity | Pseudo-logic |
|---|-------|-----------|--------------|
| Q1 | `getSampleById(id)` | Low | (own) `getSampleById.load(id)`. |
| Q2 | `getSamplesByIdsV2(ids)` | Medium | **batched** `batchParallelOperation(chunk)` → (ACL) token per batch → (own) `getSamplesByIdsV2ByPost`. **Side-effect:** if exactly one → (🔵 recentlyViewed) `addRecentlyViewed({id, type:'sample'})`. |
| Q3 | `getSamplesByParentId(humanId)` | Medium | (🟡 relationship) `getByID({id, type:'sample', maxDepth:0})` → ids → (ACL) token → (own) `getSamplesByIdsV2`; empty → []. |
| Q4 | `getColorSamplesByParentId(id)` | Low | (own) `getColorSamplesByParentId.load(id)`. |
| Q5 | `getSampleRounds(humanId)` | Low | (ACL) token → (own) `getSampleRounds`. |
| Q6 | `getSampleLocationByIds(ids)` | **High** | batched samples → for each with `rfidTagIds` → (🔴 search) `searchLatestRfidLocations({q: tagIds OR-joined})` → reduce to latest `lastSeen` → `{id, locationDescription, lastSeen}`; flatten. |
| Q7 | `getSamplesByRfidTagIds(ids)` | Medium | (ACL) token → (own) `getSamplesByRfidTagIds`. |
| Q8 | `getSampleNotificationErrors` | Low | (🟡 notification) `getSampleNotificationErrors`. |
| Q9 | `getSampleExports` | Low | (own) `getSampleExports`. |
| Q10–Q23 | master-data: `getSampleMaterialTypesV2`, `getSampleTypesV2(resourceTypes)`, `getFabricSampleTypesV2`, `getSampleProductTypesV2`, `getSampleTrackingTypesV2`, `getSampleLateReasonTypesV2`, `getColorSamplePurposesV2`, `getMaterialSampleEvaluationTypesV2`, `getProductSampleEvaluationTypesV2`, `getWashSampleTypesV2`, `getSampleFormats(type)`, `getMaterialSampleFormats(type)`, `getSampleEvaluationPurposes`, `getSampleTypeFormatMappings` | Low · cacheable | thin (own) master-data loads. |

## Mutation Resolvers (9 impl + 3 schema-drift)

| # | Mutation | Complexity | Pseudo-logic |
|---|----------|-----------|--------------|
| M1 | `createSamplesV2(samples)` | Medium | (own) `createSamplesV2`; **if first new sample has files** → (🟡 relationship) `createSampleAttachmentRelationship` + (ACL) token + (🟡 attachment) `bulkUpdateAttributes` (stamp resource/related). No rollback. |
| M2 | `updateSamplesV2(samples)` | **High** | (ACL) token for all `updateSamples[].id` + `SAMPLE_EVALUTION` → (own) `updateSamplesV2`. |
| M3 | `updateSampleWorkspaceAssociation(sampleId, workspaceId)` | Low | (ACL) token → (own) `updateSampleWorkspaceAssociation`. |
| M4 | `createSampleRoundV2(sample, sampleId)` | Low | (ACL) token for `[sampleId, SAMPLE_EVALUTION]` → (own) `createSampleRoundV2`. |
| M5 | `bulkEvaluateSamples(updateSamples, newSampleRounds)` | **High** | delegates to `bulkEvaluateSampleUtil(ctx, updateSamples, newSampleRounds)` — evaluation + new-round creation orchestration. |
| M6 | `requestSampleExport` | Low | (own) `requestSampleExport`. |
| M7 | `retrySampleNotificationError(failedMessageId)` | Low | (🟡 notification) `retrySampleNotificationError`. |
| M8 | `retryAllSampleNotificationErrors` | Low | (🟡 notification) `retryAllSampleNotificationErrors`. |
| M9 | `bulkCloneFilesForEvaluate(attachmentIds, cloneReferences)` | Medium | (ACL) token → `Promise.all(attachmentIds.map(id => (🟡 attachment) cloneAttachmentV3({cloneReferences}, id)))`, flatten. |
| ⏭ | `updateSampleEvaluations`, `dropSamples`, `undropSamples` | — | **schema-drift** — in the SDL, no top-level resolver; drop/undrop are called as service methods inside the workspace partner-action dispatcher. |

## Polymorphism · `SPARK_SampleAsset.__resolveType`
Union → `SPARK_Color` (if `isColorId(humanId)`) | `SPARK_Artwork` (if humanId starts with the Artworks
prefix) | null. **DGS:** `@DgsTypeResolver(name="SampleAsset")` mirroring the prefix logic.

## Field Resolvers (`SPARK_SampleV2`, ~35 + 6 sub-type blocks)
- **Users (system-user branch):** `createdBy`/`updatedBy`/`evaluatedBy` (🟡 user; `systemGenerated` →
  `systemUser`), `designEvaluators`/`technicalEvaluators` (🟡 user map),
  `createdByInternalPrimaryRole`/`evaluatedByInternalPrimaryRole` (🔵 role `getPage`).
- **Prefix-gated parents (→ SampleAsset/union members):** `product` (PID, 🟡 product), `colorArchroma`
  (ARCCLR/TARARCCLR/REFARCCLR, 🟡 colorArchroma), `fabricSpecCombo` (FSC, 🟡 combination), `fabricSpec`
  (FAS, 🟡 fabric), `artwork` (ART, 🟡 artwork), `asset` (🟡 material `getMaterialByIdFromService`),
  `trim` (🟡 trim), `clmPackage` (🔵 tgtColorEvaluator).
- **Partners:** `businessPartner`/`fabricSupplier` (🔵 vmm), `merchandiseVendors` (🔵 vmm), `brand` (🔵 brand),
  `designPartnerId` (computed).
- **Workspace / measurement / tag:** `workspace` (🟡 workspace `getWorkspaceV2`), `sampleMeasurementSet`
  (🟡 measurement `getSampleMeasurement` — F02), `sampleMeasurementSetAssociation` (computed), `designCycle` (🔵 tag).
- **Attachments / rfid:** `attachments` (🔴 search), `rfidLocationInfo`/`currentLocations` (🔴 search rfid).
- **Participants:** `discussionParticipants` (computed), `participants` (🔵 userGroup, `isParticipantsFromUserGroup` branch).
- **Sub-types:** `SampleDepartment.department` (🔵 ig), `SampleDiscussionParticipantTeamInfoV2.businessPartner`
  (🔵 vmm, Target-0 case), `SampleDiscussionParticipantUserInfoV2.userDetails` (🟡 user/systemUser),
  `SampleDiscussionsParticipantsV2.teams`/`users` (computed), `SampleLibraryColorsV2.color` (🟡 color).

## Service Classes
`SampleServiceV2` base `samples/v2` (+ `samples/export`). ~30 methods: by-id/byPost, rounds, master-data
types/formats/purposes/mappings, create/update/round/workspace-assoc, drop/undrop (service-level), exports,
rfid, color samples.

## EXT Service Call Inventory (summary)
~20 keys — **1 🔴** (search) · ~13 🟡 (product, workspace, measurement, relationship, attachment, notification,
userAttributes, trim, colorArchroma, color, combination, fabric, artwork, material) · ~6 🔵 (vmm, brand, ig,
tag, role, recentlyViewed, userGroup, tgtColorEvaluator) · accessControl **context**.

## Key Findings
- **Highest cost:** the **wide `SampleV2` type** with prefix-gated parent hydration + the polymorphic
  `SampleAsset` union; `bulkEvaluateSamples` and `updateSamplesV2`.
- **Schema-drift:** `updateSampleEvaluations`/`dropSamples`/`undropSamples` (deferred — drop/undrop owned by
  the workspace dispatcher at runtime).
- **Federation provider:** sample provides `SampleV2` for product `samples`/`sampleIds`, measurement
  `SampleV2.sampleMeasurement`, and workspace.
- **Quick wins:** the ~13 cacheable master-data reads; notification retries; export.

---
**Phase Completed:** Phase 2 · **Domain:** `sample` · **EXT:** ~20 keys (1🔴 · ~13🟡 · ~6🔵).
