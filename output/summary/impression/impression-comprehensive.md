# Impression — Comprehensive Migration Documentation

> **Domain:** `impression` · **Target DGS:** `plm-product (co-located)` · **Generated:** 2026-07-19
> **Confluence location:** *Federation Graph Migration ▸ Domains ▸ impression*

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
  - [Phase D — Mutations (Simple)](#phase-d--mutations-simple)
  - [Phase F — Federation & Stitching](#phase-f--federation-stitching)
  - [Phase G — Field Resolvers, Bug-fixes & Tests](#phase-g--field-resolvers-bug-fixes-tests)
- [Story Reference Table](#story-reference-table)

---

## Executive Summary

- We are moving the **Impression** domain (the product's printed/embellished artwork "impressions" and their per-partner counts) off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is the
**smallest and lowest-risk** of the thirteen domains: 2 queries, 1 mutation, and 6 field resolvers across a
66-line resolver — no polymorphism, no orchestration. We recommend migrating it **first** as a team warm-up
that proves the pipeline end-to-end.

- The only mild wrinkle is the counts query: today it returns the impressions **list** and a field resolver aggregates per-partner counts (re-fetching the product).
- We recommend a cleaner typed result as a fast-follow, but the existing contract can be preserved exactly.

**ACL note:** the current code obtains a per-product capability token via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites use **Mid-Request ACL Update** before the downstream call. Impression has zero downstream-token sites.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one reuses the other's REST call |
| Mutations | 1 | delete + update sets in one PUT |
| Field-resolver type blocks | 2 | `Impression` (5), `ImpressionCount` (1) |
| External dependencies | 4 keys (0 🔴 · 1 🟡 · 3 🔵) | workspace, VMM, user-profile |
| Federation contributions | 1 (Product extension) | BLOCKED-BY product |
| **Total stories** | **7** | green-field |

---

## Story Summary by Phase

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads (incl. DGS module init + ImpressionService wiring) | 2 | 4–6d |
| D | Mutations | 1 | 2–3d |
| F | Federation (Product) | 1 | 1–2d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 3 | 4–7d |
| **Total** | | **7** | **11–18d** (buffered) |

---

## Decisions Required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Preserve `ImpressionCount` contract or adopt `ImpressionCountResult`? | B-02/G-02 | Product Owner |
| 2 | Should `enableWorkspaceContextFiltering` filter at the backend? | B-01 | Backend Eng |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 + B-02 | **B-01:** DGS module init (schema/types/stubs/scalars) + ImpressionService wiring + `searchImpressionsByProductId`; **B-02:** counts query |
| 2 | D-01 + G-01 + G-02 | mutation + field resolvers + counts aggregation |
| 3 | G-04 | `attachment` entity reference (recommended, PO-gated). Test coverage/parity tracked outside this Jira pipeline, created manually. |
| post-launch | F-01 | Product extension (unblocked by product) |

---

## Capacity Planning

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~3–5 sprints | sequential |
| 2 engineers | ~2–3 sprints | reads + field resolvers parallel |

---
*Pipeline 2.0 — Phase 4 complete. Impression artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Lowest-risk domain — recommended first migration.*

---

## All Stories — Detailed Engineering Breakdown

> Each story is self-contained. Read: **Current Behaviour → Target → Acceptance Criteria**.
> Test cases are included only for **High** and **Very High** complexity stories.

### Phases Overview

| Phase | Name | Stories |
|---|---|---|
| B | Core Reads | B-01–B-02 |
| D | Mutations | D-01 |
| F | Federation Contributions | F-01 *(BLOCKED-BY product)* |
| G | Field Resolvers | G-01–G-04 (G-04 recommended, PO-gated — federation review) |

---

### Phase B — Core Reads

#### IMPRESSION-BE-B-01 · `searchImpressionsByProductId` data fetcher

| Field | Value |
|---|---|
| **Type** | Story |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | — |

- **Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Category:** CAT-2  ·  **Depends on:** —

- **In plain terms:** Find a product's impressions (colour / artwork placements).

> **Note — DGS Module Init (this PR only):** Creates `impression.graphqls` (federation v2.3 header,
> `scalar DateTime → Instant`, owned types `Impression @key(fields:"id")`, `ImpressionCount`,
> `CountsByBp`, 3 inputs, `@shareable CountsByBp`, plus external stubs for `VMM_BusinessPartner`,
> `Product`, `WorkspaceV2`, `UserProfileAttributes`) + registers the scalar in `ScalarConfig.kt` +
> wires `ImpressionClient` (Feign, GET repeated params + PUT snake/camel) and `ImpressionService`
> (`searchByProductId`, `update`). Full type list: be-03-schema.graphql.

---

#### Current Behaviour

1. `GET {base}/…/impressions/product/{id}?workspaceIds=…&partnerIds=…` → camelCase list.
2. `partnerIds` and `workspaceIds` forwarded as **repeated** query-string params.
3. `enableWorkspaceContextFiltering` is accepted but **not forwarded** to the backend today — intent must be confirmed.

> **EXT Services:** None.  ·  **ACL note (context only):** capability token is ignored in DGS.

---

#### Target DGS Implementation

- **Annotation:** `@DgsQuery searchImpressionsByProductId(id, partnerIds, workspaceIds, enableWorkspaceContextFiltering): List<Impression>`
- **Service:** `impressionService.searchByProductId(...)` → `ImpressionClient` GET with repeated params
- **Request/Response mapping:** Jackson snake↔camel

---

#### Files

- `plm-product/.../schema/impression.graphqls`
- `plm-product/.../config/ScalarConfig.kt`
- `plm-product/.../service/ImpressionService.kt`
- `plm-product/.../client/ImpressionClient.kt`
- `plm-product/.../dataFetcher/ImpressionQueryDataFetcher.kt`

---

**Acceptance Criteria:**

1. `searchImpressionsByProductId(id)` returns impressions list; empty product → `[]`
2. `partnerIds` and `workspaceIds` are forwarded as **repeated** query params (not CSV)
3. `enableWorkspaceContextFiltering` intent is documented in code (forwarded or intentionally ignored)
4. `./gradlew generateJava` passes and `DateTime` round-trips ISO-8601. *(One-time gate — verify once in this PR.)*

---

#### IMPRESSION-BE-B-02 · `getImpressionCountsByProductId` data fetcher

| Field | Value |
|---|---|
| **Type** | Story |
| **Complexity** | 🟢 Low |
| **Phase** | B |
| **Depends on** | B-01 |

- **Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Category:** CAT-2  ·  **Depends on:** B-01

- **In plain terms:** Count a product's impressions.

---

#### Current Behaviour

1. Reuses the same REST search call as B-01 for `id`.
2. Returns the impressions list typed as `ImpressionCount`; the `counts` field (G-02) aggregates the list.

> **EXT Services:** None.

---

#### Target DGS Implementation

- **Annotation:** `@DgsQuery getImpressionCountsByProductId(id): ImpressionCount`
- Returns the search result as the `ImpressionCount` parent (G-02 computes the `counts` child field).
- **PO decision required:** preserve list-as-parent contract, or switch to a computed `ImpressionCountResult`?

---

#### Files

- `plm-product/.../dataFetcher/ImpressionQueryDataFetcher.kt`

---

**Acceptance Criteria:**

1. Returns the impressions list as the `ImpressionCount` parent type
2. The contract decision (list-as-parent vs typed result) is recorded in story comments
3. Empty product → `counts` yields `totalCount: 0` (verified by G-02)

---

### Phase D — Mutations (Simple)

#### IMPRESSION-BE-D-01 · `updateImpressions` mutation

| Field | Value |
|---|---|
| **Type** | Story |
| **Complexity** | 🟡 Medium |
| **Phase** | D |
| **Depends on** | B-01 |

- **Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Category:** CAT-2  ·  **Depends on:** B-01

- **In plain terms:** Update a product's impressions.

---

#### Current Behaviour

1. `PUT {base}/…/impressions/product/{productId}` with body `{ impressionsToDelete, impressionsToUpdate }` (snake_case).
2. On `validationErrors || message` in the response → throw.

> **EXT Services:** None.  ·  **ACL note (context only):** capability token for `productId`; ignored in DGS.

---

#### Target DGS Implementation

- **Annotation:** `@DgsMutation updateImpressions(productId, productImpression): List<Impression>`
- **Service:** `impressionService.update(...)` → `ImpressionClient` PUT (snake_case body, camelCase response)
- **Error handling:** `validationErrors` or `message` field → throw `ImpressionValidationException` (typed, not a raw GraphQL error)

---

#### Files

- `plm-product/.../dataFetcher/ImpressionMutationDataFetcher.kt`

---

**Acceptance Criteria:**

1. PUT body includes both delete and update sets in snake_case
2. Response is mapped to camelCase and returned as `List<Impression>`
3. Backend `validationErrors` or `message` → typed `ImpressionValidationException` thrown (not a silent partial return)

---

### Phase F — Federation & Stitching

#### IMPRESSION-BE-F-01 · `Product.impressions` / `impressionCounts` (internal field resolver)

| Field | Value |
|---|---|
| **Type** | Story |
| **Complexity** | 🟢 Low |
| **Phase** | F |
| **Depends on** | B-01 |
| **Blocked by** | product (`PRODUCT-BE-B-01`, exposes the field this story reads) |

- **Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Category:** CAT-2  ·  **Depends on:** B-01  ·  **Blocked by:** product (`PRODUCT-BE-B-01`, exposes the field this story reads)

- **In plain terms:** Expose impressions and their counts on the Product type.

---

> **Monorepo note:** `product` and `impression` share the `plm-product` subgraph — this is an **internal** field resolver, not gateway federation. No `@DgsEntityFetcher` or `@extends @external` is needed.

---

#### Current Behaviour

Product exposes `impressions` and `impressionCounts` resolved via the impression search call (currently inside spark-internal-graphql).

---

#### Target DGS Implementation

- **Annotation:** `@DgsData` fields on the internal `Product` type
- `Product.impressions(partnerIds, workspaceIds)` → `impressionService.searchByProductId(...)`
- `Product.impressionCounts` → same service call, typed as `ImpressionCount`
- No gateway hop — in-process call only.

---

#### Files

- `plm-product/.../dataFetcher/ProductImpressionFieldDataFetcher.kt`

---

**Acceptance Criteria:**

1. `Product.impressions` and `Product.impressionCounts` resolve in-process via `impressionService`
2. No HTTP call is made during resolution (verified by unit test mock)
3. Output matches the current product-side resolver (parity)

---

### Phase G — Field Resolvers, Bug-fixes & Tests

#### IMPRESSION-BE-G-01 · `Impression` field resolvers (5 fields)

| Field | Value |
|---|---|
| **Type** | Story |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-01 |

- **Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Category:** CAT-2  ·  **Depends on:** B-01

- **In plain terms:** Resolve the individual Impression fields.

---

#### Current Behaviour

1. `businessPartners` — `loadBpsWithType(partnerIds.map(p => ({ partnerId: p })))` (🟡 vmm)
2. `owningBusinessPartner` — `loadBp(owningPartnerId)` (🔵 vmm)
3. `workspaces` — `getWorkspacesByIdsV2(workspaceContext)` or `[]` when context is empty (🟡 workspaceV2)
4. `createdBy` — `userAttributes.getUserByID.load(createdById)` (🔵 user-profile)
5. `updatedBy` — `userAttributes.getUserByID.load(updatedById)` (🔵 user-profile)

> **EXT Services:** 🟡 workspaceV2 · 🔵 vmm · 🔵 user-profile

---

#### Target DGS Implementation

- Five `@DgsData` fields resolving via federated references / clients.
- `workspaces` returns `[]` when `workspaceContext` is empty — no service call is made.

---

#### Files

- `plm-product/.../dataFetcher/ImpressionFieldDataFetcher.kt`

---

**Acceptance Criteria:**

1. `businessPartners` and `owningBusinessPartner` resolve correctly from `partnerIds` / `owningPartnerId`
2. `workspaces` returns `[]` when `workspaceContext` is empty; the workspace service is not called
3. `createdBy` / `updatedBy`: `null` id returns `null` — no exception thrown

---

#### IMPRESSION-BE-G-02 · `ImpressionCount.counts` aggregation

| Field | Value |
|---|---|
| **Type** | Story |
| **Complexity** | 🟡 Medium |
| **Phase** | G |
| **Depends on** | B-01 |

- **Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Category:** CAT-2  ·  **Depends on:** B-01

- **In plain terms:** Aggregate the per-type impression counts.

- **As a** DGS migration engineer **I want** the `counts` aggregation **so that** clients receive per-partner and total impression counts without a second REST call.

---

#### Current Behaviour

1. Parent is the impressions array from the search result.
2. `parentId = impressions[0].parentId` → `product.getByID.load(parentId)` *(internal same-DGS)* → partner ids from the product.
3. Per-partner count: `impressions.filter(i => i.partnerIds.includes(partnerId)).length` for each partner id.
4. Append `{ bpType: 'totalCount', counts: impressions.length }` as the final row.
5. On **any** error → log and return `[{ bpType: 'totalCount', counts: 0 }]` (no exception thrown).

> **EXT Services:** None — `product` is internal (same `plm-product` subgraph).

---

#### Target DGS Implementation

- **Annotation:** `@DgsData counts` on `ImpressionCount`
- Product fetched via `productService.getById(parentId)` (in-process, no HTTP).
- Computes per-partner rows then appends the `totalCount` row.
- Preserves the try/catch fallback: any error → `[{ bpType:'totalCount', counts:0 }]`.
- **PO note:** if `ImpressionCountResult` restructure is adopted (see B-02), this becomes a fetcher-level computation instead of a child field.

---

#### Files

- `plm-product/.../dataFetcher/ImpressionCountFieldDataFetcher.kt`

---

**Acceptance Criteria:**

1. One row per product partner containing the correct filtered impression count
2. Final row is always `{ bpType: 'totalCount', counts: <total impressions length> }`
3. Empty impressions list or missing product → `[{ bpType: 'totalCount', counts: 0 }]` — no exception is propagated
4. Product is fetched in-process; no HTTP call is made

---

#### IMPRESSION-BE-G-04 · `attachment` entity reference (recommended, PO-gated)

| Field | Value |
|---|---|
| **Type** | Field Resolver |
| **Complexity** | 🟢 Low |
| **Phase** | G |
| **Depends on** | B-01 |
| **EXT** | 🔴 `attachment` |
| **Status** | Recommended (PO-gated — federation-review/03 §2 REC-2) |

- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** B-01 · **EXT:** 🔴 `attachment`
- **Status:** Recommended (PO-gated — federation-review/03 §2 REC-2)

- **In plain terms:** Adds `attachment { … }` next to `attachmentId` so clients get file metadata without a
separate attachment-API round-trip.

- **Context:** clients select `attachmentId` on `searchImpressionsByProductId`
(`ClientCallingGqlQueries/product-queries__ProductQueries.txt:309`) and then resolve the file separately.
`attachmentId` stays (thumbnail-URL building contract).
- **Target DGS Implementation:** schema adds `attachment: Attachment` (declare the `Attachment @extends
@key(fields:"id")` stub); resolver emits `{id: attachmentId}` — the gateway/attachment subgraph hydrates
(phase 2; until then the stitched gateway serves it). Optionally pair with `associatedBoms: [Bom]`
(internal co-located resolver) if the UI asks — currently deferred (federation-review/03 §3).

**Acceptance Criteria:**

1. PO approval recorded (OQ-5) before implementation starts
2. `attachment { id }` resolves as a stub; `attachmentId` unchanged (parity)
3. Null-safe when `attachmentId` is absent

---

---

## Story Reference Table

| Story ID | Title | Phase | Complexity | Depends On |
|---|---|---|---|---|
| `IMPRESSION-BE-B-01` | `searchImpressionsByProductId` data fetcher | B | 🟢 Low | — |
| `IMPRESSION-BE-B-02` | `getImpressionCountsByProductId` data fetcher | B | 🟢 Low | B-01 |
| `IMPRESSION-BE-D-01` | `updateImpressions` mutation | D | 🟡 Medium | B-01 |
| `IMPRESSION-BE-F-01` | `Product.impressions` / `impressionCounts` (internal field resolver) | F | 🟢 Low | B-01 |
| `IMPRESSION-BE-G-01` | `Impression` field resolvers (5 fields) | G | 🟢 Low | B-01 |
| `IMPRESSION-BE-G-02` | `ImpressionCount.counts` aggregation | G | 🟡 Medium | B-01 |
| `IMPRESSION-BE-G-04` | `attachment` entity reference (recommended, PO-gated) | G | 🟢 Low | B-01 |