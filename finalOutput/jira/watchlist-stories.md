# watchlist — Jira stories (paste one block per issue)

> **Epic:** Watchlist → plm-product DGS migration  ·  **Labels:** `dgs-migration`, `watchlist`, `<type>`
> Create the Epic first, then paste each block below as a new Story's description.
> Story points are AI-derived from complexity (confirm in refinement). See [README.md](./README.md).

## SPARK-WL-A01 · Schema skeleton + DateTime scalar
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** —
**Labels:** `dgs-migration`, `watchlist`, `schema`

**Current Behaviour:** green-field; schema translated from `code/schemas/SPARK_Watchlist.txt`.
**Target:** federation v2.3 header, `scalar DateTime → Instant`, empty `extend type Query`/`Mutation`.
**Acceptance:** 1. `./gradlew generateJava` passes. 2. `DateTime` round-trips. **Tests:** ☐ compiles ☐ scalar serde.

---

## SPARK-WL-A02 · Owned types + inputs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-A01
**Labels:** `dgs-migration`, `watchlist`, `schema`

**Target:** `Watchlist` (`@key(fields:"humanId")`), `WatchlistInspection`, `WatchlistInspectionAction`,
`WatchlistPartner`, the 4 inputs, `@shareable CodeDescription` — per [03-schema.graphql](./03-schema.graphql).
**Acceptance:** 1. all types+inputs present; `@key=humanId`; nullability matches SDL. 2. validates. **Tests:** ☐ validates ☐ entity stub.

---

## SPARK-WL-A03 · External stubs (platform + sibling DGS)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-WL-A01
**Labels:** `dgs-migration`, `watchlist`, `schema`

**Target:** stubs `Attachment`, `SearchAttachment`, `WorkspaceV2`, `UserProfileAttributes`,
`UserGroup_Participants`, `VMM_BusinessPartner` + internal placeholder `Product`. **Acceptance:** 1. compiles; gateway composes. **Tests:** ☐ compiles ☐ stub resolves.

---

## SPARK-WL-A04 · WatchlistService port (watchlist/v1)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-A01
**Labels:** `dgs-migration`, `watchlist`, `service`

**Current Behaviour (Phase 2 §Service):** 7 REST methods on `watchlist/v1` (2 unused: versions).
**Target:** Kotlin service; preserve create/update throw-on-error; snake/camel at the Feign boundary. **Acceptance:** 1. used methods present (GET `?watchlistIds=`, `/watchlist_reasons`, `/watchlist_inspection_action_types`, POST, PUT). 2. create/update throw on validation error. **Tests:** ☐ endpoint build ☐ error contracts.

---

### Phase B — Core Reads

---

## SPARK-WL-B01 · getWatchlistByIds
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-WL-A02, SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `query`

**Current Behaviour (Q1):** (ACL context) token → `GET watchlist/v1?watchlistIds={csv}` → camelCase. **Target:** `@DgsQuery → [Watchlist]`. **Acceptance:** 1. returns entries for ids; empty → []. **Tests:** ☐ happy ☐ empty.

---

## SPARK-WL-B02 · getWatchlistReasons (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `query`

**Current Behaviour (Q2):** (own) `GET watchlist/v1/watchlist_reasons`. **Target:** `@DgsQuery` → `@Cacheable` → `[CodeDescription]`. **Acceptance:** 1. returns reasons; cached. **Tests:** ☐ list ☐ cache hit.

---

## SPARK-WL-B03 · getWatchlistInspectionActions (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `query`

**Current Behaviour (Q3):** (own) `GET watchlist/v1/watchlist_inspection_action_types`. **Target:** `@DgsQuery` → `@Cacheable` → `[WatchlistInspectionAction]`. **Acceptance:** 1. returns actions; cached. **Tests:** ☐ list ☐ cache hit.

---

### Phase C — Search & Listing

---

## SPARK-WL-C01 · getWatchlistByFilter (product→search→watchlist)
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `query`

**Current Behaviour (Q4):** (internal) `product.getWorkspaceProducts({q,filter,workspaceId,page,size})` →
product `humanId`s → (🔴 search) `searchWatchlist({ q:"parentId:(... OR ...) AND workspaceContext: {workspaceId} AND statusId: 501", page, size })` → watchlist ids → (ACL) token → (own) `getWatchlistByIds`.
**EXT:** 🔴 search · product internal. **Target:** `@DgsQuery → [Watchlist]`; chain the 4 calls.
**Acceptance:** 1. product→search→watchlist chain preserved. 2. elastic query string exact (incl. `statusId: 501`). **Tests:** ☐ chain ☐ query build ☐ parity.

---

### Phase D — Mutations (simple)

---

## SPARK-WL-D01 · createWatchlistEntries (create + user-group; throws)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `mutation`

**Current Behaviour (M1):** `Promise.all(entries.map(w => { (own) createWatchlistEntries([w]); **throw on validationErrors/message**; then (🔵 user-group) addUserGroup({resourceId:humanId, participantDetails, relatedResources}); **throw on error** }))`, flatten. **EXT:** 🔵 user-group. **Target:** per-entry create + user-group; port both throw contracts. **Acceptance:** 1. creates each entry + its user group. 2. either failure → exception. **Tests:** ☐ create ☐ user-group ☐ validation-error→throw.

---

## SPARK-WL-D02 · cloneFilesForWatchlist
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `mutation`

**Current Behaviour (M3):** (ACL) token → `Promise.all(attachmentIds.map((id,i) => (🔴 attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id)))`, stamp `parentResource=id`, flatten. **EXT:** 🔴 attachment. **Target:** structured-concurrency fan-out. **Acceptance:** 1. clones each id with its paired cloneReference; `parentResource` stamped. **Tests:** ☐ clone ☐ pairing ☐ parity.

---

### Phase E — Complex Operations

---

## SPARK-WL-E01 · updateWatchlistEntries (multi-step; fix un-awaited user-group map)
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `mutation`

**As a** DGS engineer **I want** the multi-step watchlist update with correct ordering + a failure strategy
**so that** user-group, body, and attachment changes stay consistent.
**Current Behaviour (M2):** 1) **per-entry (currently NOT awaited — bug):** `getUserGroups([humanId])`; if
existing participants → `updateUserGroup`, else (🔵 user-group) `addUserGroup` (throw on error);
2) (own) `updateWatchlistEntries(entries)` (throw on error); 3) collect `removedAttachmentIds` → (ACL)
token → (🔴 attachment) `archiveAttachmentBulkV3`. **No rollback.**
**EXT:** 🔴 attachment · 🔵 user-group. **Target:** **await** the per-entry user-group upserts (fix the race)
before/with the body update; chosen failure strategy (**PO decision**). **Acceptance:** 1. user-group upserts complete before the watchlist update (race fixed). 2. removed attachments archived. 3. partial-failure strategy. **Tests:** ☐ existing-participants path ☐ new-participants path ☐ attachment archive ☐ ordering/await ☐ partial-failure ☐ parity.

---

### Phase F — Federation (internal, same subgraph)

---

## SPARK-WL-F01 · Product.watchlists (INTERNAL, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `field-resolver`

**Current Behaviour:** Product exposes `watchlists` resolved from the co-located watchlist service. **Target:** **internal** `@DgsData` on `Product` calling `WatchlistService` in-process (not gateway federation). **Acceptance:** 1. resolves in-process; no gateway hop. **Tests:** ☐ resolves ☐ parity.

---

## SPARK-WL-F02 · ResourcesCount.watchlists (INTERNAL — TechPack; see SPARK-PROD-F08)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `field-resolver`

**Target:** fill the TechPack `ResourcesCount.watchlists` count **internally** (same subgraph) — the
watchlist side of product's `SPARK-PROD-F08`. **This is CAT-2 internal, not gateway federation** (watchlist
is co-located; analogous to `SPARK-BOM-F06` / `SPARK-MEAS-F04`). **Acceptance:** 1. count resolves in-process; parity vs the TechPack facade. **Tests:** ☐ count ☐ parity.

---

### Phase G — Field Resolvers & Tests

---

## SPARK-WL-G01 · Computed flatteners (statusId/statusName/reasonIds/reasons + inspection action)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-WL-A02
**Labels:** `dgs-migration`, `watchlist`, `field-resolver`

**Current Behaviour:** `statusId`=`status.code`, `statusName`=`status.description`, `reasonIds`=`reasons[].code`,
`reasons`=`reasons[].description`; `WatchlistInspection.actionId`=`action.code`, `action`=`action.description`. **Target:** computed `@DgsData` (no I/O). **Acceptance:** 1. each flattener maps correctly. **Tests:** ☐ status ☐ reasons ☐ inspection action.

---

## SPARK-WL-G02 · createdBy + updatedBy + workspaces + participantDetails + partnerName
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `field-resolver`

**Current Behaviour:** `createdBy`/`updatedBy` (🟡 user-profile); `workspaces` (🟡 workspaceV2 by
`workspaceContext`); `participantDetails` (🔵 user-group `getUserGroups([humanId])[0].participantDetails`);
`WatchlistPartner.partnerName` (🔵 vmm `getByID(partnerId).bpName`, null-safe). **Acceptance:** 1. each resolves; null-safe. **Tests:** ☐ users ☐ workspaces ☐ participants ☐ partnerName.

---

## SPARK-WL-G03 · attachments + product
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-A04
**Labels:** `dgs-migration`, `watchlist`, `field-resolver`

**Current Behaviour:** `attachments` → (🔴 search) `searchAttachmentsByRelatedResource(humanId)`; `product`
(internal, only if `parentId` starts `'PID'`). **Acceptance:** 1. attachments via elastic. 2. `product` null when not `PID*`. **Tests:** ☐ attachments ☐ product branch.

---

## SPARK-WL-G04 · Tests, parity harness
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-WL-B01, SPARK-WL-C01, SPARK-WL-E01, SPARK-WL-G02
**Labels:** `dgs-migration`, `watchlist`, `tests`

**Target:** ≥80% unit coverage; parity fixtures (incl. `getWatchlistByFilter` chain, the multi-step
`updateWatchlistEntries` with the await fix, create+user-group, computed flatteners); contract test (schema
diff intentional-only). **Acceptance:** 1. unit ≥80%. 2. parity green. 3. schema-diff intentional. **Tests:** ☐ parity ☐ contract.

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| `updateWatchlistEntries` un-awaited user-group map (race) (E01) | Medium | Medium-High | Await/`Promise.all`; failure strategy | Backend Eng + Tech Lead |
| `updateWatchlistEntries` multi-step partial failure (E01) | Medium | Medium | Saga / compensation — PO decision | Tech Lead + PO |
| `getWatchlistByFilter` 4-step chain perf (C01) | Low | Medium | Cache product lookup; paginate | Backend Eng |
| Product `SPARK-PROD-F08` mislabel (corrected to internal) | — | Low | F08 reclassified CAT-2 internal | Architect |

## 5. Summary
- **Stories:** 17 (A:4 · B:3 · C:1 · D:2 · E:1 · F:2 · G:4).
- **Critical path:** A01→A02/A04→C01→E01→G02→G04.
- **Highest risk:** `updateWatchlistEntries` (E01) — multi-step + un-awaited user-group map.
- **Co-located:** watchlist is in the `plm-product` monorepo; `Product.watchlists` + TechPack count resolve internally.

---
**Phase Completed:** Phase 4 — Migration Stories · **Domain:** `watchlist` · **Outputs:** 04-stories.md, 04-stories-index.yaml, 04-po-summary.md.

---
