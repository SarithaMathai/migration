# Federated GraphQL Breakdown — Claims · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `spark-claims (separate)` |
| **Total FE Stories** | 4 |
| **Impact** | 🔴 2 High · 🟡 2 Medium · 🟢 0 Low |
| **Estimated effort** | 17–27 days (single-engineer) |
| **Phase-1 surface** | 18 operation-to-root-field rows · 6 client files · 8 components |
| **Generated** | 2026-07-17 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Claims** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `spark-claims (separate)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `CLAIM-FE-001` | Split the claim fragment factory and re-target claim fragments | Refactor | 🟡 Medium | 2–3 days | — | — |
| `CLAIM-FE-002` | Migrate claim reads (first cross-subgraph cutover) | Query migration | 🔴 High | 6–10 days | `CLAIM-BE-B-01`, `CLAIM-BE-B-02`, `CLAIM-BE-B-03`, `CLAIM-BE-B-04`, `CLAIM-FE-001` | `getClaims`, `getClaimByIds`, `getCommunicationChannels`, `getAllClaimsAbout`, `getClaimComponentStatus` |
| `CLAIM-FE-003` | Migrate claim simple mutations and export | Mutation migration | 🟡 Medium | 4–6 days | `CLAIM-BE-D-01`, `CLAIM-BE-D-02`, `CLAIM-BE-D-03`, `CLAIM-BE-D-04`, `CLAIM-BE-D-05` | `createClaim`, `bulkUpdateClaim`, `lockClaim`, `unlockClaim`, `requestClaimExport` |
| `CLAIM-FE-004` | Migrate `updateClaim` multi-step write handling | Mutation migration (complex) | 🔴 High | 5–8 days | `CLAIM-BE-E-01` | `updateClaim` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟡 `CLAIM-FE-001` | — | Reads cutover — needs backend phase A/B reads live |
| 2 | 🔴 `CLAIM-FE-002` | `CLAIM-FE-002` → `CLAIM-BE-B-01`, `CLAIM-BE-B-02`, `CLAIM-BE-B-03`, `CLAIM-BE-B-04` | Search & listing — needs backend phase C |
| 3 | 🟡 `CLAIM-FE-003` | `CLAIM-FE-003` → `CLAIM-BE-D-01`, `CLAIM-BE-D-02`, `CLAIM-BE-D-03`, `CLAIM-BE-D-04` (+1) | Writes — needs backend phase D mutations |
| 4 | 🔴 `CLAIM-FE-004` | `CLAIM-FE-004` → `CLAIM-BE-E-01` | Complex writes / sagas — needs backend phase E + ADR ratification |

**Cutover flow:** `CLAIM-FE-001` → `CLAIM-FE-002` → `CLAIM-FE-003` → `CLAIM-FE-004`.

---

## Recommended Story Graph — 2 Frontend Engineers

> The order map above packed onto **two frontend engineers**. Lanes re-sync at each step because the step's **backend gate** — not engineer availability — is the limiter; in a single-story step the second engineer pairs on parity checks/rollout or pre-pulls the next unblocked story. FE→FE chains stay with one engineer for context.

| Step | 👤 FE-1 | 👤 FE-2 | Backend gate (focus) |
|---|---|---|---|
| 1 | 🟡 `CLAIM-FE-001` (2–3d) | — | Reads cutover — needs backend phase A/B reads live |
| 2 | 🔴 `CLAIM-FE-002` (6–10d) | — | Search & listing — needs backend phase C |
| 3 | 🟡 `CLAIM-FE-003` (4–6d) | — | Writes — needs backend phase D mutations |
| 4 | 🔴 `CLAIM-FE-004` (5–8d) | — | Complex writes / sagas — needs backend phase E + ADR ratification |

**Elapsed (nominal midpoints):** ~22 FE build days with 2 engineers vs ~22 single-engineer — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-BE-claims.md — the backend breakdown this cutover follows.
