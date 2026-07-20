# Project Plan — Combined Backend + Frontend Story Order

> 🏷️ **Tags:** `dgs-migration` · `project-plan` — **Generated:** 2026-07-19 · One combined implementation sequence per domain: backend build steps from the story dependency graph, frontend cutovers slotted into the earliest step after their backend dependencies (reads flip before writes before sagas).
> Staffing + calendar for the 1 BE + 1 FE team: see 01-implementation-plan-1BE-1FE.md (team size set in team_config.py). Day figures are AI-estimated nominal midpoints — confirm in refinement.

---

## Domain order

| # | Domain | Why here | BE stories | FE stories |
|---|---|---|---|---|
| 1 | **Watchlist** | Wave 1 pilot — smallest isolated surface; proves flag flip + rollback | 13 | 3 |
| 2 | **Product Details** | Wave 2 — small, isolated, no shared blockers | 12 | 3 |
| 3 | **Measurement** | Wave 2 — parallel with Product Details | 30 | 4 |
| 4 | **Packaging** | Wave 2 — parallel with the other wave-2 domains | 23 | 5 |
| 5 | **BOM** | Wave 3 — high complexity, search-gated list views | 37 | 7 |
| 6 | **Claims** | Wave 3 — first cross-subgraph cutover (`spark-claims`) | 20 | 4 |
| 7 | **Product** | Wave 4 — largest surface, incremental slices, orchestrated writes last | 69 | 12 |
| 8 | **Impression** | Wave 4 rider — flips with its partner domains (BOM / Product) | 7 | 2 |

> Wave-2/3 domains parallelize across the team — the numbering is the *flip* order. Phase-0 spikes (SPIKE-01…07) run before/alongside step 1 of the first domains; E-phase stories are gated on their outcomes.

---

## Watchlist

> Wave 1 pilot — smallest isolated surface; proves flag flip + rollback · **13 BE + 3 FE stories** · ≈ 31 BE + 8 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-1. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (11 in parallel: `B-02` … `G-03`) → `G-05`
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-1):** `WATCHLIST-FE-001` → `WATCHLIST-FE-002` → `WATCHLIST-FE-003`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟡 `C-01`, 🟡 `D-01`, 🟡 `D-02`, 🟠 `E-01`, 🟢 `F-01`, 🟢 `F-02`, 🟢 `G-01`, 🟡 `G-02`, 🟡 `G-03` | — | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module) |
| 3 | 🟢 `G-05` | 🟢 `WATCHLIST-FE-001` | — |
| 4 | — | 🟢 `WATCHLIST-FE-002` | — |
| 5 | — | 🟡 `WATCHLIST-FE-003` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getWatchlistByIds | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟢 `B-02` — getWatchlistReasons | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 3 | 2 | 🟢 `B-03` — getWatchlistInspectionActions | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 4 | 2 | 🟡 `C-01` — getWatchlistByFilter | Backend · BE-2 | `B-01` — getWatchlistByIds | `WATCHLIST-FE-001` | Yes |
| 5 | 2 | 🟡 `D-01` — createWatchlistEntries | Backend · BE-2 | `B-01` — getWatchlistByIds | `WATCHLIST-FE-002` | Yes |
| 6 | 2 | 🟡 `D-02` — cloneFilesForWatchlist | Backend · BE-2 | `B-01` — getWatchlistByIds | `WATCHLIST-FE-002` | Yes |
| 7 | 2 | 🟠 `E-01` — updateWatchlistEntries | Backend · BE-2 | `B-01` — getWatchlistByIds | `WATCHLIST-FE-003` | Yes |
| 8 | 2 | 🟢 `F-01` — Product.watchlists | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 9 | 2 | 🟢 `F-02` — ResourcesCount.watchlists | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 10 | 2 | 🟢 `G-01` — Computed flatteners | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 11 | 2 | 🟡 `G-02` — createdBy + updatedBy + workspaces + pa… | Backend · BE-2 | `B-01` — getWatchlistByIds | `G-05` | Yes |
| 12 | 2 | 🟡 `G-03` — attachments + product | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 13 | 3 | 🟢 `G-05` — WatchlistPartner.partner entity referen… | Backend · BE-2 | `G-02` — createdBy + updatedBy +… | None | Yes |
| 14 | 3 | 🟢 `WATCHLIST-FE-001` — Migrate watchlist reads | Frontend · FE-1 | `B-01` — getWatchlistByIds, `C-01` — getWatchlistByFilter | None | Yes |
| 15 | 4 | 🟢 `WATCHLIST-FE-002` — Migrate watchlist create and clone muta… | Frontend · FE-1 | `D-01` — createWatchlistEntries, `D-02` — cloneFilesForWatchlist | None | No |
| 16 | 5 | 🟡 `WATCHLIST-FE-003` — Migrate updateWatchlistEntries saga han… | Frontend · FE-1 | `E-01` — updateWatchlistEntries | None | No |

**Backend critical path:** `B-01` → `G-02` → `G-05`.
**Frontend cutover flow:** `WATCHLIST-FE-001` → `WATCHLIST-FE-002` → `WATCHLIST-FE-003`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Product Details

> Wave 2 — small, isolated, no shared blockers · **12 BE + 3 FE stories** · ≈ 31 BE + 10 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-1. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (11 in parallel: `C-01` … `G-03`)
- **↓ unlocks frontend after backend step 1**
- **Frontend (FE-1):** `PDTL-FE-001` → `PDTL-FE-002` → `PDTL-FE-003`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟡 `C-01`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟡 `D-04`, 🟢 `D-05`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟡 `G-02`, 🟡 `G-03` | 🟢 `PDTL-FE-001` | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module) |
| 3 | — | 🟡 `PDTL-FE-002` | — |
| 4 | — | 🟡 `PDTL-FE-003` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getProductDetailsById | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟡 `C-01` — getProductDetailsElastic | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 3 | 2 | 🟡 `D-01` — createProductDetailsSet | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-002` | Yes |
| 4 | 2 | 🟢 `D-02` — updateProductDetailAccess | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 5 | 2 | 🟢 `D-03` — productDetailLockUnlock | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-002` | Yes |
| 6 | 2 | 🟡 `D-04` — cloneFilesForProductDetails | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-002` | Yes |
| 7 | 2 | 🟢 `D-05` — updateProductDetailComponentStatus | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-002` | Yes |
| 8 | 2 | 🟠 `E-01` — updateProductDetailsSet | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-003` | Yes |
| 9 | 2 | 🟢 `F-01` — Product.productDetails | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 10 | 2 | 🟡 `G-01` — access + currentUserPermissions + parti… | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 11 | 2 | 🟡 `G-02` — product + createdBy + updatedBy + busin… | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 12 | 2 | 🟡 `G-03` — attachment + item attachment/constructi… | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 13 | 2 | 🟢 `PDTL-FE-001` — Migrate product-details reads | Frontend · FE-1 | `B-01` — getProductDetailsById | None | Yes |
| 14 | 3 | 🟡 `PDTL-FE-002` — Migrate product-details simple mutations | Frontend · FE-1 | `D-01` — createProductDetailsSet, `D-03` — productDetailLockUnlock, `D-04` — cloneFilesForProductDet…, `D-05` — updateProductDetailComp… | None | No |
| 15 | 4 | 🟡 `PDTL-FE-003` — Migrate updateProductDetailsSet saga ha… | Frontend · FE-1 | `E-01` — updateProductDetailsSet | None | No |

**Backend critical path:** `B-01` → `C-01`.
**Frontend cutover flow:** `PDTL-FE-001` → `PDTL-FE-002` → `PDTL-FE-003`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Measurement

> Wave 2 — parallel with Product Details · **30 BE + 4 FE stories** · ≈ 56 BE + 16 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (21 in parallel: `B-02` … `H-01`) → (8 in parallel: `D-08` … `G-07`)
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-2):** `MST-FE-001` ‖ `MST-FE-003` → `MST-FE-002` → `MST-FE-004`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `B-09`, 🟡 `C-01`, 🟢 `C-02`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟡 `D-06`, 🟢 `D-07`, 🟠 `E-01`, 🟡 `F-01`, 🟢 `G-02`, 🟢 `H-01` | — | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)<br>`H-01` → ⛔ BLOCKED-BY sample |
| 3 | 🟢 `D-08`, 🟢 `D-09`, 🟢 `D-10`, 🟡 `G-01`, 🟢 `G-04`, 🟢 `G-05`, 🟢 `G-06`, 🟢 `G-07` | 🟡 `MST-FE-001`, 🟢 `MST-FE-003` | — |
| 4 | — | 🟡 `MST-FE-002` | — |
| 5 | — | 🟡 `MST-FE-004` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getMeasurementByIds data fetcher | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟢 `B-02` — getUnitsOfMeasure | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `G-04`, `MST-FE-003` | Yes |
| 3 | 2 | 🟢 `B-03` — getThicknessUnitsOfMeasure | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-003` | Yes |
| 4 | 2 | 🟢 `B-04` — getMeasurementSetStatus | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-001` | Yes |
| 5 | 2 | 🟢 `B-05` — getSampleMeasurement data fetcher | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `G-04` | Yes |
| 6 | 2 | 🟢 `B-06` — getMeasurementTemplates + getMeasuremen… | Backend · BE-2 | None | `D-08`, `G-01`, `G-05` | Yes |
| 7 | 2 | 🟢 `B-07` — getSizeTemplates + getSizeCategories + … | Backend · BE-2 | None | `D-09`, `G-01`, `G-06` | Yes |
| 8 | 2 | 🟢 `B-08` — getTightFits + getTightFitByIdAndVersio… | Backend · BE-2 | None | `D-10`, `G-01`, `G-07` | Yes |
| 9 | 2 | 🟢 `B-09` — searchSparkSizes data fetcher | Backend · BE-2 | None | None | Yes |
| 10 | 2 | 🟡 `C-01` — getMeasurements data fetcher | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-002` | Yes |
| 11 | 2 | 🟢 `C-02` — getMeasurementsElastic data fetcher | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-002` | Yes |
| 12 | 2 | 🟡 `D-01` — addMeasurement mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 13 | 2 | 🟢 `D-02` — updateMeasurementAccess mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 14 | 2 | 🟢 `D-03` — lockMeasurementSet mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-004` | Yes |
| 15 | 2 | 🟢 `D-04` — unlockMeasurementSet mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-004` | Yes |
| 16 | 2 | 🟢 `D-05` — updateMeasurementComponentStatus mutati… | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 17 | 2 | 🟡 `D-06` — putSampleMeasurementSet mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-004` | Yes |
| 18 | 2 | 🟢 `D-07` — deleteSampleMeasurementSet mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-004` | Yes |
| 19 | 2 | 🟠 `E-01` — updateMeasurement — 2-step orchestrated… | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 20 | 2 | 🟡 `F-01` — Implement Product.measurementSets | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 21 | 2 | 🟢 `G-02` — SampleMeasurementSet field resolvers | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 22 | 2 | 🟢 `H-01` — Contribute sampleMeasurement to the Sam… | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 23 | 3 | 🟢 `D-08` — addMeasurementTemplate + updateMeasurem… | Backend · BE-2 | `B-06` — getMeasurementTemplates… | None | Yes |
| 24 | 3 | 🟢 `D-09` — addSizeTemplate + updateSizeTemplate mu… | Backend · BE-2 | `B-07` — getSizeTemplates + getS… | None | Yes |
| 25 | 3 | 🟢 `D-10` — addTightFit + updateTightFit mutations | Backend · BE-2 | `B-08` — getTightFits + getTight… | None | Yes |
| 26 | 3 | 🟡 `G-01` — Measurement field resolvers | Backend · BE-2 | `B-01` — getMeasurementByIds dat…, `B-06` — getMeasurementTemplates…, `B-07` — getSizeTemplates + getS…, `B-08` — getTightFits + getTight… | None | Yes |
| 27 | 3 | 🟢 `G-04` — SampleMeasurementSet.sample forward ref… | Backend · BE-2 | `B-02` — getUnitsOfMeasure, `B-05` — getSampleMeasurement da… | None | Yes |
| 28 | 3 | 🟢 `G-05` — MeasurementTemplate field resolvers | Backend · BE-2 | `B-06` — getMeasurementTemplates… | None | Yes |
| 29 | 3 | 🟢 `G-06` — SizeTemplate field resolvers | Backend · BE-2 | `B-07` — getSizeTemplates + getS… | None | Yes |
| 30 | 3 | 🟢 `G-07` — TightFit field resolvers | Backend · BE-2 | `B-08` — getTightFits + getTight… | None | Yes |
| 31 | 3 | 🟡 `MST-FE-001` — Migrate measurement reads and retire hu… | Frontend · FE-2 | `B-01` — getMeasurementByIds dat…, `B-04` — getMeasurementSetStatus | None | Yes |
| 32 | 3 | 🟢 `MST-FE-003` — Migrate measurement master-data reads | Frontend · FE-2 | `B-02` — getUnitsOfMeasure, `B-03` — getThicknessUnitsOfMeas… | None | Yes |
| 33 | 4 | 🟡 `MST-FE-002` — Migrate measurement list/search reads | Frontend · FE-2 | `C-01` — getMeasurements data fe…, `C-02` — getMeasurementsElastic … | None | No |
| 34 | 5 | 🟡 `MST-FE-004` — Migrate measurement mutations | Frontend · FE-2 | `D-03` — lockMeasurementSet muta…, `D-04` — unlockMeasurementSet mu…, `D-06` — putSampleMeasurementSet…, `D-07` — deleteSampleMeasurement… | None | No |

**Backend critical path:** `B-01` → `B-06` → `D-08`.
**Frontend cutover flow:** `MST-FE-001` → `MST-FE-003` → `MST-FE-002` → `MST-FE-004`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Packaging

> Wave 2 — parallel with the other wave-2 domains · **23 BE + 5 FE stories** · ≈ 54 BE + 27 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (22 in parallel: `B-02` … `G-05`)
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-2):** `PKG-FE-001` ‖ `PKG-FE-002` → `PKG-FE-003` ‖ `PKG-FE-004` → `PKG-FE-005`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟡 `C-01`, 🟡 `D-01`, 🟢 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟢 `D-05`, 🟢 `D-06`, 🟢 `D-07`, 🟡 `D-08`, 🟢 `D-09`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟢 `G-02`, 🟡 `G-03`, 🟠 `G-04`, 🟡 `G-05` | — | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module) |
| 3 | — | 🟡 `PKG-FE-001`, 🟢 `PKG-FE-002` | — |
| 4 | — | 🟡 `PKG-FE-003`, 🟡 `PKG-FE-004` | — |
| 5 | — | 🔴 `PKG-FE-005` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getPackagings | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟢 `B-02` — getPackagingById | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-001` | Yes |
| 3 | 2 | 🟢 `B-03` — getDielines | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-003` | Yes |
| 4 | 2 | 🟢 `B-04` — getPackagingFieldValuesByType | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-002` | Yes |
| 5 | 2 | 🟢 `B-05` — getDielineEvaluationStatuses | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-003` | Yes |
| 6 | 2 | 🟢 `B-06` — getCountries | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-002` | Yes |
| 7 | 2 | 🟡 `C-01` — getPackagingElastic | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 8 | 2 | 🟡 `D-01` — addPackaging | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 9 | 2 | 🟢 `D-02` — evaluateDieline | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-003` | Yes |
| 10 | 2 | 🟡 `D-03` — bulkAddPackagings | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 11 | 2 | 🟡 `D-04` — bulkUpdatePackagings | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 12 | 2 | 🟢 `D-05` — exportPackaging | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 13 | 2 | 🟢 `D-06` — lockPackaging | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 14 | 2 | 🟢 `D-07` — unlockPackaging | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 15 | 2 | 🟡 `D-08` — cloneFilesForDielines | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 16 | 2 | 🟢 `D-09` — updatePackagingComponentStatus | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 17 | 2 | 🟠 `E-01` — updatePackaging | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-005` | Yes |
| 18 | 2 | 🟢 `F-01` — Product packaging links | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 19 | 2 | 🟡 `G-01` — access + businessPartner + participantD… | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 20 | 2 | 🟢 `G-02` — createdBy + updatedBy + dielineEvaluato… | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 21 | 2 | 🟡 `G-03` — product + workspaces + attachments | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 22 | 2 | 🟠 `G-04` — suggestedRetailPriceByDPCI + waveDescri… | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 23 | 2 | 🟡 `G-05` — Dieline + PrinterDieline + PackagingEle… | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 24 | 3 | 🟡 `PKG-FE-001` — Migrate packaging reads | Frontend · FE-2 | `B-01` — getPackagings, `B-02` — getPackagingById | None | Yes |
| 25 | 3 | 🟢 `PKG-FE-002` — Migrate packaging master-data reads and… | Frontend · FE-2 | `B-04` — getPackagingFieldValues…, `B-06` — getCountries | None | Yes |
| 26 | 4 | 🟡 `PKG-FE-003` — Migrate dieline flows | Frontend · FE-2 | `B-03` — getDielines, `B-05` — getDielineEvaluationSta…, `D-02` — evaluateDieline | None | Yes |
| 27 | 4 | 🟡 `PKG-FE-004` — Migrate packaging simple mutations and … | Frontend · FE-2 | `D-01` — addPackaging, `D-03` — bulkAddPackagings, `D-04` — bulkUpdatePackagings, `D-05` — exportPackaging, `D-06` — lockPackaging, `D-07` — unlockPackaging, `D-09` — updatePackagingComponen… | None | Yes |
| 28 | 5 | 🔴 `PKG-FE-005` — Migrate updatePackaging saga handling a… | Frontend · FE-2 | `E-01` — updatePackaging | None | No |

**Backend critical path:** `B-01` → `B-02`.
**Frontend cutover flow:** `PKG-FE-001` → `PKG-FE-002` → `PKG-FE-003` → `PKG-FE-004` → `PKG-FE-005`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## BOM

> Wave 3 — high complexity, search-gated list views · **37 BE + 7 FE stories** · ≈ 91 BE + 38 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-1. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (29 in parallel: `A-04` … `G-14`) → (7 in parallel: `A-05` … `G-17`)
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-1):** `BOM-FE-001` ‖ `BOM-FE-004` → `BOM-FE-002` ‖ `BOM-FE-005` → `BOM-FE-007` → `BOM-FE-003` ‖ `BOM-FE-006`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟡 `A-04`, 🟢 `B-03`, 🟢 `B-04`, 🟡 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟢 `C-04`, 🟢 `C-05`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟡 `G-03`, 🟢 `G-04`, 🟢 `G-05`, 🟢 `G-06`, 🟢 `G-07`, 🟠 `G-08`, 🟢 `G-09`, 🟠 `G-10`, 🟢 `G-14` | — | `A-04` → 🔬 SPIKE-05<br>`B-05` → 🔬 SPIKE-06a |
| 3 | 🟡 `A-05`, 🔴 `E-01`, 🟡 `G-11`, 🟡 `G-12`, 🟢 `G-13`, 🟡 `G-15`, 🟡 `G-17` | 🔴 `BOM-FE-001`, 🟢 `BOM-FE-004` | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module) |
| 4 | — | 🔴 `BOM-FE-002`, 🟡 `BOM-FE-005` | — |
| 5 | — | 🟢 `BOM-FE-007` | — |
| 6 | — | 🔴 `BOM-FE-003`, 🔴 `BOM-FE-006` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getBomByIds data fetcher | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟡 `A-04` — @DgsTypeResolver for the 2 BOM interfac… | Backend · BE-2 | None | `A-05` | Yes |
| 3 | 2 | 🟢 `B-03` — getBomStatus | Backend · BE-2 | None | `BOM-FE-002` | Yes |
| 4 | 2 | 🟢 `B-04` — getBomByParentId data fetcher | Backend · BE-2 | None | `BOM-FE-002` | Yes |
| 5 | 2 | 🟡 `B-05` — getBomMaterialTypes | Backend · BE-2 | None | `BOM-FE-004` | Yes |
| 6 | 2 | 🟢 `B-06` — getBomPackagingMaterialTypes | Backend · BE-2 | None | `BOM-FE-004` | Yes |
| 7 | 2 | 🟢 `B-07` — getBomPackagingSubstrates | Backend · BE-2 | None | `BOM-FE-004` | Yes |
| 8 | 2 | 🟢 `B-08` — getBomPackagingUnitOfMeasure | Backend · BE-2 | None | `BOM-FE-004` | Yes |
| 9 | 2 | 🟢 `C-01` — getBomElastic data fetcher | Backend · BE-2 | None | `BOM-FE-003` | Yes |
| 10 | 2 | 🟡 `C-02` — searchMaterialsBom data fetcher | Backend · BE-2 | None | `G-15` | Yes |
| 11 | 2 | 🟡 `C-03` — getComboSupplierForBom data fetcher | Backend · BE-2 | None | `BOM-FE-005` | Yes |
| 12 | 2 | 🟢 `C-04` — getValidTrimSuppliersForBom data fetcher | Backend · BE-2 | None | `BOM-FE-005` | Yes |
| 13 | 2 | 🟢 `C-05` — getValidRawMaterialSuppliersForBom data… | Backend · BE-2 | None | `BOM-FE-005` | Yes |
| 14 | 2 | 🟡 `D-01` — addBom mutation | Backend · BE-2 | None | `BOM-FE-006` | Yes |
| 15 | 2 | 🟢 `D-02` — manageBomWorkspaces mutation | Backend · BE-2 | None | `E-01` | Yes |
| 16 | 2 | 🟢 `D-03` — lockBom mutation | Backend · BE-2 | None | `BOM-FE-006` | Yes |
| 17 | 2 | 🟢 `D-04` — unlockBom mutation | Backend · BE-2 | None | `BOM-FE-006` | Yes |
| 18 | 2 | 🟢 `D-05` — updateBomComponentStatus mutation | Backend · BE-2 | None | `BOM-FE-006` | Yes |
| 19 | 2 | 🟡 `F-01` — Implement Product.productBoms / boms / … | Backend · BE-2 | None | None | Yes |
| 20 | 2 | 🟢 `F-02` — Fill ResourcesCount.bomsCount | Backend · BE-2 | None | None | Yes |
| 21 | 2 | 🟡 `G-01` — Bom field resolvers | Backend · BE-2 | None | `G-17` | Yes |
| 22 | 2 | 🟡 `G-03` — BomMaterial field resolvers | Backend · BE-2 | None | None | Yes |
| 23 | 2 | 🟢 `G-04` — BomPackagingMaterial field resolvers | Backend · BE-2 | None | None | Yes |
| 24 | 2 | 🟢 `G-05` — BomFabricMaterial field resolvers | Backend · BE-2 | None | None | Yes |
| 25 | 2 | 🟢 `G-06` — BomFabricSpecMaterial field resolvers | Backend · BE-2 | None | None | Yes |
| 26 | 2 | 🟢 `G-07` — BomCombinationMaterial field resolvers | Backend · BE-2 | None | None | Yes |
| 27 | 2 | 🟠 `G-08` — BomTrimMaterial field resolvers  — trim… | Backend · BE-2 | None | None | Yes |
| 28 | 2 | 🟢 `G-09` — BomWashMaterial field resolvers | Backend · BE-2 | None | None | Yes |
| 29 | 2 | 🟠 `G-10` — Impression library-resource resolution | Backend · BE-2 | None | `G-11`, `G-12`, `G-13` | Yes |
| 30 | 2 | 🟢 `G-14` — Trivial pass-through fields | Backend · BE-2 | None | None | Yes |
| 31 | 3 | 🟡 `A-05` — Shared CI conformance gate + code → typ… | Backend · BE-2 | `A-04` — @DgsTypeResolver for th… | None | Yes |
| 32 | 3 | 🔴 `E-01` — updateBom — 3-step orchestrated write | Backend · BE-2 | `D-02` — manageBomWorkspaces mut… | None | Yes |
| 33 | 3 | 🟡 `G-11` — BomFabricLibraryImpressionDetails.libra… | Backend · BE-2 | `G-10` — Impression library-reso… | None | Yes |
| 34 | 3 | 🟡 `G-12` — BomTrimLibraryImpressionDetails field r… | Backend · BE-2 | `G-10` — Impression library-reso… | None | Yes |
| 35 | 3 | 🟢 `G-13` — BomTrimZipperLibraryImpressionDetails f… | Backend · BE-2 | `G-10` — Impression library-reso… | None | Yes |
| 36 | 3 | 🟡 `G-15` — BomMaterialSearchResult field resolvers | Backend · BE-2 | `C-02` — searchMaterialsBom data… | None | Yes |
| 37 | 3 | 🟡 `G-17` — supplier entity references on material … | Backend · BE-2 | `G-01` — Bom field resolvers | `BOM-FE-007` | Yes |
| 38 | 3 | 🔴 `BOM-FE-001` — Statically expand BOM fragment factories | Frontend · FE-1 | None | `BOM-FE-002` | Yes |
| 39 | 3 | 🟢 `BOM-FE-004` — Migrate BOM master-data reads | Frontend · FE-1 | `B-05` — getBomMaterialTypes, `B-06` — getBomPackagingMaterial…, `B-07` — getBomPackagingSubstrat…, `B-08` — getBomPackagingUnitOfMe… | None | Yes |
| 40 | 4 | 🔴 `BOM-FE-002` — Migrate BOM core reads | Frontend · FE-1 | `B-01` — getBomByIds data fetcher, `B-03` — getBomStatus, `B-04` — getBomByParentId data f…, `BOM-FE-001` — Statically expand BOM f… | `BOM-FE-007` | Yes |
| 41 | 4 | 🟡 `BOM-FE-005` — Migrate BOM supplier reads | Frontend · FE-1 | `C-03` — getComboSupplierForBom …, `C-04` — getValidTrimSuppliersFo…, `C-05` — getValidRawMaterialSupp… | None | Yes |
| 42 | 5 | 🟢 `BOM-FE-007` — Adopt BOM supplier entity references | Frontend · FE-1 | `G-17` — supplier entity referen…, `BOM-FE-002` — Migrate BOM core reads | None | No |
| 43 | 6 | 🔴 `BOM-FE-003` — Migrate BOM search and elastic reads | Frontend · FE-1 | `C-01` — getBomElastic data fetc…, `BOM-BE-S-03` | None | Yes |
| 44 | 6 | 🔴 `BOM-FE-006` — Migrate BOM mutations including updateB… | Frontend · FE-1 | `D-01` — addBom mutation, `D-03` — lockBom mutation, `D-04` — unlockBom mutation, `D-05` — updateBomComponentStatu…, `BOM-BE-S-01` | None | Yes |

**Backend critical path:** `B-01` → `A-04` → `A-05`.
**Frontend cutover flow:** `BOM-FE-001` → `BOM-FE-004` → `BOM-FE-002` → `BOM-FE-005` → `BOM-FE-007` → `BOM-FE-003` → `BOM-FE-006`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Claims

> Wave 3 — first cross-subgraph cutover (`spark-claims`) · **20 BE + 4 FE stories** · ≈ 50 BE + 22 FE nominal days · **Owners:** Backend BE-1 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-1):** `B-01` → (18 in parallel: `B-02` … `H-02`) → `G-03`
- **↓ unlocks frontend after step 1 (no backend dependency)**
- **Frontend (FE-2):** `CLAIM-FE-001` → `CLAIM-FE-002` → `CLAIM-FE-003` → `CLAIM-FE-004`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | 🟡 `CLAIM-FE-001` | — |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟡 `C-01`, 🟡 `C-02`, 🟡 `D-01`, 🟡 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟠 `E-01`, 🟡 `G-01`, 🟡 `G-02`, 🟡 `G-04`, 🟢 `G-06`, 🟡 `H-01`, 🟢 `H-02` | — | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)<br>`H-01` → ⛔ BLOCKED-BY product (PRODUCT-BE-F-14, product-side stub alignment; also waits on the Product entity existing, plm-product Phase A)<br>`H-02` → ⛔ BLOCKED-BY product (PRODUCT-BE-E-03, TechPack facade; also PRODUCT-BE-F-14 contract alignment) |
| 3 | 🟠 `G-03` | 🔴 `CLAIM-FE-002` | — |
| 4 | — | 🟡 `CLAIM-FE-003` | — |
| 5 | — | 🔴 `CLAIM-FE-004` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getClaims | Backend · BE-1 | None | every story in this domain (module scaffold) | Yes |
| 2 | 1 | 🟡 `CLAIM-FE-001` — Split the claim fragment factory and re… | Frontend · FE-2 | None | `CLAIM-FE-002` | Yes |
| 3 | 2 | 🟢 `B-02` — getClaimByIds | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-002` | Yes |
| 4 | 2 | 🟢 `B-03` — getCommunicationChannels | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-002` | Yes |
| 5 | 2 | 🟢 `B-04` — getAllClaimsAbout | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-002` | Yes |
| 6 | 2 | 🟢 `B-05` — getClaimExports | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 7 | 2 | 🟡 `C-01` — searchGuestFacing | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 8 | 2 | 🟡 `C-02` — getClaimsElastic | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 9 | 2 | 🟡 `D-01` — createClaim | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 10 | 2 | 🟡 `D-02` — bulkUpdateClaim | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 11 | 2 | 🟢 `D-03` — requestClaimExport | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 12 | 2 | 🟢 `D-04` — lockClaim | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 13 | 2 | 🟢 `D-05` — unlockClaim | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 14 | 2 | 🟠 `E-01` — updateClaim | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-004` | Yes |
| 15 | 2 | 🟡 `G-01` — access + currentUserPermissions + parti… | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 16 | 2 | 🟡 `G-02` — createdBy + updatedBy + businessPartner… | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 17 | 2 | 🟡 `G-04` — workspaces + ClaimSubstantiate.substant… | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 18 | 2 | 🟢 `G-06` — Shared value-type alignment | Backend · BE-1 | `B-01` — getClaims | `G-03` | Yes |
| 19 | 2 | 🟡 `H-01` — Product.claims | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 20 | 2 | 🟢 `H-02` — ResourcesCount.claims | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 21 | 3 | 🟠 `G-03` — product + parentDetails | Backend · BE-1 | `B-01` — getClaims, `G-06` — Shared value-type align… | None | Yes |
| 22 | 3 | 🔴 `CLAIM-FE-002` — Migrate claim reads | Frontend · FE-2 | `B-01` — getClaims, `B-02` — getClaimByIds, `B-03` — getCommunicationChannels, `B-04` — getAllClaimsAbout, `CLAIM-FE-001` — Split the claim fragmen…, `PRODUCT-BE-H-06` | None | Yes |
| 23 | 4 | 🟡 `CLAIM-FE-003` — Migrate claim simple mutations and expo… | Frontend · FE-2 | `D-01` — createClaim, `D-02` — bulkUpdateClaim, `D-03` — requestClaimExport, `D-04` — lockClaim, `D-05` — unlockClaim | None | No |
| 24 | 5 | 🔴 `CLAIM-FE-004` — Migrate updateClaim multi-step write ha… | Frontend · FE-2 | `E-01` — updateClaim | None | No |

**Backend critical path:** `B-01` → `G-06` → `G-03`.
**Frontend cutover flow:** `CLAIM-FE-001` → `CLAIM-FE-002` → `CLAIM-FE-003` → `CLAIM-FE-004`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Product

> Wave 4 — largest surface, incremental slices, orchestrated writes last · **69 BE + 12 FE stories** · ≈ 200 BE + 84 FE nominal days · **Owners:** Backend BE-1 · Frontend FE-1 + FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-1):** `B-01` → (51 in parallel: `B-02` … `H-06`) → (14 in parallel: `E-01` … `H-05`) → `F-09` ‖ `F-11` ‖ `F-12`
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-1 + FE-2):** `PRODUCT-FE-001` ‖ `PRODUCT-FE-004` → `PRODUCT-FE-002` ‖ `PRODUCT-FE-005` → `PRODUCT-FE-006` ‖ `PRODUCT-FE-007` ‖ `PRODUCT-FE-008` → `PRODUCT-FE-010` ‖ `PRODUCT-FE-011` ‖ `PRODUCT-FE-012` → `PRODUCT-FE-003` ‖ `PRODUCT-FE-009`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `B-09`, 🟢 `B-10`, 🟢 `B-11`, 🟠 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟡 `C-04`, 🟡 `C-05`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟡 `D-05`, 🟢 `D-06`, 🟢 `D-07`, 🟢 `D-08`, 🟢 `D-09`, 🟢 `D-10`, 🟢 `D-11`, 🟢 `D-12`, 🟢 `D-13`, 🟢 `D-14`, 🟢 `D-15`, 🟢 `D-16`, 🟢 `D-17`, 🟢 `D-18`, 🟠 `E-00`, 🔴 `E-03`, 🟢 `F-14`, 🔴 `G-01`, 🔴 `G-02`, 🟡 `G-04`, 🟡 `G-05`, 🟡 `G-06`, 🟡 `G-07`, 🟡 `G-08`, 🟡 `G-09`, 🟡 `G-10`, 🟡 `G-11-1`, 🟡 `G-11-2`, 🟡 `G-13`, 🟢 `G-14`, 🟡 `G-15`, 🟡 `H-06` | — | `C-01` → 🔬 SPIKE-06a<br>`D-01` → 🔬 SPIKE-06b<br>`D-02` → 🔬 SPIKE-06b<br>`D-04` → 🔬 SPIKE-06b<br>`E-00` → 🔬 SPIKE-01<br>`E-03` → 🔬 SPIKE-02<br>`G-07` → 🔬 SPIKE-04<br>`G-11-1` → 🔬 SPIKE-04 |
| 3 | 🔴 `E-01`, 🟠 `E-02`, 🔴 `E-04`, 🟢 `F-04`, 🟢 `F-06`, 🟢 `F-08`, 🟢 `F-10`, 🟠 `G-03`, 🟡 `G-17`, 🟡 `H-01`, 🟡 `H-02`, 🟡 `H-03`, 🟡 `H-04`, 🟡 `H-05` | 🔴 `PRODUCT-FE-001`, 🟡 `PRODUCT-FE-004` | `E-01` → 🔬 SPIKE-03<br>`E-02` → 🔬 SPIKE-01<br>`E-04` → 🔬 SPIKE-02<br>`H-01` → ⛔ BLOCKED-BY attachment domain (⛔ cross-subgraph — does not ship until plm-attachment is live)<br>`H-02` → ⛔ BLOCKED-BY discussion domain (⛔ cross-subgraph)<br>`H-03` → ⛔ BLOCKED-BY sample domain (⛔ cross-subgraph)<br>`H-04` → ⛔ BLOCKED-BY claim domain (⛔ cross-subgraph)<br>`H-05` → ⛔ BLOCKED-BY construction domain (⛔ cross-subgraph) |
| 4 | 🟢 `F-09`, 🟢 `F-11`, 🟢 `F-12` | 🟡 `PRODUCT-FE-002`, 🟡 `PRODUCT-FE-005` | — |
| 5 | — | 🟡 `PRODUCT-FE-006`, 🟡 `PRODUCT-FE-007`, 🟡 `PRODUCT-FE-008` | — |
| 6 | — | 🟡 `PRODUCT-FE-010`, 🟡 `PRODUCT-FE-011`, 🟡 `PRODUCT-FE-012` | — |
| 7 | — | 🔴 `PRODUCT-FE-003`, 🔴 `PRODUCT-FE-009` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getProduct | Backend · BE-1 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟢 `B-02` — getProductsByIds | Backend · BE-1 | None | `PRODUCT-FE-003` | Yes |
| 3 | 2 | 🟢 `B-03` — getProductStatus | Backend · BE-1 | None | `PRODUCT-FE-004` | Yes |
| 4 | 2 | 🟢 `B-04` — getProductVersions | Backend · BE-1 | None | `PRODUCT-FE-002` | Yes |
| 5 | 2 | 🟢 `B-05` — getCopyStatus | Backend · BE-1 | None | None | Yes |
| 6 | 2 | 🟢 `B-06` — getProductTemplateById | Backend · BE-1 | None | None | Yes |
| 7 | 2 | 🟢 `B-07` — getProductRules | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 8 | 2 | 🟢 `B-08` — getProductRulesById | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 9 | 2 | 🟢 `B-09` — getAllAvailableRules | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 10 | 2 | 🟢 `B-10` — getProductDeptRules | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 11 | 2 | 🟢 `B-11` — getProductBPRules | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 12 | 2 | 🟠 `C-01` — getProducts two-stage hydration | Backend · BE-1 | None | None | Yes |
| 13 | 2 | 🟡 `C-02` — getProductTemplates | Backend · BE-1 | None | `PRODUCT-FE-005` | Yes |
| 14 | 2 | 🟡 `C-03` — getCategories | Backend · BE-1 | None | `PRODUCT-FE-005` | Yes |
| 15 | 2 | 🟡 `C-04` — getRatingByTcin | Backend · BE-1 | None | None | Yes |
| 16 | 2 | 🟡 `C-05` — searchProductRules | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 17 | 2 | 🟡 `D-01` — addProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 18 | 2 | 🟡 `D-02` — addProducts | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 19 | 2 | 🟡 `D-03` — bulkUpdateProducts | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 20 | 2 | 🟡 `D-04` — updateProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 21 | 2 | 🟡 `D-05` — carryForwardProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 22 | 2 | 🟢 `D-06` — addTeamsToProduct 🔀 Collab Canvas | Backend · BE-1 | None | `PRODUCT-FE-008` | Yes |
| 23 | 2 | 🟢 `D-07` — addBusinessPartnersToProductWithType 🔀 … | Backend · BE-1 | None | `PRODUCT-FE-008` | Yes |
| 24 | 2 | 🟢 `D-08` — removeProductResources | Backend · BE-1 | None | None | Yes |
| 25 | 2 | 🟢 `D-09` — updateBusinessPartnerStatuses | Backend · BE-1 | None | `PRODUCT-FE-009` | Yes |
| 26 | 2 | 🟢 `D-10` — updateViewToggle | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 27 | 2 | 🟢 `D-11` — updateWorkspaceAttributes 🔀 Collab Canv… | Backend · BE-1 | None | None | Yes |
| 28 | 2 | 🟢 `D-12` — updateProductTeamsWorkspaceContext | Backend · BE-1 | None | `PRODUCT-FE-008` | Yes |
| 29 | 2 | 🟢 `D-13` — linkProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 30 | 2 | 🟢 `D-14` — unlinkProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 31 | 2 | 🟢 `D-15` — addProductRule | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 32 | 2 | 🟢 `D-16` — updateProductRule | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 33 | 2 | 🟢 `D-17` — deleteProductRule | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 34 | 2 | 🟢 `D-18` — updateComponentStatus | Backend · BE-1 | None | `PRODUCT-FE-011` | Yes |
| 35 | 2 | 🟠 `E-00` — WriteSaga shared module | Backend · BE-1 | None | `E-01`, `E-02` | Yes |
| 36 | 2 | 🔴 `E-03` — getProductTechPackCountV1 stub + aggreg… | Backend · BE-1 | None | 10 stories: `E-04`, `F-04`, `F-06`, `F-08`, `H-01`, `H-02` … | Yes |
| 37 | 2 | 🟢 `F-14` — Cross-subgraph contract alignment | Backend · BE-1 | None | `F-10`, `PRODUCT-FE-012` | Yes |
| 38 | 2 | 🔴 `G-01` — Product.attachmentsWithMetaData | Backend · BE-1 | None | `G-03`, `G-17` | Yes |
| 39 | 2 | 🔴 `G-02` — Product.components | Backend · BE-1 | None | None | Yes |
| 40 | 2 | 🟡 `G-04` — ProductsCategories.categories  + Dopple… | Backend · BE-1 | None | None | Yes |
| 41 | 2 | 🟡 `G-05` — Product.samples + sampleIds + elasticSa… | Backend · BE-1 | None | None | Yes |
| 42 | 2 | 🟡 `G-06` — Product.teams + discussionsV2 + discuss… | Backend · BE-1 | None | None | Yes |
| 43 | 2 | 🟡 `G-07` — Product.vendorAttributes + businessPart… | Backend · BE-1 | None | None | Yes |
| 44 | 2 | 🟡 `G-08` — Product.measurementSets + claims + bom … | Backend · BE-1 | None | None | Yes |
| 45 | 2 | 🟡 `G-09` — Product.productWorkspaceAttributes + pr… | Backend · BE-1 | None | None | Yes |
| 46 | 2 | 🟡 `G-10` — Product.ancestryProducts + rating + res… | Backend · BE-1 | None | None | Yes |
| 47 | 2 | 🟡 `G-11-1` — Product.notRemovablePartnerIds + notRem… | Backend · BE-1 | None | None | Yes |
| 48 | 2 | 🟡 `G-11-2` — Product.associateProductsAsks + Product… | Backend · BE-1 | None | None | Yes |
| 49 | 2 | 🟡 `G-13` — IG/tag/tcin/spg + template trivial-fiel… | Backend · BE-1 | None | None | Yes |
| 50 | 2 | 🟢 `G-14` — Simple user/status fields + trivial pas… | Backend · BE-1 | None | None | Yes |
| 51 | 2 | 🟡 `G-15` — Port product utils to Kotlin | Backend · BE-1 | None | None | Yes |
| 52 | 2 | 🟡 `H-06` — Product entity fetcher  for cross-subgr… | Backend · BE-1 | `B-01` — getProduct | `F-10` | Yes |
| 53 | 3 | 🔴 `E-01` — productBusinessPartnerActions | Backend · BE-1 | `E-00` — WriteSaga shared module | `F-12` | Yes |
| 54 | 3 | 🟠 `E-02` — updateComponentStatuses | Backend · BE-1 | `E-00` — WriteSaga shared module | `PRODUCT-FE-011` | Yes |
| 55 | 3 | 🔴 `E-04` — getProductTechPackBulkCountV1 | Backend · BE-1 | `E-03` — getProductTechPackCount… | `PRODUCT-FE-010` | Yes |
| 56 | 3 | 🟢 `F-04` — ResourcesCount.measurementSets | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 57 | 3 | 🟢 `F-06` — ResourcesCount.productBoms + packagingB… | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 58 | 3 | 🟢 `F-08` — ResourcesCount.watchlists | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 59 | 3 | 🟢 `F-10` — Hive Gateway supergraph composition | Backend · BE-1 | `H-06` — Product entity fetcher …, `F-14` — Cross-subgraph contract… | `F-11` | Yes |
| 60 | 3 | 🟠 `G-03` — Product.attachments + attachmentsV3 + a… | Backend · BE-1 | `G-01` — Product.attachmentsWith… | None | Yes |
| 61 | 3 | 🟡 `G-17` — Entity references on partner/lineage va… | Backend · BE-1 | `G-01` — Product.attachmentsWith… | None | Yes |
| 62 | 3 | 🟡 `H-01` — ResourcesCount.productAttachments + dis… | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09`, `PRODUCT-FE-010` | Yes |
| 63 | 3 | 🟡 `H-02` — ResourcesCount.discussions | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09`, `PRODUCT-FE-010` | Yes |
| 64 | 3 | 🟡 `H-03` — ResourcesCount.sample | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09`, `PRODUCT-FE-010` | Yes |
| 65 | 3 | 🟡 `H-04` — ResourcesCount.claims | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09`, `PRODUCT-FE-010` | Yes |
| 66 | 3 | 🟡 `H-05` — ResourcesCount.constructions | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09`, `PRODUCT-FE-010` | Yes |
| 67 | 3 | 🔴 `PRODUCT-FE-001` — Migrate getProduct documents in product… | Frontend · FE-1 + FE-2 | `B-01` — getProduct | `PRODUCT-FE-002`, `PRODUCT-FE-008` | Yes |
| 68 | 3 | 🟡 `PRODUCT-FE-004` — Migrate product status and workspace-co… | Frontend · FE-1 + FE-2 | `B-03` — getProductStatus | None | Yes |
| 69 | 4 | 🟢 `F-09` — Retire the TechPack aggregation facade | Backend · BE-1 | `H-01` — ResourcesCount.productA…, `H-02` — ResourcesCount.discussi…, `H-03` — ResourcesCount.sample, `F-04` — ResourcesCount.measurem…, `H-04` — ResourcesCount.claims, `F-06` — ResourcesCount.productB…, `H-05` — ResourcesCount.construc…, `F-08` — ResourcesCount.watchlis… | None | Yes |
| 70 | 4 | 🟢 `F-11` — Platform stub verification | Backend · BE-1 | `F-10` — Hive Gateway supergraph… | None | Yes |
| 71 | 4 | 🟢 `F-12` — Deferred partner-wrapper decision | Backend · BE-1 | `E-01` — productBusinessPartnerA… | None | Yes |
| 72 | 4 | 🟡 `PRODUCT-FE-002` — Migrate shared-library getProduct consu… | Frontend · FE-1 + FE-2 | `B-01` — getProduct, `B-04` — getProductVersions, `PRODUCT-FE-001` — Migrate getProduct docu… | None | Yes |
| 73 | 4 | 🟡 `PRODUCT-FE-005` — Migrate template library and categories… | Frontend · FE-1 + FE-2 | `C-02` — getProductTemplates, `C-03` — getCategories | None | Yes |
| 74 | 5 | 🟡 `PRODUCT-FE-006` — Migrate product rules administration | Frontend · FE-1 + FE-2 | `B-07` — getProductRules, `B-08` — getProductRulesById, `B-09` — getAllAvailableRules, `B-10` — getProductDeptRules, `B-11` — getProductBPRules, `C-05` — searchProductRules, `D-15` — addProductRule, `D-16` — updateProductRule, `D-17` — deleteProductRule | None | Yes |
| 75 | 5 | 🟡 `PRODUCT-FE-007` — Migrate simple product mutations | Frontend · FE-1 + FE-2 | `D-01` — addProduct, `D-02` — addProducts, `D-03` — bulkUpdateProducts, `D-04` — updateProduct, `D-05` — carryForwardProduct, `D-10` — updateViewToggle, `D-13` — linkProduct, `D-14` — unlinkProduct | None | Yes |
| 76 | 5 | 🟡 `PRODUCT-FE-008` — Migrate team and partner assignment mut… | Frontend · FE-1 + FE-2 | `D-06` — addTeamsToProduct 🔀 Col…, `D-07` — addBusinessPartnersToPr…, `D-12` — updateProductTeamsWorks…, `PRODUCT-FE-001` — Migrate getProduct docu… | None | Yes |
| 77 | 6 | 🟡 `PRODUCT-FE-010` — Migrate TechPack count queries | Frontend · FE-1 + FE-2 | `E-03` — getProductTechPackCount…, `E-04` — getProductTechPackBulkC…, `H-01` — ResourcesCount.productA…, `H-02` — ResourcesCount.discussi…, `H-03` — ResourcesCount.sample, `H-04` — ResourcesCount.claims, `H-05` — ResourcesCount.construc… | None | Yes |
| 78 | 6 | 🟡 `PRODUCT-FE-011` — Migrate component status rollups | Frontend · FE-1 + FE-2 | `B-01` — getProduct, `D-18` — updateComponentStatus, `E-02` — updateComponentStatuses | None | Yes |
| 79 | 6 | 🟡 `PRODUCT-FE-012` — Verify fragment type-conditions, __type… | Frontend · FE-1 + FE-2 | `F-14` — Cross-subgraph contract… | None | Yes |
| 80 | 7 | 🔴 `PRODUCT-FE-003` — Migrate product list and bulk reads | Frontend · FE-1 + FE-2 | `PRODUCT-BE-S-02`, `B-02` — getProductsByIds | None | Yes |
| 81 | 7 | 🔴 `PRODUCT-FE-009` — Migrate partner drop/undrop orchestrati… | Frontend · FE-1 + FE-2 | `PRODUCT-BE-S-03`, `D-09` — updateBusinessPartnerSt… | None | Yes |

**Backend critical path:** `B-01` → `E-03` → `F-04` → `F-09`.
**Frontend cutover flow:** `PRODUCT-FE-001` → `PRODUCT-FE-004` → `PRODUCT-FE-002` → `PRODUCT-FE-005` → `PRODUCT-FE-006` → `PRODUCT-FE-007` → `PRODUCT-FE-008` → `PRODUCT-FE-010` → `PRODUCT-FE-011` → `PRODUCT-FE-012` → `PRODUCT-FE-003` → `PRODUCT-FE-009`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Impression

> Wave 4 rider — flips with its partner domains (BOM / Product) · **7 BE + 2 FE stories** · ≈ 14 BE + 4 FE nominal days · **Owners:** Backend BE-1 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-1):** `B-01` → (6 in parallel: `B-02` … `G-04`)
- **↓ unlocks frontend after backend step 1**
- **Frontend (FE-2):** `IMPRESSION-FE-001` ‖ `IMPRESSION-FE-002`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟢 `B-02`, 🟡 `D-01`, 🟢 `F-01`, 🟢 `G-01`, 🟡 `G-02`, 🟢 `G-04` | 🟢 `IMPRESSION-FE-001`, 🟢 `IMPRESSION-FE-002` | `F-01` → ⛔ BLOCKED-BY product (PRODUCT-BE-B-01, exposes the field this story reads)<br>`IMPRESSION-FE-001` → cross-domain: rides `BOM-FE-002`<br>`IMPRESSION-FE-002` → cross-domain: rides `PRODUCT-FE-001` |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — searchImpressionsByProductId data fetch… | Backend · BE-1 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟢 `B-02` — getImpressionCountsByProductId data fet… | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 3 | 2 | 🟡 `D-01` — updateImpressions mutation | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 4 | 2 | 🟢 `F-01` — Product.impressions / impressionCounts | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 5 | 2 | 🟢 `G-01` — Impression field resolvers | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 6 | 2 | 🟡 `G-02` — ImpressionCount.counts aggregation | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 7 | 2 | 🟢 `G-04` — attachment entity reference | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 8 | 2 | 🟢 `IMPRESSION-FE-001` — Migrate getBomDataAndImpressions | Frontend · FE-2 | `B-01` — searchImpressionsByProd…, `B-01` — searchImpressionsByProd…, `BOM-FE-002` | None | Yes |
| 9 | 2 | 🟢 `IMPRESSION-FE-002` — Migrate getCarryForwardFormData | Frontend · FE-2 | `B-01` — searchImpressionsByProd…, `B-01` — searchImpressionsByProd…, `PRODUCT-FE-001` | None | Yes |

**Backend critical path:** `B-01` → `B-02`.
**Frontend cutover flow:** `IMPRESSION-FE-001` → `IMPRESSION-FE-002`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

*Project plan · generated 2026-07-19 by generate_project_plan.py.*