# Watchlist — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [watchlist/be-04-stories.md](../../../output/analysis/watchlist/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

One box per **phase** (reads, search, mutations, complex ops, federation, field resolvers, entity resolution) — not one box per story, which stops being readable past a couple dozen stories. An arrow between two phase boxes means at least one story in the target phase directly depends on a story in the source phase; the label is how many story-level dependencies that represents. 🔬/⛔ on a box means at least one story in that phase is spike- or cross-subgraph-gated — see the table below for exactly which one.

```mermaid
flowchart TD
  PHB["📖 Phase B<br/>Core Reads<br/>(3 stories)"]
  PHC["🔍 Phase C<br/>Search & Listing<br/>(1 story)"]
  PHD["✏️ Phase D<br/>Mutations<br/>(2 stories)"]
  PHE["⚙️ Phase E<br/>Complex Operations<br/>(1 story) 🔬 ⛔"]
  PHF["🔗 Phase F<br/>Federation & Stitching<br/>(2 stories)"]
  PHG["🧪 Phase G<br/>Field Resolvers & Tests<br/>(4 stories)"]
  PHB -->|1 dep| PHC
  PHB -->|2 deps| PHD
  PHB -->|1 dep| PHE
  PHB -->|2 deps| PHF
  PHB -->|3 deps| PHG
```

**Story-level detail** (every story in this domain, its phase, its direct `Depends on:`, and any gate):

| Story | Phase | Depends on | Gate |
|---|---|---|---|
| `B-01` — getWatchlistByIds(ids) | B | — | — |
| `B-02` — getWatchlistReasons (cacheable) | B | `B-01` | — |
| `B-03` — getWatchlistInspectionActions (cacheable) | B | `B-01` | — |
| `C-01` — getWatchlistByFilter(...) (4-step read) | C | `B-01` | — |
| `D-01` — createWatchlistEntries | D | `B-01` | — |
| `D-02` — cloneFilesForWatchlist | D | `B-01` | — |
| `E-01` — updateWatchlistEntries (multi-step write) | E | `B-01` | ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module), 🔬 SPIKE-01 |
| `F-01` — Product.watchlists (internal) | F | `B-01` | — |
| `F-02` — ResourcesCount.watchlists (internal — TechPack) | F | `B-01` | — |
| `G-01` — Computed flatteners (status/reasons/inspection action) | G | `B-01` | — |
| `G-02` — createdBy + updatedBy + workspaces + participantDetails + partnerName | G | `B-01` | — |
| `G-03` — attachments + product | G | `B-01` | — |
| `G-05` — WatchlistPartner.partner entity reference (recommended, PO-gated) | G | `G-02` | — |

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