# Federated GraphQL Breakdown — Packaging · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 5 |
| **Impact** | 🔴 1 High · 🟡 3 Medium · 🟢 1 Low |
| **Estimated effort** | 21–33 days (single-engineer) |
| **Phase-1 surface** | 21 operation-to-root-field rows · 5 client files · 8 components |
| **Generated** | 2026-07-17 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Packaging** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `PKG-FE-001` | Migrate packaging reads | Query migration | 🟡 Medium | 5–8 days | `PKG-BE-B-01`, `PKG-BE-B-02` | `getPackagings`, `getPackagingById`, `getPackagingComponentStatus` |
| `PKG-FE-002` | Migrate packaging master-data reads and retire deprecated fields | Query migration | 🟢 Low | 2–3 days | `PKG-BE-B-02`, `PKG-BE-B-06` | `getCountries`, `getPackagingFieldValuesByType` |
| `PKG-FE-003` | Migrate dieline flows | Query + mutation migration | 🟡 Medium | 4–6 days | `PKG-BE-B-02`, `PKG-BE-D-02` | `getDielines`, `getDielineEvaluationStatuses`, `evaluateDieline` |
| `PKG-FE-004` | Migrate packaging simple mutations and export | Mutation migration | 🟡 Medium | 5–8 days | `PKG-BE-D-01`, `PKG-BE-D-03`, `PKG-BE-D-04`, `PKG-BE-D-02`, `PKG-BE-D-09` | `addPackaging`, `bulkAddPackagings`, `bulkUpdatePackagings`, `exportPackaging`, `lockPackaging`, `unlockPackaging`, `updatePackagingComponentStatus` |
| `PKG-FE-005` | Migrate `updatePackaging` saga handling and packet information | Mutation migration (complex) | 🔴 High | 5–8 days | `PKG-BE-E-01` | `updatePackaging`, `getPackagingPacketsInformation`, `getPackagingPacketInformation` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟡 `PKG-FE-001`, 🟢 `PKG-FE-002` | `PKG-FE-001` → `PKG-BE-B-01`, `PKG-BE-B-02`<br>`PKG-FE-002` → `PKG-BE-B-02`, `PKG-BE-B-06` | Reads cutover — needs backend phase A/B reads live |
| 3 | 🟡 `PKG-FE-003`, 🟡 `PKG-FE-004` | `PKG-FE-003` → `PKG-BE-B-02`, `PKG-BE-D-02`<br>`PKG-FE-004` → `PKG-BE-D-01`, `PKG-BE-D-03`, `PKG-BE-D-04`, `PKG-BE-D-02` (+1) | Writes — needs backend phase D mutations |
| 4 | 🔴 `PKG-FE-005` | `PKG-FE-005` → `PKG-BE-E-01` | Complex writes / sagas — needs backend phase E + ADR ratification |

**Cutover flow:** `PKG-FE-001` → `PKG-FE-002` → `PKG-FE-003` → `PKG-FE-004` → `PKG-FE-005`.

---

## Recommended Story Graph — 2 Frontend Engineers

> The order map above packed onto **two frontend engineers**. Lanes re-sync at each step because the step's **backend gate** — not engineer availability — is the limiter; in a single-story step the second engineer pairs on parity checks/rollout or pre-pulls the next unblocked story. FE→FE chains stay with one engineer for context.

| Step | 👤 FE-1 | 👤 FE-2 | Backend gate (focus) |
|---|---|---|---|
| 1 | 🟡 `PKG-FE-001` (5–8d) | 🟢 `PKG-FE-002` (2–3d) | Reads cutover — needs backend phase A/B reads live |
| 3 | 🟡 `PKG-FE-004` (5–8d) | 🟡 `PKG-FE-003` (4–6d) | Writes — needs backend phase D mutations |
| 4 | 🔴 `PKG-FE-005` (5–8d) | — | Complex writes / sagas — needs backend phase E + ADR ratification |

**Elapsed (nominal midpoints):** ~20 FE build days with 2 engineers vs ~27 single-engineer — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-BE-packaging.md — the backend breakdown this cutover follows.
