# Phase 3: Federation Schema Analysis — Measurement

> **Domain:** `measurement` · **Target DGS:** `MeasurementService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Schema:** [be-03-schema.graphql](./be-03-schema.graphql) · **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 15 🔜 | 0 ⏭ — 15 operations**

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 2 | `Measurement` (set — ⚠ SDL type has no `id` field; `id` synthesized from `humanId`, **confirm key**), `SampleMeasurementSet` (key `sampleId`) |
| Owned value types | 6 | `MeasurementRow`, `SampleMeasurementSetRow`, `PomSize`, `MeasurementSetCoreSize`, `MeasurementBaseType`, `MeasurementPaged` |
| `@shareable` | 5 | `CodeDescription`, `SizeCodeDescription`, `UnitOfMeasure`, `Pom`, `Paging` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — sibling DGS | 11 | `Product`, `WorkspaceV2`, `UserProfileAttributes`, `SampleV2`, `MeasurementTemplate`, `SizeTemplate`, `TightFit`, `AccessControl`, `ResourcePermissions`, `UserGroup_Participants`, `ProductComponentStatus` |
| Inputs | ~18 | `MeasurementSetInput`, `MeasurementSetUpdateInput`, `SampleMeasurementSetInput`, … |

No interfaces — no `@DgsTypeResolver`. (`updatedFromResource` is currently mono-typed to `SampleV2`.)

## 2. Client Contract Verification
- 7 queries + 8 mutations preserved with **exact operation names** (`0 ✅ | 15 🔜 | 0 ⏭`).
- `SPARK_` dropped; the source type `SPARK_Measurements` → `Measurement`.
- `TightFit` uses a composite key `id version`.

## 3. Federation Boundaries

> **Monorepo:** `plm-product` is one subgraph. `product`, `measurement`, `measurementTemplate`, `sizeTemplate`,
> `tightFit` are **co-located** — references among them are **internal types**, not federation.
> See [reference-federation-patterns.md §0](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

- **Owns** `Measurement`, `SampleMeasurementSet` + value types.
- **Internal (same subgraph — NOT federation):** `Product`, `MeasurementTemplate`, `SizeTemplate`, `TightFit`.
  These are in-process `@DgsData` calls; **no** `@extends @external`.
- **External (true federation stubs):** `WorkspaceV2` (workspace), `UserProfileAttributes`/
  `UserGroup_Participants` (user-profile), `SampleV2` (sample DGS), `AccessControl`/`ResourcePermissions`
  (access-control, ACL-context-only), `relationship` (for `getMeasurements`), `search` — plus platform
  `VMM_BusinessPartner`.
- **Contributes back:**
  - `Product.measurementSets` → **internal** field resolver (co-located, F-01).
  - `SampleV2.sampleMeasurement` → **true federation** (sample is a separate DGS subgraph, H-01).

## 4. Migration Approach  *(Confluence approach page)*

Measurement is **mid-low risk** — more operations than impression but no polymorphism and only one mildly
hard write.

1. **Phase A:** schema + `MeasurementService` port (18 methods). 3 master-data queries → `@Cacheable`.
2. **Phase B:** id-fetch + master-data reads.
3. **Phase C:** the two listing queries (`getMeasurements` needs a relationship lookup first; `getMeasurementsElastic` is elastic). Push the client-side `createdAt DESC` sort to the backend if possible.
4. **Phase D:** the 6 simple mutations (add, access, lock, unlock, component-status, sample put/delete).
5. **Phase E:** `updateMeasurement` — the one 2-step write (workspace assoc → body). Lighter than BOM's
   3-step but still non-atomic; pick a failure strategy.
6. **Phase G:** field resolvers (one story per type) + tests.
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
