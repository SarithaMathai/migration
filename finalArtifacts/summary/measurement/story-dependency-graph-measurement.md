# Measurement — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [measurement/be-04-stories.md](../../../output/analysis/measurement/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by **phase** (reads, then search, then mutations, then complex/federation/field-resolver work) — arrows show only the direct `Depends on:` edges. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph PHB["📖 Phase B — Core Reads"]
    NB_01["B-01<br/>getMeasurementByIds data fetcher"]
    NB_02["B-02<br/>getUnitsOfMeasure (cacheable)"]
    NB_03["B-03<br/>getThicknessUnitsOfMeasure (cache…"]
    NB_04["B-04<br/>getMeasurementSetStatus (cacheabl…"]
    NB_05["B-05<br/>getSampleMeasurement data fetcher"]
    NB_06["B-06<br/>getMeasurementTemplates + getMeas…"]
    NB_07["B-07<br/>getSizeTemplates + getSizeCategor…"]
    NB_08["B-08<br/>getTightFits + getTightFitByIdAnd…"]
    NB_09["B-09<br/>searchSparkSizes data fetcher (NE…"]
  end
  subgraph PHC["🔍 Phase C — Search & Listing"]
    NC_01["C-01<br/>getMeasurements data fetcher (rel…"]
    NC_02["C-02<br/>getMeasurementsElastic data fetch…"]
  end
  subgraph PHD["✏️ Phase D — Mutations"]
    ND_01["D-01<br/>addMeasurement mutation"]
    ND_02["D-02<br/>updateMeasurementAccess mutation"]
    ND_03["D-03<br/>lockMeasurementSet mutation"]
    ND_04["D-04<br/>unlockMeasurementSet mutation"]
    ND_05["D-05<br/>updateMeasurementComponentStatus…"]
    ND_06["D-06<br/>putSampleMeasurementSet mutation"]
    ND_07["D-07<br/>deleteSampleMeasurementSet mutati…"]
    ND_08["D-08<br/>addMeasurementTemplate + updateMe…"]
    ND_09["D-09<br/>addSizeTemplate + updateSizeTempl…"]
    ND_10["D-10<br/>addTightFit + updateTightFit muta…"]
  end
  subgraph PHE["⚙️ Phase E — Complex Operations"]
    NE_01["E-01<br/>updateMeasurement — 2-step orches…"]
  end
  subgraph PHF["🔗 Phase F — Federation & Stitching"]
    NF_01["F-01<br/>Implement Product.measurementSets…"]
  end
  subgraph PHG["🧪 Phase G — Field Resolvers & Tests"]
    NG_01["G-01<br/>Measurement field resolvers (13 f…"]
    NG_02["G-02<br/>SampleMeasurementSet field resolv…"]
    NG_05["G-05<br/>MeasurementTemplate field resolve…"]
    NG_06["G-06<br/>SizeTemplate field resolvers (3 f…"]
    NG_07["G-07<br/>TightFit field resolvers (5 field…"]
  end
  subgraph PHH["🧬 Phase H — Entity Resolution"]
    NH_01["H-01<br/>Contribute sampleMeasurement to t…"]
    NH_02["H-02<br/>SampleMeasurementSet.sample forwa…"]
  end
  NB_01 --> NB_02
  NB_01 --> NB_03
  NB_01 --> NB_04
  NB_01 --> NB_05
  NB_01 --> NC_01
  NB_01 --> NC_02
  NB_01 --> ND_01
  NB_01 --> ND_02
  NB_01 --> ND_03
  NB_01 --> ND_04
  NB_01 --> ND_05
  NB_01 --> ND_06
  NB_01 --> ND_07
  NB_06 --> ND_08
  NB_07 --> ND_09
  NB_08 --> ND_10
  NB_01 --> NE_01
  NB_01 --> NF_01
  NB_01 --> NH_01
  NB_02 --> NH_02
  NB_05 --> NH_02
  NB_01 --> NG_01
  NB_06 --> NG_01
  NB_07 --> NG_01
  NB_08 --> NG_01
  NB_01 --> NG_02
  NB_06 --> NG_05
  NB_07 --> NG_06
  NB_08 --> NG_07
  G__SPIKE_01{{"🔬 SPIKE-01"}}
  G__SPIKE_01 -.-> NE_01
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_{{"⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)"}}
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_ -.-> NE_01
  G__BLOCKED_BY_sample{{"⛔ BLOCKED-BY sample"}}
  G__BLOCKED_BY_sample -.-> NH_01
  G__BLOCKED_BY_sample -.-> NH_02
```

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

### MST-FE-001 · Migrate measurement reads and retire `humanId`

```mermaid
flowchart LR
  NB_01["B-01<br/>getMeasurementByIds data fe…"]
  NB_04["B-04<br/>getMeasurementSetStatus (ca…"]
  NG_01["G-01<br/>Measurement field resolvers…"]
  NG_07["G-07<br/>TightFit field resolvers (5…"]
  NMST_FE_001(["MST-FE-001"])
  NB_01 ==> NMST_FE_001
  NB_04 ==> NMST_FE_001
  NG_01 ==> NMST_FE_001
  NG_07 ==> NMST_FE_001
```

### MST-FE-002 · Migrate measurement list/search reads

```mermaid
flowchart LR
  NB_01["B-01<br/>getMeasurementByIds data fe…"]
  NC_01["C-01<br/>getMeasurements data fetche…"]
  NC_02["C-02<br/>getMeasurementsElastic data…"]
  NG_01["G-01<br/>Measurement field resolvers…"]
  NG_07["G-07<br/>TightFit field resolvers (5…"]
  NMST_FE_002(["MST-FE-002"])
  NB_01 ==> NMST_FE_002
  NC_01 ==> NMST_FE_002
  NC_02 ==> NMST_FE_002
  NG_01 ==> NMST_FE_002
  NG_07 ==> NMST_FE_002
```

### MST-FE-003 · Migrate measurement master-data reads

```mermaid
flowchart LR
  NB_02["B-02<br/>getUnitsOfMeasure (cacheabl…"]
  NB_03["B-03<br/>getThicknessUnitsOfMeasure…"]
  NB_04["B-04<br/>getMeasurementSetStatus (ca…"]
  NMST_FE_003(["MST-FE-003"])
  NB_02 ==> NMST_FE_003
  NB_03 ==> NMST_FE_003
  NB_04 ==> NMST_FE_003
```

### MST-FE-004 · Migrate measurement mutations

```mermaid
flowchart LR
  ND_03["D-03<br/>lockMeasurementSet mutation"]
  ND_04["D-04<br/>unlockMeasurementSet mutati…"]
  ND_06["D-06<br/>putSampleMeasurementSet mut…"]
  ND_07["D-07<br/>deleteSampleMeasurementSet…"]
  NMST_FE_004(["MST-FE-004"])
  ND_03 ==> NMST_FE_004
  ND_04 ==> NMST_FE_004
  ND_06 ==> NMST_FE_004
  ND_07 ==> NMST_FE_004
```

---
*Story dependency graphs · measurement · generated 2026-07-21.*