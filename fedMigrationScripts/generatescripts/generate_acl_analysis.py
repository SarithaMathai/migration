#!/usr/bin/env python3
"""
Phase 7: ACL Usage Analysis — capability-token classification + Mid-Request ACL Update fit.

For every resolver/field that touches ACL (`getUserPermissionsJWT`, `ctx.loaders.accessControl.*`,
`getAccessControlBatch`, `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission`),
classify the call site as either:
  - permission-check   — reads a permission/access value for the CURRENT resource, resolver-local
  - downstream-token    — mints a capability token from ids, then hands it to a DOWNSTREAM
                           cross-domain loader call (`ctx.loaders.<otherDomain>.<method>(token)`)

For downstream-token sites, evaluate whether Mid-Request ACL Update
(`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) resolves the need —
refreshing the current thread's security context instead of re-authenticating per call.

*** This supersedes the "ACL is context-only, ignored in DGS implementation" language baked
    into every domain's be-03-schema.graphql header and be-04-stories.md. Each finding below
    is flagged where it conflicts with that existing text. Per team decision (2026-07-17) this
    script does NOT edit those files — it only produces the research; the doc rewrite is a
    separate, later pass once these findings are reviewed. ***

Inputs (all relative to the migration repo root):
  code/resolvers/**/*.txt              Legacy resolver maps
  code/utils/accessControlUtils.txt    getToken / getAccessControlBatch
  code/utils/commonLoaders.txt         getUserPermissionsJWT and friends (referenced, not parsed —
                                        no per-domain resolver logic lives there)
  fedMigrationScripts/reference/domain-service-catalog.md   Loader key -> owning domain/platform

Outputs:
  output/analysis/{domain}/be-07-acl-usage-analysis.md   Per-domain ACL call-site table
  output/analysis/aclResearch/00-acl-usage-inventory.md  Program roll-up

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_acl_analysis.py            # all domains
    python fedMigrationScripts/generatescripts/generate_acl_analysis.py bom        # one domain

⚠ Regeneration overwrites both outputs above — this is a generated artifact, never hand-edit.
"""

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BE_ANALYSIS = ROOT / "output" / "analysis"
OUT_ROLLUP = BE_ANALYSIS / "aclResearch"

TODAY = date.today().isoformat()

sys.path.insert(0, str(HERE))
import generate_schema_analysis as sa  # reuse resolver-map parser + loader catalog

ALL_DOMAINS = sa.ALL_DOMAINS
DOMAIN_LABELS = sa.DOMAIN_LABELS
DOMAIN_RESOLVER_FILE = sa.DOMAIN_RESOLVER_FILE
DOMAIN_LOADER_KEY = sa.DOMAIN_LOADER_KEY

# Existing "ACL ignored" language this research supersedes (be-03 header / be-04 note) —
# used only to render the explicit conflict callout, never edited by this script.
SUPERSEDED_TEXT = (
    'capability-token (JWT) usage in source is context-only; ACL is IGNORED in the DGS '
    'implementation (no ACL plumbing story)'
)

JWT_ASSIGN_RE = re.compile(
    r'(?:const|let)\s+(\w+)\s*=\s*await\s+getUserPermissionsJWT\s*\(([^)]*)\)'
)

def _loader_with_token_re(token):
    """Match `ctx.loaders.<key>[.<method>](<...token...>)`, allowing the token to be
    any argument in the call (e.g. `getBomByIds(permissionJWT, ids)`), and the curried
    `.method(token).load(...)` shape (token as the sole arg to the outer call)."""
    tok = re.escape(token)
    return re.compile(
        r'ctx\.loaders\.([A-Za-z0-9_]+)\s*(?:\.\s*\w+)?\s*\('
        r'[^()]*\b' + tok + r'\b[^()]*'
        r'\)',
        re.S,
    )
DIRECT_ACCESSCONTROL_RE = re.compile(r'ctx\.loaders\.accessControl\.(\w+)')
ACL_BATCH_RE = re.compile(r'getAccessControlBatch|getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission')


def classify_acl_site(field_body, block, field, own_loader_key):
    """-> list of finding dicts for this field body (may be empty, one, or several)."""
    findings = []

    # 1) Direct accessControl loader reads (permission-check, resolver-local) —
    #    e.g. ctx.loaders.accessControl.getPermissions.load(...) / getUserAccessUnencoded
    for m in DIRECT_ACCESSCONTROL_RE.finditer(field_body):
        method = m.group(1)
        findings.append({
            "kind": "permission-check",
            "detail": f"`accessControl.{method}` — reads permission/access value for the current resource",
            "downstream_domain": None,
            "downstream_kind": None,
        })

    # 2) getUserPermissionsJWT(...) -> token minted, then check whether token feeds a
    #    downstream ctx.loaders.<key>(token) call (token-for-downstream-call), or is used
    #    only for the resolver's OWN loader (still effectively a permission-gate on read/write).
    for jm in JWT_ASSIGN_RE.finditer(field_body):
        token_var = jm.group(1)
        rest = field_body[jm.end():]
        use_re = _loader_with_token_re(token_var)
        use = use_re.search(rest)
        if use:
            target_key = use.group(1)
            own_keys = own_loader_key if isinstance(own_loader_key, set) else {own_loader_key}
            if target_key in own_keys:
                findings.append({
                    "kind": "own-domain-token",
                    "detail": f"`getUserPermissionsJWT` token passed to this domain's own "
                               f"`{target_key}` loader — capability token required for the "
                               f"resolver's own write/read, not a cross-domain call",
                    "downstream_domain": None,
                    "downstream_kind": None,
                })
            else:
                kind, label = sa.classify_loader(target_key)
                findings.append({
                    "kind": "downstream-token",
                    "detail": f"`getUserPermissionsJWT` token minted then passed into "
                               f"`ctx.loaders.{target_key}.*({token_var})` — capability token "
                               f"required to call **{label}** (`{target_key}`)",
                    "downstream_domain": target_key,
                    "downstream_kind": kind,
                })
        else:
            findings.append({
                "kind": "unresolved-token",
                "detail": "`getUserPermissionsJWT` token minted but no downstream "
                          "`ctx.loaders.<key>(token)` call found in the same field body — "
                          "may be passed further (helper fn) or unused; needs manual check",
                "downstream_domain": None,
                "downstream_kind": None,
            })

    # 3) Bulk/partner-ACL helpers (product's TechPack-style aggregation)
    if ACL_BATCH_RE.search(field_body):
        findings.append({
            "kind": "permission-check",
            "detail": "bulk/partner ACL-filtered resource tree — resolver-local read filter, "
                      "not a token for a downstream call",
            "downstream_domain": None,
            "downstream_kind": None,
        })

    return findings


def recommend_for_finding(f):
    if f["kind"] == "downstream-token":
        if f["downstream_kind"] in ("phase1-domain", "sibling-dgs"):
            return ("Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions"
                    "(capabilityToken) refreshes the thread's security context before the "
                    f"downstream call to `{f['downstream_domain']}`, avoiding re-authentication")
        if f["downstream_kind"] == "platform":
            return ("Gateway-level auth passthrough — downstream is an external platform stub; "
                    "the gateway carries the original auth header, no mid-request refresh needed")
        return (f"Needs manual review — `{f['downstream_domain']}` is not in the domain-service "
                "catalog; confirm whether it's a sibling DGS (Mid-Request ACL Update applies) "
                "or an external platform (gateway passthrough) before recommending")
    if f["kind"] == "own-domain-token":
        return "No action needed — token gates the resolver's own read/write, stays resolver-local"
    if f["kind"] == "permission-check":
        return "No action needed — permission check only, resolves locally, no token handoff"
    return "Needs manual review — token minted but downstream use not statically resolved"


def conflicts_with_superseded(f):
    return f["kind"] in ("downstream-token",)


def analyze_domain_acl(domain):
    """`DOMAIN_RESOLVER_FILE[domain]` may be one path or a list of paths (a domain that folds
    in co-located sub-domains, e.g. measurement — see generate_schema_analysis.py)."""
    paths = DOMAIN_RESOLVER_FILE.get(domain)
    if not paths:
        return []
    paths = paths if isinstance(paths, list) else [paths]
    own_key = DOMAIN_LOADER_KEY.get(domain)
    out = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        blocks = sa.parse_resolver_map(text)
        for block, fields in blocks.items():
            for fname, body in fields.items():
                for finding in classify_acl_site(body, block, fname, own_key):
                    out.append({"block": block, "field": fname, **finding})
    return out


def md_escape(s):
    return (s or "").replace("|", "\\|")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def generate_domain(domain):
    label = DOMAIN_LABELS.get(domain, domain)
    findings = analyze_domain_acl(domain)
    kind_counts = defaultdict(int)
    rows = []
    conflict_rows = []
    for f in sorted(findings, key=lambda x: (x["block"], x["field"])):
        kind_counts[f["kind"]] += 1
        recommendation = recommend_for_finding(f)
        resolver = f"`{f['block']}.{f['field']}`"
        rows.append(f"| {resolver} | {f['kind']} | {f['detail']} | {md_escape(recommendation)} |")
        if conflicts_with_superseded(f):
            conflict_rows.append(f"| {resolver} | {md_escape(recommendation)} |")

    L = []
    L.append(f"# Phase 7: ACL Usage Analysis — {label}")
    L.append("")
    L.append(f"> **Domain:** `{domain}`")
    L.append(f"> **Target DGS:** `{sa.fe.DOMAIN_DGS.get(domain, '—')}`")
    L.append("> **Pipeline Version:** 1.0")
    L.append(f"> **Generated:** {TODAY}")
    L.append("> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)")
    L.append("> **DGS Target Status:** Green-field")
    L.append("")
    L.append("> ⚠ **This supersedes the existing ACL note in `be-03-schema.graphql` / "
              "`be-04-stories.md`:** *“" + SUPERSEDED_TEXT + "”*. Rows below marked "
              "**downstream-token** are cases where ACL is NOT purely context — a capability "
              "token is required to call another domain's endpoint. This file does not edit "
              "be-03/be-04 — doc updates are a separate follow-up once these findings are reviewed.")
    L.append("")
    L.append("For every resolver/field that touches ACL, this classifies the call site "
              "(permission-check vs. token required for a downstream cross-domain call) and "
              "evaluates whether **Mid-Request ACL Update** "
              "(`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) resolves it.")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Metric | Count |")
    L.append("|---|---|")
    L.append(f"| Total ACL call sites | {len(findings)} |")
    L.append(f"| Permission-check (resolver-local) | {kind_counts['permission-check']} |")
    L.append(f"| Own-domain token (resolver-local write/read gate) | {kind_counts['own-domain-token']} |")
    L.append(f"| **Downstream-token (cross-domain, Mid-Request ACL Update candidate)** | "
             f"**{kind_counts['downstream-token']}** |")
    L.append(f"| Unresolved (needs manual check) | {kind_counts['unresolved-token']} |")
    L.append("")
    L.append("## ACL Call Sites")
    L.append("")
    L.append("| Resolver | Classification | Detail | Recommendation |")
    L.append("|---|---|---|---|")
    L.extend(rows if rows else ["| _(none found)_ | | | |"])
    L.append("")
    if conflict_rows:
        L.append("## Conflicts with the Existing \"ACL Ignored\" Decision")
        L.append("")
        L.append(f"{len(conflict_rows)} resolver(s) in this domain mint a capability token to call "
                 "another domain — these are NOT context-only, contradicting the current be-03/be-04 text.")
        L.append("")
        L.append("| Resolver | Recommendation |")
        L.append("|---|---|")
        L.extend(conflict_rows)
        L.append("")
    L.append("## Classification Legend")
    L.append("")
    L.append("- **permission-check** — reads a permission/access value for the current resource "
              "(`accessControl.getPermissions`/`getUserAccessUnencoded`, or bulk ACL-filtered tree "
              "reads); resolver-local, no token handoff.")
    L.append("- **own-domain-token** — `getUserPermissionsJWT` mints a token used only by this "
              "domain's own loader (e.g. `bom` resolver calling `ctx.loaders.bom(token)`); "
              "resolver-local, stays as-is.")
    L.append("- **downstream-token** — token minted then handed to a DIFFERENT domain's loader "
              "(`ctx.loaders.<otherDomain>(token)`) — the Mid-Request ACL Update candidate.")
    L.append("- **unresolved-token** — token minted but the downstream use isn't statically visible "
              "in the same field body (e.g. passed into a helper function) — needs a manual check.")
    L.append("")
    L.append("---")
    L.append(f"**Phase Completed:** Phase 7 — ACL Usage Analysis · **Domain:** `{domain}` · "
              f"**ACL call sites:** {len(findings)} · **Downstream-token:** {kind_counts['downstream-token']}")
    L.append("")

    out = BE_ANALYSIS / domain / "be-07-acl-usage-analysis.md"
    write(out, "\n".join(L))
    return {"domain": domain, "findings": findings, "kind_counts": dict(kind_counts), "rows": rows}


def generate_rollup(domain_results):
    L = []
    L.append("# ACL Research — Usage Inventory (Program Roll-Up)")
    L.append("")
    L.append(f"> **Scope:** {len(domain_results)} phase-1 domains · **Generated:** {TODAY} · "
             "**Pipeline Version:** 1.0")
    L.append("> Aggregates each domain's `be-07-acl-usage-analysis.md`. Regenerate via "
             "`python fedMigrationScripts/generatescripts/generate_acl_analysis.py`.")
    L.append("")
    L.append("## Key Finding")
    L.append("")
    L.append('Every domain\'s `be-03-schema.graphql` header and `be-04-stories.md` currently state: '
             f'*"{SUPERSEDED_TEXT}"*. This research finds that is only true for **permission-check** '
             "and **own-domain-token** call sites. **Downstream-token** call sites mint a capability "
             "token specifically to call another domain's API — ACL is load-bearing there, and "
             "**Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions"
             "(capabilityToken)`) is the recommended resolution: refresh the current thread's "
             "security context with the newly-fetched token instead of re-authenticating per "
             "downstream call.")
    L.append("")
    L.append("**This is a proposed supersession, not yet applied to be-03/be-04** — those docs are "
             "edited in a separate follow-up once these findings are reviewed.")
    L.append("")
    total = sum(len(r["findings"]) for r in domain_results)
    totals_by_kind = defaultdict(int)
    for r in domain_results:
        for k, v in r["kind_counts"].items():
            totals_by_kind[k] += v
    L.append("## Program Totals")
    L.append("")
    L.append("| Metric | Value |")
    L.append("|---|---|")
    L.append(f"| Total ACL call sites | {total} |")
    L.append(f"| Permission-check | {totals_by_kind['permission-check']} |")
    L.append(f"| Own-domain token | {totals_by_kind['own-domain-token']} |")
    L.append(f"| **Downstream-token (Mid-Request ACL Update candidates)** | "
             f"**{totals_by_kind['downstream-token']}** |")
    L.append(f"| Unresolved (manual check) | {totals_by_kind['unresolved-token']} |")
    L.append("")
    L.append("## By Domain")
    L.append("")
    L.append("| Domain | Total sites | Permission-check | Own-domain token | Downstream-token | Unresolved |")
    L.append("|---|---|---|---|---|---|")
    for r in domain_results:
        kc = r["kind_counts"]
        L.append(f"| [{DOMAIN_LABELS.get(r['domain'], r['domain'])}](../{r['domain']}/be-07-acl-usage-analysis.md) "
                 f"| {len(r['findings'])} | {kc.get('permission-check', 0)} | "
                 f"{kc.get('own-domain-token', 0)} | **{kc.get('downstream-token', 0)}** | "
                 f"{kc.get('unresolved-token', 0)} |")
    L.append(f"| **TOTAL** | **{total}** | **{totals_by_kind['permission-check']}** | "
             f"**{totals_by_kind['own-domain-token']}** | **{totals_by_kind['downstream-token']}** | "
             f"**{totals_by_kind['unresolved-token']}** |")
    L.append("")
    L.append("## All Downstream-Token Call Sites (Mid-Request ACL Update candidates)")
    L.append("")
    L.append("| Domain | Resolver | Target domain | Recommendation |")
    L.append("|---|---|---|---|")
    any_downstream = False
    for r in domain_results:
        for f in r["findings"]:
            if f["kind"] != "downstream-token":
                continue
            any_downstream = True
            L.append(f"| {r['domain']} | `{f['block']}.{f['field']}` | `{f['downstream_domain']}` | "
                     f"{md_escape(recommend_for_finding(f))} |")
    if not any_downstream:
        L.append("| _(none found)_ | | | |")
    L.append("")
    L.append("---")
    L.append(f"*Program roll-up · generated {TODAY} from each domain's `be-07-acl-usage-analysis.md`.*")
    write(OUT_ROLLUP / "00-acl-usage-inventory.md", "\n".join(L))


def main():
    args = sys.argv[1:]
    targets = [a for a in args if not a.startswith("--")] or ALL_DOMAINS
    print(f"\n=== ACL usage analysis — {TODAY} ===\n")
    results = []
    for domain in targets:
        if domain not in ALL_DOMAINS:
            print(f"  UNKNOWN domain '{domain}' — skipping")
            continue
        try:
            results.append(generate_domain(domain))
        except Exception as e:
            print(f"  FAIL {domain}: {type(e).__name__}: {e}")
    if results and set(targets) >= set(ALL_DOMAINS):
        generate_rollup(results)
    print("\nDone.\n")


if __name__ == "__main__":
    main()
