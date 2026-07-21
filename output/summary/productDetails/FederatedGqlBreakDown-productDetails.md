## Backend

### Federated GraphQL Breakdown — Product Details

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **M** |
| **Total Stories** | 12 |
| **Complexity** | 🔴 0 Very High · 🟠 1 High · 🟡 6 Medium · 🟢 5 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-19 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H

---

#### What Are We Building?

We are moving the **ProductDetails** domain — the product's "construction" sets (build/assembly detail rows,
their attachments, and per-partner access) — off the `spark-internal-graphql` gateway into the
**`plm-product`** DGS. It is **mid-sized and mid-low risk**: 2 queries, 6 mutations, 12 field resolvers on a
129-line resolver, with **no polymorphism**. (In the backend this domain is called *construction* —
`construction/v1`; the GraphQL names stay `productDetails`.)

The one genuinely harder piece is **`updateProductDetailsSet`**, a multi-step write — workspace
associations, then bulk-archive removed attachments, then the body — with no rollback today.

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** ([`complexStories/acl/01-adr-acl-mid-request-update.md`](https://github.com/XXX/blob/main/output/complexStories/acl/01-adr-acl-mid-request-update.md)), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive step in `updateProductDetailsSet`) use **Mid-Request ACL Update** before the downstream call.

---

#### Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one by-ids (internal), one elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateProductDetailsSet` (multi-step) |
| Field-resolver type blocks | 3 | `ProductDetails` (10), item (2), category (1) |
| External dependencies | 6 keys (2 🔴 · 2 🟡 · 2 🔵) | search/attachment 🔴 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **13** | green-field |

---

#### Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `PDTL-BE-E-01` — `updateProductDetailsSet` (multi-step write) | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

#### Effort Snapshot

| Phase | Name | Stories | Effort (est., +20% buffer) |
|-------|------|---------|----------------------------|
| B | Core Reads | 1 | 1–2d |
| C | Search & Listing | 1 | 2–5d |
| D | Mutations | 5 | 8–17d |
| E | Complex Operations | 1 | 5–8d |
| F | Federation & Stitching | 1 | 1–2d |
| G | Field Resolvers & Tests | 3 | 7–14d |
| **Total** | | **12** | **24–48d** (buffered) |

> Computed live from `be-04-stories.md` (phase + complexity per story) — always reconciles with the story tables below and the program overview. Effort = sum of per-story nominal day-ranges (Low 1–2 · Medium 2–4 · High 4–7 · Very High 7–12) × 1.2 buffer, AI-estimated — confirm in refinement. See each story's **Depends On** column for real sequencing.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

---

#### Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | D-01–D-05 | simple mutations |
| 3 | E-01 + F-01 | multi-step write + Product field |
| 4 | G-01–G-03 | field resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

---

#### Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟡 `C-01`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟡 `D-04`, 🟢 `D-05`, 🟠 `E-01`, 🟢 `F-01`, 🟡 `G-01`, 🟡 `G-02`, 🟡 `G-03` | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module) | Fan-out — 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `C-01` — 2 sequential stories; everything else hangs off this chain in parallel.

---

#### Recommended Story Graph — 1 Backend Engineer

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 1 backend engineer** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 |
|---|---|
| 1 | 🟢 `B-01` (1–2d) |
| 2 | 🟠 `E-01` (4–7d) 🔬 ⛔ |
| 3 | 🟡 `C-01` (2–4d) |
| 4 | 🟡 `D-01` (2–4d) |
| 5 | 🟡 `D-04` (2–4d) |
| 6 | 🟡 `G-01` (2–4d) |
| 7 | 🟡 `G-02` (2–4d) |
| 8 | 🟡 `G-03` (2–4d) |
| 9 | 🟢 `D-02` (1–2d) |
| 10 | 🟢 `D-03` (1–2d) |
| 11 | 🟢 `D-05` (1–2d) |
| 12 | 🟢 `F-01` (1–2d) |

**BE-1:** `B-01` → `E-01` → `C-01` → `D-01` → `D-04` → `G-01` → `G-02` → `G-03` → `D-02` → `D-03` → `D-05` → `F-01`

**Elapsed (nominal midpoints):** ~31 working days.

---

#### Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

##### 📖 Phase B — Core Reads (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PDTL-BE-B-01`<br>`getProductDetailsById(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Fetch product-detail (construction) sets by id.<br>**Today —** token for ids → GET construction/v1?ids={csv} → camelCase<br>**Done when:**<br>• returns list for ids; empty → [] |

> **`PDTL-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `productDetails.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.


##### 🔍 Phase C — Search & Listing (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PDTL-BE-C-01`<br>`getProductDetailsElastic(resourceId)` | 🟡 Medium `M` | Query<br>Calls: `search` | B-01 | **Intent —** Search a product's product-detail sets via elastic.<br>**Today —** (search) search.getProductDetailsElastic → paged. - EXT: search<br>**Done when:**<br>• `parentId:` elastic query built<br>• paged shape returned |


##### ✏️ Phase D — Mutations (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `PDTL-BE-D-01`<br>`createProductDetailsSet` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create a product-detail set.<br>**Today —** token for literal capability → POST construction/v1 (snake_case). If response has validationErrors or message → throw<br>**Done when:**<br>• creates set<br>• validation error → exception (not a partial object) |
| 🔶 `PDTL-BE-D-02`<br>`updateProductDetailAccess` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Change who can access a product-detail set.<br>**Today —** map managePermissionsRequest[].resourceId → token → PUT construction/v1/manage-permissions (primeKey=humanId)<br>**Done when:**<br>• updates partner access for each resource |
| 🔶 `PDTL-BE-D-03`<br>`productDetailLockUnlock` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Lock or unlock a product-detail set.<br>**Today —** token for [constructionSetId] → PUT construction/v1/{id}/{lock\\|unlock}<br>**Done when:**<br>• `isLock=true`→lock path, false→unlock path |
| 🔶 `PDTL-BE-D-04`<br>`cloneFilesForProductDetails` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B-01 | **Intent —** Copy attachment files for product details.<br>**Today —** token → Promise.all(attachmentIds.map((id,i) => (attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id))), stamp parentResource=id, flatten. No…<br>**Done when:**<br>• clones each id with its paired cloneReference<br>• `parentResource` stamped |
| 🔶 `PDTL-BE-D-05`<br>`updateProductDetailComponentStatus` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Update component status on product-detail sets.<br>**Today —** PUT construction/v1/component_status_update; wraps result as {content}. No JWT — confirm backend-enforced<br>**Done when:**<br>• updates statuses; result wrapped as `{content}`<br>• no-token behaviour documented |


##### ⚙️ Phase E — Complex Operations (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `PDTL-BE-E-01`<br>`updateProductDetailsSet` (multi-step write)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `attachment`, `workspaceV2` | SPIKE-01, B-01 | **Intent —** Edit a product-detail set — a multi-step write (workspace + body) with no rollback today.<br>**Today —** if workspaceContext.{add,remove}Workspaces non-empty → workspaceAssociationHelper(PRODUCT_DETAIL, id, add, remove) (throws on error); 2) null workspaceContext; 3) if…<br>**Done when:**<br>• all 4 steps in order<br>• partial-failure strategy implemented<br>• workspace assoc throws propagate | ☐ full path<br>☐ workspace-only<br>☐ attachment-archive<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


##### 🔗 Phase F — Federation & Stitching (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PDTL-BE-F-01`<br>`Product.productDetails` (internal, same subgraph) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Expose a product's product-details on the Product type (same subgraph).<br>**Today —** Product exposes productDetails resolved from the co-located ProductDetails service<br>**Done when:**<br>• `Product.productDetails` resolves in-process; no gateway hop |


##### 🧪 Phase G — Field Resolvers & Tests (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PDTL-BE-G-01`<br>`access` + `currentUserPermissions` + `participantDetails` | 🟡 Medium `M` | Field Resolver<br>Calls: `userGroup` | B-01 | **Intent —** Resolve access / permission / participant fields.<br>**Today —** access → accessControl.getPermissions([humanId\\|\\|id])[0]; currentUserPermissions → getUserAccessUnencoded(humanId\\|\\|id)[0]; participantDetails → getUserGroup(humanId)<br>**Done when:**<br>• each field resolves; null-safe on empty |
| 🔸 `PDTL-BE-G-02`<br>`product` + `createdBy` + `updatedBy` + `businessPartners` + `workspaces` | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `workspaceV2`, `vmm` | B-01 | **Intent —** Resolve the product, people, partner and workspace fields.<br>**Today —** product (internal, only if parentId starts 'PID'), createdBy/updatedBy (user-profile), businessPartners (vmm loadBpsWithType), workspaces (workspaceV2 by ids)<br>**Done when:**<br>• each resolves; `product` null when `parentId` not `PID*`<br>• null id → null user |
| 🔸 `PDTL-BE-G-03`<br>`attachment` + item `attachment`/`constructionSetAttachments` + category `subCategories` | 🟡 Medium `M` | Field Resolver<br>Calls: `search` | B-01 | **Intent —** Resolve attachment and category fields on product details.<br>**Today —** ProductDetails.attachment → (search) searchAttachments([humanId\\|\\|id]), find - relatedResources.length<=2; ProductDetailsItem.attachment →…<br>**Done when:**<br>• each field resolves to the right source<br>• `attachment` length-≤2 filter preserved |



---

## Frontend

### Federated GraphQL Breakdown — Product Details · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 3 |
| **Impact** | 🔴 0 High · 🟡 2 Medium · 🟢 1 Low |
| **Estimated effort** | 8–12 days (single-engineer) |
| **Phase-1 surface** | 7 operation-to-root-field rows · 2 client files · 4 components |
| **Generated** | 2026-07-19 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

#### What Are We Changing?

- Point the **Product Details** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

#### Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `PDTL-FE-001` | Migrate product-details reads | Query migration | 🟢 Low | 2–3 days | `PDTL-BE-B-01`, `PDTL-BE-G-01`, `PDTL-BE-G-02`, `PDTL-BE-G-03` | `getProductDetailsById`, `getProductDetailComponentStatus` |
| `PDTL-FE-002` | Migrate product-details simple mutations | Mutation migration | 🟡 Medium | 3–4 days | `PDTL-BE-D-01`, `PDTL-BE-D-03`, `PDTL-BE-D-04`, `PDTL-BE-D-05` | `createProductDetailsSet`, `productDetailLockUnlock`, `cloneFilesForProductDetails`, `updateProductDetailComponentStatus` |
| `PDTL-FE-003` | Migrate `updateProductDetailsSet` saga handling | Mutation migration (complex) | 🟡 Medium | 3–5 days | `PDTL-BE-E-01` | `updateProductDetailsSet` |

---

#### Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 3 | 🟡 `PDTL-FE-002` | `PDTL-FE-002` → `PDTL-BE-D-01`, `PDTL-BE-D-03`, `PDTL-BE-D-04`, `PDTL-BE-D-05` | Writes — needs backend phase D mutations |
| 4 | 🟢 `PDTL-FE-001`, 🟡 `PDTL-FE-003` | `PDTL-FE-001` → `PDTL-BE-B-01`, `PDTL-BE-G-01`, `PDTL-BE-G-02`, `PDTL-BE-G-03`<br>`PDTL-FE-003` → `PDTL-BE-E-01` | Complex writes / sagas — needs backend phase E + ADR ratification |

**Cutover flow:** `PDTL-FE-002` → `PDTL-FE-001` → `PDTL-FE-003`.

---

#### Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 3 | 🟡 `PDTL-FE-002` (3–4d) | Writes — needs backend phase D mutations |
| 4 | 🟡 `PDTL-FE-003` (3–5d)<br>🟢 `PDTL-FE-001` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |

**Elapsed (nominal midpoints):** ~10 FE build days — calendar time is set by the backend gates, not FE capacity.

---

#### References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-productDetails.md — the combined Backend + Frontend breakdown this section lives in.

