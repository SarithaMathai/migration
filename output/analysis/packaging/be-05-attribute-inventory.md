# Phase 5: Attribute (Field) Inventory — Packaging

> **Domain:** `packaging` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [be-03-schema.graphql](./be-03-schema.graphql) + [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`schemas/SPARK_Packaging.graphqls`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` (internal) · `EXT` (severity) · `Polymorphic`.

## Table 1 — non-trivial field resolvers

| Type | Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|-----------|------------|-------|
| `Packaging` | `access` | `AccessControl` | EXT (ACL context) | acl (context) | Medium | G01 |
| `Packaging` | `businessPartner` | `VMM_BusinessPartner` | EXT | 🔵 vmm | Medium | G01 |
| `Packaging` | `participantDetails` | `UserGroup_Participants` | EXT | 🔵 user-profile | Low | G01 |
| `Packaging` | `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G02 |
| `Packaging` | `dielineEvaluators` | `[UserProfileAttributes]` | EXT | 🟡 user-profile | Low | G02 |
| `Packaging` | `product` | `Product` | Field-resolver (internal) | — same DGS (only if `parentId` starts `PID`) | Low | G03 |
| `Packaging` | `workspaces` | `[WorkspaceV2]` | EXT (elastic) | 🔴 search | Medium | G03 |
| `Packaging` | `attachments` | `[SearchAttachment]` | EXT (elastic) | 🔴 search | Medium | G03 |
| `Packaging` | `suggestedRetailPriceByDPCI` | `[SuggestedRetailPriceByDPCI]` | EXT (dielines→DPCIs→pricing) | 🔵 apex/pricing | High | G04 |
| `Packaging` | `waveDescription` | `String` | EXT (tag name fallback) | 🟡 tag | Medium | G04 |
| `Packaging` | `retailPrice` | `Float` | Computed (deprecated → 0) | — | Low | G04 |
| `Dieline` | `evaluatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G05 |
| `Dieline` | `attachments` | `[SearchAttachment]` | EXT (elastic) | 🔴 search | Low | G05 |
| `Dieline` | `attachment` | `Attachment` | EXT | 🔴 attachment | Low | G05 |
| `PrinterDieline` | `dielines(statusIdFilter)` | `[Dieline]` | Field-resolver (own) | — packaging | Low | G05 |
| `PackagingElement` | `packagingLibrary` | `SpgFileLibrary` | Field-resolver (internal) | — fileLibrary | Low | G05 |
| `Packaging` | `status` / `statuses` | `CodeDescription` / `[ProductComponentStatus]` | Direct | — | Low | B01 |

**Direct pass-throughs (from the record):** `Packaging.{humanId, placeholderId, parentId, description,
promoDescription, descriptionDisplayText, wave, requiresSuggestedRetailPrice, projectType(+Name),
projectItemType(+Name), projectLevel(+Name), group(+Name), creativePath(+Name), archived, dielineDueDate,
handoffDueDate, workspaceIds, photoRequired, illustrationRequired, notes, selectedComponents,
resolvedSelectedComponents, version, contactInformation, warningsAndCautions(+List),
copyWriterEditAndApproved, packagingElements, packagingInternalData, fulfillmentTypeId(+Name), orderCode,
manualLock, createdAt, updatedAt}`; plus all of `Dieline` (non-resolver fields), `PrinterDieline`,
`PrintingProcess`, `WarningsAndCautions`, `ContactInformation`, etc. — DTO-mapped, no resolver.

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `PackagingInput` | `parentId` | `String!` | Yes | the product |
| `PackagingInput` | `businessPartner` | `PackagingPartnerInput!` | Yes | required partner |
| `PackagingInput` | `dielineDueDate` / `statusId` | `String!` / `Int!` | Yes | required on create |
| `PackagingInput` | `attachmentsToAdd` / `attachmentsToRemove` | mixed | No | drive the multi-step update (E01) |
| `PackagingInput` | `claimId` / `claimDetails` | mixed | No | **claims pass-through** — confirm ownership |
| `DielineEvaluationInput` | `statusId` / `workspaceIds` | `Int!` / `[String]!` | Yes | dieline evaluation (D02) |
| `DielineAttachmentCloneRef` | `resourceId` / `businessPartner` | `String!` / `ProductPartnerInput!` | Yes | clone references (D08) |
| `ComponentStatusInput` | `workspaceId` | `String!` | Yes | matches `SPARK_ComponentStatusInput` (D09) |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~70 | Free — schema + DTO mapping (A02/B01); the schema is wide |
| Field-resolver (internal, same DGS) | 3 | `product`, `PrinterDieline.dielines`, `packagingLibrary` — cheap |
| EXT (cross-domain) | ~14 | federation/elastic; the pricing chain (G04) is the costliest |
| Polymorphic | 0 | none |

**Signal:** Packaging is **wide but mostly direct** — the cost is the **schema breadth** (A02), the
multi-step `updatePackaging` write (E01), and the `suggestedRetailPriceByDPCI` pricing chain (G04). No
polymorphism.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `packaging`.
