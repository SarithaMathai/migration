# Migration Options: `getProductTechPackCountV1`

> **Scope:** This document covers migration options specifically for `getProductTechPackCountV1` and its underlying helper `getTechPackResourceCountMap` from the Node.js gateway (`SPARK_Product.js`) to Netflix DGS (Kotlin/Spring Boot).

---

## What This Query Actually Does (Plain English)

A user opens a product's tech pack and asks: **"How many attachments, samples, BOMs, claims, measurement sets, constructions, and watchlists does this partner have access to for this product?"**

The current Node.js implementation does this in roughly 17 steps:

```
Input: productId, partnerId, workspaceContext, parentProductId

Step 1:  Call ACL service → get relationship tree filtered by partner permission
         (for both current product AND parent product if provided)

Step 2:  Merge attachment IDs from both product trees (v2 + v3 attachments)

Step 3:  Call Attachment service → hydrate all attachment objects

Step 4:  Check each attachment for product_packet_props
         (is this attachment marked "critical" for this partner?)

Step 5:  Fire 7 Elasticsearch queries IN PARALLEL:
         ├── samples        (filter by workspaceContext, evaluationStatus 101/102)
         ├── criticalDiscussions (filter by partner security, critical=true)
         ├── measurementSets     (filter by partner, workspace, statusId=200)
         ├── claims              (filter by partner, workspace, statusId=501)
         ├── boms                (filter by partner, workspace, statusId=501)
         ├── constructions       (filter by partner, workspace, archived=false)
         └── watchlists          (filter by partner, workspace, statusId=501)

Step 6:  From criticalDiscussions → extract parentDiscussionIds, criticalDiscussionIds, criticalThreadIds

Step 7:  If critical IDs exist → search Elastic for attachments by parent resources

Step 8:  Filter and deduplicate all IDs

Output: ResourcesCount {
  productAttachments, discussionAttachments, discussions,
  sample, measurementSets, claims, productBoms, packagingBoms,
  constructions, watchlists
}
```

### Services Called

| Service | How | Why |
|---|---|---|
| ACL / Relationship | `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission` | Build ACL-filtered resource tree |
| Attachment REST API | `getAttachmentsV3` | Hydrate attachment objects to read `product_packet_props` |
| Elasticsearch (x7) | `getSamplesPage`, `searchDiscussionsElastic`, `getMeasurementSets`, `getClaimsElastic`, `getBomElastic`, `getProductDetailsElastic`, `searchWatchlist` | Count resources per domain |
| Elasticsearch (x1) | `searchAttachmentsByParentResources` | Find attachments linked to critical discussions |

---

## Option A: Port Directly into DGS Service Layer (Kotlin Coroutines)

### What It Means

Translate the Node.js `getTechPackResourceCountMap` function line-by-line into a Kotlin Spring Service. Use Kotlin coroutines (`coroutineScope { async {} }`) to run the 7 Elasticsearch queries in parallel, exactly as `Promise.all` does today.

### Pros
- All logic lives in one place — easy to trace, test, and debug
- No new infrastructure to deploy
- Kotlin coroutines are a direct equivalent of JavaScript `Promise.all`
- Full control over error handling and retry at each step

### Cons
- DGS Product service becomes an orchestrator — it calls 3+ other service APIs directly
- Tight coupling: if ACL, Attachment, or Elastic APIs change, this service must change
- Migration effort is HIGH — need to port all utility functions (ACL tree traversal, `product_packet_props` filtering, critical discussion reduction) into Kotlin
- `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission` in `commonLoaders.js` is 200+ lines of complex logic — requires a spike to understand fully before porting

### Risk: HIGH
The ACL tree traversal function is the most complex part. Porting it incorrectly will produce wrong counts silently.

---

## Option B: Temporary Aggregation Facade (Recommended for Day 1)

### What It Means

Do NOT port the logic yet. Create a thin Kotlin HTTP client in DGS that calls a **dedicated aggregation service**. That aggregation service is a new Node.js (or Kotlin) microservice that wraps the existing `getTechPackResourceCountMap` logic exactly as-is. The DGS resolver makes ONE call to the aggregation service.

**Option B1 — Node.js port (fastest):** Extract `getTechPackResourceCountMap` from `SPARK_Product.js` into a standalone Express.js microservice. Add a REST endpoint. This is a copy-paste with minimal changes (~1–2 days).

**Option B2 — Kotlin port (cleaner):** Port the logic to a separate Kotlin Spring Boot service (not the DGS service). Keeps the DGS service clean, isolates the complexity (~5–8 days).

### Pros
- DGS Product service stays clean — zero orchestration logic in it
- Lowest risk: the aggregation service runs the exact same logic as today
- Independent deployability: aggregation service can be updated without touching DGS
- Can be retired gradually: replace aggregation calls with federated resolvers one by one
- Fastest path to having `getProductTechPackCountV1` working in DGS

### Cons
- Extra network hop per request (DGS → Aggregator → 9+ services)
- Risk of becoming permanent if there is no active plan to retire it
- Requires a new service to be deployed, monitored, and maintained
- Does not move toward federation — it is a transitional layer only

### Risk: LOW (for migration), MEDIUM (long-term if not retired)

---

## Option C: Decompose Across Domain Subgraphs (Pure Federation)

### What It Means

Split the 7 Elasticsearch queries and the attachment logic across the subgraphs that OWN those domains. `ResourcesCount` is defined with a composite federation key `@key(fields: "productId partnerId")`. Each domain subgraph resolves its own fields via federated entity resolution using `@requires`.

The Product subgraph creates the `ResourcesCount` stub with the key fields and context (productId, partnerId, workspaceContext, parentProductId). Each domain subgraph receives this full entity and fills in its own count fields.

The gateway parallelises the `_entities` calls to all owning subgraphs automatically.

### Pros
- True federation — each domain owns its own count logic entirely
- No orchestration in any single service; no aggregation service needed
- Domain subgraphs deploy and scale independently
- Cleanest long-term architecture — ownership boundaries are explicit

### Cons
- Requires ALL domain subgraphs to exist and be Hive-registered before this can work end-to-end
- ACL tree traversal must be fully ported into the Attachment subgraph — hardest single piece
- NOT viable until Attachment, Discussion, Sample, BOM, Measurement, Claims, Construction, and Watchlist subgraphs all exist and are registered

### Risk: VERY HIGH (for now), LOW (when all subgraphs exist)

---

## Option D: Hybrid — Facade Now, Federate Later (Recommended Overall)

### What It Means

Combine Options B and C in phases:

**Phase 1 (Now):** Use Option B1. Extract the existing Node.js logic into a Temporary Aggregation Service. DGS Product makes one call to it. Ship working functionality with zero risk (~2–3 days).

**Phase 2 (As subgraphs come online):** As each domain subgraph (Attachment, Sample, BOM, Claims, etc.) is built and registered with Hive, migrate that section OUT of the aggregation service and INTO the owning subgraph. The aggregation service shrinks over time (~2–3 days per section).

**Phase 3 (Done):** Once all 7 domain sections have moved into their subgraphs, retire the aggregation service. The ResourcesCount type is now fully federated (~1 day).

### Pros
- Delivers working functionality on Day 1 with lowest risk
- Clear retirement plan built in — the facade does not become permanent
- Each domain team can migrate their section independently
- No big-bang rewrite required

### Cons
- Requires active governance to ensure the aggregation service is actually retired
- Temporary extra latency from the facade hop (acceptable during migration window)

---

## Recommendation

| Phase | Action | Option | Effort |
|---|---|---|---|
| Now (Sprint 6) | Extract `getTechPackResourceCountMap` into a standalone Aggregation Service (Node.js copy-paste). Wire DGS to call it. | **Option B1** | 2–3 days |
| Sprint 7–8 | Port ACL tree traversal and attachment criticality logic to Kotlin. Write integration tests comparing output with the Node.js version. | Preparation for C | 5–8 days |
| Sprint 8–9 | As Attachment and Sample subgraphs come online, migrate their sections out of the aggregator | **Option D (Phase 2)** | 2–3 days per section |
| Sprint 9+ | Retire aggregation service once all sections federated | **Option C** | 1 day |

---

## Key Risk: ACL Tree Traversal

The single hardest piece to migrate is `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission` from `commonLoaders.js`. It:

- Traverses a multi-level relationship graph
- Filters by partner ACL permissions at each level
- Is shared across multiple domains (not just product)
- Returns a nested map keyed by attachment type and depth level

**Before any Option A or C work begins, run a spike to:**
1. Map all inputs and outputs of this function
2. Understand which service owns the relationship graph (Relationship Service)
3. Decide whether this logic moves to the Relationship subgraph or stays in an ACL utility layer
4. Write contract tests that capture current output for known inputs

Without this spike, any port of TechPack logic risks silently producing wrong counts.

---

## Decision Checklist

Answer these before choosing your option:

- [ ] Are any of the 7 domain subgraphs (Attachment, Sample, BOM, etc.) already built?
  - Yes → Start Option D Phase 2 for those domains
  - No → Start with Option B1 (fastest path)

- [ ] Is the Relationship/ACL service being migrated as part of this sprint?
  - Yes → Option A is possible in parallel
  - No → Option B1 is the only safe choice right now

- [ ] Is there a hard deadline for deprecating the Node.js gateway?
  - Hard deadline → Option B1 (days, not weeks)
  - Flexible → Option A or D Phase 1 with Kotlin port

- [ ] Is there an owner for the Aggregation Service?
  - If yes → Option B is viable
  - If no → Option A (keep it in plm-product) to avoid service ownership gaps
