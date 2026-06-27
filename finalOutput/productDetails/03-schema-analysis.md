# Phase 3: Federation Schema Analysis — ProductDetails

> **Domain:** `productDetails` · **Target DGS:** `ProductDetailsService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 8 🔜 | 0 ⏭ — 8 operations**

The target schema is translated from the source SDL (`code/schemas/SPARK_ProductDetail.txt`), verified
against the resolver.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `ProductDetails` (key `id`; SDL also exposes `humanId`) |
| Owned value types | 3 | `ProductDetailsPaged`, `ProductDetailsItem`, `ProductDetailsCategoryWithSection` |
| `@shareable` | 1 | `CodeDescription` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — sibling DGS | 6 | `Attachment`, `WorkspaceV2`, `UserProfileAttributes`, `UserGroup_Participants`, `AccessControl`, `ResourcePermissions` |
| Internal (same subgraph) | 3 | `Product`, `ProductComponentStatus`, `VersionableId` |
| Inputs | 8 | `ProductDetailSetInput`, `ProductDetailSetUpdateInput`, … |

No interfaces / unions — no `@DgsTypeResolver` needed.

## 2. Client Contract Verification
2 queries + 6 mutations preserved (`0 ✅ | 8 🔜 | 0 ⏭`). `SPARK_` prefixes dropped; `VMM_` kept.
**Watch:** the `getProductDetailsElastic` resolver reads a `types` arg **not** declared in the SDL —
either add it to the schema or drop it on the port (default: drop, confirm with consumers).
**Asymmetric input:** `workspaceContext` is `[String]` on **create** but a
`PartialWorkspaceAssociationsInput` object on **update** — preserved exactly.

## 3. Federation Boundaries

> **Monorepo:** `productDetails` is the **same `plm-product` subgraph** as product/measurement/bom/etc.
> References among them are **internal types**, not federation. See
> [reference-federation-patterns.md §0](../scripts/reference-federation-patterns.md).

- **Owns** `ProductDetails`, `ProductDetailsItem`, `ProductDetailsCategoryWithSection`, `ProductDetailsPaged`.
- **Internal (same subgraph — NOT federation):** `Product` (`product` field), `specificationsTemplate`
  (`subCategories` master data), `ProductComponentStatus`, `VersionableId`.
- **External (true federation stubs):** `attachment` (search + clone + archive), `workspace`,
  `user-profile` (`createdBy`/`updatedBy`/participants), `access-control`, `search` (elastic), platform `VMM`.
- **Contributes back** to `Product` → **internal** `productDetails` field resolver (co-located, Phase F).

## 4. Migration Approach  *(Confluence approach page)*

ProductDetails (the backend "construction" set) is a **mid-size, mid-low-risk** domain — no polymorphism.

1. **Phase A:** schema + `ProductDetailsService` port (base `construction/v1`). Preserve the create
   error-contract (throw on `validationErrors`/`message`) and the `{content}` wrap on component-status.
2. **Phase B/C:** the 2 reads — `getProductDetailsById` (internal) and `getProductDetailsElastic`
   (🔴 search, `parentId:` query).
3. **Phase D:** simple mutations — create, access, lock/unlock, clone-files (🔴 attachment), component-status.
4. **Phase E:** `updateProductDetailsSet` — the **multi-step** write (workspace assoc → attachment archive
   → body). Choose a failure strategy (saga / compensation / best-effort).
5. **Phase F:** `Product.productDetails` — **internal** field resolver (co-located), not gateway federation.
6. **Phase G:** field resolvers (ACL/permissions, attachment-by-search, partners/workspaces/users,
   category subCategories) + the test/parity harness.

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `updateProductDetailsSet` multi-step partial failure (E01) | Medium | High | Saga / compensation log — decision required | Tech Lead + PO |
| `updateProductDetailComponentStatus` has no auth token (D05) | Low | Medium | Confirm backend enforces; document | PO |
| Attachment-by-search field resolvers (perf) | Low | Medium | Shared search helper; batch where possible | Backend Eng |
| `getProductDetailsElastic` `types` arg drift | Low | Low | Drop or add to schema; confirm consumers | Backend Eng |
| Sibling refs (attachment/workspace/user-profile/VMM) need gateway stubs | Medium | Low | Standard federation sequencing | Platform |

## 6. ACL Handling
Reads/writes curry a capability token via `getUserPermissionsJWT` (resource-scoped — the backend authorizes
per construction set). **ACL is ignored in the DGS implementation** (no ACL story) — context only.

## 7. Open Questions
1. `updateProductDetailsSet` failure strategy?
2. `updateProductDetailComponentStatus` — backend-enforced without a token?
3. `getProductDetailsElastic.types` — add to schema or drop?
4. Are the 2 unused version service methods needed cross-domain?

---
**Phase Completed:** Phase 3 · **Domain:** `productDetails`.
