#!/usr/bin/env python3
"""
Compact linear dependency map — one row per story (BACKEND + FRONTEND together), the whole
dependency rendered as a single left-to-right chain string instead of the wide two-column
Depends/Blocks pair in 00-sequencing.md.

Design goals (the review criteria): **compact, easy to follow, accurate.**
  • compact   — 5 narrow columns, one row per story, no per-story mermaid; a 44-story domain
                fits on far less vertical space than the 7-wide sequence table.
  • easy      — the dependency reads as a linear chain "A ▸ B ▸ this", left to right; bare ids
                are same-domain, `⛔ID` is a cross-domain/subgraph gate, `🔬 SPIKE-n` is spike-
                gated. One "Unlocks" column shows the immediate downstream, so you can walk the
                graph in either direction without cross-referencing a second table.
  • accurate  — NOTHING here re-parses rendered markdown or invents an edge. It reuses the SAME
                engine as generate_project_plan.py / 00-sequencing.md: bd.compute_implementation_order
                for the backend Kahn levels, fe.fe_stages for the FE cutover staging, and the
                same _BE_SHORT_RE dependency extraction. Steps and edges match 00-sequencing.md
                row-for-row by construction — if that doc changes, regen this and they stay in sync.

The "Depends chain" is the story's DIRECT predecessors only (not a transitive walk) — the same
choice generate_story_dependency_graphs.py makes, and for the same reason: walking the full
upstream chain makes the module-init scaffold fan out to nearly every node and stops being a
"linear, compact" view. The implicit scaffold (`B-01`) edge is stated once in prose, not repeated
per row, exactly as 00-sequencing.md does.

Output: output/summary/03-linear-dependency-map.md
        (generate_all.py copies it to finalArtifacts/00-dependency-map.md)

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_linear_deps.py            # all domains
    python fedMigrationScripts/generatescripts/generate_linear_deps.py watchlist  # one domain
"""

import importlib.util
import re
import sys
from datetime import date
from pathlib import Path

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
pp = _load("generate_project_plan")   # reuse its DOMAIN_ORDER / ORDER_WHY so the two docs agree

_BE_SHORT_RE = re.compile(r"-BE-([A-H]-\d+(?:-\d+)?)$")
ARROW = " ▸ "


def _gate_tag(gate_strings: list[str]) -> str:
    """Collapse the breakdown's gate strings (already carrying 🔬 SPIKE-n / ⛔ BLOCKED-BY …)
    into a single compact cell. Kept verbatim so the icons/ids match every other page."""
    if not gate_strings:
        return "—"
    # gate strings look like "🔬 SPIKE-01" or "⛔ BLOCKED-BY product (PRODUCT-BE-E-00, …)".
    # Trim the parenthetical prose on the ⛔ ones so the column stays narrow; keep the id.
    out = []
    for g in gate_strings:
        g = re.sub(r"\s+", " ", g).strip()
        if g.startswith("⛔"):
            # keep "⛔ BLOCKED-BY <first token in parens or first id>"
            m = re.search(r"\(([A-Z][A-Z0-9-]+)", g)
            g = f"⛔ {m.group(1)}" if m else re.sub(r"\s*\(.*$", "", g)
        out.append(g)
    return " · ".join(dict.fromkeys(out))


def _fe_direct_be_deps(fe_story: dict, by_short: dict) -> list[str]:
    ids = []
    for d in fe_story["depends"]:
        m = _BE_SHORT_RE.search(d)
        if m and m.group(1) in by_short and m.group(1) not in ids:
            ids.append(m.group(1))
        elif "-FE-" in d and d not in ids:
            ids.append(d)                       # cross-story / cross-domain FE dependency
    return ids


def _order_key(short_id: str) -> tuple:
    m = re.match(r"([A-H])-(\d+)(?:-(\d+))?$", short_id)
    if m:
        return (bd.PHASE_SEQ.find(m.group(1)), int(m.group(2)), int(m.group(3) or 0))
    return (99, 0, 0)


def domain_section(dom: str, be_stories: list[dict], fe_group: list[dict]) -> list[str]:
    label = fe.DOMAIN_LABELS.get(dom, dom.title())
    if not be_stories and not fe_group:
        return [f"## {label}", "", "_No stories recorded for this domain._", ""]

    waves, gates, crit = bd.compute_implementation_order(be_stories)
    be_level = {bd._short_id(s["id"]): i for i, wave in enumerate(waves, 1) for s in wave}
    by_short = {bd._short_id(s["id"]): s for s in be_stories}

    # FE levels — identical staging engine to generate_project_plan.domain_plan_lines.
    fe_level: dict[str, int] = {}
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
        for s in stage_stories:
            fe_level[s["id"]] = lvl
        prev_lvl = lvl

    # Direct predecessor edges (same-domain BE only for BE rows; the implicit scaffold edge is
    # NOT drawn per-row — stated in prose), then the reverse map for the "Unlocks" column.
    scaffold = {k for k, s in by_short.items()
                if "module init" in (s.get("note", "") + " " + s["title"]).lower()}
    be_deps: dict[str, list] = {}
    for k, s in by_short.items():
        be_deps[k] = [d for d in dict.fromkeys(
            re.findall(r"\b(?:[A-Z]+-BE-)?([A-H]-\d+(?:-\d+)?)\b", s["depends"] or ""))
            if d in by_short and d != k]

    unlocks: dict[str, list] = {k: [] for k in by_short}
    for k, ds in be_deps.items():
        for d in ds:
            unlocks[d].append(k)
    fe_be_deps: dict[str, list] = {}
    for s in fe_group:
        fe_be_deps[s["id"]] = _fe_direct_be_deps(s, by_short)
        for d in fe_be_deps[s["id"]]:
            if d in unlocks:
                unlocks[d].append(s["id"])

    # ── assemble one row per story, ordered exactly like the sequence table ──
    rows = []       # (step, team_rank, sort_id, cells)
    icon = bd.COMPLEXITY_ICONS

    for k, s in by_short.items():
        chain_ids = sorted(be_deps[k], key=_order_key)
        if k in scaffold:
            chain = "— (module scaffold)"
        elif chain_ids:
            chain = ARROW.join(chain_ids + [f"**{k}**"])
        else:
            chain = f"**{k}**"
        unl = sorted(set(unlocks[k]), key=lambda x: (0, _order_key(x)) if x in by_short else (1, (99, 0, 0), x))
        if k in scaffold:
            unl_cell = "all stories (scaffold)"
        else:
            unl_cell = ", ".join(unl[:5]) + (" …" if len(unl) > 5 else "") if unl else "—"
        rows.append((be_level[k], 0, k, [
            f"{icon.get(s['complexity'], '⚪')} `{k}`",
            chain,
            _gate_tag(gates.get(k, [])),
            unl_cell,
        ]))

    for s in fe_group:
        chain_ids = sorted(fe_be_deps[s["id"]],
                           key=lambda d: _order_key(d) if d in by_short else (99, 0, 0))
        chain = ARROW.join(chain_ids + [f"**{s['id']}**"]) if chain_ids else f"**{s['id']}**"
        rows.append((fe_level[s["id"]], 1, s["id"], [
            f"{fe._impact_icon(s['impact'])} `{s['id']}`",
            chain,
            "—",
            "—",
        ]))

    rows.sort(key=lambda r: (r[0], r[1], _order_key(r[2]) if r[1] == 0 else (99, 0, 0), r[2]))

    n_be, n_fe = len(be_stories), len(fe_group)
    L = [
        f"## {label}",
        "",
        f"> **{n_be} BE + {n_fe} FE stories.** {pp.ORDER_WHY.get(dom, '')}  "
        "Rows are in build order. **Depends chain** reads left→right — the ids before **this "
        "story** must ship first (bare id = same domain; the implicit `B-01` module scaffold is "
        "assumed, not repeated). **Gate** = entry criterion, not an ordering edge. **Unlocks** = "
        "the stories that become startable once this one ships.",
        "",
        "| Step | Story | Depends chain (left→right, ▸ = then) | Gate | Unlocks |",
        "|---|---|---|---|---|",
    ]
    for step, _rank, _sid, cells in rows:
        L.append(f"| {step} | {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} |")

    if crit:
        L += ["", "**Backend critical path:** " + ARROW.join(f"`{k}`" for k in crit) + "."]
    if fe_group:
        flow = ARROW.join(f"`{s['id']}`"
                          for s in sorted(fe_group, key=lambda s: (fe_level[s["id"]], s["id"])))
        L += [f"**Frontend cutover flow:** {flow}."]
    L += ["", "---", ""]
    return L


def build() -> str:
    fe_groups: dict[str, list] = {}
    for s in fe.parse_fe_stories():
        fe_groups.setdefault(fe.domain_key_from_token(s["id"].rsplit("-FE-", 1)[0]), []).append(s)

    L = [
        "# Linear Dependency Map — Backend + Frontend, one row per story",
        "",
        f"> 🏷️ **Tags:** `dgs-migration` · `dependency-map` — **Generated:** {TODAY} by "
        "`generate_linear_deps.py` (runs inside `generate_all.py`). A compact companion to "
        "[00-sequencing.md](00-sequencing.md): the same steps and edges, rendered as a single "
        "left→right dependency chain per story instead of wide Depends/Blocks columns. Full "
        "story text lives in each domain's `be-04-stories.md`; nothing here is re-derived — the "
        "steps and edges come from the same engine that builds the sequencing doc.",
        "",
        "**How to read a row**",
        "",
        "- **Step** — build step within the domain; everything in the same step is parallelizable.",
        "- **Story** — 🔴🟠🟡🟢 backend complexity / FE impact icon + id. Bare ids (`B-01`) are "
        "this domain; full ids (`PRODUCT-BE-E-00`) are another domain.",
        "- **Depends chain** — read left→right; each id before **this story** must ship first. "
        "`A ▸ B ▸ **C**` means A then B then C. `— (module scaffold)` = the domain's init story, "
        "which everything else implicitly waits on.",
        "- **Gate** — 🔬 `SPIKE-n` (decision must be ratified first) or ⛔ `ID` (blocked by a story "
        "in another domain/subgraph). A gate is an *entry criterion*, not a build-order edge.",
        "- **Unlocks** — the immediate downstream stories that become startable once this ships "
        "(walk the graph forward without needing a second table).",
        "",
        "Cross-domain gates (the ⛔ rows) are listed in full in "
        "[cross-domain-dependencies.md](../analysis/program/cross-domain-dependencies.md).",
        "",
        "---",
        "",
    ]
    parsed: dict[str, list] = {}
    for dom in pp.DOMAIN_ORDER:
        try:
            parsed[dom] = [s for s in bd.parse_stories(bd.get_domain_dir(dom) / "be-04-stories.md")
                           if s.get("phase") != "S"]
        except Exception:
            parsed[dom] = []
    for dom in pp.DOMAIN_ORDER:
        L += domain_section(dom, parsed[dom], fe_groups.get(dom, []))
    L += [f"*Linear dependency map · generated {TODAY} by generate_linear_deps.py.*"]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    content = build()
    out = OUT / "03-linear-dependency-map.md"
    out.write_text(content, encoding="utf-8")
    print(f"  OK 03-linear-dependency-map.md ({len(content):,} chars)")


if __name__ == "__main__":
    main()
