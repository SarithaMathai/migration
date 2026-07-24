#!/usr/bin/env python3
"""
Single source of truth for team size + domain sequencing.

Every generator that renders a "Recommended Story Graph — N Backend/Frontend Engineer(s)"
section or the program-level implementation plan reads N_BE_ENGINEERS / N_FE_ENGINEERS /
BE_QUEUE / FE_PLAN from here — change the team size or the domain order in this one file,
then regenerate; no other file needs to change.

Consumers:
  generate_breakdown.py   team_plan_md(stories)               -> per-domain BE lane table
  generate_frontend.py    fe_team_plan_lines(group)            -> per-domain FE lane table
  generate_team_plan.py   build_team_plan()                    -> program-level BE+FE plan
"""

# ─── Team size ──────────────────────────────────────────────────────────────
# Bump these to re-plan with a bigger team; every consumer above re-derives its lanes
# from this number alone (no per-file engineer count to hunt down).
N_BE_ENGINEERS = 1
N_FE_ENGINEERS = 1

# ─── Backend domain queue ───────────────────────────────────────────────────
# The order the backend engineer(s) work through the 8 phase-1 domains, front to back.
# With N_BE_ENGINEERS == 1 this is one sequential lane; with N_BE_ENGINEERS > 1 the
# program-level scheduler (generate_team_plan.py) packs this same queue's domains onto
# N parallel lanes by a greedy critical-path heuristic — the order below still expresses
# priority (earlier = higher priority when two domains could start at once).
#
# ⚠ REORDERED 2026-07-24 to unblock an EXTERNAL TEAM waiting on watchlist + impression.
# The external consumer depends on the federated backend data for those two domains, and
# (per the user's call) their FE cutovers are pulled forward too. Because impression's FE
# stories are FUSED with BOM + Product screens (IMPRESSION-FE-001 needs 10 BOM BE stories +
# BOM-FE-002; IMPRESSION-FE-002 needs ~13 Product BE stories + PRODUCT-FE-001), pulling
# impression's FE forward necessarily pulls BOM's and Product's core BE+FE forward with it.
# So the priority front of the queue is: product, bom, impression, watchlist — everything
# impression's FE transitively needs — then the remaining domains in the old order.
#
# product STAYS first: (1) PRODUCT-BE-E-00 (shared WriteSaga, ADR-013) blocks every domain's
# E-01 write story — it finishes ~day 16 of product's build, before any consumer's E-01 is
# reached; (2) impression FE + BOM FE both need Product BE stories (PRODUCT-BE-B-01/G-0x/S-01,
# PRODUCT-FE-001), so product's core must precede them anyway. bom second: impression FE needs
# BOM core (A-04/B-0x/G-0x + BOM-FE-002). impression third, watchlist fourth (watchlist is the
# wave-1 pilot on the FE side; its BE is tiny and independent apart from E-01 waiting on E-00).
#
# To revert to the pilot-first ordering, restore: product, watchlist, productDetails,
# measurement, packaging, bom, claims, impression (and the matching FE_WAVES below).
BE_QUEUE = [
    "product", "bom", "impression", "watchlist",
    "productDetails", "measurement", "packaging", "claims",
]

# ─── Frontend wave plan ─────────────────────────────────────────────────────
# (wave, domain) — the program-wave order from analysis/program/fe-10-migration-sequencing.md.
# Waves are entry gates (e.g. wave 2 doesn't start before the wave-1 pilot's soak period
# ends), not engineer assignments — the program-level scheduler packs the domains within
# and across waves onto N_FE_ENGINEERS parallel lanes by the same greedy heuristic as BE.
# ⚠ REORDERED 2026-07-24 (see BE_QUEUE note): external team needs watchlist + impression
# flipped early. watchlist stays the wave-1 pilot (smallest, safest flag flip + soak). Then
# wave 2 brings product + bom + impression together — impression FE literally shares queries
# with BOM/Product screens (getBomDataAndImpressions, getCarryForwardFormData), so they must
# flip in the same wave, not before their partners. The remaining domains follow in wave 3.
# Revert note: the pilot-first order was watchlist(1), productDetails/measurement/packaging(2),
# bom/claims(3), product/impression(4).
FE_WAVES = [
    (1, "watchlist"),
    (2, "product"),
    (2, "bom"),
    (2, "impression"),
    (3, "productDetails"),
    (3, "measurement"),
    (3, "packaging"),
    (3, "claims"),
]
