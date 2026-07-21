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
# product first: host DGS, largest surface, shared wiring everything else co-locates
# into. Then the FE-wave-feeding order for the co-located domains (watchlist through
# bom), then the two separate-subgraph/small-tail domains (claims, impression).
#
# ⚠ product MUST stay first with N_BE_ENGINEERS == 1 (or be on the first lane to start
# with N_BE_ENGINEERS > 1): PRODUCT-BE-E-00 (the shared WriteSaga module, ADR-013) is a
# cross-domain Blocked-by dependency for bom/measurement/packaging/productDetails/
# watchlist/claims's own E-01 stories. Verified — with product first, E-00 finishes on
# day ~16 of product's ~200-day build, long before any other domain's lane starts, so no
# consumer can be scheduled ahead of its producer. Moving product later (or splitting it
# across a later parallel lane with N_BE_ENGINEERS > 1) would need E-00 pulled out and
# scheduled as its own zero-dependency first step, not left implicit in product's queue
# position.
BE_QUEUE = [
    "product", "watchlist", "productDetails", "measurement", "packaging", "bom",
    "claims", "impression",
]

# ─── Frontend wave plan ─────────────────────────────────────────────────────
# (wave, domain) — the program-wave order from analysis/program/fe-10-migration-sequencing.md.
# Waves are entry gates (e.g. wave 2 doesn't start before the wave-1 pilot's soak period
# ends), not engineer assignments — the program-level scheduler packs the domains within
# and across waves onto N_FE_ENGINEERS parallel lanes by the same greedy heuristic as BE.
FE_WAVES = [
    (1, "watchlist"),
    (2, "productDetails"),
    (2, "measurement"),
    (2, "packaging"),
    (3, "bom"),
    (3, "claims"),
    (4, "product"),
    (4, "impression"),
]
