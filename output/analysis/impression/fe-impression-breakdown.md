# Federated GraphQL Breakdown — Impression · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 2 |
| **Impact** | 🔴 0 High · 🟡 0 Medium · 🟢 2 Low |
| **Estimated effort** | 3–5 days (single-engineer) |
| **Phase-1 surface** | 2 operation-to-root-field rows · 2 client files · 4 components |
| **Generated** | 2026-07-21 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Impression** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `IMPRESSION-FE-001` | Migrate `getBomDataAndImpressions` (with BOM wave) | Query migration | 🟢 Low | 2–3 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-17`, `BOM-FE-002`, `IMPRESSION-BE-B-01`, `IMPRESSION-BE-G-01`, `PRODUCT-BE-B-01` | `searchImpressionsByProductId`, `getBomByIds` |
| `IMPRESSION-FE-002` | Migrate `getCarryForwardFormData` (with Product wave) | Query migration | 🟢 Low | 1–2 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-17`, `IMPRESSION-BE-B-01`, `IMPRESSION-BE-G-01`, `PRODUCT-BE-B-01`, `PRODUCT-BE-G-01`, `PRODUCT-BE-G-02`, `PRODUCT-BE-G-03`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-08`, `PRODUCT-BE-G-09`, `PRODUCT-BE-G-10`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-01`, `PRODUCT-FE-001` | `searchImpressionsByProductId`, `getProduct` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 4 | 🟢 `IMPRESSION-FE-001` | `IMPRESSION-FE-001` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01` (+9) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🟢 `IMPRESSION-FE-002` | `IMPRESSION-FE-002` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01` (+19) | Externally gated — search/read-hub decision |

**Cutover flow:** `IMPRESSION-FE-001` → `IMPRESSION-FE-002`.

---

## Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 4 | 🟢 `IMPRESSION-FE-001` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🟢 `IMPRESSION-FE-002` (1–2d) | Externally gated — search/read-hub decision |

**Elapsed (nominal midpoints):** ~4 FE build days — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-impression.md — the combined Backend + Frontend breakdown this section lives in.
