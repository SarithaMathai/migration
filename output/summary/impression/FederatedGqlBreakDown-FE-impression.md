# Federated GraphQL Breakdown — Impression · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 2 |
| **Impact** | 🔴 0 High · 🟡 0 Medium · 🟢 2 Low |
| **Estimated effort** | 3–5 days (single-engineer) |
| **Phase-1 surface** | 2 operation-to-root-field rows · 2 client files · 4 components |
| **Generated** | 2026-07-16 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Impression** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `IMPRESSION-FE-001` | Migrate `getBomDataAndImpressions` (with BOM wave) | Query migration | 🟢 Low | 2–3 days | `IMPRESSION-BE-B-01`, `BOM-BE-B-01`, `BOM-FE-002` | `searchImpressionsByProductId`, `getBomByIds` |
| `IMPRESSION-FE-002` | Migrate `getCarryForwardFormData` (with Product wave) | Query migration | 🟢 Low | 1–2 days | `IMPRESSION-BE-B-01`, `PRODUCT-BE-B-01`, `PRODUCT-FE-001` | `searchImpressionsByProductId`, `getProduct` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟢 `IMPRESSION-FE-001`, 🟢 `IMPRESSION-FE-002` | `IMPRESSION-FE-001` → `IMPRESSION-BE-B-01`, `BOM-BE-B-01`, `BOM-FE-002`<br>`IMPRESSION-FE-002` → `IMPRESSION-BE-B-01`, `PRODUCT-BE-B-01`, `PRODUCT-FE-001` | Reads cutover — needs backend phase A/B reads live |

**Cutover flow:** `IMPRESSION-FE-001` → `IMPRESSION-FE-002`.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-BE-impression.md — the backend breakdown this cutover follows.
