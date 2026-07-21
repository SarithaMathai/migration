# Product Details — Comprehensive Migration Documentation

> **Domain:** `productDetails` · **Target DGS:** `plm-product (co-located)` · **Generated:** 2026-07-19
> **Confluence location:** *Federation Graph Migration ▸ Domains ▸ productDetails*

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

We are moving the **ProductDetails** domain — the product's "construction" sets (build/assembly detail rows,
their attachments, and per-partner access) — off the `spark-internal-graphql` gateway into the
**`plm-product`** DGS. It is **mid-sized and mid-low risk**: 2 queries, 6 mutations, 12 field resolvers on a
129-line resolver, with **no polymorphism**. (In the backend this domain is called *construction* —
`construction/v1`; the GraphQL names stay `productDetails`.)

The one genuinely harder piece is **`updateProductDetailsSet`**, a multi-step write — workspace
associations, then bulk-archive removed attachments, then the body — with no rollback today.

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive step in `updateProductDetailsSet`) use **Mid-Request ACL Update** before the downstream call.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one by-ids (internal), one elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateProductDetailsSet` (multi-step) |
| Field-resolver type blocks | 3 | `ProductDetails` (10), item (2), category (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

---

## Story Summary by Phase

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 1 | 1–2d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateProductDetailsSet`) | 1 | 4–7d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 4 | 9–15d |
| **Total** | | **13** | **24–42d** (buffered) |

> One engineer ≈ **5–9 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

---

## Decisions Required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateProductDetailsSet` failure strategy | E-01 | Tech Lead + PO |
| 2 | `updateProductDetailComponentStatus` no token — backend-enforced? | D-05 | PO |
| 3 | `getProductDetailsElastic.types` — add to schema or drop? | C-01 | Backend Eng |
| 4 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | D-01–D-05 | simple mutations |
| 3 | E-01 + F-01 | multi-step write + Product field |
| 4 | G-01–G-03 | field resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

---

## Capacity Planning

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

---
*Pipeline 2.0 — Phase 4 complete. ProductDetails artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*

---

## All Stories — Detailed Engineering Breakdown

> Each story is self-contained. Read: **Current Behaviour → Target → Acceptance Criteria**.
> Test cases are included only for **High** and **Very High** complexity stories.

### Phases Overview

| Phase | Name | Stories |
|---|---|---|
| B | Core Reads | B-01 |
| C | Search & Listing | C-01 |
| D | Mutations (simple) | D-01–D-05 |
| E | Complex (multi-step write) | E-01 |
| F | Federation (internal) | F-01 |
| G | Field Resolvers | G-01–G-03 |

> **Self-contained story model.** The Netflix-DGS-on-REST framework already exists, so **every operation story below is end-to-end in a single PR**: it adds the schema (query/mutation + the GraphQL type definitions it returns), the DGS data fetcher, the Kotlin REST service method (read or write) that calls the backend, and pushes the schema change to the **Hive** registry. There is **no separate service-layer story** — the former `*Service` Kotlin-port story has been dissolved into the operation stories.

---

### Phase B — Core Reads

#### PDTL-BE-B-01 · `getProductDetailsById(ids)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Fetch product-detail (construction) sets by id.

> **Note — DGS Module Init (this PR only):** Creates `productDetails.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.
- **Current Behaviour (Q1):** (ACL context) token for `ids` → `GET construction/v1?ids={csv}` → camelCase list.
- **Target:** `@DgsQuery getProductDetailsById(ids): [ProductDetails]`.

**Acceptance Criteria:**

1. returns list for ids; empty → []

---

### Phase C — Search & Listing

#### PDTL-BE-C-01 · `getProductDetailsElastic(resourceId)`

| Field | Value |
|---|---|
| **Type** | Query |
| **Complexity** | 🟡 Medium |
| **Phase** | C |
| **Depends on** | B-01 |
| **EXT** | 🔴 `search` |

- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search`

- **In plain terms:** Search a product's product-detail sets via elastic.

- **Current Behaviour (Q2):** (🔴 search) `search.getProductDetailsElastic.load({ q:"parentId: {resourceId}" })` → paged.
- **EXT:** 🔴 search. **Target:** `@DgsQuery → ProductDetailsPaged`. **Note:** the source resolver reads a `types` arg not in the SDL — drop (or add to schema) per 03-analysis §2.

**Acceptance Criteria:**

1. `parentId:` elastic query built
2. paged shape returned

---

### Phase D — Mutations (Simple)

#### PDTL-BE-D-01 · `createProductDetailsSet`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Create a product-detail set.

- **Current Behaviour (M1):** (ACL context) token for literal capability → `POST construction/v1` (snake_case). **If response has `validationErrors` or `message` → throw.** **Target:** `@DgsMutation`; port the throw-on-error contract.

**Acceptance Criteria:**

1. creates set
2. validation error → exception (not a partial object)

---

#### PDTL-BE-D-02 · `updateProductDetailAccess`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Change who can access a product-detail set.

- **Current Behaviour (M2):** map `managePermissionsRequest[].resourceId` → token → `PUT construction/v1/manage-permissions` (`primeKey=humanId`). **Target:** `@DgsMutation → [ProductDetails]`.

**Acceptance Criteria:**

1. updates partner access for each resource

---

#### PDTL-BE-D-03 · `productDetailLockUnlock`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Lock or unlock a product-detail set.

- **Current Behaviour (M3):** token for `[constructionSetId]` → `PUT construction/v1/{id}/{lock|unlock}`. **Target:** `@DgsMutation`.

**Acceptance Criteria:**

1. `isLock=true`→lock path, false→unlock path

---

#### PDTL-BE-D-04 · `cloneFilesForProductDetails`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` |

- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment`

- **In plain terms:** Copy attachment files for product details.

- **Current Behaviour (M5):** token → `Promise.all(attachmentIds.map((id,i) => (🔴 attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id)))`, stamp `parentResource=id`, flatten. No rollback. **EXT:** 🔴 attachment. **Target:** structured-concurrency fan-out via `AttachmentClient`.

**Acceptance Criteria:**

1. clones each id with its paired cloneReference
2. `parentResource` stamped

---

#### PDTL-BE-D-05 · `updateProductDetailComponentStatus`

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟢 Low |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Update component status on product-detail sets.

- **Current Behaviour (M6):** `PUT construction/v1/component_status_update`; wraps result as `{content}`. **No JWT — confirm backend-enforced.** **Target:** `@DgsMutation → ProductDetailsPaged`.

**Acceptance Criteria:**

1. updates statuses; result wrapped as `{content}`
2. no-token behaviour documented

---

### Phase E — Complex Operations

#### PDTL-BE-E-01 · `updateProductDetailsSet` (multi-step write)

| Field | Value |
|---|---|
| **Type** | Mutation |
| **Complexity** | 🟠 High |
| **Phase** | E |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` · 🟡 `workspaceV2` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |
| **Blocked by** | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) |

- **Type:** Mutation · **Phase:** E · **Complexity:** 🔶 High · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment` · 🟡 `workspaceV2` · **Blocked by:** product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module)

> **Draft ADR-013, ratification pending.** Against the shared `WriteSaga` module built in `PRODUCT-BE-E-00`:
> workspace assoc `COMPENSATE` (fix the copy-paste 'measurement set' error text) → attachment archive
> `RECORD` (destructive step currently runs before the body — order preserved for parity, failure now
> visible) → body PUT checked (today returned unchecked, ADR-013 pin-down 5).

- **In plain terms:** Edit a product-detail set — a multi-step write (workspace + body) with no rollback today.

- **As a** DGS engineer **I want** the multi-step product-details update with a failure strategy **so that**
workspace, attachment, and body changes stay consistent.
- **Current Behaviour (M4):** 1) if `workspaceContext.{add,remove}Workspaces` non-empty →
`workspaceAssociationHelper(PRODUCT_DETAIL, id, add, remove)` (throws on error); 2) null `workspaceContext`;
3) if `deleteAttachmentIds` → (🔴 attachment) `archiveAttachmentBulkV3` (separate ACL token);
4) `PUT construction/v1/{id}`. **No rollback across steps.**
- **EXT:** 🔴 attachment · 🟡 workspaceV2. **Target:** ordered steps with a chosen failure strategy

(**PO decision** saga / compensation log / best-effort).

**Acceptance Criteria:**

1. all 4 steps in order
2. partial-failure strategy implemented
3. workspace assoc throws propagate

**Test Cases:**

- [ ] full path
- [ ] workspace-only
- [ ] attachment-archive
- [ ] partial-failure
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### Phase F — Federation & Stitching

#### PDTL-BE-F-01 · `Product.productDetails` (internal, same subgraph)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | F |
| **Depends on** | B-01 |

- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01

- **In plain terms:** Expose a product's product-details on the Product type (same subgraph).

- **Current Behaviour:** Product exposes `productDetails` resolved from the co-located ProductDetails service. **Target:** **internal** `@DgsData` on `Product` calling `ProductDetailsService` in-process (not gateway federation; depends only on the `Product` type existing).

**Acceptance Criteria:**

1. `Product.productDetails` resolves in-process; no gateway hop

---

### Phase G — Field Resolvers, Bug-fixes & Tests

#### PDTL-BE-G-01 · `access` + `currentUserPermissions` + `participantDetails`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🔵 `userGroup` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔵 `userGroup`

- **In plain terms:** Resolve access / permission / participant fields.

- **Current Behaviour:** `access` → `accessControl.getPermissions([humanId||id])[0]`; `currentUserPermissions`
→ `getUserAccessUnencoded(humanId||id)[0]`; `participantDetails` → `getUserGroup(humanId)`. (ACL context.) **Target:** thin `@DgsData`; ACL is context-only.

**Acceptance Criteria:**

1. each field resolves; null-safe on empty

---

#### PDTL-BE-G-02 · `product` + `createdBy` + `updatedBy` + `businessPartners` + `workspaces`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🟡 `userAttributes` · 🟡 `workspaceV2` · 🔵 `vmm` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🟡 `userAttributes` · 🟡 `workspaceV2` · 🔵 `vmm`

- **In plain terms:** Resolve the product, people, partner and workspace fields.

- **Current Behaviour:** `product` (internal, only if `parentId` starts `'PID'`), `createdBy`/`updatedBy`
(🟡 user-profile), `businessPartners` (🔵 vmm `loadBpsWithType`), `workspaces` (🟡 workspaceV2 by ids). **Target:** internal + federated references.

**Acceptance Criteria:**

1. each resolves; `product` null when `parentId` not `PID*`
2. null id → null user

---

#### PDTL-BE-G-03 · `attachment` + item `attachment`/`constructionSetAttachments` + category `subCategories`

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🔴 `search` |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `search`

- **In plain terms:** Resolve attachment and category fields on product details.

- **Current Behaviour:** `ProductDetails.attachment` → (🔴 search) `searchAttachments([humanId||id])`, find
- `relatedResources.length<=2`; `ProductDetailsItem.attachment` → `searchAttachments([templateId])[0]||{}`; `constructionSetAttachments` → `searchAttachments([id]).content||[]`; `CategoryWithSection.subCategories` → (internal `specificationsTemplate`) `getProductDetailsCategorySection()` find by `code`.
- **Target:** shared search helper + internal master-data call.

**Acceptance Criteria:**

1. each field resolves to the right source
2. `attachment` length-≤2 filter preserved

---

---

## Story Reference Table

| Story ID | Title | Phase | Complexity | Depends On |
|---|---|---|---|---|
| `PDTL-BE-B-01` | `getProductDetailsById(ids)` | B | 🟢 Low | — |
| `PDTL-BE-C-01` | `getProductDetailsElastic(resourceId)` | C | 🟡 Medium | B-01 |
| `PDTL-BE-D-01` | `createProductDetailsSet` | D | 🟡 Medium | B-01 |
| `PDTL-BE-D-02` | `updateProductDetailAccess` | D | 🟢 Low | B-01 |
| `PDTL-BE-D-03` | `productDetailLockUnlock` | D | 🟢 Low | B-01 |
| `PDTL-BE-D-04` | `cloneFilesForProductDetails` | D | 🟡 Medium | B-01 |
| `PDTL-BE-D-05` | `updateProductDetailComponentStatus` | D | 🟢 Low | B-01 |
| `PDTL-BE-E-01` | `updateProductDetailsSet` (multi-step write) | E | 🟠 High | B-01 |
| `PDTL-BE-F-01` | `Product.productDetails` (internal, same subgraph) | F | 🟢 Low | B-01 |
| `PDTL-BE-G-01` | `access` + `currentUserPermissions` + `participantDetails` | G | 🟡 Medium | B-01 |
| `PDTL-BE-G-02` | `product` + `createdBy` + `updatedBy` + `businessPartners` + `workspaces` | G | 🟡 Medium | B-01 |
| `PDTL-BE-G-03` | `attachment` + item `attachment`/`constructionSetAttachments` + category `subCategories` | G | 🟡 Medium | B-01 |