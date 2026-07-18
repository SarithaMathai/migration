#!/usr/bin/env python3
"""
Story-level project plan — the combined BACKEND + FRONTEND implementation order,
domain by domain, in one sequence per domain.

Builds output/summary/02-project-plan.md (+ .docx twin) from the same parsers as the
breakdowns (grouped-XS merges included), so ids and counts match every other page.

Ordering rules (per domain):
  • Backend steps come from the story dependency graph (Kahn levels — same engine as
    each breakdown's "Recommended Implementation Order").
  • A frontend story slots into the earliest step AFTER all its backend dependencies,
    while keeping the cutover discipline sequential: reads flip before writes before
    sagas (the FE stage order from the FE breakdown pages).
  • Domains run in the program cutover order (pilot first, Product last) — staffing and
    calendar for the team live in 01-implementation-plan-{N_BE_ENGINEERS}BE-{N_FE_ENGINEERS}FE.md
    (team size set in team_config.py).
"""

import importlib.util
import re
from datetime import date
from pathlib import Path

from team_config import N_BE_ENGINEERS, N_FE_ENGINEERS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT  = ROOT / "output" / "summary"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
    spec.loader.exec_module(mod)                          # type: ignore[union-attr]
    return mod


bd = _load("generate_breakdown")
fe = _load("generate_frontend")

# Program cutover order — watchlist pilot first, Product last, Impression riding its
# partner flips. Same sequencing rationale as the team plan + fe-10.
DOMAIN_ORDER = ["watchlist", "productDetails", "measurement", "packaging",
                "bom", "claims", "product", "impression"]
ORDER_WHY = {
    "watchlist":      "Wave 1 pilot — smallest isolated surface; proves flag flip + rollback",
    "productDetails": "Wave 2 — small, isolated, no shared blockers",
    "measurement":    "Wave 2 — parallel with Product Details",
    "packaging":      "Wave 2 — parallel with the other wave-2 domains",
    "bom":            "Wave 3 — high complexity, search-gated list views",
    "claims":         "Wave 3 — first cross-subgraph cutover (`spark-claims`)",
    "product":        "Wave 4 — largest surface, incremental slices, orchestrated writes last",
    "impression":     "Wave 4 rider — flips with its partner domains (BOM / Product)",
}

_BE_SHORT_RE = re.compile(r"-BE-([A-H]-\d+(?:-\d+)?)$")


def _fe_by_domain():
    groups: dict[str, list] = {}
    for s in fe.parse_fe_stories():
        groups.setdefault(fe.domain_key_from_token(s["id"].rsplit("-FE-", 1)[0]), []).append(s)
    return groups


def _short_title(story: dict, width: int = 40) -> str:
    t = re.sub(r"\(.*?\)", "", story["title"]).replace("`", "").strip()
    return (t[: width - 1] + "…") if len(t) > width else t


def domain_plan_lines(dom: str, be_stories: list[dict], fe_group: list[dict]) -> list[str]:
    label = fe.DOMAIN_LABELS.get(dom, dom.title())
    waves, gates, crit = bd.compute_implementation_order(be_stories)
    be_level = {bd._short_id(s["id"]): i for i, wave in enumerate(waves, 1) for s in wave}

    # FE stories: earliest step after their BE deps, kept sequential by cutover stage
    # (reads → search → writes → sagas — the FE breakdown's staged order).
    fe_level: dict[str, int] = {}
    fe_notes: dict[str, list] = {}
    stage = fe.fe_stages(fe_group) if fe_group else {}
    prev_lvl = 0
    for n in sorted(set(stage.values())):
        stage_stories = [s for s in fe_group if stage[s["id"]] == n]
        lvl = prev_lvl + 1 if prev_lvl else 1
        for s in stage_stories:
            for d in s["depends"]:
                m = _BE_SHORT_RE.search(d)
                if m and m.group(1) in be_level:
                    lvl = max(lvl, be_level[m.group(1)] + 1)
                elif d in fe_level:
                    lvl = max(lvl, fe_level[d] + 1)
                elif "-FE-" in d and not any(o["id"] == d for o in fe_group):
                    fe_notes.setdefault(s["id"], []).append(f"cross-domain: rides `{d}`")
        for s in stage_stories:
            fe_level[s["id"]] = lvl
        prev_lvl = lvl

    n_steps = max([*be_level.values(), *fe_level.values()], default=0)
    be_days = sum(sum(bd.EFFORT_DAYS.get(s["complexity"], (2, 4))) / 2 for s in be_stories)
    fe_days = sum(sum(fe._effort_range(s["effort"])) / 2 for s in fe_group)
    owners = bd.DOMAIN_OWNERS.get(dom, {"be": "BE-?", "fe": "FE-?"})
    by_short = {bd._short_id(s["id"]): s for s in be_stories}
    fe_by_id = {s["id"]: s for s in fe_group}

    # ── roadmap (spec: at the beginning of each domain) ──────────────────────
    def _wave_cell(wave):
        if len(wave) <= 4:
            return " ‖ ".join(f"`{bd._short_id(s['id'])}`" for s in wave)
        return (f"({len(wave)} in parallel: `{bd._short_id(wave[0]['id'])}` … "
                f"`{bd._short_id(wave[-1]['id'])}`)")

    be_flow = " → ".join(_wave_cell(w) for w in waves) or "—"
    fe_chain = []
    for n in sorted(set(fe_level.values())):
        ids = [s["id"] for s in sorted(fe_group, key=lambda s: s["id"]) if fe_level[s["id"]] == n]
        fe_chain.append(" ‖ ".join(f"`{i}`" for i in ids))
    first_fe_lvl = min(fe_level.values()) if fe_level else None

    L = [
        f"## {label}",
        "",
        f"> {ORDER_WHY.get(dom, '')} · **{len(be_stories)} BE + {len(fe_group)} FE stories** · "
        f"≈ {be_days:.0f} BE + {fe_days:.0f} FE nominal days · "
        f"**Owners:** Backend {owners['be']} · Frontend {owners['fe']}. "
        "Stories in the same step are independent and parallelize; a FE story never starts "
        "before every BE story it depends on is delivered.",
        "",
        "**Roadmap**",
        "",
        f"- **Backend ({owners['be']}):** {be_flow}",
    ]
    if fe_chain:
        unlock = ("step 1 (no backend dependency)" if first_fe_lvl == 1
                  else f"backend step {first_fe_lvl - 1}")
        L += [
            f"- **↓ unlocks frontend after {unlock}**",
            f"- **Frontend ({owners['fe']}):** " + " → ".join(fe_chain),
        ]
    L += [
        "",
        "| Step | 🛠️ Backend — build | 🖥️ Frontend — cutover | Gates / notes |",
        "|---|---|---|---|",
    ]
    for i in range(1, n_steps + 1):
        be_cell = ", ".join(
            f"{bd.COMPLEXITY_ICONS.get(s['complexity'], '⚪')} `{bd._short_id(s['id'])}`"
            for wave_i, wave in enumerate(waves, 1) if wave_i == i for s in wave) or "—"
        fe_cell = ", ".join(
            f"{fe._impact_icon(s['impact'])} `{s['id']}`"
            for s in sorted(fe_group, key=lambda s: s["id"]) if fe_level.get(s["id"]) == i) or "—"
        notes = []
        for wave_i, wave in enumerate(waves, 1):
            if wave_i != i:
                continue
            for s in wave:
                k = bd._short_id(s["id"])
                if k in gates:
                    notes.append(f"`{k}` → " + " · ".join(gates[k]))
        for s in fe_group:
            if fe_level.get(s["id"]) == i and s["id"] in fe_notes:
                notes.append(f"`{s['id']}` → " + " · ".join(fe_notes[s["id"]]))
        L.append(f"| {i} | {be_cell} | {fe_cell} | {'<br>'.join(notes) or '—'} |")

    # ── story sequence — one row per story, spec metadata ────────────────────
    # explicit dependency edges only (the implicit module-init edge is stated in prose)
    exp_deps: dict[str, list] = {}
    for k, s in by_short.items():
        exp_deps[k] = [d for d in dict.fromkeys(
            re.findall(r"\b(?:[A-Z]+-BE-)?([A-H]-\d+(?:-\d+)?)\b", s["depends"] or ""))
            if d in by_short and d != k]
    blocks: dict[str, list] = {k: [] for k in by_short}
    for k, ds in exp_deps.items():
        for d in ds:
            blocks[d].append(f"`{k}`")
    fe_blocks: dict[str, list] = {s["id"]: [] for s in fe_group}
    for s in fe_group:
        for d in s["depends"]:
            m = _BE_SHORT_RE.search(d)
            if m and m.group(1) in blocks:
                blocks[m.group(1)].append(f"`{s['id']}`")
            elif d in fe_blocks:
                fe_blocks[d].append(f"`{s['id']}`")

    step_pop: dict[int, int] = {}
    for k, lvl in be_level.items():
        step_pop[lvl] = step_pop.get(lvl, 0) + 1
    for sid, lvl in fe_level.items():
        step_pop[lvl] = step_pop.get(lvl, 0) + 1

    scaffold = {k for k, s in by_short.items()
                if "module init" in (s.get("note", "") + " " + s["title"]).lower()}

    entries = []           # (step, team_rank, sort_id, row cells...)
    for k, s in by_short.items():
        dep_cell = ", ".join(
            f"`{d}` — {_short_title(by_short[d], 24)}" for d in exp_deps[k]) or "None"
        blk = blocks[k]
        blk_cell = ("every story in this domain (module scaffold)" if k in scaffold
                    else (f"{len(blk)} stories: " + ", ".join(blk[:6]) + " …" if len(blk) > 6
                          else ", ".join(blk) or "None"))
        entries.append((be_level[k], 0, k, [
            f"{bd.COMPLEXITY_ICONS.get(s['complexity'], '⚪')} `{k}` — {_short_title(s)}",
            f"Backend · {owners['be']}",
            dep_cell, blk_cell,
            "Yes" if step_pop[be_level[k]] > 1 else "No",
        ]))
    for s in fe_group:
        dep_bits = []
        for d in s["depends"]:
            m = _BE_SHORT_RE.search(d)
            if m and m.group(1) in by_short:
                dep_bits.append(f"`{m.group(1)}` — {_short_title(by_short[m.group(1)], 24)}")
            elif d in fe_by_id:
                dep_bits.append(f"`{d}` — {_short_title(fe_by_id[d], 24)}")
            else:
                dep_bits.append(f"`{d}`")
        blk = fe_blocks[s["id"]]
        entries.append((fe_level[s["id"]], 1, s["id"], [
            f"{fe._impact_icon(s['impact'])} `{s['id']}` — {_short_title(s)}",
            f"Frontend · {owners['fe']}",
            ", ".join(dep_bits) or "None",
            ", ".join(blk) or "None",
            "Yes" if step_pop[fe_level[s["id"]]] > 1 else "No",
        ]))
    entries.sort(key=lambda e: (e[0], e[1], e[2]))

    L += [
        "",
        "### Story sequence",
        "",
        "> One row per story in implementation order. `Depends On`/`Blocks` reference story "
        "ids + names (never order numbers). Every operation story also implicitly requires "
        "the `B-01` module-init scaffold — not repeated per row. **Parallelizable = Yes** "
        "means other stories share its step.",
        "",
        "| Order | Step | Story | Team · Owner | Depends On | Blocks | ∥ |",
        "|---|---|---|---|---|---|---|",
    ]
    for order, (step, _rank, _sid, cells) in enumerate(entries, 1):
        L.append(f"| {order} | {step} | " + " | ".join(cells) + " |")

    if crit:
        L += ["", "**Backend critical path:** " + " → ".join(f"`{k}`" for k in crit) + "."]
    if fe_group:
        flow = " → ".join(f"`{s['id']}`" for s in sorted(fe_group, key=lambda s: (fe_level[s["id"]], s["id"])))
        L += [f"**Frontend cutover flow:** {flow}."]
    L += [
        "",
        f"**Domain done when:** the last FE story is flipped and stable; BE F/G stories "
        "(federation stitches, field-resolver parity) may trail post-flip.",
        "",
        "---",
        "",
    ]
    return L


def build_project_plan() -> str:
    today = date.today().isoformat()
    fe_groups = _fe_by_domain()
    L = [
        "# Project Plan — Combined Backend + Frontend Story Order",
        "",
        f"> 🏷️ **Tags:** `dgs-migration` · `project-plan` — **Generated:** {today} · "
        "One combined implementation sequence per domain: backend build steps from the story "
        "dependency graph, frontend cutovers slotted into the earliest step after their "
        "backend dependencies (reads flip before writes before sagas).",
        f"> Staffing + calendar for the {N_BE_ENGINEERS} BE + {N_FE_ENGINEERS} FE team: see "
        f"01-implementation-plan-{N_BE_ENGINEERS}BE-{N_FE_ENGINEERS}FE.md (team size set in "
        "team_config.py). Day figures are AI-estimated nominal midpoints — confirm in refinement.",
        "",
        "---",
        "",
        "## Domain order",
        "",
        "| # | Domain | Why here | BE stories | FE stories |",
        "|---|---|---|---|---|",
    ]
    parsed: dict[str, list] = {}
    for i, dom in enumerate(DOMAIN_ORDER, 1):
        try:
            stories = [s for s in bd.parse_stories(bd.get_domain_dir(dom) / "be-04-stories.md")
                       if s.get("phase") != "S"]
        except Exception:
            stories = []
        parsed[dom] = stories
        label = fe.DOMAIN_LABELS.get(dom, dom.title())
        L.append(f"| {i} | **{label}** | {ORDER_WHY.get(dom, '—')} | {len(stories)} | "
                 f"{len(fe_groups.get(dom, []))} |")
    L += [
        "",
        "> Wave-2/3 domains parallelize across the team — the numbering is the *flip* order. "
        "Phase-0 spikes (SPIKE-01…07) run before/alongside step 1 of the first domains; "
        "E-phase stories are gated on their outcomes.",
        "",
        "---",
        "",
    ]
    for dom in DOMAIN_ORDER:
        L += domain_plan_lines(dom, parsed[dom], fe_groups.get(dom, []))
    L += [f"*Project plan · generated {today} by generate_project_plan.py.*"]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    content = build_project_plan()
    out = OUT / "02-project-plan.md"
    out.write_text(content, encoding="utf-8")
    print(f"  OK 02-project-plan.md ({len(content):,} chars)")

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
        doc.save(str(OUT / "02-project-plan.docx"))
        print("  OK 02-project-plan.docx")
    except Exception as e:                     # pragma: no cover — md is the deliverable
        print(f"  (docx twin skipped: {type(e).__name__}: {e})")


if __name__ == "__main__":
    main()
