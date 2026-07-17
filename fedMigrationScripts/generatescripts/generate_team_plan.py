#!/usr/bin/env python3
"""
Program-level implementation plan for a fixed team of 2 backend + 2 frontend engineers.

Builds output/summary/01-implementation-plan-2BE-2FE.md (+ .docx twin) from the same
parsers as the per-domain breakdowns (grouped-XS merges included), so all numbers
reconcile with the domain pages and the Jira CSVs.

Model (kept deliberately simple — refine in planning):
  BE-1  owns Product end-to-end (host DGS, largest surface, shared wiring).
  BE-2  runs the co-located/small domains in FE-wave-feeding order:
        watchlist → productDetails → measurement → packaging → bom → claims → impression,
        then joins BE-1 on Product.
  FE gate per domain = that domain's backend phases A–E delivered (reads+writes live);
        F/G (federation stitches, field-resolver parity) trail behind the cutover.
  FE-1/FE-2 follow the program waves (fe-10): watchlist pilot (+1 sprint soak) →
        PDTL/MST/PKG in parallel → BOM + Claims → Product (split across both) + Impression riders.

Day figures are nominal midpoints of the per-complexity ranges (EFFORT_DAYS) —
AI-estimated, confirm in refinement. 1 sprint = 10 working days.
"""

import importlib.util
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT  = ROOT / "output" / "summary"

SPRINT_DAYS = 10


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
    spec.loader.exec_module(mod)                          # type: ignore[union-attr]
    return mod


bd = _load("generate_breakdown")
fe = _load("generate_frontend")

BE1_QUEUE = ["product", "claims", "impression"]
BE2_QUEUE = ["watchlist", "productDetails", "measurement", "packaging", "bom"]

# (wave, domain, engineer) — "both" splits the domain across FE-1 and FE-2.
FE_PLAN = [
    (1, "watchlist",      "FE-1"),
    (2, "productDetails", "FE-1"),
    (2, "measurement",    "FE-2"),
    (2, "packaging",      "FE-2"),
    (3, "bom",            "FE-1"),
    (3, "claims",         "FE-2"),
    (4, "product",        "both"),
    (4, "impression",     "FE-2"),
]


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


def build_team_plan() -> str:
    today = date.today().isoformat()
    be = {d: be_domain_effort(d) for d in BE1_QUEUE + BE2_QUEUE}
    fes = fe_domain_effort(fe.parse_fe_stories())
    labels = fe.DOMAIN_LABELS

    # ── backend lanes ────────────────────────────────────────────────────────
    seg = {}                                   # dom -> (lane, start, end, gate_day)
    t = 0.0
    for dom in BE1_QUEUE:
        mid, ae, *_ = be[dom]
        seg[dom] = ("BE-1", t, t + mid, t + ae)
        t += mid
    be1_end = t
    t = 0.0
    for dom in BE2_QUEUE:
        mid, ae, *_ = be[dom]
        seg[dom] = ("BE-2", t, t + mid, t + ae)
        t += mid
    be2_end = t

    be_end = max(be1_end, be2_end)

    # ── frontend lanes ───────────────────────────────────────────────────────
    free = {"FE-1": 0.0, "FE-2": 0.0}
    fe_rows = []                               # (wave, dom, eng, days, gate_txt, start, end)
    soak_after = None                          # watchlist pilot + 1 sprint soak gates wave 2
    for wave, dom, eng in FE_PLAN:
        if dom not in fes:
            continue
        days = fes[dom][0]
        gate_day = seg[dom][3] if dom in seg else 0.0
        gate_txt = f"BE {labels.get(dom, dom)} A–E done (d{gate_day:.0f})"
        floor_day = gate_day
        if wave >= 2 and soak_after is not None:
            if soak_after > floor_day:
                floor_day = soak_after
                gate_txt += f" + pilot soak (d{soak_after:.0f})"
        if eng == "both":
            start = max(floor_day, max(free.values()))
            end = start + days / 2
            free["FE-1"] = free["FE-2"] = end
        else:
            start = max(floor_day, free[eng])
            end = start + days
            free[eng] = end
        fe_rows.append((wave, dom, eng, days, gate_txt, start, end))
        if wave == 1:
            soak_after = end + SPRINT_DAYS     # exit criterion: one sprint on the router
    fe_end = max((r[6] for r in fe_rows), default=0.0)
    program_end = max(fe_end, be_end)

    # ── emit ─────────────────────────────────────────────────────────────────
    L = [
        "# Implementation Plan — 2 Backend + 2 Frontend Engineers",
        "",
        f"> 🏷️ **Tags:** `dgs-migration` · `team-plan` — **Generated:** {today} · "
        "Derived from the same story parsers as the per-domain breakdowns (grouped-XS "
        "merges included), so story counts and day totals reconcile.",
        "> Day figures are **nominal midpoints of AI-estimated ranges — confirm in "
        "refinement.** 1 sprint = 10 working days. d0 = program start.",
        "",
        "---",
        "",
        "## Team & operating model",
        "",
        "- **BE-1** owns **Product** end-to-end (host DGS, shared wiring, largest surface — "
        "one owner avoids schema-merge churn), then takes **Claims** (the separate "
        "`spark-claims` subgraph) and the tiny **Impression** tail — this balances the two "
        "lanes to within a sprint of each other.",
        "- **BE-2** runs the co-located domains **in the order the FE waves need them**: "
        "watchlist → productDetails → measurement → packaging → bom.",
        "- **FE-1 / FE-2** follow the program waves (fe-10): watchlist pilot first "
        "(1-sprint production soak is the wave-2 entry gate), then parallel domain "
        "cutovers, Product split across both engineers last.",
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
        "## Backend lanes",
        "",
        "| Lane | # | Domain | Stories | Est. days (lo–hi) | Day window | FE gate (A–E done) |",
        "|---|---|---|---|---|---|---|",
    ]
    for lane, queue in (("👤 BE-1", BE1_QUEUE), ("👤 BE-2", BE2_QUEUE)):
        for i, dom in enumerate(queue, 1):
            mid, ae, lo, hi, n = be[dom]
            _, start, end, gate = seg[dom]
            L.append(f"| {lane} | {i} | **{labels.get(dom, dom)}** | {n} | "
                     f"{mid:.0f} ({lo}–{hi}) | {_win(start, end)} | d{gate:.0f} |")
    L += [
        "",
        f"- Lanes are load-balanced: **BE-1 drains at d{be1_end:.0f}**, **BE-2 at "
        f"d{be2_end:.0f}** — whoever frees first picks up post-launch F-phase stitches, "
        "G-phase parity leftovers, and pairs on the other lane's remaining domain.",
        "- Cross-subgraph F-phase stories that wait on later-phase domains "
        "(attachment/discussion/sample/search subgraphs) are excluded from these gates — "
        "they land post-launch when the owning subgraph exists.",
        "",
        "---",
        "",
        "## Frontend lanes",
        "",
        "| Wave | Domain | Engineer | FE days | Waits for | Day window |",
        "|---|---|---|---|---|---|",
    ]
    for wave, dom, eng, days, gate_txt, start, end in fe_rows:
        eng_txt = "FE-1 + FE-2" if eng == "both" else eng
        L.append(f"| {wave} | **{labels.get(dom, dom)}** | 👤 {eng_txt} | {days:.0f} | "
                 f"{gate_txt} | {_win(start, end)} |")
    L += [
        "",
        "- FE engineers are gate-bound, not capacity-bound — between gates they pair on "
        "parity dashboards, dual-run monitoring and rollback drills, and pre-pull the next "
        "domain's fragment/codegen prep.",
        "- Search-gated stories (`MST-FE-002`, `BOM-FE-003`, `PRODUCT-FE-003`) also wait on "
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
        f"| 🧱 All backend lanes drained (both subgraphs schema-complete) | d{be_end:.0f} | {_sprint(be_end)} |",
        f"| ✅ All FE cutovers flipped | d{fe_end:.0f} | {_sprint(fe_end)} |",
        f"| **Program complete (excl. post-launch F-phase)** | **d{program_end:.0f}** | **{_sprint(program_end)}** |",
        "",
        f"> ≈ **{_sprint(program_end)} sprints (~{_sprint(program_end) / 2:.0f} months)** "
        "with this team, vs the sequential single-pair estimate in 00-program-overview.md. "
        "Buffered (+20%) planning figure: "
        f"~{_sprint(program_end * 1.2)} sprints.",
        "",
        "---",
        "",
        "## How to read this with the other docs",
        "",
        "- Per-domain lane detail: **Recommended Story Graph — 2 Backend Engineers** in each "
        "`FederatedGqlBreakDown-BE-{domain}` page, and **— 2 Frontend Engineers** in each "
        "`FederatedGqlBreakDown-FE-{domain}` page.",
        "- Dependency-only view (no team constraint): **Recommended Implementation Order** "
        "on the same pages.",
        "- Program waves and external gates: `analysis/program/fe-10-migration-sequencing.md`.",
        "",
        "---",
        f"*Team plan · generated {today} by generate_team_plan.py.*",
    ]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    content = build_team_plan()
    out = OUT / "01-implementation-plan-2BE-2FE.md"
    out.write_text(content, encoding="utf-8")
    print(f"  OK 01-implementation-plan-2BE-2FE.md ({len(content):,} chars)")

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
        doc.save(str(OUT / "01-implementation-plan-2BE-2FE.docx"))
        print("  OK 01-implementation-plan-2BE-2FE.docx")
    except Exception as e:                     # pragma: no cover — md is the deliverable
        print(f"  (docx twin skipped: {type(e).__name__}: {e})")


if __name__ == "__main__":
    main()
