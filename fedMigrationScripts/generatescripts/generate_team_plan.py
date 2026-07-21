#!/usr/bin/env python3
"""
Program-level implementation plan for a configurable backend + frontend team.

Builds output/summary/01-implementation-plan-{n_be}BE-{n_fe}FE.md (+ .docx twin) from the
same parsers as the per-domain breakdowns (grouped-XS merges included), so all numbers
reconcile with the domain pages and the Jira CSVs.

Team size + domain sequencing are read from team_config.py — N_BE_ENGINEERS,
N_FE_ENGINEERS, BE_QUEUE, FE_WAVES. Change the team size or the domain order there and
regenerate; nothing in this file needs to change.

Model (kept deliberately simple — refine in planning):
  The backend queue (team_config.BE_QUEUE) is packed onto N_BE_ENGINEERS lanes by a
        greedy critical-path heuristic: each domain, in queue order, starts on whichever
        lane frees up soonest — with N_BE_ENGINEERS == 1 this collapses to one sequential
        lane through all 8 domains in queue order.
  FE gate per domain = that domain's backend phases A–E delivered (reads+writes live);
        F/G (federation stitches, field-resolver parity) trail behind the cutover.
  The frontend wave plan (team_config.FE_WAVES) is packed onto N_FE_ENGINEERS lanes the
        same way, additionally gated by each wave's own entry gate (e.g. wave 2 doesn't
        start before the wave-1 pilot's 1-sprint production soak ends).

Day figures are nominal midpoints of the per-complexity ranges (EFFORT_DAYS) —
AI-estimated, confirm in refinement. 1 sprint = 10 working days.
"""

import importlib.util
from datetime import date
from pathlib import Path

from team_config import N_BE_ENGINEERS, N_FE_ENGINEERS, BE_QUEUE, FE_WAVES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT  = ROOT / "output" / "summary"

SPRINT_DAYS = 10
PLAN_TAG = f"{N_BE_ENGINEERS}BE-{N_FE_ENGINEERS}FE"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
    spec.loader.exec_module(mod)                          # type: ignore[union-attr]
    return mod


bd = _load("generate_breakdown")
fe = _load("generate_frontend")


def _sprint(day: float) -> int:
    return int(day // SPRINT_DAYS) + 1


def _win(start: float, end: float) -> str:
    return f"d{start:.0f}–d{end:.0f} (spr {_sprint(start)}–{_sprint(max(end - 0.01, start))})"


def be_domain_effort(dom: str):
    """(midpoint_days, A–E midpoint_days, lo, hi, story_count) for one domain."""
    stories = [s for s in bd.parse_stories(bd.get_domain_dir(dom) / "be-04-stories.md")
               if s["phase"] != "S"]
    def rng(s): return bd.EFFORT_DAYS.get(s["complexity"], (2, 4))
    mid = sum(sum(rng(s)) / 2 for s in stories)
    ae  = sum(sum(rng(s)) / 2 for s in stories if s["phase"] in "ABCDE")
    lo  = sum(rng(s)[0] for s in stories)
    hi  = sum(rng(s)[1] for s in stories)
    return mid, ae, lo, hi, len(stories)


def fe_domain_effort(fe_stories):
    """{domain: (midpoint_days, lo, hi, count)} from fe-08 (dep-remapped parser)."""
    out: dict[str, list] = {}
    for s in fe_stories:
        k = fe.domain_key_from_token(s["id"].rsplit("-FE-", 1)[0])
        lo, hi = fe._effort_range(s["effort"])
        cur = out.setdefault(k, [0.0, 0, 0, 0])
        cur[0] += (lo + hi) / 2
        cur[1] += lo
        cur[2] += hi
        cur[3] += 1
    return out


def _pack_lanes(items: list[tuple], n_lanes: int) -> dict:
    """Greedy critical-path packing of (key, days, floor_day) items onto n_lanes parallel
    lanes, in the given queue order — mirrors generate_breakdown.py's _schedule_lanes
    heuristic (earliest-available lane, respecting each item's own floor/gate day) but
    over whole-domain effort blocks instead of individual stories.

    Returns {key: (lane_index, start, end)}."""
    lane_free = [0.0] * n_lanes
    seg: dict[str, tuple] = {}
    for key, days, floor_day in items:
        e = min(range(n_lanes), key=lambda i: max(lane_free[i], floor_day))
        start = max(lane_free[e], floor_day)
        end = start + days
        lane_free[e] = end
        seg[key] = (e, start, end)
    return seg


def build_team_plan() -> str:
    today = date.today().isoformat()
    be = {d: be_domain_effort(d) for d in BE_QUEUE}
    fes = fe_domain_effort(fe.parse_fe_stories())
    labels = fe.DOMAIN_LABELS

    # ── backend lanes ────────────────────────────────────────────────────────
    be_items = [(dom, be[dom][0], 0.0) for dom in BE_QUEUE]
    be_seg = _pack_lanes(be_items, N_BE_ENGINEERS)
    # gate day (A–E delivered) = lane-start + that domain's own A–E midpoint
    seg = {dom: (be_seg[dom][0], be_seg[dom][1], be_seg[dom][2],
                 be_seg[dom][1] + be[dom][1]) for dom in BE_QUEUE}
    be_end = max((s[2] for s in seg.values()), default=0.0)

    # ── frontend lanes ───────────────────────────────────────────────────────
    # Wave 1's pilot domain gates its own soak period onto every wave >= 2 domain's floor
    # day, same "pilot soak" rule as the single-lane version — computed once up front so
    # the packer can use it as part of each item's floor_day.
    wave1_doms = [dom for wv, dom in FE_WAVES if wv == 1 and dom in fes]
    fe_items = []
    for wave, dom in FE_WAVES:
        if dom not in fes:
            continue
        gate_day = seg[dom][3] if dom in seg else 0.0
        floor_day = gate_day
        gate_txt = f"BE {labels.get(dom, dom)} A–E done (d{gate_day:.0f})"
        fe_items.append((wave, dom, fes[dom][0], floor_day, gate_txt))

    # Two-pass: pack wave 1 first to learn the pilot's finish day, then apply the soak
    # floor to every wave >= 2 item before packing the rest — preserves the "1-sprint
    # production soak gates wave 2" rule from the single-lane model, generalized to N lanes.
    wave1 = [(dom, days, floor_day) for wv, dom, days, floor_day, _ in fe_items if wv == 1]
    seg1 = _pack_lanes(wave1, N_FE_ENGINEERS)
    soak_after = max((s[2] for s in seg1.values()), default=0.0) + SPRINT_DAYS if seg1 else None

    rest = []
    gate_txt_of = {}
    for wave, dom, days, floor_day, gate_txt in fe_items:
        if wave == 1:
            continue
        if soak_after is not None and soak_after > floor_day:
            floor_day = soak_after
            gate_txt += f" + pilot soak (d{soak_after:.0f})"
        gate_txt_of[dom] = gate_txt
        rest.append((dom, days, floor_day))
    seg2 = _pack_lanes(rest, N_FE_ENGINEERS)

    fe_seg = {**seg1, **seg2}
    fe_rows = []   # (wave, dom, lane, days, gate_txt, start, end)
    for wave, dom, days, floor_day, gate_txt in fe_items:
        lane, start, end = fe_seg[dom]
        fe_rows.append((wave, dom, lane, days, gate_txt_of.get(dom, gate_txt), start, end))
    fe_end = max((r[6] for r in fe_rows), default=0.0)
    program_end = max(fe_end, be_end)

    be_word = "Engineer" if N_BE_ENGINEERS == 1 else "Engineers"
    fe_word = "Engineer" if N_FE_ENGINEERS == 1 else "Engineers"

    # ── emit ─────────────────────────────────────────────────────────────────
    L = [
        f"# Implementation Plan — {N_BE_ENGINEERS} Backend + {N_FE_ENGINEERS} Frontend {fe_word}"
        if N_BE_ENGINEERS == N_FE_ENGINEERS else
        f"# Implementation Plan — {N_BE_ENGINEERS} Backend {be_word} + {N_FE_ENGINEERS} Frontend {fe_word}",
        "",
        f"> 🏷️ **Tags:** `dgs-migration` · `team-plan` — **Generated:** {today} · "
        "Derived from the same story parsers as the per-domain breakdowns (grouped-XS "
        "merges included), so story counts and day totals reconcile.",
        "> Day figures are **nominal midpoints of AI-estimated ranges — confirm in "
        "refinement.** 1 sprint = 10 working days. d0 = program start. Team size and "
        "domain sequencing are set in `team_config.py` — change them there and "
        "regenerate.",
        "",
        "---",
        "",
        "## Team & operating model",
        "",
    ]
    if N_BE_ENGINEERS == 1:
        L.append(
            "- **The backend engineer** runs all 8 domains sequentially: **Product** first "
            "(host DGS, shared wiring, largest surface — the foundation the rest build on), "
            "then the remaining domains in `team_config.BE_QUEUE` order.")
    else:
        L.append(
            f"- **{N_BE_ENGINEERS} backend engineers** work `team_config.BE_QUEUE` "
            "(product first — host DGS, shared wiring, largest surface) packed onto "
            f"{N_BE_ENGINEERS} parallel lanes by a greedy critical-path heuristic — each "
            "domain starts on whichever lane frees up soonest.")
    if N_FE_ENGINEERS == 1:
        L.append(
            "- **The frontend engineer** follows the program waves (fe-10) sequentially: "
            "watchlist pilot first (1-sprint production soak is the wave-2 entry gate), "
            "then each domain cutover in turn.")
    else:
        L.append(
            f"- **{N_FE_ENGINEERS} frontend engineers** follow the program waves (fe-10) — "
            "watchlist pilot first (1-sprint production soak is the wave-2 entry gate for "
            f"every lane), then wave 2+ domains packed onto {N_FE_ENGINEERS} parallel lanes "
            "by the same heuristic.")
    L += [
        "- A domain's FE cutover starts when its **backend phases A–E** (reads, search, "
        "writes) are live; BE phases F–G (federation stitches, field-resolver parity) "
        "trail behind the flip and don't block it. *(Refinement lever: FE read-stories "
        "can start dual-running right after B/C — that pulls each FE start earlier than "
        "shown here.)*",
        "- Phase-0 **spikes (SPIKE-01…07)** are not on these lanes — run them in the first "
        "1–2 sprints alongside `PRODUCT-BE` scaffold work; E-phase stories are gated on "
        "their outcomes.",
        "",
        "---",
        "",
        f"## Backend lane{'s' if N_BE_ENGINEERS > 1 else ''}",
        "",
        "| # | Domain | Lane | Stories | Est. days (lo–hi) | Day window | FE gate (A–E done) |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, dom in enumerate(BE_QUEUE, 1):
        mid, ae, lo, hi, n = be[dom]
        lane, start, end, gate = seg[dom]
        lane_txt = f"BE-{lane + 1}" if N_BE_ENGINEERS > 1 else "—"
        L.append(f"| {i} | **{labels.get(dom, dom)}** | {lane_txt} | {n} | "
                 f"{mid:.0f} ({lo}–{hi}) | {_win(start, end)} | d{gate:.0f} |")
    lane_drain = ", ".join(
        f"**BE-{e + 1} at d{max((s[2] for d, s in seg.items() if s[0] == e), default=0.0):.0f}**"
        for e in range(N_BE_ENGINEERS)
    ) if N_BE_ENGINEERS > 1 else f"**backend drains at d{be_end:.0f}**"
    L += [
        "",
        f"- {lane_drain} — post-launch F-phase stitches and G-phase parity leftovers land "
        "after the queue above" + (", whoever frees first picks up the other lane's "
        "remaining domain" if N_BE_ENGINEERS > 1 else "") + ".",
        "- Cross-subgraph F-phase stories that wait on later-phase domains "
        "(attachment/discussion/sample/search subgraphs) are excluded from these gates — "
        "they land post-launch when the owning subgraph exists.",
        "",
        "---",
        "",
        f"## Frontend lane{'s' if N_FE_ENGINEERS > 1 else ''}",
        "",
        "| Wave | Domain | Lane | FE days | Waits for | Day window |",
        "|---|---|---|---|---|---|",
    ]
    for wave, dom, lane, days, gate_txt, start, end in fe_rows:
        lane_txt = f"FE-{lane + 1}" if N_FE_ENGINEERS > 1 else "—"
        L.append(f"| {wave} | **{labels.get(dom, dom)}** | {lane_txt} | {days:.0f} | "
                 f"{gate_txt} | {_win(start, end)} |")
    fe_word_lower = "engineer is" if N_FE_ENGINEERS == 1 else "engineers are"
    L += [
        "",
        f"- The frontend {fe_word_lower} gate-bound, not capacity-bound — between gates "
        "they work parity dashboards, dual-run monitoring and rollback drills, and "
        "pre-pull the next domain's fragment/codegen prep.",
        "- Search-gated stories (`MST-FE-002`, `BOM-FE-003`, `PRODUCT-FE-002`) also wait on "
        "the search read-hub decision — external to this plan and may slide independently.",
        "- Impression rides its partner flips (`IMPRESSION-FE-001` with `BOM-FE-002`, "
        "`IMPRESSION-FE-002` with `PRODUCT-FE-001`).",
        "",
        "---",
        "",
        "## Milestones",
        "",
        "| Milestone | ≈ Day | ≈ Sprint |",
        "|---|---|---|",
    ]
    wl = next((r for r in fe_rows if r[1] == "watchlist"), None)
    cl = next((r for r in fe_rows if r[1] == "claims"), None)
    if wl:
        L.append(f"| 🚦 Watchlist pilot live on the router | d{wl[6]:.0f} | {_sprint(wl[6])} |")
    if cl:
        L.append(f"| 🔗 First cross-subgraph cutover (Claims FE) | d{cl[6]:.0f} | {_sprint(cl[6])} |")
    L += [
        f"| 🏁 Product backend complete (`plm-product` host) | d{seg['product'][2]:.0f} | {_sprint(seg['product'][2])} |",
        f"| 🧱 Backend lane{'s' if N_BE_ENGINEERS > 1 else ''} drained (both subgraphs schema-complete) | d{be_end:.0f} | {_sprint(be_end)} |",
        f"| ✅ All FE cutovers flipped | d{fe_end:.0f} | {_sprint(fe_end)} |",
        f"| **Program complete (excl. post-launch F-phase)** | **d{program_end:.0f}** | **{_sprint(program_end)}** |",
        "",
        f"> ≈ **{_sprint(program_end)} sprints (~{_sprint(program_end) / 2:.0f} months)** "
        f"with this {N_BE_ENGINEERS} BE + {N_FE_ENGINEERS} FE team — see "
        "00-program-overview.md for the program-level totals. Buffered (+20%) planning "
        f"figure: ~{_sprint(program_end * 1.2)} sprints.",
        "",
        "---",
        "",
        "## How to read this with the other docs",
        "",
        f"- Per-domain lane detail: **Recommended Story Graph — {N_BE_ENGINEERS} Backend "
        f"{be_word}** and **— {N_FE_ENGINEERS} Frontend {fe_word}** in the Backend / "
        "Frontend sections of each `FederatedGqlBreakDown-{domain}` page.",
        "- Dependency-only view (no team constraint): **Recommended Implementation Order** "
        "on the same pages.",
        "- Program waves and external gates: `analysis/program/fe-10-migration-sequencing.md`.",
        "- Team size and domain sequencing: `team_config.py`.",
        "",
        "---",
        f"*Team plan · generated {today} by generate_team_plan.py.*",
    ]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    content = build_team_plan()
    out = OUT / f"01-implementation-plan-{PLAN_TAG}.md"
    out.write_text(content, encoding="utf-8")
    print(f"  OK 01-implementation-plan-{PLAN_TAG}.md ({len(content):,} chars)")

    # .docx twin — same Markdown→Word renderer as the breakdown pages.
    try:
        gw = _load("generate_word")
        doc = gw.Document()
        style = doc.styles["Normal"]
        style.font.name = "Calibri"
        style.font.size = gw.Pt(10)
        lines = content.split("\n")
        tp = doc.add_paragraph()
        gw.add_run(tp, lines[0].lstrip("# "), bold=True, size_pt=20, color_hex=gw.C_TITLE)
        gw.render_md_block(doc, lines[1:])
        doc.save(str(OUT / f"01-implementation-plan-{PLAN_TAG}.docx"))
        print(f"  OK 01-implementation-plan-{PLAN_TAG}.docx")
    except Exception as e:                     # pragma: no cover — md is the deliverable
        print(f"  (docx twin skipped: {type(e).__name__}: {e})")


if __name__ == "__main__":
    main()
