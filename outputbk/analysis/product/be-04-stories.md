# Phase 4: Migration Plan & Stories — Product

> **Domain:** `product` · **Target DGS:** `ProductService` → `plm-product` · **Generated:** 2026-06-26
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md), [be-03-schema.graphql](./be-03-schema.graphql), [be-03-schema-analysis.md](./be-03-schema-analysis.md), [be-05-attribute-inventory.md](./be-05-attribute-inventory.md)
> **Index:** `be-04-stories-index.yaml`

- Engineers: each story is self-contained (read *Current Behaviour → Target → Files → Acceptance → Tests*).
- Detailed pseudo-logic for every operation is in [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) (referenced per story).
- **ACL is context-only** — no ACL work in any story.

## 1. Phases Overview
| Phase | Name | Stories |
|---|---|---|
| 0 | Spikes | S-01–S-03 |
| B | Core Reads | B-01–B-11 |
| C | Search & Listing | C-01–C-05 |
| D | Mutations (simple) | D-01–D-18 |
| E | Complex Operations (partner actions, component fan-out, TechPack) | E-01–E-04 |
| F | Federation & Stitching — platform/gateway work (facade retirement, composition, stub verification, contract alignment; **F-14 added by the federation review**) | F-04, F-06, F-08–F-12, F-14 |
| G | Field Resolvers, Utils (**G-11 split into G-11-1/G-11-2**; **G-17 added, recommended/PO-gated**) | G-01–G-11-2, G-13–G-15, G-17 |
| H | Entity Resolution — cross-subgraph `@DgsEntityFetcher`/`@key` fields resolved by a *separate* subgraph (split out from Phase F) | H-01–H-06 |

> **Phase 0 note.** Three items that used to sit as open "Decisions Required" bullets, or as a bare annotation
> on a story row, are now real spike stories: `S-01` (cross-domain association pattern, program id
> `SPIKE-06b` — blocks `D-01`/`D-02`/`D-04`; draft ADR-011 descopes `D-03` (pure passthrough) and
> `D-06`/`D-07`/`D-11` (single-backend writes)), `S-02` (`getProducts` two-stage hydration research, program id
> `SPIKE-06a`, blocks `C-01`), `S-03` (partner drop/undrop failure strategy, program id `SPIKE-03`
> — do this one first, blocks `E-01`; draft ADR-012).

> **Self-contained story model.** The Netflix-DGS-on-REST framework already exists, so **every operation story below is end-to-end in a single PR**: it adds the schema (query/mutation + the GraphQL type definitions it returns), the DGS data fetcher, the Kotlin REST service method (read or write) that calls the backend, and pushes the schema change to the **Hive** registry. There is **no separate service-layer story** — the former `*Service` Kotlin-port story has been dissolved into the operation stories. The `Categories` union `@DgsTypeResolver` (A-04) remains a dedicated story.

> **These are thin DGS wrappers — and why `B-01` is *not* in the Depends On column.** The domain **model**, the
> **REST controller (GET/POST/PUT)**, and the Kotlin **service** already exist; each story only adds the
> Netflix-DGS layer (a schema type + `@DgsQuery`/`@DgsMutation`/`@DgsData` + wiring) so the federated graph can
> stitch this subgraph. The **one-time DGS module scaffold** that `B-01` lands in its PR — `product.graphqls`,
> scalar registration in `ScalarConfig.kt`, service + Feign wiring — is a prerequisite for **every** operation
> story, so it is **assumed once (shown in the graph below) and not repeated in each row's `Depends On`**. Rows
> list only **genuine story-to-story dependencies** (a spike, or a story another story truly builds on).
> Example: **`D-08 removeProductResources`** is a one-line wrapper over the existing REST `DELETE`/`PUT`, so its
> `Depends On` is **—**. Once `B-01` lands the scaffold, all of B, C, D and G run **fully in parallel**.

## 2. Dependency Graph
```mermaid
graph TD
  S01[S-01 cross-domain association spike] --> D01 & D02 & D04
  S02[S-02 getProducts hydration spike] --> C01[C-01 getProducts]
  S03[S-03 partner drop/undrop failure-strategy spike] --> E01[E-01 partnerActions]
  B01["B-01 getProduct + one-time DGS module scaffold\n(product.graphqls, scalars, service + Feign wiring)"]-->B[B Reads]&C[C Search]&D[D Mutations]&G[G Field resolvers]
  D-->E01 & E02[E-02 componentStatuses]
  B01-->E03[E-03 TechPack facade]-->E04[E-04 TechPack bulk]
  E03-->H01[H-01-H-05 subgraph federation]-->F09[F-09 retire facade]
  B01-->H06[H-06 Product entity fetcher]
  F14[F-14 contract alignment: keys/names/paged wrappers]-->F10[F-10 Hive composition]
  H06-->F10
  F09-->F10
```

> **F-13/F-14 added by the federation review (2026-07-17):** `F-14` is a schema-only fix with no
> in-graph predecessor; `F-13` only needs the `B-01` scaffold (it reuses the `getProduct` service path).
> Both must land before `F-10` (Hive composition) — see `F-10`'s own `Depends on` line.

> **Reading the graph:** an arrow from `B-01` means *"needs the DGS module scaffold that B-01 lands"* (the
> schema file, scalar registration, and service/Feign wiring) — **not** a dependency on `getProduct`'s logic.
> This scaffold prerequisite is shown **once here** and is deliberately **not** duplicated in each story's
> `Depends On`. Because the model + REST (GET/POST/PUT) + service already exist, every B/C/D/G story is a thin
> DGS wrapper, so they are **mutually independent and parallelizable** the moment the scaffold exists.

---

## 3. Stories

### Phase 0 — Spikes

> A spike is time-boxed research, not shipped code. It ends in a recorded decision that
> gets written back into the story it blocks.

---

### PRODUCT-BE-S-01 · Cross-domain association pattern spike
- **Type:** Spike · **Phase:** S · **Complexity:** Medium · **Category:** CAT-1 · **Depends on:** — · **Blocks:** D-01, D-02, D-04 *(D-03/D-06/D-07/D-11 descoped — see below)*
- **Status:** 🟠 Draft ADR-011 proposed (`complexStories/cross-domain-association/01-adr-cross-domain-association.md`) — ratification pending

- **Layman summary:** `Product` doesn't live alone — creating or updating a product often also has to create
- links to *other* domains: attach files (`attachment`), put the product in a workspace, add teams, add business partners.
- Today that "and also link X" logic is scattered across several mutations, each doing its own version of "create/update the product, then separately call out to link it." The spike's job is to agree on **one pattern** for how a product mutation builds these cross-domain associations, so `D-01`/`D-02`/`D-04` follow it consistently instead of ad-hoc approaches.
- **Scope note (per draft ADR-011 §1):** the resolver-source analysis shows `D-03` is a pure passthrough (no cross-domain call) and `D-06`/`D-07`/`D-11` ("Collab Canvas") are association *semantics* on a **single backend** — all their endpoints are on the product service, no sibling service is called. They are the documented exception (AC-3) and are **not gated** on this spike.

- **What's unknown:**
1. Should association-building be inline in the product mutation (call the other domain's service directly,
   synchronously), or should it be event-driven (product mutation completes, then an async listener in the
   other domain reacts)?
2. What happens if the product write succeeds but the association call fails — is that acceptable (today it
   mostly is, undocumented), or does it need the same saga/compensation treatment as `updateBom`?
3. Whether the *same* pattern should also cover `D-06` (`addTeamsToProduct`), `D-07`
   (`addBusinessPartnersToProductWithType`), and `D-11` (`updateWorkspaceAttributes`) — these three are already
   flagged "Collab Canvas" because they're pure association mutations, not just product-mutations-that-also-associate.

- **Candidate patterns:**
| Option | What it means | Tradeoff |
|---|---|---|
| Synchronous direct call (today's pattern, formalized) | Product mutation calls the other domain's client inline, in the same request | Simple, consistent latency; a failure there fails (or partially fails) the whole mutation |
| Event-driven / async | Product mutation publishes "product created/updated"; attachment/workspace/team domains subscribe and react | Decouples product from knowing about every consumer; harder to give the caller a synchronous "did the link succeed" answer |
| Shared `AssociationService` used by all product mutations | One internal service with `link(productId, targetDomain, targetId)`, called synchronously by every mutation that needs it | Cheapest to adopt today (same sync behavior, less duplicated code); doesn't solve the "what if it fails" question by itself |

> **Prior art:** the teams↔domain association question has been researched before — this spike's scope is
> broader (attachments, workspace, partners too) but should stay consistent with the earlier teams decision.

- **Example:** `addProduct(sparkProduct, copyProduct: null)` today creates the product, then — inline, same
- request — calls the workspace-association endpoint if a `workspaceId` was passed.
- Under the "shared service" candidate pattern: `addProduct` would call `associationService.link(newProduct.id, "workspace", workspaceId)` instead of building that call itself — same behavior, shared code instead of five copies of it.

#### Acceptance Criteria

1. One pattern (from the candidates above, or a variant) is chosen and recorded here — draft ADR-011
   proposes **Option B**: synchronous in-subgraph orchestration through one shared association component,
   with per-mutation failure policy declared explicitly (ratification pending).
2. `D-01`/`D-02`/`D-04`'s Target DGS Implementation text is updated to reference the chosen pattern instead
   of each inventing its own approach.
3. `D-06`/`D-07`/`D-11` (Collab Canvas) are confirmed to fit the same pattern, or a documented exception is
   recorded for why they differ — **done in draft ADR-011 §4**: single-backend writes, plain
   `@DgsMutation`s, component not required; `D-03` likewise descoped as a pure passthrough.

---

### PRODUCT-BE-S-02 · `getProducts` two-stage hydration research spike
- **Type:** Spike · **Phase:** S · **Complexity:** High · **Category:** CAT-1 · **Depends on:** — · **Blocks:** C-01
- **Status:** ⬜ Not Started

- **Layman summary:** the product listing screen needs two kinds of information merged together: fields that
- live on the canonical product record (name, status, dates — from the product database) and fields that only exist in the search index (whether it has boms/claims/samples, workspace membership, computed flags).
- Today that merge is a two-step "ask elastic for ids + flags, then ask the product DB for the full records, then glue the flags onto the records" dance.
- The spike's job is to work out **how to apply workspace filters and pull the calculated fields from elastic, then correctly stitch that onto the canonical product data** — before `C-01` is implemented — because the two-stage shape is exactly where the two data sources can disagree (e.g. a product elastic thinks is in workspace W might have just been removed from W in the canonical store).

- **What's unknown:**
1. What happens when elastic and the canonical store disagree (elastic is eventually-consistent; the canonical
   product record is not) — does the caller see stale flags, or does `C-01` need a reconciliation step?
2. Whether workspace filtering should happen in the elastic query (stage 1) or after canonical hydration
   (stage 2) — filtering earlier is cheaper but risks filtering on stale workspace membership.
3. Whether the "calculated fields" (has-boms, has-claims, sample-due flags, etc.) can be computed once and
   cached, or must be recomputed per request.

- **Candidate patterns:**
| Option | What it means | Tradeoff |
|---|---|---|
| Filter in elastic, hydrate canonical after (today's shape) | Workspace/type filters run against the search index first; canonical DB only fetches the ids that survived | Cheap DB load; filter correctness depends on elastic's freshness |
| Filter after canonical hydration | Fetch broadly from elastic, hydrate all canonical records, then filter in application code | Filter is always correct against current canonical data; more DB load |
| Hybrid: cheap filters in elastic, precise filters after hydration | Split filter predicates by which source is authoritative for each one | Most correct, most code |

- **Example:** caller asks for `getProducts(resourceType: "workspaces", filter: [...])`. Stage 1 (elastic) returns
- `ids: [P1, P2, P3]` plus flags `{P1: {hasBoms: true}, ...}`.
- Stage 2 (canonical) fetches `P1, P2, P3` and merges the flags on.
- If `P2` was removed from the target workspace one second ago (canonical already reflects it, elastic hasn't caught up), should `P2` still appear in the result?
- That's the exact question this spike answers.

#### Acceptance Criteria

1. Workspace-filter placement (stage 1 vs stage 2 vs hybrid) is decided and recorded here.
2. The elastic/canonical staleness question (§What's unknown #1) has a documented answer — even if the answer
   is "accept the staleness window, document it."
3. `C-01`'s Target DGS Implementation and Acceptance Criteria are updated from the spike-framing placeholder to
   concrete behavior per the decision.

---

### PRODUCT-BE-S-03 · `productBusinessPartnerActions` failure-strategy spike (do this one first)
- **Type:** Spike · **Phase:** S · **Complexity:** Medium · **Category:** CAT-1 · **Depends on:** — · **Blocks:** E-01 · **Program id:** `SPIKE-03`
- **Status:** 🟠 Draft ADR-012 proposed (`complexStories/partner-drop-undrop-write/01-adr-partner-drop-undrop.md`) — ratification pending

- **Layman summary:** dropping or un-dropping a business partner from a product isn't one write — it's a
- dispatcher with 3 cases (remove / drop / undrop), each of which fans out to *several* cleanup services (recently-viewed, todo, favorites, sample evaluations).
- If one of those cleanup calls fails partway through, today there's no rollback and no record of what's now inconsistent.
- This is the same shape of problem as BOM's `updateBom` (see `BOM-BE-S-01`) — same candidate patterns apply — but the concrete steps are different (it's a fan-out to N cleanup services, not a fixed 3-step sequence), so it needs its own answer.
- **The reviewer marked this the first of the product spikes to run** — it blocks `E-01`, the single highest-risk mutation in the whole Product domain.

- **What's unknown:**
1. Which failure strategy fits a *fan-out* shape (potentially failing independently in any of 4-5 places)
   rather than BOM's fixed 3-step sequence — a straight saga may not translate directly.
2. Whether `REMOVE`/`DROP`/`UNDROP` need the *same* strategy, or whether (e.g.) `UNDROP` — which is already a
   corrective action — can be best-effort while `DROP` needs stronger guarantees.

- **Candidate patterns:** same three options as `BOM-BE-S-01` (saga w/ compensation, compensation-log +
reconcile, documented best-effort) — see that spike for the general tradeoffs. This spike's job is picking the
one that fits a fan-out (not sequential) shape.

> **Prior art:** [`../../complexStories/partner-drop-undrop-write/00-overview.md`](../../complexStories/partner-drop-undrop-write/00-overview.md)
> already designs this specific case, and the shared `WriteSaga` from
> [`../../complexStories/non-atomic-write-saga/00-overview.md`](../../complexStories/non-atomic-write-saga/00-overview.md)
> is built to support fan-out steps, not just sequential ones — this spike's job is largely to confirm that
> design fits and pick the per-cleanup-service compensation, not invent a new mechanism.

- **Example:** `productBusinessPartnerActions(action: DROP_PARTNER, partnerId: "BP42")` updates the partner
- status, then fans out to remove `BP42` from recently-viewed, todo, favorites, and sample evaluations.
- If the "favorites" cleanup call fails, today: partner status is already dropped, the other 3 cleanups already ran, favorites cleanup silently didn't happen, caller gets a 500 with no indication which of the 4 fan-out calls actually failed.

#### Acceptance Criteria

1. Failure strategy chosen and recorded here (may reuse the BOM `WriteSaga`/`WriteRegistry` shared infra).
2. Per-cleanup-service compensation (or log-and-reconcile action) is specified for each of the 4-5 fan-out
   targets, concretely enough for `E-01` to implement.
3. `E-01`'s Target DGS Implementation is updated with the concrete choice.

---

### Phase B — Core Reads (one query per story)

> Pattern: each story adds `@DgsQuery` + its `ProductReadService` method (calling the backend REST endpoint) + the returned GraphQL types + Hive schema push. Full pseudo-logic in [02 §Query Resolvers](./be-02-resolver-analysis.md). All depend on B-01 (module init).

---

### PRODUCT-BE-B-01 · `getProduct(id)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Looks up a single product by id (the core product read everything else builds on).

> **Note — DGS Module Init (this PR only):** Creates `product.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: [be-03-schema.graphql](./be-03-schema.graphql). **This scaffold is a prerequisite for every B/C/D/G story** — they need the module + schema file to compile their DGS wrapper — so it is assumed globally (shown once in the dependency graph) and **not repeated** in each story's `Depends On`. After it lands, the wrappers parallelize.
- **Current Behaviour (Q3):** `getByID.load(id)` `GET ${v1}?productId={id}` → camelCase or null; DataLoader-batched.
- **Target:** `@DgsQuery getProduct(id): Product` via `ProductDataLoader` keyed on id. 

#### Acceptance Criteria

1. returns product; 404→null.
2. batches N ids in 1 call.

---

### PRODUCT-BE-B-02 · `getProductsByIds(ids)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Looks up several products at once by their ids.

- **Current Behaviour (Q6):** `getByIdList.load(ids)` `GET ${v1}?productId={csv}&page=0&size=10000&sort=createdDate,desc`; primes `getByID`. **Target:** `@DgsQuery` → `ProductsPaged`. 

#### Acceptance Criteria

1. returns paged products for ids.
2. primes single-id loader.

---

### PRODUCT-BE-B-03 · `getProductStatus` (cacheable)
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Returns the list of possible product statuses (dropdown options).

- **Current Behaviour (Q7):** `getStatus.load()` master status list. **Target:** `@DgsQuery` → `@Cacheable` → `[MasterProductStatus]`. 

#### Acceptance Criteria

1. returns statuses.
2. cached.

---

### PRODUCT-BE-B-04 · `getProductVersions(id)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Lists the saved versions of a product.

- **Current Behaviour (Q10):** `getVersions.load({id})` `GET ${v1}/{id}/versions?page=0&size=10000`. **Target:** `@DgsQuery` → `ProductsPaged`. 

#### Acceptance Criteria

1. returns versions.

---

### PRODUCT-BE-B-05 · `getCopyStatus(id)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Tells you whether a product copy is still in progress or done.

- **Current Behaviour (Q4):** `getCopyStatus.load(id)` `GET ${v2}/count/resource-type?copyId={id}`. **Target:** `@DgsQuery` → `ProductCopy`. 

#### Acceptance Criteria

1. returns copy status.

---

### PRODUCT-BE-B-06 · `getProductTemplateById(id)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Looks up a product template by id.

- **Current Behaviour (Q18):** `getByID.load(id)` → `response || {}` (empty object on miss — **preserve**). **Target:** `@DgsQuery getProductTemplateById(id): Product`. 

#### Acceptance Criteria

1. returns product or empty object (not null).

---

### PRODUCT-BE-B-07 · `getProductRules`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Returns the product business rules.

- **Current Behaviour (Q12):** `getAllRules.load()` `GET ${base}/spark_rules/v1` → `content`. **Target:** `@DgsQuery` → `[ProductRules]`. 

#### Acceptance Criteria

1. returns rules content.

---

### PRODUCT-BE-B-08 · `getProductRulesById(id)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Looks up one business rule by id.

- **Current Behaviour (Q13):** `getRuleById.load(id)` `GET ${base}/spark_rules/v1/{id}`. **Target:** `@DgsQuery` → `ProductRules`. 

#### Acceptance Criteria

1. returns rule.

---

### PRODUCT-BE-B-09 · `getAllAvailableRules`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Lists all the rules that are available to apply.

- **Current Behaviour (Q14):** `getAvailableRules.load()` `GET …/spark_rules/v1/rules`. **Target:** `@DgsQuery` → `[AvailableRules]`. 

#### Acceptance Criteria

1. returns available rules.

---

### PRODUCT-BE-B-10 · `getProductDeptRules(productIds, departmentIds, activeOnly)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `ruleLibrary`

- **In plain terms:** Returns the department-level rules for given products.

- **Current Behaviour (Q15):** **flag fork** `USE_NEW_RULES_API ? ruleLibrary.searchRuleLibrary : product.searchProductDeptRules` `GET …/spark_rules/v1/search?productIds=&departmentIds=&activeOnly=`. **PO decision:** flag cutover (rules may move to spark-tag DGS). **Target:** `@DgsQuery`; both code paths covered. 

#### Acceptance Criteria

1. default `activeOnly=true`.
2. flag selects the correct backend.

---

### PRODUCT-BE-B-11 · `getProductBPRules(productIds, businessPartnerIds, activeOnly)`
- **Type:** Query · **Phase:** B · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `ruleLibrary`

- **In plain terms:** Returns the business-partner-level rules for given products.

- **Current Behaviour (Q16):** same as B-10 with `businessPartnerIds`. **Target:** `@DgsQuery`. 

#### Acceptance Criteria

1. flag fork honored; BP filter applied.

---

### Phase C — Search & Listing

---

### PRODUCT-BE-C-01 · `getProducts(...)` two-stage hydration
- **Type:** Query · **Phase:** C · **Complexity:** High · **Category:** CAT-2 · **Depends on:** S-02 · **EXT:** 🔴 `search`

- **In plain terms:** List products by combining the search index with the canonical record (two-stage hydration).

- **As a** DGS engineer **I want** `getProducts` with elastic+canonical two-stage hydration **so that** listing
returns canonical records enriched with elastic flags.
- **Current Behaviour, in plain terms:** listing products needs data from two places — the search index (which
- knows flags like "has boms", "has claims", workspace membership) and the canonical product database (the actual product fields).
- Today's code asks the search index first for matching ids + flags, then asks the product database for the full records, then glues the flags onto the records.
- (🔴 search) `getFilteredProductsListing({resourceType ?? 'products', includeBoms ?? true, includeClaims ?? true, includeMeasurementSets ?? true, includeProductDetails ?? true, filter ?? [], q ?? '', page, size})` → ids → (internal) `getPage({products:ids, page:0, size})` `GET ${v1}?productId=&sort=createdDate,desc` → merge elastic flags (`boms, productDetails, claims, measurementSets, samples, sampleIds, hasSamplesUpcomingDue, hasNotEvaluatedReceivedSamples, receivedNotEvaluatedCount`) onto canonical records.
- **Boolean defaults are truthy (`?? true`) — pin in tests.**
- **EXT:** 🔴 search. **Target: implement per `PRODUCT-BE-S-02`'s outcome.** That spike answers exactly how the
- workspace filter and elastic-vs-canonical staleness are handled — this story is the implementation, not the design.
- Until `S-02` concludes, the safe default is to preserve today's shape (`ProductElasticService.getFilteredProductsListing` then `ProductReadService.getPage`; merge) so this story isn't blocked on the spike's timeline.

#### Acceptance Criteria

1. parity for 4 arg combos (no flags / all flags / resourceType=workspaces / filter array).
2. truthy defaults preserved.
3. elastic flags merged onto canonical.
4. Workspace-filter placement and elastic/canonical staleness handling match `SPIKE-06a`'s decision.

#### Test Cases

- [ ] 4 combos
- [ ] default truthiness
- [ ] merge
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### PRODUCT-BE-C-02 · `getProductTemplates(...)`
- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔴 `search`

- **In plain terms:** Lists product templates, with optional filters on what to include.

- **Current Behaviour (Q2):** (🔴 search) `getFilteredProductsListing({resourceType:'product', includeBoms:false, ...7 includeXxxTemplates flags, types})` → return elastic response (no 2nd hydration). **Target:** `@DgsQuery` → `ProductTemplatesList`. 

#### Acceptance Criteria

1. all 7 template-include flags forwarded.
2. `types:[Int]` filter applied.

---

### PRODUCT-BE-C-03 · `getCategories(...)`
- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔴 `search`

- **In plain terms:** Returns the category tree for products.

- **Current Behaviour (Q5):** default `productType ?? 100`; (🔴 search) `getProductCategories` `GET ${elastic}/search/${snake_case(type)}?resourceType=&resourceId=&productType=` → `ProductsCategories` (polymorphic `categories` via A-04). **Target:** `@DgsQuery`; preserve `snakeCase(type)` in the path. 

#### Acceptance Criteria

1. `snake_case(type)` path exact.
2. wires to `Categories` union.

---

### PRODUCT-BE-C-04 · `getRatingByTcin(tcin)` (external rating)
- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `rating`

- **In plain terms:** Gets the customer rating for a product (from an external ratings service).

- **Current Behaviour (Q11):** (🔵 external) `GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={API_KEY}` (`skipJsonParse`) → `JSON.parse` → `{averageRating, reviewCount}`; **catch → null** (silent). **Target:** `RatingClient` Feign (text/plain, manual parse); secret from Vault. 

#### Acceptance Criteria

1. parses statistics to `Rating`.
2. any error → null.
3. API key from config/Vault, not source.

---

### PRODUCT-BE-C-05 · `searchProductRules(...)`
- **Type:** Query · **Phase:** C · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `ruleLibrary`

- **In plain terms:** Searches product rules.

- **Current Behaviour (Q17):** flag fork; legacy `GET …/spark_rules/v1/search_mapped?...` → `productRuleResponseTransformer` → camelCase. **Target:** `@DgsQuery`; port the transformer. 

#### Acceptance Criteria

1. flag fork honored.
2. legacy response transformed correctly.

---

### Phase D — Mutations (simple, one per story)

> Pattern: each story adds `@DgsMutation` + its `ProductWriteService` method (calling the backend REST endpoint) + the input/payload types + Hive schema push. Pseudo-logic in [02 §Mutation Resolvers](./be-02-resolver-analysis.md). All depend on B-01. ACL is context-only.

---

### PRODUCT-BE-D-01 · `addProduct`
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** S-01 · **EXT:** 🔴 `workspaceV2` · 🔴 `attachment`

- **In plain terms:** Create a product (optionally copy from another + associate a workspace).

- **Current Behaviour (M1):** `POST ${v1}` + optional `copyProductToProduct(copyProduct)` + workspace association. **Target:** `@DgsMutation addProduct(workspaceId, sparkProduct, copyProduct): Product`; orchestrate create→copy→assoc **per `PRODUCT-BE-S-01`'s chosen cross-domain association pattern** (draft ADR-011 Option B: shared association component, sync, service-to-service REST). 

#### Acceptance Criteria

1. creates product.
2. optional copy runs when `copyProduct` present.
3. workspace assoc applied via the shared association component (no bespoke fan-out code).
4. failure after create (link or copy fails) surfaces per the mutation's declared failure policy — default fail-fast, no rollback, documented (ADR-011 §4).

---

### PRODUCT-BE-D-02 · `addProducts` (bulk)
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** S-01 · **EXT:** 🔴 `attachment`

- **In plain terms:** Create many products at once (plus attachment links).

- **Current Behaviour (M2):** bulk `POST ${v1}/bulk` + attachment-link side-effects (no rollback — **preserve, flag**). **Target:** `@DgsMutation` → `ProductBulkType`; attachment linking follows `PRODUCT-BE-S-01`'s pattern (draft ADR-011: the `bulkUpdateAttachmentsV2` cross-resolver import becomes an attachment-service client call inside the component; the unawaited `bulkUpdateResource` becomes awaited — both accepted deviations, ADR-011 §4 pin-downs 1/3). 

#### Acceptance Criteria

1. bulk creates.
2. attachment links applied via the shared association component; no-rollback behaviour documented (compensation deferred to the shared `WriteSaga` module, `PRODUCT-BE-E-00`, per ADR-011 pin-down 2).
3. no resolver import remains; the formerly fire-and-forget attachment re-point is awaited and its failure visible (accepted deviations per ADR-011 §4).

---

### PRODUCT-BE-D-03 · `bulkUpdateProducts`
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Update many products in one call.

> **Not gated on `PRODUCT-BE-S-01`** (draft ADR-011 §1): the resolver is a pure passthrough — no
> cross-domain call; "cross-domain" only in that the DTO can carry association-ish fields the backend fans out.

- **Current Behaviour (M3):** `PUT ${v1}/mass_update`. **Target:** `@DgsMutation` → `ProductBulkType`. 

#### Acceptance Criteria

1. mass-updates products.

---

### PRODUCT-BE-D-04 · `updateProduct`
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** S-01 · **EXT:** 🔴 `attachment`

- **In plain terms:** Edit a product (optional copy + template-attachment cleanup).

- **Current Behaviour (M4):** `PUT ${v1}/{id}` + optional copy + archive removed-template attachments (template branch). **Target:** `@DgsMutation updateProduct(input, copyProduct): Product`; attachment archiving follows `PRODUCT-BE-S-01`'s pattern (draft ADR-011 Option B: shared association component, per-mutation declared failure policy). 

#### Acceptance Criteria

1. updates product.
2. optional copy.
3. removed-template attachments archived (template branch).
4. attachment archiving applied via the shared association component (no bespoke fan-out code).

---

### PRODUCT-BE-D-05 · `carryForwardProduct`
- **Type:** Mutation · **Phase:** D · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Carries a product forward (creates the next season/version from it).

- **Current Behaviour (M5):** `PUT ${v1}/{productId}/carry_forward/{workspaceId}` — uses **every** field on `CarryForwardProductInput`. **Target:** `@DgsMutation`; verify full input mapping. 

#### Acceptance Criteria

1. all input fields mapped to the request.

---

### PRODUCT-BE-D-06 · `addTeamsToProduct` 🔀 Collab Canvas
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Adds teams (and their partners) to a product.

> **Collab Canvas — not gated on `PRODUCT-BE-S-01`** (draft ADR-011 §1/§4, the documented exception):
> association *semantics*, but all 3 endpoints (`partners-add/bulk`, `resources/bulk`,
> `manage_workspace_teams`) are on the **product backend** — no sibling service is called, so no
> cross-subgraph pattern applies. Plain `@DgsMutation`; the association component is not required.

- **Current Behaviour (M6):** `POST ${v1}/{productId}/resources/bulk` + manage_workspace_teams. **Target:** plain `@DgsMutation` (single-backend write). 

#### Acceptance Criteria

1. adds teams + new partners + workspace links.
2. partner-add failure exits early with a thrown typed error (today `return new Error(...)` — standardized per ADR-011 §4 pin-down 4, accepted deviation); teams are not added after a failed partner add (legacy order preserved).

---

### PRODUCT-BE-D-07 · `addBusinessPartnersToProductWithType` 🔀 Collab Canvas
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Adds business partners to a product with a given type.

> **Collab Canvas — not gated on `PRODUCT-BE-S-01`** (draft ADR-011 §1/§4, same exception as `D-06`):
> single write to the product backend (`partners-add/bulk`); no sibling service called. Plain `@DgsMutation`.

- **Current Behaviour (M7):** `POST ${v1}/{productId}/partners-add/bulk`; success = response has `product_id` and no `status_code`; failure = log + `return new Error(...)` (returned, not thrown — surfaces as a field error). **Target:** plain `@DgsMutation`. 

#### Acceptance Criteria

1. adds partners with type.
2. failure throws a typed `DgsException` instead of `return new Error(...)` (accepted parity deviation, ADR-011 §4 pin-down 4).

---

### PRODUCT-BE-D-08 · `removeProductResources`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Removes resources (links) from a product.

- **Current Behaviour (M8):** `DELETE ${v1}/{productId}/resources/bulk`. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. removes resources.

---

### PRODUCT-BE-D-09 · `updateBusinessPartnerStatuses`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Updates the status of business partners on a product.

- **Current Behaviour (M9):** `PUT ${v1}/{productId}/status_update/bulk`. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. updates partner statuses.

---

### PRODUCT-BE-D-10 · `updateViewToggle`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Toggles whether a product is hidden.

- **Current Behaviour (M11):** `PUT ${v1}` view toggle. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. toggles hidden.

---

### PRODUCT-BE-D-11 · `updateWorkspaceAttributes` 🔀 Collab Canvas
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Updates a product's workspace attributes.

> **Collab Canvas — not gated on `PRODUCT-BE-S-01`** (draft ADR-011 §1/§4, same exception as `D-06`/`D-07`):
> per-workspace attributes live **on the product record** (`PUT ${v1}/{productId}/workspaceAttributes/{humanId}`);
> the workspace service is never called. Plain `@DgsMutation`.

- **Current Behaviour (M12):** `PUT ${v1}/{productId}` workspace attrs. **Target:** plain `@DgsMutation` (single-backend write). 

#### Acceptance Criteria

1. updates workspace attrs.

---

### PRODUCT-BE-D-12 · `updateProductTeamsWorkspaceContext`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Adds or removes team↔workspace pairings on a product.

- **Current Behaviour (M13):** `PUT` team-workspace add/remove. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. adds/removes team-workspace pairs.

---

### PRODUCT-BE-D-13 · `linkProduct`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Links a parent and child product together.

- **Current Behaviour (M14):** `PUT` link — **throws on backend error** (only mutation that does). **Target:** `@DgsMutation`; port `throwOnError` as a checked exception. 

#### Acceptance Criteria

1. links parent/child.
2. backend error → exception (not null).

---

### PRODUCT-BE-D-14 · `unlinkProduct`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Unlinks a parent and child product.

- **Current Behaviour (M15):** `PUT` unlink. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. unlinks parent/child.

---

### PRODUCT-BE-D-15 · `addProductRule`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Creates a product rule.

- **Current Behaviour (M16):** `POST …/spark_rules/v1`. **Target:** `@DgsMutation` → `ProductRules`. 

#### Acceptance Criteria

1. creates rule.

---

### PRODUCT-BE-D-16 · `updateProductRule`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Updates a product rule.

- **Current Behaviour (M17):** `PUT …/spark_rules/v1/{id}`. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. updates rule.

---

### PRODUCT-BE-D-17 · `deleteProductRule`
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Deletes a product rule.

- **Current Behaviour (M18):** `DELETE …/spark_rules/v1/{id}` → Boolean. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. deletes; returns Boolean.

---

### PRODUCT-BE-D-18 · `updateComponentStatus` (bulk)
- **Type:** Mutation · **Phase:** D · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Bulk-updates the status of many components at once.

- **Current Behaviour (M19):** bulk `PUT ${v1}/component_status_update/bulk`. **Target:** `@DgsMutation`. 

#### Acceptance Criteria

1. bulk-updates component statuses.

---

### Phase E — Complex Operations

---

### PRODUCT-BE-E-00 · `WriteSaga` shared module (Sprint 0, critical path)
- **Type:** Service · **Phase:** E · **Complexity:** High · **Category:** CAT-3 · **Depends on:** — · **Blocks:** E-01, E-02, and every other domain's E-phase multi-step write story

- **In plain terms:** Build the one shared "ordered steps + per-step failure policy" mechanism every multi-step write in the program will use, instead of nine domains each guessing their own.

- **As a** DGS migration engineer **I want** one shared `WriteSaga` module **so that** every multi-step mutation
gets ordered execution, a declared per-step failure policy, and a visible result — instead of a bespoke,
undocumented guess per mutation.

- **Current Behaviour, in plain terms:** today, nine different multi-step "save" mutations across seven domains
(`updateBom`, `updateMeasurement`, `updatePackaging`, `updateProductDetailsSet`, `updateWatchlistEntries`,
`updateClaim`, `updateComponentStatuses`, plus the later-phase sample mutations) each hand-roll their own
ordering and failure handling — none of them roll back, most don't even check every step's response, and one
has an unawaited race. There is no shared answer to "step 2 failed, what happens to step 1's already-committed
change?" — see [ADR-013 §1-§2](../../complexStories/non-atomic-write-saga/01-adr-non-atomic-write-saga.md) for
the full write-by-write inventory and the write-operations grid.
- **Pattern (draft ADR-013 Option B, pending ratification):** one shared `WriteSaga` module, living in
`plm-product`, reused by every subgraph. Ordered steps, each declaring an `action` + a `policy` —
`COMPENSATE(inverse)` (an inverse call exists and is cheap — workspace associate/dissociate, relationship
add/remove) · `RETRY(n)` then `PARTIAL_FAILURE` (ACL/permissions writes after the body) · `RECORD` + reconcile
(destructive steps with no reliable inverse, e.g. attachment archive/attrs — the Mid-Request ACL Update call
for those downstream-token sites rides inside the attachment-client call itself, it is not a separate saga
step). The body PUT (the primary write) is the point of no return: fail there, stop, and compensate whatever
already committed. Parallel fan-out branches (e.g. `updateComponentStatuses`) are isolated per branch with an
aggregated result, never a bare `Promise.all` first-rejection-wins. See
[ADR-013 §4 Option B](../../complexStories/non-atomic-write-saga/01-adr-non-atomic-write-saga.md) for the full
default policy table and the `updateBom` step-3-failure sequence diagram.

- **Example (the module's shape, from ADR-013 §4):**
```kotlin
class WriteSaga {
  fun <T> step(name: String, action: () -> T, compensation: (() -> Unit)? = null, policy: StepPolicy = StepPolicy.RECORD)
  fun finish(): SagaResult   // COMMITTED | COMPENSATED | PARTIAL_FAILURE, with per-step detail
}

// a consumer (e.g. updateBom, PRODUCT-BE-... / BOM-BE-E-01) declares its steps against the shared module:
saga.step("workspace-assoc", { workspaceAssocHelper.associate(...) }, { workspaceAssocHelper.dissociate(...) }, COMPENSATE)
saga.step("body", { bomService.updateBom(input) }, policy = POINT_OF_NO_RETURN)
saga.step("permissions", { bomService.updatePermissions(jwt) }, policy = RETRY_THEN_PARTIAL_FAILURE)
val result = saga.finish()
```

- **Files to Create:** `plm-product/.../saga/WriteSaga.kt`, `plm-product/.../saga/StepPolicy.kt`,
`plm-product/.../saga/SagaResult.kt` — the module and its policy table only; no consumer wiring in this story.

#### Acceptance Criteria

1. `WriteSaga` executes ordered steps, stops at the first non-retryable failure, and runs declared
   compensations (in reverse order) for every already-completed step that has one.
2. Every step's response is checked by construction — there is no code path where a step's result is silently
   ignored (closes ADR-013 pin-down 5).
3. `finish()` returns `COMMITTED` (all steps succeeded), `COMPENSATED` (a step failed, compensations ran, no
   net change), or `PARTIAL_FAILURE` (a step failed, some compensations don't exist or also failed) — always
   with per-step detail, never a bare generic error (ADR-013 pin-down 6; surfaced via GraphQL error extensions
   by each consumer).
4. Parallel fan-out steps isolate per-branch failures and aggregate a per-branch result — a `Promise.all`-style
   first-rejection-wins is not possible through this API (ADR-013 pin-down 7).
5. Compensation inventory completed and recorded before any consumer story starts: for every step kind in the
   §4-B policy table, confirm the declared inverse actually exists (workspace associate↔dissociate,
   relationship add↔remove); anything without a confirmed inverse defaults to `RECORD`, never assumed
   (ADR-013 pin-down 1 — this is a blocking pre-condition on every consumer story, not optional polish).
6. Injected mid-sequence failures in unit tests yield `COMPENSATED` or `PARTIAL_FAILURE` with correct per-step
   detail for at least one `COMPENSATE`, one `RETRY`, and one `RECORD` step in the same saga run.
7. Zero consumer-facing API changes are needed if a later step kind's policy is refined (e.g. Option D's
   backend-composed atomic endpoints replace a saga step with one call) — the saga's public contract is
   step-name + action + compensation + policy, nothing consumer-specific leaks in.
8. This story ships alone — no domain's E-phase mutation story is modified here; `MST-BE-E-01`
   (`updateMeasurement`, the smallest real case) is the designated pilot adopter in its own story, followed by
   `BOM-BE-E-01`, `PKG-BE-E-01`, `PDTL-BE-E-01`, `WATCHLIST-BE-E-01`, `CLAIM-BE-E-01`, `PRODUCT-BE-E-02`, and the
   later-phase sample mutations, each per their own story's acceptance criteria.

#### Test Cases

- [ ] Unit: a 3-step saga where step 2 fails → step 1's compensation runs, step 3 never runs, result is `COMPENSATED`
- [ ] Unit: a step with `RETRY(n)` policy fails `n` times then still fails → result is `PARTIAL_FAILURE` with that step's detail
- [ ] Unit: a step with `RECORD` policy fails → saga continues past it (not a hard stop), failure recorded in per-step detail
- [ ] Unit: a step declares `COMPENSATE` but its own compensation call also fails → surfaced as `PARTIAL_FAILURE`, not silently swallowed
- [ ] Unit: a 5-branch parallel fan-out where 1 branch fails → the other 4 branches' results are still returned, aggregated
- [ ] Integration: compensation inventory checklist (pin-down 1) run and recorded against real backend endpoints before this story closes

---

### PRODUCT-BE-E-01 · `productBusinessPartnerActions` (REMOVE/DROP/UNDROP)
- **Type:** Mutation · **Phase:** E · **Complexity:** Very High · **Category:** CAT-2 · **Depends on:** S-03, E-00 · **EXT:** 🟡 `sampleV2` · 🔵 `recentlyViewed` · 🔵 `todo` · 🔵 `favorite`

- **In plain terms:** Remove / drop / undrop a business partner across a product — a ~220-line orchestrated write.

- **As a** DGS engineer **I want** the partner-action dispatcher with a failure strategy **so that** drop/undrop
stays consistent across cleanup services.
- **Current Behaviour, in plain terms:** removing, dropping, or un-dropping a business partner from a product
- isn't one write — it's a ~220-line dispatcher that updates the partner's status and then fans out to clean up that partner's traces in 4 other places (recently-viewed, todo list, favorites, sample evaluations), with no undo if one of those cleanup calls fails partway through. ~220-line dispatcher, 3 cases (`REMOVE_PARTNER`/`DROP_PARTNER`/`UNDROP_PARTNER`).
- Partner update + cleanup across `recentlyViewed`/`todo`/`favorite`/`sampleV2`/accessControl.
- No rollback.
- (ACL context.)
- **Target:** `ProductBusinessPartnerActionService` with 3 strategy methods, orchestrated via the shared
`WriteSaga` module built in `PRODUCT-BE-E-00`. **Failure strategy is whatever `PRODUCT-BE-S-03` concludes**
(the spike the reviewer asked to run first) for the fan-out-specific compensation choices; the underlying
saga mechanism itself is settled by ADR-013 (`PRODUCT-BE-E-00`).
- **Draft direction (pending ratification):** [ADR-012](../../complexStories/partner-drop-undrop-write/01-adr-partner-drop-undrop.md)
proposes Option B — the resource owner (`plm-product`) orchestrates via the shared `WriteSaga` (`PRODUCT-BE-E-00`)
over a per-domain participant contract; **security ordering constraint:** on drop, the ACL bulk-drop must
complete before the mutation returns success (testable invariant, ADR-012 §4).

- **Pseudocode (shape only — the exact fan-out compensation depends on `S-03`'s answer):**
```kotlin
class ProductBusinessPartnerActionService(private val saga: WriteSaga) {

  fun execute(action: PartnerAction, productId: String, partnerId: String): Product {
    saga.step("partner-status-update",
      { restClient.updatePartnerStatus(productId, partnerId, action) },
      { restClient.updatePartnerStatus(productId, partnerId, action.inverse()) }  // compensation, if S-03 picks saga
    )

    // fan-out cleanup — each is its own saga step so one failing doesn't silently skip the rest
    listOf(recentlyViewedClient, todoClient, favoriteClient, sampleV2Client).forEach { cleanupClient ->
      saga.step("cleanup-${cleanupClient.name}",
        { cleanupClient.removeReferencesTo(partnerId, productId) },
        { /* compensation or log+reconcile — per S-03 */ }
      )
    }

    val result = saga.finish()   // COMMITTED | COMPENSATED | PARTIAL_FAILURE (with per-step detail)
    return result.product
  }
}
```

#### Acceptance Criteria

1. all 3 paths reach REST parity (recorded fixtures), incl. the design-partner branch (`skipSamples` when `partnerType == DESIGN_PARTNER`).
2. partial-failure compensation log/strategy implemented per `SPIKE-03`'s decision (draft ADR-012: per-step policy — partner-status compensate · ACL retry-then-fail · activity/profile retry+reconcile).
3. cleanup fan-out runs per case, with per-target failure isolation (one cleanup failing is visible and
   doesn't silently swallow the others).
4. on DROP, ACL revocation completes **before** the mutation returns success; on UNDROP, ACL restore precedes participant undrops — proven by an automated test, not convention (ADR-012 §4 ordering constraint).
5. no Relationship-Service traversal and no `UserProfileAttributes` resolver import remain in the ported flow (replaced by participant enumeration + a user-profile client call).

> **Note:** ADR-012 pin-down 4 (async-refinement scope — recentlyViewed/todo/favorite/user-profile only, never
> ACL or partner status) and pin-down 6 (keep the `actionType` dispatcher shape for phase-1 parity; splitting
> is a v2 API question) are scope/architecture statements, not independently testable behavior — no dedicated
> AC needed; honored by construction in the service shape above.

#### Test Cases

- [ ] REMOVE
- [ ] DROP
- [ ] UNDROP
- [ ] design-partner branch (samples skipped)
- [ ] partial-failure per step
- [ ] ACL-before-return ordering invariant
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### PRODUCT-BE-E-02 · `updateComponentStatuses` (5-loader fan-out)
- **Type:** Mutation · **Phase:** E · **Complexity:** High · **Category:** CAT-2 · **Depends on:** E-00 · **EXT:** 🟡 `claim`

- **In plain terms:** Update a product's component statuses, fanning out to 5 sibling loaders.

- **Current Behaviour, in plain terms:** updating component statuses fans out to 5 places in parallel (bom,
- measurement, productDetail, packaging — all internal — plus claim, external).
- The bug: a loop variable meant to be captured per-iteration is instead shared across iterations ("shadow-var bug"), so by the time the async callbacks run, they can all see the *last* loop value instead of their own — a classic closure-over-loop-variable mistake. parallel fan-out to `bom`/`measurement`/`productDetail`/`packaging` (internal) + `claim` (🟡 EXT).
- **Target:** `coroutineScope { launch {…} } ×5` with structured concurrency; claim via `ClaimClient`.
- Fix the shadow var.
- **Pattern (draft ADR-013, pending ratification):** parallel fan-out branches run as isolated `WriteSaga` steps (built in `PRODUCT-BE-E-00`) with an aggregated per-domain result (ADR-013 pin-down 7); the duplicated `claimIds` DTO bug and the void return are fixed as accepted deviations (pin-down 4).

- **Example (the bug, and the fix):**
```kotlin
// before (bug): all 5 launched coroutines can end up reading the same `loader` reference
for (loader in listOf(bomLoader, measurementLoader, productDetailLoader, packagingLoader, claimLoader)) {
  launch { loader.updateStatus(componentId, status) }   // `loader` here is not safely captured per-iteration
}

// after (fixed): structured concurrency with an explicit per-item bind
coroutineScope {
  listOf(bomLoader, measurementLoader, productDetailLoader, packagingLoader, claimLoader).map { loader ->
    async { runCatching { loader.updateStatus(componentId, status) } }   // each async captures its own `loader`
  }.awaitAll()
}
```

#### Acceptance Criteria

1. per-loader failures don't fail siblings.
2. shadow var fixed.
3. parity.

#### Test Cases

- [ ] 5-way fan-out
- [ ] partial failure isolation
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### PRODUCT-BE-E-03 · `getProductTechPackCountV1` stub + aggregation facade (facade-then-federate, Phase 1)
- **Type:** Query · **Phase:** E · **Complexity:** Very High · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔴 `attachment` · 🔴 `search`

- **In plain terms:** Build the TechPack panel's badge counts by aggregating across ~8 domains.

> **Direction already resolved — not an open Phase 0 item.** The "Node extract vs Kotlin aggregation" facade
> decision (previously Decision #1 in `be-04-po-summary.md`) has already concluded: **facade-then-federate** —
> ship a thin query over a temporary aggregation facade now, federate each piece to its owning domain later,
> retire the facade last (`F-09`). This is draft **ADR-015 Option B** (the pattern
> `techpack-migration-options.md` labels "Option D (hybrid)"); ADR ratification is pending. Research:
> [`../../complexStories/techpack/00-overview.md`](../../complexStories/techpack/00-overview.md) ·
> [`ADR-015 (draft)`](../../complexStories/techpack/01-adr-techpack.md).

- **As a** DGS engineer **I want** the TechPack query served by a thin stub over an aggregation facade **so that**
it works on day 1 while per-subgraph federation is sequenced.
- **Current Behaviour, in plain terms:** the TechPack panel shows badge counts (attachments, discussions,
- samples, boms, claims, etc.) for a product.
- Getting those counts today means walking the *entire* product relationship graph in memory, checking permissions node-by-node (serially — one call per node), and — if the product has a parent — doing the whole walk again for the parent.
- It's an 8-domain, ~200-line function doing work that really belongs to 8 different teams: the 14-step `getTechPackResourceCountMap` (relationship walk + ACL filter ×2, attachment hydration, 7 elastic slice queries — sequential today, critical-discussion→attachment join, packet filter, build `ResourcesCount`). 8 domains' data, but only 4 physical services called (relationship, ACL, attachment, elastic) — see [ADR-015 §1](../../complexStories/techpack/01-adr-techpack.md).
- See [02 §Helper](./be-02-resolver-analysis.md).
- **Target (facade-then-federate Phase 1, ADR-015 Option B):** `@DgsQuery getProductTechPackCountV1(...)` → `TechPackAggregatorClient.getCount(...)` (Feign to a facade extracted from `getTechPackResourceCountMap`, behavior-frozen except the pinned deviations in ADR-015 §4); `@DgsEntityFetcher(name="ResourcesCount")` rebuilds the entity from `_entities`. See [reference-federation-patterns.md §3](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

- **Example — the eventual target shape (each domain answers its own slice, no relationship-graph walk; see `H-01`-`H-05` + the co-located `F-04`/`F-06`/`F-08`):**
```graphql
# plm-product — defines the shell (the extend-type end-state, ADR-015 §3-B Phase 2/3; the facade in this story is the interim step)
type ProductTechPack @key(fields: "productId partnerId") {
  productId: ID!
  partnerId: ID!
}
# plm-attachment extends it directly with the fields it owns:
extend type ProductTechPack @key(fields: "productId partnerId") {
  productAttachments: [ID!]!  @requires(fields: "parentProductId")
}
```
- **This story's facade**, in the interim, answers all 11 `ResourcesCount` fields itself by calling into each
domain's existing REST/elastic endpoint — same external contract as the eventual federated version, so `H-01`-`H-05` (+ the co-located `F-04`/`F-06`/`F-08`)
can swap the facade out one domain at a time without a breaking schema change.

#### Acceptance Criteria

1. Returns a fully populated 11-field `ResourcesCount` from the facade for a valid `(productId, partnerId, workspaceContext, parentProductId)` input.
2. `@DgsEntityFetcher(name="ResourcesCount")` reconstructs the entity from key + context on an `_entities` query (federation-ready shell).
3. Recorded-fixture parity vs `spark-internal-graphql` for ≥ 5 pinned inputs, including: a product **with a parent** (double-walk), > 100 walked ids (chunked ACL), a 3D attachment, and a critical thread whose parent discussion is outside the walk — 100% field-value match modulo the ADR-015 §4 deviation list (parallelized elastic/ACL calls; counts unchanged).
4. Facade is observable: per-slice latency + error metrics and a health endpoint exist (they gate the `H-01`–`H-05` re-homings and the `F-09` retirement check).
5. Facade is behavior-frozen: deviations limited to ADR-015 §4 pin-downs; `CODEOWNERS` guard in place so new feature work lands in the owning domain's `F0x` story instead.

#### Test Cases

- [ ] facade call returns 11 populated fields
- [ ] entity fetcher via `_entities`
- [ ] parity ≥ 5 pinned inputs (incl. parent double-walk, >100 ids, 3D attachment, out-of-walk critical thread)
- [ ] per-slice metrics emitted
- [ ] Integration: full query via DGS test client returns expected shape

---

### PRODUCT-BE-E-04 · `getProductTechPackBulkCountV1` (bulk wrapper, ordering fix)
- **Type:** Query · **Phase:** E · **Complexity:** Very High · **Category:** CAT-2 · **Depends on:** E-03 · **EXT:** 🔴 `attachment` · 🔴 `search`

- **In plain terms:** Return TechPack counts for many products at once, in the caller's order.

- **Current Behaviour, in plain terms:** the bulk version runs all N single-product lookups concurrently and
- returns them in whatever order they happen to finish — **not** the order the caller asked for.
- If a caller requests `[P3, P1, P2]` and `P1` happens to resolve fastest, they get `[P1, P3, P2]` back with no way to tell which result is which without matching on id themselves.
- `Promise.all(bulk.map(getTechPackResourceCountMap))` — **latent ordering bug** (result order = completion order).
- **Target:** bulk facade endpoint; **return in input order** (key/sort by productId).

- **Example:**
```kotlin
// before (bug): Promise.all-style — result order is completion order, not input order
val results = inputs.map { async { facade.getCount(it) } }.awaitAll()  // order not guaranteed to match `inputs`

// after (fixed): key results by productId, then re-order to match input
val byProductId = inputs.map { async { it.productId to facade.getCount(it) } }.awaitAll().toMap()
val results = inputs.map { byProductId.getValue(it.productId) }        // now order == input order
```

#### Acceptance Criteria

1. `bulk(P1..Pn) == [single(P1)..single(Pn)]` in input order.
2. empty list → [].

#### Test Cases

- [ ] order preserved
- [ ] empty
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### Phase F — Federation & Stitching (TechPack federate + gateway + decisions)

---

> **Phase F/H — how `ResourcesCount` gets filled (read once, applies to H-01–H-05 + the co-located F-04/F-06/F-08).** `ResourcesCount` is the
> TechPack badge-count aggregate; it is **owned by `product`** in the `plm-product` subgraph, and each of its
> 11 fields is contributed by whichever domain owns that data. Two contribution mechanisms — and this is
> exactly where the **ship-on-green exception** lives:
>
> - 🔗 **Cross-subgraph federation** (`extend type ResourcesCount @key(fields:"productId partnerId")` +
>   `@DgsEntityFetcher`) — used when the owning data lives in a **separate DGS**. These **⛔ cannot ship until
>   that owning subgraph is deployed** → marked **BLOCKED-BY `<domain>`**. Stories: `H-01, H-02, H-03, H-04, H-05`.
> - 🏠 **Internal same-subgraph `@DgsData`** — used when the owning domain is **co-located in `plm-product`**
>   (bom/measurement/watchlist). No federation, no separate deploy → **✅ ships on green**. Stories: `F-04, F-06, F-08`.
>
> Ownership map: H-01 Attachment · H-02 Discussion · H-03 Sample · F-04 Measurement · H-04 Claim · F-06 BOM ·
> H-05 Construction · F-08 Watchlist. Federation-pattern reference: `scripts/reference-federation-patterns.md §0/§3`.

---

### PRODUCT-BE-F-04 · `ResourcesCount.measurementSets` (internal, from Measurement)
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** E-03

- **In plain terms:** Fills in the product's measurement-set count — answered in-process by the co-located Measurement code.

- 🏠 **Internal, same subgraph — ✅ ships on green** (no BLOCKED-BY).
- Measurement is co-located in `plm-product`, so this is a plain `@DgsData` on `ResourcesCount` calling `measurementService` directly — identical pattern to BOM's `BOM-BE-F-02` (`bomsCount`).
- No federation annotations, no separate deploy.

#### Acceptance Criteria

1. `measurementSets` resolves in-process; no gateway hop; parity vs facade.

---

### PRODUCT-BE-F-06 · `ResourcesCount.productBoms` + `packagingBoms` + `boms` (internal, from BOM)
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** E-03

- **In plain terms:** Fills in the product's BOM counts — answered in-process by the co-located BOM code.

🏠 **Internal, same subgraph — ✅ ships on green.** BOM is co-located in `plm-product`; these are plain
`@DgsData` fields calling `bomService` directly (implemented BOM-side as `BOM-BE-F-02`). No separate deploy.

#### Acceptance Criteria

1. `productBoms`/`packagingBoms`/`boms` resolve in-process; no gateway hop; parity vs facade.

---

### PRODUCT-BE-F-08 · `ResourcesCount.watchlists` (internal, from Watchlist)
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** E-03

- **In plain terms:** Fills in the product's watchlist count — answered in-process by the co-located Watchlist code.

🏠 **Internal, same subgraph — ✅ ships on green.** Watchlist is co-located in `plm-product`; plain `@DgsData`
calling `watchlistService` directly. No separate deploy.

#### Acceptance Criteria

1. `watchlists` resolves in-process; no gateway hop; parity vs facade.

---

### PRODUCT-BE-F-09 · Retire the TechPack aggregation facade
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** H-01, H-02, H-03, F-04, H-04, F-06, H-05, F-08

- **In plain terms:** Removes the temporary TechPack 'facade' once every count is served by its real owner.

- **Context:** this is the cleanup story once all 8 sibling domains have shipped their federated
`ResourcesCount` fields (`H-01`-`H-05` + the co-located `F-04`/`F-06`/`F-08`) — the temporary `E-03` facade is no longer needed for anything.
- **Target:** remove `TechPackAggregatorClient`; `TechPackDataFetcher` returns key+context only; decommission the facade.

- **Example:** before this story, `getProductTechPackCountV1` calls `TechPackAggregatorClient.getCount(...)` (the
facade). After: it returns only `ResourcesCount(productId, partnerId)` — the shell — and the gateway fans out
to `H-01`-`H-05`'s (+ the co-located `F-04`/`F-06`/`F-08`) federated resolvers for the 11 count fields, same as any other federated entity.

#### Acceptance Criteria

1. all 11 `ResourcesCount` fields resolve via federation.
2. facade health-check endpoint returns 404 (decommissioned).
3. no orphaned config (feature flags, Feign client beans, etc. referencing the retired facade).

---

### PRODUCT-BE-F-10 · Hive Gateway supergraph composition
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** H-06, F-14

- **In plain terms:** Composes all the subgraphs into one federated graph at the gateway.

- **Context:** before `plm-product` can serve any federated query, the Hive Gateway needs to know it exists and
successfully compose it into the supergraph alongside every other subgraph.
- **Target:** add `plm-product` subgraph URL; verify composition with VMM/IG/CORONA/Doppler stubs; smoke-test cross-subgraph query.

- **Example:** `hive compose --subgraph plm-product=https://plm-product.internal/graphql` succeeds with no
composition errors (no conflicting type definitions, no missing `@key` fields), then a smoke query like
`{ getProduct(id: "P1") { name businessPartners { name } } }` resolves cleanly across the `plm-product` +
VMM subgraphs.

#### Acceptance Criteria

1. supergraph composes.
2. cross-subgraph smoke test passes.
3. composition runs as a CI gate on every schema change (not a one-off) and fails on any `@key`/type-name mismatch between subgraphs (regression guard for federation-review/03 §R1–R5).
4. zero remaining contract mismatches: `VMM_BusinessPartner`/`VMM_Brand` keyed `id`; every entity keyed `id` (Claims/Packaging/Watchlist/Dieline synthesize `id` from humanId — program decision 2026-07-17); `ProductDetails`/`MeasurementPaged` names aligned.

---

### PRODUCT-BE-F-11 · Platform stub verification (VMM/IG/Doppler/CORONA/APEX)
- **Type:** Field Resolver · **Phase:** F · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** F-10

- **In plain terms:** Verifies each external platform (VMM, IG, etc.) resolves through its stub.

- **Context:** `plm-product` emits `@key` stubs (e.g. a bare `VMM_BusinessPartner{id}`) for platform types it
references but doesn't own; this story confirms the gateway can actually resolve the *full* object from that
stub via the owning platform subgraph.
- **Target:** confirm the gateway resolves full platform types from product-emitted `@key` stubs.

- **Example:** `Product.businessPartners` returns `[VMM_BusinessPartner{id: "BP1"}]` as a stub from `plm-product`;
querying `{ businessPartners { id name } }` should come back with `name` populated by VMM's subgraph, not `null`.

#### Acceptance Criteria

1. each platform type resolves via its stub key.

---

### PRODUCT-BE-F-12 · Deferred partner-wrapper decision (drift mutations)
- **Type:** Schema · **Phase:** F · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** E-01

- **In plain terms:** Decide the fate of three drift partner mutations that have no resolvers.

- **Current Behaviour, in plain terms:** three old mutation names (`removeProductBusinessPartner`,
- `dropProductBusinessPartner`, `unDropProductBusinessPartner`) still exist in the schema, but nothing calls them anymore — all real traffic already goes through the newer `productBusinessPartnerActions` dispatcher (`E-01`).
- They're schema drift: dead surface area nobody has cleaned up.
- **Target:** PO decides delete vs keep `@deprecated`; implement.

- **Example:** a traffic survey (checking gateway request logs for these 3 mutation names over, say, the last
- 90 days) shows zero calls → PO decides to delete them outright.
- If the survey instead finds a stray internal tool still calling `dropProductBusinessPartner` directly, PO may choose `@deprecated(reason: "use productBusinessPartnerActions")` instead, giving that caller time to migrate before actual removal.

#### Acceptance Criteria

1. traffic survey complete.
2. decision implemented.

---

### PRODUCT-BE-F-14 · Cross-subgraph contract alignment (keys, type names, paged wrappers)
- **Type:** Schema · **Phase:** F · **Complexity:** Low · **Category:** CAT-4 · **Depends on:** — · **EXT:** —

- **In plain terms:** Fixes the naming/key mismatches between product's stubs and the owning schemas so the supergraph can actually compose.

- **Context (federation-review/03 §1):** the schema files have been aligned already; this story carries the
verification + the remaining declaration work into the DGS implementation:
  - `VMM_BusinessPartner` / `VMM_Brand` stubs keyed `id` (source SDL has `id`, not `bpId`/`brandId`) — R1/R2.
  - `Claim` → `Claims` (owner: spark-claims) — R3. **Key = `id`** per the program decision (2026-07-17):
    humanId-only entities (Claims, Packaging, Watchlist, Dieline) synthesize `id` from humanId — the
    Measurement pattern — so all stitching happens uniformly on `id`.
  - `ProductDetail` → `ProductDetails`; `MeasurementsPaged` → `MeasurementPaged` — R4.
  - `ProductComponentStatus` marked `@shareable` (claims duplicates it as a value type) — R5.
  - ✅ Declared the cross-subgraph paged wrappers product references but never defined (`TeamPaged`,
    `TeamPagedV2`, `WorkspacesPagedV2`, `DiscussionElastic`) as `@shareable` placeholder value types
    sized to today's field usage; `TeamPaged` is duplicated field-for-field in claims'
    `be-03-schema.graphql` (R5) — both must stay in sync until the team subgraph (phase 2) becomes the
    single owner and retires both duplicates.
  - `CORONA_ItemDetails` — ✅ decided (2026-07-17): stays an entity keyed `tcinId`; where a tcin exists the
    record carries `tcinId` and Corona inflates the item details from that key via the gateway.

#### Acceptance Criteria

1. `plm-product` schema compiles standalone with every referenced type declared (including `TeamPaged`, `TeamPagedV2`, `WorkspacesPagedV2`, `DiscussionElastic`).
2. `hive compose` over plm-product + spark-claims + platform stubs reports zero key/name conflicts, including zero `@shareable` field-shape conflicts on `TeamPaged` (must match claims' declaration exactly).
3. `CORONA_ItemDetails` entity form implemented per the 2026-07-17 decision (keyed `tcinId`; Corona inflates via the gateway).
4. Blocks released: F-10, CLAIM-BE-H-01, CLAIM-BE-H-02.

---

### Phase H — Entity Resolution (cross-domain @key)

---

### PRODUCT-BE-H-01 · `ResourcesCount.productAttachments` + `discussionAttachments` (federated, from Attachment)
- **Type:** Field Resolver · **Phase:** H · **Complexity:** Medium · **Category:** CAT-4 · **Depends on:** E-03 · **Blocked by:** attachment domain (⛔ cross-subgraph — does not ship until `plm-attachment` is live)

- **In plain terms:** Contribute attachment counts to the product's TechPack rollup (from Attachment).

- **Current Behaviour, in plain terms:** today the TechPack facade computes these two attachment counts itself
by walking the product's relationship graph. Once `plm-attachment` is federated, **Attachment** answers these
fields directly against its own store, filtered by partner — no graph walk, no serial ACL.

- **Example — the federated shape (this is the representative case; `H-02`/`H-03`/`H-04`/`H-05` are identical in
shape, just a different owning subgraph + field name):**
```graphql
# plm-attachment — owns productAttachments/discussionAttachments, extends the shell product defines
extend type ResourcesCount @key(fields: "productId partnerId") {
  productAttachments: [ID!]!    @requires(fields: "parentProductId")
  discussionAttachments: [ID!]! @requires(fields: "parentProductId")
}
```
```kotlin
// plm-attachment implements the entity fetcher + the field resolvers directly against its own store
@DgsEntityFetcher(name = "ResourcesCount")
fun resourcesCount(values: Map<String, Any>): ResourcesCount =
  ResourcesCount(productId = values["productId"] as String, partnerId = values["partnerId"] as String)

@DgsData(parentType = "ResourcesCount", field = "productAttachments")
fun productAttachments(dfe: DgsDataFetchingEnvironment): List<String> {
  val rc = dfe.getSource<ResourcesCount>()
  return attachmentService.getIdsByProductAndPartner(rc.productId, rc.partnerId)   // no relationship-graph walk
}
```

#### Acceptance Criteria

1. `productAttachments`/`discussionAttachments` resolve on the federated `ResourcesCount`; the `E-03` facade stops populating them.
2. Parity vs the facade for the same inputs.
3. Field is live in prod only after `plm-attachment` is deployed (ship gate honored).

---

### PRODUCT-BE-H-02 · `ResourcesCount.discussions` (federated, from Discussion)
- **Type:** Field Resolver · **Phase:** H · **Complexity:** Medium · **Category:** CAT-4 · **Depends on:** E-03 · **Blocked by:** discussion domain (⛔ cross-subgraph)

- **In plain terms:** Fills in the product's discussion count — answered by the Discussion service once it's live.

Same federated shape as `H-01`, owned by **Discussion** (`plm-discussion`). Full body lives in the discussion domain's stories.

#### Acceptance Criteria

1. `discussions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade.
2. Live in prod only after `plm-discussion` is deployed.

---

### PRODUCT-BE-H-03 · `ResourcesCount.sample` (federated, from Sample)
- **Type:** Field Resolver · **Phase:** H · **Complexity:** Medium · **Category:** CAT-4 · **Depends on:** E-03 · **Blocked by:** sample domain (⛔ cross-subgraph)

- **In plain terms:** Fills in the product's sample count — answered by the Sample service once it's live.

Same federated shape as `H-01`, owned by **Sample** (`plm-sample`).

#### Acceptance Criteria

1. `sample` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade.
2. Live in prod only after `plm-sample` is deployed.

---

### PRODUCT-BE-H-04 · `ResourcesCount.claims` (federated, from Claim)
- **Type:** Field Resolver · **Phase:** H · **Complexity:** Medium · **Category:** CAT-4 · **Depends on:** E-03 · **Blocked by:** claim domain (⛔ cross-subgraph)

- **In plain terms:** Fills in the product's claims count — answered by the Claims service once it's live.

Same federated shape as `H-01`, owned by **Claim** (`spark-claims`).

#### Acceptance Criteria

1. `claims` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade.
2. Live in prod only after `spark-claims` is deployed.

---

### PRODUCT-BE-H-05 · `ResourcesCount.constructions` (federated, from Construction)
- **Type:** Field Resolver · **Phase:** H · **Complexity:** Medium · **Category:** CAT-4 · **Depends on:** E-03 · **Blocked by:** construction domain (⛔ cross-subgraph)

- **In plain terms:** Fills in the product's construction count — answered by the Construction service once it's live.

Same federated shape as `H-01`, owned by **Construction**.

#### Acceptance Criteria

1. `constructions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade.
2. Live in prod only after the construction subgraph is deployed.

---

### PRODUCT-BE-H-06 · `Product` entity fetcher (`@DgsEntityFetcher`) for cross-subgraph references
- **Type:** Field Resolver · **Phase:** H · **Complexity:** Medium · **Category:** CAT-3 · **Depends on:** B-01 · **EXT:** —

- **In plain terms:** Lets *other* subgraphs (today: claims) turn a bare `Product{id}` reference into a full product through the gateway.

- **Context (federation-review/04 §4):** the claims subgraph is a **separate DGS** (`spark-claims`). Its
`Claims.product` field emits only a `Product` key stub; the Hive Gateway then calls `plm-product`'s
`_entities(representations: [{__typename: "Product", id: …}])` to hydrate it. DGS does **not** generate that
resolver automatically — without an explicit `@DgsEntityFetcher(name = "Product")`, `Claims.product` (and any
future external subgraph's product reference) resolves to `null`. `ResourcesCount` already has its entity
fetcher (TechPack story); `Product` itself had none.
- **Target DGS Implementation:** `@DgsEntityFetcher(name = "Product")` → `productService.getById(id)` behind a
`DataLoader` (one batched backend call per request, not per representation); null-tolerant (missing id → null
entry, no exception, per federation spec).
- **Files / Dependencies:** `ProductEntityFetcher.kt`; reuses the B-01 service path.

- **Example:**
```
POST /graphql  { _entities(representations: [{__typename:"Product", id:"PID1"}, {__typename:"Product", id:"PID2"}]) { ... on Product { id description } } }
→ one batched productService call → [Product{PID1}, Product{PID2}]
```

#### Acceptance Criteria

1. `_entities` resolves `Product` representations with a single batched backend call.
2. Unknown ids yield `null` entries without failing the whole `_entities` response.
3. End-to-end: a claims-subgraph query `{ getClaims { product { description } } }` hydrates through the gateway (pairs with CLAIM-BE-G-03).
4. No ACL plumbing introduced.

---

### Phase G — Field Resolvers, Bug-fixes, Utils, Tests (one story per group)

---

### PRODUCT-BE-G-01 · `Product.attachmentsWithMetaData`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Very High · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔴 `attachment` · 🟡 `relationship`

- **In plain terms:** Resolve a product's mixed attachments-with-metadata feed (files + discussions + samples).

- **Current Behaviour, in plain terms:** the attachments panel on a product shows a mixed feed — actual file
- attachments, plus discussions and samples that are *also* surfaced as if they were attachments (each with their own metadata), plus threaded replies — sorted together by type-priority then recency.
- Building that feed today is ~150 lines: walk the relationship graph to find related discussions/samples, fetch each category's data (v2 and v3 attachment APIs, batched discussion/thread/sample lookups), merge all 5 sources into one list, filter out drafts, then sort.
- `relationship.searchByIds` → 5-bucket partition → v2+v3 attachment hydration → discussions/threads/samples batched → 5-source merge → draft filter → `orderProductAttachments`.
- **Target:** `AttachmentEnrichmentService` Kotlin port; keep the "ACL should do draft filter" TODO as a follow-up.
- **Pattern (draft ADR-018, pending ratification):** owner-computed enrichment over one shared library with a per-surface policy table — this story builds the library + the product policy row; `G-03` becomes thin doors on it; the workspace phase adds its own policy row, not a redesign. Mandatory fixes ride the port as accepted deviations (parallel independent fetches, guarded thread→parent-discussion lookup, direct discussion client + batched replies). See [ADR-018 §4](../../complexStories/attachments-enrichment/01-adr-attachments-enrichment.md).

- **Pseudocode — the 5-source merge + ordering (the part parity tests actually check):**
```kotlin
class AttachmentEnrichmentService(
  private val relationshipClient: RelationshipClient,
  private val attachmentClient: AttachmentClient,   // v2 + v3
  private val discussionClient: DiscussionClient,
  private val sampleClient: SampleClient,
) {
  fun attachmentsWithMetaData(productId: String): List<AttachmentWithMetaData> {
    val related = relationshipClient.searchByIds(productId)          // 1 call, replaces N+1 graph walks
    val buckets = related.partitionByType()                          // 5 buckets: attachment/discussion/thread/sample/etc.

    val merged = listOf(
      attachmentClient.hydrateV2AndV3(buckets.attachments),
      discussionClient.batchGet(buckets.discussions),
      discussionClient.batchGetThreads(buckets.threads),
      sampleClient.batchGet(buckets.samples),
    ).flatten()
      .filterNot { it.isDraft }                                      // draft filter (ACL should eventually own this — tracked as follow-up)

    return merged.sortedWith(
      compareBy<AttachmentWithMetaData> { it.typeRank() }             // product=0, discussion=1, sample=2
        .thenByDescending { it.createdAt }                            // tiebreak: newest first
    )
  }
}
```

#### Acceptance Criteria

1. parity for mixed attachment/discussion/thread/sample.
2. ordering rank preserved (product=0, discussion=1, sample=2; createdAt DESC tiebreak).
3. product side hydrates both v2 and v3 attachment ids (no v2-ignoring gap) — the workspace-side v2-ignoring behaviour (ADR-018 pin-down 2) does not apply here; confirmed by fixture.
4. thread→parent-discussion lookup guarded — a thread whose parent discussion falls outside the walk is skipped + logged, not a crash (accepted deviation, ADR-018 pin-down 3).
5. discussion data sourced via a direct discussion-service client + one batched replies call — the cross-resolver import and the per-discussion reply N+1 are both gone (ADR-018 pin-down 4).
6. `attachmentElasticResponseFeatureFlag` state surveyed across every environment BEFORE fixtures are recorded — blocking precondition on fixture recording (ADR-018 pin-down 5).
7. draft-filter TODO ("ACL should be doing this") kept verbatim in the ported code — filter not removed; ACL-enforcement backlog item filed separately (ADR-018 pin-down 7).
8. `createAttachmentPaged`'s `relatedResources` precedence bug preserved exactly as today's output — pinned by a fixture using a row with its own non-empty `relatedResources` (ADR-018 pin-down 9).
9. independent fetches (token, discussions, threads, samples) run in parallel — accepted performance fix (ADR-018 pin-down 10).

> **Note:** the missing-ACL skip+log behaviour here is intentionally asymmetric with `G-02`'s missing-ACL throw (ADR-014 pin-down 2) — each surface's UI is calibrated to its own behaviour; this asymmetry is by design (ADR-018 pin-down 8) and should not be "fixed" to match.

#### Test Cases

- [ ] merge
- [ ] ordering
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### PRODUCT-BE-G-02 · `Product.components`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Very High · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔴 `search`

- **In plain terms:** List everything attached to a product, tagged by type, with counts.

- **Current Behaviour, in plain terms:** the components tab lists everything attached to a product — measurements,
- claims, boms, product-details, packaging — tagged by type, with counts (how many are archived, how many per component type, broken down per business partner).
- Today's biggest performance problem: for every claim in the result, it makes a **separate** ACL permission check call — 50 claims means 50 sequential ACL calls ("N+1"), instead of one batched call for all 50. ~190 ln — 4 parallel elastic (measurement/claim/bom/productDetail) + packaging + **per-claim N+1 ACL** + 5-type merge + count rollups.
- **Target:** refactor N+1 ACL into a batched call; preserve type tagging + `cloneDeep(initialCountsByBp)`.
- **Pattern (draft ADR-014, pending ratification):** owner-computed rollup — bom/measurement/packaging/productDetail queries become in-process calls (co-located), elastic/claims/ACL stay sibling clients; the four fixes (batched claim ACL, packaging joins the parallel group, explicit field args replacing `info.variableValues`, zeros-object) are accepted deviations. Preserve `type 2 → packagingBom` tagging (recorded in `SPIKE-05`'s code→type registry). See [ADR-014 §4](../../complexStories/components-and-counts-rollups/01-adr-components-counts-rollups.md).

- **Pseudocode — the N+1 → batched ACL fix (the actual point of this port):**
```kotlin
// before (bug, N+1): one ACL call per claim
val claimsWithAccess = claims.map { claim -> claim to aclClient.checkAccess(claim.id) }   // 50 claims = 50 calls

// after (fixed): one batched call for every claim id up front
val accessByClaimId = aclClient.checkAccessBatch(claims.map { it.id })                    // 50 claims = 1 call
val claimsWithAccess = claims.map { claim -> claim to accessByClaimId.getValue(claim.id) }
```
The 5-type merge (measurement/claim/bom/productDetail/packaging) and count rollups
(`archivedCount`, `countByComponents` per business partner) are ported as-is — same logic, same
`cloneDeep(initialCountsByBp)` pattern to avoid mutating the shared initial-counts template across requests.

#### Acceptance Criteria

1. parity for 50+ components, incl. a product with > 100 components (chunked ACL) and a claim with a missing ACL record (throw path preserved, ADR-014 pin-down 2).
2. `archivedCount`/`countByComponents` match source exactly (incl. name/status fallbacks and `type 2 → packagingBom`).
3. ACL batched — exactly one `getAccessControlBatch` call per resolution (no N+1), asserted by a call-count test.
4. no `info.variableValues` read; explicit field args confirmed against UI queries (contract test, ADR-014 pin-down 5).
5. sample→discussion **+1** roll-up quirk preserved exactly, not "fixed" to real counts — pinned by a dedicated fixture documenting the quirk as intentional (ADR-014 pin-down 4).
6. packaging elastic query joins the 4-way `Promise.all` (5-way parallel) instead of running sequentially after — accepted performance fix, not a behaviour change (ADR-014 pin-down 7).

> **Note:** ADR-014 pin-downs 3 (`counts` scalar-`0` → zeros-object fix) and 8 (`WorkspaceV2.products` include-flags delegation) are `WorkspaceV2`-side, not `Product`-side — they belong to the later-phase `WorkspaceV2` twin story (`WORKSPACE-BE-G-02`/`G-04`), not here.

#### Test Cases

- [ ] merge
- [ ] counts
- [ ] batched ACL
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### PRODUCT-BE-G-03 · `Product.attachments` + `attachmentsV3` + `attachmentSummary` + `ProductTemplate.attachmentsData`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** High · **Category:** CAT-2 · **Depends on:** G-01 · **EXT:** 🔴 `attachment` · 🔴 `search`

- **In plain terms:** Resolve the product's attachment views (via a shared enrichment service).

- **Current Behaviour:** four related resolvers sharing `AttachmentEnrichmentService` (G-01). **Target:** thin `@DgsData` fields over the shared service.

- **Example:** `Product.attachments` calls `attachmentEnrichmentService.attachments(productId)` (the plain list,
no discussion/sample merge); `attachmentsV3` calls the v3-shaped variant; `attachmentSummary` returns just the
counts; all four share the one `G-01` service instance rather than each re-implementing hydration.

#### Acceptance Criteria

1. each field returns its shape.
2. shares G-01 service.
3. thin fields inherit all of `G-01`'s fixtures/pin-downs by construction (no separate fixture set).

#### Test Cases

- [ ] each field
- [ ] draft discussion attachment fixture (draft filter)
- [ ] workspace-v2-only-attachments fixture
- [ ] both `attachmentsV3` modes (args-present elastic vs args-absent walk/flag) produce parity output
- [ ] Parity: DGS response matches spark-internal-graphql baseline

---

### PRODUCT-BE-G-04 · `ProductsCategories.categories` (12-case) + `DopplerDepartment` fields
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `doppler`

- **In plain terms:** Resolve the polymorphic categories union (12 branches) and department fields.

- **Current Behaviour, in plain terms:** `categories` is a polymorphic union — depending on which category type
- the caller asked for, a different one of 12 branches builds the response shape.
- Two of those branches (`DopplerDepartment.primaryCapacityTypeName` / `secondaryCapacityTypeName`) both need the same Doppler department lookup, so today's code memoizes that one call and reuses it for both fields.
- 12-branch dispatcher; `DopplerDepartment.primary/secondaryCapacityTypeName` share one Doppler call (memoized).
- **Target:** Kotlin dispatcher → 12 helpers; Doppler via DataLoader.

- **Example:** `getCategories(type: "department")` → dispatches to the `department` branch → builds a
`DopplerDepartment`; its two capacity-type-name fields both call `dopplerLoader.load(departmentId)` — same
`DataLoader` batch key, so it's one Doppler call even though two fields need it.

#### Acceptance Criteria

1. each category type built correctly.
2. Doppler fetched once.

---

### PRODUCT-BE-G-05 · `Product.samples` + `sampleIds` + `elasticSamplesList`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🟡 `sampleV2` · 🔴 `search`

- **In plain terms:** Resolve a product's samples from local context (removing the fragile args hack).

- **Current Behaviour, in plain terms:** today these fields reach into GraphQL's internal `info.variableValues`
to read arguments that were passed to a *different, parent* query — a fragile, implicit way to pass data down.
The port makes that explicit: the parent query passes what these fields need as normal arguments.
**stops reading `info.variableValues`** — pass explicit args from the query layer (contract change). **Target:** explicit args; document the contract change.

- **Example (before → after):**
```
// before: Product.samples reaches up into the parent query's raw GraphQL info object
fun samples(product: Product, info: DataFetchingEnvironment) = info.variableValues["sampleFilter"]  // implicit, fragile

// after: sampleFilter is an explicit argument on the field itself
fun samples(product: Product, @InputArgument sampleFilter: SampleFilter?) = sampleService.getSamples(product.id, sampleFilter)
```

#### Acceptance Criteria

1. samples/sampleIds/elastic resolve.
2. no `info.variableValues` read.

---

### PRODUCT-BE-G-06 · `Product.teams` + `discussionsV2` + `discussionsCount` + `workspaces`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🟡 `teamV2` · 🟡 `discussion` · 🔴 `search` · 🔴 `workspaceV2`

- **In plain terms:** Resolve a product's team / discussion / workspace fields.

- **Current Behaviour:** team/discussion/workspace elastic lookups. **Target:** federated references + elastic.

- **Example:** `Product.teams` → federated reference to `plm-team`'s `TeamV2` type; `discussionsCount` → an
elastic count query scoped to the product id, same semantics as today, just called from Kotlin.

#### Acceptance Criteria

1. each field resolves.

---

### PRODUCT-BE-G-07 · `Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `vmm`

- **In plain terms:** Resolve a product's partner fields (with id normalization).

- **Current Behaviour, in plain terms:** business-partner ids sometimes arrive as strings that need to be
- parsed to ints before VMM will accept them (`vmmUtils`'s int-parse normalization) — an easy detail to drop silently on a naive port.
- `loadBps`/`loadBpsWithType` (VMM); `status` merges partner/workspace statuses.
- **Target:** `vmmUtils` Kotlin port; preserve int-parse normalization.
- **`unDroppablePartners` (spike-gated, `SPIKE-04`):** implement per draft [ADR-016](../../complexStories/notRemovable-undroppable-partners/01-adr-notremovable-undroppable-partners.md) — owner-computed union over per-domain partner lanes (phase 1: direct scoped client calls, never sibling resolver pipelines); preserve the `isDesignPartner`-only gate, the `dps` whole-resource exclusion, and `.filter(Number)` semantics exactly (ADR-016 pin-downs 5–7), each pinned by fixture.

- **Example:** `businessPartners(ids: ["123", "456"])` → normalize to `[123, 456]` (Int) before calling
`vmmClient.getPartners(ids)` — dropping this normalization would silently break VMM lookups for any caller
passing partner ids as strings (which is most callers, since GraphQL doesn't distinguish).

#### Acceptance Criteria

1. partners resolve via VMM.
2. `status` merge correct.

---

### PRODUCT-BE-G-08 · `Product.measurementSets` + `claims` + `bom` + `productBom` + `packagingBom` + `productDetails` + `variations` + `associateProductsAsks`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Resolve the 8 'ask a sibling domain' product fields (bom, measurement, …), each on demand.

- **Current Behaviour, in plain terms:** each of these 8 fields is "go ask a sibling domain (bom, measurement,
- etc.) for this product's data" — but only if the caller asked for it (each has an `includeXxx: Boolean` flag to avoid an unnecessary call).
- Since product, bom, measurement, etc. all live in the same `plm-product` service after migration, "ask the sibling domain" becomes a plain method call, not a network hop. sibling-domain passthroughs with `includeXxx` boolean branches — **internal same-DGS calls** (not cross-subgraph).
- **Target:** internal service calls to the co-located sibling services.

- **Example:** `Product.bom(includeBom: true)` → `bomService.getBomsByProductId(productId)` (plain in-process
call, same JVM); `includeBom: false` → skip the call entirely, return `null`/`[]` without touching `bomService`.

#### Acceptance Criteria

1. each sibling field resolves internally.
2. `includeXxx` branches honored.

---

### PRODUCT-BE-G-09 · `Product.productWorkspaceAttributes` + `productWorkspaceInfo`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔴 `workspaceV2` · 🔴 `search` · 🟡 `tag`

- **In plain terms:** Resolve a product's per-workspace attributes (incl. lazy designCycle).

- **Current Behaviour, in plain terms:** `designCycle` is computed lazily today — an inline `async () => ...`
- closure attached to the value, evaluated only if a caller actually reads that sub-field.
- GraphQL/DGS already has a first-class way to express "only compute this if asked": a nested field resolver.
- Same laziness, cleaner code. both produce shapes with a **deferred `designCycle: async()=>…`** field-on-value.
- **Target:** model `designCycle` as a nested `@DgsData`, not an inline closure.

- **Example (before → after):**
```
// before: designCycle is an inline lazy closure attached to the parent object
return ProductWorkspaceAttributes(..., designCycle = { -> designCycleService.compute(productId) })

// after: designCycle is its own @DgsData field, resolved only when queried — same laziness, no closures
@DgsData(parentType = "ProductWorkspaceAttributes", field = "designCycle")
fun designCycle(dfe: DgsDataFetchingEnvironment) = designCycleService.compute(dfe.getSource<ProductWorkspaceAttributes>().productId)
```

#### Acceptance Criteria

1. both fields resolve.
2. `designCycle` is a nested fetcher.

---

### PRODUCT-BE-G-10 · `Product.ancestryProducts` + `rating` + `reservedDpcis`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🟡 `relationship` · 🔵 `rating` · 🔵 `apex`

- **In plain terms:** Resolve a product's ancestry, rating and reserved-DPCI fields.

- **Current Behaviour:** `rating` via `RatingClient`; `reservedDpcis` via `getReservedDpcisFromApex`. **Target:** federated/Feign references.

- **Example:** `rating` calls the same external rating endpoint as `C-04` (`getRatingByTcin`) — any error there
(timeout, 4xx/5xx) resolves to `null`, never an exception, exactly like `C-04`'s "any error → null" rule.

#### Acceptance Criteria

1. ancestry/rating/dpcis resolve.
2. rating null-on-error.

---

> **Split in two (per review).** The original `G-11` bundled two unrelated concerns — a reflective-call fix
> (partner/workspace removability) and two plain sibling passthroughs (asks/variations) — into one story.
> Splitting lets the reflective-call fix (the only part with real risk) be reviewed and tested independently
> of the two trivial passthroughs.

---

### PRODUCT-BE-G-11-1 · `Product.notRemovablePartnerIds` + `notRemovableWorkspaceIds`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `vmm` · 🔴 `workspaceV2`

- **In plain terms:** Compute which partners/workspaces can't be removed (still referenced).

- **Current Behaviour, in plain terms:** to figure out which partners/workspaces *can't* be removed from a
product (e.g. because they're the last remaining owner), today's code calls into 4-5 other field resolvers
**reflectively** — by resolver name, at runtime — instead of just calling the underlying service methods those
- resolvers themselves call.
- Reflection here buys nothing (the set of resolvers is fixed, known at compile time) and makes the code harder to trace, test, and refactor safely. source utils call into 4–5 sibling field resolvers **reflectively**.
- **Target:** **replace reflective resolver invocation with direct service-method calls** (same logical union).
- **Pattern (spike-gated, `SPIKE-04` — draft ADR-016, pending ratification):** the aggregator stays owned by `plm-product` and resolves per-domain **lanes** (discussion/attachment/sample/watchlist partner slices) via direct scoped client calls in phase 1; each lane flips to a federated contribution as its subgraph ships, aggregator unchanged. The `samples` source's `info.variableValues` coupling cannot be ported — the lane contract must be settled with the UI team before cutover (ADR-016 pin-down 2, hard blocker). Sources fetch in parallel (accepted deviation, pin-down 3).

- **Example (before → after):**
```kotlin
// before: reflectively invoke resolver functions by name
val removable = resolverRegistry.invoke("businessPartners", product) +
                 resolverRegistry.invoke("droppedPartners", product) + /* ... */

// after: call the same underlying services directly, no reflection
val removable = vmmService.getBusinessPartners(product.id) +
                 vmmService.getDroppedPartners(product.id) + /* ... */
```

#### Acceptance Criteria

1. `notRemovablePartnerIds`/`notRemovableWorkspaceIds` return the same results as source (same logical union
   of the underlying sibling data).
2. No reflective resolver invocation remains — every call is a direct, statically-typed service method call.
3. samples lane's `variableValues` coupling contract-checked against the UI's samples queries BEFORE cutover — this is a blocking pre-condition, not a nice-to-have (ADR-016 pin-down 2).
4. the 5 sequential source fetches (discussions/attachments/components/samples/watchlists) parallelize — accepted deviation, union output is order-insensitive (ADR-016 pin-down 3).
5. the serial ACL chunk loop (`getAccessControlBatch`) parallelizes — same fix family as ADR-015 pin-down 3 (ADR-016 pin-down 4).
6. watchlist lane's `productWorkspaceInfo[0]`-only / first-workspace-only scope preserved exactly as today's semantics (ADR-016 pin-down 8).
7. the Relationship-Service walk inside `unDroppablePartners`'s owner-enumeration client is a quarantined interim — each lane's future arrival deletes its own share of the walk (ADR-016 pin-down 9).
8. schema-diff gate proves no lane field (`…PartnerIds` naming + externals until fed-2/`@inaccessible` is usable) is exposed to clients (ADR-016 pin-down 10).

---

### PRODUCT-BE-G-11-2 · `Product.associateProductsAsks` + `Product.variations`
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** —

- **In plain terms:** Resolve two sibling passthroughs (product-asks and variations).

- **Current Behaviour, in plain terms:** two straightforward sibling passthroughs — `associateProductsAsks`
- (the product-ask records tied to this product) and `variations` (sibling product variation records) — with no reflective-call complexity, no batching concern, no external-service risk.
- Bundled separately from `G-11-1` precisely because there's nothing here that needs the same scrutiny.
- **Target:** thin `@DgsData` fields calling the co-located `productAskService`/`productVariationService` directly.

- **Example:** `Product.associateProductsAsks` → `productAskService.getByProductId(productId)`; `Product.variations`
→ `productVariationService.getByProductId(productId)` — both plain in-process calls, same pattern as `G-08`.

#### Acceptance Criteria

1. `associateProductsAsks` resolves the product's ask records.
2. `variations` resolves the product's variation records.

---

### PRODUCT-BE-G-13 · IG/tag/tcin/spg + template trivial-field group
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🔵 `ig` · 🟡 `tag` · 🔵 `corona`

- **In plain terms:** Resolve a group of trivial IG / tag / TCIN / template fields.

- **Current Behaviour:** `department`/`departments`/`clazz`/`brand`/`brands`/`divisions`/`productTemplateDepartments`, `tags`, `tcins`, `SPARK_Tcin.itemDetails` (CORONA), `SPARK_PackagingAttribute.spg` (internal fileLibrary), `SPARK_ProductRules.*`, `VMM_BusinessPartnerCategory.*`, `MasterProductStatus.*`. **Target:** group into one PR; federated/internal references.

- **Example:** `department`/`divisions` → federated references to `ig`'s subgraph (**note:** unlike the known
`Product.division`/`DopplerDepartment.division` wrong-loader bug — tracked outside this Jira pipeline — these
already call the correct IG endpoint; they're grouped here only because they're trivial); `SPARK_Tcin.itemDetails`
→ federated reference to CORONA; `SPARK_PackagingAttribute.spg`
→ internal `fileLibraryService` call (co-located, no federation).

#### Acceptance Criteria

1. each field resolves to the right source.

---

### PRODUCT-BE-G-14 · Simple user/status fields + trivial pass-throughs (bundle)
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Low · **Category:** CAT-2 · **Depends on:** — · **EXT:** 🟡 `userAttributes`

- **In plain terms:** Resolve simple people / status fields and trivial pass-throughs.

- **Current Behaviour:** `createdBy`/`updatedBy`/`versionCreatedBy` (user-profile), `ProductComponentStatus.updatedBy`, `SPARK_ResourcesCount.productThumbnailId` (re-fetch product), plus ~60 direct scalar pass-throughs (DTO-mapped). **Target:** thin `@DgsData` for user/thumbnail; Jackson DTO mapping for scalars.

- **Example:** `createdBy` → federated reference to `user-profile` by id, `null` id → `null`, no call made;
the ~60 scalar fields (`name`, `status`, `createdAt`, etc.) need no resolver at all — Jackson maps them
straight from the REST response DTO to the GraphQL type by field name.

#### Acceptance Criteria

1. user fields resolve (null id → null).
2. `productThumbnailId` re-fetches.
3. scalars mapped.

---

### PRODUCT-BE-G-15 · Port product utils to Kotlin
- **Type:** Service · **Phase:** G · **Complexity:** Medium · **Category:** CAT-3 · **Depends on:** —

- **In plain terms:** Port the shared product utility helpers to Kotlin.

- **Current Behaviour:** `attachmentUtils`, `partnerUtils`, `teamUtils`, `productUtils`, `componentStatusUtils`, `resolvePaging`, `vmmUtils`, `accessControlUtils`, `removePartnerUtils`. **Target:** Kotlin ports; single camel/snake normalization at the Feign boundary; **fix** `componentStatusUtils.incrementAllContextCounter` (never resets — verify intent); batch `getAccessControlBatch` with parallel chunking.

- **Example — the counter bug to verify/fix:** `incrementAllContextCounter` increments a running total every
- call but is never reset between requests — meaning under the current code, the "count" it reports keeps growing across unrelated requests instead of reflecting just the current one.
- Verify with the source team whether that's intentional (a genuinely global counter) or a bug (should reset per-request); if a bug, scope the counter to the request context.
- **Example — ACL batch chunking:** `getAccessControlBatch(ids: 500 ids)` splits into chunks (e.g. 50 at a
time) and issues the chunks **in parallel** (`coroutineScope { chunks.map { async { ... } } }.awaitAll()`),
rather than one giant call or 500 sequential ones.

#### Acceptance Criteria

1. utils ported with unit tests.
2. counter logic fixed/verified.
3. ACL batch parallel-chunked.

---

### PRODUCT-BE-G-17 · Entity references on partner/lineage value types (recommended, PO-gated)
- **Type:** Field Resolver · **Phase:** G · **Complexity:** Medium · **Category:** CAT-2 · **Depends on:** G-01 · **EXT:** 🔵 `vmm`
- **Status:** Recommended (PO-gated — federation-review/03 §2 REC-5/REC-6, OQ-5)

- **In plain terms:** Adds `partner { … }` / `product { … }` object fields next to the existing ids on the
per-partner and lineage value rows, so clients stop re-joining ids against separate lookups.

- **Context:** `ProductVendorAttributes.partnerId` and `WorkspaceInfoPartner.partnerId` force clients to join
rows against the `businessPartners` list client-side; `AncestryProducts`/`ChildProducts` carry only a product
id, so lineage detail needs a follow-up `getProductsByIds`. All additions are additive — every existing id
field stays (client contract).
- **Target DGS Implementation:** schema adds `partner: VMM_BusinessPartner` (emit `{id}` key stub — the gateway
hydrates) on `ProductVendorAttributes` + `WorkspaceInfoPartner`, and `product: Product` (internal
`productService` call, DataLoader-batched) on `AncestryProducts` + `ChildProducts`.

#### Acceptance Criteria

1. PO approval recorded (OQ-5) before implementation starts.
2. New object fields resolve; all existing id fields unchanged.
3. `product` lineage refs batch via DataLoader (no N+1 on `ancestryProducts`).
4. Codegen/contract parity suite passes with the additive fields present.

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| TechPack composite-key aggregate (E-03/E-04) | High | High | facade-then-federate (draft ADR-015 Option B; direction already resolved); bulk-order fix | Tech Lead + Platform |
| `productBusinessPartnerActions` partial failure (E-01) | Medium | High | `S-03` spike (run first, program id `SPIKE-03`, draft ADR-012) picks the failure strategy before `E-01` starts | Tech Lead |
| `components` N+1 ACL regression (G-02) | Medium | Medium | Batch ACL on port | Backend Eng |
| `attachmentsWithMetaData` perf (G-01) | Medium | High | Parallel fetch + cached relationship walk | Backend Eng |
| `getProducts` workspace-filter/staleness handling (C-01) | Medium | Medium | `S-02` spike resolves the two-stage hydration design before `C-01` starts | Backend Eng |
| Cross-domain association pattern inconsistency (D-01/D-02/D-04) | Medium | Medium | `S-01` spike (program id `SPIKE-06b`, draft ADR-011) sets one pattern; D-03/D-06/D-07/D-11 descoped (single-backend) | Tech Lead |
| `Product.division`/`DopplerDepartment.division` wrong-loader bug fix breaks clients | Medium | Medium | Client survey before rollout; tracked outside this Jira pipeline, created manually | PO |
| 8 TechPack placeholders block on 8 domains | High | Medium | Facade keeps day-1 function; retire only when all live | Tech Lead |
| `USE_NEW_RULES_API` legacy delete | Low | High | Verify all envs; staged rollout | PO |
| Drift wrappers may have live consumers | Medium | Medium | Traffic survey (F-12) | PO |
| External rating secret | Low | Medium | Vault | Platform |

## 5. Summary
- **Stories:** 71 (S:3 · B:11 · C:5 · D:18 · E:5 · F:6 · H:6 · G:16). `E-00` (shared `WriteSaga` module, Sprint 0)
  added per ADR-013's build order — the module every other E-phase write depends on. `G-11` was **split into G-11-1/G-11-2** (+1 to G);
  `H` counts the 6 real cross-subgraph entity-resolution stories (5 `ResourcesCount` federated slices + the
  `Product` entity fetcher — see Phase H); `F` covers the remaining federation-platform work (facade retirement,
  gateway composition, stub verification, contract alignment; G-17 is recommended/PO-gated). Bug-fix/
  test-coverage stories (former `G-12`, `G-16`) tracked outside this Jira pipeline, created manually.
- **Critical path:** S-01/S-02/S-03 → B-01 → C-01/D-01-D-04/E-01 → E-03 (TechPack facade) → G-01 → G-02.
- **Highest risk:** TechPack (E-03/E-04); `productBusinessPartnerActions` (E-01, pending `S-03`).
- **Host DGS:** product is the home of the whole product family; co-located siblings resolve internally.
