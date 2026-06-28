# Phase 1: Schema Inventory — Search

> **Domain:** `search`
> **Target DGS:** `SearchService` → **separate `plm-elastic-search` subgraph** (elastic-backed)
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `code/schemas/SPARK_Search.txt` (655-line SDL) + `code/resolvers/SPARK_Search.txt` (507) + `code/services/Search.txt` (1,034)
> **Depends on:** None (entry phase) · **DGS Target Status:** Green-field

---

## 1. Context Registration

No `context.js`. `SearchService extends SparkService` takes the base URL **directly**
(`this.endpoint = endpoint`, `Search.txt:20`) — the REST service is **`plm-elastic-search`** (per platform
direction). Every query builds an elastic query string/body and posts to this backend.

| Setting | Value |
|---|---|
| Loader key | `search` |
| Service class | `SearchService extends SparkService` |
| Backend / DGS | **`plm-elastic-search`** (separate subgraph + backend) |
| Auth | base `Authorization`; some proxy reads add `SPARK-Capability-Token` (ACL — context only) |
| Target DGS | **separate `plm-elastic-search` subgraph** — the read hub used by **every** product-family domain |

## 2. Source File Manifest

| File | Lines | Role |
|---|---|---|
| `code/schemas/SPARK_Search.txt` | 655 | the source SDL — ~48 queries, 1 mutation, ~50 result/value types, ~10 inputs |
| `code/resolvers/SPARK_Search.txt` | 507 | ~43 query resolvers, 1 mutation, ~12 result-type field-resolver blocks |
| `code/services/Search.txt` | 1,034 ⚠️ | ~80 elastic query-builder methods (suggestions, materials, samples, teams, templates, …) |
| **⚠️ Large file** | 1,034 | service read by section; resolver/SDL read in full |

Schema: **`code/schemas/SPARK_Search.txt` (655 lines)** — target schema in [03-schema.graphql](./03-schema.graphql)
translated from it (nullability from the SDL).

## 3. Import Graph
```
SPARK_Search.txt imports (to ENRICH elastic hits) from:
  resolvers/SPARK_Attachment, SPARK_WorkspaceV2, SPARK_UserAttributes, SPARK_UserGroup, SPARK_Color,
  resolvers/product/SPARK_Bom, material/SPARK_BaseMaterialCommonFields, SPARK_Fabric (searchClaimsForParentResource)
  utils/commonLoaders (getUserPermissionsJWT, loadTags), resolvePaging, vmmUtils (loadBps, loadBusinessPartners,
  loadDroppedBusinessPartners, loadTeams), getTagsBatched, Reporting/queryUtil, Product/attachmentUtils
SearchService extends SparkService; uses loadListing/loadOne/postOne/convertFunctions/qs
```

## 4. Cross-Domain Reference Table (search ENRICHES elastic hits from many subgraphs)

| Used in | Loader key | Owning DGS / platform | Strategy | Severity |
|---|---|---|---|---|
| `relatedProduct`, `Material`/`Watchlist`/`Component.product`, suggestions | `product` | ProductService | federation | 🟡 |
| `materials` (Component), bom materials | `bom` | BomService | federation | 🟡 |
| `relatedWorkspace`, `workspaces` (Component/Watchlist) | `workspaceV2` | WorkspaceService | federation | 🟡 |
| `createdBy`/`updatedBy`, `Requested samples user` | `userAttributes` | UserProfileService | federation | 🟡 |
| `participantDetails` (Watchlist) | `userGroup` | UserProfileService | federation | 🔵 |
| `currentUserFileAccess`, `Material.permissions` | `accessControl` | AccessControlService | **context only** | n/a |
| `renders`/`gallery`/`modelFile`, `Material.attachments` | `attachment` | AttachmentService | federation | 🟡 |
| `businessPartners`/`droppedPartnerIds`/`teams`, partner-name maps | `vmm` | VMM platform | Gateway stitch | 🔵 |
| `division`/`department`/`clazz` (combination/palette/report counts) | `ig` | Item Groups | Gateway stitch | 🔵 |
| `brands` | `brand` | VMM/Brand | Gateway stitch | 🔵 |
| `tags`/`designCycles`/`materialCategory` | `tag` | TagService | federation | 🔵 |
| `Material.claims` | `fabric` | FabricService | federation | 🔵 |
| `Material.colorLinks` | `color` | ColorService | federation | 🔵 |
| `searchProductsES` (resolver-only) | `adminTools` | AdminToolsService | federation | 🔵 |

## 5. Co-located Siblings
**None** — `search` is its **own DGS** (`plm-elastic-search`). It is the **read hub**: nearly every other
domain calls `ctx.loaders.search.*` (the 🔴 search dependency seen across product/bom/measurement/packaging/
productDetails/claims/watchlist/workspace). In the target, those become calls to this subgraph's queries.

## 6. Hot Spots
1. **Breadth, not depth** — ~48 queries, most are **thin elastic wrappers** (build a query string/body → post →
   camelCase). The migration cost is the **type surface** (~50 result types) and the **enrichment field
   resolvers**, not orchestration.
2. **Suggestion family** — `searchSuggestions(type)` + ~11 specific `search*Suggestions` all wrap an elastic
   suggestion endpoint; **group** them in stories.
3. **Result-type enrichment** — `SPARK_SearchAttachment` (~13 fields), `SPARK_Material` (~18), `SPARK_SearchCombination`,
   `SPARK_SearchPalette`, `SPARK_SearchWatchlist`, `SPARK_SearchComponent` re-hydrate from product/vmm/ig/tag/
   brand/workspace/user/accessControl/attachment/fabric/color (cross-subgraph).
4. **Schema-drift / cross-file resolvers:**
   - `searchProducts: [SPARK_Product]` (SDL) has **no resolver** here; the resolver has `searchProductsES`
     (→ adminTools) which is **not in this SDL**. Reconcile (drift).
   - `searchWorkspaceSuggestions`, `searchWorkspaceProductsSuggestions` are declared in this SDL but **resolved
     in the workspace resolver**; `searchSPGSuggestions`/`searchUsersSuggestions`/`searchTeamsSuggestions` are
     declared in the SDL but have **no resolver in this snapshot** (confirm owner). Flag in Phase 3.
5. **Material search** — `searchMaterialsV2`/`Nested`/`multiRequest` build rich elastic bodies (RGB color
   criteria, nested filters); the heaviest read shapes.
6. **`Material.colorLinks`** — prefix-gated (12 color resource prefixes) → color service hydration.

## 7. Operation Lists (grouped)
**Queries (~48):** attachments (`searchAttachments`, `getAttachmentsCounts`); materials (`searchMaterials`,
`…V2`, `…Nested`, `…ByProxyIds`, `multiRequestMaterialSearch`, `searchMaterialsById`); samples (`searchSamples`,
`…ByParentId`, `getElasticSamplesByIds`, `getSampleCount`, `getSamplesCountGroupBy`, `getMaterialSamplesGroupBy`,
`getRequestedSamplesByUser`); teams (`searchTeamsElastic`, `…ResourceType`, `…ByProxyIds`, `searchTeamsWithTypeCheck`);
templates (`searchMeasurementTemplates`, `searchSizeTemplates`, `searchProductDetailsTemplates` + suggestions);
products (`searchProducts`⏭, `searchProductByField`, `getProductSuggestions`/`…V1`, `getTemplateSuggestions`);
combinations/palettes (`searchCombinations`, `searchPalettes`); other (`searchWatchlist`, `searchClaimsByProxyIds`,
`searchRfidLocations`); reports (`getConnectedBOMs`, `getProductReport`, `getProductWorkspaceMetricsReportCount`);
suggestions family (`searchSuggestions`, `searchRfidSuggestions`, `searchSPGSuggestions`, `searchUsersSuggestions`,
`searchTeamsSuggestions`, `searchPointOfMeasureSuggestions`, `searchCombinationSuggestions`,
`searchPaletteSuggestions`, `searchMeasurementTemplatesSuggestions`, `searchSizeTemplatesSuggestions`,
`getProductDetailsTemplateSuggestions`, `searchWorkspaceSuggestions`†, `searchWorkspaceProductsSuggestions`†).
**Mutation (1):** `sendBulkCombinationUpdates`.
† resolved in the workspace resolver.

## 8. Summary Statistics

| Metric | Count |
|--------|-------|
| Queries | ~48 (SDL) |
| Mutations | 1 |
| Result/value types | ~50 |
| Field-resolver type blocks | ~12 (`SearchAttachment`, `Material`, `SearchCombination`, `SearchPalette`, `SearchWatchlist`, `SearchComponent`, paged types, access, report groups) |
| Service methods | ~80 (elastic builders) |
| Cross-domain loader keys | ~14 (all cross-subgraph) |
| EXT calls | 0 🔴 (search IS the elastic backend) · ~6 🟡 · ~7 🔵 · accessControl context |
| Interfaces / unions | 0 |
| Large files | 1 ⚠️ (service 1,034) |

---
**Phase Completed:** Phase 1 — Schema Inventory · **Domain:** `search` · **Files:** 3 (2,196 lines: schema 655 + resolver 507 + service 1,034).
