# Project Plan — Combined Backend + Frontend Story Order

> 🏷️ **Tags:** `dgs-migration` · `project-plan` — **Generated:** 2026-07-17 · One combined implementation sequence per domain: backend build steps from the story dependency graph, frontend cutovers slotted into the earliest step after their backend dependencies (reads flip before writes before sagas).
> Staffing + calendar for the 2 BE + 2 FE team: see 01-implementation-plan-2BE-2FE.md. Day figures are AI-estimated nominal midpoints — confirm in refinement.

---

## Domain order

| # | Domain | Why here | BE stories | FE stories |
|---|---|---|---|---|
| 1 | **Watchlist** | Wave 1 pilot — smallest isolated surface; proves flag flip + rollback | 11 | 3 |
| 2 | **Product Details** | Wave 2 — small, isolated, no shared blockers | 11 | 3 |
| 3 | **Measurement** | Wave 2 — parallel with Product Details | 14 | 4 |
| 4 | **Packaging** | Wave 2 — parallel with the other wave-2 domains | 18 | 5 |
| 5 | **BOM** | Wave 3 — high complexity, search-gated list views | 24 | 6 |
| 6 | **Claims** | Wave 3 — first cross-subgraph cutover (`spark-claims`) | 15 | 4 |
| 7 | **Product** | Wave 4 — largest surface, incremental slices, orchestrated writes last | 48 | 11 |
| 8 | **Impression** | Wave 4 rider — flips with its partner domains (BOM / Product) | 7 | 2 |

> Wave-2/3 domains parallelize across the team — the numbering is the *flip* order. Phase-0 spikes (SPIKE-01…07) run before/alongside step 1 of the first domains; E-phase stories are gated on their outcomes.

---

## Watchlist

> Wave 1 pilot — smallest isolated surface; proves flag flip + rollback · **11 BE + 3 FE stories** · ≈ 30 BE + 8 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-1. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (9 in parallel: `B-02` … `G-03`) → `G-04`
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-1):** `WATCHLIST-FE-001` → `WATCHLIST-FE-002` → `WATCHLIST-FE-003`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟢 `B-02`, 🟡 `C-01`, 🟡 `D-01`, 🟡 `D-02`, 🟠 `E-01`, 🟢 `F-01`, 🟢 `G-01`, 🟡 `G-02`, 🟡 `G-03` | — | `E-01` → 🔬 SPIKE-01 |
| 3 | 🟡 `G-04` | 🟢 `WATCHLIST-FE-001` | — |
| 4 | — | 🟢 `WATCHLIST-FE-002` | — |
| 5 | — | 🟡 `WATCHLIST-FE-003` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getWatchlistByIds | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟢 `B-02` — getWatchlistReasons · getWatchlistInspe… | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 3 | 2 | 🟡 `C-01` — getWatchlistByFilter | Backend · BE-2 | `B-01` — getWatchlistByIds | `G-04`, `WATCHLIST-FE-001` | Yes |
| 4 | 2 | 🟡 `D-01` — createWatchlistEntries | Backend · BE-2 | `B-01` — getWatchlistByIds | `WATCHLIST-FE-002` | Yes |
| 5 | 2 | 🟡 `D-02` — cloneFilesForWatchlist | Backend · BE-2 | `B-01` — getWatchlistByIds | `WATCHLIST-FE-002` | Yes |
| 6 | 2 | 🟠 `E-01` — updateWatchlistEntries | Backend · BE-2 | `B-01` — getWatchlistByIds | `G-04`, `WATCHLIST-FE-003` | Yes |
| 7 | 2 | 🟢 `F-01` — Product.watchlists · ResourcesCount.wat… | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 8 | 2 | 🟢 `G-01` — Computed flatteners | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 9 | 2 | 🟡 `G-02` — createdBy + updatedBy + workspaces + pa… | Backend · BE-2 | `B-01` — getWatchlistByIds | `G-04` | Yes |
| 10 | 2 | 🟡 `G-03` — attachments + product | Backend · BE-2 | `B-01` — getWatchlistByIds | None | Yes |
| 11 | 3 | 🟡 `G-04` — Tests, parity harness | Backend · BE-2 | `B-01` — getWatchlistByIds, `C-01` — getWatchlistByFilter, `E-01` — updateWatchlistEntries, `G-02` — createdBy + updatedBy +… | None | Yes |
| 12 | 3 | 🟢 `WATCHLIST-FE-001` — Migrate watchlist reads | Frontend · FE-1 | `B-01` — getWatchlistByIds, `C-01` — getWatchlistByFilter | None | Yes |
| 13 | 4 | 🟢 `WATCHLIST-FE-002` — Migrate watchlist create and clone muta… | Frontend · FE-1 | `D-01` — createWatchlistEntries, `D-02` — cloneFilesForWatchlist | None | No |
| 14 | 5 | 🟡 `WATCHLIST-FE-003` — Migrate updateWatchlistEntries saga han… | Frontend · FE-1 | `E-01` — updateWatchlistEntries | None | No |

**Backend critical path:** `B-01` → `G-02` → `G-04`.
**Frontend cutover flow:** `WATCHLIST-FE-001` → `WATCHLIST-FE-002` → `WATCHLIST-FE-003`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Product Details

> Wave 2 — small, isolated, no shared blockers · **11 BE + 3 FE stories** · ≈ 32 BE + 10 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-1. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (9 in parallel: `C-01` … `G-03`) → `G-04`
- **↓ unlocks frontend after backend step 1**
- **Frontend (FE-1):** `PDTL-FE-001` → `PDTL-FE-002` → `PDTL-FE-003`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟡 `C-01`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-04`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟡 `G-02`, 🟡 `G-03` | 🟢 `PDTL-FE-001` | `E-01` → 🔬 SPIKE-01 |
| 3 | 🟡 `G-04` | 🟡 `PDTL-FE-002` | — |
| 4 | — | 🟡 `PDTL-FE-003` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getProductDetailsById | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟡 `C-01` — getProductDetailsElastic | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 3 | 2 | 🟡 `D-01` — createProductDetailsSet | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-002` | Yes |
| 4 | 2 | 🟡 `D-02` — updateProductDetailAccess · productDeta… | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-002` | Yes |
| 5 | 2 | 🟡 `D-04` — cloneFilesForProductDetails | Backend · BE-2 | `B-01` — getProductDetailsById | `PDTL-FE-002` | Yes |
| 6 | 2 | 🟠 `E-01` — updateProductDetailsSet | Backend · BE-2 | `B-01` — getProductDetailsById | `G-04`, `PDTL-FE-003` | Yes |
| 7 | 2 | 🟢 `F-01` — Product.productDetails | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 8 | 2 | 🟡 `G-01` — access + currentUserPermissions + parti… | Backend · BE-2 | `B-01` — getProductDetailsById | `G-04` | Yes |
| 9 | 2 | 🟡 `G-02` — product + createdBy + updatedBy + busin… | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 10 | 2 | 🟡 `G-03` — attachment + item attachment/constructi… | Backend · BE-2 | `B-01` — getProductDetailsById | None | Yes |
| 11 | 2 | 🟢 `PDTL-FE-001` — Migrate product-details reads | Frontend · FE-1 | `B-01` — getProductDetailsById | None | Yes |
| 12 | 3 | 🟡 `G-04` — Tests, parity harness | Backend · BE-2 | `B-01` — getProductDetailsById, `E-01` — updateProductDetailsSet, `G-01` — access + currentUserPer… | None | Yes |
| 13 | 3 | 🟡 `PDTL-FE-002` — Migrate product-details simple mutations | Frontend · FE-1 | `D-01` — createProductDetailsSet, `D-02` — updateProductDetailAcce…, `D-04` — cloneFilesForProductDet… | None | Yes |
| 14 | 4 | 🟡 `PDTL-FE-003` — Migrate updateProductDetailsSet saga ha… | Frontend · FE-1 | `E-01` — updateProductDetailsSet | None | No |

**Backend critical path:** `B-01` → `E-01` → `G-04`.
**Frontend cutover flow:** `PDTL-FE-001` → `PDTL-FE-002` → `PDTL-FE-003`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Measurement

> Wave 2 — parallel with Product Details · **14 BE + 4 FE stories** · ≈ 37 BE + 16 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (12 in parallel: `B-02` … `G-02`) → `G-03`
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-2):** `MST-FE-001` ‖ `MST-FE-003` → `MST-FE-002` → `MST-FE-004`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟡 `B-02`, 🟡 `C-01`, 🟢 `C-02`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-06`, 🟢 `D-07`, 🟠 `E-01`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟢 `G-02` | — | `E-01` → 🔬 SPIKE-01<br>`F-02` → ⛔ BLOCKED-BY sample |
| 3 | 🟡 `G-03` | 🟡 `MST-FE-001`, 🟢 `MST-FE-003` | — |
| 4 | — | 🟡 `MST-FE-002` | — |
| 5 | — | 🟡 `MST-FE-004` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getMeasurementByIds data fetcher | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟡 `B-02` — getUnitsOfMeasure · getThicknessUnitsOf… | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-001`, `MST-FE-003` | Yes |
| 3 | 2 | 🟡 `C-01` — getMeasurements data fetcher | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `G-03`, `MST-FE-002` | Yes |
| 4 | 2 | 🟢 `C-02` — getMeasurementsElastic data fetcher | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-002` | Yes |
| 5 | 2 | 🟡 `D-01` — addMeasurement mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 6 | 2 | 🟡 `D-02` — updateMeasurementAccess mutation · lock… | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-004` | Yes |
| 7 | 2 | 🟡 `D-06` — putSampleMeasurementSet mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-004` | Yes |
| 8 | 2 | 🟢 `D-07` — deleteSampleMeasurementSet mutation | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `MST-FE-004` | Yes |
| 9 | 2 | 🟠 `E-01` — updateMeasurement — 2-step orchestrated… | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `G-03` | Yes |
| 10 | 2 | 🟡 `F-01` — Implement Product.measurementSets | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 11 | 2 | 🟢 `F-02` — Contribute sampleMeasurement to the Sam… | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 12 | 2 | 🟡 `G-01` — Measurement field resolvers | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | `G-03` | Yes |
| 13 | 2 | 🟢 `G-02` — SampleMeasurementSet field resolvers | Backend · BE-2 | `B-01` — getMeasurementByIds dat… | None | Yes |
| 14 | 3 | 🟡 `G-03` — Test coverage & parity | Backend · BE-2 | `B-01` — getMeasurementByIds dat…, `C-01` — getMeasurements data fe…, `E-01` — updateMeasurement — 2-s…, `G-01` — Measurement field resol… | None | Yes |
| 15 | 3 | 🟡 `MST-FE-001` — Migrate measurement reads and retire hu… | Frontend · FE-2 | `B-01` — getMeasurementByIds dat…, `B-02` — getUnitsOfMeasure · get… | None | Yes |
| 16 | 3 | 🟢 `MST-FE-003` — Migrate measurement master-data reads | Frontend · FE-2 | `B-02` — getUnitsOfMeasure · get… | None | Yes |
| 17 | 4 | 🟡 `MST-FE-002` — Migrate measurement list/search reads | Frontend · FE-2 | `C-01` — getMeasurements data fe…, `C-02` — getMeasurementsElastic … | None | No |
| 18 | 5 | 🟡 `MST-FE-004` — Migrate measurement mutations | Frontend · FE-2 | `D-02` — updateMeasurementAccess…, `D-06` — putSampleMeasurementSet…, `D-07` — deleteSampleMeasurement… | None | No |

**Backend critical path:** `B-01` → `E-01` → `G-03`.
**Frontend cutover flow:** `MST-FE-001` → `MST-FE-003` → `MST-FE-002` → `MST-FE-004`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Packaging

> Wave 2 — parallel with the other wave-2 domains · **18 BE + 5 FE stories** · ≈ 52 BE + 27 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (16 in parallel: `B-02` … `G-05`) → `G-06`
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-2):** `PKG-FE-001` ‖ `PKG-FE-002` → `PKG-FE-003` ‖ `PKG-FE-004` → `PKG-FE-005`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟡 `B-02`, 🟢 `B-06`, 🟡 `C-01`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟡 `D-08`, 🟢 `D-09`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟢 `G-02`, 🟡 `G-03`, 🟠 `G-04`, 🟡 `G-05` | — | `E-01` → 🔬 SPIKE-01 |
| 3 | 🟡 `G-06` | 🟡 `PKG-FE-001`, 🟢 `PKG-FE-002` | — |
| 4 | — | 🟡 `PKG-FE-003`, 🟡 `PKG-FE-004` | — |
| 5 | — | 🔴 `PKG-FE-005` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getPackagings | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟡 `B-02` — getPackagingById · getDielines · getPac… | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-001`, `PKG-FE-002`, `PKG-FE-003` | Yes |
| 3 | 2 | 🟢 `B-06` — getCountries | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-002` | Yes |
| 4 | 2 | 🟡 `C-01` — getPackagingElastic | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 5 | 2 | 🟡 `D-01` — addPackaging | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 6 | 2 | 🟡 `D-02` — evaluateDieline · exportPackaging · loc… | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-003`, `PKG-FE-004` | Yes |
| 7 | 2 | 🟡 `D-03` — bulkAddPackagings | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 8 | 2 | 🟡 `D-04` — bulkUpdatePackagings | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 9 | 2 | 🟡 `D-08` — cloneFilesForDielines | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 10 | 2 | 🟢 `D-09` — updatePackagingComponentStatus | Backend · BE-2 | `B-01` — getPackagings | `PKG-FE-004` | Yes |
| 11 | 2 | 🟠 `E-01` — updatePackaging | Backend · BE-2 | `B-01` — getPackagings | `G-06`, `PKG-FE-005` | Yes |
| 12 | 2 | 🟢 `F-01` — Product packaging links | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 13 | 2 | 🟡 `G-01` — access + businessPartner + participantD… | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 14 | 2 | 🟢 `G-02` — createdBy + updatedBy + dielineEvaluato… | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 15 | 2 | 🟡 `G-03` — product + workspaces + attachments | Backend · BE-2 | `B-01` — getPackagings | `G-06` | Yes |
| 16 | 2 | 🟠 `G-04` — suggestedRetailPriceByDPCI + waveDescri… | Backend · BE-2 | `B-01` — getPackagings | `G-06` | Yes |
| 17 | 2 | 🟡 `G-05` — Dieline + PrinterDieline + PackagingEle… | Backend · BE-2 | `B-01` — getPackagings | None | Yes |
| 18 | 3 | 🟡 `G-06` — Tests, parity harness | Backend · BE-2 | `B-01` — getPackagings, `E-01` — updatePackaging, `G-03` — product + workspaces + …, `G-04` — suggestedRetailPriceByD… | None | Yes |
| 19 | 3 | 🟡 `PKG-FE-001` — Migrate packaging reads | Frontend · FE-2 | `B-01` — getPackagings, `B-02` — getPackagingById · getD… | None | Yes |
| 20 | 3 | 🟢 `PKG-FE-002` — Migrate packaging master-data reads and… | Frontend · FE-2 | `B-02` — getPackagingById · getD…, `B-06` — getCountries | None | Yes |
| 21 | 4 | 🟡 `PKG-FE-003` — Migrate dieline flows | Frontend · FE-2 | `B-02` — getPackagingById · getD…, `D-02` — evaluateDieline · expor… | None | Yes |
| 22 | 4 | 🟡 `PKG-FE-004` — Migrate packaging simple mutations and … | Frontend · FE-2 | `D-01` — addPackaging, `D-03` — bulkAddPackagings, `D-04` — bulkUpdatePackagings, `D-02` — evaluateDieline · expor…, `D-09` — updatePackagingComponen… | None | Yes |
| 23 | 5 | 🔴 `PKG-FE-005` — Migrate updatePackaging saga handling a… | Frontend · FE-2 | `E-01` — updatePackaging | None | No |

**Backend critical path:** `B-01` → `G-03` → `G-06`.
**Frontend cutover flow:** `PKG-FE-001` → `PKG-FE-002` → `PKG-FE-003` → `PKG-FE-004` → `PKG-FE-005`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## BOM

> Wave 3 — high complexity, search-gated list views · **24 BE + 6 FE stories** · ≈ 76 BE + 34 FE nominal days · **Owners:** Backend BE-2 · Frontend FE-1. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-2):** `B-01` → (17 in parallel: `A-04` … `G-10`) → (5 in parallel: `E-01` … `G-15`) → `G-16`
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-1):** `BOM-FE-001` ‖ `BOM-FE-004` → `BOM-FE-002` ‖ `BOM-FE-005` → `BOM-FE-003` ‖ `BOM-FE-006`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟡 `A-04`, 🟡 `B-03`, 🟡 `B-05`, 🟢 `B-08`, 🟡 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟡 `G-03`, 🟡 `G-04`, 🟠 `G-08`, 🟢 `G-09`, 🟠 `G-10` | — | `A-04` → 🔬 SPIKE-05<br>`B-05` → 🔬 SPIKE-06a |
| 3 | 🔴 `E-01`, 🟡 `G-11`, 🟡 `G-12`, 🟢 `G-13`, 🟡 `G-15` | 🔴 `BOM-FE-001`, 🟢 `BOM-FE-004` | `E-01` → 🔬 SPIKE-01 |
| 4 | 🟡 `G-16` | 🔴 `BOM-FE-002`, 🟡 `BOM-FE-005` | — |
| 5 | — | 🔴 `BOM-FE-003`, 🔴 `BOM-FE-006` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getBomByIds data fetcher | Backend · BE-2 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟡 `A-04` — @DgsTypeResolver for the 2 BOM interfac… | Backend · BE-2 | None | None | Yes |
| 3 | 2 | 🟡 `B-03` — getBomStatus · getBomByParentId data fe… | Backend · BE-2 | None | `BOM-FE-002`, `BOM-FE-004` | Yes |
| 4 | 2 | 🟡 `B-05` — getBomMaterialTypes | Backend · BE-2 | None | `BOM-FE-004` | Yes |
| 5 | 2 | 🟢 `B-08` — getBomPackagingUnitOfMeasure | Backend · BE-2 | None | `BOM-FE-004` | Yes |
| 6 | 2 | 🟡 `C-01` — getBomElastic data fetcher · getValidTr… | Backend · BE-2 | None | `BOM-FE-003`, `BOM-FE-005` | Yes |
| 7 | 2 | 🟡 `C-02` — searchMaterialsBom data fetcher | Backend · BE-2 | None | `G-15` | Yes |
| 8 | 2 | 🟡 `C-03` — getComboSupplierForBom data fetcher | Backend · BE-2 | None | `BOM-FE-005` | Yes |
| 9 | 2 | 🟡 `D-01` — addBom mutation | Backend · BE-2 | None | `BOM-FE-006` | Yes |
| 10 | 2 | 🟡 `D-02` — manageBomWorkspaces mutation · lockBom … | Backend · BE-2 | None | `E-01`, `BOM-FE-006` | Yes |
| 11 | 2 | 🟡 `F-01` — Implement Product.productBoms / boms / … | Backend · BE-2 | None | None | Yes |
| 12 | 2 | 🟢 `F-02` — Fill ResourcesCount.bomsCount | Backend · BE-2 | None | None | Yes |
| 13 | 2 | 🟡 `G-01` — Bom field resolvers | Backend · BE-2 | None | None | Yes |
| 14 | 2 | 🟡 `G-03` — BomMaterial field resolvers | Backend · BE-2 | None | None | Yes |
| 15 | 2 | 🟡 `G-04` — BomPackagingMaterial field resolvers · … | Backend · BE-2 | None | None | Yes |
| 16 | 2 | 🟠 `G-08` — BomTrimMaterial field resolvers  — trim… | Backend · BE-2 | None | `G-16` | Yes |
| 17 | 2 | 🟢 `G-09` — BomWashMaterial field resolvers · Trivi… | Backend · BE-2 | None | None | Yes |
| 18 | 2 | 🟠 `G-10` — Impression library-resource resolution | Backend · BE-2 | None | `G-11`, `G-12`, `G-13`, `G-16` | Yes |
| 19 | 3 | 🔴 `E-01` — updateBom — 3-step orchestrated write | Backend · BE-2 | `D-02` — manageBomWorkspaces mut… | `G-16` | Yes |
| 20 | 3 | 🟡 `G-11` — BomFabricLibraryImpressionDetails.libra… | Backend · BE-2 | `G-10` — Impression library-reso… | None | Yes |
| 21 | 3 | 🟡 `G-12` — BomTrimLibraryImpressionDetails field r… | Backend · BE-2 | `G-10` — Impression library-reso… | None | Yes |
| 22 | 3 | 🟢 `G-13` — BomTrimZipperLibraryImpressionDetails f… | Backend · BE-2 | `G-10` — Impression library-reso… | None | Yes |
| 23 | 3 | 🟡 `G-15` — BomMaterialSearchResult field resolvers | Backend · BE-2 | `C-02` — searchMaterialsBom data… | None | Yes |
| 24 | 3 | 🔴 `BOM-FE-001` — Statically expand BOM fragment factories | Frontend · FE-1 | None | `BOM-FE-002` | Yes |
| 25 | 3 | 🟢 `BOM-FE-004` — Migrate BOM master-data reads | Frontend · FE-1 | `B-05` — getBomMaterialTypes, `B-03` — getBomStatus · getBomBy…, `B-08` — getBomPackagingUnitOfMe… | None | Yes |
| 26 | 4 | 🟡 `G-16` — Test coverage & parity harness | Backend · BE-2 | `E-01` — updateBom — 3-step orch…, `G-08` — BomTrimMaterial field r…, `G-10` — Impression library-reso… | None | Yes |
| 27 | 4 | 🔴 `BOM-FE-002` — Migrate BOM core reads | Frontend · FE-1 | `B-01` — getBomByIds data fetcher, `B-03` — getBomStatus · getBomBy…, `BOM-FE-001` — Statically expand BOM f… | None | Yes |
| 28 | 4 | 🟡 `BOM-FE-005` — Migrate BOM supplier reads | Frontend · FE-1 | `C-03` — getComboSupplierForBom …, `C-01` — getBomElastic data fetc… | None | Yes |
| 29 | 5 | 🔴 `BOM-FE-003` — Migrate BOM search and elastic reads | Frontend · FE-1 | `C-01` — getBomElastic data fetc…, `BOM-BE-S-03` | None | Yes |
| 30 | 5 | 🔴 `BOM-FE-006` — Migrate BOM mutations including updateB… | Frontend · FE-1 | `D-01` — addBom mutation, `D-02` — manageBomWorkspaces mut…, `BOM-BE-S-01` | None | Yes |

**Backend critical path:** `B-01` → `D-02` → `E-01` → `G-16`.
**Frontend cutover flow:** `BOM-FE-001` → `BOM-FE-004` → `BOM-FE-002` → `BOM-FE-005` → `BOM-FE-003` → `BOM-FE-006`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Claims

> Wave 3 — first cross-subgraph cutover (`spark-claims`) · **15 BE + 4 FE stories** · ≈ 47 BE + 22 FE nominal days · **Owners:** Backend BE-1 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-1):** `B-01` → (13 in parallel: `B-02` … `G-04`) → `G-05`
- **↓ unlocks frontend after step 1 (no backend dependency)**
- **Frontend (FE-2):** `CLAIM-FE-001` → `CLAIM-FE-002` → `CLAIM-FE-003` → `CLAIM-FE-004`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | 🟡 `CLAIM-FE-001` | — |
| 2 | 🟡 `B-02`, 🟡 `C-01`, 🟡 `C-02`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-03`, 🟠 `E-01`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟡 `G-02`, 🟠 `G-03`, 🟡 `G-04` | — | `E-01` → 🔬 SPIKE-01<br>`F-01` → ⛔ BLOCKED-BY product<br>`F-02` → ⛔ BLOCKED-BY product |
| 3 | 🟡 `G-05` | 🔴 `CLAIM-FE-002` | — |
| 4 | — | 🟡 `CLAIM-FE-003` | — |
| 5 | — | 🔴 `CLAIM-FE-004` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getClaims | Backend · BE-1 | None | every story in this domain (module scaffold) | Yes |
| 2 | 1 | 🟡 `CLAIM-FE-001` — Split the claim fragment factory and re… | Frontend · FE-2 | None | `CLAIM-FE-002` | Yes |
| 3 | 2 | 🟡 `B-02` — getClaimByIds · getCommunicationChannel… | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-002` | Yes |
| 4 | 2 | 🟡 `C-01` — searchGuestFacing | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 5 | 2 | 🟡 `C-02` — getClaimsElastic | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 6 | 2 | 🟡 `D-01` — createClaim | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 7 | 2 | 🟡 `D-02` — bulkUpdateClaim | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 8 | 2 | 🟡 `D-03` — requestClaimExport · lockClaim · unlock… | Backend · BE-1 | `B-01` — getClaims | `CLAIM-FE-003` | Yes |
| 9 | 2 | 🟠 `E-01` — updateClaim | Backend · BE-1 | `B-01` — getClaims | `G-05`, `CLAIM-FE-004` | Yes |
| 10 | 2 | 🟡 `F-01` — Product.claims | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 11 | 2 | 🟢 `F-02` — ResourcesCount.claims | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 12 | 2 | 🟡 `G-01` — access + currentUserPermissions + parti… | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 13 | 2 | 🟡 `G-02` — createdBy + updatedBy + businessPartner… | Backend · BE-1 | `B-01` — getClaims | `G-05` | Yes |
| 14 | 2 | 🟠 `G-03` — product + parentDetails | Backend · BE-1 | `B-01` — getClaims | `G-05` | Yes |
| 15 | 2 | 🟡 `G-04` — workspaces + ClaimSubstantiate.substant… | Backend · BE-1 | `B-01` — getClaims | None | Yes |
| 16 | 3 | 🟡 `G-05` — Tests, parity harness | Backend · BE-1 | `B-01` — getClaims, `E-01` — updateClaim, `G-02` — createdBy + updatedBy +…, `G-03` — product + parentDetails | None | Yes |
| 17 | 3 | 🔴 `CLAIM-FE-002` — Migrate claim reads | Frontend · FE-2 | `B-01` — getClaims, `B-02` — getClaimByIds · getComm…, `CLAIM-FE-001` — Split the claim fragmen… | None | Yes |
| 18 | 4 | 🟡 `CLAIM-FE-003` — Migrate claim simple mutations and expo… | Frontend · FE-2 | `D-01` — createClaim, `D-02` — bulkUpdateClaim, `D-03` — requestClaimExport · lo… | None | No |
| 19 | 5 | 🔴 `CLAIM-FE-004` — Migrate updateClaim multi-step write ha… | Frontend · FE-2 | `E-01` — updateClaim | None | No |

**Backend critical path:** `B-01` → `G-03` → `G-05`.
**Frontend cutover flow:** `CLAIM-FE-001` → `CLAIM-FE-002` → `CLAIM-FE-003` → `CLAIM-FE-004`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Product

> Wave 4 — largest surface, incremental slices, orchestrated writes last · **48 BE + 11 FE stories** · ≈ 174 BE + 80 FE nominal days · **Owners:** Backend BE-1 · Frontend FE-1 + FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-1):** `B-01` → (35 in parallel: `B-02` … `G-15`) → (11 in parallel: `E-04` … `G-16`) → `F-09`
- **↓ unlocks frontend after backend step 2**
- **Frontend (FE-1 + FE-2):** `PRODUCT-FE-001` ‖ `PRODUCT-FE-004` → `PRODUCT-FE-002` ‖ `PRODUCT-FE-005` → `PRODUCT-FE-006` ‖ `PRODUCT-FE-007` ‖ `PRODUCT-FE-008` → `PRODUCT-FE-010` ‖ `PRODUCT-FE-011` → `PRODUCT-FE-003` ‖ `PRODUCT-FE-009`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟡 `B-02`, 🟡 `B-06`, 🟢 `B-10`, 🟠 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟡 `C-04`, 🟡 `C-05`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟡 `D-05`, 🟡 `D-06`, 🟡 `D-10`, 🟡 `D-14`, 🟢 `D-18`, 🔴 `E-01`, 🟠 `E-02`, 🔴 `E-03`, 🟢 `F-10`, 🔴 `G-01`, 🔴 `G-02`, 🟡 `G-04`, 🟡 `G-05`, 🟡 `G-06`, 🟡 `G-07`, 🟡 `G-08`, 🟡 `G-09`, 🟡 `G-10`, 🟡 `G-11-1`, 🟡 `G-11-2`, 🟢 `G-12`, 🟡 `G-13`, 🟡 `G-15` | — | `C-01` → 🔬 SPIKE-06a<br>`D-01` → 🔬 SPIKE-06b<br>`D-02` → 🔬 SPIKE-06b<br>`D-04` → 🔬 SPIKE-06b<br>`E-01` → 🔬 SPIKE-03<br>`E-02` → 🔬 SPIKE-01<br>`E-03` → 🔬 SPIKE-02<br>`G-07` → 🔬 SPIKE-04<br>`G-11-1` → 🔬 SPIKE-04 |
| 3 | 🔴 `E-04`, 🟡 `F-01`, 🟡 `F-02`, 🟡 `F-03`, 🟡 `F-04`, 🟡 `F-05`, 🟡 `F-07`, 🟢 `F-11`, 🟢 `F-12`, 🟠 `G-03`, 🟠 `G-16` | 🔴 `PRODUCT-FE-001`, 🟡 `PRODUCT-FE-004` | `E-04` → 🔬 SPIKE-02<br>`F-01` → ⛔ BLOCKED-BY attachment domain (⛔ cross-subgraph — does not ship until plm-attachment is live)<br>`F-02` → ⛔ BLOCKED-BY discussion domain (⛔ cross-subgraph)<br>`F-03` → ⛔ BLOCKED-BY sample domain (⛔ cross-subgraph)<br>`F-05` → ⛔ BLOCKED-BY claim domain (⛔ cross-subgraph)<br>`F-07` → ⛔ BLOCKED-BY construction domain (⛔ cross-subgraph) |
| 4 | 🟢 `F-09` | 🟡 `PRODUCT-FE-002`, 🟡 `PRODUCT-FE-005` | — |
| 5 | — | 🟡 `PRODUCT-FE-006`, 🟡 `PRODUCT-FE-007`, 🟡 `PRODUCT-FE-008` | — |
| 6 | — | 🟡 `PRODUCT-FE-010`, 🟡 `PRODUCT-FE-011` | — |
| 7 | — | 🔴 `PRODUCT-FE-003`, 🔴 `PRODUCT-FE-009` | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — getProduct | Backend · BE-1 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟡 `B-02` — getProductsByIds · getProductStatus · g… | Backend · BE-1 | None | `PRODUCT-FE-002`, `PRODUCT-FE-003`, `PRODUCT-FE-004` | Yes |
| 3 | 2 | 🟡 `B-06` — getProductTemplateById · getProductRule… | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 4 | 2 | 🟢 `B-10` — getProductDeptRules · getProductBPRules | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 5 | 2 | 🟠 `C-01` — getProducts two-stage hydration | Backend · BE-1 | None | `G-16` | Yes |
| 6 | 2 | 🟡 `C-02` — getProductTemplates | Backend · BE-1 | None | `PRODUCT-FE-005` | Yes |
| 7 | 2 | 🟡 `C-03` — getCategories | Backend · BE-1 | None | `PRODUCT-FE-005` | Yes |
| 8 | 2 | 🟡 `C-04` — getRatingByTcin | Backend · BE-1 | None | None | Yes |
| 9 | 2 | 🟡 `C-05` — searchProductRules | Backend · BE-1 | None | `PRODUCT-FE-006` | Yes |
| 10 | 2 | 🟡 `D-01` — addProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 11 | 2 | 🟡 `D-02` — addProducts | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 12 | 2 | 🟡 `D-03` — bulkUpdateProducts | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 13 | 2 | 🟡 `D-04` — updateProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 14 | 2 | 🟡 `D-05` — carryForwardProduct | Backend · BE-1 | None | `PRODUCT-FE-007` | Yes |
| 15 | 2 | 🟡 `D-06` — addTeamsToProduct 🔀 Collab Canvas · add… | Backend · BE-1 | None | `PRODUCT-FE-008`, `PRODUCT-FE-009` | Yes |
| 16 | 2 | 🟡 `D-10` — updateViewToggle · updateWorkspaceAttri… | Backend · BE-1 | None | `PRODUCT-FE-007`, `PRODUCT-FE-008` | Yes |
| 17 | 2 | 🟡 `D-14` — unlinkProduct · addProductRule · update… | Backend · BE-1 | None | `PRODUCT-FE-006`, `PRODUCT-FE-007` | Yes |
| 18 | 2 | 🟢 `D-18` — updateComponentStatus | Backend · BE-1 | None | `PRODUCT-FE-011` | Yes |
| 19 | 2 | 🔴 `E-01` — productBusinessPartnerActions | Backend · BE-1 | None | `F-12`, `G-16` | Yes |
| 20 | 2 | 🟠 `E-02` — updateComponentStatuses | Backend · BE-1 | None | `PRODUCT-FE-011` | Yes |
| 21 | 2 | 🔴 `E-03` — getProductTechPackCountV1 stub + aggreg… | Backend · BE-1 | None | 9 stories: `E-04`, `F-01`, `F-02`, `F-03`, `F-04`, `F-05` … | Yes |
| 22 | 2 | 🟢 `F-10` — Hive Gateway supergraph composition | Backend · BE-1 | None | `F-11` | Yes |
| 23 | 2 | 🔴 `G-01` — Product.attachmentsWithMetaData | Backend · BE-1 | None | `G-03`, `G-16` | Yes |
| 24 | 2 | 🔴 `G-02` — Product.components | Backend · BE-1 | None | `G-16` | Yes |
| 25 | 2 | 🟡 `G-04` — ProductsCategories.categories  + Dopple… | Backend · BE-1 | None | None | Yes |
| 26 | 2 | 🟡 `G-05` — Product.samples + sampleIds + elasticSa… | Backend · BE-1 | None | None | Yes |
| 27 | 2 | 🟡 `G-06` — Product.teams + discussionsV2 + discuss… | Backend · BE-1 | None | None | Yes |
| 28 | 2 | 🟡 `G-07` — Product.vendorAttributes + businessPart… | Backend · BE-1 | None | None | Yes |
| 29 | 2 | 🟡 `G-08` — Product.measurementSets + claims + bom … | Backend · BE-1 | None | None | Yes |
| 30 | 2 | 🟡 `G-09` — Product.productWorkspaceAttributes + pr… | Backend · BE-1 | None | None | Yes |
| 31 | 2 | 🟡 `G-10` — Product.ancestryProducts + rating + res… | Backend · BE-1 | None | None | Yes |
| 32 | 2 | 🟡 `G-11-1` — Product.notRemovablePartnerIds + notRem… | Backend · BE-1 | None | None | Yes |
| 33 | 2 | 🟡 `G-11-2` — Product.associateProductsAsks + Product… | Backend · BE-1 | None | None | Yes |
| 34 | 2 | 🟢 `G-12` — Product.division **bug fix** · Simple u… | Backend · BE-1 | None | None | Yes |
| 35 | 2 | 🟡 `G-13` — IG/tag/tcin/spg + template trivial-fiel… | Backend · BE-1 | None | None | Yes |
| 36 | 2 | 🟡 `G-15` — Port product utils to Kotlin | Backend · BE-1 | None | None | Yes |
| 37 | 3 | 🔴 `E-04` — getProductTechPackBulkCountV1 | Backend · BE-1 | `E-03` — getProductTechPackCount… | `PRODUCT-FE-010` | Yes |
| 38 | 3 | 🟡 `F-01` — ResourcesCount.productAttachments + dis… | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 39 | 3 | 🟡 `F-02` — ResourcesCount.discussions | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 40 | 3 | 🟡 `F-03` — ResourcesCount.sample | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 41 | 3 | 🟡 `F-04` — ResourcesCount.measurementSets · Resour… | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 42 | 3 | 🟡 `F-05` — ResourcesCount.claims | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 43 | 3 | 🟡 `F-07` — ResourcesCount.constructions | Backend · BE-1 | `E-03` — getProductTechPackCount… | `F-09` | Yes |
| 44 | 3 | 🟢 `F-11` — Platform stub verification | Backend · BE-1 | `F-10` — Hive Gateway supergraph… | None | Yes |
| 45 | 3 | 🟢 `F-12` — Deferred partner-wrapper decision | Backend · BE-1 | `E-01` — productBusinessPartnerA… | None | Yes |
| 46 | 3 | 🟠 `G-03` — Product.attachments + attachmentsV3 + a… | Backend · BE-1 | `G-01` — Product.attachmentsWith… | None | Yes |
| 47 | 3 | 🟠 `G-16` — Test coverage, parity harness, load & c… | Backend · BE-1 | `C-01` — getProducts two-stage h…, `E-01` — productBusinessPartnerA…, `E-03` — getProductTechPackCount…, `G-01` — Product.attachmentsWith…, `G-02` — Product.components | None | Yes |
| 48 | 3 | 🔴 `PRODUCT-FE-001` — Migrate getProduct documents in product… | Frontend · FE-1 + FE-2 | `B-01` — getProduct | `PRODUCT-FE-002`, `PRODUCT-FE-008` | Yes |
| 49 | 3 | 🟡 `PRODUCT-FE-004` — Migrate product status and workspace-co… | Frontend · FE-1 + FE-2 | `B-02` — getProductsByIds · getP… | None | Yes |
| 50 | 4 | 🟢 `F-09` — Retire the TechPack aggregation facade | Backend · BE-1 | `F-01` — ResourcesCount.productA…, `F-02` — ResourcesCount.discussi…, `F-03` — ResourcesCount.sample, `F-04` — ResourcesCount.measurem…, `F-05` — ResourcesCount.claims, `F-07` — ResourcesCount.construc… | None | Yes |
| 51 | 4 | 🟡 `PRODUCT-FE-002` — Migrate shared-library getProduct consu… | Frontend · FE-1 + FE-2 | `B-01` — getProduct, `B-02` — getProductsByIds · getP…, `PRODUCT-FE-001` — Migrate getProduct docu… | None | Yes |
| 52 | 4 | 🟡 `PRODUCT-FE-005` — Migrate template library and categories… | Frontend · FE-1 + FE-2 | `C-02` — getProductTemplates, `C-03` — getCategories | None | Yes |
| 53 | 5 | 🟡 `PRODUCT-FE-006` — Migrate product rules administration | Frontend · FE-1 + FE-2 | `B-06` — getProductTemplateById …, `B-10` — getProductDeptRules · g…, `C-05` — searchProductRules, `D-14` — unlinkProduct · addProd… | None | Yes |
| 54 | 5 | 🟡 `PRODUCT-FE-007` — Migrate simple product mutations | Frontend · FE-1 + FE-2 | `D-01` — addProduct, `D-02` — addProducts, `D-03` — bulkUpdateProducts, `D-04` — updateProduct, `D-05` — carryForwardProduct, `D-10` — updateViewToggle · upda…, `D-14` — unlinkProduct · addProd… | None | Yes |
| 55 | 5 | 🟡 `PRODUCT-FE-008` — Migrate team and partner assignment mut… | Frontend · FE-1 + FE-2 | `D-06` — addTeamsToProduct 🔀 Col…, `D-10` — updateViewToggle · upda…, `PRODUCT-FE-001` — Migrate getProduct docu… | None | Yes |
| 56 | 6 | 🟡 `PRODUCT-FE-010` — Migrate TechPack count queries | Frontend · FE-1 + FE-2 | `E-03` — getProductTechPackCount…, `E-04` — getProductTechPackBulkC… | None | Yes |
| 57 | 6 | 🟡 `PRODUCT-FE-011` — Migrate component status rollups | Frontend · FE-1 + FE-2 | `B-01` — getProduct, `D-18` — updateComponentStatus, `E-02` — updateComponentStatuses | None | Yes |
| 58 | 7 | 🔴 `PRODUCT-FE-003` — Migrate product list and bulk reads | Frontend · FE-1 + FE-2 | `PRODUCT-BE-S-02`, `B-02` — getProductsByIds · getP… | None | Yes |
| 59 | 7 | 🔴 `PRODUCT-FE-009` — Migrate partner drop/undrop orchestrati… | Frontend · FE-1 + FE-2 | `PRODUCT-BE-S-03`, `D-06` — addTeamsToProduct 🔀 Col… | None | Yes |

**Backend critical path:** `B-01` → `E-03` → `F-04` → `F-09`.
**Frontend cutover flow:** `PRODUCT-FE-001` → `PRODUCT-FE-004` → `PRODUCT-FE-002` → `PRODUCT-FE-005` → `PRODUCT-FE-006` → `PRODUCT-FE-007` → `PRODUCT-FE-008` → `PRODUCT-FE-010` → `PRODUCT-FE-011` → `PRODUCT-FE-003` → `PRODUCT-FE-009`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

## Impression

> Wave 4 rider — flips with its partner domains (BOM / Product) · **7 BE + 2 FE stories** · ≈ 14 BE + 4 FE nominal days · **Owners:** Backend BE-1 · Frontend FE-2. Stories in the same step are independent and parallelize; a FE story never starts before every BE story it depends on is delivered.

**Roadmap**

- **Backend (BE-1):** `B-01` → (5 in parallel: `B-02` … `G-02`) → `G-03`
- **↓ unlocks frontend after backend step 1**
- **Frontend (FE-2):** `IMPRESSION-FE-001` ‖ `IMPRESSION-FE-002`

| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | — |
| 2 | 🟢 `B-02`, 🟡 `D-01`, 🟢 `F-01`, 🟢 `G-01`, 🟡 `G-02` | 🟢 `IMPRESSION-FE-001`, 🟢 `IMPRESSION-FE-002` | `F-01` → ⛔ BLOCKED-BY product B-01<br>`IMPRESSION-FE-001` → cross-domain: rides `BOM-FE-002`<br>`IMPRESSION-FE-002` → cross-domain: rides `PRODUCT-FE-001` |
| 3 | 🟢 `G-03` | — | — |

### Story sequence

> One row per story in implementation order. `Depends On`/`Blocks` reference story ids + names (never order numbers). Every operation story also implicitly requires the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** means other stories share its step.

| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |
|---|---|---|---|---|---|---|
| 1 | 1 | 🟢 `B-01` — searchImpressionsByProductId data fetch… | Backend · BE-1 | None | every story in this domain (module scaffold) | No |
| 2 | 2 | 🟢 `B-02` — getImpressionCountsByProductId data fet… | Backend · BE-1 | `B-01` — searchImpressionsByProd… | `G-03` | Yes |
| 3 | 2 | 🟡 `D-01` — updateImpressions mutation | Backend · BE-1 | `B-01` — searchImpressionsByProd… | `G-03` | Yes |
| 4 | 2 | 🟢 `F-01` — Product.impressions / impressionCounts | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 5 | 2 | 🟢 `G-01` — Impression field resolvers | Backend · BE-1 | `B-01` — searchImpressionsByProd… | None | Yes |
| 6 | 2 | 🟡 `G-02` — ImpressionCount.counts aggregation | Backend · BE-1 | `B-01` — searchImpressionsByProd… | `G-03` | Yes |
| 7 | 2 | 🟢 `IMPRESSION-FE-001` — Migrate getBomDataAndImpressions | Frontend · FE-2 | `B-01` — searchImpressionsByProd…, `B-01` — searchImpressionsByProd…, `BOM-FE-002` | None | Yes |
| 8 | 2 | 🟢 `IMPRESSION-FE-002` — Migrate getCarryForwardFormData | Frontend · FE-2 | `B-01` — searchImpressionsByProd…, `B-01` — searchImpressionsByProd…, `PRODUCT-FE-001` | None | Yes |
| 9 | 3 | 🟢 `G-03` — Test coverage & parity | Backend · BE-1 | `B-01` — searchImpressionsByProd…, `B-02` — getImpressionCountsByPr…, `D-01` — updateImpressions mutat…, `G-02` — ImpressionCount.counts … | None | No |

**Backend critical path:** `B-01` → `G-02` → `G-03`.
**Frontend cutover flow:** `IMPRESSION-FE-001` → `IMPRESSION-FE-002`.

**Domain done when:** the last FE story is flipped and stable; BE F/G stories (federation stitches, field-resolver parity) may trail post-flip.

---

*Project plan · generated 2026-07-17 by generate_project_plan.py.*