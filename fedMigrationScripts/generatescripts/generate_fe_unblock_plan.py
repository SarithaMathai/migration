#!/usr/bin/env python3
"""
FE-unblock plan — a BLOCKER-FIRST, cross-domain view of what to build so frontend can start
as early as possible, independent of domain boundaries.

Motivation (user, 2026-07-24): "work on blockers first so FE can start earlier irrespective of
domain; not all BE stories need to be complete before FE can start; FE stories can run in parallel."
The domain-by-domain plans answer "when do we finish each domain"; THIS answers "what's the shortest
path to unblocking frontend work anywhere." It is a **dependency-only** view — it shows what CAN run
in parallel, not what a fixed-size team schedules (the 1BE+1FE calendar stays the capacity-bound view).

Three sections:
  1. Backend unblocker sequence — only the BE stories that gate at least one FE story (program-wide),
     in dependency order (Kahn levels across ALL domains at once), each annotated with how many FE
     stories it helps unblock. Build these first.
  2. Frontend readiness waves — every FE story grouped into "ready waves": a wave = all FE stories
     whose direct BE deps are satisfied by the end of the corresponding backend level. FE stories in
     the same wave have no ordering constraint between them → they can run in parallel (as many as
     you have FE capacity for). Cross-domain: a wave mixes domains freely.
  3. Trailing backend — the BE stories that gate NO frontend story (federation stitches, parity).
     They can land after the flips, in the background.

ACCURACY: dependency edges come from the same parsers as every other plan (bd.parse_stories'
`depends`, fe.parse_fe_stories' remapped `depends`). The only cross-domain resolution here is mapping
a full BE id (e.g. PRODUCT-BE-G-01) to its (domain, short) — done from the id itself, no guessing.
Program-wide product-E-00 → every-domain-E-01 gate is honored because E-00 is itself an FE blocker
only if some FE waits on an E-01 (it is, transitively via the saga FE stories).

Output: output/summary/00-fe-unblock-plan.md  ->  finalArtifacts/00-fe-unblock-plan.md

Run:
    python fedMigrationScripts/generatescripts/generate_fe_unblock_plan.py
"""

import importlib.util
import re
from collections import defaultdict, Counter
from datetime import date
from pathlib import Path

from team_config import BE_QUEUE

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

# token in a full BE id -> domain key (e.g. PRODUCT-BE-G-01 -> product)
TOKEN_TO_DOMAIN = {
    "PRODUCT": "product", "BOM": "bom", "IMPRESSION": "impression", "WATCHLIST": "watchlist",
    "PDTL": "productDetails", "MST": "measurement", "PKG": "packaging", "CLAIM": "claims",
}
_BE_FULL_RE = re.compile(r"([A-Z]+)-BE-([A-H]-\d+(?:-\d+)?)")


def _gid(domain: str, short: str) -> str:
    """Program-wide node id for a BE story: 'product/G-01'."""
    return f"{domain}/{short}"


def _order_key(short: str) -> tuple:
    m = re.match(r"([A-H])-(\d+)(?:-(\d+))?$", short)
    return (bd.PHASE_SEQ.find(m.group(1)), int(m.group(2)), int(m.group(3) or 0)) if m else (99, 0, 0)


def load():
    """Return (be, deps, fe_deps) where
       be[gid]     = story dict (+ 'domain','short')
       deps[gid]   = set of gids this BE story depends on (intra-domain; the module-scaffold edge)
       fe_deps[fe] = (fe_story, set of BE gids it directly depends on)."""
    be, deps = {}, {}
    scaffold_of = {}   # domain -> its module-init short id
    for dom in BE_QUEUE:
        try:
            stories = [s for s in bd.parse_stories(bd.get_domain_dir(dom) / "be-04-stories.md")
                       if s.get("phase") != "S"]
        except Exception:
            stories = []
        by_short = {bd._short_id(s["id"]): s for s in stories}
        scaf = next((k for k, s in by_short.items()
                     if "module init" in (s.get("note", "") + " " + s["title"]).lower()), None)
        scaffold_of[dom] = scaf
        for short, s in by_short.items():
            gid = _gid(dom, short)
            s = {**s, "domain": dom, "short": short}
            be[gid] = s
            d = set()
            for m in re.finditer(r"\b(?:[A-Z]+-BE-)?([A-H]-\d+(?:-\d+)?)\b", s["depends"] or ""):
                if m.group(1) in by_short and m.group(1) != short:
                    d.add(_gid(dom, m.group(1)))
            if scaf and short != scaf:
                d.add(_gid(dom, scaf))
            deps[gid] = d

    fe_deps = {}
    for s in fe.parse_fe_stories():
        bset = set()
        for dep in s["depends"]:
            m = _BE_FULL_RE.search(dep)
            if m:
                dom = TOKEN_TO_DOMAIN.get(m.group(1))
                if dom and _gid(dom, m.group(2)) in be:
                    bset.add(_gid(dom, m.group(2)))
        fe_deps[s["id"]] = (s, bset)
    return be, deps, fe_deps


def transitive_blockers(fe_deps, deps):
    """Every BE gid that some FE story needs, DIRECTLY or via BE→BE prerequisites."""
    blockers = set()
    stack = [g for _s, bset in fe_deps.values() for g in bset]
    while stack:
        g = stack.pop()
        if g in blockers:
            continue
        blockers.add(g)
        stack.extend(deps.get(g, ()))
    return blockers


def _same_domain_fe(be, fe_deps):
    """How many FE stories depend ONLY on their own domain's backend (or nothing)."""
    n = 0
    for fid, (_s, bset) in fe_deps.items():
        fedom = fe.domain_key_from_token(fid.rsplit("-FE-", 1)[0])
        doms = {be[g]["domain"] for g in bset}
        if not doms or doms <= {fedom}:
            n += 1
    return n


def kahn_levels(nodes, deps):
    """Assign each node the length of its longest dependency chain (1-based) within `nodes`."""
    level = {}
    def lvl(g):
        if g in level:
            return level[g]
        level[g] = 1  # guard against cycles
        preds = [p for p in deps.get(g, ()) if p in nodes]
        level[g] = 1 + max((lvl(p) for p in preds), default=0)
        return level[g]
    for g in nodes:
        lvl(g)
    return level


def build() -> str:
    be, deps, fe_deps = load()
    blockers = transitive_blockers(fe_deps, deps)
    non_blockers = [g for g in be if g not in blockers]

    be_level = kahn_levels(blockers, deps)

    icon = bd.COMPLEXITY_ICONS
    dom_label = fe.DOMAIN_LABELS

    # which FE stories each BE gid directly unblocks (names, not just a count) — used both to
    # prioritize within a level (more FE = more leverage) and to list them in the table.
    unblocks_fe = defaultdict(list)
    for fid, (_s, bset) in fe_deps.items():
        for g in bset:
            unblocks_fe[g].append(fid)
    directly_unblocks = {g: len(v) for g, v in unblocks_fe.items()}

    def _fe_ids_by_domain(gid):
        """The FE ids waiting on this BE story, grouped by FE domain, e.g.
        'Product: PRODUCT-FE-001, -002 ‖ Impression: IMPRESSION-FE-002'."""
        ids = unblocks_fe.get(gid, [])
        if not ids:
            return "— (prereq only)"
        by_dom = defaultdict(list)
        for fid in ids:
            by_dom[fe.domain_key_from_token(fid.rsplit("-FE-", 1)[0])].append(fid)
        chunks = []
        for d in sorted(by_dom):
            fids = ", ".join(f"`{i}`" for i in sorted(by_dom[d]))
            chunks.append(f"{dom_label.get(d, d)}: {fids}")
        return " ‖ ".join(chunks)

    L = [
        "# FE-Unblock Plan — build blockers first so frontend can start earliest",
        "",
        f"> 🏷️ `dgs-migration` · `fe-unblock` — **Generated:** {TODAY} by "
        "`generate_fe_unblock_plan.py` (in `generate_all.py`). A **dependency-only** view of what to "
        "build so frontend can start as early as possible. **Domain-first** — 38 of 41 FE stories "
        "stay inside their own domain, so keep building domain by domain; this doc just shows, within "
        "that, that FE starts on its own deps (not the whole domain) and that ready FE stories can "
        "run in parallel. Shows what CAN run in parallel, not a fixed-team schedule — for the "
        "capacity-bound calendar see [01-implementation-plan-1BE-1FE.md](01-implementation-plan-1BE-1FE.md) "
        "and [00-domain-rollout.md](00-domain-rollout.md).",
        "",
        "**Do domains as coherent units — this view refines *within* that, it doesn't replace it.** "
        f"Of the {len(fe_deps)} frontend stories, **{_same_domain_fe(be, fe_deps)} depend only on "
        f"their OWN domain's backend**; only **{len(fe_deps) - _same_domain_fe(be, fe_deps)}** reach "
        "across domains (the impression pair fused with BOM/Product screens, chiefly). So keep "
        "building domain by domain — the point here is the two refinements below, not a cross-domain "
        "free-for-all:",
        "",
        "1. **You don't need a whole domain's backend done before its frontend starts** — each FE "
        "story starts when *its own* deps land (reads need B+G, writes need D, saga needs E).",
        "2. **FE stories that are ready together can run in parallel** (capacity permitting) — nothing "
        "orders them beyond their backend deps.",
        "3. **A handful of cross-domain blockers are worth pulling forward** — mainly Product/BOM "
        "field resolvers that unblock impression's fused FE; those are the only reason to look past "
        "one domain at a time.",
        "",
        "**Supporting facts:**",
        "",
        f"- **{len(blockers)} of {len(be)} backend stories** gate at least one frontend story "
        f"(directly or via a BE prerequisite). Build these first.",
        f"- **{len(non_blockers)} backend stories gate NO frontend story** — federation stitches, "
        "parity, later-phase counts. They can **trail after the flips** (§3).",
        "- Frontend stories are grouped into **readiness waves**: a wave holds every FE story whose "
        "backend deps are all satisfied by that point — **FE stories in the same wave have no "
        "dependency on each other and can run in parallel** (limited only by FE capacity, not order).",
        "- **Not all of a domain's backend must finish before its FE starts** — an FE reads story "
        "needs only that entity's B + field-resolver (G) stories, not its writes (D/E); a writes "
        "story needs only its D stories; the saga FE needs only E. Each starts when *its own* deps "
        "land.",
        "",
        "---",
        "",
        "## 1. Backend unblocker sequence (build these first)",
        "",
        "Only the frontend-blocking backend stories, in dependency order (level = longest dependency "
        "chain). Grouped across domains only so you can see the earliest unblock — in practice most "
        "of a level belongs to whichever domain you're building. Everything in a level is independent "
        "(parallel if you have the backend capacity). **Frontend stories unblocked** lists exactly "
        "which FE stories name this backend story as a dependency (grouped by FE domain; the number "
        "in parens is the count). More = more leverage → do first within its level. A story shown "
        "'— (prereq only)' unblocks no FE story directly; it's here because another blocker needs it.",
        "",
    ]
    max_lvl = max(be_level.values(), default=0)
    for lv in range(1, max_lvl + 1):
        rows = sorted((g for g in blockers if be_level[g] == lv),
                      key=lambda g: (-directly_unblocks.get(g, 0), be[g]["domain"], _order_key(be[g]["short"])))
        if not rows:
            continue
        L.append(f"### Backend level {lv}")
        L.append("")
        L.append("| BE story | Domain | Story | Frontend stories unblocked (by domain) |")
        L.append("|---|---|---|---|")
        for g in rows:
            s = be[g]
            n = directly_unblocks.get(g, 0)
            fe_cell = _fe_ids_by_domain(g)
            if n:
                fe_cell += f" **({n})**"
            title = re.sub(r"`", "", s["title"]).strip()
            title = (title[:44] + "…") if len(title) > 45 else title
            L.append(f"| {icon.get(s['complexity'], '⚪')} `{s['short']}` "
                     f"| {dom_label.get(s['domain'], s['domain'])} | {title} | {fe_cell} |")
        L.append("")

    # ── 2. FE readiness waves ────────────────────────────────────────────────
    # An FE story is ready at wave = max backend level among its deps (0 deps -> wave 0/immediate).
    fe_wave = {}
    for fid, (s, bset) in fe_deps.items():
        fe_wave[fid] = max((be_level[g] for g in bset if g in be_level), default=0)
    waves = defaultdict(list)
    for fid, w in fe_wave.items():
        waves[w].append(fid)

    L += [
        "---",
        "",
        "## 2. Frontend readiness waves (parallel within a wave)",
        "",
        "Each frontend story appears in the wave where **all its backend deps are done** (wave n = "
        "after backend level n above). **Everything in one wave can be built in parallel** — no "
        "dependency between them. With one FE engineer you'd still do them one at a time (take a whole "
        "domain as a unit if you prefer); with more capacity, anything in a wave can go at once.",
        "",
        "Grouped by domain within each wave, so you can still take a domain's frontend as one unit — "
        "the wave just tells you the earliest point each becomes startable.",
        "",
        "| Ready after | Frontend stories, grouped by domain (‖ = parallel-eligible) |",
        "|---|---|",
    ]
    for w in sorted(waves):
        by_dom = defaultdict(list)
        for i in waves[w]:
            by_dom[fe.domain_key_from_token(i.rsplit("-FE-", 1)[0])].append(i)
        chunks = []
        for d in sorted(by_dom):
            ids = " ‖ ".join(f"`{i}`" for i in sorted(by_dom[d]))
            chunks.append(f"**{dom_label.get(d, d)}:** {ids}")
        after = "immediately (no BE dep)" if w == 0 else f"backend level {w}"
        L.append(f"| {after} | " + " · ".join(chunks) + " |")
    L.append("")
    L.append(f"> Earliest frontend work can begin after **backend level "
             f"{min((w for w in waves if w > 0), default=1)}** — you do not have to wait for a whole "
             "domain, or for the backend queue to drain.")

    # ── 3. Trailing backend ──────────────────────────────────────────────────
    L += [
        "",
        "---",
        "",
        "## 3. Trailing backend (gates no frontend — can land after the flips)",
        "",
        f"These **{len(non_blockers)}** backend stories are not on any frontend story's critical "
        "path. Ship them in the background after the cutovers — they're federation stitches, "
        "field-resolver parity, and later-phase counts.",
        "",
        "| BE story | Domain | Story |",
        "|---|---|---|",
    ]
    for g in sorted(non_blockers, key=lambda g: (be[g]["domain"], _order_key(be[g]["short"]))):
        s = be[g]
        title = re.sub(r"`", "", s["title"]).strip()
        title = (title[:56] + "…") if len(title) > 57 else title
        L.append(f"| {icon.get(s['complexity'], '⚪')} `{s['short']}` | {dom_label.get(s['domain'], s['domain'])} | {title} |")

    L += [
        "",
        "---",
        f"*FE-unblock plan · generated {TODAY} by generate_fe_unblock_plan.py.*",
    ]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    content = build()
    out = OUT / "00-fe-unblock-plan.md"
    out.write_text(content, encoding="utf-8")
    print(f"  OK 00-fe-unblock-plan.md ({len(content):,} chars)")


if __name__ == "__main__":
    main()
