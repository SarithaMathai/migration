#!/usr/bin/env python3
"""
Generate FederatedGqlBrakDown-{domain}.md and Federated+Graphql+Stories+-+BreakDown.md.

Format mirrors the reference Word docs in 'final PO BreakDown Doc/':
  - Compact header banner
  - Scope · Effort · Sprint Sequencing · Capacity sections (from 04-po-summary.md)
  - Stories rendered as TABLES (one row per story) grouped by phase — Confluence-ready
  - High/VH tests shown beneath the phase table, not inline

Output:
  oneStopDoc/{domain}/FederatedGqlBrakDown-{domain}.md   (per domain)
  oneStopDoc/Federated+Graphql+Stories+-+BreakDown.md    (global)

Run:
    python generate_breakdown.py              # all domains + global
    python generate_breakdown.py attachment   # single domain
    python generate_breakdown.py --global     # global only
"""

import re
import sys
from pathlib import Path
from datetime import date

# ─── Paths ─────────────────────────────────────────────────────────────────────
HERE      = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
UPD_SRC   = HERE.parent.parent / "output" / "initial-analysis"
FALLBACK  = HERE.parent.parent / "output" / "initial-analysis"
OUT_DIR   = HERE.parent.parent / "output" / "summary"

# Published pages (Confluence/Jira) must link to the repo on GitHub, not a local file path.
GITHUB_REPO = "https://github.com/XXX"


def repo_linkify(text: str) -> str:
    """Turn backtick-wrapped repo article paths (complexStories/…, output/…, adrs/…, code/…) into
    clickable GitHub links, so a published breakdown page points at the article in the repo — not a
    meaningless local path. Folders → /tree/main, files → /blob/main."""
    def repl(m: "re.Match") -> str:
        path = m.group(1).rstrip("/")
        norm = path if path.startswith(("output/", "adrs/", "code/", "fedMigrationScripts/")) else "output/" + path
        seg  = "blob" if re.search(r"\.[A-Za-z0-9]+$", norm) else "tree"
        return f"[`{path}`]({GITHUB_REPO}/{seg}/main/{norm})"
    return re.sub(r"`((?:complexStories/|output/|adrs/|code/)[^`\s<>]+)`", repl, text)

# thirdAttempt scope: all 13 domains — the 8 phase-1 domains plus attachment,
# discussion, sample, search and workspace.
ALL_DOMAINS = [
    "attachment", "bom", "claims", "discussion", "impression",
    "measurement", "packaging", "product", "productDetails",
    "sample", "search", "watchlist", "workspace",
]

DOMAIN_LABELS = {
    "attachment":     "Attachment",
    "bom":            "Bill of Materials (BOM)",
    "claims":         "Claims",
    "discussion":     "Discussion",
    "impression":     "Impression",
    "measurement":    "Measurement",
    "packaging":      "Packaging",
    "product":        "Product",
    "productDetails": "Product Details",
    "sample":         "Sample",
    "search":         "Search",
    "watchlist":      "Watchlist",
    "workspace":      "Workspace",
}

DGS_MAP = {
    "product":        "plm-product (host)",
    "bom":            "plm-product (co-located)",
    "measurement":    "plm-product (co-located)",
    "packaging":      "plm-product (co-located)",
    "impression":     "plm-product (co-located)",
    "productDetails": "plm-product (co-located)",
    "watchlist":      "plm-product (co-located)",
    "workspace":      "plm-workspace (separate)",
    "sample":         "plm-sample (separate)",
    "discussion":     "plm-discussion (separate)",
    "attachment":     "plm-attachment (separate)",
    "search":         "plm-elastic-search (separate)",
    "claims":         "spark-claims (separate)",
}

PHASE_ICONS = {
    "S": "🔬", "A": "🧱", "B": "📖", "C": "🔍", "D": "✏️",
    "E": "⚙️", "F": "🔗", "G": "🧪",
}
PHASE_NAMES = {
    "S": "Spikes",
    "A": "Foundation & Type Resolvers",
    "B": "Core Reads",
    "C": "Search & Listing",
    "D": "Mutations",
    "E": "Complex Operations",
    "F": "Federation & Stitching",
    "G": "Field Resolvers & Tests",
}
TYPE_ICONS = {
    "query":          "🔷",
    "mutation":       "🔶",
    "field resolver": "🔸",
    "fieldresolver":  "🔸",
    "type resolver":  "🔸",
    "utility":        "🔹",
    "bug fix":        "🐛",
    "bugfix":         "🐛",
    "test":           "🧪",
    "spike":          "🔬",
}
DEFAULT_STATUS = "⬜ Not Started"
COMPLEXITY_ICONS = {
    "low":       "🟢",
    "medium":    "🟡",
    "high":      "🟠",
    "very high": "🔴",
}
SIZE_MAP = {"low": "XS", "medium": "M", "high": "L", "very high": "XL"}

TSHIRT_DATA = {
    "product":        (76, 330),
    "bom":            (42, 114),
    "workspace":      (32, 126),
    "discussion":     (37, 102),
    "sample":         (33, 116),
    "packaging":      (26,  72),
    "attachment":     (26,  71),
    "measurement":    (20,  55),
    "claims":         (22,  62),
    "search":         (21,  99),
    "productDetails": (13,  42),
    "watchlist":      (13,  44),
    "impression":     ( 7,  18),
}

def tshirt(domain: str) -> str:
    stories, ehi = TSHIRT_DATA.get(domain, (0, 0))
    if stories >= 60 or ehi >= 200: return "XXL"
    if stories >= 35 or ehi >= 100: return "XL"
    if stories >= 25 or ehi >= 60:  return "L"
    if stories >= 15 or ehi >= 40:  return "M"
    if stories >= 8  or ehi >= 20:  return "S"
    return "XS"


# ─── Program-level spikes (cross-domain complex buckets) ──────────────────────
# Per-domain spike/decision tables are GONE. Every genuinely complex, cross-cutting
# problem is generalized into ONE of these buckets and tracked once, globally.
# A domain story that is gated on a bucket is marked 🔴🔬 in its phase table and
# lists the SPARK-SPIKE-0x id in Depends On.
SPIKE_TITLES = {
    "01": "Non-Atomic Write Saga",
    "02": "TechPack Aggregate",
    "03": "Partner Drop/Undrop + Ownership",
    "04": "Not-Removable / Undroppable Partners",
    "05": "Polymorphic Type Resolution",
    "06": "Cross-Domain Association / Hydration",
}
# Story-id → spike bucket. Any Phase-E story defaults to bucket 01 (multi-step write
# saga); the entries below override that default or flag a non-E complex story.
SPIKE_OVERRIDES = {
    "SPARK-PROD-E01": "03",   # productBusinessPartnerActions — partner drop/undrop
    "SPARK-PROD-E03": "02",   # getProductTechPack…          — TechPack aggregate
    "SPARK-PROD-E04": "02",   # getProductTechPackBulk…      — TechPack aggregate
    "SPARK-WS-E01":   "03",   # workspaceBusinessPartnerActions — partner drop/undrop
    "SPARK-BOM-A04":  "05",   # BOM material @DgsTypeResolver — polymorphic
    "SPARK-SMPL-B01": "05",   # SampleAsset union            — polymorphic
    "SPARK-SRCH-A02": "05",   # search value-type resolution — polymorphic
    "SPARK-PROD-G07": "04",   # unDroppablePartners          — not-removable read aggregation
    "SPARK-WS-G05":   "04",   # workspace partners           — not-removable read aggregation
    "SPARK-WS-D04":   "06",   # addResourcesToWorkspaceV2    — cross-domain association
    "SPARK-WS-G04":   "06",   # Workspace.products           — cross-domain association/hydration
    # Cross-domain association / hydration (bucket 06) — these B/C/D research items were raised in
    # PO review (SPARK-PROD-S01 "association pattern", SPARK-PROD-S02 "two-stage hydration",
    # SPARK-BOM-S02 "material federation rollout order") and the domain Effort/Sprint tables already
    # declare them gated on SPARK-SPIKE-06 — but the gating never reached this map. See each domain's
    # 04-po-summary.md "Decisions Required" table for the source of truth.
    "SPARK-PROD-C01": "06",   # getProducts two-stage hydration          — SPARK-PROD-S02
    "SPARK-PROD-D01": "06",   # addProduct (workspace + attachment assoc) — SPARK-PROD-S01
    "SPARK-PROD-D02": "06",   # addProducts bulk (attachment links)      — SPARK-PROD-S01
    "SPARK-PROD-D03": "06",   # bulkUpdateProducts (mass assoc update)   — SPARK-PROD-S01
    "SPARK-PROD-D04": "06",   # updateProduct (attachment cleanup)       — SPARK-PROD-S01
    "SPARK-PROD-D06": "06",   # addTeamsToProduct (team/workspace)       — SPARK-PROD-S01
    "SPARK-PROD-D07": "06",   # addBusinessPartnersToProductWithType     — SPARK-PROD-S01
    "SPARK-PROD-D11": "06",   # updateWorkspaceAttributes                — SPARK-PROD-S01
    "SPARK-BOM-B05":  "06",   # getBomMaterialTypes (Material-Hub merge) — SPARK-BOM-S02 (rollout order)
}


def spike_for(story: dict) -> str | None:
    """Return the SPARK-SPIKE bucket number this story is gated on, or None."""
    sid = story["id"]
    if sid in SPIKE_OVERRIDES:
        return SPIKE_OVERRIDES[sid]
    if story.get("phase") == "E":
        return "01"
    return None


def spike_how_to_read() -> list[str]:
    """A short 'how to read the spikes' guide for the two audiences — global doc only."""
    return [
        "## How to read the spikes & related stories",
        "",
        "> The `SPARK-SPIKE-0x` id is the join key between a **program spike** (here) and the **domain stories** "
        "it gates. Read **global → domain** to plan decisions, or **domain → global** to implement.",
        "",
        "**👔 Product Owner:**",
        "",
        "1. **Phase 0 — Program Spikes table** — what each spike blocks and its status. Nothing dependent starts until the spike's decision is recorded.",
        "2. **Spike Detail** (per bucket) — the brief, the **Decision to make**, the **intended steps**, and the resolver table (blast radius).",
        "3. **Sequencing** — `SPARK-SPIKE-01/02/03` are critical path (Sprint 0); `04/05/06` run in parallel. Assign an owner + timebox each.",
        "4. In a **domain page**, the *Spikes & Complex Cases* map lists which of that domain's stories are 🔴🔬-blocked — plan the domain around them.",
        "",
        "**🔧 Engineer:**",
        "",
        "1. In the **domain A–G table**, find your story. If it's **🔴🔬 with `SPARK-SPIKE-0x` in Depends On**, the complex part is blocked until that spike concludes — check its status first.",
        "2. **Follow the `SPARK-SPIKE-0x` id → Spike Detail**: the **intended cross-domain steps** (your target flow) + the resolver table (external services you'll call + what each resolver does today = your parity target).",
        "3. **Research so far** — the **Phase 0 — Program Spikes** table links each spike to its `complexStories/<case>/` brief.",
        "4. **Non-gated stories** (no 🔴🔬) — build straight from the story's Acceptance Criteria; no spike needed.",
        "5. **In Jira/CSV** — the spike is a `Spike` issue (`SPARK-SPIKE-0x`) with the brief + steps in its description; your gated story lists it in **Depends On**.",
        "",
        "> **One-line model —** *Product Owner:* \"which decisions block work, who owns them, when?\" → the spike table. "
        "*Engineer:* \"is my story blocked, and once unblocked what's the flow + who do I call?\" → follow the id to Spike Detail.",
        "",
        "---",
        "",
    ]


def program_spike_table() -> list[str]:
    """The single cross-domain SPIKE table, rendered on the global overview page only."""
    return [
        "## 🔬 Phase 0 — Program Spikes (cross-domain research buckets)",
        "",
        "> **Why this table lives here and not in the domain pages.** The same handful of hard problems recur "
        "across many domains under different operation names (e.g. every domain's multi-step `update*` write hits "
        "the *same* \"no rollback\" question). Rather than repeat a decision list on every domain page, each "
        "recurring problem is **generalized into one program spike bucket** below. A spike is **time-boxed "
        "research that produces a recorded decision** — not shipped code — and every domain story gated on one "
        "is marked **🔴🔬 in its domain page** with the spike id in `Depends On`.",
        "",
        "> 🔬 **A spike is only for a genuinely complex problem that needs a solve/migrate approach.** Simple, "
        "intuitive, one-off decisions (delete-vs-`@deprecate` drift ops, dead service-method audits, auth-token "
        "parity, sort pushdown, DTO request-shape) are **not** spikes — they are resolved inline in the owning "
        "story's acceptance criteria and no longer appear anywhere as a decision table.",
        "",
        "| Spike ID | Bucket / Generic Problem | Domains affected (home story) | Blocks | Research so far | Status |",
        "|---|---|---|---|---|---|",
        "| `SPARK-SPIKE-01` | 🔬 **Non-Atomic Write Saga** — a mutation fans out across ≥2 REST services "
        "(workspace-assoc · body · permissions · component-status) with no transaction; on partial failure state "
        "is left inconsistent. Choose the failure strategy: (a) compensating saga · (b) compensation-log + "
        "best-effort · (c) best-effort. | bom `E01` · claims `E01` · measurement `E01` · packaging `E01` · "
        "productDetails `E01` · sample `E01/E02` · watchlist `E01` · discussion `E01/E02` · product `E02` | all "
        "`E`-phase writes | `complexStories/non-atomic-write-saga/` (shared `WriteSaga`) | 🔴 Open — failure strategy to decide |",
        "| `SPARK-SPIKE-02` | 🔬 **TechPack Aggregate** — build a `ProductTechPack` entity where **every field is "
        "computed from a different microservice REST API**; pick the assembly pattern (A `extend type` · B elastic "
        "DGS · C orchestrator · D interface · E materialized). | product `E03/E04` | product techpack | "
        "`complexStories/techpack/` | 🔴 Open — assembly pattern to decide |",
        "| `SPARK-SPIKE-03` | 🔬 **Partner Drop/Undrop + Ownership** — orchestrated drop/undrop of a business "
        "partner across every referencing child domain; decide ownership (domain subgraph vs workspace) and the "
        "write saga. | product `E01` · workspace `E01` · attachment · discussion · sample | partner-write "
        "`E`/`F` | `complexStories/partner-drop-undrop-write/` | 🔴 Open — ownership + orchestration to decide |",
        "| `SPARK-SPIKE-04` | 🔬 **Not-Removable / Undroppable Partners** — read aggregation computing which "
        "partners cannot be removed/dropped because still referenced (cross-domain `@requires` union). | product "
        "`E01` · workspace `E01` | partner-read fields | "
        "`complexStories/notRemovable-undroppable-partners/` | 🔴 Open — contribution contract to agree |",
        "| `SPARK-SPIKE-05` | 🔬 **Polymorphic Type Resolution** — interfaces/unions resolved by a category "
        "dispatcher; confirm the full `code → type` table + union membership, then `@DgsTypeResolver` + per-variant "
        "+ CI schema-conformance. | bom `A04` · sample `B01` (`SampleAsset` union) · search `A02` | type-resolver + "
        "variant fields | `complexStories/polymorphic-type-resolution/` | 🔴 Open — code→type table to confirm |",
        "| `SPARK-SPIKE-06` | 🔬 **Cross-Domain Association / Hydration** — how a domain references another's "
        "entity (federated `@key` ref vs REST client); two-stage hydration; federation/read-hub rollout ordering "
        "across sibling DGS. | product `S01/S02` · workspace `D04/G04` · search (read-hub order) · bom (material "
        "rollout) | association + hydration + rollout | "
        "`complexStories/cross-domain-association/` | 🔴 Open — per-edge rule to decide |",
        "",
        "> **Sequencing:** `SPARK-SPIKE-01/02/03` are on the critical path (they block `E`-phase writes and "
        "TechPack); run them in Sprint 0 alongside each domain's `B01` module scaffold. `04/05/06` block specific "
        "reads and can run in parallel. Each spike concludes with the decision recorded back into the affected "
        "domain stories.",
        "",
        "---",
        "",
    ]


# ─── Spike detail (layman + per-resolver: external deps + current logic) ───────
SPIKE_LAYMAN = {
    "01": "Some “save” buttons actually fire two or three separate backend calls in a row (e.g. first "
          "update which workspaces a record belongs to, then save the record body, then save its permissions). "
          "There is no database transaction across them, so if call 2 or 3 fails, call 1 is already committed and "
          "nothing undoes it — the record is left half-saved. This spike picks one consistent way to detect and "
          "recover from that partial failure for every write of this shape.",
    "02": "A “TechPack” is one screen that shows counts and lists pulled from ~8 different backend services "
          "(attachments, discussions, samples, claims, BOMs, measurements, constructions, watchlists). Today a single "
          "gateway helper calls all of them and adds up the numbers. This spike decides how to assemble that one "
          "entity under federation so each service owns and contributes its own slice.",
    "03": "When a business partner is dropped or undropped from a product or workspace, every child domain that "
          "references that partner has to be updated too. This spike decides who orchestrates that fan-out write "
          "and how it recovers if one of the child updates fails midway.",
    "04": "The UI needs to know which partners can’t be removed yet because something still references them. "
          "Answering that means asking several domains “do you still use this partner?” and combining the "
          "answers. This spike designs that cross-domain read.",
    "05": "Some GraphQL types are interfaces or unions — one field can return one of several concrete shapes, "
          "chosen by a category code. This spike confirms the full code→type mapping and how the resolver "
          "dispatches each row to the right variant.",
    "06": "One domain often needs another domain’s object (e.g. a `product` on a `bom`). This spike decides "
          "whether to stitch it as a federated `@key` reference or call the other service directly, plus the order "
          "the services must ship so nothing launches half-wired.",
}
SPIKE_DECISION = {
    "01": "Pick (a) compensating saga, (b) compensation-log + best-effort, or (c) best-effort — and write down how to undo each step.",
    "02": "Confirm the assembly pattern (chosen: Option A, `extend type ProductTechPack`) and each domain’s contribution.",
    "03": "Decide ownership (domain subgraph vs workspace) and the write-saga/rollback for the drop/undrop fan-out.",
    "04": "Agree the `@requires` contribution each domain exposes and where the union is computed.",
    "05": "Confirm the `code → type` table + union membership, then wire `@DgsTypeResolver` + CI conformance.",
    "06": "Choose federated `@key` reference vs REST client per edge, and the cross-DGS rollout order.",
}
# Intended cross-domain interaction steps per bucket — the target flow, in order,
# so an engineer can follow what talks to what. Shown under each gated story (domain doc)
# and once per bucket (global Spike Detail).
SPIKE_STEPS = {
    "01": [
        "Open a **write-saga** and record each step so it can be undone",
        "PUT **workspace-association** first (compensatable — remembers add/remove to reverse)",
        "PUT the **record body** (typed validation exception on error)",
        "PUT **permissions/partners** only if the input carries them",
        "On any step failure → run the chosen strategy: compensate (saga) or log + best-effort",
    ],
    "02": [
        "Gateway resolves the `ProductTechPack` **`@key`** (product id → shell entity)",
        "Fans out **in parallel** to each contributing subgraph (attachments · discussions · samples · claims · BOMs · measurements · constructions · watchlists)",
        "Each subgraph returns **only its own slice** (its count/list) — it owns that field",
        "Gateway **stitches** the slices into one `ProductTechPack` response",
    ],
    "03": [
        "Owner (product/workspace) receives the **drop/undrop** request and starts the orchestration",
        "**Fans out** the write to every child domain that references the partner",
        "Each child applies its change with **per-target failure isolation** (one failure is visible, doesn't swallow the rest)",
        "On partial failure → compensate/log per the SPIKE-01 saga",
    ],
    "04": [
        "Owner exposes the public field (`notRemovablePartnerIds` / `unDroppablePartners`)",
        "Each contributing domain declares its refs as **`@external`**; owner **`@requires`** them",
        "Gateway fetches every domain's contribution and **batches** them",
        "Owner resolver **unions + dedupes** into the final answer",
    ],
    "05": [
        "Read the row's **category code** (or union discriminator)",
        "`@DgsTypeResolver` maps code → **concrete type** (unknown → base type)",
        "Resolve the **per-variant** field set for that concrete type",
        "CI **schema-conformance** check fails the build if a variant misses an interface field",
    ],
    "06": [
        "Decide the edge shape: **federated `@key` reference** vs a direct **REST client** call",
        "If `@key`: emit the key and let the **owning subgraph** hydrate it (gateway hop)",
        "If REST: call the other service **in-process/directly** and map the result",
        "Sequence the **rollout order** so no consumer launches before its provider is federated",
    ],
}
SPIKE_CASE_FOLDER = {
    "01": "non-atomic-write-saga",
    "02": "techpack",
    "03": "partner-drop-undrop-write",
    "04": "notRemovable-undroppable-partners",
    "05": "polymorphic-type-resolution",
    "06": "cross-domain-association",
}
KIND_LABEL = {"query": "Query", "mutation": "Mutation", "field resolver": "Field resolver",
              "type resolver": "Type resolver"}


def minimal_logic(s: dict) -> str:
    """One-line, plain-language 'what it does today' for a resolver — de-jargoned:
    raw REST paths, loader syntax, camelCase-plumbing and ACL footnotes are stripped so the
    line reads as the *shape of the flow*, not implementation trivia."""
    t = clean_plain(s.get("current") or s.get("target") or "")
    # ACL/permission footnotes — not the flow.
    t = re.sub(r"\(ACL[^)]*\)", "", t, flags=re.I)
    t = re.sub(r"ACL note[^.;]*[.;]", "", t, flags=re.I)
    # Ownership / severity markers: "(own)", "(🔴 search)" → keep the service name only.
    t = re.sub(r"\(own\)\s*", "", t)
    t = re.sub(r"\(\s*[🔴🟡🔵]\s*([a-zA-Z0-9 _-]+?)\s*\)", r"(\1)", t)
    t = re.sub(r"[🔴🟡🔵]\s*", "", t)
    # Raw REST endpoints: "GET {base}/…/bom/v1?ids={ids}" → "GET …" (verb kept, URL dropped).
    t = re.sub(r"\b(GET|POST|PUT|DELETE|PATCH)\s+[`'\"]?[/{][^\s;,]*", r"\1 …", t)
    t = re.sub(r"\{base\}[^\s;,]*", "…", t)
    # Loader / method plumbing and camelCase-conversion chatter.
    t = re.sub(r"\.load\([^)]*\)", "", t)
    t = re.sub(r"→\s*deep(?:To)?[Cc]amel[Cc]ase|→\s*camel[Cc]ase(?:\s+list)?", "→ camelCase", t)
    t = re.sub(r"\s+", " ", t).strip(" ;,.")
    t = re.sub(r"^\d+[.)]\s*", "", t)          # drop a leading list marker ("1. …")
    t = re.sub(r"^(?:then|and)\s+", "", t, flags=re.I)
    if not t:
        return "—"
    if len(t) > 170:                           # trim at a clean word boundary, not mid-word
        cut = t[:168]
        sp  = cut.rfind(" ")
        t   = (cut[:sp] if sp > 120 else cut).rstrip(" ,;:") + "…"
    return t.replace("|", "\\|")


def build_spike_detail(domain_data: list[tuple]) -> list[str]:
    """Per-bucket plain-English detail + a resolver table (external deps + current logic),
    auto-built from the parsed stories that map to each spike. Regenerates with the source."""
    # bucket -> list of (domain, story)
    buckets: dict[str, list] = {b: [] for b in SPIKE_TITLES}
    for row in domain_data:
        domain, stories = row[0], row[9]
        for s in stories:
            b = spike_for(s)
            if b:
                buckets[b].append((domain, s))

    lines = [
        "## 🔬 Spike Detail — the brief + the resolvers each spike touches",
        "",
        "> For each spike: what it means, the decision to make, and the exact "
        "queries/mutations/field-resolvers it covers — with the **external services each one calls today** and a "
        "**one-line summary of its current logic**, so an engineer knows what to look at before starting.",
        "",
    ]
    for b in sorted(SPIKE_TITLES):
        rows = buckets.get(b, [])
        lines += [
            f"### 🔬 `SPARK-SPIKE-{b}` · {SPIKE_TITLES[b]}",
            "",
            *[f"- {sent.strip()}" for sent in re.split(r"(?<=[.!?]) +(?=[A-Z`])", SPIKE_LAYMAN[b]) if sent.strip()],
            "",
            f"**Decision to make:** {SPIKE_DECISION[b]}",
            "",
            "**Intended cross-domain steps:**",
            "",
        ]
        lines += [f"{i}. {st}" for i, st in enumerate(SPIKE_STEPS.get(b, []), 1)]
        lines.append("")
        if rows:
            lines += [
                "| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |",
                "|---|---|---|---|---|",
            ]
            for domain, s in rows:
                kind = KIND_LABEL.get(s["type"], s["type"].title())
                ext  = ", ".join(f"`{e}`" for e in s["ext_services"]) or "— (internal only)"
                title = s["title"].replace("|", "\\|")
                lines.append(f"| 🔴🔬 `{s['id']}` {title} | {domain} | {kind} | {ext} | {minimal_logic(s)} |")
            lines.append("")
        lines += ["", "---", ""]
    return lines


# ─── Source resolution ─────────────────────────────────────────────────────────
def get_domain_dir(domain: str) -> Path:
    for src in [FALLBACK / domain]:
        if (src / "04-stories.md").exists():
            return src
    raise FileNotFoundError(f"No source for '{domain}'")


# ─── Text helpers ──────────────────────────────────────────────────────────────
STORY_HEADER_RE = re.compile(
    r"^### (SPARK-[A-Z]+-[A-Za-z0-9]+(?:-\d+)?) · (.+)$", re.MULTILINE
)
META_RE    = re.compile(r"\*\*Type:\*\*\s*([^·\n]+).*?\*\*Complexity:\*\*\s*([^·\n]+)", re.DOTALL)
PHASE_RE   = re.compile(r"\*\*Phase:\*\*\s*([A-Z])\b")
DEPENDS_RE = re.compile(r"\*\*Depends on:\*\*\s*([^\n*·]+)")
EXT_RE     = re.compile(r"\*\*EXT:\*\*\s*([^\n]+)")
BLOCKED_RE = re.compile(r"\*\*Blocked by:\*\*\s*([^\n]+)")
COVERS_RE  = re.compile(r"\*\*Covers:\*\*\s*([^\n]+)")
STATUS_RE  = re.compile(r"\*\*Status:\*\*\s*([^\n*·]+)")
ADR_RE     = re.compile(r"\*\*ADR:\*\*\s*([^\n]+)")


def dedupe_ids(raw: str) -> str:
    """Collapse a comma-separated dependency list to unique ids, preserving order.
    Fixes the 'B01, B01' class of bug left over from the Phase-A-dissolved-into-B01 rename."""
    if not raw or raw.strip() in ("—", ""):
        return raw
    seen: list[str] = []
    for part in raw.split(","):
        p = part.strip()
        if p and p not in seen:
            seen.append(p)
    return ", ".join(seen) if seen else raw
INTENT_RE  = re.compile(r"\*\*In plain terms:?\*\*\s*([^\n]+)")
NOTE_RE    = re.compile(r"^> \*\*Note[^*]*\*\*[^\n]*(?:\n>.*)*", re.MULTILINE)
CB_RE      = re.compile(
    r"\*\*Current Behaviour[^:]*:\*\*\s*(.*?)(?=\s*(?:-\s*)?\*\*Target)", re.DOTALL
)
TGT_RE     = re.compile(r"\*\*Target[^:\n]*:\*\*\s*([^\n.]+)")


def clean_ac(t: str) -> str:
    """Strip links, collapse whitespace; preserve backticks and bold."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\s+", " ", t.replace("\n", " "))
    return t.strip().rstrip(".")


def clean_plain(t: str) -> str:
    """Strip all markdown — for metadata fields."""
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*",     r"\1", t)
    t = re.sub(r"`([^`]+)`",       r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.strip()


def strip_noise(text: str) -> str:
    """Remove only genuine noise: 'Phase A dissolved' blockquote notes and pipeline footers.
    Does NOT delete legit Phase-A story rows/refs — BOM's `A04` type-resolver is a real story."""
    text = re.sub(r"^>.*[Pp]hase A dissolved[^\n]*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^>.*No separate Phase A[^\n]*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\*Pipeline 2\.0[^\n]*\n?", "",   text, flags=re.MULTILINE)
    return text.strip()


def strip_relative_links(text: str) -> str:
    """Confluence/Jira-safe: convert relative markdown links to plain text (they break once the
    page is hosted). Keep http(s) links and in-page #anchors clickable."""
    def repl(m: "re.Match") -> str:
        label, url = m.group(1), m.group(2)
        return m.group(0) if url.startswith(("http://", "https://", "#")) else label
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


# Complex-story breakdowns live in generate_comprehensive; import so the Confluence breakdown shows them.
try:
    from generate_comprehensive import COMPLEX_STORIES
except Exception:
    COMPLEX_STORIES = {}


def render_complex_section(domain: str) -> list[str]:
    """A 'Complex Story Breakdowns' section for the Confluence breakdown: parent → sub-tasks → case."""
    data = COMPLEX_STORIES.get(domain)
    if not data:
        return []
    out = [
        "## Complex Story Breakdowns",
        "",
        data.get("intro", "Some stories were broken into M-size (≤5 day) sub-tasks."),
        "",
        "| Parent story | Sub-tasks (each M, 3–5d) | Detailed cross-domain case |",
        "|---|---|---|",
    ]
    for r in data.get("very_high", []) + data.get("high", []):
        case = f"`complexStories/{r['complex_case']}/`" if r.get("complex_case") else "—"
        out.append(f"| `{r['id']}` {r['name']} | {r['subtasks']} | {case} |")
    for r in data.get("delegated", []):
        case = r["case"].rstrip("/").split("/")[-1]
        out.append(f"| `{r['id']}` {r['name']} | delegated | `complexStories/{case}/` |")
    out += [
        "",
        "> Parent stories are milestones (0 points); sub-tasks nest under them in Jira. Each detailed case "
        "folder has its own `{case}.csv` to import the sub-tasks.",
        "",
        "---",
        "",
    ]
    return out


def extract_section(text: str, *headers: str) -> str:
    """Extract first matching `## Header` section; try all header variants."""
    for h in headers:
        pat = rf"## {re.escape(h)}\s*\n(.*?)(?=\n## |\Z)"
        m = re.search(pat, text, re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""


def extract_named_sub(body: str, header: str) -> str:
    pattern = rf"#### {re.escape(header)}\s*\n(.*?)(?=\n####|\n---|\n###|\Z)"
    m = re.search(pattern, body, re.DOTALL)
    return m.group(1).strip() if m else ""


# ─── Story parser ──────────────────────────────────────────────────────────────
def parse_stories(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text    = path.read_text(encoding="utf-8")
    matches = list(STORY_HEADER_RE.finditer(text))
    out     = []
    for i, m in enumerate(matches):
        sid   = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body  = text[start:end]

        meta           = META_RE.search(body)
        op_type_raw    = meta.group(1).strip() if meta else "Story"
        complexity_raw = meta.group(2).strip() if meta else ""
        if not complexity_raw:
            yaml_c = re.search(r"\bcomplexity:\s*([A-Za-z ]+)", body, re.IGNORECASE)
            complexity_raw = yaml_c.group(1).strip() if yaml_c else "Low"
        complexity = re.sub(r"[⚠️🔶⚪]\s*", "", complexity_raw).strip().lower()

        phase_m = PHASE_RE.search(body)
        if phase_m:
            phase = phase_m.group(1)
        else:
            yaml_p = re.search(r"\bphase:\s*([A-G])\b", body, re.IGNORECASE)
            if yaml_p:
                phase = yaml_p.group(1).upper()
            else:
                id_p = re.search(r"SPARK-[A-Z]+-([A-G])\d", sid)
                phase = id_p.group(1) if id_p else "?"

        dep_m    = DEPENDS_RE.search(body)
        ext_m    = EXT_RE.search(body)
        blk_m    = BLOCKED_RE.search(body)
        cov_m    = COVERS_RE.search(body)
        note_m   = NOTE_RE.search(body)
        intent_m = INTENT_RE.search(body)
        cb_m     = CB_RE.search(body)
        tgt_m    = TGT_RE.search(body)
        status_m = STATUS_RE.search(body)
        adr_m    = ADR_RE.search(body)

        ac_sec   = extract_named_sub(body, "Acceptance Criteria")
        ac_items = re.findall(r"\d+\.\s*(.+?)(?=\n\d+\.|\Z)", ac_sec, re.DOTALL)
        ac       = [clean_ac(x) for x in ac_items if x.strip()]

        tests_sec  = extract_named_sub(body, "Test Cases")
        test_items = re.findall(r"- \[ \]\s*(.+)", tests_sec)
        if not test_items:
            test_items = re.findall(r"- \[[ x]\]\s*(.+)", tests_sec)
        tests = [clean_ac(x) for x in test_items]

        op_type = clean_plain(op_type_raw).lower()

        # Infer type when source says "story" (some domains use generic type)
        if op_type in ("story", ""):
            title_l = title.lower()
            if any(k in title_l for k in ("data fetcher", "query", "search", "get", "list", "fetch")):
                op_type = "query"
            elif any(k in title_l for k in ("mutation", "update", "create", "delete", "archive",
                                             "add", "remove", "bulk", "publish", "copy")):
                op_type = "mutation"
            elif any(k in title_l for k in ("field resolver", "field resolvers", "extension",
                                             "parity", "test coverage", "tests")):
                op_type = "field resolver"
            elif phase in ("B", "C"):
                op_type = "query"
            elif phase in ("D", "E"):
                op_type = "mutation"
            elif phase in ("F", "G"):
                op_type = "field resolver"

        # Depends on — strip to just story IDs for table readability, deduped.
        # Also drop references to now-removed domain spikes (bare `S0x` or `SPARK-*-S0x`) —
        # spikes are centralized as program spikes; spike-gating is shown via SPARK-SPIKE-0x.
        raw_dep = dep_m.group(1).strip() if dep_m else "—"
        raw_dep = re.sub(r"\b(?:SPARK-[A-Z]+-)?S\d+\b", "", raw_dep)
        raw_dep = re.sub(r"\s*,\s*,\s*", ", ", raw_dep).strip(" ,")
        depends = dedupe_ids(re.sub(r"\s+", " ", raw_dep).strip() or "—") or "—"

        # External services the resolver calls — harvested from `EXT → key: `x`` blocks
        # and inline severity tokens (🔴/🟡/🔵 `x`). Used by the spike-detail tables.
        ext_services: list[str] = []
        for k in re.findall(r"key:\s*`([^`]+)`", body) + re.findall(r"[🔴🟡🔵]\s*`([^`]+)`", body):
            if k not in ext_services:
                ext_services.append(k)

        out.append({
            "id":         sid,
            "title":      title,
            "type":       op_type,
            "complexity": complexity,
            "phase":      phase,
            "depends":    depends,
            "ext":        ext_m.group(1).strip() if ext_m else "",
            "blocked":    blk_m.group(1).strip() if blk_m else "",
            "covers":     cov_m.group(1).strip() if cov_m else "",
            "note":       note_m.group(0).strip() if note_m else "",
            "current":    cb_m.group(1).strip() if cb_m else "",
            "target":     tgt_m.group(1).strip() if tgt_m else "",
            "ac":         ac,
            "tests":      tests,
            "status":     status_m.group(1).strip() if status_m else DEFAULT_STATUS,
            "adr":        adr_m.group(1).strip() if adr_m else "—",
            "ext_services": ext_services,
            "intent":     intent_m.group(1).strip() if intent_m else "",
        })
    return out   # keep Phase A — the type-resolver story (e.g. BOM A04) is real, not dissolved


def group_by_phase(stories: list[dict]) -> dict[str, list]:
    g: dict[str, list] = {}
    for s in stories:
        g.setdefault(s["phase"], []).append(s)
    return dict(sorted(g.items()))


# ─── PO summary parser ────────────────────────────────────────────────────────
def read_po_sections(po_path: Path) -> dict[str, str]:
    if not po_path.exists():
        return {}
    text = strip_noise(po_path.read_text(encoding="utf-8"))
    return {
        "what":      extract_section(text, "What Are We Building?"),
        "deploy":    extract_section(text, "Deployment model — ship on green, per story", "Deployment model"),
        "scope":     extract_section(text, "Migration Scope"),
        "phases":    extract_section(text,
                        "Story Summary by Phase (AI-estimated)",
                        "Story Summary by Phase"),
        "risks":     extract_section(text,
                        "Key Risk Areas",
                        "Key Risk Areas (plain English)"),
        "decisions": extract_section(text,
                        "Decisions Required",
                        "Decisions Required from Product Owner"),
        "deps":      extract_section(text, "Dependency Map"),
        "sprints":   extract_section(text, "Recommended Sprint Sequencing"),
        "capacity":  extract_section(text, "Capacity Planning"),
    }


# ─── Phase renderer (one row per story — tabular) ─────────────────────────────
def md_cell(text: str) -> str:
    """Escape a value for use inside a Markdown table cell: pipes escaped, newlines → <br>."""
    return text.replace("|", "\\|").replace("\n", "<br>")


def _ac_cell(s: dict) -> str:
    """Build the Acceptance Criteria cell: Intent, Today, then bulleted Done-when — one cell,
    <br>-separated so it renders as stacked lines in Markdown/Confluence tables."""
    parts: list[str] = []
    if s.get("intent"):
        parts.append(f"**Intent —** {s['intent'].strip()}")
    today = minimal_logic(s)
    if today and today != "—":
        parts.append(f"**Today —** {today}")
    if s["ac"]:
        parts.append("**Done when:**")
        parts += [f"• {a}" for a in s["ac"]]
    return md_cell("<br>".join(parts)) if parts else "—"


def _tests_cell(s: dict) -> str:
    """Key-Tests cell for a High/Very-High story: ☐ checkboxes, <br>-separated. Else —."""
    if s["tests"] and s["complexity"] in ("high", "very high"):
        return md_cell("<br>".join(f"☐ {t}" for t in s["tests"]))
    return "—"


def render_phase_table(phase_key: str, stories: list[dict]) -> list[str]:
    """Render the phase's stories as a Markdown table — one row per story. Intent, Today and
    Done-when live together in the **Acceptance Criteria** column; **Key Tests** is a separate
    column shown ONLY for complex phases (those containing a High / Very High story)."""
    lines: list[str] = []

    # A "complex phase" carries the Key Tests column; simple phases omit it entirely.
    complex_phase = any(s["complexity"] in ("high", "very high") for s in stories)

    headers = ["Story", "Complexity", "Type", "Depends On", "Acceptance Criteria"]
    if complex_phase:
        headers.append("Key Tests")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "---|" * len(headers))

    for s in stories:
        cl    = s["complexity"]
        cicon = COMPLEXITY_ICONS.get(cl, "⚪")
        size  = SIZE_MAP.get(cl, "?")
        ticon = TYPE_ICONS.get(s["type"], "📄")
        tname = s["type"].title()

        spk  = spike_for(s)
        flag = "🔴🔬 " if spk else ""

        # Story cell — id + title, plus a spike-gated note when applicable.
        story_cell = f"{flag}{ticon} `{s['id']}`<br>{s['title']}"
        if spk:
            story_cell += (f"<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-{spk}` "
                           f"({SPIKE_TITLES.get(spk, '')}) — see global Spike Detail_")

        # Type cell — surface external Calls only when there are any (internal-only is noise).
        type_cell = tname
        if s["ext_services"]:
            type_cell += "<br>Calls: " + ", ".join(f"`{e}`" for e in s["ext_services"])

        # Depends cell — link the program spike first when the story is gated.
        dep = s["depends"]
        if spk:
            sref = f"SPARK-SPIKE-{spk}"
            dep  = sref if dep in ("—", "") else f"{sref}, {dep}"

        row = [
            md_cell(story_cell),
            f"{cicon} {cl.title()} `{size}`",
            md_cell(type_cell),
            md_cell(dep),
            _ac_cell(s),
        ]
        if complex_phase:
            row.append(_tests_cell(s))
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    # DGS init notes (B01-type) — kept as callouts beneath the table.
    for s in stories:
        if s["note"]:
            note_clean = strip_noise(s["note"])
            if note_clean:
                lines += [f"> **`{s['id']}`** — {note_clean.lstrip('> ').strip()}", ""]

    return lines


# ─── Spike table renderer (Phase 0 — visually distinct from regular stories) ──
def render_spike_table(stories: list[dict]) -> list[str]:
    """Render Phase 0 spikes, wrapped in a highlighted callout so it reads as
    research, not committed delivery."""
    lines: list[str] = [
        "> 🔬 **SPIKE — time-boxed research, not fixed-scope delivery.** Output is a recorded "
        "decision — not shipped code. Downstream stories stay blocked until "
        "the spike concludes and the decision is recorded back into this doc.",
        "",
        "| Story ID | Summary | Type | Complexity | Depends On | Status | Acceptance Criteria |",
        "|---|---|---|---|---|---|---|",
    ]

    for s in stories:
        cl    = s["complexity"]
        cicon = COMPLEXITY_ICONS.get(cl, "⚪")
        size  = SIZE_MAP.get(cl, "?")
        # One criterion per line — points, not a paragraph blob.
        ac_cell = "<br>".join(f"• {a}" for a in s["ac"]) if s["ac"] else "—"
        ac_cell = ac_cell.replace("|", "\\|")

        lines.append(
            f"| `{s['id']}` | 🔬 **{s['title']}** | 🔬 Spike | "
            f"{cicon} {cl.title()} `{size}` | {s['depends']} | {s['status']} | {ac_cell} |"
        )

    return lines


# ─── Domain breakdown builder ─────────────────────────────────────────────────
def build_breakdown(domain: str) -> str:
    label    = DOMAIN_LABELS[domain]
    dgs      = DGS_MAP[domain]
    today    = date.today().isoformat()
    ts       = tshirt(domain)
    src_dir  = get_domain_dir(domain)
    # Spike (Phase-S) stories are no longer domain-local — they are centralized as
    # program spikes on the global overview page, so drop them from every count and table.
    stories  = [s for s in parse_stories(src_dir / "04-stories.md") if s["phase"] != "S"]
    po       = read_po_sections(src_dir / "04-po-summary.md")
    by_phase = group_by_phase(stories)

    total = len(stories)
    vh    = sum(1 for s in stories if s["complexity"] == "very high")
    hi    = sum(1 for s in stories if s["complexity"] == "high")
    me    = sum(1 for s in stories if s["complexity"] == "medium")
    lo    = sum(1 for s in stories if s["complexity"] == "low")
    phases_covered = " · ".join(
        f"{PHASE_ICONS[k]} {k}" for k in sorted(by_phase.keys()) if k in PHASE_ICONS
    )

    lines: list[str] = [
        f"# Federated GraphQL Breakdown — {label}",
        "",
        f"| | |",
        f"|---|---|",
        f"| **Target DGS** | `{dgs}` |",
        f"| **T-Shirt Size** | **{ts}** |",
        f"| **Total Stories** | {total} |",
        f"| **Complexity** | 🔴 {vh} Very High · 🟠 {hi} High · 🟡 {me} Medium · 🟢 {lo} Low |",
        f"| **Phase Coverage** | {phases_covered} |",
        f"| **Generated** | {today} |",
        "",
        "> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  "
        "· 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  "
        "· 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G",
        "",
        "---",
        "",
    ]

    # §1 — What Are We Building
    if po.get("what"):
        lines += [
            "## What Are We Building?",
            "",
            po["what"],
            "",
            "---",
            "",
        ]

    # §2 — Migration Scope
    if po.get("scope"):
        lines += [
            "## Migration Scope",
            "",
            po["scope"],
            "",
            "---",
            "",
        ]

    # Phase 0 — Spikes are centralized on the global overview page (program spikes),
    # NOT repeated per domain. This section RELATES this domain's stories to those program
    # spikes (a compact map) and points to the single source for the full detail — so the
    # shared brief/steps/resolver-detail are never duplicated across the 13 domain pages.
    gated = [(s, spike_for(s)) for s in stories]
    gated = [(s, b) for s, b in gated if b]
    lines += [
        "## Spikes & Complex Cases",
        "",
        "> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global "
        "breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the "
        "decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in "
        "the \"Federated+Graphql+Stories+-+BreakDown\" overview. Nothing from there is repeated here; the stories below just "
        "**link** to it.",
        "",
    ]
    if gated:
        lines += [
            "**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in "
            "`Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the "
            "external services each resolver calls. See **How to read the spikes & related stories** in the "
            "global doc.)*",
            "",
            "| Story | Program spike | Bucket |",
            "|---|---|---|",
        ]
        for s, b in gated:
            lines.append(f"| 🔴🔬 `{s['id']}` — {s['title']} | `SPARK-SPIKE-{b}` | {SPIKE_TITLES[b]} |")
        lines += [
            "",
            f"> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and "
            f"cross-service resolver breakdown.",
            "",
        ]
    else:
        lines += ["> _No spike-gated stories in this domain._", ""]
    lines += [
        "> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) "
        "are resolved inline in the owning story — they are **not** spikes.",
        "",
        "---",
        "",
    ]

    # §2b — Deployment model (ship on green, per story)
    if po.get("deploy"):
        lines += [
            "## Deployment Model — Ship on Green, Per Story",
            "",
            po["deploy"],
            "",
            "---",
            "",
        ]

    # §3 — Effort by Phase + Capacity Planning
    if po.get("phases") or po.get("capacity"):
        lines += ["## Effort Snapshot", ""]
        if po.get("phases"):
            lines += [po["phases"], ""]
        if po.get("capacity"):
            lines += ["", "**Capacity Planning**", "", po["capacity"], ""]
        lines += ["---", ""]

    # §4 — Sprint Sequencing
    if po.get("sprints"):
        lines += [
            "## Recommended Sprint Sequencing",
            "",
            po["sprints"],
            "",
            "---",
            "",
        ]

    # §5 — Jira Stories by Phase (TABLE format)
    lines += [
        "## Jira Stories by Phase",
        "",
        "> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. "
        "`Depends On` lists blocking story IDs within this domain — including Phase 0 spikes "
        "where a story's implementation is gated on a spike's outcome.",
        "",
    ]

    if not stories:
        lines += ["_No stories found._", ""]
    else:
        for phase_key in sorted(by_phase.keys()):
            if phase_key == "S":
                continue   # spikes rendered above in §4b
            phase_icon  = PHASE_ICONS.get(phase_key, "📄")
            phase_name  = PHASE_NAMES.get(phase_key, f"Phase {phase_key}")
            ph_stories  = by_phase[phase_key]
            vh_count    = sum(1 for s in ph_stories if s["complexity"] == "very high")
            hi_count    = sum(1 for s in ph_stories if s["complexity"] == "high")

            lines += [
                f"### {phase_icon} Phase {phase_key} — {phase_name} ({len(ph_stories)} stories)",
                "",
            ]
            lines += render_phase_table(phase_key, ph_stories)
            lines.append("")

    # §5b — Complex Story Breakdowns and Decisions Required are intentionally REMOVED
    # from domain pages. Complex cross-domain cases are the program spikes (global page);
    # simple decisions are folded into their owning story's acceptance criteria.
    # (Key Risks and Dependency Map were already omitted.)

    text = "\n".join(lines)
    while "---\n\n---" in text:            # collapse consecutive horizontal rules
        text = text.replace("---\n\n---", "---")
    text = re.sub(r"\n+(?:---\s*)+$", "\n", text)   # drop any trailing horizontal rule
    return strip_relative_links(repo_linkify(text))


# ─── Global breakdown builder ─────────────────────────────────────────────────
def program_overview_preamble() -> list[str]:
    """Shared Overview / Glossary / Phases / T-Shirt front-matter for the global breakdown.
    Used by both the .md (build_global) and the .docx (generate_word) so they stay identical."""
    return [
        "## Overview",
        "",
        "We are migrating the entire Product Lifecycle Management (PLM) GraphQL API surface off the monolithic "
        "`spark-internal-graphql` Node.js gateway onto a set of independently owned **Netflix DGS** (Domain Graph "
        "Service) subgraphs, federated via the **Hive Schema Registry**.",
        "",
        "Each DGS is a Kotlin/Spring Boot service that exposes its domain's schema as a federated subgraph. The "
        "supergraph stitches them together transparently for clients.",
        "",
        "**Why?**",
        "",
        "- The monolith is a ~15,000-line Node.js resolver with no clear ownership boundaries",
        "- Federation gives each team autonomous schema ownership, independent deployability, and fine-grained caching",
        "- Netflix DGS provides production-proven tooling (DataLoaders, code generation, Hive integration)",
        "- Hive Schema Registry enforces schema contracts and enables safe rollout with schema checks",
        "",
        "**Engineering model:** every story is self-contained in one PR — schema additions, DGS data fetcher, "
        "Kotlin REST service method, and Hive registry push. There are no separate service-layer stories.",
        "",
        "**ACL note:** the current gateway obtains per-resource ACL capability tokens. ACL is **not** re-implemented "
        "in the DGS layer (decided at program level); it is noted in stories for context only.",
        "",
        "---",
        "",
        "## Glossary",
        "",
        "| Term | Meaning |",
        "|---|---|",
        "| **DGS** | Netflix Domain Graph Service — a Spring/Kotlin GraphQL subgraph |",
        "| **Hive Gateway / plm-gateway** | the federation gateway that composes the subgraphs into one supergraph |",
        "| **subgraph** | one DGS (e.g. `plm-product`, `plm-sample`) |",
        "| **co-located** | a domain compiling into `plm-product` (in-process call, not a gateway hop) |",
        "| **CAT-1…5** | story categories: 1 schema · 2 resolver · 3 service · 4 federation · 5 tests |",
        "| **Phase A–G** | the migration order within a domain (see the phases table below) |",
        "| **EXT severity** | 🔴 critical/sequential · 🟡 single enrichment call · 🔵 optional/gateway |",
        "",
        "---",
        "",
        "## The migration phases (A→G) — the order of replacement",
        "",
        "Stories are grouped into phases that encode the replacement order within a domain:",
        "",
        "| Phase | Replaces / builds | Category |",
        "|---|---|---|",
        "| **A** | schema skeleton, owned types, external stubs, `@DgsTypeResolver`, service port, ACL/JWT plumbing | CAT-1/CAT-3 |",
        "| **B / C** | query resolvers (reads) | CAT-2 |",
        "| **D** | mutation resolvers (writes) | CAT-2 |",
        "| **E** | complex operations (multi-step writes, aggregations) — often a stub + facade pointing at a complex case | CAT-2 |",
        "| **F** | federation boundaries — one story per cross-domain edge (`@extends @external`) | CAT-4 |",
        "| **G** | field resolvers (incl. the heavy ones) + the domain parity harness | CAT-2/CAT-5 |",
        "",
        "> **Phase 0 = Spikes** — time-boxed research producing a recorded decision before the phase it blocks.",
        "",
        "---",
        "",
    ] + spike_how_to_read() + program_spike_table() + [
        "## T-Shirt Size Classification",
        "",
        "| T-Shirt | Story count | Effort (high est., eng-days) | Rule | Typical scope |",
        "|---|---|---|---|---|",
        "| 🔴 **XXL** | ≥ 60 | ≥ 200 | stories ≥ 60 OR effort_hi ≥ 200 | Very large, cross-domain initiative |",
        "| 🔴 **XL** | 35–59 | 100–199 | stories ≥ 35 OR effort_hi ≥ 100 | Large feature or domain |",
        "| 🟠 **L** | 25–34 | 60–99 | stories ≥ 25 OR effort_hi ≥ 60 | Medium-large project |",
        "| 🟡 **M** | 15–24 | 40–59 | stories ≥ 15 OR effort_hi ≥ 40 | Medium-sized project |",
        "| 🟢 **S** | 8–14 | 20–39 | stories ≥ 8 OR effort_hi ≥ 20 | Small project |",
        "| 🟢 **XS** | < 8 | < 20 | otherwise | Minor enhancement or maintenance |",
        "",
        "---",
        "",
    ]


def build_global(domains: "list[str] | None" = None, scope_label: str = "All Domains") -> str:
    today   = date.today().isoformat()
    domains = domains or ALL_DOMAINS

    # Collect all domain data
    all_stats:   list[tuple] = []
    domain_data: list[tuple] = []
    grand_total = grand_vh = grand_hi = grand_me = grand_lo = 0

    for domain in domains:
        label = DOMAIN_LABELS[domain]
        dgs   = DGS_MAP[domain]
        ts    = tshirt(domain)
        try:
            src_dir  = get_domain_dir(domain)
            # Exclude Phase-S spikes — they are centralized as program spikes, not domain stories.
            stories  = [s for s in parse_stories(src_dir / "04-stories.md") if s["phase"] != "S"]
            po       = read_po_sections(src_dir / "04-po-summary.md")
        except FileNotFoundError:
            stories = []
            po      = {}

        total = len(stories)
        vh    = sum(1 for s in stories if s["complexity"] == "very high")
        hi    = sum(1 for s in stories if s["complexity"] == "high")
        me    = sum(1 for s in stories if s["complexity"] == "medium")
        lo    = sum(1 for s in stories if s["complexity"] == "low")
        grand_total += total
        grand_vh    += vh
        grand_hi    += hi
        grand_me    += me
        grand_lo    += lo
        all_stats.append((domain, label, dgs, ts, total, vh, hi, me, lo))
        domain_data.append((domain, label, dgs, ts, total, vh, hi, me, lo, stories, po))

    n_domains = len(domains)
    n_dgs     = len({DGS_MAP[d].split(" (")[0] for d in domains})
    is_custom = scope_label != "All Domains"

    # ── Cover page (banner) — same format as the per-domain breakdowns ────────────
    lines: list[str] = [
        f"# Federated GraphQL — Migration Overview · {scope_label}",
        "",
        (f"> **Scoped overview** — a rollup of **{n_domains} selected modules** "
         f"({', '.join(DOMAIN_LABELS[d] for d in domains)}). The full-program overview is the untouched "
         "`Federated+Graphql+Stories+-+BreakDown` page." if is_custom else
         "> **Program overview** — the full `spark-internal-graphql` → Netflix DGS migration at a glance. "
         "Each domain's phase tables live in its own FederatedGqlBrakDown-<domain> breakdown page (see the Domain "
         "Index); the complex, cross-cutting problems are centralized here as **program spikes** (below)."),
        "",
        "| | |",
        "|---|---|",
        "| **Program** | `spark-internal-graphql` → Netflix DGS Federation (Hive Schema Registry) |",
        f"| **Domains** | {n_domains} |",
        f"| **Target DGS services** | {n_dgs} |",
        f"| **Total Stories** | **{grand_total}** |",
        f"| **Complexity** | 🔴 {grand_vh} Very High · 🟠 {grand_hi} High · 🟡 {grand_me} Medium · 🟢 {grand_lo} Low |",
        "| **Phase Coverage** | 🔬 6 Spikes · 🧱 A Foundation · 📖 B Reads · 🔍 C Search · ✏️ D Mutations · ⚙️ E Complex · 🔗 F Federation · 🧪 G Field-resolvers/Tests |",
        "| **Cross-domain spikes** | 🔬 6 program-level research spikes — see *Phase 0 — Program Spikes* below. Only genuinely **complex** problems that need a solve/migrate approach are spikes; straightforward decisions are resolved inline in the owning story. |",
        f"| **Generated** | {today} |",
        "",
        "> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  "
        "· 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  "
        "· 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G",
        "",
        "---",
        "",
    ]
    lines += program_overview_preamble()
    lines += [
        "## Domain Index",
        "",
        "> Each domain's full story detail is in its own breakdown page (named in the last column).",
        "",
        "| # | Domain | Target DGS | T-Shirt | Stories | 🔴 VH | 🟠 High | 🟡 Med | 🟢 Low | Breakdown page |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]

    for i, (domain, label, dgs, ts, total, vh, hi, me, lo) in enumerate(all_stats, 1):
        lines.append(
            f"| {i} | **{label}** | `{dgs}` | **{ts}** | "
            f"**{total}** | {vh} | {hi} | {me} | {lo} | `FederatedGqlBrakDown-{domain}` |"
        )

    lines += [
        f"| | **TOTAL** | — | — | **{grand_total}** | "
        f"**{grand_vh}** | **{grand_hi}** | **{grand_me}** | **{grand_lo}** | — |",
        "",
        "---",
        "",
    ]

    # Spike detail — plain-English brief + per-resolver (external deps + current logic).
    lines += build_spike_detail(domain_data)

    # Per-domain story detail intentionally NOT included here — this is an overview.
    # Each domain's phase tables live in its own FederatedGqlBrakDown-<domain> breakdown.

    text = re.sub(r"\n+(?:---\s*)+$", "\n", "\n".join(lines))   # drop any trailing horizontal rule
    return strip_relative_links(repo_linkify(text))


# ─── Runner ────────────────────────────────────────────────────────────────────
def generate_breakdown_for(domain: str) -> None:
    out_subdir = OUT_DIR / domain
    out_subdir.mkdir(parents=True, exist_ok=True)
    content  = build_breakdown(domain)
    out_file = out_subdir / f"FederatedGqlBrakDown-{domain}.md"
    out_file.write_text(content, encoding="utf-8")
    print(f"  OK {domain}/FederatedGqlBrakDown-{domain}.md ({len(content):,} chars)")


def generate_global() -> None:
    content  = build_global()
    out_file = OUT_DIR / "Federated+Graphql+Stories+-+BreakDown.md"
    out_file.write_text(content, encoding="utf-8")
    print(f"  OK Federated+Graphql+Stories+-+BreakDown.md ({len(content):,} chars)")


# A second, scoped global page for a hand-picked set of modules (plm-product monorepo + claims).
# The default global page above is left untouched.
CUSTOM_DOMAINS = ["product", "bom", "claims", "productDetails", "packaging", "watchlist", "measurement", "impression"]


def generate_global_custom() -> None:
    content  = build_global(CUSTOM_DOMAINS, scope_label="Selected Modules")
    out_file = OUT_DIR / "Federated+Graphql+Stories+-+BreakDown_custom.md"
    out_file.write_text(content, encoding="utf-8")
    print(f"  OK Federated+Graphql+Stories+-+BreakDown_custom.md ({len(content):,} chars · "
          f"{', '.join(CUSTOM_DOMAINS)})")


def main() -> None:
    args        = sys.argv[1:]
    global_only = "--global" in args
    custom_only = "--custom" in args
    targets     = [a for a in args if not a.startswith("--")]

    if custom_only:
        generate_global_custom()
        return
    if global_only:
        generate_global()
        return

    domains = targets if targets else ALL_DOMAINS
    today   = date.today().isoformat()
    print(f"\n=== Breakdown generation — {today} ===\n")

    for domain in domains:
        if domain not in ALL_DOMAINS:
            print(f"  UNKNOWN '{domain}' — skipping")
            continue
        try:
            generate_breakdown_for(domain)
        except Exception as e:
            print(f"  FAIL {domain}: {type(e).__name__}: {e}")

    if not targets:
        try:
            generate_global()
        except Exception as e:
            print(f"  FAIL global: {type(e).__name__}: {e}")
        try:
            generate_global_custom()
        except Exception as e:
            print(f"  FAIL global_custom: {type(e).__name__}: {e}")

    print("\nDone.\n")


if __name__ == "__main__":
    main()
