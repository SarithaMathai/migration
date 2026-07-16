# Building Investigation Tools: Skills, Agents, Instructions, and Templates

A practical guide for engineers building or extending this migration investigation framework. Explains what each component type is, when to use each, the rule of thumb for creating them, and demonstrates each with a real example from this framework.

---

## Overview: The Four Component Types

| Type | What It Is | Written For | Scope |
|------|-----------|------------|-------|
| **Skill** | A focused, single-capability analysis tool | AI assistants (GitHub Copilot, Claude) | One well-defined task |
| **Agent** | A multi-step orchestrator that coordinates skills | AI assistants | One investigation goal |
| **Instruction** | A human-readable operational playbook | Engineers | Setup, process, workflow |
| **Template** | A fill-in-the-blank output format | AI and Engineers | Standardized artifacts |

---

## Part 1: Skills

### What Is a Skill?

A skill is the smallest useful unit of reusable capability. It does one thing well, takes defined inputs, and produces defined outputs. It can be used standalone or composed into an agent.

Think of a skill like a Unix command: focused, composable, predictable.

### What Makes Something a Skill (Not an Agent)?

A skill should:
- Do **one thing** (analyze resolvers, not analyze resolvers AND derive schema)
- Have a **clear input** (a domain name, a file, a phase's output)
- Have a **clear output** (a specific artifact or analysis)
- Be **invocable independently** without needing to run anything else first
- Be **composable** — an agent can chain it with other skills

A skill should NOT:
- Contain workflow logic ("if X done, then do Y")
- Orchestrate other skills
- Include setup/teardown instructions
- Embed output format specifications (those go in templates)

### Rule of Thumb for Creating a Skill

> **Can an engineer describe this capability in one sentence that starts with a verb?**
> "Analyze GraphQL resolver dependencies" → Skill.
> "Investigate a domain and produce migration artifacts" → Agent, not a skill.

If the capability requires coordinating multiple smaller capabilities, it's an agent.
If it's a process with conditional steps ("first check X, then if Y do Z"), it's an instruction.
If it's a fill-in-the-blank document, it's a template.

### Skill File Structure

```
skills/{skill-name}/SKILL.md
```

Every SKILL.md contains:

```markdown
---
name: {kebab-case-skill-name}
description: {one sentence: what it does and what it produces}
argument-hint: {example invocations}
---

# {Skill Title}

## Purpose
{2–3 sentences on what this skill does and when to use it}

## Cannot Run Without
{pre-conditions: what inputs are required}

## Step-by-Step Procedure
### Step 1: {name}
{concrete actions}
### Step 2: {name}
...

## Output Format
{what file or artifact it produces — reference a template if applicable}

## Completion Criteria
- [ ] {objective, verifiable criterion}
- [ ] {another criterion}
```

---

### Skill Example: `resolver-dependency-analysis`

**The question that created it:** "What does every resolver in this domain actually do, and what services does it depend on?"

**Why it's a skill, not an agent:**
- It does one thing: reads source code and produces pseudo-logic
- Its input is well-defined: the output of `graphql-schema-inventory`
- Its output is well-defined: `be-02-resolver-analysis.md`
- It can be run independently: `"Run the resolver analysis for the bom domain"`
- It can be composed: the `full-migration-investigation` agent calls it as Phase 2

**What it is NOT:**
- It doesn't decide what schema to derive (that's `federation-schema-derivation`)
- It doesn't generate stories (that's `migration-story-generation`)
- It doesn't explain HOW to run the pipeline (that's an instruction)

**Example SKILL.md (abbreviated):**

```markdown
---
name: resolver-dependency-analysis
description: "Reads every resolver, service method, and util in a domain and produces
  plain-English pseudo-logic with step-numbered logic, REST endpoint details, and
  EXT service call tagging. Output: output/{domain}/be-02-resolver-analysis.md"
argument-hint: "Provide the domain: 'Run resolver analysis for bom'"
---

# Resolver Dependency Analysis

## Purpose
Reads every source file identified in the schema inventory and produces plain-English
pseudo-logic that engineers can implement from — without reading JavaScript.
Tags every cross-domain HTTP call with severity 🔴/🟡/🔵.

## Cannot Run Without
- output/{domain}/be-01-schema-inventory.md (from graphql-schema-inventory skill)
- Read access to resolver, service, and utils files listed in the manifest

## Step-by-Step Procedure

### Step 1: Read the file manifest
Open output/{domain}/be-01-schema-inventory.md and note all files to analyze.

### Step 2: Analyze each query resolver
For every query, produce a pseudo-logic block: schema signature, numbered steps,
REST endpoint details, error handling, EXT service calls with severity.
...

## Output Format
Write to: output/{domain}/be-02-resolver-analysis.md
Follow the format in templates/resolver-analysis.md
```

---

### When Should a Skill Be Split Into Two?

Split a skill if:
- It produces two unrelated outputs (e.g., both a file inventory AND a schema analysis)
- It answers two different questions that engineers ask independently
- One half of it is substantially larger than the other
- Adding it to different agents would only need one half

**Example split that was made in this framework:**

The original `03-schema-derivation` skill did two things:
1. Identify which types are entity candidates (federation analysis)
2. Write the DGS schema file

These were split into:
- `federation-candidate-detection` — answers "what should be federated?"
- `federation-schema-derivation` — answers "what does the DGS schema look like?"

An architect can now invoke `federation-candidate-detection` without generating a full schema file.

---

## Part 2: Agents

### What Is an Agent?

An agent is a goal-oriented orchestrator. It coordinates multiple skills toward a specific investigation outcome. An engineer invokes an agent with a high-level goal; the agent decides which skills to run and in what order.

Think of an agent like a process: it has a start state (the investigation question), a set of steps (the skills), and an end state (the artifacts produced).

### What Makes Something an Agent (Not a Skill)?

An agent should:
- Have a **clear investigation goal** ("investigate domain X for migration")
- **Coordinate multiple skills** (not implement analysis itself)
- Make **workflow decisions** (if Phase 1 finds a large file, adjust Phase 2 mode)
- Produce a **coherent set of outputs** that together answer the goal

An agent should NOT:
- Implement analysis logic (that goes in skills)
- Duplicate skill logic inline (the skill defines the procedure)
- Be so broad it covers every possible investigation (create multiple focused agents)

### Rule of Thumb for Creating an Agent

> **Can an engineer describe this investigation goal in one sentence?**
> "Perform a full migration analysis for a domain" → Agent.
> "Determine if a domain is ready for federation" → Agent.
> "Analyze resolver dependencies" → Skill, not an agent.

If the goal requires only one skill, it's not an agent — just invoke the skill directly.
If the goal is so broad it's everything, split it into multiple focused agents.

### Agent File Structure

```
agents/{name}.agent.md
```

Every agent file contains:

```markdown
---
name: {agent-name}
description: {one paragraph: what it does, when to use it, what it produces}
argument-hint: {example invocations}
model: claude-sonnet-4-6
temperature: 0.1
---

# {Agent Title}

## Role
{What expertise and perspective this agent brings}

## What You Need to Provide
{Required and optional inputs}

## What You Produce
{Table of outputs: artifact, file, audience}

## Skills Coordinated
{List of skills this agent orchestrates, in order}

## Workflow
{When to run which skills, conditional logic, how to handle errors}

## Quick Examples
{3–5 copy-paste invocations}
```

---

### Agent Example: `federation-readiness`

**The question that created it:** "I need an architect to quickly assess which entities in this domain should be federated before we plan the full migration."

**Why it's an agent, not a skill:**
- It coordinates two skills: `federation-candidate-detection` + `stitching-pattern-analysis`
- It has a clear investigation goal: assess federation readiness
- It makes workflow decisions: runs candidate detection first, then uses those findings to assess stitching strategy

**Why it's a separate agent, not part of `full-migration-investigation`:**
- Architects need this answer without running a 60-minute full pipeline
- The output is targeted: federation boundary decisions only, no stories, no sprint plan
- It can be completed in ~10 minutes

**Example agent file (abbreviated):**

```markdown
---
name: federation-readiness
description: >
  Assesses federation readiness for a domain by identifying entity boundaries,
  @key candidates, and gateway stitching requirements. For architects and tech leads
  who need federation design decisions before committing to full migration analysis.
  Produces a Cross-Domain Reference Analysis table and stitching strategy per field.
argument-hint: "Assess federation readiness for the {domain} domain."
---

# Federation Readiness Agent

## Role
Federation architect for the spark-internal-graphql → DGS migration. Identifies which types
should be federated via @key, which should be gateway-stitched, and which can be
resolved directly. Produces actionable federation design decisions.

## What You Need to Provide
- Domain name (loader key)
- (Optional) Phase 2 output if already complete — saves re-analysis

## What You Produce
| Output | Format | Audience |
|--------|--------|---------|
| Entity boundary analysis | Chat + optional file | Architects |
| Cross-domain reference table | In-chat table | Tech Lead |
| Stitching strategy per field | In-chat table | Architects |

## Skills Coordinated
1. graphql-schema-inventory (if Phase 1 not done)
2. federation-candidate-detection
3. stitching-pattern-analysis

## Workflow
Step 1: Check if Phase 1 output exists for the domain.
  - If yes: load it. Skip to Step 2.
  - If no: invoke graphql-schema-inventory skill first.
Step 2: Invoke federation-candidate-detection.
Step 3: Invoke stitching-pattern-analysis using the candidates from Step 2.
Step 4: Produce Cross-Domain Reference Analysis table with strategy per field.
```

---

### The Right Number of Agents

This framework has four agents:

| Agent | Goal | Time |
|-------|------|------|
| `full-migration-investigation` | Complete domain analysis, all 6 artifacts | 20–60 min |
| `schema-ownership` | Type ownership and schema structure | ~10 min |
| `federation-readiness` | Entity boundaries and stitching decisions | ~10 min |
| `quick-scope` | Complexity estimate for planning | ~5 min |

**Why not more?** Agents are entry points. Too many creates confusion about which to use. The rule: one agent per distinct investigation goal that engineers will ask for independently.

**Why not fewer?** A single monolithic agent forces engineers through a 60-minute pipeline when they only need a 5-minute estimate. Focused agents let engineers get answers proportional to their actual question.

---

## Part 3: Instructions

### What Is an Instruction?

An instruction is a human-readable operational playbook. It tells engineers (not AI assistants) how to do something: how to set up their workspace, how to decide which agent to run, how to collect and document findings.

Think of an instruction like a runbook or SOP: sequential steps, decision points, clear outcomes.

### What Makes Something an Instruction (Not a Skill)?

Instructions are for **humans**. Skills are for **AI assistants**.

An instruction should:
- Be written for an engineer to read and follow
- Explain **why** steps matter, not just what to do
- Include **decision trees** ("if X, then Y")
- Cover **setup, process, and validation**
- Reference skills and agents by name without embedding their logic

An instruction should NOT:
- Contain the analysis logic itself (that goes in skills)
- Duplicate output format specs (those go in templates)
- Be structured as a SKILL.md

### Rule of Thumb for Creating an Instruction

> **Is this guidance a human would follow, or a procedure an AI assistant would execute?**
> "How to set up your workspace before running investigations" → Instruction.
> "How to read and document every resolver's dependencies" → Skill.

If a human reads it to understand what to do, it's an instruction.
If an AI assistant reads it to execute a procedure, it's a skill.

### Instruction File Structure

```
instructions/{topic}.md
```

Each instruction is a plain markdown document. No YAML frontmatter required.

```markdown
# {Instruction Title}

## Purpose
{What this instruction covers and who it's for}

## Prerequisites
{What must be true before following this instruction}

## Steps
### Step 1: {name}
{clear actions + decision branches if applicable}

## Checklist
- [ ] {item}

## References
- [Skill: X](../skills/X/SKILL.md)
- [Template: Y](../templates/Y.md)
```

---

### Instruction Example: `investigation-workflow.md`

**The question that created it:** "I have spark-internal-graphql open — which agent do I run for what I need?"

**Why it's an instruction, not an agent:**
- It doesn't run analysis; it helps a human decide what to run
- It contains a decision tree for the human to follow
- It references agents and skills by name without executing them

**Why it's an instruction, not a skill:**
- An AI assistant doesn't need this decision tree — it can read the agent descriptions
- A human engineer is the reader
- It contains contextual guidance ("if you're a tech lead scoping a new domain...")

**Example (abbreviated):**

```markdown
# Investigation Workflow — Which Agent to Run

## By Role

### I'm a Tech Lead scoping a new domain
→ Run: quick-scope agent
→ Time: ~5 minutes
→ You'll get: complexity estimate, operation count, EXT service summary

### I'm an Architect assessing federation design
→ Run: federation-readiness agent
→ Time: ~10 minutes
→ You'll get: entity boundary decisions, stitching strategy per field

### I'm an Engineer implementing a domain
→ Run: full-migration-investigation agent
→ Time: 20–60 minutes depending on domain size

## By Question

| Question | Agent/Skill |
|---------|------------|
| How many operations does this domain have? | quick-scope |
| What types should be @key federated? | federation-readiness |
| What does this resolver actually do? | resolver-dependency-analysis (skill, standalone) |
| What does the DGS schema look like? | Run phases 1+2+3 via full-migration-investigation |
| What stories should engineering work on? | Run all phases via full-migration-investigation |
```

---

## Part 4: Templates

### What Is a Template?

A template is a fill-in-the-blank output format. It defines what an artifact looks like — the sections, the ordering, the table shapes, the mandatory fields.

Think of a template like a document standard: it ensures every investigator produces artifacts in the same shape, making them reviewable and auditable by anyone.

### What Makes Something a Template (Not a Skill or Instruction)?

A template defines **what output looks like**. A skill defines **how to produce output**. An instruction defines **how a human runs the process**.

A template should:
- Define all sections of an artifact
- Show the exact table structure with placeholder values
- Define mandatory vs. optional sections
- Be referenced by skills ("write output using templates/X.md")

A template should NOT:
- Contain analysis logic (that's a skill)
- Contain setup steps (that's an instruction)
- Be embedded inside a skill file (skills reference templates; they don't duplicate them)

### Rule of Thumb for Creating a Template

> **Would two different investigators, given the same input, produce a differently shaped document?**
> If yes, you need a template to standardize the output.

If an artifact format is used only once, don't template it.
If two or more skills produce similar output shapes, template the shared structure.

### Template File Structure

```
templates/{artifact-type}.md
```

Templates use `{placeholders}` for variable content and `[Description of what goes here]` for explanatory notes.

---

### Template Example: `resolver-analysis.md`

**The question that created it:** "Every domain investigation produces a resolver analysis document. How do we make sure they all look the same so a reviewer can scan them predictably?"

**Why it's a template, not embedded in the skill:**
- The `resolver-dependency-analysis` skill references it — the format is decoupled from the logic
- A different skill (`federation-candidate-detection`) also reads resolver analysis output — a stable format makes it parseable
- If the format changes, you update one template, not every skill that produces resolver output

**Example (abbreviated):**

```markdown
# Phase 2: Resolver Dependency Analysis — {Domain Display Name}

> **Domain:** `{loader-key}`
> **Target DGS:** `{ServiceClassName}` (repo: `{repo}`)
> **Pipeline Version:** 1.1
> **Generated:** {YYYY-MM-DD}
> **Depends on:** [be-01-schema-inventory.md](./be-01-schema-inventory.md)
> **DGS Target Status:** {Green-field | Existing schema found}

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Query resolvers | {n} |
| Mutation resolvers | {n} |
| Field resolvers | {n} (trivial: {n}) |
...

---

## Q{n}: `{queryName}`

**Schema signature:**
```graphql
{queryName}({args}): {ReturnType}
```

**Resolver location:** `{relativePath}:{startLine}-{endLine}`
**Complexity:** {Low | Medium | High | Very High}

**Pseudo-logic:**
1. {Step}
   - {Sub-step if applicable}
2. {Step}

**EXT Service Calls:**
[None | EXT Service tags with severity]

**Error handling:**
- {Specific error condition} → {specific behavior}
```

---

## How the Four Types Work Together

The following example shows how a single investigation uses all four component types:

### Scenario: Tech lead wants to know if the BOM domain is ready for federation

**1. The tech lead reads an instruction:**
`instructions/investigation-workflow.md`
→ Finds: "I'm assessing federation design → Run: federation-readiness agent"

**2. The tech lead invokes an agent:**
`agents/federation-readiness.agent.md`
→ The agent orchestrates two skills

**3. The agent invokes skills:**
- `skills/graphql-schema-inventory/SKILL.md` → discovers BOM source files
- `skills/federation-candidate-detection/SKILL.md` → identifies Bom, BomMaterial as @key candidates
- `skills/stitching-pattern-analysis/SKILL.md` → determines Product reference = gateway stitch

**4. Skills write output using templates:**
- `templates/federation-entity.md` → structures the entity candidate findings
- Cross-domain Reference Analysis table (inline in chat)

**Result:** In 10 minutes, the tech lead has:
- Which BOM types should be `@key` federated
- Which fields are gateway-stitched
- Which EXT calls need CAT-4 stories

**Without templates:** Each investigation would produce a differently shaped table.
**Without skills:** The agent would have to implement the analysis logic itself, making it non-reusable.
**Without instructions:** The tech lead wouldn't know which agent to run.
**Without agents:** The tech lead would have to manually orchestrate 3 skills in the right order.

---

## Decision Cheat Sheet

| I want to… | Create a… |
|-----------|-----------|
| Define a reusable analysis capability | Skill |
| Orchestrate multiple skills toward a goal | Agent |
| Write a runbook for engineers to follow | Instruction |
| Standardize what an artifact looks like | Template |
| Document domain-specific lookup data | Reference (not any of the above) |
| Explain how the framework works | Instruction or README |

---

## Common Mistakes

| Mistake | What Happened | Fix |
|---------|--------------|-----|
| Embedding output format specs inside a skill | Format changes require editing the skill | Move format to a template; skill references it |
| Creating an agent that does only one skill's work | Not really an agent | Just invoke the skill directly |
| Writing domain-specific logic inside a skill | Skill becomes non-reusable | Move domain facts to reference/domain-service-catalog.md |
| Creating an instruction that an AI is supposed to execute | Instructions are for humans | Convert to a skill with SKILL.md frontmatter |
| Creating a skill so broad it needs 20 steps | It's actually two skills | Split into two focused skills |
| Duplicating the domain catalog in multiple files | Single source of truth broken | Reference/domain-service-catalog.md is the only copy |

---

## Naming Conventions

| Type | Convention | Examples |
|------|-----------|---------|
| Skill folders | `kebab-case-capability-verb-noun` | `resolver-dependency-analysis`, `graphql-schema-inventory` |
| Agent files | `kebab-case-goal.agent.md` | `federation-readiness.agent.md`, `quick-scope.agent.md` |
| Instruction files | `kebab-case-topic.md` | `investigation-workflow.md`, `migration-checklist.md` |
| Template files | `kebab-case-artifact-type.md` | `resolver-analysis.md`, `story-format.md` |
| Reference files | `kebab-case-topic.md` | `domain-service-catalog.md`, `federation-patterns.md` |

**Rule:** Names should answer "what does this do?" without reading the file.
`02-code-analysis` does not answer that question. `resolver-dependency-analysis` does.
