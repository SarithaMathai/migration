# Impression — Resolver Analysis: Services + Utils

> **Domain:** `impression` · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## D1. `ImpressionService` (2 methods, 44 lines)

| # | Method | HTTP | Path | JWT | Notes |
|---|---|---|---|---|---|
| 1 | `searchImpressionsByProductId(jwt, productId, partnerIds, workspaceIds)` | GET | `/impressions/product/{productId}?workspaceIds=&partnerIds=` | ✓ | Manual query-string assembly. **`enableWorkspaceContextFiltering` arg is missing** from signature (latent bug — schema declares it). |
| 2 | `updateImpressions(jwt, productId, productImpression)` | PUT | `/impressions/product/{productId}` | ✓ | camelCase ↔ snake_case both ways |

Service extends `SparkService` (base class, only inherits logger plumbing).

---

## D2. No dedicated utils

All cross-cutting helpers are **shared**:

| Util | Owner | Usage |
|---|---|---|
| `commonLoaders.getUserPermissionsJWT` | shared | Q1, Q2, M1 |
| `vmmUtils.loadBp` / `loadBpsWithType` | vmm | C1 |
| `logger` | shared | C2 |
| `resolvers/SPARK_WorkspaceV2.Query.getWorkspacesByIdsV2` | workspace | C1 |
| `ctx.loaders.userAttributes.getUserByID` | user-profile | C1 |
| `ctx.loaders.product.getByID` | product | C2 |

**Finding 🟡:** Cross-resolver import of `SPARK_WorkspaceV2`. Replace with native call in port.

---

## D3. Findings

| # | Finding | Severity |
|---|---|---|
| 1 | `enableWorkspaceContextFiltering` arg never reaches backend — fix during port | 🔴 |
| 2 | Manual query-string assembly — replace with Feign multi-param | 🟢 |
| 3 | No DataLoader batching at the resolver level (single product per call); add per-product cache in DGS request scope | 🟢 |
| 4 | `SparkService` base class — keep parity helper or fold into Spring base controller | 🟢 |

---

## D4. Phase 2 Grand Total

| Sub-phase | Days |
|---|---|
| 2A Queries | 2–4 |
| 2B Mutations | 1–2 |
| 2C Field resolvers | 2–4 |
| 2D Service + utils | 2–3 |
| **Phase 2 raw** | **7–13** |
| **+20% buffer** | **8–16** |

---

**Phase Completed:** Phase 2D — Services + Utils
