# Impression — Frontend Readiness

> Generated 2026-07-24 from `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [impression/be-04-stories.md](../../../output/analysis/impression/be-04-stories.md). Backend build-order sequencing: [00-sequencing.md](../../00-sequencing.md).

---

## What must ship before FE can start

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. A frontend story cannot start until every backend story pointing at it has shipped.

### IMPRESSION-FE-001 · Migrate `getBomDataAndImpressions` (with BOM wave)

```mermaid
flowchart LR
  NB_01["B-01<br/>searchImpressionsByProductI…"]
  NG_01["G-01<br/>Impression field resolvers…"]
  NIMPRESSION_FE_001(["IMPRESSION-FE-001"])
  NB_01 ==> NIMPRESSION_FE_001
  NG_01 ==> NIMPRESSION_FE_001
```

### IMPRESSION-FE-002 · Migrate `getCarryForwardFormData` (with Product wave)

```mermaid
flowchart LR
  NB_01["B-01<br/>searchImpressionsByProductI…"]
  NG_01["G-01<br/>Impression field resolvers…"]
  NG_02["G-02<br/>ImpressionCount.counts aggr…"]
  NIMPRESSION_FE_002(["IMPRESSION-FE-002"])
  NB_01 ==> NIMPRESSION_FE_002
  NG_01 ==> NIMPRESSION_FE_002
  NG_02 ==> NIMPRESSION_FE_002
```

---
*Story dependency graph · impression · generated 2026-07-24.*