#!/usr/bin/env python3
"""
Master runner — regenerates the publication artifacts for every phase-1 domain.

Output structure (all paths relative to the migration repo root):
  output/summary/{domain}/
    FederatedGqlBrakDown-{domain}.docx Word/Confluence-ready breakdown (tables, icons, formatting)
    FederatedGqlBrakDown-{domain}.md   Confluence-ready breakdown (Markdown fallback)
    {domain}-comprehensive.md          Full engineering doc (OPT-IN: --full)
    {domain}-po-review.md              PO/stakeholder executive review (OPT-IN: --full)
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
  generated files must first be folded back into the source (initial-analysis/*/04-stories.md
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

ALL_DOMAINS = comp_mod.ALL_DOMAINS


# ─── Program-level domain metadata (feeds build_program_overview) ────────────
# Only the effort/sprint/decision/risk columns are read from here — story counts and
# complexity are computed live from each domain's 04-stories.md so totals reconcile.
DOMAIN_META = [
    # (key, label, dgs, stories, effort_lo, effort_hi, sprints_1eng_lo, sprints_1eng_hi,
    #  queries, mutations, field_blocks, open_decisions, top_risk, risk_level)
    ("product",        "Product",         "plm-product (host)",          70,  197, 330, 42, 71, 18,  23, 16,  6, "TechPack aggregation + partner drop/undrop orchestration",  "🔴 High"),
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
# build_program_overview() below (which computes live counts from 04-stories.md
# instead of hardcoded snapshots) and never called since the merge.

def build_program_overview() -> str:
    today = date.today().isoformat()
    # Live per-domain counts + complexity from the actual 04-stories.md → program totals always reconcile
    # with the global breakdown and the Jira CSVs (all use the same parser).
    live: dict[str, tuple] = {}
    for key in (d[0] for d in DOMAIN_META):
        try:
            st = breakdown_mod.parse_stories(breakdown_mod.get_domain_dir(key) / "04-stories.md")
        except Exception:
            st = []
        live[key] = (
            len(st),
            sum(1 for s in st if s["complexity"] == "very high"),
            sum(1 for s in st if s["complexity"] == "high"),
            sum(1 for s in st if s["complexity"] == "medium"),
            sum(1 for s in st if s["complexity"] == "low"),
        )
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
        f"| **Total stories** | **{total_stories}** |",
        f"| Complexity | 🔴 {tvh} Very High · 🟠 {th} High · 🟡 {tm} Medium · 🟢 {tl} Low |",
        f"| Open decisions | {total_decisions} |",
        f"| **Effort (buffered +20%)** | **{total_lo}–{total_hi} engineer-days** |",
        "",
        "---",
        "",
        "## Domains at a glance",
        "",
        "| Domain | Target DGS | Stories | T-Shirt | 🔴 | 🟠 | 🟡 | 🟢 | Effort (buffered) | Top risk |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for (key,label,dgs,stories,elo,ehi,slo,shi,q,mut,fb,dec,risk,rl) in DOMAIN_META:
        total, vh, h, m, lo = live[key]
        ts = tshirt(total, ehi)
        L.append(f"| [{label}](./{key}/FederatedGqlBrakDown-{key}.md) | `{dgs}` | **{total}** | {ts} | "
                 f"{vh} | {h} | {m} | {lo} | {elo}–{ehi}d | {rl} {risk} |")
    L += [
        f"| **TOTAL** | — | **{total_stories}** | — | **{tvh}** | **{th}** | **{tm}** | **{tl}** | "
        f"**{total_lo}–{total_hi}d** | — |",
        "",
        "> All counts + complexity are computed live from each domain's `04-stories.md` (same parser as the "
        "breakdown + Jira CSVs), so these totals always reconcile.",
        "",
        "---",
        "",
        "## DGS service groupings",
        "",
        "| DGS Service | Domains | Combined stories |",
        "|---|---|---|",
        f"| `plm-product` | Product · BOM · Measurement · Packaging · Impression · Product Details · Watchlist | {plm_product} |",
        "| `plm-sample` | Sample | 33 |",
        "| `plm-discussion` | Discussion | 37 |",
        "| `plm-workspace` | Workspace | 32 |",
        "| `plm-attachment` | Attachment | 26 |",
        "| `plm-elastic-search` | Search | 21 |",
        "| `spark-claims` | Claims | 22 |",
        "",
        "---",
        "",
        "## Recommended sequencing",
        "",
        "```",
        "Tier 1 — Foundation:  Search (read hub) · Product (host DGS, shared wiring)",
        "Tier 2 — Co-located:  Impression → Measurement → ProductDetails → Watchlist → BOM → Packaging",
        "Tier 3 — Separate:    Attachment · Claims · Discussion · Sample · Workspace",
        "Tier 4 — Federation:  all F-phase stories, once the owning subgraph is live",
        "```",
        "",
        "## Cross-domain blockers (true federation — a separate DGS must migrate first)",
        "",
        "| Blocked story | Domain | Waits on |",
        "|---|---|---|",
        "| `SPARK-PROD-F01` (attachments) | product | **attachment** |",
        "| `SPARK-PROD-F02` (discussions) | product | **discussion** |",
        "| `SPARK-PROD-F03` (sample) | product | **sample** |",
        "| `SPARK-PROD-F05` (claims) | product | **claim** |",
        "| `SPARK-PROD-F07` (constructions) | product | **construction** |",
        "| `SPARK-MEAS-F02` (sampleMeasurement) | measurement | **sample** |",
        "",
        "> Internal (NOT blockers, same `plm-product` subgraph): `SPARK-BOM-F01/F02`, `SPARK-PROD-F04/F06/F08`, "
        "`SPARK-MEAS-F01`, `SPARK-IMP-F01`, `SPARK-PDTL-F01`, `SPARK-PKG-F01`.",
        "",
        "---",
        "",
        "## How to consume",
        "",
        "- **Per domain:** open `summary/{domain}/FederatedGqlBrakDown-{domain}.md` (or the `.docx` for Confluence/Word).",
        "- **Jira:** import `jira/{domain}.csv` (or `jira/all-stories.csv`). See `PUSH-TO-JIRA-CONFLUENCE.md`.",
        "- **Read order by role + regeneration:** see `README.md`.",
        "",
        "---",
        f"*Program overview · generated {today} from `output/initial-analysis/*/04-*.md`.*",
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

        domain_dir = OUTPUT / domain
        domain_dir.mkdir(parents=True, exist_ok=True)

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
        # per domain — engineers work from initial-analysis/{domain}/04-stories.md.
        if full:
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

    print("\nDone. Run `python generate_all.py <domain>` to regenerate a single domain.\n")


if __name__ == "__main__":
    main()
