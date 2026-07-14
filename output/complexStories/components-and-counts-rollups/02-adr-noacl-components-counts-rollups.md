# ADR-014-noACL (draft) — `Product.components` + `WorkspaceV2.counts` under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-components-counts-rollups.md` (ADR-014) — read that first; this ADR re-scores it
> under one changed premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The DGS / orchestration layer makes **no**
> ACL calls.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option A (owner-computed rollup) remains the proposal.

---

## 1. What the assumption removes from this case

| Today (DGS layer) | Under domain-ACL |
|---|---|
| 🐞 per-claim N+1 `getUserAccessUnencoded` loop | **gone entirely** — the named fix of the 01 ADR becomes moot; the claims service returns claims already viewer-scoped and permission-annotated |
| `getAccessControlBatch(allIds, 100)` for every non-packaging component | **moves** — each owning service (bom / measurement / productDetail / packaging / claims) returns its rows with grantee → partner data attached (it reads ACL itself) |
| 🐞 throw on missing ACL entry (fails the whole field) | **moves** — becomes each domain service's contract behavior, no longer rollup code |
| grantees → `partners` (+ `locked`) → `countsByBp` increments | **splits** — grantee *retrieval* is the domain's job; the `countsByBp` *aggregation* stays in the rollup (business rule, needs all 5 types together) |
| `convertV2AccessToV3` normalization | **moves** — domain services return the v3 access shape |

- `WorkspaceV2.counts` and the list siblings make **no ACL calls today** — completely unaffected.
- What survives untouched: hydration short-circuit, 5-type merge, `type 2 → packagingBom` tagging,
  name/status fallbacks, `archivedCount`, the +1 sample→discussion roll-up, the `variableValues` problem.

## 2. Impact on decision drivers

- The N+1 driver ("the thing to fix while we're in there") is satisfied by the global decision itself —
  no rollup-side fix needed.
- New driver: **partner/grantee data becomes a contract field** on five domain responses. All five
  services already integrate with ACL — no new ACL plumbing is being added; the ask is that each
  **exposes** the partner/access annotation it already resolves, in one agreed shape. `countsByBp`
  parity depends on that shape being uniform across the five.
- Latency: the batched-ACL hop disappears from the rollup; each domain call absorbs its own ACL read
  (net calls likely similar, but the orchestration is flatter and each hop is independently owned).

## 3. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Owner-computed rollup | slimmer — no ACL client at all; keeps merge, tagging, counts, fallbacks | **recommended** | **recommended — unchanged** |
| B | Search-DGS computes the rollups | its "'one hop' is not actually one — ACL still per-viewer" con **weakens** (search-DGS is a domain service and could ACL-scope its own reads) — but the decisive objection stands: the merge rules, type tagging, and `countsByBp` are product/workspace business rules in the wrong owner, and index staleness remains | rejected phase 1 | still rejected — ownership + staleness decide |
| C | Federation-native decomposition | marginally stronger (per-domain fields arrive ACL-complete) — but the merged, typed, cross-type `countsByBp` still cannot be assembled by the gateway; contract still breaks | disqualified | unchanged |
| D | Materialized counts | its worst blocker ("per-viewer ACL filtering can't be precomputed") is **unchanged** — viewer scoping just moved, it didn't disappear | later refinement | unchanged |

## 4. Proposed decision — no change

- **Option A** stands: `plm-product` / `plm-workspace` compute their own rollups — now with **zero ACL
  code** — over domain-service responses that arrive viewer-scoped and partner-annotated.
- Of the 01 ADR's four named fixes, two survive (full parallelization incl. packaging; explicit field args
  replacing `variableValues`), one becomes moot (N+1 claim ACL), one is unchanged (zeros object).
- Option B/D remain later refinements for viewer-independent numbers only.

## 5. Pin-downs affected (vs 01 §4)

| 01 # | Item | Under domain-ACL |
|---|---|---|
| 1 | N+1 claim ACL | **moot** — closed by the global decision |
| 2 | Throw on missing ACL entry | re-homed: specify per-domain contract behavior (recommend: keep the field-failing semantics in phase 1 for parity, implemented as the domain returning an error row); pin with a fixture |
| 7 | Packaging fetch ordering | unchanged — join the `Promise.all` |
| new | Grantee/partner contract shape | define **one** shared "partners + locked + access(v3)" response fragment for all five component domains; each already holds the data via its existing ACL integration, so this is a response-shape check, not new ACL work — contract-test before fixture recording |
| new | `>100 components` fixture | the chunked-ACL edge disappears from the rollup, but each domain service inherits its own batching — the fixture moves to the domain contract tests |

Pin-downs 3–6, 8 (scalar `0`, +1 roll-up, `variableValues`, `type 2 → packagingBom`, include-flags) are
unaffected.

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes.*
