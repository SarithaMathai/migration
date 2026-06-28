# Phase 5: Attribute (Field) Inventory — Sample

> **Domain:** `sample` · **Target DGS:** separate `plm-sample` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`code/schemas/SPARK_SampleV2.txt`).
> `SampleV2` is wide (~35 field resolvers); this lists the non-trivial ones and groups the direct fields.

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — `SampleV2` (and sub-type) non-trivial field resolvers

| Type | Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|-----------|------------|-------|
| `SampleV2` | `asset` | `SampleAsset` | **Polymorphic** (union) | 🟡 material | High | A04/G02 |
| `SampleV2` | `product` | `Product` | EXT (PID prefix) | 🟡 product | High | G02 |
| `SampleV2` | `trim` | `Trim` | EXT | 🟡 trim | High | G02 |
| `SampleV2` | `colorArchroma` | `ColorArchroma` | EXT (ARCCLR prefixes) | 🟡 colorArchroma | High | G02 |
| `SampleV2` | `fabricSpecCombo` | `FabricSpecCombo` | EXT (FSC prefix) | 🟡 combination | High | G02 |
| `SampleV2` | `fabricSpec` | `FabricSpecification` | EXT (FAS prefix) | 🟡 fabric | High | G02 |
| `SampleV2` | `artwork` | `Artwork` | EXT (ART prefix) | 🟡 artwork | Medium | G02 |
| `SampleV2` | `createdBy`/`updatedBy`/`evaluatedBy` | `UserProfileAttributes` | EXT (system-user branch) | 🟡 user-profile | Medium | G01 |
| `SampleV2` | `designEvaluators`/`technicalEvaluators` | `[UserProfileAttributes]` | EXT | 🟡 user-profile | Medium | G01 |
| `SampleV2` | `createdByInternalPrimaryRole`/`evaluatedByInternalPrimaryRole` | `Role` | EXT | 🔵 role | Medium | G01 |
| `SampleV2` | `businessPartner`/`fabricSupplier`/`merchandiseVendors` | `VMM_BusinessPartner` | EXT | 🔵 vmm | Medium | G03 |
| `SampleV2` | `brand` | `VMM_Brand` | EXT | 🔵 brand | Low | G03 |
| `SampleV2` | `designPartnerId` | `[ID]` | Computed | — | Low | G03 |
| `SampleV2` | `workspace` | `WorkspaceV2` | EXT | 🟡 workspaceV2 | Medium | G04 |
| `SampleV2` | `sampleMeasurementSet` | `SampleMeasurementSet` | EXT (gated) | 🟡 measurement | Medium | G04 |
| `SampleV2` | `designCycle` | `Tag` | EXT | 🔵 tag | Low | G04 |
| `SampleV2` | `clmPackage` | `Spark_AsapEvaluation` | EXT | 🔵 tgtColorEvaluator | Low | G04 |
| `SampleV2` | `attachments` | `[Attachment]` | EXT (elastic) | 🔴 search | Medium | G05 |
| `SampleV2` | `rfidLocationInfo`/`currentLocations` | mixed | EXT (rfid latest reduce) | 🔴 search | Medium | G05 |
| `SampleV2` | `participants` | `SampleDiscussionsParticipantsV2` | EXT (userGroup branch) | 🔵 userGroup | Medium | G06 |
| `SampleV2` | `discussionParticipants` / `sampleMeasurementSetAssociation` | mixed | Computed | — | Low | G06/G04 |
| `SampleDepartment` | `department` | `IG_Department` | EXT | 🔵 ig | Low | G06 |
| `SampleDiscussionParticipantTeamInfoV2` | `businessPartner` | `VMM_BusinessPartner` | EXT (Target-0) | 🔵 vmm | Low | G06 |
| `SampleDiscussionParticipantUserInfoV2` | `userDetails` | `UserProfileAttributes` | EXT (system-user) | 🟡 user-profile | Low | G06 |
| `SampleLibraryColorsV2` | `color` | `LibraryColorV2` | EXT | 🟡 color | Low | G06 |

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `CreateSamplesInputV2` | `newSamples[].files` | `[String]` | No | drives the file-relationship side-effect (D01) |
| `Sample_RoundV2` | `dueDate`/`format`/`evaluationPurposes` | mixed | No | new round (D02) |
| `BulkSampleRound` | `id`/`dueDate` | `String!` | Yes | bulk-evaluate new rounds (E02) |
| `SampleUpdateSampleEvaluationInput` | `id` | `String!` | Yes | evaluation payload (E02 / drift) |
| `SampleAttachmentCloneRef` | `resourceId`/`businessPartner` | mixed | No | clone references (D07) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~30 (most of the SDL `SampleV2` scalars + value types) | Free — schema + DTO mapping (A02/B01) |
| Field-resolver (internal) | 0 | sample is its own subgraph |
| EXT (cross-domain) | ~25 across the entity + sub-types | DataLoader-batched federation/gateway lookups (G01–G06) |
| Polymorphic | 1 union (`SampleAsset`) | `@DgsTypeResolver` (A04) + per-member tests |

**Signal:** Sample is **wide and enrichment-heavy** with **prefix-gated polymorphic parents** — the cost is
the `SampleV2` field-resolver surface (G02 is the heaviest) and the evaluation writes; the long master-data
tail is cheap. One union (`SampleAsset`).

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `sample`.
