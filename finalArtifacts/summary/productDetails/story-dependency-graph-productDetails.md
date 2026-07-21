# Product Details — Frontend Readiness

> Generated 2026-07-21 from `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [productDetails/be-04-stories.md](../../../output/analysis/productDetails/be-04-stories.md). Backend build-order sequencing: [00-sequencing.md](../../00-sequencing.md).

---

## What must ship before FE can start

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. A frontend story cannot start until every backend story pointing at it has shipped.

### PDTL-FE-001 · Migrate product-details reads

```mermaid
flowchart LR
  NB_01["B-01<br/>getProductDetailsById(ids)"]
  NG_01["G-01<br/>access + currentUserPermiss…"]
  NG_02["G-02<br/>product + createdBy + updat…"]
  NG_03["G-03<br/>attachment + item attachmen…"]
  NPDTL_FE_001(["PDTL-FE-001"])
  NB_01 ==> NPDTL_FE_001
  NG_01 ==> NPDTL_FE_001
  NG_02 ==> NPDTL_FE_001
  NG_03 ==> NPDTL_FE_001
```

### PDTL-FE-002 · Migrate product-details simple mutations

```mermaid
flowchart LR
  ND_01["D-01<br/>createProductDetailsSet"]
  ND_03["D-03<br/>productDetailLockUnlock"]
  ND_04["D-04<br/>cloneFilesForProductDetails"]
  ND_05["D-05<br/>updateProductDetailComponen…"]
  NPDTL_FE_002(["PDTL-FE-002"])
  ND_01 ==> NPDTL_FE_002
  ND_03 ==> NPDTL_FE_002
  ND_04 ==> NPDTL_FE_002
  ND_05 ==> NPDTL_FE_002
```

### PDTL-FE-003 · Migrate `updateProductDetailsSet` saga handling

```mermaid
flowchart LR
  NE_01["E-01<br/>updateProductDetailsSet (mu…"]
  NPDTL_FE_003(["PDTL-FE-003"])
  NE_01 ==> NPDTL_FE_003
```

---
*Story dependency graph · productDetails · generated 2026-07-21.*