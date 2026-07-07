# Complex Story — `Product.components` + `WorkspaceV2.counts` rollups

> **Summary —** Roll up a product’s component list and a workspace’s dashboard counts via parallel per-domain fan-out + one batched ACL call.
> **Spike:** — *(read pattern applied at cutover, not a research spike)* · **Status:** Problem brief
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub story:** `SPARK-PROD-G02` + `SPARK-WS-G02` (later phase)/`G04`

> **Migrates (source resolvers → this case):** product **FR `components`** (`SPARK-PROD-G02`, the per-claim N+1
> ACL) + workspace **FR `counts`** (`SPARK-WS-G02` (later phase)) and `products`/`productsCount`/`combinations` (`SPARK-WS-G04` (later phase)).
> Fans out to elastic-search + a batched access-control call.

## 1. The problem (grounded in the code)

**What this read does.** Two dashboard views: a product's **components list** (every BOM, measurement set,
detail set, packaging record and claim under the product, with the viewer's access applied) and a workspace's
**counts strip** (how many products, discussions and samples it holds). Both are one-screen reads whose rows
and numbers come from several domains at once.

Two Very-High field resolvers aggregate across domains and **roll up counts**:

### `Product.components` (~190 ln, `SPARK-PROD-G02`)
4 parallel elastic queries (measurement / claim / bom / productDetail) **+** packaging **+** a **per-claim N+1
ACL call** → a 5-type merge → `archivedCount` / `countByComponents` rollups (`cloneDeep(initialCountsByBp)`).

### `WorkspaceV2.counts` (~85 ln, `SPARK-WS-G02` (later phase)) — the product dashboard rollup
- `getFilteredProductsWithSummary` (search) → `getPage` (product) → product **discussion counts** + **sample counts** + a **sample-discussion roll-up into the product discussion count** → `WorkspaceCountsV2` (+ dashboard, nonEvaluated).
- Empty product set → zeros.
- `WorkspaceV2.products`/`productsCount`/`combinations` (`SPARK-WS-G04` (later phase)) are the cross-subgraph list siblings.

**Why it's complex:** same root as TechPack — multi-domain fan-out + ACL — but here it also **merges typed
lists** and **computes count rollups** (incl. the subtle sample→discussion count increment), with a real
**N+1 ACL** to fix.

## 2. What must be decided before build

- Who computes each list/count rollup.
- How the fan-out stays within the latency budget of the dashboard views.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
