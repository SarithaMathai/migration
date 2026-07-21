---
name: stitching-pattern-analysis
description: "Determines the correct stitching strategy for every cross-domain field in a domain: federation via @key, Hive Gateway stitch, or direct resolution. Provides DGS Kotlin stub patterns, Hive Gateway YAML config patterns, and stitching complexity ratings. Can be invoked standalone for architecture Q&A or loaded by federation-schema-derivation and migration-story-generation."
argument-hint: "Invoked automatically by federation-schema-derivation and migration-story-generation. Can also be invoked directly: 'What stitching strategy should I use for Product.bom?' or 'What external services does product need to stitch?'"
---

# Skill: Stitching Pattern Analysis

## Purpose

Analyze cross-domain type references to determine:
- Which fields are **federated** via `@key` (both services are DGS)
- Which fields are **gateway-stitched** (external platform, Hive Gateway resolves)
- Which fields are **directly resolved** (same backend, no cross-service boundary)

Also provides the concrete implementation patterns for each strategy — Kotlin stub code, Hive Gateway YAML config, entity fetcher templates.

## When to Use

- **Standalone:** When an architect needs stitching strategy decisions without running the full pipeline
- **Loaded by `federation-schema-derivation`:** Drives CAT-4 story classification in `be-03-schema-analysis.md`
- **Loaded by `migration-story-generation`:** Drives CAT-4 story content in `be-04-stories.md`

## Cannot Run Without

- Cross-domain reference data — either from:
  - `output/{domain}/be-01-schema-inventory.md` Cross-Domain Reference table
  - `output/{domain}/be-02-resolver-analysis.md` EXT Service Call Inventory (preferred)
  - Or the engineer describes the specific field/type relationship directly

## Reference Files to Read First

| For… | Read |
|------|------|
| EXT severity scale (🔴 / 🟡 / 🔵) | `reference/output-conventions.md` §5 |
| Federation patterns and @key rules | `reference/federation-patterns.md` |
| External platform services list (gateway-only) | `reference/stitching-patterns.md` §1 |

---

## Stitching Strategy Decision Tree

```
Is the referenced service an external platform?
(VMM, IG/Item Groups, Doppler, LDAP, APEX, Corona, Nexus,
 Assortment, Negotiator, Brand Compliance)
│
├── YES → GATEWAY STITCH
│         DGS returns stub key only.
│         Hive Gateway resolves the full type.
│         No DGS entity fetcher needed.
│
└── NO → Is it a co-located domain (same backend URL)?
          │
          ├── YES → DIRECT RESOLUTION
          │         Same Feign client, same REST API.
          │         No federation boundary needed.
          │
          └── NO → Is the referenced service already migrated to DGS?
                    │
                    ├── YES → FEDERATION (@key + entity fetcher)
                    │         This DGS returns only the key field(s).
                    │         The owning DGS resolves the rest.
                    │
                    └── NO → EXT SERVICE (pending migration)
                              Treat as Gateway stitch for now.
                              Create a CAT-4 story to revisit when
                              the owning service migrates.
```

---

## External Platform Services (Always Gateway — Never DGS)

| Service | Loader Keys | What DGS Returns |
|---------|-------------|-----------------|
| VMM Business Partners | `vmm` | `{ bpId: "..." }` stub |
| VMM Brands | `brand` | `{ brandId: "..." }` stub |
| Item Groups (Dept) | `department` | `{ id: "..." }` stub |
| Item Groups (Div) | `division` | `{ id: "..." }` stub |
| Item Groups (Class) | `clazz` | `{ id: "..." }` stub |
| Doppler | `doppler` | `{ id: "..." }` stub |
| LDAP Directory | `ldap` | `{ id: "..." }` stub |
| APEX | `apex` | `{ id: "..." }` stub |
| Corona Items | `coronaItems` | `{ tcin: "..." }` stub |
| Nexus Attributes | `nexusAttributes` | `{ id: "..." }` stub |
| Assortment Items | `assortmentItem` | `{ id: "..." }` stub |
| Negotiator Bids | `negotiatorBids` | `{ id: "..." }` stub |
| Brand Compliance | `brandCompliance` | `{ id: "..." }` stub |

---

## Stitching Complexity Ratings

| Complexity | Criteria |
|-----------|---------|
| **Low** | Single ID → stub. Pure gateway stitch. No transformation. |
| **Medium** | List of IDs → batch stub. Or conditional stitching based on a flag. |
| **High** | Multi-step resolution. Data from both this domain and external service needed in one response. |
| **Very High** | Composite key federation. Context fields passed via `@requires`. Cross-domain aggregation (e.g., ResourcesCount pattern). |

---

## Implementation Patterns

### Gateway-Stitched Type (Simple ID Stub — Kotlin)

```kotlin
// DGS service — return stub, Hive Gateway fills the rest
brand = this.brandId?.let { Brand(brandId = it) }
```

### Gateway-Stitched Type (List of IDs — Kotlin)

```kotlin
businessPartners = this.partnerIds?.map { VMM_BusinessPartner(bpId = it) }
```

### DGS-to-DGS Federation (Entity Fetcher — Kotlin)

```kotlin
@DgsEntityFetcher(name = "Product")
fun product(values: Map<String, Any>): Product? {
    val id = values["id"] as String
    return productService.getById(id)?.toGraphql()
}
```

### Composite Key Federation (ResourcesCount Pattern — Kotlin)

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

### Hive Gateway Type Merging Config (YAML)

```yaml
sources:
  - name: {dgs-service}
    handler:
      graphql:
        endpoint: {url}
    transforms:
      - typeMerging:
          types:
            - typeName: {TypeName}
              key: { selectionSet: "{ id }" }
              fieldName: {lookupQuery}
```

---

## Step-by-Step Procedure (Standalone Invocation)

### Step 1: Load Cross-Domain References

Load from the EXT Service Call Inventory (Phase 2) if available. Otherwise load from the Cross-Domain Reference table (Phase 1).

### Step 2: Apply Decision Tree

For each cross-domain reference, apply the decision tree above and record:
- Strategy
- Implementation pattern needed
- Severity
- Whether a CAT-4 story is required

### Step 3: Produce Stitching Strategy Output

```markdown
## Stitching Strategy — {Domain}

| Field | Referenced Type | Domain | Strategy | Complexity | Kotlin Pattern | CAT-4 Required? |
|-------|----------------|--------|----------|-----------|---------------|----------------|
| {Type}.{field} | {RefType} | {domain} | Gateway Stitch | Low | Simple ID stub | Yes — minimal |
| {Type}.{field} | {RefType} | {domain} | Federation | Medium | Entity fetcher | Yes — entity fetcher |
```

### Step 4: Produce Implementation Templates

For each CAT-4 boundary, provide:
- DGS Kotlin stub code
- Hive Gateway YAML config (for gateway-stitched types)
- Schema stub pattern (`@extends` + `@external`)

---

## Output

When invoked **standalone:**
Produces Stitching Strategy table and implementation templates in chat. No file written.

When loaded by **`federation-schema-derivation`:**
Type classification and external stubs are fed into `be-03-schema.graphql` and `be-03-schema-analysis.md`.

When loaded by **`migration-story-generation`:**
CAT-4 story content (Gateway config, entity fetcher implementation) is embedded in `be-04-stories.md`.

---

## Completion Criteria (Standalone)

- [ ] Every cross-domain reference has a strategy assigned
- [ ] Gateway-only services correctly identified (never marked for DGS migration)
- [ ] Stitching complexity rating applied to each boundary
- [ ] Kotlin implementation pattern provided for each CAT-4 boundary
- [ ] Hive Gateway YAML config provided for each gateway-stitched type
- [ ] CAT-4 story requirement flagged for each EXT boundary
