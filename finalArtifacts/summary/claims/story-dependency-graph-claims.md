# Claims — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [claims/be-04-stories.md](../../../output/analysis/claims/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by implementation step — everything in one step can be built in parallel once every step before it is done. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph STEP1["Step 1 — 📖 Core Reads"]
    NB_01["B-01<br/>getClaims(parentHumanId, claimHum…"]
  end
  subgraph STEP2["Step 2 — 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🧪 Field Resolvers & Tests · 🧬 Entity Resolution"]
    NB_02["B-02<br/>getClaimByIds(claimHumanIds)"]
    NB_03["B-03<br/>getCommunicationChannels (cacheab…"]
    NB_04["B-04<br/>getAllClaimsAbout (cacheable)"]
    NB_05["B-05<br/>getClaimExports"]
    NC_01["C-01<br/>searchGuestFacing(queryParam)"]
    NC_02["C-02<br/>getClaimsElastic(parentHumanId)"]
    ND_01["D-01<br/>createClaim"]
    ND_02["D-02<br/>bulkUpdateClaim"]
    ND_03["D-03<br/>requestClaimExport"]
    ND_04["D-04<br/>lockClaim"]
    ND_05["D-05<br/>unlockClaim"]
    NE_01["E-01<br/>updateClaim (proxy ACL + multi-st…"]
    NG_01["G-01<br/>access + currentUserPermissions +…"]
    NG_02["G-02<br/>createdBy + updatedBy + businessP…"]
    NG_04["G-04<br/>workspaces + ClaimSubstantiate.su…"]
    NG_06["G-06<br/>Shared value-type alignment (@sha…"]
    NH_01["H-01<br/>Product.claims (federation contri…"]
    NH_02["H-02<br/>ResourcesCount.claims (TechPack —…"]
  end
  subgraph STEP3["Step 3 — 🧪 Field Resolvers & Tests"]
    NG_03["G-03<br/>product + parentDetails (otherCla…"]
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
  NB_01 --> NE_01
  NB_01 --> NH_01
  NB_01 --> NH_02
  NB_01 --> NG_01
  NB_01 --> NG_02
  NB_01 --> NG_03
  NG_06 --> NG_03
  NB_01 --> NG_04
  NB_01 --> NG_06
  G__SPIKE_01{{"🔬 SPIKE-01"}}
  G__SPIKE_01 -.-> NE_01
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_{{"⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)"}}
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_ -.-> NE_01
  G__BLOCKED_BY_product__PRODUCT_BE_F_14__product_side_stub_alignment__also_waits_on_the_Product_entity_existing__plm_product_Phase_A_{{"⛔ BLOCKED-BY product (PRODUCT-BE-F-14, product-side stub alignment; also waits on the Product entity existing, plm-product Phase A)"}}
  G__BLOCKED_BY_product__PRODUCT_BE_F_14__product_side_stub_alignment__also_waits_on_the_Product_entity_existing__plm_product_Phase_A_ -.-> NH_01
  G__BLOCKED_BY_product__PRODUCT_BE_E_03__TechPack_facade__also_PRODUCT_BE_F_14_contract_alignment_{{"⛔ BLOCKED-BY product (PRODUCT-BE-E-03, TechPack facade; also PRODUCT-BE-F-14 contract alignment)"}}
  G__BLOCKED_BY_product__PRODUCT_BE_E_03__TechPack_facade__also_PRODUCT_BE_F_14_contract_alignment_ -.-> NH_02
```

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: the **bold arrows** are the actual gate — a frontend story cannot start until every backend story pointing at it (and, transitively, everything upstream of those) has shipped.

```mermaid
flowchart LR
  subgraph BE["Backend — must ship first"]
    NB_01["B-01<br/>getClaims(parentHumanId, claimHum…"]
    NB_02["B-02<br/>getClaimByIds(claimHumanIds)"]
    NB_03["B-03<br/>getCommunicationChannels (cacheab…"]
    NB_04["B-04<br/>getAllClaimsAbout (cacheable)"]
    ND_01["D-01<br/>createClaim"]
    ND_02["D-02<br/>bulkUpdateClaim"]
    ND_03["D-03<br/>requestClaimExport"]
    ND_04["D-04<br/>lockClaim"]
    ND_05["D-05<br/>unlockClaim"]
    NE_01["E-01<br/>updateClaim (proxy ACL + multi-st…"]
    NG_01["G-01<br/>access + currentUserPermissions +…"]
    NG_02["G-02<br/>createdBy + updatedBy + businessP…"]
    NG_03["G-03<br/>product + parentDetails (otherCla…"]
    NG_06["G-06<br/>Shared value-type alignment (@sha…"]
  end
  subgraph FE["Frontend — this domain's cutover stories"]
    NCLAIM_FE_001["CLAIM-FE-001<br/>Split the claim fragment factory a"]
    NCLAIM_FE_002["CLAIM-FE-002<br/>Migrate claim reads (first cross-s"]
    NCLAIM_FE_003["CLAIM-FE-003<br/>Migrate claim simple mutations and"]
    NCLAIM_FE_004["CLAIM-FE-004<br/>Migrate `updateClaim` multi-step w"]
  end
  NB_01 --> NB_02
  NB_01 --> ND_04
  NG_06 --> NG_03
  NB_01 --> NG_03
  NB_01 --> NB_03
  NB_01 --> NG_06
  NB_01 --> NG_02
  NB_01 --> NG_01
  NB_01 --> ND_02
  NB_01 --> ND_01
  NB_01 --> NB_04
  NB_01 --> ND_03
  NB_01 --> ND_05
  NB_01 --> NE_01
  NB_01 ==>|gates| NCLAIM_FE_002
  NB_02 ==>|gates| NCLAIM_FE_002
  NB_03 ==>|gates| NCLAIM_FE_002
  NB_04 ==>|gates| NCLAIM_FE_002
  NG_01 ==>|gates| NCLAIM_FE_002
  NG_02 ==>|gates| NCLAIM_FE_002
  NG_03 ==>|gates| NCLAIM_FE_002
  ND_01 ==>|gates| NCLAIM_FE_003
  ND_02 ==>|gates| NCLAIM_FE_003
  ND_03 ==>|gates| NCLAIM_FE_003
  ND_04 ==>|gates| NCLAIM_FE_003
  ND_05 ==>|gates| NCLAIM_FE_003
  NE_01 ==>|gates| NCLAIM_FE_004
```

---
*Story dependency graphs · claims · generated 2026-07-21.*