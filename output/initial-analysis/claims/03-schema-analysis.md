# Phase 3: Federation Schema Analysis — Claims

> **Domain:** `claims` · **Target DGS:** separate `claims` subgraph (repo `spark-claims`)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 13 🔜 | 0 ⏭ — 13 operations**

- The target schema is translated from the source SDL (`schemas/SPARK_Claims.graphqls`), verified against the resolver.
- **Claims is its own subgraph** — every reference to Product/search/workspace/user-profile/VMM is cross-subgraph.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `Claims` (**key `humanId`** — SDL has no `id` field) |
| Owned value types | 7 | `ClaimDetails`, `ParentDetails`, `ClaimSubstantiate`, `ClaimPackagingCopy`, `ClaimExport`, `Guest_Facing`, `CommunicationChannel` |
| `@shareable` | 1 | `CodeDescription` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — sibling/other DGS | 8 | `Product`, `WorkspaceV2`, `UserProfileAttributes`, `UserGroup_Participants`, `AccessControl`, `ResourcePermissions`, `ProductComponentStatus`, `TeamPaged` |
| Inputs | ~9 | `ClaimsInput`, `ClaimsUpdateInput`, `BulkClaimsUpdateInput`, `PartnerDetails`, … |

No interfaces / unions — no `@DgsTypeResolver` needed.

## 2. Client Contract Verification
7 queries + 6 mutations preserved (`0 ✅ | 13 🔜 | 0 ⏭`). `SPARK_` prefixes dropped; `VMM_` kept.
**Entity key:** `Claims` is keyed on **`humanId`** (the SDL exposes no `id` field; the resolver uses
`humanId` for every ACL/lookup). Do **not** synthesize an `id`.
**Asymmetric input:** `workspaceContext` is `[ID]` on **create** but a `PartialWorkspaceAssociationsInput`
object on **update** — preserved.

## 3. Federation Boundaries

> **Separate subgraph:** unlike bom/measurement/productDetails, `claims` is **not** in the plm-product
> monorepo. All its cross-references are **true federation** (or gateway stitch for platforms).

- **Owns** `Claims` + the 7 value types.
- **External (federation):** `Product` (`product`, `parentDetails`), `search` (elastic claims + teams),
  `workspace`, `user-profile` (`createdBy`/`updatedBy`/`substantiatedBy`/participants), `access-control`,
  `team` (`TeamPaged`); **gateway stitch:** `VMM` (business/design partners).
- **Contributes back** (Phase F, BLOCKED-BY product): `extend type Product { claims }` (F-01) and the
  TechPack `ResourcesCount.claims` count (F-02 — the claims side of `PRODUCT-BE-F-05`).

## 4. Migration Approach  *(Confluence approach page)*

Claims is a **mid-size, mid risk** domain in its **own subgraph** — no polymorphism, but a proxy-ACL
multi-step update and several federation contributions.

1. **Phase A:** schema + `ClaimService` port (base injected; preserve create/update throw-on-error and the
   `bulkUpdateClaim` `status_code` contract — and **fix** its response transform to camelCase).
2. **Phase B:** the 5 simple reads (incl. 2 cacheable master-data: communication-channels, claims-about).
3. **Phase C:** `searchGuestFacing` (own search) and `getClaimsElastic` (🔴 search).
4. **Phase D:** simple mutations — create, bulk-update, request-export, lock/unlock.
5. **Phase E:** `updateClaim` — **proxy ACL** (`getUserPermissionsJWTByProxy`, basePermissions) + workspace
   association + body + throw. Choose a failure strategy.
6. **Phase F:** contribute `Product.claims` + `ResourcesCount.claims` back to plm-product (federation).
7. **Phase G:** field resolvers (ACL, users, the `businessPartner` 3-way fallback, `ParentDetails` elastic
   team/BP lookups, workspaces, computed `claimName`) + tests.

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `updateClaim` proxy-ACL multi-step partial failure (E-01) | Medium | High | Saga / compensation — decision required | Tech Lead + PO |
| `bulkUpdateClaim` response transform is `deepToSnakeCase` (likely bug) | Medium | Medium | Fix to camelCase; parity test | Backend Eng |
| `ParentDetails.systemTeams` elastic query from BPs (perf/empty) | Low | Medium | Preserve empty→`{content:[]}`; paginate | Backend Eng |
| `businessPartner` 3-way fallback easy to get wrong | Low | Medium | Preserve incl. `{bpId:0,bpName:'Target'}`; unit-test each branch | Backend Eng |
| Federation contributions wait on product | Low | Low | F-01/F-02 post-launch | Product Owner |

## 6. ACL Handling
- Reads/writes curry capability tokens; `updateClaim` uses the **proxy** variant (`getUserPermissionsJWTByProxy`, `basePermissions:true`, `proxyIds:[parentId]`) — the external/proxy path (+1 complexity).
- **ACL is ignored in the DGS implementation** (no ACL story) — context only.

## 7. Open Questions
1. `updateClaim` failure strategy (proxy ACL + workspace + body)?
2. `bulkUpdateClaim` — confirm the response should be camelCase (current code snake-cases it).
3. Are the 2 unused version service methods needed cross-domain?

---
**Phase Completed:** Phase 3 · **Domain:** `claims`.
