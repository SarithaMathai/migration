# Complex Story — `Product.components` + `WorkspaceV2.counts` rollups

> **Summary —** Two dashboards, same trick — a product's component list and a workspace's counts strip both fan out to every domain in parallel then roll up into one number; fix the N+1 ACL call while we're in there.
> **Spike:** — *(read pattern applied at cutover, not a research spike)* · **Status:** 🟠 Draft ADR-014 proposed — ratification pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub story:** `PRODUCT-BE-G-02` + `WORKSPACE-BE-G-02` (later phase)/`G-04`

> **Migrates (source resolvers → this case):** product **FR `components`** (`PRODUCT-BE-G-02`, the per-claim N+1
> ACL) + workspace **FR `counts`** (`WORKSPACE-BE-G-02` (later phase)) and `products`/`productsCount`/`combinations` (`WORKSPACE-BE-G-04` (later phase)).
> Fans out to elastic-search + a batched access-control call.

## 1. The problem (grounded in the code)

### 1.1 Problem statement

- Two dashboard field resolvers — `Product.components` and `WorkspaceV2.counts` — merge typed lists and
  roll up counts across five domains' data plus per-viewer ACL, inside the gateway, with a real N+1 ACL
  defect and rollup semantics the UI is calibrated to.
- The merged, ACL-annotated result cannot be assembled by a federation gateway — the rollup must have an
  explicit owner under federation.

### 1.2 Current state & root cause

**What this read does.** Two dashboard views: a product's **components list** (every BOM, measurement set,
detail set, packaging record and claim under the product, with the viewer's access applied) and a workspace's
**counts strip** (how many products, discussions and samples it holds). Both are one-screen reads whose rows
and numbers come from several domains at once.

Two Very-High field resolvers aggregate across domains and **roll up counts**:

### `Product.components` (~190 ln, `PRODUCT-BE-G-02`)
4 parallel elastic queries (measurement / claim / bom / productDetail) **+** packaging **+** a **per-claim N+1
ACL call** → a 5-type merge → `archivedCount` / `countByComponents` rollups (`cloneDeep(initialCountsByBp)`).

### `WorkspaceV2.counts` (~85 ln, `WORKSPACE-BE-G-02` (later phase)) — the product dashboard rollup
- `getFilteredProductsWithSummary` (search) → `getPage` (product) → product **discussion counts** + **sample counts** + a **sample-discussion roll-up into the product discussion count** → `WorkspaceCountsV2` (+ dashboard, nonEvaluated).
- Empty product set → zeros.
- `WorkspaceV2.products`/`productsCount`/`combinations` (`WORKSPACE-BE-G-04` (later phase)) are the cross-subgraph list siblings.

**Root cause:** same as TechPack — the monolith let one resolver call every domain, so cross-domain
rollups were written inline (including by importing sibling resolvers and reading
`info.variableValues`) — but here the business rules ride along: type tagging (`bom.type 2 →
packagingBom`), name/status fallbacks, and the sample→discussion +1 increment, none of which any single
downstream service can compute.

### 1.3 Impact if not addressed

- **Performance** — a per-claim N+1 ACL call and needlessly sequential fetches on two dashboard screens
  whose budget is one paint.
- **Fragility** — one component with a missing ACL entry throws the whole `components` field; `counts`
  returns a schema-illegal scalar `0` on the empty path.
- **Portability** — the `info.variableValues` coupling (counts, products) has no DGS equivalent and
  **cannot be ported**; unresolved, it blocks the workspace phase.
- **Parity risk** — "fixing" the +1 rollup or the type tagging during port silently breaks dashboards
  calibrated to today's numbers.

### 1.4 Objectives

The cutover pattern is done when the following are recorded:
- An owner for each rollup (product vs workspace subgraph) and the aggregation's runtime location, with
  rollup semantics preserved exactly and pinned by recorded fixtures.
- The four named fixes (batched claim ACL, full parallelization, explicit field args, zeros-object)
  applied as accepted, documented parity deviations.
- A contract check that UI queries pass explicit `id`/`filter` args before cutover (replacing
  `variableValues`).
- A settled pattern + deviation list the later-phase workspace stories inherit without redesign.

## 2. What must be decided before build

- Who computes each list/count rollup.
- How the fan-out stays within the latency budget of the dashboard views.
- **Draft decision:** [ADR-014 (draft)](./01-adr-components-counts-rollups.md) proposes owner-computed
  rollups, lift-and-shift semantics + the four fixes (Option A) — status 🔴 Proposed, pending
  ratification. Scenario variant under the domain-ACL assumption:
  [ADR-014-noACL](./02-adr-noacl-components-counts-rollups.md).

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
