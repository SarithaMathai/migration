# Watchlist — Comprehensive Migration Documentation

> **Domain:** `watchlist` · **Target DGS:** `plm-product (co-located)` · **Generated:** 2026-07-19
> **Confluence location:** *Federation Graph Migration ▸ Domains ▸ watchlist*

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Migration Scope](#migration-scope)
- [Story Summary by Phase](#story-summary-by-phase)
- [Decisions Required](#decisions-required)
- [Recommended Sprint Sequencing](#recommended-sprint-sequencing)
- [Capacity Planning](#capacity-planning)
- [All Stories — Detailed Engineering Breakdown](#all-stories--detailed-engineering-breakdown)
  - [Phase B — Core Reads](#phase-b--core-reads)
  - [Phase C — Search & Listing](#phase-c--search-listing)
  - [Phase D — Mutations (Simple)](#phase-d--mutations-simple)
  - [Phase E — Complex Operations](#phase-e--complex-operations)
  - [Phase F — Federation & Stitching](#phase-f--federation-stitching)
  - [Phase G — Field Resolvers, Bug-fixes & Tests](#phase-g--field-resolvers-bug-fixes-tests)
- [Story Reference Table](#story-reference-table)

---

## Executive Summary

- We are moving the **Watchlist** domain — quality watchlist entries on a product (reasons, statuses, inspections, partners, attachments) — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **small and mid-low risk**: 4 queries, 3 mutations, 13 field resolvers on a 129-line resolver, with **no polymorphism**.
- It is **co-located** in the product family, so `Product.watchlists` and the TechPack `ResourcesCount.watchlists` count resolve **internally** (not across the federation gateway).

The one genuinely harder piece is **`updateWatchlistEntries`**, a multi-step write (user-group upsert, then
the body, then attachment archival) that today **does not await** its per-entry user-group updates — a race
to fix on the port.

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive step in `updateWatchlistEntries`) use **Mid-Request ACL Update** before the downstream call.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 4 | 2 cacheable master-data; 1 four-step filtered read |
| Mutations | 3 | 2 simple + `updateWatchlistEntries` (multi-step) |
| Field-resolver type blocks | 3 | `Watchlist` (10), inspection (2), partner (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 2 (Product, ResourcesCount) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

---

## Story Summary by Phase

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 3 | 3–6d |
| C | Search & Listing | 1 | 3–5d |
| D | Mutations (simple) | 2 | 4–7d |
| E | Complex (`updateWatchlistEntries`) | 1 | 4–7d |
| F | Federation (Product + TechPack, internal) | 2 | 2–4d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **13** | **25–44d** (buffered) |

> One engineer ≈ **5–9 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

---

## Decisions Required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateWatchlistEntries` — await user-group upserts + failure strategy | E-01 | Tech Lead + PO |
| 2 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01 + D-01/D-02 | filtered read + simple mutations |
| 3 | E-01 + F-01/F-02 | multi-step update + Product/TechPack internal contributions |
| 4 | G-01–G-03, G-05 (recommended, PO-gated) | field resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

---

## Capacity Planning

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

---
*Pipeline 2.0 — Phase 4 complete. Watchlist artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*

---

## All Stories — Detailed Engineering Breakdown

> Each story is self-contained. Read: **Current Behaviour → Target → Acceptance Criteria**.
> Test cases are included only for **High** and **Very High** complexity stories.

### Phases Overview

| Phase | Name | Stories |
|---|---|---|
| B | Core Reads | B-01–B-03 |
| C | Search & Listing | C-01 |
| D | Mutations (simple) | D-01–D-02 |
| E | Complex (multi-step write) | E-01 |
| F | Federation (internal) | F-01–F-02 |
| G | Field Resolvers | G-01–G-05 (G-05 recommended, PO-gated — federation review) |

> **Self-contained story model.** The Netflix-DGS-on-REST framework already exists, so **every operation story below is end-to-end in a single PR**: it adds the schema (query/mutation + the GraphQL type definitions it returns), the DGS data fetcher, the Kotlin REST service method (read or write) that calls the backend, and pushes the schema change to the **Hive** registry. There is **no separate service-layer story** — the former `*Service` Kotlin-port story has been dissolved into the operation stories.

---

### Phase B — Core Reads

#### WATCHLIST-BE-B-01 · `getWatchlistByIds(ids)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Fetch watchlist entries by id.

> **Note — DGS Module Init (this PR only):** Creates `watchlist.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.
- **Current Behaviour (Q1):** (ACL context) token → `GET watchlist/v1?watchlistIds={csv}` → camelCase. **Target:** `@DgsQuery → [Watchlist]`.

**Acceptance Criteria:**

1. returns entries for ids; empty → []

---

#### WATCHLIST-BE-B-02 · `getWatchlistReasons` (cacheable)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the watchlist-reason lookup (cached).

- **Current Behaviour (Q2):** (own) `GET watchlist/v1/watchlist_reasons`. **Target:** `@DgsQuery` → `@Cacheable` → `[CodeDescription]`.

**Acceptance Criteria:**

1. returns reasons; cached

---

#### WATCHLIST-BE-B-03 · `getWatchlistInspectionActions` (cacheable)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the inspection-action lookup (cached).

- **Current Behaviour (Q3):** (own) `GET watchlist/v1/watchlist_inspection_action_types`. **Target:** `@DgsQuery` → `@Cacheable` → `[WatchlistInspectionAction]`.

**Acceptance Criteria:**

1. returns actions; cached

---

### Phase C — Search & Listing

#### WATCHLIST-BE-C-01 · `getWatchlistByFilter(...)` (4-step read)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟡 Medium |
| **Phase** | C |
| **Depends on** | B-01 |
| **EXT** | 🔴 `search` · 🟡 `product` |

- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search` · 🟡 `product`

- **In plain terms:** List watchlist entries for a workspace's products (a 4-step read).

- **Current Behaviour (Q4):** (internal) `product.getWorkspaceProducts({q,filter,workspaceId,page,size})` →
product `humanId`s → (🔴 search) `searchWatchlist({ q:"parentId:(... OR ...) AND workspaceContext: {workspaceId} AND statusId: 501", page, size })` → watchlist ids → (ACL) token → (own) `getWatchlistByIds`.
- **EXT:** 🔴 search · product internal. **Target:** `@DgsQuery → [Watchlist]`; chain the 4 calls.

**Acceptance Criteria:**

1. product→search→watchlist chain preserved
2. elastic query string exact (incl. `statusId: 501`)

---

### Phase D — Mutations (Simple)

#### WATCHLIST-BE-D-01 · `createWatchlistEntries`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |
| **EXT** | 🔵 `userGroup` |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔵 `userGroup`

- **In plain terms:** Create watchlist entries (and their user-groups).

- **Current Behaviour (M1):** `Promise.all(entries.map(w => { (own) createWatchlistEntries([w]); **throw on validationErrors/message**; then (🔵 user-group) addUserGroup({resourceId:humanId, participantDetails, relatedResources}); **throw on error** }))`, flatten. **EXT:** 🔵 user-group. **Target:** per-entry create + user-group; port both throw contracts.

**Acceptance Criteria:**

1. creates each entry + its user group
2. either failure → exception

---

#### WATCHLIST-BE-D-02 · `cloneFilesForWatchlist`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment`

- **In plain terms:** Copy attachment files for watchlist entries.

- **Current Behaviour (M3):** (ACL) token → `Promise.all(attachmentIds.map((id,i) => (🔴 attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id)))`, stamp `parentResource=id`, flatten. **EXT:** 🔴 attachment. **Target:** structured-concurrency fan-out.

**Acceptance Criteria:**

1. clones each id with its paired cloneReference; `parentResource` stamped

---

### Phase E — Complex Operations

#### WATCHLIST-BE-E-01 · `updateWatchlistEntries` (multi-step write)

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟠 High |
| **Phase** | E |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` · 🔵 `userGroup` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |
| **Blocked by** | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |

- **Type:** Mutation · **Phase:** E · **Complexity:** 🔶 High · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment` · 🔵 `userGroup` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module)

> **Draft ADR-013, ratification pending.** Against the shared `WriteSaga` module built in `PRODUCT-BE-E-00`:
> the unawaited per-entry user-group map is **awaited and ordered before the body** (accepted deviation,
> ADR-013 pin-down 2 — closes the race/unhandled-rejection defect); attachment archive is a `RECORD` step;
> JWT no longer fetched when the archive list is empty.

- **In plain terms:** Edit watchlist entries — a multi-step write (user-groups + body); today the group step isn't awaited (a bug).

- **As a** DGS engineer **I want** the multi-step watchlist update with correct ordering + a failure strategy
**so that** user-group, body, and attachment changes stay consistent.
- **Current Behaviour (M2):** 1) **per-entry (currently NOT awaited — bug):** `getUserGroups([humanId])`; if
existing participants → `updateUserGroup`, else (🔵 user-group) `addUserGroup` (throw on error);
2) (own) `updateWatchlistEntries(entries)` (throw on error); 3) collect `removedAttachmentIds` → (ACL)
token → (🔴 attachment) `archiveAttachmentBulkV3`. **No rollback.**
- **EXT:** 🔴 attachment · 🔵 user-group. **Target:** **await** the per-entry user-group upserts (fix the race)

before/with the body update; chosen failure strategy (**PO decision**).

**Acceptance Criteria:**

1. user-group upserts complete before the watchlist update (race fixed)
2. removed attachments archived
3. partial-failure strategy

**Test Cases:**

- [ ] existing-participants path
- [ ] new-participants path
- [ ] attachment archive
- [ ] ordering/await
- [ ] partial-failure
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### Phase F — Federation & Stitching

#### WATCHLIST-BE-F-01 · `Product.watchlists` (internal)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | F |
| **Depends on** | B-01 |

- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Expose a product's watchlists on the Product type.

- **Current Behaviour:** Product exposes `watchlists` resolved from the co-located watchlist service. **Target:** **internal** `@DgsData` on `Product` calling `WatchlistService` in-process (not gateway federation).

**Acceptance Criteria:**

1. resolves in-process; no gateway hop

---

#### WATCHLIST-BE-F-02 · `ResourcesCount.watchlists` (internal — TechPack)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | F |
| **Depends on** | B-01 |

- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Contribute the watchlists count to the TechPack rollup.

- **Target:** fill the TechPack `ResourcesCount.watchlists` count **internally** (same subgraph) — the
watchlist side of product's `PRODUCT-BE-F-08`. **This is CAT-2 internal, not gateway federation** (watchlist
is co-located; analogous to `BOM-BE-F-06` / `MST-BE-F-04`).

**Acceptance Criteria:**

1. count resolves in-process; parity vs the TechPack facade

---

### Phase G — Field Resolvers, Bug-fixes & Tests

#### WATCHLIST-BE-G-01 · Computed flatteners (status/reasons/inspection action)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-01 |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Flatten status / reason / inspection-action codes into readable fields.

- **Current Behaviour:** `statusId`=`status.code`, `statusName`=`status.description`, `reasonIds`=`reasons[].code`,
`reasons`=`reasons[].description`; `WatchlistInspection.actionId`=`action.code`, `action`=`action.description`. **Target:** computed `@DgsData` (no I/O).

**Acceptance Criteria:**

1. each flattener maps correctly

---

#### WATCHLIST-BE-G-02 · `createdBy` + `updatedBy` + `workspaces` + `participantDetails` + `partnerName`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🟡 `userAttributes` · 🟡 `workspaceV2` · 🔵 `userGroup` · 🔵 `vmm` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🟡 `userAttributes` · 🟡 `workspaceV2` · 🔵 `userGroup` · 🔵 `vmm`

- **In plain terms:** Resolve the people, workspace and partner fields.

- **Current Behaviour:** `createdBy`/`updatedBy` (🟡 user-profile); `workspaces` (🟡 workspaceV2 by
`workspaceContext`); `participantDetails` (🔵 user-group `getUserGroups([humanId])[0].participantDetails`);
`WatchlistPartner.partnerName` (🔵 vmm `getByID(partnerId).bpName`, null-safe).

**Acceptance Criteria:**

1. each resolves; null-safe

---

#### WATCHLIST-BE-G-03 · `attachments` + `product`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🔴 `search` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search`

- **In plain terms:** Resolve a watchlist entry's attachments and parent product.

- **Current Behaviour:** `attachments` → (🔴 search) `searchAttachmentsByRelatedResource(humanId)`; `product`
(internal, only if `parentId` starts `'PID'`).

**Acceptance Criteria:**

1. attachments via elastic
2. `product` null when not `PID*`

---

#### WATCHLIST-BE-G-05 · `WatchlistPartner.partner` entity reference (recommended, PO-gated)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | G-02 |
| **EXT** | 🔵 `vmm` |
| **Status** | Recommended (PO-gated — federation-review/03 §2 REC-3) |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** G-02 · **EXT:** 🔵 `vmm`
- **Status:** Recommended (PO-gated — federation-review/03 §2 REC-3)

- **In plain terms:** Adds `partner { … }` next to `partnerId`/`partnerName` on watchlist partner rows.

- **Context:** `WatchlistPartner.partnerName` is *already* a live VMM lookup (`getByID(partnerId).bpName`,
G-02) — the entity ref exposes the full partner from the same underlying call instead of one denormalized
field. `partnerId`/`partnerName` stay (client contract).
- **Target DGS Implementation:** schema adds `partner: VMM_BusinessPartner` on `WatchlistPartner`; resolver
emits `{id: partnerId}` — gateway hydrates from VMM; null-safe on missing `partnerId`.

**Acceptance Criteria:**

1. PO approval recorded (OQ-5) before implementation starts
2. `partner { id name }` resolves via the gateway; `partnerName` parity is preserved
3. No additional VMM calls from the watchlist subgraph (stub emission only)

---

---

## Story Reference Table

| Story ID | Title | Phase | Complexity | Depends On |
|---|---|---|---|---|
| `WATCHLIST-BE-B-01` | `getWatchlistByIds(ids)` | B | 🟢 Low | — |
| `WATCHLIST-BE-B-02` | `getWatchlistReasons` (cacheable) | B | 🟢 Low | B-01 |
| `WATCHLIST-BE-B-03` | `getWatchlistInspectionActions` (cacheable) | B | 🟢 Low | B-01 |
| `WATCHLIST-BE-C-01` | `getWatchlistByFilter(...)` (4-step read) | C | 🟡 Medium | B-01 |
| `WATCHLIST-BE-D-01` | `createWatchlistEntries` | D | 🟡 Medium | B-01 |
| `WATCHLIST-BE-D-02` | `cloneFilesForWatchlist` | D | 🟡 Medium | B-01 |
| `WATCHLIST-BE-E-01` | `updateWatchlistEntries` (multi-step write) | E | 🟠 High | B-01 |
| `WATCHLIST-BE-F-01` | `Product.watchlists` (internal) | F | 🟢 Low | B-01 |
| `WATCHLIST-BE-F-02` | `ResourcesCount.watchlists` (internal — TechPack) | F | 🟢 Low | B-01 |
| `WATCHLIST-BE-G-01` | Computed flatteners (status/reasons/inspection action) | G | 🟢 Low | B-01 |
| `WATCHLIST-BE-G-02` | `createdBy` + `updatedBy` + `workspaces` + `participantDetails` + `partnerName` | G | 🟡 Medium | B-01 |
| `WATCHLIST-BE-G-03` | `attachments` + `product` | G | 🟡 Medium | B-01 |
| `WATCHLIST-BE-G-05` | `WatchlistPartner.partner` entity reference (recommended, PO-gated) | G | 🟢 Low | G-02 |