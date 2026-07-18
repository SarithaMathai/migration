# Implementation Plan — 2 Backend + 2 Frontend Engineers

> 🏷️ **Tags:** `dgs-migration` · `team-plan` — **Generated:** 2026-07-17 · Derived from the same story parsers as the per-domain breakdowns (grouped-XS merges included), so story counts and day totals reconcile.
> Day figures are **nominal midpoints of AI-estimated ranges — confirm in refinement.** 1 sprint = 10 working days. d0 = program start.

---

## Team & operating model

- **BE-1** owns **Product** end-to-end (host DGS, shared wiring, largest surface — one owner avoids schema-merge churn), then takes **Claims** (the separate `spark-claims` subgraph) and the tiny **Impression** tail — this balances the two lanes to within a sprint of each other.
- **BE-2** runs the co-located domains **in the order the FE waves need them**: watchlist → productDetails → measurement → packaging → bom.
- **FE-1 / FE-2** follow the program waves (fe-10): watchlist pilot first (1-sprint production soak is the wave-2 entry gate), then parallel domain cutovers, Product split across both engineers last.
- A domain's FE cutover starts when its **backend phases A–E** (reads, search, writes) are live; BE phases F–G (federation stitches, field-resolver parity) trail behind the flip and don't block it. *(Refinement lever: FE read-stories can start dual-running right after B/C — that pulls each FE start earlier than shown here.)*
- Phase-0 **spikes (SPIKE-01…07)** are not on these lanes — run them in the first 1–2 sprints alongside `PRODUCT-BE` scaffold work; E-phase stories are gated on their outcomes.

---

## Backend lanes

| Lane | # | Domain | Stories | Est. days (lo–hi) | Day window | FE gate (A–E done) |
|---|---|---|---|---|---|---|
| 👤 BE-1 | 1 | **Product** | 70 | 202 (139–264) | d0–d202 (spr 1–21) | d102 |
| 👤 BE-1 | 2 | **Claims** | 21 | 53 (36–70) | d202–d254 (spr 21–26) | d231 |
| 👤 BE-1 | 3 | **Impression** | 8 | 15 (10–20) | d254–d270 (spr 26–27) | d260 |
| 👤 BE-2 | 1 | **Watchlist** | 14 | 34 (23–45) | d0–d34 (spr 1–4) | d19 |
| 👤 BE-2 | 2 | **Product Details** | 13 | 34 (23–45) | d34–d68 (spr 4–7) | d54 |
| 👤 BE-2 | 3 | **Measurement** | 21 | 44 (30–59) | d68–d112 (spr 7–12) | d99 |
| 👤 BE-2 | 4 | **Packaging** | 24 | 58 (39–76) | d112–d170 (spr 12–17) | d150 |
| 👤 BE-2 | 5 | **BOM** | 37 | 91 (62–120) | d170–d261 (spr 18–27) | d214 |

- Lanes are load-balanced: **BE-1 drains at d270**, **BE-2 at d261** — whoever frees first picks up post-launch F-phase stitches, G-phase parity leftovers, and pairs on the other lane's remaining domain.
- Cross-subgraph F-phase stories that wait on later-phase domains (attachment/discussion/sample/search subgraphs) are excluded from these gates — they land post-launch when the owning subgraph exists.

---

## Frontend lanes

| Wave | Domain | Engineer | FE days | Waits for | Day window |
|---|---|---|---|---|---|
| 1 | **Watchlist** | 👤 FE-1 | 8 | BE Watchlist A–E done (d19) | d19–d28 (spr 2–3) |
| 2 | **Product Details** | 👤 FE-1 | 10 | BE Product Details A–E done (d54) | d54–d64 (spr 6–7) |
| 2 | **Measurement** | 👤 FE-2 | 16 | BE Measurement A–E done (d99) | d99–d114 (spr 10–12) |
| 2 | **Packaging** | 👤 FE-2 | 27 | BE Packaging A–E done (d150) | d150–d176 (spr 15–18) |
| 3 | **BOM** | 👤 FE-1 | 38 | BE BOM A–E done (d214) | d214–d252 (spr 22–26) |
| 3 | **Claims** | 👤 FE-2 | 22 | BE Claims A–E done (d231) | d231–d253 (spr 24–26) |
| 4 | **Product** | 👤 FE-1 + FE-2 | 84 | BE Product A–E done (d102) | d253–d295 (spr 26–30) |
| 4 | **Impression** | 👤 FE-2 | 4 | BE Impression A–E done (d260) | d295–d299 (spr 30–30) |

- FE engineers are gate-bound, not capacity-bound — between gates they pair on parity dashboards, dual-run monitoring and rollback drills, and pre-pull the next domain's fragment/codegen prep.
- Search-gated stories (`MST-FE-002`, `BOM-FE-003`, `PRODUCT-FE-003`) also wait on the search read-hub decision — external to this plan and may slide independently.
- Impression rides its partner flips (`IMPRESSION-FE-001` with `BOM-FE-002`, `IMPRESSION-FE-002` with `PRODUCT-FE-001`).

---

## Milestones

| Milestone | ≈ Day | ≈ Sprint |
|---|---|---|
| 🚦 Watchlist pilot live on the router | d28 | 3 |
| 🔗 First cross-subgraph cutover (Claims FE) | d253 | 26 |
| 🏁 Product backend complete (`plm-product` host) | d202 | 21 |
| 🧱 All backend lanes drained (both subgraphs schema-complete) | d270 | 27 |
| ✅ All FE cutovers flipped | d299 | 30 |
| **Program complete (excl. post-launch F-phase)** | **d299** | **30** |

> ≈ **30 sprints (~15 months)** with this team, vs the sequential single-pair estimate in 00-program-overview.md. Buffered (+20%) planning figure: ~36 sprints.

---

## How to read this with the other docs

- Per-domain lane detail: **Recommended Story Graph — 2 Backend Engineers** in each `FederatedGqlBreakDown-BE-{domain}` page, and **— 2 Frontend Engineers** in each `FederatedGqlBreakDown-FE-{domain}` page.
- Dependency-only view (no team constraint): **Recommended Implementation Order** on the same pages.
- Program waves and external gates: `analysis/program/fe-10-migration-sequencing.md`.

---
*Team plan · generated 2026-07-17 by generate_team_plan.py.*