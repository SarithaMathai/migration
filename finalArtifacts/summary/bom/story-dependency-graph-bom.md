# BOM — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [bom/be-04-stories.md](../../../output/analysis/bom/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

One box per **phase** (reads, search, mutations, complex ops, federation, field resolvers, entity resolution) — not one box per story, which stops being readable past a couple dozen stories. An arrow between two phase boxes means at least one story in the target phase directly depends on a story in the source phase; the label is how many story-level dependencies that represents. 🔬/⛔ on a box means at least one story in that phase is spike- or cross-subgraph-gated — see the table below for exactly which one.

```mermaid
flowchart TD
  PHA["🧱 Phase A<br/>Foundation & Type Resolvers<br/>(2 stories) 🔬"]
  PHB["📖 Phase B<br/>Core Reads<br/>(7 stories) 🔬"]
  PHC["🔍 Phase C<br/>Search & Listing<br/>(5 stories)"]
  PHD["✏️ Phase D<br/>Mutations<br/>(5 stories)"]
  PHE["⚙️ Phase E<br/>Complex Operations<br/>(1 story) 🔬 ⛔"]
  PHF["🔗 Phase F<br/>Federation & Stitching<br/>(2 stories)"]
  PHG["🧪 Phase G<br/>Field Resolvers & Tests<br/>(15 stories)"]
  PHD -->|1 dep| PHE
  PHC -->|1 dep| PHG
```

**Story-level detail** (every story in this domain, its phase, its direct `Depends on:`, and any gate):

| Story | Phase | Depends on | Gate |
|---|---|---|---|
| `A-04` — @DgsTypeResolver for the 2 BOM interfaces | A | — | 🔬 SPIKE-05 |
| `A-05` — Shared CI conformance gate + code → type registry (SPIKE-05) | A | `A-04` | — |
| `B-01` — getBomByIds data fetcher | B | — | — |
| `B-03` — getBomStatus (cacheable master data) | B | — | — |
| `B-04` — getBomByParentId data fetcher | B | — | — |
| `B-05` — getBomMaterialTypes (merge with Material Hub) | B | — | 🔬 SPIKE-06a |
| `B-06` — getBomPackagingMaterialTypes (cacheable) | B | — | — |
| `B-07` — getBomPackagingSubstrates (cacheable) | B | — | — |
| `B-08` — getBomPackagingUnitOfMeasure (cacheable) | B | — | — |
| `C-01` — getBomElastic data fetcher | C | — | — |
| `C-02` — searchMaterialsBom data fetcher | C | — | — |
| `C-03` — getComboSupplierForBom data fetcher | C | — | — |
| `C-04` — getValidTrimSuppliersForBom data fetcher | C | — | — |
| `C-05` — getValidRawMaterialSuppliersForBom data fetcher | C | — | — |
| `D-01` — addBom mutation | D | — | — |
| `D-02` — manageBomWorkspaces mutation | D | — | — |
| `D-03` — lockBom mutation | D | — | — |
| `D-04` — unlockBom mutation | D | — | — |
| `D-05` — updateBomComponentStatus mutation | D | — | — |
| `E-01` — updateBom — 3-step orchestrated write | E | `D-02` | ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module), 🔬 SPIKE-01 |
| `F-01` — Implement Product.productBoms / boms / packagingBoms (internal) | F | — | — |
| `F-02` — Fill ResourcesCount.bomsCount (internal) | F | — | — |
| `G-01` — Bom field resolvers (9 shared fields) | G | — | — |
| `G-03` — BomMaterial field resolvers (8 fields) | G | — | — |
| `G-04` — BomPackagingMaterial field resolvers (2 fields) | G | — | — |
| `G-05` — BomFabricMaterial field resolvers (4 fields) | G | — | — |
| `G-06` — BomFabricSpecMaterial field resolvers (4 fields) | G | — | — |
| `G-07` — BomCombinationMaterial field resolvers (4 fields) | G | — | — |
| `G-08` — BomTrimMaterial field resolvers (7 fields) — trim size dispatchers | G | — | — |
| `G-09` — BomWashMaterial field resolvers (4 fields) | G | — | — |
| `G-10` — Impression library-resource resolution (shared internal/external branch + MaterialDataLoader) | G | — | — |
| `G-11` — BomFabricLibraryImpressionDetails.libraryResource | G | `G-10` | — |
| `G-12` — BomTrimLibraryImpressionDetails field resolvers (3 fields) | G | `G-10` | — |
| `G-13` — BomTrimZipperLibraryImpressionDetails field resolvers (3 colors) | G | `G-10` | — |
| `G-14` — Trivial pass-through fields (bundle) | G | — | — |
| `G-15` — BomMaterialSearchResult field resolvers (5 fields) | G | `C-02` | — |
| `G-17` — supplier entity references on material rows (recommended, PO-gated) | G | `G-01` | — |

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

### BOM-FE-001 · Statically expand BOM fragment factories (pre-cutover)

```mermaid
flowchart LR
  NBOM_FE_001["BOM-FE-001<br/>no backend gate — ready to start"]
```

### BOM-FE-002 · Migrate BOM core reads

```mermaid
flowchart LR
  NA_04["A-04<br/>@DgsTypeResolver for the 2…"]
  NB_01["B-01<br/>getBomByIds data fetcher"]
  NB_03["B-03<br/>getBomStatus (cacheable mas…"]
  NB_04["B-04<br/>getBomByParentId data fetch…"]
  NG_01["G-01<br/>Bom field resolvers (9 shar…"]
  NG_03["G-03<br/>BomMaterial field resolvers…"]
  NG_08["G-08<br/>BomTrimMaterial field resol…"]
  NG_12["G-12<br/>BomTrimLibraryImpressionDet…"]
  NG_13["G-13<br/>BomTrimZipperLibraryImpress…"]
  NG_17["G-17<br/>supplier entity references…"]
  NBOM_FE_002(["BOM-FE-002"])
  NA_04 ==> NBOM_FE_002
  NB_01 ==> NBOM_FE_002
  NB_03 ==> NBOM_FE_002
  NB_04 ==> NBOM_FE_002
  NG_01 ==> NBOM_FE_002
  NG_03 ==> NBOM_FE_002
  NG_08 ==> NBOM_FE_002
  NG_12 ==> NBOM_FE_002
  NG_13 ==> NBOM_FE_002
  NG_17 ==> NBOM_FE_002
```

### BOM-FE-003 · Migrate BOM search and elastic reads

```mermaid
flowchart LR
  NC_01["C-01<br/>getBomElastic data fetcher"]
  NG_01["G-01<br/>Bom field resolvers (9 shar…"]
  NG_14["G-14<br/>Trivial pass-through fields…"]
  NBOM_FE_003(["BOM-FE-003"])
  NC_01 ==> NBOM_FE_003
  NG_01 ==> NBOM_FE_003
  NG_14 ==> NBOM_FE_003
```

### BOM-FE-004 · Migrate BOM master-data reads

```mermaid
flowchart LR
  NB_05["B-05<br/>getBomMaterialTypes (merge…"]
  NB_06["B-06<br/>getBomPackagingMaterialType…"]
  NB_07["B-07<br/>getBomPackagingSubstrates (…"]
  NB_08["B-08<br/>getBomPackagingUnitOfMeasur…"]
  NG_14["G-14<br/>Trivial pass-through fields…"]
  NBOM_FE_004(["BOM-FE-004"])
  NB_05 ==> NBOM_FE_004
  NB_06 ==> NBOM_FE_004
  NB_07 ==> NBOM_FE_004
  NB_08 ==> NBOM_FE_004
  NG_14 ==> NBOM_FE_004
```

### BOM-FE-005 · Migrate BOM supplier reads

```mermaid
flowchart LR
  NC_03["C-03<br/>getComboSupplierForBom data…"]
  NC_04["C-04<br/>getValidTrimSuppliersForBom…"]
  NC_05["C-05<br/>getValidRawMaterialSupplier…"]
  NBOM_FE_005(["BOM-FE-005"])
  NC_03 ==> NBOM_FE_005
  NC_04 ==> NBOM_FE_005
  NC_05 ==> NBOM_FE_005
```

### BOM-FE-006 · Migrate BOM mutations including `updateBom` saga handling

```mermaid
flowchart LR
  ND_01["D-01<br/>addBom mutation"]
  ND_03["D-03<br/>lockBom mutation"]
  ND_04["D-04<br/>unlockBom mutation"]
  ND_05["D-05<br/>updateBomComponentStatus mu…"]
  NBOM_FE_006(["BOM-FE-006"])
  ND_01 ==> NBOM_FE_006
  ND_03 ==> NBOM_FE_006
  ND_04 ==> NBOM_FE_006
  ND_05 ==> NBOM_FE_006
```

### BOM-FE-007 · Adopt BOM `supplier` entity references (optional, PO-gated)

```mermaid
flowchart LR
  NA_04["A-04<br/>@DgsTypeResolver for the 2…"]
  NB_01["B-01<br/>getBomByIds data fetcher"]
  NB_03["B-03<br/>getBomStatus (cacheable mas…"]
  NB_04["B-04<br/>getBomByParentId data fetch…"]
  NG_01["G-01<br/>Bom field resolvers (9 shar…"]
  NG_03["G-03<br/>BomMaterial field resolvers…"]
  NG_08["G-08<br/>BomTrimMaterial field resol…"]
  NG_12["G-12<br/>BomTrimLibraryImpressionDet…"]
  NG_13["G-13<br/>BomTrimZipperLibraryImpress…"]
  NG_14["G-14<br/>Trivial pass-through fields…"]
  NG_17["G-17<br/>supplier entity references…"]
  NBOM_FE_007(["BOM-FE-007"])
  NA_04 ==> NBOM_FE_007
  NB_01 ==> NBOM_FE_007
  NB_03 ==> NBOM_FE_007
  NB_04 ==> NBOM_FE_007
  NG_01 ==> NBOM_FE_007
  NG_03 ==> NBOM_FE_007
  NG_08 ==> NBOM_FE_007
  NG_12 ==> NBOM_FE_007
  NG_13 ==> NBOM_FE_007
  NG_14 ==> NBOM_FE_007
  NG_17 ==> NBOM_FE_007
```

---
*Story dependency graphs · bom · generated 2026-07-21.*