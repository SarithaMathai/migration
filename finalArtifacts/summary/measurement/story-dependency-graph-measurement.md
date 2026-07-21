# Measurement — Frontend Readiness

> Generated 2026-07-21 from `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [measurement/be-04-stories.md](../../../output/analysis/measurement/be-04-stories.md). Backend build-order sequencing: [00-sequencing.md](../../00-sequencing.md).

---

## What must ship before FE can start

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. A frontend story cannot start until every backend story pointing at it has shipped.

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
*Story dependency graph · measurement · generated 2026-07-21.*