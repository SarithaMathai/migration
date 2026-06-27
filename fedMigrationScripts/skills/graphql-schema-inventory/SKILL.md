---
name: graphql-schema-inventory
description: "Discovers, reads, and catalogs every source file related to a domain before analysis begins — schema, resolver, service, utils, config, and cross-domain references. Builds a complete file manifest, import dependency graph, and cross-domain reference table. Output: output/{domain}/01-schema-inventory.md"
argument-hint: "Provide the domain (loader key). Example: 'Run schema inventory for bom' or 'Inventory the measurement domain files'."
---

# Skill: GraphQL Schema Inventory

## Purpose

Discover and catalog every source file for a domain before any analysis begins. This is the entry point for every domain investigation — Phase 1 of the full pipeline.

Produces a structured manifest that tells the team:
- What files exist and how large they are
- What operations are defined in the schema
- Which utility files are used
- Which external services are called (cross-domain references)
- Whether any files are large enough to need chunked reading in Phase 2

## When to Use

- At the start of every domain investigation
- When briefing a team on what's in a domain
- When scoping a migration before committing to full analysis
- When identifying EXT service dependencies early

## Cannot Run Without

- Domain loader key (confirmed via `reference/domain-service-catalog.md`)
- Read access to `spark-internal-graphql/packages/data-source-spark/src/`

## Reference Files to Read First

| For… | Read |
|------|------|
| Domain lookup (loader key, source files, target DGS) | `reference/domain-service-catalog.md` §2 |
| Output conventions (header block, status symbols, response footer) | `reference/output-conventions.md` |
| Output format for this phase | `templates/migration-report.md` Phase 1 section |

---

## Step-by-Step Procedure

### Step 1: Look Up Domain in Catalog

From `reference/domain-service-catalog.md` §2, record:
- Loader key (e.g., `bom`)
- Service class (e.g., `BomService`)
- Schema file (e.g., `SPARK_Bom.graphql`)
- Resolver file (e.g., `product/SPARK_Bom.js`)
- Target DGS (e.g., `BomService` → `plm-product`)
- Backend URL and repo name

### Step 2: Read `context.js` Entry

Open `spark-internal-graphql/packages/data-source-spark/src/context.js`.

Find the entry for this loader key. Record the `url`, `repo`, and `service` values verbatim as a JS code block (not a paraphrase).

Also record every OTHER loader key that points to the same URL — these are co-located domains sharing the same backend.

### Step 3: Locate and Read Schema Files

Open `spark-internal-graphql/packages/data-source-spark/src/schemas/SPARK_{Domain}.graphql`.

Record:
- File path and line count
- Every `type`, `input`, `enum`, `interface`, `union` defined
- Every `Query` and `Mutation` field with its arguments and return type
- Cross-domain type references (types from other domains)

### Step 4: Locate and Read Resolver Files

Open the resolver file(s) from `spark-internal-graphql/packages/data-source-spark/src/resolvers/`.

Check for child resolver files in subdirectories (e.g., `resolvers/product/SPARK_Bom.js`).

Record:
- File path and line count
- Every resolver method (Query, Mutation, and field resolvers)
- All `import`/`require` statements

**Large file alert:** If any resolver file exceeds 1000 lines, note prominently:
`⚠️ Large file: {n} lines — Phase 2 will use chunked reading (500-line windows).`

### Step 5: Locate and Read Service Files

Open `spark-internal-graphql/packages/data-source-spark/src/services/{Domain}.js`.

Record:
- File path and line count
- Every exported method with its signature
- The base URL pattern used for REST calls

### Step 6: Locate Referenced Utils

From the resolver and service import statements, identify every utils file referenced.

For each util in `spark-internal-graphql/packages/data-source-spark/src/utils/`:
- Record file path and line count
- Record every exported function
- Classify as **Core util** (used by many domains) or **Domain-specific util**

Map each util to its DGS equivalent using `reference/domain-service-catalog.md` §3.

### Step 7: Locate Config Files

Check `spark-internal-graphql/packages/data-source-spark/src/config/` for config files referenced by this domain. Record constants, feature flags, and business partner config.

### Step 8: Target DGS Section (Green-Field Default)

Since the target DGS repo is not open in this workspace, write:

```markdown
## Target DGS: Green-Field

**Status:** No existing DGS schema found — green-field derivation.
**Target service:** `{ServiceClassName}` (repo: `{repo}`)
**Phase 3 approach:** All types and operations will be derived fresh and marked 🔜.

If you have DGS files to compare against, provide them when running Phase 3.
```

Exception: If the engineer has provided DGS files directly (pasted into chat), scan them and note what exists vs. what needs migration.

### Step 9: Build Cross-Domain Reference Table

From the schema and resolver analysis, identify every field referencing a type from another domain.

| Field | Referenced Type | Domain | Loader Key | URL | Strategy | Severity |
|-------|----------------|--------|------------|-----|----------|----------|

Classify each as:
- **Internal** — same backend, resolve in the DGS service directly
- **EXT Service** — different backend, requires federation/stitching design
- **Gateway Stitch** — external platform (VMM, IG, Doppler, etc.) — always Gateway, never DGS

### Step 10: Build Import Graph

Show which files import which utilities as a text dependency tree:

```
SPARK_{Domain}.js (resolver)
├── imports: {ServiceClassName} from services/{Domain}
├── imports: loadOne from utils/loadOne
├── imports: commonLoaders from utils/commonLoaders
└── imports: {util} from utils/{util}
```

### Step 11: Compile Summary Statistics

```markdown
## Summary Statistics

| Metric | Count |
|--------|-------|
| Schema files | {n} |
| Total schema lines | {n} |
| Types defined | {n} |
| Queries | {n} |
| Mutations | {n} |
| Resolver files | {n} |
| Total resolver lines | {n} |
| Service files | {n} |
| Total service lines | {n} |
| Utils files | {n} |
| Cross-domain references | {n} |
| EXT Service calls (estimated) | {n} |
| Large files (>1000 lines) | {n} ⚠️ |
```

---

## Output Format

Write to: `output/{domain}/01-schema-inventory.md`

Follow the Phase 1 section of `templates/migration-report.md` for exact section ordering and table structures.

Mandatory sections (in order):
1. Header block (per `reference/output-conventions.md` §2)
2. Context Registration (JS code block + co-located domains table)
3. Source File Manifest (5 tables: schema, resolver, service, utils, config)
4. Import Graph
5. Target DGS section (green-field marker by default)
6. Cross-Domain Reference table
7. Summary Statistics block

---

## Completion Criteria

- [ ] Every source file for the domain is identified and line-counted
- [ ] The `context.js` entry is recorded verbatim as a JS code block
- [ ] Co-located domains (same backend URL) are listed
- [ ] All resolver/service imports are traced in the Import Graph
- [ ] Cross-domain references are classified (Internal / EXT Service / Gateway Stitch) with provisional severity
- [ ] Target DGS section is present (green-field marker or existing-files scan)
- [ ] Summary Statistics block is complete
- [ ] Large file warnings are noted (⚠️)
- [ ] Output written to `output/{domain}/01-schema-inventory.md`
- [ ] Response footer included (per `reference/output-conventions.md` §10)

## Next Skill

After completing this inventory, run `resolver-dependency-analysis` for Phase 2.
