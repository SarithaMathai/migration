# Measurement — Schema Analysis (Federation v2.3)

> **Domain:** `measurement` (+ `measurementTemplate`) · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

Analysis of [03-schema.graphql](output/measurement/03-schema.graphql) — the federated DGS shape derived from `SPARK_Measurement.graphql` + `SPARK_MeasurementTemplate.graphql`.

---

## 1. Naming Decisions

| Source | Target | Rationale |
|---|---|---|
| `SPARK_Measurements` (type) | `MeasurementSet` | Singular noun; old name was a misnomer (one entity, plural-named) |
| `SPARK_MeasurementTemplate` | `MeasurementTemplate` | Drop SPARK_ prefix |
| `SPARK_SampleMeasurementSet` | `SampleMeasurementSet` | Drop prefix |
| `humanId` field | `id` | Federation entity key; consistent with bom/product migration |
| `resourceId` field | `parentId` | Field already marked `@deprecated(reason: "Use parentId")` in source |
| `Spark_MeasurementRowInput` | `MeasurementRowInput` | **Fixes casing anomaly** in source schema (only input with `Spark_` prefix) |
| `SPARK_MeasurementsInput` | `MeasurementSetInput` | Align with type rename |
| `SPARK_MeasurementsUpdateInput` | `MeasurementSetUpdateInput` | Align + `id` required |
| `getMeasurementByIds` | `measurementSetsByIds` | Standard collection naming |
| `getMeasurements` | `measurementSets(parentId:)` | Make required arg explicit |
| `getMeasurementsElastic` | `measurementSetsElastic` | Reuse; rename only |
| `getSampleMeasurement` | `sampleMeasurement` | |
| `updateMeasurementAccess` (polymorphic body) | `updateMeasurementSetAccess(access: MeasurementAccessInput!)` | Tagged input replaces XOR pattern |

---

## 2. Entity Keys

| Entity | Key | Notes |
|---|---|---|
| `MeasurementSet` | `@key(fields: "id")` | Was `humanId`; used by all field resolvers |
| `MeasurementTemplate` | `@key(fields: "id")` | Was `humanId`; resolvable via `measurementTemplatesByIds` reference resolver |
| `SampleMeasurementSet` | `@key(fields: "sampleId")` | Sub-resource directly addressable by sampleId |

---

## 3. Federation Contributions

### F01 · `MeasurementSet.product → plm-product.Product`

Source resolver: `product` field reads `parentId` (was `resourceId`) and calls `product.getByID.load` only when prefix is `PID`.

**Port:** Remove inline product fetch from this DGS. Instead:
- `MeasurementSet.product` becomes a federated entity reference: `Product @key(fields: "id")`. Gateway joins via the existing `parentId` field on `MeasurementSet`.
- Add `Product.measurementSets(...)` contribution **owned by plm-measurement**.

```graphql
extend type Product @key(fields: "id") {
  id: ID! @external
  measurementSets(calculated: Boolean, businessPartnerIds: [String!], mustHaveRows: Boolean): MeasurementSetConnection
}
```
The current `getMeasurements(resourceId: ...)` query becomes this field. The relationship-tree pre-walk stays inside plm-measurement.

### F02 · `MeasurementSet.workspaces / .businessPartners / .createdBy / .updatedBy / .access / .currentUserPermissions / .participantDetails`

All become entity references to sibling subgraphs (Workspace, BusinessPartner, UserProfileAttributes, AccessControl, ResourcePermissions, UserGroupParticipants). Replace local lookups with `@key` resolution.

### F03 · `MeasurementSet.measurementTemplates / .sizeTemplate / .tightFitTemplate`

- `measurementTemplates: [MeasurementTemplate!]` — **same subgraph** (co-located in plm-measurement). Direct field resolver.
- `sizeTemplate: SizeTemplate` — federation reference (`@key id`).
- `tightFitTemplate: TightFit` — federation reference with composite `@key(fields: "id version")` (because resolver loads by id+version pair).

### F04 · `MeasurementSet.updatedFromResource: SampleV2`

Resolver only handles `type === 'sample'`. Two options:
- **(A) Keep as `SampleV2` entity reference** — current behavior; schema-truthful.
- **(B) Make it a union** (`MeasurementSourceResource = SampleV2 | ...`) once additional source types are known.

**Recommendation:** Option A now; flag for revisit.

### F05 · `SampleV2.sampleMeasurement → SampleMeasurementSet`

Inverse contribution: plm-sample-v2 already owns SampleV2; plm-measurement contributes `sampleMeasurement` field.

### F06 · Shared scalars

`UnitOfMeasure`, `Pom`, `CodeDescription`, `SizeCodeDescription`, `Pageable`, `Paging` marked `@shareable` — used by multiple subgraphs. Source-of-truth ownership decision recorded in [reference/domain-service-catalog.md](fedMigrationScripts/reference/domain-service-catalog.md).

---

## 4. Input Shape Cleanups

| Source Issue | Cleanup |
|---|---|
| `Spark_MeasurementRowInput` (lowercase prefix) | Renamed `MeasurementRowInput` |
| `SPARK_MeasurementsUpdateInput` lacks `humanId` as required | `MeasurementSetUpdateInput.id: ID!` required |
| `updateMeasurementAccess(measurementSetId, systemTeamIds, systemTeamDto)` polymorphic args | Single `MeasurementAccessInput { systemTeamIds, systemTeamDto }` tagged input |
| `@deprecated` misplaced between `humanId` and `resourceId` declarations | Removed in port (parentId is the new field; resourceId dropped from schema) |
| `updateMeasurementComponentStatus(productId, ids, status)` | `updateMeasurementComponentStatus(productId, measurementSetIds, status)` — name `ids` was ambiguous |

---

## 5. Query Renames + Arg Refinements

| Source | Target | Args |
|---|---|---|
| `getMeasurementByIds` | `measurementSetsByIds` | `ids: [ID!]!, calculated: Boolean` |
| `getMeasurements(resourceId)` | `measurementSets(parentId!)` | Renamed + made required |
| `getMeasurementsElastic(resourceId)` | `measurementSetsElastic(parentId!)` | Renamed |
| `getMeasurementSetStatus` | `measurementSetStatuses` | Plural |
| `getSampleMeasurement(sampleId)` | `sampleMeasurement(sampleId: ID!)` | Required, ID type |
| `getUnitsOfMeasure(ids)` | `unitsOfMeasure(ids)` | |
| `getThicknessUnitsOfMeasure` | `thicknessUnitsOfMeasure` | |
| `getMeasurementTemplates(page!, size!)` | `measurementTemplates(page!, size!)` | Add `measurementTemplate(id)` single-fetch |
| `getMeasurementTemplatesByIds(ids)` | `measurementTemplatesByIds(ids!)` | |

---

## 6. Mutation Renames

| Source | Target |
|---|---|
| `addMeasurement` | `addMeasurementSet` |
| `updateMeasurement` | `updateMeasurementSet` |
| `updateMeasurementAccess` | `updateMeasurementSetAccess` (tagged input) |
| `lockMeasurementSet` / `unlockMeasurementSet` | unchanged |
| `putSampleMeasurementSet` | unchanged |
| `deleteSampleMeasurementSet` | unchanged; return type changed `String → SampleMeasurementSet` (deleted entity echo) |
| `updateMeasurementComponentStatus` | unchanged; arg `ids` → `measurementSetIds` |
| `addMeasurementTemplate` / `updateMeasurementTemplate` / `deleteMeasurementTemplate` | unchanged |

---

## 7. Pre-Migration Validation

Before publishing the DGS schema:

1. Run an introspection diff against `spark-internal-graphql` to confirm no client field is dropped.
2. Verify Hive Gateway composition succeeds with the new `@shareable` scalars + extended `Product`, `SampleV2`.
3. Confirm all clients of `getMeasurements` (UI search-by-product) accept the new `MeasurementSetConnection` shape.
4. Confirm clients of `updateMeasurementAccess` migrate to `MeasurementAccessInput` tagged shape.
5. Confirm the JWT-sentinel (`SPARK_POM_CREATE_MODIFY_TARGET_LIBRARY`) semantic with access-control team — DGS port needs a clean equivalent.

---

## 8. Open Questions

| # | Question | Owner |
|---|---|---|
| 1 | Should `updatedFromResource` become a union (`SampleV2 | OtherSourceType`)? | PM + backend |
| 2 | What is the production-correct delete endpoint for measurement templates (current uses `purgeTestMeasurementTemplateData`)? | Backend |
| 3 | Is `brandIds === -1` a sentinel for "all brands"? | PM |
| 4 | Should template `delete` enforce ACL? | Security |
| 5 | Should `updateMeasurementComponentStatus` require JWT? (consistent gap across product/bom/measurement) | Security |

---

**Phase Completed:** Phase 3 — Schema Derivation + Analysis
