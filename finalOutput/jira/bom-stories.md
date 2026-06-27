# bom — Jira stories (paste one block per issue)

> **Epic:** BOM → plm-product DGS migration  ·  **Labels:** `dgs-migration`, `bom`, `<type>`
> Create the Epic first, then paste each block below as a new Story's description.
> Story points are AI-derived from complexity (confirm in refinement). See [README.md](./README.md).

## SPARK-BOM-A01 · Schema skeleton + DGS module + DateTime scalar
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** —
**Labels:** `dgs-migration`, `bom`, `schema`

**As a** DGS migration engineer **I want** the `bom.graphqls` skeleton with the federation v2.3 header and
the `DateTime` scalar wired **so that** all later BOM type/resolver work compiles on a stable base.

**Current Behaviour:** No DGS exists (green-field). Schema is translated from `code/schemas/SPARK_Bom.txt` — see
[03-schema.graphql](./03-schema.graphql).

**Target DGS Implementation:** Create `bom.graphqls` with `@link(url:"https://specs.apollo.dev/federation/v2.3", import:["@key","@extends","@external","@shareable","@requires"])`, `scalar DateTime`, empty `extend type Query`/`Mutation`. Wire `DateTime → Instant` in `ScalarConfig.kt`.

**Files to Create / Modify:** `schema/bom.graphqls`; `config/ScalarConfig.kt`.
**Dependencies:** None.
**Acceptance Criteria:**
1. `./gradlew generateJava` passes with the empty schema.
2. `DateTime` round-trips ISO-8601 UTC.
3. PR passes schema lint.
**Test Cases:** ☐ Unit: schema compiles ☐ Unit: `DateTime` serde round-trip.

---

## SPARK-BOM-A02 · Define all owned BOM types + inputs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A01
**Labels:** `dgs-migration`, `bom`, `schema`

**As a** DGS migration engineer **I want** all owned BOM types + 16 input types defined **so that** field
resolvers and mutations have a stable contract.

**Current Behaviour:** ~34 owned types (2 entities, 7 material impls, 5 impression impls, value types) +
16 inputs — all listed in [03-schema.graphql §4–§5](./03-schema.graphql).

**Target DGS Implementation:** Port every owned type from `03-schema.graphql`. Apply `@key(fields:"id")`
to `Bom` and `Bom_Unified` only. Apply `@shareable` to `CodeDescription`, `UnitsOfMeasure`, `Paging`,
`ValueWithUnit`. Do **not** add `@key` to embedded value types.

**Files to Create / Modify:** `schema/bom.graphqls`.
**Dependencies:** A01.
**Acceptance Criteria:**
1. All owned types + inputs from `03-schema.graphql` present.
2. `@key` only on `Bom`/`Bom_Unified`; `@shareable` on the 4 shared value types.
3. `./gradlew generateJava` passes.
**Test Cases:** ☐ Unit: schema validates ☐ Unit: `Bom` entity resolves via federation stub.

---

## SPARK-BOM-A03 · Add external stubs (platform + sibling DGS)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A01
**Labels:** `dgs-migration`, `bom`, `schema`

**As a** DGS migration engineer **I want** the 23 external stub types defined with `@extends @external`
**so that** BOM fields can reference gateway-stitched and sibling-DGS types without schema errors.

**Current Behaviour:** BOM references 1 platform type (`VMM_BusinessPartner`) + 22 sibling-DGS types
(see [03-schema.graphql §1–§2](./03-schema.graphql)).

**Target DGS Implementation:** Add each stub as `type X @extends @key(fields:"id") { id: ID! @external }`.
**Files to Create / Modify:** `schema/bom.graphqls`.
**Dependencies:** A01.
**Acceptance Criteria:**
1. All 23 stubs compile; Hive Gateway composes the subgraph without type conflicts.
2. No stub carries a body beyond its `@key` field(s).
**Test Cases:** ☐ Unit: schema compiles with external refs ☐ Integration: gateway resolves a `VMM_BusinessPartner` stub for a bom query.

---

## SPARK-BOM-A04 · @DgsTypeResolver for the 2 BOM interfaces (7+5 impls)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A02
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**As a** DGS migration engineer **I want** type resolvers for `BomMaterialInterface` (7 impls) and
`BomImpressionDetailsInterface` (5 impls) **so that** polymorphic material/impression lists resolve to the
correct concrete type.

**Current Behaviour (from Phase 2 — C3 / C11):**
- Material: switch on `material.materialCategory.code` → 4→Trim, 6→Wash, 2→Fabric, 15→Combination,
  16→FabricSpec, {10,11,12,13,14,17–24}→Packaging, **default (1,5,9)→BomMaterial**.
- Impression: switch on `impression.type` → 603→Trim, 605→TrimZipper, 604→Wash, 602→Fabric, **default 601→Base**.

**Target DGS Implementation:** Two `@DgsTypeResolver(name=...)` functions mirroring the switches. Keep the
default branches exactly (HUB code 9 must fall through to `BomMaterial`). Source the category codes from a
`BomConstants.kt` enum (replaces the resolver's `MATERIAL_CATEGORY_ID` — fixes the circular import).

**Files to Create / Modify:** `dataFetcher/BomTypeResolvers.kt`; `model/BomConstants.kt`.
**Dependencies:** A02.
**Acceptance Criteria:**
1. Each `materialCategory.code` maps to the type in the table above; unknown codes → `BomMaterial`.
2. Each impression `type` maps correctly; unknown → `BomBaseImpressionDetails`.
3. `BomConstants` holds all 21 category codes + 5 impression codes (verify values against backend).
**Test Cases:** ☐ Unit: all 7 material codes + default ☐ Unit: all 5 impression codes + default.

---

## SPARK-BOM-A05 · BomService Kotlin port (17 REST methods)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A01
**Labels:** `dgs-migration`, `bom`, `service`

**As a** DGS migration engineer **I want** `BomService` ported to Kotlin **so that** data fetchers delegate
to typed service calls instead of Node loaders.

**Current Behaviour (from Phase 2 — S1):** 17 methods against base
`{spark-product}/enterprise_product_development_products/bom/v1` + `/masterData`. See the table in
[02-resolver-analysis.md §Service Classes](./02-resolver-analysis.md). Requests use `deepToSnakeCase`,
responses `deepToCamelCase`. `addBom`/`updateBom` prime the read cache (`primeKey: humanId`);
`updateBom` sets `omitParamsInBody: true`. **ACL note (context):** read/write of a specific bom curries a
capability token because the backend authorizes per-resource access — ACL is ignored here.

**Target DGS Implementation:** `BomClient` Feign interface (one method per REST endpoint) + `BomService`
delegating to it. Jackson `SnakeCaseStrategy` for request/response. Master-data methods (`getBomStatus`,
`getBomMaterialTypes`, packaging master data) annotated `@Cacheable("bomMasterData")`. Preserve
`omitParamsInBody` (don't send `humanId` in the PUT body). Confirm the fate of 3 unused methods
(`getActiveBomsByProductIdAndBomType`, `getBomVersionsById`, `getBomVersion`) before deleting.

**Files to Create / Modify:** `service/BomService.kt`; `client/BomClient.kt`; `model/BomDto.kt` (+ master-data DTOs).
**Dependencies:** A01.
**Acceptance Criteria:**
1. All 17 method signatures present; each maps to the verb/path in §Service Classes.
2. Jackson converts camelCase ↔ snake_case both directions.
3. Master-data methods are `@Cacheable`; cache hit on second call.
4. PUT `updateBom` omits `humanId` from the body.
5. 3 unused methods either ported with a `// TODO confirm cross-domain caller` or removed per PO decision.
**Test Cases:** ☐ Unit: `getBomByIds` builds `GET …/bom/v1?ids=` ☐ Unit: snake/camel mapping ☐ Unit: master-data cache hit.

---

### Phase B — Core Reads (one query per story)

---

## SPARK-BOM-B01 · getBomByIds data fetcher
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A02, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**As a** DGS migration engineer **I want** the `getBomByIds` query **so that** clients can fetch boms by id list.

**Current Behaviour (Q1):** if `ids` empty → `[]`; else `GET {base}/…/bom/v1?ids={ids}` → `deepToCamelCase`.
**ACL note (context):** current impl gets a capability token for `ids` because boms are resource-scoped; ACL ignored in DGS.

**Target DGS Implementation:** `@DgsQuery fun getBomByIds(ids): List<Bom>` → `bomService.getByIds(ids)`.
Add a request-scoped `BomDataLoader` keyed on id (the source isn't batched — improve here). Empty list → `[]`.
**Files to Create / Modify:** `dataFetcher/BomQueryDataFetcher.kt` (+ `dataloader/BomDataLoader.kt`).
**Dependencies:** A02, A05.
**Acceptance Criteria:**
1. `getBomByIds(["B1","B2"])` returns mapped `Bom` objects from the REST list endpoint.
2. Empty `ids` → returns `[]` with **no** REST call.
3. Response snake_case → camelCase per schema.
**Test Cases:** ☐ Unit: happy path 2 ids ☐ Unit: empty ids → no REST call ☐ Integration: query via DGS test client.

---

## SPARK-BOM-B02 · getBomDataV2 data fetcher
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A02, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**As a** DGS migration engineer **I want** `getBomDataV2` **so that** callers needing the smaller
`Bom_Unified` projection are served.

**Current Behaviour (Q2):** identical REST call to B01; only the return type differs (`Bom_Unified` ⊆ `Bom`).
**Target DGS Implementation:** `@DgsQuery getBomDataV2(ids): List<Bom_Unified>` reusing `bomService.getByIds`;
map to `Bom_Unified`. Confirm `Bom_Unified` is a strict field subset.
**Files / Dependencies:** `BomQueryDataFetcher.kt`; A02, A05.
**Acceptance Criteria:**
1. Returns `Bom_Unified` for the same REST payload as B01.
2. Empty ids → `[]`.
3. No field present on `Bom_Unified` that is absent from the REST response.
**Test Cases:** ☐ Unit: maps to `Bom_Unified` ☐ Unit: empty ids ☐ Parity: B01 vs B02 share source data.

---

## SPARK-BOM-B03 · getBomStatus (cacheable master data)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q3):** `GET {base}/masterData?name=BomStatus`; transform `{key:value}` map → `[{code,description}]`. No ACL.
**Target DGS Implementation:** `@DgsQuery getBomStatus(): List<CodeDescription>` → `@Cacheable("bomMasterData", key="'status'")` service method that maps the map to the list.
**Files / Dependencies:** `BomQueryDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. Returns `[{code,description}]` from the status map. 2. Second call served from cache (no REST). 3. Map key→`code`, value→`description`.
**Test Cases:** ☐ Unit: map→list ☐ Unit: cache hit ☐ Integration: query returns statuses.

---

## SPARK-BOM-B04 · getBomByParentId data fetcher
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q4):** `GET {base}/…/bom/v1/byProductId/{parentId}` → sort `content` by `createdAt` DESC (client-side) → `{content}`. **ACL note (context):** capability token for `parentId`; ignored in DGS.
**Target DGS Implementation:** `@DgsQuery getBomByParentId(parentId): BomPaged`. **PO decision B04:** push the
sort to the backend; until then replicate `sortedByDescending { it.createdAt }`. Return `BomPaged{content}`.
**Files / Dependencies:** `BomQueryDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. Returns boms for `parentId` sorted `createdAt` DESC. 2. Empty → `{content: []}`. 3. Sort location documented (client vs backend).
**Test Cases:** ☐ Unit: sort order ☐ Unit: empty ☐ Integration: query via DGS client.

---

## SPARK-BOM-B05 · getBomMaterialTypes (merge with Material Hub)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q5):** load bom material types (`GET …/master_data/bom_material_types[?ids]`) **and**
`materialHub.getHubMaterialTypes` (today sequential), concat; map each hub type →
`{code:9, description:type, bomType:{code:1,description:'Product'}, libraryLink:true, freeText:true}`.
**EXT Service Calls:** **EXT** → key: `materialHub` · severity: 🟡 — hub material type list to merge into bom types.
**Target DGS Implementation:** `@DgsQuery getBomMaterialTypes(ids): List<BomMaterialType>`. Fetch both
sources **in parallel** (`coroutineScope`), concat, synthesize hub rows as above. Hub fetch via federated
`materialHub` reference or a `MaterialHubClient`.
**Files / Dependencies:** `BomQueryDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. Returns bom types + synthesized hub types. 2. Hub rows carry `code=9, libraryLink=true, freeText=true, bomType={1,'Product'}`. 3. The two fetches run concurrently. 4. EXT hub failure → return bom types only (partial), logged.
**Test Cases:** ☐ Unit: merge shape ☐ Unit: hub synthesis fields ☐ Unit: hub failure → partial ☐ Integration.

---

## SPARK-BOM-B06 · getBomPackagingMaterialTypes (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q6):** `GET …/master_data/packaging_bom_material_types` → camelCase. No ACL.
**Target DGS Implementation:** `@DgsQuery` → `@Cacheable` service method.
**Files / Dependencies:** `BomQueryDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. Returns packaging material types. 2. Cached on second call.
**Test Cases:** ☐ Unit: returns list ☐ Unit: cache hit.

---

## SPARK-BOM-B07 · getBomPackagingSubstrates (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q7):** `GET …/master_data/packaging_bom_substrate_types` → camelCase.
**Target DGS Implementation:** `@DgsQuery` → `@Cacheable` service method returning `[BomPackagingSubstrate]`.
**Acceptance Criteria:** 1. Returns substrate list. 2. Cached.
**Test Cases:** ☐ Unit: list ☐ Unit: cache hit.

---

## SPARK-BOM-B08 · getBomPackagingUnitOfMeasure (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q8):** `GET …/master_data/packaging_unit_of_measure` → camelCase (`units_of_measure`).
**Target DGS Implementation:** `@DgsQuery` → `@Cacheable` returning `[UnitsOfMeasure]`.
**Acceptance Criteria:** 1. Returns UoM list. 2. Cached.
**Test Cases:** ☐ Unit: list ☐ Unit: cache hit.

---

### Phase C — Search & Listing

---

## SPARK-BOM-C01 · getBomElastic data fetcher
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q9):** `{content} = search.getBomElastic.load(query)`; return `content`. The **entire
`query` object** is passed to elastic — document the exact field set.
**EXT Service Calls:** **EXT** → key: `search` · severity: 🔴 — elastic bom search index.
**Target DGS Implementation:** `@DgsQuery getBomElastic(q): List<Bom>` → `searchClient.bomElastic(query)`; return `content`. Define the query DTO from the fields the backend expects (verify).
**Files / Dependencies:** `BomSearchDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. Returns `content` boms for a query. 2. Query DTO field set documented + matches backend. 3. Empty → `[]`.
**Test Cases:** ☐ Unit: returns content ☐ Unit: empty ☐ Integration.

---

## SPARK-BOM-C02 · searchMaterialsBom data fetcher
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q10):**
1. `fabricSuppliers = VMM_BusinessPartner.getRelatedFabricSuppliersByMerchVendors({merchVendorIds: partnerIds})` (cross-resolver import — replace with a service/federation call).
2. Build `queryPayload` from args.
3. If `nestedSearchFilters` present: flatten each `[i]` into 5 keys `nestedSearchFilters[i].{type|fieldPath|nestedFieldPath|operator|values}`, then delete the array key.
4. `search.searchMaterialsBom.load(queryPayload)`.
**EXT Service Calls:** **EXT** → key: `search` · 🔴; **EXT** → key: `vmm` · 🔵 (fabric-supplier lookup).
**Target DGS Implementation:** `@DgsQuery searchMaterialsBom(...): BomMaterialSearch`. Fetch fabric suppliers
via a `VmmClient`/federation (not a resolver import). **PO decision C02:** keep the query-string flatten or
send a structured nested DTO if the backend supports it — preserve the existing wire format by default.
**Files / Dependencies:** `BomSearchDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. Returns `BomMaterialSearch{content,paging}`. 2. With `nestedSearchFilters`, the request serializes to the same `nestedSearchFilters[i].*` keys as today (or the agreed DTO). 3. `size` default 20. 4. Fabric-supplier prefetch via service/federation, not a resolver import.
**Test Cases:** ☐ Unit: payload build ☐ Unit: nested-filter flatten ☐ Unit: default size ☐ Integration.

---

## SPARK-BOM-C03 · getComboSupplierForBom data fetcher
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q13):**
1. `fabricSpecCombos = SPARK_Combination.searchFabricSpecCombos({q:`parentComboId:${comboId}`, page:0, size:100})` (cross-resolver import).
2. Filter combos: keep where `fsId` set AND ((`partnerIds` non-empty & `mvIds.length===1` & `partnerIds.includes(mvIds[0])`) OR `partnerIds` empty).
3. For each (parallel): `fs = vmm.getByID.load(fsId)`; if `fs.bpName`, push `{fabricSupplier:{id:fsId,name:fs.bpName}, fabricSpecCombo}`.
**EXT Service Calls:** **EXT** → key: `combination` · 🟡; **EXT** → key: `vmm` · 🔵.
**Target DGS Implementation:** `@DgsQuery getComboSupplierForBom(comboId, partnerIds): List<BomComboSupplier>`.
Call combination via `CombinationClient`/federation. VMM lookups in parallel (`coroutineScope`/`async`).
**PO decision:** the `mvIds.length===1` filter silently drops multi-MV combos — confirm intended.
**Files / Dependencies:** `BomSearchDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. Returns suppliers only for combos with a resolvable `fsId` and `bpName`. 2. Filter logic matches the rule above (document the `mvIds.length===1` behaviour). 3. VMM lookups run concurrently.
**Test Cases:** ☐ Unit: filter incl/excl ☐ Unit: missing `bpName` skipped ☐ Unit: empty partnerIds path ☐ Integration.

---

## SPARK-BOM-C04 · getValidTrimSuppliersForBom data fetcher
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q11):** `getRelatedSuppliersForMVs(ctx, merchVendorIds, [TRIM_SUPPLIER.code])` → `[Int]` partner ids.
**EXT Service Calls:** **EXT** → key: `vmm` · 🔵.
**Target DGS Implementation:** `@DgsQuery` delegating to a `VmmSupplierService.relatedSuppliers(merchVendorIds, roles=[TRIM_SUPPLIER])`. Source the role code from `BomConstants` (confirm code value).
**Acceptance Criteria:** 1. Returns related trim-supplier partner ids. 2. Role filter = TRIM_SUPPLIER only. 3. Empty input → `[]`.
**Test Cases:** ☐ Unit: role filter ☐ Unit: empty ☐ Integration.

---

## SPARK-BOM-C05 · getValidRawMaterialSuppliersForBom data fetcher
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `query`

**Current Behaviour (Q12):** same as C04 with roles `[RAW_MATERIAL_SUPPLIER, FABRIC_SUPPLIER, TRIM_SUPPLIER]`.
**Target DGS Implementation:** `@DgsQuery` delegating with the three roles.
**Acceptance Criteria:** 1. Returns ids matching the 3 roles. 2. Empty input → `[]`.
**Test Cases:** ☐ Unit: 3-role filter ☐ Unit: empty ☐ Integration.

---

### Phase D — Mutations (simple)

---

## SPARK-BOM-D01 · addBom mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `mutation`

**Current Behaviour (M1):** `bom = bomService.addBom(sparkBom)` → `POST {base}/…/bom/v1`
(`transformRequest: deepToSnakeCase`, `primeKey: humanId`); if `bom.validationErrors || bom.message` →
throw. No ACL (new resource).
**Input validation:** `name` and `parentId` required (schema `String!`).
**Target DGS Implementation:** `@DgsMutation addBom(sparkBom: BomInput): Bom` → `bomService.add(...)`. Map
camelCase→snake_case. On `validationErrors`/`message` in the response → throw typed `BomValidationException`.
After success, `bomDataLoader.prime(humanId, bom)`.
**Files / Dependencies:** `BomMutationDataFetcher.kt`; A05.
**Acceptance Criteria:** 1. POST creates a bom and returns it mapped to `Bom`. 2. Backend `validationErrors`/`message` → `BomValidationException` (not a silent return). 3. Request body is snake_case. 4. Read cache primed with `humanId`.
**Test Cases:** ☐ Unit: happy path ☐ Unit: validationErrors → exception ☐ Unit: cache primed ☐ Integration.

---

## SPARK-BOM-D02 · manageBomWorkspaces mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `mutation`

**Current Behaviour (M3):** if `toAdd`/`toRemove` non-empty → `workspaceAssociationHelper(BOM, bomId, toAdd, toRemove)` → PUT `…/{bomId}/{associate|dissociate}_workspace`; else returns `undefined`.
**EXT Service Calls:** **EXT** → key: `workspaceV2` · 🟡 (association). **ACL note (context):** capability token for `bomId`; ignored in DGS.
**Target DGS Implementation:** `@DgsMutation manageBomWorkspaces(bomId, workspacesToAdd, workspacesToRemove): Bom`
→ `bomService.manageWorkspaceAssociations(...)`. Both empty → return `null` (document for clients).
**Acceptance Criteria:** 1. Adds/removes workspace associations via the correct endpoint. 2. Both lists empty → `null`, no REST call. 3. Returns the updated bom.
**Test Cases:** ☐ Unit: add path ☐ Unit: remove path ☐ Unit: both empty → null ☐ Integration.

---

## SPARK-BOM-D03 · lockBom mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `mutation`

**Current Behaviour (M4):** `PUT …/{bomId}/lock`. **ACL note (context):** capability token for `bomId`; ignored in DGS.
**Target DGS Implementation:** `@DgsMutation lockBom(bomId): Bom` → `bomService.lock(bomId)`.
**Acceptance Criteria:** 1. PUT to `/lock` returns the locked bom. 2. 404 → null.
**Test Cases:** ☐ Unit: lock ☐ Unit: 404 ☐ Integration.

---

## SPARK-BOM-D04 · unlockBom mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `mutation`

**Current Behaviour (M5):** `PUT …/{bomId}/unlock`. ACL note as D03.
**Target DGS Implementation:** `@DgsMutation unlockBom(bomId): Bom` → `bomService.unlock(bomId)`.
**Acceptance Criteria:** 1. PUT to `/unlock` returns the unlocked bom. 2. 404 → null.
**Test Cases:** ☐ Unit: unlock ☐ Unit: 404 ☐ Integration.

---

## SPARK-BOM-D05 · updateBomComponentStatus mutation
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `mutation`

**Current Behaviour (M6):** `PUT …/bom/v1/component_status_update` body `{productId, ids, status}`. **No ACL token** — the only write without one. **PO decision D05:** confirm backend enforces authorization server-side.
**Target DGS Implementation:** `@DgsMutation updateBomComponentStatus(productId, ids, status): BomPaged` → `bomService.updateComponentStatus({...})`; wrap result as `{content}`.
**Acceptance Criteria:** 1. PUT sends `{productId, ids, status}` (snake_case). 2. Returns `BomPaged{content}`. 3. Decision on server-side auth recorded in the PR.
**Test Cases:** ☐ Unit: body shape ☐ Unit: result wrap ☐ Integration.

---

### Phase E — Complex Operations

---

## SPARK-BOM-E01 · updateBom — 3-step orchestrated write
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** Very High  ·  **Points (est.):** 8  ·  **Depends on:** SPARK-BOM-A05, SPARK-BOM-D02
**Labels:** `dgs-migration`, `bom`, `mutation`

**As a** DGS migration engineer **I want** `updateBom` implemented as an explicit 3-step orchestration with a
chosen failure strategy **so that** body, workspace, and permission updates stay consistent.

**Current Behaviour (M2):**
1. (ACL note — context) capability token obtained for `humanId` because the update is resource-scoped; ignored in DGS.
2. **If** `workspaceContext` has add/remove → `workspaceAssociationHelper(BOM, humanId, add, remove)` (**commits first**) → PUT `…/{bomId}/{associate|dissociate}_workspace`.
3. `bomService.updateBom(sparkBom)` → `PUT {base}/…/bom/v1/{humanId}` (`omitParamsInBody: true`).
4. If `validationErrors || message` → throw.
5. **If** `businessPartners` present → `bomService.updatePermissions().load(sparkBom)` → PUT `…/{humanId}/permission`.
6. Return the updated bom.
**Risk 🔴:** three sequential writes, **no rollback** today. Step-2 workspace change persists even if step 3 fails; step-5 permission update can leave ACL stale.
**EXT Service Calls:** **EXT** → key: `workspaceV2` · 🟡 (association step).
**Target DGS Implementation:** `BomUpdateOrchestrator` running steps in order: workspace assoc → body PUT
(`omitParamsInBody`) → optional permissions PUT. **PO decision E01:** apply one of — (a) saga with
compensating dissociate/associate, (b) compensation log + alert, (c) documented best-effort. Replace the
`validationErrors||message` shape-sniff with a typed `BomValidationException`. Prime the read cache on success.
**Files / Dependencies:** `service/BomUpdateOrchestrator.kt`, `BomMutationDataFetcher.kt`; A05, D02 (shares the workspace step).
**Acceptance Criteria:**
1. Parity for 5 fixtures: body-only; body+workspace-add; body+workspace-remove; body+partners; body+workspace+partners.
2. Workspace step runs **before** the body PUT; permissions step only when `businessPartners` present.
3. Body PUT omits `humanId` from the body.
4. Chosen failure strategy implemented; partial failure emits a compensation-log entry (if (b)/(c)) or compensates (if (a)).
5. Backend `validationErrors`/`message` → `BomValidationException`.
6. Read cache updated with the returned bom.
**Test Cases:** ☐ Unit: order workspace→body→perms ☐ Unit: no-workspace skip ☐ Unit: no-partners skip ☐ Unit: step-3 failure path (strategy) ☐ Parity: 5 fixtures.

---

### Phase F — Internal Contributions to Product / ResourcesCount (same subgraph)

> **Monorepo:** `product` and `bom` are the **same `plm-product` subgraph**, so these are **internal field
> resolvers** (CAT-2), not cross-subgraph federation. They depend on the `Product`/`ResourcesCount` types
> existing in the merged schema but are **not** gateway-federated and **not** blocked by a separate
> deployment. See [reference-federation-patterns.md §0](../scripts/reference-federation-patterns.md).

---

## SPARK-BOM-F01 · Implement Product.productBoms/boms/packagingBoms (internal, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**As a** DGS migration engineer **I want** the bom-list fields on `Product` served by the BOM code **so that**
product → bom navigation lives with the BOM service inside `plm-product`.

**Current Behaviour:** these three field resolvers live in the product resolver and call
`ctx.loaders.bom.getActiveBomsByProductId(...)` / `...AndBomType(...)`.
**Target DGS Implementation:** plain `@DgsData` field resolvers on the `Product` type (same subgraph) →
`bomService.getActiveBomsByProductId` (and `...AndBomType` for `boms(types)`). **No** `@DgsEntityFetcher` /
`@extends @external` — `Product` is an internal type. Depends on `Product` existing (product A02), not on a
separate deployment.
**Acceptance Criteria:** 1. `Product.productBoms/boms/packagingBoms` resolve via `bomService` internally. 2. the equivalent product-side resolvers are removed. 3. `boms(types)` filters by bom type. 4. no gateway hop.
**Test Cases:** ☐ Unit: each field calls `bomService` ☐ Integration: `Product { productBoms { id } }` in-process ☐ Parity vs current product resolver.

---

## SPARK-BOM-F02 · Fill ResourcesCount.bomsCount (internal, same subgraph)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**As a** DGS migration engineer **I want** `bomsCount` on `ResourcesCount` filled by the BOM code **so that**
the TechPack aggregate's bom count is owned by BOM.
**Current Behaviour:** the TechPack count map computes a bom count via elastic in the product orchestration.
**Target DGS Implementation:** `@DgsData bomsCount` on the `ResourcesCount` type (owned by `product` in the
**same subgraph**) → internal bom elastic count. **No** entity fetcher / federation — only the *externally*
owned `ResourcesCount` fields (attachments/discussions/etc.) need real federation. Depends on `ResourcesCount`
existing (product A05).
**EXT:** 🔴 `search` (count query, the search DGS).
**Acceptance Criteria:** 1. `bomsCount` resolves internally on `ResourcesCount`. 2. count matches current elastic semantics. 3. no gateway hop for this field.
**Test Cases:** ☐ Unit: count query ☐ Integration: `ResourcesCount { bomsCount }` in-process ☐ Parity vs facade count.

---

### Phase G — Field Resolvers & Tests (one story per type block)

> Each Phase-G story implements all field resolvers for one type. Titles name the type, not an "and" of
> operations. Trivial scalar pass-throughs are bundled in **G14**. Every sibling-DGS field resolves as a
> federated reference; until that subgraph publishes its stub it returns `{id}`.

---

## SPARK-BOM-G01 · Bom + Bom_Unified field resolvers (9 shared)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A02, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C1):** 9 identical fields on both types — `humanId` (`humanId ?? id`), `access` &
`currentUserPermissions` (accessControl — **ACL context only, ignore in impl**), `businessPartners`
(`loadBusinessPartners`), `createdBy`/`updatedBy` (`getUser`), `product` (if `parentId` starts `PID` →
`product.getByID`, else null), `workspaces` (`getWorkspacesByIdsV2`), `participantDetails` (`getUserGroup`).
**EXT Service Calls:** 🟡 `workspaceV2`; 🔵 user-profile (`createdBy`/`updatedBy`/`participantDetails`); 🔵 teams (`businessPartners`). `product` is an internal same-DGS call.
**Target DGS Implementation:** One `@DgsData` set backing both `Bom` and `Bom_Unified`. Sibling fields →
federated references; `product` → internal `productService.getById`. `access`/`currentUserPermissions` —
omit ACL work; if surfaced, resolve via the platform-provided permission context (no plumbing).
**PO note:** confirm `parentId` only ever starts `PID`.
**Files / Dependencies:** `BomEntityFieldDataFetcher.kt`; A02, A05.
**Acceptance Criteria:** 1. All 9 fields resolve on both types from one impl. 2. `product` null when `parentId` not `PID*`. 3. Sibling fields emit correct `@key`s for federation. 4. No ACL plumbing introduced.
**Test Cases:** ☐ Unit: `humanId` fallback ☐ Unit: `product` PID branch ☐ Unit: workspace mapping ☐ Integration: federated `Bom { createdBy { id } }`.

---

## SPARK-BOM-G02 · BomMaterial_Unified field resolvers (3)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C2):** `libraryResourceId` (Direct), `libraryResource` = `getBomMaterial` 4-case
dispatcher (TRIM→trim batch+size+caption, WASH→wash, FABRIC→fabricSpecCombo search, HUB→hub; default null),
`materialLibraryUom` (only when category=TRIM → trim UoMs). **ACL context:** wash/hub use a capability token; ignore in impl.
**EXT:** 🟡 materialHub/trim/wash, 🔴 fabric(search).
**Target DGS Implementation:** `BomMaterialEnrichmentService.summary(material)` dispatching on
`materialCategory.code`. Reuse the per-source clients/federation.
**Files / Dependencies:** `BomMaterialUnifiedFieldDataFetcher.kt`; A04, A05.
**Acceptance Criteria:** 1. Each category routes to the correct source; unknown → null. 2. `materialLibraryUom` resolves only for TRIM. 3. `libraryResourceId` = `libraryResource.id`.
**Test Cases:** ☐ Unit: 4 category routes + default ☐ Unit: UoM TRIM-only ☐ Integration.

---

## SPARK-BOM-G03 · BomMaterial field resolvers (8)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C4):** `libraryResource` (H5 hub), `genericMaterialType` (hub `baseMaterial.relatedMaterialType`
precedence over local), `origins`/`certifications` (H3 coded-options filter+enrich), `weight` (H1),
`sizeUnitOfMeasure` (H2), `countryOfOrigin` (tag), `parentLibraryResourceId`/`libraryResourceId` (Direct),
`impressionDetails` (`material.impressions`). Hub resource loaded twice (libraryResource + genericMaterialType) — DataLoader-memoized; consolidate. **ACL context:** hub uses a capability token; ignore in impl.
**EXT:** 🟡 materialHub; 🔵 tag.
**Target DGS Implementation:** `BomMaterialFieldDataFetcher` with a single memoized hub fetch reused by
`libraryResource` + `genericMaterialType`. Coded-options cached per request (`@Cacheable`).
**Acceptance Criteria:** 1. `genericMaterialType` returns hub value when `relatedMaterialType` differs from local, else local. 2. `origins`/`certifications` filtered to known codes and enriched to `{code,description}`. 3. `weight` uses UoM fallback code 23 (grams). 4. Hub fetched once per material.
**Test Cases:** ☐ Unit: genericMaterialType precedence ☐ Unit: origins enrich/filter ☐ Unit: weight fallback ☐ Unit: single hub fetch ☐ Integration.

---

## SPARK-BOM-G04 · BomPackagingMaterial field resolvers (2)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C5):** `impressionDetails` (`material.impressions`), `countryOfOrigin` (tag).
**Target DGS Implementation:** two `@DgsData` fields; `countryOfOrigin` via `tag` reference.
**Acceptance Criteria:** 1. `impressionDetails` = parent impressions. 2. `countryOfOrigin` resolves from `countryOfOriginIds` (empty → `[]`).
**Test Cases:** ☐ Unit: passthrough ☐ Unit: tag lookup ☐ Unit: empty ids.

---

## SPARK-BOM-G05 · BomFabricMaterial field resolvers (4)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C6):** `libraryResource` = `search.searchFabricSpecCombos({q:`id:${fscId}`,page:0,size:1})` → `content[0] ?? {id:fscId}`; `weight` (H1), `countryOfOrigin`, `impressionDetails`, `libraryResourceId`.
**EXT:** 🔴 search; 🟡 materialHub (weight); 🔵 tag.
**Target DGS Implementation:** `libraryResource` via `searchClient.fabricSpecCombos(...)` with `{id}` fallback.
**Acceptance Criteria:** 1. Returns the matched fabricSpecCombo or `{id}`. 2. `weight`/`countryOfOrigin` as G03. 
**Test Cases:** ☐ Unit: found ☐ Unit: fallback `{id}` ☐ Integration.

---

## SPARK-BOM-G06 · BomFabricSpecMaterial field resolvers (4)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C7):** `libraryResource` = `fabric.getSpecificationByID.load(id) ?? {id}`; `weight`, `countryOfOrigin`, `impressionDetails`.
**EXT:** 🟡 fabric, materialHub; 🔵 tag.
**Target DGS Implementation:** `libraryResource` via `FabricClient.getSpecificationById` with `{id}` fallback.
**Acceptance Criteria:** 1. Returns fabric spec or `{id}`. 2. weight/countryOfOrigin as G03.
**Test Cases:** ☐ Unit: found ☐ Unit: fallback ☐ Integration.

---

## SPARK-BOM-G07 · BomCombinationMaterial field resolvers (4)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C8):** `libraryResource` = `combination.getById.load(id) ?? {id}`; `weight`, `countryOfOrigin`.
**Target DGS Implementation:** `libraryResource` via `CombinationClient.getById` with `{id}` fallback.
**Acceptance Criteria:** 1. Returns combination or `{id}`. 2. weight/countryOfOrigin as G03.
**Test Cases:** ☐ Unit: found ☐ Unit: fallback ☐ Integration.

---

## SPARK-BOM-G08 · BomTrimMaterial field resolvers (7) — trim size dispatchers
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**As a** DGS migration engineer **I want** the trim material fields including the 15-case size/caption
dispatchers **so that** trim rows display the correct size value, caption, UoM and facility.

**Current Behaviour (C9):**
- `libraryResource` = `trim.getTrimBatch.load(trimId)`.
- `materialLibraryUom` = trim UoMs, find by `materialLibraryUomId.toString()` (preserve int→string coercion).
- `sizeValue` = reload trim → match size by `librarySizeId` → `getTrimSizeValue(trimType, trimSubType, size)` — **15-case TRIM_TYPES** (`bomUtils.txt:57-114`).
- `sizeCaption` = reload trim → `getBomSizeCaption(trim, size)` — **15-case**, returns `{edit, view}` (`bomUtils.txt:116-187`).
- `facilityName` = if already set return it; else reload trim → find supplier by `supplierId` → facility by `facilityId` → `location.getLocationById(facilityId)` → `vmmFacility.name`.
- `weight`, `countryOfOrigin` as G03. The trim is loaded 3× (memoized) — consolidate.
**EXT:** 🟡 trim; 🔵 location (facility); 🔵 tag.
**Target DGS Implementation:** `TrimEnrichmentService.enrich(material)` does **one** `getTrimBatch` and feeds
`libraryResource`/`sizeValue`/`sizeCaption`/`materialLibraryUom`. Port the two 15-case dispatchers into a
single Kotlin `TrimSizePresentation` table (`sizeValue` + `{edit,view}` caption per trim type/subtype).
Preserve `materialLibraryUomId.toString()`. `facilityName` 2-level lookup via `LocationClient`.
**Files / Dependencies:** `BomTrimMaterialFieldDataFetcher.kt`, `TrimSizePresentation.kt`, `TrimEnrichmentService.kt`; A04, A05.
**Acceptance Criteria:**
1. `sizeValue` matches `getTrimSizeValue` for all 15 trim types (parity table) incl. THREAD/LABEL subtype branches.
2. `sizeCaption` returns the correct `{edit,view}` per type incl. compatible-size and finished-size cases.
3. `materialLibraryUom` matches via string-coerced code.
4. `facilityName` returns the pre-set value if present, else the resolved VMM facility name.
5. Trim is fetched once per material (one REST call).
**Test Cases:** ☐ Unit: 15 trim-type `sizeValue` cases ☐ Unit: caption edit/view per type ☐ Unit: UoM string coercion ☐ Unit: facilityName pre-set vs resolved ☐ Unit: single trim fetch ☐ Parity: recorded trim fixtures.

---

## SPARK-BOM-G09 · BomWashMaterial field resolvers (4)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C10):** `libraryResource` = `wash.getWash(jwt).load(washId) ?? {id}`; `weight`, `countryOfOrigin`, `impressionDetails`. **ACL context:** wash uses a capability token; ignore in impl.
**Target DGS Implementation:** `libraryResource` via `WashClient.getWash(washId)` with `{id}` fallback.
**Acceptance Criteria:** 1. Returns wash or `{id}`. 2. weight/countryOfOrigin as G03.
**Test Cases:** ☐ Unit: found ☐ Unit: fallback ☐ Integration.

---

## SPARK-BOM-G10 · BomImpressionDetails_Unified field resolvers (6) — internal/external branch
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-BOM-A04, SPARK-BOM-A05
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**As a** DGS migration engineer **I want** the unified impression-detail resolvers with the
internal/external user branch **so that** library/color materials resolve for both user types.

**Current Behaviour (C12):**
- `libraryResource`: **internal** (`currentUser.internal`) → `searchMaterialById('libraryResource', detail)`;
  **external** → `bomIds = args.ids`; if no `libraryResource.id` → null; else `searchMaterialsByProxyIds.load({q:`id:(${id})`, proxyIds: bomIds, page:0, size:1})` → `content[0] ?? {id}`.
- `groundColor`/`textColor`/`sliderColor`/`tapeColor`/`teethColor` → `searchMaterialById(name, detail)` (5 loader calls).
**Risk 🔴:** the external branch reads `args.ids` — only present when the parent query carried `ids`. **ACL context:** external path obtains a capability token for `bomIds`; ignore in impl, but keep `proxyIds`.
**EXT:** 🔴 search.
**Target DGS Implementation:** Pass `bomIds` via `DgsDataFetchingEnvironment` **local context** set by the
parent query — **do not** read `args.ids`. Branch on the user-internal flag from the request context. Color
fields via a `MaterialDataLoader` keyed on id.
**Files / Dependencies:** `BomImpressionDetailsFieldDataFetcher.kt`; A04, A05.
**Acceptance Criteria:**
1. Internal path resolves `libraryResource` via material-by-id; external path via proxy-id search.
2. `bomIds` come from DGS local context, not field args (the fragile `args.ids` contract is removed).
3. Missing `libraryResource.id` → null.
4. 5 color fields resolve via batched material loader.
**Test Cases:** ☐ Unit: internal branch ☐ Unit: external branch (proxyIds) ☐ Unit: null id ☐ Unit: color batch ☐ Parity: internal vs external.

---

## SPARK-BOM-G11 · BomFabricLibraryImpressionDetails.libraryResource
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-G10
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C13):** single `libraryResource` field with the same internal/external branch as G10.
**Target DGS Implementation:** reuse the G10 branch helper.
**Acceptance Criteria:** 1. Same behaviour as G10's `libraryResource` for this type. 2. Uses local-context `bomIds`.
**Test Cases:** ☐ Unit: internal ☐ Unit: external.

---

## SPARK-BOM-G12 · BomTrimLibraryImpressionDetails field resolvers (3)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-G10
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C14):** `libraryResource` (G10 branch) + `groundColor`, `textColor` via `searchMaterialById`.
**Target DGS Implementation:** reuse G10 helper + 2 color fields via material loader.
**Acceptance Criteria:** 1. `libraryResource` as G10. 2. `groundColor`/`textColor` resolve via material loader.
**Test Cases:** ☐ Unit: libraryResource ☐ Unit: colors.

---

## SPARK-BOM-G13 · BomTrimZipperLibraryImpressionDetails field resolvers (3 colors)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-G10
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C15):** `sliderColor`, `tapeColor`, `teethColor` via `searchMaterialById`.
**Target DGS Implementation:** 3 `@DgsData` fields via material loader.
**Acceptance Criteria:** 1. Three color fields resolve by id. 2. Missing id → null.
**Test Cases:** ☐ Unit: three colors ☐ Unit: null id.

---

## SPARK-BOM-G14 · Trivial pass-through fields (bundle)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-BOM-A02
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour:** the only allowed bundle — fields that return a parent value with no service call:
`BomMaterialType.id` = `` `${code}_${description}` `` (computed); `BomMaterialSearch.paging` = whole-object
passthrough; every material type's `impressionDetails` = `parent.impressions` (rename); `*.libraryResourceId`
= `get(parent,'libraryResource.id')`; `*.parentLibraryResourceId`; and ~30 scalar pass-throughs per material
type covered by DTO mapping.
**Target DGS Implementation:** Jackson DTO mapping for scalars; tiny `@DgsData` for the 3 computed/renamed fields.
**Acceptance Criteria:** 1. `BomMaterialType.id` = `code_description`. 2. `impressionDetails` maps from `impressions`. 3. `libraryResourceId` from nested id. 4. No EXT calls.
**Test Cases:** ☐ Unit: synthetic id ☐ Unit: rename mapping ☐ Unit: nested id extraction.

---

## SPARK-BOM-G15 · BomMaterialSearchResult field resolvers (5)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-A05, SPARK-BOM-C02
**Labels:** `dgs-migration`, `bom`, `field-resolver`

**Current Behaviour (C18):** `description` (`description ?? name`), `status` (`status?.description ?? status`),
`fabricSpec` (if `type==='fabric_spec_combo'` & `fabricSpecId` → `fabric.getSpecificationByID`), `fabric`
(if `type==='combination'` & `fabricRecordHumanId` → `fabric.getByID(jwt)`), `fabricId` (combination → `fabricRecordHumanId`),
`relatedMaterials` (2-branch internal/external elastic by `relatedAssetIds` buckets). **Bug 🟡:** external
branch does `proxyIds.push(detail.parentComboId)` — mutates the args array; defensive-copy. **ACL context:** `fabric.getByID` and external branch use a capability token; ignore in impl, keep `proxyIds`.
**EXT:** 🟡 fabric; 🔴 search.
**Target DGS Implementation:** field resolvers as above; `relatedMaterials` builds buckets from `intentLineIds`
(`split('.')[0]`, unique) and runs the internal (`getPage`) or external (`searchMaterialsByProxyIds`) query.
**Defensive-copy** `proxyIds` before appending `parentComboId`.
**Acceptance Criteria:** 1. `description`/`status` handle both shapes. 2. `fabricSpec`/`fabric`/`fabricId` gated by `type`. 3. `relatedMaterials` buckets `intentLineIds` correctly. 4. `proxyIds` not mutated (copy used). 
**Test Cases:** ☐ Unit: status object/string ☐ Unit: type gates ☐ Unit: bucket dedup ☐ Unit: proxyIds immutability ☐ Parity: internal vs external.

---

## SPARK-BOM-G16 · Test coverage & parity harness
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-BOM-B01, SPARK-BOM-E01, SPARK-BOM-G08, SPARK-BOM-G10
**Labels:** `dgs-migration`, `bom`, `tests`

**As a** DGS migration engineer **I want** unit + integration + parity coverage **so that** the BOM subgraph
matches spark-internal-graphql before cut-over.
**Target DGS Implementation:** ≥80% unit coverage on fetchers/services; a parity harness recording ≥30
query/mutation fixtures (all 7 material variants + both impression branches represented) and diffing JSON;
a CI schema-conformance check across the 7 material impls.
**Acceptance Criteria:** 1. Unit coverage ≥80%. 2. Parity harness covers all 7 material types + internal/external impression branch + `updateBom` 5 fixtures. 3. Schema-conformance check fails the build if an impl misses an interface field.
**Test Cases:** ☐ Parity: 30+ fixtures green ☐ CI: conformance check ☐ Load: p95 parity for `getBomByIds`, `getBomByParentId`, `searchMaterialsBom`.

---

## 4. Risk Register

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| `updateBom` 3-step non-atomic write | Medium | High | E01 failure strategy (saga/compensation/best-effort) | Tech Lead |
| `BomImpressionDetails_Unified.libraryResource` `args.ids` contract | Medium | Medium | G10 moves `bomIds` to DGS local context | Backend Eng |
| 7-variant polymorphism drift | Medium | Medium | G16 CI schema-conformance check | Backend Eng |
| Sibling material subgraphs not federated yet | High | Medium | Sequence hub/trim/wash/fabric/combination stubs first | Platform |
| Trim 15-case dispatcher porting errors (G08) | Medium | Medium | Parity table per trim type | Backend Eng |
| Latent bugs (`getHubMaterial` await; `getFabricMaterial` null; array mutation) | Medium | Low | Fix on port (G03/G05/G15) + unit tests | Backend Eng |
| F01/F02 are internal (same subgraph) — depend on Product/ResourcesCount types existing | Low | Low | Sequence after product A02/A05; no gateway block | Tech Lead |

## 5. Summary
- **Stories:** 42 (A:5 · B:8 · C:5 · D:5 · E:1 · F:2 · G:16).
- **Critical path:** A01→A02→A05→E01 and A04→G08/G10→G16.
- **Highest risk:** `updateBom` atomicity (E01); impression `args.ids` contract (G10).
- **Monorepo:** F01/F02 are **internal** field resolvers in the same `plm-product` subgraph (not gateway
  federation). Real cross-subgraph federation in BOM is only the **material DGS** references (hub/trim/wash/
  fabric/combination) + workspace/tag/user-profile/access-control.

---
**Phase Completed:** Phase 4 — Migration Stories · **Domain:** `bom` · **Outputs:** 04-stories.md, 04-stories-index.yaml, 04-po-summary.md.

---
