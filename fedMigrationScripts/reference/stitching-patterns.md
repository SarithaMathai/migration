# Stitching Patterns Reference

Gateway stitching patterns, Hive Gateway configuration, and cross-domain join patterns.
Used by `skills/stitching-pattern-analysis` and `skills/migration-story-generation`.

---

## 1. External Platform Services (Always Gateway — Never DGS)

These services are **never migrated to DGS**. Always Hive Gateway stitch. DGS returns only the key field.

| Service | Loader Keys | What DGS Returns | Hive Resolves |
|---------|-------------|-----------------|--------------|
| VMM Business Partners | `vmm` | `{ bpId: "..." }` stub | Full business partner fields |
| VMM Brands | `brand` | `{ brandId: "..." }` stub | Full brand fields |
| Item Groups — Dept | `department` | `{ id: "..." }` stub | Full department fields |
| Item Groups — Div | `division` | `{ id: "..." }` stub | Full division fields |
| Item Groups — Class | `clazz` | `{ id: "..." }` stub | Full class fields |
| Doppler | `doppler` | `{ id: "..." }` stub | Supply plan details |
| LDAP Directory | `ldap` | `{ id: "..." }` stub | User directory fields |
| APEX | `apex` | `{ id: "..." }` stub | Product plan data |
| Corona Items | `coronaItems` | `{ tcin: "..." }` stub | Item attributes |
| Nexus Attributes | `nexusAttributes` | `{ id: "..." }` stub | Attribute data |
| Assortment Items | `assortmentItem` | `{ id: "..." }` stub | Assortment data |
| Negotiator Bids | `negotiatorBids` | `{ id: "..." }` stub | Bid data |
| Brand Compliance | `brandCompliance` | `{ id: "..." }` stub | Compliance data |

---

## 2. Stitching Complexity Ratings

| Complexity | Criteria | CAT-4 Effort |
|-----------|---------|-------------|
| **Low** | Single ID → stub. Pure gateway stitch. No transformation. | 1–2d |
| **Medium** | List of IDs → batch stub. Or conditional stitching on a flag. | 3–5d |
| **High** | Multi-step. Data from both DGS and external service in one response. | 5–8d |
| **Very High** | Composite key federation. `@requires`. Cross-domain aggregation. | 8–13d |

---

## 3. Hive Gateway Configuration Patterns

### Simple Type Merging (Single Service)

```yaml
sources:
  - name: bom-service
    handler:
      graphql:
        endpoint: https://plm-product-dgs.target.com/graphql
    transforms:
      - typeMerging:
          types:
            - typeName: Bom
              key: { selectionSet: "{ id }" }
              fieldName: getBom
              argsFromKeys: (ids) => ({ input: { ids } })
```

### Gateway Stitch for External Platform

```yaml
sources:
  - name: vmm-gateway
    handler:
      graphql:
        endpoint: https://stgapi-internal.target.com/graphql
    transforms:
      - typeMerging:
          types:
            - typeName: VMM_Brand
              key: { selectionSet: "{ brandId }" }
              fieldName: getBrandById
              argsFromKeys: (brandIds) => ({ brandIds })
```

### Stitching Multiple Services on One Type

```yaml
# Product type is resolved by multiple subgraphs
sources:
  - name: product-service
    handler:
      graphql:
        endpoint: https://plm-product-dgs.target.com/graphql
    transforms:
      - typeMerging:
          types:
            - typeName: Product
              key: { selectionSet: "{ id }" }
              fieldName: getProduct
  - name: attachment-service
    handler:
      graphql:
        endpoint: https://spark-attachment-dgs.target.com/graphql
    transforms:
      - typeMerging:
          types:
            - typeName: Product
              key: { selectionSet: "{ id }" }
              fieldName: _productAttachments   # entity fetcher on attachment DGS
```

---

## 4. DGS Stub Return Patterns (Kotlin)

### Simple ID Stub (Gateway-Stitched Type)

```kotlin
// DGS service returns only the key; Hive Gateway fills the full type
data class BomResolverResult(
    val id: String,
    val brand: VMM_Brand? = brandId?.let { VMM_Brand(brandId = it) }
)
```

### List of Stubs

```kotlin
val brands = partnerIds?.map { VMM_Brand(bpId = it) } ?: emptyList()
```

### Conditional Stub (Only Return When Key Exists)

```kotlin
val department = departmentId?.let { IgDepartment(id = it) }
```

---

## 5. Cross-Domain Join Patterns

### Pattern 1: Pass-Through Field (No Join)

The source domain includes the foreign key in its response. The gateway resolves the full type.

```graphql
type Product @key(fields: "id") {
  id: ID!
  brandId: ID          # DGS just stores this
  brand: VMM_Brand     # Gateway resolves using brandId
}
```

DGS Kotlin:
```kotlin
fun brand(): VMM_Brand? = brandId?.let { VMM_Brand(brandId = it) }
```

---

### Pattern 2: Entity Reference (DGS-to-DGS)

This domain returns a typed entity stub. The owning DGS adds the fields via entity fetcher.

```graphql
# BOM domain schema
type Bom @key(fields: "id") {
  id: ID!
  product: Product   # Product domain resolves this
}

type Product @key(fields: "id") @extends {
  id: ID! @external
}
```

DGS Kotlin (BOM side):
```kotlin
fun product(): Product? = productId?.let { Product(id = it) }
```

DGS Kotlin (Product side — entity fetcher):
```kotlin
@DgsEntityFetcher(name = "Product")
fun product(values: Map<String, Any>): Product? {
    val id = values["id"] as String
    return productService.getById(id)?.toGraphql()
}
```

---

### Pattern 3: @requires — Context-Dependent Resolution

When resolving a field on an extended type requires context fields from the parent:

```graphql
extend type Product @key(fields: "id") {
  id: ID! @external
  partnerId: ID! @external
  boms: [Bom] @requires(fields: "id partnerId")
}
```

DGS Kotlin (BOM domain):
```kotlin
@DgsData(parentType = "Product", field = "boms")
fun productBoms(dfe: DataFetchingEnvironment): List<Bom> {
    val product = dfe.getSource<Product>()
    // product.id and product.partnerId are available because of @requires
    return bomService.getByProductAndPartner(product.id, product.partnerId)
}
```

---

### Pattern 4: Composite Key (ResourcesCount Pattern)

For entities whose identity is a context tuple rather than a single ID:

```graphql
type ResourcesCount @key(fields: "productId partnerId") {
  productId: ID!
  partnerId: ID!
  workspaceContext: String
  parentProductId: ID
}
```

DGS Kotlin:
```kotlin
@DgsEntityFetcher(name = "ResourcesCount")
fun resolveResourcesCount(values: Map<String, Any>): ResourcesCount {
    return ResourcesCount(
        productId = values["productId"] as String,
        partnerId = values["partnerId"] as String,
        workspaceContext = values["workspaceContext"] as? String,
        parentProductId = values["parentProductId"] as? String,
    )
}
```

See `techpack-migration-options.md` at the project root for full analysis of the TechPack composite key pattern and migration options (B, C, D).

---

## 6. Migration Sequencing for EXT Dependencies

When a domain depends on a service not yet migrated to DGS:

### Phase 1 (Now — During Own Domain Migration)
- Implement a gateway stitch for the unresolved dependency
- DGS returns the stub key only
- Hive Gateway resolves via the existing spark-internal-graphql endpoint
- Create CAT-4 story: "Replace gateway stitch with federation when {service} migrates"

### Phase 2 (Later — When Dependency Migrates)
- Upgrade from gateway stitch to DGS-to-DGS federation
- Implement entity fetcher on the owning DGS
- Update Hive Gateway config to route to the new DGS endpoint
- Run parity tests to verify output matches

This is the **Option D: Hybrid** approach — facade now, federate later.

---

## 7. Stitching Strategy Decision Guide

| Scenario | Strategy | CAT-4 Pattern |
|---------|---------|--------------|
| Field references a VMM/IG/Doppler type | Gateway Stitch | Simple ID stub |
| Field references a co-located domain | Direct Resolution | No CAT-4 needed |
| Field references a migrated DGS service | Federation | Entity fetcher |
| Field references a not-yet-migrated service | Gateway Stitch (temporary) | Stub + CAT-4 follow-up story |
| Field requires context from parent to resolve | @requires | Extended type with @requires |
| Entity identity is a tuple | Composite key | `@key(fields: "a b")` |
