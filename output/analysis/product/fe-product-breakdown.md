# Federated GraphQL Breakdown — Product · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (host)` |
| **Total FE Stories** | 12 |
| **Impact** | 🔴 3 High · 🟡 9 Medium · 🟢 0 Low |
| **Estimated effort** | 66–102 days (single-engineer) |
| **Phase-1 surface** | 66 operation-to-root-field rows · 20 client files · 48 components |
| **Generated** | 2026-07-18 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Product** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (host)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `PRODUCT-FE-001` | Migrate `getProduct` documents in product-queries | Query migration | 🔴 High | 10–15 days | `PRODUCT-BE-B-01` | `getProduct` |
| `PRODUCT-FE-002` | Migrate shared-library `getProduct` consumers | Query migration | 🟡 Medium | 5–8 days | `PRODUCT-BE-B-01`, `PRODUCT-BE-B-04`, `PRODUCT-FE-001` | `getProduct`, `getProductVersions` |
| `PRODUCT-FE-003` | Migrate product list and bulk reads | Query migration | 🔴 High | 8–12 days | `PRODUCT-BE-S-02`, `PRODUCT-BE-B-02` | `getProducts`, `getProductsByIds` |
| `PRODUCT-FE-004` | Migrate product status and workspace-context reads | Query migration | 🟡 Medium | 5–8 days | `PRODUCT-BE-B-03` | `getProductStatus` |
| `PRODUCT-FE-005` | Migrate template library and categories reads | Query migration | 🟡 Medium | 5–8 days | `PRODUCT-BE-C-02`, `PRODUCT-BE-C-03` | `getProductTemplates`, `getCategories` |
| `PRODUCT-FE-006` | Migrate product rules administration | Query + mutation migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-B-07`, `PRODUCT-BE-B-08`, `PRODUCT-BE-B-09`, `PRODUCT-BE-B-10`, `PRODUCT-BE-B-11`, `PRODUCT-BE-C-05`, `PRODUCT-BE-D-15`, `PRODUCT-BE-D-16`, `PRODUCT-BE-D-17` | `getProductRules`, `getProductRulesById`, `getAllAvailableRules`, `getProductDeptRules`, `getProductBPRules`, `searchProductRules`, `addProductRule`, `updateProductRule`, `deleteProductRule` |
| `PRODUCT-FE-007` | Migrate simple product mutations | Mutation migration | 🟡 Medium | 6–10 days | `PRODUCT-BE-D-01`, `PRODUCT-BE-D-02`, `PRODUCT-BE-D-03`, `PRODUCT-BE-D-04`, `PRODUCT-BE-D-05`, `PRODUCT-BE-D-10`, `PRODUCT-BE-D-13`, `PRODUCT-BE-D-14` | `addProduct`, `addProducts`, `updateProduct`, `bulkUpdateProducts`, `carryForwardProduct`, `updateViewToggle`, `linkProduct`, `unlinkProduct` |
| `PRODUCT-FE-008` | Migrate team and partner assignment mutations | Mutation migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-D-06`, `PRODUCT-BE-D-07`, `PRODUCT-BE-D-12`, `PRODUCT-FE-001` | `addTeamsToProduct`, `addBusinessPartnersToProductWithType`, `updateProductTeamsWorkspaceContext` |
| `PRODUCT-FE-009` | Migrate partner drop/undrop orchestration | Mutation migration (complex) | 🔴 High | 8–12 days | `PRODUCT-BE-S-03`, `PRODUCT-BE-D-09` | `productBusinessPartnerActions`, `updateBusinessPartnerStatuses` |
| `PRODUCT-FE-010` | Migrate TechPack count queries (facade-then-federate) | Query migration (staged) | 🟡 Medium | 4–6 days (step 1) + 4–6 days (step 2) | `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-H-01`, `PRODUCT-BE-H-02`, `PRODUCT-BE-H-03`, `PRODUCT-BE-H-04`, `PRODUCT-BE-H-05` | `getProductTechPackCountV1`, `getProductTechPackBulkCountV1` |
| `PRODUCT-FE-011` | Migrate component status rollups | Query + mutation migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-B-01`, `PRODUCT-BE-D-18`, `PRODUCT-BE-E-02` | `getProduct`, `updateComponentStatus`, `updateComponentStatuses` |
| `PRODUCT-FE-012` | Verify fragment type-conditions, `__typename` logic and cache keys against federated type names | Verification / refactor | 🟡 Medium | 3–5 days | `PRODUCT-BE-F-14` | `cross-cutting (no single operation)` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🔴 `PRODUCT-FE-001`, 🟡 `PRODUCT-FE-004` | `PRODUCT-FE-001` → `PRODUCT-BE-B-01`<br>`PRODUCT-FE-004` → `PRODUCT-BE-B-03` | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `PRODUCT-FE-002`, 🟡 `PRODUCT-FE-005` | `PRODUCT-FE-002` → `PRODUCT-BE-B-01`, `PRODUCT-BE-B-04`<br>`PRODUCT-FE-005` → `PRODUCT-BE-C-02`, `PRODUCT-BE-C-03` | Search & listing — needs backend phase C |
| 3 | 🟡 `PRODUCT-FE-006`, 🟡 `PRODUCT-FE-007`, 🟡 `PRODUCT-FE-008` | `PRODUCT-FE-006` → `PRODUCT-BE-B-07`, `PRODUCT-BE-B-08`, `PRODUCT-BE-B-09`, `PRODUCT-BE-B-10` (+5)<br>`PRODUCT-FE-007` → `PRODUCT-BE-D-01`, `PRODUCT-BE-D-02`, `PRODUCT-BE-D-03`, `PRODUCT-BE-D-04` (+4)<br>`PRODUCT-FE-008` → `PRODUCT-BE-D-06`, `PRODUCT-BE-D-07`, `PRODUCT-BE-D-12` | Writes — needs backend phase D mutations |
| 4 | 🟡 `PRODUCT-FE-010`, 🟡 `PRODUCT-FE-011`, 🟡 `PRODUCT-FE-012` | `PRODUCT-FE-010` → `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-H-01`, `PRODUCT-BE-H-02` (+3)<br>`PRODUCT-FE-011` → `PRODUCT-BE-B-01`, `PRODUCT-BE-D-18`, `PRODUCT-BE-E-02`<br>`PRODUCT-FE-012` → `PRODUCT-BE-F-14` | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `PRODUCT-FE-003`, 🔴 `PRODUCT-FE-009` | `PRODUCT-FE-003` → `PRODUCT-BE-S-02`, `PRODUCT-BE-B-02`<br>`PRODUCT-FE-009` → `PRODUCT-BE-S-03`, `PRODUCT-BE-D-09` | Externally gated — search/read-hub decision |

**Cutover flow:** `PRODUCT-FE-001` → `PRODUCT-FE-004` → `PRODUCT-FE-002` → `PRODUCT-FE-005` → `PRODUCT-FE-006` → `PRODUCT-FE-007` → `PRODUCT-FE-008` → `PRODUCT-FE-010` → `PRODUCT-FE-011` → `PRODUCT-FE-012` → `PRODUCT-FE-003` → `PRODUCT-FE-009`.

---

## Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 1 | 🔴 `PRODUCT-FE-001` (10–15d)<br>🟡 `PRODUCT-FE-004` (5–8d) | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `PRODUCT-FE-002` (5–8d)<br>🟡 `PRODUCT-FE-005` (5–8d) | Search & listing — needs backend phase C |
| 3 | 🟡 `PRODUCT-FE-007` (6–10d)<br>🟡 `PRODUCT-FE-006` (4–6d)<br>🟡 `PRODUCT-FE-008` (4–6d) | Writes — needs backend phase D mutations |
| 4 | 🟡 `PRODUCT-FE-010` (4–6d)<br>🟡 `PRODUCT-FE-011` (4–6d)<br>🟡 `PRODUCT-FE-012` (3–5d) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `PRODUCT-FE-003` (8–12d)<br>🔴 `PRODUCT-FE-009` (8–12d) | Externally gated — search/read-hub decision |

**Elapsed (nominal midpoints):** ~84 FE build days — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-product.md — the combined Backend + Frontend breakdown this section lives in.
