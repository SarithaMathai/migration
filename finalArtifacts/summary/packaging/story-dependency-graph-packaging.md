# Packaging — Frontend Readiness

> Generated 2026-07-21 from `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [packaging/be-04-stories.md](../../../output/analysis/packaging/be-04-stories.md). Backend build-order sequencing: [00-sequencing.md](../../00-sequencing.md).

---

## What must ship before FE can start

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. A frontend story cannot start until every backend story pointing at it has shipped.

### PKG-FE-001 · Migrate packaging reads

```mermaid
flowchart LR
  NB_01["B-01<br/>getPackagings(...)"]
  NB_02["B-02<br/>getPackagingById(packagingI…"]
  NG_01["G-01<br/>access + businessPartner +…"]
  NG_02["G-02<br/>createdBy + updatedBy + die…"]
  NG_04["G-04<br/>suggestedRetailPriceByDPCI…"]
  NPKG_FE_001(["PKG-FE-001"])
  NB_01 ==> NPKG_FE_001
  NB_02 ==> NPKG_FE_001
  NG_01 ==> NPKG_FE_001
  NG_02 ==> NPKG_FE_001
  NG_04 ==> NPKG_FE_001
```

### PKG-FE-002 · Migrate packaging master-data reads and retire deprecated fields

```mermaid
flowchart LR
  NB_04["B-04<br/>getPackagingFieldValuesByTy…"]
  NB_06["B-06<br/>getCountries(codes) (cachea…"]
  NPKG_FE_002(["PKG-FE-002"])
  NB_04 ==> NPKG_FE_002
  NB_06 ==> NPKG_FE_002
```

### PKG-FE-003 · Migrate dieline flows

```mermaid
flowchart LR
  NB_03["B-03<br/>getDielines(...)"]
  NB_05["B-05<br/>getDielineEvaluationStatuse…"]
  ND_02["D-02<br/>evaluateDieline"]
  NG_05["G-05<br/>Dieline + PrinterDieline +…"]
  NPKG_FE_003(["PKG-FE-003"])
  NB_03 ==> NPKG_FE_003
  NB_05 ==> NPKG_FE_003
  ND_02 ==> NPKG_FE_003
  NG_05 ==> NPKG_FE_003
```

### PKG-FE-004 · Migrate packaging simple mutations and export

```mermaid
flowchart LR
  ND_01["D-01<br/>addPackaging"]
  ND_03["D-03<br/>bulkAddPackagings"]
  ND_04["D-04<br/>bulkUpdatePackagings"]
  ND_05["D-05<br/>exportPackaging"]
  ND_06["D-06<br/>lockPackaging"]
  ND_07["D-07<br/>unlockPackaging"]
  ND_09["D-09<br/>updatePackagingComponentSta…"]
  NPKG_FE_004(["PKG-FE-004"])
  ND_01 ==> NPKG_FE_004
  ND_03 ==> NPKG_FE_004
  ND_04 ==> NPKG_FE_004
  ND_05 ==> NPKG_FE_004
  ND_06 ==> NPKG_FE_004
  ND_07 ==> NPKG_FE_004
  ND_09 ==> NPKG_FE_004
```

### PKG-FE-005 · Migrate `updatePackaging` saga handling and packet information

```mermaid
flowchart LR
  NE_01["E-01<br/>updatePackaging (multi-step…"]
  NPKG_FE_005(["PKG-FE-005"])
  NE_01 ==> NPKG_FE_005
```

---
*Story dependency graph · packaging · generated 2026-07-21.*