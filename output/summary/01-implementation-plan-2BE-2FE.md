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
| 👤 BE-1 | 1 | **Product** | 51 | 182 (126–238) | d0–d182 (spr 1–19) | d86 |
| 👤 BE-1 | 2 | **Claims** | 16 | 48 (33–64) | d182–d230 (spr 19–24) | d207 |
| 👤 BE-1 | 3 | **Impression** | 7 | 14 (9–18) | d230–d244 (spr 24–25) | d236 |
| 👤 BE-2 | 1 | **Watchlist** | 12 | 31 (21–41) | d0–d31 (spr 1–4) | d18 |
| 👤 BE-2 | 2 | **Product Details** | 11 | 32 (22–43) | d31–d64 (spr 4–7) | d50 |
| 👤 BE-2 | 3 | **Measurement** | 15 | 38 (26–51) | d64–d102 (spr 7–11) | d88 |
| 👤 BE-2 | 4 | **Packaging** | 18 | 52 (35–68) | d102–d154 (spr 11–16) | d133 |
| 👤 BE-2 | 5 | **BOM** | 25 | 79 (54–104) | d154–d232 (spr 16–24) | d190 |

- Lanes are load-balanced: **BE-1 drains at d244**, **BE-2 at d232** — whoever frees first picks up post-launch F-phase stitches, G-phase parity leftovers, and pairs on the other lane's remaining domain.
- Cross-subgraph F-phase stories that wait on later-phase domains (attachment/discussion/sample/search subgraphs) are excluded from these gates — they land post-launch when the owning subgraph exists.

---

## Frontend lanes

| Wave | Domain | Engineer | FE days | Waits for | Day window |
|---|---|---|---|---|---|
| 1 | **Watchlist** | 👤 FE-1 | 8 | BE Watchlist A–E done (d18) | d18–d26 (spr 2–3) |
| 2 | **Product Details** | 👤 FE-1 | 10 | BE Product Details A–E done (d50) | d50–d60 (spr 6–6) |
| 2 | **Measurement** | 👤 FE-2 | 16 | BE Measurement A–E done (d88) | d88–d104 (spr 9–11) |
| 2 | **Packaging** | 👤 FE-2 | 27 | BE Packaging A–E done (d133) | d133–d160 (spr 14–16) |
| 3 | **BOM** | 👤 FE-1 | 38 | BE BOM A–E done (d190) | d190–d228 (spr 20–23) |
| 3 | **Claims** | 👤 FE-2 | 22 | BE Claims A–E done (d207) | d207–d229 (spr 21–23) |
| 4 | **Product** | 👤 FE-1 + FE-2 | 84 | BE Product A–E done (d86) | d229–d271 (spr 23–28) |
| 4 | **Impression** | 👤 FE-2 | 4 | BE Impression A–E done (d236) | d271–d275 (spr 28–28) |

- FE engineers are gate-bound, not capacity-bound — between gates they pair on parity dashboards, dual-run monitoring and rollback drills, and pre-pull the next domain's fragment/codegen prep.
- Search-gated stories (`MST-FE-002`, `BOM-FE-003`, `PRODUCT-FE-003`) also wait on the search read-hub decision — external to this plan and may slide independently.
- Impression rides its partner flips (`IMPRESSION-FE-001` with `BOM-FE-002`, `IMPRESSION-FE-002` with `PRODUCT-FE-001`).

---

## Milestones

| Milestone | ≈ Day | ≈ Sprint |
|---|---|---|
| 🚦 Watchlist pilot live on the router | d26 | 3 |
| 🔗 First cross-subgraph cutover (Claims FE) | d229 | 23 |
| 🏁 Product backend complete (`plm-product` host) | d182 | 19 |
| 🧱 All backend lanes drained (both subgraphs schema-complete) | d244 | 25 |
| ✅ All FE cutovers flipped | d275 | 28 |
| **Program complete (excl. post-launch F-phase)** | **d275** | **28** |

> ≈ **28 sprints (~14 months)** with this team, vs the sequential single-pair estimate in 00-program-overview.md. Buffered (+20%) planning figure: ~34 sprints.

---

## How to read this with the other docs

- Per-domain lane detail: **Recommended Story Graph — 2 Backend Engineers** in each `FederatedGqlBreakDown-BE-{domain}` page, and **— 2 Frontend Engineers** in each `FederatedGqlBreakDown-FE-{domain}` page.
- Dependency-only view (no team constraint): **Recommended Implementation Order** on the same pages.
- Program waves and external gates: `analysis/program/fe-10-migration-sequencing.md`.

---
*Team plan · generated 2026-07-17 by generate_team_plan.py.*