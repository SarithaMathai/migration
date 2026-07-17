#!/usr/bin/env python3
"""
Master runner — regenerates the publication artifacts for every phase-1 domain.

Output structure (all paths relative to the migration repo root — per-domain breakdowns live
in output/summary/{domain}/, backend artifacts carry -BE- in the name; the -FE- frontend
counterparts come from generate_frontend.py into the same domain folder):
  output/summary/{domain}/
    FederatedGqlBreakDown-BE-{domain}.docx Word/Confluence-ready breakdown (tables, icons, formatting)
    FederatedGqlBreakDown-BE-{domain}.md   Confluence-ready breakdown (Markdown fallback)
    {domain}-comprehensive.md             Full engineering doc (OPT-IN: --full)
    {domain}-po-review.md                 PO/stakeholder executive review (OPT-IN: --full)
  output/jira/{domain}.csv             Jira-import CSV per domain

Program-level:
  output/summary/Federated+Graphql+Stories+-+BreakDown.docx  Global Word doc (all domains)
  output/summary/Federated+Graphql+Stories+-+BreakDown.md    Global all-domain breakdown
  output/summary/00-program-overview.md                      Merged program overview
  output/jira/all-stories.csv                                All stories + program spikes, one file

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_all.py              # all domains
    python fedMigrationScripts/generatescripts/generate_all.py impression   # specific domain(s)
    python fedMigrationScripts/generatescripts/generate_all.py --no-summary # skip program-level docs

⚠ Regeneration overwrites output/summary/* and output/jira/* — any hand edits to those
  generated files must first be folded back into the source (analysis/*/be-04-stories.md
  or the tables in generate_breakdown.py) or they will be lost.
"""

import sys
from pathlib import Path
from datetime import date

HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent.parent / "output" / "summary"   # generated docs go to migration/output/summary/

# ─── Import the two per-domain generators ────────────────────────────────────
# (Run from the same directory — direct import works)
import importlib.util, types

def _load(script_name: str) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(script_name, HERE / f"{script_name}.py")
    mod  = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
    spec.loader.exec_module(mod)                           # type: ignore[union-attr]
    return mod

comp_mod      = _load("generate_comprehensive")
review_mod    = _load("generate_po_review")
jira_mod      = _load("generate_jira")
breakdown_mod = _load("generate_breakdown")
word_mod      = _load("generate_word")
frontend_mod  = _load("generate_frontend")

ALL_DOMAINS = comp_mod.ALL_DOMAINS


# ─── Program-level domain metadata (feeds build_program_overview) ────────────
# Only the effort/sprint/decision/risk columns are read from here — story counts and
# complexity are computed live from each domain's be-04-stories.md so totals reconcile.
DOMAIN_META = [
    # (key, label, dgs, stories, effort_lo, effort_hi, sprints_1eng_lo, sprints_1eng_hi,
    #  queries, mutations, field_blocks, open_decisions, top_risk, risk_level)
    ("product",        "Product",         "plm-product (host)",          70,  194, 326, 39, 66, 18,  23, 16,  6, "TechPack aggregation + partner drop/undrop orchestration",  "🔴 High"),
    ("bom",            "BOM",             "plm-product (co-located)",    39,   68, 114, 15, 25, 13,   6, 18,  8, "`updateBom` 3-step write — no rollback path today",          "🔴 High"),
    ("workspace",      "Workspace",       "plm-workspace (separate)",    32,   75, 126, 17, 29,  8,  12,  3,  3, "Partner-action dispatcher with un-awaited promise chains",   "🔴 High"),
    ("sample",         "Sample",          "plm-sample (separate)",       33,   70, 116, 16, 27, 23,  12,  7,  4, "RFID ops + clone + multi-round write orchestration",         "🟡 Medium"),
    ("discussion",     "Discussion",      "plm-discussion (separate)",   37,   61, 102, 14, 24, 11,  29, 12,  3, "Three API versions (v1/v2/V3) + core* twins to consolidate", "🟡 Medium"),
    ("search",         "Search",          "plm-elastic-search (sep.)",   21,   59,  99, 15, 25, 48,   1, 12,  4, "Read-hub cutover — every domain depends on search",          "🔴 High"),
    ("packaging",      "Packaging",       "plm-product (co-located)",    26,   42,  72, 10, 17,  7,  10,  4,  4, "`updatePackaging` multi-step write + elastic search cutover", "🟡 Medium"),
    ("attachment",     "Attachment",      "plm-attachment (separate)",   26,   42,  71, 10, 17,  9,  15,  5,  3, "Dual record shape (snake/camel) + ACL-permission writes",     "🟡 Medium"),
    ("measurement",    "Measurement",     "plm-product (co-located)",    20,   32,  55,  8, 14,  7,   8,  2,  5, "`updateMeasurement` 2-step write + master-data cache",        "🟡 Medium"),
    ("claims",         "Claims",          "spark-claims (separate)",     22,   36,  62,  9, 15,  7,   6,  4,  3, "`updateClaim` proxy-ACL multi-step + camelCase response bug", "🟡 Medium"),
    ("impression",     "Impression",      "plm-product (co-located)",     7,   11,  18,  3,  5,  2,   1,  2,  2, "Impression sub-type polymorphism (5 types)",                 "🟢 Low"),
    ("productDetails", "Product Details", "plm-product (co-located)",    13,   24,  42,  6, 11,  2,   6,  3,  4, "`updateProductDetailsSet` multi-step + elastic search",       "🟡 Medium"),
    ("watchlist",      "Watchlist",       "plm-product (co-located)",    13,   25,  44,  6, 11,  4,   3,  3,  2, "`updateWatchlistEntries` multi-step write",                  "🟡 Medium"),
]

# Phase 1 runs on the 8 domains in ALL_DOMAINS — the remaining rows rejoin in a later phase.
DOMAIN_META = [d for d in DOMAIN_META if d[0] in ALL_DOMAINS]


def tshirt(stories: int, effort_hi: int) -> str:
    if stories >= 60 or effort_hi >= 200: return "XXL"
    if stories >= 35 or effort_hi >= 100: return "XL"
    if stories >= 25 or effort_hi >= 60:  return "L"
    if stories >= 15 or effort_hi >= 40:  return "M"
    if stories >= 8  or effort_hi >= 20:  return "S"
    return "XS"


# build_executive_summary() / build_portfolio() were deleted: superseded by
# build_program_overview() below (which computes live counts from be-04-stories.md
# instead of hardcoded snapshots) and never called since the merge.

def build_program_overview() -> str:
    today = date.today().isoformat()
    # Live per-domain counts + complexity from the actual be-04-stories.md → program totals always reconcile
    # with the global breakdown and the Jira CSVs (all use the same parser).
    live: dict[str, tuple] = {}
    phase_counts: dict[str, dict[str, int]] = {}
    for key in (d[0] for d in DOMAIN_META):
        try:
            st = breakdown_mod.parse_stories(breakdown_mod.get_domain_dir(key) / "be-04-stories.md")
        except Exception:
            st = []
        # Build stories only — S-phase spike stubs are tracked as Phase-0 program spikes,
        # same convention as the global breakdown page and the Jira CSVs (totals reconcile).
        st = [s for s in st if s.get("phase") != "S"]
        live[key] = (
            len(st),
            sum(1 for s in st if s["complexity"] == "very high"),
            sum(1 for s in st if s["complexity"] == "high"),
            sum(1 for s in st if s["complexity"] == "medium"),
            sum(1 for s in st if s["complexity"] == "low"),
        )
        pc: dict[str, int] = {}
        for s in st:
            pc[s["phase"]] = pc.get(s["phase"], 0) + 1
        phase_counts[key] = pc

    # Frontend per-domain: story count + effort range from fe-08-frontend-stories.md
    # (same parser as the FE breakdown pages and Jira CSVs, so numbers reconcile).
    fe_by_dom: dict[str, tuple[int, int, int]] = {}   # key -> (count, effort_lo, effort_hi)
    try:
        for s in frontend_mod.parse_fe_stories():
            k = frontend_mod.domain_key_from_token(s["id"].rsplit("-FE-", 1)[0])
            lo, hi = frontend_mod._effort_range(s["effort"])
            c, tlo, thi = fe_by_dom.get(k, (0, 0, 0))
            fe_by_dom[k] = (c + 1, tlo + lo, thi + hi)
    except Exception:
        pass
    fe_total   = sum(v[0] for v in fe_by_dom.values())
    fe_eff_lo  = sum(v[1] for v in fe_by_dom.values())
    fe_eff_hi  = sum(v[2] for v in fe_by_dom.values())
    total_stories   = sum(live[d[0]][0] for d in DOMAIN_META)
    total_lo        = sum(d[4]  for d in DOMAIN_META)
    total_hi        = sum(d[5]  for d in DOMAIN_META)
    total_decisions = sum(d[11] for d in DOMAIN_META)
    tvh = sum(live[d[0]][1] for d in DOMAIN_META)
    th  = sum(live[d[0]][2] for d in DOMAIN_META)
    tm  = sum(live[d[0]][3] for d in DOMAIN_META)
    tl  = sum(live[d[0]][4] for d in DOMAIN_META)
    plm_product = sum(live[d[0]][0] for d in DOMAIN_META if d[2].startswith("plm-product"))

    L: list[str] = [
        "# Spark → Federated GraphQL Migration — Program Overview",
        "",
        f"> 🏷️ **Tags:** `dgs-migration` · `program-overview` — **Confluence:** *Federation Graph Migration* (space home)",
        f"> **Generated:** {today} · **Scope:** {len(ALL_DOMAINS)} domains (phase 1) · `spark-internal-graphql` → Netflix DGS via Hive Schema Registry",
        "> Effort is **AI-estimated — confirm in refinement.**",
        "",
        "---",
        "",
        "## What & why",
        "",
        "- We are moving the PLM GraphQL API off the monolithic `spark-internal-graphql` Node.js gateway onto "
        "**Netflix DGS** subgraphs, federated via the **Hive Schema Registry**.",
        "- Phase 1 covers 8 domains: seven compile into the **same `plm-product` subgraph** "
        "(their cross-references resolve internally); **claims** is its own subgraph.",
        "- The remaining domains (attachment, discussion, sample, search, workspace) federate in a later phase.",
        "",
        "**Engineering model:**",
        "- Every story is self-contained in one PR — schema + DGS data fetcher + Kotlin REST service method + Hive push.",
        "- The model, REST controllers (GET/POST/PUT) and services already exist; each story only adds the thin DGS wrapper.",
        "- **Ship on green, per story** — except cross-subgraph entity extensions, which wait for their owning subgraph.",
        "",
        "---",
        "",
        "## Program totals",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total domains | {len(ALL_DOMAINS)} |",
        f"| Target DGS services | {len({d[2].split()[0] for d in DOMAIN_META})} |",
        f"| **Total backend stories** | **{total_stories}** build stories (Phase-0 spikes tracked separately: 7 program spikes + their domain stubs) |",
        f"| **Total frontend stories** | **{fe_total}** (platform enablement complete — waves 1–4) |",
        f"| Complexity (backend) | 🔴 {tvh} Very High · 🟠 {th} High · 🟡 {tm} Medium · 🟢 {tl} Low |",
        f"| Open decisions | {total_decisions} |",
        f"| **Backend effort (buffered +20%)** | **{total_lo}–{total_hi} engineer-days** |",
        f"| **Frontend effort (single-engineer)** | **{fe_eff_lo}–{fe_eff_hi} engineer-days** |",
        "",
        "---",
        "",
        "## Domains at a glance",
        "",
        "| Domain | Target DGS | BE Stories | T-Shirt | 🔴 | 🟠 | 🟡 | 🟢 | BE effort (buffered) | FE Stories | FE effort | Top risk |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for (key,label,dgs,stories,elo,ehi,slo,shi,q,mut,fb,dec,risk,rl) in DOMAIN_META:
        total, vh, h, m, lo = live[key]
        ts = tshirt(total, ehi)
        fc, flo, fhi = fe_by_dom.get(key, (0, 0, 0))
        L.append(f"| [{label}](./{key}/FederatedGqlBreakDown-BE-{key}.md) | `{dgs}` | **{total}** | {ts} | "
                 f"{vh} | {h} | {m} | {lo} | {elo}–{ehi}d | {fc} | {flo}–{fhi}d | {rl} {risk} |")
    L += [
        f"| **TOTAL** | — | **{total_stories}** | — | **{tvh}** | **{th}** | **{tm}** | **{tl}** | "
        f"**{total_lo}–{total_hi}d** | **{fe_total}** | **{fe_eff_lo}–{fe_eff_hi}d** | — |",
        "",
        "> BE counts + complexity are computed live from each domain's `be-04-stories.md`; FE counts + effort from "
        "`fe-08-frontend-stories.md` (same parsers as the breakdowns + Jira CSVs), so these totals always reconcile. "
        "BE effort is buffered +20%; FE effort is single-engineer, unbuffered. Each domain's FE stories live in "
        "`summary/{domain}/FederatedGqlBreakDown-FE-{domain}.md`.",
        "",
        "---",
        "",
        "## Backend stories by phase",
        "",
        "> Phases: " + " · ".join(
            f"{breakdown_mod.PHASE_ICONS[p]} **{p}** {breakdown_mod.PHASE_NAMES[p]}"
            for p in breakdown_mod.PHASE_SEQ) + ". "
        "Phase-0 spikes are tracked separately (program spike register). Frontend stories are staged by "
        "**wave**, not phase — see `analysis/program/fe-10-migration-sequencing.md`.",
        "",
        "| Domain | " + " | ".join(f"{breakdown_mod.PHASE_ICONS[p]} {p}" for p in breakdown_mod.PHASE_SEQ) + " | Total |",
        "|---|" + "---|" * (len(breakdown_mod.PHASE_SEQ) + 1),
    ]
    for (key,label,*_rest) in DOMAIN_META:
        pc = phase_counts.get(key, {})
        cells = " | ".join(str(pc.get(p, 0)) for p in breakdown_mod.PHASE_SEQ)
        L.append(f"| [{label}](./{key}/FederatedGqlBreakDown-BE-{key}.md) | {cells} | **{live[key][0]}** |")
    phase_tot = {p: sum(phase_counts.get(d[0], {}).get(p, 0) for d in DOMAIN_META)
                 for p in breakdown_mod.PHASE_SEQ}
    L += [
        "| **TOTAL** | " + " | ".join(f"**{phase_tot[p]}**" for p in breakdown_mod.PHASE_SEQ)
        + f" | **{total_stories}** |",
        "",
        "---",
        "",
        "## DGS service groupings",
        "",
        "| DGS Service | Phase | Domains | Combined stories |",
        "|---|---|---|---|",
        f"| `plm-product` | 1 | Product · BOM · Measurement · Packaging · Impression · Product Details · Watchlist | {plm_product} |",
        f"| `spark-claims` | 1 | Claims | {live['claims'][0]} |",
        "| `plm-sample` | later | Sample | ~33 (estimate — analysis not yet regenerated) |",
        "| `plm-discussion` | later | Discussion | ~37 (estimate) |",
        "| `plm-workspace` | later | Workspace | ~32 (estimate) |",
        "| `plm-attachment` | later | Attachment | ~26 (estimate) |",
        "| `plm-elastic-search` | later | Search | ~21 (estimate) |",
        "",
        "> Phase-1 rows are computed live from `be-04-stories.md`; later-phase rows are earlier-pass estimates,",
        "> re-baselined when those domains' analyses are regenerated.",
        "",
        "---",
        "",
        "## Recommended sequencing",
        "",
        "```",
        "Tier 1 — Foundation:  Product (host DGS, shared wiring; phase 1) · Search (read hub — later-phase domain,",
        "                      sequenced first among them because every domain reads through it)",
        "Tier 2 — Co-located:  Impression → Measurement → ProductDetails → Watchlist → BOM → Packaging  (phase 1)",
        "Tier 3 — Separate:    Claims (phase 1) · Attachment · Discussion · Sample · Workspace  (later phase)",
        "Tier 4 — Federation:  all F-phase stories, once the owning subgraph is live",
        "```",
        "",
        "## Cross-domain blockers (true federation — a separate DGS must migrate first)",
        "",
        "| Blocked story | Domain | Waits on |",
        "|---|---|---|",
        "| `PRODUCT-BE-F-01` (attachments) | product | **attachment** (`plm-attachment`, later phase) |",
        "| `PRODUCT-BE-F-02` (discussions) | product | **discussion** (`plm-discussion`, later phase) |",
        "| `PRODUCT-BE-F-03` (sample) | product | **sample** (`plm-sample`, later phase) |",
        "| `PRODUCT-BE-F-05` (claims) | product | **claims** (`spark-claims`, phase 1) |",
        "| `PRODUCT-BE-F-07` (constructions) | product | **construction** (no subgraph scheduled yet — `F-07` stays blocked until one exists) |",
        "| `MST-BE-F-02` (sampleMeasurement) | measurement | **sample** (`plm-sample`, later phase) |",
        "",
        "> Internal (NOT blockers, same `plm-product` subgraph): `BOM-BE-F-01/F-02`, `PRODUCT-BE-F-04/F-06/F-08`, "
        "`MST-BE-F-01`, `IMPRESSION-BE-F-01`, `PDTL-BE-F-01`, `PKG-BE-F-01`.",
        "",
        "---",
        "",
        "## How to consume",
        "",
        "- **Per domain (backend):** open `summary/{domain}/FederatedGqlBreakDown-BE-{domain}.md` (or the `.docx` for Confluence/Word).",
        "- **Per domain (frontend):** open `summary/{domain}/FederatedGqlBreakDown-FE-{domain}.md` (generated by `generate_frontend.py`).",
        "- **Jira:** import `jira/{domain}.csv` (or `jira/all-stories.csv`). See `PUSH-TO-JIRA-CONFLUENCE.md`.",
        "- **Read order by role + regeneration:** see `README.md`.",
        "",
        "---",
        f"*Program overview · generated {today} from `output/analysis/*/04-*.md`.*",
    ]
    return "\n".join(L)


# ─── Runner ───────────────────────────────────────────────────────────────────
def main() -> None:
    args = sys.argv[1:]
    no_summary = "--no-summary" in args
    full       = "--full" in args      # also build -comprehensive / -po-review deep-dives
    targets    = [a for a in args if not a.startswith("--")] or ALL_DOMAINS

    OUTPUT.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    print(f"\n=== oneStopDoc generation — {today} ===\n")

    # Per-domain: comprehensive + po-review + breakdown, all under {domain}/ subfolder
    for domain in targets:
        if domain not in ALL_DOMAINS:
            print(f"  UNKNOWN domain '{domain}' — skipping")
            continue

        # Word doc (primary: .docx with full formatting, tables, icons)
        try:
            word_mod.generate_word_for(domain)
        except Exception as e:
            print(f"  FAIL {domain} word: {type(e).__name__}: {e}")

        # Breakdown markdown (Confluence fallback)
        try:
            breakdown_mod.generate_breakdown_for(domain)
        except Exception as e:
            print(f"  FAIL {domain} breakdown: {type(e).__name__}: {e}")

        # Deep-dives are OPT-IN (--full): the default deliverable is ONE breakdown
        # per domain — engineers work from analysis/{domain}/be-04-stories.md.
        if full:
            domain_dir = OUTPUT / domain
            domain_dir.mkdir(parents=True, exist_ok=True)
            # Comprehensive
            try:
                content  = comp_mod.build_comprehensive(domain)
                out_file = domain_dir / f"{domain}-comprehensive.md"
                out_file.write_text(content, encoding="utf-8")
                print(f"  OK {domain}/{domain}-comprehensive.md ({len(content):,} chars)")
            except Exception as e:
                print(f"  FAIL {domain}-comprehensive: {type(e).__name__}: {e}")

            # PO review
            try:
                content  = review_mod.build_po_review(domain)
                out_file = domain_dir / f"{domain}-po-review.md"
                out_file.write_text(content, encoding="utf-8")
                print(f"  OK {domain}/{domain}-po-review.md ({len(content):,} chars)")
            except Exception as e:
                print(f"  FAIL {domain}-po-review: {type(e).__name__}: {e}")

        # Jira CSV — canonical location is finalOutput/jira/ (documented Jira-import path).
        # (out_dir omitted → defaults to JIRA_OUT; no subfolder copy, avoids the two-location drift.)
        try:
            jira_mod.generate_domain(domain)
        except Exception as e:
            print(f"  FAIL {domain} jira CSV: {type(e).__name__}: {e}")

    if not no_summary and not (targets != ALL_DOMAINS):
        print()
        # Global Word doc (all domains, fully formatted)
        try:
            word_mod.generate_global_word()
        except Exception as e:
            print(f"  FAIL global word: {type(e).__name__}: {e}")

        # Global breakdown markdown (Confluence fallback)
        try:
            breakdown_mod.generate_global()
        except Exception as e:
            print(f"  FAIL global breakdown: {type(e).__name__}: {e}")

    # The scoped custom page is OPT-IN — build it only on explicit request, never on a full run.
    if "--custom" in sys.argv[1:]:
        try:
            breakdown_mod.generate_global_custom()
            word_mod.generate_global_custom_word()
        except Exception as e:
            print(f"  FAIL global_custom: {type(e).__name__}: {e}")

    if not no_summary:
        # Program overview (merged: replaces 00-executive-summary + 00-portfolio)
        try:
            content  = build_program_overview()
            OUTPUT.mkdir(parents=True, exist_ok=True)
            out_file = OUTPUT / "00-program-overview.md"
            out_file.write_text(content, encoding="utf-8")
            print(f"  OK 00-program-overview.md ({len(content):,} chars)")
            # remove the two superseded files so they don't linger as stale clutter
            for old in ("00-executive-summary.md", "00-portfolio.md"):
                p = OUTPUT / old
                if p.exists():
                    p.unlink()
                    print(f"  RM  {old} (merged into 00-program-overview.md)")
        except Exception as e:
            print(f"  FAIL 00-program-overview: {type(e).__name__}: {e}")

        # All-domains Jira CSV
        try:
            jira_mod.generate_all_csv(ALL_DOMAINS)
        except Exception as e:
            print(f"  FAIL all-stories.csv: {type(e).__name__}: {e}")

        # Frontend inventory docs + FE Jira rows appended into output/jira/{domain}.csv
        # (runs AFTER the backend jira CSVs above so the combined files carry both)
        try:
            frontend_mod.main()
        except Exception as e:
            print(f"  FAIL frontend analysis: {type(e).__name__}: {e}")

        # Program-level team plan (2 BE + 2 FE engineers) — needs both BE + FE parsers
        try:
            _load("generate_team_plan").main()
        except Exception as e:
            print(f"  FAIL team plan: {type(e).__name__}: {e}")

        # Story-level project plan (combined BE + FE order, domain by domain)
        try:
            _load("generate_project_plan").main()
        except Exception as e:
            print(f"  FAIL project plan: {type(e).__name__}: {e}")

    print("\nDone. Run `python generate_all.py <domain>` to regenerate a single domain.\n")


if __name__ == "__main__":
    main()
