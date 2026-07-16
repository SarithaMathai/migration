# Reference — Federation & Stitching Patterns (condensed)

How a cross-domain (`ctx.loaders.{otherKey}`) call in the Node resolver becomes a DGS/Hive-Gateway
construct. Use this when writing CAT-4 (Phase F) stories.

## 0. Monorepo rule — `plm-product` is ONE subgraph (read first)

`plm-product` is a **monorepo / single DGS subgraph** that hosts the whole product family:
**`product`, `bom`, `measurement`, `impression`, `packaging`, `productDetails`, `sizeTemplate`,
`tightFit`, `watchlist`, `fileLibrary`, `pom`, `measurementTemplate`, `specificationsTemplate`,
`productPlan`, `productAsk`, `productVariation`.**

- References **among these co-located domains are plain internal GraphQL types** — define the type once
  (in its owning domain's `.graphqls`), reference it normally from the others. **No `@key`/`@extends`/
  `@external`, no gateway hop, no CAT-4 story.** A field like `Bom.product` or `Product.measurementSets`
  is an internal `@DgsData` calling the sibling service in the same JVM.
- **Federation (`@extends @external`, CAT-4) applies ONLY to genuinely separate subgraphs/services:**
  `attachment`, `workspaceV2`, `discussion`, `sampleV2`, `claim`, `tag`, `relationship`, `accessControl`,
  `userAttributes`/`teamV2` (user-profile), `search`, and the material DGSs `materialHub`/`trim`/`wash`/
  `fabric`/`combination` — plus platforms (VMM, IG, Doppler, CORONA, APEX) which are always gateway stitch.
- **Consequence for stories:** "contribute X back to `Product`" between co-located domains is an **internal
  field resolver in the same subgraph** (CAT-2), not a cross-subgraph entity extension (CAT-4). It still
  depends on the `Product` type existing in the merged schema (ordering), but there is no gateway federation
  and nothing is "BLOCKED-BY" a separate deployment.
- **TechPack `ResourcesCount`:** fields owned by co-located domains (`measurementSets`, `productBoms`,
  `packagingBoms`, `boms`) are filled **internally**; only the externally-owned fields
  (`productAttachments`, `discussionAttachments`, `discussions`, `sample`, `claims`, `constructions`,
  `watchlists`) need true cross-subgraph federation.

## 1. Pick the pattern by severity

| Severity | Source shape | DGS / Gateway pattern |
|----------|--------------|------------------------|
| 🔵 BLUE | Optional enrichment from an external platform (VMM, IG, Doppler) | **Gateway stitch only.** Return a key-only stub (`@key @extends @external`); the gateway resolves the full type. No DGS code beyond the stub. |
| 🟡 YELLOW | Single call to a sibling DGS for enrichment | **Entity reference.** Define `@extends type X @key(fields: "id")`; the sibling DGS owns the body. One `@DgsEntityFetcher` if this domain contributes fields back. |
| 🔴 RED | Sequential/merged calls critical to the result | **Owned federation + facade.** May need an aggregation facade during migration (see §3) before full federation. |

## 2. Owned entity vs. external stub

- **Owned** (`@key(fields:"id")` + full body): the domain that holds the data. e.g. `Bom` is owned by
  the BOM subgraph.
- **External stub** (`@key @extends @external`): a type owned elsewhere but referenced here. e.g.
  `Product`, `VMM_BusinessPartner`, `HubMaterial` inside the BOM schema.
- A field that *contributes* to a type owned elsewhere → `extend type X { newField }` in this subgraph
  with a `@DgsEntityFetcher` keyed on `X`'s `@key`.

## 3. Composite-key aggregate (the TechPack pattern) — Option D (hybrid), a.k.a. **facade-then-federate**

> **Naming note:** "Option D" is this catalogue's label (from `techpack-migration-options.md`). The same
> pattern is **ADR-015 Option B** — ADR option letters are local to each ADR, so always cite them qualified.
> The canonical prose name is **facade-then-federate**.

When one query returns a type assembled from N subgraphs (e.g. `ResourcesCount @key(fields:"productId partnerId")`
filled from attachment/discussion/sample/measurement/claim/bom/…):

1. **Phase E — stub + facade (Option D Phase 1):** define the `@key` type in the defining subgraph;
   implement the query as a thin `@DgsQuery` that calls a temporary **aggregation facade**
   (fastest: extract the existing Node orchestration into a small service). Works on day 1.
2. **Phase F — federate per subgraph (Option D Phase 2):** each owning subgraph adds
   `extend type ResourcesCount @key(...) { itsFields }` with a `@DgsEntityFetcher`. These are
   **placeholder stories** `BLOCKED-BY: {domain} migration`, written in the owning domain's `be-04-stories.md`.
3. **Phase F — retire facade:** once all subgraphs are live, delete the facade; the gateway fans out.

## 4. ACL / capability-token (JWT) calls — **context only, not build work**

When the source does `getUserPermissionsJWT(ids, ctx)` then curries a loader with
`SPARK-Capability-Token: permissionJWT`, that is the current gateway obtaining an **ACL capability
token** so the downstream backend authorizes the request for those resource ids.

**Rule for these artifacts (per stakeholder decision):**
- **Do NOT create ACL/JWT plumbing as a migration story or task.** ACL can be ignored in the DGS
  implementation — assume the platform/gateway provides authorization.
- **DO note, per affected operation:** *"Current implementation calls ACL (`getUserPermissionsJWT`) to
  obtain a capability token because {reason — e.g. the bom records are resource-scoped and the backend
  enforces per-resource read/write permission}. ACL is ignored in the DGS implementation."*
- Keep the note short; it explains intent for reviewers, nothing to build.
- In the EXT inventory, mark `accessControl` calls **`context-only`** rather than a 🔴 build dependency.

## 5. Internal vs. external user branch

`if (ctx.currentUser.internal) {...} else {...}` → both paths must exist in DGS. External path typically
adds `searchMaterialsByProxyIds(permissionJWT)` with `proxyIds`. This is a **+1 complexity** bump and
needs a parity test per branch.
