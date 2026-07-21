# Packaging — Comprehensive Migration Documentation

> **Domain:** `packaging` · **Target DGS:** `plm-product (co-located)` · **Generated:** 2026-07-19
> **Confluence location:** *Federation Graph Migration ▸ Domains ▸ packaging*

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Migration Scope](#migration-scope)
- [Story Summary by Phase](#story-summary-by-phase)
- [Decisions Required](#decisions-required)
- [Recommended Sprint Sequencing](#recommended-sprint-sequencing)
- [Capacity Planning](#capacity-planning)
- [Complex Story Breakdowns](#complex-story-breakdowns)
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

- We are moving the **Packaging** domain — packaging records, their dielines (print artwork specs), printers, elements, and exports — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is
**mid-sized with a wide schema** (24 object types, 20 inputs): 7 queries, 10 mutations, 17 field resolvers
on a 273-line resolver, but **no polymorphism**.

Two pieces carry the real work: **`updatePackaging`**, a multi-step write (body, then attachment
remove via archive + relationship, then attachment add via relationship + attribute update) with no
rollback; and **`suggestedRetailPriceByDPCI`**, a multi-hop pricing field (printers → dielines → DPCIs →
pricing service).

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive steps in `updatePackaging`) use **Mid-Request ACL Update** before the downstream call.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 10 | 9 simple + `updatePackaging` (multi-step) |
| Field-resolver type blocks | 4 | `Packaging` (12), `Dieline` (3), `PrinterDieline` (1), `PackagingElement` (1) |
| External dependencies | 7 keys (2 🔴 · 3 🟡 · 2 🔵) | search/attachment 🔴; relationship/user-profile/tag 🟡 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **24** | green-field |

---

## Story Summary by Phase

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 6 | 6–11d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 9 | 13–22d |
| E | Complex (`updatePackaging`) | 1 | 5–8d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 6 | 15–25d |
| **Total** | | **24** | **42–72d** (buffered) |

> One engineer ≈ **9–15 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

---

## Decisions Required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updatePackaging` failure strategy + align add/remove error handling | E-01 | Tech Lead + PO |
| 2 | `suggestedRetailPriceByDPCI` — cache the dieline→DPCI→pricing chain? | G-04 | Backend Eng |
| 3 | `updatePackagingComponentStatus` no token — backend-enforced? | D-09 | PO |
| 4 | Claims pass-through (`claimId`/`claimDetails`) — keep on packaging or route to claims? | B-01 | Product Owner |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, core reads |
| 2 | B-04–B-06 + C-01 + D-02/D-05–D-07 | master-data + search + simple mutations |
| 3 | D-01/D-03/D-04/D-08/D-09 | create/bulk/clone/component-status |
| 4 | E-01 + F-01 | multi-step update + Product links |
| 5 | G-01–G-03 | ACL/users/refs field resolvers |
| 6 | G-04/G-05 | pricing + dieline resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

---

## Capacity Planning

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~10–17 sprints | sequential |
| 2 engineers | ~6–10 sprints | reads + mutations parallel after B-01 |
| 3 engineers | ~4–7 sprints | critical path A → E-01 → G-04 → G-05 |

---
*Pipeline 2.0 — Phase 4 complete. Packaging artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*

---

## Complex Story Breakdowns

One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.

### High stories (split into M-size sub-tasks)

| Parent milestone | Why split | Sub-tasks |
|---|---|---|
| `PKG-BE-E-01` updatePackaging (body + attachment add/remove, branching) | see story | E-01-1 body + attachment add · E-01-2 attachment remove + pricing |

> Sub-tasks carry T-shirt size **M** (3–5 days). Parent stories are **milestones** (0 points in Jira).
> In Jira sub-tasks appear nested under their parent story.

---

## All Stories — Detailed Engineering Breakdown

> Each story is self-contained. Read: **Current Behaviour → Target → Acceptance Criteria**.
> Test cases are included only for **High** and **Very High** complexity stories.

### Phases Overview

| Phase | Name | Stories |
|---|---|---|
| B | Core Reads | B-01–B-06 |
| C | Search & Listing | C-01 |
| D | Mutations (simple) | D-01–D-09 |
| E | Complex (multi-step write) | E-01 |
| F | Federation (internal) | F-01 |
| G | Field Resolvers | G-01–G-05 |

> **Self-contained story model.** The Netflix-DGS-on-REST framework already exists, so **every operation story below is end-to-end in a single PR**: it adds the schema (query/mutation + the GraphQL type definitions it returns), the DGS data fetcher, the Kotlin REST service method (read or write) that calls the backend, and pushes the schema change to the **Hive** registry. There is **no separate service-layer story** — the former `*Service` Kotlin-port story has been dissolved into the operation stories.

---

### Phase B — Core Reads

#### PKG-BE-B-01 · `getPackagings(...)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** List packagings with paging and filters.

> **Note — DGS Module Init (this PR only):** Creates `packaging.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.
- **Current Behaviour (Q1):** (own) `getPackagings().load({page,size,packagingIds,parentIds,workspaceIds,partnerIds,statusIds})` → paged. **Target:** `@DgsQuery → PackagingPaged`.

**Acceptance Criteria:**

1. all 7 filter args forwarded; defaults page=0/size=10000

---

#### PKG-BE-B-02 · `getPackagingById(packagingId)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Fetch one packaging by id.

- **Current Behaviour (Q2):** (ACL context) token → (own) `getPackagingById.load(packagingId)`. **Target:** `@DgsQuery → Packaging`.

**Acceptance Criteria:**

1. returns packaging; miss→null

---

#### PKG-BE-B-03 · `getDielines(...)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** List dielines (print layouts) for a packaging.

- **Current Behaviour (Q3):** (own) `getDielines.load({...})` → `.dielines`. **Target:** `@DgsQuery → [Dieline]`.

**Acceptance Criteria:**

1. filters forwarded; returns the `dielines` array

---

#### PKG-BE-B-04 · `getPackagingFieldValuesByType(type, ids)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return packaging field-value lookups by type.

- **Current Behaviour (Q4):** (own) `getPackagingFieldValuesByType(type, ids)`. **Target:** `@DgsQuery → [PackagingFieldValues]`.

**Acceptance Criteria:**

1. by type (+optional ids)

---

#### PKG-BE-B-05 · `getDielineEvaluationStatuses` (cacheable)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the dieline evaluation-status lookup (cached).

- **Current Behaviour (Q5):** (own) `getDielineEvaluationStatuses()`. **Target:** `@DgsQuery` → `@Cacheable` → `[CodeDescription]`.

**Acceptance Criteria:**

1. returns statuses; cached

---

#### PKG-BE-B-06 · `getCountries(codes)` (cacheable)

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Return the country lookup (cached).

- **Current Behaviour (Q6):** (own) `getCountries(codes)`. **Target:** `@DgsQuery` → `@Cacheable` → `[Countries]`.

**Acceptance Criteria:**

1. returns countries (optionally filtered by codes)

---

### Phase C — Search & Listing

#### PKG-BE-C-01 · `getPackagingElastic(parentHumanId)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟡 Medium |
| **Phase** | C |
| **Depends on** | B-01 |
| **EXT** | 🔴 `search` |

- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search`

- **In plain terms:** Search a product's packagings via elastic.

- **Current Behaviour (Q7):** (🔴 search) `search.getPackagingElastic.load({ q:"parentId: {parentHumanId}" })` → `.content`. **EXT:** 🔴 search. **Target:** `@DgsQuery → [Packaging]`.

**Acceptance Criteria:**

1. `parentId:` elastic query built; returns content

---

### Phase D — Mutations (Simple)

#### PKG-BE-D-01 · `addPackaging`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Create a packaging.

- **Current Behaviour (M1):** (own) `POST packaging/v1`. **Throw on `validationErrors`/`message`.** **Target:** `@DgsMutation → Packaging`; port throw-on-error.

**Acceptance Criteria:**

1. creates
2. validation error → exception

---

#### PKG-BE-D-02 · `evaluateDieline`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Trigger evaluation of a dieline.

- **Current Behaviour (M3):** (own) `PUT packaging/v1/dielines/{dielineId}/evaluate`. **Target:** `@DgsMutation → Dieline`.

**Acceptance Criteria:**

1. evaluates the dieline

---

#### PKG-BE-D-03 · `bulkAddPackagings`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Create many packagings at once.

- **Current Behaviour (M4):** (own) `bulkAddPackagings`. **Throw on `validationErrors`/`message`.** **Target:** `@DgsMutation → PackagingBulk`.

**Acceptance Criteria:**

1. bulk creates
2. error → throw

---

#### PKG-BE-D-04 · `bulkUpdatePackagings`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Update many packagings at once.

- **Current Behaviour (M5):** token for `packaging[].humanId` → (own) `bulkUpdatePackagings`. **Throw on error.** **Target:** `@DgsMutation → PackagingBulk`.

**Acceptance Criteria:**

1. bulk updates
2. error → throw

---

#### PKG-BE-D-05 · `exportPackaging`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Kick off a packaging export.

- **Current Behaviour (M6):** token → (own) `requestPackagingExport({workspace_id, workspace_description, product_ids})` → request id. **Target:** `@DgsMutation → String`.

**Acceptance Criteria:**

1. returns the export request id

---

#### PKG-BE-D-06 · `lockPackaging`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Lock a packaging from edits.

- **Current Behaviour (M7):** token → `PUT packaging/v1/{id}/lock`. **Target:** `@DgsMutation → Packaging`.

**Acceptance Criteria:**

1. locks

---

#### PKG-BE-D-07 · `unlockPackaging`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Unlock a packaging.

- **Current Behaviour (M8):** token → `PUT packaging/v1/{id}/unlock`. **Target:** `@DgsMutation → Packaging`.

**Acceptance Criteria:**

1. unlocks

---

#### PKG-BE-D-08 · `cloneFilesForDielines`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment`

- **In plain terms:** Copy attachment files for dielines.

- **Current Behaviour (M9):** token → `Promise.all(attachmentIds.map(id => (🔴 attachment) cloneAttachmentV3({cloneReferences}, id)))`, flatten. **EXT:** 🔴 attachment. **Target:** structured-concurrency fan-out.

**Acceptance Criteria:**

1. clones each id with the shared `cloneReferences`

---

#### PKG-BE-D-09 · `updatePackagingComponentStatus`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Update component status on packagings.

- **Current Behaviour (M10):** (own) `updatePackagingComponentStatus({productId, ids, status})`. **No JWT — confirm backend-enforced.** **Target:** `@DgsMutation → PackagingPagedForStatus`.

**Acceptance Criteria:**

1. updates statuses
2. no-token behaviour documented

---

### Phase E — Complex Operations

#### PKG-BE-E-01 · `updatePackaging` (multi-step write)

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟠 High |
| **Phase** | E |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` · 🟡 `relationship` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |
| **Blocked by** | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |

- **Type:** Mutation · **Phase:** E · **Complexity:** 🔶 High · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment` · 🟡 `relationship` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module)

> **Draft ADR-013, ratification pending.** Against the shared `WriteSaga` module built in `PRODUCT-BE-E-00`:
> body PUT (validation checked **before** attachment side-effects — the late-check defect is fixed as an
> accepted deviation, ADR-013 pin-down 3) → attachment archive/attrs `RECORD`+reconcile → relationship
> add/remove `COMPENSATE`.

- **In plain terms:** Edit a packaging — a multi-step write (body + attachments + relationships) with no rollback today.

- **As a** DGS engineer **I want** the multi-step packaging update with a failure strategy **so that** body and
attachment add/remove changes stay consistent.
- **Current Behaviour (M2):** 1) token; set `humanId=packagingId`; `PUT packaging/v1` (body); 2) if
`attachmentsToRemove` → (🔴 attachment) `archiveAttachmentBulkV2` + (🟡 relationship) `removeRelationship`;
3) if `attachmentsToAdd` → (🟡 relationship) `addBulkRelationShip` (**reject on status≥400**) then
(🔴 attachment) `bulkUpdateAttributes`; 4) **throw on `validationErrors`/`message`**. No rollback.
- **EXT:** 🔴 attachment · 🟡 relationship. **Target:** ordered steps + chosen failure strategy

(**PO decision**); **align** the add/remove error handling (the remove branch currently swallows errors).

**Acceptance Criteria:**

1. all branches in order
2. add rejects on status≥400; remove error handling decided
3. partial-failure strategy

**Test Cases:**

- [ ] body-only
- [ ] remove
- [ ] add
- [ ] status≥400
- [ ] partial-failure
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### Phase F — Federation & Stitching

#### PKG-BE-F-01 · Product packaging links (internal, same subgraph)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | F |
| **Depends on** | B-01 |

- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Expose a product's packagings on the Product type (same subgraph).

- **Current Behaviour:** Product references packaging (e.g. `components(...packaging)`, packaging attributes)
from the co-located packaging service. **Target:** **internal** `@DgsData` calling `PackagingService`
in-process (not gateway federation; depends only on the `Product`/`Component` types existing).

**Acceptance Criteria:**

1. resolves in-process; no gateway hop

---

### Phase G — Field Resolvers, Bug-fixes & Tests

#### PKG-BE-G-01 · `access` + `businessPartner` + `participantDetails`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🔵 `vmm` · 🔵 `userGroup` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔵 `vmm` · 🔵 `userGroup`

- **In plain terms:** Resolve a packaging's access / partner / participant fields.

- **Current Behaviour:** `access` → `accessControl.getPermissions([humanId])[0]` (context); `businessPartner`
→ (🔵 vmm) `loadBpsWithType([businessPartner])[0]`; `participantDetails` → `getUserGroup(humanId||id)`.

**Acceptance Criteria:**

1. each resolves; null-safe

---

#### PKG-BE-G-02 · `createdBy` + `updatedBy` + `dielineEvaluators`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🟡 `userAttributes` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🟡 `userAttributes`

- **In plain terms:** Resolve the people fields on a packaging.

- **Current Behaviour:** `createdBy`/`updatedBy` (🟡 user-profile `getUser`); `dielineEvaluators` → map
`userAttributes.getUserByID`, default `[]`.

**Acceptance Criteria:**

1. each resolves; null id → null

---

#### PKG-BE-G-03 · `product` + `workspaces` + `attachments`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🔴 `search` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search`

- **In plain terms:** Resolve a packaging's product, workspaces and attachments.

- **Current Behaviour:** `product` (internal, only if `parentId` starts `'PID'`); `workspaces`
→ (🔴 search) `getWorkspacesPagedV3({q:"id:(...)"})`.content; `attachments`
→ (🔴 search) `searchAttachmentsByRelatedResource(humanId)`.

**Acceptance Criteria:**

1. `product` null when not `PID*`
2. workspaces/attachments via elastic

---

#### PKG-BE-G-04 · `suggestedRetailPriceByDPCI` + `waveDescription` + `retailPrice`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟠 High |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🟡 `tag` · 🔵 `apex` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** 🔶 High · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🟡 `tag` · 🔵 `apex`

- **In plain terms:** Resolve pricing fields (the dieline→DPCI→price chain).

- **Current Behaviour:** `suggestedRetailPriceByDPCI` — gated on `requiresSuggestedRetailPrice` + a BP id:
- collect printer ids from `packagingElements` → (own) `getDielines(printerIds)` → unique dpcis → (🔵 apex/pricing) `getRetailPriceByDpci({dpcis, bpId, productId})`; else `[]`.
- `waveDescription` → (🟡 tag) `getTag(wave).name` if `wave`, else `waveDescription`.
- `retailPrice` → `0` (deprecated).
- **Target:** port the pricing chain; cache/batch dielines.

**Acceptance Criteria:**

1. price chain matches source; gate honored
2. wave tag fallback
3. `retailPrice`→0

**Test Cases:**

- [ ] price chain
- [ ] gate
- [ ] wave
- [ ] retailPrice

---

#### PKG-BE-G-05 · `Dieline` + `PrinterDieline` + `PackagingElement` field resolvers

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` · 🔴 `search` · 🟡 `userAttributes` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment` · 🔴 `search` · 🟡 `userAttributes`

- **In plain terms:** Resolve the dieline / printer-dieline / element sub-type fields.

- **Current Behaviour:** `Dieline.evaluatedBy` (🟡 user-profile), `Dieline.attachments` (🔴 search),
`Dieline.attachment` (🔴 attachment `getAttachmentsV3([attachmentId])[0]`); `PrinterDieline.dielines`
(own `getDielines({printerIds, statusIds})`); `PackagingElement.packagingLibrary` (internal fileLibrary).

**Acceptance Criteria:**

1. each field resolves to the right source

---

---

## Story Reference Table

| Story ID | Title | Phase | Complexity | Depends On |
|---|---|---|---|---|
| `PKG-BE-B-01` | `getPackagings(...)` | B | 🟢 Low | — |
| `PKG-BE-B-02` | `getPackagingById(packagingId)` | B | 🟢 Low | B-01 |
| `PKG-BE-B-03` | `getDielines(...)` | B | 🟢 Low | B-01 |
| `PKG-BE-B-04` | `getPackagingFieldValuesByType(type, ids)` | B | 🟢 Low | B-01 |
| `PKG-BE-B-05` | `getDielineEvaluationStatuses` (cacheable) | B | 🟢 Low | B-01 |
| `PKG-BE-B-06` | `getCountries(codes)` (cacheable) | B | 🟢 Low | B-01 |
| `PKG-BE-C-01` | `getPackagingElastic(parentHumanId)` | C | 🟡 Medium | B-01 |
| `PKG-BE-D-01` | `addPackaging` | D | 🟡 Medium | B-01 |
| `PKG-BE-D-02` | `evaluateDieline` | D | 🟢 Low | B-01 |
| `PKG-BE-D-03` | `bulkAddPackagings` | D | 🟡 Medium | B-01 |
| `PKG-BE-D-04` | `bulkUpdatePackagings` | D | 🟡 Medium | B-01 |
| `PKG-BE-D-05` | `exportPackaging` | D | 🟢 Low | B-01 |
| `PKG-BE-D-06` | `lockPackaging` | D | 🟢 Low | B-01 |
| `PKG-BE-D-07` | `unlockPackaging` | D | 🟢 Low | B-01 |
| `PKG-BE-D-08` | `cloneFilesForDielines` | D | 🟡 Medium | B-01 |
| `PKG-BE-D-09` | `updatePackagingComponentStatus` | D | 🟢 Low | B-01 |
| `PKG-BE-E-01` | `updatePackaging` (multi-step write) | E | 🟠 High | B-01 |
| `PKG-BE-F-01` | Product packaging links (internal, same subgraph) | F | 🟢 Low | B-01 |
| `PKG-BE-G-01` | `access` + `businessPartner` + `participantDetails` | G | 🟡 Medium | B-01 |
| `PKG-BE-G-02` | `createdBy` + `updatedBy` + `dielineEvaluators` | G | 🟢 Low | B-01 |
| `PKG-BE-G-03` | `product` + `workspaces` + `attachments` | G | 🟡 Medium | B-01 |
| `PKG-BE-G-04` | `suggestedRetailPriceByDPCI` + `waveDescription` + `retailPrice` | G | 🟠 High | B-01 |
| `PKG-BE-G-05` | `Dieline` + `PrinterDieline` + `PackagingElement` field resolvers | G | 🟡 Medium | B-01 |