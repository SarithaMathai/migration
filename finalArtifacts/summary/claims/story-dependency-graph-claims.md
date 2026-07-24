# Claims — Frontend Readiness

> Generated 2026-07-24 from `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [claims/be-04-stories.md](../../../output/analysis/claims/be-04-stories.md). Backend build-order sequencing: [00-sequencing.md](../../00-sequencing.md).

---

## What must ship before FE can start

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. A frontend story cannot start until every backend story pointing at it has shipped.

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
*Story dependency graph · claims · generated 2026-07-24.*