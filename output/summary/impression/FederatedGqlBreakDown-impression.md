## Backend

### Federated GraphQL Breakdown — Impression

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **XS** |
| **Total Stories** | 7 |
| **Complexity** | 🔴 0 Very High · 🟠 0 High · 🟡 2 Medium · 🟢 5 Low |
| **Phase Coverage** | 📖 B · ✏️ D · 🔗 F · 🧪 G |
| **Generated** | 2026-07-19 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H

---

#### What Are We Building?

- We are moving the **Impression** domain (the product's printed/embellished artwork "impressions" and their per-partner counts) off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is the
**smallest and lowest-risk** of the thirteen domains: 2 queries, 1 mutation, and 6 field resolvers across a
66-line resolver — no polymorphism, no orchestration. We recommend migrating it **first** as a team warm-up
that proves the pipeline end-to-end.

- The only mild wrinkle is the counts query: today it returns the impressions **list** and a field resolver aggregates per-partner counts (re-fetching the product).
- We recommend a cleaner typed result as a fast-follow, but the existing contract can be preserved exactly.

**ACL note:** the current code obtains a per-product capability token via ACL. Per **ADR-019** ([`complexStories/acl/01-adr-acl-mid-request-update.md`](https://github.com/XXX/blob/main/output/complexStories/acl/01-adr-acl-mid-request-update.md)), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites use **Mid-Request ACL Update** before the downstream call. Impression has zero downstream-token sites.

---

#### Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one reuses the other's REST call |
| Mutations | 1 | delete + update sets in one PUT |
| Field-resolver type blocks | 2 | `Impression` (5), `ImpressionCount` (1) |
| External dependencies | 4 keys (0 🔴 · 1 🟡 · 3 🔵) | workspace, VMM, user-profile |
| Federation contributions | 1 (Product extension) | BLOCKED-BY product |
| **Total stories** | **7** | green-field |

---

#### Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

> _No spike-gated stories in this domain._

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

#### Effort Snapshot

| Phase | Name | Stories | Effort (est., +20% buffer) |
|-------|------|---------|----------------------------|
| B | Core Reads | 2 | 2–5d |
| D | Mutations | 1 | 2–5d |
| F | Federation & Stitching | 1 | 1–2d |
| G | Field Resolvers & Tests | 3 | 5–10d |
| **Total** | | **7** | **10–22d** (buffered) |

> Computed live from `be-04-stories.md` (phase + complexity per story) — always reconciles with the story tables below and the program overview. Effort = sum of per-story nominal day-ranges (Low 1–2 · Medium 2–4 · High 4–7 · Very High 7–12) × 1.2 buffer, AI-estimated — confirm in refinement. See each story's **Depends On** column for real sequencing.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~3–5 sprints | sequential |
| 2 engineers | ~2–3 sprints | reads + field resolvers parallel |

---

#### Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 + B-02 | **B-01:** DGS module init (schema/types/stubs/scalars) + ImpressionService wiring + `searchImpressionsByProductId`; **B-02:** counts query |
| 2 | D-01 + G-01 + G-02 | mutation + field resolvers + counts aggregation |
| 3 | G-04 | `attachment` entity reference (recommended, PO-gated). Test coverage/parity tracked outside this Jira pipeline, created manually. |
| post-launch | F-01 | Product extension (unblocked by product) |

---

#### Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟢 `B-02`, 🟡 `D-01`, 🟢 `F-01`, 🟢 `G-01`, 🟡 `G-02`, 🟢 `G-04` | `F-01` → ⛔ BLOCKED-BY product (PRODUCT-BE-B-01, exposes the field this story reads) | Fan-out — 📖 Core Reads · ✏️ Mutations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `B-02` — 2 sequential stories; everything else hangs off this chain in parallel.

---

#### Recommended Story Graph — 1 Backend Engineer

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 1 backend engineer** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 |
|---|---|
| 1 | 🟢 `B-01` (1–2d) |
| 2 | 🟡 `D-01` (2–4d) |
| 3 | 🟡 `G-02` (2–4d) |
| 4 | 🟢 `B-02` (1–2d) |
| 5 | 🟢 `F-01` (1–2d) ⛔ |
| 6 | 🟢 `G-01` (1–2d) |
| 7 | 🟢 `G-04` (1–2d) |

**BE-1:** `B-01` → `D-01` → `G-02` → `B-02` → `F-01` → `G-01` → `G-04`

**Elapsed (nominal midpoints):** ~14 working days.

---

#### Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

##### 📖 Phase B — Core Reads (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `IMPRESSION-BE-B-01`<br>`searchImpressionsByProductId` data fetcher | 🟢 Low `XS` | Query | — | **Intent —** Find a product's impressions (colour / artwork placements).<br>**Done when:**<br>• `searchImpressionsByProductId(id)` returns impressions list; empty product → `[]`<br>• `partnerIds` and `workspaceIds` are forwarded as **repeated** query params (not CSV)<br>• `enableWorkspaceContextFiltering` intent is documented in code (forwarded or intentionally ignored)<br>• `./gradlew generateJava` passes and `DateTime` round-trips ISO-8601. *(One-time gate — verify once in this PR.)* |
| 🔷 `IMPRESSION-BE-B-02`<br>`getImpressionCountsByProductId` data fetcher | 🟢 Low `XS` | Query | B-01 | **Intent —** Count a product's impressions.<br>**Done when:**<br>• Returns the impressions list as the `ImpressionCount` parent type<br>• The contract decision (list-as-parent vs typed result) is recorded in story comments<br>• Empty product → `counts` yields `totalCount: 0` (verified by G-02) |

> **`IMPRESSION-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `impression.graphqls` (federation v2.3 header,
> `scalar DateTime → Instant`, owned types `Impression @key(fields:"id")`, `ImpressionCount`,
> `CountsByBp`, 3 inputs, `@shareable CountsByBp`, plus external stubs for `VMM_BusinessPartner`,
> `Product`, `WorkspaceV2`, `UserProfileAttributes`) + registers the scalar in `ScalarConfig.kt` +
> wires `ImpressionClient` (Feign, GET repeated params + PUT snake/camel) and `ImpressionService`
> (`searchByProductId`, `update`). Full type list: be-03-schema.graphql.


##### ✏️ Phase D — Mutations (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `IMPRESSION-BE-D-01`<br>`updateImpressions` mutation | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Update a product's impressions.<br>**Done when:**<br>• PUT body includes both delete and update sets in snake_case<br>• Response is mapped to camelCase and returned as `List<Impression>`<br>• Backend `validationErrors` or `message` → typed `ImpressionValidationException` thrown (not a silent partial return) |


##### 🔗 Phase F — Federation & Stitching (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `IMPRESSION-BE-F-01`<br>`Product.impressions` / `impressionCounts` (internal field resolver) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Expose impressions and their counts on the Product type.<br>**Done when:**<br>• `Product.impressions` and `Product.impressionCounts` resolve in-process via `impressionService`<br>• No HTTP call is made during resolution (verified by unit test mock)<br>• Output matches the current product-side resolver (parity) |


##### 🧪 Phase G — Field Resolvers & Tests (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `IMPRESSION-BE-G-01`<br>`Impression` field resolvers (5 fields) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Resolve the individual Impression fields.<br>**Done when:**<br>• `businessPartners` and `owningBusinessPartner` resolve correctly from `partnerIds` / `owningPartnerId`<br>• `workspaces` returns `[]` when `workspaceContext` is empty; the workspace service is not called<br>• `createdBy` / `updatedBy`: `null` id returns `null` — no exception thrown |
| 🔸 `IMPRESSION-BE-G-02`<br>`ImpressionCount.counts` aggregation | 🟡 Medium `M` | Field Resolver | B-01 | **Intent —** Aggregate the per-type impression counts.<br>**Done when:**<br>• One row per product partner containing the correct filtered impression count<br>• Final row is always `{ bpType: 'totalCount', counts: <total impressions length> }`<br>• Empty impressions list or missing product → `[{ bpType: 'totalCount', counts: 0 }]` — no exception is propagated<br>• Product is fetched in-process; no HTTP call is made |
| 🔸 `IMPRESSION-BE-G-04`<br>`attachment` entity reference (recommended, PO-gated) | 🟢 Low `XS` | Field Resolver<br>Calls: `attachment` | B-01 | **Intent —** Adds `attachment { … }` next to `attachmentId` so clients get file metadata without a<br>**Today —** schema adds attachment: Attachment (declare the `Attachment @extends<br>**Done when:**<br>• PO approval recorded (OQ-5) before implementation starts<br>• `attachment { id }` resolves as a stub; `attachmentId` unchanged (parity)<br>• Null-safe when `attachmentId` is absent |



---

## Frontend

### Federated GraphQL Breakdown — Impression · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 2 |
| **Impact** | 🔴 0 High · 🟡 0 Medium · 🟢 2 Low |
| **Estimated effort** | 3–5 days (single-engineer) |
| **Phase-1 surface** | 2 operation-to-root-field rows · 2 client files · 4 components |
| **Generated** | 2026-07-19 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

#### What Are We Changing?

- Point the **Impression** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

#### Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `IMPRESSION-FE-001` | Migrate `getBomDataAndImpressions` (with BOM wave) | Query migration | 🟢 Low | 2–3 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-17`, `BOM-FE-002`, `IMPRESSION-BE-B-01`, `IMPRESSION-BE-G-01`, `PRODUCT-BE-B-01` | `searchImpressionsByProductId`, `getBomByIds` |
| `IMPRESSION-FE-002` | Migrate `getCarryForwardFormData` (with Product wave) | Query migration | 🟢 Low | 1–2 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-17`, `IMPRESSION-BE-B-01`, `IMPRESSION-BE-G-01`, `PRODUCT-BE-B-01`, `PRODUCT-BE-G-01`, `PRODUCT-BE-G-02`, `PRODUCT-BE-G-03`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-08`, `PRODUCT-BE-G-09`, `PRODUCT-BE-G-10`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-01`, `PRODUCT-FE-001` | `searchImpressionsByProductId`, `getProduct` |

---

#### Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 4 | 🟢 `IMPRESSION-FE-001` | `IMPRESSION-FE-001` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01` (+9) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🟢 `IMPRESSION-FE-002` | `IMPRESSION-FE-002` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-G-01` (+19) | Externally gated — search/read-hub decision |

**Cutover flow:** `IMPRESSION-FE-001` → `IMPRESSION-FE-002`.

---

#### Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 4 | 🟢 `IMPRESSION-FE-001` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🟢 `IMPRESSION-FE-002` (1–2d) | Externally gated — search/read-hub decision |

**Elapsed (nominal midpoints):** ~4 FE build days — calendar time is set by the backend gates, not FE capacity.

---

#### References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-impression.md — the combined Backend + Frontend breakdown this section lives in.

