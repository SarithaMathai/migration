# Phase 5: Attribute (Field) Inventory — Impression

> **Domain:** `impression` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source:** [03-schema.graphql](./03-schema.graphql) + [02-resolver-analysis.md](./02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`schemas/SPARK_Impression.graphqls`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — Object-type attributes (non-trivial)

| Type | Attribute | GraphQL Type | Resolution | Resolver Loc | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|--------------|-----------|------------|-------|
| `Impression` | `businessPartners` | `[VMM_BusinessPartner]` | EXT | `resolvers/SPARK_Impression.js:31` | 🔵 vmm | Low | G01 |
| `Impression` | `owningBusinessPartner` | `VMM_BusinessPartner` | EXT | `:32` | 🔵 vmm | Low | G01 |
| `Impression` | `workspaces` | `[WorkspaceV2]` | EXT | `:33-39` | 🟡 workspaceV2 | Low | G01 |
| `Impression` | `createdBy` | `UserProfileAttributes` | EXT | `:40-41` | 🔵 user-profile | Low | G01 |
| `Impression` | `updatedBy` | `UserProfileAttributes` | EXT | `:42-43` | 🔵 user-profile | Low | G01 |
| `ImpressionCount` | `counts` | `[CountsByBp]` | Computed + EXT (internal product) | `:46-65` | — (internal product) | Medium | G02 |

**Direct pass-throughs (from the impression record):** `id, name, parentId, version,
- owningPartnerId, owningPartnerType, workspaceContext, deletable, associatedBomIds, attachmentId, relatedResources, sortOrder, createdAt, updatedAt` — all DTO-mapped, no resolver.
- Covered by A02 schema + B01/B02 mapping.
- (`partnerIds` exists on the data record and is read internally by `businessPartners`/ `counts`, but is **not** an exposed field in the SDL `SPARK_Impression` type.)

## Table 2 — Input-object attributes

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `ProductImpressionInput` | `impressionsToDelete` | `[String]` | No | ids to remove in `updateImpressions` |
| `ProductImpressionInput` | `impressionsToUpdate` | `[ImpressionInput]` | No | upsert set |
| `ImpressionInput` | `id` | `String` | No | absent → create |
| `ImpressionInput` | `partnerIds` / `businessPartners` | `[ID]` / `[ProductPartnerInput]` | No | partner assignment |
| `ImpressionInput` | `workspacesToAdd` / `workspacesToRemove` | `[String]` | No | workspace assoc within update |
| `ProductPartnerInput` | `partnerId` / `partnerType` | `ID` / `Int` | No | |

## Table 3 — Summary roll-up

| Resolution kind | # fields | Migration signal |
|-----------------|----------|------------------|
| Direct | ~15 | Free — schema + DTO mapping |
| EXT (cross-domain) | 5 | federated references (1 🟡 workspace, 2 🔵 vmm, 2 🔵 user-profile) |
| Computed + internal | 1 (`counts`) | small aggregation + internal product call |
| Polymorphic | 0 | — |

**Signal:** Impression is almost entirely direct pass-throughs plus 5 simple federated-reference fields and
one small aggregation. **Lowest-risk domain — recommended first/early migration.**

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `impression`.
