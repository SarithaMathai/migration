# Migration Checklist — Pre and Post Migration Validation

**Purpose:** Structured checklist to validate that migration investigation is complete and that the DGS implementation is ready for cutover.
**Audience:** Tech leads and engineers validating migration readiness.

---

## Part 1: Investigation Completeness Checklist

Run this before handing investigation artifacts to the engineering team.

### Domain Investigation Complete?

- [ ] Domain is in the service catalog (`reference/domain-service-catalog.md` §2)
- [ ] All 6 artifacts exist in `output/{domain}/`:
  - [ ] `01-schema-inventory.md`
  - [ ] `02-resolver-analysis.md`
  - [ ] `03-schema.graphql`
  - [ ] `03-schema-analysis.md`
  - [ ] `04-stories.md`
  - [ ] `04-po-summary.md`
- [ ] All artifacts have the mandatory header block (domain, target DGS, pipeline version, date)
- [ ] All artifacts have the response footer

### Schema Inventory Complete?

- [ ] Every source file listed with path and line count
- [ ] Co-located domains identified
- [ ] Cross-domain references classified (Internal / EXT Service / Gateway Stitch)
- [ ] All utils mapped to DGS equivalents

### Resolver Analysis Complete?

- [ ] All queries documented (no gaps)
- [ ] All mutations documented (no gaps)
- [ ] Non-trivial field resolvers documented
- [ ] Every EXT service call has severity tag (🔴/🟡/🔵)
- [ ] Master EXT inventory table is present
- [ ] Complexity Assessment table covers all operations
- [ ] Key Findings section is complete

### Schema Derivation Complete?

- [ ] All types classified (no "unknown" entries)
- [ ] Federation @key directives defined for all owned types
- [ ] External stubs present for all gateway-only services
- [ ] Client contract verified (no breaking changes)
- [ ] Gap analysis summary line present: `{n} ✅ | {n} 🔜 | {n} ⏭`

### Story Generation Complete?

- [ ] Every operation has at least one story
- [ ] Every story uses the mandatory template (no missing sections)
- [ ] Acceptance criteria are objectively verifiable
- [ ] Dependency graph (Mermaid) is present
- [ ] Risk Register has entries for all High/Very-High stories
- [ ] PO summary has sprint sequencing and Decisions Required table
- [ ] **Composite key entity stubs checked:** For any operation returning a type classified with `@key(fields: "X Y")` composite key (e.g., `ResourcesCount`): (a) stub resolver story present in this domain's file; (b) one CAT-4 placeholder story per owning subgraph is present (BLOCKED-BY their migration); (c) aggregation facade story included for Option D Phase 1; (d) facade retirement story included. See `reference/federation-patterns.md` §9.

---

## Part 2: Pre-Implementation Checklist

Run this before engineers start building the DGS service.

### Architecture Decisions Made?

- [ ] Federation boundaries confirmed (which types are @key federated)
- [ ] Gateway stitching strategy confirmed (which services go through Hive)
- [ ] Co-located domain approach confirmed (same DGS service or separate?)
- [ ] Composite key patterns approved (e.g., `ResourcesCount @key(fields: "productId partnerId")`)
- [ ] **For composite key entities with multi-subgraph stubs:** TechPack migration option confirmed (B/C/D); owning domain teams identified for each stub field group; cross-domain CAT-4 story ownership assigned
- [ ] ACL token strategy confirmed (V1 `Authorization` header vs. V2 `SPARK-Capability-Token`)

### Blocking Dependencies Identified?

- [ ] All EXT Service dependencies cataloged
- [ ] For each 🔴 RED EXT service: Is the owning service already migrated to DGS?
  - If NO: CAT-4 story added, migration sequenced accordingly
- [ ] For each 🟡 YELLOW EXT service: Is it gateway-stitched or pending migration?
- [ ] Schema CAT-1 story approved by architect before CAT-2/CAT-3 stories start

### DGS Service Ready for Schema?

- [ ] Target DGS repo identified and accessible
- [ ] Schema file location confirmed: `{dgs-repo}/apps/app/src/main/resources/schema/{domain}.graphqls`
- [ ] Naming convention applied: `SPARK_` prefix dropped from owned types
- [ ] Federation configuration reviewed

---

## Part 3: Post-Implementation Validation Checklist

Run this before cutover from spark-internal-graphql to DGS.

### Schema Parity

- [ ] Every query in the source schema exists in the DGS schema
- [ ] Every mutation in the source schema exists in the DGS schema
- [ ] Argument names, types, and defaults match exactly
- [ ] Return type structure matches (nullability not loosened)
- [ ] Deprecated fields are preserved with `@deprecated(reason: "...")`

### Resolver Parity (Per Operation)

For each High/Very-High complexity operation, verify:

- [ ] REST endpoint matches source: `{HTTP verb} {URL pattern}`
- [ ] Request headers match: `Authorization` and/or `SPARK-Capability-Token`
- [ ] Request body transformation matches: snake_case field mapping
- [ ] Response transformation matches: camelCase field mapping
- [ ] Pagination defaults match: `page` and `size` default values
- [ ] Error handling matches: 404 → null? 500 → exception? specific error codes?
- [ ] DataLoader batching matches: same batch key, same max batch size

### EXT Service Integration

For each 🔴 RED EXT service:
- [ ] CAT-4 story implemented (federation entity fetcher or gateway config)
- [ ] Gateway type merging config deployed
- [ ] Entity fetcher tested with realistic data

For each 🟡 YELLOW EXT service:
- [ ] Stub return pattern implemented
- [ ] Gateway stitch or entity fetcher in place

For each 🔵 BLUE EXT service:
- [ ] Gateway stitch verified

### Test Coverage

- [ ] Unit tests cover happy path for every operation
- [ ] Unit tests cover documented error paths (from Phase 2 error handling)
- [ ] Integration tests verify end-to-end via DGS test client
- [ ] Parity tests pass for all High/Very-High complexity operations:
  - Same input → same output from both spark-internal-graphql and DGS

### Client Contract

- [ ] GraphQL operation names unchanged (no renames)
- [ ] All existing clients can query DGS without schema changes
- [ ] Deprecated fields still respond (even if returning stub values)

---

## Part 4: Cutover Readiness

| Criterion | Owner | Status |
|----------|-------|--------|
| All CAT-1 stories complete (schema deployed) | Tech Lead | |
| All CAT-2 stories complete (data fetchers deployed) | Backend Eng | |
| All CAT-3 stories complete (service layer deployed) | Backend Eng | |
| CAT-4 stories for 🔴 RED EXT services complete | Gateway Team | |
| CAT-5 parity tests passing | QA / Backend Eng | |
| Load testing complete | Platform | |
| Hive Gateway routing config updated | Gateway Team | |
| Rollback plan confirmed | Tech Lead | |
| PO sign-off on business acceptance criteria | PO | |

---

## EXT Service Migration Sequencing

When migrating a domain with 🔴 RED EXT dependencies on services not yet migrated to DGS:

1. **Do not block** — implement the domain with a gateway stitch for the unresolved EXT service
2. Create a CAT-4 story: "Replace gateway stitch with federation when {service} migrates to DGS"
3. Mark the CAT-4 story with a dependency on the EXT service's migration ticket
4. When the EXT service migrates, revisit and upgrade from gateway stitch to entity fetcher

This is the **Option D: Hybrid** approach — facade now, federate later.

---

## Risk Register Review

Before cutover, review the Risk Register in `04-stories.md` and confirm each risk is:

- [ ] **Mitigated** — the mitigation was implemented and verified
- [ ] **Accepted** — PO/Tech Lead consciously accepted the risk
- [ ] **Deferred** — deferred to a follow-on sprint with a ticket created

No risk should be "unreviewed" at cutover time.
