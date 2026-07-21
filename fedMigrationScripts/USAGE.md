# Migration Investigation Framework — Detailed Usage Guide

> **Who this is for:** Engineers, tech leads, and architects investigating spark-internal-graphql domains for DGS migration.
> **Assumes:** You've read [ONBOARDING.md](./ONBOARDING.md) and confirmed your workspace setup.

---

## Table of Contents

1. [What This Framework Does](#1-what-this-framework-does)
2. [The Investigation Pipeline](#2-the-investigation-pipeline)
3. [Skills Reference](#3-skills-reference)
4. [Agents Reference](#4-agents-reference)
5. [Running Investigations](#5-running-investigations)
6. [Understanding Each Output Artifact](#6-understanding-each-output-artifact)
7. [Effort and Complexity Reference](#7-effort-and-complexity-reference)
8. [EXT Service Severity Reference](#8-ext-service-severity-reference)
9. [Working With Large Domains](#9-working-with-large-domains)
10. [Domain-Specific Guidance](#10-domain-specific-guidance)
11. [Troubleshooting](#11-troubleshooting)
12. [Framework Design Decisions](#12-framework-design-decisions)

---

## 1. What This Framework Does

You name a domain (e.g., `bom`, `product`, `measurement`). The framework reads the spark-internal-graphql source code — schemas, resolvers, service files, and utilities — and produces migration-ready artifacts for the target DGS service.

**What you get:**

| Artifact | File | Audience |
|---------|------|---------|
| Schema inventory | `be-01-schema-inventory.md` | Tech Lead |
| Resolver pseudo-logic | `be-02-resolver-analysis.md` | Backend Engineers |
| Target DGS schema | `be-03-schema.graphql` | Architects |
| Schema gap analysis | `be-03-schema-analysis.md` | Architects |
| Engineering stories | `be-04-stories.md` | Engineering Team |
| PO sprint plan | `be-04-po-summary.md` | Product Owner |

**What you do NOT need:**
- The target DGS repository (e.g., `plm-product`, `plm-bom`)
- Any running services or databases
- Any environment variables
- Any target microservice source code

All output is derived from `spark-internal-graphql` source alone. DGS schemas are derived green-field (all operations marked 🔜 needs migration).

---

## 2. The Investigation Pipeline

The pipeline has four sequential phases. Each builds on the previous.

```
Phase 0         Phase 1              Phase 2              Phase 3           Phase 4
Workspace   →   Schema           →   Resolver         →   Federation    →   Migration
Setup           Inventory            Analysis             Schema            Stories
(~1 min)        (~3–5 min)           (~15–60 min)         Derivation        (~10 min)
                                                          (~5 min)

No output.      01-schema-           02-resolver-          03-schema.        be-04-stories.md
Confirms        inventory.md         analysis.md           graphql           be-04-po-summary.md
paths and                                                  03-schema-
loader key.                                                analysis.md
```

### Phase 0 — Workspace Setup (automatic)

Confirms the domain name maps to a valid loader key, locates the source files, checks for existing output, flags any large files that will need chunked reading. This phase runs automatically before Phase 1 — you do not need to invoke it separately.

**Output:** Chat confirmation only. No file written.

### Phase 1 — Schema Inventory

Reads `context.js`, schema files, resolver files, service files, and all referenced utility files. Produces a complete manifest with file paths, line counts, cross-domain references, import dependency graph, and co-located domain siblings.

**Skills used:** `graphql-schema-inventory`
**Output:** `be-01-schema-inventory.md`
**Time:** ~3–5 minutes

**Use when:**
- Scoping a migration before committing to full analysis
- Briefing the team on what's in a domain
- Identifying EXT service dependencies early

### Phase 2 — Resolver Analysis

Reads every resolver, service method, and utility function and produces plain-English pseudo-logic that engineers can implement from — without reading JavaScript. Tags every cross-domain HTTP call with severity (🔴 RED / 🟡 YELLOW / 🔵 BLUE). Rates every operation by complexity.

**Skills used:** `resolver-dependency-analysis`
**Output:** `be-02-resolver-analysis.md`
**Time:** ~15 min (small domain) to ~60 min (product domain, 2600+ lines)

**Two modes:**
- **Full mode** (default): Complete pseudo-logic for every operation. Required before stories.
- **Quick Scan mode**: Top-level operations only, summary complexity table, rough effort estimate. Takes 5–10 min.

**Use when:**
- Building implementation specs for engineers
- Identifying migration complexity before sprint planning
- Finding EXT service call patterns for architecture decisions

### Phase 3 — Federation Schema Derivation

Derives the target DGS GraphQL schema. Classifies every type (Owned / Extended / External stub / Gateway-only / Shared / Input / Enum). Defines `@key` federation directives for owned entities. Produces a gap analysis.

**Skills used:** `federation-schema-derivation`, `federation-candidate-detection`
**Output:** `be-03-schema.graphql` + `be-03-schema-analysis.md`
**Time:** ~5 minutes

**Green-field mode** (default): No existing DGS repo needed. All types and operations marked 🔜. If you later provide DGS files, Phase 3 can be re-run with the existing schema for a real gap analysis.

**Use when:**
- Sharing schema contracts with the architecture team
- Defining federation entity boundaries
- Planning the DGS service structure

### Phase 4 — Migration Story Generation

Breaks the migration into Jira-ready stories grouped by functional phase (A–Z). Each story embeds the Phase 2 pseudo-logic as the implementation spec, along with acceptance criteria, files to create, test cases, and dependency chain. Also produces a PO-facing sprint planning summary.

**Skills used:** `migration-story-generation`, `stitching-pattern-analysis`
**Output:** `be-04-stories.md` + `be-04-po-summary.md`
**Time:** ~10 minutes

**Cannot run without:** Phases 1, 2, and 3 complete. Stories embed pseudo-logic from Phase 2. Schema is referenced from Phase 3.

**Story categories:**
- **CAT-1**: Schema migration (`.graphqls` files in DGS)
- **CAT-2**: Resolver / data fetcher (`@DgsQuery`, `@DgsMutation`, `@DgsData`)
- **CAT-3**: Service logic (Kotlin service, Feign clients, DTOs)
- **CAT-4**: Federation / stitching (Hive Gateway config, entity fetchers)
- **CAT-5**: Test coverage (unit, integration, parity tests)

---

## 3. Skills Reference

Skills are focused, single-capability tools. They can be composed by agents or invoked independently.

| Skill | Purpose | Standalone? |
|-------|---------|------------|
| `graphql-schema-inventory` | Locate and catalog all domain source files, build cross-domain reference table | Yes |
| `resolver-dependency-analysis` | Document resolver logic, service calls, EXT dependencies, complexity | Yes |
| `federation-schema-derivation` | Derive DGS schema, classify types, define @key directives | Yes (needs Phase 2 output) |
| `federation-candidate-detection` | Identify entity boundaries and @key candidates from resolver patterns | Yes |
| `stitching-pattern-analysis` | Determine federation vs. gateway stitch vs. direct resolution strategy | Yes — for architecture Q&A |
| `migration-story-generation` | Convert analysis into Jira-ready stories with acceptance criteria | Yes (needs Phases 1–3 output) |

To invoke a skill directly:
> "Use the resolver-dependency-analysis skill for the {domain} domain"
> "What federation strategy should I use for Product.bom? Use the stitching-pattern-analysis skill."

---

## 4. Agents Reference

Agents orchestrate multiple skills toward an investigation goal.

### `full-migration-investigation` (primary agent)

**Use when:** You want all 6 artifacts for a domain.
**Skills used:** All 5 analysis skills + migration-story-generation
**Prompt:** `Analyze the {domain} domain for DGS migration — run all phases.`

### `schema-ownership`

**Use when:** You want to understand what a domain owns vs. references vs. stitches.
**Skills used:** `graphql-schema-inventory` + `federation-candidate-detection`
**Time:** ~10 minutes
**Prompt:** `Analyze schema ownership for the {domain} domain.`

### `federation-readiness`

**Use when:** An architect needs to assess federation boundaries without full analysis.
**Skills used:** `federation-candidate-detection` + `stitching-pattern-analysis`
**Time:** ~10 minutes
**Prompt:** `Assess federation readiness for the {domain} domain.`

### `quick-scope`

**Use when:** A tech lead or PO needs a rough complexity estimate before committing to full analysis.
**Skills used:** `graphql-schema-inventory` + `resolver-dependency-analysis` (quick scan mode)
**Time:** ~5 minutes
**Prompt:** `Give me a quick scan of the {domain} domain — top operations only.`

---

## 5. Running Investigations

### Full Pipeline — All 4 Phases

```
Analyze the bom domain for DGS migration — run all phases.
```

Produces all 6 artifacts in `output/bom/`. Takes 15–60 minutes depending on domain size.

---

### Phased Approach — Review Between Phases

```
Run the schema inventory for the bom domain.
```
Review `output/bom/be-01-schema-inventory.md` with the team.

```
Run the resolver analysis for bom — Phase 1 is already done.
```
Review `output/bom/be-02-resolver-analysis.md`. Discuss complexity and EXT dependencies.

```
Derive the DGS schema for bom — Phases 1 and 2 are done.
```
Review `output/bom/be-03-schema.graphql` and `be-03-schema-analysis.md` with architects.

```
Generate migration stories for bom — Phases 1, 2, and 3 are done.
```
Produces `be-04-stories.md` and `be-04-po-summary.md`.

---

### Targeted Investigations

**Quick scope estimate:**
```
Give me a quick scan of the product domain — top-level operations only, skip field resolvers.
```

**Federation boundaries only:**
```
Assess federation readiness for the attachment domain.
```

**Explain a specific operation:**
```
Explain what getTechPackResourceCountMap does in SPARK_Product.js. What services does it call?
```

**Find EXT service dependencies:**
```
What external services does the product domain call? Show all EXT calls with severity.
```

**Stories from existing analysis:**
```
Generate migration stories for the bom domain — analysis is already in output/bom/.
```

**PO sprint plan for a completed domain:**
```
The BOM analysis is complete — all 6 output files are in output/bom/. Give me a sprint sequencing plan for a team of 3 engineers.
```

**Audit existing output:**
```
Audit output/product/be-04-stories.md — check it against the story format and report any gaps.
```

---

## 6. Understanding Each Output Artifact

### `be-01-schema-inventory.md` — Schema Inventory

The entry point for every domain investigation. Contains:

- **Context registration** — the `context.js` entry for this domain (loader key, URL, repo, auth pattern)
- **Co-located domains** — other domains sharing the same backend URL
- **Source file manifest** — every schema, resolver, service, utils, and config file with path and line count
- **Import dependency graph** — which files import which utilities
- **Cross-domain reference table** — every field that references a type from another domain, classified as Internal / EXT Service / Gateway Stitch
- **Summary statistics** — total lines, operation counts, EXT service call estimates

**Use it to:**
- Scope the migration
- Identify hidden EXT dependencies before starting
- Brief the team on what's in the domain
- Plan chunked reading for Phase 2

---

### `be-02-resolver-analysis.md` — Resolver Dependency Analysis

The most detailed artifact. Contains:

- **Helper functions** — shared logic used by multiple resolvers
- **Query resolvers** — step-numbered pseudo-logic for every query, with REST endpoint details, error handling, and EXT service calls
- **Mutation resolvers** — same, plus input validation rules, orchestration steps, and rollback behavior
- **Field resolvers** — non-trivial field resolvers documented individually; trivial pass-throughs grouped in a table
- **Service classes** — every service method with HTTP verb, URL pattern, request/response shape
- **Referenced utils** — every utility function with its DGS equivalent
- **EXT service call inventory** — master table of every cross-domain HTTP call with severity
- **Complexity assessment** — every operation rated Low / Medium / High / Very High
- **Key findings** — highest risk operations, migration blockers, refactor recommendations, quick wins

**Use it to:**
- Implement the DGS service without reading JavaScript
- Write acceptance criteria for stories
- Estimate effort per operation
- Identify federation design decisions

---

### `be-03-schema.graphql` — DGS Target Schema

The actual GraphQL schema file ready to drop into the DGS service's `resources/schema/` folder.

- Section-ordered: External stubs → Owned types → Embedded types → Shared → Inputs → Enums → Queries → Mutations
- Every type classified and annotated
- Every operation marked with status symbol (🔜 for green-field)
- `@key` federation directives on all owned entity types
- External platform stubs (VMM, IG, Doppler, etc.) marked as gateway-only

**Use it to:**
- Start building the DGS service schema
- Define federation contracts with other teams
- Set up Hive Gateway type merging configuration

---

### `be-03-schema-analysis.md` — Schema Gap Analysis

Analytical companion to the schema file. Contains:

- **Type Classification table** — every type with its category (Owned/Extended/External stub/etc.)
- **External Type Stubs table** — gateway-stitched types with their stub pattern
- **Client Contract Verification** — every query and mutation confirmed preserved
- **Query Gap Analysis** — status (✅ exists / 🔜 needs migration / ⏭ deferred) per operation
- **Mutation Gap Analysis** — same
- **Risks and Recommendations**

Gap analysis summary line format: `{n} ✅ | {n} 🔜 | {n} ⏭ — {total} total`
For green-field migrations: always `0 ✅ | {n} 🔜 | {n} ⏭`

---

### `be-04-stories.md` — Engineering Migration Stories

Jira-ready stories grouped by functional phase. Each story contains:

- Story ID (`SPARK-{DOMAIN}-{PHASE}{SEQ}`)
- User story format with specific, actionable goal
- Current behavior (embedded Phase 2 pseudo-logic)
- EXT service calls with severity
- Target DGS implementation spec
- Files to create or modify
- Dependencies (what must ship first)
- Acceptance criteria (objectively verifiable — no vague language)
- Test cases (unit, integration, parity)

Functional phases: **A** (Schema) → **B** (Core Reads) → **C** (Mutations) → **D** (Search/Listing) → **E** (Complex Operations) → **F** (Federation/Stitching) → **G** (Tests/Parity)

**Use it to:**
- Create Jira tickets directly from each story
- Assign work to engineers
- Build sprint plans

---

### `be-04-po-summary.md` — PO Sprint Planning Summary

Plain-English, no pseudo-logic. Contains:

- **What Are We Building?** — 2–3 paragraph overview for stakeholders
- **Migration Scope** — operation counts table
- **Story Summary by Phase** — effort ranges per phase with +20% buffer
- **Key Risk Areas** — risk table without technical detail
- **Decisions Required** — items blocking phase kickoff, with due-before dates
- **Dependency Map** — text-format dependency tree
- **Recommended Sprint Sequencing** — sprint-by-sprint table
- **Capacity Planning** — adjusted estimates for 1, 2, or 3-engineer teams

---

## 7. Effort and Complexity Reference

| Complexity | Effort Label | Day Range | Typical Operation |
|-----------|-------------|----------|------------------|
| Low | Small | 1–2 days | Single REST call, no EXT dependencies, < 20 lines of logic |
| Medium | Medium | 3–5 days | 2–3 service calls, 1 EXT call, some transformation |
| High | Large | 5–8 days | 4+ service calls, multi-step orchestration |
| Very High | X-Large | 8–13 days | Cross-domain aggregation, 8+ EXT calls, polymorphic resolution |

**Complexity bumps (apply as appropriate):**
- +1 tier for polymorphic `__resolveType` (e.g., BOM's 7 material variants)
- +1 tier for internal/external user bifurcation (`context.user.isExternal`)

**Buffer:** All domain-level totals include a +20% buffer for integration testing and parity verification.

---

## 8. EXT Service Severity Reference

Every cross-domain HTTP call is tagged with a severity wherever it appears in artifacts:

```
EXT Service → key: `{loaderKey}` · url: `{url}` · repo: `{repo}` · severity: 🔴/🟡/🔵
Purpose: {one-line description}
```

| Severity | Criteria | Migration Treatment |
|---------|---------|-------------------|
| 🔴 RED | Critical to business logic; sequential calls; data merged from multiple services | Full CAT-4 federation/stitching design required |
| 🟡 YELLOW | Important enrichment; single EXT call; partial response acceptable | Standard CAT-4 stub story |
| 🔵 BLUE | Optional enrichment; gateway can resolve | Pure gateway stitch; minimal CAT-4 effort |

**External Platform Services** (always 🔵, never migrated to DGS — always Hive Gateway stitch):
VMM, Item Groups (IG), Doppler, LDAP, APEX, Corona, Nexus, Assortment, Negotiator, Brand Compliance

---

## 9. Working With Large Domains

### Large File Protocol (>1000 lines)

When a resolver file exceeds 1000 lines (e.g., `SPARK_Product.js` at 2,629 lines):

1. The agent reads in **500-line windows** — never the whole file at once
2. Progress is announced: "Chunk 1/5 complete — 18 queries found. Reading lines 501–1000 next."
3. For files >2000 lines, Phase 2 can be run in sections:
   - Section A: Query resolvers
   - Section B: Mutation resolvers
   - Section C: Field resolvers
   - Section D: Service + Utils
4. Output is written progressively — each section appended to the output file as it completes

### When to Use Quick Scan Instead

For very large domains (product), consider Quick Scan mode for Phase 2:

```
Give me a quick scan of the product domain — top-level operations only, no field resolvers.
```

Quick Scan produces:
- Summary table (operation, type, complexity, EXT calls, lines)
- Rough effort estimate by complexity tier
- Top-5 risk operations
- EXT service dependency summary

Use it to get a PO-level estimate in 5 minutes. **Run full analysis before generating stories** — stories require complete pseudo-logic.

### Trivial Field Resolver Grouping

Large domains often have 50–60+ field resolvers. Simple pass-throughs (returns `parent.fieldName` directly) are grouped in a table rather than getting individual pseudo-logic blocks:

```markdown
### Trivial Pass-Through Resolvers
| Resolver | Returns |
|---------|---------|
| Product.status | parent.status |
| Product.type | parent.type |
```

Non-trivial field resolvers (any service call, conditional branch, or transformation) always get full pseudo-logic.

---

## 10. Domain-Specific Guidance

### BOM Domain

The BOM domain uses a polymorphic `BomMaterial` interface with 7 concrete variants resolved via `__resolveType`. Phase 2 documents all 7 variants. Phase 4 generates separate test cases per variant. Budget for Very High complexity.

Also note: BOM has internal vs. external user bifurcation — resolvers branch on `context.user.isExternal`. Both code paths are documented explicitly.

### Product Domain

The largest domain: 2,629-line resolver, 18 queries, 23 mutations, 60+ field resolvers.

- Run phases individually and review between each
- Phase 2 alone takes ~45–60 minutes
- `getTechPackResourceCountMap` is the most complex operation — see `reference/stitching-patterns.md` and `techpack-migration-options.md` for migration options before Phase 4

### Co-Located Domains

Several domains share the `spark-product` backend: `product`, `bom`, `measurement`, `impression`, `packaging`, `productPlan`, `productVariation`, and others. They share the target DGS service (`plm-product`) but are analyzed independently. Phase 1 lists all co-located siblings.

When analyzing co-located domains, note:
- They share the same Feign client base URL
- Federation stories (CAT-4) may be shared across siblings
- Schema files go into the same DGS `resources/schema/` directory

### TechPack Analysis (`getProductTechPackCountV1`)

This is the most complex operation in the system — 17 orchestration steps calling 9+ services in parallel. Before running Phase 4, read:
- `reference/stitching-patterns.md` for the composite key federation pattern
- `techpack-migration-options.md` for migration option comparison (Options B, C, D)

Recommended migration approach: **Option D — Hybrid** (temporary aggregation facade now, federate later).

---

## 11. Troubleshooting

### "Domain not found in catalog"
```
What domains are in the service catalog?
```
Lists all 37+ loader keys. If yours is missing:
```
Add {loaderKey} to the catalog with URL {url} and target DGS {ServiceName}
```

### "Analysis is taking too long on a large domain"
Switch to Quick Scan for Phase 2:
```
Give me a quick scan of {domain} — top-level operations only, skip field resolvers and utils.
```

### "I only have partial output files"
Tell the agent which phases are done:
```
Run Phase 3 for bom — Phases 1 and 2 outputs are in output/bom/.
```

### "Output folder doesn't exist"
The agent creates it during Phase 0 workspace setup. Or create it manually:
```
mkdir -p output/{domain}
```

### "I need just one resolver explained"
You don't need the full pipeline:
```
Explain what getProducts does in SPARK_Product.js — what does it call and how does it work?
```

### "Phase 4 stories are vague or missing implementation detail"
This means Phase 2 ran in Quick Scan mode. Re-run Phase 2 in full mode before generating stories:
```
Run the resolver analysis for {domain} in full mode — write complete pseudo-logic.
Then run Phase 4.
```

### "I need to re-run a phase with new information"
Just tell the agent:
```
Re-run Phase 3 for bom — I have DGS schema files to provide. [paste or reference the .graphqls file]
```

---

## 12. Framework Design Decisions

These decisions were made deliberately and explain why the framework is structured this way.

**No target DGS repo required.** The most common blocker for engineers starting migration investigations was needing access to the target DGS repo. By defaulting to green-field mode (all output marked 🔜), the framework unblocks all 37+ domains.

**Skills named by capability, not phase number.** `resolver-dependency-analysis` is discoverable; `02-code-analysis` is not. Engineers who need to "check federation boundaries" can now find the right skill without reading documentation.

**Three agents for different investigation depths.** A tech lead scoping a domain doesn't need full stories. An architect assessing federation boundaries doesn't need a sprint plan. The `quick-scope`, `schema-ownership`, and `federation-readiness` agents let engineers get answers in 5–10 minutes instead of 60.

**Templates separated from instructions.** Output format specifications (what the artifacts look like) are in `templates/`. Operational guidance (how to run investigations) is in `instructions/`. Reference data (the domain catalog) is in `reference/`. Each concern has one home.

**Deterministic section ordering.** Every Phase 2 output follows the same section order. Every Phase 4 story uses the same template. This makes artifact review and audit predictable — reviewers know exactly where to look.

**+20% buffer built in.** All effort totals include an automatic 20% buffer. This was calibrated against actual Product and BOM domain analysis. It accounts for integration testing and parity verification that are always underestimated.
