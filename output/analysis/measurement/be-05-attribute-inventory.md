# Phase 5: Attribute (Field) Inventory — Measurement

> **Domain:** `measurement` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Source:** [be-03-schema.graphql](./be-03-schema.graphql) + [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> Field types/nullability are taken from the source SDL (`schemas/SPARK_Measurement.graphqls`).

Resolution kinds: `Direct` · `Computed` · `Field-resolver` · `EXT` (severity) · `Polymorphic`.

## Table 1 — Object-type attributes (non-trivial)

| Type | Attribute | GraphQL Type | Resolution | Resolver Loc | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|--------------|-----------|------------|-------|
| `Measurement` | `access` | `AccessControl` | EXT | `resolvers/SPARK_Measurement.js:95-101` | accessControl (context) | Low | G01 |
| `Measurement` | `currentUserPermissions` | `ResourcePermissions` | EXT | `:102-105` | accessControl (context) | Low | G01 |
| `Measurement` | `businessPartners` | `[VMM_BusinessPartner]` | EXT | `:106` | 🔵 vmm | Low | G01 |
| `Measurement` | `createdBy` | `UserProfileAttributes` | EXT | `:107-111` | 🔵 user-profile | Low | G01 |
| `Measurement` | `updatedBy` | `UserProfileAttributes` | EXT | `:129-131` | 🔵 user-profile | Low | G01 |
| `Measurement` | `product` | `Product` | Field-resolver (internal) | `:112-117` | — (same DGS) | Low | G01 |
| `Measurement` | `workspaces` | `[WorkspaceV2]` | EXT | `:118-124` | 🟡 workspaceV2 | Low | G01 |
| `Measurement` | `status` | `CodeDescription` | Computed | `:125-128` | — | Low | G01 |
| `Measurement` | `updatedFromResource` | `SampleV2` | EXT (switch type='sample') | `:132-141` | 🟡 sampleV2 | Medium | G01 |
| `Measurement` | `measurementTemplates` | `[MeasurementTemplate]` | EXT | `:142-149` | 🟡 measurementTemplate | Medium | G01 |
| `Measurement` | `sizeTemplate` | `SizeTemplate` | EXT | `:150-155` | 🟡 sizeTemplate | Low | G01 |
| `Measurement` | `tightFitTemplate` | `TightFit` | EXT | `:156-162` | 🟡 tightFit | Low | G01 |
| `Measurement` | `participantDetails` | `UserGroup_Participants` | EXT | `:163` | 🔵 user-profile | Low | G01 |
| `SampleMeasurementSet` | `createdBy` | `UserProfileAttributes` | EXT | `:166-170` | 🔵 user-profile | Low | G02 |
| `SampleMeasurementSet` | `measurementSizeId` | `String` | Computed | `:171-173` | — | Low | G02 |
| `MeasurementTemplate` | `createdBy` | `UserProfileAttributes` | EXT | `resolvers/SPARK_MeasurementTemplate.js:61-63` | 🔵 user-profile | Low | G05 |
| `MeasurementTemplate` | `updatedBy` | `UserProfileAttributes` | EXT | `:64-66` | 🔵 user-profile | Low | G05 |
| `MeasurementTemplate` | `departments` | `[IG_Department]` | EXT | `:67-73` | 🔵 ig | Low | G05 |
| `MeasurementTemplate` | `divisions` | `[IG_Division]` | EXT | `:74-80` | 🔵 ig | Low | G05 |
| `MeasurementTemplate` | `brands` | `[VMM_Brand]` | EXT | `:81-85` | 🔵 vmm | Low | G05 |
| `SizeTemplate` | `humanId` | `String` | Computed | `resolvers/product/SPARK_SizeTemplate.js:31` | — | Low | G06 |
| `SizeTemplate` | `createdBy` | `UserProfileAttributes` | EXT | `:32-34` | 🔵 user-profile | Low | G06 |
| `SizeTemplate` | `updatedBy` | `UserProfileAttributes` | EXT | `:35-37` | 🔵 user-profile | Low | G06 |
| `TightFit` | `departments` | `[IG_Department]` | EXT | `resolvers/product/SPARK_TightFit.js:36-38` | 🔵 ig | Low | G07 |
| `TightFit` | `divisions` | `[IG_Division]` | EXT | `:39-41` | 🔵 ig | Low | G07 |
| `TightFit` | `brands` | `[VMM_Brand]` | EXT | `:42-45` | 🔵 vmm | Low | G07 |
| `TightFit` | `createdBy` | `UserProfileAttributes` | EXT | `:46-47` | 🔵 user-profile | Low | G07 |
| `TightFit` | `updatedBy` | `UserProfileAttributes` | EXT | `:48-49` | 🔵 user-profile | Low | G07 |

**Direct pass-throughs (from the measurement record):** `id, humanId, resourceId, parentId, name, notes,
- type, baseType, manualLock, version, status, statuses, toleranceSet, defaultUnitOfMeasure, coreSizes, rows, workspaceContext, createdAt, updatedAt` — DTO-mapped, no resolver.
- Covered by A02 + B01 mapping.
- (`statusId`/`statusName`/`businessPartnerIds` exist on the data record and are read internally to build `status` and `businessPartners`, but are **not** exposed fields in the SDL `SPARK_Measurements` type.)

**Direct pass-throughs (sub-domains):** `MeasurementTemplate`: `humanId, name, status, version, rows` (rows
themselves have direct `pointOfMeasure`/`toleranceOver`/`toleranceUnder`/`unitOfMeasure`). `SizeTemplate`:
`coreSizes, name, rows, toleranceSet, sizeCategory, status, categoryId, version, unitOfMeasure`. `TightFit`:
`humanId, version, name, statusId, statusName, coreSizes, rows, createdAt, updatedAt`. `Sizes`: `id, name,
source` (all 3 built directly in the resolver, no field-level sub-resolvers). Covered by each sub-domain's
own B-phase story mapping.

## Table 2 — Input-object attributes (key inputs)

| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `MeasurementSetInput` | `name` | `String!` | Yes | |
| `MeasurementSetInput` | `resourceId` | `String` | No | parent product/template id |
| `MeasurementSetInput` | `rows` | `[MeasurementRowInput]` | No | the POM rows |
| `MeasurementSetUpdateInput` | `humanId` | `ID!` | Yes | primeKey |
| `MeasurementSetUpdateInput` | `updateWorkspaceAssociations` | `PartialWorkspaceAssociationsInput` | No | drives the workspace step of `updateMeasurement` (E01) |
| `MeasurementAccessInput` | `systemTeamIds` / `systemTeamDto` | `[String]` / dto | No | either/or — recommend tagged input |
| `SampleMeasurementSetInput` | `sampleId`, `measurementSetId` | `ID!` | Yes | composite identity |
| `SampleMeasurementSetRowInput` | `updateParentMeasurementSet` | `Boolean` | No | propagate edits up to the set |
| `MeasurementTemplateInput` | `templateId` | `String` | No | primeKey on update |
| `MeasurementTemplateInput` | `divisionIds`/`brandIds`/`departmentIds` | `[Int]` | No | drive the platform field resolvers |
| `SPARK_SizeTemplateInput` | `categoryId` | `Int` | No | |
| `SPARK_SizeTemplateUpdateInput` | `id` | `ID` | No | primeKey on update |
| `SPARK_TightFitInput` | `tightFitId` | `String` | No | primeKey on update |
| `SPARK_TightFitInput` | `divisionIds`/`brandIds`/`departmentIds` | `[Int]` | No | drive the platform field resolvers |

## Table 3 — Summary roll-up

| Resolution kind | # fields | Migration signal |
|-----------------|----------|------------------|
| Direct | ~20 (measurement) + ~25 (sub-domains) | Free — schema + DTO mapping |
| Computed | 2 (`status`, `measurementSizeId`) + 1 (`SizeTemplate.humanId`) | trivial |
| Field-resolver (internal) | 1 (`product`) | thin |
| EXT (cross-domain) | 13 (measurement, unchanged) + 13 (sub-domains: 5 MeasurementTemplate, 3 SizeTemplate, 5 TightFit) | federated references (2 🔴 relationship/search heaviest on measurement; sub-domains all 🔵 low-severity) |
| Polymorphic | 0 | — |

**Signal:** Measurement is mostly direct fields plus ~13 federated-reference field resolvers (workspace,
sample, user, partner — the former "template" EXT rows are now internal, see the 2026-07-19 correction in
be-02/be-03). Migration risk is the **2-step `updateMeasurement` write** and the **relationship dependency**
of `getMeasurements`; the field resolvers are individually simple. The 4 sub-domains
(measurementTemplate/sizeTemplate/tightFit/sizes) add 15 new operations that are all straightforward
CRUD/search/lookup — no orchestration, no polymorphism — plus their own small set of 🔵-severity EXT field
resolvers (ig/vmm/user-profile), consistent with measurement's own risk profile.

---
**Phase Completed:** Phase 5 — Attribute Inventory · **Domain:** `measurement`.
