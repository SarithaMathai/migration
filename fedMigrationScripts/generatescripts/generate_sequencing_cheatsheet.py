#!/usr/bin/env python3
"""
Sequencing cheat-sheet — the condensed one-page distillation of the four plan docs
(00-sequencing.md, 00-dependency-map.md, 00-domain-rollout.md, 01-implementation-plan-*.md).

The only two things a reader needs from here: **the domain order, and the order stories are
implemented within each domain.** No day windows, no dependency chains, no per-story tables —
just a flat, numbered "do these in this order" list per domain: backend build steps (grouped by
dependency step, parallelizable within a step), the frontend-start gate, then the frontend cutover.

ACCURACY BY REUSE — same engine as the other plans, nothing re-derived:
  • Domain order = team_config.FE_WAVES (the FE flip order) + any BE-only tail — identical to
    generate_project_plan.DOMAIN_ORDER.
  • Backend step grouping = bd.compute_implementation_order (Kahn levels).
  • FE staging + the FE-start gate = the same computation as generate_domain_rollout / project_plan.
So this page can never disagree with the four it condenses; regenerate all together.

Output: output/summary/00-sequencing-cheatsheet.md
        (generate_all.py copies it to finalArtifacts/00-cheatsheet.md)

Run:
    python fedMigrationScripts/generatescripts/generate_sequencing_cheatsheet.py
"""

import importlib.util
import re
from datetime import date
from pathlib import Path

from team_config import N_BE_ENGINEERS, N_FE_ENGINEERS, FE_WAVES, BE_QUEUE

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "output" / "summary"
TODAY = date.today().isoformat()

def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
    spec.loader.exec_module(mod)                          # type: ignore[union-attr]
    return mod

bd = _load("generate_breakdown")
fe = _load("generate_frontend")
pp = _load("generate_project_plan")     # reuse DOMAIN_ORDER + ORDER_WHY

_BE_SHORT_RE = re.compile(r"-BE-([A-H]-\d+(?:-\d+)?)$")


def _order_key(short_id: str) -> tuple:
    m = re.match(r"([A-H])-(\d+)(?:-(\d+))?$", short_id)
    return (bd.PHASE_SEQ.find(m.group(1)), int(m.group(2)), int(m.group(3) or 0)) if m else (99, 0, 0)


def _levels(be_stories, fe_group):
    """(be_waves_by_step, fe_by_step, gate_ids, by_short) — the same steps/gate the rollout uses."""
    waves, gates, crit = bd.compute_implementation_order(be_stories)
    be_level = {bd._short_id(s["id"]): i for i, w in enumerate(waves, 1) for s in w}
    by_short = {bd._short_id(s["id"]): s for s in be_stories}

    fe_level, stage, prev = {}, (fe.fe_stages(fe_group) if fe_group else {}), 0
    for n in sorted(set(stage.values())):
        grp = [s for s in fe_group if stage[s["id"]] == n]
        lvl = prev + 1 if prev else 1
        for s in grp:
            for d in s["depends"]:
                m = _BE_SHORT_RE.search(d)
                if m and m.group(1) in be_level:
                    lvl = max(lvl, be_level[m.group(1)] + 1)
                elif d in fe_level:
                    lvl = max(lvl, fe_level[d] + 1)
        for s in grp:
            fe_level[s["id"]] = lvl
        prev = lvl

    # BE stories grouped by step, ordered within a step by phase id
    be_by_step: dict[int, list] = {}
    for k in by_short:
        be_by_step.setdefault(be_level[k], []).append(k)
    for step in be_by_step:
        be_by_step[step].sort(key=_order_key)

    fe_by_step: dict[int, list] = {}
    for s in fe_group:
        fe_by_step.setdefault(fe_level[s["id"]], []).append(s["id"])
    for step in fe_by_step:
        fe_by_step[step].sort()

    # FE-start gate = the BE stories at least one FE story directly waits on
    gate_ids = set()
    for s in fe_group:
        for d in s["depends"]:
            m = _BE_SHORT_RE.search(d)
            if m and m.group(1) in by_short:
                gate_ids.add(m.group(1))
    return be_by_step, fe_by_step, sorted(gate_ids, key=_order_key), by_short, crit


def _icon(k, by_short):
    return bd.COMPLEXITY_ICONS.get(by_short[k]["complexity"], "⚪")


def domain_block(idx, dom, be_stories, fe_group):
    label = fe.DOMAIN_LABELS.get(dom, dom.title())
    be_by_step, fe_by_step, gate_ids, by_short, crit = _levels(be_stories, fe_group)

    last_be_step = max(be_by_step) if be_by_step else 0

    L = [f"### {idx}. {label} — {len(be_stories)} BE + {len(fe_group)} FE", ""]

    # Backend, step by step (a step = do-in-any-order; steps go top to bottom)
    L.append("**Backend — build in this step order** (`BE-n`; ids in the same step are parallel):")
    L.append("")
    for step in sorted(be_by_step):
        ids = be_by_step[step]
        cells = ", ".join(f"{_icon(k, by_short)} `{k}`" for k in ids)
        L.append(f"- **BE-{step}.** {cells}")
    L.append("")

    # FE-start gate — state it as a step threshold, not a 50-id list. The gate day equals the
    # last BE step any FE story waits on; anything up to that step being done opens the gate.
    if gate_ids and fe_group:
        gate_step = max(be_level_of(g, be_by_step) for g in gate_ids)
        if len(gate_ids) <= 8:
            gate_txt = ", ".join(f"`{g}`" for g in gate_ids)
            L.append(f"**▶ Frontend starts once these ship:** {gate_txt} "
                     f"(all within **BE-{gate_step}**).")
        else:
            L.append(f"**▶ Frontend starts once backend steps BE-1…BE-{gate_step} are done** "
                     f"({len(gate_ids)} stories — essentially this domain's reads/writes/field "
                     "resolvers; the trailing F/G stitches can lag).")
        L.append("")

    # Frontend cutover order — renumber FE stages 1..k so they don't visually collide with the
    # BE step numbers (they share a global scale internally, but for a reader "FE-1, FE-2…" is clearer).
    if fe_group:
        L.append("**Frontend — cutover in this order** (reads → writes → saga):")
        L.append("")
        for fe_stage, step in enumerate(sorted(fe_by_step), 1):
            cells = ", ".join(f"`{i}`" for i in fe_by_step[step])
            L.append(f"- **FE-{fe_stage}.** {cells}")
        L.append("")
    else:
        L += ["_No frontend stories in this domain._", ""]

    return L


def be_level_of(short_id, be_by_step):
    for step, ids in be_by_step.items():
        if short_id in ids:
            return step
    return 0


def build() -> str:
    fe_groups: dict[str, list] = {}
    for s in fe.parse_fe_stories():
        fe_groups.setdefault(fe.domain_key_from_token(s["id"].rsplit("-FE-", 1)[0]), []).append(s)
    parsed = {}
    for dom in pp.DOMAIN_ORDER:
        try:
            parsed[dom] = [s for s in bd.parse_stories(bd.get_domain_dir(dom) / "be-04-stories.md")
                           if s.get("phase") != "S"]
        except Exception:
            parsed[dom] = []

    L = [
        "# Sequencing Cheat-Sheet — what order to build",
        "",
        f"> 🏷️ `dgs-migration` · `cheatsheet` — **Generated:** {TODAY} by "
        "`generate_sequencing_cheatsheet.py` (in `generate_all.py`). The condensed one-pager: "
        "**domain order + the order stories are implemented.** For day windows / calendar see "
        "[00-domain-rollout.md](00-domain-rollout.md) & [01-implementation-plan-"
        f"{N_BE_ENGINEERS}BE-{N_FE_ENGINEERS}FE.md](01-implementation-plan-"
        f"{N_BE_ENGINEERS}BE-{N_FE_ENGINEERS}FE.md); for full per-story dependency detail see "
        "[00-sequencing.md](00-sequencing.md) / [00-dependency-map.md](00-dependency-map.md).",
        "",
        "**How to read it:** domains are listed in cutover order. Within a domain, do the backend "
        "steps `BE-1, BE-2, …` top to bottom — **ids in the same step have no dependency on each "
        "other and can be done in any order / in parallel;** finish a step before starting the next. "
        "`▶` marks when the frontend engineer can start. Then do the frontend stages `FE-1, FE-2, …` "
        "in order (reads flip before writes before the multi-step saga). Complexity: 🔴 very high · "
        "🟠 high · 🟡 medium · 🟢 low.",
        "",
        "> **⚠ Order reprioritized 2026-07-24** for an external team waiting on `watchlist` + "
        "`impression`. Impression's FE is fused with BOM + Product screens, so those move up too. "
        "Order is set in `team_config.py`.",
        "",
        "---",
        "",
        "## Domain order",
        "",
        "| # | Domain | Why here | BE | FE |",
        "|---|---|---|---|---|",
    ]
    for i, dom in enumerate(pp.DOMAIN_ORDER, 1):
        L.append(f"| {i} | **{fe.DOMAIN_LABELS.get(dom, dom)}** | {pp.ORDER_WHY.get(dom, '—')} | "
                 f"{len(parsed[dom])} | {len(fe_groups.get(dom, []))} |")
    L += ["", "---", "", "## Story order, domain by domain", ""]

    for i, dom in enumerate(pp.DOMAIN_ORDER, 1):
        L += domain_block(i, dom, parsed[dom], fe_groups.get(dom, []))
        L += ["---", ""]

    L += [
        "**Cross-domain note:** every domain's `E-01` write story needs product's `PRODUCT-BE-E-00` "
        "(shared WriteSaga) first — product is built first, so it's ready in time. Impression's "
        "`F-01` and BOM/Product FE cross-links are handled by the domain order above.",
        "",
        f"*Sequencing cheat-sheet · generated {TODAY} by generate_sequencing_cheatsheet.py.*",
    ]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    content = build()
    out = OUT / "00-sequencing-cheatsheet.md"
    out.write_text(content, encoding="utf-8")
    print(f"  OK 00-sequencing-cheatsheet.md ({len(content):,} chars)")


if __name__ == "__main__":
    main()
