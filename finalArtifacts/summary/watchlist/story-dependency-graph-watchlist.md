# Watchlist — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [watchlist/be-04-stories.md](../../../output/analysis/watchlist/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by **phase** (reads, then search, then mutations, then complex/federation/field-resolver work) — arrows show only the direct `Depends on:` edges. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph PHB["📖 Phase B — Core Reads"]
    NB_01["B-01<br/>getWatchlistByIds(ids)"]
    NB_02["B-02<br/>getWatchlistReasons (cacheable)"]
    NB_03["B-03<br/>getWatchlistInspectionActions (ca…"]
  end
  subgraph PHC["🔍 Phase C — Search & Listing"]
    NC_01["C-01<br/>getWatchlistByFilter(...) (4-step…"]
  end
  subgraph PHD["✏️ Phase D — Mutations"]
    ND_01["D-01<br/>createWatchlistEntries"]
    ND_02["D-02<br/>cloneFilesForWatchlist"]
  end
  subgraph PHE["⚙️ Phase E — Complex Operations"]
    NE_01["E-01<br/>updateWatchlistEntries (multi-ste…"]
  end
  subgraph PHF["🔗 Phase F — Federation & Stitching"]
    NF_01["F-01<br/>Product.watchlists (internal)"]
    NF_02["F-02<br/>ResourcesCount.watchlists (intern…"]
  end
  subgraph PHG["🧪 Phase G — Field Resolvers & Tests"]
    NG_01["G-01<br/>Computed flatteners (status/reaso…"]
    NG_02["G-02<br/>createdBy + updatedBy + workspace…"]
    NG_03["G-03<br/>attachments + product"]
    NG_05["G-05<br/>WatchlistPartner.partner entity r…"]
  end
  NB_01 --> NB_02
  NB_01 --> NB_03
  NB_01 --> NC_01
  NB_01 --> ND_01
  NB_01 --> ND_02
  NB_01 --> NE_01
  NB_01 --> NF_01
  NB_01 --> NF_02
  NB_01 --> NG_01
  NB_01 --> NG_02
  NB_01 --> NG_03
  NG_02 --> NG_05
  G__SPIKE_01{{"🔬 SPIKE-01"}}
  G__SPIKE_01 -.-> NE_01
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_{{"⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)"}}
  G__BLOCKED_BY_product__PRODUCT_BE_E_00__the_shared_WriteSaga_module_ -.-> NE_01
```

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

### WATCHLIST-FE-001 · Migrate watchlist reads

```mermaid
flowchart LR
  NB_01["B-01<br/>getWatchlistByIds(ids)"]
  NC_01["C-01<br/>getWatchlistByFilter(...) (…"]
  NG_01["G-01<br/>Computed flatteners (status…"]
  NG_02["G-02<br/>createdBy + updatedBy + wor…"]
  NG_03["G-03<br/>attachments + product"]
  NG_05["G-05<br/>WatchlistPartner.partner en…"]
  NWATCHLIST_FE_001(["WATCHLIST-FE-001"])
  NB_01 ==> NWATCHLIST_FE_001
  NC_01 ==> NWATCHLIST_FE_001
  NG_01 ==> NWATCHLIST_FE_001
  NG_02 ==> NWATCHLIST_FE_001
  NG_03 ==> NWATCHLIST_FE_001
  NG_05 ==> NWATCHLIST_FE_001
```

### WATCHLIST-FE-002 · Migrate watchlist create and clone mutations

```mermaid
flowchart LR
  ND_01["D-01<br/>createWatchlistEntries"]
  ND_02["D-02<br/>cloneFilesForWatchlist"]
  NWATCHLIST_FE_002(["WATCHLIST-FE-002"])
  ND_01 ==> NWATCHLIST_FE_002
  ND_02 ==> NWATCHLIST_FE_002
```

### WATCHLIST-FE-003 · Migrate `updateWatchlistEntries` saga handling

```mermaid
flowchart LR
  NE_01["E-01<br/>updateWatchlistEntries (mul…"]
  NWATCHLIST_FE_003(["WATCHLIST-FE-003"])
  NE_01 ==> NWATCHLIST_FE_003
```

---
*Story dependency graphs · watchlist · generated 2026-07-21.*