# Implementation Plan — 1 Backend + 1 Frontend Engineer

> 🏷️ **Tags:** `dgs-migration` · `team-plan` — **Generated:** 2026-07-18 · Derived from the same story parsers as the per-domain breakdowns (grouped-XS merges included), so story counts and day totals reconcile.
> Day figures are **nominal midpoints of AI-estimated ranges — confirm in refinement.** 1 sprint = 10 working days. d0 = program start. Team size and domain sequencing are set in `team_config.py` — change them there and regenerate.

---

## Team & operating model

- **The backend engineer** runs all 8 domains sequentially: **Product** first (host DGS, shared wiring, largest surface — the foundation the rest build on), then the remaining domains in `team_config.BE_QUEUE` order.
- **The frontend engineer** follows the program waves (fe-10) sequentially: watchlist pilot first (1-sprint production soak is the wave-2 entry gate), then each domain cutover in turn.
- A domain's FE cutover starts when its **backend phases A–E** (reads, search, writes) are live; BE phases F–G (federation stitches, field-resolver parity) trail behind the flip and don't block it. *(Refinement lever: FE read-stories can start dual-running right after B/C — that pulls each FE start earlier than shown here.)*
- Phase-0 **spikes (SPIKE-01…07)** are not on these lanes — run them in the first 1–2 sprints alongside `PRODUCT-BE` scaffold work; E-phase stories are gated on their outcomes.

---

## Backend lane

| # | Domain | Lane | Stories | Est. days (lo–hi) | Day window | FE gate (A–E done) |
|---|---|---|---|---|---|---|
| 1 | **Product** | — | 69 | 200 (138–262) | d0–d200 (spr 1–20) | d108 |
| 2 | **Watchlist** | — | 13 | 31 (21–41) | d200–d231 (spr 21–24) | d219 |
| 3 | **Product Details** | — | 12 | 31 (21–41) | d231–d262 (spr 24–27) | d252 |
| 4 | **Measurement** | — | 20 | 42 (28–55) | d262–d304 (spr 27–31) | d293 |
| 5 | **Packaging** | — | 23 | 54 (37–72) | d304–d358 (spr 31–36) | d340 |
| 6 | **BOM** | — | 37 | 91 (62–120) | d358–d449 (spr 36–45) | d405 |
| 7 | **Claims** | — | 20 | 50 (34–66) | d449–d499 (spr 45–50) | d478 |
| 8 | **Impression** | — | 7 | 14 (9–18) | d499–d512 (spr 50–52) | d505 |

- **backend drains at d512** — post-launch F-phase stitches and G-phase parity leftovers land after the queue above.
- Cross-subgraph F-phase stories that wait on later-phase domains (attachment/discussion/sample/search subgraphs) are excluded from these gates — they land post-launch when the owning subgraph exists.

---

## Frontend lane

| Wave | Domain | Lane | FE days | Waits for | Day window |
|---|---|---|---|---|---|
| 1 | **Watchlist** | — | 8 | BE Watchlist A–E done (d219) | d219–d228 (spr 22–23) |
| 2 | **Product Details** | — | 10 | BE Product Details A–E done (d252) | d252–d262 (spr 26–27) |
| 2 | **Measurement** | — | 16 | BE Measurement A–E done (d293) | d293–d308 (spr 30–31) |
| 2 | **Packaging** | — | 27 | BE Packaging A–E done (d340) | d340–d368 (spr 35–37) |
| 3 | **BOM** | — | 38 | BE BOM A–E done (d405) | d405–d442 (spr 41–45) |
| 3 | **Claims** | — | 22 | BE Claims A–E done (d478) | d478–d500 (spr 48–51) |
| 4 | **Product** | — | 84 | BE Product A–E done (d108) + pilot soak (d238) | d500–d584 (spr 51–59) |
| 4 | **Impression** | — | 4 | BE Impression A–E done (d505) | d584–d588 (spr 59–59) |

- The frontend engineer is gate-bound, not capacity-bound — between gates they work parity dashboards, dual-run monitoring and rollback drills, and pre-pull the next domain's fragment/codegen prep.
- Search-gated stories (`MST-FE-002`, `BOM-FE-003`, `PRODUCT-FE-003`) also wait on the search read-hub decision — external to this plan and may slide independently.
- Impression rides its partner flips (`IMPRESSION-FE-001` with `BOM-FE-002`, `IMPRESSION-FE-002` with `PRODUCT-FE-001`).

---

## Milestones

| Milestone | ≈ Day | ≈ Sprint |
|---|---|---|
| 🚦 Watchlist pilot live on the router | d228 | 23 |
| 🔗 First cross-subgraph cutover (Claims FE) | d500 | 51 |
| 🏁 Product backend complete (`plm-product` host) | d200 | 21 |
| 🧱 Backend lane drained (both subgraphs schema-complete) | d512 | 52 |
| ✅ All FE cutovers flipped | d588 | 59 |
| **Program complete (excl. post-launch F-phase)** | **d588** | **59** |

> ≈ **59 sprints (~30 months)** with this 1 BE + 1 FE team — see 00-program-overview.md for the program-level totals. Buffered (+20%) planning figure: ~71 sprints.

---

## How to read this with the other docs

- Per-domain lane detail: **Recommended Story Graph — 1 Backend Engineer** and **— 1 Frontend Engineer** in the Backend / Frontend sections of each `FederatedGqlBreakDown-{domain}` page.
- Dependency-only view (no team constraint): **Recommended Implementation Order** on the same pages.
- Program waves and external gates: `analysis/program/fe-10-migration-sequencing.md`.
- Team size and domain sequencing: `team_config.py`.

---
*Team plan · generated 2026-07-18 by generate_team_plan.py.*