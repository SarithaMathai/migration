# Bom — PO Sprint Planning Summary

> **Domain:** `bom` · **Target DGS:** `plm-bom` (Kotlin/DGS, green-field)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18
> **Stories:** [04-stories.md](output/bom/04-stories.md)

---

## What Are We Building?

The Bill of Materials (Bom) domain is the structured record of all materials, suppliers, and impressions that make up a product. It sits one level below Product and is referenced from many other domains (packaging, fabric, trim, wash, material-hub). This migration moves Bom from the centralized **Node.js spark-internal-graphql gateway** to a dedicated **Kotlin / Netflix DGS** service called **`plm-bom`**.

Bom is a **mid-size domain** — meaningful complexity (rich material polymorphism, trim-size dispatcher, 3-step `updateBom` write) but ~5× smaller than the Product domain:
- 988-line GraphQL schema
- 735-line resolver file
- 184-line service (17 methods)
- 325-line `bomUtils` helper file

The most distinctive technical challenge is **material polymorphism**: 7 concrete material types (`BomMaterial`, `BomFabricMaterial`, `BomFabricSpecMaterial`, `BomCombinationMaterial`, `BomTrimMaterial`, `BomWashMaterial`, `BomPackagingMaterial`) resolved via a 17-case category dispatcher, plus 5 impression-detail subtypes via a separate dispatcher.

---

## Migration Scope

| Surface | Count | Status |
|---|---|---|
| Queries | 13 | 🔜 all to build |
| Mutations | 6 | 🔜 all to build |
| Field resolvers | ~52 across 18 type blocks | 🔜 all to build |
| Material polymorphism | 7 concrete types + 1 interface + type-resolver | 🔜 |
| Impression polymorphism | 5 concrete types + 1 interface + type-resolver | 🔜 |
| External dependencies | 23 (1 platform VMM, 22 co-located sibling DGSs) | 🔵 / 🔜 |
| Federation contributions to other entities | 2 (Product extension + ResourcesCount stub) | 🔜 BLOCKED-BY product |

This is a **green-field** migration — no existing DGS code to inherit.

---

## Story Summary by Phase

| Phase | Description | Stories | Raw days | +20% buffer |
|---|---|---|---|---|
| A | Foundation & Schema | 6 | 11–18 | 13–22 |
| B | Core Queries | 5 | 5–10 | 6–12 |
| C | Search & Listing | 3 | 8–13 | 10–16 |
| D | Core Mutations | 5 | 6–12 | 7–14 |
| E | Complex Mutation (updateBom 3-step) | 1 | 5–8 | 6–10 |
| F | Federation Contributions | 2 | 4–7 | 5–9 |
| G | Field Resolvers | 15 | 26–47 | 31–56 |
| H | Services + Utils + Cleanup | 4 | 11–17 | 13–20 |
| I | Test Coverage | 4 | 12–18 | 14–22 |
| **Total** | | **45** | **88–150** | **105–181** |

> **Calendar:** one engineer ≈ **21–37 sprints** (5d/sprint). B/C/D/G highly parallelizable after A.

---

## Key Risk Areas

| Risk | Severity | Story |
|---|---|---|
| `updateBom` 3-step non-atomic write — rollback strategy required | 🔴 Critical | E01 |
| `BomImpressionDetails_Unified.libraryResource` reads `args.ids` — contract leak | 🔴 Critical | G10 |
| `BomTrimMaterial` enrichment X-Large (15-case TRIM_TYPES × 2 dispatchers, 3-loader memoization) | 🟡 High | G08 |
| Cross-DGS dependencies on 5 sibling material domains (hub, trim, wash, fabric, combination) | 🟡 High | A03 |
| `getHubMaterial` missing `await` before promise-passing — latent bug | 🟡 High | H02 |
| `updateBomComponentStatus` (M6) missing JWT vs all other writes | 🟡 High | D05 |
| Nested-filter query-string flattening in `searchMaterialsBom` | 🟡 High | C02 |
| 3 unused service methods — confirm cross-domain callers | 🟡 High | A05 |
| F01/F02 BLOCKED-BY product domain migration sequencing | 🟡 High | F01, F02 |
| Polymorphic material type-resolver — schema-check enforcement | 🟡 High | I04 |
| `Bom` ↔ `Bom_Unified` ~80% duplication — refactor opportunity | 🟢 Low | G01 |
| Circular import `bomUtils ↔ SPARK_Bom` | 🟢 Low | H03 |

---

## Decisions Required from PO / Architecture

| # | Decision | Due Before | Impact |
|---|---|---|---|
| 1 | `updateBom` rollback strategy (saga, compensation log, or best-effort) | E kickoff | E01 design |
| 2 | `updateBomComponentStatus` (M6) — JWT-less intentional or oversight? Add JWT? | D kickoff | D05 |
| 3 | Should `Bom_Unified` survive as a separate type, or be replaced by selective field projection on `Bom`? | A kickoff | G01 scope |
| 4 | Are unused service methods (`getActiveBomsByProductIdAndBomType`, `getBomVersionsById`, `getBomVersion`) called by other domains? Confirm before delete. | A kickoff | A05 |
| 5 | Federation rollout order for 5 sibling material domains (material-hub, trim, wash, fabric, combination) — bom needs at least stubs published | A kickoff | A03 |
| 6 | Server-side sort for `getBomByParentId` — eliminate client-side `orderBy` round-trip? | B kickoff | B03 |
| 7 | Q10 nested-filter shape — keep query-string flattening or replace with structured DTO? Coordinate with backend team. | C kickoff | C02 |
| 8 | Latent bug fix policy — apply during port (recommended) or back-port to source first? Applies to `getHubMaterial` await + `getFabricMaterial` null-guard + `getSuppliers` mutation. | A kickoff | H02 |
| 9 | F01 product entity extension: when does product domain Phase 3 publish `Product @key`? Schedules F01. | F kickoff | F01 |
| 10 | F02 `ResourcesCount.bomsCount` count source: re-use existing elastic count or switch to backend aggregate? | F kickoff | F02 |

---

## Dependency Map

```
plm-bom depends on:
  spark-product backend  (REST: /enterprise_product_development_products/bom/v1 + /masterData)
  spark-product backend  (elastic: bom search, materials search, materials-by-proxy)
  spark-access-control   (ACL JWT + permissions on 9/13 queries, 3/6 mutations, ~12 field resolvers)
  spark-workspace        (workspace association mgmt, getWorkspacesByIdsV2)
  spark-user-profile     (createdBy / updatedBy)
  spark-team             (loadBusinessPartners, userGroup participants)
  spark-tag              (countryOfOrigin tag lookups)
  Hive Gateway → VMM     (BusinessPartner stubs, supplier role lookups, facility location)
  Hive Gateway → material-hub  (HubMaterial, coded options, units of measure)
  Hive Gateway → trim          (trim batch, trim UoMs)
  Hive Gateway → wash          (JWT-curried wash loader)
  Hive Gateway → fabric        (fabricSpec by ID, getByID)
  Hive Gateway → combination   (getById)
  Hive Gateway → plm-product   (Bom.product field, F01 Product extension)
```

---

## Recommended Sprint Sequencing

| Sprint | Phases | Focus |
|---|---|---|
| S1 | A01–A06 | Schema skeleton, owned types, external stubs, type resolvers, BomService Kotlin port, ACL JWT |
| S2 | B01–B05 + D01–D04 | Master-data + simple queries + 4 thin mutations (parallel; 2 engineers ideal) |
| S3 | C01–C03 + D05 | Search + last mutation |
| S4 | E01 | `updateBom` 3-step atomicity — concentrated focus |
| S5 | G01–G03 | Bom + Bom_Unified + BomMaterial + BomPackagingMaterial fields |
| S6 | G04–G07 + G14 | Packaging/Fabric/FabricSpec/Combination materials + trivial fields |
| S7 | G08 | `BomTrimMaterial` (Large) — concentrated focus |
| S8 | G09–G15 | Wash + impression types + search result enrichment |
| S9 | H01–H04 | bomUtils Kotlin port + cleanup + circular-import fix |
| S10 | I01–I04 | Test coverage + cut-over rehearsal |
| Ongoing | F01, F02 | Federation contributions — unblocked when product domain completes Phase 3 / TechPack stub |

---

## Capacity Planning

| Team size | Calendar (5d sprints) | Notes |
|---|---|---|
| 1 engineer | ~21–37 sprints | Sequential |
| 2 engineers | ~12–20 sprints | B/C/D + bulk of G parallelizable |
| 3 engineers | ~8–14 sprints | Critical path = A → E01 → G08 → I03 |

> Phase G (Field Resolvers, 31–56 buffered days) dominates calendar. G08 (BomTrimMaterial) is the single biggest story.

---

## Cross-Domain Coordination

Bom contributes to two cross-domain entities:

1. **`Product` entity extension** (F01) — owns `productBoms`, `boms`, `packagingBoms` after migration. Currently lives in `plm-product`. **BLOCKED-BY** product domain Phase 3.
2. **`ResourcesCount` composite-key entity** (F02) — owns `bomsCount` field on the TechPack aggregator. **BLOCKED-BY** product domain F-phase TechPack facade (E05/F09 in product's [04-stories.md](output/product/04-stories.md)).

Bom can be **production-ready independently** of these federation contributions; F01/F02 are post-launch cleanup.

---

## Phase 2 Estimate Reconciliation

Phase 2 (Resolvers + Services + Utils) totaled **69–118 raw / 83–142 buffered** (see [02-resolver-analysis-services.md §D6](output/bom/02-resolver-analysis-services.md)). The story-level total here (**88–150 raw / 105–181 buffered**) is **higher** because Phase 4 adds Foundation (Phase A), Federation contributions (Phase F), and Test Coverage (Phase I) — none of which are in scope for Phase 2 effort estimation. The resolver + service effort is consistent between the two views.

---

*Generated by spark-migration pipeline v1.1 — Phase 4 complete. All 8 artifacts ready under `output/bom/`.*
