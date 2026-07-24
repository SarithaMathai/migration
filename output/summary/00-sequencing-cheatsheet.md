# Sequencing Cheat-Sheet — what order to build

> 🏷️ `dgs-migration` · `cheatsheet` — **Generated:** 2026-07-24 by `generate_sequencing_cheatsheet.py` (in `generate_all.py`). The condensed one-pager: **domain order + the order stories are implemented.** For day windows / calendar see [00-domain-rollout.md](00-domain-rollout.md) & [01-implementation-plan-1BE-1FE.md](01-implementation-plan-1BE-1FE.md); for full per-story dependency detail see [00-sequencing.md](00-sequencing.md) / [00-dependency-map.md](00-dependency-map.md).

**How to read it:** domains are listed in cutover order. Within a domain, do the backend steps `BE-1, BE-2, …` top to bottom — **ids in the same step have no dependency on each other and can be done in any order / in parallel;** finish a step before starting the next. `▶` marks when the frontend engineer can start. Then do the frontend stages `FE-1, FE-2, …` in order (reads flip before writes before the multi-step saga). Complexity: 🔴 very high · 🟠 high · 🟡 medium · 🟢 low.

> **⚠ Order reprioritized 2026-07-24** for an external team waiting on `watchlist` + `impression`. Impression's FE is fused with BOM + Product screens, so those move up too. Order is set in `team_config.py`.

---

## Domain order

| # | Domain | Why here | BE | FE |
|---|---|---|---|---|
| 1 | **Watchlist** | Wave 1 pilot — smallest isolated surface; proves flag flip + rollback | 13 | 3 |
| 2 | **Product** | Largest surface + host DGS — pulled up (feeds impression/BOM FE); writes last | 69 | 13 |
| 3 | **BOM** | High complexity, search-gated list views — pulled up to feed impression FE | 37 | 7 |
| 4 | **Impression** | Prioritized for an external team; FE flips with its BOM / Product partners | 7 | 2 |
| 5 | **Product Details** | Small, isolated, no shared blockers | 12 | 3 |
| 6 | **Measurement** | Parallel with the other small domains | 30 | 4 |
| 7 | **Packaging** | Parallel with the other small domains | 23 | 5 |
| 8 | **Claims** | First cross-subgraph cutover (`spark-claims`) | 20 | 4 |

---

## Story order, domain by domain

### 1. Watchlist — 13 BE + 3 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟢 `B-02`, 🟢 `B-03`, 🟡 `C-01`, 🟡 `D-01`, 🟡 `D-02`, 🟠 `E-01`, 🟢 `F-01`, 🟢 `F-02`, 🟢 `G-01`, 🟡 `G-02`, 🟡 `G-03`
- **BE-3.** 🟢 `G-05`

**▶ Frontend starts once backend steps BE-1…BE-3 are done** (9 stories — essentially this domain's reads/writes/field resolvers; the trailing F/G stitches can lag).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `WATCHLIST-FE-002`
- **FE-2.** `WATCHLIST-FE-001`, `WATCHLIST-FE-003`

---

### 2. Product — 69 BE + 13 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `B-09`, 🟢 `B-10`, 🟢 `B-11`, 🟠 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟡 `C-04`, 🟡 `C-05`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟡 `D-05`, 🟢 `D-06`, 🟢 `D-07`, 🟢 `D-08`, 🟢 `D-09`, 🟢 `D-10`, 🟢 `D-11`, 🟢 `D-12`, 🟢 `D-13`, 🟢 `D-14`, 🟢 `D-15`, 🟢 `D-16`, 🟢 `D-17`, 🟢 `D-18`, 🟠 `E-00`, 🔴 `E-03`, 🟢 `F-14`, 🔴 `G-01`, 🔴 `G-02`, 🟡 `G-04`, 🟡 `G-05`, 🟡 `G-06`, 🟡 `G-07`, 🟡 `G-08`, 🟡 `G-09`, 🟡 `G-10`, 🟡 `G-11-1`, 🟡 `G-11-2`, 🟡 `G-13`, 🟢 `G-14`, 🟡 `G-15`, 🟡 `H-06`
- **BE-3.** 🔴 `E-01`, 🟠 `E-02`, 🔴 `E-04`, 🟢 `F-04`, 🟢 `F-06`, 🟢 `F-08`, 🟢 `F-10`, 🟠 `G-03`, 🟡 `G-17`, 🟡 `H-01`, 🟡 `H-02`, 🟡 `H-03`, 🟡 `H-04`, 🟡 `H-05`
- **BE-4.** 🟢 `F-09`, 🟢 `F-11`, 🟢 `F-12`

**▶ Frontend starts once backend steps BE-1…BE-3 are done** (51 stories — essentially this domain's reads/writes/field resolvers; the trailing F/G stitches can lag).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `PRODUCT-FE-003`
- **FE-2.** `PRODUCT-FE-008`
- **FE-3.** `PRODUCT-FE-006`, `PRODUCT-FE-007`, `PRODUCT-FE-011`, `PRODUCT-FE-013`
- **FE-4.** `PRODUCT-FE-001`, `PRODUCT-FE-002`, `PRODUCT-FE-004`, `PRODUCT-FE-005`, `PRODUCT-FE-010`
- **FE-5.** `PRODUCT-FE-009`, `PRODUCT-FE-012`

---

### 3. BOM — 37 BE + 7 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟡 `A-04`, 🟢 `B-03`, 🟢 `B-04`, 🟡 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟢 `C-04`, 🟢 `C-05`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟡 `G-03`, 🟢 `G-04`, 🟢 `G-05`, 🟢 `G-06`, 🟢 `G-07`, 🟠 `G-08`, 🟢 `G-09`, 🟠 `G-10`, 🟢 `G-14`
- **BE-3.** 🟡 `A-05`, 🔴 `E-01`, 🟡 `G-11`, 🟡 `G-12`, 🟢 `G-13`, 🟡 `G-15`, 🟡 `G-17`

**▶ Frontend starts once backend steps BE-1…BE-3 are done** (23 stories — essentially this domain's reads/writes/field resolvers; the trailing F/G stitches can lag).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `BOM-FE-001`
- **FE-2.** `BOM-FE-005`
- **FE-3.** `BOM-FE-002`, `BOM-FE-004`
- **FE-4.** `BOM-FE-003`, `BOM-FE-006`, `BOM-FE-007`

---

### 4. Impression — 7 BE + 2 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟢 `B-02`, 🟡 `D-01`, 🟢 `F-01`, 🟢 `G-01`, 🟡 `G-02`, 🟢 `G-04`

**▶ Frontend starts once these ship:** `B-01`, `G-01`, `G-02` (all within **BE-2**).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `IMPRESSION-FE-001`
- **FE-2.** `IMPRESSION-FE-002`

---

### 5. Product Details — 12 BE + 3 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟡 `C-01`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟡 `D-04`, 🟢 `D-05`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟡 `G-02`, 🟡 `G-03`

**▶ Frontend starts once backend steps BE-1…BE-2 are done** (9 stories — essentially this domain's reads/writes/field resolvers; the trailing F/G stitches can lag).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `PDTL-FE-002`
- **FE-2.** `PDTL-FE-001`, `PDTL-FE-003`

---

### 6. Measurement — 30 BE + 4 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `B-09`, 🟡 `C-01`, 🟢 `C-02`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟡 `D-06`, 🟢 `D-07`, 🟠 `E-01`, 🟡 `F-01`, 🟢 `G-02`, 🟢 `H-01`
- **BE-3.** 🟢 `D-08`, 🟢 `D-09`, 🟢 `D-10`, 🟡 `G-01`, 🟢 `G-05`, 🟢 `G-06`, 🟢 `G-07`, 🟢 `H-02`

**▶ Frontend starts once backend steps BE-1…BE-3 are done** (12 stories — essentially this domain's reads/writes/field resolvers; the trailing F/G stitches can lag).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `MST-FE-003`
- **FE-2.** `MST-FE-004`
- **FE-3.** `MST-FE-001`, `MST-FE-002`

---

### 7. Packaging — 23 BE + 5 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟡 `C-01`, 🟡 `D-01`, 🟢 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟢 `D-05`, 🟢 `D-06`, 🟢 `D-07`, 🟡 `D-08`, 🟢 `D-09`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟢 `G-02`, 🟡 `G-03`, 🟠 `G-04`, 🟡 `G-05`

**▶ Frontend starts once backend steps BE-1…BE-2 are done** (19 stories — essentially this domain's reads/writes/field resolvers; the trailing F/G stitches can lag).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `PKG-FE-002`
- **FE-2.** `PKG-FE-004`
- **FE-3.** `PKG-FE-001`, `PKG-FE-003`, `PKG-FE-005`

---

### 8. Claims — 20 BE + 4 FE

**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):

- **BE-1.** 🟢 `B-01`
- **BE-2.** 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟡 `C-01`, 🟡 `C-02`, 🟡 `D-01`, 🟡 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟠 `E-01`, 🟡 `G-01`, 🟡 `G-02`, 🟡 `G-04`, 🟢 `G-06`, 🟡 `H-01`, 🟢 `H-02`
- **BE-3.** 🟠 `G-03`

**▶ Frontend starts once backend steps BE-1…BE-3 are done** (13 stories — essentially this domain's reads/writes/field resolvers; the trailing F/G stitches can lag).

**Frontend — cutover in this order** (reads → writes → saga):

- **FE-1.** `CLAIM-FE-001`
- **FE-2.** `CLAIM-FE-003`
- **FE-3.** `CLAIM-FE-002`, `CLAIM-FE-004`

---

**Cross-domain note:** every domain's `E-01` write story needs product's `PRODUCT-BE-E-00` (shared WriteSaga) first — product is built first, so it's ready in time. Impression's `F-01` and BOM/Product FE cross-links are handled by the domain order above.

*Sequencing cheat-sheet · generated 2026-07-24 by generate_sequencing_cheatsheet.py.*