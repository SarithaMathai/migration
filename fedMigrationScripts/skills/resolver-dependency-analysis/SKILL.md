---
name: resolver-dependency-analysis
description: "Reads every source file identified in the schema inventory and produces plain-English pseudo-logic for every resolver, service method, and util. Tags every cross-domain HTTP call as EXT Service with severity 🔴/🟡/🔵. Rates every operation by complexity. Supports Full mode (complete pseudo-logic) and Quick Scan mode (top-level summary). Output: output/{domain}/02-resolver-analysis.md"
argument-hint: "Provide the domain whose schema inventory is complete. Example: 'Run resolver analysis for bom' or 'Quick scan of product domain'."
---

# Skill: Resolver Dependency Analysis

## Purpose

Read every resolver, service method, and utility function in a domain and produce plain-English pseudo-logic that engineers can implement from — without reading JavaScript.

This skill is the most detailed analysis in the pipeline. It tags every cross-domain HTTP call with severity, rates every operation by complexity, and identifies migration risks.

## When to Use

- Before creating migration stories (Phase 4 requires this output)
- When engineers need implementation specs without reading JavaScript
- When identifying EXT service call patterns for architecture decisions
- As a Quick Scan for fast complexity estimates

## Cannot Run Without

- `output/{domain}/01-schema-inventory.md` from `graphql-schema-inventory` skill
- Read access to resolver, service, and utils files listed in the manifest

## Reference Files to Read First

| For… | Read |
|------|------|
| Output conventions (header, status symbols, EXT severity, complexity/effort scale, response footer) | `reference/output-conventions.md` |
| Pseudo-logic block format — resolver/service/util templates, section ordering | `templates/resolver-analysis.md` |
| Utils inventory and DGS equivalent mapping | `reference/domain-service-catalog.md` §3 |

---

## Two Analysis Modes

### Full Mode (default)

Documents every query, mutation, field resolver, service method, and utility function. Produces a complete specification engineers can implement from. Takes 15–60 minutes depending on domain size.

Use full mode when:
- Building implementation specs for a team about to start coding
- Running Phase 4 story generation (requires complete pseudo-logic)
- Domains are actively being migrated

### Quick Scan Mode

Documents only top-level queries and mutations. No field resolvers, no utils detail. Produces a summary table with complexity ratings and EXT service counts. Takes 5–10 minutes.

Use Quick Scan when:
- Scoping a domain before committing to full analysis
- Producing a PO-level estimate without full stories
- Large domains where stakeholders want a preview first

> Specify at invocation: "Run resolver analysis for product — quick scan only" or "Full analysis for bom."

---

## Large File Protocol (Files > 1000 Lines)

For any resolver file exceeding 1000 lines (flagged in Phase 1 with ⚠️):

1. Read lines 1–500. Document all resolvers in this range.
2. Announce progress: "Chunk 1/5 complete — {n} query resolvers found. Reading lines 501–1000 next."
3. Read lines 501–1000. Continue documentation.
4. Repeat until fully read.
5. After all chunks, compile output in section order (not chunk order).

For files >2000 lines, offer to run in sections:
- Section A: Query resolvers
- Section B: Mutation resolvers
- Section C: Field resolvers
- Section D: Service + Utils

**Trivial resolver skip rule:** Field resolvers that only return `parent.{field}` (no service call, no branch, no transformation) are grouped in a table, not given individual pseudo-logic blocks.

---

## Step-by-Step Procedure

### Step 1: Read File Manifest from Phase 1

Open `output/{domain}/01-schema-inventory.md`. Note:
- All resolver, service, and util files to analyze
- Large file warnings (⚠️) that require chunked reading
- The import graph (which utils are needed)

### Step 2: Analyze Query Resolvers

For every query defined in the schema, find its resolver and document it using the block format from `templates/resolver-analysis.md`:

- Schema signature (copied from schema file)
- Resolver location: `{relative path}:{startLine}-{endLine}`
- Complexity rating (Low / Medium / High / Very High)
- Pseudo-logic (numbered steps, sub-bullets for branches)
- Service calls table (method, HTTP verb, endpoint, purpose)
- EXT Service calls (tagged with severity — never omit if present)
- Pagination details (source defaults, DGS target: Spring Pageable)
- Error handling (one line per error path — never collapse)
- Side effects (cache invalidation, activity log, Kafka, ACL refresh)
- User bifurcation (if resolver branches on `isExternal` — document BOTH paths)

### Step 3: Analyze Mutation Resolvers

Same format as queries, plus:
- Input validation rules (every rule, not just "validates input")
- Orchestration steps table (if mutation calls multiple services — can they parallelize?)
- Rollback / partial failure behavior (if any)

### Step 4: Analyze Field Resolvers

For every non-trivial field resolver:
- Parent type and field name
- Resolver location
- Trigger condition (when does this fire?)
- Pseudo-logic (numbered steps)
- Data source (Internal same-backend, or EXT Service)
- Caching / batching (DataLoader? Batch key? Max batch size?)

Group trivial pass-throughs at the end of this section:
```markdown
### Trivial Pass-Through Resolvers
| Resolver | Returns |
|---------|---------|
| {ParentType}.{field} | parent.{field} |
```

### Step 5: Analyze Service Classes

For each service file:
- Class name and base URL
- Every exported method: signature, HTTP verb, URL pattern, query params, request body shape
- Response shape and transformations (snake_case → camelCase, field renames, etc.)
- Error handling per method

### Step 6: Analyze Referenced Utils

For every util function referenced by this domain (from the import graph):
- Function signature and numbered steps
- DGS equivalent (from `reference/domain-service-catalog.md` §3)

Core utils (`loadOne`, `loadListing`, `postOne`, etc.) can use the standard DGS equivalent from the catalog rather than full re-analysis.

### Step 7: Build Helper Functions Section

If the resolver file defines local helper functions used by 2+ resolvers:
- Document them in a `## Helper Functions` section BEFORE the query/mutation sections
- Use the `H{n}` ID prefix

If a helper is used by only one resolver, document it inline in that resolver's pseudo-logic — do not create a Helper section.

### Step 8: Build EXT Service Call Inventory

Master table of every cross-domain HTTP call found in the domain:

```markdown
## EXT Service Call Inventory

| # | Called From | EXT Service | Loader Key | URL | Repo | HTTP | Endpoint | Severity | Purpose |
|---|-------------|-------------|------------|-----|------|------|----------|----------|---------|
```

Summary line: `{n} total — {n} 🔴 RED / {n} 🟡 YELLOW / {n} 🔵 BLUE`

### Step 9: Build Complexity Assessment

```markdown
## Complexity Assessment

| Operation | Type | Lines | Service Calls | EXT Calls | Orchestration Steps | Complexity |
|-----------|------|-------|---------------|-----------|---------------------|------------|
```

Complexity bump rules:
- +1 tier for polymorphic `__resolveType`
- +1 tier for internal/external user bifurcation
- +1 tier for parallel orchestration with 5+ services

### Step 10: Key Findings

```markdown
## Key Findings

### Highest Risk Operations
{Top 3–5 operations with Very High or High complexity}

### Migration Blockers
{Operations that cannot migrate until another service is ready}

### Refactor Recommendations
{Architecture debt found: resolvers doing business logic, N+1 patterns, shared utils spanning domains}

### Quick Wins
{Low complexity operations that can be shipped in Sprint 1}
```

---

## Quick Scan Output Format

When running in Quick Scan mode:

```markdown
# Quick Scan — {Domain}

> ⚡ Quick Scan Mode — top-level queries and mutations only.
> Field resolvers, utils, and service methods are not fully documented.
> Run full analysis before generating stories (Phase 4).

## Operation Summary

| Operation | Type | Complexity | EXT Calls | Lines | Notes |
|-----------|------|------------|-----------|-------|-------|

## EXT Service Summary

| EXT Service | Loader Key | # Calls | Max Severity | Called By |
|-------------|------------|---------|--------------|-----------|

## Effort Estimate (Rough Order of Magnitude)

| Complexity | Count | Day Range (each) | Total Range |
|-----------|-------|-----------------|-------------|
| Low       | {n}   | 1–2d             | {range}d    |
| Medium    | {n}   | 3–5d             | {range}d    |
| High      | {n}   | 5–8d             | {range}d    |
| Very High | {n}   | 8–13d            | {range}d    |
| **Total** | **{n}** | | **{range}d** (+20% buffer → **{range}d**) |

## Top 5 Risk Operations
{list with one-line risk description each}
```

---

## Output Format

Write to: `output/{domain}/02-resolver-analysis.md`

Section order (full mode — per `reference/output-conventions.md` §7):
1. Header block
2. Summary Statistics
3. Helper Functions (only if shared helpers exist — omit section if not)
4. Query Resolvers
5. Mutation Resolvers
6. Field Resolvers (omit section if zero; include trivial pass-throughs table at end if applicable)
7. Service Classes
8. Referenced Utils
9. EXT Service Call Inventory
10. Complexity Assessment
11. Key Findings

Follow `templates/resolver-analysis.md` for the exact block format of each resolver entry.

---

## Completion Criteria

Full mode:
- [ ] Every query resolver has a pseudo-logic block using the template format
- [ ] Every mutation resolver has a pseudo-logic block with input validation
- [ ] Every non-trivial field resolver is documented; trivial pass-throughs are in a grouped table
- [ ] Every service method is documented with REST endpoint details and transformation rules
- [ ] Every referenced util has a DGS equivalent noted
- [ ] Every EXT Service call is tagged with severity 🔴 / 🟡 / 🔵
- [ ] Master EXT inventory table contains every EXT call exactly once
- [ ] Complexity Assessment table is complete with bump rules applied
- [ ] Key Findings section covers: highest risk, migration blockers, refactor recommendations, quick wins
- [ ] No vague language ("various transformations", "standard error handling") in any pseudo-logic block
- [ ] Output written to `output/{domain}/02-resolver-analysis.md`
- [ ] Response footer included

## Next Skill

After completing this analysis, run `federation-schema-derivation` for Phase 3.
For federation boundary questions only, run `federation-candidate-detection` instead.
