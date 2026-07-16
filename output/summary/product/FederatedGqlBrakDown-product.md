# Federated GraphQL Breakdown — Product

| | |
|---|---|
| **Target DGS** | `plm-product (host)` |
| **T-Shirt Size** | **XXL** |
| **Total Stories** | 67 |
| **Complexity** | 🔴 5 Very High · 🟠 4 High · 🟡 25 Medium · 🟢 33 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-15 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving **Product** — the central entity of the PLM system — off the `spark-internal-graphql` gateway into the **`plm-product`** Netflix DGS.
- Product is the **largest and highest-risk** domain (18 queries, 20 mutations, ~50 field resolvers on a 2,629-line resolver) and the **host service** for the whole product family: BOM, Measurement, Impression, Packaging and others live in the same DGS, so their links from Product resolve **internally** rather than across the federation gateway.

- Most of the work is mechanical (the long tail of CRUD and simple field resolvers), but a handful of items carry real risk: the **TechPack count** query (a ~200-line, 14-step aggregation spanning 8 domains' data via 4 physical services, which becomes a federated composite-key entity), the **partner drop/undrop** orchestration, the cross-domain **components** and **attachmentsWithMetaData** field resolvers, and a **latent `division` bug**.
- We recommend the **facade-then-federate** approach for TechPack (draft **ADR-015** Option B; the pattern `techpack-migration-options.md` labels "Option D (hybrid)"): ship a thin query over a temporary aggregation facade so it works on day 1, then federate each piece to its owning domain, then retire the facade (`F-09`).

**ACL note:** the legacy gateway obtains per-resource capability tokens via ACL on nearly every call. Per
the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service
performs its own access control. Each complex case carries a scenario ADR
([`complexStories/*/02-adr-noacl-*.md`](https://github.com/XXX/blob/main/output/complexStories/*/02-adr-noacl-*.md)) recording this assumption's impact; those ratify together with the
global decision. ACL steps are noted in stories for context only.

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
| **Total stories** | **67** | green-field build stories (`G-11` split into `G-11-1`/`G-11-2` = +1). The 3 Phase-0 spike stubs (`S-01`–`S-03`) are tracked as **program spikes** in the global breakdown and Jira, not as rows here |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `PRODUCT-BE-C-01` — `getProducts(...)` two-stage hydration | `SPIKE-06a` | Hydration |
| 🔴🔬 `PRODUCT-BE-D-01` — `addProduct` | `SPIKE-06b` | Cross-Domain Association |
| 🔴🔬 `PRODUCT-BE-D-02` — `addProducts` (bulk) | `SPIKE-06b` | Cross-Domain Association |
| 🔴🔬 `PRODUCT-BE-D-04` — `updateProduct` | `SPIKE-06b` | Cross-Domain Association |
| 🔴🔬 `PRODUCT-BE-E-01` — `productBusinessPartnerActions` (REMOVE/DROP/UNDROP) | `SPIKE-03` | Partner Drop/Undrop + Ownership |
| 🔴🔬 `PRODUCT-BE-E-02` — `updateComponentStatuses` (5-loader fan-out) | `SPIKE-01` | Non-Atomic Write Saga |
| 🔴🔬 `PRODUCT-BE-E-03` — `getProductTechPackCountV1` stub + aggregation facade (facade-then-federate, Phase 1) | `SPIKE-02` | TechPack Aggregate |
| 🔴🔬 `PRODUCT-BE-E-04` — `getProductTechPackBulkCountV1` (bulk wrapper, ordering fix) | `SPIKE-02` | TechPack Aggregate |
| 🔴🔬 `PRODUCT-BE-G-07` — `Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status` | `SPIKE-04` | Not-Removable / Undroppable Partners |
| 🔴🔬 `PRODUCT-BE-G-11-1` — `Product.notRemovablePartnerIds` + `notRemovableWorkspaceIds` | `SPIKE-04` | Not-Removable / Undroppable Partners |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Deployment Model — Ship on Green, Per Story

- Every story is **end-to-end in one PR** and **independently deployable to production once its own tests and parity pass** — no waiting for the rest of the phase.
- The **one exception** is a story whose field is produced by **composing another subgraph's data** (a cross-subgraph **entity extension**, `extend type … @key` resolved by a different DGS): those go live only once the **owning subgraph is deployed**, and are marked
**BLOCKED-BY `<domain>`**.

- ✅ **Ships on green** — all B/C/D/E/G stories, the internal Phase-F contributions (`F-04`, `F-06`, `F-08`), the
  gateway/platform stories (`F-10`, `F-11`), and the **TechPack facade** (`E-03`/`E-04`), which is *designed* to
  work day 1 before any sibling federates.
- ⛔ **Waits for an owning subgraph (the exception)** — the true cross-subgraph federation stories
  **`F-01` (attachment), `F-02` (discussion), `F-03` (sample), `F-05` (claim), `F-07` (construction)**, plus
  **`F-09`** (facade retirement, which needs all 8 contributions live). These are the only stories held back
  from per-story prod release.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) | Ready when |
|---|---|---|---|---|
| B | Core Reads | 11 | 11–18d | after B-01 |
| C | Search & Listing | 5 | 17–29d | after B-01; C-01 gated on `SPIKE-06a` (Hydration, via `PRODUCT-BE-S-02`) |
| D | Mutations (simple) | 18 | 25–40d | after B-01; D-01/D-02/D-04 gated on `SPIKE-06b` (Association, via `PRODUCT-BE-S-01`); D-03/D-06/D-07/D-11 unblocked (single-backend, per ADR-011 scope) |
| E | Complex (partner/components/TechPack) | 4 | 33–56d | E-01 gated on `SPIKE-03` |
| F | Federation & Stitching | 12 | 22–40d (most BLOCKED-BY siblings) | after E-03 / siblings |
| G | Field Resolvers, Bug-fixes, Utils, Tests | 17 | 86–143d | after B-01. `G-11` split into `G-11-1`/`G-11-2` (16 → 17) |
| **Total** | | **67** | **194–326d** (buffered; sum of phase rows) | |

> One engineer ≈ **39–66 sprints**. Heavily parallelizable after B-01; 2–3 engineers strongly recommended.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories; the `Categories` union `@DgsTypeResolver` remains a dedicated story.

> **Thin DGS wrappers — parallel after B-01.** The model, REST controller (GET/POST/PUT) and service already exist; each story only adds the Netflix-DGS layer so the federated graph can stitch this subgraph. The **one-time DGS module scaffold** B-01 lands (schema file + scalar registration + service/Feign wiring) is a prerequisite for every operation story, so it is **assumed — not repeated in each story's `Depends On`** (rows list only genuine story-to-story dependencies). E.g. `D-08 removeProductResources` is a one-line wrapper over the existing REST `DELETE`/`PUT`, so its `Depends On` is **—**. After B-01, phases B/C/D/G run fully in parallel.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~39–66 sprints | sequential — not recommended for this domain |
| 2 engineers | ~25–42 sprints | B/C/D parallel after B-01 |
| 3–4 engineers | ~18–28 sprints | A done → B + C + D + most of G in parallel; E and the two X-Large fields on dedicated owners |

> Phase G dominates the calendar; the two X-Large field resolvers (`attachmentsWithMetaData`, `components`)
> and TechPack (E-03/E-04) are the cost-and-risk centre of the whole program.

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 0 | Program spikes | run in Sprint 0 (see global Phase 0 — Program Spikes) so D/C/E work isn't waiting |
| 1–2 | B-01 (DGS module init + service wiring + first resolver) | schema, types, stubs, Categories resolver, ResourcesCount, service port |
| 3 | B-01–B-11 | all core reads (incl. rules reads) |
| 4 | C-01–C-05 | search/listing + rating + rules search (C-01 needs `SPIKE-06a` concluded) |
| 5–6 | D-01–D-18 | all simple mutations, parallelizable (D-01/D-02/D-04 need `SPIKE-06b` concluded; D-03/D-06/D-07/D-11 unblocked) |
| 7–8 | E-03/E-04 | TechPack facade + bulk (focused; facade-then-federate direction already resolved, draft ADR-015) |
| 9 | E-01/E-02 | partner actions (needs `SPIKE-03` concluded) + component fan-out |
| 10–12 | G-01–G-10, G-11-1, G-11-2, G-12–G-14 | field resolvers (G-01/G-02 X-Large get their own sprint) |
| 13 | G-15 + G-16 | utils port + tests/parity/load/cut-over |
| post-launch | F-01–F-09 | TechPack federation (unblocked as siblings migrate) + facade retirement |
| any | F-10–F-12 | gateway composition + platform verify + drift decision |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (11 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PRODUCT-BE-B-01`<br>`getProduct(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up a single product by id (the core product read everything else builds on).<br>**Today —** getByID GET ${v1}?productId={id} → camelCase or null; DataLoader-batched<br>**Done when:**<br>• returns product; 404→null<br>• batches N ids in 1 call |
| 🔷 `PRODUCT-BE-B-02`<br>`getProductsByIds(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up several products at once by their ids.<br>**Today —** getByIdList GET ${v1}?productId={csv}&page=0&size=10000&sort=createdDate,desc; primes getByID<br>**Done when:**<br>• returns paged products for ids<br>• primes single-id loader |
| 🔷 `PRODUCT-BE-B-03`<br>`getProductStatus` (cacheable) | 🟢 Low `XS` | Query | — | **Intent —** Returns the list of possible product statuses (dropdown options).<br>**Today —** getStatus master status list<br>**Done when:**<br>• returns statuses<br>• cached |
| 🔷 `PRODUCT-BE-B-04`<br>`getProductVersions(id)` | 🟢 Low `XS` | Query | — | **Intent —** Lists the saved versions of a product.<br>**Today —** getVersions GET ${v1}/{id}/versions?page=0&size=10000<br>**Done when:**<br>• returns versions |
| 🔷 `PRODUCT-BE-B-05`<br>`getCopyStatus(id)` | 🟢 Low `XS` | Query | — | **Intent —** Tells you whether a product copy is still in progress or done.<br>**Today —** getCopyStatus GET ${v2}/count/resource-type?copyId={id}<br>**Done when:**<br>• returns copy status |
| 🔷 `PRODUCT-BE-B-06`<br>`getProductTemplateById(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up a product template by id.<br>**Today —** getByID → response \\|\\| {} (empty object on miss — preserve)<br>**Done when:**<br>• returns product or empty object (not null) |
| 🔷 `PRODUCT-BE-B-07`<br>`getProductRules` | 🟢 Low `XS` | Query | — | **Intent —** Returns the product business rules.<br>**Today —** getAllRules GET $… → content<br>**Done when:**<br>• returns rules content |
| 🔷 `PRODUCT-BE-B-08`<br>`getProductRulesById(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up one business rule by id.<br>**Today —** getRuleById GET $…<br>**Done when:**<br>• returns rule |
| 🔷 `PRODUCT-BE-B-09`<br>`getAllAvailableRules` | 🟢 Low `XS` | Query | — | **Intent —** Lists all the rules that are available to apply.<br>**Today —** getAvailableRules GET …/spark_rules/v1/rules<br>**Done when:**<br>• returns available rules |
| 🔷 `PRODUCT-BE-B-10`<br>`getProductDeptRules(productIds, departmentIds, activeOnly)` | 🟢 Low `XS` | Query<br>Calls: `ruleLibrary` | — | **Intent —** Returns the department-level rules for given products.<br>**Today —** flag fork USE_NEW_RULES_API ? ruleLibrary.searchRuleLibrary : product.searchProductDeptRules GET …/spark_rules/v1/search?productIds=&departmentIds=&activeOnly=. PO…<br>**Done when:**<br>• default `activeOnly=true`<br>• flag selects the correct backend |
| 🔷 `PRODUCT-BE-B-11`<br>`getProductBPRules(productIds, businessPartnerIds, activeOnly)` | 🟢 Low `XS` | Query<br>Calls: `ruleLibrary` | — | **Intent —** Returns the business-partner-level rules for given products.<br>**Today —** same as B-10 with businessPartnerIds<br>**Done when:**<br>• flag fork honored; BP filter applied |

> **`PRODUCT-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `product.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql. **This scaffold is a prerequisite for every B/C/D/G story** — they need the module + schema file to compile their DGS wrapper — so it is assumed globally (shown once in the dependency graph) and **not repeated** in each story's `Depends On`. After it lands, the wrappers parallelize.


### 🔍 Phase C — Search & Listing (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔷 `PRODUCT-BE-C-01`<br>`getProducts(...)` two-stage hydration<br>🔴🔬 _Spike-gated on `SPIKE-06a` (Hydration) — see global Spike Detail_ | 🟠 High `L` | Query<br>Calls: `search` | SPIKE-06a | **Intent —** List products by combining the search index with the canonical record (two-stage hydration).<br>**Today —** listing products needs data from two places — the search index (which - knows flags like "has boms", "has claims", workspace membership) and the canonical product…<br>**Done when:**<br>• parity for 4 arg combos (no flags / all flags / resourceType=workspaces / filter array)<br>• truthy defaults preserved<br>• elastic flags merged onto canonical<br>• Workspace-filter placement and elastic/canonical staleness handling match `SPIKE-06a`'s decision | ☐ 4 combos<br>☐ default truthiness<br>☐ merge<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔷 `PRODUCT-BE-C-02`<br>`getProductTemplates(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | — | **Intent —** Lists product templates, with optional filters on what to include.<br>**Today —** (search) getFilteredProductsListing({resourceType:'product', includeBoms:false, ...7 includeXxxTemplates flags, types}) → return elastic response (no 2nd hydration)<br>**Done when:**<br>• all 7 template-include flags forwarded<br>• `types:[Int]` filter applied | — |
| 🔷 `PRODUCT-BE-C-03`<br>`getCategories(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | — | **Intent —** Returns the category tree for products.<br>**Today —** default productType ?? 100; (search) getProductCategories GET ${elastic}/search/${snake_case(type)}?resourceType=&resourceId=&productType= → ProductsCategories…<br>**Done when:**<br>• `snake_case(type)` path exact<br>• wires to `Categories` union | — |
| 🔷 `PRODUCT-BE-C-04`<br>`getRatingByTcin(tcin)` (external rating) | 🟡 Medium `M` | Query<br>Calls: `rating` | — | **Intent —** Gets the customer rating for a product (from an external ratings service).<br>**Today —** (external) GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={API_KEY} (skipJsonParse) → JSON.parse → {averageRating, reviewCount}…<br>**Done when:**<br>• parses statistics to `Rating`<br>• any error → null<br>• API key from config/Vault, not source | — |
| 🔷 `PRODUCT-BE-C-05`<br>`searchProductRules(...)` | 🟡 Medium `M` | Query<br>Calls: `ruleLibrary` | — | **Intent —** Searches product rules.<br>**Today —** flag fork; legacy GET …/spark_rules/v1/search_mapped?... → productRuleResponseTransformer → camelCase<br>**Done when:**<br>• flag fork honored<br>• legacy response transformed correctly | — |


### ✏️ Phase D — Mutations (18 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔴🔬 🔶 `PRODUCT-BE-D-01`<br>`addProduct`<br>🔴🔬 _Spike-gated on `SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `workspaceV2`, `attachment` | SPIKE-06b | **Intent —** Create a product (optionally copy from another + associate a workspace).<br>**Today —** POST ${v1} + optional copyProductToProduct(copyProduct) + workspace association<br>**Done when:**<br>• creates product<br>• optional copy runs when `copyProduct` present<br>• workspace assoc applied via the shared association component (no bespoke fan-out code)<br>• failure after create (link or copy fails) surfaces per the mutation's declared failure policy — default fail-fast, no rollback, documented (ADR-011 §4) |
| 🔴🔬 🔶 `PRODUCT-BE-D-02`<br>`addProducts` (bulk)<br>🔴🔬 _Spike-gated on `SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | SPIKE-06b | **Intent —** Create many products at once (plus attachment links).<br>**Today —** bulk POST ${v1}/bulk + attachment-link side-effects (no rollback — preserve, flag)<br>**Done when:**<br>• bulk creates<br>• attachment links applied via the shared association component; no-rollback behaviour documented (compensation deferred to `SPIKE-01`)<br>• no resolver import remains; the formerly fire-and-forget attachment re-point is awaited and its failure visible (accepted deviations per ADR-011 §4) |
| 🔶 `PRODUCT-BE-D-03`<br>`bulkUpdateProducts` | 🟡 Medium `M` | Mutation | — | **Intent —** Update many products in one call.<br>**Today —** PUT ${v1}/mass_update<br>**Done when:**<br>• mass-updates products |
| 🔴🔬 🔶 `PRODUCT-BE-D-04`<br>`updateProduct`<br>🔴🔬 _Spike-gated on `SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | SPIKE-06b | **Intent —** Edit a product (optional copy + template-attachment cleanup).<br>**Today —** PUT ${v1}/{id} + optional copy + archive removed-template attachments (template branch)<br>**Done when:**<br>• updates product<br>• optional copy<br>• removed-template attachments archived (template branch) |
| 🔶 `PRODUCT-BE-D-05`<br>`carryForwardProduct` | 🟡 Medium `M` | Mutation | — | **Intent —** Carries a product forward (creates the next season/version from it).<br>**Today —** PUT ${v1}/{productId}/carry_forward/{workspaceId} — uses every field on CarryForwardProductInput<br>**Done when:**<br>• all input fields mapped to the request |
| 🔶 `PRODUCT-BE-D-06`<br>`addTeamsToProduct` 🔀 Collab Canvas | 🟢 Low `XS` | Mutation | — | **Intent —** Adds teams (and their partners) to a product.<br>**Today —** POST ${v1}/{productId}/resources/bulk + manage_workspace_teams<br>**Done when:**<br>• adds teams + new partners + workspace links<br>• partner-add failure exits early with a thrown typed error (today `return new Error(...)` — standardized per ADR-011 §4 pin-down 4, accepted deviation); teams are not added after a failed partner add (legacy order preserved) |
| 🔶 `PRODUCT-BE-D-07`<br>`addBusinessPartnersToProductWithType` 🔀 Collab Canvas | 🟢 Low `XS` | Mutation | — | **Intent —** Adds business partners to a product with a given type.<br>**Today —** POST ${v1}/{productId}/partners-add/bulk; success = response has product_id and no status_code; failure = log + return new Error(...) (returned, not thrown — surfaces…<br>**Done when:**<br>• adds partners with type<br>• failure throws a typed `DgsException` instead of `return new Error(...)` (accepted parity deviation, ADR-011 §4 pin-down 4) |
| 🔶 `PRODUCT-BE-D-08`<br>`removeProductResources` | 🟢 Low `XS` | Mutation | — | **Intent —** Removes resources (links) from a product.<br>**Today —** DELETE ${v1}/{productId}/resources/bulk<br>**Done when:**<br>• removes resources |
| 🔶 `PRODUCT-BE-D-09`<br>`updateBusinessPartnerStatuses` | 🟢 Low `XS` | Mutation | — | **Intent —** Updates the status of business partners on a product.<br>**Today —** PUT ${v1}/{productId}/status_update/bulk<br>**Done when:**<br>• updates partner statuses |
| 🔶 `PRODUCT-BE-D-10`<br>`updateViewToggle` | 🟢 Low `XS` | Mutation | — | **Intent —** Toggles whether a product is hidden.<br>**Today —** PUT ${v1} view toggle<br>**Done when:**<br>• toggles hidden |
| 🔶 `PRODUCT-BE-D-11`<br>`updateWorkspaceAttributes` 🔀 Collab Canvas | 🟢 Low `XS` | Mutation | — | **Intent —** Updates a product's workspace attributes.<br>**Today —** PUT ${v1}/{productId} workspace attrs<br>**Done when:**<br>• updates workspace attrs |
| 🔶 `PRODUCT-BE-D-12`<br>`updateProductTeamsWorkspaceContext` | 🟢 Low `XS` | Mutation | — | **Intent —** Adds or removes team↔workspace pairings on a product.<br>**Today —** PUT team-workspace add/remove<br>**Done when:**<br>• adds/removes team-workspace pairs |
| 🔶 `PRODUCT-BE-D-13`<br>`linkProduct` | 🟢 Low `XS` | Mutation | — | **Intent —** Links a parent and child product together.<br>**Today —** PUT link — throws on backend error (only mutation that does)<br>**Done when:**<br>• links parent/child<br>• backend error → exception (not null) |
| 🔶 `PRODUCT-BE-D-14`<br>`unlinkProduct` | 🟢 Low `XS` | Mutation | — | **Intent —** Unlinks a parent and child product.<br>**Today —** PUT unlink<br>**Done when:**<br>• unlinks parent/child |
| 🔶 `PRODUCT-BE-D-15`<br>`addProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Creates a product rule.<br>**Today —** POST …/spark_rules/v1<br>**Done when:**<br>• creates rule |
| 🔶 `PRODUCT-BE-D-16`<br>`updateProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Updates a product rule.<br>**Today —** PUT …/spark_rules/v1/{id}<br>**Done when:**<br>• updates rule |
| 🔶 `PRODUCT-BE-D-17`<br>`deleteProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Deletes a product rule.<br>**Today —** DELETE …/spark_rules/v1/{id} → Boolean<br>**Done when:**<br>• deletes; returns Boolean |
| 🔶 `PRODUCT-BE-D-18`<br>`updateComponentStatus` (bulk) | 🟢 Low `XS` | Mutation | — | **Intent —** Bulk-updates the status of many components at once.<br>**Today —** bulk PUT ${v1}/component_status_update/bulk<br>**Done when:**<br>• bulk-updates component statuses |


### ⚙️ Phase E — Complex Operations (4 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `PRODUCT-BE-E-01`<br>`productBusinessPartnerActions` (REMOVE/DROP/UNDROP)<br>🔴🔬 _Spike-gated on `SPIKE-03` (Partner Drop/Undrop + Ownership) — see global Spike Detail_ | 🔴 Very High `XL` | Mutation<br>Calls: `sampleV2`, `recentlyViewed`, `todo`, `favorite` | SPIKE-03 | **Intent —** Remove / drop / undrop a business partner across a product — a ~220-line orchestrated write.<br>**Today —** removing, dropping, or un-dropping a business partner from a product - isn't one write — it's a ~220-line dispatcher that updates the partner's status and then fans…<br>**Done when:**<br>• all 3 paths reach REST parity (recorded fixtures), incl. the design-partner branch (`skipSamples` when `partnerType == DESIGN_PARTNER`)<br>• partial-failure compensation log/strategy implemented per `SPIKE-03`'s decision (draft ADR-012: per-step policy — partner-status compensate · ACL retry-then-fail · activity/profile retry+reconcile)<br>• cleanup fan-out runs per case, with per-target failure isolation (one cleanup failing is visible and doesn't silently swallow the others)<br>• on DROP, ACL revocation completes **before** the mutation returns success; on UNDROP, ACL restore precedes participant undrops — proven by an automated test, not convention (ADR-012 §4 ordering constraint)<br>• no Relationship-Service traversal and no `UserProfileAttributes` resolver import remain in the ported flow (replaced by participant enumeration + a user-profile client call) | ☐ REMOVE<br>☐ DROP<br>☐ UNDROP<br>☐ design-partner branch (samples skipped)<br>☐ partial-failure per step<br>☐ ACL-before-return ordering invariant<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔴🔬 🔶 `PRODUCT-BE-E-02`<br>`updateComponentStatuses` (5-loader fan-out)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `claim` | SPIKE-01 | **Intent —** Update a product's component statuses, fanning out to 5 sibling loaders.<br>**Today —** updating component statuses fans out to 5 places in parallel (bom, - measurement, productDetail, packaging — all internal — plus claim, external). - The bug: a loop…<br>**Done when:**<br>• per-loader failures don't fail siblings<br>• shadow var fixed<br>• parity | ☐ 5-way fan-out<br>☐ partial failure isolation<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔴🔬 🔷 `PRODUCT-BE-E-03`<br>`getProductTechPackCountV1` stub + aggregation facade (facade-then-federate, Phase 1)<br>🔴🔬 _Spike-gated on `SPIKE-02` (TechPack Aggregate) — see global Spike Detail_ | 🔴 Very High `XL` | Query<br>Calls: `attachment`, `search` | SPIKE-02 | **Intent —** Build the TechPack panel's badge counts by aggregating across ~8 domains.<br>**Today —** the TechPack panel shows badge counts (attachments, discussions, - samples, boms, claims, etc.) for a product. - Getting those counts today means walking the entire…<br>**Done when:**<br>• Returns a fully populated 11-field `ResourcesCount` from the facade for a valid `(productId, partnerId, workspaceContext, parentProductId)` input<br>• `@DgsEntityFetcher(name="ResourcesCount")` reconstructs the entity from key + context on an `_entities` query (federation-ready shell)<br>• Recorded-fixture parity vs `spark-internal-graphql` for ≥ 5 pinned inputs, including: a product **with a parent** (double-walk), > 100 walked ids (chunked ACL), a 3D attachment, and a critical thread whose parent discussion is outside the walk — 100% field-value match modulo the ADR-015 §4 deviation list (parallelized elastic/ACL calls; counts unchanged)<br>• Facade is observable: per-slice latency + error metrics and a health endpoint exist (they gate the `F-01`–`F-08` re-homings and the `F-09` retirement check)<br>• Facade is behavior-frozen: deviations limited to ADR-015 §4 pin-downs; `CODEOWNERS` guard in place so new feature work lands in the owning domain's `F0x` story instead | ☐ facade call returns 11 populated fields<br>☐ entity fetcher via `_entities`<br>☐ parity ≥ 5 pinned inputs (incl. parent double-walk, >100 ids, 3D attachment, out-of-walk critical thread)<br>☐ per-slice metrics emitted<br>☐ Integration: full query via DGS test client returns expected shape |
| 🔴🔬 🔷 `PRODUCT-BE-E-04`<br>`getProductTechPackBulkCountV1` (bulk wrapper, ordering fix)<br>🔴🔬 _Spike-gated on `SPIKE-02` (TechPack Aggregate) — see global Spike Detail_ | 🔴 Very High `XL` | Query<br>Calls: `attachment`, `search` | SPIKE-02, E-03 | **Intent —** Return TechPack counts for many products at once, in the caller's order.<br>**Today —** the bulk version runs all N single-product lookups concurrently and - returns them in whatever order they happen to finish — not the order the caller asked for. - If a…<br>**Done when:**<br>• `bulk(P1..Pn) == [single(P1)..single(Pn)]` in input order<br>• empty list → [] | ☐ order preserved<br>☐ empty<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (12 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PRODUCT-BE-F-01`<br>`ResourcesCount.productAttachments` + `discussionAttachments` (federated, from Attachment) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Contribute attachment counts to the product's TechPack rollup (from Attachment).<br>**Done when:**<br>• `productAttachments`/`discussionAttachments` resolve on the federated `ResourcesCount`; the `E-03` facade stops populating them<br>• Parity vs the facade for the same inputs<br>• Field is live in prod only after `plm-attachment` is deployed (ship gate honored) |
| 🔸 `PRODUCT-BE-F-02`<br>`ResourcesCount.discussions` (federated, from Discussion) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's discussion count — answered by the Discussion service once it's live.<br>**Done when:**<br>• `discussions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `plm-discussion` is deployed |
| 🔸 `PRODUCT-BE-F-03`<br>`ResourcesCount.sample` (federated, from Sample) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's sample count — answered by the Sample service once it's live.<br>**Done when:**<br>• `sample` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `plm-sample` is deployed |
| 🔸 `PRODUCT-BE-F-04`<br>`ResourcesCount.measurementSets` (internal, from Measurement) | 🟢 Low `XS` | Field Resolver | E-03 | **Intent —** Fills in the product's measurement-set count — answered in-process by the co-located Measurement code.<br>**Done when:**<br>• `measurementSets` resolves in-process; no gateway hop; parity vs facade |
| 🔸 `PRODUCT-BE-F-05`<br>`ResourcesCount.claims` (federated, from Claim) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's claims count — answered by the Claims service once it's live.<br>**Done when:**<br>• `claims` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `spark-claims` is deployed |
| 🔸 `PRODUCT-BE-F-06`<br>`ResourcesCount.productBoms` + `packagingBoms` + `boms` (internal, from BOM) | 🟢 Low `XS` | Field Resolver | E-03 | **Intent —** Fills in the product's BOM counts — answered in-process by the co-located BOM code.<br>**Done when:**<br>• `productBoms`/`packagingBoms`/`boms` resolve in-process; no gateway hop; parity vs facade |
| 🔸 `PRODUCT-BE-F-07`<br>`ResourcesCount.constructions` (federated, from Construction) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's construction count — answered by the Construction service once it's live.<br>**Done when:**<br>• `constructions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after the construction subgraph is deployed |
| 🔸 `PRODUCT-BE-F-08`<br>`ResourcesCount.watchlists` (internal, from Watchlist) | 🟢 Low `XS` | Field Resolver | E-03 | **Intent —** Fills in the product's watchlist count — answered in-process by the co-located Watchlist code.<br>**Done when:**<br>• `watchlists` resolves in-process; no gateway hop; parity vs facade |
| 🔸 `PRODUCT-BE-F-09`<br>Retire the TechPack aggregation facade | 🟢 Low `XS` | Field Resolver | F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08 | **Intent —** Removes the temporary TechPack 'facade' once every count is served by its real owner.<br>**Today —** remove TechPackAggregatorClient; TechPackDataFetcher returns key+context only; decommission the facade<br>**Done when:**<br>• all 11 `ResourcesCount` fields resolve via federation<br>• facade health-check endpoint returns 404 (decommissioned)<br>• no orphaned config (feature flags, Feign client beans, etc. referencing the retired facade) |
| 🔸 `PRODUCT-BE-F-10`<br>Hive Gateway supergraph composition | 🟢 Low `XS` | Field Resolver | — | **Intent —** Composes all the subgraphs into one federated graph at the gateway.<br>**Today —** add plm-product subgraph URL; verify composition with VMM/IG/CORONA/Doppler stubs; smoke-test cross-subgraph query<br>**Done when:**<br>• supergraph composes<br>• cross-subgraph smoke test passes |
| 🔸 `PRODUCT-BE-F-11`<br>Platform stub verification (VMM/IG/Doppler/CORONA/APEX) | 🟢 Low `XS` | Field Resolver | F-10 | **Intent —** Verifies each external platform (VMM, IG, etc.) resolves through its stub.<br>**Today —** confirm the gateway resolves full platform types from product-emitted @key stubs<br>**Done when:**<br>• each platform type resolves via its stub key |
| 📄 `PRODUCT-BE-F-12`<br>Deferred partner-wrapper decision (drift mutations) | 🟢 Low `XS` | Schema | E-01 | **Intent —** Decide the fate of three drift partner mutations that have no resolvers.<br>**Today —** three old mutation names (removeProductBusinessPartner, - dropProductBusinessPartner, unDropProductBusinessPartner) still exist in the schema, but nothing calls them…<br>**Done when:**<br>• traffic survey complete<br>• decision implemented |


### 🧪 Phase G — Field Resolvers & Tests (17 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `PRODUCT-BE-G-01`<br>`Product.attachmentsWithMetaData` | 🔴 Very High `XL` | Field Resolver<br>Calls: `attachment`, `relationship` | — | **Intent —** Resolve a product's mixed attachments-with-metadata feed (files + discussions + samples).<br>**Today —** the attachments panel on a product shows a mixed feed — actual file - attachments, plus discussions and samples that are also surfaced as if they were attachments…<br>**Done when:**<br>• parity for mixed attachment/discussion/thread/sample<br>• ordering rank preserved (product=0, discussion=1, sample=2; createdAt DESC tiebreak) | ☐ merge<br>☐ ordering<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `PRODUCT-BE-G-02`<br>`Product.components` | 🔴 Very High `XL` | Field Resolver<br>Calls: `search` | — | **Intent —** List everything attached to a product, tagged by type, with counts.<br>**Today —** the components tab lists everything attached to a product — measurements, - claims, boms, product-details, packaging — tagged by type, with counts (how many are…<br>**Done when:**<br>• parity for 50+ components, incl. a product with > 100 components (chunked ACL) and a claim with a missing ACL record (throw path preserved, ADR-014 pin-down 2)<br>• `archivedCount`/`countByComponents` match source exactly (incl. name/status fallbacks and `type 2 → packagingBom`)<br>• ACL batched — exactly one `getAccessControlBatch` call per resolution (no N+1), asserted by a call-count test<br>• no `info.variableValues` read; explicit field args confirmed against UI queries (contract test, ADR-014 pin-down 5) | ☐ merge<br>☐ counts<br>☐ batched ACL<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `PRODUCT-BE-G-03`<br>`Product.attachments` + `attachmentsV3` + `attachmentSummary` + `ProductTemplate.attachmentsData` | 🟠 High `L` | Field Resolver<br>Calls: `attachment`, `search` | G-01 | **Intent —** Resolve the product's attachment views (via a shared enrichment service).<br>**Today —** four related resolvers sharing AttachmentEnrichmentService (G-01)<br>**Done when:**<br>• each field returns its shape<br>• shares G-01 service | ☐ each field<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `PRODUCT-BE-G-04`<br>`ProductsCategories.categories` (12-case) + `DopplerDepartment` fields | 🟡 Medium `M` | Field Resolver<br>Calls: `doppler` | — | **Intent —** Resolve the polymorphic categories union (12 branches) and department fields.<br>**Today —** categories is a polymorphic union — depending on which category type - the caller asked for, a different one of 12 branches builds the response shape. - Two of those…<br>**Done when:**<br>• each category type built correctly<br>• Doppler fetched once | — |
| 🔸 `PRODUCT-BE-G-05`<br>`Product.samples` + `sampleIds` + `elasticSamplesList` | 🟡 Medium `M` | Field Resolver<br>Calls: `sampleV2`, `search` | — | **Intent —** Resolve a product's samples from local context (removing the fragile args hack).<br>**Today —** today these fields reach into GraphQL's internal info.variableValues to read arguments that were passed to a different, parent query — a fragile, implicit way to pass…<br>**Done when:**<br>• samples/sampleIds/elastic resolve<br>• no `info.variableValues` read | — |
| 🔸 `PRODUCT-BE-G-06`<br>`Product.teams` + `discussionsV2` + `discussionsCount` + `workspaces` | 🟡 Medium `M` | Field Resolver<br>Calls: `teamV2`, `discussion`, `search`, `workspaceV2` | — | **Intent —** Resolve a product's team / discussion / workspace fields.<br>**Today —** team/discussion/workspace elastic lookups<br>**Done when:**<br>• each field resolves | — |
| 🔴🔬 🔸 `PRODUCT-BE-G-07`<br>`Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status`<br>🔴🔬 _Spike-gated on `SPIKE-04` (Not-Removable / Undroppable Partners) — see global Spike Detail_ | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm` | SPIKE-04 | **Intent —** Resolve a product's partner fields (with id normalization).<br>**Today —** business-partner ids sometimes arrive as strings that need to be - parsed to ints before VMM will accept them (vmmUtils's int-parse normalization) — an easy detail to…<br>**Done when:**<br>• partners resolve via VMM<br>• `status` merge correct | — |
| 🔸 `PRODUCT-BE-G-08`<br>`Product.measurementSets` + `claims` + `bom` + `productBom` + `packagingBom` + `productDetails` + `variations` + `associateProductsAsks` | 🟡 Medium `M` | Field Resolver | — | **Intent —** Resolve the 8 'ask a sibling domain' product fields (bom, measurement, …), each on demand.<br>**Today —** each of these 8 fields is "go ask a sibling domain (bom, measurement, - etc.) for this product's data" — but only if the caller asked for it (each has an includeXxx…<br>**Done when:**<br>• each sibling field resolves internally<br>• `includeXxx` branches honored | — |
| 🔸 `PRODUCT-BE-G-09`<br>`Product.productWorkspaceAttributes` + `productWorkspaceInfo` | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `search`, `tag` | — | **Intent —** Resolve a product's per-workspace attributes (incl. lazy designCycle).<br>**Today —** designCycle is computed lazily today — an inline async () => ... - closure attached to the value, evaluated only if a caller actually reads that sub-field. -…<br>**Done when:**<br>• both fields resolve<br>• `designCycle` is a nested fetcher | — |
| 🔸 `PRODUCT-BE-G-10`<br>`Product.ancestryProducts` + `rating` + `reservedDpcis` | 🟡 Medium `M` | Field Resolver<br>Calls: `relationship`, `rating`, `apex` | — | **Intent —** Resolve a product's ancestry, rating and reserved-DPCI fields.<br>**Today —** rating via RatingClient; reservedDpcis via getReservedDpcisFromApex<br>**Done when:**<br>• ancestry/rating/dpcis resolve<br>• rating null-on-error | — |
| 🔴🔬 🔸 `PRODUCT-BE-G-11-1`<br>`Product.notRemovablePartnerIds` + `notRemovableWorkspaceIds`<br>🔴🔬 _Spike-gated on `SPIKE-04` (Not-Removable / Undroppable Partners) — see global Spike Detail_ | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm`, `workspaceV2` | SPIKE-04 | **Intent —** Compute which partners/workspaces can't be removed (still referenced).<br>**Today —** to figure out which partners/workspaces can't be removed from a product (e.g. because they're the last remaining owner), today's code calls into 4-5 other field…<br>**Done when:**<br>• `notRemovablePartnerIds`/`notRemovableWorkspaceIds` return the same results as source (same logical union of the underlying sibling data)<br>• No reflective resolver invocation remains — every call is a direct, statically-typed service method call | — |
| 🔸 `PRODUCT-BE-G-11-2`<br>`Product.associateProductsAsks` + `Product.variations` | 🟡 Medium `M` | Field Resolver | — | **Intent —** Resolve two sibling passthroughs (product-asks and variations).<br>**Today —** two straightforward sibling passthroughs — associateProductsAsks - (the product-ask records tied to this product) and variations (sibling product variation records) —…<br>**Done when:**<br>• `associateProductsAsks` resolves the product's ask records<br>• `variations` resolves the product's variation records | — |
| 🔸 `PRODUCT-BE-G-12`<br>`Product.division` **bug fix** (wrong loader) | 🟢 Low `XS` | Field Resolver<br>Calls: `ig` | — | **Intent —** Fix the wrong-loader bug so `division` returns the product's actual division.<br>**Today —** Product.division is supposed to return the product's division - (a specific org unit). - Instead, the source code has a copy-paste-style mistake: it calls…<br>**Done when:**<br>• `Product.division` and `DopplerDepartment.division` both return the true division shape (via `DivisionService`), not the department shape<br>• The client-shape-change risk is logged with the PO and confirmed via a client survey before rollout | — |
| 🔸 `PRODUCT-BE-G-13`<br>IG/tag/tcin/spg + template trivial-field group | 🟡 Medium `M` | Field Resolver<br>Calls: `ig`, `tag`, `corona` | — | **Intent —** Resolve a group of trivial IG / tag / TCIN / template fields.<br>**Today —** department/departments/clazz/brand/brands/divisions/productTemplateDepartments, tags, tcins, SPARK_Tcin.itemDetails (CORONA), SPARK_PackagingAttribute.spg (internal…<br>**Done when:**<br>• each field resolves to the right source | — |
| 🔸 `PRODUCT-BE-G-14`<br>Simple user/status fields + trivial pass-throughs (bundle) | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | — | **Intent —** Resolve simple people / status fields and trivial pass-throughs.<br>**Today —** createdBy/updatedBy/versionCreatedBy (user-profile), ProductComponentStatus.updatedBy, SPARK_ResourcesCount.productThumbnailId (re-fetch product), plus ~60 direct…<br>**Done when:**<br>• user fields resolve (null id → null)<br>• `productThumbnailId` re-fetches<br>• scalars mapped | — |
| 📄 `PRODUCT-BE-G-15`<br>Port product utils to Kotlin | 🟡 Medium `M` | Service | — | **Intent —** Port the shared product utility helpers to Kotlin.<br>**Today —** attachmentUtils, partnerUtils, teamUtils, productUtils, componentStatusUtils, resolvePaging, vmmUtils, accessControlUtils, removePartnerUtils<br>**Done when:**<br>• utils ported with unit tests<br>• counter logic fixed/verified<br>• ACL batch parallel-chunked | — |
| 📄 `PRODUCT-BE-G-16`<br>Test coverage, parity harness, load & cut-over rehearsal | 🟠 High `L` | Tests | C-01, E-01, E-03, G-01, G-02 | **Intent —** The safety net: tests + parity + load checks proving the new Product DGS matches the old gateway before cut-over.<br>**Today —** ≥80% unit coverage; parity harness ≥50 fixtures (incl<br>**Done when:**<br>• unit ≥80%<br>• ≥50 parity fixtures green<br>• load p95 parity<br>• schema-diff intentional-only<br>• shadow-traffic rehearsal + rollback drill | ☐ Parity: DGS response matches spark-internal-graphql baseline<br>☐ Load: p95 latency is within spark-internal-graphql baseline<br>☐ contract<br>☐ Integration: shadow traffic rehearsal + rollback drill passes |

