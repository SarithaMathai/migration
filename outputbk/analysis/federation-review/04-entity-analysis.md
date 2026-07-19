# 04 · Federation Entity Analysis & Entity-Resolver Recommendations

> Phase 4 of the federation review · 2026-07-17
> Rule of thumb applied: a `@DgsEntityFetcher` (reference resolver) is required **only when a *separate* subgraph (or the gateway) can hand the owner a representation** — co-located references inside the `plm-product` monorepo resolve in-process and need none (per reference-federation-patterns §0).

## 1. Owned entities (phase-1 domains)

| Entity | Owner (subgraph) | Referenced by | `@key` | Entity resolver required? | Notes |
|---|---|---|---|---|---|
| `Product` | plm-product | claims (**separate** DGS: `Claims.product`, `Product.claims` extension), all co-located domains | `id` | **YES — missing story; added as PRODUCT-BE-H-06** | The only phase-1 owned entity that a *separate* subgraph resolves through `_entities` |
| `ResourcesCount` | plm-product (product) | claims (CLAIM-BE-H-02), phase-2 attachment/discussion/sample/construction | `productId partnerId` | Yes — ✅ covered (PRODUCT-BE-B-14/TechPack story implements `@DgsEntityFetcher(name="ResourcesCount")`) | Composite key; stub `[ID]` fields by design |
| `Bom` | plm-product (bom) | product (co-located), impression (co-located) | `id` | No (internal) | Add one only if a phase-2 external subgraph starts referencing Bom |
| `Measurement` | plm-product (measurement) | product (co-located) | `id` (synthesized from `humanId`) | No (internal) | Synthesized-id wrap is the program standard (OQ-1 ✅ resolved 2026-07-17) |
| `SampleMeasurementSet` | plm-product (measurement) | sample (phase-2, via `SampleV2.sampleMeasurement` MST-BE-F-04) | `sampleId` | Deferred to MST-BE-F-04 | — |
| `Impression` | plm-product (impression) | product (co-located), bom (co-located) | `id` | No (internal) | — |
| `Packaging` | plm-product (packaging) | product (co-located) | `id` (synthesized from `humanId`) | No (internal) | Key decision 2026-07-17; product stub aligned in R4 |
| `Dieline` | plm-product (packaging) | — (own queries only) | `id` (synthesized from `humanId`) | No | — |
| `ProductDetails` | plm-product (productDetails) | product (co-located) | `id` | No (internal) | Product stub name aligned in R4 |
| `Watchlist` | plm-product (watchlist) | product (co-located, `ResourcesCount.watchlists`) | `id` (synthesized from `humanId`) | No (internal) | — |
| `Claims` | **spark-claims** (separate) | product (`Product.claims`) | `id` (synthesized from `humanId`) | Yes — ✅ covered (CLAIM-BE-H-01 `@DgsEntityFetcher` fills `Product.claims` over the gateway) | Product-side stub fixed by R3 |
| `ProductRules` | plm-product (product) | — (own queries only) | `id` | No | Phase-4 question: stays in plm-product vs own DGS |

## 2. Referenced external entities (stubs) — who must resolve them

| Entity | Owner | Referenced by (phase-1) | `@key` | Resolution path |
|---|---|---|---|---|
| `VMM_BusinessPartner` | VMM platform (gateway-stitched 🔵) | all 8 domains | `id` (after R1) | Hive gateway → VMM; PRODUCT-BE-F-11 verifies |
| `VMM_Brand`, `IG_Department/Division/Clazz(_Filter)`, `DopplerCapacityType` | platforms (🔵) | product | `id` (after R2) | gateway-stitched |
| `CORONA_ItemDetails` | Corona (🔵) | product | `tcinId` (✅ decided 2026-07-17) | Entity form; record carries `tcinId`, Corona inflates item details via the gateway |
| `WorkspaceV2` | workspace DGS (phase 2) | 8 domains | `id` | until phase 2: gateway-stitched; risk RK-4 |
| `UserProfileAttributes`, `UserGroup_Participants` | user-profile DGS (phase 2) | 8 domains | `id` | same |
| `Attachment`, `SearchAttachment`, `FileLibrary` | attachment/search DGS (phase 2) | product, packaging, watchlist, productDetails, impression (REC-2) | `id` | same |
| `SampleV2` | sample DGS (phase 2) | product, measurement | `id` | same |
| `Tag` | tag DGS | product, bom | `id` | same |
| `TeamV2` | team DGS (phase 2) | product, claims (inside `TeamPaged` after R5) | `teamId` | same |
| `Discussion`, `DiscussionThread` | discussion DGS (phase 2) | product | `discussionId`/`discussionThreadId` | same |
| `AccessControl`, `ResourcePermissions` | access-control (ACL ignored in impl) | bom, claims, measurement, productDetails | `id` / `@shareable` value (R5) | context-only |
| Material DGS family (`HubMaterialInterface`, `Material`, `Trim`, `Wash`, `Fabric`, `FabricSpecCombo`, `FabricSpecification`, `Combination`, `BaseMaterial`, + row/size/supplier types) | material DGSs | bom | `id` | BOM-BE-S-02 spike owns rollout order |
| `ProductAsk`, `ProductVariation` | product-ask / variation DGSs | product | `id` | gateway-stitched |

## 3. Consistency verdict

- After R1–R5, every entity has exactly **one** owner, **one** `@key` shape, and consistent naming across all referencing subgraphs.
- **Program key rule (decided 2026-07-17):** every entity federates on `id`. humanId-only entities (Claims, Packaging, Watchlist, Dieline) wrap the record with a synthesized `id` (= humanId, the Measurement pattern) so gateway stitching is uniform; `humanId` remains on the type for the client contract.
- Value types shared across subgraphs (`CodeDescription`, `Paging`, `Pageable`, `UnitsOfMeasure`, `ValueWithUnit`, `ResourcePermissions`, `PermissionEntry`, `ProductComponentStatus`, `TeamPaged`, `CountsByBp`, `WorkspaceStatus`, `AccessV3`, `SpgFileLibrary`) are `@shareable` everywhere they are declared.
- Composition must be gated in CI: `hive compose` (or `rover compose`) across the 2 phase-1 subgraphs + platform stubs — acceptance criteria added to PRODUCT-BE-F-10.

## 4. Entity-resolver recommendations (actionable list)

1. **PRODUCT-BE-H-06 (new, REQUIRED):** `@DgsEntityFetcher(name = "Product")` in plm-product resolving `_entities([{__typename:"Product", id}])` → `productService.getById(id)` with a DataLoader batch. Without it, `Claims.product` (and every future external subgraph's `product` ref) returns null through the gateway. Blocks nothing locally; **blocks CLAIM-BE-G-03 end-to-end**.
2. **CLAIM-BE-H-01 / CLAIM-BE-H-02:** unchanged — claims-side entity fetchers for the `Product`/`ResourcesCount` extensions; now explicitly depend on R3 (key/name alignment).
3. **Co-located domains:** do **not** add defensive entity fetchers now (YAGNI — nothing external references them in phase 1); revisit per-domain when phase-2 subgraphs (sample→measurement, search→watchlist) come online.
4. **Platform stubs:** no resolvers to write; PRODUCT-BE-F-11 verifies the gateway hydrates them from `@key` stubs (now keyed `id` per R1/R2).
