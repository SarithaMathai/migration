# Phase 3: Federation Schema Analysis — Impression

> **Domain:** `impression` · **Target DGS:** `ImpressionService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 3 🔜 | 0 ⏭ — 3 operations**

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `Impression` |
| Owned value types | 2 | `ImpressionCount`, `CountsByBp` |
| `@shareable` | 1 | `CountsByBp` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — sibling DGS | 3 | `Product`, `WorkspaceV2`, `UserProfileAttributes` |
| Inputs | 3 | `ProductImpressionInput`, `ImpressionInput`, `ProductPartnerInput` |

No interfaces/unions — no `@DgsTypeResolver` needed.

## 2. Client Contract Verification
2 queries + 1 mutation preserved (`0 ✅ | 3 🔜 | 0 ⏭`). `SPARK_` prefixes dropped; `VMM_` kept.

## 3. Federation Boundaries

> **Monorepo:** `product` and `impression` are the **same `plm-product` subgraph** — references between them
> are **internal types**, not federation. See [reference-federation-patterns.md §0](../scripts/reference-federation-patterns.md).

- **Owns** `Impression`, `ImpressionCount`, `CountsByBp`.
- **Internal (same subgraph — NOT federation):** `Product` (the `ImpressionCount.counts` product lookup is an
  in-process call).
- **External (true federation stubs):** `WorkspaceV2` (workspace), `UserProfileAttributes` (user-profile),
  `VMM_BusinessPartner` (platform).
- **Contributes back** to `Product` → **internal** field resolvers (co-located): `impressions(...)` +
  `impressionCounts`. Not gateway-federated; depends only on the `Product` type existing.

## 4. Migration Approach  *(Confluence approach page)*

Impression is the **smallest and lowest-risk** of the thirteen domains — a good early win.

1. **Phase A:** schema + `ImpressionService` port (one GET, one PUT). No interfaces, no type resolvers.
2. **Phase B:** the 2 reads. `getImpressionCountsByProductId` reuses the search call; the aggregation lives
   in the `ImpressionCount.counts` field resolver.
3. **Phase D:** `updateImpressions` (delete + update sets in one PUT; typed validation exception).
4. **Phase G:** `Impression` field resolvers (partners/workspaces/users via federation; all 🔵/🟡) and the
   `counts` aggregation. The product lookup in `counts` is an **internal** same-DGS call.
5. **Phase F:** Product entity extension — post-launch, BLOCKED-BY product.

**Recommended improvement (PO decision):** the source `getImpressionCountsByProductId` returns the
impressions **array** typed as `ImpressionCount`, and the `counts` field reads `impressions[0].parentId`
to re-fetch the product. This is fragile (empty list throws; caught → dummy `0`). Recommend migrating the
contract to a typed **`ImpressionCountResult { productId, totalCount, countsByPartner[] }`** computed in the
data fetcher. If the existing client contract must be preserved exactly, keep `ImpressionCount` and port the
try/catch fallback faithfully. **Default: preserve contract; offer `ImpressionCountResult` as a fast-follow.**

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `ImpressionCount` array-as-parent contract is fragile (empty list path) | Low | Low | Preserve try/catch fallback; consider `ImpressionCountResult` | Architect |
| `enableWorkspaceContextFiltering` accepted but not forwarded to service | Low | Low | Confirm intended; wire through if needed | Backend Eng |
| Sibling refs (workspace/user-profile/VMM) need stubs in gateway | Medium | Low | Standard federation sequencing | Platform |

## 6. ACL Handling
Both queries and the mutation curry a capability token via `getUserPermissionsJWT` because impression
reads/writes are product-scoped and the backend authorizes per product. **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

## 7. Open Questions
1. Restructure `ImpressionCount` → `ImpressionCountResult`, or preserve exactly?
2. Should `enableWorkspaceContextFiltering` be forwarded to the backend?

---
**Phase Completed:** Phase 3 · **Domain:** `impression`.
