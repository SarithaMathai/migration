# Phase 3: Federation Schema Analysis — Measurement

> **Domain:** `measurement` · **Target DGS:** `MeasurementService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26 · **Sub-domains folded in:** 2026-07-19
> **Schema:** [be-03-schema.graphql](./be-03-schema.graphql) · **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 30 🔜 | 0 ⏭ — 30 operations** (15 measurement + 15 sub-domain)

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 5 | `Measurement` (set — ⚠ SDL type has no `id` field; `id` synthesized from `humanId`, **confirm key**), `SampleMeasurementSet` (key `sampleId`), `MeasurementTemplate` (key `humanId`), `SizeTemplate` (key `humanId`), `TightFit` (key `humanId version` — composite) |
| Owned value types | 6 | `MeasurementRow`, `SampleMeasurementSetRow`, `PomSize`, `MeasurementSetCoreSize`, `MeasurementBaseType`, `MeasurementPaged` |
| Sub-domain owned value types | ~10 | `MeasurementTemplateRow`, `SizeGroup`, `CoreSizes`, `GradeInfo`, `SizeValues`, `RowTolerance`, `TightFitsResponse`, `MeasurementTemplatesPaged`, `Sizes` (search-result union shape, no own `@key`) |
| `@shareable` | 6 | `CodeDescription`, `SizeCodeDescription`, `UnitOfMeasure`, `Pom`, `Paging`, `Unit_Of_Measure` (SizeTemplate's own UoM shape) |
| External stub — platform | 2 | `VMM_BusinessPartner` (measurement), `IG_Department`/`IG_Division`/`VMM_Brand` (sub-domain field resolvers — TightFit + MeasurementTemplate) |
| External stub — sibling DGS | 8 | `WorkspaceV2`, `UserProfileAttributes`, `SampleV2`, `AccessControl`, `ResourcePermissions`, `UserGroup_Participants`, `ProductComponentStatus`, `Product` (internal, listed here only as the placeholder-stub convention) |
| Inputs | ~24 | `MeasurementSetInput`, `MeasurementSetUpdateInput`, `SampleMeasurementSetInput`, `MeasurementTemplateInput`, `SizeTemplateInput`, `SizeTemplateUpdateInput`, `TightFitInput`, … |

No interfaces — no `@DgsTypeResolver`. (`updatedFromResource` is currently mono-typed to `SampleV2`.)

> **Sub-domain correction (2026-07-19):** `MeasurementTemplate`, `SizeTemplate`, `TightFit` were previously
> listed under "External stub — sibling DGS" (11 total). They are **owned entities of this domain**
> (co-located, own REST base, own CRUD operations) — moved to "Owned entities" above. This corrects the
> classification in the original pass, which treated them as opaque pass-through stubs because only their
> USE as a `Measurement` field was analyzed, not their own operations.

## 2. Client Contract Verification
- 7 queries + 8 mutations (measurement) + 8 queries + 7 mutations (sub-domains) preserved with **exact
  operation names** (`0 ✅ | 30 🔜 | 0 ⏭`).
- `SPARK_` dropped; the source type `SPARK_Measurements` → `Measurement`.
- `TightFit` uses a composite key `id version` (kept as `humanId version` in the target — see be-03-schema.graphql key-synthesis note).
- `SizeTemplate`/`MeasurementTemplate` have no `id` field in their SDL either — `id` synthesized from
  `humanId` (same pattern as `Measurement`, `Claims`, `Packaging`, `Watchlist`, `Dieline` — program-wide
  convention, decided 2026-07-17).

## 3. Federation Boundaries

> **Monorepo:** `plm-product` is one subgraph. `product`, `measurement`, `measurementTemplate`, `sizeTemplate`,
> `tightFit` are **co-located** — references among them are **internal types**, not federation.
> See [federation-patterns-condensed.md §0](../../../fedMigrationScripts/reference/federation-patterns-condensed.md).

- **Owns** `Measurement`, `SampleMeasurementSet` + value types — **and, as of 2026-07-19, `MeasurementTemplate`,
  `SizeTemplate`, `TightFit`** as first-class owned entities with their own operations (see be-04-stories.md
  Phase B/D/G), not merely pass-through stubs.
- **Internal (same subgraph — NOT federation):** `Product` (Measurement ↔ Product reference only).
  `MeasurementTemplate`/`SizeTemplate`/`TightFit` are no longer "internal stubs referenced by Measurement" —
  they are owned types in their own right, defined once in this domain's schema, referenced by `Measurement`
  as plain internal GraphQL types (in-process `@DgsData`, **no** `@extends @external`).
- **External (true federation stubs):** `WorkspaceV2` (workspace), `UserProfileAttributes`/
  `UserGroup_Participants` (user-profile), `SampleV2` (sample DGS), `AccessControl`/`ResourcePermissions`
  (access-control, ACL-context-only), `relationship` (for `getMeasurements`), `search` — plus platform
  `VMM_BusinessPartner`/`VMM_Brand` (vmm/brand) and platform `IG_Department`/`IG_Division` (ig, used by
  `TightFit.departments`/`.divisions` and `MeasurementTemplate.departments`/`.divisions`) and platform
  `NEXUS_Attributes` (used only by `Sizes`' `searchSparkSizes`).
- **Contributes back:**
  - `Product.measurementSets` → **internal** field resolver (co-located, F-01).
  - `SampleV2.sampleMeasurement` → **true federation** (sample is a separate DGS subgraph, H-01).

## 4. Migration Approach  *(Confluence approach page)*

Measurement is **mid-low risk** — more operations than impression but no polymorphism and only one mildly
hard write. The 3 sub-domains (measurementTemplate, sizeTemplate, tightFit) add straightforward CRUD/search
work — no orchestrated writes, no polymorphism, same risk profile as the master-data reads.

1. **Phase A:** schema + `MeasurementService` port (18 methods) + `MeasurementTemplateService`/
   `SizeTemplateService`/`TightFitService` ports (14 methods combined). 3 measurement master-data queries +
   2 sizeTemplate master-data queries (size categories, material types) → `@Cacheable`.
2. **Phase B:** id-fetch + master-data reads, plus the sub-domains' own list/search reads
   (`getMeasurementTemplates(ByIds)`, `getSizeTemplates`/`getSizeCategories`/`getMaterialTypes`,
   `getTightFits`/`getTightFitByIdAndVersion`, `searchSparkSizes`).
3. **Phase C:** the two listing queries (`getMeasurements` needs a relationship lookup first; `getMeasurementsElastic` is elastic). Push the client-side `createdAt DESC` sort to the backend if possible.
4. **Phase D:** the 6 simple measurement mutations (add, access, lock, unlock, component-status, sample
   put/delete) + the 3 sub-domain CRUD mutation pairs (measurementTemplate add/update/delete, sizeTemplate
   add/update, tightFit add/update).
5. **Phase E:** `updateMeasurement` — the one 2-step write (workspace assoc → body). Lighter than BOM's
   3-step but still non-atomic; pick a failure strategy.
6. **Phase G:** field resolvers (one story per type, including the 3 new sub-domain types) + tests.
7. **Phase F:** Product + SampleV2 contributions — post-launch, BLOCKED-BY those domains.

**Recommended improvement:** `updateMeasurementAccess` takes `systemTeamIds` **or** `systemTeamDto` — port as
a single tagged `MeasurementAccessInput` (keep the wire format).

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `updateMeasurement` 2-step non-atomic write | Medium | Medium | E-01 failure strategy (workspace then body) | Tech Lead |
| `getMeasurements` depends on relationship subgraph 🔴 | Medium | Medium | Sequence relationship federation; or call its service | Platform |
| `updateMeasurementAccess` polymorphic input | Low | Low | Tagged `MeasurementAccessInput` | Backend Eng |
| `updateMeasurementComponentStatus` no JWT | Low | Low | Confirm backend enforces (context only) | PO |
| Client-side sorts (Q2/Q3) | Low | Low | Push to backend | Backend Eng |

## 6. ACL Handling
Most reads/writes curry a capability token because measurement sets are resource-scoped. **ACL is ignored in
the DGS implementation** (no ACL story) — noted for context only.

## 7. Open Questions
1. `updateMeasurement` rollback strategy?
2. `updateMeasurementComponentStatus` JWT-less — backend-enforced?
3. Push `getMeasurements`/`getMeasurementsElastic` sort to backend?
4. Adopt tagged `MeasurementAccessInput`?
5. Are the 2 unused version service methods needed cross-domain?

---
**Phase Completed:** Phase 3 · **Domain:** `measurement`.
