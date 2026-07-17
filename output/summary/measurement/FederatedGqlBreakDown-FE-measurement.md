# Federated GraphQL Breakdown — Measurement · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 4 |
| **Impact** | 🔴 0 High · 🟡 3 Medium · 🟢 1 Low |
| **Estimated effort** | 12–19 days (single-engineer) |
| **Phase-1 surface** | 13 operation-to-root-field rows · 4 client files · 7 components |
| **Generated** | 2026-07-17 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Measurement** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `MST-FE-001` | Migrate measurement reads and retire `humanId` | Query migration | 🟡 Medium | 4–6 days | `MST-BE-B-01`, `MST-BE-B-02` | `getMeasurementByIds`, `getMeasurementSetStatus`, `getMeasurementComponentStatus` |
| `MST-FE-002` | Migrate measurement list/search reads | Query migration | 🟡 Medium | 3–5 days | `MST-BE-C-01`, `MST-BE-C-02` | `getMeasurements`, `getMeasurementsElastic` |
| `MST-FE-003` | Migrate measurement master-data reads | Query migration | 🟢 Low | 1–2 days | `MST-BE-B-02` | `getUnitsOfMeasure`, `getThicknessUnitsOfMeasure` |
| `MST-FE-004` | Migrate measurement mutations | Mutation migration | 🟡 Medium | 4–6 days | `MST-BE-D-02`, `MST-BE-D-06`, `MST-BE-D-07` | `lockMeasurementSet`, `unlockMeasurementSet`, `putSampleMeasurementSet`, `deleteSampleMeasurementSet` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟡 `MST-FE-001`, 🟢 `MST-FE-003` | `MST-FE-001` → `MST-BE-B-01`, `MST-BE-B-02`<br>`MST-FE-003` → `MST-BE-B-02` | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `MST-FE-002` | `MST-FE-002` → `MST-BE-C-01`, `MST-BE-C-02` | Search & listing — needs backend phase C |
| 3 | 🟡 `MST-FE-004` | `MST-FE-004` → `MST-BE-D-02`, `MST-BE-D-06`, `MST-BE-D-07` | Writes — needs backend phase D mutations |

**Cutover flow:** `MST-FE-001` → `MST-FE-003` → `MST-FE-002` → `MST-FE-004`.

---

## Recommended Story Graph — 2 Frontend Engineers

> The order map above packed onto **two frontend engineers**. Lanes re-sync at each step because the step's **backend gate** — not engineer availability — is the limiter; in a single-story step the second engineer pairs on parity checks/rollout or pre-pulls the next unblocked story. FE→FE chains stay with one engineer for context.

| Step | 👤 FE-1 | 👤 FE-2 | Backend gate (focus) |
|---|---|---|---|
| 1 | 🟡 `MST-FE-001` (4–6d) | 🟢 `MST-FE-003` (1–2d) | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `MST-FE-002` (3–5d) | — | Search & listing — needs backend phase C |
| 3 | 🟡 `MST-FE-004` (4–6d) | — | Writes — needs backend phase D mutations |

**Elapsed (nominal midpoints):** ~14 FE build days with 2 engineers vs ~16 single-engineer — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-BE-measurement.md — the backend breakdown this cutover follows.
