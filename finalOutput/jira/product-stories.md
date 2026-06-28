# product — Jira stories (paste one block per issue)

> **Epic:** Product → plm-product DGS migration  ·  **Labels:** `dgs-migration`, `product`, `<type>`
> Create the Epic first, then paste each block below as a new Story's description.
> Story points are AI-derived from complexity (confirm in refinement). See [README.md](./README.md).

## SPARK-PROD-A01 · Schema skeleton + scalars
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** —
**Labels:** `dgs-migration`, `product`, `schema`

**As a** DGS engineer **I want** the `product.graphqls` skeleton + federation header + `DateTime`/`JsonNode`
scalars **so that** all later product work compiles. **Current Behaviour:** green-field (schema translated from `code/schemas/SPARK_Product.txt`).
**Target:** v2.3 `@link`, `scalar DateTime→Instant`, `scalar JsonNode`, empty `extend type Query`/`Mutation`.
**Files:** `schema/product.graphqls`, `config/ScalarConfig.kt`. **Deps:** none.
**Acceptance:** 1. `./gradlew generateJava` passes. 2. scalars round-trip. **Tests:** ☐ compiles ☐ scalar serde.

---

## SPARK-PROD-A02 · Owned types + inputs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A01
**Labels:** `dgs-migration`, `product`, `schema`

**As a** DGS engineer **I want** ~40 owned types + ~30 inputs from [03-schema.graphql](./03-schema.graphql)
**so that** resolvers/mutations have a contract. **Target:** `@key(fields:"id")` on `Product`/`ProductRules`;
`@shareable` on `Paging`/`Pageable`/`CodeDescription`/`CodeDescriptionOrder`/`AccessV3`/`WorkspaceStatus`/
`ResourcePermissions`/`PermissionEntry`/`SpgFileLibrary`. **Deps:** A01.
**Acceptance:** 1. All owned types+inputs present. 2. Keys/shareables applied. 3. Schema validates. **Tests:** ☐ validates ☐ entity stub.

---

## SPARK-PROD-A03 · External stubs (platform + sibling)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A01
**Labels:** `dgs-migration`, `product`, `schema`

**Target:** 6 platform stubs (`VMM_*`, `IG_*`, `DopplerCapacityType`, `CORONA_ItemDetails`) + ~16 sibling
stubs per [03-schema.graphql §1](./03-schema.graphql). Note co-located stubs resolve internally at runtime.
**Deps:** A01. **Acceptance:** 1. all stubs compile; gateway composes. **Tests:** ☐ compiles ☐ gateway resolves a VMM stub.

---

## SPARK-PROD-A04 · Categories union @DgsTypeResolver
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A02, SPARK-PROD-A03
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour (Phase 2):** 12-case switch over `category.type`, **default → `IG_Clazz_Filter`**.
**Target:** `@DgsTypeResolver(name="Categories")` mirroring the 12 cases + default. **Deps:** A02, A03.
**Acceptance:** 1. all 12 known tags map correctly. 2. unknown → `IG_Clazz_Filter`. **Tests:** ☐ 12 cases ☐ default.

---

## SPARK-PROD-A05 · ResourcesCount composite-key type
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A01
**Labels:** `dgs-migration`, `product`, `schema`

**Target:** add the composite-key type with 11 stub fields, each commented with its owning subgraph (see
[03-schema.graphql §3](./03-schema.graphql)). Product owns the type + stub resolver; siblings extend later (Phase F).
**Deps:** A01. **Acceptance:** 1. `@key` = `productId partnerId`; context fields not in key. 2. stub fields annotated. **Tests:** ☐ compiles ☐ entity fetcher stub.

---

## SPARK-PROD-A06 · ProductService Kotlin port (42 methods)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-PROD-A01
**Labels:** `dgs-migration`, `product`, `service`

**Current Behaviour (Phase 2 §Service):** 42 REST wrappers against `v1`/`v2`, elastic, `spark_rules`, external rating.
**Target:** split into `ProductReadService`, `ProductWriteService`, `ProductElasticService`, `ProductCopyService`,
`ProductRuleService`, `ProductComponentStatusService`, `RatingClient` (Feign, external), plus internal calls for
co-located ops. Master/status reads `@Cacheable`. Preserve `getByID` priming, `linkProduct` `throwOnError`,
external-rating API-key (→ Vault). **ACL note (context):** capability-token currying is omitted (ACL ignored).
**Deps:** A01. **Acceptance:** 1. all 42 signatures present. 2. co-located methods make no outbound HTTP. 3. rating secret in config/Vault. 4. `linkProduct` throws on backend error. **Tests:** ☐ endpoint build ☐ cache hit ☐ rating parse ☐ linkProduct throws.

---

### Phase B — Core Reads (one query per story)

> Pattern: `@DgsQuery` → `ProductReadService.method`. Full pseudo-logic in [02 §Query Resolvers](./02-resolver-analysis.md). All depend on A02+A06.

---

## SPARK-PROD-B01 · getProduct
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A02, SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q3):** `getByID.load(id)` `GET ${v1}?productId={id}` → camelCase or null; DataLoader-batched.
**Target:** `@DgsQuery getProduct(id): Product` via `ProductDataLoader` keyed on id. **Acceptance:** 1. returns product; 404→null. 2. batches N ids in 1 call. **Tests:** ☐ happy ☐ 404→null ☐ batch ☐ integration.

---

## SPARK-PROD-B02 · getProductsByIds
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A02, SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q6):** `getByIdList.load(ids)` `GET ${v1}?productId={csv}&page=0&size=10000&sort=createdDate,desc`; primes `getByID`. **Target:** `@DgsQuery` → `ProductsPaged`. **Acceptance:** 1. returns paged products for ids. 2. primes single-id loader. **Tests:** ☐ happy ☐ empty ☐ integration.

---

## SPARK-PROD-B03 · getProductStatus (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q7):** `getStatus.load()` master status list. **Target:** `@DgsQuery` → `@Cacheable` → `[MasterProductStatus]`. **Acceptance:** 1. returns statuses. 2. cached. **Tests:** ☐ list ☐ cache hit.

---

## SPARK-PROD-B04 · getProductVersions
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q10):** `getVersions.load({id})` `GET ${v1}/{id}/versions?page=0&size=10000`. **Target:** `@DgsQuery` → `ProductsPaged`. **Acceptance:** 1. returns versions. **Tests:** ☐ happy ☐ integration.

---

## SPARK-PROD-B05 · getCopyStatus
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q4):** `getCopyStatus.load(id)` `GET ${v2}/count/resource-type?copyId={id}`. **Target:** `@DgsQuery` → `ProductCopy`. **Acceptance:** 1. returns copy status. **Tests:** ☐ happy ☐ integration.

---

## SPARK-PROD-B06 · getProductTemplateById
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q18):** `getByID.load(id)` → `response || {}` (empty object on miss — **preserve**). **Target:** `@DgsQuery getProductTemplateById(id): Product`. **Acceptance:** 1. returns product or empty object (not null). **Tests:** ☐ happy ☐ miss→{}.

---

## SPARK-PROD-B07 · getProductRules
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q12):** `getAllRules.load()` `GET ${base}/spark_rules/v1` → `content`. **Target:** `@DgsQuery` → `[ProductRules]`. **Acceptance:** 1. returns rules content. **Tests:** ☐ list ☐ integration.

---

## SPARK-PROD-B08 · getProductRulesById
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q13):** `getRuleById.load(id)` `GET ${base}/spark_rules/v1/{id}`. **Target:** `@DgsQuery` → `ProductRules`. **Acceptance:** 1. returns rule. **Tests:** ☐ happy ☐ 404.

---

## SPARK-PROD-B09 · getAllAvailableRules
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q14):** `getAvailableRules.load()` `GET …/spark_rules/v1/rules`. **Target:** `@DgsQuery` → `[AvailableRules]`. **Acceptance:** 1. returns available rules. **Tests:** ☐ list.

---

## SPARK-PROD-B10 · getProductDeptRules (flag fork)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q15):** **flag fork** `USE_NEW_RULES_API ? ruleLibrary.searchRuleLibrary : product.searchProductDeptRules` `GET …/spark_rules/v1/search?productIds=&departmentIds=&activeOnly=`. **PO decision:** flag cutover (rules may move to spark-tag DGS). **Target:** `@DgsQuery`; both code paths covered. **Acceptance:** 1. default `activeOnly=true`. 2. flag selects the correct backend. **Tests:** ☐ legacy path ☐ flag path ☐ parity.

---

## SPARK-PROD-B11 · getProductBPRules (flag fork)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q16):** same as B10 with `businessPartnerIds`. **Target:** `@DgsQuery`. **Acceptance:** 1. flag fork honored; BP filter applied. **Tests:** ☐ legacy ☐ flag ☐ parity.

---

### Phase C — Search & Listing

---

## SPARK-PROD-C01 · getProducts (two-stage hydration)
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**As a** DGS engineer **I want** `getProducts` with elastic+canonical two-stage hydration **so that** listing
returns canonical records enriched with elastic flags.
**Current Behaviour (Q1):** (🔴 search) `getFilteredProductsListing({resourceType ?? 'products', includeBoms ?? true, includeClaims ?? true, includeMeasurementSets ?? true, includeProductDetails ?? true, filter ?? [], q ?? '', page, size})` → ids → (internal) `getPage({products:ids, page:0, size})` `GET ${v1}?productId=&sort=createdDate,desc` → merge elastic flags (`boms, productDetails, claims, measurementSets, samples, sampleIds, hasSamplesUpcomingDue, hasNotEvaluatedReceivedSamples, receivedNotEvaluatedCount`) onto canonical records. **Boolean defaults are truthy (`?? true`) — pin in tests.**
**EXT:** 🔴 search. **Target:** `ProductElasticService.getFilteredProductsListing` then `ProductReadService.getPage`; merge. **Deps:** A06.
**Acceptance:** 1. parity for 4 arg combos (no flags / all flags / resourceType=workspaces / filter array). 2. truthy defaults preserved. 3. elastic flags merged onto canonical. **Tests:** ☐ 4 combos ☐ default truthiness ☐ merge ☐ parity.

---

## SPARK-PROD-C02 · getProductTemplates
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q2):** (🔴 search) `getFilteredProductsListing({resourceType:'product', includeBoms:false, ...7 includeXxxTemplates flags, types})` → return elastic response (no 2nd hydration). **Target:** `@DgsQuery` → `ProductTemplatesList`. **Acceptance:** 1. all 7 template-include flags forwarded. 2. `types:[Int]` filter applied. **Tests:** ☐ flags ☐ types filter ☐ parity.

---

## SPARK-PROD-C03 · getCategories
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A04, SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q5):** default `productType ?? 100`; (🔴 search) `getProductCategories` `GET ${elastic}/search/${snake_case(type)}?resourceType=&resourceId=&productType=` → `ProductsCategories` (polymorphic `categories` via A04). **Target:** `@DgsQuery`; preserve `snakeCase(type)` in the path. **Acceptance:** 1. `snake_case(type)` path exact. 2. wires to `Categories` union. **Tests:** ☐ snake-case path ☐ union dispatch ☐ parity.

---

## SPARK-PROD-C04 · getRatingByTcin (external)
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q11):** (🔵 external) `GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={API_KEY}` (`skipJsonParse`) → `JSON.parse` → `{averageRating, reviewCount}`; **catch → null** (silent). **Target:** `RatingClient` Feign (text/plain, manual parse); secret from Vault. **Acceptance:** 1. parses statistics to `Rating`. 2. any error → null. 3. API key from config/Vault, not source. **Tests:** ☐ parse ☐ error→null ☐ secret config.

---

## SPARK-PROD-C05 · searchProductRules
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q17):** flag fork; legacy `GET …/spark_rules/v1/search_mapped?...` → `productRuleResponseTransformer` → camelCase. **Target:** `@DgsQuery`; port the transformer. **Acceptance:** 1. flag fork honored. 2. legacy response transformed correctly. **Tests:** ☐ legacy transform ☐ flag path ☐ parity.

---

### Phase D — Mutations (simple, one per story)

> Pattern: `@DgsMutation` → `ProductWriteService.method`. Pseudo-logic in [02 §Mutation Resolvers](./02-resolver-analysis.md). All depend on A06. ACL is context-only.

---

## SPARK-PROD-D01 · addProduct
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M1):** `POST ${v1}` + optional `copyProductToProduct(copyProduct)` + workspace association. **Target:** `@DgsMutation addProduct(workspaceId, sparkProduct, copyProduct): Product`; orchestrate create→copy→assoc. **Acceptance:** 1. creates product. 2. optional copy runs when `copyProduct` present. 3. workspace assoc applied. **Tests:** ☐ create ☐ create+copy ☐ create+assoc ☐ integration.

---

## SPARK-PROD-D02 · addProducts (bulk)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M2):** bulk `POST ${v1}/bulk` + attachment-link side-effects (no rollback — **preserve, flag**). **Target:** `@DgsMutation` → `ProductBulkType`. **Acceptance:** 1. bulk creates. 2. attachment links applied; no-rollback behaviour documented. **Tests:** ☐ bulk ☐ links ☐ integration.

---

## SPARK-PROD-D03 · bulkUpdateProducts
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M3):** `PUT ${v1}/mass_update`. **Target:** `@DgsMutation` → `ProductBulkType`. **Acceptance:** 1. mass-updates products. **Tests:** ☐ bulk update ☐ integration.

---

## SPARK-PROD-D04 · updateProduct
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M4):** `PUT ${v1}/{id}` + optional copy + archive removed-template attachments (template branch). **Target:** `@DgsMutation updateProduct(input, copyProduct): Product`. **Acceptance:** 1. updates product. 2. optional copy. 3. removed-template attachments archived (template branch). **Tests:** ☐ update ☐ copy ☐ template archival.

---

## SPARK-PROD-D05 · carryForwardProduct
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M5):** `PUT ${v1}/{productId}/carry_forward/{workspaceId}` — uses **every** field on `CarryForwardProductInput`. **Target:** `@DgsMutation`; verify full input mapping. **Acceptance:** 1. all input fields mapped to the request. **Tests:** ☐ full mapping ☐ integration.

---

## SPARK-PROD-D06 · addTeamsToProduct
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M6):** `POST ${v1}/{productId}/resources/bulk` + manage_workspace_teams. **Target:** `@DgsMutation`. **Acceptance:** 1. adds teams + new partners + workspace links. **Tests:** ☐ teams ☐ partners ☐ integration.

---

## SPARK-PROD-D07 · addBusinessPartnersToProductWithType
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M7):** `POST ${v1}/{productId}/partners-add/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. adds partners with type. **Tests:** ☐ add ☐ integration.

---

## SPARK-PROD-D08 · removeProductResources
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M8):** `DELETE ${v1}/{productId}/resources/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. removes resources. **Tests:** ☐ remove ☐ integration.

---

## SPARK-PROD-D09 · updateBusinessPartnerStatuses
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M9):** `PUT ${v1}/{productId}/status_update/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. updates partner statuses. **Tests:** ☐ update ☐ integration.

---

## SPARK-PROD-D10 · updateViewToggle
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M11):** `PUT ${v1}` view toggle. **Target:** `@DgsMutation`. **Acceptance:** 1. toggles hidden. **Tests:** ☐ toggle.

---

## SPARK-PROD-D11 · updateWorkspaceAttributes
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M12):** `PUT ${v1}/{productId}` workspace attrs. **Target:** `@DgsMutation`. **Acceptance:** 1. updates workspace attrs. **Tests:** ☐ update.

---

## SPARK-PROD-D12 · updateProductTeamsWorkspaceContext
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M13):** `PUT` team-workspace add/remove. **Target:** `@DgsMutation`. **Acceptance:** 1. adds/removes team-workspace pairs. **Tests:** ☐ add ☐ remove.

---

## SPARK-PROD-D13 · linkProduct (throws on error)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M14):** `PUT` link — **throws on backend error** (only mutation that does). **Target:** `@DgsMutation`; port `throwOnError` as a checked exception. **Acceptance:** 1. links parent/child. 2. backend error → exception (not null). **Tests:** ☐ link ☐ error→exception.

---

## SPARK-PROD-D14 · unlinkProduct
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M15):** `PUT` unlink. **Target:** `@DgsMutation`. **Acceptance:** 1. unlinks parent/child. **Tests:** ☐ unlink.

---

## SPARK-PROD-D15 · addProductRule
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M16):** `POST …/spark_rules/v1`. **Target:** `@DgsMutation` → `ProductRules`. **Acceptance:** 1. creates rule. **Tests:** ☐ create.

---

## SPARK-PROD-D16 · updateProductRule
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M17):** `PUT …/spark_rules/v1/{id}`. **Target:** `@DgsMutation`. **Acceptance:** 1. updates rule. **Tests:** ☐ update.

---

## SPARK-PROD-D17 · deleteProductRule
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M18):** `DELETE …/spark_rules/v1/{id}` → Boolean. **Target:** `@DgsMutation`. **Acceptance:** 1. deletes; returns Boolean. **Tests:** ☐ delete ☐ not-found.

---

## SPARK-PROD-D18 · updateComponentStatus (bulk)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M19):** bulk `PUT ${v1}/component_status_update/bulk`. **Target:** `@DgsMutation`. **Acceptance:** 1. bulk-updates component statuses. **Tests:** ☐ bulk ☐ integration.

---

### Phase E — Complex Operations

---

## SPARK-PROD-E01 · productBusinessPartnerActions
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** Very High  ·  **Points (est.):** 8  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**As a** DGS engineer **I want** the partner-action dispatcher with a failure strategy **so that** drop/undrop
stays consistent across cleanup services.
**Current Behaviour (M10):** ~220-line dispatcher, 3 cases (`REMOVE_PARTNER`/`DROP_PARTNER`/`UNDROP_PARTNER`).
Partner update + cleanup across `recentlyViewed`/`todo`/`favorite`/`sampleV2`/accessControl. No rollback. (ACL context.)
**Target:** `ProductBusinessPartnerActionService` with 3 strategy methods; **PO decision** saga vs compensation-log vs best-effort. **Acceptance:** 1. all 3 paths reach REST parity (recorded fixtures). 2. partial-failure compensation log/strategy. 3. cleanup fan-out runs per case. **Tests:** ☐ REMOVE ☐ DROP ☐ UNDROP ☐ partial-failure ☐ parity.

---

## SPARK-PROD-E02 · updateComponentStatuses (5-loader fan-out)
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `mutation`

**Current Behaviour (M20):** parallel fan-out to `bom`/`measurement`/`productDetail`/`packaging` (internal) + `claim` (🟡 EXT). **Shadow-var bug** noted. **Target:** `coroutineScope { launch {…} } ×5` with structured concurrency; claim via `ClaimClient`. Fix the shadow var. **Acceptance:** 1. per-loader failures don't fail siblings. 2. shadow var fixed. 3. parity. **Tests:** ☐ 5-way fan-out ☐ partial failure isolation ☐ parity.

---

## SPARK-PROD-E03 · getProductTechPackCountV1 stub + facade (Option D)
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** Very High  ·  **Points (est.):** 8  ·  **Depends on:** SPARK-PROD-A05
**Labels:** `dgs-migration`, `product`, `query`

**As a** DGS engineer **I want** the TechPack query served by a thin stub over an aggregation facade **so that**
it works on day 1 while per-subgraph federation is sequenced.
**Current Behaviour (Q8 / helper):** the 17-step `getTechPackResourceCountMap` (ACL tree ×2, attachment hydration, 7 parallel elastic, critical-discussion→attachment join, build `ResourcesCount`). See [02 §Helper](./02-resolver-analysis.md).
**Target (Option D Phase 1):** `@DgsQuery getProductTechPackCountV1(...)` → `TechPackAggregatorClient.getCount(...)` (Feign to a facade extracted from `getTechPackResourceCountMap`); `@DgsEntityFetcher(name="ResourcesCount")` rebuilds the entity from `_entities`. **PO decision:** Node extract vs Kotlin aggregation service. See [reference-federation-patterns.md §3](../scripts/reference-federation-patterns.md). **Deps:** A05.
**Acceptance:** 1. returns populated `ResourcesCount` from the facade. 2. entity fetcher reconstructs from key+context. 3. parity vs source for 5 inputs. 4. facade observable. **Tests:** ☐ facade call ☐ entity fetcher ☐ parity 5 inputs ☐ integration.

---

## SPARK-PROD-E04 · getProductTechPackBulkCountV1 (ordering fix)
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** Very High  ·  **Points (est.):** 8  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `query`

**Current Behaviour (Q9):** `Promise.all(bulk.map(getTechPackResourceCountMap))` — **latent ordering bug** (result order = completion order). **Target:** bulk facade endpoint; **return in input order** (key/sort by productId). **Deps:** E03. **Acceptance:** 1. `bulk(P1..Pn) == [single(P1)..single(Pn)]` in input order. 2. empty list → []. **Tests:** ☐ order preserved ☐ empty ☐ parity.

---

### Phase F — Federation & Stitching (TechPack federate + gateway + decisions)

---

## SPARK-PROD-F01 · ResourcesCount.productAttachments+discussionAttachments (Attachment)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `field-resolver`

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

---

## SPARK-PROD-F02 · ResourcesCount.discussions (Discussion)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `federation`

ResourcesCount.discussions (Discussion)

_(Full detail bundled in ../product/04-stories.md — phase F section.)_

---

## SPARK-PROD-F03 · ResourcesCount.sample (Sample)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `federation`

ResourcesCount.sample (Sample)

_(Full detail bundled in ../product/04-stories.md — phase F section.)_

---

## SPARK-PROD-F04 · ResourcesCount.measurementSets (Measurement — INTERNAL, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `story`

ResourcesCount.measurementSets (Measurement — INTERNAL, same subgraph)

_(Full detail bundled in ../product/04-stories.md — phase F section.)_

---

## SPARK-PROD-F05 · ResourcesCount.claims (Claim)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `federation`

ResourcesCount.claims (Claim)

_(Full detail bundled in ../product/04-stories.md — phase F section.)_

---

## SPARK-PROD-F06 · ResourcesCount.productBoms+packagingBoms+boms (BOM — INTERNAL, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `story`

ResourcesCount.productBoms+packagingBoms+boms (BOM — INTERNAL, same subgraph)

_(Full detail bundled in ../product/04-stories.md — phase F section.)_

---

## SPARK-PROD-F07 · ResourcesCount.constructions (Construction)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `federation`

ResourcesCount.constructions (Construction)

_(Full detail bundled in ../product/04-stories.md — phase F section.)_

---

## SPARK-PROD-F08 · ResourcesCount.watchlists (Watchlist — INTERNAL, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E03
**Labels:** `dgs-migration`, `product`, `story`

ResourcesCount.watchlists (Watchlist — INTERNAL, same subgraph)

_(Full detail bundled in ../product/04-stories.md — phase F section.)_

---

## SPARK-PROD-F09 · Retire TechPack aggregation facade
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-F01, SPARK-PROD-F02, SPARK-PROD-F03, SPARK-PROD-F04, SPARK-PROD-F05, SPARK-PROD-F06, SPARK-PROD-F07, SPARK-PROD-F08
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Target:** remove `TechPackAggregatorClient`; `TechPackDataFetcher` returns key+context only; decommission the facade. **Acceptance:** 1. all 11 `ResourcesCount` fields resolve via federation. 2. facade health-check 404. 3. no orphaned config. **Tests:** ☐ all fields via federation ☐ no facade alerts.

---

## SPARK-PROD-F10 · Hive Gateway supergraph composition
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Target:** add `plm-product` subgraph URL; verify composition with VMM/IG/CORONA/Doppler stubs; smoke-test cross-subgraph query. **Acceptance:** 1. supergraph composes. 2. cross-subgraph smoke test passes. **Tests:** ☐ compose ☐ smoke.

---

## SPARK-PROD-F11 · Platform stub verification
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-F10
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Target:** confirm the gateway resolves full platform types from product-emitted `@key` stubs. **Acceptance:** 1. each platform type resolves via its stub key. **Tests:** ☐ VMM ☐ IG ☐ Doppler ☐ CORONA.

---

## SPARK-PROD-F12 · Deferred partner-wrapper decision
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-E01
**Labels:** `dgs-migration`, `product`, `schema`

**Current Behaviour:** `removeProductBusinessPartner`/`dropProductBusinessPartner`/`unDropProductBusinessPartner` are schema-drift wrappers; traffic routes through `productBusinessPartnerActions`. **Target:** PO decides delete vs keep `@deprecated`; implement. **Acceptance:** 1. traffic survey complete. 2. decision implemented. **Tests:** ☐ schema diff intentional.

---

### Phase G — Field Resolvers, Bug-fixes, Utils, Tests (one story per group)

---

## SPARK-PROD-G01 · Product.attachmentsWithMetaData
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Very High  ·  **Points (est.):** 8  ·  **Depends on:** SPARK-PROD-A02, SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour (Phase 2C):** ~150 ln — `relationship.searchByIds` → 5-bucket partition → v2+v3 attachment hydration → discussions/threads/samples batched → 5-source merge → draft filter → `orderProductAttachments`. **Target:** `AttachmentEnrichmentService` Kotlin port; keep the "ACL should do draft filter" TODO as a follow-up. **Acceptance:** 1. parity for mixed attachment/discussion/thread/sample. 2. ordering rank preserved (product=0, discussion=1, sample=2; createdAt DESC tiebreak). **Tests:** ☐ merge ☐ ordering ☐ parity.

---

## SPARK-PROD-G02 · Product.components
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Very High  ·  **Points (est.):** 8  ·  **Depends on:** SPARK-PROD-A02, SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour (Phase 2C):** ~190 ln — 4 parallel elastic (measurement/claim/bom/productDetail) + packaging + **per-claim N+1 ACL** + 5-type merge + count rollups. **Target:** refactor N+1 ACL into a batched call; preserve type tagging + `cloneDeep(initialCountsByBp)`. **Acceptance:** 1. parity for 50+ components. 2. `archivedCount`/`countByComponents` match source. 3. ACL batched (no N+1). **Tests:** ☐ merge ☐ counts ☐ batched ACL ☐ parity.

---

## SPARK-PROD-G03 · Product.attachments/attachmentsV3/attachmentSummary
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-PROD-G01
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** four related resolvers sharing `AttachmentEnrichmentService` (G01). **Target:** thin `@DgsData` fields over the shared service. **Acceptance:** 1. each field returns its shape. 2. shares G01 service. **Tests:** ☐ each field ☐ parity.

---

## SPARK-PROD-G04 · ProductsCategories.categories (12-case) + Doppler
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A04
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** 12-branch dispatcher; `DopplerDepartment.primary/secondaryCapacityTypeName` share one Doppler call (memoized). **Target:** Kotlin dispatcher → 12 helpers; Doppler via DataLoader. **Acceptance:** 1. each category type built correctly. 2. Doppler fetched once. **Tests:** ☐ 12 cases ☐ single doppler fetch.

---

## SPARK-PROD-G05 · Product.samples/sampleIds/elasticSamplesList
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** **stops reading `info.variableValues`** — pass explicit args from the query layer (contract change). **Target:** explicit args; document the contract change. **Acceptance:** 1. samples/sampleIds/elastic resolve. 2. no `info.variableValues` read. **Tests:** ☐ samples ☐ contract change ☐ parity.

---

## SPARK-PROD-G06 · Product.teams/discussionsV2/discussionsCount/workspaces
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** team/discussion/workspace elastic lookups. **Target:** federated references + elastic. **Acceptance:** 1. each field resolves. **Tests:** ☐ teams ☐ discussions ☐ workspaces ☐ parity.

---

## SPARK-PROD-G07 · Product.partners + status
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** `loadBps`/`loadBpsWithType` (VMM); `status` merges partner/workspace statuses. **Target:** `vmmUtils` Kotlin port; preserve int-parse normalization. **Acceptance:** 1. partners resolve via VMM. 2. `status` merge correct. **Tests:** ☐ partners ☐ status merge ☐ parity.

---

## SPARK-PROD-G08 · Product.sibling components (internal)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** sibling-domain passthroughs with `includeXxx` boolean branches — **internal same-DGS calls** (not cross-subgraph). **Target:** internal service calls to the co-located sibling services. **Acceptance:** 1. each sibling field resolves internally. 2. `includeXxx` branches honored. **Tests:** ☐ each field ☐ include branch ☐ parity.

---

## SPARK-PROD-G09 · Product.productWorkspaceAttributes/Info
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** both produce shapes with a **deferred `designCycle: async()=>…`** field-on-value. **Target:** model `designCycle` as a nested `@DgsData`, not an inline closure. **Acceptance:** 1. both fields resolve. 2. `designCycle` is a nested fetcher. **Tests:** ☐ attrs ☐ designCycle nested ☐ parity.

---

## SPARK-PROD-G10 · Product.ancestryProducts/rating/reservedDpcis
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** `rating` via `RatingClient`; `reservedDpcis` via `getReservedDpcisFromApex`. **Target:** federated/Feign references. **Acceptance:** 1. ancestry/rating/dpcis resolve. 2. rating null-on-error. **Tests:** ☐ ancestry ☐ rating ☐ dpcis.

---

## SPARK-PROD-G11 · Product.notRemovable* + asks + variations (de-reflect)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** source utils call into 4–5 sibling field resolvers **reflectively**. **Target:** **replace reflective resolver invocation with direct service-method calls** (same logical union). **Acceptance:** 1. same results as source. 2. no reflective resolver calls. **Tests:** ☐ union correctness ☐ no reflection ☐ parity.

---

## SPARK-PROD-G12 · Product.division bug fix (wrong loader)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** source `Product.division` (and `DopplerDepartment.division`) call `ig.department.getByID` instead of `ig.division.getByID` — **latent bug**. **Target:** wire to `DivisionService`; **PO decision** whether to feature-flag the fix during cutover (clients may depend on department-shaped result). **Acceptance:** 1. returns true division shape. 2. fix logged with PO; flag decision recorded. **Tests:** ☐ division shape ☐ contract parity expectation documented.

---

## SPARK-PROD-G13 · IG/tag/tcin/spg + template trivial group
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** `department`/`departments`/`clazz`/`brand`/`brands`/`divisions`/`productTemplateDepartments`, `tags`, `tcins`, `SPARK_Tcin.itemDetails` (CORONA), `SPARK_PackagingAttribute.spg` (internal fileLibrary), `SPARK_ProductRules.*`, `VMM_BusinessPartnerCategory.*`, `MasterProductStatus.*`. **Target:** group into one PR; federated/internal references. **Acceptance:** 1. each field resolves to the right source. **Tests:** ☐ hierarchy ☐ tcin/CORONA ☐ spg internal.

---

## SPARK-PROD-G14 · Simple user/status fields + trivial pass-throughs
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-PROD-A02
**Labels:** `dgs-migration`, `product`, `field-resolver`

**Current Behaviour:** `createdBy`/`updatedBy`/`versionCreatedBy` (user-profile), `ProductComponentStatus.updatedBy`, `SPARK_ResourcesCount.productThumbnailId` (re-fetch product), plus ~60 direct scalar pass-throughs (DTO-mapped). **Target:** thin `@DgsData` for user/thumbnail; Jackson DTO mapping for scalars. **Acceptance:** 1. user fields resolve (null id → null). 2. `productThumbnailId` re-fetches. 3. scalars mapped. **Tests:** ☐ user fields ☐ thumbnail ☐ scalar mapping.

---

## SPARK-PROD-G15 · Port product utils to Kotlin
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-PROD-A06
**Labels:** `dgs-migration`, `product`, `service`

**Current Behaviour:** `attachmentUtils`, `partnerUtils`, `teamUtils`, `productUtils`, `componentStatusUtils`, `resolvePaging`, `vmmUtils`, `accessControlUtils`, `removePartnerUtils`. **Target:** Kotlin ports; single camel/snake normalization at the Feign boundary; **fix** `componentStatusUtils.incrementAllContextCounter` (never resets — verify intent); batch `getAccessControlBatch` with parallel chunking. **Acceptance:** 1. utils ported with unit tests. 2. counter logic fixed/verified. 3. ACL batch parallel-chunked. **Tests:** ☐ each util ☐ counter ☐ ACL chunking.

---

## SPARK-PROD-G16 · Tests, parity, load, cut-over rehearsal
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-PROD-C01, SPARK-PROD-E01, SPARK-PROD-E03, SPARK-PROD-G01, SPARK-PROD-G02
**Labels:** `dgs-migration`, `product`, `tests`

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

---
