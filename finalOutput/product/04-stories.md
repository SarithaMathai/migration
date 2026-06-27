# Phase 4: Migration Plan & Stories — Product

> **Domain:** `product` · **Target DGS:** `ProductService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md), [03-schema.graphql](./03-schema.graphql), [03-schema-analysis.md](./03-schema-analysis.md), [05-attribute-inventory.md](./05-attribute-inventory.md)
> **Index:** [04-stories-index.yaml](./04-stories-index.yaml)

Junior engineers: each story is self-contained (read *Current Behaviour → Target → Files → Acceptance →
Tests*). Detailed pseudo-logic for every operation is in [02-resolver-analysis.md](./02-resolver-analysis.md)
(referenced per story). **ACL is context-only** — no ACL work in any story.

## 1. Phases Overview
| Phase | Name | Stories |
|---|---|---|
| A | Foundation & Schema | A01–A06 |
| B | Core Reads | B01–B11 |
| C | Search & Listing | C01–C05 |
| D | Mutations (simple) | D01–D18 |
| E | Complex Operations (partner actions, component fan-out, TechPack) | E01–E04 |
| F | Federation & Stitching (TechPack federate + gateway + decisions) | F01–F12 |
| G | Field Resolvers, Bug-fixes, Utils, Tests | G01–G16 |

## 2. Dependency Graph
```mermaid
graph TD
  A01[A01 Schema]-->A02[A02 Types]&A03[A03 Stubs]&A04[A04 Categories resolver]&A05[A05 ResourcesCount]&A06[A06 ProductService port]
  A06-->B[B Reads]&C[C Search]&D[D Mutations]
  A05-->E03[E03 TechPack facade]-->E04[E04 TechPack bulk]
  D-->E01[E01 partnerActions]&E02[E02 componentStatuses]
  A02-->G[G Field resolvers]
  E03-->F01[F01-F08 subgraph placeholders]-->F09[F09 retire facade]
  G-->G16[G16 Tests]
```

---

## 3. Stories

### Phase A — Foundation & Schema

### SPARK-PROD-A01 · Schema skeleton + DGS module + DateTime/JsonNode scalars
```yaml
{id: SPARK-PROD-A01, operation: "-", type: schema, category: CAT-1, phase: A, complexity: Low, depends_on: [], ext_services: [], files: [plm-product/.../schema/product.graphqls, plm-product/.../config/ScalarConfig.kt], blocked_by: none}
```
**As a** DGS engineer **I want** the `product.graphqls` skeleton + federation header + `DateTime`/`JsonNode`
scalars **so that** all later product work compiles. **Current Behaviour:** green-field (schema translated from `code/schemas/SPARK_Product.txt`).
**Target:** v2.3 `@link`, `scalar DateTime→Instant`, `scalar JsonNode`, empty `extend type Query`/`Mutation`.
**Files:** `schema/product.graphqls`, `config/ScalarConfig.kt`. **Deps:** none.
**Acceptance:** 1. `./gradlew generateJava` passes. 2. scalars round-trip. **Tests:** ☐ compiles ☐ scalar serde.

### SPARK-PROD-A02 · Define all owned types + ~30 inputs
```yaml
{id: SPARK-PROD-A02, operation: "-", type: schema, category: CAT-1, phase: A, complexity: Medium, depends_on: [SPARK-PROD-A01], ext_services: [], files: [plm-product/.../schema/product.graphqls], blocked_by: none}
```
**As a** DGS engineer **I want** ~40 owned types + ~30 inputs from [03-schema.graphql](./03-schema.graphql)
**so that** resolvers/mutations have a contract. **Target:** `@key(fields:"id")` on `Product`/`ProductRules`;
`@shareable` on `Paging`/`Pageable`/`CodeDescription`/`CodeDescriptionOrder`/`AccessV3`/`WorkspaceStatus`/
`ResourcePermissions`/`PermissionEntry`/`SpgFileLibrary`. **Deps:** A01.
**Acceptance:** 1. All owned types+inputs present. 2. Keys/shareables applied. 3. Schema validates. **Tests:** ☐ validates ☐ entity stub.

### SPARK-PROD-A03 · External stubs (platform + sibling DGS)
```yaml
{id: SPARK-PROD-A03, operation: "-", type: schema, category: CAT-1, phase: A, complexity: Low, depends_on: [SPARK-PROD-A01], ext_services: [], files: [plm-product/.../schema/product.graphqls], blocked_by: none}
```
**Target:** 6 platform stubs (`VMM_*`, `IG_*`, `DopplerCapacityType`, `CORONA_ItemDetails`) + ~16 sibling
stubs per [03-schema.graphql §1](./03-schema.graphql). Note co-located stubs resolve internally at runtime.
**Deps:** A01. **Acceptance:** 1. all stubs compile; gateway composes. **Tests:** ☐ compiles ☐ gateway resolves a VMM stub.

### SPARK-PROD-A04 · `Categories` union `@DgsTypeResolver`
```yaml
{id: SPARK-PROD-A04, operation: "Categories", type: field-resolver, category: CAT-2, phase: A, complexity: Medium, depends_on: [SPARK-PROD-A02, SPARK-PROD-A03], ext_services: [], files: [plm-product/.../dataFetcher/CategoriesTypeResolver.kt], blocked_by: none}
```
**Current Behaviour (Phase 2):** 12-case switch over `category.type`, **default → `IG_Clazz_Filter`**.
**Target:** `@DgsTypeResolver(name="Categories")` mirroring the 12 cases + default. **Deps:** A02, A03.
**Acceptance:** 1. all 12 known tags map correctly. 2. unknown → `IG_Clazz_Filter`. **Tests:** ☐ 12 cases ☐ default.

### SPARK-PROD-A05 · `ResourcesCount @key(fields:"productId partnerId")` composite type
```yaml
{id: SPARK-PROD-A05, operation: "ResourcesCount", type: schema, category: CAT-1, phase: A, complexity: Low, depends_on: [SPARK-PROD-A01], ext_services: [], files: [plm-product/.../schema/product.graphqls], blocked_by: none}
```
**Target:** add the composite-key type with 11 stub fields, each commented with its owning subgraph (see
[03-schema.graphql §3](./03-schema.graphql)). Product owns the type + stub resolver; siblings extend later (Phase F).
**Deps:** A01. **Acceptance:** 1. `@key` = `productId partnerId`; context fields not in key. 2. stub fields annotated. **Tests:** ☐ compiles ☐ entity fetcher stub.

### SPARK-PROD-A06 · `ProductService` Kotlin port (42 methods, grouped)
```yaml
{id: SPARK-PROD-A06, operation: "ProductService", type: service, category: CAT-3, phase: A, complexity: High, depends_on: [SPARK-PROD-A01], ext_services: [], files: [plm-product/.../service/Product*Service.kt, plm-product/.../client/*Client.kt, plm-product/.../model/*Dto.kt], blocked_by: none}
```
**Current Behaviour (Phase 2 §Service):** 42 REST wrappers against `v1`/`v2`, elastic, `spark_rules`, external rating.
**Target:** split into `ProductReadService`, `ProductWriteService`, `ProductElasticService`, `ProductCopyService`,
`ProductRuleService`, `ProductComponentStatusService`, `RatingClient` (Feign, external), plus internal calls for
co-located ops. Master/status reads `@Cacheable`. Preserve `getByID` priming, `linkProduct` `throwOnError`,
external-rating API-key (→ Vault). **ACL note (context):** capability-token currying is omitted (ACL ignored).
**Deps:** A01. **Acceptance:** 1. all 42 signatures present. 2. co-located methods make no outbound HTTP. 3. rating secret in config/Vault. 4. `linkProduct` throws on backend error. **Tests:** ☐ endpoint build ☐ cache hit ☐ rating parse ☐ linkProduct throws.

---

### Phase B — Core Reads (one query per story)

> Pattern: `@DgsQuery` → `ProductReadService.method`. Full pseudo-logic in [02 §Query Resolvers](./02-resolver-analysis.md). All depend on A02+A06.

### SPARK-PROD-B01 · `getProduct(id)`
```yaml
{id: SPARK-PROD-B01, operation: getProduct, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A02, SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductQueryDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q3):** `getByID.load(id)` `GET ${v1}?productId={id}` → camelCase or null; DataLoader-batched.
**Target:** `@DgsQuery getProduct(id): Product` via `ProductDataLoader` keyed on id. **Acceptance:** 1. returns product; 404→null. 2. batches N ids in 1 call. **Tests:** ☐ happy ☐ 404→null ☐ batch ☐ integration.

### SPARK-PROD-B02 · `getProductsByIds(ids)`
```yaml
{id: SPARK-PROD-B02, operation: getProductsByIds, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A02, SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductQueryDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q6):** `getByIdList.load(ids)` `GET ${v1}?productId={csv}&page=0&size=10000&sort=createdDate,desc`; primes `getByID`. **Target:** `@DgsQuery` → `ProductsPaged`. **Acceptance:** 1. returns paged products for ids. 2. primes single-id loader. **Tests:** ☐ happy ☐ empty ☐ integration.

### SPARK-PROD-B03 · `getProductStatus` (cacheable)
```yaml
{id: SPARK-PROD-B03, operation: getProductStatus, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductQueryDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q7):** `getStatus.load()` master status list. **Target:** `@DgsQuery` → `@Cacheable` → `[MasterProductStatus]`. **Acceptance:** 1. returns statuses. 2. cached. **Tests:** ☐ list ☐ cache hit.

### SPARK-PROD-B04 · `getProductVersions(id)`
```yaml
{id: SPARK-PROD-B04, operation: getProductVersions, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductQueryDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q10):** `getVersions.load({id})` `GET ${v1}/{id}/versions?page=0&size=10000`. **Target:** `@DgsQuery` → `ProductsPaged`. **Acceptance:** 1. returns versions. **Tests:** ☐ happy ☐ integration.

### SPARK-PROD-B05 · `getCopyStatus(id)`
```yaml
{id: SPARK-PROD-B05, operation: getCopyStatus, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductQueryDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q4):** `getCopyStatus.load(id)` `GET ${v2}/count/resource-type?copyId={id}`. **Target:** `@DgsQuery` → `ProductCopy`. **Acceptance:** 1. returns copy status. **Tests:** ☐ happy ☐ integration.

### SPARK-PROD-B06 · `getProductTemplateById(id)`
```yaml
{id: SPARK-PROD-B06, operation: getProductTemplateById, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductQueryDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q18):** `getByID.load(id)` → `response || {}` (empty object on miss — **preserve**). **Target:** `@DgsQuery getProductTemplateById(id): Product`. **Acceptance:** 1. returns product or empty object (not null). **Tests:** ☐ happy ☐ miss→{}.

### SPARK-PROD-B07 · `getProductRules`
```yaml
{id: SPARK-PROD-B07, operation: getProductRules, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q12):** `getAllRules.load()` `GET ${base}/spark_rules/v1` → `content`. **Target:** `@DgsQuery` → `[ProductRules]`. **Acceptance:** 1. returns rules content. **Tests:** ☐ list ☐ integration.

### SPARK-PROD-B08 · `getProductRulesById(id)`
```yaml
{id: SPARK-PROD-B08, operation: getProductRulesById, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q13):** `getRuleById.load(id)` `GET ${base}/spark_rules/v1/{id}`. **Target:** `@DgsQuery` → `ProductRules`. **Acceptance:** 1. returns rule. **Tests:** ☐ happy ☐ 404.

### SPARK-PROD-B09 · `getAllAvailableRules`
```yaml
{id: SPARK-PROD-B09, operation: getAllAvailableRules, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q14):** `getAvailableRules.load()` `GET …/spark_rules/v1/rules`. **Target:** `@DgsQuery` → `[AvailableRules]`. **Acceptance:** 1. returns available rules. **Tests:** ☐ list.

### SPARK-PROD-B10 · `getProductDeptRules(productIds, departmentIds, activeOnly)`
```yaml
{id: SPARK-PROD-B10, operation: getProductDeptRules, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [{key: ruleLibrary, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q15):** **flag fork** `USE_NEW_RULES_API ? ruleLibrary.searchRuleLibrary : product.searchProductDeptRules` `GET …/spark_rules/v1/search?productIds=&departmentIds=&activeOnly=`. **PO decision:** flag cutover (rules may move to spark-tag DGS). **Target:** `@DgsQuery`; both code paths covered. **Acceptance:** 1. default `activeOnly=true`. 2. flag selects the correct backend. **Tests:** ☐ legacy path ☐ flag path ☐ parity.

### SPARK-PROD-B11 · `getProductBPRules(productIds, businessPartnerIds, activeOnly)`
```yaml
{id: SPARK-PROD-B11, operation: getProductBPRules, type: query, category: CAT-2, phase: B, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [{key: ruleLibrary, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q16):** same as B10 with `businessPartnerIds`. **Target:** `@DgsQuery`. **Acceptance:** 1. flag fork honored; BP filter applied. **Tests:** ☐ legacy ☐ flag ☐ parity.

---

### Phase C — Search & Listing

### SPARK-PROD-C01 · `getProducts(...)` two-stage hydration
```yaml
{id: SPARK-PROD-C01, operation: getProducts, type: query, category: CAT-2, phase: C, complexity: High, depends_on: [SPARK-PROD-A06], ext_services: [{key: search, severity: RED}], files: [plm-product/.../dataFetcher/ProductSearchDataFetcher.kt], blocked_by: none}
```
**As a** DGS engineer **I want** `getProducts` with elastic+canonical two-stage hydration **so that** listing
returns canonical records enriched with elastic flags.
**Current Behaviour (Q1):** (🔴 search) `getFilteredProductsListing({resourceType ?? 'products', includeBoms ?? true, includeClaims ?? true, includeMeasurementSets ?? true, includeProductDetails ?? true, filter ?? [], q ?? '', page, size})` → ids → (internal) `getPage({products:ids, page:0, size})` `GET ${v1}?productId=&sort=createdDate,desc` → merge elastic flags (`boms, productDetails, claims, measurementSets, samples, sampleIds, hasSamplesUpcomingDue, hasNotEvaluatedReceivedSamples, receivedNotEvaluatedCount`) onto canonical records. **Boolean defaults are truthy (`?? true`) — pin in tests.**
**EXT:** 🔴 search. **Target:** `ProductElasticService.getFilteredProductsListing` then `ProductReadService.getPage`; merge. **Deps:** A06.
**Acceptance:** 1. parity for 4 arg combos (no flags / all flags / resourceType=workspaces / filter array). 2. truthy defaults preserved. 3. elastic flags merged onto canonical. **Tests:** ☐ 4 combos ☐ default truthiness ☐ merge ☐ parity.

### SPARK-PROD-C02 · `getProductTemplates(...)`
```yaml
{id: SPARK-PROD-C02, operation: getProductTemplates, type: query, category: CAT-2, phase: C, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: search, severity: RED}], files: [plm-product/.../dataFetcher/ProductSearchDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q2):** (🔴 search) `getFilteredProductsListing({resourceType:'product', includeBoms:false, ...7 includeXxxTemplates flags, types})` → return elastic response (no 2nd hydration). **Target:** `@DgsQuery` → `ProductTemplatesList`. **Acceptance:** 1. all 7 template-include flags forwarded. 2. `types:[Int]` filter applied. **Tests:** ☐ flags ☐ types filter ☐ parity.

### SPARK-PROD-C03 · `getCategories(...)`
```yaml
{id: SPARK-PROD-C03, operation: getCategories, type: query, category: CAT-2, phase: C, complexity: Medium, depends_on: [SPARK-PROD-A04, SPARK-PROD-A06], ext_services: [{key: search, severity: RED}], files: [plm-product/.../dataFetcher/ProductSearchDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q5):** default `productType ?? 100`; (🔴 search) `getProductCategories` `GET ${elastic}/search/${snake_case(type)}?resourceType=&resourceId=&productType=` → `ProductsCategories` (polymorphic `categories` via A04). **Target:** `@DgsQuery`; preserve `snakeCase(type)` in the path. **Acceptance:** 1. `snake_case(type)` path exact. 2. wires to `Categories` union. **Tests:** ☐ snake-case path ☐ union dispatch ☐ parity.

### SPARK-PROD-C04 · `getRatingByTcin(tcin)` (external rating)
```yaml
{id: SPARK-PROD-C04, operation: getRatingByTcin, type: query, category: CAT-2, phase: C, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: rating, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductQueryDataFetcher.kt, plm-product/.../client/RatingClient.kt], blocked_by: none}
```
**Current Behaviour (Q11):** (🔵 external) `GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={API_KEY}` (`skipJsonParse`) → `JSON.parse` → `{averageRating, reviewCount}`; **catch → null** (silent). **Target:** `RatingClient` Feign (text/plain, manual parse); secret from Vault. **Acceptance:** 1. parses statistics to `Rating`. 2. any error → null. 3. API key from config/Vault, not source. **Tests:** ☐ parse ☐ error→null ☐ secret config.

### SPARK-PROD-C05 · `searchProductRules(...)`
```yaml
{id: SPARK-PROD-C05, operation: searchProductRules, type: query, category: CAT-2, phase: C, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: ruleLibrary, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q17):** flag fork; legacy `GET …/spark_rules/v1/search_mapped?...` → `productRuleResponseTransformer` → camelCase. **Target:** `@DgsQuery`; port the transformer. **Acceptance:** 1. flag fork honored. 2. legacy response transformed correctly. **Tests:** ☐ legacy transform ☐ flag path ☐ parity.

---

### Phase D — Mutations (simple, one per story)

> Pattern: `@DgsMutation` → `ProductWriteService.method`. Pseudo-logic in [02 §Mutation Resolvers](./02-resolver-analysis.md). All depend on A06. ACL is context-only.

### SPARK-PROD-D01 · `addProduct`
```yaml
{id: SPARK-PROD-D01, operation: addProduct, type: mutation, category: CAT-2, phase: D, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: workspaceV2, severity: RED}, {key: attachment, severity: RED}], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M1):** `POST ${v1}` + optional `copyProductToProduct(copyProduct)` + workspace association. **Target:** `@DgsMutation addProduct(workspaceId, sparkProduct, copyProduct): Product`; orchestrate create→copy→assoc. **Acceptance:** 1. creates product. 2. optional copy runs when `copyProduct` present. 3. workspace assoc applied. **Tests:** ☐ create ☐ create+copy ☐ create+assoc ☐ integration.

### SPARK-PROD-D02 · `addProducts` (bulk)
```yaml
{id: SPARK-PROD-D02, operation: addProducts, type: mutation, category: CAT-2, phase: D, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: attachment, severity: RED}], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M2):** bulk `POST ${v1}/bulk` + attachment-link side-effects (no rollback — **preserve, flag**). **Target:** `@DgsMutation` → `ProductBulkType`. **Acceptance:** 1. bulk creates. 2. attachment links applied; no-rollback behaviour documented. **Tests:** ☐ bulk ☐ links ☐ integration.

### SPARK-PROD-D03 · `bulkUpdateProducts`
```yaml
{id: SPARK-PROD-D03, operation: bulkUpdateProducts, type: mutation, category: CAT-2, phase: D, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M3):** `PUT ${v1}/mass_update`. **Target:** `@DgsMutation` → `ProductBulkType`. **Acceptance:** 1. mass-updates products. **Tests:** ☐ bulk update ☐ integration.

### SPARK-PROD-D04 · `updateProduct`
```yaml
{id: SPARK-PROD-D04, operation: updateProduct, type: mutation, category: CAT-2, phase: D, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: attachment, severity: RED}], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M4):** `PUT ${v1}/{id}` + optional copy + archive removed-template attachments (template branch). **Target:** `@DgsMutation updateProduct(input, copyProduct): Product`. **Acceptance:** 1. updates product. 2. optional copy. 3. removed-template attachments archived (template branch). **Tests:** ☐ update ☐ copy ☐ template archival.

### SPARK-PROD-D05 · `carryForwardProduct`
```yaml
{id: SPARK-PROD-D05, operation: carryForwardProduct, type: mutation, category: CAT-2, phase: D, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M5):** `PUT ${v1}/{productId}/carry_forward/{workspaceId}` — uses **every** field on `CarryForwardProductInput`. **Target:** `@DgsMutation`; verify full input mapping. **Acceptance:** 1. all input fields mapped to the request. **Tests:** ☐ full mapping ☐ integration.

### SPARK-PROD-D06 · `addTeamsToProduct`
```yaml
{id: SPARK-PROD-D06, operation: addTeamsToProduct, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M6):** `POST ${v1}/{productId}/resources/bulk` + manage_workspace_teams. **Target:** `@DgsMutation`. **Acceptance:** 1. adds teams + new partners + workspace links. **Tests:** ☐ teams ☐ partners ☐ integration.

### SPARK-PROD-D07 · `addBusinessPartnersToProductWithType`
```yaml
{id: SPARK-PROD-D07, operation: addBusinessPartnersToProductWithType, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M7):** `POST ${v1}/{productId}/partners-add/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. adds partners with type. **Tests:** ☐ add ☐ integration.

### SPARK-PROD-D08 · `removeProductResources`
```yaml
{id: SPARK-PROD-D08, operation: removeProductResources, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M8):** `DELETE ${v1}/{productId}/resources/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. removes resources. **Tests:** ☐ remove ☐ integration.

### SPARK-PROD-D09 · `updateBusinessPartnerStatuses`
```yaml
{id: SPARK-PROD-D09, operation: updateBusinessPartnerStatuses, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M9):** `PUT ${v1}/{productId}/status_update/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. updates partner statuses. **Tests:** ☐ update ☐ integration.

### SPARK-PROD-D10 · `updateViewToggle`
```yaml
{id: SPARK-PROD-D10, operation: updateViewToggle, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M11):** `PUT ${v1}` view toggle. **Target:** `@DgsMutation`. **Acceptance:** 1. toggles hidden. **Tests:** ☐ toggle.

### SPARK-PROD-D11 · `updateWorkspaceAttributes`
```yaml
{id: SPARK-PROD-D11, operation: updateWorkspaceAttributes, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M12):** `PUT ${v1}/{productId}` workspace attrs. **Target:** `@DgsMutation`. **Acceptance:** 1. updates workspace attrs. **Tests:** ☐ update.

### SPARK-PROD-D12 · `updateProductTeamsWorkspaceContext`
```yaml
{id: SPARK-PROD-D12, operation: updateProductTeamsWorkspaceContext, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M13):** `PUT` team-workspace add/remove. **Target:** `@DgsMutation`. **Acceptance:** 1. adds/removes team-workspace pairs. **Tests:** ☐ add ☐ remove.

### SPARK-PROD-D13 · `linkProduct`
```yaml
{id: SPARK-PROD-D13, operation: linkProduct, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M14):** `PUT` link — **throws on backend error** (only mutation that does). **Target:** `@DgsMutation`; port `throwOnError` as a checked exception. **Acceptance:** 1. links parent/child. 2. backend error → exception (not null). **Tests:** ☐ link ☐ error→exception.

### SPARK-PROD-D14 · `unlinkProduct`
```yaml
{id: SPARK-PROD-D14, operation: unlinkProduct, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M15):** `PUT` unlink. **Target:** `@DgsMutation`. **Acceptance:** 1. unlinks parent/child. **Tests:** ☐ unlink.

### SPARK-PROD-D15 · `addProductRule`
```yaml
{id: SPARK-PROD-D15, operation: addProductRule, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M16):** `POST …/spark_rules/v1`. **Target:** `@DgsMutation` → `ProductRules`. **Acceptance:** 1. creates rule. **Tests:** ☐ create.

### SPARK-PROD-D16 · `updateProductRule`
```yaml
{id: SPARK-PROD-D16, operation: updateProductRule, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M17):** `PUT …/spark_rules/v1/{id}`. **Target:** `@DgsMutation`. **Acceptance:** 1. updates rule. **Tests:** ☐ update.

### SPARK-PROD-D17 · `deleteProductRule`
```yaml
{id: SPARK-PROD-D17, operation: deleteProductRule, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductRuleDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M18):** `DELETE …/spark_rules/v1/{id}` → Boolean. **Target:** `@DgsMutation`. **Acceptance:** 1. deletes; returns Boolean. **Tests:** ☐ delete ☐ not-found.

### SPARK-PROD-D18 · `updateComponentStatus` (bulk)
```yaml
{id: SPARK-PROD-D18, operation: updateComponentStatus, type: mutation, category: CAT-2, phase: D, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductMutationDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (M19):** bulk `PUT ${v1}/component_status_update/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. bulk-updates component statuses. **Tests:** ☐ bulk ☐ integration.

---

### Phase E — Complex Operations

### SPARK-PROD-E01 · `productBusinessPartnerActions` (REMOVE/DROP/UNDROP)
```yaml
{id: SPARK-PROD-E01, operation: productBusinessPartnerActions, type: mutation, category: CAT-2, phase: E, complexity: Very High, depends_on: [SPARK-PROD-A06], ext_services: [{key: sampleV2, severity: YELLOW}, {key: recentlyViewed, severity: BLUE}, {key: todo, severity: BLUE}, {key: favorite, severity: BLUE}], files: [plm-product/.../service/ProductBusinessPartnerActionService.kt], blocked_by: none}
```
**As a** DGS engineer **I want** the partner-action dispatcher with a failure strategy **so that** drop/undrop
stays consistent across cleanup services.
**Current Behaviour (M10):** ~220-line dispatcher, 3 cases (`REMOVE_PARTNER`/`DROP_PARTNER`/`UNDROP_PARTNER`).
Partner update + cleanup across `recentlyViewed`/`todo`/`favorite`/`sampleV2`/accessControl. No rollback. (ACL context.)
**Target:** `ProductBusinessPartnerActionService` with 3 strategy methods; **PO decision** saga vs compensation-log vs best-effort. **Acceptance:** 1. all 3 paths reach REST parity (recorded fixtures). 2. partial-failure compensation log/strategy. 3. cleanup fan-out runs per case. **Tests:** ☐ REMOVE ☐ DROP ☐ UNDROP ☐ partial-failure ☐ parity.

### SPARK-PROD-E02 · `updateComponentStatuses` (5-loader fan-out)
```yaml
{id: SPARK-PROD-E02, operation: updateComponentStatuses, type: mutation, category: CAT-2, phase: E, complexity: High, depends_on: [SPARK-PROD-A06], ext_services: [{key: claim, severity: YELLOW}], files: [plm-product/.../service/ComponentStatusFanoutService.kt], blocked_by: none}
```
**Current Behaviour (M20):** parallel fan-out to `bom`/`measurement`/`productDetail`/`packaging` (internal) + `claim` (🟡 EXT). **Shadow-var bug** noted. **Target:** `coroutineScope { launch {…} } ×5` with structured concurrency; claim via `ClaimClient`. Fix the shadow var. **Acceptance:** 1. per-loader failures don't fail siblings. 2. shadow var fixed. 3. parity. **Tests:** ☐ 5-way fan-out ☐ partial failure isolation ☐ parity.

### SPARK-PROD-E03 · `getProductTechPackCountV1` stub + aggregation facade (Option D Phase 1)
```yaml
{id: SPARK-PROD-E03, operation: getProductTechPackCountV1, type: query, category: CAT-2, phase: E, complexity: Very High, depends_on: [SPARK-PROD-A05], ext_services: [{key: attachment, severity: RED}, {key: search, severity: RED}], files: [plm-product/.../dataFetcher/TechPackDataFetcher.kt, plm-product/.../client/TechPackAggregatorClient.kt], blocked_by: none}
```
**As a** DGS engineer **I want** the TechPack query served by a thin stub over an aggregation facade **so that**
it works on day 1 while per-subgraph federation is sequenced.
**Current Behaviour (Q8 / helper):** the 17-step `getTechPackResourceCountMap` (ACL tree ×2, attachment hydration, 7 parallel elastic, critical-discussion→attachment join, build `ResourcesCount`). See [02 §Helper](./02-resolver-analysis.md).
**Target (Option D Phase 1):** `@DgsQuery getProductTechPackCountV1(...)` → `TechPackAggregatorClient.getCount(...)` (Feign to a facade extracted from `getTechPackResourceCountMap`); `@DgsEntityFetcher(name="ResourcesCount")` rebuilds the entity from `_entities`. **PO decision:** Node extract vs Kotlin aggregation service. See [reference-federation-patterns.md §3](../scripts/reference-federation-patterns.md). **Deps:** A05.
**Acceptance:** 1. returns populated `ResourcesCount` from the facade. 2. entity fetcher reconstructs from key+context. 3. parity vs source for 5 inputs. 4. facade observable. **Tests:** ☐ facade call ☐ entity fetcher ☐ parity 5 inputs ☐ integration.

### SPARK-PROD-E04 · `getProductTechPackBulkCountV1` (bulk wrapper, ordering fix)
```yaml
{id: SPARK-PROD-E04, operation: getProductTechPackBulkCountV1, type: query, category: CAT-2, phase: E, complexity: Very High, depends_on: [SPARK-PROD-E03], ext_services: [{key: attachment, severity: RED}, {key: search, severity: RED}], files: [plm-product/.../dataFetcher/TechPackDataFetcher.kt], blocked_by: none}
```
**Current Behaviour (Q9):** `Promise.all(bulk.map(getTechPackResourceCountMap))` — **latent ordering bug** (result order = completion order). **Target:** bulk facade endpoint; **return in input order** (key/sort by productId). **Deps:** E03. **Acceptance:** 1. `bulk(P1..Pn) == [single(P1)..single(Pn)]` in input order. 2. empty list → []. **Tests:** ☐ order preserved ☐ empty ☐ parity.

---

### Phase F — Federation & Stitching (TechPack federate + gateway + decisions)

### SPARK-PROD-F01..F08 · Per-subgraph `extend type ResourcesCount` (placeholders, BLOCKED-BY owning domain)
```yaml
{id: SPARK-PROD-F01, operation: "ResourcesCount.*", type: field-resolver, category: CAT-4, phase: F, complexity: Medium, depends_on: [SPARK-PROD-E03], ext_services: [], files: [<owning-domain>/.../schema, dataFetcher], blocked_by: "<owning domain>"}
```
**Monorepo split:** `ResourcesCount` is owned by `product` in the `plm-product` subgraph. Fields owned by
**co-located** domains (`measurementSets`→measurement, `productBoms`/`packagingBoms`/`boms`→bom) are filled by
**internal** `@DgsData` (CAT-2, same subgraph — these are `SPARK-MEAS-F.../SPARK-BOM-F02` internal stories,
not gateway federation). Fields owned by **separate DGS subgraphs** use true federation
(`extend type ResourcesCount @key(fields:"productId partnerId")` + `@DgsEntityFetcher`), with full bodies in
each owning domain's `04-stories.md`. See [reference-federation-patterns.md §0/§3](../scripts/reference-federation-patterns.md).

| Story | Owner | Fields | Mechanism |
|---|---|---|---|
| F01 | Attachment | `productAttachments`, `discussionAttachments` | **federation** — BLOCKED-BY attachment domain |
| F02 | Discussion | `discussions` | **federation** — BLOCKED-BY discussion domain |
| F03 | Sample | `sample` | **federation** — BLOCKED-BY sample domain |
| F04 | Measurement | `measurementSets` | **internal** (same subgraph) — see [measurement F-stories](../measurement/04-stories.md) |
| F05 | Claim | `claims` | **federation** — BLOCKED-BY claim domain |
| F06 | BOM | `productBoms`, `packagingBoms`, `boms` | **internal** (same subgraph) — see [bom F02](../bom/04-stories.md) |
| F07 | Construction | `constructions` | **federation** — BLOCKED-BY construction domain |
| F08 | Watchlist | `watchlists` | **internal** (same subgraph) — see [watchlist F-stories](../watchlist/04-stories.md) |

**Acceptance (federated F01/F02/F03/F05/F07):** the field resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade.
**Acceptance (internal F04/F06/F08):** the field resolves in-process; no gateway hop; parity vs facade. **Tests:** ☐ field resolves ☐ parity.

### SPARK-PROD-F09 · Retire the TechPack aggregation facade
```yaml
{id: SPARK-PROD-F09, operation: "techpack-facade-retire", type: field-resolver, category: CAT-4, phase: F, complexity: Low, depends_on: [SPARK-PROD-F01, SPARK-PROD-F02, SPARK-PROD-F03, SPARK-PROD-F04, SPARK-PROD-F05, SPARK-PROD-F06, SPARK-PROD-F07, SPARK-PROD-F08], ext_services: [], files: [plm-product/.../dataFetcher/TechPackDataFetcher.kt], blocked_by: none}
```
**Target:** remove `TechPackAggregatorClient`; `TechPackDataFetcher` returns key+context only; decommission the facade. **Acceptance:** 1. all 11 `ResourcesCount` fields resolve via federation. 2. facade health-check 404. 3. no orphaned config. **Tests:** ☐ all fields via federation ☐ no facade alerts.

### SPARK-PROD-F10 · Hive Gateway supergraph composition
```yaml
{id: SPARK-PROD-F10, operation: "gateway-compose", type: field-resolver, category: CAT-4, phase: F, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [], files: [gateway/supergraph-config], blocked_by: none}
```
**Target:** add `plm-product` subgraph URL; verify composition with VMM/IG/CORONA/Doppler stubs; smoke-test cross-subgraph query. **Acceptance:** 1. supergraph composes. 2. cross-subgraph smoke test passes. **Tests:** ☐ compose ☐ smoke.

### SPARK-PROD-F11 · Platform stub verification (VMM/IG/Doppler/CORONA/APEX)
```yaml
{id: SPARK-PROD-F11, operation: "platform-stub-verify", type: field-resolver, category: CAT-4, phase: F, complexity: Low, depends_on: [SPARK-PROD-F10], ext_services: [], files: [gateway/tests], blocked_by: none}
```
**Target:** confirm the gateway resolves full platform types from product-emitted `@key` stubs. **Acceptance:** 1. each platform type resolves via its stub key. **Tests:** ☐ VMM ☐ IG ☐ Doppler ☐ CORONA.

### SPARK-PROD-F12 · Deferred partner-wrapper decision (drift mutations)
```yaml
{id: SPARK-PROD-F12, operation: "drift-wrappers", type: schema, category: CAT-4, phase: F, complexity: Low, depends_on: [SPARK-PROD-E01], ext_services: [], files: [plm-product/.../schema/product.graphqls], blocked_by: none}
```
**Current Behaviour:** `removeProductBusinessPartner`/`dropProductBusinessPartner`/`unDropProductBusinessPartner` are schema-drift wrappers; traffic routes through `productBusinessPartnerActions`. **Target:** PO decides delete vs keep `@deprecated`; implement. **Acceptance:** 1. traffic survey complete. 2. decision implemented. **Tests:** ☐ schema diff intentional.

---

### Phase G — Field Resolvers, Bug-fixes, Utils, Tests (one story per group)

### SPARK-PROD-G01 · `Product.attachmentsWithMetaData`
```yaml
{id: SPARK-PROD-G01, operation: "Product.attachmentsWithMetaData", type: field-resolver, category: CAT-2, phase: G, complexity: Very High, depends_on: [SPARK-PROD-A02, SPARK-PROD-A06], ext_services: [{key: attachment, severity: RED}, {key: relationship, severity: YELLOW}], files: [plm-product/.../service/AttachmentEnrichmentService.kt], blocked_by: none}
```
**Current Behaviour (Phase 2C):** ~150 ln — `relationship.searchByIds` → 5-bucket partition → v2+v3 attachment hydration → discussions/threads/samples batched → 5-source merge → draft filter → `orderProductAttachments`. **Target:** `AttachmentEnrichmentService` Kotlin port; keep the "ACL should do draft filter" TODO as a follow-up. **Acceptance:** 1. parity for mixed attachment/discussion/thread/sample. 2. ordering rank preserved (product=0, discussion=1, sample=2; createdAt DESC tiebreak). **Tests:** ☐ merge ☐ ordering ☐ parity.

### SPARK-PROD-G02 · `Product.components`
```yaml
{id: SPARK-PROD-G02, operation: "Product.components", type: field-resolver, category: CAT-2, phase: G, complexity: Very High, depends_on: [SPARK-PROD-A02, SPARK-PROD-A06], ext_services: [{key: search, severity: RED}], files: [plm-product/.../service/ComponentsAggregationService.kt], blocked_by: none}
```
**Current Behaviour (Phase 2C):** ~190 ln — 4 parallel elastic (measurement/claim/bom/productDetail) + packaging + **per-claim N+1 ACL** + 5-type merge + count rollups. **Target:** refactor N+1 ACL into a batched call; preserve type tagging + `cloneDeep(initialCountsByBp)`. **Acceptance:** 1. parity for 50+ components. 2. `archivedCount`/`countByComponents` match source. 3. ACL batched (no N+1). **Tests:** ☐ merge ☐ counts ☐ batched ACL ☐ parity.

### SPARK-PROD-G03 · `Product.attachments` + `attachmentsV3` + `attachmentSummary` + `ProductTemplate.attachmentsData`
```yaml
{id: SPARK-PROD-G03, operation: "Product.attachments*", type: field-resolver, category: CAT-2, phase: G, complexity: High, depends_on: [SPARK-PROD-G01], ext_services: [{key: attachment, severity: RED}, {key: search, severity: RED}], files: [plm-product/.../dataFetcher/ProductAttachmentFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** four related resolvers sharing `AttachmentEnrichmentService` (G01). **Target:** thin `@DgsData` fields over the shared service. **Acceptance:** 1. each field returns its shape. 2. shares G01 service. **Tests:** ☐ each field ☐ parity.

### SPARK-PROD-G04 · `ProductsCategories.categories` (12-case) + `DopplerDepartment` fields
```yaml
{id: SPARK-PROD-G04, operation: "ProductsCategories.categories", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A04], ext_services: [{key: doppler, severity: BLUE}], files: [plm-product/.../dataFetcher/CategoriesFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** 12-branch dispatcher; `DopplerDepartment.primary/secondaryCapacityTypeName` share one Doppler call (memoized). **Target:** Kotlin dispatcher → 12 helpers; Doppler via DataLoader. **Acceptance:** 1. each category type built correctly. 2. Doppler fetched once. **Tests:** ☐ 12 cases ☐ single doppler fetch.

### SPARK-PROD-G05 · `Product.samples` + `sampleIds` + `elasticSamplesList`
```yaml
{id: SPARK-PROD-G05, operation: "Product.samples*", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: sampleV2, severity: YELLOW}, {key: search, severity: RED}], files: [plm-product/.../dataFetcher/ProductSampleFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** **stops reading `info.variableValues`** — pass explicit args from the query layer (contract change). **Target:** explicit args; document the contract change. **Acceptance:** 1. samples/sampleIds/elastic resolve. 2. no `info.variableValues` read. **Tests:** ☐ samples ☐ contract change ☐ parity.

### SPARK-PROD-G06 · `Product.teams` + `discussionsV2` + `discussionsCount` + `workspaces`
```yaml
{id: SPARK-PROD-G06, operation: "Product.teams+discussions", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: teamV2, severity: YELLOW}, {key: discussion, severity: YELLOW}, {key: search, severity: RED}, {key: workspaceV2, severity: RED}], files: [plm-product/.../dataFetcher/ProductTeamDiscussionFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** team/discussion/workspace elastic lookups. **Target:** federated references + elastic. **Acceptance:** 1. each field resolves. **Tests:** ☐ teams ☐ discussions ☐ workspaces ☐ parity.

### SPARK-PROD-G07 · `Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status`
```yaml
{id: SPARK-PROD-G07, operation: "Product.partners+status", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: vmm, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductPartnerFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** `loadBps`/`loadBpsWithType` (VMM); `status` merges partner/workspace statuses. **Target:** `vmmUtils` Kotlin port; preserve int-parse normalization. **Acceptance:** 1. partners resolve via VMM. 2. `status` merge correct. **Tests:** ☐ partners ☐ status merge ☐ parity.

### SPARK-PROD-G08 · `Product.measurementSets` + `claims` + `bom` + `productBom` + `packagingBom` + `productDetails` + `variations` + `associateProductsAsks`
```yaml
{id: SPARK-PROD-G08, operation: "Product.siblings", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../dataFetcher/ProductSiblingFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** sibling-domain passthroughs with `includeXxx` boolean branches — **internal same-DGS calls** (not cross-subgraph). **Target:** internal service calls to the co-located sibling services. **Acceptance:** 1. each sibling field resolves internally. 2. `includeXxx` branches honored. **Tests:** ☐ each field ☐ include branch ☐ parity.

### SPARK-PROD-G09 · `Product.productWorkspaceAttributes` + `productWorkspaceInfo`
```yaml
{id: SPARK-PROD-G09, operation: "Product.workspaceAttrs", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: workspaceV2, severity: RED}, {key: search, severity: RED}, {key: tag, severity: YELLOW}], files: [plm-product/.../dataFetcher/ProductWorkspaceFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** both produce shapes with a **deferred `designCycle: async()=>…`** field-on-value. **Target:** model `designCycle` as a nested `@DgsData`, not an inline closure. **Acceptance:** 1. both fields resolve. 2. `designCycle` is a nested fetcher. **Tests:** ☐ attrs ☐ designCycle nested ☐ parity.

### SPARK-PROD-G10 · `Product.ancestryProducts` + `rating` + `reservedDpcis`
```yaml
{id: SPARK-PROD-G10, operation: "Product.ancestry+rating+dpcis", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: relationship, severity: YELLOW}, {key: rating, severity: BLUE}, {key: apex, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductMiscFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** `rating` via `RatingClient`; `reservedDpcis` via `getReservedDpcisFromApex`. **Target:** federated/Feign references. **Acceptance:** 1. ancestry/rating/dpcis resolve. 2. rating null-on-error. **Tests:** ☐ ancestry ☐ rating ☐ dpcis.

### SPARK-PROD-G11 · `Product.notRemovablePartnerIds` + `notRemovableWorkspaceIds` + `associateProductsAsks` + `variations`
```yaml
{id: SPARK-PROD-G11, operation: "Product.notRemovable", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: vmm, severity: BLUE}, {key: workspaceV2, severity: RED}], files: [plm-product/.../dataFetcher/ProductNotRemovableFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** source utils call into 4–5 sibling field resolvers **reflectively**. **Target:** **replace reflective resolver invocation with direct service-method calls** (same logical union). **Acceptance:** 1. same results as source. 2. no reflective resolver calls. **Tests:** ☐ union correctness ☐ no reflection ☐ parity.

### SPARK-PROD-G12 · `Product.division` **bug fix** (wrong loader)
```yaml
{id: SPARK-PROD-G12, operation: "Product.division", type: field-resolver, category: CAT-2, phase: G, complexity: Low, depends_on: [SPARK-PROD-A06], ext_services: [{key: ig, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductHierarchyFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** source `Product.division` (and `DopplerDepartment.division`) call `ig.department.getByID` instead of `ig.division.getByID` — **latent bug**. **Target:** wire to `DivisionService`; **PO decision** whether to feature-flag the fix during cutover (clients may depend on department-shaped result). **Acceptance:** 1. returns true division shape. 2. fix logged with PO; flag decision recorded. **Tests:** ☐ division shape ☐ contract parity expectation documented.

### SPARK-PROD-G13 · IG/tag/tcin/spg + template trivial-field group
```yaml
{id: SPARK-PROD-G13, operation: "Product.hierarchy+misc", type: field-resolver, category: CAT-2, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [{key: ig, severity: BLUE}, {key: tag, severity: YELLOW}, {key: corona, severity: BLUE}], files: [plm-product/.../dataFetcher/ProductTrivialFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** `department`/`departments`/`clazz`/`brand`/`brands`/`divisions`/`productTemplateDepartments`, `tags`, `tcins`, `SPARK_Tcin.itemDetails` (CORONA), `SPARK_PackagingAttribute.spg` (internal fileLibrary), `SPARK_ProductRules.*`, `VMM_BusinessPartnerCategory.*`, `MasterProductStatus.*`. **Target:** group into one PR; federated/internal references. **Acceptance:** 1. each field resolves to the right source. **Tests:** ☐ hierarchy ☐ tcin/CORONA ☐ spg internal.

### SPARK-PROD-G14 · Simple user/status fields + trivial pass-throughs (bundle)
```yaml
{id: SPARK-PROD-G14, operation: "trivial-passthroughs", type: field-resolver, category: CAT-2, phase: G, complexity: Low, depends_on: [SPARK-PROD-A02], ext_services: [{key: userAttributes, severity: YELLOW}], files: [plm-product/.../dataFetcher/ProductSimpleFieldDataFetcher.kt], blocked_by: none}
```
**Current Behaviour:** `createdBy`/`updatedBy`/`versionCreatedBy` (user-profile), `ProductComponentStatus.updatedBy`, `SPARK_ResourcesCount.productThumbnailId` (re-fetch product), plus ~60 direct scalar pass-throughs (DTO-mapped). **Target:** thin `@DgsData` for user/thumbnail; Jackson DTO mapping for scalars. **Acceptance:** 1. user fields resolve (null id → null). 2. `productThumbnailId` re-fetches. 3. scalars mapped. **Tests:** ☐ user fields ☐ thumbnail ☐ scalar mapping.

### SPARK-PROD-G15 · Port product utils to Kotlin
```yaml
{id: SPARK-PROD-G15, operation: "utils-port", type: service, category: CAT-3, phase: G, complexity: Medium, depends_on: [SPARK-PROD-A06], ext_services: [], files: [plm-product/.../util/*.kt], blocked_by: none}
```
**Current Behaviour:** `attachmentUtils`, `partnerUtils`, `teamUtils`, `productUtils`, `componentStatusUtils`, `resolvePaging`, `vmmUtils`, `accessControlUtils`, `removePartnerUtils`. **Target:** Kotlin ports; single camel/snake normalization at the Feign boundary; **fix** `componentStatusUtils.incrementAllContextCounter` (never resets — verify intent); batch `getAccessControlBatch` with parallel chunking. **Acceptance:** 1. utils ported with unit tests. 2. counter logic fixed/verified. 3. ACL batch parallel-chunked. **Tests:** ☐ each util ☐ counter ☐ ACL chunking.

### SPARK-PROD-G16 · Test coverage, parity harness, load & cut-over rehearsal
```yaml
{id: SPARK-PROD-G16, operation: "tests", type: tests, category: CAT-5, phase: G, complexity: High, depends_on: [SPARK-PROD-C01, SPARK-PROD-E01, SPARK-PROD-E03, SPARK-PROD-G01, SPARK-PROD-G02], ext_services: [], files: [plm-product/.../test/*.kt], blocked_by: none}
```
**Target:** ≥80% unit coverage; parity harness ≥50 fixtures (incl. TechPack, partner actions, components, attachmentsWithMetaData, the division-bug-fix, rules flag both paths); load test p95 for `getProduct`/`getProducts`/`components`/`attachmentsWithMetaData`/TechPack; contract test (schema diff shows only intentional changes); cut-over rehearsal (shadow traffic). **Acceptance:** 1. unit ≥80%. 2. ≥50 parity fixtures green. 3. load p95 parity. 4. schema-diff intentional-only. 5. shadow-traffic rehearsal + rollback drill. **Tests:** ☐ parity ☐ load ☐ contract ☐ shadow.

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| TechPack composite-key aggregate (E03/E04) | High | High | Option D facade-then-federate; bulk-order fix | Tech Lead + Platform |
| `productBusinessPartnerActions` partial failure (E01) | Medium | High | Saga/compensation — PO decision | Tech Lead |
| `components` N+1 ACL regression (G02) | Medium | Medium | Batch ACL on port | Backend Eng |
| `attachmentsWithMetaData` perf (G01) | Medium | High | Parallel fetch + cached relationship walk | Backend Eng |
| `Product.division` bug fix (G12) breaks clients | Medium | Medium | Feature-flag + client survey | PO |
| 8 TechPack placeholders block on 8 domains | High | Medium | Facade keeps day-1 function; retire only when all live | Tech Lead |
| `USE_NEW_RULES_API` legacy delete | Low | High | Verify all envs; staged rollout | PO |
| Drift wrappers may have live consumers | Medium | Medium | Traffic survey (F12) | PO |
| External rating secret | Low | Medium | Vault | Platform |

## 5. Summary
- **Stories:** 72 (A:6 · B:11 · C:5 · D:18 · E:4 · F:12 · G:16).
- **Critical path:** A01→A02/A06→C01→E03(TechPack facade)→G01→G02→G16.
- **Highest risk:** TechPack (E03/E04), `productBusinessPartnerActions` (E01).
- **Host DGS:** product is the home of the whole product family; co-located siblings resolve internally.

---
**Phase Completed:** Phase 4 — Migration Stories · **Domain:** `product` · **Outputs:** 04-stories.md, 04-stories-index.yaml, 04-po-summary.md.
