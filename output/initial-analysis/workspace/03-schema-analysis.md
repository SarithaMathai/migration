# Phase 3: Federation Schema Analysis — Workspace

> **Domain:** `workspace` · **Target DGS:** separate `plm-workspace` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 20 🔜 | 2 ⏭ — 22 operations**

- The target schema is translated from the source SDL (`schemas/SPARK_WorkspaceV2.graphqls`), verified against the resolver.
- **Workspace is its own subgraph** (`plm-workspace`) — every reference is cross-subgraph.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `WorkspaceV2` (key `id`) |
| Owned value types | ~13 | `WorkspaceCountsV2`, `WorkspaceProductDashboard`, `WorkspaceReportV2`, `WorkspaceDepartmentV2`, `AttachmentWithMetaData`, paged/receipt/type-count/date-range |
| `@shareable` | 4 | `CodeDescription`, `Paging`, `Pageable`, `ResourceCount` |
| External stub — platform | 5 | `VMM_BusinessPartner`, `VMM_Brand`, `IG_Division`, `IG_Clazz`, `IG_Department` |
| External stub — other DGS | ~12 | `Product`, `ProductsPaged`, `Claims`, `CombinationSourcePaged`, `Attachment`, `SearchAttachment(sPaged)`, `DiscussionPaged`, `DiscussionElastic`, `TeamPaged`, `UserProfileAttributes`, `ResourcePermissions`, `ResourceMapping`, `Tag`, `Status` |
| Inputs | ~10 | `CreateWorkspaceInputV2`, `UpdateWorkspaceInputV2`, `WorkspaceTeamInput`, `WorkspacePartnerActionInputV2`, `WorkspaceExportOptions`, … |

No interfaces / unions — no `@DgsTypeResolver` needed.

## 2. Client Contract Verification
- 8 queries + 10 mutations preserved (`0 ✅ | 20 🔜`); **2 schema-drift wrappers deferred ⏭** (`dropWorkspaceBusinessPartnerV2`, `unDropWorkspaceBusinessPartnerV2` — traffic routes through `workspaceBusinessPartnerActionsV2`).
- `SPARK_`/`V2` naming preserved exactly (client contract); `VMM_`/`IG_` kept.
**Entity key:** `WorkspaceV2.id` (resolver derives from `workspaceHumanId || humanId`).

## 3. Federation Boundaries

> **Separate subgraph:** `workspace` is **not** in the plm-product monorepo. All references are true
> federation (or gateway stitch for platforms). Conversely, **`WorkspaceV2` is referenced as an entity** by
> product/bom/measurement/impression/productDetails/packaging/claims/watchlist (their `workspaces` fields).

- **Owns** `WorkspaceV2` + ~13 value types.
- **External (federation):** `product` (workspace products, page, view-toggle, status cleanup), `search`
  (paged/elastic, discussions/teams/combinations/samples, exports), `attachment`, `discussion`, `sampleV2`,
  `combination`, `relationship`, `tag`, `user-profile`, `access-control`, `exportHub`, `favorite`;
  **gateway stitch:** `VMM`, `IG`, `Brand`.
- **Provides** `WorkspaceV2` (the `@key(fields:"id")` entity) for all the product-family subgraphs to resolve
  their `workspaces` fields.

## 4. Migration Approach  *(Confluence approach page)*

Workspace is a **large, high-risk** standalone subgraph — a hub that nearly every product-family domain
references, and that itself reaches into product/search/discussion/sample/ACL.

1. **Phase A:** schema (~15 types, ~10 inputs) + `WorkspaceServiceV2` port (`plm-workspace` base). Preserve
   the create/update **dup-check** throw (`"A workspace with the same criteria already exists"`), the
   `changeWorkspace` throw-on-error, and the default `workspaceType=103`.
2. **Phase B:** the 6 simple/lookup reads.
3. **Phase C:** `getWorkspacesPagedV2/V3` (🔴 search; array-param CSV join + `omitBy`).
4. **Phase D:** the simpler mutations — create/update/change, add/remove resources (with their product
   side-effects), add-teams, and the 3 exports.
5. **Phase E:** `workspaceBusinessPartnerActionsV2` — the **Very-High** 5-case drop/undrop dispatcher.
   Choose a failure strategy (saga / compensation) and **fix the fire-and-forget `.then()` blocks** (await).
6. **Phase F:** expose `WorkspaceV2` as a federated entity (`@DgsEntityFetcher` by `id`) for the
   product-family subgraphs; decide the 2 deferred drop/undrop wrappers.
7. **Phase G:** field resolvers — the two Very-High (`attachmentsWithMetaData`, `counts`), `attachmentsV3`,
   the cross-subgraph `products`/`combinations`/`sampleReport`, partners, hierarchy/tags, users/computed —
   + the test/parity harness.

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `workspaceBusinessPartnerActionsV2` partial failure + un-awaited `.then()` (E01) | High | High | Saga/compensation; await the drop/undrop chains; parity per case | Tech Lead + PO |
| `attachmentsWithMetaData` / `counts` perf (G01/G03) | Medium | High | Parallel fetch + cached relationship/ACL; batch | Backend Eng |
| Cross-subgraph coupling to product (`products`, `addResources`) | Medium | Medium | Replace direct resolver calls with entity refs / a product client | Product Owner |
| Schema-drift drop/undrop wrappers may have live consumers | Medium | Medium | Traffic survey before delete (Phase F) | PO |
| `getWorkspacePackagingAttachments` needs `WORKSPACE_PACKAGING_TAG_ID` env | Low | Medium | Move to config; fail fast if unset (preserve) | Platform |

## 6. ACL Handling
- The dispatcher curries capability tokens and calls ACL `dropPartnerFromResources`/`unDropPartnerFromResources` with manual compensation.
- **ACL is ignored in the DGS implementation** (no ACL story) — context only; but the
**drop/undrop orchestration + compensation IS build work** (it is resource bookkeeping, not authorization).

## 7. Open Questions
1. `workspaceBusinessPartnerActionsV2` failure strategy; await the currently fire-and-forget chains?
2. Delete or `@deprecated` the 2 drop/undrop drift wrappers?
3. `products`/`addResources` — entity reference vs a thin product client?

---
**Phase Completed:** Phase 3 · **Domain:** `workspace`.
