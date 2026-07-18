# Phase 7: ACL Usage Analysis — Claims

> **Domain:** `claims`
> **Target DGS:** `spark-claims (separate)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-17
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field

> ⚠ **This supersedes the existing ACL note in `be-03-schema.graphql` / `be-04-stories.md`:** *“capability-token (JWT) usage in source is context-only; ACL is IGNORED in the DGS implementation (no ACL plumbing story)”*. Rows below marked **downstream-token** are cases where ACL is NOT purely context — a capability token is required to call another domain's endpoint. This file does not edit be-03/be-04 — doc updates are a separate follow-up once these findings are reviewed.

For every resolver/field that touches ACL, this classifies the call site (permission-check vs. token required for a downstream cross-domain call) and evaluates whether **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) resolves it.

## Summary

| Metric | Count |
|---|---|
| Total ACL call sites | 5 |
| Permission-check (resolver-local) | 2 |
| Own-domain token (resolver-local write/read gate) | 3 |
| **Downstream-token (cross-domain, Mid-Request ACL Update candidate)** | **0** |
| Unresolved (needs manual check) | 0 |

## ACL Call Sites

| Resolver | Classification | Detail | Recommendation |
|---|---|---|---|
| `Mutation.lockClaim` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `claim` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `Mutation.unlockClaim` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `claim` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `Query.getClaimByIds` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `claim` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `SPARK_Claims.access` | permission-check | `accessControl.getPermissions` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_Claims.currentUserPermissions` | permission-check | `accessControl.getUserAccessUnencoded` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |

## Classification Legend

- **permission-check** — reads a permission/access value for the current resource (`accessControl.getPermissions`/`getUserAccessUnencoded`, or bulk ACL-filtered tree reads); resolver-local, no token handoff.
- **own-domain-token** — `getUserPermissionsJWT` mints a token used only by this domain's own loader (e.g. `bom` resolver calling `ctx.loaders.bom(token)`); resolver-local, stays as-is.
- **downstream-token** — token minted then handed to a DIFFERENT domain's loader (`ctx.loaders.<otherDomain>(token)`) — the Mid-Request ACL Update candidate.
- **unresolved-token** — token minted but the downstream use isn't statically visible in the same field body (e.g. passed into a helper function) — needs a manual check.

---
**Phase Completed:** Phase 7 — ACL Usage Analysis · **Domain:** `claims` · **ACL call sites:** 5 · **Downstream-token:** 0
