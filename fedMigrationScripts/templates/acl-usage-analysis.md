# Template: ACL Usage Analysis (`be-07-acl-usage-analysis.md`)

This template defines the exact format for Phase 7 output, produced by
`generatescripts/generate_acl_analysis.py`. Regenerated, never hand-edited.

---

## File Header Block

```markdown
# Phase 7: ACL Usage Analysis — {Domain Display Name}

> **Domain:** `{loader-key}`
> **Target DGS:** `{target-dgs-label}`
> **Pipeline Version:** 1.0
> **Generated:** {YYYY-MM-DD}
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field
```

Immediately after the header, every file carries the fixed supersession banner (do not
paraphrase — it must quote the exact superseded text so a future diff/search can find it):

```markdown
> ⚠ **This supersedes the existing ACL note in `be-03-schema.graphql` / `be-04-stories.md`:**
> *"capability-token (JWT) usage in source is context-only; ACL is IGNORED in the DGS
> implementation (no ACL plumbing story)"*. Rows below marked **downstream-token** are
> cases where ACL is NOT purely context — a capability token is required to call another
> domain's endpoint. This file does not edit be-03/be-04 — doc updates are a separate
> follow-up once these findings are reviewed.
```

## Summary (Mandatory)

```markdown
## Summary

| Metric | Count |
|---|---|
| Total ACL call sites | {n} |
| Permission-check (resolver-local) | {n} |
| Own-domain token (resolver-local write/read gate) | {n} |
| **Downstream-token (cross-domain, Mid-Request ACL Update candidate)** | **{n}** |
| Unresolved (needs manual check) | {n} |
```

## ACL Call Sites Table (Mandatory)

```markdown
## ACL Call Sites

| Resolver | Classification | Detail | Recommendation |
|---|---|---|---|
| `{Type.field}` | permission-check \| own-domain-token \| downstream-token \| unresolved-token | {one-line detail, name the actual accessControl method or loader key} | {recommendation from output-conventions.md §14} |
```

## Conflicts Section (Only if downstream-token findings exist)

```markdown
## Conflicts with the Existing "ACL Ignored" Decision

{n} resolver(s) in this domain mint a capability token to call another domain — these are NOT context-only, contradicting the current be-03/be-04 text.

| Resolver | Recommendation |
|---|---|
```

## Classification Legend (Mandatory, fixed text)

```markdown
## Classification Legend

- **permission-check** — reads a permission/access value for the current resource (`accessControl.getPermissions`/`getUserAccessUnencoded`, or bulk ACL-filtered tree reads); resolver-local, no token handoff.
- **own-domain-token** — `getUserPermissionsJWT` mints a token used only by this domain's own loader; resolver-local, stays as-is.
- **downstream-token** — token minted then handed to a DIFFERENT domain's loader — the Mid-Request ACL Update candidate.
- **unresolved-token** — token minted but the downstream use isn't statically visible in the same field body — needs a manual check.
```

## Response Footer (Mandatory)

```markdown
---
**Phase Completed:** Phase 7 — ACL Usage Analysis · **Domain:** `{loader-key}` · **ACL call sites:** {n} · **Downstream-token:** {n}
```

---

## Program Roll-Up (`aclResearch/00-acl-usage-inventory.md`)

Sections, in order: Key Finding (the supersession statement), Program Totals, By Domain
table, All Downstream-Token Call Sites (the full Mid-Request ACL Update candidate list
across every domain). See `generate_acl_analysis.generate_rollup()` for the generator.
