# Phase 7: ACL Usage Analysis — Product

> **Domain:** `product`
> **Target DGS:** `plm-product (host)`
> **Pipeline Version:** 1.0
> **Generated:** 2026-07-24
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md)
> **DGS Target Status:** Green-field

> ⚠ **This supersedes the existing ACL note in `be-03-schema.graphql` / `be-04-stories.md`:** *“capability-token (JWT) usage in source is context-only; ACL is IGNORED in the DGS implementation (no ACL plumbing story)”*. Rows below marked **downstream-token** are cases where ACL is NOT purely context — a capability token is required to call another domain's endpoint. This file does not edit be-03/be-04 — doc updates are a separate follow-up once these findings are reviewed.

For every resolver/field that touches ACL, this classifies the call site (permission-check vs. token required for a downstream cross-domain call) and evaluates whether **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) resolves it.

## Summary

| Metric | Count |
|---|---|
| Total ACL call sites | 18 |
| Permission-check (resolver-local) | 8 |
| Own-domain token (resolver-local write/read gate) | 1 |
| **Downstream-token (cross-domain, Mid-Request ACL Update candidate)** | **9** |
| Unresolved (needs manual check) | 0 |

## ACL Call Sites

| Resolver | Classification | Detail | Recommendation |
|---|---|---|---|
| `Mutation.addProduct` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.workspaceV2.*(workspaceResourcePermissionJWT)` — capability token required to call **WorkspaceService** (`workspaceV2`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `workspaceV2`, avoiding re-authentication |
| `Mutation.addProducts` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.workspaceV2.*(workspaceResourcePermissionJWT)` — capability token required to call **WorkspaceService** (`workspaceV2`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `workspaceV2`, avoiding re-authentication |
| `Mutation.addProducts` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.attachment.*(permissionJWT)` — capability token required to call **separate DGS (plm-attachment)** (`attachment`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `Mutation.productBusinessPartnerActions` | permission-check | `accessControl.dropPartnerFromResources` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `Mutation.productBusinessPartnerActions` | permission-check | `accessControl.unDropPartnerFromResources` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `Mutation.productBusinessPartnerActions` | own-domain-token | `getUserPermissionsJWT` token passed to this domain's own `product` loader — capability token required for the resolver's own write/read, not a cross-domain call | No action needed — token gates the resolver's own read/write, stays resolver-local |
| `Mutation.productBusinessPartnerActions` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.sampleV2.*(capabilityToken)` — capability token required to call **SampleService** (`sampleV2`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `sampleV2`, avoiding re-authentication |
| `Mutation.updateProduct` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.attachment.*(permissionJWT)` — capability token required to call **separate DGS (plm-attachment)** (`attachment`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `Mutation.updateProduct` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.attachment.*(permissionJWT)` — capability token required to call **separate DGS (plm-attachment)** (`attachment`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `SPARK_Product.associateProductsAsks` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.productAsk.*(permissionJWT)` — capability token required to call **ProductAskService** (`productAsk`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `productAsk`, avoiding re-authentication |
| `SPARK_Product.attachments` | permission-check | `accessControl.getUserAccessByPost` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_Product.attachmentsWithMetaData` | permission-check | `accessControl.getUserAccessByPost` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_Product.attachmentsWithMetaData` | permission-check | `accessControl.getUserAccessByPost` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_Product.attachmentsWithMetaData` | permission-check | `accessControl.getUserAccessUnencoded` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_Product.components` | permission-check | `accessControl.getUserAccessUnencoded` — reads permission/access value for the current resource | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_Product.components` | permission-check | bulk/partner ACL-filtered resource tree — resolver-local read filter, not a token for a downstream call | No action needed — permission check only, resolves locally, no token handoff |
| `SPARK_Product.teams` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.teamV2.*(jwt)` — capability token required to call **TeamService** (`teamV2`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `teamV2`, avoiding re-authentication |
| `SPARK_Product.variations` | downstream-token | `getUserPermissionsJWT` token minted then passed into `ctx.loaders.productVariation.*(permissionJWT)` — capability token required to call **ProductVariationService** (`productVariation`) | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `productVariation`, avoiding re-authentication |

## Conflicts with the Existing "ACL Ignored" Decision

9 resolver(s) in this domain mint a capability token to call another domain — these are NOT context-only, contradicting the current be-03/be-04 text.

| Resolver | Recommendation |
|---|---|
| `Mutation.addProduct` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `workspaceV2`, avoiding re-authentication |
| `Mutation.addProducts` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `workspaceV2`, avoiding re-authentication |
| `Mutation.addProducts` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `Mutation.productBusinessPartnerActions` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `sampleV2`, avoiding re-authentication |
| `Mutation.updateProduct` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `Mutation.updateProduct` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `attachment`, avoiding re-authentication |
| `SPARK_Product.associateProductsAsks` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `productAsk`, avoiding re-authentication |
| `SPARK_Product.teams` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `teamV2`, avoiding re-authentication |
| `SPARK_Product.variations` | Mid-Request ACL Update — SparkSecurityService.updateCurrentUserPermissions(capabilityToken) refreshes the thread's security context before the downstream call to `productVariation`, avoiding re-authentication |

## Classification Legend

- **permission-check** — reads a permission/access value for the current resource (`accessControl.getPermissions`/`getUserAccessUnencoded`, or bulk ACL-filtered tree reads); resolver-local, no token handoff.
- **own-domain-token** — `getUserPermissionsJWT` mints a token used only by this domain's own loader (e.g. `bom` resolver calling `ctx.loaders.bom(token)`); resolver-local, stays as-is.
- **downstream-token** — token minted then handed to a DIFFERENT domain's loader (`ctx.loaders.<otherDomain>(token)`) — the Mid-Request ACL Update candidate.
- **unresolved-token** — token minted but the downstream use isn't statically visible in the same field body (e.g. passed into a helper function) — needs a manual check.

---
**Phase Completed:** Phase 7 — ACL Usage Analysis · **Domain:** `product` · **ACL call sites:** 18 · **Downstream-token:** 9
