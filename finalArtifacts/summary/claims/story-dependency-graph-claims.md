# Claims — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [claims/be-04-stories.md](../../../output/analysis/claims/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by **phase** (reads, then search, then mutations, then complex/federation/field-resolver work) — arrows show only the direct `Depends on:` edges. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph PHB["📖 Phase B — Core Reads"]
    NB_01["B-01<br/>getClaims(parentHumanId, claimHum…"]
    NB_02["B-02<br/>getClaimByIds(claimHumanIds)"]
    NB_03["B-03<br/>getCommunicationChannels (cacheab…"]
    NB_04["B-04<br/>getAllClaimsAbout (cacheable)"]
    NB_05["B-05<br/>getClaimExports"]
  end
  subgraph PHC["🔍 Phase C — Search & Listing"]
    NC_01["C-01<br/>searchGuestFacing(queryParam)"]
    NC_02["C-02<br/>getClaimsElastic(parentHumanId)"]
  end
  subgraph PHD["✏️ Phase D — Mutations"]
    ND_01["D-01<br/>createClaim"]
    ND_02["D-02<br/>bulkUpdateClaim"]
    ND_03["D-03<br/>requestClaimExport"]
    ND_04["D-04<br/>lockClaim"]
    ND_05["D-05<br/>unlockClaim"]
  end
  subgraph PHE["⚙️ Phase E — Complex Operations"]
    NE_01["E-01<br/>updateClaim (proxy ACL + multi-st…"]
  end
  subgraph PHG["🧪 Phase G — Field Resolvers & Tests"]
    NG_01["G-01<br/>access + currentUserPermissions +…"]
    NG_02["G-02<br/>createdBy + updatedBy + businessP…"]
    NG_03["G-03<br/>product + parentDetails (otherCla…"]
    NG_04["G-04<br/>workspaces + ClaimSubstantiate.su…"]
    NG_06["G-06<br/>Shared value-type alignment (@sha…"]
  end
  subgraph PHH["🧬 Phase H — Entity Resolution"]
    NH_01["H-01<br/>Product.claims (federation contri…"]
    NH_02["H-02<br/>ResourcesCount.claims (TechPack —…"]
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

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

### CLAIM-FE-001 · Split the claim fragment factory and re-target claim fragments

```mermaid
flowchart LR
  NCLAIM_FE_001["CLAIM-FE-001<br/>no backend gate — ready to start"]
```

### CLAIM-FE-002 · Migrate claim reads (first cross-subgraph cutover)

```mermaid
flowchart LR
  NB_01["B-01<br/>getClaims(parentHumanId, cl…"]
  NB_02["B-02<br/>getClaimByIds(claimHumanIds)"]
  NB_03["B-03<br/>getCommunicationChannels (c…"]
  NB_04["B-04<br/>getAllClaimsAbout (cacheabl…"]
  NG_01["G-01<br/>access + currentUserPermiss…"]
  NG_02["G-02<br/>createdBy + updatedBy + bus…"]
  NG_03["G-03<br/>product + parentDetails (ot…"]
  NCLAIM_FE_002(["CLAIM-FE-002"])
  NB_01 ==> NCLAIM_FE_002
  NB_02 ==> NCLAIM_FE_002
  NB_03 ==> NCLAIM_FE_002
  NB_04 ==> NCLAIM_FE_002
  NG_01 ==> NCLAIM_FE_002
  NG_02 ==> NCLAIM_FE_002
  NG_03 ==> NCLAIM_FE_002
```

### CLAIM-FE-003 · Migrate claim simple mutations and export

```mermaid
flowchart LR
  ND_01["D-01<br/>createClaim"]
  ND_02["D-02<br/>bulkUpdateClaim"]
  ND_03["D-03<br/>requestClaimExport"]
  ND_04["D-04<br/>lockClaim"]
  ND_05["D-05<br/>unlockClaim"]
  NCLAIM_FE_003(["CLAIM-FE-003"])
  ND_01 ==> NCLAIM_FE_003
  ND_02 ==> NCLAIM_FE_003
  ND_03 ==> NCLAIM_FE_003
  ND_04 ==> NCLAIM_FE_003
  ND_05 ==> NCLAIM_FE_003
```

### CLAIM-FE-004 · Migrate `updateClaim` multi-step write handling

```mermaid
flowchart LR
  NE_01["E-01<br/>updateClaim (proxy ACL + mu…"]
  NCLAIM_FE_004(["CLAIM-FE-004"])
  NE_01 ==> NCLAIM_FE_004
```

---
*Story dependency graphs · claims · generated 2026-07-21.*