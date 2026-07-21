#!/usr/bin/env python3
"""
Phase 6: Cross-Domain Field Analysis — schema + resolver dependency mapping.

For every query, mutation, and field resolver in a domain's resolver map, find which
OTHER phase-1 domains (or sibling/platform services) it must hydrate from, cross-check
whether the field is actually consumed by a real frontend client operation, rate
complexity, and recommend a federation resolution.

Inputs (all relative to the migration repo root):
  code/resolvers/**/*.txt              Legacy resolver maps (Query/Mutation/Type blocks,
                                        `ctx.loaders.<key>.<method>` calls)
  fedMigrationScripts/reference/domain-service-catalog.md   Loader key -> owning domain/
                                        platform/subgraph catalog (parsed for the mapping;
                                        keep this file authoritative, do not hardcode drift)
  ClientCallingGqlQueries/*.txt + QUERY_INVENTORY.md   Client usage (via generate_frontend's
                                        parser — imported, not reimplemented)
  output/analysis/{domain}/be-01-schema-inventory.md   Resolver file manifest per domain

Outputs:
  output/analysis/{domain}/be-06-cross-domain-field-analysis.md   Per-domain field table
  output/analysis/schemaAnalysis/00-cross-domain-field-inventory.md   Program roll-up

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_schema_analysis.py            # all domains
    python fedMigrationScripts/generatescripts/generate_schema_analysis.py bom        # one domain

⚠ Regeneration overwrites both outputs above — this is a generated artifact, never hand-edit.
"""

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CODE_RESOLVERS = ROOT / "code" / "resolvers"
BE_ANALYSIS = ROOT / "output" / "analysis"
OUT_ROLLUP = BE_ANALYSIS / "schemaAnalysis"
CATALOG_MD = HERE.parent / "reference" / "domain-service-catalog.md"

TODAY = date.today().isoformat()

sys.path.insert(0, str(HERE))
import generate_frontend as fe  # reuse client-query parsing (no reimplementation)

ALL_DOMAINS = ["product", "bom", "measurement", "productDetails",
               "packaging", "watchlist", "impression", "claims"]

DOMAIN_LABELS = fe.DOMAIN_LABELS
DOMAIN_RESOLVER_FILE = {
    "product":        CODE_RESOLVERS / "SPARK_Product.txt",
    "bom":            CODE_RESOLVERS / "product" / "SPARK_Bom.txt",
    # measurement + its co-located sub-domains (folded in 2026-07-19 — same
    # enterprise_product_development_products service base, own operations, not EXT;
    # see output/analysis/measurement/be-01-schema-inventory.md §2 scope correction).
    # A list here (rather than one path) is scanned as ONE domain by analyze_domain_resolvers.
    "measurement":    [CODE_RESOLVERS / "product" / "SPARK_Measurement.txt",
                        CODE_RESOLVERS / "SPARK_MeasurementTemplate.txt",
                        CODE_RESOLVERS / "product" / "SPARK_SizeTemplate.txt",
                        CODE_RESOLVERS / "product" / "SPARK_TightFit.txt",
                        CODE_RESOLVERS / "product" / "SPARK_Sizes.txt"],
    "productDetails": CODE_RESOLVERS / "product" / "SPARK_ProductDetail.txt",
    "packaging":      CODE_RESOLVERS / "product" / "SPARK_Packaging.txt",
    "watchlist":      CODE_RESOLVERS / "product" / "SPARK_Watchlist.txt",
    "impression":     CODE_RESOLVERS / "product" / "SPARK_Impression.txt",
    "claims":         CODE_RESOLVERS / "product" / "SPARK_Claims.txt",
}
# The literal `ctx.loaders.<key>` string each domain's OWN resolver file uses to call
# itself — verified against code/resolvers/**/*.txt (case-sensitive; productDetails and
# claims use different casing/singular form than their domain key). measurement's
# sub-domain files call themselves via their OWN loader key (measurementTemplate/
# sizeTemplate/tightFit), not "measurement" — all excluded here so a sub-domain's own
# reference to ITSELF isn't miscounted as a cross-domain dependency of `measurement`.
DOMAIN_LOADER_KEY = {
    "product": "product", "bom": "bom",
    "measurement": {"measurement", "measurementTemplate", "sizeTemplate", "tightFit"},
    "productDetails": "ProductDetails", "packaging": "packaging",
    "watchlist": "watchlist", "impression": "impression", "claims": "claim",
}


# ─── Loader-key catalog (parsed from domain-service-catalog.md, single source of truth) ──
def load_loader_catalog():
    """-> {loader_key: (owner_label, migrate_target, default_severity)}
    Parses BOTH tables in the catalog: the 4-column "EXT loader keys" table (loader key |
    owner | migrate? | severity) and the 6-column "Adding a new domain" table (loader key |
    schema | resolver | service | subgraph | status) — the latter is where sibling-DGS
    domains like attachment/workspace/sample/discussion/search are documented.
    """
    text = CATALOG_MD.read_text(encoding="utf-8", errors="replace")
    catalog = {}

    row4_re = re.compile(r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$', re.M)
    for m in row4_re.finditer(text):
        keys, owner, migrate, severity = m.groups()
        if keys.lower() in ("loader key",) or set(keys) <= {"-", " "}:
            continue
        for key in re.split(r'\s*/\s*', keys):
            key = key.strip().strip("`").strip()
            if key:
                catalog[key] = (owner.strip(), migrate.strip(), severity.strip())

    row6_re = re.compile(
        r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$',
        re.M,
    )
    for m in row6_re.finditer(text):
        key, _schema, _resolver, _service, subgraph, status = m.groups()
        key = key.strip().strip("`").strip()
        if not key or key.lower() == "loader key" or set(key) <= {"-", " "}:
            continue
        subgraph = subgraph.strip()
        if "separate DGS" in subgraph or "separate" in subgraph.lower():
            # Don't clobber an existing phase-1/platform entry from the first table.
            catalog.setdefault(key, (subgraph.strip("*"), "Yes (sibling — separate DGS)", "🟡"))
    return catalog


LOADER_CATALOG = load_loader_catalog()
# Invert DOMAIN_LOADER_KEY -> {own_loader_key: phase1_domain}. A domain's value may be a
# single key (most domains) or a set of keys (measurement, which folds in 3 co-located
# sub-domains each calling themselves via their OWN loader key — see DOMAIN_LOADER_KEY).
LOADER_TO_PHASE1_DOMAIN = {}
for _dom, _keys in DOMAIN_LOADER_KEY.items():
    for _k in (_keys if isinstance(_keys, set) else {_keys}):
        LOADER_TO_PHASE1_DOMAIN[_k] = _dom


def classify_loader(key):
    """-> (kind, label) kind in {'phase1-domain','sibling-dgs','platform','acl','unknown'}"""
    if key in LOADER_TO_PHASE1_DOMAIN:
        return "phase1-domain", DOMAIN_LABELS[LOADER_TO_PHASE1_DOMAIN[key]]
    if key == "accessControl":
        # ACL is analyzed separately (be-07-acl-usage-analysis.md) — not a
        # cross-domain hydration in the schema-analysis sense.
        owner, _migrate, _severity = LOADER_CATALOG.get(key, ("AccessControlService", "", ""))
        return "acl", owner
    owner, migrate, severity = LOADER_CATALOG.get(key, (key, "", ""))
    if "Gateway stitch" in migrate:
        return "platform", owner
    if "sibling" in migrate or "separate DGS" in owner or "separate" in migrate:
        return "sibling-dgs", owner
    return "unknown", owner or key


# ─── Resolver-map parser (JS resolver files: Query/Mutation/Type blocks) ─────────────────
TOPLEVEL_KEY_RE = re.compile(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(\{|\(|async\s*\(|\w)', re.M)
LOADER_CALL_RE = re.compile(r'ctx\.loaders\.([A-Za-z0-9_]+)')
JWT_RE = re.compile(r'getUserPermissionsJWT')


def find_matching_brace(text, open_idx):
    depth = 0
    i = open_idx
    while i < len(text):
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(text) - 1


def parse_resolver_map(text):
    """Best-effort structural parse of `export default { Query: {...}, Mutation: {...}, Type: {...} }`.
    Returns {block_name: {field_name: field_body_text}}.
    """
    m = re.search(r'export\s+default\s*\{', text)
    if not m:
        return {}
    root_open = text.index("{", m.start())
    root_close = find_matching_brace(text, root_open)
    root_body = text[root_open + 1:root_close]

    blocks = {}
    for bm in re.finditer(r'([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\{', root_body):
        name = bm.group(1)
        b_open = root_body.index("{", bm.start())
        b_close = find_matching_brace(root_body, b_open)
        block_body = root_body[b_open + 1:b_close]
        fields = {}
        for fm in re.finditer(r'([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?:async\s*)?\(', block_body):
            fname = fm.group(1)
            start = fm.start()
            # Walk the arg-list '(...)' first, then continue past '=>' into the
            # function body — either a '{ ... }' block or a bare expression that
            # ends at the next top-level ',' (sibling field) or the enclosing '}'.
            depth = 0
            j = fm.end() - 1  # at '('
            arglist_end = len(block_body)
            while j < len(block_body):
                c = block_body[j]
                if c in "({[":
                    depth += 1
                elif c in ")}]":
                    depth -= 1
                    if depth == 0:
                        arglist_end = j + 1
                        break
                j += 1
            k = arglist_end
            while k < len(block_body) and block_body[k] in " \t\r\n":
                k += 1
            if block_body[k:k + 2] == "=>":
                k += 2
                while k < len(block_body) and block_body[k] in " \t\r\n":
                    k += 1
            if k < len(block_body) and block_body[k] == "{":
                end = find_matching_brace(block_body, k) + 1
            else:
                # bare expression body: scan to the next top-level ',' or the
                # enclosing block's end, respecting nested brackets.
                depth = 0
                end = len(block_body)
                m = k
                while m < len(block_body):
                    c = block_body[m]
                    if c in "({[":
                        depth += 1
                    elif c in ")}]":
                        if depth == 0:
                            end = m
                            break
                        depth -= 1
                    elif c == "," and depth == 0:
                        end = m
                        break
                    m += 1
            fields[fname] = block_body[start:end]
        blocks[name] = fields
    return blocks


def analyze_domain_resolvers(domain):
    """-> list of {block, field, loader_keys:set, has_jwt:bool} for every resolver field.
    `DOMAIN_RESOLVER_FILE[domain]` may be one path or a list of paths (a domain that folds
    in co-located sub-domains, e.g. measurement + measurementTemplate/sizeTemplate/tightFit/
    sizes, each its own resolver file but analyzed together as one domain)."""
    paths = DOMAIN_RESOLVER_FILE.get(domain)
    if not paths:
        return []
    paths = paths if isinstance(paths, list) else [paths]
    own_keys = DOMAIN_LOADER_KEY.get(domain)
    own_keys = own_keys if isinstance(own_keys, set) else {own_keys}
    out = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        blocks = parse_resolver_map(text)
        for block, fields in blocks.items():
            for fname, body in fields.items():
                # accessControl is cross-cutting auth, not a domain hydration — tracked
                # separately in be-07-acl-usage-analysis.md (generate_acl_analysis.py).
                keys = {k for k in LOADER_CALL_RE.findall(body) if k not in own_keys and k != "accessControl"}
                out.append({
                    "block": block, "field": fname,
                    "loader_keys": keys, "has_jwt": bool(JWT_RE.search(body)),
                    "line": text[:text.index(body)].count("\n") + 1 if body in text else None,
                })
    return out


# ─── Complexity + recommendation ─────────────────────────────────────────────────────────
def complexity_for(entry):
    n_ext = len(entry["loader_keys"])
    bump = 0
    if entry["block"] not in ("Query", "Mutation") and entry["block"].endswith("Interface"):
        bump += 1
    if n_ext >= 3:
        return "Very High" if n_ext >= 5 else "High"
    if n_ext == 2:
        return "Medium" if not bump else "High"
    if n_ext == 1:
        return "Low" if not bump else "Medium"
    return "Low"


def recommend_for(entry, kinds):
    """kinds: set of classify_loader() kind values for this entry's loader_keys."""
    if not entry["loader_keys"]:
        return "No cross-domain dependency — resolves locally, no federation work needed"
    if "phase1-domain" in kinds and len(kinds) == 1 and len(entry["loader_keys"]) == 1:
        return "@requires field composition — single co-located phase-1 domain, same plm-product subgraph"
    if "phase1-domain" in kinds:
        return "Co-locate + @requires — multiple phase-1 domains, same plm-product subgraph, order dependency"
    if "sibling-dgs" in kinds:
        return "Entity resolver (@key + @DgsEntityFetcher) — separate DGS subgraph, gateway federation required"
    if "platform" in kinds:
        return "Gateway stitch (@extends stub) — external platform, no DGS migration, gateway resolves"
    return "Needs manual review — unclassified loader key"


# ─── Client usage index (reuse generate_frontend's parser) ───────────────────────────────
def build_client_usage_index():
    """-> {domain: {field_name: [(op_name, src_file), ...]}}"""
    registry = fe.build_schema_registry()
    client_defs = fe.load_client_defs()
    usage_idx = fe.load_usage_index()
    be_stories = fe.load_be_stories()
    ops, frag_records, coverage, fragments = fe.cross_reference(registry=registry,
        client_defs=client_defs, usage_idx=usage_idx, be_stories=be_stories)
    idx = defaultdict(lambda: defaultdict(list))
    for o in ops:
        for r in o["roots"]:
            if r["domain"]:
                idx[r["domain"]][r["field"]].append((o["op_name"] or o["const"], o["src"]))
    return idx


# ─── Markdown emission ────────────────────────────────────────────────────────────────────
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def md_escape(s):
    return (s or "").replace("|", "\\|")


def generate_domain(domain, client_idx=None):
    if client_idx is None:
        client_idx = build_client_usage_index()
    entries = analyze_domain_resolvers(domain)
    label = DOMAIN_LABELS.get(domain, domain)
    rows = []
    n_cross = 0
    complexity_counts = defaultdict(int)
    for e in sorted(entries, key=lambda x: (x["block"], x["field"])):
        if not e["loader_keys"]:
            continue
        n_cross += 1
        kinds = set()
        dep_labels = []
        for k in sorted(e["loader_keys"]):
            kind, lbl = classify_loader(k)
            kinds.add(kind)
            dep_labels.append(f"`{k}` ({lbl})")
        complexity = complexity_for(e)
        complexity_counts[complexity] += 1
        usage = client_idx.get(domain, {}).get(e["field"], [])
        if usage:
            used_str = "; ".join(f"`{op}`" for op, _src in usage[:3])
            if len(usage) > 3:
                used_str += f" (+{len(usage) - 3} more)"
        else:
            used_str = "⏭ not found in ClientCallingGqlQueries"
        recommendation = recommend_for(e, kinds)
        rows.append(
            f"| `{e['block']}.{e['field']}` | {', '.join(dep_labels)} | {used_str} | "
            f"{complexity} | {md_escape(recommendation)} |"
        )

    total = len(entries)
    L = []
    L.append(f"# Phase 6: Cross-Domain Field Analysis — {label}")
    L.append("")
    L.append(f"> **Domain:** `{domain}`")
    L.append(f"> **Target DGS:** `{fe.DOMAIN_DGS.get(domain, '—')}`")
    L.append("> **Pipeline Version:** 1.0")
    L.append(f"> **Generated:** {TODAY}")
    L.append("> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · "
              "[be-03-schema.graphql](./be-03-schema.graphql)")
    L.append("> **DGS Target Status:** Green-field")
    L.append("")
    L.append("For every query/mutation/field resolver that hydrates from another domain or service, this "
              "identifies the dependency, whether the field is used by a real frontend client operation "
              "(cross-checked against `ClientCallingGqlQueries/`), complexity, and a federation recommendation.")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Metric | Count |")
    L.append("|---|---|")
    L.append(f"| Total resolvers scanned | {total} |")
    L.append(f"| Resolvers with cross-domain/EXT dependency | {n_cross} |")
    for tier in ("Very High", "High", "Medium", "Low"):
        if complexity_counts[tier]:
            L.append(f"| {tier} complexity | {complexity_counts[tier]} |")
    unused = sum(1 for r in rows if "⏭ not found" in r)
    L.append(f"| Cross-domain fields with no client usage found | {unused} |")
    L.append("")
    L.append("## Cross-Domain Field Dependencies")
    L.append("")
    L.append("| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |")
    L.append("|---|---|---|---|---|")
    L.extend(rows if rows else ["| _(none found)_ | | | | |"])
    L.append("")
    L.append("## Recommendation Legend")
    L.append("")
    L.append("- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); "
              "compose via Federation `@requires`, no gateway hop.")
    L.append("- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, "
              "sequence the `@requires` chain, document ordering.")
    L.append("- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS "
              "subgraph; needs a federation entity fetcher on the owning side.")
    L.append("- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS "
              "migration, the gateway resolves the stub directly.")
    L.append("- **No cross-domain dependency** — resolves locally; no federation work needed.")
    L.append("")
    L.append("---")
    L.append(f"**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `{domain}` · "
              f"**Cross-domain fields:** {n_cross}/{total}")
    L.append("")

    out = BE_ANALYSIS / domain / "be-06-cross-domain-field-analysis.md"
    write(out, "\n".join(L))
    return {"domain": domain, "total": total, "n_cross": n_cross,
            "complexity_counts": dict(complexity_counts), "rows": rows, "unused": unused}


def generate_rollup(domain_results):
    L = []
    L.append("# Schema Analysis — Cross-Domain Field Inventory (Program Roll-Up)")
    L.append("")
    L.append(f"> **Scope:** {len(domain_results)} phase-1 domains · **Generated:** {TODAY} · "
             "**Pipeline Version:** 1.0")
    L.append("> Aggregates each domain's `be-06-cross-domain-field-analysis.md`. Regenerate via "
             "`python fedMigrationScripts/generatescripts/generate_schema_analysis.py`.")
    L.append("")
    total = sum(r["total"] for r in domain_results)
    n_cross = sum(r["n_cross"] for r in domain_results)
    unused = sum(r["unused"] for r in domain_results)
    L.append("## Program Totals")
    L.append("")
    L.append("| Metric | Value |")
    L.append("|---|---|")
    L.append(f"| Total resolvers scanned | {total} |")
    L.append(f"| Cross-domain/EXT dependent resolvers | {n_cross} |")
    L.append(f"| Cross-domain fields with no client usage found | {unused} |")
    L.append("")
    L.append("## By Domain")
    L.append("")
    L.append("| Domain | Resolvers | Cross-domain | 🔴 Very High | 🟠 High | 🟡 Medium | 🟢 Low | Unused (no client match) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in domain_results:
        cc = r["complexity_counts"]
        L.append(f"| [{DOMAIN_LABELS.get(r['domain'], r['domain'])}](../{r['domain']}/be-06-cross-domain-field-analysis.md) "
                 f"| {r['total']} | {r['n_cross']} | {cc.get('Very High', 0)} | {cc.get('High', 0)} | "
                 f"{cc.get('Medium', 0)} | {cc.get('Low', 0)} | {r['unused']} |")
    L.append(f"| **TOTAL** | **{total}** | **{n_cross}** | "
             f"**{sum(r['complexity_counts'].get('Very High', 0) for r in domain_results)}** | "
             f"**{sum(r['complexity_counts'].get('High', 0) for r in domain_results)}** | "
             f"**{sum(r['complexity_counts'].get('Medium', 0) for r in domain_results)}** | "
             f"**{sum(r['complexity_counts'].get('Low', 0) for r in domain_results)}** | **{unused}** |")
    L.append("")
    L.append("## Unused Cross-Domain Fields (candidates for deferral)")
    L.append("")
    L.append("Fields that hydrate from another domain but were not matched to any operation in "
              "`ClientCallingGqlQueries/` — candidates to defer or drop rather than build federation for.")
    L.append("")
    any_unused = False
    for r in domain_results:
        unused_rows = [row for row in r["rows"] if "⏭ not found" in row]
        if not unused_rows:
            continue
        any_unused = True
        L.append(f"### {DOMAIN_LABELS.get(r['domain'], r['domain'])}")
        L.append("")
        L.append("| Resolver | Requires | Complexity |")
        L.append("|---|---|---|")
        for row in unused_rows:
            cells = [c.strip() for c in row.split("|")[1:-1]]
            L.append(f"| {cells[0]} | {cells[1]} | {cells[3]} |")
        L.append("")
    if not any_unused:
        L.append("_None — every cross-domain field matched a client operation._")
        L.append("")
    L.append("---")
    L.append(f"*Program roll-up · generated {TODAY} from each domain's `be-06-cross-domain-field-analysis.md`.*")
    write(OUT_ROLLUP / "00-cross-domain-field-inventory.md", "\n".join(L))


def main():
    args = sys.argv[1:]
    targets = [a for a in args if not a.startswith("--")] or ALL_DOMAINS
    print(f"\n=== Cross-domain field analysis — {TODAY} ===\n")
    client_idx = build_client_usage_index()
    results = []
    for domain in targets:
        if domain not in ALL_DOMAINS:
            print(f"  UNKNOWN domain '{domain}' — skipping")
            continue
        try:
            results.append(generate_domain(domain, client_idx))
        except Exception as e:
            print(f"  FAIL {domain}: {type(e).__name__}: {e}")
    if results and set(targets) >= set(ALL_DOMAINS):
        generate_rollup(results)
    elif results:
        # partial run: still refresh the roll-up using existing per-domain files where present
        all_results = []
        for domain in ALL_DOMAINS:
            match = next((r for r in results if r["domain"] == domain), None)
            all_results.append(match) if match else None
        if len(all_results) == len(ALL_DOMAINS):
            generate_rollup(all_results)
    print("\nDone.\n")


if __name__ == "__main__":
    main()
