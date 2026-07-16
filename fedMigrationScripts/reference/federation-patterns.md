# Federation Patterns Reference

Patterns for entity federation, @key directives, entity fetchers, and cross-domain type composition.
Used by `skills/federation-candidate-detection` and `skills/federation-schema-derivation`.

---

## 1. Type Classification Categories

| Category | When to Use | Schema Pattern |
|----------|-------------|---------------|
| **Owned** | Data originates from this domain's backend | `type X @key(fields: "id") { ... }` |
| **Extended** | Type owned by another DGS; this domain adds fields | `extend type X @key(fields: "id") { newField: Type }` |
| **External stub** | Type owned by another DGS; referenced but not extended | `type X @key(fields: "id") @extends { id: ID! @external }` |
| **Gateway-only** | Resolved entirely by Hive Gateway | Same pattern as External stub |
| **Shared** | Utility types (Paging, CodeDescription) | `type X @shareable { ... }` |
| **Input** | Mutation input types | `input X { ... }` |
| **Enum** | Enumeration types | `enum X { ... }` |

---

## 2. Federation Key Rules

| Type Role | @key Directive | When |
|-----------|--------------|------|
| Primary entity | `@key(fields: "id")` | Default — covers 90% of cases |
| Dual-key entity | `@key(fields: "id humanId")` | When BOTH are used as independent lookup keys |
| Response wrapper / embedded | No `@key` | Not independently fetchable |
| Composite context | `@key(fields: "productId partnerId")` | Identity is a tuple (ResourcesCount pattern) |
| Input type | No `@key` | Inputs are never federated |
| Shared utility | `@shareable`, no `@key` | Paging, CodeDescription, etc. |

---

## 3. Schema Patterns

### Owned Entity Type

```graphql
# Primary entity — independently fetchable
type Bom @key(fields: "id") {
  id: ID!
  humanId: String
  type: Int
  product: Product   # External stub — gateway resolves
  materials: [BomMaterial]
}
```

### Extended Type (This Domain Adds Fields)

```graphql
# Another DGS owns Product, this domain adds a field
extend type Product @key(fields: "id") {
  id: ID! @external
  boms: [Bom]   # This domain owns this field
}
```

### External Stub (DGS-to-DGS Federation)

```graphql
# Product is owned by plm-product DGS, referenced here
type Product @key(fields: "id") @extends {
  id: ID! @external
}
```

### Gateway-Only Stub (Hive Gateway Resolves)

```graphql
# VMM Brand — never migrates to DGS, always Hive Gateway
type VMM_Brand @key(fields: "brandId") @extends {
  brandId: ID! @external
}
```

### Composite Key Entity (ResourcesCount Pattern)

```graphql
# Identity is a context tuple, not a single ID
type ResourcesCount @key(fields: "productId partnerId") {
  productId: ID!
  partnerId: ID!
  workspaceContext: String
  parentProductId: ID
  # Fields filled in by domain subgraphs:
  productAttachments: [ID] @requires(fields: "productId partnerId workspaceContext parentProductId")
}
```

---

## 4. Kotlin DGS Implementation Patterns

### Standard Entity Fetcher (DGS-to-DGS Federation)

```kotlin
@DgsEntityFetcher(name = "Product")
fun product(values: Map<String, Any>): Product? {
    val id = values["id"] as String
    return productService.getById(id)?.toGraphql()
}
```

### Gateway-Stitched Type Stub (Simple ID)

```kotlin
// DGS service returns only the key field; Hive Gateway fills the rest
brand = this.brandId?.let { Brand(brandId = it) }
```

### Gateway-Stitched Type Stub (List of IDs)

```kotlin
businessPartners = this.partnerIds?.map { VMM_BusinessPartner(bpId = it) }
```

### Composite Key Entity Fetcher

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

### Data Fetcher with DataLoader

```kotlin
@DgsQuery
fun getBom(@InputArgument id: String, dfe: DataFetchingEnvironment): CompletableFuture<Bom?> {
    val dataLoader = dfe.getDataLoader<String, Bom>(BomDataLoader::class.java)
    return dataLoader.load(id)
}

@DgsDataLoader(name = "Bom")
class BomDataLoader : MappedBatchLoaderWithContext<String, Bom> {
    override fun load(keys: Set<String>, environment: BatchLoaderEnvironment): CompletableFuture<Map<String, Bom>> {
        return CompletableFuture.supplyAsync {
            bomService.getByIds(keys).associateBy { it.id }
        }
    }
}
```

---

## 5. @requires Pattern

Use `@requires` when a field on an extended type needs context fields from the parent to resolve:

```graphql
extend type Product @key(fields: "id") {
  id: ID! @external
  partnerId: ID! @external  # needed for the resolver below
  boms(workspaceId: ID): [Bom] @requires(fields: "id partnerId")
}
```

```kotlin
@DgsData(parentType = "Product", field = "boms")
fun productBoms(dfe: DataFetchingEnvironment): List<Bom> {
    val product = dfe.getSource<Product>()
    return bomService.getByProductAndPartner(product.id, product.partnerId)
}
```

---

## 6. ACL Token Patterns

### V1 — Authorization Bearer

```kotlin
// Standard service call
fun getBom(id: String, token: String): Bom? {
    return feignClient.getBom(id, authorization = "Bearer $token")
}
```

### V2 — SPARK-Capability-Token

```kotlin
// For services requiring both headers
fun addBom(input: BomInput, token: String, capabilityToken: String): Bom {
    return feignClient.addBom(
        input = input,
        authorization = "Bearer $token",
        sparkCapabilityToken = capabilityToken
    )
}
```

---

## 7. Pagination Pattern

### Source (Node.js)
```javascript
const page = args.page ?? 0;
const size = args.size ?? 10;
return service.getListing({ page, size });
```

### Target (Kotlin DGS)
```kotlin
@DgsQuery
fun getBoms(
    @InputArgument page: Int = 0,
    @InputArgument size: Int = 10
): BomPaged {
    val pageable = PageRequest.of(page, size)
    return bomService.getListing(pageable)
}
```

---

## 8. Cross-Domain Reference Decision Tree

```
Is the referenced service an external platform?
(VMM, IG/Item Groups, Doppler, LDAP, APEX, Corona, Nexus,
 Assortment, Negotiator, Brand Compliance)
│
├── YES → GATEWAY STITCH
│         DGS returns stub key only.
│
└── NO → Is it a co-located domain (same backend URL)?
          │
          ├── YES → DIRECT RESOLUTION
          │         Same Feign client, same REST API. No federation boundary.
          │
          └── NO → Is the referenced service already migrated to DGS?
                    │
                    ├── YES → FEDERATION (@key + entity fetcher)
                    │
                    └── NO → EXT SERVICE STUB (treat as Gateway until migration)
                              Create CAT-4 story to revisit.
```

---

## 9. Multi-Subgraph Composite Key Pattern (TechPack / ResourcesCount)

Use when a composite key entity has **stub fields owned by multiple different subgraphs**. The defining subgraph creates the type and the query stub; each domain subgraph extends the type to resolve its own fields.

### When This Applies

- A query returns an aggregate "count" or "summary" object that collects data from many domains
- The entity's identity is a context tuple (e.g., `productId + partnerId`), not a single opaque ID
- Each field group is the responsibility of a different owning service (Attachment, Sample, BOM, etc.)
- Identified by schema comments on stub fields: `# → {domain} subgraph`

### Schema Distribution Across Subgraphs

```graphql
# ─── PRODUCT SUBGRAPH — defines the entity, owns the query ───────────────────
type ResourcesCount @key(fields: "productId partnerId") {
  productId:        ID!
  partnerId:        ID!
  workspaceContext: String    # carried via @requires — NOT part of @key
  parentProductId:  ID        # carried via @requires — needed for attachment rollup

  # Stub fields — Product returns null; each owning subgraph fills these in:
  productAttachments:    [ID]  # → Attachment subgraph
  discussionAttachments: [ID]  # → Attachment subgraph
  discussions:           [ID]  # → Discussion subgraph
  sample:                [ID]  # → Sample subgraph
  measurementSets:       [ID]  # → Measurement subgraph
  claims:                [ID]  # → Claims subgraph
  productBoms:           [ID]  # → BOM subgraph
  packagingBoms:         [ID]  # → BOM subgraph
  constructions:         [ID]  # → Construction subgraph
  watchlists:            [ID]  # → Watchlist subgraph
}

# ─── ATTACHMENT SUBGRAPH — extends and resolves its two fields ────────────────
extend type ResourcesCount @key(fields: "productId partnerId") {
  productId:        ID! @external
  partnerId:        ID! @external
  workspaceContext: String @external
  parentProductId:  ID  @external
  productAttachments:    [ID] @requires(fields: "productId partnerId workspaceContext parentProductId")
  discussionAttachments: [ID] @requires(fields: "productId partnerId")
}

# ─── SAMPLE SUBGRAPH (all other subgraphs follow the same extend pattern) ─────
extend type ResourcesCount @key(fields: "productId partnerId") {
  productId:        ID!    @external
  partnerId:        ID!    @external
  workspaceContext: String @external
  sample: [ID] @requires(fields: "productId partnerId workspaceContext")
}
```

### Story Decomposition Rule

One `getProductTechPackCountV1`-style query generates stories in **two groups**:

| Group | Type | Phase | Scope | Where Tracked |
|-------|------|-------|-------|--------------|
| ResourcesCount schema + `@key` | CAT-1 | Phase A | Product subgraph | Product `be-04-stories.md` |
| Product stub resolver | CAT-2 | Phase E | Product subgraph only | Product `be-04-stories.md` |
| Aggregation facade | CAT-3 | Phase E | Temp service (Option D Phase 1) | Product `be-04-stories.md` |
| Per-subgraph extension × N | CAT-4 | Phase F | One per owning subgraph | **Each owning domain's** `be-04-stories.md` |
| Facade retirement | CAT-4 | Phase F | After all subgraphs live | Product `be-04-stories.md` |

**N = number of owning subgraphs** (for `ResourcesCount`: N = 8 — Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist).

Until each domain is in scope, add a `BLOCKED-BY: {domain} migration` placeholder CAT-4 story in the Product domain file.

### Migration Phasing (Option D Hybrid — Recommended)

```
Phase 1 (Immediate):
  Product stub resolver → Aggregation Service → all 9 backend calls
  Stories: CAT-1 schema + CAT-2 stub + CAT-3 aggregation facade

Phase 2 (Gradual, as each domain subgraph comes online):
  Each domain subgraph adds:
    extend type ResourcesCount + @DgsEntityFetcher + @DgsData resolvers
  Aggregation service shrinks field-by-field.
  Stories: 1 CAT-4 per owning subgraph, tracked in THAT domain's be-04-stories.md

Phase 3 (Retirement):
  Aggregation service retired; ResourcesCount fully federated.
  Story: 1 CAT-4 cleanup tracked in Product be-04-stories.md
```

See `reference/techpack-migration-options.md` for full Option A/B/C/D analysis.

### Kotlin: Entity Fetcher Boilerplate (All Extending Subgraphs)

Every extending subgraph implements the same entity fetcher pattern:

```kotlin
@DgsEntityFetcher(name = "ResourcesCount")
fun resolveResourcesCount(values: Map<String, Any>): ResourcesCount = ResourcesCount(
    productId        = values["productId"] as String,
    partnerId        = values["partnerId"] as String,
    workspaceContext = values["workspaceContext"] as? String,
    parentProductId  = values["parentProductId"] as? String,
)

@DgsData(parentType = "ResourcesCount", field = "sample")
suspend fun sample(dfe: DgsDataFetchingEnvironment): List<String> {
    val rc = dfe.getSource<ResourcesCount>()
    return elasticClient
        .searchSamples(rc.productId, rc.partnerId, rc.workspaceContext)
        .content.map { it.id }
}
```

`workspaceContext` and `parentProductId` are not part of the `@key` but are available in the `_entities` call because they are declared as fields on the `ResourcesCount` type in the Product subgraph and returned by the Product stub resolver.

### Key Constraint: Context Fields vs. Key Fields

| Field | In `@key`? | Available to extending subgraphs? | How |
|-------|-----------|----------------------------------|-----|
| `productId` | YES | YES | Part of `@key` |
| `partnerId` | YES | YES | Part of `@key` |
| `workspaceContext` | NO | YES | Returned by Product stub; gateway passes in `_entities` |
| `parentProductId` | NO | YES | Returned by Product stub; gateway passes in `_entities` |

Declare non-key context fields as `@external` in extending subgraphs and reference them via `@requires`.
