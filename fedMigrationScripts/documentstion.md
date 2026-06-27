# ADR-001: AI-Assisted GraphQL Federation Migration Investigation Framework

**Status:** Proposed  
**Date:** 2026-05-17  
**Authors:** Platform Engineering / Architecture Team  
**Decision Type:** Architecture & Engineering Enablement  
**Related Initiative:** Spark GraphQL → Federated GraphQL Migration

---

# 1. Context

The organization is undertaking a large-scale migration from a legacy Spark GraphQL edge-layer architecture toward a Federated GraphQL platform model hosted in Hive.

The existing Spark GraphQL implementation contains:
- Aggregated GraphQL schemas
- Custom resolver orchestration
- Cross-domain stitching logic
- Service-layer integrations
- Shared utility/helper patterns
- Domain coupling through custom resolver composition

The target architecture moves ownership closer to domain-aligned GraphQL services and uses federation principles to reduce custom edge orchestration.

Key migration goals include:
- Reduce custom stitching logic
- Establish clear entity ownership
- Enable federation by entity IDs
- Identify cross-domain dependencies
- Improve maintainability
- Standardize migration analysis across engineering teams
- Generate reusable migration artifacts

Because multiple domains must be analyzed repeatedly by different senior engineers, the organization requires a reusable investigation framework that:
- Produces deterministic outputs
- Minimizes onboarding complexity
- Standardizes migration analysis
- Avoids dependency on running services or environments
- Works primarily from source code analysis
- Supports VS Code + GitHub Copilot workflows

---

# 2. Problem Statement

Migration investigations were previously:
- Manual
- Inconsistent across engineers
- Difficult to scale
- Hard to audit
- Dependent on tribal knowledge
- Time-consuming for large resolver files
- Missing standardized deliverables

There was no clear separation between:
- reusable analysis capabilities
- orchestration workflows
- human operational instructions
- output formatting conventions
- reference knowledge

As a result:
- engineers duplicated investigation work
- outputs varied in quality and format
- migration planning lacked consistency
- onboarding new investigators required excessive knowledge transfer

---

# 3. Decision

We will implement a reusable AI-assisted migration investigation framework with the following architecture:

## Core Architectural Principles

1. Separate orchestration from execution capabilities
2. Standardize all generated outputs through templates
3. Keep reference knowledge centralized and reusable
4. Optimize for repeatable engineering workflows
5. Prefer deterministic structured analysis over creative reasoning
6. Produce auditable markdown artifacts
7. Use source-code analysis only
8. Minimize operational dependencies

---

# 4. Selected Architecture

## 4.1 Component Model

The framework will consist of five primary component types:

| Component | Purpose | Audience |
|---|---|---|
| Agents | Orchestrate workflows | AI Runtime |
| Skills | Execute focused analysis capabilities | AI Runtime |
| Templates | Standardize outputs | AI Runtime |
| Reference | Supply stable knowledge | AI Runtime |
| Instructions | Human operational guidance | Engineers |

---

## 4.2 High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                     AI-Assisted Migration Framework                │
└─────────────────────────────────────────────────────────────────────┘

        ┌────────────────────┐
        │    👤 Engineer     │
        └─────────┬──────────┘
                  │
                  ▼
    ┌──────────────────────────────┐
    │       Human Components       │
    ├──────────────────────────────┤
    │ • Onboarding Instructions    │
    │ • Workflow Guides            │
    │ • Migration Checklists       │
    │ • Example Investigations     │
    └──────────────┬───────────────┘
                   │ invokes
                   ▼
    ┌──────────────────────────────┐
    │        🤖 AI Agents          │
    │   Workflow Orchestration     │
    └──────────────┬───────────────┘
                   │ coordinates
                   ▼
    ┌──────────────────────────────┐
    │         🔧 Skills            │
    ├──────────────────────────────┤
    │ • Schema Inventory           │
    │ • Resolver Analysis          │
    │ • Federation Detection       │
    │ • Story Generation           │
    └───────┬───────────┬──────────┘
            │           │
            │ reads     │ formats with
            ▼           ▼
┌────────────────┐   ┌────────────────┐
│ 📚 Reference   │   │ 📄 Templates   │
│ Rules/Catalogs │   │ Output Formats │
└────────┬───────┘   └────────┬───────┘
         │                    │
         └─────────┬──────────┘
                   │ analyzes
                   ▼
      ┌──────────────────────────┐
      │   spark-internal-graphql Source   │
      │ Schemas • Resolvers      │
      │ Services • Utilities     │
      └─────────────┬────────────┘
                    │ generates
                    ▼
      ┌──────────────────────────┐
      │   Migration Artifacts    │
      ├──────────────────────────┤
      │ 01-schema-inventory      │
      │ 02-resolver-analysis     │
      │ 03-schema.graphql        │
      │ 03-schema-analysis       │
      │ 04-stories               │
      │ 04-po-summary            │
      └──────────────────────────┘
```

---

# 5. Repository Structure Decision

The repository will follow a convention-based structure.

```text
/framework
├── agents/
├── skills/
├── templates/
├── reference/
├── instructions/
├── examples/
└── output/
```

---

## 5.1 Skills

Skills represent focused reusable analysis capabilities.

### Characteristics

- Narrow responsibility
- Input/output oriented
- Reusable across workflows
- Deterministic behavior
- No workflow orchestration

### Examples

```text
skills/
├── graphql-schema-inventory/
├── resolver-dependency-analysis/
├── federation-candidate-detection/
├── federation-schema-derivation/
├── stitching-pattern-analysis/
└── migration-story-generation/
```

### Rule of Thumb

If the capability can be independently executed and reused by multiple workflows, it belongs in a skill.

---

## 5.2 Agents

Agents orchestrate multi-step workflows.

### Characteristics

- Coordinate multiple skills
- Make workflow decisions
- Manage phase execution
- Handle sequencing
- Provide user entry points

### Examples

```text
agents/
├── full-migration-investigation.agent.md
├── federation-readiness.agent.md
├── schema-ownership.agent.md
└── quick-scope.agent.md
```

### Rule of Thumb

If the logic determines *what happens next*, it belongs in an agent.

---

## 5.3 Templates

Templates standardize output structures.

### Characteristics

- Enforce consistency
- Define section ordering
- Define mandatory fields
- Ensure deterministic outputs

### Examples

```text
templates/
├── migration-report.md
├── resolver-analysis.md
├── federation-entity.md
└── story-format.md
```

### Rule of Thumb

If the artifact defines the shape of generated output, it belongs in a template.

---

## 5.4 Reference

Reference files contain reusable stable knowledge.

### Characteristics

- Centralized lookup information
- Shared conventions
- Reusable rules
- Minimal workflow logic

### Examples

```text
reference/
├── domain-service-catalog.md
├── federation-patterns.md
├── stitching-patterns.md
├── output-conventions.md
└── techpack-migration-options.md
```

### Rule of Thumb

If the content acts as lookup knowledge rather than procedural execution, it belongs in reference.

---

## 5.5 Instructions

Instructions are human operational guides.

### Characteristics

- Step-by-step onboarding
- Operational workflows
- Checklists
- Human-readable guidance

### Examples

```text
instructions/
├── onboarding.md
├── investigation-workflow.md
├── evidence-collection.md
└── migration-checklist.md
```

### Rule of Thumb

If the primary reader is a human engineer, it belongs in instructions.

---

# 6. Workflow Decision

The framework will support a phase-based migration investigation workflow.

## Standard Pipeline

```text
┌──────────────────────────────────────────────────────────────┐
│                Standard Migration Pipeline                  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│ Phase 0              │
│ Workspace Setup      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Phase 1              │
│ Schema Inventory     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Phase 2              │
│ Resolver Analysis    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Phase 3              │
│ Federation Schema    │
│ Derivation           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Phase 4              │
│ Migration Stories    │
│ & Planning Artifacts │
└──────────────────────┘
```

---

## 6.1 Phase Outputs

| Phase | Primary Deliverable |
|---|---|
| Phase 1 | 01-schema-inventory.md |
| Phase 2 | 02-resolver-analysis.md |
| Phase 3 | 03-schema.graphql |
| Phase 3 | 03-schema-analysis.md |
| Phase 4 | 04-stories.md |
| Phase 4 | 04-po-summary.md |

---

# 7. Investigation Flow

```text
┌────────────────────────────────────────────────────────────────────┐
│                     End-to-End Investigation Flow                 │
└────────────────────────────────────────────────────────────────────┘

 Engineer
    │
    │  "Analyze BOM domain"
    ▼
┌──────────────────────┐
│      AI Agent        │
│ Workflow Orchestrator│
└──────────┬───────────┘
           │
           │ Resolve metadata
           ▼
┌──────────────────────┐
│  Reference Catalogs  │
│ Domains • Patterns   │
│ Rules • Conventions  │
└──────────┬───────────┘
           │
           │ Invoke analysis skills
           ▼
┌──────────────────────┐
│       Skills         │
├──────────────────────┤
│ • Schema Inventory   │
│ • Resolver Analysis  │
│ • Federation Logic   │
│ • Story Generation   │
└──────────┬───────────┘
           │
           │ Analyze
           ▼
┌──────────────────────┐
│  spark-internal-graphql Repo  │
│ Source Code Analysis │
└──────────┬───────────┘
           │
           │ Generate artifacts
           ▼
┌──────────────────────┐
│  Migration Outputs   │
├──────────────────────┤
│ • Inventory Reports  │
│ • Resolver Analysis  │
│ • Federation Schema  │
│ • Migration Stories  │
└──────────┬───────────┘
           │
           │ Deliver results
           ▼
        Engineer
```

---

# 8. Tooling Decision

## Selected Tooling

| Tool | Decision |
|---|---|
| VS Code | Approved |
| GitHub Copilot Extension | Primary assistant |
| Claude Agents | Optional |
| Running services | Not required |
| Databases | Not required |
| Environment variables | Not required |
| Target DGS repos | Optional |

---

## Model Selection

The framework standardizes on Sonnet-class reasoning models for all analysis tasks.

### Rationale

The migration workflow primarily requires:
- deterministic structured analysis
- large file reading
- markdown generation
- schema inspection
- resolver analysis
- template-conforming output

Higher-cost creative reasoning models provide limited additional value for these deterministic workflows.

---

# 9. Engineering Workflow Decision

The onboarding process must remain intentionally simple to support repeated use by multiple engineers.

## Standard Engineer Workflow

```text
┌─────────────────────────────────────────────────────────────┐
│                 Standard Engineer Workflow                 │
└─────────────────────────────────────────────────────────────┘

   Clone Repo
        │
        ▼
┌──────────────────────┐
│  spark-internal-graphql Repo  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Copy Framework Assets│
│ agents/ skills/ etc. │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Open VS Code         │
│ Enable GitHub        │
│ Copilot              │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Run Investigation    │
│ Prompts / Agents     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Generate Migration   │
│ Analysis Artifacts   │
└──────────────────────┘
```

---

## Standardized Onboarding

### Step 1
Clone `spark-internal-graphql` locally.

### Step 2
Copy framework assets into the working directory.

### Step 3
Open the workspace in VS Code.

### Step 4
Enable GitHub Copilot.

### Step 5
Run investigation prompts.

### Step 6
Review generated markdown artifacts.

---

# 10. Key Architectural Benefits

## 10.1 Repeatability

All engineers follow the same workflow and generate the same artifact structure.

---

## 10.2 Reduced Knowledge Silos

Migration understanding becomes documented in reusable artifacts rather than tribal knowledge.

---

## 10.3 Deterministic Outputs

Templates and conventions standardize generated analysis.

---

## 10.4 Faster Migration Planning

Resolver analysis and schema derivation are generated systematically.

---

## 10.5 Better Auditability

All generated outputs are stored as markdown artifacts and can be reviewed independently.

---

# 11. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Overly large skills becoming unmaintainable | Keep skills narrowly scoped |
| Agent duplication of skill logic | Centralize execution logic inside skills |
| Inconsistent outputs | Enforce template usage |
| Overly intelligent non-deterministic behavior | Prefer convention-driven workflows |
| Large resolver files exceeding context limits | Use chunked analysis strategy |
| Human onboarding friction | Keep setup steps minimal |

---

# 12. Non-Goals

The framework does NOT attempt to:
- generate production-ready DGS implementations
- deploy services
- run databases
- execute GraphQL services
- automate runtime validation
- replace engineering review
- infer business ownership automatically

The framework is strictly focused on migration investigation and planning.

---

# 13. Alternatives Considered

## Alternative 1 — Fully Manual Investigation

Rejected because:
- inconsistent outputs
- poor scalability
- high engineer effort
- knowledge fragmentation

---

## Alternative 2 — Monolithic Agent Architecture

Rejected because:
- difficult to maintain
- poor reusability
- harder debugging
- excessive prompt complexity

---

## Alternative 3 — Direct Production Code Generation

Rejected because:
- migration requires architectural review
- domain ownership decisions require human validation
- federation boundaries require governance

---

# 14. Consequences

## Positive

- Standardized migration investigations
- Faster onboarding
- Repeatable engineering workflows
- Better migration visibility
- Reusable knowledge base
- Improved planning artifacts

## Negative

- Initial framework investment required
- Requires discipline around conventions
- Generated outputs still require human validation

---

# 15. Final Decision

The organization will adopt a modular AI-assisted migration investigation framework built around:

- Agents for orchestration
- Skills for reusable analysis
- Templates for deterministic outputs
- Reference documents for stable knowledge
- Instructions for operational onboarding

The framework will prioritize:
- simplicity
- repeatability
- auditability
- deterministic engineering workflows
- reusable migration artifacts

This decision establishes the standard investigation architecture for all Spark GraphQL → Federated GraphQL migration initiatives.

