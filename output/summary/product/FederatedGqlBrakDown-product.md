# Federated GraphQL Breakdown — Product

| | |
|---|---|
| **Target DGS** | `plm-product (host)` |
| **T-Shirt Size** | **XXL** |
| **Total Stories** | 67 |
| **Complexity** | 🔴 5 Very High · 🟠 4 High · 🟡 25 Medium · 🟢 33 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving **Product** — the central entity of the PLM system — off the `spark-internal-graphql` gateway into the **`plm-product`** Netflix DGS.
- Product is the **largest and highest-risk** domain (18 queries, 20 mutations, ~50 field resolvers on a 2,629-line resolver) and the **host service** for the whole product family: BOM, Measurement, Impression, Packaging and others live in the same DGS, so their links from Product resolve **internally** rather than across the federation gateway.

- Most of the work is mechanical (the long tail of CRUD and simple field resolvers), but a handful of items carry real risk: the **TechPack count** query (a 17-step aggregation across 9+ services that becomes a federated composite-key entity), the **partner drop/undrop** orchestration, the cross-domain **components** and **attachmentsWithMetaData** field resolvers, and a **latent `division` bug**.
- We recommend the **Option D** approach for TechPack: ship a thin query over a temporary aggregation facade so it works on day 1, then federate each piece to its owning domain, then retire the facade.

**ACL note:** the source obtains per-resource capability tokens via ACL on nearly every call; **ACL is
ignored in the DGS implementation** (no ACL story) — noted for context only.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 18 | incl. TechPack (Very High) and two-stage `getProducts` |
| Mutations | 20 (+3 deferred) | incl. partner actions + component fan-out |
| Field-resolver stories | ~16 | incl. 2 X-Large (attachmentsWithMetaData, components) |
| External dependencies | 12 EXT + 6 platform | search/attachment/workspace 🔴 |
| Composite-key aggregate | 1 (TechPack `ResourcesCount`) | 8 sibling subgraphs extend it |
| Federation contributions received | 8 | from sibling domains (Phase F placeholders) |
| **Total stories** | **67** | green-field build stories (3 complex problems centralized as program spikes; `G11` split into `G11-1`/`G11-2` = +1) |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `SPARK-PROD-C01` — `getProducts(...)` two-stage hydration | `SPARK-SPIKE-06a` (via `SPARK-PROD-S02`) | Hydration |
| 🔴🔬 `SPARK-PROD-D01` — `addProduct` | `SPARK-SPIKE-06b` (via `SPARK-PROD-S01`) | Cross-Domain Association |
| 🔴🔬 `SPARK-PROD-D02` — `addProducts` (bulk) | `SPARK-SPIKE-06b` (via `SPARK-PROD-S01`) | Cross-Domain Association |
| `SPARK-PROD-D03` — `bulkUpdateProducts` | ~~`SPARK-SPIKE-06b`~~ — **not blocked** (pure passthrough; no cross-domain call) | — |
| 🔴🔬 `SPARK-PROD-D04` — `updateProduct` | `SPARK-SPIKE-06b` (via `SPARK-PROD-S01`) | Cross-Domain Association |
| `SPARK-PROD-D06` — `addTeamsToProduct` 🔀 Collab Canvas | ~~`SPARK-SPIKE-06b`~~ — **not blocked** (single-backend write; product backend owns all endpoints) | — |
| `SPARK-PROD-D07` — `addBusinessPartnersToProductWithType` 🔀 Collab Canvas | ~~`SPARK-SPIKE-06b`~~ — **not blocked** (single-backend write) | — |
| `SPARK-PROD-D11` — `updateWorkspaceAttributes` 🔀 Collab Canvas | ~~`SPARK-SPIKE-06b`~~ — **not blocked** (single-backend write) | — |
| 🔴🔬 `SPARK-PROD-E01` — `productBusinessPartnerActions` (REMOVE/DROP/UNDROP) | `SPARK-SPIKE-03` | Partner Drop/Undrop + Ownership |
| 🔴🔬 `SPARK-PROD-E02` — `updateComponentStatuses` (5-loader fan-out) | `SPARK-SPIKE-01` | Non-Atomic Write Saga |
| 🔴🔬 `SPARK-PROD-E03` — `getProductTechPackCountV1` stub + aggregation facade (Option D Phase 1) | `SPARK-SPIKE-02` | TechPack Aggregate |
| 🔴🔬 `SPARK-PROD-E04` — `getProductTechPackBulkCountV1` (bulk wrapper, ordering fix) | `SPARK-SPIKE-02` | TechPack Aggregate |
| 🔴🔬 `SPARK-PROD-G07` — `Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status` | `SPARK-SPIKE-04` | Not-Removable / Undroppable Partners |

> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Deployment Model — Ship on Green, Per Story

- Every story is **end-to-end in one PR** and **independently deployable to production once its own tests and parity pass** — no waiting for the rest of the phase.
- The **one exception** is a story whose field is produced by **composing another subgraph's data** (a cross-subgraph **entity extension**, `extend type … @key` resolved by a different DGS): those go live only once the **owning subgraph is deployed**, and are marked
**BLOCKED-BY `<domain>`**.

- ✅ **Ships on green** — all B/C/D/E/G stories, the internal Phase-F contributions (`F04`, `F06`, `F08`), the
  gateway/platform stories (`F10`, `F11`), and the **TechPack facade** (`E03`/`E04`), which is *designed* to
  work day 1 before any sibling federates.
- ⛔ **Waits for an owning subgraph (the exception)** — the true cross-subgraph federation stories
  **`F01` (attachment), `F02` (discussion), `F03` (sample), `F05` (claim), `F07` (construction)**, plus
  **`F09`** (facade retirement, which needs all 8 contributions live). These are the only stories held back
  from per-story prod release.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) | Ready when |
|---|---|---|---|---|
| B | Core Reads | 11 | 11–18d | after B01 |
| C | Search & Listing | 5 | 17–29d | after B01; C01 gated on `SPARK-SPIKE-06a` (Hydration) |
| D | Mutations (simple) | 18 | 25–40d | after B01; D01/D02/D04 gated on `SPARK-SPIKE-06b` (Association); D03/D06/D07/D11 unblocked (single-backend) |
| E | Complex (partner/components/TechPack) | 4 | 33–56d | E01 gated on `SPARK-SPIKE-03` |
| F | Federation & Stitching | 12 | 22–40d (most BLOCKED-BY siblings) | after E03 / siblings |
| G | Field Resolvers, Bug-fixes, Utils, Tests | 17 | 86–143d | after B01. `G11` split into `G11-1`/`G11-2` (16 → 17) |
| **Total** | | **67** | **203–348d** (buffered) | |

> One engineer ≈ **40–66 sprints**. Heavily parallelizable after B01; 2–3 engineers strongly recommended.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories; the `Categories` union `@DgsTypeResolver` remains a dedicated story.

> **Thin DGS wrappers — parallel after B01.** The model, REST controller (GET/POST/PUT) and service already exist; each story only adds the Netflix-DGS layer so the federated graph can stitch this subgraph. The **one-time DGS module scaffold** B01 lands (schema file + scalar registration + service/Feign wiring) is a prerequisite for every operation story, so it is **assumed — not repeated in each story's `Depends On`** (rows list only genuine story-to-story dependencies). E.g. `D08 removeProductResources` is a one-line wrapper over the existing REST `DELETE`/`PUT`, so its `Depends On` is **—**. After B01, phases B/C/D/G run fully in parallel.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~42–71 sprints | sequential — not recommended for this domain |
| 2 engineers | ~25–42 sprints | B/C/D parallel after B01 |
| 3–4 engineers | ~18–28 sprints | A done → B + C + D + most of G in parallel; E and the two X-Large fields on dedicated owners |

> Phase G dominates the calendar; the two X-Large field resolvers (`attachmentsWithMetaData`, `components`)
> and TechPack (E03/E04) are the cost-and-risk centre of the whole program.

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 0 | Program spikes | run in Sprint 0 (see global Phase 0 — Program Spikes) so D/C/E work isn't waiting |
| 1–2 | B01 (DGS module init + service wiring + first resolver) | schema, types, stubs, Categories resolver, ResourcesCount, service port |
| 3 | B01–B11 | all core reads (incl. rules reads) |
| 4 | C01–C05 | search/listing + rating + rules search (C01 needs `SPARK-SPIKE-06a` concluded) |
| 5–6 | D01–D18 | all simple mutations, parallelizable (D01/D02/D04 need `SPARK-SPIKE-06b` concluded; D03/D06/D07/D11 unblocked) |
| 7–8 | E03/E04 | TechPack facade + bulk (focused; facade-vs-federate spike already resolved) |
| 9 | E01/E02 | partner actions (needs `SPARK-SPIKE-03` concluded) + component fan-out |
| 10–12 | G01–G10, G11-1, G11-2, G12–G14 | field resolvers (G01/G02 X-Large get their own sprint) |
| 13 | G15 + G16 | utils port + tests/parity/load/cut-over |
| post-launch | F01–F09 | TechPack federation (unblocked as siblings migrate) + facade retirement |
| any | F10–F12 | gateway composition + platform verify + drift decision |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (11 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-PROD-B01`<br>`getProduct(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up a single product by id (the core product read everything else builds on).<br>**Today —** getByID GET ${v1}?productId={id} → camelCase or null; DataLoader-batched<br>**Done when:**<br>• returns product; 404→null<br>• batches N ids in 1 call |
| 🔷 `SPARK-PROD-B02`<br>`getProductsByIds(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up several products at once by their ids.<br>**Today —** getByIdList GET ${v1}?productId={csv}&page=0&size=10000&sort=createdDate,desc; primes getByID<br>**Done when:**<br>• returns paged products for ids<br>• primes single-id loader |
| 🔷 `SPARK-PROD-B03`<br>`getProductStatus` (cacheable) | 🟢 Low `XS` | Query | — | **Intent —** Returns the list of possible product statuses (dropdown options).<br>**Today —** getStatus master status list<br>**Done when:**<br>• returns statuses<br>• cached |
| 🔷 `SPARK-PROD-B04`<br>`getProductVersions(id)` | 🟢 Low `XS` | Query | — | **Intent —** Lists the saved versions of a product.<br>**Today —** getVersions GET ${v1}/{id}/versions?page=0&size=10000<br>**Done when:**<br>• returns versions |
| 🔷 `SPARK-PROD-B05`<br>`getCopyStatus(id)` | 🟢 Low `XS` | Query | — | **Intent —** Tells you whether a product copy is still in progress or done.<br>**Today —** getCopyStatus GET ${v2}/count/resource-type?copyId={id}<br>**Done when:**<br>• returns copy status |
| 🔷 `SPARK-PROD-B06`<br>`getProductTemplateById(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up a product template by id.<br>**Today —** getByID → response \\|\\| {} (empty object on miss — preserve)<br>**Done when:**<br>• returns product or empty object (not null) |
| 🔷 `SPARK-PROD-B07`<br>`getProductRules` | 🟢 Low `XS` | Query | — | **Intent —** Returns the product business rules.<br>**Today —** getAllRules GET $… → content<br>**Done when:**<br>• returns rules content |
| 🔷 `SPARK-PROD-B08`<br>`getProductRulesById(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up one business rule by id.<br>**Today —** getRuleById GET $…<br>**Done when:**<br>• returns rule |
| 🔷 `SPARK-PROD-B09`<br>`getAllAvailableRules` | 🟢 Low `XS` | Query | — | **Intent —** Lists all the rules that are available to apply.<br>**Today —** getAvailableRules GET …/spark_rules/v1/rules<br>**Done when:**<br>• returns available rules |
| 🔷 `SPARK-PROD-B10`<br>`getProductDeptRules(productIds, departmentIds, activeOnly)` | 🟢 Low `XS` | Query<br>Calls: `ruleLibrary` | — | **Intent —** Returns the department-level rules for given products.<br>**Today —** flag fork USE_NEW_RULES_API ? ruleLibrary.searchRuleLibrary : product.searchProductDeptRules GET …/spark_rules/v1/search?productIds=&departmentIds=&activeOnly=. PO…<br>**Done when:**<br>• default `activeOnly=true`<br>• flag selects the correct backend |
| 🔷 `SPARK-PROD-B11`<br>`getProductBPRules(productIds, businessPartnerIds, activeOnly)` | 🟢 Low `XS` | Query<br>Calls: `ruleLibrary` | — | **Intent —** Returns the business-partner-level rules for given products.<br>**Today —** same as B10 with businessPartnerIds<br>**Done when:**<br>• flag fork honored; BP filter applied |

> **`SPARK-PROD-B01`** — **Note — DGS Module Init (this PR only):** Creates `product.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql. **This scaffold is a prerequisite for every B/C/D/G story** — they need the module + schema file to compile their DGS wrapper — so it is assumed globally (shown once in the dependency graph) and **not repeated** in each story's `Depends On`. After it lands, the wrappers parallelize.


### 🔍 Phase C — Search & Listing (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔷 `SPARK-PROD-C01`<br>`getProducts(...)` two-stage hydration<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-06a` (Hydration) — see global Spike Detail_ | 🟠 High `L` | Query<br>Calls: `search` | SPARK-SPIKE-06a | **Intent —** List products by combining the search index with the canonical record (two-stage hydration).<br>**Today —** listing products needs data from two places — the search index (which - knows flags like "has boms", "has claims", workspace membership) and the canonical product…<br>**Done when:**<br>• parity for 4 arg combos (no flags / all flags / resourceType=workspaces / filter array)<br>• truthy defaults preserved<br>• elastic flags merged onto canonical<br>• Workspace-filter placement and elastic/canonical staleness handling match `SPARK-SPIKE-06a`'s decision | ☐ 4 combos<br>☐ default truthiness<br>☐ merge<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔷 `SPARK-PROD-C02`<br>`getProductTemplates(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | — | **Intent —** Lists product templates, with optional filters on what to include.<br>**Today —** (search) getFilteredProductsListing({resourceType:'product', includeBoms:false, ...7 includeXxxTemplates flags, types}) → return elastic response (no 2nd hydration)<br>**Done when:**<br>• all 7 template-include flags forwarded<br>• `types:[Int]` filter applied | — |
| 🔷 `SPARK-PROD-C03`<br>`getCategories(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | — | **Intent —** Returns the category tree for products.<br>**Today —** default productType ?? 100; (search) getProductCategories GET ${elastic}/search/${snake_case(type)}?resourceType=&resourceId=&productType= → ProductsCategories…<br>**Done when:**<br>• `snake_case(type)` path exact<br>• wires to `Categories` union | — |
| 🔷 `SPARK-PROD-C04`<br>`getRatingByTcin(tcin)` (external rating) | 🟡 Medium `M` | Query<br>Calls: `rating` | — | **Intent —** Gets the customer rating for a product (from an external ratings service).<br>**Today —** (external) GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={API_KEY} (skipJsonParse) → JSON.parse → {averageRating, reviewCount}…<br>**Done when:**<br>• parses statistics to `Rating`<br>• any error → null<br>• API key from config/Vault, not source | — |
| 🔷 `SPARK-PROD-C05`<br>`searchProductRules(...)` | 🟡 Medium `M` | Query<br>Calls: `ruleLibrary` | — | **Intent —** Searches product rules.<br>**Today —** flag fork; legacy GET …/spark_rules/v1/search_mapped?... → productRuleResponseTransformer → camelCase<br>**Done when:**<br>• flag fork honored<br>• legacy response transformed correctly | — |


### ✏️ Phase D — Mutations (18 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔴🔬 🔶 `SPARK-PROD-D01`<br>`addProduct`<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `workspaceV2`, `attachment` | SPARK-SPIKE-06b | **Intent —** Create a product (optionally copy from another + associate a workspace).<br>**Today —** POST ${v1} + optional copyProductToProduct(copyProduct) + workspace association<br>**Done when:**<br>• creates product<br>• optional copy runs when `copyProduct` present<br>• workspace assoc applied |
| 🔴🔬 🔶 `SPARK-PROD-D02`<br>`addProducts` (bulk)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | SPARK-SPIKE-06b | **Intent —** Create many products at once (plus attachment links).<br>**Today —** bulk POST ${v1}/bulk + attachment-link side-effects (no rollback — preserve, flag)<br>**Done when:**<br>• bulk creates<br>• attachment links applied; no-rollback behaviour documented |
| 🔴🔬 🔶 `SPARK-PROD-D03`<br>`bulkUpdateProducts`<br>_No spike dependency — pure passthrough_ | 🟡 Medium `M` | Mutation | — | **Intent —** Update many products in one call.<br>**Today —** PUT ${v1}/mass_update<br>**Note —** Pure passthrough; no cross-domain call; not blocked by SPARK-SPIKE-06b.<br>**Done when:**<br>• mass-updates products |
| 🔴🔬 🔶 `SPARK-PROD-D04`<br>`updateProduct`<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | SPARK-SPIKE-06b | **Intent —** Edit a product (optional copy + template-attachment cleanup).<br>**Today —** PUT ${v1}/{id} + optional copy + archive removed-template attachments (template branch)<br>**Done when:**<br>• updates product<br>• optional copy<br>• removed-template attachments archived (template branch) |
| 🔶 `SPARK-PROD-D05`<br>`carryForwardProduct` | 🟡 Medium `M` | Mutation | — | **Intent —** Carries a product forward (creates the next season/version from it).<br>**Today —** PUT ${v1}/{productId}/carry_forward/{workspaceId} — uses every field on CarryForwardProductInput<br>**Done when:**<br>• all input fields mapped to the request |
| � `SPARK-PROD-D06`<br>`addTeamsToProduct` 🔀 Collab Canvas<br>_No spike dependency — single-backend write_ | 🟢 Low `XS` | Mutation | — | **Intent —** Adds teams (and their partners) to a product.<br>**Today —** POST ${v1}/{productId}/resources/bulk + manage_workspace_teams<br>**Note —** All 3 endpoints on product backend; no external service called. Not blocked by SPARK-SPIKE-06b.<br>**Done when:**<br>• adds teams + new partners + workspace links |
| � `SPARK-PROD-D07`<br>`addBusinessPartnersToProductWithType` 🔀 Collab Canvas<br>_No spike dependency — single-backend write_ | 🟢 Low `XS` | Mutation | — | **Intent —** Adds business partners to a product with a given type.<br>**Today —** POST ${v1}/{productId}/partners-add/bulk<br>**Note —** Single-backend write; no external partner service called. Not blocked by SPARK-SPIKE-06b. Throw `DgsException` on failure (not `return new Error`).<br>**Done when:**<br>• adds partners with type |
| 🔶 `SPARK-PROD-D08`<br>`removeProductResources` | 🟢 Low `XS` | Mutation | — | **Intent —** Removes resources (links) from a product.<br>**Today —** DELETE ${v1}/{productId}/resources/bulk<br>**Done when:**<br>• removes resources |
| 🔶 `SPARK-PROD-D09`<br>`updateBusinessPartnerStatuses` | 🟢 Low `XS` | Mutation | — | **Intent —** Updates the status of business partners on a product.<br>**Today —** PUT ${v1}/{productId}/status_update/bulk<br>**Done when:**<br>• updates partner statuses |
| 🔶 `SPARK-PROD-D10`<br>`updateViewToggle` | 🟢 Low `XS` | Mutation | — | **Intent —** Toggles whether a product is hidden.<br>**Today —** PUT ${v1} view toggle<br>**Done when:**<br>• toggles hidden |
| � `SPARK-PROD-D11`<br>`updateWorkspaceAttributes` 🔀 Collab Canvas<br>_No spike dependency — single-backend write_ | 🟢 Low `XS` | Mutation | — | **Intent —** Updates a product's workspace attributes.<br>**Today —** PUT ${v1}/{productId}/workspaceAttributes/{humanId} workspace attrs<br>**Note —** Workspace attributes live on the product record; workspace service never called. Not blocked by SPARK-SPIKE-06b.<br>**Done when:**<br>• updates workspace attrs |
| 🔶 `SPARK-PROD-D12`<br>`updateProductTeamsWorkspaceContext` | 🟢 Low `XS` | Mutation | — | **Intent —** Adds or removes team↔workspace pairings on a product.<br>**Today —** PUT team-workspace add/remove<br>**Done when:**<br>• adds/removes team-workspace pairs |
| 🔶 `SPARK-PROD-D13`<br>`linkProduct` | 🟢 Low `XS` | Mutation | — | **Intent —** Links a parent and child product together.<br>**Today —** PUT link — throws on backend error (only mutation that does)<br>**Done when:**<br>• links parent/child<br>• backend error → exception (not null) |
| 🔶 `SPARK-PROD-D14`<br>`unlinkProduct` | 🟢 Low `XS` | Mutation | — | **Intent —** Unlinks a parent and child product.<br>**Today —** PUT unlink<br>**Done when:**<br>• unlinks parent/child |
| 🔶 `SPARK-PROD-D15`<br>`addProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Creates a product rule.<br>**Today —** POST …/spark_rules/v1<br>**Done when:**<br>• creates rule |
| 🔶 `SPARK-PROD-D16`<br>`updateProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Updates a product rule.<br>**Today —** PUT …/spark_rules/v1/{id}<br>**Done when:**<br>• updates rule |
| 🔶 `SPARK-PROD-D17`<br>`deleteProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Deletes a product rule.<br>**Today —** DELETE …/spark_rules/v1/{id} → Boolean<br>**Done when:**<br>• deletes; returns Boolean |
| 🔶 `SPARK-PROD-D18`<br>`updateComponentStatus` (bulk) | 🟢 Low `XS` | Mutation | — | **Intent —** Bulk-updates the status of many components at once.<br>**Today —** bulk PUT ${v1}/component_status_update/bulk<br>**Done when:**<br>• bulk-updates component statuses |


### ⚙️ Phase E — Complex Operations (4 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `SPARK-PROD-E01`<br>`productBusinessPartnerActions` (REMOVE/DROP/UNDROP)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-03` (Partner Drop/Undrop + Ownership) — see global Spike Detail_ | 🔴 Very High `XL` | Mutation<br>Calls: `sampleV2`, `recentlyViewed`, `todo`, `favorite` | SPARK-SPIKE-03 | **Intent —** Remove / drop / undrop a business partner across a product — a ~220-line orchestrated write.<br>**Today —** removing, dropping, or un-dropping a business partner from a product - isn't one write — it's a ~220-line dispatcher that updates the partner's status and then fans…<br>**Done when:**<br>• all 3 paths reach REST parity (recorded fixtures)<br>• partial-failure compensation log/strategy implemented per `SPARK-SPIKE-03`'s decision<br>• cleanup fan-out runs per case, with per-target failure isolation (one cleanup failing is visible and doesn't silently swallow the others) | ☐ REMOVE<br>☐ DROP<br>☐ UNDROP<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔴🔬 🔶 `SPARK-PROD-E02`<br>`updateComponentStatuses` (5-loader fan-out)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `claim` | SPARK-SPIKE-01 | **Intent —** Update a product's component statuses, fanning out to 5 sibling loaders.<br>**Today —** updating component statuses fans out to 5 places in parallel (bom, - measurement, productDetail, packaging — all internal — plus claim, external). - The bug: a loop…<br>**Done when:**<br>• per-loader failures don't fail siblings<br>• shadow var fixed<br>• parity | ☐ 5-way fan-out<br>☐ partial failure isolation<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔴🔬 🔷 `SPARK-PROD-E03`<br>`getProductTechPackCountV1` stub + aggregation facade (Option D Phase 1)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-02` (TechPack Aggregate) — see global Spike Detail_ | 🔴 Very High `XL` | Query<br>Calls: `attachment`, `search` | SPARK-SPIKE-02 | **Intent —** Build the TechPack panel's badge counts by aggregating across ~8 domains.<br>**Today —** the TechPack panel shows badge counts (attachments, discussions, - samples, boms, claims, etc.) for a product. - Getting those counts today means walking the entire…<br>**Done when:**<br>• returns populated `ResourcesCount` from the facade<br>• entity fetcher reconstructs from key+context<br>• parity vs source for 5 inputs<br>• facade observable | ☐ facade call<br>☐ entity fetcher<br>☐ parity 5 inputs<br>☐ Integration: full query via DGS test client returns expected shape |
| 🔴🔬 🔷 `SPARK-PROD-E04`<br>`getProductTechPackBulkCountV1` (bulk wrapper, ordering fix)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-02` (TechPack Aggregate) — see global Spike Detail_ | 🔴 Very High `XL` | Query<br>Calls: `attachment`, `search` | SPARK-SPIKE-02, E03 | **Intent —** Return TechPack counts for many products at once, in the caller's order.<br>**Today —** the bulk version runs all N single-product lookups concurrently and - returns them in whatever order they happen to finish — not the order the caller asked for. - If a…<br>**Done when:**<br>• `bulk(P1..Pn) == [single(P1)..single(Pn)]` in input order<br>• empty list → [] | ☐ order preserved<br>☐ empty<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (12 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-PROD-F01`<br>`ResourcesCount.productAttachments` + `discussionAttachments` (federated, from Attachment) | 🟡 Medium `M` | Field Resolver | E03 | **Intent —** Contribute attachment counts to the product's TechPack rollup (from Attachment).<br>**Done when:**<br>• `productAttachments`/`discussionAttachments` resolve on the federated `ResourcesCount`; the `E03` facade stops populating them<br>• Parity vs the facade for the same inputs<br>• Field is live in prod only after `plm-attachment` is deployed (ship gate honored) |
| 🔸 `SPARK-PROD-F02`<br>`ResourcesCount.discussions` (federated, from Discussion) | 🟡 Medium `M` | Field Resolver | E03 | **Intent —** Fills in the product's discussion count — answered by the Discussion service once it's live.<br>**Done when:**<br>• `discussions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `plm-discussion` is deployed |
| 🔸 `SPARK-PROD-F03`<br>`ResourcesCount.sample` (federated, from Sample) | 🟡 Medium `M` | Field Resolver | E03 | **Intent —** Fills in the product's sample count — answered by the Sample service once it's live.<br>**Done when:**<br>• `sample` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `plm-sample` is deployed |
| 🔸 `SPARK-PROD-F04`<br>`ResourcesCount.measurementSets` (internal, from Measurement) | 🟢 Low `XS` | Field Resolver | E03 | **Intent —** Fills in the product's measurement-set count — answered in-process by the co-located Measurement code.<br>**Done when:**<br>• `measurementSets` resolves in-process; no gateway hop; parity vs facade |
| 🔸 `SPARK-PROD-F05`<br>`ResourcesCount.claims` (federated, from Claim) | 🟡 Medium `M` | Field Resolver | E03 | **Intent —** Fills in the product's claims count — answered by the Claims service once it's live.<br>**Done when:**<br>• `claims` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `spark-claims` is deployed |
| 🔸 `SPARK-PROD-F06`<br>`ResourcesCount.productBoms` + `packagingBoms` + `boms` (internal, from BOM) | 🟢 Low `XS` | Field Resolver | E03 | **Intent —** Fills in the product's BOM counts — answered in-process by the co-located BOM code.<br>**Done when:**<br>• `productBoms`/`packagingBoms`/`boms` resolve in-process; no gateway hop; parity vs facade |
| 🔸 `SPARK-PROD-F07`<br>`ResourcesCount.constructions` (federated, from Construction) | 🟡 Medium `M` | Field Resolver | E03 | **Intent —** Fills in the product's construction count — answered by the Construction service once it's live.<br>**Done when:**<br>• `constructions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after the construction subgraph is deployed |
| 🔸 `SPARK-PROD-F08`<br>`ResourcesCount.watchlists` (internal, from Watchlist) | 🟢 Low `XS` | Field Resolver | E03 | **Intent —** Fills in the product's watchlist count — answered in-process by the co-located Watchlist code.<br>**Done when:**<br>• `watchlists` resolves in-process; no gateway hop; parity vs facade |
| 🔸 `SPARK-PROD-F09`<br>Retire the TechPack aggregation facade | 🟢 Low `XS` | Field Resolver | F01, F02, F03, F04, F05, F06, F07, F08 | **Intent —** Removes the temporary TechPack 'facade' once every count is served by its real owner.<br>**Today —** remove TechPackAggregatorClient; TechPackDataFetcher returns key+context only; decommission the facade<br>**Done when:**<br>• all 11 `ResourcesCount` fields resolve via federation<br>• facade health-check endpoint returns 404 (decommissioned)<br>• no orphaned config (feature flags, Feign client beans, etc. referencing the retired facade) |
| 🔸 `SPARK-PROD-F10`<br>Hive Gateway supergraph composition | 🟢 Low `XS` | Field Resolver | — | **Intent —** Composes all the subgraphs into one federated graph at the gateway.<br>**Today —** add plm-product subgraph URL; verify composition with VMM/IG/CORONA/Doppler stubs; smoke-test cross-subgraph query<br>**Done when:**<br>• supergraph composes<br>• cross-subgraph smoke test passes |
| 🔸 `SPARK-PROD-F11`<br>Platform stub verification (VMM/IG/Doppler/CORONA/APEX) | 🟢 Low `XS` | Field Resolver | F10 | **Intent —** Verifies each external platform (VMM, IG, etc.) resolves through its stub.<br>**Today —** confirm the gateway resolves full platform types from product-emitted @key stubs<br>**Done when:**<br>• each platform type resolves via its stub key |
| 📄 `SPARK-PROD-F12`<br>Deferred partner-wrapper decision (drift mutations) | 🟢 Low `XS` | Schema | E01 | **Intent —** Decide the fate of three drift partner mutations that have no resolvers.<br>**Today —** three old mutation names (removeProductBusinessPartner, - dropProductBusinessPartner, unDropProductBusinessPartner) still exist in the schema, but nothing calls them…<br>**Done when:**<br>• traffic survey complete<br>• decision implemented |


### 🧪 Phase G — Field Resolvers & Tests (17 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `SPARK-PROD-G01`<br>`Product.attachmentsWithMetaData` | 🔴 Very High `XL` | Field Resolver<br>Calls: `attachment`, `relationship` | — | **Intent —** Resolve a product's mixed attachments-with-metadata feed (files + discussions + samples).<br>**Today —** the attachments panel on a product shows a mixed feed — actual file - attachments, plus discussions and samples that are also surfaced as if they were attachments…<br>**Done when:**<br>• parity for mixed attachment/discussion/thread/sample<br>• ordering rank preserved (product=0, discussion=1, sample=2; createdAt DESC tiebreak) | ☐ merge<br>☐ ordering<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `SPARK-PROD-G02`<br>`Product.components` | 🔴 Very High `XL` | Field Resolver<br>Calls: `search` | — | **Intent —** List everything attached to a product, tagged by type, with counts.<br>**Today —** the components tab lists everything attached to a product — measurements, - claims, boms, product-details, packaging — tagged by type, with counts (how many are…<br>**Done when:**<br>• parity for 50+ components<br>• `archivedCount`/`countByComponents` match source<br>• ACL batched (no N+1) | ☐ merge<br>☐ counts<br>☐ batched ACL<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `SPARK-PROD-G03`<br>`Product.attachments` + `attachmentsV3` + `attachmentSummary` + `ProductTemplate.attachmentsData` | 🟠 High `L` | Field Resolver<br>Calls: `attachment`, `search` | G01 | **Intent —** Resolve the product's attachment views (via a shared enrichment service).<br>**Today —** four related resolvers sharing AttachmentEnrichmentService (G01)<br>**Done when:**<br>• each field returns its shape<br>• shares G01 service | ☐ each field<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `SPARK-PROD-G04`<br>`ProductsCategories.categories` (12-case) + `DopplerDepartment` fields | 🟡 Medium `M` | Field Resolver<br>Calls: `doppler` | — | **Intent —** Resolve the polymorphic categories union (12 branches) and department fields.<br>**Today —** categories is a polymorphic union — depending on which category type - the caller asked for, a different one of 12 branches builds the response shape. - Two of those…<br>**Done when:**<br>• each category type built correctly<br>• Doppler fetched once | — |
| 🔸 `SPARK-PROD-G05`<br>`Product.samples` + `sampleIds` + `elasticSamplesList` | 🟡 Medium `M` | Field Resolver<br>Calls: `sampleV2`, `search` | — | **Intent —** Resolve a product's samples from local context (removing the fragile args hack).<br>**Today —** today these fields reach into GraphQL's internal info.variableValues to read arguments that were passed to a different, parent query — a fragile, implicit way to pass…<br>**Done when:**<br>• samples/sampleIds/elastic resolve<br>• no `info.variableValues` read | — |
| 🔸 `SPARK-PROD-G06`<br>`Product.teams` + `discussionsV2` + `discussionsCount` + `workspaces` | 🟡 Medium `M` | Field Resolver<br>Calls: `teamV2`, `discussion`, `search`, `workspaceV2` | — | **Intent —** Resolve a product's team / discussion / workspace fields.<br>**Today —** team/discussion/workspace elastic lookups<br>**Done when:**<br>• each field resolves | — |
| 🔴🔬 🔸 `SPARK-PROD-G07`<br>`Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status`<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-04` (Not-Removable / Undroppable Partners) — see global Spike Detail_ | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm` | SPARK-SPIKE-04 | **Intent —** Resolve a product's partner fields (with id normalization).<br>**Today —** business-partner ids sometimes arrive as strings that need to be - parsed to ints before VMM will accept them (vmmUtils's int-parse normalization) — an easy detail to…<br>**Done when:**<br>• partners resolve via VMM<br>• `status` merge correct | — |
| 🔸 `SPARK-PROD-G08`<br>`Product.measurementSets` + `claims` + `bom` + `productBom` + `packagingBom` + `productDetails` + `variations` + `associateProductsAsks` | 🟡 Medium `M` | Field Resolver | — | **Intent —** Resolve the 8 'ask a sibling domain' product fields (bom, measurement, …), each on demand.<br>**Today —** each of these 8 fields is "go ask a sibling domain (bom, measurement, - etc.) for this product's data" — but only if the caller asked for it (each has an includeXxx…<br>**Done when:**<br>• each sibling field resolves internally<br>• `includeXxx` branches honored | — |
| 🔸 `SPARK-PROD-G09`<br>`Product.productWorkspaceAttributes` + `productWorkspaceInfo` | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `search`, `tag` | — | **Intent —** Resolve a product's per-workspace attributes (incl. lazy designCycle).<br>**Today —** designCycle is computed lazily today — an inline async () => ... - closure attached to the value, evaluated only if a caller actually reads that sub-field. -…<br>**Done when:**<br>• both fields resolve<br>• `designCycle` is a nested fetcher | — |
| 🔸 `SPARK-PROD-G10`<br>`Product.ancestryProducts` + `rating` + `reservedDpcis` | 🟡 Medium `M` | Field Resolver<br>Calls: `relationship`, `rating`, `apex` | — | **Intent —** Resolve a product's ancestry, rating and reserved-DPCI fields.<br>**Today —** rating via RatingClient; reservedDpcis via getReservedDpcisFromApex<br>**Done when:**<br>• ancestry/rating/dpcis resolve<br>• rating null-on-error | — |
| 🔸 `SPARK-PROD-G11-1`<br>`Product.notRemovablePartnerIds` + `notRemovableWorkspaceIds` | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm`, `workspaceV2` | — | **Intent —** Compute which partners/workspaces can't be removed (still referenced).<br>**Today —** to figure out which partners/workspaces can't be removed from a product (e.g. because they're the last remaining owner), today's code calls into 4-5 other field…<br>**Done when:**<br>• `notRemovablePartnerIds`/`notRemovableWorkspaceIds` return the same results as source (same logical union of the underlying sibling data)<br>• No reflective resolver invocation remains — every call is a direct, statically-typed service method call | — |
| 🔸 `SPARK-PROD-G11-2`<br>`Product.associateProductsAsks` + `Product.variations` | 🟡 Medium `M` | Field Resolver | — | **Intent —** Resolve two sibling passthroughs (product-asks and variations).<br>**Today —** two straightforward sibling passthroughs — associateProductsAsks - (the product-ask records tied to this product) and variations (sibling product variation records) —…<br>**Done when:**<br>• `associateProductsAsks` resolves the product's ask records<br>• `variations` resolves the product's variation records | — |
| 🔸 `SPARK-PROD-G12`<br>`Product.division` **bug fix** (wrong loader) | 🟢 Low `XS` | Field Resolver<br>Calls: `ig` | — | **Intent —** Fix the wrong-loader bug so `division` returns the product's actual division.<br>**Today —** Product.division is supposed to return the product's division - (a specific org unit). - Instead, the source code has a copy-paste-style mistake: it calls…<br>**Done when:**<br>• `Product.division` and `DopplerDepartment.division` both return the true division shape (via `DivisionService`), not the department shape<br>• The client-shape-change risk is logged with the PO and confirmed via a client survey before rollout | — |
| 🔸 `SPARK-PROD-G13`<br>IG/tag/tcin/spg + template trivial-field group | 🟡 Medium `M` | Field Resolver<br>Calls: `ig`, `tag`, `corona` | — | **Intent —** Resolve a group of trivial IG / tag / TCIN / template fields.<br>**Today —** department/departments/clazz/brand/brands/divisions/productTemplateDepartments, tags, tcins, SPARK_Tcin.itemDetails (CORONA), SPARK_PackagingAttribute.spg (internal…<br>**Done when:**<br>• each field resolves to the right source | — |
| 🔸 `SPARK-PROD-G14`<br>Simple user/status fields + trivial pass-throughs (bundle) | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | — | **Intent —** Resolve simple people / status fields and trivial pass-throughs.<br>**Today —** createdBy/updatedBy/versionCreatedBy (user-profile), ProductComponentStatus.updatedBy, SPARK_ResourcesCount.productThumbnailId (re-fetch product), plus ~60 direct…<br>**Done when:**<br>• user fields resolve (null id → null)<br>• `productThumbnailId` re-fetches<br>• scalars mapped | — |
| 📄 `SPARK-PROD-G15`<br>Port product utils to Kotlin | 🟡 Medium `M` | Service | — | **Intent —** Port the shared product utility helpers to Kotlin.<br>**Today —** attachmentUtils, partnerUtils, teamUtils, productUtils, componentStatusUtils, resolvePaging, vmmUtils, accessControlUtils, removePartnerUtils<br>**Done when:**<br>• utils ported with unit tests<br>• counter logic fixed/verified<br>• ACL batch parallel-chunked | — |
| 📄 `SPARK-PROD-G16`<br>Test coverage, parity harness, load & cut-over rehearsal | 🟠 High `L` | Tests | C01, E01, E03, G01, G02 | **Intent —** The safety net: tests + parity + load checks proving the new Product DGS matches the old gateway before cut-over.<br>**Today —** ≥80% unit coverage; parity harness ≥50 fixtures (incl<br>**Done when:**<br>• unit ≥80%<br>• ≥50 parity fixtures green<br>• load p95 parity<br>• schema-diff intentional-only<br>• shadow-traffic rehearsal + rollback drill | ☐ Parity: DGS response matches spark-internal-graphql baseline<br>☐ Load: p95 latency is within spark-internal-graphql baseline<br>☐ contract<br>☐ Integration: shadow traffic rehearsal + rollback drill passes |

