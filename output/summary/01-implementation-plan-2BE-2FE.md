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
| 👤 BE-1 | 1 | **Product** | 48 | 174 (121–228) | d0–d174 (spr 1–18) | d86 |
| 👤 BE-1 | 2 | **Claims** | 15 | 47 (32–62) | d174–d222 (spr 18–23) | d200 |
| 👤 BE-1 | 3 | **Impression** | 7 | 14 (9–18) | d222–d235 (spr 23–24) | d228 |
| 👤 BE-2 | 1 | **Watchlist** | 11 | 30 (20–39) | d0–d30 (spr 1–3) | d18 |
| 👤 BE-2 | 2 | **Product Details** | 11 | 32 (22–43) | d30–d62 (spr 3–7) | d48 |
| 👤 BE-2 | 3 | **Measurement** | 14 | 37 (25–49) | d62–d99 (spr 7–10) | d87 |
| 👤 BE-2 | 4 | **Packaging** | 18 | 52 (35–68) | d99–d150 (spr 10–16) | d130 |
| 👤 BE-2 | 5 | **BOM** | 24 | 76 (52–100) | d150–d226 (spr 16–23) | d187 |

- Lanes are load-balanced: **BE-1 drains at d235**, **BE-2 at d226** — whoever frees first picks up post-launch F-phase stitches, G-phase parity leftovers, and pairs on the other lane's remaining domain.
- Cross-subgraph F-phase stories that wait on later-phase domains (attachment/discussion/sample/search subgraphs) are excluded from these gates — they land post-launch when the owning subgraph exists.

---

## Frontend lanes

| Wave | Domain | Engineer | FE days | Waits for | Day window |
|---|---|---|---|---|---|
| 1 | **Watchlist** | 👤 FE-1 | 8 | BE Watchlist A–E done (d18) | d18–d26 (spr 2–3) |
| 2 | **Product Details** | 👤 FE-1 | 10 | BE Product Details A–E done (d48) | d48–d58 (spr 5–6) |
| 2 | **Measurement** | 👤 FE-2 | 16 | BE Measurement A–E done (d87) | d87–d102 (spr 9–11) |
| 2 | **Packaging** | 👤 FE-2 | 27 | BE Packaging A–E done (d130) | d130–d157 (spr 14–16) |
| 3 | **BOM** | 👤 FE-1 | 34 | BE BOM A–E done (d187) | d187–d222 (spr 19–23) |
| 3 | **Claims** | 👤 FE-2 | 22 | BE Claims A–E done (d200) | d200–d222 (spr 20–23) |
| 4 | **Product** | 👤 FE-1 + FE-2 | 80 | BE Product A–E done (d86) | d222–d262 (spr 23–27) |
| 4 | **Impression** | 👤 FE-2 | 4 | BE Impression A–E done (d228) | d262–d266 (spr 27–27) |

- FE engineers are gate-bound, not capacity-bound — between gates they pair on parity dashboards, dual-run monitoring and rollback drills, and pre-pull the next domain's fragment/codegen prep.
- Search-gated stories (`MST-FE-002`, `BOM-FE-003`, `PRODUCT-FE-003`) also wait on the search read-hub decision — external to this plan and may slide independently.
- Impression rides its partner flips (`IMPRESSION-FE-001` with `BOM-FE-002`, `IMPRESSION-FE-002` with `PRODUCT-FE-001`).

---

## Milestones

| Milestone | ≈ Day | ≈ Sprint |
|---|---|---|
| 🚦 Watchlist pilot live on the router | d26 | 3 |
| 🔗 First cross-subgraph cutover (Claims FE) | d222 | 23 |
| 🏁 Product backend complete (`plm-product` host) | d174 | 18 |
| 🧱 All backend lanes drained (both subgraphs schema-complete) | d235 | 24 |
| ✅ All FE cutovers flipped | d266 | 27 |
| **Program complete (excl. post-launch F-phase)** | **d266** | **27** |

> ≈ **27 sprints (~14 months)** with this team, vs the sequential single-pair estimate in 00-program-overview.md. Buffered (+20%) planning figure: ~32 sprints.

---

## How to read this with the other docs

- Per-domain lane detail: **Recommended Story Graph — 2 Backend Engineers** in each `FederatedGqlBreakDown-BE-{domain}` page, and **— 2 Frontend Engineers** in each `FederatedGqlBreakDown-FE-{domain}` page.
- Dependency-only view (no team constraint): **Recommended Implementation Order** on the same pages.
- Program waves and external gates: `analysis/program/fe-10-migration-sequencing.md`.

---
*Team plan · generated 2026-07-17 by generate_team_plan.py.*