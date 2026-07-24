# Watchlist — Frontend Readiness

> Generated 2026-07-24 from `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [watchlist/be-04-stories.md](../../../output/analysis/watchlist/be-04-stories.md). Backend build-order sequencing: [00-sequencing.md](../../00-sequencing.md).

---

## What must ship before FE can start

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. A frontend story cannot start until every backend story pointing at it has shipped.

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
*Story dependency graph · watchlist · generated 2026-07-24.*