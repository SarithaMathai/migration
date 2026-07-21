# Federated GraphQL Breakdown — BOM · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 7 |
| **Impact** | 🔴 4 High · 🟡 1 Medium · 🟢 2 Low |
| **Estimated effort** | 29–46 days (single-engineer) |
| **Phase-1 surface** | 21 operation-to-root-field rows · 4 client files · 7 components |
| **Generated** | 2026-07-19 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **BOM** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `BOM-FE-001` | Statically expand BOM fragment factories (pre-cutover) | Refactor | 🔴 High | 3–4 days | — | — |
| `BOM-FE-002` | Migrate BOM core reads | Query migration | 🔴 High | 6–10 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-17`, `BOM-FE-001` | `getBomByIds`, `getBomByParentId`, `getBomStatus`, `getBomComponentStatus` |
| `BOM-FE-003` | Migrate BOM search and elastic reads | Query migration | 🔴 High | 5–8 days | `BOM-BE-C-01`, `BOM-BE-G-01`, `BOM-BE-G-14`, `BOM-BE-S-03` | `getBomElastic`, `searchMaterialsBom` |
| `BOM-FE-004` | Migrate BOM master-data reads | Query migration | 🟢 Low | 2–3 days | `BOM-BE-B-05`, `BOM-BE-B-06`, `BOM-BE-B-07`, `BOM-BE-B-08`, `BOM-BE-G-14` | `getBomMaterialTypes`, `getBomPackagingMaterialTypes`, `getBomPackagingSubstrates`, `getBomPackagingUnitOfMeasure` |
| `BOM-FE-005` | Migrate BOM supplier reads | Query migration | 🟡 Medium | 3–5 days | `BOM-BE-C-03`, `BOM-BE-C-04`, `BOM-BE-C-05` | `getComboSupplierForBom`, `getValidTrimSuppliersForBom`, `getValidRawMaterialSuppliersForBom` |
| `BOM-FE-006` | Migrate BOM mutations including `updateBom` saga handling | Mutation migration (complex) | 🔴 High | 8–12 days | `BOM-BE-D-01`, `BOM-BE-D-03`, `BOM-BE-D-04`, `BOM-BE-D-05`, `BOM-BE-S-01` | `addBom`, `lockBom`, `unlockBom`, `updateBom`, `updateBomComponentStatus` |
| `BOM-FE-007` | Adopt BOM `supplier` entity references (optional, PO-gated) | Query enhancement | 🟢 Low | 2–4 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-14`, `BOM-BE-G-17`, `BOM-BE-S-03`, `BOM-FE-002` | `getBomByIds`, `getBomByParentId`, `searchMaterialsBom` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🔴 `BOM-FE-001` | — | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `BOM-FE-005` | `BOM-FE-005` → `BOM-BE-C-03`, `BOM-BE-C-04`, `BOM-BE-C-05` | Search & listing — needs backend phase C |
| 4 | 🔴 `BOM-FE-002`, 🟢 `BOM-FE-004` | `BOM-FE-002` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04` (+6)<br>`BOM-FE-004` → `BOM-BE-B-05`, `BOM-BE-B-06`, `BOM-BE-B-07`, `BOM-BE-B-08` (+1) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `BOM-FE-003`, 🔴 `BOM-FE-006`, 🟢 `BOM-FE-007` | `BOM-FE-003` → `BOM-BE-C-01`, `BOM-BE-G-01`, `BOM-BE-G-14`, `BOM-BE-S-03`<br>`BOM-FE-006` → `BOM-BE-D-01`, `BOM-BE-D-03`, `BOM-BE-D-04`, `BOM-BE-D-05` (+1)<br>`BOM-FE-007` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04` (+8) | Externally gated — search/read-hub decision |

**Cutover flow:** `BOM-FE-001` → `BOM-FE-005` → `BOM-FE-002` → `BOM-FE-004` → `BOM-FE-003` → `BOM-FE-006` → `BOM-FE-007`.

---

## Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 1 | 🔴 `BOM-FE-001` (3–4d) | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `BOM-FE-005` (3–5d) | Search & listing — needs backend phase C |
| 4 | 🔴 `BOM-FE-002` (6–10d)<br>🟢 `BOM-FE-004` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `BOM-FE-006` (8–12d)<br>🔴 `BOM-FE-003` (5–8d)<br>🟢 `BOM-FE-007` (2–4d) | Externally gated — search/read-hub decision |

**Elapsed (nominal midpoints):** ~38 FE build days — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-bom.md — the combined Backend + Frontend breakdown this section lives in.
