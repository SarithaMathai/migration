# BOM — Frontend Readiness

> Generated 2026-07-24 from `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [bom/be-04-stories.md](../../../output/analysis/bom/be-04-stories.md). Backend build-order sequencing: [00-sequencing.md](../../00-sequencing.md).

---

## What must ship before FE can start

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. A frontend story cannot start until every backend story pointing at it has shipped.

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
*Story dependency graph · bom · generated 2026-07-24.*