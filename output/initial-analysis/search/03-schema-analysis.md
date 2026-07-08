# Phase 3: Federation Schema Analysis — Search

> **Domain:** `search` · **Target DGS:** separate `plm-elastic-search` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | ~47 🔜 | 1 ⏭ — ~48 operations**

- The target schema is translated from the source SDL (`schemas/SPARK_Search.graphqls`), verified against the resolver.
- **Search is its own subgraph** (`plm-elastic-search`) and the **read hub** for the whole program.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | ~6 | `SearchAttachment`, `Material`, `SearchCombination`, `SearchPalette`, `SearchWatchlist`, `SearchComponent` |
| Owned value/result types | ~44 | paged wrappers, `Suggestion`, counts, report/group-by shapes, material/attachment sub-objects |
| `@shareable` | ~5 | `Paging`, `CodeDescription`, `ResourceCount`, `BpCount`, `IdName` |
| External stub — platform | 4 | `VMM_BusinessPartner`, `VMM_Brand`, `IG_Division`, `IG_Department` |
| External stub — other DGS | ~12 | `Product(sPaged)`, `WorkspaceV2`, `Bom`, `SampleV2`, `Attachment`, `UserProfileAttributes`, `UserGroup_Participants`, `Tag`, `TeamPaged`, template paged wrappers |
| Inputs | ~10 | `MaterialSearchArguments`, `MaterialSearchCriteria`/`Filter`/`NestedFilter`, `MaterialRGBSearchCriteria`, … |

No interfaces / unions — no `@DgsTypeResolver`. (Result enrichment is via per-type field resolvers.)

## 2. Client Contract Verification
~47 queries + 1 mutation preserved; **1 schema-drift query deferred ⏭** (`searchProducts` — declared in the
SDL, no resolver). **Ownership reconciliations (Phase F):**
- `searchProductsES` is in the **resolver but not this SDL** (→ adminTools) — add to SDL or drop.
- `searchSPGSuggestions` / `searchUsersSuggestions` / `searchTeamsSuggestions` — in the SDL, **no resolver in
  this snapshot** — confirm the owner before exposing.
- `searchWorkspaceSuggestions` / `searchWorkspaceProductsSuggestions` — in the SDL, **resolved in the workspace
  resolver** — decide whether they live in `search` or `workspace`.
`SPARK_` prefixes dropped; `VMM_`/`IG_` kept.

## 3. Federation Boundaries

> **Read hub:** `search` is its own subgraph and is **referenced (called) by every product-family domain**
> (the 🔴 `search` dependency in product/bom/measurement/packaging/productDetails/claims/watchlist/workspace).
> In federation, those `ctx.loaders.search.*` calls become **queries against this subgraph** (or, for
> result-type enrichment, `@key` entity references resolved here).

- **Owns** the elastic result types (`SearchAttachment`, `Material`, `SearchCombination`, `SearchPalette`,
  `SearchWatchlist`, `SearchComponent`, + paged/report/suggestion shapes).
- **External (enrichment, cross-subgraph):** `product`, `bom`, `workspace`, `sample`, `attachment`,
  `user-profile`, `user-group`, `fabric`, `color`, `adminTools`; **gateway stitch:** `VMM`, `IG`, `Brand`, `Tag`.
- **Provides** search queries + the enriched result entities for the whole gateway.

## 4. Migration Approach  *(Confluence approach page)*

Search is **breadth-dominated**: ~48 thin elastic-wrapper queries + a large result-type surface with heavy
enrichment. Low orchestration risk, high surface-area cost.

1. **Phase A:** schema (~50 result types + ~10 inputs) + `SearchService` port (~80 elastic builders →
   grouped clients). The **type surface (A02) is the single biggest task** — expand the SDL value types
   (some shown as `JSON` placeholders in `03-schema.graphql`) to concrete types.
2. **Phase B:** by-id / counts reads (`searchMaterialsById`, `getElasticSamplesByIds`, counts).
3. **Phase C:** the search families — attachments, materials, samples, teams, templates, products,
   combinations/palettes, other, suggestions, reports — **grouped one story per family**.
4. **Phase D:** `sendBulkCombinationUpdates`.
5. **Phase F:** gateway composition + ownership reconciliation of the drift/cross-file suggestion queries.
6. **Phase G:** the enrichment field resolvers per result type (`SearchAttachment`, `Material`,
   `SearchCombination`, `SearchPalette`, `SearchWatchlist`, `SearchComponent`, access/report groups) + tests.

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Type-surface breadth (A02) under-scoped | High | Medium | Expand all SDL value types; CI schema-conformance | Product Owner |
| Enrichment field resolvers fan out to many subgraphs (G01/G02) | Medium | Medium | DataLoader batching; cache platform lookups | Backend Eng |
| Ownership drift (searchProducts/ES, *Suggestions) | Medium | Medium | Reconcile before exposing; traffic survey | Product Owner |
| Search is the read hub — cutover coordination | High | High | Migrate search early or dual-run; sequence dependents | Tech Lead + Platform |
| `Material.colorLinks` 12-prefix color gate | Low | Low | Port the prefix table exactly | Backend Eng |

## 6. ACL Handling
- A few proxy reads (`searchMaterialsByProxyIds`, `searchTeamsByProxyIds`, `searchClaimsByProxyIds`) and `Material.permissions`/`currentUserFileAccess` curry capability tokens / call accessControl.
- **ACL is ignored in the DGS implementation** (no ACL story) — context only.

## 7. Open Questions
1. Expand the `JSON`-placeholder value types to concrete SDL types (scope of A02)?
2. Reconcile `searchProducts` vs `searchProductsES`; and the 3 no-resolver `*Suggestions` + the 2
   workspace-resolved suggestions — which subgraph owns each?
3. Migration ordering — search is the read hub; migrate early or dual-run during dependents' cutover?

---
**Phase Completed:** Phase 3 · **Domain:** `search`.
