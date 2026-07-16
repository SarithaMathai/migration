# Phase 5: Attribute (Field) Inventory — Claims

> **Domain:** `claims` · **Target DGS:** separate `claims` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`schemas/SPARK_Claims.graphqls`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — non-trivial field resolvers

| Type | Attribute | GraphQL Type | Resolution | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|-----------|------------|-------|
| `Claims` | `access` | `AccessControl` | EXT (ACL context) | acl (context) | Medium | G01 |
| `Claims` | `currentUserPermissions` | `ResourcePermissions` | EXT (ACL context) | acl (context) | Medium | G01 |
| `Claims` | `participantDetails` | `UserGroup_Participants` | EXT | 🔵 user-profile | Low | G01 |
| `Claims` | `createdBy` / `updatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G02 |
| `Claims` | `businessPartner` | `VMM_BusinessPartner` | EXT (**3-way fallback**) | 🔵 vmm | Medium | G02 |
| `Claims` | `designPartner` | `VMM_BusinessPartner` | EXT | 🔵 vmm | Low | G02 |
| `Claims` | `product` | `Product` | EXT (federation; only if `parentId` starts `PID`) | 🟡 product | Medium | G03 |
| `Claims` | `parentDetails` | `ParentDetails` | EXT (loads parent product) | 🟡 product | High | G03 |
| `Claims` | `workspaces` | `[WorkspaceV2]` | EXT | 🟡 workspaceV2 | Low | G04 |
| `ParentDetails` | `otherClaimBps` | `[Int]` | EXT (elastic claims by parentId) | 🔴 search | Medium | G03 |
| `ParentDetails` | `systemTeams` | `TeamPaged` | EXT (elastic team search from BPs) | 🔴 search | High | G03 |
| `ParentDetails` | `droppedPartnerIds` | `[Int]` | Direct (from product) | — | Low | G03 |
| `ClaimSubstantiate` | `substantiatedBy` | `UserProfileAttributes` | EXT | 🟡 user-profile | Low | G04 |
| `ClaimDetails` | `claimName` | `String` | Computed (= `guestFacingClaim`) | — | Low | G04 |
| `Claims` | `status` | `CodeDescription` | Direct | — | Low | A02 |
| `Claims` | `statuses` | `[ProductComponentStatus]` | Direct | — | Low | A02 |

**Direct pass-throughs:** `Claims.{humanId, parentId, version, claimName, additionalInfo, claimNotes,
- manualLock, subjectiveStatements, workspaceContext, claimDetails, createdAt, updatedAt, partners}`; `ClaimDetails.{id, claimCategory, technicalClaim, claimId, claimDescription, guestFacingClaim, guestFacingClaimId, appliesTo, status, communicationChannel, shareWithGuests, claimsAbout, packagingCopy}`; all of `ClaimPackagingCopy`, `ClaimSubstantiate.{substantiated, substantiatedAt}`, `ClaimExport`, `Guest_Facing`, `CommunicationChannel` — DTO-mapped, no resolver.
- Covered by A02 + B01/B02.

## Table 2 — Input objects (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `ClaimsInput` | `workspaceContext` | `[ID]` | No | **create**: plain id list |
| `ClaimsUpdateInput` | `workspaceContext` | `PartialWorkspaceAssociationsInput` | No | **update**: add/remove (drives the multi-step write, E01) |
| `ClaimsUpdateInput` | `partner` / `dpPartner` | `PartnerDetails` | No | feed the `businessPartner`/`designPartner` resolution |
| `ClaimsUpdateInput` | `statuses` | `[ProductComponentStatusUpdateInput]` | No | per-workspace status updates |
| `BulkClaimsUpdateInput` | `updateClaimDtoList` | `[ClaimsUpdateInput]` | No | bulk update (D02) |
| `ClaimDetailsInput` | `vendorSubstantiate` | `ClaimSubstantiateInput` | No | substantiation flag |

## Table 3 — Summary roll-up

| Resolution kind | ~# fields | Migration signal |
|-----------------|-----------|------------------|
| Direct / Computed | ~36 | Free — schema + DTO mapping (A02/B01) |
| Field-resolver (internal) | 0 | claims is its own subgraph — nothing co-located |
| EXT (cross-domain) | ~15 | federation/elastic; 2 via 🔴 search; product is cross-subgraph |
| Polymorphic | 0 | none |

**Signal:** Claims is **shallow but federation-heavy** — most fields are direct, but as a standalone
- subgraph every reference (Product, search, workspace, user-profile, VMM) is cross-subgraph.
- Cost concentrates in `updateClaim` (proxy-ACL multi-step, E01) and the `parentDetails` elastic lookups (G03).
- No polymorphism.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `claims`.
