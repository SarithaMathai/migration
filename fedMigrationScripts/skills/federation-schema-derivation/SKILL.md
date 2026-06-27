---
name: federation-schema-derivation
description: "Derives the target Netflix DGS GraphQL schema for a domain. Default mode is green-field (no existing DGS repo required). Uses federation-candidate-detection to classify types. Defines @key federation directives. Produces a gap analysis. Output: output/{domain}/03-schema.graphql + output/{domain}/03-schema-analysis.md"
argument-hint: "Provide the domain whose Phase 2 analysis is complete. Example: 'Derive the DGS schema for bom' or 'Run Phase 3 for measurement'."
---

# Skill: Federation Schema Derivation

## Purpose

Derive the complete target DGS GraphQL schema for a domain using the resolver analysis output. Classifies every type, defines federation directives, and produces a gap analysis.

This skill is the schema contract output — the `.graphqls` file engineers will build the DGS service from.

## When to Use

- After completing resolver analysis (Phase 2) to produce the DGS schema
- When an architect needs the schema contract to share with other teams
- When defining federation boundaries before implementation starts

## Cannot Run Without

- `output/{domain}/02-resolver-analysis.md` — pseudo-logic and EXT inventory drive type classification
- `spark-internal-graphql/packages/data-source-spark/src/schemas/SPARK_{Domain}.graphql` — source schema

## Reference Files to Read First

| For… | Read |
|------|------|
| Universal output conventions (header block, status symbols, response footer) | `reference/output-conventions.md` |
| Schema file body ordering, comment format, naming conventions | `reference/output-conventions.md` §8 |
| Federation type classification, @key rules, cross-domain decision tree | `reference/federation-patterns.md` |
| Output template for schema analysis document | `templates/federation-entity.md` |

Also invoke `federation-candidate-detection` skill to classify types before writing the schema.

---

## Green-Field Default

**No target DGS repo required.** This skill defaults to green-field mode:

- Skip reading existing DGS schema (Step 1 below)
- Mark all queries and mutations as 🔜 (needs migration)
- Schema status: "No existing DGS schema found — green-field derivation"

If the engineer provides DGS files directly (pasted into chat), use them for real gap analysis.

---

## Step-by-Step Procedure

### Step 1: DGS Schema Check (Green-Field Default)

**If no DGS repo available (default):**
Mark schema status in `03-schema-analysis.md` as:
> "No existing DGS schema found — green-field derivation. All types and operations marked 🔜."

Skip remainder of Step 1 and proceed to Step 2.

**If engineer has provided DGS files (exception):**
Read the provided `.graphqls` files. Note types, queries, and mutations already defined. Note commented-out fields (planned but not implemented → 🔜 in gap analysis). Use these as authoritative for naming and shape.

### Step 2: Invoke Federation Candidate Detection

Load `skills/federation-candidate-detection/SKILL.md` and run the full type classification procedure. This produces:
- Type classification for every type
- `@key` directive for every Owned type
- Strategy (Gateway Stitch / Direct / Federation / EXT pending) for every cross-domain reference

### Step 3: Preserve Client Contract

Every query, mutation, and type from the source schema must appear in the derived schema with:
- Same query/mutation name (no renames)
- Same argument names, types, and defaults
- Same return type structure (nullability can be tightened, not loosened)
- Deprecated fields kept with `@deprecated(reason: "...")`
- Enum values preserved (can add, cannot remove)

Note any breaking changes as CONFLICT in the gap analysis.

### Step 4: Apply Naming Conventions

| Convention | Rule |
|------------|------|
| Drop `SPARK_` prefix | `SPARK_Product` → `Product` for owned types |
| Keep external prefix | `VMM_Brand` stays `VMM_Brand` |
| File extension | `.graphqls` in DGS (not `.graphql`) |
| File location | `{dgs-repo}/apps/app/src/main/resources/schema/{domain}.graphqls` |

### Step 5: Write the Schema File

Schema body order (mandatory — per `reference/output-conventions.md` §8):
1. File header comment block
2. `extend schema @link(...)` federation header (if federation v2)
3. Scalar declarations
4. External type stubs — `# --- External stubs (Gateway-only) ---`
5. Owned entity types with `@key` — `# --- Owned types ---`
6. Embedded/nested types — `# --- Embedded types ---`
7. Shared types (`@shareable`) — `# --- Shared types ---`
8. Input types — `# --- Inputs ---`
9. Enum types — `# --- Enums ---`
10. `extend type Query { ... }` — `# --- Queries ---`
11. `extend type Mutation { ... }` — `# --- Mutations ---`

Every query, mutation, and field MUST have a `#` comment with status symbol and one-line description.

### Step 6: Write the Schema Analysis Document

The `03-schema-analysis.md` document must include all sections from `templates/federation-entity.md`:
1. Header block
2. Type Classification table (all types, one row per type)
3. External Type Stubs table (gateway-stitched types with stub pattern)
4. Client Contract Verification table (every query/mutation — breaking? yes/no)
5. Query Gap Analysis table with summary line: `{n} ✅ | {n} 🔜 | {n} ⏭ — {total} total`
6. Mutation Gap Analysis table with summary line
7. Schema Analysis Summary block (counts per type category)
8. Risks and Recommendations

For green-field: all Query/Mutation gap analysis rows are 🔜. Summary line: `0 ✅ | {n} 🔜 | {n} ⏭`.

---

## Output Format

Write TWO files:

### `output/{domain}/03-schema.graphql`
The actual DGS schema file. Use the mandatory comment header from `reference/output-conventions.md` §8.

### `output/{domain}/03-schema-analysis.md`
Full analysis document. Follow `templates/federation-entity.md` for all table structures.

---

## Completion Criteria

- [ ] DGS availability is explicitly marked (green-field or existing schema scan)
- [ ] Every type from the source schema is classified into exactly one of the 7 categories
- [ ] Federation `@key` directives are defined for all Owned entity types
- [ ] All cross-domain references resolved via the decision tree
- [ ] Client Contract Verification table covers every query and mutation
- [ ] Query Gap Analysis and Mutation Gap Analysis both present with summary lines
- [ ] Schema Analysis Summary block is complete
- [ ] Breaking change count is explicitly stated (0 for green-field)
- [ ] `output/{domain}/03-schema.graphql` written with correct body ordering
- [ ] `output/{domain}/03-schema-analysis.md` written with all required tables
- [ ] Response footer included

## Next Skill

After completing schema derivation, run `migration-story-generation` for Phase 4.
