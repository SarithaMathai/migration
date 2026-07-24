# Implementation Plan — 1 Backend + 1 Frontend Engineer

> 🏷️ **Tags:** `dgs-migration` · `team-plan` — **Generated:** 2026-07-24 · Derived from the same story parsers as the per-domain breakdowns (grouped-XS merges included), so story counts and day totals reconcile.
> Day figures are **nominal midpoints of AI-estimated ranges — confirm in refinement.** 1 sprint = 10 working days. d0 = program start. Team size and domain sequencing are set in `team_config.py` — change them there and regenerate.

---

## Team & operating model

> **⚠ Priority reorder (2026-07-24):** an **external team is waiting on the `watchlist` + `impression` dependencies**, so those two are prioritized. Impression's *backend* is now pulled far forward (its A–E gate lands early — see the backend lane), which is what unblocks the external consumer of the federated impression data. Impression's *frontend* stories are fused with BOM + Product screens (`getBomDataAndImpressions`, `getCarryForwardFormData`), so they still flip in the same wave as BOM/Product — the scheduler will not place them ahead of the partner stories they read. Net effect: `bom` and `product` core also move up; the smaller domains (`productDetails`, `measurement`, `packaging`, `claims`) shift later. Order is set in `team_config.py` (`BE_QUEUE` / `FE_WAVES`) with a revert note.

- **The backend engineer** runs all 8 domains sequentially: **Product** first (host DGS, shared wiring, largest surface — the foundation the rest build on), then the remaining domains in `team_config.BE_QUEUE` order.
- **The frontend engineer** follows the program waves (fe-10) sequentially: watchlist pilot first (1-sprint production soak is the wave-2 entry gate), then each domain cutover in turn.
- A domain's FE cutover starts when its **backend phases A–E** (reads, search, writes) are live; BE phases F–G (federation stitches, field-resolver parity) trail behind the flip and don't block it. *(Refinement lever: FE read-stories can start dual-running right after B/C — that pulls each FE start earlier than shown here.)*
- Phase-0 **spikes (SPIKE-01…07)** are not on these lanes — run them in the first 1–2 sprints alongside `PRODUCT-BE` scaffold work; E-phase stories are gated on their outcomes.

---

## Backend lane

| # | Domain | Lane | Stories | Est. days (lo–hi) | Day window | FE gate (A–E done) |
|---|---|---|---|---|---|---|
| 1 | **Product** | — | 69 | 200 (138–262) | d0–d200 (spr 1–20) | d108 |
| 2 | **BOM** | — | 37 | 91 (62–120) | d200–d291 (spr 21–30) | d247 |
| 3 | **Impression** | — | 7 | 14 (9–18) | d291–d304 (spr 30–31) | d297 |
| 4 | **Watchlist** | — | 13 | 31 (21–41) | d304–d336 (spr 31–34) | d324 |
| 5 | **Product Details** | — | 12 | 31 (21–41) | d336–d366 (spr 34–37) | d356 |
| 6 | **Measurement** | — | 30 | 56 (38–75) | d366–d423 (spr 37–43) | d408 |
| 7 | **Packaging** | — | 23 | 54 (37–72) | d423–d478 (spr 43–48) | d460 |
| 8 | **Claims** | — | 20 | 50 (34–66) | d478–d528 (spr 48–53) | d507 |

- **backend drains at d528** — post-launch F-phase stitches and G-phase parity leftovers land after the queue above.
- Cross-subgraph F-phase stories that wait on later-phase domains (attachment/discussion/sample/search subgraphs) are excluded from these gates — they land post-launch when the owning subgraph exists.

---

## Frontend lane

| Wave | Domain | Lane | FE days | Waits for | Day window |
|---|---|---|---|---|---|
| 1 | **Watchlist** | — | 8 | BE Watchlist A–E done (d324) | d324–d332 (spr 33–34) |
| 2 | **Product** | — | 86 | BE Product A–E done (d108) + pilot soak (d342) | d342–d428 (spr 35–43) |
| 2 | **BOM** | — | 38 | BE BOM A–E done (d247) + pilot soak (d342) | d428–d466 (spr 43–47) |
| 2 | **Impression** | — | 4 | BE Impression A–E done (d297) + pilot soak (d342) | d466–d470 (spr 47–47) |
| 3 | **Product Details** | — | 10 | BE Product Details A–E done (d356) | d470–d480 (spr 47–48) |
| 3 | **Measurement** | — | 16 | BE Measurement A–E done (d408) | d480–d495 (spr 48–50) |
| 3 | **Packaging** | — | 27 | BE Packaging A–E done (d460) | d495–d522 (spr 50–53) |
| 3 | **Claims** | — | 22 | BE Claims A–E done (d507) | d522–d544 (spr 53–55) |

- The frontend engineer is gate-bound, not capacity-bound — between gates they work parity dashboards, dual-run monitoring and rollback drills, and pre-pull the next domain's fragment/codegen prep.
- Search-gated stories (`MST-FE-002`, `BOM-FE-003`, `PRODUCT-FE-002`) also wait on the search read-hub decision — external to this plan and may slide independently.
- Impression rides its partner flips (`IMPRESSION-FE-001` with `BOM-FE-002`, `IMPRESSION-FE-002` with `PRODUCT-FE-001`) — this is why the priority reorder pulls `bom` and `product` forward too, not just impression. Impression's **backend** is unblocked much earlier (see its A–E gate in the backend lane) for any external consumer that needs the data rather than the UI cutover.

---

## Milestones

| Milestone | ≈ Day | ≈ Sprint |
|---|---|---|
| 🚦 Watchlist pilot live on the router | d332 | 34 |
| 🔗 First cross-subgraph cutover (Claims FE) | d544 | 55 |
| 🏁 Product backend complete (`plm-product` host) | d200 | 21 |
| 🧱 Backend lane drained (both subgraphs schema-complete) | d528 | 53 |
| ✅ All FE cutovers flipped | d544 | 55 |
| **Program complete (excl. post-launch F-phase)** | **d544** | **55** |

> ≈ **55 sprints (~28 months)** with this 1 BE + 1 FE team — see 00-program-overview.md for the program-level totals. Buffered (+20%) planning figure: ~66 sprints.

---

## How to read this with the other docs

- Per-domain lane detail: **Recommended Story Graph — 1 Backend Engineer** and **— 1 Frontend Engineer** in the Backend / Frontend sections of each `FederatedGqlBreakDown-{domain}` page.
- Dependency-only view (no team constraint): **Recommended Implementation Order** on the same pages.
- Program waves and external gates: `analysis/program/fe-10-migration-sequencing.md`.
- Team size and domain sequencing: `team_config.py`.

---
*Team plan · generated 2026-07-24 by generate_team_plan.py.*