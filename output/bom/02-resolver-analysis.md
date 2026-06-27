# Bom — Resolver Analysis: Queries

> **Domain:** `bom` · **Source:** [resolvers/product/SPARK_Bom.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_Bom.js) (lines 80–225)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18
> **Depends on:** [01-schema-inventory.md](output/bom/01-schema-inventory.md)

12 query resolvers. Effort below is raw days (apply +20% buffer at Phase 4).

---

## Q1 · `getBomByIds(ids: [String!]) : [SPARK_Bom]` — CAT-2 · Small (1–2d)

**Pseudocode:**
```
if ids.empty -> []
permissionJWT = await getUserPermissionsJWT(ids, ctx)
return ctx.loaders.bom.getBomByIds(permissionJWT, ids)
```
**Service:** `BomService.getBomByIds` → `GET /enterprise_product_development_products/bom/v1?ids={ids}` with `SPARK-Capability-Token` header.
**Notes:** Empty-array short-circuit. `getBomByIds` is *not* DataLoader-batched at the resolver level — `ids` passed through directly. Verify whether a request-scoped DataLoader is needed in DGS.

---

## Q2 · `getBomDataV2(ids: [String!]) : [SPARK_Bom_Unified]` — CAT-2 · Small (1–2d)

**Pseudocode:** Identical to Q1, returns same data shaped as `SPARK_Bom_Unified`. **Schema-only difference** — same REST call, same loader.
**Finding 🟡:** Both queries call the same backend with different return types. Confirm whether `SPARK_Bom_Unified` is a strict subset of `SPARK_Bom` (it appears so — fewer fields).

---

## Q3 · `getBomStatus : [SPARK_CodeDescription]` — CAT-2 · Small (<1d)

**Pseudocode:** `ctx.loaders.bom.getBomStatus()` → `GET /masterData?name=BomStatus`. Transform: `{key: value}` map → `[{code, description}]`. **Master data — cacheable.**

---

## Q4 · `getBomByParentId(parentId: String!) : SPARK_BomPaged` — CAT-2 · Small (1–2d)

**Pseudocode:**
```
permissionJWT = await getUserPermissionsJWT(parentId, ctx)
boms = await ctx.loaders.bom.getActiveBomsByProductId(permissionJWT, parentId)
return { content: orderBy(boms, b -> new Date(b.createdAt), 'desc') }
```
**Service:** `GET /enterprise_product_development_products/bom/v1/byProductId/{parentId}`. Client-side `createdAt DESC` sort.
**Finding 🟡:** Sort done in gateway, not backend. Verify backend can sort to remove this hop.

---

## Q5 · `getBomMaterialTypes(ids: [String]) : [SPARK_BomMaterialType]` — CAT-2 · Medium (3–5d)

**Pseudocode:**
```
[bomMaterialTypes, materialHubTypes] = await Promise.all([   // (today: sequential — fix in port)
  ctx.loaders.bom.getBomMaterialTypes(ids),
  ctx.loaders.materialHub.getHubMaterialTypes.load()
])
return [
  ...bomMaterialTypes,
  ...materialHubTypes.map(t => ({ code: 9, description: t, bomType: {code:1, description:'Product'}, libraryLink: true, freeText: true }))
]
```
**Services:** `BomService.getBomMaterialTypes` + Material-Hub loader.
**Finding 🟡 perf:** Source `await`s sequentially — easy parallelism win in port.

---

## Q6 · `getBomPackagingMaterialTypes : [SPARK_BomMaterialType]` — CAT-2 · Small (<1d)

`GET /enterprise_product_development_products/master_data/packaging_bom_material_types`. **Master data — cacheable.**

---

## Q7 · `getBomPackagingSubstrates : [SPARK_BomPackagingSubstrate]` — CAT-2 · Small (<1d)

`GET /enterprise_product_development_products/master_data/packaging_bom_substrate_types`. **Master data — cacheable.**

---

## Q8 · `getBomPackagingUnitOfMeasure : [SPARK_UnitsOfMeasure]` — CAT-2 · Small (<1d)

`GET /enterprise_product_development_products/master_data/packaging_unit_of_measure`. **Master data — cacheable.**

---

## Q9 · `getBomElastic(q: String!) : [SPARK_Bom]` — CAT-2 · Small (1–2d)

**Pseudocode:** `ctx.loaders.search.getBomElastic.load(query)` → returns `{content}` → return `content` only.
**Service:** elastic search (not in `BomService`). **No JWT — elastic queries usually carry pre-filtered ACL.**
**Notes:** Source passes the **entire `query` object** (not just `q`) into `.load()` — confirm exact field set expected by elastic.

---

## Q10 · `searchMaterialsBom(searchString, materialType, partnerIds, internalOnly, excludedTypes, size, sortField, sortDirection, nestedSearchFilters)` — CAT-2 · Medium (3–5d)

**Pseudocode:**
```
fabricSuppliers = await VMM_BusinessPartner.Query.getRelatedFabricSuppliersByMerchVendors(null, {merchVendorIds: partnerIds}, ctx)
queryPayload = { q: searchString, type, fabricSuppliers, partnerIds, internalOnly, excludedTypes, size, sortField, sortDirection }
if (nestedSearchFilters?.length)
  for each filter[i]:
    queryPayload[`nestedSearchFilters[${i}].type`] = filter.type
    ...4 more keys
  delete queryPayload.nestedSearchFilters
return ctx.loaders.search.searchMaterialsBom.load(queryPayload)
```
**Services:** VMM cross-resolver call + elastic.
**Finding 🟡:** The `nestedSearchFilters[i].field` query-string flattening is fragile. **In DGS port, pass as proper nested DTO** to backend if supported, otherwise wrap in a single helper. Document the existing serialization contract.

---

## Q11 · `getValidTrimSuppliersForBom(merchVendorIds: [ID]) : [Int]` — CAT-2 · Small (<1d)

```
return getRelatedSuppliersForMVs(ctx, merchVendorIds, [BusinessPartnerRole.TRIM_SUPPLIER.code])
```
Single VMM call via `vmmUtils.getRelatedSuppliersForMVs`. Returns array of partner IDs.

---

## Q12 · `getValidRawMaterialSuppliersForBom(merchVendorIds: [ID]) : [Int]` — CAT-2 · Small (<1d)

Same as Q11 but with `[RAW_MATERIAL_SUPPLIER, FABRIC_SUPPLIER, TRIM_SUPPLIER]` roles.

---

## Q13 · `getComboSupplierForBom(comboId: String, partnerIds: [ID]) : [SPARK_BomComboSupplier]` — CAT-2 · Medium (3–5d)

**Pseudocode:**
```
fabricSpecCombos = await SPARK_Combination.Query.searchFabricSpecCombos(null, {q:`parentComboId:${comboId}`, page:0, size:100}, ctx)
filtered = combos.filter(c => c.fsId && ((partnerIds?.length && c.mvIds?.length === 1 && partnerIds.includes(c.mvIds[0])) || !partnerIds?.length))
suppliers = []
await Promise.all(filtered.map(async c => {
  fs = await ctx.loaders.vmm.getByID.load(c.fsId)
  if (fs.bpName) suppliers.push({fabricSupplier: {id: c.fsId, name: fs.bpName}, fabricSpecCombo: c})
}))
return suppliers
```
**Cross-resolver call** into `SPARK_Combination` + VMM lookup per combo. Race-tolerant `push` into shared array works because each is awaited in `Promise.all`.

**Finding 🟡:** `partnerIds && partnerIds.length > 0 && fabricSpecCombo && ...` — the `c.mvIds.length === 1` constraint silently filters out multi-MV combos. Document — may be intentional.

---

## Cross-Cutting Findings

| # | Finding | Severity |
|---|---|---|
| 1 | 4 master-data queries (Q3, Q6, Q7, Q8) ripe for `@Cacheable` in DGS | 🟢 perf |
| 2 | Q5 sequential `await` of two independent loaders — parallelize | 🟢 perf |
| 3 | Q10 flattens nested filters into query-string keys — fragile | 🟡 |
| 4 | Q9 passes entire `query` object (not just `q`) into elastic loader — verify | 🟡 |
| 5 | Q1 not DataLoader-batched at resolver level; downstream `BomService.getBomByIds` makes one REST call per resolver invocation | 🟡 |
| 6 | Q13 cross-domain dependency on `SPARK_Combination.Query.searchFabricSpecCombos` — couples bom to combination subgraph migration order | 🟡 coordination |
| 7 | `getRelatedFabricSuppliersByMerchVendors` is reached by importing `VMM_BusinessPartner` resolver directly — anti-pattern; replace with service-level call in DGS | 🟡 |

---

## Effort Summary

| Tier | Queries | Days |
|---|---|---|
| Small | Q1, Q2, Q3, Q4, Q6, Q7, Q8, Q9, Q11, Q12 (10) | 8–14 |
| Medium | Q5, Q10, Q13 (3) | 9–15 |
| **Subtotal queries** | **13** | **17–29** |

---

**Phase Completed:** Phase 2A — Query Resolvers
**Output:** [output/bom/02-resolver-analysis.md](output/bom/02-resolver-analysis.md)
