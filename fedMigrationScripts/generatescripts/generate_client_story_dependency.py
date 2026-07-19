#!/usr/bin/env python3
"""
Field-indexed client-story dependency reports — per query-bearing phase-1 FE story.

Replaces the hand-authored files that used to live at output/clientStoryDependency/
(see output/prompts/scripts/per-client-file-story-view.md for the original by-hand
prompt this automates). Everything below is derived from files already on disk —
this script invents no data, it only cross-references what the pipeline already
produced plus a small GraphQL-selection-set parser over the raw client `.txt` files.

Inputs (all relative to the migration repo root):
  output/analysis/program/frontend-inventory.json   Operation-level facts (root fields,
      BE story, fragments spread) — written by generate_frontend.py.
  output/analysis/program/fe-08-frontend-stories.md  The 23 FE stories: id, title,
      Operations line (query ops only are in scope; mutations are excluded/counted).
  ClientCallingGqlQueries/*.txt                      Raw client gql`...` sources — parsed
      here (brace-matching, not a full GraphQL AST) for the actual field names each
      operation selects, at least one level deep, resolving `...FragmentName` spreads
      by searching every file under ClientCallingGqlQueries/ for that fragment's body.
  output/analysis/<domain>/be-05-attribute-inventory.md  Table 1 (Attribute -> Story,
      "EXT (sev)" column) — the field -> story / field -> external-service source of truth.
  output/analysis/<domain>/be-04-stories.md          Full story text — validates story ids
      genuinely exist, and supplies SPIKE-0x gating context for the Notes column.

Outputs:
  output/clientStoryDependency/<FE_STORY_ID>.md               one per query-bearing FE story
  output/clientStoryDependency/00-NEWLY-IDENTIFIED-STORIES.md consolidated gap + external-dep register

Run (from anywhere — paths resolve relative to this script):
    python fedMigrationScripts/generatescripts/generate_client_story_dependency.py

⚠ Regeneration overwrites every file in output/clientStoryDependency/ — this folder has
  no hand-authored content anymore; re-run after any be-04-stories.md / be-05-attribute-
  inventory.md / fe-08-frontend-stories.md change.
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CLIENT_DIR = ROOT / "ClientCallingGqlQueries"
ANALYSIS = ROOT / "output" / "analysis"
FE_OUT = ANALYSIS / "program"
OUT_DIR = ROOT / "output" / "clientStoryDependency"

# ─── Domain catalogue (mirrors generate_frontend.py / generate_cross_domain_deps.py) ──
ALL_DOMAINS = [
    "bom", "claims", "impression", "measurement",
    "packaging", "product", "productDetails", "watchlist",
]
DOMAIN_FE_TOKEN = {
    "product": "PRODUCT", "bom": "BOM", "claims": "CLAIM",
    "measurement": "MST", "impression": "IMPRESSION",
    "productDetails": "PDTL", "packaging": "PKG", "watchlist": "WATCHLIST",
}
FE_TOKEN_DOMAIN = {v: k for k, v in DOMAIN_FE_TOKEN.items()}

# The 23 query-bearing phase-1 FE stories in scope, and — for the 3 "mixed"
# query+mutation stories — the explicit subset of QUERY operations to include
# (everything else on their Operations line is a mutation, excluded from the table
# but counted in "Mutations excluded"). Stories not listed here use every operation
# on their fe-08 Operations line that frontend-inventory.json marks kind == "query".
IN_SCOPE_STORIES = [
    "PRODUCT-FE-001", "PRODUCT-FE-002", "PRODUCT-FE-003", "PRODUCT-FE-004",
    "PRODUCT-FE-005", "PRODUCT-FE-006", "PRODUCT-FE-010", "PRODUCT-FE-011",
    "BOM-FE-002", "BOM-FE-003", "BOM-FE-004", "BOM-FE-005", "BOM-FE-007",
    "MST-FE-001", "MST-FE-002", "MST-FE-003",
    "PDTL-FE-001",
    "PKG-FE-001", "PKG-FE-002", "PKG-FE-003",
    "WATCHLIST-FE-001",
    "IMPRESSION-FE-001", "IMPRESSION-FE-002",
    "CLAIM-FE-002",
]

# Explicit query-op allowlist for the 3 mixed stories (per the program brief) —
# the rest of their fe-08 Operations line is mutations, excluded from the table.
MIXED_STORY_QUERY_OPS = {
    "PRODUCT-FE-006": {"getProductRules", "getProductRulesById", "getAllAvailableRules",
                        "getProductDeptRules", "getProductBPRules", "searchProductRules"},
    "PRODUCT-FE-011": {"getProduct"},
    "PKG-FE-003": {"getDielines", "getDielineEvaluationStatuses"},
}


# ─── FE stories (fe-08) ──────────────────────────────────────────────────────
FE_STORY_RE = re.compile(r'^### ([A-Z]+-FE-\d+)\s*·\s*(.+)$', re.M)


def load_fe_stories():
    """-> {fe_id: {"title": str, "operations": [str, ...]}}"""
    p = FE_OUT / "fe-08-frontend-stories.md"
    text = p.read_text(encoding="utf-8", errors="replace")
    matches = list(FE_STORY_RE.finditer(text))
    out = {}
    for i, m in enumerate(matches):
        sid, title = m.group(1), m.group(2).strip()
        body = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        ops_m = re.search(r'\*\*Operations:\*\*\s*([^\n]+)', body)
        ops = [x.strip().strip('`') for x in (ops_m.group(1).split(',') if ops_m else [])]
        out[sid] = {"title": title, "operations": [o for o in ops if o and o != "—"]}
    return out


# ─── frontend-inventory.json ─────────────────────────────────────────────────
def load_inventory():
    """-> (ops, by_op_name, by_root_field). Two SEPARATE indexes, not merged: an
    fe-08 Operations-line entry almost always names the GraphQL operation (op_name)
    and must match by op_name first — falling back to indexing by root-field name
    would wrongly conflate distinct operations that happen to share a root field
    (e.g. `getProductScaffolding`'s root field is also `getProduct`, but it is a
    different operation from `query getProduct(...)`). Root-field matching is only
    a fallback for the rare case where fe-08 names a root field directly instead of
    the operation (e.g. PRODUCT-FE-006 lists `getProductRulesById`, which is a root
    field of op `getProductRule` — no operation is itself NAMED `getProductRulesById`)."""
    import json
    p = FE_OUT / "frontend-inventory.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    ops = data["operations"]
    by_op_name = {}
    by_root_field = {}
    for o in ops:
        if o.get("op_name"):
            by_op_name.setdefault(o["op_name"], []).append(o)
        for r in o.get("roots", []):
            if r.get("field"):
                by_root_field.setdefault(r["field"], []).append(o)
    return ops, by_op_name, by_root_field


# ─── Raw client .txt selection-set parser ────────────────────────────────────
# Small brace-matching parser — not a full GraphQL AST. Finds `query NAME(...) { ... }`
# / `fragment NAME on TYPE { ... }` blocks inside gql`...` template literals, then scans
# the block body's TOP-LEVEL tokens only (brace-depth tracked) for field names / spreads,
# recursing one level into each field's own `{ ... }` sub-selection to capture immediate
# children (so `businessPartners { id name }` yields the field `businessPartners`, not
# each child separately, matching the level of granularity in the program brief).
GQL_TEMPLATE_RE = re.compile(r'gql\s*`')
GQL_CONST_NAME_RE = re.compile(
    r'(?:export\s+)?const\s+([A-Za-z0-9_]+)\s*(?::[^=]+)?=\s*'
    r'(?:(?:\([^)]*\)|[A-Za-z0-9_]+)\s*=>\s*)?gql\s*`', re.S)


def _extract_templates(text):
    """Yield raw text inside every gql`...` template literal in a file."""
    for m in GQL_TEMPLATE_RE.finditer(text):
        start = m.end()
        i = start
        while i < len(text):
            if text[i] == "\\":
                i += 2
                continue
            if text[i] == "`":
                break
            i += 1
        yield text[start:i]


def _extract_templates_with_const(text):
    """Yield (const_name_or_None, template_text) for every gql`...` in a file — the
    const name disambiguates multiple operations sharing one GraphQL operation name
    in the same file (e.g. `GET_PRODUCT` and `GET_PRODUCT_MINIMAL` both `query getProduct`)."""
    for m in GQL_CONST_NAME_RE.finditer(text):
        start = m.end()
        i = start
        while i < len(text):
            if text[i] == "\\":
                i += 2
                continue
            if text[i] == "`":
                break
            i += 1
        yield m.group(1), text[start:i]


OP_BLOCK_RE = re.compile(
    r'(query|mutation)\s+([A-Za-z0-9_]+)\s*(\([^)]*\))?\s*\{', re.S)
FRAGMENT_BLOCK_RE = re.compile(
    r'fragment\s+([A-Za-z0-9_]+)\s+on\s+([A-Za-z0-9_]+)\s*\{', re.S)


def _find_matching_brace(text, open_idx):
    """text[open_idx] == '{'; return index of its matching '}'."""
    depth = 0
    i = open_idx
    n = len(text)
    while i < n:
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return n - 1


TOP_TOKEN_RE = re.compile(
    r'\.\.\.\s*([A-Za-z0-9_]+)'                      # ...FragmentName
    r'|([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_]+)'          # alias: field
    r'|([A-Za-z0-9_]+)'                                # field
)


def _scan_top_level(body):
    """Scan a selection-set body's TOP-LEVEL tokens (brace-depth tracked so nested
    sub-selections are not treated as top-level). Returns
    [("spread", name), ("field", name, sub_body_or_None), ...]."""
    out = []
    i = 0
    n = len(body)
    depth = 0
    while i < n:
        c = body[i]
        if c == "{":
            depth += 1
            i += 1
            continue
        if c == "}":
            depth -= 1
            i += 1
            continue
        if depth != 0:
            i += 1
            continue
        if c in " \t\r\n,":
            i += 1
            continue
        if c == "#":  # line comment
            j = body.find("\n", i)
            i = n if j == -1 else j + 1
            continue
        if body.startswith("...", i):
            # inline fragment `... on TypeName { ... }` — NOT a named-fragment spread
            # (`...FragmentName`); must be checked first, or the `on` keyword gets
            # misparsed as if it were the spread's fragment name.
            im = re.match(r'\.\.\.\s*on\s+([A-Za-z0-9_]+)\s*\{', body[i:])
            if im:
                open_brace = i + im.end() - 1
                close = _find_matching_brace(body, open_brace)
                out.append(("inline", im.group(1), body[open_brace + 1:close]))
                i = close + 1
                continue
            m = re.match(r'\.\.\.\s*([A-Za-z0-9_]+)', body[i:])
            if m:
                out.append(("spread", m.group(1)))
                i += m.end()
                continue
        m = re.match(r'[A-Za-z0-9_]+', body[i:])
        if not m:
            i += 1
            continue
        name = m.group(0)
        i += m.end()
        # skip whitespace
        j = i
        while j < n and body[j] in " \t\r\n":
            j += 1
        # alias?
        if j < n and body[j] == ":":
            j += 1
            while j < n and body[j] in " \t\r\n":
                j += 1
            m2 = re.match(r'[A-Za-z0-9_]+', body[j:])
            if m2:
                name = m2.group(0)  # use the real field name, not the alias
                j += m2.end()
            i = j
        # skip arguments (...)
        while i < n and body[i] in " \t\r\n":
            i += 1
        if i < n and body[i] == "(":
            depth2 = 0
            k = i
            while k < n:
                if body[k] == "(":
                    depth2 += 1
                elif body[k] == ")":
                    depth2 -= 1
                    if depth2 == 0:
                        k += 1
                        break
                k += 1
            i = k
        while i < n and body[i] in " \t\r\n":
            i += 1
        # skip directives (@dir(args))
        while i < n and body[i] == "@":
            m3 = re.match(r'@[A-Za-z0-9_]+', body[i:])
            i += m3.end() if m3 else 1
            while i < n and body[i] in " \t\r\n":
                i += 1
            if i < n and body[i] == "(":
                depth2 = 0
                k = i
                while k < n:
                    if body[k] == "(":
                        depth2 += 1
                    elif body[k] == ")":
                        depth2 -= 1
                        if depth2 == 0:
                            k += 1
                            break
                    k += 1
                i = k
            while i < n and body[i] in " \t\r\n":
                i += 1
        sub = None
        if i < n and body[i] == "{":
            close = _find_matching_brace(body, i)
            sub = body[i + 1:close]
            i = close + 1
        out.append(("field", name, sub))
    return out


def _immediate_children(sub_body):
    """One level of child field names from a field's sub-selection (for context only —
    the row stays indexed by the parent field itself, not by each child)."""
    if sub_body is None:
        return []
    kids = []
    for tok in _scan_top_level(sub_body):
        if tok[0] == "field":
            kids.append(tok[1])
        elif tok[0] == "spread":
            kids.append("..." + tok[1])
    return kids


EXTERNAL_TYPE_PREFIX_RE = re.compile(r'^(VMM_|IG_|CORONA_|APEX_|NEXUS_|LDAP_|OBDP_|Doppler)')


def is_external_platform_type(type_name):
    """True for a GraphQL type that belongs to an external platform / later-phase
    subgraph rather than one of the 8 phase-1 domain schemas (which all use the
    SPARK_ prefix, or no prefix for shared value types) — VMM_BusinessPartner,
    IG_Department, etc. Mirrors the platform-prefix convention already used by
    generate_frontend.py's LATER_SCHEMA_LABEL table."""
    return bool(type_name) and bool(EXTERNAL_TYPE_PREFIX_RE.match(type_name))


class _FragmentIndex:
    """Global registry of fragment name -> raw body text, built once by scanning every
    ClientCallingGqlQueries/*.txt for `fragment NAME on TYPE { ... }` blocks — fragments
    are exported as JS consts and imported across files, but the GraphQL fragment name
    is unique program-wide, so a name-keyed global index avoids having to trace imports."""

    def __init__(self):
        self.bodies = {}   # name -> body text
        self.on_type = {}  # name -> GraphQL type the fragment is defined on
        for f in sorted(CLIENT_DIR.glob("*.txt")):
            text = f.read_text(encoding="utf-8", errors="replace")
            for tmpl in _extract_templates(text):
                for m in FRAGMENT_BLOCK_RE.finditer(tmpl):
                    name, on_type = m.group(1), m.group(2)
                    if name in self.bodies:
                        continue
                    close = _find_matching_brace(tmpl, m.end() - 1)
                    self.bodies[name] = tmpl[m.end():close]
                    self.on_type[name] = on_type

    def resolve(self, name):
        return self.bodies.get(name), self.on_type.get(name)


def collect_op_fields(txt_filename, op_name, frag_index, const=None, visited=None,
                       root_type=None):
    """Parse ClientCallingGqlQueries/<txt_filename> for the `query <op_name>(...) { ... }`
    (or `mutation`) block and return a list of row dicts:
      {"field": name, "children": [...], "via_fragment": fragment_name_or_None,
       "on_type": type_or_None, "resolved_container": container_type_or_None,
       "not_found_fragment": bool}
    Fragment spreads at the top level are resolved recursively (one hop per spread —
    a spread's OWN top-level tokens become rows too, tagged with which fragment they
    came through); a spread that also has a `{ ... }`-less bare presence with no
    definition anywhere is reported once as "fragment body not found in snapshot".

    IMPORTANT: a single file frequently defines SEVERAL operations with the SAME
    GraphQL operation name (e.g. `GET_PRODUCT` and `GET_PRODUCT_MINIMAL` both
    `query getProduct(...)`, selecting different fields). `const`, when given, pins
    the exact JS export to parse — op_name alone would silently always return only
    the FIRST such definition found in the file.

    `root_type` (optional, the operation's own root return type — e.g. `CodeDescription`
    for `getBomStatus`): threaded through the walk as `container_type`, updated only
    when descending into a fragment/inline spread (whose own `on TYPE` is known exactly
    from its definition). Every row records the container type it was found under as
    `resolved_container` — this is what a caller should key a type-scoped be-05 lookup
    on, NOT `on_type` (which keeps its separate, original meaning: the identity of an
    external-platform entity fragment, e.g. `VMM_BusinessPartner` — unrelated to this).
    Without `resolved_container`, a bare field name like `description` — declared on
    several unrelated types in the same domain (`CodeDescription`, `Status`,
    `BomMaterialSearchResult`, ...) — collides across all of them in a bare-name be-05
    lookup, misattributing one type's field-resolver story to a different type's
    same-named field. `resolved_container` is None when `root_type` wasn't given, or a
    fragment's own declared type couldn't be resolved — same as the old untyped
    behavior for that subtree, not a hard failure.
    """
    path = CLIENT_DIR / txt_filename
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    target_body = None
    if const:
        for cname, tmpl in _extract_templates_with_const(text):
            if cname != const:
                continue
            for m in OP_BLOCK_RE.finditer(tmpl):
                close = _find_matching_brace(tmpl, m.end() - 1)
                target_body = tmpl[m.end():close]
                break
            if target_body is not None:
                break
    if target_body is None:
        # fallback: first `query/mutation <op_name>` block anywhere in the file
        for tmpl in _extract_templates(text):
            for m in OP_BLOCK_RE.finditer(tmpl):
                kind, name = m.group(1), m.group(2)
                if name == op_name:
                    close = _find_matching_brace(tmpl, m.end() - 1)
                    # body of the ROOT selection set is one level in: the op's `{ ... }`
                    # wraps the root field(s) — but root fields themselves carry `{ ... }`
                    # sub-selections that are what we actually want to index. We treat
                    # the op block's top level as the "root fields" level, then descend
                    # one level into the (usually single) root field for real fields.
                    target_body = tmpl[m.end():close]
                    break
            if target_body is not None:
                break
    if target_body is None:
        return []

    rows = []
    seen_frag = set(visited or ())

    def walk(body, via_fragment, group, container, container_type):
        for tok in _scan_top_level(body):
            if tok[0] == "spread":
                fname = tok[1]
                if fname in seen_frag:
                    continue
                seen_frag.add(fname)
                fbody, on_type = frag_index.resolve(fname)
                if fbody is None:
                    rows.append({"field": fname, "children": [], "via_fragment": None,
                                 "on_type": None, "resolved_container": container_type,
                                 "not_found_fragment": True, "group": group,
                                 "container": container})
                    continue
                if is_external_platform_type(on_type):
                    # Cross-subgraph/external-platform fragment (VMM_*, IG_*, ...) —
                    # per the worked example this is indexed as its OWN row keyed by
                    # the `on` type itself (e.g. VMM_BusinessPartner), since resolving
                    # its full shape is a distinct (often not-yet-covered) concern from
                    # the flat id/name stub the parent field already resolves.
                    rows.append({"field": on_type, "children": _immediate_children(fbody),
                                 "via_fragment": fname, "on_type": on_type,
                                 "resolved_container": container_type,
                                 "not_found_fragment": False, "group": group,
                                 "container": container})
                else:
                    # Same-DGS / internal-shape fragment (SPARK_*, or any type native to
                    # this subgraph) — fold its OWN top-level selections directly into the
                    # parent context instead of manufacturing a synthetic "entity" row for
                    # a type that isn't actually a separate federation concern here. Stays
                    # in the SAME sibling group: once flattened these are semantically
                    # direct siblings of the fields around the spread. `container` is NOT
                    # changed by folding a fragment in — its fields are still children of
                    # the SAME enclosing field the spread itself sat inside. The fragment's
                    # OWN `on TYPE` (schema_target_type_name-normalized) becomes the new
                    # container_type for its fields — more reliable than whatever the
                    # enclosing field's schema-registry lookup guessed, since the fragment
                    # declares its type explicitly.
                    frag_type = schema_target_type_name(on_type) if on_type else container_type
                    walk(fbody, fname, group, container, frag_type)
            elif tok[0] == "inline":
                # `... on TypeName { ... }` inline fragment — NOT a named-fragment
                # spread. Same treatment as a same-domain named fragment (fold fields
                # into the current context) unless the inline-fragment's own type is a
                # genuinely external-platform entity, in which case it gets its own row
                # exactly like the named-fragment case above.
                _, inline_type, inline_body = tok
                if is_external_platform_type(inline_type):
                    rows.append({"field": inline_type, "children": _immediate_children(inline_body),
                                 "via_fragment": None, "on_type": inline_type,
                                 "resolved_container": container_type,
                                 "not_found_fragment": False, "group": group,
                                 "container": container})
                else:
                    walk(inline_body, via_fragment, group, container,
                         schema_target_type_name(inline_type) or container_type)
            else:
                _, name, sub = tok
                # `on_type` keeps its ORIGINAL meaning (identity of an external-entity
                # fragment row — set elsewhere, always None here). `resolved_container`
                # is new: the type THIS field is declared ON (e.g. `description` on
                # `CodeDescription`) — resolved from the schema registry using the
                # enclosing container_type threaded down through the walk, so a be-05
                # lookup can disambiguate same-named fields on different types (e.g.
                # `description` is declared on both `CodeDescription` and
                # `BomMaterialSearchResult` — without this, both collided on the bare
                # name and misattributed each other's story). None when the registry
                # doesn't know this container/field (unmapped type, or no schema_reg
                # given) — falls back to the old untyped behavior for that field.
                rows.append({"field": name, "children": _immediate_children(sub),
                             "via_fragment": via_fragment, "on_type": None,
                             "resolved_container": container_type,
                             "not_found_fragment": False, "group": group,
                             "container": container})

    # Descend into each root field's own selection set (the op body's top-level
    # tokens are the root field(s); their children are the real fields to index).
    # Each root field's body is its own sibling group — "siblings" means "selected
    # directly alongside each other under the same parent object", used only for the
    # narrow best-confidence fallback (see spike_gate_for_story / process_story) that
    # assigns a computed/derived field with no story of its own to whichever single
    # story already covers ALL of its siblings in the same selection.
    group_counter = [0]
    for tok in _scan_top_level(target_body):
        if tok[0] == "field" and tok[2] is not None:
            group_counter[0] += 1
            walk(tok[2], None, group_counter[0], tok[1], root_type)
        elif tok[0] == "spread":
            # (rare) a fragment spread directly under the op's root selection
            group_counter[0] += 1
            walk(target_body, None, group_counter[0], None, root_type)
            break
    return rows


# ─── be-05-attribute-inventory.md (field -> story, EXT source of truth) ──────
SHORT_STORY_RE = re.compile(r'^[A-Z]\d{1,3}[a-z]?$')


def full_story_id(domain, short):
    """'G01' + domain 'product' -> 'PRODUCT-BE-G-01'. Inserts a dash before the number
    if not already present; leaves an existing dash / trailing-letter suffix as-is."""
    token = DOMAIN_FE_TOKEN[domain]
    short = short.strip().strip("*").strip()
    m = re.match(r'^([A-Za-z]+)-?(\d+[a-z]?)$', short)
    if not m:
        return f"{token}-BE-{short}"
    letter, num = m.group(1), m.group(2)
    return f"{token}-BE-{letter}-{num}"


EXT_ICON_RE = re.compile(r'[\U0001F300-\U0001FAFF☀-➿]')


NON_EXTERNAL_MARKERS = {
    "acl", "accesscontrol", "context", "context-only", "same dgs", "internal",
    "n/a", "none",
}


def parse_ext_cell(cell):
    """'🔴 attachment + relationship' / '🟡 sampleV2 / 🔴 search' -> ['attachment',
    'relationship'] / ['sampleV2', 'search'] — strip icons, split on '/' or '+'.
    '— same DGS (only if `parentId` starts `PID`)' -> [] (internal field-resolver,
    not an external dependency — the leading em-dash/hyphen + parenthetical asides
    must both be stripped, not just a trailing "(...)")."""
    if not cell or cell.strip() in ("—", "-", ""):
        return []
    cleaned = EXT_ICON_RE.sub(" ", cell)
    cleaned = cleaned.replace("`", "")
    cleaned = re.sub(r'\([^)]*\)', ' ', cleaned)      # drop ALL parentheticals, any position
    cleaned = re.sub(r'^[\s—–-]+', '', cleaned)       # drop leading em-dash/hyphen marker
    parts = re.split(r'[/+]', cleaned)
    out = []
    for p in parts:
        p = p.strip(" —–-\t")
        if p and p.lower() not in NON_EXTERNAL_MARKERS:
            out.append(p)
    return out


# ─── be-03-schema.graphql (federated target SDL — plain-DTO-field fallback) ──
TYPE_HEADER_RE = re.compile(r'^type\s+([A-Za-z0-9_]+)\b([^{]*)\{', re.M)
SCHEMA_FIELD_LINE_RE = re.compile(
    r'(?:^|[\s{,])([A-Za-z_][A-Za-z0-9_]*)\s*(?:\([^)]*\))?\s*:\s*\[?([A-Za-z0-9_]+)', re.M)


def load_schema_registry(domain):
    """-> {"types": {type_name: {field_name: return_type_base}}, "external": set(type
    names carrying @extends — cross-subgraph stub types, NOT this domain's own shape)}.
    Parsed from the federated TARGET schema (be-03-schema.graphql, SPARK_ prefix already
    dropped) — used only as a last-resort fallback to distinguish "field is a plain
    same-shape DTO passthrough with no separate resolver" (covered by the root query's
    own story) from "field is itself a reference to an external/cross-subgraph entity"
    (a genuine resolver gap) when be-05/be-04 are silent on it."""
    p = ANALYSIS / domain / "be-03-schema.graphql"
    result = {"types": {}, "external": set()}
    if not p.exists():
        return result
    text = p.read_text(encoding="utf-8", errors="replace")
    for m in TYPE_HEADER_RE.finditer(text):
        tname, header_rest = m.group(1), m.group(2)
        close = _find_matching_brace(text, m.end() - 1)
        body = text[m.end():close]
        if "@extends" in header_rest:
            result["external"].add(tname)
        fields = {}
        for fm in SCHEMA_FIELD_LINE_RE.finditer(body):
            fname, ftype = fm.group(1), fm.group(2)
            fields[fname] = ftype
        result["types"].setdefault(tname, {}).update(fields)
    return result


def schema_target_type_name(sdl_source_type):
    """'SPARK_Product' -> 'Product' (federated target schema drops the SPARK_ prefix;
    non-SPARK-prefixed source types, e.g. later-phase/platform ones, pass through as-is)."""
    if not sdl_source_type:
        return None
    return sdl_source_type[len("SPARK_"):] if sdl_source_type.startswith("SPARK_") else sdl_source_type


def schema_covers_as_plain_field(schema_reg, container_type, field_name):
    """True if `field_name` is declared directly on `container_type` in the federated
    target schema AND its return type is NOT itself a genuinely EXTERNAL-PLATFORM
    entity reference (VMM_/IG_/CORONA_/APEX_/... — see is_external_platform_type) —
    i.e. a plain, same-shape DTO field the root story's own resolver already returns,
    never individually named in be-05's illustrative pass-through list. Returns
    (covered: bool, is_external_ref: bool) so callers can tell "definitely plain" from
    "declared, but itself an external-entity reference" (still a real resolver gap).

    Deliberately does NOT treat every `@extends`-stubbed type in THIS domain's local
    schema file as external — `@extends` also appears on genuinely shared/`@shareable`
    value types owned by ANOTHER phase-1 domain in the SAME gateway (e.g.
    `ProductComponentStatus` is `@shareable`, duplicated across subgraphs per
    federation-review R5 — it is not a cross-team platform entity needing its own
    `@DgsEntityFetcher` story). Only the platform-prefix convention is a reliable
    "genuinely external, needs its own entity-fetcher story" signal; a same-gateway
    stub with no such prefix is still a plain field as far as THIS story is concerned."""
    fields = schema_reg["types"].get(container_type)
    if not fields or field_name not in fields:
        return False, False
    return_type = fields[field_name]
    is_ext = is_external_platform_type(return_type)
    return (not is_ext), is_ext


def load_be05(domain):
    """-> {"fields": {field_name: {"story": full_id, "ext": [service,...]}},
           "by_type_field": {(container_type, field_name): {"story":..., "ext":...}} —
               type-qualified index, checked BEFORE the bare-name "fields" dict so two
               different types' same-named field (e.g. `description` on both
               `CodeDescription` and `BomMaterialSearchResult`) never collide,
           "field_types": {field_name: {container_type, ...}} — every type this domain's
               be-05 documents a row for under this bare field name; used to tell "no
               be-05 row anywhere names this exact (type, field)" (safe to fall through
               to the bare-name dict — there's truly only one candidate) apart from "a
               DIFFERENT type has a row for this field name, but not the one we're
               actually looking at" (NOT safe to fall through — that's the collision),
           "bundle_fields": set(field_name for trivial pass-throughs),
           "bundle_stories": [full_id, ...]}"""
    p = ANALYSIS / domain / "be-05-attribute-inventory.md"
    result = {"fields": {}, "by_type_field": {}, "field_types": {}, "bundle_fields": set(),
               "bundle_prefixes": set(), "bundle_stories": [], "catch_all_scalars": False}
    if not p.exists():
        return result
    text = p.read_text(encoding="utf-8", errors="replace")

    # Table 1 rows: header/column layout varies by domain — some have a leading "Type"
    # column (bom/claims/impression/measurement/productDetails/watchlist: "| Type |
    # Attribute | GraphQL Type | Resolution | [Resolver Loc |] EXT (sev) | Complexity |
    # Story |"), others don't (product/packaging: "| Attribute | GraphQL Type |
    # Resolution | EXT (sev) | Complexity | Story |"). Detect columns BY HEADER NAME,
    # never by fixed position — a positional guess (e.g. "cells[0] if it has a
    # backtick") silently grabs the Type column instead of Attribute on tables that
    # have one, which was silently swallowing every EXT/story mapping on those domains.
    header_idx = text.find("## Table 1")
    table2_idx = text.find("## Table 2")
    section = text[header_idx:table2_idx] if header_idx != -1 else text
    col_idx = None  # {"attribute": i, "ext": i, "story": i}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # header row detection: exactly the column-name cells, no data (no backticks,
        # matches known header labels)
        lowered = [c.lower() for c in cells]
        if col_idx is None:
            if any("attribute" in c for c in lowered) and any("story" in c for c in lowered):
                idx = {}
                for i, c in enumerate(lowered):
                    if c == "type":
                        idx["type"] = i
                    elif c == "attribute":
                        idx["attribute"] = i
                    elif c.startswith("ext"):
                        idx["ext"] = i
                    elif c == "story":
                        idx["story"] = i
                    elif c == "resolution":
                        idx["resolution"] = i
                if "attribute" in idx and "story" in idx:
                    col_idx = idx
            continue
        if set(cells) <= {"", "-"} or all(re.match(r'^:?-+:?$', c or "-") for c in cells):
            continue  # markdown separator row (---|---|---)
        if len(cells) <= max(col_idx.values()):
            continue
        story_cell = cells[col_idx["story"]]
        if not SHORT_STORY_RE.match(story_cell.strip("`* ")):
            continue  # not a data row (e.g. wrapped continuation line)
        attr_cell = cells[col_idx["attribute"]]
        attrs = re.findall(r'`([^`]+)`', attr_cell)
        if not attrs:
            continue
        ext_cell = cells[col_idx["ext"]] if "ext" in col_idx else ""
        ext_services = parse_ext_cell(ext_cell)
        sid = full_story_id(domain, story_cell.strip("`* "))
        # a table with a separate leading "Type" column names the container type this
        # row's Attribute belongs to (bom/claims/impression/measurement/productDetails/
        # watchlist's layout) — capture it so same-named fields on DIFFERENT types (e.g.
        # `description` on both `CodeDescription` and `BomMaterialSearchResult`) don't
        # collide in the bare-name index below.
        type_cell = cells[col_idx["type"]] if "type" in col_idx else ""
        type_names = re.findall(r'`([^`]+)`', type_cell)
        row_type = type_names[0] if len(type_names) == 1 else None
        for a in attrs:
            # attribute may be 'Type.field' or 'field' — index by the bare field name
            field = a.rsplit(".", 1)[-1]
            entry = {"story": sid, "ext": ext_services}
            result["fields"][field] = entry
            result["fields"][a] = entry
            known_type = row_type or (a.rsplit(".", 1)[0] if "." in a else None)
            if known_type:
                result["by_type_field"][(known_type, field)] = entry
                result["field_types"].setdefault(field, set()).add(known_type)

    # "Direct/Computed pass-throughs (...)" bundle line(s) + "Bundled into **Gxx**" /
    # "Covered by A02 + B01" trailer within the next ~2 lines.
    for m in re.finditer(
            r'(?:Direct(?:/Computed)?|Trivial scalar) pass-throughs[^\n]*:\*\*([\s\S]{0,900}?)(?=\n\n|\Z)',
            section):
        chunk = m.group(0)
        fields = re.findall(r'`([^`]+)`', chunk)
        for grp in fields:
            for piece in re.split(r'[,\n]', grp):
                piece = piece.strip()
                # markdown soft-wraps some backtick-quoted spans onto a new line with a
                # leading '- ' list marker (e.g. "...internalNotes,\n- vendorStyleNumber,
                # ...") — that '-' is a rendering artifact, not part of the field name.
                piece = re.sub(r'^-\s*', '', piece).strip()
                # unwrap 'Type.{a, b}' / 'Type.a' forms down to bare names
                piece = re.sub(r'^[A-Za-z0-9_]+\.\{?', '', piece).rstrip("}").strip()
                # 'projectType(+Name)' -> also covers the companion 'projectTypeName'
                # field (packaging's convention for a code/name pair sharing one
                # resolver); 'warningsAndCautions(+List)' likewise -> ...List.
                companion_m = re.match(r'^([A-Za-z][A-Za-z0-9_]*)\(\+([A-Za-z][A-Za-z0-9_]*)\)$', piece)
                if companion_m:
                    result["bundle_fields"].add(companion_m.group(1))
                    result["bundle_fields"].add(companion_m.group(1) + companion_m.group(2))
                    continue
                if piece.endswith("*"):
                    # wildcard prefix (e.g. `presentation*` covers presentationDepth,
                    # presentationWidth, ...) — keep the '*' as a sentinel marker.
                    prefix = piece[:-1].strip()
                    if re.match(r'^[A-Za-z][A-Za-z0-9_]*$', prefix):
                        result["bundle_prefixes"].add(prefix)
                    continue
                if re.match(r'^[A-Za-z][A-Za-z0-9_]*$', piece):
                    result["bundle_fields"].add(piece)
        story_refs = re.findall(r'\*\*([A-Z]\d{1,3}[a-z]?)\*\*', chunk)
        story_refs += re.findall(r'(?:Covered by|Bundled into)\s+([A-Z]\d{1,3}(?:\s*\+\s*[A-Z]\d{1,3})*)', chunk)
        for ref in story_refs:
            for single in re.split(r'\s*\+\s*', ref):
                single = single.strip()
                if SHORT_STORY_RE.match(single):
                    sid = full_story_id(domain, single)
                    if sid not in result["bundle_stories"]:
                        result["bundle_stories"].append(sid)
        if re.search(r'all value-type scalar fields|all\s+DTO-mapped|plus all\b', chunk, re.I):
            result["catch_all_scalars"] = True
    return result


SCALAR_ID_SUFFIX_RE = re.compile(r'(Id|Ids|Count|Name|At|By|Number|Type|Depth|Width|Height|'
                                  r'Dimensions|Cost|Notes|Version)$')


def bundle_covers(be05, field):
    """True if `field` is covered by the domain's trivial-scalar pass-through bundle —
    exact name, a `prefix*` wildcard match, or (only when the doc explicitly says
    'plus all value-type scalar fields') a plain scalar-shaped name we have no
    stronger signal for. The catch-all is intentionally narrow (simple
    camelCase-looking identifiers only) — never used to swallow an entity/fragment row."""
    if field in be05["bundle_fields"]:
        return True
    if any(field.startswith(pfx) for pfx in be05["bundle_prefixes"]):
        return True
    return False


# ─── be-04-stories.md (story existence + SPIKE gating) ───────────────────────
BE_STORY_HEADER_RE = re.compile(r"^### ([A-Z][A-Za-z0-9]*-BE-[A-Za-z0-9-]+)\s*·\s*(.+)$", re.M)
SPIKE_RE = re.compile(r'SPIKE-0\d[a-z]?')
DEPENDS_ON_RE = re.compile(r'\*\*Depends on:\*\*\s*([^·\n]+)')
SHORT_ID_RE = re.compile(r'\b([A-Z]-\d+[a-z]?)\b')
# "`S-02` (... program id `SPIKE-06a`" / "`S-03` spike (run first, program id `SPIKE-03`" —
# the short spike-story id and its assigned program SPIKE-0x id, however the prose orders them.
SPIKE_PROGRAM_ID_RE = re.compile(
    r'`(S-\d+[a-z]?)`[^`]{0,80}?program id `(SPIKE-0\d[a-z]?)`'
    r'|program id `(SPIKE-0\d[a-z]?)`[^`]{0,80}?`(S-\d+[a-z]?)`', re.S)


TITLE_FIELD_TOKEN_RE = re.compile(r'`([A-Za-z_][A-Za-z0-9_.]*)`')


def _parse_title_fields(title):
    """'`Product.vendorAttributes` + `businessPartners` + `droppedPartners`' -> {
    'vendorAttributes', 'businessPartners', 'droppedPartners'} — later `+`-joined
    tokens that omit their own `Type.` prefix belong to the same header title, so
    both the bare name AND (if a Type prefix appears anywhere in the title) the
    qualified name are indexed. This is a fallback cross-check alongside be-05's
    Attribute column and the schema DTO check — a story's title sometimes names a
    field (e.g. `status` in PRODUCT-BE-G-07's title) that be-05's own row text
    happens to also carry, but titles are the more authoritative single source for
    "which fields does this multi-field story cover" when in doubt."""
    names = set()
    for tok in TITLE_FIELD_TOKEN_RE.findall(title):
        bare = tok.rsplit(".", 1)[-1]
        names.add(bare)
        names.add(tok)
    return names


def load_be04(domain):
    """-> {"ids": set(full story ids that really exist), "bodies": {id: body_text},
           "types": {id: "Spike"/"Query"/...}, "depends": {id: [short_id, ...]},
           "spike_program_id": {"S-02": "SPIKE-06a", ...} (domain-wide preamble map),
           "title_field_index": {field_name: story_id} built from every story header's
           own `+`-joined field-name title, first-story-wins on a field-name collision}"""
    p = ANALYSIS / domain / "be-04-stories.md"
    out = {"ids": set(), "bodies": {}, "types": {}, "depends": {}, "spike_program_id": {},
           "title_field_index": {}}
    if not p.exists():
        return out
    text = p.read_text(encoding="utf-8", errors="replace")
    for m in SPIKE_PROGRAM_ID_RE.finditer(text):
        s_id = m.group(1) or m.group(4)
        prog_id = m.group(2) or m.group(3)
        if s_id:
            out["spike_program_id"][s_id] = prog_id
    matches = list(BE_STORY_HEADER_RE.finditer(text))
    for i, m in enumerate(matches):
        sid, title = m.group(1), m.group(2)
        body = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        out["ids"].add(sid)
        out["bodies"][sid] = title + "\n" + body
        tm = re.search(r'\*\*Type:\*\*\s*([^·\n]+)', body)
        out["types"][sid] = tm.group(1).strip() if tm else ""
        dm = DEPENDS_ON_RE.search(body)
        deps = SHORT_ID_RE.findall(dm.group(1)) if dm else []
        out["depends"][sid] = deps
        for fname in _parse_title_fields(title):
            out["title_field_index"].setdefault(fname, sid)
    return out


def field_in_be04_title(field, be04):
    """First-priority-after-be05 lookup: does any story's OWN header title name this
    field (bare or Type-qualified)? Catches multi-field stories whose title lists a
    field not repeated verbatim in be-05's Attribute column (e.g. PRODUCT-BE-G-07's
    title includes `status` alongside the partner fields)."""
    return be04["title_field_index"].get(field)


def field_in_be04_prose(field, be04):
    """grep for the field name anywhere in be-04-stories.md prose -> the story id whose
    body contains it (first match), or None."""
    needle = field
    for sid, body in be04["bodies"].items():
        if re.search(rf'`{re.escape(needle)}`', body) or re.search(rf'\b{re.escape(needle)}\b', body):
            return sid
    return None


def _short_to_full(domain, short_id):
    return full_story_id(domain, short_id) if SHORT_STORY_RE.match(short_id) else None


def spike_gate_for_story(domain, story_id, be04, field=None):
    """Returns a Notes-ready string (or None) describing any spike/draft-ADR gate on
    `story_id` — covers BOTH styles seen across domains:
      1) story_id's own body mentions a literal SPIKE-0x directly (e.g. PRODUCT-BE-G-07's
         prose on `unDroppablePartners`/SPIKE-04) — field-proximate when `field` given.
      2) story_id's **Depends on:** line names a short `S-0x` id that is itself a Spike-
         type story not yet resolved — resolved to that domain's program SPIKE-0x id via
         the preamble map when one is registered, else the bare spike-story id.
    Distinguishes a soft gate (a documented safe default exists — the story ships without
    waiting on the spike's timeline) from a hard block (no safe default / explicit
    "pending ratification" language), based on the story's own text.
    """
    body = be04["bodies"].get(story_id, "")
    if not body:
        return None

    def _hardness(window):
        if re.search(r'safe default|isn.t blocked on the spike', window, re.I):
            return "safe default exists — not a hard block"
        if re.search(r'hard block|pending ratification|cannot be ported|must be settled', window, re.I):
            return "hard blocker — pending resolution"
        return "gated"

    # style 1: literal SPIKE-0x in this story's own body
    direct = list(SPIKE_RE.finditer(body))
    if direct:
        for m in direct:
            window = body[max(0, m.start() - 350):m.end() + 350]
            if field is None or re.search(rf'\b{re.escape(field)}\b', window):
                return f"🔬 {m.group(0)} ({_hardness(window)})"
        m = direct[0]
        window = body[max(0, m.start() - 350):m.end() + 350]
        return f"🔬 {m.group(0)} ({_hardness(window)})"

    # style 2: Depends on: names an unresolved Spike-type story
    for short in be04["depends"].get(story_id, []):
        target_full = _short_to_full(domain, short)
        target_type = be04["types"].get(target_full, "")
        if "spike" not in target_type.lower():
            continue
        prog_id = be04["spike_program_id"].get(short)
        label = prog_id if prog_id else target_full
        return f"🔬 {label} via {story_id} ({_hardness(body)})"
    return None


# ─── Gap classification ──────────────────────────────────────────────────────
def guess_gap_phase(field, on_type, is_root):
    if is_root:
        return "B"
    if on_type and re.match(r'^[A-Z]+_[A-Za-z]', on_type):
        # external-platform-shaped type (VMM_*, IG_*, CORONA_* convention) with no
        # entity-fetcher story anywhere -> H-phase cross-subgraph gap.
        return "H"
    return "G"


# ─── External-dependency gap -> real authored story (output/analysis/program/
# ext-dependency-stories.md) ──────────────────────────────────────────────────
STORY_HEADER_NUM_RE = re.compile(r"^### ([A-Z]+)-BE-([A-Z])-(\d+)[a-z]?\s*·", re.M)


class ExtAuthoring:
    """Authors a REAL story id (never a NEW-...-?? placeholder) for every genuinely
    new AND externally-owned gap found while processing the 23 FE stories, collecting
    them into ONE program-wide file (the resolution is fundamentally about an external
    entity/service, not domain business logic, so one file serves all 8 domains).
    Dedupes by (domain, field, external type/service) so the SAME gap surfacing from
    multiple FE stories reuses one authored story instead of minting duplicates."""

    def __init__(self, be04_cache):
        self._be04_cache = be04_cache
        self._next_num = {}          # (domain, phase_letter) -> next available number
        self._authored = {}          # (domain, field, ext) -> {"id":, "blocks": set(), ...}
        self._order = []             # authoring order, for stable output
        self._seed_existing_numbers()

    def _seed_existing_numbers(self):
        for dom in ALL_DOMAINS:
            p = ANALYSIS / dom / "be-04-stories.md"
            token = DOMAIN_FE_TOKEN[dom]
            if p.exists():
                text = p.read_text(encoding="utf-8", errors="replace")
                for m in STORY_HEADER_NUM_RE.finditer(text):
                    if m.group(1) != token:
                        continue
                    key = (dom, m.group(2))
                    self._next_num[key] = max(self._next_num.get(key, 0), int(m.group(3)))

    def _next_id(self, domain, phase_letter):
        key = (domain, phase_letter)
        n = self._next_num.get(key, 0) + 1
        self._next_num[key] = n
        return f"{DOMAIN_FE_TOKEN[domain]}-BE-{phase_letter}-{n:02d}"

    def author(self, domain, field, ext_type_or_service, fe_id):
        """-> (story_id, service_label). Idempotent per (domain, field, ext)."""
        dedupe_key = (domain, field, ext_type_or_service)
        if dedupe_key in self._authored:
            entry = self._authored[dedupe_key]
            entry["blocks"].add(fe_id)
            return entry["id"], entry["service"]

        is_entity_ref = is_external_platform_type(ext_type_or_service)
        phase = "H" if is_entity_ref else "G"
        story_id = self._next_id(domain, phase)
        service = ext_type_or_service if is_entity_ref else ext_type_or_service
        service_label = ext_type_or_service.lower() if not is_entity_ref else \
            ext_type_or_service.split("_")[0].lower()
        entry = {"id": story_id, "field": field, "domain": domain, "ext": ext_type_or_service,
                 "service": service_label, "is_entity_ref": is_entity_ref,
                 "blocks": {fe_id}}
        self._authored[dedupe_key] = entry
        self._order.append(dedupe_key)
        return story_id, service_label

    def render(self):
        """Full be-04-story-formatted markdown block for every authored story, in
        authoring order — appended into output/analysis/program/ext-dependency-stories.md."""
        if not self._order:
            return None
        L = [
            "# Externally-Owned Field/Entity Gaps — Newly Authored Backend Stories",
            "",
            "> Auto-generated by generate_client_story_dependency.py. Every story below "
            "resolves a field/entity that (a) has no covering story anywhere in its "
            "domain's be-04-stories.md, and (b) depends on a service/entity owned by a "
            "different team (VMM/IG/CORONA/APEX/materialHub/attachment/discussion/sample/"
            "relationship/user-group/workspaceV2/search/etc.) — a genuine cross-team "
            "dependency, not domain-internal business logic. These ARE real story ids "
            "(same `<DOMAIN>-BE-<phase>-<NN>` numbering as be-04-stories.md, continuing "
            "from the highest existing number in that domain+phase) — ready to fold into "
            "the domain's own be-04-stories.md and push to Jira. Regenerate after any "
            "be-04-stories.md / be-05-attribute-inventory.md change (re-run may renumber "
            "if earlier gaps are resolved by then — reconcile before re-pushing to Jira).",
            "",
            "---",
            "",
        ]
        for key in self._order:
            e = self._authored[key]
            sid, field, dom, ext = e["id"], e["field"], e["domain"], e["ext"]
            blocks = ", ".join(sorted(e["blocks"]))
            if e["is_entity_ref"]:
                title = f"`{ext}` entity fetcher (`@DgsEntityFetcher`) for cross-subgraph references"
                plain_terms = (f"Lets `plm-product`'s own queries — and any other subgraph "
                                f"referencing a `{ext}` — resolve the field `{field}`, which "
                                f"selects this externally-owned entity's full shape.")
                context = (f"Identified via `output/clientStoryDependency/` field-by-field "
                           f"drill-down: `{field}` (domain `{dom}`) selects `{ext}` — an "
                           f"external-platform entity (`{ext}` is `@extends`-stubbed in the "
                           f"federated target schema, `{dom}/be-03-schema.graphql`) — but no "
                           f"story anywhere resolves its full shape; today it silently "
                           f"resolves to a bare `{{id}}` key stub. Blocks: {blocks}.")
                impl = (f"`@DgsEntityFetcher(name = \"{ext}\")` -> the owning service's client, "
                       f"behind a `DataLoader` (batched, one call per request not per "
                       f"representation); null-tolerant per federation spec.")
                files = f"`{ext}EntityFetcher.kt`."
            else:
                title = f"`{field}` field resolver ({ext} external dependency)"
                plain_terms = (f"Resolve the `{field}` field, which depends on the "
                                f"externally-owned `{ext}` service.")
                context = (f"Identified via `output/clientStoryDependency/` field-by-field "
                           f"drill-down: `{field}` (domain `{dom}`) is selected by the "
                           f"frontend but has no covering story in be-04-stories.md or "
                           f"be-05-attribute-inventory.md, and its resolution depends on "
                           f"the `{ext}` service (owned by a different team, not domain-"
                           f"internal logic). Blocks: {blocks}.")
                impl = (f"Thin `@DgsData` field resolver -> the existing `{ext}` client "
                       f"(reuse the port already established by this domain's other `{ext}` "
                       f"stories, if any), behind a `DataLoader` where batching applies.")
                files = "TBD — pending confirmation of the existing `{}` client port.".format(ext)
            L += [
                f"### {sid} · {title}",
                f"- **Type:** Field Resolver · **Phase:** {'H' if e['is_entity_ref'] else 'G'} "
                f"· **Complexity:** Medium · **Category:** CAT-3 · **Depends on:** — "
                f"· **EXT:** 🔵 `{e['service']}`",
                "",
                f"- **In plain terms:** {plain_terms}",
                "",
                f"- **Context (identified via `output/clientStoryDependency/` field-by-field "
                f"drill-down):** {context}",
                f"- **Target DGS Implementation:** {impl}",
                f"- **Files / Dependencies:** {files}",
                "",
                "#### Acceptance Criteria",
                "",
                "1. The field resolves the externally-owned shape end-to-end for every "
                "operation listed above, not just a bare id stub.",
                "2. Unknown/missing upstream ids yield `null` without failing the whole response.",
                "3. No ACL plumbing introduced beyond what the domain's other stories already carry.",
                "",
                "---",
                "",
            ]
        return "\n".join(L)


# ─── Sibling-confidence-match AC editor — appends a concrete Acceptance Criterion
# directly into output/analysis/<domain>/be-04-stories.md for the narrow case where a
# field is confidently assigned to an existing story (all its siblings already resolve
# there) but isn't individually named in that story's title/be-05 row/schema check ──
AC_BLOCK_RE_CACHE = {}


class ACEditor:
    """Queues (domain, story_id, field, fe_id) during processing; applies every queued
    edit ONCE at the end of the run (dedup'd per story+field) by appending one new
    numbered Acceptance Criteria item to that story's existing `#### Acceptance
    Criteria` list in its domain's be-04-stories.md. Never touches anything else in
    the file — only inserts a new list item immediately after the last existing one,
    before the story's closing `---` separator."""

    def __init__(self):
        self._queue = {}   # (domain, story_id) -> {field: set(fe_ids)}
        self.applied = []  # [(domain, story_id, field, path)] — for the run report

    def queue(self, domain, story_id, field, fe_id):
        key = (domain, story_id)
        self._queue.setdefault(key, {}).setdefault(field, set()).add(fe_id)

    def apply_all(self):
        for (domain, story_id), fields in self._queue.items():
            path = ANALYSIS / domain / "be-04-stories.md"
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            header_m = re.search(rf"^### {re.escape(story_id)}\s*·", text, re.M)
            if not header_m:
                continue
            next_header_m = BE_STORY_HEADER_RE.search(text, header_m.end())
            story_end = next_header_m.start() if next_header_m else len(text)
            story_text = text[header_m.start():story_end]
            ac_m = re.search(r"#### Acceptance Criteria\n\n((?:\d+\..*\n?)+)", story_text)
            if not ac_m:
                continue  # no AC block to append to — leave the story untouched
            existing_items = ac_m.group(1)
            last_num_m = list(re.finditer(r"^(\d+)\.", existing_items, re.M))
            next_num = int(last_num_m[-1].group(1)) + 1 if last_num_m else 1
            new_lines = []
            for field in sorted(fields):
                new_lines.append(f"{next_num}. `{field}` resolves correctly as a "
                                  f"derived/computed value from this story's other fields.")
                next_num += 1
                self.applied.append((domain, story_id, field,
                                      str(path.relative_to(ROOT))))
            insertion = existing_items.rstrip("\n") + "\n" + "\n".join(new_lines) + "\n"
            new_story_text = (story_text[:ac_m.start(1)] + insertion
                               + story_text[ac_m.end(1):])
            text = text[:header_m.start()] + new_story_text + text[story_end:]
            path.write_text(text, encoding="utf-8")


# ─── Per-story processing ────────────────────────────────────────────────────
def md_escape(s):
    return (s or "").replace("|", "\\|")


def process_story(fe_id, fe_meta, by_op_name, by_root_field, frag_index, be05_cache, be04_cache,
                   schema_cache, ext_authoring, ac_editor):
    token = fe_id.rsplit("-FE-", 1)[0]
    domain_default = FE_TOKEN_DOMAIN.get(token)
    all_ops = fe_meta["operations"]
    allow = MIXED_STORY_QUERY_OPS.get(fe_id)

    # A named operation in fe-08's Operations line (e.g. `getProduct`) is frequently
    # DEFINED MULTIPLE TIMES — same GraphQL operation name, different `const`/file,
    # different (often wider or narrower) selection set (e.g. GET_PRODUCT vs
    # GET_PRODUCT_WITH_META_DATA vs GET_PRODUCT_MINIMAL, all `query getProduct`).
    # We must fold the fields from EVERY such definition into the table, or fields
    # unique to one document silently vanish. "Impacts (queries)" still reports by
    # the shared operation NAME (matching "Queries in scope"), not by const.
    query_ops = []      # [(display_name, [op_record, ...])]
    mutation_count = 0
    seen_names = set()
    for name in all_ops:
        if name in seen_names:
            continue
        seen_names.add(name)
        # Prefer an exact operation-name match; only fall back to root-field matching
        # when no operation anywhere is actually NAMED `name` (see load_inventory()).
        recs = by_op_name.get(name) or by_root_field.get(name, [])
        if allow is not None and name not in allow:
            mutation_count += 1
            continue
        q_recs = [r for r in recs if r["kind"] == "query"]
        if not q_recs:
            m_recs = [r for r in recs if r["kind"] == "mutation"]
            if m_recs:
                mutation_count += 1
            # else: not found in inventory at all — nothing to fold in, skip silently
            continue
        # Dedupe by (txt file, const) — NOT bare const alone: the same JS const NAME
        # can be independently defined in two different files (e.g. GET_UNITS_OF_MEASURE
        # exists in both `product-common/MeasurementQueries` (in-scope, measurement
        # domain) and `spark-materials-hub-graphql/BaseMaterialQueries` (out-of-scope,
        # later-phase domain) — a bare-const dict would silently drop one of them.
        # Only keep records whose root actually resolves to THIS story's own domain
        # (or an unmapped/no-domain root, which still needs folding in) — a same-named
        # operation belonging to a different, out-of-scope domain is not this story's
        # concern even though it shares an operation name string.
        by_const = {}
        for r in q_recs:
            if not any(rt.get("phase1") for rt in r.get("roots", [])):
                continue  # this definition of the shared op-name resolves to a
                          # later-phase/out-of-scope domain — not what this FE story means
            by_const[(r["txt"], r["const"])] = r
        if not by_const:
            # no phase-1 definition of this name at all (shouldn't normally happen for
            # an in-scope FE story, but stay tolerant rather than crash)
            by_const = {(r["txt"], r["const"]): r for r in q_recs}
        query_ops.append((name, list(by_const.values())))

    if not query_ops:
        return None  # nothing to emit — pure mutation / cross-cutting story

    # rows keyed by (field name, on_type) so an entity-fragment row (e.g.
    # VMM_BusinessPartner) doesn't collide with a plain scalar field of the same name.
    rows = {}   # key -> {"field","story","ext","new","impacts": set(op_name...), "notes"}
    domains_touched = set()

    for op_display_name, recs in query_ops:
        for rec in recs:
            dom = rec.get("primary_domain") or domain_default
            if dom:
                domains_touched.add(dom)
            op_dom = dom or domain_default
            be05 = be05_cache.setdefault(op_dom, load_be05(op_dom)) if op_dom else {
                "fields": {}, "by_type_field": {}, "field_types": {}, "bundle_fields": set(),
                "bundle_prefixes": set(), "bundle_stories": [], "catch_all_scalars": False}
            be04 = be04_cache.setdefault(op_dom, load_be04(op_dom)) if op_dom else {
                "ids": set(), "bodies": {}, "types": {}, "depends": {}, "spike_program_id": {}}
            schema_reg = schema_cache.setdefault(op_dom, load_schema_registry(op_dom)) if op_dom else {"types": {}, "external": set()}
            # container type this operation's root resolves to (federated target name,
            # SPARK_ prefix dropped) — used as the fallback "is this a plain DTO field
            # on the root's own type" check before ever declaring a field a gap.
            root_container_types = [schema_target_type_name(r.get("return_type"))
                                     for r in rec.get("roots", []) if r.get("phase1")]

            # 1) root field(s) themselves are rows too (be_story already known from the JSON).
            for r in rec.get("roots", []):
                if not r.get("phase1"):
                    continue
                key = (r["field"], None)
                row = rows.setdefault(key, {"field": r["field"], "story": None, "ext": [],
                                             "new": False, "impacts": set(), "notes": set(),
                                             "on_type": None, "is_query": True})
                row["impacts"].add(op_display_name)
                if r.get("be_story"):
                    row["story"] = r["be_story"]
                    row["new"] = False   # a later operation's root resolved what an
                                          # earlier one on the same key couldn't — the
                                          # field IS covered; never leave a stale New=Yes.
                elif not row["story"]:
                    row["story"] = f"NEW-{DOMAIN_FE_TOKEN.get(r['domain'], (r['domain'] or '?').upper())}-BE-B-??"
                    row["new"] = True
                if row["story"] and not row["story"].startswith("NEW-"):
                    gate = spike_gate_for_story(op_dom, row["story"], be04, field=r["field"])
                    if gate:
                        row["notes"].add(gate)

            # 2) fields inside the selection set, parsed from the raw client .txt.
            # root_type: pass this operation's OWN root return type (when there's
            # exactly one root, which is the common case) so collect_op_fields can
            # thread real container types through the walk instead of leaving every
            # plain field's container unresolved.
            op_root_type = root_container_types[0] if len(root_container_types) == 1 else None
            field_rows = collect_op_fields(rec["txt"], rec["op_name"], frag_index,
                                            const=rec.get("const"), root_type=op_root_type)
            for fr in field_rows:
                fname = fr["field"]
                if fname == "__typename":
                    continue  # universal GraphQL introspection meta-field — resolved by
                               # the engine itself, never a story; never a gap.
                on_type = fr.get("on_type")
                key = (fname, on_type)
                row = rows.setdefault(key, {"field": fname, "story": None, "ext": [],
                                             "new": False, "impacts": set(), "notes": set(),
                                             "on_type": on_type, "is_query": False})
                row["impacts"].add(op_display_name)
                if fr.get("via_fragment"):
                    row["notes"].add(f"via `...{fr['via_fragment']}`")
                if fr.get("not_found_fragment"):
                    row["notes"].add("fragment body not found in snapshot")
                    row["story"] = row["story"] or f"NEW-{DOMAIN_FE_TOKEN.get(op_dom, '?')}-BE-G-??"
                    row["new"] = row["new"] or (row["story"] is not None and row["story"].startswith("NEW-"))
                    continue
                if row["story"] and not row["story"].startswith("NEW-"):
                    gate = spike_gate_for_story(op_dom, row["story"], be04, field=fname)
                    if gate:
                        row["notes"].add(gate)
                    continue  # already resolved by an earlier operation
                lookup_name = fname
                # Type-scoped be-05 lookup FIRST: `resolved_container` (from
                # collect_op_fields's real type-tracking through the walk) names the
                # ACTUAL type this field is declared on, when knowable — e.g.
                # `description` under `getBomStatus { code description }` resolves to
                # container `CodeDescription`, not the field's own value type. Checking
                # by_type_field with this before ever falling back to the bare-name
                # "fields" dict prevents a same-named field on an UNRELATED type (e.g.
                # `description` on `BomMaterialSearchResult`, a totally different type
                # elsewhere in the same domain) from being misattributed here just
                # because both types happen to have a field with that name. Falls back
                # to root_container_types (the operation's own root type) when the walk
                # couldn't resolve a container for this specific field.
                resolved_container = fr.get("resolved_container")
                candidate_containers = [resolved_container] if resolved_container else root_container_types
                hit = None
                for container in candidate_containers:
                    if container:
                        hit = be05["by_type_field"].get((container, lookup_name))
                        if hit:
                            break
                if not hit:
                    # Bare-name fallback is safe only when we DON'T know the real
                    # container (resolved_container is None — old untyped behavior, be-05
                    # is the best guess available), OR be-05 never documents this field
                    # name under any type OTHER than the one we're looking at (nothing to
                    # collide with). If be-05 has a row for this field name under some
                    # OTHER, DIFFERENT type than the container we've resolved, that row
                    # belongs to that other type — using it here is exactly the collision
                    # this type-tracking exists to prevent (e.g. `description` has a
                    # be-05 row for `BomMaterialSearchResult` only; a `getBomStatus` field
                    # resolved to container `CodeDescription` must NOT borrow it — it's a
                    # plain schema field with no be-05 row of its own, which tier 3 below
                    # will correctly recognize instead).
                    known_types = be05["field_types"].get(lookup_name)
                    collides_with_other_type = (
                        resolved_container is not None and known_types
                        and resolved_container not in known_types
                    )
                    if not collides_with_other_type:
                        hit = be05["fields"].get(lookup_name)
                if hit:
                    row["story"] = hit["story"]
                    row["ext"] = hit["ext"]
                    row["new"] = False   # clears a placeholder an EARLIER operation on
                                          # this same key left behind (root-field pass or
                                          # a prior op that missed it) — now genuinely covered.
                    gate = spike_gate_for_story(op_dom, row["story"], be04, field=fname)
                    if gate:
                        row["notes"].add(gate)
                    continue
                if bundle_covers(be05, lookup_name):
                    # be-05 confirms this field is a trivial pass-through, but not every
                    # domain's doc names WHICH story the bundle rolls into (e.g. packaging's
                    # trailer ends "DTO-mapped, no resolver" with no "Bundled into **Gxx**"
                    # sentence at all) — falling straight to a NEW-...-?? gap in that case
                    # would be wrong: the field IS covered, just by whichever story the root
                    # query itself resolves through. Use the operation's own root story.
                    root_story = next((r["be_story"] for r in rec.get("roots", [])
                                        if r.get("phase1") and r.get("be_story")), None)
                    row["story"] = (be05["bundle_stories"][0] if be05["bundle_stories"]
                                     else root_story or f"NEW-{DOMAIN_FE_TOKEN.get(op_dom, '?')}-BE-G-??")
                    row["new"] = not (be05["bundle_stories"] or root_story)
                    if be05["bundle_stories"]:
                        row["notes"].add("bundled trivial pass-through")
                    elif root_story:
                        row["notes"].add("bundled trivial pass-through (no story named in be-05 — root story used)")
                    continue
                # Cross-check #2 (after be-05's Attribute column): does any story's OWN
                # header TITLE name this field? Multi-field stories sometimes list a
                # field in the `+`-joined title that isn't repeated verbatim as its own
                # be-05 row (e.g. PRODUCT-BE-G-07's title lists `status` alongside its
                # partner fields) — checking titles here, before the broad prose grep,
                # avoids ever minting a duplicate/competing story for something a real
                # story's title already claims.
                title_hit = field_in_be04_title(fname, be04)
                if title_hit:
                    row["story"] = title_hit
                    row["new"] = False
                    gate = spike_gate_for_story(op_dom, title_hit, be04, field=fname)
                    if gate:
                        row["notes"].add(gate)
                    continue
                # Bug-1 fallback — before ever declaring a gap, check whether this field
                # is simply a PLAIN field on the type the root query already returns (the
                # be-05 "pass-throughs" list is illustrative, not exhaustive — it names
                # ~60 fields but the schema has more plain scalars/objects than that).
                # If the schema shows it declared there with a non-external return type,
                # it's a direct DTO field the root story already resolves — not a gap.
                plain_hit = False
                for container in root_container_types:
                    covered, is_ext_ref = schema_covers_as_plain_field(schema_reg, container, fname)
                    if covered:
                        root_story = next((r["be_story"] for r in rec.get("roots", [])
                                            if r.get("phase1") and r.get("be_story")), None)
                        row["story"] = root_story or row["story"] or \
                            f"NEW-{DOMAIN_FE_TOKEN.get(op_dom, '?')}-BE-G-??"
                        row["new"] = not root_story
                        row["notes"].add("direct DTO field, no separate resolver")
                        plain_hit = True
                        break
                if plain_hit:
                    continue
                # 4th tier (broadest, lowest-priority — after be-05/title/schema all
                # missed): does ANY story's prose mention this field at all? Catches
                # real coverage the first 3 checks can't (e.g. `content` on a paged
                # wrapper type only described in a story's prose, e.g. "`{content} =
                # getMeasurementByIds(...)`", never in be-05's table or a title).
                prose_hit = field_in_be04_prose(fname, be04)
                if prose_hit:
                    row["story"] = prose_hit
                    row["new"] = False
                    gate = spike_gate_for_story(op_dom, prose_hit, be04, field=fname)
                    if gate:
                        row["notes"].add(gate)
                    continue
                # genuine gap — only if no PRIOR operation already resolved this exact
                # key; don't downgrade an already-resolved row back to New=Yes.
                if row["story"] and not row["new"]:
                    continue
                # Sibling-confidence fallback (narrow, conservative — same reasoning
                # pattern as Product.status, which is computed/merged from the sibling
                # `businessPartners`/`vendorAttributes` fields' already-fetched data but
                # isn't individually named in be-05/title/schema anywhere). Sibling-
                # story-uniqueness ALONE is not enough signal (most fields in a
                # selection share a story simply because they're plain pass-throughs —
                # e.g. `paging` sits alongside `content` under `getProducts` with no
                # derivation relationship at all). This only fires when there is ALSO
                # explicit textual evidence, in the candidate story's OWN body, that
                # THIS SPECIFIC field is computed/derived/merged from other data —
                # requiring the field name to literally appear near derivation language
                # (mirrors how PRODUCT-BE-G-07's body says "`status` merges partner/
                # workspace statuses" — a field-specific claim, not a generic one).
                sibling_story = None
                if fr.get("group") is not None:
                    sibling_stories = set()
                    for other in field_rows:
                        if other is fr or other.get("group") != fr.get("group"):
                            continue
                        other_row = rows.get((other["field"], other.get("on_type")))
                        if not other_row or not other_row["story"]:
                            continue
                        if other_row["new"] or other_row["story"].startswith("NEW-"):
                            continue
                        sibling_stories.add(other_row["story"])
                    if len(sibling_stories) == 1:
                        candidate = next(iter(sibling_stories))
                        body = be04["bodies"].get(candidate, "")
                        derivation_re = re.compile(
                            rf'\b{re.escape(fname)}\b[^.\n]{{0,60}}\b(merge[sd]?|derived?|computed?|'
                            rf'combin\w*)\b|\b(merge[sd]?|derived?|computed?|combin\w*)\b[^.\n]{{0,60}}'
                            rf'\b{re.escape(fname)}\b', re.I)
                        if body and derivation_re.search(body):
                            sibling_story = candidate
                if sibling_story:
                    row["story"] = sibling_story
                    row["new"] = False
                    row["notes"].add("derived from sibling fields, AC added")
                    gate = spike_gate_for_story(op_dom, sibling_story, be04, field=fname)
                    if gate:
                        row["notes"].add(gate)
                    ac_editor.queue(op_dom, sibling_story, fname, fe_id)
                    continue
                # is this gap externally owned (a genuinely different-team platform
                # entity — VMM/IG/CORONA/APEX/... — not just any @extends stub in this
                # domain's local schema, since same-gateway @shareable value types like
                # ProductComponentStatus also show @extends here but are NOT a separate
                # team's entity)? if so it gets a REAL authored story, not a placeholder.
                ext_guess = None
                for container in root_container_types:
                    fields = schema_reg["types"].get(container, {})
                    ret = fields.get(fname)
                    if ret and is_external_platform_type(ret):
                        ext_guess = ret
                        break
                if on_type and is_external_platform_type(on_type):
                    ext_guess = ext_guess or on_type
                if ext_guess:
                    real_id, svc_name = ext_authoring.author(op_dom, fname, ext_guess, fe_id)
                    row["story"] = real_id
                    row["new"] = False
                    if svc_name and svc_name not in row["ext"]:
                        row["ext"] = [svc_name] + row["ext"]
                    row["notes"].add(f"newly authored — {real_id}")
                    continue
                phase = guess_gap_phase(fname, on_type, is_root=False)
                dom_token = DOMAIN_FE_TOKEN.get(op_dom, "?")
                row["story"] = row["story"] or f"NEW-{dom_token}-BE-{phase}-??"
                row["new"] = True

    # Second pass: fill External Dep "also depends" cross-reference for New=Yes rows,
    # and finalize SPIKE lookups for root-field rows resolved via be04 bodies directly.
    ext_index = {}  # service -> [story ids using it] across ALL rows in this story
    for row in rows.values():
        for svc in row["ext"]:
            ext_index.setdefault(svc, set()).add(row["story"])

    return {
        "fe_id": fe_id, "title": fe_meta["title"],
        "query_ops": [name for name, _ in query_ops],
        "mutation_count": mutation_count,
        "rows": rows, "ext_index": ext_index,
        "domains": domains_touched or ({domain_default} if domain_default else set()),
    }


_PASSTHROUGH_NOTE_MARKERS = (
    "direct DTO field, no separate resolver",   # tier 3: schema_covers_as_plain_field
    "bundled trivial pass-through",             # tier 2: be-05's bundle (covers both the
                                                  # named-story and root-story-used variants)
)


def _is_plain_passthrough(row):
    """True for a row that is a plain DTO field/enum riding along on its parent
    query/fragment with no resolver of its own — either a schema-declared plain
    field (tier 3) or one of be-05's documented trivial-scalar-pass-through bundle
    fields (tier 2, e.g. `comments`/`description` on Product, or `code`/
    `description` on a shared `CodeDescription`-shaped value type). Neither
    represents a distinct backend story, so both are dropped from the per-story
    table/counts entirely — a domain-direct object/enum field should never appear
    as its own "must complete first" dependency. Never drops a row whose story is
    still a NEW-...-?? placeholder — a genuine gap must stay visible even if it
    happens to also carry one of these notes."""
    if row["new"] or (row["story"] and row["story"].startswith("NEW-")):
        return False
    return any(marker in n for n in row["notes"] for marker in _PASSTHROUGH_NOTE_MARKERS)


def render_story_md(result):
    fe_id, title = result["fe_id"], result["title"]
    L = [f"## {fe_id} — {title}",
         f"Queries in scope: {', '.join(result['query_ops'])} · "
         f"Mutations excluded: {result['mutation_count']}",
         ""]

    kept_rows = {k: r for k, r in result["rows"].items() if not _is_plain_passthrough(r)}

    be_ids, spike_ids, new_ids = [], [], []
    for row in kept_rows.values():
        sid = row["story"]
        if sid and sid.startswith("NEW-"):
            if sid not in new_ids:
                new_ids.append(sid)
        elif sid:
            if sid not in be_ids:
                be_ids.append(sid)
        for n in row["notes"]:
            m = re.match(r'🔬 (SPIKE-0\d[a-z]?|[A-Z]+-BE-S-\d+[a-z]?)\b', n)
            if m and m.group(1) not in spike_ids:
                spike_ids.append(m.group(1))

    must = [f"**Must complete first:** BE — {', '.join(sorted(be_ids)) or '—'}"]
    if spike_ids:
        must.append(f"Spikes — {', '.join(sorted(spike_ids))}")
    if new_ids:
        must.append(f"New — {', '.join(sorted(new_ids))}")
    L.append(" · ".join(must))
    L.append("")

    def sort_key(item):
        (fname, on_type), row = item
        return (0 if row["story"] and row["story"].startswith("NEW-") else 1, fname.lower())

    def render_row(fname, row):
        story = row["story"] or "—"
        ext_cell = "—"
        if row["ext"]:
            svc = row["ext"][0]
            ext_cell = svc
            if row["new"]:
                others = sorted(s for s in result["ext_index"].get(svc, set())
                                 if s and s != story and not s.startswith("NEW-"))
                if others:
                    ext_cell = f"{svc} — also {', '.join(others)}"
        impacts = ", ".join(sorted(row["impacts"]))
        # keep 🔬 spike notes first
        note_list = sorted(row["notes"], key=lambda n: (0 if n.startswith("🔬") else 1, n))
        notes = "; ".join(note_list)
        return (f"| {md_escape(fname)} | {story} | {md_escape(ext_cell)} | "
                f"{'Yes' if row['new'] else 'No'} | {md_escape(impacts)} | {md_escape(notes)} |")

    query_rows = {k: r for k, r in kept_rows.items() if r["is_query"]}
    field_rows = {k: r for k, r in kept_rows.items() if not r["is_query"]}

    L.append("### Queries")
    L.append("")
    L.append("> The root GraphQL operations this story ships. Readiness is driven from this "
             "table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through "
             "field with no resolver of its own is not a distinct story and does not appear "
             "in either table.")
    L.append("")
    L.append("| Query | Story | External Dep | New? | Impacts (queries) | Notes |")
    L.append("|---|---|---|---|---|---|")
    for (fname, on_type), row in sorted(query_rows.items(), key=sort_key):
        L.append(render_row(fname, row))

    L.append("")
    L.append("### Fields")
    L.append("")
    L.append("> Field/entity-level detail behind the queries above, for traceability — not "
             "part of the readiness count except where `New?` = Yes (a genuine gap).")
    L.append("")
    L.append("| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |")
    L.append("|---|---|---|---|---|---|")
    for (fname, on_type), row in sorted(field_rows.items(), key=sort_key):
        L.append(render_row(fname, row))

    L.append("")
    L.append(f"## {fe_id} — Readiness")
    new_count = sum(1 for r in kept_rows.values() if r["new"])
    spike_count = len(spike_ids)
    total = len(kept_rows)
    ready = total - new_count
    if new_count == 0 and spike_count == 0:
        summary = (f"All {total} distinct fields/entities this story's queries touch resolve to "
                   "existing, real backend stories — no gaps, no spike gates. This story is ready "
                   "to sequence as soon as its listed BE stories are delivered.")
    else:
        parts = [f"{ready} of {total} distinct fields/entities resolve to existing backend stories."]
        if new_count:
            parts.append(f"{new_count} field(s) have no covering story yet (see the `NEW-...-??` "
                         "placeholders above) and block full readiness until a real story is authored.")
        if spike_count:
            parts.append(f"{spike_count} field(s) sit behind an unresolved spike "
                         f"({', '.join(sorted(spike_ids))}) and cannot be built past the spike's decision.")
        summary = " ".join(parts)
    L.append(summary)
    L.append("")
    return "\n".join(L)


# ─── Consolidated gap + external-dep register ────────────────────────────────
def render_consolidated(all_results, ext_authoring):
    gap_rows = {}      # internal-only NEW-...-?? placeholder -> {"field","fe_ids": set(),"domain"}
    ext_rows = {}      # service -> set(fe_ids)  (risk register — every EXT dep seen, not just gaps)

    for res in all_results:
        for (fname, on_type), row in res["rows"].items():
            if row["new"] and row["story"] and row["story"].startswith("NEW-"):
                # domain comes from the placeholder id itself (NEW-<TOKEN>-BE-...),
                # never from the FE story's own domain set — a cross-cutting FE story
                # (e.g. IMPRESSION-FE-002) can touch several BACKEND domains, and
                # picking an arbitrary one from that set mislabels every gap it finds
                # in a domain other than its own primary one.
                tok_m = re.match(r'NEW-([A-Z]+)-BE-', row["story"])
                dom = FE_TOKEN_DOMAIN.get(tok_m.group(1), "?") if tok_m else "?"
                g = gap_rows.setdefault(row["story"], {"field": fname, "fe_ids": set(), "domain": dom})
                g["fe_ids"].add(res["fe_id"])
            for svc in row["ext"]:
                ext_rows.setdefault(svc, set()).add(res["fe_id"])

    authored = ext_authoring._authored  # {key: entry} in authoring order via _order

    L = [
        "# Newly Identified Backend Stories — Consolidated Gap List",
        "",
        "> Auto-generated by generate_client_story_dependency.py from all query-bearing phase-1 "
        "FE story reports in this folder. Regenerate after any be-04-stories.md or "
        "be-05-attribute-inventory.md change.",
        "",
        "## Genuinely new, internal-only gaps (no story anywhere, no external dependency)",
        "",
        "> `NEW-...-??` placeholders are NOT real story ids — never write them into "
        "be-04-stories.md/Jira/Confluence without first authoring the real story. These are "
        "rare by design: every externally-owned gap below already got a REAL story authored "
        "in `ext-dependency-stories.md` — only a genuinely internal, no-external-service gap "
        "stays a placeholder here.",
        "",
        "| Placeholder | Field/Entity | Blocks (FE stories) | Domain |",
        "|---|---|---|---|",
    ]
    if gap_rows:
        for placeholder in sorted(gap_rows, key=lambda k: (gap_rows[k]["domain"], k)):
            g = gap_rows[placeholder]
            L.append(f"| {placeholder} | {md_escape(g['field'])} | "
                     f"{', '.join(sorted(g['fe_ids']))} | {g['domain']} |")
    else:
        L.append("| — | — | — | — |")

    L += [
        "",
        "## Newly authored real stories (externally-owned gaps — identified, not yet pushed to Jira)",
        "",
        "> These ARE real story ids (same numbering convention as be-04-stories.md) — full text lives "
        "in [`ext-dependency-stories.md`](../analysis/program/ext-dependency-stories.md). "
        "They are \"newly identified\" "
        "in the sense of not yet folded into their domain's be-04-stories.md / pushed to Jira — not "
        "placeholders.",
        "",
        "| Story id | Field/Entity | External Dep | Blocks (FE stories) | Domain |",
        "|---|---|---|---|---|",
    ]
    if authored:
        for key in sorted(authored, key=lambda k: authored[k]["id"]):
            e = authored[key]
            L.append(f"| {e['id']} | {md_escape(e['field'])} | {e['service']} | "
                     f"{', '.join(sorted(e['blocks']))} | {e['domain']} |")
    else:
        L.append("| — | — | — | — | — |")

    L += [
        "",
        "## External-service dependencies (risk register — every EXT dep seen, gap or not)",
        "",
        "| Service | Affects (FE stories) |",
        "|---|---|",
    ]
    if ext_rows:
        for svc in sorted(ext_rows):
            L.append(f"| {svc} | {', '.join(sorted(ext_rows[svc]))} |")
    else:
        L.append("| — | — |")
    L.append("")
    return "\n".join(L), len(gap_rows), len(authored), len(ext_rows)


# ─── main ────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # wipe stale per-story files from a previous run (wholesale regeneration, not incremental)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()

    print("Loading fe-08 frontend stories…")
    fe_stories = load_fe_stories()

    print("Loading frontend-inventory.json…")
    _ops, by_op_name, by_root_field = load_inventory()

    print("Indexing fragments across ClientCallingGqlQueries/…")
    frag_index = _FragmentIndex()
    print(f"  {len(frag_index.bodies)} fragment definitions found")

    be05_cache, be04_cache, schema_cache = {}, {}, {}
    ext_authoring = ExtAuthoring(be04_cache)
    ac_editor = ACEditor()

    results = []
    skipped = []
    for fe_id in IN_SCOPE_STORIES:
        meta = fe_stories.get(fe_id)
        if not meta:
            print(f"  ! {fe_id} not found in fe-08-frontend-stories.md — skipping")
            continue
        res = process_story(fe_id, meta, by_op_name, by_root_field, frag_index,
                             be05_cache, be04_cache, schema_cache, ext_authoring, ac_editor)
        if res is None:
            skipped.append(fe_id)
            continue
        results.append(res)
        out_path = OUT_DIR / f"{fe_id}.md"
        out_path.write_text(render_story_md(res), encoding="utf-8")
        print(f"  OK {out_path.relative_to(ROOT)} ({len(res['rows'])} field rows)")

    # Apply queued sibling-confidence-match AC edits AFTER all 23 stories are processed
    # (never mid-run — every story's be04_cache read during processing must reflect the
    # ORIGINAL file, not a partially-edited one from an earlier FE story in this same run).
    ac_editor.apply_all()
    if ac_editor.applied:
        print(f"\nAppended {len(ac_editor.applied)} Acceptance Criteria "
              f"(sibling-confidence-match, narrow fallback):")
        for domain, story_id, field, path in ac_editor.applied:
            print(f"  {story_id} ({path}): + AC for `{field}`")

    ext_story_md = ext_authoring.render()
    ext_out_path = FE_OUT / "ext-dependency-stories.md"
    if ext_story_md:
        ext_out_path.write_text(ext_story_md, encoding="utf-8")
        print(f"  OK {ext_out_path.relative_to(ROOT)} ({len(ext_story_md):,} chars, "
              f"{len(ext_authoring._order)} stories authored)")
    elif ext_out_path.exists():
        ext_out_path.unlink()

    consolidated, gap_count, authored_count, ext_count = render_consolidated(results, ext_authoring)
    out_path = OUT_DIR / "00-NEWLY-IDENTIFIED-STORIES.md"
    out_path.write_text(consolidated, encoding="utf-8")
    print(f"  OK {out_path.relative_to(ROOT)} ({len(consolidated):,} chars)")

    if skipped:
        print(f"  (skipped — no query operations found: {', '.join(skipped)})")
    print(f"\n{len(results)} story reports written · {gap_count} internal-only placeholder gap(s) · "
          f"{authored_count} real external-dependency stories authored · "
          f"{ext_count} distinct external service(s) referenced.")


if __name__ == "__main__":
    main()
