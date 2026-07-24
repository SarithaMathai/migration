# Federated GraphQL Breakdown — Product · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (host)` |
| **Total FE Stories** | 13 |
| **Impact** | 🔴 3 High · 🟡 9 Medium · 🟢 1 Low |
| **Estimated effort** | 68–104 days (single-engineer) |
| **Phase-1 surface** | 66 operation-to-root-field rows · 20 client files · 48 components |
| **Generated** | 2026-07-24 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Product** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (host)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `PRODUCT-FE-001` | Migrate all `getProduct` documents (single root query, 17 flavors) | Query migration | 🔴 High | 13–19 days | `PRODUCT-BE-B-01`, `PRODUCT-BE-F-10`, `PRODUCT-BE-G-01`, `PRODUCT-BE-G-02`, `PRODUCT-BE-G-03`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-08`, `PRODUCT-BE-G-09`, `PRODUCT-BE-G-10`, `PRODUCT-BE-G-13`, `PRODUCT-BE-G-14`, `PRODUCT-BE-S-01`, `PRODUCT-BE-B-04` | `getProduct` |
| `PRODUCT-FE-002` | Migrate `getProducts` documents (list/search/bulk-create) | Query migration | 🔴 High | 6–9 days | `PRODUCT-BE-B-02`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-02` | `getProducts` |
| `PRODUCT-FE-003` | Migrate `getProductsByIds` documents (bulk-by-id reads) | Query migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-B-03` | `getProductsByIds` |
| `PRODUCT-FE-004` | Migrate `getProductStatus` documents | Query migration | 🟡 Medium | 5–8 days | `PRODUCT-BE-B-01`, `PRODUCT-BE-B-02`, `PRODUCT-BE-B-03`, `PRODUCT-BE-F-10`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-09`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-01` | `getProductStatus` |
| `PRODUCT-FE-005` | Migrate `getProductTemplates` documents | Query migration | 🟡 Medium | 6–9 days | `PRODUCT-BE-B-03`, `PRODUCT-BE-C-02`, `PRODUCT-BE-C-03`, `PRODUCT-BE-G-03`, `PRODUCT-BE-G-04`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-08`, `PRODUCT-BE-G-13`, `PRODUCT-BE-G-14`, `PRODUCT-BE-H-07`, `PRODUCT-BE-S-01`, `PRODUCT-BE-S-02` | `getProductTemplates` |
| `PRODUCT-FE-006` | Migrate `getCategories` documents | Query migration | 🟢 Low | 2–3 days | `PRODUCT-BE-G-03`, `PRODUCT-BE-G-13` | `getCategories` |
| `PRODUCT-FE-007` | Migrate product rules administration | Query + mutation migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-B-07`, `PRODUCT-BE-B-08`, `PRODUCT-BE-B-09`, `PRODUCT-BE-B-10`, `PRODUCT-BE-B-11`, `PRODUCT-BE-C-05`, `PRODUCT-BE-D-15`, `PRODUCT-BE-D-16`, `PRODUCT-BE-D-17`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-13`, `PRODUCT-BE-H-08` | `getProductRules`, `getProductRulesById`, `getAllAvailableRules`, `getProductDeptRules`, `getProductBPRules`, `searchProductRules`, `addProductRule`, `updateProductRule`, `deleteProductRule` |
| `PRODUCT-FE-008` | Migrate simple product mutations | Mutation migration | 🟡 Medium | 6–10 days | `PRODUCT-BE-D-01`, `PRODUCT-BE-D-02`, `PRODUCT-BE-D-03`, `PRODUCT-BE-D-04`, `PRODUCT-BE-D-05`, `PRODUCT-BE-D-10`, `PRODUCT-BE-D-13`, `PRODUCT-BE-D-14` | `addProduct`, `addProducts`, `updateProduct`, `bulkUpdateProducts`, `carryForwardProduct`, `updateViewToggle`, `linkProduct`, `unlinkProduct` |
| `PRODUCT-FE-009` | Migrate team and partner assignment mutations | Mutation migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-D-06`, `PRODUCT-BE-D-07`, `PRODUCT-BE-D-12`, `PRODUCT-FE-001` | `addTeamsToProduct`, `addBusinessPartnersToProductWithType`, `updateProductTeamsWorkspaceContext` |
| `PRODUCT-FE-010` | Migrate partner drop/undrop orchestration | Mutation migration (complex) | 🔴 High | 8–12 days | `PRODUCT-BE-S-03`, `PRODUCT-BE-D-09` | `productBusinessPartnerActions`, `updateBusinessPartnerStatuses` |
| `PRODUCT-FE-011` | Migrate TechPack count queries (facade-then-federate) | Query migration (staged) | 🟡 Medium | 4–6 days (step 1) + 4–6 days (step 2) | `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-F-06`, `PRODUCT-BE-F-08`, `PRODUCT-BE-G-08`, `PRODUCT-BE-H-01`, `PRODUCT-BE-H-02`, `PRODUCT-BE-H-03`, `PRODUCT-BE-H-04`, `PRODUCT-BE-H-05` | `getProductTechPackCountV1`, `getProductTechPackBulkCountV1` |
| `PRODUCT-FE-012` | Migrate component status mutations and rollup counts | Mutation migration | 🟡 Medium | 3–5 days | `PRODUCT-BE-D-18`, `PRODUCT-BE-E-02`, `PRODUCT-FE-001` | `updateComponentStatus`, `updateComponentStatuses` |
| `PRODUCT-FE-013` | Verify fragment type-conditions, `__typename` logic and cache keys against federated type names | Verification / refactor | 🟡 Medium | 3–5 days | `PRODUCT-BE-F-14` | `cross-cutting (no single operation)` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟡 `PRODUCT-FE-003` | `PRODUCT-FE-003` → `PRODUCT-BE-B-03` | Reads cutover — needs backend phase A/B reads live |
| 3 | 🟡 `PRODUCT-FE-008` | `PRODUCT-FE-008` → `PRODUCT-BE-D-01`, `PRODUCT-BE-D-02`, `PRODUCT-BE-D-03`, `PRODUCT-BE-D-04` (+4) | Writes — needs backend phase D mutations |
| 4 | 🟢 `PRODUCT-FE-006`, 🟡 `PRODUCT-FE-007`, 🟡 `PRODUCT-FE-011`, 🟡 `PRODUCT-FE-013` | `PRODUCT-FE-006` → `PRODUCT-BE-G-03`, `PRODUCT-BE-G-13`<br>`PRODUCT-FE-007` → `PRODUCT-BE-B-07`, `PRODUCT-BE-B-08`, `PRODUCT-BE-B-09`, `PRODUCT-BE-B-10` (+8)<br>`PRODUCT-FE-011` → `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-F-06`, `PRODUCT-BE-F-08` (+6)<br>`PRODUCT-FE-013` → `PRODUCT-BE-F-14` | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `PRODUCT-FE-001`, 🔴 `PRODUCT-FE-002`, 🟡 `PRODUCT-FE-004`, 🟡 `PRODUCT-FE-005`, 🔴 `PRODUCT-FE-010` | `PRODUCT-FE-001` → `PRODUCT-BE-B-01`, `PRODUCT-BE-F-10`, `PRODUCT-BE-G-01`, `PRODUCT-BE-G-02` (+10)<br>`PRODUCT-FE-002` → `PRODUCT-BE-B-02`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-02`<br>`PRODUCT-FE-004` → `PRODUCT-BE-B-01`, `PRODUCT-BE-B-02`, `PRODUCT-BE-B-03`, `PRODUCT-BE-F-10` (+5)<br>`PRODUCT-FE-005` → `PRODUCT-BE-B-03`, `PRODUCT-BE-C-02`, `PRODUCT-BE-C-03`, `PRODUCT-BE-G-03` (+9)<br>`PRODUCT-FE-010` → `PRODUCT-BE-S-03`, `PRODUCT-BE-D-09` | Externally gated — search/read-hub decision |
| 6 | 🟡 `PRODUCT-FE-009`, 🟡 `PRODUCT-FE-012` | `PRODUCT-FE-009` → `PRODUCT-BE-D-06`, `PRODUCT-BE-D-07`, `PRODUCT-BE-D-12`<br>`PRODUCT-FE-012` → `PRODUCT-BE-D-18`, `PRODUCT-BE-E-02` | Follow-on cutover — after the stories it depends on |

**Cutover flow:** `PRODUCT-FE-003` → `PRODUCT-FE-008` → `PRODUCT-FE-006` → `PRODUCT-FE-007` → `PRODUCT-FE-011` → `PRODUCT-FE-013` → `PRODUCT-FE-001` → `PRODUCT-FE-002` → `PRODUCT-FE-004` → `PRODUCT-FE-005` → `PRODUCT-FE-010` → `PRODUCT-FE-009` → `PRODUCT-FE-012`.

---

## Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 1 | 🟡 `PRODUCT-FE-003` (4–6d) | Reads cutover — needs backend phase A/B reads live |
| 3 | 🟡 `PRODUCT-FE-008` (6–10d) | Writes — needs backend phase D mutations |
| 4 | 🟡 `PRODUCT-FE-007` (4–6d)<br>🟡 `PRODUCT-FE-011` (4–6d)<br>🟡 `PRODUCT-FE-013` (3–5d)<br>🟢 `PRODUCT-FE-006` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `PRODUCT-FE-001` (13–19d)<br>🔴 `PRODUCT-FE-010` (8–12d)<br>🔴 `PRODUCT-FE-002` (6–9d)<br>🟡 `PRODUCT-FE-005` (6–9d)<br>🟡 `PRODUCT-FE-004` (5–8d) | Externally gated — search/read-hub decision |
| 6 | 🟡 `PRODUCT-FE-009` (4–6d)<br>🟡 `PRODUCT-FE-012` (3–5d) | Follow-on cutover — after the stories it depends on |

**Elapsed (nominal midpoints):** ~86 FE build days — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-product.md — the combined Backend + Frontend breakdown this section lives in.
