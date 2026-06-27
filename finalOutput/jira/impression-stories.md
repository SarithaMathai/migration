# impression — Jira stories (paste one block per issue)

> **Epic:** Impression → plm-product DGS migration  ·  **Labels:** `dgs-migration`, `impression`, `<type>`
> Create the Epic first, then paste each block below as a new Story's description.
> Story points are AI-derived from complexity (confirm in refinement). See [README.md](./README.md).

## SPARK-IMP-A01 · Schema skeleton + DateTime scalar
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** —
**Labels:** `dgs-migration`, `impression`, `schema`

**As a** DGS migration engineer **I want** the `impression.graphqls` skeleton + `DateTime` scalar **so that**
later impression work compiles on a stable base.
**Current Behaviour:** green-field; schema translated from `code/schemas/SPARK_Impression.txt`.
**Target DGS Implementation:** federation v2.3 header, `scalar DateTime → Instant`, empty `extend type Query`/`Mutation`.
**Files:** `schema/impression.graphqls`, `config/ScalarConfig.kt`. **Dependencies:** None.
**Acceptance Criteria:** 1. `./gradlew generateJava` passes. 2. `DateTime` round-trips ISO-8601.
**Test Cases:** ☐ Unit: schema compiles ☐ Unit: DateTime serde.

---

## SPARK-IMP-A02 · Owned types + inputs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-A01
**Labels:** `dgs-migration`, `impression`, `schema`

**As a** DGS migration engineer **I want** `Impression`, `ImpressionCount`, `CountsByBp` and the 3 inputs
defined **so that** resolvers/mutations have a contract.
**Current Behaviour:** see [03-schema.graphql](./03-schema.graphql).
**Target DGS Implementation:** add the types; `@key(fields:"id")` on `Impression`; `@shareable` on `CountsByBp`.
**Files:** `schema/impression.graphqls`. **Dependencies:** A01.
**Acceptance Criteria:** 1. All owned types + inputs present. 2. `@key` only on `Impression`. 3. Schema validates.
**Test Cases:** ☐ Unit: schema validates ☐ Unit: `Impression` entity stub resolves.

---

## SPARK-IMP-A03 · External stubs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-A01
**Labels:** `dgs-migration`, `impression`, `schema`

**Current Behaviour:** references `VMM_BusinessPartner`, `Product`, `WorkspaceV2`, `UserProfileAttributes`.
**Target DGS Implementation:** add each as `@extends @key(fields:"id") { id: ID! @external }`.
**Files:** `schema/impression.graphqls`. **Dependencies:** A01.
**Acceptance Criteria:** 1. 4 stubs compile; gateway composes without conflict.
**Test Cases:** ☐ Unit: compiles ☐ Integration: gateway resolves a `VMM_BusinessPartner` stub.

---

## SPARK-IMP-A04 · ImpressionService Kotlin port (2 methods)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-A01
**Labels:** `dgs-migration`, `impression`, `service`

**Current Behaviour (S1):** base `…/impressions/product`. `searchImpressionsByProductId` →
`GET /{productId}?workspaceIds=&partnerIds=` (repeated params from arrays); `updateImpressions` →
`PUT /{productId}` (snake_case request, camelCase response). **ACL note (context):** both curry a capability
token because impressions are product-scoped; ignored in DGS.
**Target DGS Implementation:** `ImpressionClient` Feign (GET + PUT) + `ImpressionService`. Build the GET query
string by repeating `workspaceIds`/`partnerIds`. Jackson snake/camel.
**Files:** `service/ImpressionService.kt`, `client/ImpressionClient.kt`, `model/ImpressionDto.kt`. **Dependencies:** A01.
**Acceptance Criteria:** 1. GET builds repeated `workspaceIds`/`partnerIds` params. 2. PUT sends snake_case, maps camelCase response. 3. Both signatures present.
**Test Cases:** ☐ Unit: GET query-string build ☐ Unit: snake/camel mapping.

---

## SPARK-IMP-B01 · searchImpressionsByProductId data fetcher
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-A02, SPARK-IMP-A04
**Labels:** `dgs-migration`, `impression`, `query`

**Current Behaviour (Q1):** `GET {base}/…/impressions/product/{id}?workspaceIds=&partnerIds=` → camelCase list.
`enableWorkspaceContextFiltering` is accepted but **not forwarded** to the service today — confirm intended.
**ACL note (context):** capability token for `id`; ignored in DGS.
**Target DGS Implementation:** `@DgsQuery searchImpressionsByProductId(id, partnerIds, workspaceIds, enableWorkspaceContextFiltering): List<Impression>` → `impressionService.searchByProductId(...)`. Decide whether to wire `enableWorkspaceContextFiltering` to the backend.
**Files:** `dataFetcher/ImpressionQueryDataFetcher.kt`. **Dependencies:** A02, A04.
**Acceptance Criteria:** 1. Returns impressions for `id` with optional partner/workspace filters. 2. `enableWorkspaceContextFiltering` behaviour documented (forwarded or intentionally ignored). 3. Empty → `[]`.
**Test Cases:** ☐ Unit: filters in query string ☐ Unit: empty ☐ Integration.

---

## SPARK-IMP-B02 · getImpressionCountsByProductId data fetcher
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-A02, SPARK-IMP-A04
**Labels:** `dgs-migration`, `impression`, `query`

**Current Behaviour (Q2):** reuses the same REST search call for `id`; returns the impressions list typed as
`ImpressionCount`; the `ImpressionCount.counts` field (G02) aggregates.
**Target DGS Implementation:** `@DgsQuery getImpressionCountsByProductId(id): ImpressionCount` → returns the
impressions list as the parent for `counts`. **PO decision:** preserve this contract, or switch to a typed
`ImpressionCountResult` computed in the fetcher (see 03-analysis).
**Files:** `dataFetcher/ImpressionQueryDataFetcher.kt`. **Dependencies:** A02, A04.
**Acceptance Criteria:** 1. Returns the impressions list as the `ImpressionCount` parent. 2. Contract decision recorded. 3. Empty product → `counts` yields `totalCount: 0` (see G02).
**Test Cases:** ☐ Unit: returns list-as-parent ☐ Integration: `{ counts { bpType counts } }`.

---

## SPARK-IMP-D01 · updateImpressions mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-IMP-A04
**Labels:** `dgs-migration`, `impression`, `mutation`

**Current Behaviour (M1):** `PUT {base}/…/impressions/product/{productId}` with `{impressionsToDelete, impressionsToUpdate}` (snake_case); on `validationErrors || message` → throw. **ACL note (context):** capability token for `productId`; ignored in DGS.
**Target DGS Implementation:** `@DgsMutation updateImpressions(productId, productImpression): List<Impression>`
→ `impressionService.update(...)`; map camelCase↔snake_case; on `validationErrors`/`message` → typed
`ImpressionValidationException`.
**Files:** `dataFetcher/ImpressionMutationDataFetcher.kt`. **Dependencies:** A04.
**Acceptance Criteria:** 1. PUT sends delete + update sets snake_case. 2. Returns updated impressions camelCase. 3. Backend `validationErrors`/`message` → exception (not silent return).
**Test Cases:** ☐ Unit: request shape ☐ Unit: validationErrors → exception ☐ Integration.

---

## SPARK-IMP-F01 · Implement Product.impressions/impressionCounts (internal, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-A04
**Labels:** `dgs-migration`, `impression`, `field-resolver`

**Monorepo:** `product` and `impression` are the same `plm-product` subgraph — this is an **internal** field
resolver, not gateway federation.
**Current Behaviour:** product navigates to impressions via the impression search call.
**Target DGS Implementation:** plain `@DgsData` fields on the internal `Product` type for
`impressions(partnerIds, workspaceIds)` and `impressionCounts` → in-process `impressionService` calls.
**No** `@DgsEntityFetcher`/`@extends @external`. Depends on `Product` existing (product A02).
**Acceptance Criteria:** 1. `Product.impressions/impressionCounts` resolve internally via `impressionService`. 2. no gateway hop. 3. Parity vs current product-side resolver.
**Test Cases:** ☐ Unit: calls impression service ☐ Integration: `Product { impressions { id } }` in-process ☐ Parity.

---

## SPARK-IMP-G01 · Impression field resolvers (5)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-A02, SPARK-IMP-A04
**Labels:** `dgs-migration`, `impression`, `field-resolver`

**Current Behaviour (F1–F5):** `businessPartners` (`loadBpsWithType(partnerIds.map(p=>({partnerId:p})))`),
`owningBusinessPartner` (`loadBp(owningPartnerId)`), `workspaces` (`getWorkspacesByIdsV2(workspaceContext)` or `[]`),
`createdBy`/`updatedBy` (`userAttributes.getUserByID.load(...)`).
**EXT:** 🟡 workspaceV2; 🔵 vmm; 🔵 user-profile.
**Target DGS Implementation:** 5 `@DgsData` fields resolving via federated references / clients.
`workspaces` → `[]` when `workspaceContext` empty.
**Files:** `dataFetcher/ImpressionFieldDataFetcher.kt`. **Dependencies:** A02, A04.
**Acceptance Criteria:** 1. partners resolve from `partnerIds`/`owningPartnerId`. 2. `workspaces` empty → `[]`. 3. `createdBy`/`updatedBy` resolve by user id (null id → null).
**Test Cases:** ☐ Unit: partners mapping ☐ Unit: empty workspaces ☐ Unit: null user id ☐ Integration: federated `Impression { createdBy { id } }`.

---

## SPARK-IMP-G02 · ImpressionCount.counts aggregation
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-IMP-A02, SPARK-IMP-A04
**Labels:** `dgs-migration`, `impression`, `field-resolver`

**As a** DGS migration engineer **I want** the `counts` aggregation **so that** clients get per-partner +
total impression counts.
**Current Behaviour (F6):** parent = impressions array. `parentId = impressions[0].parentId` →
`product.getByID.load(parentId)` (**internal** same-DGS) → partner ids → per-partner count
`impressions.filter(i => i.partnerIds.includes(partnerId)).length` → append `{bpType:'totalCount', counts: impressions.length}`.
On any error → log + return `[{bpType:'totalCount', counts:0}]`.
**Target DGS Implementation:** `@DgsData counts` computing the per-partner + total rows; product via internal
`productService.getById`. Preserve the try/catch fallback. **PO note:** consider `ImpressionCountResult`
restructure (03-analysis) — if adopted, this becomes a fetcher computation, not a field-on-array.
**Files:** `dataFetcher/ImpressionCountFieldDataFetcher.kt`. **Dependencies:** A02, A04.
**Acceptance Criteria:** 1. One row per product partner with the correct count + a `totalCount` row. 2. Empty/missing product → `[{bpType:'totalCount', counts:0}]` (no exception thrown). 3. Product fetched internally (no HTTP hop).
**Test Cases:** ☐ Unit: per-partner counts ☐ Unit: totalCount row ☐ Unit: error → dummy 0 ☐ Integration.

---

## SPARK-IMP-G03 · Test coverage & parity
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-IMP-B01, SPARK-IMP-B02, SPARK-IMP-D01, SPARK-IMP-G02
**Labels:** `dgs-migration`, `impression`, `tests`

**Target DGS Implementation:** ≥80% unit coverage; parity fixtures for both queries + the mutation +
`counts` (incl. the error→0 path).
**Acceptance Criteria:** 1. Unit ≥80%. 2. Parity green for search/counts/update. 3. `counts` error path covered.
**Test Cases:** ☐ Parity: search/counts/update ☐ Unit: counts error path ☐ Load: p95 parity for search.

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `ImpressionCount` array-as-parent contract (empty list) | Low | Low | Preserve fallback; consider `ImpressionCountResult` | Architect |
| `enableWorkspaceContextFiltering` not forwarded | Low | Low | Confirm intent (B01) | Backend Eng |
| F01 internal (same subgraph) — depends on Product type existing | Low | Low | Sequence after product A02; no gateway block | Tech Lead |

## 5. Summary
- **Stories:** 11 (A:4 · B:2 · D:1 · F:1 · G:3). **No High/Very-High** beyond the small `counts` aggregation.
- **Lowest-risk domain — recommended first migration / team warm-up.**
- **Independent of federation:** ships before F01.

---
**Phase Completed:** Phase 4 · **Domain:** `impression`.

---
