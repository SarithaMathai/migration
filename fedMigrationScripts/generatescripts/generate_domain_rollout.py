#!/usr/bin/env python3
"""
Domain-by-domain rollout plan for the 1 BE + 1 FE team.

Same team + same numbers as 01-implementation-plan-{n}BE-{n}FE.md, but reorganized the way the
work is actually run: **one self-contained block per domain**, in cutover order, each showing

    BE builds the prerequisite stories  →  FE start gate (which BE stories, which day)
      →  FE cutover sequence  →  domain done.

The idea is "we complete domain by domain": the backend engineer gets a domain far enough along
(its reads/search/writes — phases A–E) that the frontend engineer can start flipping it, while the
backend engineer moves on to the next domain and the trailing F/G parity work lands post-flip.

ACCURACY BY REUSE — nothing here re-derives an estimate or an edge:
  • Day math / lane windows / FE gate days come from generate_team_plan.py's own helpers
    (be_domain_effort, fe_domain_effort, _pack_lanes, _win, _sprint) — so every day figure in
    this doc equals the corresponding cell in 01-implementation-plan-{n}BE-{n}FE.md.
  • Which specific BE stories gate FE, and the FE cutover order, come from generate_project_plan.py's
    per-domain step engine (bd.compute_implementation_order + fe.fe_stages) — same as 00-sequencing.md.
  • Domain order = team_config.FE_WAVES (the cutover/flip order), since this doc is organized around
    the FE flip. team_config.py stays the single source of truth for team size + sequencing.

Intended for 1 BE + 1 FE (N_BE_ENGINEERS == N_FE_ENGINEERS == 1). It still renders for larger teams
but the "BE moves to the next domain while FE flips this one" narrative is written for the 1+1 case.

Output: output/summary/01b-domain-rollout-{n}BE-{n}FE.md
        (generate_all.py copies it to finalArtifacts/00-domain-rollout.md)

Run (from anywhere):
    python fedMigrationScripts/generatescripts/generate_domain_rollout.py
"""

import importlib.util
import re
from datetime import date
from pathlib import Path

from team_config import N_BE_ENGINEERS, N_FE_ENGINEERS, BE_QUEUE, FE_WAVES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "output" / "summary"
TODAY = date.today().isoformat()
PLAN_TAG = f"{N_BE_ENGINEERS}BE-{N_FE_ENGINEERS}FE"
SPRINT_DAYS = 10


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
    spec.loader.exec_module(mod)                          # type: ignore[union-attr]
    return mod


bd = _load("generate_breakdown")
fe = _load("generate_frontend")
tp = _load("generate_team_plan")        # reuse its day-math so numbers match the team plan
pp = _load("generate_project_plan")     # reuse its per-domain step engine

_BE_SHORT_RE = re.compile(r"-BE-([A-H]-\d+(?:-\d+)?)$")


def _short_title(story: dict, width: int = 46) -> str:
    t = re.sub(r"`", "", story["title"]).strip()
    return (t[: width - 1] + "…") if len(t) > width else t


def _order_key(short_id: str) -> tuple:
    m = re.match(r"([A-H])-(\d+)(?:-(\d+))?$", short_id)
    return (bd.PHASE_SEQ.find(m.group(1)), int(m.group(2)), int(m.group(3) or 0)) if m else (99, 0, 0)


def _domain_levels(be_stories, fe_group):
    """Return (be_level, fe_level, gates, crit, by_short) — the SAME computation
    generate_project_plan.domain_plan_lines does, so steps line up with 00-sequencing.md."""
    waves, gates, crit = bd.compute_implementation_order(be_stories)
    be_level = {bd._short_id(s["id"]): i for i, wave in enumerate(waves, 1) for s in wave}
    by_short = {bd._short_id(s["id"]): s for s in be_stories}

    fe_level, stage, prev = {}, (fe.fe_stages(fe_group) if fe_group else {}), 0
    for n in sorted(set(stage.values())):
        stage_stories = [s for s in fe_group if stage[s["id"]] == n]
        lvl = prev + 1 if prev else 1
        for s in stage_stories:
            for d in s["depends"]:
                m = _BE_SHORT_RE.search(d)
                if m and m.group(1) in be_level:
                    lvl = max(lvl, be_level[m.group(1)] + 1)
                elif d in fe_level:
                    lvl = max(lvl, fe_level[d] + 1)
        for s in stage_stories:
            fe_level[s["id"]] = lvl
        prev = lvl
    return be_level, fe_level, gates, crit, by_short


def _fe_gate_stories(fe_group, by_short):
    """The set of BE short-ids that at least one FE story in this domain directly waits on —
    i.e. exactly what the BE engineer must finish before the FE flip can begin."""
    gate = set()
    for s in fe_group:
        for d in s["depends"]:
            m = _BE_SHORT_RE.search(d)
            if m and m.group(1) in by_short:
                gate.add(m.group(1))
    return gate


def domain_block(dom, be_stories, fe_group, be_seg, fe_seg, fe_gatetxt, idx):
    label = fe.DOMAIN_LABELS.get(dom, dom.title())
    be_lane, be_start, be_end, gate_day = be_seg[dom]
    mid, ae, lo, hi, n_be = tp.be_domain_effort(dom)

    be_level, fe_level, gates, crit, by_short = _domain_levels(be_stories, fe_group)
    gate_ids = sorted(_fe_gate_stories(fe_group, by_short), key=_order_key)

    L = [
        f"## Domain {idx} — {label}",
        "",
        f"> **{n_be} BE + {len(fe_group)} FE stories** · {pp.ORDER_WHY.get(dom, '')}",
        "",
    ]

    # ── 1. Backend: build to the FE gate ─────────────────────────────────────
    L += [
        f"**① Backend builds first** — window **{tp._win(be_start, be_end)}** "
        f"(≈ {mid:.0f} days, {lo}–{hi}).",
        "",
        f"The backend engineer works this domain's phases in dependency steps. The frontend flip "
        f"can begin once the **A–E** stories the FE stories depend on are live (≈ **d{gate_day:.0f}** "
        f"— reads, search, writes); the trailing **F/G** federation stitches and field-resolver "
        f"parity land after the flip and don't block it.",
        "",
    ]
    if crit:
        L.append("- **Backend critical path (longest chain):** "
                 + " → ".join(f"`{k}`" for k in crit) + ".")
    scaffold = next((k for k in by_short
                     if "module init" in (by_short[k].get("note", "") + " "
                                           + by_short[k]["title"]).lower()), None)
    if scaffold:
        L.append(f"- **Starts with** `{scaffold}` — {_short_title(by_short[scaffold])} "
                 "(the module scaffold every other story waits on).")
    L.append("")

    # ── 2. The FE start gate — the specific BE stories that must ship first ───
    L += [
        f"**② Frontend can start after these backend stories ship** (the FE gate, ≈ d{gate_day:.0f}):",
        "",
        "| BE story | What it delivers | Unlocks FE |",
        "|---|---|---|",
    ]
    fe_by_gate: dict[str, list] = {g: [] for g in gate_ids}
    for s in fe_group:
        for d in s["depends"]:
            m = _BE_SHORT_RE.search(d)
            if m and m.group(1) in fe_by_gate:
                fe_by_gate[m.group(1)].append(s["id"])
    if gate_ids:
        for g in gate_ids:
            s = by_short[g]
            unlocked = ", ".join(f"`{x}`" for x in dict.fromkeys(fe_by_gate[g])) or "—"
            icon = bd.COMPLEXITY_ICONS.get(s["complexity"], "⚪")
            L.append(f"| {icon} `{g}` | {_short_title(s)} | {unlocked} |")
    else:
        L.append("| — | _No FE story in this domain names a backend dependency._ | — |")
    L.append("")

    # ── 3. Frontend cutover order ────────────────────────────────────────────
    if fe_group:
        fe_lane, fe_start, fe_end = fe_seg[dom]
        L += [
            f"**③ Frontend cutover** — window **{tp._win(fe_start, fe_end)}**, gated by: "
            f"{fe_gatetxt.get(dom, 'BE ' + label + ' A–E done')}.",
            "",
            "Reads flip first, then writes, then the multi-step saga — one FE story per stage:",
            "",
            "| Stage | FE story | Waits on (BE) |",
            "|---|---|---|",
        ]
        for s in sorted(fe_group, key=lambda s: (fe_level[s["id"]], s["id"])):
            deps = [m.group(1) for d in s["depends"]
                    if (m := _BE_SHORT_RE.search(d)) and m.group(1) in by_short]
            deps = sorted(dict.fromkeys(deps), key=_order_key)
            dep_txt = ", ".join(f"`{d}`" for d in deps) or "—"
            icon = fe._impact_icon(s["impact"])
            L.append(f"| {fe_level[s['id']]} | {icon} `{s['id']}` — {_short_title(s, 40)} | {dep_txt} |")
        L += [
            "",
            f"- **FE cutover flow:** "
            + " → ".join(f"`{s['id']}`"
                         for s in sorted(fe_group, key=lambda s: (fe_level[s["id"]], s["id"])))
            + ".",
        ]
    else:
        L += ["**③ Frontend cutover** — _no frontend stories recorded for this domain._"]

    # ── 4. Domain done ───────────────────────────────────────────────────────
    dom_done = fe_seg[dom][2] if fe_group else be_end
    L += [
        "",
        f"**④ Domain done ≈ d{dom_done:.0f} (sprint {tp._sprint(dom_done)})** — the last FE story is "
        "flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while "
        "the backend engineer is already on the next domain.",
        "",
        "---",
        "",
    ]
    return L


def build() -> str:
    labels = fe.DOMAIN_LABELS

    # ── recompute the exact BE + FE segments the team plan produces ──────────
    be = {d: tp.be_domain_effort(d) for d in BE_QUEUE}
    be_items = [(dom, be[dom][0], 0.0) for dom in BE_QUEUE]
    be_pack = tp._pack_lanes(be_items, N_BE_ENGINEERS)
    be_seg = {dom: (be_pack[dom][0], be_pack[dom][1], be_pack[dom][2],
                    be_pack[dom][1] + be[dom][1]) for dom in BE_QUEUE}

    fes = tp.fe_domain_effort(fe.parse_fe_stories())
    fe_items = []
    for wave, dom in FE_WAVES:
        if dom not in fes:
            continue
        gate_day = be_seg[dom][3] if dom in be_seg else 0.0
        fe_items.append((wave, dom, fes[dom][0], gate_day,
                         f"BE {labels.get(dom, dom)} A–E done (d{gate_day:.0f})"))
    wave1 = [(dom, days, floor) for wv, dom, days, floor, _ in fe_items if wv == 1]
    seg1 = tp._pack_lanes(wave1, N_FE_ENGINEERS)
    soak_after = (max((s[2] for s in seg1.values()), default=0.0) + SPRINT_DAYS) if seg1 else None
    rest, gate_txt_of = [], {}
    for wave, dom, days, floor, gate_txt in fe_items:
        if wave == 1:
            gate_txt_of[dom] = gate_txt
            continue
        if soak_after is not None and soak_after > floor:
            floor = soak_after
            gate_txt += f" + pilot soak (d{soak_after:.0f})"
        gate_txt_of[dom] = gate_txt
        rest.append((dom, days, floor))
    seg2 = tp._pack_lanes(rest, N_FE_ENGINEERS)
    fe_seg = {**seg1, **seg2}

    program_end = max([s[2] for s in fe_seg.values()] + [s[2] for s in be_seg.values()], default=0.0)

    # domain order = the FE flip order (this doc is organized around the cutover)
    domain_order = [dom for _wv, dom in FE_WAVES if dom in fes] + \
                   [dom for dom in BE_QUEUE if dom not in fes]

    parsed = {}
    for dom in domain_order:
        try:
            parsed[dom] = [s for s in bd.parse_stories(bd.get_domain_dir(dom) / "be-04-stories.md")
                           if s.get("phase") != "S"]
        except Exception:
            parsed[dom] = []
    fe_groups: dict[str, list] = {}
    for s in fe.parse_fe_stories():
        fe_groups.setdefault(fe.domain_key_from_token(s["id"].rsplit("-FE-", 1)[0]), []).append(s)

    L = [
        f"# Domain-by-Domain Rollout — {N_BE_ENGINEERS} BE + {N_FE_ENGINEERS} FE",
        "",
        f"> 🏷️ **Tags:** `dgs-migration` · `rollout-plan` — **Generated:** {TODAY} by "
        "`generate_domain_rollout.py` (runs inside `generate_all.py`). The same team and the same "
        "day math as [01-implementation-plan-" + PLAN_TAG + ".md](01-implementation-plan-" + PLAN_TAG
        + ".md), reorganized **one block per domain** in cutover order: what the **backend engineer** "
        "builds first → the exact **frontend start gate** → the **FE cutover** → domain done. "
        "Day figures are AI-estimated midpoints — confirm in refinement. 1 sprint = 10 days, d0 = start.",
        "",
        "## Operating model (1 BE + 1 FE)",
        "",
        "- **One backend engineer, one frontend engineer, working in parallel**, completing the "
        "program **domain by domain**.",
        "- The backend engineer runs the domains in `team_config.BE_QUEUE` order — **Product first** "
        "(host DGS + the shared `WriteSaga` module `PRODUCT-BE-E-00` that every other domain's write "
        "story is blocked on), then the rest.",
        "- For each domain the backend engineer builds its **phases A–E** (reads → search → writes). "
        "Once the specific A–E stories the FE stories depend on are live, the **frontend engineer "
        "starts the cutover for that domain** while the backend engineer moves on to the next domain.",
        "- Backend **F/G** stories (federation stitches, field-resolver parity) trail *behind* the "
        "flip — they don't gate it.",
        "- **Reads flip before writes before the multi-step saga** — the FE stage order inside each "
        "domain.",
        "- **Spikes (SPIKE-01…07)** run in the first 1–2 sprints alongside Product scaffold work; "
        "E-phase (saga) stories are gated on their outcomes.",
        "",
        "> **⚠ Priority reorder (2026-07-24):** an **external team is waiting on `watchlist` + "
        "`impression`**, so those are prioritized. Impression's **backend** is pulled far forward "
        f"(A–E gate ≈ d{be_seg['impression'][3]:.0f}, vs ~d520 in the pilot-first order) — that is "
        "what unblocks the external consumer of the federated impression data. Impression's "
        "**frontend**, though, is fused with BOM + Product screens "
        "(`getBomDataAndImpressions`, `getCarryForwardFormData`), so its FE flip can only happen "
        "in the same wave as BOM/Product, not before them — which is why `bom` and `product` core "
        "also move up and the smaller domains shift later. If the external team only needs the "
        "backend data, impression is effectively unblocked at its BE gate above, well before its FE "
        "cutover row. Order lives in `team_config.py` with a revert note.",
        "",
        f"**Bottom line:** ≈ **{tp._sprint(program_end)} sprints (~{tp._sprint(program_end) / 2:.0f} "
        f"months)** end-to-end with this 1 BE + 1 FE team; buffered (+20%) ≈ "
        f"{tp._sprint(program_end * 1.2)} sprints. The backend lane is the long pole — the frontend "
        "engineer is gate-bound (waiting on backend), not capacity-bound, so between flips they run "
        "parity dashboards, dual-run monitoring, rollback drills, and pre-pull the next domain's prep.",
        "",
        "---",
        "",
    ]

    for i, dom in enumerate(domain_order, 1):
        L += domain_block(dom, parsed[dom], fe_groups.get(dom, []),
                          be_seg, fe_seg, gate_txt_of, i)

    L += [
        "## How this reconciles with the other docs",
        "",
        "- Same numbers, two-lane view: [01-implementation-plan-" + PLAN_TAG + ".md]"
        "(01-implementation-plan-" + PLAN_TAG + ".md) (backend lane + frontend lane tables).",
        "- Step/edge detail per story: [00-sequencing.md](00-sequencing.md) and the compact "
        "[00-dependency-map.md](00-dependency-map.md) / [03-linear-dependency-map.md](03-linear-dependency-map.md).",
        "- Cross-domain gates (the ⛔ blockers, e.g. every domain's `E-01` waiting on "
        "`PRODUCT-BE-E-00`): [cross-domain-dependencies.md](../analysis/program/cross-domain-dependencies.md).",
        "- Team size + domain order: `team_config.py` — change there and regenerate.",
        "",
        "---",
        f"*Domain rollout plan · generated {TODAY} by generate_domain_rollout.py.*",
    ]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    content = build()
    out = OUT / f"01b-domain-rollout-{PLAN_TAG}.md"
    out.write_text(content, encoding="utf-8")
    print(f"  OK 01b-domain-rollout-{PLAN_TAG}.md ({len(content):,} chars)")


if __name__ == "__main__":
    main()
