#!/usr/bin/env python3
"""
Frontend GraphQL inventory & federation cross-reference pipeline.

Inputs (all relative to the migration repo root):
  ClientCallingGqlQueries/*.txt         Client-side gql tagged-template sources (pdex-ui-react)
  ClientCallingGqlQueries/QUERY_INVENTORY.md  Usage index (definition -> consuming files)
  code/schemas/*.txt                    spark-internal-graphql SDL (local copies of schemas/*.graphqls)
  output/initial-analysis/*/04-stories.md     Backend story ids (for FE->BE traceability)
  output/frontend-analysis/08-frontend-stories.md  Hand-authored FE stories (parsed for Jira CSV)

Outputs:
  output/frontend-analysis/01-client-inventory.md
  output/frontend-analysis/02-backend-schema-inventory.md
  output/frontend-analysis/03-merged-inventory.md
  output/frontend-analysis/04-domain-analysis.md
  output/frontend-analysis/11-traceability-matrix.md
  output/frontend-analysis/frontend-inventory.json      (machine-readable master data)
  output/jira/frontend/{domain}-fe.csv + all-frontend-stories.csv   (only when 08 exists)

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_frontend.py

⚠ Regeneration overwrites the generated docs above — hand edits belong in the
  hand-authored deliverables (00, 05, 06, 07, 08, 10) which are never overwritten.
"""

import csv
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CLIENT_DIR = ROOT / "ClientCallingGqlQueries"
SCHEMA_DIR = ROOT / "code" / "schemas"
BE_ANALYSIS = ROOT / "output" / "initial-analysis"
FE_OUT = ROOT / "output" / "frontend-analysis"
JIRA_OUT = ROOT / "output" / "jira" / "frontend"

TODAY = date.today().isoformat()

# ─── Domain catalogue ────────────────────────────────────────────────────────
# Phase-1 backend domains and the schema file that owns each (1:1, mirrors
# output/initial-analysis/*/01-schema-inventory.md).
PHASE1_SCHEMA_DOMAIN = {
    "SPARK_Product":       "product",
    "SPARK_Bom":           "bom",
    "SPARK_Claims":        "claims",
    "SPARK_Measurement":   "measurement",
    "SPARK_Impression":    "impression",
    "SPARK_ProductDetail": "productDetails",
    "SPARK_Packaging":     "packaging",
    "SPARK_Watchlist":     "watchlist",
}
DOMAIN_LABELS = {
    "product": "Product", "bom": "BOM", "claims": "Claims",
    "measurement": "Measurement", "impression": "Impression",
    "productDetails": "Product Details", "packaging": "Packaging",
    "watchlist": "Watchlist",
}
DOMAIN_FE_TOKEN = {
    "product": "PRODUCT", "bom": "BOM", "claims": "CLAIM",
    "measurement": "MST", "impression": "IMPRESSION",
    "productDetails": "PDTL", "packaging": "PKG", "watchlist": "WATCHLIST",
}
DOMAIN_DGS = {
    "product": "plm-product (host)", "bom": "plm-product (co-located)",
    "claims": "spark-claims (separate)", "measurement": "plm-product (co-located)",
    "impression": "plm-product (co-located)", "productDetails": "plm-product (co-located)",
    "packaging": "plm-product (co-located)", "watchlist": "plm-product (co-located)",
}
PHASE1_ORDER = ["product", "bom", "measurement", "productDetails",
                "packaging", "watchlist", "impression", "claims"]

# Later-phase schema files -> business-domain label (everything else falls back
# to a label derived from the schema file name).
LATER_SCHEMA_LABEL = {
    "core": "Core / Cross-cutting", "index": "Gateway index",
    "SPARK_Greenfield": "Workspace", "SPARK_Team": "Team", "SPARK_TeamV2": "Team",
    "SPARK_FileLibrary": "Attachment / Files", "SPARK_Combination": "Combination",
    "SPARK_Fabric": "Fabric", "SPARK_Material": "Materials",
    "SPARK_MaterialHub": "Materials Hub", "SPARK_Color": "Color",
    "SPARK_Trim": "Trim", "SPARK_Wash": "Wash", "SPARK_Palette": "Palette",
    "SPARK_Favorite": "Favorites", "SPARK_Tag": "Tags",
    "SPARK_MeasurementTemplate": "Measurement (templates)",
    "SPARK_TightFit": "Measurement (tight-fit)",
    "SPARK_SpecificationTemplate": "Product Details (templates)",
    "SPARK_AccessControl": "Access Control", "SPARK_Role": "Access Control",
    "SPARK_UserGroup": "Access Control", "SPARK_UserAttributes": "User",
    "SPARK_ActivityCenter": "Activity", "SPARK_AdminTools": "Admin",
    "SPARK_RuleLibrary": "Rules", "SPARK_ValueAssessment": "Value Assessment",
    "SPARK_Artwork": "Artwork", "SPARK_Pom": "Measurement (POM)",
    "SPARK_Sizes": "Sizes", "SPARK_SizeTemplate": "Sizes",
    "SPARK_Status": "Status", "SPARK_RecentlyViewed": "Dashboard",
    "SPARK_ToDo": "Dashboard", "SPARK_Banner": "Dashboard",
    "SPARK_Notification": "Notifications", "SPARK_BackgroundNotifications": "Notifications",
    "SPARK_BusinessPartner": "Business Partner", "VMM_BusinessPartner": "Business Partner",
    "VMM_Brand": "Business Partner", "VMM_Location": "Business Partner",
    "SPARK_Relationship": "Relationships", "SPARK_Variation": "Variations",
    "SPARK_RequestDetails": "Requests", "SPARK_RFID": "Sample (RFID)",
    "SPARK_Component": "Components", "SPARK_ByoTemplate": "Templates",
    "SPARK_Pdf": "Export / PDF", "SPARK_Tools": "Admin",
    "SPARK_InsightsIntegration": "Insights", "SPARK_Negotiator": "Negotiator",
    "SPARK_ColorArchroma": "Color", "SPARK_ColorColoro": "Color",
    "SPARK_AsapTGTColorEvaluator": "Color",
    "APEX_ProductPlan": "Product Plan", "SPARK_ProductPlan": "Product Plan",
    "AssortmentItem": "Assortment", "CONFLUENCE_Training": "Training / Resources",
    "Doppler": "Doppler", "IG_Clazz": "Item Hierarchy", "IG_Department": "Item Hierarchy",
    "IG_Division": "Item Hierarchy", "IG_MerchType": "Item Hierarchy",
    "LDAP_Directory": "User Directory", "NEXUS_Attributes": "Nexus Attributes",
    "OBDP_BrandCompliance": "Brand Compliance",
}

BUILTIN_SCALARS = {"String", "Int", "Float", "Boolean", "ID"}


# ─── GraphQL tokenizer (shared by executable-document and SDL parsers) ───────
TOKEN_RE = re.compile(r'''
    (?P<ws>[\s,]+)
  | (?P<comment>\#[^\n]*)
  | (?P<block>"""(?:[^"]|"(?!""))*""")
  | (?P<str>"(?:\\.|[^"\\])*")
  | (?P<spread>\.\.\.)
  | (?P<name>[_A-Za-z][_0-9A-Za-z]*)
  | (?P<punct>[!$():=@\[\]{}|&])
''', re.X)


def tokenize(text):
    toks = []
    for m in TOKEN_RE.finditer(text):
        kind = m.lastgroup
        if kind in ("ws", "comment", "block", "str"):
            if kind in ("block", "str"):
                toks.append(("str", m.group(0)))
            continue
        toks.append((kind, m.group(0)))
    return toks


class Tok:
    def __init__(self, toks):
        self.toks = toks
        self.i = 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def next(self):
        t = self.peek()
        self.i += 1
        return t

    def eof(self):
        return self.i >= len(self.toks)


def skip_balanced(tk, open_p, close_p):
    """Consume from current '(' to matching ')' returning raw arg text."""
    depth = 0
    parts = []
    while not tk.eof():
        kind, val = tk.next()
        if val == open_p:
            depth += 1
            if depth == 1:
                continue
        elif val == close_p:
            depth -= 1
            if depth == 0:
                break
        if depth >= 1:
            parts.append(val)
    return " ".join(parts)


def parse_selection_set(tk):
    """Parse '{ ... }' -> list of selection dicts."""
    sels = []
    kind, val = tk.next()
    if val != "{":
        raise ValueError(f"expected '{{' got {val!r}")
    while not tk.eof():
        kind, val = tk.peek()
        if val == "}":
            tk.next()
            return sels
        if kind == "spread":
            tk.next()
            k2, v2 = tk.peek()
            if v2 == "on":
                tk.next()
                _, tname = tk.next()
                sub = parse_selection_set(tk)
                sels.append({"kind": "inline", "on": tname, "children": sub})
            else:
                _, fname = tk.next()
                # optional directives on spread
                while tk.peek()[1] == "@":
                    tk.next(); tk.next()
                    if tk.peek()[1] == "(":
                        skip_balanced(tk, "(", ")")
                sels.append({"kind": "spread", "name": fname})
            continue
        if kind != "name":
            tk.next()
            continue
        _, name = tk.next()
        alias = None
        if tk.peek()[1] == ":":
            tk.next()
            alias, name = name, tk.next()[1]
        args = None
        if tk.peek()[1] == "(":
            args = skip_balanced(tk, "(", ")")
        directives = []
        while tk.peek()[1] == "@":
            tk.next()
            directives.append(tk.next()[1])
            if tk.peek()[1] == "(":
                skip_balanced(tk, "(", ")")
        children = []
        if tk.peek()[1] == "{":
            children = parse_selection_set(tk)
        sels.append({"kind": "field", "name": name, "alias": alias,
                     "args": args, "directives": directives, "children": children})
    return sels


def parse_type_ref(tk):
    parts = []
    depth = 0
    while not tk.eof():
        kind, val = tk.peek()
        if val == "[":
            depth += 1
            parts.append(tk.next()[1])
        elif val == "]":
            depth -= 1
            parts.append(tk.next()[1])
        elif val == "!":
            parts.append(tk.next()[1])
        elif kind == "name" and (not parts or parts[-1] in ("[",)):
            parts.append(tk.next()[1])
        elif kind == "name" and depth == 0 and parts and parts[-1] not in ("[",):
            break
        else:
            break
    return "".join(parts)


def parse_variables(tk):
    """Parse '(' $var: Type = default ')' -> [(name, type)]."""
    out = []
    if tk.peek()[1] != "(":
        return out
    tk.next()
    while not tk.eof():
        kind, val = tk.next()
        if val == ")":
            break
        if val == "$":
            _, vname = tk.next()
            if tk.peek()[1] == ":":
                tk.next()
            vtype = parse_type_ref(tk)
            # skip default value
            if tk.peek()[1] == "=":
                tk.next()
                d, dv = tk.peek()
                if dv == "{":
                    skip_balanced(tk, "{", "}")
                elif dv == "[":
                    skip_balanced(tk, "[", "]")
                else:
                    tk.next()
            out.append((vname, vtype))
    return out


def parse_executable(text):
    """Parse a gql template -> list of operation/fragment definitions."""
    tk = Tok(tokenize(text))
    defs = []
    while not tk.eof():
        kind, val = tk.peek()
        if val == "{":  # anonymous query shorthand
            sels = parse_selection_set(tk)
            defs.append({"kind": "query", "name": None, "variables": [], "selections": sels})
            continue
        if kind != "name":
            tk.next()
            continue
        tk.next()
        if val in ("query", "mutation", "subscription"):
            name = None
            if tk.peek()[0] == "name":
                name = tk.next()[1]
            variables = parse_variables(tk)
            while tk.peek()[1] == "@":
                tk.next(); tk.next()
                if tk.peek()[1] == "(":
                    skip_balanced(tk, "(", ")")
            sels = parse_selection_set(tk)
            defs.append({"kind": val, "name": name, "variables": variables, "selections": sels})
        elif val == "fragment":
            _, fname = tk.next()
            tk.next()  # 'on'
            _, on_type = tk.next()
            sels = parse_selection_set(tk)
            defs.append({"kind": "fragment", "name": fname, "on": on_type, "selections": sels})
    return defs


# ─── SDL parser ──────────────────────────────────────────────────────────────
def parse_sdl(text, source_file, registry):
    """Parse SDL into registry: types/inputs/enums/interfaces/unions/scalars."""
    tk = Tok(tokenize(text))

    def parse_field_block(type_entry):
        # consume '{' ... '}' of a type/interface/input body
        tk.next()  # '{'
        while not tk.eof():
            kind, val = tk.peek()
            if val == "}":
                tk.next()
                return
            if kind != "name":
                tk.next()
                continue
            _, fname = tk.next()
            args = None
            if tk.peek()[1] == "(":
                args = skip_balanced(tk, "(", ")")
            if tk.peek()[1] == ":":
                tk.next()
            ftype = parse_type_ref(tk)
            deprecated = None
            while tk.peek()[1] == "@":
                tk.next()
                _, dname = tk.next()
                dargs = ""
                if tk.peek()[1] == "(":
                    dargs = skip_balanced(tk, "(", ")")
                if dname == "deprecated":
                    m = re.search(r'"((?:\\.|[^"\\])*)"', dargs)
                    deprecated = m.group(1) if m else "deprecated"
            # skip default value on input fields
            if tk.peek()[1] == "=":
                tk.next()
                d, dv = tk.peek()
                if dv == "{":
                    skip_balanced(tk, "{", "}")
                elif dv == "[":
                    skip_balanced(tk, "[", "]")
                else:
                    tk.next()
            type_entry["fields"][fname] = {
                "type": ftype, "args": args, "deprecated": deprecated,
                "file": source_file,
            }

    while not tk.eof():
        kind, val = tk.peek()
        if kind != "name":
            tk.next()
            continue
        tk.next()
        is_extend = False
        if val == "extend":
            is_extend = True
            _, val = tk.next()
        if val in ("type", "interface", "input"):
            _, tname = tk.next()
            implements = []
            if tk.peek()[1] == "implements":
                tk.next()
                while tk.peek()[0] == "name":
                    implements.append(tk.next()[1])
                    if tk.peek()[1] == "&":
                        tk.next()
            entry = registry["types"].setdefault(tname, {
                "kind": {"type": "object", "interface": "interface", "input": "input"}[val],
                "fields": {}, "implements": implements, "files": [],
            })
            if source_file not in entry["files"]:
                entry["files"].append(source_file)
            if implements and not entry["implements"]:
                entry["implements"] = implements
            if tk.peek()[1] == "{":
                parse_field_block(entry)
        elif val == "enum":
            _, tname = tk.next()
            values = []
            if tk.peek()[1] == "{":
                tk.next()
                while not tk.eof():
                    k2, v2 = tk.next()
                    if v2 == "}":
                        break
                    if k2 == "name":
                        values.append(v2)
            registry["enums"][tname] = {"values": values, "file": source_file}
        elif val == "union":
            _, tname = tk.next()
            if tk.peek()[1] == "=":
                tk.next()
            members = []
            while tk.peek()[0] == "name" or tk.peek()[1] == "|":
                k2, v2 = tk.next()
                if k2 == "name":
                    members.append(v2)
            registry["unions"][tname] = {"members": members, "file": source_file}
        elif val == "scalar":
            _, sname = tk.next()
            registry["scalars"].add(sname)
        elif val == "directive":
            # skip directive definitions
            continue


# ─── Client file loading ─────────────────────────────────────────────────────
GQL_CONST_RE = re.compile(
    r'(?:export\s+)?const\s+([A-Za-z0-9_]+)\s*(?::\s*[A-Za-z0-9_<>\[\]. ]+)?=\s*'
    r'(?:(?:\([^)]*\)|[A-Za-z0-9_]+)\s*=>\s*)?'   # arrow-function gql factories
    r'gql\s*(?:<[^>`]*>)?\s*`'
)


def extract_gql_templates(text):
    """Yield (const_name, template_text, interpolated_const_refs)."""
    for m in GQL_CONST_RE.finditer(text):
        start = m.end()
        i = start
        while i < len(text):
            if text[i] == "\\":
                i += 2
                continue
            if text[i] == "`":
                break
            i += 1
        raw = text[start:i]
        refs = []
        def keep(mm):
            refs.append(mm.group(1).strip())
            return " "
        cleaned = re.sub(r'\.\.\.\s*\$\{([^}]+)\}', keep, raw)
        cleaned = re.sub(r'\$\{([^}]+)\}', keep, cleaned)
        yield m.group(1), cleaned, refs


def load_client_defs():
    """Parse every client txt file -> list of definition dicts."""
    defs = []
    for f in sorted(CLIENT_DIR.glob("*.txt")):
        lib, _, base = f.stem.partition("__")
        text = f.read_text(encoding="utf-8", errors="replace")
        for const, template, refs in extract_gql_templates(text):
            try:
                parsed = parse_executable(template)
            except Exception as e:  # tolerant: record and continue
                defs.append({"const": const, "lib": lib, "base": base, "txt": f.name,
                             "kind": "parse_error", "error": str(e), "interp_refs": refs})
                continue
            for d in parsed:
                d2 = dict(d)
                d2.update({"const": const, "lib": lib, "base": base,
                           "txt": f.name, "interp_refs": refs})
                defs.append(d2)
    return defs


# ─── QUERY_INVENTORY.md usage index ─────────────────────────────────────────
def load_usage_index():
    """-> {(lib, base, const): {"src": path, "used_in": [...], "client_domain": str}}"""
    idx = {}
    text = (CLIENT_DIR / "QUERY_INVENTORY.md").read_text(encoding="utf-8", errors="replace")
    domain = None
    src = None
    for line in text.splitlines():
        m = re.match(r'^## (.+)$', line)
        if m and m.group(1) not in ("Summary", "Table of Contents"):
            domain = m.group(1).strip()
            continue
        m = re.match(r'^### `([^`]+)`', line)
        if m:
            src = m.group(1)
            continue
        m = re.match(r'^\|\s*[^|]*?\s*\|\s*`([A-Za-z0-9_]+)`\s*\|(.*)\|\s*$', line)
        if m and src:
            const = m.group(1)
            used = re.findall(r'`([^`]+)`', m.group(2))
            libm = re.search(r'src/libs/([^/]+)/', src)
            lib = libm.group(1) if libm else ""
            base = Path(src).stem
            idx[(lib, base, const)] = {"src": src, "used_in": used, "client_domain": domain}
    return idx


# ─── Backend story index (op name -> BE story id) ───────────────────────────
BE_STORY_RE = re.compile(r'^### ([A-Z]+-BE-[A-Z]-\d+[a-z]?)\s*·\s*`?([A-Za-z0-9_]+)', re.M)


def load_be_stories():
    """-> {domain: {op_name: story_id}}"""
    out = defaultdict(dict)
    for domain in PHASE1_ORDER:
        p = BE_ANALYSIS / domain / "04-stories.md"
        if not p.exists():
            continue
        for sid, op in BE_STORY_RE.findall(p.read_text(encoding="utf-8", errors="replace")):
            out[domain].setdefault(op, sid)
    return out


# ─── Cross-reference engine ──────────────────────────────────────────────────
def base_type(type_str):
    return re.sub(r'[\[\]!\s]', "", type_str or "")


def build_schema_registry():
    registry = {"types": {}, "enums": {}, "unions": {}, "scalars": set()}
    for f in sorted(SCHEMA_DIR.glob("*.txt")):
        parse_sdl(f.read_text(encoding="utf-8", errors="replace"), f.stem, registry)
    return registry


def schema_domain(schema_file):
    if schema_file in PHASE1_SCHEMA_DOMAIN:
        return PHASE1_SCHEMA_DOMAIN[schema_file], True
    label = LATER_SCHEMA_LABEL.get(schema_file, schema_file.replace("SPARK_", ""))
    return label, False


def walk_selections(sels, type_name, registry, fragments, coverage, missing, path, seen_frags):
    """Recursively validate selections against SDL type; record coverage/missing."""
    t = registry["types"].get(type_name)
    is_union = type_name in registry["unions"]
    for s in sels:
        if s["kind"] == "inline":
            walk_selections(s["children"], s["on"], registry, fragments,
                            coverage, missing, path, seen_frags)
            continue
        if s["kind"] == "spread":
            frag = fragments.get(s["name"])
            if frag is None:
                missing.append((path or type_name, f"…{s['name']} (fragment defined outside snapshot)"))
            elif s["name"] not in seen_frags:
                seen_frags.add(s["name"])
                walk_selections(frag["selections"], frag["on"], registry, fragments,
                                coverage, missing, frag["on"], seen_frags)
            continue
        fname = s["name"]
        if fname == "__typename":
            continue
        if is_union:
            missing.append((type_name, f"{fname} (union — needs inline fragment)"))
            continue
        if t is None:
            # unknown container type: cannot validate deeper
            continue
        fdef = t["fields"].get(fname)
        if fdef is None:
            # check implemented interfaces
            found = False
            for iname in t.get("implements", []):
                idef = registry["types"].get(iname, {}).get("fields", {}).get(fname)
                if idef:
                    fdef = idef
                    found = True
                    break
            if not found:
                missing.append((type_name, fname))
                continue
        coverage.add((type_name, fname))
        if s["children"]:
            walk_selections(s["children"], base_type(fdef["type"]), registry,
                            fragments, coverage, missing, base_type(fdef["type"]), seen_frags)


def count_fields(sels):
    n = 0
    for s in sels:
        if s["kind"] == "field":
            n += 1 + count_fields(s["children"])
        elif s["kind"] == "inline":
            n += count_fields(s["children"])
    return n


def collect_spreads(sels, out):
    for s in sels:
        if s["kind"] == "spread":
            out.add(s["name"])
        elif s.get("children"):
            collect_spreads(s["children"], out)
    return out


def classify_usage(paths):
    comps, hooks, tests, other = [], [], [], []
    for p in paths:
        if p in ("—", ""):
            continue
        b = Path(p).name
        if ".test." in b or ".spec." in b:
            tests.append(p)
        elif re.match(r'^use[A-Z]', b):
            hooks.append(p)
        elif b.endswith(".tsx") and b[0].isupper():
            comps.append(p)
        else:
            other.append(p)
    return comps, hooks, tests, other


def cross_reference(client_defs, registry, usage_idx, be_stories):
    # fragment registry: by GraphQL fragment name AND by const name
    fragments = {}
    for d in client_defs:
        if d["kind"] == "fragment":
            fragments[d["name"]] = d
            fragments[d["const"]] = d

    q_fields = registry["types"].get("Query", {}).get("fields", {})
    m_fields = registry["types"].get("Mutation", {}).get("fields", {})

    ops = []
    coverage = set()
    for d in client_defs:
        if d["kind"] not in ("query", "mutation", "subscription"):
            continue
        root_reg = q_fields if d["kind"] == "query" else m_fields
        u = usage_idx.get((d["lib"], d["base"], d["const"]), {})
        roots = []
        missing = []
        seen_frags = set()
        for s in d["selections"]:
            if s["kind"] != "field":
                continue
            rdef = root_reg.get(s["name"])
            if rdef is None:
                roots.append({"field": s["name"], "schema_file": None,
                              "domain": None, "phase1": False, "be_story": None,
                              "return_type": None})
                continue
            sf = rdef["file"]
            dom, p1 = schema_domain(sf)
            rt = base_type(rdef["type"])
            coverage.add(("Query" if d["kind"] == "query" else "Mutation", s["name"]))
            walk_selections(s["children"], rt, registry, fragments,
                            coverage, missing, rt, seen_frags)
            roots.append({"field": s["name"], "schema_file": sf, "domain": dom,
                          "phase1": p1,
                          "be_story": be_stories.get(dom, {}).get(s["name"]),
                          "return_type": rt})
        spreads = collect_spreads(d["selections"], set())
        comps, hooks, tests, other = classify_usage(u.get("used_in", []))
        # primary domain = first phase-1 root, else first mapped root
        p1_roots = [r for r in roots if r["phase1"]]
        mapped = [r for r in roots if r["schema_file"]]
        primary = (p1_roots or mapped or [{"domain": None}])[0]["domain"]
        ops.append({
            "const": d["const"], "op_name": d["name"], "kind": d["kind"],
            "lib": d["lib"], "base": d["base"], "txt": d["txt"],
            "src": u.get("src", f"(local) ClientCallingGqlQueries/{d['txt']}"),
            "client_domain": u.get("client_domain", d["lib"]),
            "variables": d["variables"], "roots": roots,
            "fragments": sorted(spreads | set(d["interp_refs"])),
            "field_count": count_fields(d["selections"]),
            "missing": missing,
            "components": comps, "hooks": hooks, "tests": tests, "services": other,
            "primary_domain": primary,
        })

    # fragment records (validated against their target type)
    frag_records = []
    for d in client_defs:
        if d["kind"] != "fragment":
            continue
        u = usage_idx.get((d["lib"], d["base"], d["const"]), {})
        missing = []
        walk_selections(d["selections"], d["on"], registry, fragments,
                        coverage, missing, d["on"], {d["name"]})
        dom, p1 = (None, False)
        for sf, files in [(t, registry["types"][t]["files"]) for t in [d["on"]] if t in registry["types"]]:
            dom, p1 = schema_domain(files[0])
        frag_records.append({
            "const": d["const"], "name": d["name"], "on": d["on"],
            "lib": d["lib"], "base": d["base"],
            "src": u.get("src", f"(local) ClientCallingGqlQueries/{d['txt']}"),
            "client_domain": u.get("client_domain", d["lib"]),
            "field_count": count_fields(d["selections"]),
            "missing": missing, "domain": dom, "phase1": p1,
            "used_in": u.get("used_in", []),
        })

    return ops, frag_records, coverage, fragments


# ─── Markdown helpers ────────────────────────────────────────────────────────
def md_escape(s):
    return (s or "").replace("|", "\\|")


def fmt_vars(variables):
    return ", ".join(f"${n}: {t}" for n, t in variables) or "—"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


# ─── Doc 01: client inventory ────────────────────────────────────────────────
def emit_client_inventory(ops, frags, dynamics=()):
    all_ops, all_frags = ops, frags
    ops = [o for o in all_ops if any(r["phase1"] for r in o["roots"])]
    frags = [f for f in all_frags if f["phase1"]]
    L = []
    L.append("# Frontend GraphQL Client Inventory — Phase-1 Domains")
    L.append("")
    L.append(f"> Source: `pdex-ui-react` gql definitions (ClientCallingGqlQueries snapshot) · Generated: {TODAY}")
    L.append("> Scope: frontend operations that call a phase-1 domain root field (product, bom, measurement, productDetails, packaging, watchlist, impression, claims), with variables, root fields, fragment usage and consuming files.")
    L.append("")
    q = [o for o in ops if o["kind"] == "query"]
    m = [o for o in ops if o["kind"] == "mutation"]
    L.append("## Summary")
    L.append("")
    L.append("| Stat | Count |")
    L.append("|---|---|")
    L.append(f"| Phase-1 operations | {len(ops)} |")
    L.append(f"| Queries | {len(q)} |")
    L.append(f"| Mutations | {len(m)} |")
    L.append(f"| Fragments on phase-1 types | {len(frags)} |")
    L.append(f"| Client libraries involved | {len({o['lib'] for o in ops})} |")
    L.append(f"| Dynamic (runtime-composed) definitions | {len(dynamics)} |")
    L.append("")
    L.append("### Out of scope")
    L.append("")
    L.append(f"- {len(all_ops) - len(ops)} further client operations resolve to later-phase domains or to services outside spark-internal-graphql — excluded per program scope (phase 1 = the 8 domains above).")
    L.append(f"- {len(all_frags) - len(frags)} further fragments target non-phase-1 types.")
    L.append("")
    if dynamics:
        L.append("## Dynamic / runtime-composed definitions")
        L.append("")
        L.append("- These gql documents are assembled at runtime (interpolated operation names, conditional fragments) and cannot be statically inventoried.")
        L.append("- They are incompatible with GraphQL codegen and persisted queries — each needs an explicit refactoring story before federation cutover.")
        L.append("")
        L.append("| Const | Client file | Failure mode |")
        L.append("|---|---|---|")
        for d in dynamics:
            L.append(f"| `{d['const']}` | `ClientCallingGqlQueries/{d['txt']}` | {md_escape(d['error'])} |")
        L.append("")
    by_cd = defaultdict(list)
    for o in ops:
        doms = {r["domain"] for r in o["roots"] if r["phase1"]}
        for d in doms:
            by_cd[d].append(o)
    frag_by_cd = defaultdict(list)
    for f in frags:
        frag_by_cd[f["domain"]].append(f)
    for cd in [d for d in PHASE1_ORDER if d in by_cd or d in frag_by_cd]:
        L.append(f"## {DOMAIN_LABELS[cd]} (`{cd}`)")
        L.append("")
        group = by_cd[cd]
        L.append(f"- Definitions: {len(group)} operations ({sum(1 for o in group if o['kind']=='query')} queries, "
                 f"{sum(1 for o in group if o['kind']=='mutation')} mutations) + {len(frag_by_cd.get(cd, []))} fragments")
        libs = sorted({o["lib"] for o in group})
        L.append(f"- Client libraries: {', '.join(f'`{x}`' for x in libs)}")
        L.append("")
        L.append("| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for o in sorted(group, key=lambda x: (x["kind"], x["const"])):
            roots = ", ".join(f"`{r['field']}`" for r in o["roots"]) or "—"
            fragl = ", ".join(f"`{x}`" for x in o["fragments"]) or "—"
            comps = "<br>".join(f"`{Path(c).name}`" for c in o["components"]) or "—"
            hooks = "<br>".join(f"`{Path(c).name}`" for c in o["hooks"]) or "—"
            other = "<br>".join(f"`{Path(c).name}`" for c in (o["services"] + o["tests"])[:6]) or "—"
            L.append(f"| `{o['op_name'] or '(anonymous)'}` | {o['kind']} | `{o['const']}` | `{o['src']}` "
                     f"| {md_escape(fmt_vars(o['variables']))} | {roots} | {fragl} | {comps} | {hooks} | {other} |")
        fr = frag_by_cd.get(cd, [])
        if fr:
            L.append("")
            L.append("### Fragments")
            L.append("")
            L.append("| Fragment | On type | Const | Client file | Fields | Used in |")
            L.append("|---|---|---|---|---|---|")
            for f in sorted(fr, key=lambda x: x["name"] or ""):
                used = "<br>".join(f"`{Path(u).name}`" for u in f["used_in"][:6]) or "—"
                L.append(f"| `{f['name']}` | `{f['on']}` | `{f['const']}` | `{f['src']}` | {f['field_count']} | {used} |")
        L.append("")
    write(FE_OUT / "01-client-inventory.md", "\n".join(L))


# ─── Doc 02: backend schema inventory ────────────────────────────────────────
def emit_backend_inventory(registry, ops, coverage):
    # group types by schema file
    files = defaultdict(lambda: {"types": [], "inputs": [], "interfaces": [], "enums": [], "unions": []})
    for tname, t in registry["types"].items():
        for f in t["files"]:
            key = {"object": "types", "input": "inputs", "interface": "interfaces"}[t["kind"]]
            files[f][key].append(tname)
    for ename, e in registry["enums"].items():
        files[e["file"]]["enums"].append(ename)
    for uname, u in registry["unions"].items():
        files[u["file"]]["unions"].append(uname)

    q_fields = registry["types"].get("Query", {}).get("fields", {})
    m_fields = registry["types"].get("Mutation", {}).get("fields", {})
    used_roots = {(k, r["field"]) for o in ops for r in o["roots"]
                  for k in [("Query" if o["kind"] == "query" else "Mutation")]}

    p1_files = set(PHASE1_SCHEMA_DOMAIN)

    def p1_type(t):
        return any(f in p1_files for f in t["files"])

    L = []
    L.append("# Backend GraphQL Schema Inventory — spark-internal-graphql (Phase-1 Domains)")
    L.append("")
    L.append(f"> Source: `schemas/*.graphqls` (spark-internal-graphql) · Generated: {TODAY}")
    L.append("> Scope: the 8 phase-1 domain schemas. Cross-referenced against the frontend client inventory (01-client-inventory.md).")
    L.append("")
    L.append("## Summary")
    L.append("")
    p1q = {k: v for k, v in q_fields.items() if v["file"] in p1_files}
    p1m = {k: v for k, v in m_fields.items() if v["file"] in p1_files}
    L.append("| Stat | Count |")
    L.append("|---|---|")
    L.append(f"| Phase-1 schema files | {len(p1_files)} (of {len(list(SCHEMA_DIR.glob('*.txt')))} total) |")
    L.append(f"| Object types (phase-1 files) | {sum(1 for t in registry['types'].values() if t['kind'] == 'object' and p1_type(t))} |")
    L.append(f"| Input types (phase-1 files) | {sum(1 for t in registry['types'].values() if t['kind'] == 'input' and p1_type(t))} |")
    L.append(f"| Interfaces (phase-1 files) | {sum(1 for t in registry['types'].values() if t['kind'] == 'interface' and p1_type(t))} |")
    L.append(f"| Enums (phase-1 files) | {sum(1 for e in registry['enums'].values() if e['file'] in p1_files)} |")
    L.append(f"| Unions (phase-1 files) | {sum(1 for u in registry['unions'].values() if u['file'] in p1_files)} |")
    L.append(f"| Custom scalars (gateway-wide) | {len(registry['scalars'])} ({', '.join(sorted(registry['scalars']))}) |")
    L.append(f"| Phase-1 Query root fields | {len(p1q)} |")
    L.append(f"| Phase-1 Mutation root fields | {len(p1m)} |")
    L.append(f"| Phase-1 Query fields called by the frontend | {sum(1 for f in p1q if ('Query', f) in used_roots)} |")
    L.append(f"| Phase-1 Mutation fields called by the frontend | {sum(1 for f in p1m if ('Mutation', f) in used_roots)} |")
    L.append("")

    dep = []
    for tname, t in registry["types"].items():
        for fname, fd in t["fields"].items():
            if fd["deprecated"] and fd["file"] in p1_files:
                dep.append((tname, fname, fd["deprecated"], fd["file"]))
    L.append("## Deprecations (phase-1 schemas)")
    L.append("")
    if dep:
        L.append("| Type | Field | Reason | Schema file |")
        L.append("|---|---|---|---|")
        for tname, fname, reason, f in sorted(dep):
            L.append(f"| `{tname}` | `{fname}` | {md_escape(reason)} | `schemas/{f}.graphqls` |")
    else:
        L.append("- No `@deprecated` directives found in the phase-1 SDL files.")
    L.append("")

    def emit_file_section(f, dom_label, phase_note):
        info = files.get(f, {"types": [], "inputs": [], "interfaces": [], "enums": [], "unions": []})
        fq = sorted(k for k, v in q_fields.items() if v["file"] == f)
        fm = sorted(k for k, v in m_fields.items() if v["file"] == f)
        L.append(f"### `schemas/{f}.graphqls` — {dom_label}{phase_note}")
        L.append("")
        L.append(f"- Object types ({len([t for t in info['types'] if t not in ('Query','Mutation')])}): "
                 + (", ".join(f"`{t}`" for t in sorted(info["types"]) if t not in ("Query", "Mutation")) or "—"))
        if info["inputs"]:
            L.append(f"- Input types ({len(info['inputs'])}): " + ", ".join(f"`{t}`" for t in sorted(info["inputs"])))
        if info["interfaces"]:
            L.append("- Interfaces: " + ", ".join(f"`{t}`" for t in sorted(info["interfaces"])))
        if info["enums"]:
            L.append("- Enums: " + ", ".join(f"`{t}`" for t in sorted(info["enums"])))
        if info["unions"]:
            L.append("- Unions: " + ", ".join(f"`{t}`" for t in sorted(info["unions"])))
        if fq:
            L.append("- Query fields: " + ", ".join(
                f"`{x}`" + (" ✅" if ("Query", x) in used_roots else " ⚠ unused-by-FE") for x in fq))
        if fm:
            L.append("- Mutation fields: " + ", ".join(
                f"`{x}`" + (" ✅" if ("Mutation", x) in used_roots else " ⚠ unused-by-FE") for x in fm))
        L.append("")

    L.append("## Phase-1 domain schemas")
    L.append("")
    L.append("✅ = called by the frontend today · ⚠ = no frontend caller found (server-side or dead field)")
    L.append("")
    for dom in PHASE1_ORDER:
        f = [k for k, v in PHASE1_SCHEMA_DOMAIN.items() if v == dom][0]
        emit_file_section(f, DOMAIN_LABELS[dom], f" · DGS target: `{DOMAIN_DGS[dom]}`")
    L.append("## Out of scope")
    L.append("")
    L.append(f"- The remaining {len(list(SCHEMA_DIR.glob('*.txt'))) - len(p1_files)} schema files (later-phase and platform-stitched domains) are excluded per program scope.")
    L.append("")
    write(FE_OUT / "02-backend-schema-inventory.md", "\n".join(L))


# ─── Doc 03: merged inventory ────────────────────────────────────────────────
def emit_merged_inventory(ops, frags, registry, coverage):
    q_fields = registry["types"].get("Query", {}).get("fields", {})
    m_fields = registry["types"].get("Mutation", {}).get("fields", {})

    L = []
    L.append("# Merged GraphQL Inventory — Frontend Usage × Backend Schema")
    L.append("")
    L.append(f"> Authoritative migration-planning inventory · Generated: {TODAY}")
    L.append("> One row per frontend operation × backend root field. FE story ids resolve in 08-frontend-stories.md; BE story ids in output/initial-analysis/{{domain}}/04-stories.md.")
    L.append("")

    rows = []
    for o in ops:
        for r in o["roots"]:
            rows.append((o, r))

    p1_rows = [(o, r) for o, r in rows if r["phase1"]]
    later_rows = [(o, r) for o, r in rows if r["schema_file"] and not r["phase1"]]
    unmapped = [(o, r) for o, r in rows if not r["schema_file"]]

    L.append("## Summary")
    L.append("")
    L.append("| Bucket | Operation-to-root-field rows |")
    L.append("|---|---|")
    L.append(f"| Phase-1 domains (8) — in scope | {len(p1_rows)} |")
    L.append(f"| Later-phase / shared domains — out of scope | {len(later_rows)} |")
    L.append(f"| No mapping in spark-internal-graphql — out of scope | {len(unmapped)} |")
    L.append("")
    L.append("- Program scope: only phase-1 domain queries/mutations and their fields are inventoried below.")
    L.append("- Out-of-scope rows are counted for completeness; they migrate with their own subgraph phase.")
    L.append("")

    L.append("## Phase-1 domains")
    L.append("")
    for dom in PHASE1_ORDER:
        drows = [(o, r) for o, r in p1_rows if r["domain"] == dom]
        if not drows:
            continue
        L.append(f"### {DOMAIN_LABELS[dom]} (`{dom}`) — {len(drows)} rows · DGS: `{DOMAIN_DGS[dom]}`")
        L.append("")
        L.append("| Backend resolver (root field) | GraphQL kind | BE story | Client operation | Client file | Components | Fields req. | Missing fields | Notes |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for o, r in sorted(drows, key=lambda x: (x[1]["field"], x[0]["const"])):
            miss = "; ".join(f"`{t}.{f}`" for t, f in o["missing"][:5]) or "—"
            if len(o["missing"]) > 5:
                miss += f" (+{len(o['missing'])-5})"
            note = []
            if len(o["roots"]) > 1:
                note.append(f"multi-root op ({len(o['roots'])} root fields)")
            if o["fragments"]:
                note.append(f"{len(o['fragments'])} fragment(s)")
            L.append(f"| `{r['field']}` | {o['kind']} | {r['be_story'] or '—'} "
                     f"| `{o['op_name'] or o['const']}` | `{o['src']}` "
                     f"| {len(o['components'])} | {o['field_count']} | {miss} | {'; '.join(note) or '—'} |")
        L.append("")

    L.append("## Unused backend operations on phase-1 schemas (no frontend caller)")
    L.append("")
    L.append("- Candidates for deprecation review, or callers outside pdex-ui-react (service-to-service, exports, jobs).")
    L.append("")
    used_roots = {("Query" if o["kind"] == "query" else "Mutation", r["field"]) for o in ops for r in o["roots"]}
    L.append("| Root field | Kind | Schema file | Domain |")
    L.append("|---|---|---|---|")
    for kind_label, reg in (("query", q_fields), ("mutation", m_fields)):
        tkey = "Query" if kind_label == "query" else "Mutation"
        for fname in sorted(reg):
            if (tkey, fname) not in used_roots and reg[fname]["file"] in PHASE1_SCHEMA_DOMAIN:
                dom, _ = schema_domain(reg[fname]["file"])
                L.append(f"| `{fname}` | {kind_label} | `schemas/{reg[fname]['file']}.graphqls` | {DOMAIN_LABELS.get(dom, dom)} |")
    L.append("")

    L.append("## Unused schema fields on phase-1 types")
    L.append("")
    L.append("- Fields defined on phase-1 object types that no frontend selection ever requests.")
    L.append("- Input: consolidation candidates when deriving the federated schema.")
    L.append("")
    L.append("| Type | Unused fields |")
    L.append("|---|---|")
    for tname in sorted(registry["types"]):
        t = registry["types"][tname]
        if t["kind"] != "object" or tname in ("Query", "Mutation"):
            continue
        if not any(f in PHASE1_SCHEMA_DOMAIN for f in t["files"]):
            continue
        unused = [f for f in t["fields"] if (tname, f) not in coverage]
        if unused and len(unused) < len(t["fields"]):
            L.append(f"| `{tname}` | {', '.join(f'`{x}`' for x in sorted(unused))} |")
        elif unused:
            L.append(f"| `{tname}` | *(entire type unreferenced by FE selections)* |")
    L.append("")
    write(FE_OUT / "03-merged-inventory.md", "\n".join(L))


# ─── Doc 04: domain-level analysis ───────────────────────────────────────────
def emit_domain_analysis(ops, frags, registry):
    L = []
    L.append("# Domain-Level Analysis — Frontend GraphQL by Business Domain")
    L.append("")
    L.append(f"> Groups every frontend operation by backend business domain (not by client file) · Generated: {TODAY}")
    L.append("")
    by_dom = defaultdict(list)
    for o in ops:
        doms = {r["domain"] for r in o["roots"] if r["schema_file"]}
        for d in doms:
            by_dom[d].append(o)

    L.append("## Phase-1 domains")
    L.append("")
    for dom in PHASE1_ORDER:
        group = by_dom.get(dom, [])
        L.append(f"### {DOMAIN_LABELS[dom]} (`{dom}`)")
        L.append("")
        qs = [o for o in group if o["kind"] == "query"]
        ms = [o for o in group if o["kind"] == "mutation"]
        L.append(f"- Frontend operations: {len(group)} ({len(qs)} queries, {len(ms)} mutations)")
        L.append(f"- Backend ownership: `{DOMAIN_DGS[dom]}` · schema `schemas/{[k for k,v in PHASE1_SCHEMA_DOMAIN.items() if v==dom][0]}.graphqls`")
        libs = sorted({o["lib"] for o in group})
        L.append(f"- Client ownership (libraries): {', '.join(f'`{x}`' for x in libs) or '—'}")
        cds = sorted({o["client_domain"] for o in group})
        L.append(f"- Client domains consuming: {', '.join(cds) or '—'}")
        dom_frags = sorted({fr for o in group for fr in o["fragments"]})
        if dom_frags:
            L.append(f"- Shared fragments: {', '.join(f'`{x}`' for x in dom_frags)}")
        # cross-domain: ops in this domain that also hit other domains
        cross = defaultdict(list)
        for o in group:
            others = {r["domain"] for r in o["roots"] if r["schema_file"] and r["domain"] != dom}
            for od in others:
                cross[od].append(o["op_name"] or o["const"])
        if cross:
            L.append("- Cross-domain operations (same document also selects another domain's root field):")
            for od in sorted(cross):
                L.append(f"  - with **{DOMAIN_LABELS.get(od, od)}**: " + ", ".join(f"`{x}`" for x in sorted(set(cross[od]))[:8]))
        if qs:
            L.append("- Queries: " + ", ".join(f"`{o['op_name'] or o['const']}`" for o in sorted(qs, key=lambda x: x['const'])))
        if ms:
            L.append("- Mutations: " + ", ".join(f"`{o['op_name'] or o['const']}`" for o in sorted(ms, key=lambda x: x['const'])))
        L.append("")

    # shared object types across domains (phase-1 types selected by >1 client domain)
    L.append("## Shared object types (phase-1)")
    L.append("")
    L.append("- Phase-1 types selected by fragments from more than one client domain — federation `@key` candidates.")
    L.append("")
    type_clients = defaultdict(set)
    for f in frags:
        if f["phase1"]:
            type_clients[f["on"]].add(f["client_domain"])
    L.append("| Type | Client domains with fragments on it |")
    L.append("|---|---|")
    for tname in sorted(type_clients):
        if len(type_clients[tname]) > 1:
            L.append(f"| `{tname}` | {', '.join(sorted(type_clients[tname]))} |")
    L.append("")
    write(FE_OUT / "04-domain-analysis.md", "\n".join(L))


# ─── Doc 11: traceability matrix ─────────────────────────────────────────────
def emit_traceability(ops, fe_story_index):
    L = []
    L.append("# Traceability Matrix — Domain → Schema → Resolver → Client → Impact → Stories")
    L.append("")
    L.append(f"> Generated: {TODAY} · One row per phase-1 frontend operation × backend root field.")
    L.append("> Chain: Business Domain → Backend Schema → Resolver → Frontend Query → Client Component → FE story → BE story.")
    L.append("")
    for dom in PHASE1_ORDER:
        rows = [(o, r) for o in ops for r in o["roots"] if r["phase1"] and r["domain"] == dom]
        if not rows:
            continue
        L.append(f"## {DOMAIN_LABELS[dom]}")
        L.append("")
        L.append("| Backend schema | Resolver | Frontend operation | Components / hooks | FE story | BE story |")
        L.append("|---|---|---|---|---|---|")
        for o, r in sorted(rows, key=lambda x: (x[1]["field"], x[0]["const"])):
            consumers = o["components"] + o["hooks"]
            cons = "<br>".join(f"`{Path(c).name}`" for c in consumers[:4]) or "—"
            if len(consumers) > 4:
                cons += f"<br>(+{len(consumers)-4})"
            fe = fe_story_index.get((dom, o["const"])) or fe_story_index.get((dom, r["field"])) or "—"
            L.append(f"| `schemas/{r['schema_file']}.graphqls` | `{r['field']}` "
                     f"| `{o['op_name'] or o['const']}` | {cons} | {fe} | {r['be_story'] or '—'} |")
        L.append("")
    write(FE_OUT / "11-traceability-matrix.md", "\n".join(L))


# ─── FE stories parsing + Jira CSV ───────────────────────────────────────────
FE_STORY_RE = re.compile(r'^### ([A-Z]+-FE-\d+)\s*·\s*(.+)$', re.M)


def parse_fe_stories():
    p = FE_OUT / "08-frontend-stories.md"
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8", errors="replace")
    matches = list(FE_STORY_RE.finditer(text))
    stories = []
    for i, m in enumerate(matches):
        body = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        def grab(label):
            mm = re.search(rf'\*\*{label}:\*\*\s*([^\n·]+)', body)
            return mm.group(1).strip() if mm else ""
        ops_m = re.search(r'\*\*Operations:\*\*\s*([^\n]+)', body)
        stories.append({
            "id": m.group(1), "title": m.group(2).strip(),
            "type": grab("Type"), "impact": grab("Impact"),
            "domain": grab("Domain"), "effort": grab("Estimated effort"),
            "depends": [d.strip() for d in re.split(r'[,;]', grab("Depends on")) if d.strip() and d.strip() != "—"],
            "operations": [x.strip().strip('`') for x in (ops_m.group(1).split(',') if ops_m else [])],
            "body": body.strip(),
        })
    return stories


def domain_key_from_token(token):
    for k, v in DOMAIN_FE_TOKEN.items():
        if v == token:
            return k
    return token.lower()


FE_EPIC_NAME = "Federate BreakDown Product — Frontend"
FE_EPIC_DESC = (
    "Umbrella epic for the pdex-ui-react frontend migration to the federated GraphQL "
    "gateway. Holds the frontend stories for the 8 phase-1 domains (Product, Impression, "
    "BOM, Measurement, Product Details, Packaging, Watchlist, Claims) plus the shared "
    "platform enablement stories. Every story lists the backend stories it depends on; "
    "a frontend story is Done only after its backend dependencies are delivered."
)
CSV_HEADER = ["Issue Type", "Story ID", "Summary", "Epic Name", "Epic Link", "Phase",
              "T-shirt size", "Labels", "Labels", "Labels", "Parent Link",
              "Depends On", "Status", "Description"]


def impact_to_tshirt(impact):
    return {"High": "L", "Medium": "M", "Low": "S", "None": "XS"}.get(impact.split()[0] if impact else "", "M")


def md_to_jira(md):
    t = re.sub(r'^####\s+(.+)$', r'*\1*', md, flags=re.M)
    t = re.sub(r'\*\*([^*]+)\*\*', r'*\1*', t)
    t = re.sub(r'`([^`]+)`', r'{{\1}}', t)
    t = re.sub(r'^- ', '* ', t, flags=re.M)
    t = re.sub(r'^  - ', '** ', t, flags=re.M)
    return t


def emit_jira(stories):
    if not stories:
        print("  (08-frontend-stories.md not found — skipping Jira CSVs)")
        return
    JIRA_OUT.mkdir(parents=True, exist_ok=True)
    by_dom = defaultdict(list)
    for s in stories:
        token = s["id"].rsplit("-FE-", 1)[0]
        by_dom[domain_key_from_token(token)].append(s)

    def rows_for(stories_group, include_epic):
        rows = []
        if include_epic:
            rows.append(["Epic", "", FE_EPIC_NAME, FE_EPIC_NAME, "", "", "",
                         "fed-graphql-fe", "frontend", "epic", "", "", "", FE_EPIC_DESC])
        for s in stories_group:
            dom = domain_key_from_token(s["id"].rsplit("-FE-", 1)[0])
            label = DOMAIN_LABELS.get(dom, dom.title())
            rows.append([
                "Story", s["id"], f"[{label} FE] {s['title']} [{s['id']}]",
                "", FE_EPIC_NAME, "FE", impact_to_tshirt(s["impact"]),
                "fed-graphql-fe", dom, (s["type"] or "migration").lower().replace(" ", "-"),
                "", " ".join(s["depends"]), "To Do", md_to_jira(s["body"]),
            ])
        return rows

    for dom, group in sorted(by_dom.items()):
        out = JIRA_OUT / f"{dom}-fe.csv"
        with out.open("w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh)
            w.writerow(CSV_HEADER)
            for r in rows_for(sorted(group, key=lambda s: s["id"]), include_epic=False):
                w.writerow(r)
        print(f"  wrote {out.relative_to(ROOT)}")
    out = JIRA_OUT / "all-frontend-stories.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_HEADER)
        for r in rows_for(sorted(stories, key=lambda s: s["id"]), include_epic=True):
            w.writerow(r)
    print(f"  wrote {out.relative_to(ROOT)}")


# ─── Doc 09: dependency matrix (generated from 08 + BE indexes) ──────────────
def emit_dependency_matrix(stories):
    if not stories:
        return
    L = []
    L.append("# Story Dependency Matrix — Frontend × Backend")
    L.append("")
    L.append(f"> Generated from 08-frontend-stories.md · {TODAY}")
    L.append("> A frontend story is not Done until every backend story it depends on has been delivered.")
    L.append("")
    L.append("| FE story | Title | Impact | Depends on (BE / FE) | Domain |")
    L.append("|---|---|---|---|---|")
    for s in sorted(stories, key=lambda x: x["id"]):
        dom = domain_key_from_token(s["id"].rsplit("-FE-", 1)[0])
        deps = ", ".join(s["depends"]) or "—"
        L.append(f"| {s['id']} | {md_escape(s['title'])} | {s['impact'] or '—'} | {deps} | {DOMAIN_LABELS.get(dom, dom.title())} |")
    L.append("")
    L.append("## Reverse index — backend story → blocked frontend stories")
    L.append("")
    rev = defaultdict(list)
    for s in stories:
        for d in s["depends"]:
            if "-BE-" in d:
                rev[d].append(s["id"])
    L.append("| BE story | Blocks FE stories |")
    L.append("|---|---|")
    for d in sorted(rev):
        L.append(f"| {d} | {', '.join(sorted(rev[d]))} |")
    L.append("")
    write(FE_OUT / "09-story-dependency-matrix.md", "\n".join(L))


# ─── main ────────────────────────────────────────────────────────────────────
def main():
    print("Parsing client gql definitions…")
    client_defs = load_client_defs()
    errors = [d for d in client_defs if d["kind"] == "parse_error"]
    print(f"  {len(client_defs)} definitions ({len(errors)} parse errors)")
    for e in errors:
        print(f"    ! {e['txt']} :: {e['const']} :: {e['error']}")

    print("Parsing usage index…")
    usage_idx = load_usage_index()
    print(f"  {len(usage_idx)} usage rows")

    print("Parsing backend SDL…")
    registry = build_schema_registry()
    print(f"  {len(registry['types'])} types, {len(registry['enums'])} enums, "
          f"{len(registry['unions'])} unions, {len(registry['scalars'])} scalars")

    print("Loading backend story index…")
    be_stories = load_be_stories()
    print(f"  {sum(len(v) for v in be_stories.values())} BE story ↔ operation links")

    print("Cross-referencing…")
    ops, frags, coverage, fragments = cross_reference(client_defs, registry, usage_idx, be_stories)
    print(f"  {len(ops)} operations, {len(frags)} fragments, "
          f"{sum(1 for o in ops if any(r['phase1'] for r in o['roots']))} phase-1 operations")

    FE_OUT.mkdir(parents=True, exist_ok=True)
    emit_client_inventory(ops, frags, errors)
    emit_backend_inventory(registry, ops, coverage)
    emit_merged_inventory(ops, frags, registry, coverage)
    emit_domain_analysis(ops, frags, registry)

    stories = parse_fe_stories()
    fe_story_index = {}
    for s in stories:
        dom = domain_key_from_token(s["id"].rsplit("-FE-", 1)[0])
        for op in s["operations"]:
            fe_story_index[(dom, op)] = s["id"]
    emit_traceability(ops, fe_story_index)
    emit_dependency_matrix(stories)
    emit_jira(stories)

    # machine-readable master data
    data = {
        "generated": TODAY,
        "operations": [{k: v for k, v in o.items() if k != "selections"} for o in ops],
        "fragments": frags,
    }
    (FE_OUT / "frontend-inventory.json").write_text(
        json.dumps(data, indent=1, default=list), encoding="utf-8")
    print(f"  wrote {(FE_OUT / 'frontend-inventory.json').relative_to(ROOT)}")
    print("Done.")


if __name__ == "__main__":
    sys.exit(main())
