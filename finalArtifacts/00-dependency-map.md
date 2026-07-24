# Linear Dependency Map — Backend + Frontend, one row per story

> 🏷️ **Tags:** `dgs-migration` · `dependency-map` — **Generated:** 2026-07-24 by `generate_linear_deps.py` (runs inside `generate_all.py`). A compact companion to [00-sequencing.md](00-sequencing.md): the same steps and edges, rendered as a single left→right dependency chain per story instead of wide Depends/Blocks columns. Full story text lives in each domain's `be-04-stories.md`; nothing here is re-derived — the steps and edges come from the same engine that builds the sequencing doc.

**How to read a row**

- **Step** — build step within the domain; everything in the same step is parallelizable.
- **Story** — 🔴🟠🟡🟢 backend complexity / FE impact icon + id. Bare ids (`B-01`) are this domain; full ids (`PRODUCT-BE-E-00`) are another domain.
- **Depends chain** — read left→right; each id before **this story** must ship first. `A ▸ B ▸ **C**` means A then B then C. `— (module scaffold)` = the domain's init story, which everything else implicitly waits on.
- **Gate** — 🔬 `SPIKE-n` (decision must be ratified first) or ⛔ `ID` (blocked by a story in another domain/subgraph). A gate is an *entry criterion*, not a build-order edge.
- **Unlocks** — the immediate downstream stories that become startable once this ships (walk the graph forward without needing a second table).

Cross-domain gates (the ⛔ rows) are listed in full in [cross-domain-dependencies.md](../analysis/program/cross-domain-dependencies.md).

---

## Watchlist

> **13 BE + 3 FE stories.** Wave 1 pilot — smallest isolated surface; proves flag flip + rollback  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 2 | 🟢 `B-02` | B-01 ▸ **B-02** | — | — |
| 2 | 🟢 `B-03` | B-01 ▸ **B-03** | — | — |
| 2 | 🟡 `C-01` | B-01 ▸ **C-01** | — | WATCHLIST-FE-001 |
| 2 | 🟡 `D-01` | B-01 ▸ **D-01** | — | WATCHLIST-FE-002 |
| 2 | 🟡 `D-02` | B-01 ▸ **D-02** | — | WATCHLIST-FE-002 |
| 2 | 🟠 `E-01` | B-01 ▸ **E-01** | 🔬 SPIKE-01 · ⛔ PRODUCT-BE-E-00 | WATCHLIST-FE-003 |
| 2 | 🟢 `F-01` | B-01 ▸ **F-01** | — | — |
| 2 | 🟢 `F-02` | B-01 ▸ **F-02** | — | — |
| 2 | 🟢 `G-01` | B-01 ▸ **G-01** | — | WATCHLIST-FE-001 |
| 2 | 🟡 `G-02` | B-01 ▸ **G-02** | — | G-05, WATCHLIST-FE-001 |
| 2 | 🟡 `G-03` | B-01 ▸ **G-03** | — | WATCHLIST-FE-001 |
| 3 | 🟢 `G-05` | G-02 ▸ **G-05** | — | WATCHLIST-FE-001 |
| 3 | 🟢 `WATCHLIST-FE-002` | D-01 ▸ D-02 ▸ **WATCHLIST-FE-002** | — | — |
| 4 | 🟢 `WATCHLIST-FE-001` | B-01 ▸ C-01 ▸ G-01 ▸ G-02 ▸ G-03 ▸ G-05 ▸ **WATCHLIST-FE-001** | — | — |
| 4 | 🟡 `WATCHLIST-FE-003` | E-01 ▸ **WATCHLIST-FE-003** | — | — |

**Backend critical path:** `B-01` ▸ `G-02` ▸ `G-05`.
**Frontend cutover flow:** `WATCHLIST-FE-002` ▸ `WATCHLIST-FE-001` ▸ `WATCHLIST-FE-003`.

---

## Product

> **69 BE + 13 FE stories.** Largest surface + host DGS — pulled up (feeds impression/BOM FE); writes last  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 2 | 🟢 `B-02` | **B-02** | — | PRODUCT-FE-002, PRODUCT-FE-004 |
| 2 | 🟢 `B-03` | **B-03** | — | PRODUCT-FE-003, PRODUCT-FE-004, PRODUCT-FE-005 |
| 2 | 🟢 `B-04` | **B-04** | — | PRODUCT-FE-001 |
| 2 | 🟢 `B-05` | **B-05** | — | — |
| 2 | 🟢 `B-06` | **B-06** | — | — |
| 2 | 🟢 `B-07` | **B-07** | — | PRODUCT-FE-007 |
| 2 | 🟢 `B-08` | **B-08** | — | PRODUCT-FE-007 |
| 2 | 🟢 `B-09` | **B-09** | — | PRODUCT-FE-007 |
| 2 | 🟢 `B-10` | **B-10** | 🔬 SPIKE-07 | PRODUCT-FE-007 |
| 2 | 🟢 `B-11` | **B-11** | 🔬 SPIKE-07 | PRODUCT-FE-007 |
| 2 | 🟠 `C-01` | **C-01** | 🔬 SPIKE-06a | — |
| 2 | 🟡 `C-02` | **C-02** | — | PRODUCT-FE-005 |
| 2 | 🟡 `C-03` | **C-03** | — | PRODUCT-FE-005 |
| 2 | 🟡 `C-04` | **C-04** | — | — |
| 2 | 🟡 `C-05` | **C-05** | 🔬 SPIKE-07 | PRODUCT-FE-007 |
| 2 | 🟡 `D-01` | **D-01** | 🔬 SPIKE-06b | PRODUCT-FE-008 |
| 2 | 🟡 `D-02` | **D-02** | 🔬 SPIKE-06b | PRODUCT-FE-008 |
| 2 | 🟡 `D-03` | **D-03** | — | PRODUCT-FE-008 |
| 2 | 🟡 `D-04` | **D-04** | 🔬 SPIKE-06b | PRODUCT-FE-008 |
| 2 | 🟡 `D-05` | **D-05** | — | PRODUCT-FE-008 |
| 2 | 🟢 `D-06` | **D-06** | — | PRODUCT-FE-009 |
| 2 | 🟢 `D-07` | **D-07** | — | PRODUCT-FE-009 |
| 2 | 🟢 `D-08` | **D-08** | — | — |
| 2 | 🟢 `D-09` | **D-09** | — | PRODUCT-FE-010 |
| 2 | 🟢 `D-10` | **D-10** | — | PRODUCT-FE-008 |
| 2 | 🟢 `D-11` | **D-11** | — | — |
| 2 | 🟢 `D-12` | **D-12** | — | PRODUCT-FE-009 |
| 2 | 🟢 `D-13` | **D-13** | — | PRODUCT-FE-008 |
| 2 | 🟢 `D-14` | **D-14** | — | PRODUCT-FE-008 |
| 2 | 🟢 `D-15` | **D-15** | — | PRODUCT-FE-007 |
| 2 | 🟢 `D-16` | **D-16** | — | PRODUCT-FE-007 |
| 2 | 🟢 `D-17` | **D-17** | — | PRODUCT-FE-007 |
| 2 | 🟢 `D-18` | **D-18** | — | PRODUCT-FE-012 |
| 2 | 🟠 `E-00` | **E-00** | 🔬 SPIKE-01 | E-01, E-02 |
| 2 | 🔴 `E-03` | **E-03** | 🔬 SPIKE-02 | E-04, F-04, F-06, F-08, H-01 … |
| 2 | 🟢 `F-14` | **F-14** | — | F-10, PRODUCT-FE-013 |
| 2 | 🔴 `G-01` | **G-01** | — | G-03, G-17, PRODUCT-FE-001 |
| 2 | 🔴 `G-02` | **G-02** | — | PRODUCT-FE-001 |
| 2 | 🟡 `G-04` | **G-04** | — | PRODUCT-FE-005 |
| 2 | 🟡 `G-05` | **G-05** | — | — |
| 2 | 🟡 `G-06` | **G-06** | — | PRODUCT-FE-001, PRODUCT-FE-004, PRODUCT-FE-005 |
| 2 | 🟡 `G-07` | **G-07** | 🔬 SPIKE-04 | PRODUCT-FE-001, PRODUCT-FE-004, PRODUCT-FE-005, PRODUCT-FE-007 |
| 2 | 🟡 `G-08` | **G-08** | — | PRODUCT-FE-001, PRODUCT-FE-005, PRODUCT-FE-011 |
| 2 | 🟡 `G-09` | **G-09** | — | PRODUCT-FE-001, PRODUCT-FE-004 |
| 2 | 🟡 `G-10` | **G-10** | — | PRODUCT-FE-001 |
| 2 | 🟡 `G-11-1` | **G-11-1** | 🔬 SPIKE-04 | — |
| 2 | 🟡 `G-11-2` | **G-11-2** | — | — |
| 2 | 🟡 `G-13` | **G-13** | — | PRODUCT-FE-001, PRODUCT-FE-002, PRODUCT-FE-004, PRODUCT-FE-005, PRODUCT-FE-006 … |
| 2 | 🟢 `G-14` | **G-14** | — | PRODUCT-FE-001, PRODUCT-FE-005 |
| 2 | 🟡 `G-15` | **G-15** | — | — |
| 2 | 🟡 `H-06` | B-01 ▸ **H-06** | — | F-10 |
| 3 | 🔴 `E-01` | E-00 ▸ **E-01** | 🔬 SPIKE-03 | F-12 |
| 3 | 🟠 `E-02` | E-00 ▸ **E-02** | 🔬 SPIKE-01 | PRODUCT-FE-012 |
| 3 | 🔴 `E-04` | E-03 ▸ **E-04** | 🔬 SPIKE-02 | PRODUCT-FE-011 |
| 3 | 🟢 `F-04` | E-03 ▸ **F-04** | — | F-09 |
| 3 | 🟢 `F-06` | E-03 ▸ **F-06** | — | F-09, PRODUCT-FE-011 |
| 3 | 🟢 `F-08` | E-03 ▸ **F-08** | — | F-09, PRODUCT-FE-011 |
| 3 | 🟢 `F-10` | F-14 ▸ H-06 ▸ **F-10** | — | F-11, PRODUCT-FE-001, PRODUCT-FE-004 |
| 3 | 🟠 `G-03` | G-01 ▸ **G-03** | — | PRODUCT-FE-001, PRODUCT-FE-005, PRODUCT-FE-006 |
| 3 | 🟡 `G-17` | G-01 ▸ **G-17** | — | — |
| 3 | 🟡 `H-01` | E-03 ▸ **H-01** | ⛔ BLOCKED-BY attachment domain | F-09, PRODUCT-FE-011 |
| 3 | 🟡 `H-02` | E-03 ▸ **H-02** | ⛔ BLOCKED-BY discussion domain | F-09, PRODUCT-FE-011 |
| 3 | 🟡 `H-03` | E-03 ▸ **H-03** | ⛔ BLOCKED-BY sample domain | F-09, PRODUCT-FE-011 |
| 3 | 🟡 `H-04` | E-03 ▸ **H-04** | ⛔ BLOCKED-BY claim domain | F-09, PRODUCT-FE-011 |
| 3 | 🟡 `H-05` | E-03 ▸ **H-05** | ⛔ BLOCKED-BY construction domain | F-09, PRODUCT-FE-011 |
| 3 | 🟡 `PRODUCT-FE-003` | B-03 ▸ **PRODUCT-FE-003** | — | — |
| 4 | 🟢 `F-09` | F-04 ▸ F-06 ▸ F-08 ▸ H-01 ▸ H-02 ▸ H-03 ▸ H-04 ▸ H-05 ▸ **F-09** | — | — |
| 4 | 🟢 `F-11` | F-10 ▸ **F-11** | — | — |
| 4 | 🟢 `F-12` | E-01 ▸ **F-12** | — | — |
| 4 | 🟡 `PRODUCT-FE-008` | D-01 ▸ D-02 ▸ D-03 ▸ D-04 ▸ D-05 ▸ D-10 ▸ D-13 ▸ D-14 ▸ **PRODUCT-FE-008** | — | — |
| 5 | 🟢 `PRODUCT-FE-006` | G-03 ▸ G-13 ▸ **PRODUCT-FE-006** | — | — |
| 5 | 🟡 `PRODUCT-FE-007` | B-07 ▸ B-08 ▸ B-09 ▸ B-10 ▸ B-11 ▸ C-05 ▸ D-15 ▸ D-16 ▸ D-17 ▸ G-07 ▸ G-13 ▸ **PRODUCT-FE-007** | — | — |
| 5 | 🟡 `PRODUCT-FE-011` | E-03 ▸ E-04 ▸ F-06 ▸ F-08 ▸ G-08 ▸ H-01 ▸ H-02 ▸ H-03 ▸ H-04 ▸ H-05 ▸ **PRODUCT-FE-011** | — | — |
| 5 | 🟡 `PRODUCT-FE-013` | F-14 ▸ **PRODUCT-FE-013** | — | — |
| 6 | 🔴 `PRODUCT-FE-001` | B-01 ▸ B-04 ▸ F-10 ▸ G-01 ▸ G-02 ▸ G-03 ▸ G-06 ▸ G-07 ▸ G-08 ▸ G-09 ▸ G-10 ▸ G-13 ▸ G-14 ▸ **PRODUCT-FE-001** | — | — |
| 6 | 🔴 `PRODUCT-FE-002` | B-02 ▸ G-13 ▸ **PRODUCT-FE-002** | — | — |
| 6 | 🟡 `PRODUCT-FE-004` | B-01 ▸ B-02 ▸ B-03 ▸ F-10 ▸ G-06 ▸ G-07 ▸ G-09 ▸ G-13 ▸ **PRODUCT-FE-004** | — | — |
| 6 | 🟡 `PRODUCT-FE-005` | B-03 ▸ C-02 ▸ C-03 ▸ G-03 ▸ G-04 ▸ G-06 ▸ G-07 ▸ G-08 ▸ G-13 ▸ G-14 ▸ **PRODUCT-FE-005** | — | — |
| 6 | 🔴 `PRODUCT-FE-010` | D-09 ▸ **PRODUCT-FE-010** | — | — |
| 7 | 🟡 `PRODUCT-FE-009` | D-06 ▸ D-07 ▸ D-12 ▸ PRODUCT-FE-001 ▸ **PRODUCT-FE-009** | — | — |
| 7 | 🟡 `PRODUCT-FE-012` | D-18 ▸ E-02 ▸ PRODUCT-FE-001 ▸ **PRODUCT-FE-012** | — | — |

**Backend critical path:** `B-01` ▸ `E-03` ▸ `F-04` ▸ `F-09`.
**Frontend cutover flow:** `PRODUCT-FE-003` ▸ `PRODUCT-FE-008` ▸ `PRODUCT-FE-006` ▸ `PRODUCT-FE-007` ▸ `PRODUCT-FE-011` ▸ `PRODUCT-FE-013` ▸ `PRODUCT-FE-001` ▸ `PRODUCT-FE-002` ▸ `PRODUCT-FE-004` ▸ `PRODUCT-FE-005` ▸ `PRODUCT-FE-010` ▸ `PRODUCT-FE-009` ▸ `PRODUCT-FE-012`.

---

## BOM

> **37 BE + 7 FE stories.** High complexity, search-gated list views — pulled up to feed impression FE  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 1 | 🔴 `BOM-FE-001` | **BOM-FE-001** | — | — |
| 2 | 🟡 `A-04` | **A-04** | 🔬 SPIKE-05 | A-05, BOM-FE-002, BOM-FE-007 |
| 2 | 🟢 `B-03` | **B-03** | — | BOM-FE-002, BOM-FE-007 |
| 2 | 🟢 `B-04` | **B-04** | — | BOM-FE-002, BOM-FE-007 |
| 2 | 🟡 `B-05` | **B-05** | 🔬 SPIKE-06a | BOM-FE-004 |
| 2 | 🟢 `B-06` | **B-06** | — | BOM-FE-004 |
| 2 | 🟢 `B-07` | **B-07** | — | BOM-FE-004 |
| 2 | 🟢 `B-08` | **B-08** | — | BOM-FE-004 |
| 2 | 🟢 `C-01` | **C-01** | — | BOM-FE-003 |
| 2 | 🟡 `C-02` | **C-02** | — | G-15 |
| 2 | 🟡 `C-03` | **C-03** | — | BOM-FE-005 |
| 2 | 🟢 `C-04` | **C-04** | — | BOM-FE-005 |
| 2 | 🟢 `C-05` | **C-05** | — | BOM-FE-005 |
| 2 | 🟡 `D-01` | **D-01** | — | BOM-FE-006 |
| 2 | 🟢 `D-02` | **D-02** | — | E-01 |
| 2 | 🟢 `D-03` | **D-03** | — | BOM-FE-006 |
| 2 | 🟢 `D-04` | **D-04** | — | BOM-FE-006 |
| 2 | 🟢 `D-05` | **D-05** | — | BOM-FE-006 |
| 2 | 🟡 `F-01` | **F-01** | — | — |
| 2 | 🟢 `F-02` | **F-02** | — | — |
| 2 | 🟡 `G-01` | **G-01** | — | G-17, BOM-FE-002, BOM-FE-003, BOM-FE-007 |
| 2 | 🟡 `G-03` | **G-03** | — | BOM-FE-002, BOM-FE-007 |
| 2 | 🟢 `G-04` | **G-04** | — | — |
| 2 | 🟢 `G-05` | **G-05** | — | — |
| 2 | 🟢 `G-06` | **G-06** | — | — |
| 2 | 🟢 `G-07` | **G-07** | — | — |
| 2 | 🟠 `G-08` | **G-08** | — | BOM-FE-002, BOM-FE-007 |
| 2 | 🟢 `G-09` | **G-09** | — | — |
| 2 | 🟠 `G-10` | **G-10** | — | G-11, G-12, G-13 |
| 2 | 🟢 `G-14` | **G-14** | — | BOM-FE-003, BOM-FE-004, BOM-FE-007 |
| 3 | 🟡 `A-05` | A-04 ▸ **A-05** | — | — |
| 3 | 🔴 `E-01` | D-02 ▸ **E-01** | 🔬 SPIKE-01 · ⛔ PRODUCT-BE-E-00 | — |
| 3 | 🟡 `G-11` | G-10 ▸ **G-11** | — | — |
| 3 | 🟡 `G-12` | G-10 ▸ **G-12** | — | BOM-FE-002, BOM-FE-007 |
| 3 | 🟢 `G-13` | G-10 ▸ **G-13** | — | BOM-FE-002, BOM-FE-007 |
| 3 | 🟡 `G-15` | C-02 ▸ **G-15** | — | — |
| 3 | 🟡 `G-17` | G-01 ▸ **G-17** | — | BOM-FE-002, BOM-FE-007 |
| 3 | 🟡 `BOM-FE-005` | C-03 ▸ C-04 ▸ C-05 ▸ **BOM-FE-005** | — | — |
| 4 | 🔴 `BOM-FE-002` | A-04 ▸ B-01 ▸ B-03 ▸ B-04 ▸ G-01 ▸ G-03 ▸ G-08 ▸ G-12 ▸ G-13 ▸ G-17 ▸ BOM-FE-001 ▸ **BOM-FE-002** | — | — |
| 4 | 🟢 `BOM-FE-004` | B-05 ▸ B-06 ▸ B-07 ▸ B-08 ▸ G-14 ▸ **BOM-FE-004** | — | — |
| 5 | 🔴 `BOM-FE-003` | C-01 ▸ G-01 ▸ G-14 ▸ **BOM-FE-003** | — | — |
| 5 | 🔴 `BOM-FE-006` | D-01 ▸ D-03 ▸ D-04 ▸ D-05 ▸ **BOM-FE-006** | — | — |
| 5 | 🟢 `BOM-FE-007` | A-04 ▸ B-01 ▸ B-03 ▸ B-04 ▸ G-01 ▸ G-03 ▸ G-08 ▸ G-12 ▸ G-13 ▸ G-14 ▸ G-17 ▸ BOM-FE-002 ▸ **BOM-FE-007** | — | — |

**Backend critical path:** `B-01` ▸ `A-04` ▸ `A-05`.
**Frontend cutover flow:** `BOM-FE-001` ▸ `BOM-FE-005` ▸ `BOM-FE-002` ▸ `BOM-FE-004` ▸ `BOM-FE-003` ▸ `BOM-FE-006` ▸ `BOM-FE-007`.

---

## Impression

> **7 BE + 2 FE stories.** Prioritized for an external team; FE flips with its BOM / Product partners  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 2 | 🟢 `B-02` | B-01 ▸ **B-02** | — | — |
| 2 | 🟡 `D-01` | B-01 ▸ **D-01** | — | — |
| 2 | 🟢 `F-01` | B-01 ▸ **F-01** | ⛔ PRODUCT-BE-B-01 | — |
| 2 | 🟢 `G-01` | B-01 ▸ **G-01** | — | IMPRESSION-FE-001, IMPRESSION-FE-002 |
| 2 | 🟡 `G-02` | B-01 ▸ **G-02** | — | IMPRESSION-FE-002 |
| 2 | 🟢 `G-04` | B-01 ▸ **G-04** | — | — |
| 3 | 🟢 `IMPRESSION-FE-001` | B-01 ▸ G-01 ▸ BOM-FE-002 ▸ **IMPRESSION-FE-001** | — | — |
| 4 | 🟢 `IMPRESSION-FE-002` | B-01 ▸ G-01 ▸ G-02 ▸ PRODUCT-FE-001 ▸ **IMPRESSION-FE-002** | — | — |

**Backend critical path:** `B-01` ▸ `B-02`.
**Frontend cutover flow:** `IMPRESSION-FE-001` ▸ `IMPRESSION-FE-002`.

---

## Product Details

> **12 BE + 3 FE stories.** Small, isolated, no shared blockers  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 2 | 🟡 `C-01` | B-01 ▸ **C-01** | — | — |
| 2 | 🟡 `D-01` | B-01 ▸ **D-01** | — | PDTL-FE-002 |
| 2 | 🟢 `D-02` | B-01 ▸ **D-02** | — | — |
| 2 | 🟢 `D-03` | B-01 ▸ **D-03** | — | PDTL-FE-002 |
| 2 | 🟡 `D-04` | B-01 ▸ **D-04** | — | PDTL-FE-002 |
| 2 | 🟢 `D-05` | B-01 ▸ **D-05** | — | PDTL-FE-002 |
| 2 | 🟠 `E-01` | B-01 ▸ **E-01** | 🔬 SPIKE-01 · ⛔ PRODUCT-BE-E-00 | PDTL-FE-003 |
| 2 | 🟢 `F-01` | B-01 ▸ **F-01** | — | — |
| 2 | 🟡 `G-01` | B-01 ▸ **G-01** | — | PDTL-FE-001 |
| 2 | 🟡 `G-02` | B-01 ▸ **G-02** | — | PDTL-FE-001 |
| 2 | 🟡 `G-03` | B-01 ▸ **G-03** | — | PDTL-FE-001 |
| 3 | 🟡 `PDTL-FE-002` | D-01 ▸ D-03 ▸ D-04 ▸ D-05 ▸ **PDTL-FE-002** | — | — |
| 4 | 🟢 `PDTL-FE-001` | B-01 ▸ G-01 ▸ G-02 ▸ G-03 ▸ **PDTL-FE-001** | — | — |
| 4 | 🟡 `PDTL-FE-003` | E-01 ▸ **PDTL-FE-003** | — | — |

**Backend critical path:** `B-01` ▸ `C-01`.
**Frontend cutover flow:** `PDTL-FE-002` ▸ `PDTL-FE-001` ▸ `PDTL-FE-003`.

---

## Measurement

> **30 BE + 4 FE stories.** Parallel with the other small domains  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 2 | 🟢 `B-02` | B-01 ▸ **B-02** | — | H-02, MST-FE-003 |
| 2 | 🟢 `B-03` | B-01 ▸ **B-03** | — | MST-FE-003 |
| 2 | 🟢 `B-04` | B-01 ▸ **B-04** | — | MST-FE-001, MST-FE-003 |
| 2 | 🟢 `B-05` | B-01 ▸ **B-05** | — | H-02 |
| 2 | 🟢 `B-06` | **B-06** | — | D-08, G-01, G-05 |
| 2 | 🟢 `B-07` | **B-07** | — | D-09, G-01, G-06 |
| 2 | 🟢 `B-08` | **B-08** | — | D-10, G-01, G-07 |
| 2 | 🟢 `B-09` | **B-09** | — | — |
| 2 | 🟡 `C-01` | B-01 ▸ **C-01** | — | MST-FE-002 |
| 2 | 🟢 `C-02` | B-01 ▸ **C-02** | — | MST-FE-002 |
| 2 | 🟡 `D-01` | B-01 ▸ **D-01** | — | — |
| 2 | 🟢 `D-02` | B-01 ▸ **D-02** | — | — |
| 2 | 🟢 `D-03` | B-01 ▸ **D-03** | — | MST-FE-004 |
| 2 | 🟢 `D-04` | B-01 ▸ **D-04** | — | MST-FE-004 |
| 2 | 🟢 `D-05` | B-01 ▸ **D-05** | — | — |
| 2 | 🟡 `D-06` | B-01 ▸ **D-06** | — | MST-FE-004 |
| 2 | 🟢 `D-07` | B-01 ▸ **D-07** | — | MST-FE-004 |
| 2 | 🟠 `E-01` | B-01 ▸ **E-01** | 🔬 SPIKE-01 · ⛔ PRODUCT-BE-E-00 | — |
| 2 | 🟡 `F-01` | B-01 ▸ **F-01** | — | — |
| 2 | 🟢 `G-02` | B-01 ▸ **G-02** | — | — |
| 2 | 🟢 `H-01` | B-01 ▸ **H-01** | ⛔ BLOCKED-BY sample | — |
| 3 | 🟢 `D-08` | B-06 ▸ **D-08** | — | — |
| 3 | 🟢 `D-09` | B-07 ▸ **D-09** | — | — |
| 3 | 🟢 `D-10` | B-08 ▸ **D-10** | — | — |
| 3 | 🟡 `G-01` | B-01 ▸ B-06 ▸ B-07 ▸ B-08 ▸ **G-01** | — | MST-FE-001, MST-FE-002 |
| 3 | 🟢 `G-05` | B-06 ▸ **G-05** | — | — |
| 3 | 🟢 `G-06` | B-07 ▸ **G-06** | — | — |
| 3 | 🟢 `G-07` | B-08 ▸ **G-07** | — | MST-FE-001, MST-FE-002 |
| 3 | 🟢 `H-02` | B-02 ▸ B-05 ▸ **H-02** | ⛔ BLOCKED-BY sample | — |
| 3 | 🟢 `MST-FE-003` | B-02 ▸ B-03 ▸ B-04 ▸ **MST-FE-003** | — | — |
| 4 | 🟡 `MST-FE-004` | D-03 ▸ D-04 ▸ D-06 ▸ D-07 ▸ **MST-FE-004** | — | — |
| 5 | 🟡 `MST-FE-001` | B-01 ▸ B-04 ▸ G-01 ▸ G-07 ▸ **MST-FE-001** | — | — |
| 5 | 🟡 `MST-FE-002` | B-01 ▸ C-01 ▸ C-02 ▸ G-01 ▸ G-07 ▸ **MST-FE-002** | — | — |

**Backend critical path:** `B-01` ▸ `B-06` ▸ `D-08`.
**Frontend cutover flow:** `MST-FE-003` ▸ `MST-FE-004` ▸ `MST-FE-001` ▸ `MST-FE-002`.

---

## Packaging

> **23 BE + 5 FE stories.** Parallel with the other small domains  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 2 | 🟢 `B-02` | B-01 ▸ **B-02** | — | PKG-FE-001 |
| 2 | 🟢 `B-03` | B-01 ▸ **B-03** | — | PKG-FE-003 |
| 2 | 🟢 `B-04` | B-01 ▸ **B-04** | — | PKG-FE-002 |
| 2 | 🟢 `B-05` | B-01 ▸ **B-05** | — | PKG-FE-003 |
| 2 | 🟢 `B-06` | B-01 ▸ **B-06** | — | PKG-FE-002 |
| 2 | 🟡 `C-01` | B-01 ▸ **C-01** | — | — |
| 2 | 🟡 `D-01` | B-01 ▸ **D-01** | — | PKG-FE-004 |
| 2 | 🟢 `D-02` | B-01 ▸ **D-02** | — | PKG-FE-003 |
| 2 | 🟡 `D-03` | B-01 ▸ **D-03** | — | PKG-FE-004 |
| 2 | 🟡 `D-04` | B-01 ▸ **D-04** | — | PKG-FE-004 |
| 2 | 🟢 `D-05` | B-01 ▸ **D-05** | — | PKG-FE-004 |
| 2 | 🟢 `D-06` | B-01 ▸ **D-06** | — | PKG-FE-004 |
| 2 | 🟢 `D-07` | B-01 ▸ **D-07** | — | PKG-FE-004 |
| 2 | 🟡 `D-08` | B-01 ▸ **D-08** | — | — |
| 2 | 🟢 `D-09` | B-01 ▸ **D-09** | — | PKG-FE-004 |
| 2 | 🟠 `E-01` | B-01 ▸ **E-01** | 🔬 SPIKE-01 · ⛔ PRODUCT-BE-E-00 | PKG-FE-005 |
| 2 | 🟢 `F-01` | B-01 ▸ **F-01** | — | — |
| 2 | 🟡 `G-01` | B-01 ▸ **G-01** | — | PKG-FE-001 |
| 2 | 🟢 `G-02` | B-01 ▸ **G-02** | — | PKG-FE-001 |
| 2 | 🟡 `G-03` | B-01 ▸ **G-03** | — | — |
| 2 | 🟠 `G-04` | B-01 ▸ **G-04** | — | PKG-FE-001 |
| 2 | 🟡 `G-05` | B-01 ▸ **G-05** | — | PKG-FE-003 |
| 3 | 🟢 `PKG-FE-002` | B-04 ▸ B-06 ▸ **PKG-FE-002** | — | — |
| 4 | 🟡 `PKG-FE-004` | D-01 ▸ D-03 ▸ D-04 ▸ D-05 ▸ D-06 ▸ D-07 ▸ D-09 ▸ **PKG-FE-004** | — | — |
| 5 | 🟡 `PKG-FE-001` | B-01 ▸ B-02 ▸ G-01 ▸ G-02 ▸ G-04 ▸ **PKG-FE-001** | — | — |
| 5 | 🟡 `PKG-FE-003` | B-03 ▸ B-05 ▸ D-02 ▸ G-05 ▸ **PKG-FE-003** | — | — |
| 5 | 🔴 `PKG-FE-005` | E-01 ▸ **PKG-FE-005** | — | — |

**Backend critical path:** `B-01` ▸ `B-02`.
**Frontend cutover flow:** `PKG-FE-002` ▸ `PKG-FE-004` ▸ `PKG-FE-001` ▸ `PKG-FE-003` ▸ `PKG-FE-005`.

---

## Claims

> **20 BE + 4 FE stories.** First cross-subgraph cutover (`spark-claims`)  Rows are in build order. **Depends chain** reads left→right — the ids before **this story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = the stories that become startable once this one ships.

| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |
|---|---|---|---|---|
| 1 | 🟢 `B-01` | — (module scaffold) | — | all stories (scaffold) |
| 1 | 🟡 `CLAIM-FE-001` | **CLAIM-FE-001** | — | — |
| 2 | 🟢 `B-02` | B-01 ▸ **B-02** | — | CLAIM-FE-002 |
| 2 | 🟢 `B-03` | B-01 ▸ **B-03** | — | CLAIM-FE-002 |
| 2 | 🟢 `B-04` | B-01 ▸ **B-04** | — | CLAIM-FE-002 |
| 2 | 🟢 `B-05` | B-01 ▸ **B-05** | — | — |
| 2 | 🟡 `C-01` | B-01 ▸ **C-01** | — | — |
| 2 | 🟡 `C-02` | B-01 ▸ **C-02** | — | — |
| 2 | 🟡 `D-01` | B-01 ▸ **D-01** | — | CLAIM-FE-003 |
| 2 | 🟡 `D-02` | B-01 ▸ **D-02** | — | CLAIM-FE-003 |
| 2 | 🟢 `D-03` | B-01 ▸ **D-03** | — | CLAIM-FE-003 |
| 2 | 🟢 `D-04` | B-01 ▸ **D-04** | — | CLAIM-FE-003 |
| 2 | 🟢 `D-05` | B-01 ▸ **D-05** | — | CLAIM-FE-003 |
| 2 | 🟠 `E-01` | B-01 ▸ **E-01** | 🔬 SPIKE-01 · ⛔ PRODUCT-BE-E-00 | CLAIM-FE-004 |
| 2 | 🟡 `G-01` | B-01 ▸ **G-01** | — | CLAIM-FE-002 |
| 2 | 🟡 `G-02` | B-01 ▸ **G-02** | — | CLAIM-FE-002 |
| 2 | 🟡 `G-04` | B-01 ▸ **G-04** | — | — |
| 2 | 🟢 `G-06` | B-01 ▸ **G-06** | — | G-03 |
| 2 | 🟡 `H-01` | B-01 ▸ **H-01** | ⛔ PRODUCT-BE-F-14 | — |
| 2 | 🟢 `H-02` | B-01 ▸ **H-02** | ⛔ PRODUCT-BE-E-03 | — |
| 3 | 🟠 `G-03` | B-01 ▸ G-06 ▸ **G-03** | — | CLAIM-FE-002 |
| 3 | 🟡 `CLAIM-FE-003` | D-01 ▸ D-02 ▸ D-03 ▸ D-04 ▸ D-05 ▸ **CLAIM-FE-003** | — | — |
| 4 | 🔴 `CLAIM-FE-002` | B-01 ▸ B-02 ▸ B-03 ▸ B-04 ▸ G-01 ▸ G-02 ▸ G-03 ▸ CLAIM-FE-001 ▸ **CLAIM-FE-002** | — | — |
| 4 | 🔴 `CLAIM-FE-004` | E-01 ▸ **CLAIM-FE-004** | — | — |

**Backend critical path:** `B-01` ▸ `G-06` ▸ `G-03`.
**Frontend cutover flow:** `CLAIM-FE-001` ▸ `CLAIM-FE-003` ▸ `CLAIM-FE-002` ▸ `CLAIM-FE-004`.

---

*Linear dependency map · generated 2026-07-24 by generate_linear_deps.py.*