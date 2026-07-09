# Federated GraphQL Breakdown — Impression

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **XS** |
| **Total Stories** | 7 |
| **Complexity** | 🔴 0 Very High · 🟠 0 High · 🟡 2 Medium · 🟢 5 Low |
| **Phase Coverage** | 📖 B · ✏️ D · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Impression** domain (the product's printed/embellished artwork "impressions" and their per-partner counts) off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is the
**smallest and lowest-risk** of the thirteen domains: 2 queries, 1 mutation, and 6 field resolvers across a
66-line resolver — no polymorphism, no orchestration. We recommend migrating it **first** as a team warm-up
that proves the pipeline end-to-end.

- The only mild wrinkle is the counts query: today it returns the impressions **list** and a field resolver aggregates per-partner counts (re-fetching the product).
- We recommend a cleaner typed result as a fast-follow, but the existing contract can be preserved exactly.

**ACL note:** the current code obtains a per-product capability token via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

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

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

> _No spike-gated stories in this domain._

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads (incl. DGS module init + ImpressionService wiring) | 2 | 4–6d |
| D | Mutations | 1 | 2–3d |
| F | Federation (Product) | 1 | 1–2d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 3 | 4–7d |
| **Total** | | **7** | **11–18d** (buffered) |


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~3–5 sprints | sequential |
| 2 engineers | ~2–3 sprints | reads + field resolvers parallel |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B01 + B02 | **B01:** DGS module init (schema/types/stubs/scalars) + ImpressionService wiring + `searchImpressionsByProductId`; **B02:** counts query |
| 2 | D01 + G01 + G02 | mutation + field resolvers + counts aggregation |
| 3 | G03 | tests & parity |
| post-launch | F01 | Product extension (unblocked by product) |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-IMP-B01`<br>`searchImpressionsByProductId` data fetcher | 🟢 Low `XS` | Query | — | **Intent —** Find a product's impressions (colour / artwork placements).<br>**Done when:**<br>• `searchImpressionsByProductId(id)` returns impressions list; empty product → `[]`<br>• `partnerIds` and `workspaceIds` are forwarded as **repeated** query params (not CSV)<br>• `enableWorkspaceContextFiltering` intent is documented in code (forwarded or intentionally ignored)<br>• `./gradlew generateJava` passes and `DateTime` round-trips ISO-8601. *(One-time gate — verify once in this PR.)* |
| 🔷 `SPARK-IMP-B02`<br>`getImpressionCountsByProductId` data fetcher | 🟢 Low `XS` | Query | B01 | **Intent —** Count a product's impressions.<br>**Done when:**<br>• Returns the impressions list as the `ImpressionCount` parent type<br>• The contract decision (list-as-parent vs typed result) is recorded in story comments<br>• Empty product → `counts` yields `totalCount: 0` (verified by G02) |

> **`SPARK-IMP-B01`** — **Note — DGS Module Init (this PR only):** Creates `impression.graphqls` (federation v2.3 header,
> `scalar DateTime → Instant`, owned types `Impression @key(fields:"id")`, `ImpressionCount`,
> `CountsByBp`, 3 inputs, `@shareable CountsByBp`, plus external stubs for `VMM_BusinessPartner`,
> `Product`, `WorkspaceV2`, `UserProfileAttributes`) + registers the scalar in `ScalarConfig.kt` +
> wires `ImpressionClient` (Feign, GET repeated params + PUT snake/camel) and `ImpressionService`
> (`searchByProductId`, `update`). Full type list: 03-schema.graphql.


### ✏️ Phase D — Mutations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `SPARK-IMP-D01`<br>`updateImpressions` mutation | 🟡 Medium `M` | Mutation | B01 | **Intent —** Update a product's impressions.<br>**Done when:**<br>• PUT body includes both delete and update sets in snake_case<br>• Response is mapped to camelCase and returned as `List<Impression>`<br>• Backend `validationErrors` or `message` → typed `ImpressionValidationException` thrown (not a silent partial return) |


### 🔗 Phase F — Federation & Stitching (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-IMP-F01`<br>`Product.impressions` / `impressionCounts` (internal field resolver) | 🟢 Low `XS` | Field Resolver | B01 | **Intent —** Expose impressions and their counts on the Product type.<br>**Done when:**<br>• `Product.impressions` and `Product.impressionCounts` resolve in-process via `impressionService`<br>• No HTTP call is made during resolution (verified by unit test mock)<br>• Output matches the current product-side resolver (parity) |


### 🧪 Phase G — Field Resolvers & Tests (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-IMP-G01`<br>`Impression` field resolvers (5 fields) | 🟢 Low `XS` | Field Resolver | B01 | **Intent —** Resolve the individual Impression fields.<br>**Done when:**<br>• `businessPartners` and `owningBusinessPartner` resolve correctly from `partnerIds` / `owningPartnerId`<br>• `workspaces` returns `[]` when `workspaceContext` is empty; the workspace service is not called<br>• `createdBy` / `updatedBy`: `null` id returns `null` — no exception thrown |
| 🔸 `SPARK-IMP-G02`<br>`ImpressionCount.counts` aggregation | 🟡 Medium `M` | Field Resolver | B01 | **Intent —** Aggregate the per-type impression counts.<br>**Done when:**<br>• One row per product partner containing the correct filtered impression count<br>• Final row is always `{ bpType: 'totalCount', counts: <total impressions length> }`<br>• Empty impressions list or missing product → `[{ bpType: 'totalCount', counts: 0 }]` — no exception is propagated<br>• Product is fetched in-process; no HTTP call is made |
| 🔸 `SPARK-IMP-G03`<br>Test coverage & parity | 🟢 Low `XS` | Field Resolver | B01, B02, D01, G02 | **Intent —** Prove the impression logic matches the old gateway.<br>**Done when:**<br>• Unit test coverage ≥ 80% for all impression data fetchers<br>• Parity tests are green for search, counts, and the update mutation<br>• The `counts` error-fallback path is explicitly covered by a unit test |

