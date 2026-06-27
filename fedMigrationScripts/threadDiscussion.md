# Thread Discussion — Framework Design Rationale

This document captures the design discussion that produced the `fedMigrationScripts/` structure.
It serves as a record of what was evaluated, what was changed, and why.

---

## The Initial Request

An engineer presented a request to build a **reusable engineering investigation framework** for migrating from a legacy Spark GraphQL edge layer to a Federated GraphQL architecture hosted in Hive.

**The goal was explicitly NOT to implement production code.**

The goal was to create:
- Reusable investigation skills
- Reusable investigation agents
- Reusable instructions and playbooks
- Migration analysis artifacts
- Onboarding guidance for engineers

### Key Constraints Given

- Engineers use VS Code with GitHub Copilot extension (do NOT assume Claude subscription)
- No running services are required
- No databases are required
- No environment variables are required
- Do NOT require target DGS microservice repositories
- Focus only on GraphQL schema / data stitching / migration investigation

### Migration Context

**Current State:**
- `spark-internal-graphql` acts as an edge GraphQL aggregation layer
- Contains custom stitching and business aggregation logic
- Schemas and resolvers perform orchestration
- Joins happen through custom Node.js code

**Target State:**
- Federated GraphQL architecture (Netflix DGS + Hive Gateway)
- Ownership moves closer to domain services
- Federation stitches data by entity IDs
- Reduce/remove custom edge orchestration code
- Leverage GraphQL federation entity references where possible

### Preferred Repository Organization Proposed by Engineer

```
/skills      ← graphql-schema-analysis, federation-candidate-detection,
               resolver-dependency-analysis, entity-boundary-analysis,
               stitching-pattern-analysis

/agents      ← migration-investigation-agent, schema-ownership-agent,
               federation-readiness-agent

/instructions ← onboarding.md, investigation-workflow.md,
                migration-checklist.md, evidence-collection.md

/templates   ← migration-report-template.md, federation-entity-template.md,
               resolver-analysis-template.md
```

---

## Repository State Before This Redesign

The existing repository (`revised/` folder) contained:

### What Was Good

- A detailed, deterministic 4-phase analysis pipeline that produced 6 artifacts per domain
- A comprehensive domain service catalog (37+ services accurately mapped)
- An EXT service severity scale (🔴/🟡/🔵) that made cross-domain dependencies visible
- A green-field default — no target DGS repo required
- Real sample output for the Product domain
- A well-written EXAMPLES.md with copy-paste invocations

### What Was Problematic

**1. `revised/` was a subdirectory, not the root**
The original version and the v1.1 revision coexisted. Engineers were unclear which was canonical.

**2. Skills were named as pipeline phases, not capabilities**
`01-file-inventory`, `02-code-analysis`, `03-schema-derivation`, `04-story-breakdown`

Phase numbers encode execution order, not capability. An engineer wanting to "check federation boundaries" couldn't find the right skill without reading everything.

**3. One monolithic agent**
A single `spark-migration.agent.md` handled all phases. Engineers doing targeted investigations (just federation boundaries, just schema ownership) had no focused entry point. This forced everyone through a 60-minute pipeline even when they needed a 5-minute estimate.

**4. No templates folder**
Output format specifications were buried inside instruction files (`file-inventory-format.instructions.md`, `pseudo-logic-format.instructions.md`, etc.). There was no standalone templates directory. Skills and instructions contained duplicated format definitions.

**5. Instructions mixed two concerns**
`instructions/` contained both:
- **Format specifications** (what artifacts look like) — these are templates, not instructions
- **Reference data** (the domain service catalog) — this is reference, not an instruction

True human operational guidance (how to run an investigation) was mixed in with machine-readable format specs.

**6. Phase 0 was incorrectly a skill**
`00-domain-context/SKILL.md` was workspace validation — it had no analysis output, produced "chat confirmation only," and ran automatically. This is setup guidance, not a reusable analysis capability.

**7. Domain catalog was split across two files**
`domain-service-catalog.instructions.md` and `domain-service-catalog.addendum.md` both existed. Single source of truth was broken.

**8. Skills had embedded output format specs**
Each skill described the format of its output inline. When the format changed, multiple files needed updating. Formats should live in templates; skills should reference them.

---

## Design Decisions Made

### Decision 1: Flatten the structure — promote `revised/` to root, archive original

**Rationale:** Engineers should not have to guess which version is current. The `revised/` improvements were v1.1 — they become the canonical root.

### Decision 2: Rename skills by capability, not phase number

| Old Name | New Name | Why |
|----------|---------|-----|
| `01-file-inventory` | `graphql-schema-inventory` | Describes what it does, not when it runs |
| `02-code-analysis` | `resolver-dependency-analysis` | Precise: it analyzes resolver dependencies |
| `03-schema-derivation` | `federation-schema-derivation` | Clarifies the federation context |
| `04-story-breakdown` | `migration-story-generation` | Verb-noun capability name |
| `federation-stitching` | `stitching-pattern-analysis` | Consistent naming convention |

### Decision 3: Add a new `federation-candidate-detection` skill

The original `03-schema-derivation` did two things:
1. Identify entity boundaries and @key candidates
2. Write the DGS schema file

These are different questions. An architect asking "what should be federated?" doesn't need a schema file. Splitting them creates a skill that the `federation-readiness` agent can use without running the full schema derivation.

### Decision 4: Replace one monolithic agent with four focused agents

| New Agent | Replaces | Rationale |
|----------|---------|-----------|
| `full-migration-investigation` | spark-migration.agent.md | Behavior identical, name clarified |
| `schema-ownership` | (new) | Tech leads need type ownership answers in ~10 min |
| `federation-readiness` | (new) | Architects need boundary decisions in ~10 min |
| `quick-scope` | Quick scan mode buried in Phase 2 | Makes it a first-class entry point |

### Decision 5: Create `templates/` folder — move format specs out of instructions

All output format specifications were extracted from instruction files and placed in standalone template files:

| From (instructions) | To (templates) |
|--------------------|----------------|
| `file-inventory-format.instructions.md` | `templates/migration-report.md` |
| `pseudo-logic-format.instructions.md` | `templates/resolver-analysis.md` |
| `dgs-schema-conventions.instructions.md` | `templates/federation-entity.md` |
| `story-format.instructions.md` | `templates/story-format.md` |

### Decision 6: Create `reference/` folder — move stable lookup data

Domain-specific lookup data that agents and skills need to function:

| From (instructions) | To (reference) |
|--------------------|---------------|
| `domain-service-catalog.instructions.md` + `.addendum.md` | `reference/domain-service-catalog.md` (merged) |
| `output-conventions.instructions.md` | `reference/output-conventions.md` |
| (scattered in agent and skills) | `reference/federation-patterns.md` |
| (scattered in agent and skills) | `reference/stitching-patterns.md` |

### Decision 7: Convert `instructions/` to pure human operational guidance

After extracting templates and reference data, `instructions/` becomes four genuine playbooks:

- `onboarding.md` — workspace setup steps (absorbs Phase 0 skill content)
- `investigation-workflow.md` — decision tree for which agent/skill to run
- `evidence-collection.md` — what artifacts to capture and how
- `migration-checklist.md` — pre/post migration validation

### Decision 8: Remove `00-domain-context` as a skill

Phase 0 workspace validation steps were moved into `instructions/onboarding.md`. It is not a reusable analysis capability — it is setup guidance that happens to be automatable.

### Decision 9: Merge `USAGE.md`, `EXAMPLES.md`, `README.md` into clear separation

- `README.md` — one-page overview, structure map, links
- `ONBOARDING.md` — 5-step start guide with copy-paste prompts (replaces USAGE.md intro)
- `USAGE.md` — detailed usage reference for all scenarios
- `examples/EXAMPLES.md` — copy-paste invocation examples (moved to `examples/` folder)
- `agentsMakeGuide.md` — new: how to create and extend skills/agents/instructions/templates

---

## What Was Preserved Unchanged

The following were kept exactly as-is because they were correct:

- The 4-phase pipeline logic and sequencing
- The EXT service severity scale (🔴/🟡/🔵)
- The green-field default behavior
- The chunked reading protocol for large files (500-line windows)
- The domain service catalog content (37+ services)
- The effort/complexity scale (Low/Medium/High/Very High → 1–2d/3–5d/5–8d/8–13d)
- The +20% buffer on all domain totals
- The mandatory response footer after each phase
- The story template (20+ fields, objectively verifiable acceptance criteria)
- The PO summary structure (decisions required, sprint sequencing, capacity planning)
- The Quick Scan mode for Phase 2
- The sample output for the Product domain

---

## Final Structure Summary

```
fedMigrationScripts/
├── README.md                          ← What this is, full structure map
├── ONBOARDING.md                      ← 5-step start guide
├── USAGE.md                           ← Detailed usage for all scenarios
├── agentsMakeGuide.md                 ← How to build skills/agents/instructions/templates
├── threadDiscussion.md                ← This file: design rationale
│
├── skills/
│   ├── graphql-schema-inventory/
│   ├── resolver-dependency-analysis/
│   ├── federation-schema-derivation/
│   ├── federation-candidate-detection/   ← NEW: split from schema-derivation
│   ├── stitching-pattern-analysis/
│   └── migration-story-generation/
│
├── agents/
│   ├── full-migration-investigation.agent.md
│   ├── federation-readiness.agent.md      ← NEW
│   ├── schema-ownership.agent.md          ← NEW
│   └── quick-scope.agent.md               ← NEW (was buried as Quick Scan mode)
│
├── instructions/                          ← Human operational guidance only
│   ├── onboarding.md
│   ├── investigation-workflow.md
│   ├── evidence-collection.md
│   └── migration-checklist.md
│
├── templates/                             ← NEW folder: output format specs
│   ├── resolver-analysis.md
│   ├── federation-entity.md
│   ├── migration-report.md
│   └── story-format.md
│
├── reference/                             ← NEW folder: stable lookup data
│   ├── domain-service-catalog.md
│   ├── output-conventions.md
│   ├── federation-patterns.md
│   └── stitching-patterns.md
│
└── examples/
    ├── EXAMPLES.md
    └── product-domain/
```

---

## Open Questions Not Resolved in This Thread

1. **Should `output-conventions.md` live in `reference/` or be a template?** It's consumed by skills as a format spec (template behavior) but also serves as a universal rule reference (reference behavior). Decision: `reference/` for now, since skills reference it and it's not a fill-in-the-blank document.

2. **When the team adds new domains not in the catalog, what's the contribution process?** A lightweight contribution guide would help. Suggested next step: add a `CONTRIBUTING.md` with the pattern for adding a new domain entry.

3. **Should the `examples/product-domain/` sample output use the new file naming (`01-schema-inventory.md`) or keep the old naming?** The sample output uses old filenames. Recommend renaming to match new skill names for consistency.

4. **The `techpack-migration-options.md` reference document** was at the root of the original repo. It belongs in `reference/` but wasn't moved in this thread — it should be added there.
