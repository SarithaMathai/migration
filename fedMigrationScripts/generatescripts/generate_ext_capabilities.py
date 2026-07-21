#!/usr/bin/env python3
"""
Phase 6b: External Capability Consolidation — one EXT story per reusable external
lookup/entity, not one per (domain, field).

Problem this replaces: `generate_client_story_dependency.py`'s `ExtAuthoring` class
(see `output/analysis/program/ext-dependency-stories.md`) authors a new BE-H/BE-G
story per (domain, field, external type) triple — so `businessPartners` resolved via
VMM in `product`, `bom`, `claims`, `watchlist`, ... would (if every domain's gap were
genuinely uncovered) mint FOUR separate stories for what is really ONE external
capability: "VMM exposes a business-partner lookup." That script's scope is narrower
in practice (it only authors a story for a gap with NO existing covering story), but
the same wrong-granularity risk applies wherever it fires, and it does nothing for the
much larger set of external dependencies that already have a per-domain covering story
in be-04-stories.md (e.g. PRODUCT-BE-G-07, BOM-BE-G-01, CLAIM-BE-G-0x all separately
implement their own VMM client call) — those never get consolidated at all today.

This script analyzes the SAME source facts `generate_schema_analysis.py` (be-06) already
computed per domain — resolver -> loader key -> owner label, via the single catalog
`fedMigrationScripts/reference/domain-service-catalog.md` (`LOADER_CATALOG`) — and groups
by OWNER LABEL (the actual reusable capability boundary the catalog already encodes,
e.g. `vmm`/`location`/`brand` all collapse to "VMM platform"; `clazz`/`department`/
`division`/`ig` all collapse to "Item Groups (IG)"), not by loader key and not by domain.

Inputs (all relative to the migration repo root; nothing here is re-derived by hand):
  fedMigrationScripts/reference/domain-service-catalog.md   loader key -> owner label
      (via generate_schema_analysis.LOADER_CATALOG / classify_loader — imported, not
      reimplemented)
  code/resolvers/**/*.txt                     per-domain resolver maps (via
      generate_schema_analysis.analyze_domain_resolvers)
  ClientCallingGqlQueries/*.txt                real FE usage (via
      generate_schema_analysis.build_client_usage_index)
  output/analysis/{domain}/be-04-stories.md    existing per-domain story ids + titles,
      to link each capability's per-domain "verification" story to a REAL id when one
      already exists, instead of inventing a placeholder

Output:
  output/analysis/program/ext-capability-stories.md   one EXT-<TOKEN>-NN story per
      owner-capability that is genuinely a separate-DGS or external-platform dependency
      (never a phase1-domain co-located one — those stay `@requires`, be-06's own
      recommendation), each listing every (domain, resolver field) consumer and,
      where resolvable, the existing per-domain BE-*-G story that already does the
      federation wiring for that capability in that domain.

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_ext_capabilities.py

⚠ Regeneration overwrites the whole output file — this folder has no hand-authored
  content; re-run after any domain-service-catalog.md / be-04-stories.md change.
"""

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ANALYSIS = ROOT / "output" / "analysis"
PROGRAM = ANALYSIS / "program"
OUT = PROGRAM / "ext-capability-stories.md"

sys.path.insert(0, str(HERE))
import generate_schema_analysis as sa  # reuse loader catalog + resolver analysis, no reimplementation

TODAY = date.today().isoformat()

DOMAIN_FE_TOKEN = {
    "product": "PRODUCT", "bom": "BOM", "claims": "CLAIM",
    "measurement": "MST", "impression": "IMPRESSION",
    "productDetails": "PDTL", "packaging": "PKG", "watchlist": "WATCHLIST",
}

# be-04-stories.md story headers, to find an EXISTING per-domain story that already
# names this capability's EXT service tag — reused so the per-domain "verification"
# row links to a real id instead of a placeholder wherever one already exists.
STORY_HEADER_RE = re.compile(r"^### ([A-Z][A-Za-z0-9]*-BE-[A-Za-z0-9-]+) · (.+?)\n"
                              r"- \*\*Type:\*\*[^\n]*", re.M)
EXT_TAG_RE = re.compile(r"\*\*EXT:\*\*\s*(.+)$", re.M)


def load_domain_ext_stories(domain):
    """-> {loader_key: [(story_id, title), ...]} — every be-04 story that tags this
    loader key in its own **EXT:** line, so a capability's per-domain consumer row can
    link to the REAL story already doing that domain's federation wiring."""
    p = ANALYSIS / domain / "be-04-stories.md"
    out = defaultdict(list)
    if not p.exists():
        return out
    text = p.read_text(encoding="utf-8", errors="replace")
    matches = list(re.finditer(r"^### ([A-Z][A-Za-z0-9]*-BE-[A-Za-z0-9-]+) · (.+)$", text, re.M))
    for i, m in enumerate(matches):
        sid, title = m.group(1), m.group(2).strip()
        body = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        head = body.split("\n\n", 1)[0]
        ext_m = EXT_TAG_RE.search(m.group(0) + head)
        if not ext_m:
            continue
        for km in re.finditer(r"`([A-Za-z][A-Za-z0-9_]*)`", ext_m.group(1)):
            out[km.group(1)].append((sid, title))
    return out


def owner_key(label):
    """Normalize an owner label to a stable capability slug, e.g. 'VMM platform' ->
    'VMM', 'Item Groups (IG)' -> 'IG', 'UserProfileService' -> 'USERPROFILE',
    'separate DGS (plm-attachment)' -> 'ATTACHMENT' (the plm-<x> name, not the
    generic 'separate DGS' prefix every sibling-subgraph label shares — matching on
    that prefix alone collided plm-attachment and plm-discussion onto one id)."""
    plm = re.search(r"\(plm-([A-Za-z0-9]+)\)", label)
    if plm:
        return plm.group(1).upper()
    paren = re.search(r"\(([A-Za-z0-9]+)\)", label)
    if paren and len(paren.group(1)) <= 6:
        return paren.group(1).upper()
    m = re.match(r"^\(?([A-Za-z]+)", label)
    base = m.group(1).upper() if m else re.sub(r"[^A-Za-z0-9]", "", label).upper()
    base = re.sub(r"(SERVICE|PLATFORM)$", "", base)
    return base or "EXT"


def collect_capabilities():
    """-> {owner_label: {"kind": kind, "loader_keys": set, "consumers": [
        {"domain","field","block","loader_key","complexity","used_by":[...]}]}}
    Only sibling-dgs / platform kinds — phase1-domain co-located deps are excluded
    (be-06 already recommends plain `@requires`, no separate capability story needed)."""
    client_idx = sa.build_client_usage_index()
    capabilities = defaultdict(lambda: {"kind": None, "loader_keys": set(), "consumers": []})

    for domain in sa.ALL_DOMAINS:
        entries = sa.analyze_domain_resolvers(domain)
        for e in entries:
            if not e["loader_keys"]:
                continue
            for lk in sorted(e["loader_keys"]):
                kind, label = sa.classify_loader(lk)
                if kind not in ("sibling-dgs", "platform"):
                    continue  # phase1-domain (@requires, same subgraph) or acl/unknown — not this script's concern
                cap = capabilities[label]
                cap["kind"] = kind
                cap["loader_keys"].add(lk)
                usage = client_idx.get(domain, {}).get(e["field"], [])
                cap["consumers"].append({
                    "domain": domain, "field": e["field"], "block": e["block"],
                    "loader_key": lk, "complexity": sa.complexity_for(e),
                    "used_by": [op for op, _src in usage],
                })
    return capabilities


def render(capabilities):
    header = [
        "# External Capability Stories — Consolidated by Reusable Dependency",
        "",
        f"> **Generated:** {TODAY} · by `generate_ext_capabilities.py`. Auto-generated — regenerate "
        "after any `domain-service-catalog.md` or `be-04-stories.md` change; never hand-edit.",
        "",
        "> **Why this file exists:** `output/clientStoryDependency/` and "
        "`output/analysis/program/ext-dependency-stories.md` correctly identify WHICH fields "
        "depend on an external service, but authored a story per (domain, field) — so the SAME "
        "external capability (e.g. VMM's business-partner lookup) could get re-authored once per "
        "consuming domain. This file re-groups every cross-domain/EXT resolver "
        "(`be-06-cross-domain-field-analysis.md`, all 8 domains) by its **owning service/platform** "
        "— the real reusable-capability boundary already encoded in "
        "`domain-service-catalog.md`'s owner-label column — so there is exactly ONE EXT story per "
        "capability, and every consuming domain gets its own lightweight verification story instead "
        "of a duplicate implementation story.",
        "",
        "**Dependency chain this produces:** `EXT capability (owning service exposes the lookup) → "
        "domain implementation (existing be-04 G/H story does the DGS-side fetch) → federation "
        "verification (confirm entity stitching / gateway stub resolves end-to-end) → client story`.",
        "",
        "- **Sibling DGS** capabilities need a real `@DgsEntityFetcher` (or equivalent client-backed "
        "resolver) built ONCE by the owning domain/subgraph; every consumer then just references the "
        "entity via `@key` — no per-consumer reimplementation.",
        "- **External platform** capabilities (VMM/IG/Doppler/Corona/...) are gateway-stub "
        "(`@extends`) dependencies — no DGS build on our side at all; every consumer's job is only to "
        "declare the stub and verify the gateway resolves it.",
        "",
        "---",
        "",
    ]

    L = []
    next_num = 1
    rows_summary = []
    sorted_caps = sorted(capabilities.items(),
                          key=lambda kv: (-len({c["domain"] for c in kv[1]["consumers"]}), kv[0]))

    for label, cap in sorted_caps:
        domains = sorted({c["domain"] for c in cap["consumers"]})
        if len(domains) < 1:
            continue
        ext_id = f"EXT-{owner_key(label)}-{next_num:02d}"
        next_num += 1
        kind_label = "Sibling DGS subgraph" if cap["kind"] == "sibling-dgs" else "External platform (gateway stitch)"
        loader_keys = ", ".join(f"`{k}`" for k in sorted(cap["loader_keys"]))
        used_consumers = [c for c in cap["consumers"] if c["used_by"]]
        unused_consumers = [c for c in cap["consumers"] if not c["used_by"]]

        L += [
            f"### {ext_id} · {label} — external lookup/entity resolver",
            f"- **Kind:** {kind_label} · **Loader key(s):** {loader_keys} · "
            f"**Consuming domains:** {len(domains)} ({', '.join(domains)}) · "
            f"**Consuming resolvers:** {len(cap['consumers'])} "
            f"({len(used_consumers)} with confirmed client usage)",
            "",
        ]
        if cap["kind"] == "sibling-dgs":
            L.append(f"- **Owning-side work (build once):** {label} exposes a federation entity "
                      f"(`@key`) with a `@DgsEntityFetcher` (batched via `DataLoader`, null-tolerant "
                      f"per federation spec) — OR, if {label} isn't itself migrating to DGS in this "
                      f"phase, a thin shared client/module every consumer imports rather than each "
                      f"reimplementing its own call. This is the SINGLE piece of work that unblocks "
                      f"every consumer below.")
        else:
            L.append(f"- **Owning-side work:** none on our side — {label} is an external platform; "
                      f"the gateway resolves an `@extends @external` stub directly. Each consumer only "
                      f"needs to declare the stub correctly and verify the gateway stitch end-to-end.")
        L.append("")

        L += [
            "#### Consumers (per domain — verification story, not a duplicate implementation)",
            "",
            "| Domain | Resolver field(s) | Client usage | Existing covering BE story | Verification story |",
            "|---|---|---|---|---|",
        ]
        by_domain = defaultdict(list)
        for c in cap["consumers"]:
            by_domain[c["domain"]].append(c)
        domain_ext_cache = {}
        for domain in domains:
            consumers = by_domain[domain]
            fields = ", ".join(f"`{c['block']}.{c['field']}`" for c in
                                sorted(consumers, key=lambda x: x["field"]))
            any_used = any(c["used_by"] for c in consumers)
            used_str = "✅ yes" if any_used else "⏭ not found in ClientCallingGqlQueries"
            if domain not in domain_ext_cache:
                domain_ext_cache[domain] = load_domain_ext_stories(domain)
            existing = []
            for c in consumers:
                existing.extend(domain_ext_cache[domain].get(c["loader_key"], []))
            existing = sorted(set(existing))
            existing_str = ", ".join(f"`{sid}`" for sid, _t in existing) if existing else "— (none found; needs authoring)"
            token = DOMAIN_FE_TOKEN.get(domain, domain.upper())
            verify_id = existing[0][0] if existing else f"{token}-BE-G-VERIFY-{owner_key(label)}"
            L.append(f"| {domain} | {fields} | {used_str} | {existing_str} | `{verify_id}` — "
                     f"verify {label} entity stitching in the {domain} subgraph |")
        L.append("")

        if unused_consumers:
            unused_fields = ", ".join(f"`{c['domain']}.{c['field']}`" for c in unused_consumers)
            L.append(f"> ⏭ No confirmed client usage for: {unused_fields} — candidates to defer rather "
                      f"than build/verify federation for, pending confirmation against "
                      f"`ClientCallingGqlQueries/`.")
            L.append("")

        L += [
            "#### Acceptance Criteria",
            "",
            "1. The owning-side entity fetcher / gateway stub resolves the capability end-to-end for "
            "every consuming domain listed above, not just one.",
            "2. Every consuming domain's own verification story confirms ITS query returns the "
            "hydrated entity correctly — it does not reimplement the lookup.",
            "3. Unknown/missing upstream ids yield `null` without failing the whole response "
            "(federation spec null-tolerance).",
            "",
            "---",
            "",
        ]
        rows_summary.append((ext_id, label, kind_label, len(domains), len(cap["consumers"])))

    summary = [
        "## Summary",
        "",
        f"| Capability | Kind | Domains | Consuming resolvers |",
        "|---|---|---|---|",
    ]
    for ext_id, label, kind_label, ndom, ncons in rows_summary:
        summary.append(f"| `{ext_id}` {label} | {kind_label} | {ndom} | {ncons} |")
    summary.append("")
    summary.append("---")
    summary.append("")

    return "\n".join(header + summary + L)


def main():
    capabilities = collect_capabilities()
    content = render(capabilities)
    PROGRAM.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    n_caps = len({label for label, cap in capabilities.items() if cap["consumers"]})
    print(f"  OK {OUT.relative_to(ROOT)} ({n_caps} capabilities, {len(content):,} chars)")


if __name__ == "__main__":
    main()
