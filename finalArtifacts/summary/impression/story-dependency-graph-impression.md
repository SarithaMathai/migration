# Impression — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [impression/be-04-stories.md](../../../output/analysis/impression/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by **phase** (reads, then search, then mutations, then complex/federation/field-resolver work) — arrows show only the direct `Depends on:` edges. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph PHB["📖 Phase B — Core Reads"]
    NB_01["B-01<br/>searchImpressionsByProductId data…"]
    NB_02["B-02<br/>getImpressionCountsByProductId da…"]
  end
  subgraph PHD["✏️ Phase D — Mutations"]
    ND_01["D-01<br/>updateImpressions mutation"]
  end
  subgraph PHF["🔗 Phase F — Federation & Stitching"]
    NF_01["F-01<br/>Product.impressions / impressionC…"]
  end
  subgraph PHG["🧪 Phase G — Field Resolvers & Tests"]
    NG_01["G-01<br/>Impression field resolvers (5 fie…"]
    NG_02["G-02<br/>ImpressionCount.counts aggregation"]
    NG_04["G-04<br/>attachment entity reference (reco…"]
  end
  NB_01 --> NB_02
  NB_01 --> ND_01
  NB_01 --> NF_01
  NB_01 --> NG_01
  NB_01 --> NG_02
  NB_01 --> NG_04
  G__BLOCKED_BY_product__PRODUCT_BE_B_01__exposes_the_field_this_story_reads_{{"⛔ BLOCKED-BY product (PRODUCT-BE-B-01, exposes the field this story reads)"}}
  G__BLOCKED_BY_product__PRODUCT_BE_B_01__exposes_the_field_this_story_reads_ -.-> NF_01
```

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

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
*Story dependency graphs · impression · generated 2026-07-21.*