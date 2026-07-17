# Federated GraphQL Breakdown — Watchlist · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 3 |
| **Impact** | 🔴 0 High · 🟡 1 Medium · 🟢 2 Low |
| **Estimated effort** | 7–10 days (single-engineer) |
| **Phase-1 surface** | 5 operation-to-root-field rows · 1 client files · 4 components |
| **Generated** | 2026-07-17 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

## What Are We Changing?

- Point the **Watchlist** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

## Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `WATCHLIST-FE-001` | Migrate watchlist reads | Query migration | 🟢 Low | 2–3 days | `WATCHLIST-BE-B-01`, `WATCHLIST-BE-C-01` | `getWatchlistByIds`, `getWatchlistByFilter` |
| `WATCHLIST-FE-002` | Migrate watchlist create and clone mutations | Mutation migration | 🟢 Low | 2–3 days | `WATCHLIST-BE-D-01`, `WATCHLIST-BE-D-02` | `createWatchlistEntries`, `cloneFilesForWatchlist` |
| `WATCHLIST-FE-003` | Migrate `updateWatchlistEntries` saga handling | Mutation migration (complex) | 🟡 Medium | 3–4 days | `WATCHLIST-BE-E-01` | `updateWatchlistEntries` |

---

## Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 2 | 🟢 `WATCHLIST-FE-001` | `WATCHLIST-FE-001` → `WATCHLIST-BE-B-01`, `WATCHLIST-BE-C-01` | Search & listing — needs backend phase C |
| 3 | 🟢 `WATCHLIST-FE-002` | `WATCHLIST-FE-002` → `WATCHLIST-BE-D-01`, `WATCHLIST-BE-D-02` | Writes — needs backend phase D mutations |
| 4 | 🟡 `WATCHLIST-FE-003` | `WATCHLIST-FE-003` → `WATCHLIST-BE-E-01` | Complex writes / sagas — needs backend phase E + ADR ratification |

**Cutover flow:** `WATCHLIST-FE-001` → `WATCHLIST-FE-002` → `WATCHLIST-FE-003`.

---

## Recommended Story Graph — 2 Frontend Engineers

> The order map above packed onto **two frontend engineers**. Lanes re-sync at each step because the step's **backend gate** — not engineer availability — is the limiter; in a single-story step the second engineer pairs on parity checks/rollout or pre-pulls the next unblocked story. FE→FE chains stay with one engineer for context.

| Step | 👤 FE-1 | 👤 FE-2 | Backend gate (focus) |
|---|---|---|---|
| 2 | 🟢 `WATCHLIST-FE-001` (2–3d) | — | Search & listing — needs backend phase C |
| 3 | 🟢 `WATCHLIST-FE-002` (2–3d) | — | Writes — needs backend phase D mutations |
| 4 | 🟡 `WATCHLIST-FE-003` (3–4d) | — | Complex writes / sagas — needs backend phase E + ADR ratification |

**Elapsed (nominal midpoints):** ~8 FE build days with 2 engineers vs ~8 single-engineer — calendar time is set by the backend gates, not FE capacity.

---

## References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-BE-watchlist.md — the backend breakdown this cutover follows.
