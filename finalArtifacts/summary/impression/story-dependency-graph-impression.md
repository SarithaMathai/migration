# Impression — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [impression/be-04-stories.md](../../../output/analysis/impression/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by implementation step — everything in one step can be built in parallel once every step before it is done. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph STEP1["Step 1 — 📖 Core Reads"]
    NB_01["B-01<br/>searchImpressionsByProductId data…"]
  end
  subgraph STEP2["Step 2 — 📖 Core Reads · ✏️ Mutations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests"]
    NB_02["B-02<br/>getImpressionCountsByProductId da…"]
    ND_01["D-01<br/>updateImpressions mutation"]
    NF_01["F-01<br/>Product.impressions / impressionC…"]
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

For the frontend engineer or PO checking whether backend is far enough along: the **bold arrows** are the actual gate — a frontend story cannot start until every backend story pointing at it (and, transitively, everything upstream of those) has shipped.

```mermaid
flowchart LR
  subgraph BE["Backend — must ship first"]
    NB_01["B-01<br/>searchImpressionsByProductId data…"]
    NG_01["G-01<br/>Impression field resolvers (5 fie…"]
    NG_02["G-02<br/>ImpressionCount.counts aggregation"]
  end
  subgraph FE["Frontend — this domain's cutover stories"]
    NIMPRESSION_FE_001["IMPRESSION-FE-001<br/>Migrate `getBomDataAndImpressions`"]
    NIMPRESSION_FE_002["IMPRESSION-FE-002<br/>Migrate `getCarryForwardFormData` "]
  end
  NB_01 --> NG_02
  NB_01 --> NG_01
  NB_01 ==>|gates| NIMPRESSION_FE_001
  NG_01 ==>|gates| NIMPRESSION_FE_001
  NB_01 ==>|gates| NIMPRESSION_FE_002
  NG_01 ==>|gates| NIMPRESSION_FE_002
  NG_02 ==>|gates| NIMPRESSION_FE_002
```

---
*Story dependency graphs · impression · generated 2026-07-21.*