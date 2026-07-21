# Federated GraphQL Breakdown — Product Details · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 3 |
| **Impact** | 🔴 0 High · 🟡 2 Medium · 🟢 1 Low |
| **Estimated effort** | 8–12 days (single-engineer) |
| **Phase-1 surface** | 7 operation-to-root-field rows · 2 client files · 4 components |
| **Generated** | 2026-07-21 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Product Details** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `PDTL-FE-001` | Migrate product-details reads | Query migration | 🟢 Low | 2–3 days | `PDTL-BE-B-01`, `PDTL-BE-G-01`, `PDTL-BE-G-02`, `PDTL-BE-G-03` | `getProductDetailsById`, `getProductDetailComponentStatus` |
| `PDTL-FE-002` | Migrate product-details simple mutations | Mutation migration | 🟡 Medium | 3–4 days | `PDTL-BE-D-01`, `PDTL-BE-D-03`, `PDTL-BE-D-04`, `PDTL-BE-D-05` | `createProductDetailsSet`, `productDetailLockUnlock`, `cloneFilesForProductDetails`, `updateProductDetailComponentStatus` |
| `PDTL-FE-003` | Migrate `updateProductDetailsSet` saga handling | Mutation migration (complex) | 🟡 Medium | 3–5 days | `PDTL-BE-E-01` | `updateProductDetailsSet` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 3 | 🟡 `PDTL-FE-002` | `PDTL-FE-002` → `PDTL-BE-D-01`, `PDTL-BE-D-03`, `PDTL-BE-D-04`, `PDTL-BE-D-05` | Writes — needs backend phase D mutations |
| 4 | 🟢 `PDTL-FE-001`, 🟡 `PDTL-FE-003` | `PDTL-FE-001` → `PDTL-BE-B-01`, `PDTL-BE-G-01`, `PDTL-BE-G-02`, `PDTL-BE-G-03`<br>`PDTL-FE-003` → `PDTL-BE-E-01` | Complex writes / sagas — needs backend phase E + ADR ratification |

**Cutover flow:** `PDTL-FE-002` → `PDTL-FE-001` → `PDTL-FE-003`.

---

## Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 3 | 🟡 `PDTL-FE-002` (3–4d) | Writes — needs backend phase D mutations |
| 4 | 🟡 `PDTL-FE-003` (3–5d)<br>🟢 `PDTL-FE-001` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |

**Elapsed (nominal midpoints):** ~10 FE build days — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-productDetails.md — the combined Backend + Frontend breakdown this section lives in.
