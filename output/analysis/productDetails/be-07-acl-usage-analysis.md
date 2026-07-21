# Phase 7: ACL Usage Analysis — Product Details

> **Domain:** `productDetails`
> **Target DGS:** `plm-product (co-located)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-21
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field

> ⚠ **This supersedes the existing ACL note in `be-03-schema.graphql` / `be-04-stories.md`:** *“capability-token (JWT) usage in source is context-only; ACL is IGNORED in the DGS implementation (no ACL plumbing story)”*. Rows below marked **downstream-token** are cases where ACL is NOT purely context — a capability token is required to call another domain's endpoint. This file does not edit be-03/be-04 — doc updates are a separate follow-up once these findings are reviewed.

For every resolver/field that touches ACL, this classifies the call site (permission-check vs. token required for a downstream cross-domain call) and evaluates whether **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) resolves it.

## Summary

| Metric | Count |
|---|---|
| Total ACL call sites | 9 |
| Permission-check (resolver-local) | 2 |
| Own-domain token (resolver-local write/read gate) | 5 |
| **Downstream-token (cross-domain, Mid-Request ACL Update candidate)** | **2** |
| Unresolved (needs manual check) | 0 |

## ACL Call Sites

| Resolver | Classification | Detail | Recommendation |
|---|---|---|---|
| `Mutation.cloneFilesForProductDetails` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.attachment.*(permissionJWT)` — capability token required to call **separate DGS (plm-attachment)** (`attachment`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `Mutation.createProductDetailsSet` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `ProductDetails` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `Mutation.productDetailLockUnlock` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `ProductDetails` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `Mutation.updateProductDetailAccess` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `ProductDetails` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `Mutation.updateProductDetailsSet` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `ProductDetails` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `Mutation.updateProductDetailsSet` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.attachment.*(attachmentPermissionJWT)` — capability token required to call **separate DGS (plm-attachment)** (`attachment`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `Query.getProductDetailsById` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `ProductDetails` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `SPARK_ProductDetails.access` | permission-check | `accessControl.getPermissions` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_ProductDetails.currentUserPermissions` | permission-check | `accessControl.getUserAccessUnencoded` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |

## Conflicts with the Existing "ACL Ignored" Decision

2 resolver(s) in this domain mint a capability token to call another domain — these are NOT context-only, contradicting the current be-03/be-04 text.

| Resolver | Recommendation |
|---|---|
| `Mutation.cloneFilesForProductDetails` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `Mutation.updateProductDetailsSet` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |

## Classification Legend

- **permission-check** — reads a permission/access value for the current resource (`accessControl.getPermissions`/`getUserAccessUnencoded`, or bulk ACL-filtered tree reads); resolver-local, no token handoff.
- **own-domain-token** — `getUserPermissionsJWT` mints a token used only by this domain's own loader (e.g. `bom` resolver calling `ctx.loaders.bom(token)`); resolver-local, stays as-is.
- **downstream-token** — token minted then handed to a DIFFERENT domain's loader (`ctx.loaders.<otherDomain>(token)`) — the Mid-Request ACL Update candidate.
- **unresolved-token** — token minted but the downstream use isn't statically visible in the same field body (e.g. passed into a helper function) — needs a manual check.

---
**Phase Completed:** Phase 7 — ACL Usage Analysis · **Domain:** `productDetails` · **ACL call sites:** 9 · **Downstream-token:** 2
