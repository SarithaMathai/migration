# Federated GraphQL Breakdown — Product Details

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **M** |
| **Total Stories** | 13 |
| **Complexity** | 🔴 0 Very High · 🟠 1 High · 🟡 7 Medium · 🟢 5 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-15 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

We are moving the **ProductDetails** domain — the product's "construction" sets (build/assembly detail rows,
their attachments, and per-partner access) — off the `spark-internal-graphql` gateway into the
**`plm-product`** DGS. It is **mid-sized and mid-low risk**: 2 queries, 6 mutations, 12 field resolvers on a
129-line resolver, with **no polymorphism**. (In the backend this domain is called *construction* —
`construction/v1`; the GraphQL names stay `productDetails`.)

The one genuinely harder piece is **`updateProductDetailsSet`**, a multi-step write — workspace
associations, then bulk-archive removed attachments, then the body — with no rollback today.

**ACL note:** the current code obtains per-resource capability tokens via ACL; Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs ([`complexStories/*/02-adr-noacl-*.md`](https://github.com/XXX/blob/main/output/complexStories/*/02-adr-noacl-*.md)) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

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

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `PDTL-BE-E-01` — `updateProductDetailsSet` (multi-step write) | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

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


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~6–11 sprints | sequential |
| 2 engineers | ~4–6 sprints | reads + mutations parallel after B-01 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | D-01–D-05 | simple mutations |
| 3 | E-01 + F-01 | multi-step write + Product field |
| 4 | G-01–G-03 | field resolvers |
| 5 | G-04 | tests & parity |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PDTL-BE-B-01`<br>`getProductDetailsById(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Fetch product-detail (construction) sets by id.<br>**Today —** token for ids → GET construction/v1?ids={csv} → camelCase<br>**Done when:**<br>• returns list for ids; empty → [] |

> **`PDTL-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `productDetails.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql.


### 🔍 Phase C — Search & Listing (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PDTL-BE-C-01`<br>`getProductDetailsElastic(resourceId)` | 🟡 Medium `M` | Query<br>Calls: `search` | B-01 | **Intent —** Search a product's product-detail sets via elastic.<br>**Today —** (search) search.getProductDetailsElastic → paged. - EXT: search<br>**Done when:**<br>• `parentId:` elastic query built<br>• paged shape returned |


### ✏️ Phase D — Mutations (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `PDTL-BE-D-01`<br>`createProductDetailsSet` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create a product-detail set.<br>**Today —** token for literal capability → POST construction/v1 (snake_case). If response has validationErrors or message → throw<br>**Done when:**<br>• creates set<br>• validation error → exception (not a partial object) |
| 🔶 `PDTL-BE-D-02`<br>`updateProductDetailAccess` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Change who can access a product-detail set.<br>**Today —** map managePermissionsRequest[].resourceId → token → PUT construction/v1/manage-permissions (primeKey=humanId)<br>**Done when:**<br>• updates partner access for each resource |
| 🔶 `PDTL-BE-D-03`<br>`productDetailLockUnlock` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Lock or unlock a product-detail set.<br>**Today —** token for [constructionSetId] → PUT construction/v1/{id}/{lock\\|unlock}<br>**Done when:**<br>• `isLock=true`→lock path, false→unlock path |
| 🔶 `PDTL-BE-D-04`<br>`cloneFilesForProductDetails` | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | B-01 | **Intent —** Copy attachment files for product details.<br>**Today —** token → Promise.all(attachmentIds.map((id,i) => (attachment) cloneAttachmentV3({cloneReferences:[cloneReference[i]]}, id))), stamp parentResource=id, flatten. No…<br>**Done when:**<br>• clones each id with its paired cloneReference<br>• `parentResource` stamped |
| 🔶 `PDTL-BE-D-05`<br>`updateProductDetailComponentStatus` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Update component status on product-detail sets.<br>**Today —** PUT construction/v1/component_status_update; wraps result as {content}. No JWT — confirm backend-enforced<br>**Done when:**<br>• updates statuses; result wrapped as `{content}`<br>• no-token behaviour documented |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `PDTL-BE-E-01`<br>`updateProductDetailsSet` (multi-step write)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `attachment`, `workspaceV2` | SPIKE-01, B-01 | **Intent —** Edit a product-detail set — a multi-step write (workspace + body) with no rollback today.<br>**Today —** if workspaceContext.{add,remove}Workspaces non-empty → workspaceAssociationHelper(PRODUCT_DETAIL, id, add, remove) (throws on error); 2) null workspaceContext; 3) if…<br>**Done when:**<br>• all 4 steps in order<br>• partial-failure strategy implemented<br>• workspace assoc throws propagate | ☐ full path<br>☐ workspace-only<br>☐ attachment-archive<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PDTL-BE-F-01`<br>`Product.productDetails` (internal, same subgraph) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Expose a product's product-details on the Product type (same subgraph).<br>**Today —** Product exposes productDetails resolved from the co-located ProductDetails service<br>**Done when:**<br>• `Product.productDetails` resolves in-process; no gateway hop |


### 🧪 Phase G — Field Resolvers & Tests (4 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PDTL-BE-G-01`<br>`access` + `currentUserPermissions` + `participantDetails` | 🟡 Medium `M` | Field Resolver<br>Calls: `userGroup` | B-01 | **Intent —** Resolve access / permission / participant fields.<br>**Today —** access → accessControl.getPermissions([humanId\\|\\|id])[0]; currentUserPermissions → getUserAccessUnencoded(humanId\\|\\|id)[0]; participantDetails → getUserGroup(humanId)<br>**Done when:**<br>• each field resolves; null-safe on empty |
| 🔸 `PDTL-BE-G-02`<br>`product` + `createdBy` + `updatedBy` + `businessPartners` + `workspaces` | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `workspaceV2`, `vmm` | B-01 | **Intent —** Resolve the product, people, partner and workspace fields.<br>**Today —** product (internal, only if parentId starts 'PID'), createdBy/updatedBy (user-profile), businessPartners (vmm loadBpsWithType), workspaces (workspaceV2 by ids)<br>**Done when:**<br>• each resolves; `product` null when `parentId` not `PID*`<br>• null id → null user |
| 🔸 `PDTL-BE-G-03`<br>`attachment` + item `attachment`/`constructionSetAttachments` + category `subCategories` | 🟡 Medium `M` | Field Resolver<br>Calls: `search` | B-01 | **Intent —** Resolve attachment and category fields on product details.<br>**Today —** ProductDetails.attachment → (search) searchAttachments([humanId\\|\\|id]), find - relatedResources.length<=2; ProductDetailsItem.attachment →…<br>**Done when:**<br>• each field resolves to the right source<br>• `attachment` length-≤2 filter preserved |
| 📄 `PDTL-BE-G-04`<br>Tests, parity harness | 🟡 Medium `M` | Tests | B-01, E-01, G-01 | **Intent —** Prove the product-details subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity fixtures (incl<br>**Done when:**<br>• unit ≥80%<br>• parity fixtures green<br>• schema-diff intentional-only |

