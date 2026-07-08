# Phase 2: Resolver Dependency Analysis — Search

> **Domain:** `search` · **Target DGS:** `SearchService` → separate `plm-elastic-search` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Source of truth:** `schemas/SPARK_Search.graphqls` (SDL), `resolvers/SPARK_Search.js` (507), `services/Search.js` (1,034)
> **Depends on:** [01-schema-inventory.md](./01-schema-inventory.md) · **Mode:** Full (queries grouped by family)

- Implementation spec.
- ACL/JWT usage is **context-only**.
- `search` is the elastic read hub (its own subgraph).
- Most queries are **thin elastic wrappers**; the work is the **type surface + enrichment field resolvers**.

## Summary Statistics
| Metric | Count |
|--------|-------|
| Query resolvers | ~43 (grouped into 10 families below) |
| Mutation resolvers | 1 |
| Field-resolver blocks | ~12 result types |
| Service methods | ~80 (elastic builders) |
| EXT loaders | ~14 (cross-subgraph) |
| Very High | 0 (breadth-dominated) · High: material/sample search bodies, enrichment blocks |

---

## Query families (pseudo-logic)

| Family | Queries | Pattern |
|---|---|---|
| **Attachments** | `searchAttachments`, `getAttachmentsCounts` | (own elastic) `searchAttachments({q,parentIds,relatedIds,partnerId,asset3D,proxyIds,page,size,sort})`; counts on demand. |
| **Materials** | `searchMaterials` (`getPage`), `searchMaterialsV2` (body: query+sort+options+searchArguments incl. RGB criteria/nested filters), `searchMaterialsNested` (`getPageNested`), `searchMaterialsByProxyIds` (ACL token), `multiRequestMaterialSearch`, `searchMaterialsById` | build elastic body → post; proxy variant curries a capability token. |
| **Samples** | `searchSamples`, `searchSamplesByParentId`, `getElasticSamplesByIds`, `getSampleCount`, `getSamplesCountGroupBy` (→ `.samplesCount`), `getMaterialSamplesGroupBy`, `getRequestedSamplesByUser` | elastic sample queries + group-by aggregates. |
| **Teams** | `searchTeamsElastic`, `searchTeamsElasticResourceType`, `searchTeamsByProxyIds` (ACL), `searchTeamsWithTypeCheck` (mvs/dps params) | elastic team queries. |
| **Templates** | `searchMeasurementTemplates`, `searchSizeTemplates`, `searchProductDetailsTemplates` (+ their `*Suggestions`) | elastic template queries. |
| **Products** | `searchProductByField` (field-weight body), `getProductSuggestions` (SMP-prefix → sample suggestions branch), `getProductSuggestionsV1`, `getTemplateSuggestions` | elastic product queries; `searchProducts`⏭ (no resolver — drift), `searchProductsES`→adminTools (resolver-only, not in SDL). |
| **Combinations/Palettes** | `searchCombinations`, `searchPalettes` | elastic queries. |
| **Other** | `searchWatchlist`, `searchClaimsByProxyIds` (ACL), `searchRfidLocations` | elastic queries. |
| **Reports** | `getConnectedBOMs` (query built via `getQueryForConnectedBOMSearch`), `getProductReport`, `getProductWorkspaceMetricsReportCount` | elastic aggregate reports. |
| **Suggestions** | `searchSuggestions(type)` + `searchRfidSuggestions`, `searchPointOfMeasureSuggestions`, `searchCombinationSuggestions`, `searchPaletteSuggestions`, `searchMeasurementTemplatesSuggestions`, `searchSizeTemplatesSuggestions`, `getProductDetailsTemplateSuggestions` (+ `searchSPGSuggestions`/`searchUsersSuggestions`/`searchTeamsSuggestions` — **no resolver in snapshot**; `searchWorkspaceSuggestions`/`searchWorkspaceProductsSuggestions` — **resolved in workspace**) | thin elastic suggestion wrappers → `[Suggestion]`. |

## Mutation
- `sendBulkCombinationUpdates(combinationUpdates): BulkCombination` — (own) `sendBulkCombinationUpdates` → `{requestId}`.

## Field Resolvers (enrichment — by result type)
- **`SPARK_SearchAttachment` (~13):** `createdBy`/`updatedBy` (🟡 user), `tags` (delegates to Attachment),
  `relatedProduct` (🟡 product, PID-prefix), `relatedWorkspace` (🟡 workspace, WRK-prefix),
  `currentUserFileAccess` (accessControl context), `renders`/`gallery`/`modelFile` (🟡 attachment, gated on
  `canShareWithGallery`/`canOpenInShowDog`), `productPacketProps`/`canOpenInShowDog`/`finalVirtualFile` (snake/camel coalesce).
- **`SPARK_Material` (~18):** `supplierName` (🔵 vmm), `permissions` (accessControl), `claims` (🔵 fabric),
  `tags` (🔵 tag), `attachments` (own elastic), `businessPartners`/`droppedPartnerIds`/`teams` (🔵 vmm),
  `baseMaterial` (resolveBaseMaterial), `createdBy` (🟡 user), `colorLinks` (🔵 color, 12-prefix gate),
  `referenceId`/`impressionIntent`/`is3D`/`trimSuppliers` (computed).
- **`SPARK_SearchCombination`:** `brands` (🔵 brand), `businessPartners`/`droppedPartnerIds` (🔵 vmm),
  `department`/`division` (🔵 ig), `designCycles`/`materialCategory`/`tags` (🔵 tag), `fabricSpec` (🔵 fabric).
- **`SPARK_SearchPalette`:** `brands` (🔵 brand), `tags`/`designCycles` (🔵 tag), `departments` (🔵 ig),
  `businessPartners`/`droppedPartnerIds` (🔵 vmm).
- **`SPARK_SearchWatchlist`:** `businessPartners` (🔵 vmm), `createdBy`/`updatedBy` (🟡 user), `attachments`
  (own elastic), `workspaces` (🟡 workspace), `participantDetails` (🔵 userGroup), `product` (🟡 product).
- **`SPARK_SearchComponent`:** `createdBy`/`updatedBy` (🟡 user), `workspaces` (🟡 workspace), `materials`
  (🟡 bom, BOM/PKGBOM/PRDBOM prefix).
- **`SPARK_SearchAttachmentAccess`:** `bps` (union of bp/merch/fab), `partnerNamesMap` (🔵 vmm).
- **Paged types** (`SearchAttachmentsPaged`/`MaterialsPaged`/`CombinationPaged`/`PalettePaged`/`SearchSamplesPaged`/
  `SizeTemplatePaged`): `paging`/`counts` (computed; `MaterialsPaged.counts` calls `getCounts`).
- **Report groups** (`ConnectedBOMGroup`/`…GroupResult`, `Requested_Evaluated_Samples_By_User`,
  `SearchProductDivision/DepartmentCount`): `groupBy`/`designCycle`/`user`/`division`/`department` (🔵 ig/tag/user).

## Service Classes
- `SearchService` base = `plm-elastic-search`. ~80 methods, each building an elastic query string/body and posting/loading; transforms via `deepToCamelCase`.
- Counts/group-by helpers (`keyValuesTransform`).

## EXT Service Call Inventory (summary)
~14 keys — **0 🔴** (search **is** the elastic backend) · ~6 🟡 (product, bom, workspace, attachment,
userAttributes) · ~7 🔵 (vmm, ig, brand, tag, fabric, color, userGroup/adminTools) · accessControl **context**.

## Key Findings
- **Highest cost:** the **type surface** (~50 result types, A02) + the enrichment field resolvers
  (`SearchAttachment`, `Material`) — they re-hydrate from many subgraphs.
- **Schema-drift / ownership:** `searchProducts` (no resolver) vs `searchProductsES` (not in SDL);
  `searchSPGSuggestions`/`searchUsersSuggestions`/`searchTeamsSuggestions` (no resolver in snapshot);
  `searchWorkspace*Suggestions` resolved in workspace. Reconcile ownership in Phase 3/F.
- **Quick wins:** the by-id reads, counts, and the thin suggestion wrappers (grouped).
- **Architectural:** search is the **read hub** — in federation, the `ctx.loaders.search.*` calls made by every
  other domain become queries against this subgraph; coordinate the cutover.

---
**Phase Completed:** Phase 2 · **Domain:** `search` · **EXT:** ~14 keys (0🔴 · ~6🟡 · ~7🔵).
