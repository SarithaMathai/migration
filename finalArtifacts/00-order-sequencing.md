# Migration Order & Sequencing — Backend + Frontend

> 🏷️ **Tags:** `dgs-migration` · `sequencing` — **Assembled:** 2026-07-24 from the generated plan
> artifacts (`00-cheatsheet.md`, `00-sequencing.md`, `00-domain-rollout.md`, `00-fe-unblock-plan.md`)
> and validated against the story sources in `output/analysis/*/be-04-stories.md` and the client
> queries in `ClientCallingGqlQueries/`. Day figures are AI-estimated midpoints — confirm in
> refinement. 1 sprint = 10 working days · d0 = program start.
>
> **Companion page:** *External Dependencies* — the cross-domain and externally-owned blockers this
> plan has to honor. Read both together.

---

## 1. The one thing to know

Build the program **domain by domain**, but **frontend does not wait for a whole domain** — each FE
story starts the moment *its own* backend dependencies land, and FE stories that are ready together can
run in parallel. Most of the frontend is reachable after only **2–3 backend dependency levels**, not
after the backend queue drains.

- **Team assumed:** 1 backend + 1 frontend engineer, in parallel. (Change in `team_config.py` to
  re-plan for a bigger team.)
- **Program length:** ≈ **55 sprints (~28 months)**, buffered (+20%) ≈ 66 sprints.

---

## 2. Domain order (cutover / flip order)

> **⚠ Reprioritized 2026-07-24** to unblock an external team waiting on **watchlist + impression**.
> Because impression's frontend shares screens with BOM + Product (`getBomDataAndImpressions`),
> those move up too. Order is set in `team_config.py`.

| # | Domain | Why here | BE stories | FE stories |
|---|---|---|---|---|
| 1 | **Watchlist** | Wave 1 pilot — smallest isolated surface; proves flag flip + rollback | 13 | 3 |
| 2 | **Product** | Largest surface + host DGS — pulled up (feeds impression/BOM FE); writes last | 69 | 13 |
| 3 | **BOM** | High complexity, search-gated list views — pulled up to feed impression FE | 37 | 7 |
| 4 | **Impression** | Prioritized for an external team; FE flips with its BOM / Product partners | 7 | 2 |
| 5 | **Product Details** | Small, isolated, no shared blockers | 12 | 3 |
| 6 | **Measurement** | Parallel with the other small domains | 30 | 4 |
| 7 | **Packaging** | Parallel with the other small domains | 23 | 5 |
| 8 | **Claims** | First cross-subgraph cutover (`spark-claims`) | 20 | 4 |

**Product first, always** — `PRODUCT-BE-E-00` (the shared `WriteSaga` module) is a hard blocker for
**every** domain's `E-01` write story; building Product first means it's ready before any consumer needs it.

---

## 3. Backend → Frontend handoff per domain

For each domain: the backend builds its **phases A–E** (reads → search → writes) far enough that the
**specific** stories a frontend story needs are live; then the frontend flip for that domain can begin
while the backend engineer moves to the next domain. Backend **F/G** stories (federation stitches,
field-resolver parity) trail *behind* the flip and don't gate it.

| Domain | BE build window | FE can start (gate day) | FE cutover window | FE order (reads → writes → saga) |
|---|---|---|---|---|
| Watchlist | d0–d31* | d219 | d219–d228 | FE-002 → FE-001, FE-003 |
| Product | d0–d200 | **d108** | d342–d428 | FE-003 → FE-008 → FE-006/007/011/013 → FE-001/002/004/005/010 → FE-009/012 |
| BOM | d200–d291 | d247 | d428–d466 | FE-001 → FE-005 → FE-002/004 → FE-003/006/007 |
| Impression | d291–d304 | d297 | d466–d470 | FE-001 → FE-002 |
| Product Details | d336–d366 | d356 | d470–d480 | FE-002 → FE-001, FE-003 |
| Measurement | d366–d423 | d408 | d480–d495 | FE-003 → FE-004 → FE-001, FE-002 |
| Packaging | d423–d478 | d460 | d495–d522 | FE-002 → FE-004 → FE-001/003/005 |
| Claims | d478–d528 | d507 | d522–d544 | FE-001 → FE-003 → FE-002, FE-004 |

> \* Watchlist backend is tiny; the d0–d31 figures are its own effort — its FE gate lands at d219 in
> the calendar because the single backend engineer reaches watchlist only after Product + BOM.
> **Full per-story build order:** `finalArtifacts/00-cheatsheet.md`. **Day-by-day calendar:**
> `finalArtifacts/00-domain-rollout.md` and `01-implementation-plan-1BE-1FE.md`.

---

## 4. Earliest FE start — the parallelism opportunity

Frontend does **not** need a whole domain done. Grouped by "all backend deps satisfied," here is when
each FE story becomes startable (level = backend dependency depth, not calendar days). **Everything in
one row has no dependency on the others — parallel-eligible** (limited only by FE capacity):

| Ready after | Frontend stories (parallel-eligible), by domain |
|---|---|
| **immediately** (no BE dep) | **BOM:** `BOM-FE-001` · **Claims:** `CLAIM-FE-001` |
| **backend level 2** | **BOM:** `BOM-FE-003/004/005/006` · **Claims:** `CLAIM-FE-003/004` · **Measurement:** `MST-FE-003/004` · **Packaging:** `PKG-FE-001/002/003/004/005` · **Product:** `PRODUCT-FE-002/003/007/008/009/010/013` · **Product Details:** `PDTL-FE-001/002/003` · **Watchlist:** `WATCHLIST-FE-002/003` |
| **backend level 3** | **BOM:** `BOM-FE-002/007` · **Claims:** `CLAIM-FE-002` · **Impression:** `IMPRESSION-FE-001/002` · **Measurement:** `MST-FE-001/002` · **Product:** `PRODUCT-FE-001/004/005/006/011/012` · **Watchlist:** `WATCHLIST-FE-001` |

**Takeaway:** ~2 FE stories need zero backend; ~25 more are ready after just **backend level 2**,
across 7 domains. The frontend engineer is **gate-bound, not capacity-bound** — between flips they run
parity dashboards, dual-run monitoring, rollback drills, and pre-pull the next domain's prep.

> **Of 41 FE stories, 38 depend only on their own domain's backend** — only 3 reach across domains
> (the impression pair, fused with BOM/Product screens). So domain-by-domain is the right structure;
> the parallelism above is the refinement within it. Full detail: `00-fe-unblock-plan.md`.

---

## 5. Backend build order within a domain (illustrative — Watchlist)

Within each domain the backend is built in **dependency steps**; stories in the same step are
independent and can be built in any order. The frontend gate opens once the A–E stories its FE stories
read are done — the trailing F/G stitches lag.

- **BE-1.** `B-01` (module scaffold — everything waits on it)
- **BE-2.** `B-02`, `B-03`, `C-01`, `D-01`, `D-02`, `E-01`, `F-01`, `F-02`, `G-01`, `G-02`, `G-03`
- **BE-3.** `G-05`
- **▶ Frontend starts** once `B-01, C-01, D-01, D-02, E-01, G-01, G-02, G-03, G-05` are done.
- **FE-1.** `WATCHLIST-FE-002` (writes) → **FE-2.** `WATCHLIST-FE-001` (reads) ‖ `WATCHLIST-FE-003` (saga)

The same shape for all 8 domains is in `finalArtifacts/00-cheatsheet.md` (one page).

---

## 6. How this reconciles with the other docs

- **Condensed one-pager (build order):** `finalArtifacts/00-cheatsheet.md`
- **Full per-story step tables:** `finalArtifacts/00-sequencing.md`
- **Compact per-story dependency chains:** `finalArtifacts/00-dependency-map.md`
- **Day-by-day domain rollout:** `finalArtifacts/00-domain-rollout.md`
- **Blocker-first / FE readiness waves:** `finalArtifacts/00-fe-unblock-plan.md`
- **Team calendar:** `output/summary/01-implementation-plan-1BE-1FE.md`
- **External / cross-domain blockers:** the *External Dependencies* companion page.

---
*Order & Sequencing · assembled 2026-07-24 · source of truth = team_config.py + the generated plan docs.*
