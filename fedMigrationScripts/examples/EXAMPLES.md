# Migration Pipeline — Copy-Paste Examples

> These are real invocations you can type into Claude Code or GitHub Copilot. Each shows the exact command, what the agent will do, and what output to expect.

---

## Example 1: Full BOM Domain Analysis (All Phases)

**What you type:**
```
Analyze the bom domain for DGS migration — run all phases.
```

**What happens:**
1. Phase 0: Agent confirms `bom` loader key, source files `SPARK_Bom.graphql` + `product/SPARK_Bom.js`, output folder `output/bom/`
2. Phase 1: Reads `context.js`, schema (BOM types, inputs, enums), resolver file, `BomService`, `bomUtils.js`, `commonLoaders.js`
3. Phase 2: Documents every resolver method (`getBom`, `getBomByPartnerAndProduct`, `addBom`, etc.) with pseudo-logic, REST endpoints, error handling
4. Phase 3: Derives `output/bom/be-03-schema.graphql` — classifies `Bom`, `BomMaterial`, `BomPaged` as Owned; `Product` as External stub
5. Phase 4: Breaks into ~25–35 Jira stories with `BOM-BE-` prefix, grouped by phases A–G

**Files written:**
```
output/bom/be-01-schema-inventory.md
output/bom/be-02-resolver-analysis.md
output/bom/be-03-schema.graphql
output/bom/be-03-schema-analysis.md
output/bom/be-04-stories.md
output/bom/be-04-po-summary.md
```

**Time:** ~15–25 minutes

---

## Example 2: Schema Inventory Only (Fast Scope Check)

**What you type:**
```
Run Phase 1 for the measurement domain.
```

**What happens:**
- Reads `SPARK_Measurement.graphql`, `product/SPARK_Measurement.js`, `MeasurementService.js`
- Reads referenced utils (likely `loadListing.js`, `accessControlUtils.js`)
- Produces one file: `output/measurement/be-01-schema-inventory.md`

**What you get (excerpt from output):**
```markdown
### Schema Files
| File | Path | Lines | Types | Inputs | Enums | Queries | Mutations |
|------|------|-------|-------|--------|-------|---------|-----------|
| SPARK_Measurement.graphql | spark-internal-graphql/packages/.../schemas/ | 340 | 8 | 5 | 2 | 9 | 6 |

### Cross-Domain References
| Field | Referenced Type | Domain | Loader Key | Severity |
|-------|----------------|--------|------------|----------|
| measurementSet.product | Product | product | product | 🟡 YELLOW |
```

**Time:** ~3–5 minutes

---

## Example 3: Resolver Analysis Without Stories

**What you type:**
```
Run Phase 1 and 2 for the attachment domain. I don't need stories yet.
```

**What happens:**
- Phase 1 catalogs all attachment files (`be-01-schema-inventory.md`)
- Phase 2 produces full pseudo-logic for every resolver and service method (`be-02-resolver-analysis.md`)
- Stops after Phase 2 — schema derivation and stories not run

**Useful when:** You want to review the pseudo-logic with the team before committing to a story breakdown.

---

## Example 4: Schema Only (Skip Stories)

**What you type:**
```
Run Phases 1, 2, and 3 for the discussion domain. Stop before stories.
```

**What happens:**
- Runs full pipeline through Phase 3
- Writes `be-03-schema.graphql` and `be-03-schema-analysis.md`
- Does NOT write `be-04-stories.md`

**Useful when:** You need the schema contract to share with the architecture team, but story breakdown is scheduled for a later sprint.

---

## Example 5: Stories From Existing Analysis

**What you type:**
```
Run Phase 4 for the bom domain. Phases 1, 2, and 3 outputs are already in output/bom/.
```

**What happens:**
- Reads `output/bom/be-02-resolver-analysis.md` for pseudo-logic
- Reads `output/bom/be-03-schema.graphql` for schema contract
- Reads `output/bom/be-03-schema-analysis.md` for type classifications and EXT stubs
- Generates stories with `BOM-BE-` prefix, writes `be-04-stories.md` and `be-04-po-summary.md`

**Useful when:** Phases 1–3 already ran and you want to re-generate or refine stories.

---

## Example 6: Quick Scan of a Large Domain

**What you type:**
```
Give me a quick scan of the product domain — top-level operations only, no field resolvers, no utils.
```

**Agent used:** `quick-scope`

**What you get:**
- Summary table: 18 queries, 23 mutations, complexity distribution
- Top-3 highest complexity operations flagged
- EXT service dependency count (not full detail)
- Estimated total effort range

**Time:** ~5 minutes (vs 60 minutes for full pipeline)

**Useful when:** PO or tech lead needs a scope estimate before committing to full analysis.

---

## Example 7: Federation Readiness Assessment

**What you type:**
```
Assess federation readiness for the attachment domain.
```

**Agent used:** `federation-readiness`

**What you get:**
- Entity boundary analysis: which types should be `@key` federated
- Cross-domain reference table with strategy per field (federation vs. gateway stitch vs. direct)
- `@key` candidate decisions with rationale
- EXT service calls requiring CAT-4 stories

**Time:** ~10 minutes

**Useful when:** An architect needs federation design decisions before committing to full analysis.

---

## Example 8: Schema Ownership Investigation

**What you type:**
```
Analyze schema ownership for the discussion domain.
```

**Agent used:** `schema-ownership`

**What you get:**
- File inventory (Phase 1 output)
- Type ownership classification: Owned / Extended / External stub / Shared
- Co-located domain siblings
- Which fields are gateway-stitched and which need federation entity fetchers

**Time:** ~10 minutes

**Useful when:** Tech lead needs to understand what a domain owns before planning the migration sprint.

---

## Example 9: Explain a Specific Operation

**What you type:**
```
Explain what getTechPackResourceCountMap does in SPARK_Product.js. What services does it call?
```

**What you get:**
- Step-by-step plain-English explanation of the function
- Table of all 9+ services it calls
- Migration recommendation (references `reference/techpack-migration-options.md`)
- Complexity rating: Very High

**Useful when:** Investigating a specific piece of complexity before starting the full migration.

---

## Example 10: Find All External Service Dependencies

**What you type:**
```
What external services does the product domain call? Show me all EXT service calls with severity.
```

**What you get:**
```
EXT Service Call Inventory — Product Domain

| # | Called From | Service | Key | URL | Severity |
|---|-------------|---------|-----|-----|----------|
| 1 | attachmentsWithMetaData | AttachmentService | attachment | spark-attachment.dev... | 🔴 RED |
| 2 | attachmentsWithMetaData | RelationshipService | relationship | spark-relationship... | 🔴 RED |
| 3 | getProducts | ElasticSearch | search | ... | 🟡 YELLOW |
| ... | ... | ... | ... | ... | ... |
| 29 | division field resolver | IgDivisionService | division | stgapi-internal... | 🔵 BLUE |
```

**Useful when:** Architecture team needs to understand federation boundaries.

---

## Example 11: PO Sprint Plan Only

**What you type:**
```
The BOM analysis is complete — all 6 output files are in output/bom/. Give me a sprint sequencing plan for a team of 3 engineers.
```

**What you get:**
- Sprint-by-sprint table with story IDs, effort, and what each sprint unlocks
- Parallelism opportunities called out
- Critical path highlighted
- Risk flags per sprint

---

## Example 12: Audit Existing Output

**What you type:**
```
Audit output/product/be-04-stories.md — check it against the story format and report any gaps.
```

**What you get:**
- List of stories missing acceptance criteria
- Stories without Phase 2 pseudo-logic in the "Current Behavior" section
- Stories missing test cases
- Stories where effort estimate seems inconsistent with complexity rating

**Useful when:** Reviewing output before handing to the engineering team.

---

## Sample Output Excerpts

### From `be-02-resolver-analysis.md` (Phase 2)

```markdown
### Q3: `getProductTechPackCountV1`

**Schema signature:**
```graphql
getProductTechPackCountV1(input: SPARK_ProductTechPackCountInput!): SPARK_ResourcesCount
```

**Resolver location:** `resolvers/SPARK_Product.js:83-293`
**Complexity:** Very High

**Pseudo-logic:**
1. Extract `productId`, `partnerId`, `workspaceContext`, `parentProductId` from input.
2. Call `getTechPackResourceCountMap(ctx, productId, partnerId, workspaceContext, parentProductId)`.
   - This helper (~200 lines) performs all the heavy lifting — see Helper H3.
3. Return the `ResourcesCount` object from the helper.

**EXT Service calls:**
1. **EXT Service** → key: `attachment` · url: `spark-attachment.dev.target.com` · repo: `spark-attachment` · severity: 🔴 RED
   Purpose: Hydrate attachment objects to read product_packet_props.critical flags.
2. **EXT Service** → key: `relationship` · url: `spark-relationship.dev.target.com` · severity: 🔴 RED
   Purpose: Get ACL-filtered resource tree for product and parent product.

**Error handling:**
- Any EXT call failure → propagates as GraphQL error (no fallback)
- Empty attachment list → skips product_packet_props filter, returns zero counts
```

---

### From `be-04-po-summary.md` (Phase 4)

```markdown
| Story ID | Title | Priority | Effort | Dependencies | Phase | Description |
|----------|-------|----------|--------|-------------|-------|-------------|
| BOM-BE-A-01 | Schema: BOM domain in DGS | P0 | Small (1-2d) | None | A | Add bom.graphqls to plm-product with BOM types, queries, mutations |
| BOM-BE-B-01 | Query: getBom by ID | P0 | Small (1-2d) | A-01 | B | Implement getBom data fetcher calling BOM REST API |
| BOM-BE-C-01 | Mutation: addBom | P0 | Medium (3-5d) | A-01, B-01 | C | Implement addBom with workspace association and ACL token |
| BOM-BE-D-01 | Federation: BOM ↔ Product | P1 | Medium (3-5d) | A-01, B-01 | D | Set up Hive Gateway type merging for BomPaged on Product |
```

---

### From `be-03-schema.graphql` (Phase 3)

```graphql
# =============================================================================
# BOM Domain — Derived DGS Schema (Target State)
# Pipeline Version: 1.1
# Generated: 2026-05-17
# DGS Target: Green-field (no existing schema)
# Source:    spark-internal-graphql/.../schemas/SPARK_Bom.graphql
# Target:    plm-product/apps/app/src/main/resources/schema/bom.graphqls
# =============================================================================

# --- External stubs (resolved by Hive Gateway) ---
type Product @key(fields: "id") @extends {
  id: ID! @external
}

# --- Owned types ---
# 🔜 Needs migration
type Bom @key(fields: "id") {
  id: ID!
  humanId: String
  type: Int
  statusId: Int
  product: Product   # stub — gateway resolves
  materials: [BomMaterial]
}

# --- Queries ---
extend type Query {
  # 🔜 Needs migration
  getBom(id: ID!): Bom
  # 🔜 Needs migration
  getBomByPartnerAndProduct(partnerId: ID!, productId: ID!): BomPaged
}
```

---

## Example 13: TechPack Multi-Subgraph Decomposition

**What you type:**
```
getProductTechPackCountV1 returns ResourcesCount which has stub fields for Attachment, Sample, BOM, Claims, Measurement, Construction, Watchlist, and Discussion subgraphs. Break this into sub-stories following the composite key entity pattern.
```

**Agent used:** `full-migration-investigation` (Phase 4)

**What happens:**
- Agent detects `ResourcesCount` has `@key(fields: "productId partnerId")` composite key in the schema analysis.
- Reads `reference/federation-patterns.md` §9 (Multi-Subgraph Composite Key Pattern).
- Generates:
  1. **PRODUCT-BE-E-01** (CAT-1): `ResourcesCount` schema with `@key(fields: "productId partnerId")`.
  2. **PRODUCT-BE-E-02** (CAT-2+CAT-3): Product stub resolver + aggregation facade (Option D Phase 1). Includes `@DgsEntityFetcher` boilerplate.
  3. **PRODUCT-BE-E-03** (CAT-2): `getProductTechPackBulkCountV1` bulk wrapper.
  4. **PRODUCT-BE-F-01 through F-08** (CAT-4): One placeholder per owning subgraph, each labeled `BLOCKED-BY: {domain} migration`. Full CAT-4 story goes in that domain's `be-04-stories.md`.
  5. **PRODUCT-BE-F-09** (CAT-4): Retire aggregation facade once all sub-stories complete.

**What you get:**
- All TechPack stories with full acceptance criteria and test cases.
- Phase E stories are self-contained (Product team can start immediately).
- Phase F placeholders give other teams a clear pickup point when their domain enters migration scope.
- Aggregation facade retirement story ensures the temporary solution has a defined end.

**Useful when:** A query returns an entity whose fields are spread across 5+ domain subgraphs — don't put all the logic in one story, break it per ownership boundary.

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Running Phase 4 without Phase 2 | Stories need pseudo-logic. Always run Phases 1+2 first. |
| Asking for a domain not in the catalog | Check catalog first: `What domains are in the service catalog?` |
| Expecting the DGS target repo to be scanned | It won't be — all output is green-field unless you explicitly provide DGS files |
| Running full product analysis in one shot | Break it up: run Phase 1, review, then Phase 2 (it's 2600 lines) |
| Not reading `be-04-po-summary.md` before sprint planning | The PO summary has sprint sequencing built in — don't skip it |
| Using quick-scope agent for story generation | Quick Scan doesn't produce complete pseudo-logic — run full Phase 2 before Phase 4 |
| Skipping the response footer check | Every phase produces a mandatory footer — use it to confirm what was analyzed |
| Treating `getProductTechPackCountV1` as a single story | It decomposes into 12+ sub-stories (schema + stub + facade + 8 per-subgraph CAT-4 + retirement). See `reference/federation-patterns.md` §9. |
| Putting sub-subgraph CAT-4 stories in the Product domain's file | Per-subgraph extension stories (F-01–F-08) belong in the OWNING domain's `be-04-stories.md`. Product's file holds stubs only. |
