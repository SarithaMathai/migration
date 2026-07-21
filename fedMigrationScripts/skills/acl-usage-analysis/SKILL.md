---
name: acl-usage-analysis
description: "For every resolver/field that touches ACL, classifies the call site as permission-check (resolver-local) or downstream-token (capability token minted to call ANOTHER domain's endpoint), and evaluates whether Mid-Request ACL Update (SparkSecurityService.updateCurrentUserPermissions) resolves it. Explicitly supersedes the 'ACL is context-only, ignored' language in be-03/be-04. Output: output/{domain}/be-07-acl-usage-analysis.md + program roll-up output/aclResearch/00-acl-usage-inventory.md"
argument-hint: "Provide the domain whose resolver analysis (Phase 2) is complete. Example: 'Run ACL usage analysis for bom' or 'Regenerate ACL research for all domains'."
---

# Skill: ACL Usage Analysis

## Purpose

Every domain's `be-03-schema.graphql` header and `be-04-stories.md` currently state ACL/JWT
usage is *"context-only... IGNORED in the DGS implementation (no ACL plumbing story)"*. This
skill tests that claim resolver-by-resolver: for every ACL call site, is the capability
token only gating the CURRENT resource (truly context-only), or is it minted specifically
to call ANOTHER domain's API (load-bearing, not ignorable)?

For the load-bearing cases, it evaluates **Mid-Request ACL Update** —
`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`, callable from within
the application after fetching a new capability token, to refresh the current thread's
security context without re-authenticating — as the resolution.

## When to Use

- After `be-02-resolver-analysis.md` exists for a domain (ACL call sites are already
  flagged there per-field, but not classified by purpose)
- Before finalizing the "ACL ignored" language in be-03/be-04 for a domain — this is the
  research pass; **doc edits are a deliberate separate follow-up**, never bundled into this
  skill's run (per program decision, 2026-07-17)
- When scoping whether a federation entity-resolver story also needs an ACL-refresh step

## Cannot Run Without

- `code/resolvers/**/*.txt` (parsed directly for `getUserPermissionsJWT` call sites and
  `ctx.loaders.accessControl.*` reads — be-02's ACL mentions are prose/scattered, not a
  single machine-parseable table, so this skill re-derives from source)
- `fedMigrationScripts/reference/domain-service-catalog.md` (to determine whether a
  downstream loader key is a phase-1 domain / sibling DGS / external platform)
- `generate_schema_analysis.py`'s resolver-map parser (`parse_resolver_map`) — imported,
  not reimplemented

## How It Works

This is a **generated artifact** — run the generator:

```
python fedMigrationScripts/generatescripts/generate_acl_analysis.py            # all domains
python fedMigrationScripts/generatescripts/generate_acl_analysis.py bom        # one domain
```

The generator (`generate_acl_analysis.py`) classifies every ACL call site into one of four
kinds:

| Kind | Meaning | Recommendation |
|---|---|---|
| `permission-check` | `accessControl.getPermissions`/`getUserAccessUnencoded` or a bulk ACL-filtered tree read for the CURRENT resource | No action — resolver-local, ACL genuinely context-only here |
| `own-domain-token` | `getUserPermissionsJWT` token used only by this domain's OWN loader (e.g. `bom` resolver → `ctx.loaders.bom(token)`) | No action — resolver-local write/read gate |
| `downstream-token` | Token minted then handed to a DIFFERENT domain's loader (`ctx.loaders.<otherDomain>(token)`) | **Mid-Request ACL Update** if the target is a phase-1/sibling DGS domain; gateway auth passthrough if the target is an external platform stub |
| `unresolved-token` | Token minted but no downstream use found in the same field body (e.g. passed into a helper function) | Manual check — the parser only looks within one field body, not across helper-function boundaries |

Every `downstream-token` finding is flagged as an explicit conflict with the existing
"ACL ignored" text — this skill records the conflict, it does not resolve it by editing
be-03/be-04.

## Output Format

Per domain: `output/{domain}/be-07-acl-usage-analysis.md` — header block (with the
supersession warning banner), summary table, one row per ACL call site, a "Conflicts with
the Existing ACL Ignored Decision" section listing every downstream-token finding, a
classification legend, response footer.

Program roll-up: `output/aclResearch/00-acl-usage-inventory.md` — the key finding statement,
totals by domain and classification, and a consolidated table of every downstream-token
call site across all 8 domains (the full Mid-Request ACL Update candidate list).

⚠ Regeneration overwrites both — never hand-edit; fix the generator or the catalog instead.

## Follow-Up (Not Part of This Skill)

Once findings are reviewed, a separate pass updates the superseded "ACL is context-only,
ignored" language in each domain's `be-03-schema.graphql` header and `be-04-stories.md`
ACL note, and adds any new ACL-refresh stories these findings imply. Do not fold that
doc-rewrite into this generator — it stays a deliberate, reviewed, separate step.
