# ADR-014 (draft) — `Product.components` + `WorkspaceV2.counts` rollups

> **Status:** 🔴 Proposed — draft for review
> **Spike:** — (read pattern applied at cutover, not a research spike)
> **Home stubs:** `PRODUCT-BE-G-02` · `WORKSPACE-BE-G-02` / `WORKSPACE-BE-G-04` (later phase)
> **Scope:** the two dashboard **read rollups** — a product's typed component list and a workspace's counts
> strip — plus their list siblings (`products` / `productsCount` / `combinations`). Reads only; writes are
> ADR-011/012/013.
> **Related:** `SPIKE-06a` (hydration — the search→canonical two-stage read recurs here) ·
> `SPIKE-05` (the `code → type` tagging table) · techpack case (same fan-out root).
> **Evidence:** `resolvers/SPARK_Product.js` (components, ~190 ln) + `resolvers/SPARK_WorkspaceV2.js`
> (counts, ~85 ln; verified from the jun30 snapshot) at `https://github.com/XXX`.

---

## 1. Today's behavior

### `Product.components` (`PRODUCT-BE-G-02`) — 5-type merge + ACL rollup

1. **Hydration short-circuit** — if the product already carries `boms` / `measurementSets` / `claims` /
   `productDetails` (e.g. it was fetched through `WorkspaceV2.products` with include-flags), use them;
   skip step 2.
2. Else **4 parallel elastic queries** — measurement, claim, bom, productDetail — each invoked
   **by importing the sibling resolver directly** (`SPARK_Measurement.Query.getMeasurementsElastic`,
   `SPARK_Claims.Query.getClaimsElastic`, `SPARK_Bom.Query.getBomElastic`,
   `SPARK_ProductDetail.Query.getProductDetailsElastic`).
3. **Packaging elastic — always, and sequentially after** step 2 (`getPackagingElastic`);
   display name composed as `promoDescription + description`.
4. 🐞 **Per-claim N+1 ACL** — a `for` loop over claims, one `accessControl.getUserAccessUnencoded`
   call per claim → `currentUserClaimPermissions`. The stated fix of this case.
5. Seed `countsByBp` — `cloneDeep(initialCountsByBp)` + one zero entry per product business partner.
6. Collect all component ids (5 lists); empty → return `{content: [], counts, archivedCount: 0}`.
7. **Batched ACL** — `getAccessControlBatch(allIds, 100)` (chunks of 100) for every non-packaging component.
8. `mapComponent` per component:
   - `PKG-*` ids: partner comes from `component.businessPartner` (no ACL lookup),
   - all others: find the ACL entry — 🐞 **missing entry throws**, failing the whole field for one bad id,
   - grantees → `partners` (+ `locked` flag) → `addPartnersToCountObject` increments `countsByBp`,
   - normalize to one shape: name fallbacks (`name || claimName || description`), status fallback
     (`{code: statusId, description: statusName}`), access via `convertV2AccessToV3`.
9. **Type tagging** — measurement → `measurement` · claim → `claim` · bom → `bom` **but
   `bom.type === 2` → `packagingBom`** · productDetail → `productDetail` · packaging → `packaging`.
10. Rollups — `archivedCount` (re-filter with `archived: true`) · filtered content ordered by date ·
    `countByComponents` per type.

### `WorkspaceV2.counts` (`WORKSPACE-BE-G-02`, later phase) — the dashboard rollup

1. No products mapped on the workspace → 🐞 **returns scalar `0`** (the field's type is an object).
2. **Two-stage hydration** — `search.getFilteredProductsWithSummary` (elastic; filter/q/paging) →
   `product.getPage` for the canonical page. 🐞 both read `info.variableValues.id` / `.filter` —
   coupled to the *names of the caller's GraphQL variables*, not the field args.
3. Page has content → three **sequential** reads:
   - `discussion.getDiscussionsCount` for the product ids,
   - `search.getSampleCount` for the product ids,
   - `search.searchSamplesByParentId` (size 10000) for the sample list.
4. Samples exist → `discussion.getDiscussionsCount` for the **sample** ids, then the
   **sample→product roll-up**: for each sample with a non-zero discussion count, find its parent
   product's entry and 🐞 **increment it by exactly 1** — one per sample, regardless of how many
   discussions the sample has. Quirk or intent — the UI today is calibrated to it.
5. Return `{productsCount, productsDiscussionsCount, productsSamplesCount,
   nonEvaluatedRecievedSamplesCount, workspaceProductDashboard}`; empty page → zeros object
   (without `workspaceProductDashboard`).

### The list siblings (`WORKSPACE-BE-G-04`, later phase)

- `WorkspaceV2.products` — delegates to `Product.Query.getProducts` (cross-resolver import) with
  `includeBoms/Claims/MeasurementSets/ProductDetails: true` — the hydration source for step 1 of
  `components`; also reads `info.variableValues`.
- `WorkspaceV2.productsCount` — `product.getPage` with `size: 1` → `totalElements`.
- `WorkspaceV2.combinations` — elastic `searchCombinations` → capability JWT → `combination.getByIds`
  (two-stage hydration again).

### Interaction grid

Homes: search/elastic → separate DGS · claims → separate DGS · bom/measurement/packaging/productDetails →
**co-located on `plm-product`** · discussion → `plm-discussion` · combination → sibling DGS ·
ACL → AccessControlService.

| Field resolver | Elastic (search DGS) | Product | Claims DGS | Discussion DGS | Combination | ACL | Quirks |
|---|---|---|---|---|---|---|---|
| `Product.components` | ×5 (meas / claim / bom / pdtl / pkg) | context only | via elastic + N+1 ACL | — | — | 🐞 N+1 per claim + batch(100) | throw on missing ACL · `type 2 → packagingBom` |
| `WorkspaceV2.counts` | summary + sampleCount + samples(10k) | `getPage` | — | ×2 (products, samples) | — | — | scalar `0` · +1 roll-up · `variableValues` |
| `WorkspaceV2.products` | — (delegates) | `getProducts` + include-flags | — | — | — | — | cross-resolver import · `variableValues` |
| `WorkspaceV2.productsCount` | — | `getPage size 1` | — | — | — | — | — |
| `WorkspaceV2.combinations` | `searchCombinations` | — | — | — | `getByIds` | JWT | two-stage |

> **Key findings:**
> - `Product.components`' five child types are **mostly co-located on `plm-product`** — the real external
>   edges are elastic (search DGS), claims, and ACL. The fan-out is smaller than it looks.
> - `WorkspaceV2.counts` is the true cross-subgraph read: workspace → search → product → discussion →
>   sample, sequentially.
> - Four defects ride along: the N+1 claim ACL, the throw-on-missing-ACL, the scalar `0`, and the
>   `info.variableValues` coupling (which **cannot be ported** — DGS has no equivalent hack).

---

## 2. Decision drivers

- Phase-1 goal is **behavioral parity** — including the subtle rollup semantics (the +1 sample→discussion
  increment, `type 2 → packagingBom`, name/status fallbacks), verified by recorded fixtures.
- These are **dashboard reads** — the latency budget is one screen paint; the fan-out must stay parallel
  where it is parallel today and become parallel where it needlessly isn't.
- The N+1 claim ACL is named in the case brief as **the thing to fix while we're in there**.
- The `variableValues` coupling forces an API contract check: field args must carry what the resolver
  needs, and the UI queries must be confirmed to pass them.
- Reads don't need sagas or outboxes — the questions are **who computes each rollup** and
  **where the aggregation runs**.
- `counts` lands with the workspace domain (later phase) — this ADR fixes the pattern now so
  `plm-workspace` inherits a decision, not a redesign.

### Assumptions, constraints & success criteria

**Assumptions**
- The rollup quirks (+1 sample→discussion increment, `type 2 → packagingBom`, name/status fallbacks) are
  UI-calibrated contract; fixtures encode today's numbers as the target.
- UI queries can pass explicit `id`/`filter` field args (or will be updated to) — verified by a contract
  test before cutover (pin-down 5).
- bom/measurement/packaging/productDetail remain co-located in `plm-product`, so most of `components`
  resolves in-process.

**Constraints**
- The `info.variableValues` coupling cannot be ported — explicit field args are mandatory, not optional.
- Dashboard latency budget is one screen paint — fetches independent today (or needlessly sequential)
  must run in parallel.
- The merged, ACL-annotated list shape and the `countsByBp`/`archivedCount` rollups are the public
  contract and may not change in phase 1.

**Success criteria (measurable)**
- Recorded-fixture parity for `Product.components` including a product with > 100 components (chunked
  ACL) and a claim with a missing ACL record (the throw path); every rollup number identical to source.
- Exactly one batched ACL call per `components` resolution (N+1 eliminated) — asserted by a call-count
  test; the five component queries run in one parallel group.
- The four fixes ship as documented deviations with PO sign-off; no other behavioral drift in fixtures.
- The workspace stories inherit the pattern + deviation list with no new design decisions recorded.

---

## 3. Options

| | Option | Who computes | Latency | Parity | Verdict |
|---|---|---|---|---|---|
| A | Owner-computed rollup (lift-and-shift + fixes) | `plm-product` / `plm-workspace` field resolvers | same, improved by parallelizing | exact | **recommended** |
| B | Search-DGS computes the rollups | `plm-elastic-search` exposes ready aggregates | best (1 hop) | risky — business rules move | attractive later, not phase 1 |
| C | Federation-native decomposition | each child domain contributes its own field | gateway fans out | breaks contract | v2 API question |
| D | Materialized counts | indexer precomputes; DGS reads one doc | best possible | staleness | later refinement |

### A — Owner-computed rollup (lift-and-shift, formalized + the four fixes) ⭐

- `plm-product` computes `Product.components`: bom/measurement/packaging/productDetail queries become
  **internal service calls** (co-located); elastic + claims + ACL become sibling clients.
- `plm-workspace` computes `WorkspaceV2.counts` the same way when its phase arrives.
- Mandatory fixes riding the port (each an accepted, documented deviation):
  1. claim ACL joins the **single batched** `getAccessControlBatch` call — N+1 eliminated,
  2. packaging query joins the `Promise.all` (5 parallel, not 4+1),
  3. `counts`' three sequential reads parallelize where independent (product-discussions ∥ sample-count ∥ sample-list),
  4. `variableValues` replaced by explicit field args (contract check with the UI).
- ➕ exact rollup semantics preserved where they matter · smallest change surface · co-location makes most
  of `components` in-process.
- ➖ the owning subgraph keeps clients for search/claims/discussion/ACL · dashboard latency is still
  bounded by the slowest sibling call.

### B — Search-DGS computes the rollups

- The elastic DGS exposes `productComponents(productId)` / `workspaceCounts(workspaceId)` as ready-made
  aggregates — it already holds most of the rows.
- ➕ one hop for the dashboard; the fan-out disappears from the owners.
- ➖ business rules (ACL merge, +1 roll-up, type tagging, name fallbacks) move into the search domain —
  the wrong owner for them; ACL still requires per-viewer calls, so "one hop" is not actually one;
  index staleness becomes user-visible in counts. Not for phase 1; revisit per-aggregate later.

### C — Federation-native decomposition

- Each domain contributes its own subfield (`Product.claims` from the claims DGS via `extend type`,
  counts as per-domain count fields); the gateway assembles; the UI composes the list.
- ➕ purest ownership; no orchestrator.
- ➖ the *merged, typed, ACL-annotated* list and the cross-type `countsByBp` **cannot be assembled by the
  gateway** — a client-side rewrite of the rollup logic in every consumer; breaks the API contract.
  Disqualified for parity; a v2 API question.

### D — Materialized / precomputed counts

- An indexer maintains per-workspace and per-product rollup documents (events or scheduled); the field
  resolver reads one document.
- ➕ best latency; kills the fan-out and the N+1 wholesale.
- ➖ counts go stale between updates; needs the event pipeline ADR-011 §3-D describes (outbox etc.);
  per-viewer ACL filtering still can't be precomputed. **Recorded as a later refinement** for the
  viewer-independent numbers only.

---

## 4. Proposed decision (to ratify)

- **Option A** — the owning subgraph computes its own rollup, lift-and-shift semantics, with the four
  named fixes (batched claim ACL, full parallelization, explicit args, zeros-object) as accepted deviations.
- **Option B/D recorded as later refinements** — per-aggregate, viewer-independent numbers first;
  never the ACL-dependent parts.
- The `WORKSPACE-BE-G-02/G-04` stories (later phase) inherit this pattern — no second decision round.

### Pin-downs at ratification

| # | Item | Choice to make | Draft recommendation |
|---|---|---|---|
| 1 | N+1 claim ACL 🐞 | — | fold claim ids into the one `getAccessControlBatch` call; deviation noted |
| 2 | Throw on missing ACL entry 🐞 | fail whole field vs degrade per component | keep the throw in phase 1 (parity); log the id; revisit as a per-component `access: null` later |
| 3 | `counts` scalar `0` 🐞 | — | return the zeros object (a scalar is schema-illegal in DGS); accepted deviation |
| 4 | Sample→discussion **+1** roll-up 🐞 | preserve vs "fix" to real counts | **preserve exactly** — the UI is calibrated to it; document as intentional in the fixture notes |
| 5 | `info.variableValues` coupling 🐞 | — | explicit field args; confirm UI queries pass `id`/`filter` before cutover (contract test) |
| 6 | `type 2 → packagingBom` tagging | — | preserve; record in `SPIKE-05`'s `code → type` table |
| 7 | Packaging fetch ordering | sequential vs parallel | join the `Promise.all`; deviation noted |
| 8 | `WorkspaceV2.products` include-flags delegation | keep hydrated short-circuit vs always self-fetch | keep — it is the hydration edge `SPIKE-06a` governs; align with 06a's per-edge rule |

---

## 5. Consequences

- If accepted:
  - `PRODUCT-BE-G-02` builds `components` mostly **in-process** (co-located children) + three sibling
    clients (search, claims via search, ACL) — one batched ACL call total,
  - the workspace stories get a settled pattern and a settled deviation list before their phase starts,
  - dashboard latency improves (5-way parallel + batched ACL) without changing a single rollup number,
  - the four 🐞 fixes are closed with documented deviations instead of silent behavior drift.
- Risks:
  - pin-down 4: anyone "fixing" the +1 roll-up to real counts breaks dashboard parity — the fixture
    must encode today's numbers,
  - pin-down 5: if a UI query relies on the `variableValues` hack with different variable names, the
    contract test must catch it before cutover,
  - fixture recording must include a product with **> 100 components** (chunked ACL) and a claim with a
    missing ACL record (the throw path), or the edge behavior ships unverified.

---

## 6. On acceptance

Per `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md` (adapted — no spike id; this case is
pattern-at-cutover):

1. Copy this write-up to `adrs/`; add a case block to `adrs/adr-index.yaml`
   (`status: Accepted`, `chosen: "A — …"`, all options preserved).
2. Flip `00-overview.md` §2 to **Decided**; add `01-stories.md` + implementation notes
   (incl. the deviation list and the fixture-edge checklist from §5).
3. Update `output/analysis/product/be-04-stories.md` (`G-02`) with the concrete pattern;
   workspace stories follow in their phase.
4. Regenerate domain + global docs; push to Jira/Confluence.
