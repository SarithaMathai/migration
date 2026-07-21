# BOM — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [bom/be-04-stories.md](../../../output/analysis/bom/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by **phase** (reads, then search, then mutations, then complex/federation/field-resolver work) — arrows show only the direct `Depends on:` edges. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph PHA["🧱 Phase A — Foundation & Type Resolvers"]
    NA_04["A-04<br/>@DgsTypeResolver for the 2 BOM in…"]
    NA_05["A-05<br/>Shared CI conformance gate + code…"]
  end
  subgraph PHB["📖 Phase B — Core Reads"]
    NB_01["B-01<br/>getBomByIds data fetcher"]
    NB_03["B-03<br/>getBomStatus (cacheable master da…"]
    NB_04["B-04<br/>getBomByParentId data fetcher"]
    NB_05["B-05<br/>getBomMaterialTypes (merge with M…"]
    NB_06["B-06<br/>getBomPackagingMaterialTypes (cac…"]
    NB_07["B-07<br/>getBomPackagingSubstrates (cachea…"]
    NB_08["B-08<br/>getBomPackagingUnitOfMeasure (cac…"]
  end
  subgraph PHC["🔍 Phase C — Search & Listing"]
    NC_01["C-01<br/>getBomElastic data fetcher"]
    NC_02["C-02<br/>searchMaterialsBom data fetcher"]
    NC_03["C-03<br/>getComboSupplierForBom data fetch…"]
    NC_04["C-04<br/>getValidTrimSuppliersForBom data…"]
    NC_05["C-05<br/>getValidRawMaterialSuppliersForBo…"]
  end
  subgraph PHD["✏️ Phase D — Mutations"]
    ND_01["D-01<br/>addBom mutation"]
    ND_02["D-02<br/>manageBomWorkspaces mutation"]
    ND_03["D-03<br/>lockBom mutation"]
    ND_04["D-04<br/>unlockBom mutation"]
    ND_05["D-05<br/>updateBomComponentStatus mutation"]
  end
  subgraph PHE["⚙️ Phase E — Complex Operations"]
    NE_01["E-01<br/>updateBom — 3-step orchestrated w…"]
  end
  subgraph PHF["🔗 Phase F — Federation & Stitching"]
    NF_01["F-01<br/>Implement Product.productBoms / b…"]
    NF_02["F-02<br/>Fill ResourcesCount.bomsCount (in…"]
  end
  subgraph PHG["🧪 Phase G — Field Resolvers & Tests"]
    NG_01["G-01<br/>Bom field resolvers (9 shared fie…"]
    NG_03["G-03<br/>BomMaterial field resolvers (8 fi…"]
    NG_04["G-04<br/>BomPackagingMaterial field resolv…"]
    NG_05["G-05<br/>BomFabricMaterial field resolvers…"]
    NG_06["G-06<br/>BomFabricSpecMaterial field resol…"]
    NG_07["G-07<br/>BomCombinationMaterial field reso…"]
    NG_08["G-08<br/>BomTrimMaterial field resolvers (…"]
    NG_09["G-09<br/>BomWashMaterial field resolvers (…"]
    NG_10["G-10<br/>Impression library-resource resol…"]
    NG_11["G-11<br/>BomFabricLibraryImpressionDetails…"]
    NG_12["G-12<br/>BomTrimLibraryImpressionDetails f…"]
    NG_13["G-13<br/>BomTrimZipperLibraryImpressionDet…"]
    NG_14["G-14<br/>Trivial pass-through fields (bund…"]
    NG_15["G-15<br/>BomMaterialSearchResult field res…"]
    NG_17["G-17<br/>supplier entity references on mat…"]
  end
  NA_04 --> NA_05
  ND_02 --> NE_01
  NG_10 --> NG_11
  NG_10 --> NG_12
  NG_10 --> NG_13
  NC_02 --> NG_15
  NG_01 --> NG_17
  G__SPIKE_05{{"🔬 SPIKE-05"}}
  G__SPIKE_05 -.-> NA_04
  G__SPIKE_06a{{"🔬 SPIKE-06a"}}
  G__SPIKE_06a -.-> NB_05
  G__SPIKE_01{{"🔬 SPIKE-01"}}
  G__SPIKE_01 -.-> NE_01
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_{{"⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)"}}
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_ -.-> NE_01
```

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