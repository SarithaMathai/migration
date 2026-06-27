# Investigation Workflow — Which Agent or Skill to Run

**Purpose:** Help you choose the right starting point for your investigation based on your role and question.
**Audience:** Engineers, tech leads, architects, and product owners starting an investigation.

---

## Start Here: What's Your Question?

### "What's in this domain? How big is it?"

→ **Run: `quick-scope` agent**
→ Time: ~5 minutes
→ You'll get: operation count, complexity distribution, EXT service summary, rough effort estimate

```
Quick scope of the {domain} domain.
```

---

### "What types does this domain own? What does it reference from other domains?"

→ **Run: `schema-ownership` agent**
→ Time: ~10 minutes
→ You'll get: source file manifest, type ownership table, cross-domain reference summary

```
Analyze schema ownership for the {domain} domain.
```

---

### "Which types should be federated? What needs Hive Gateway stitching?"

→ **Run: `federation-readiness` agent**
→ Time: ~10 minutes
→ You'll get: entity candidate list with @key decisions, stitching strategy per field, CAT-4 requirements

```
Assess federation readiness for the {domain} domain.
```

---

### "I need everything — inventory, pseudo-logic, schema, stories, sprint plan"

→ **Run: `full-migration-investigation` agent**
→ Time: 20–60 minutes depending on domain size
→ You'll get: all 6 artifacts

```
Analyze the {domain} domain for DGS migration — run all phases.
```

---

## By Role

### Tech Lead

| Task | Agent/Skill | Time |
|------|------------|------|
| Scope a new domain before committing team | `quick-scope` | ~5 min |
| Compare complexity across multiple domains | `quick-scope` (run for each) | ~5 min each |
| Understand what's in a domain | `schema-ownership` | ~10 min |
| Identify EXT service dependencies before sprint planning | `graphql-schema-inventory` (skill, standalone) | ~5 min |
| Full domain analysis for the team | `full-migration-investigation` | 20–60 min |

### Architect

| Task | Agent/Skill | Time |
|------|------------|------|
| Define federation entity boundaries | `federation-readiness` | ~10 min |
| Determine Hive Gateway stitching requirements | `federation-readiness` or `stitching-pattern-analysis` (skill, standalone) | ~10 min |
| Validate federation strategy for a specific field | `stitching-pattern-analysis` (skill, standalone) | ~2 min |
| Get the DGS schema contract | `full-migration-investigation` Phases 1–3 | 20–45 min |
| Review schema type classification | `federation-schema-derivation` (skill, standalone) | ~5 min |

### Backend Engineer

| Task | Agent/Skill | Time |
|------|------------|------|
| Get implementation spec for a domain | `full-migration-investigation` Phase 2 (full mode) | 15–60 min |
| Understand one resolver | `resolver-dependency-analysis` (skill) on specific function | ~2 min |
| Get Jira stories for implementation | `full-migration-investigation` all phases | 20–60 min |
| Re-generate stories after analysis changes | `migration-story-generation` (skill, standalone) | ~10 min |

### Product Owner

| Task | Agent/Skill | Time |
|------|------------|------|
| Get effort estimate before sprint planning | `quick-scope` | ~5 min |
| Get full sprint plan with priorities | `full-migration-investigation` all phases | 20–60 min |
| Understand what's in each migration phase | Read `04-po-summary.md` after full pipeline | — |

---

## Phased Approach Decision Tree

Use this when you want to run phases individually and review between each:

```
Start
│
├── Do you know the domain is worth full analysis?
│   ├── NO → Run quick-scope first (~5 min)
│   └── YES → Continue
│
├── Do you need federation decisions before schema derivation?
│   ├── YES → Run federation-readiness before or alongside Phase 3
│   └── NO → Continue straight through phases
│
├── Is the domain large (>1000 line resolver)?
│   ├── YES → Run Phase 1, review, then Phase 2 in full mode
│   │         Consider running Phase 2 by section (Queries, Mutations, Fields)
│   └── NO → Can run Phases 1+2 together
│
└── Do you need the DGS schema first (for other teams to use)?
    ├── YES → Run Phases 1+2+3, share schema, run Phase 4 later
    └── NO → Run all phases in one go
```

---

## Commonly Asked Questions — Exact Prompts

| Question | Prompt to Type |
|---------|---------------|
| What domains are available? | `What domains are in the service catalog?` |
| What phases are done for a domain? | `What phases are complete for {domain}? Check output/{domain}/` |
| How complex is this domain? | `Quick scope of the {domain} domain` |
| What EXT services does this domain call? | `What external services does the {domain} domain call? Show all EXT calls with severity.` |
| What does resolver X do? | `Explain what {functionName} does in SPARK_{Domain}.js` |
| What should be @key federated? | `Assess federation readiness for the {domain} domain` |
| What Hive Gateway config do I need? | `What does the {domain} domain need to stitch in Hive Gateway?` |
| Re-run one phase | `Re-run Phase {N} for {domain} — {reason for re-run}` |
| Audit existing output | `Audit output/{domain}/04-stories.md — check against story format, report gaps` |
| Add a missing domain | `Add {loaderKey} to the catalog with URL {url} and target DGS {ServiceName}` |

---

## When to Use Individual Skills vs. Agents

**Use an agent** when you have an investigation goal and want the AI to decide which skills to run.

**Use a skill directly** when you know exactly what you need and want to skip agent orchestration overhead.

| Invoke | When |
|--------|------|
| `full-migration-investigation` agent | You want all 6 artifacts |
| `schema-ownership` agent | You want type ownership decisions |
| `federation-readiness` agent | You want federation boundary decisions |
| `quick-scope` agent | You want a fast complexity estimate |
| `graphql-schema-inventory` skill | You want just the file manifest |
| `resolver-dependency-analysis` skill | You want just the pseudo-logic |
| `federation-candidate-detection` skill | You want just type classification |
| `stitching-pattern-analysis` skill | You want a specific stitching strategy |
| `federation-schema-derivation` skill | You want just the schema file |
| `migration-story-generation` skill | You want just the stories (phases 1–3 done) |

---

## What NOT to Do

| Don't | Do Instead |
|-------|-----------|
| Run Phase 4 without Phase 2 | Always run Phase 2 in full mode before stories |
| Run quick-scope and use it for story generation | Quick Scan output doesn't have enough detail — run full Phase 2 |
| Skip Phase 1 and go straight to Phase 2 | Phase 2 depends on the file manifest from Phase 1 |
| Ask for a domain not in the catalog | Add it first: `Add {key} to the catalog with URL {url}` |
| Run product domain full pipeline in one shot | Product is 2600+ lines — run phases individually |
| Expect DGS schema to scan existing DGS files | It won't — all output is green-field unless you provide DGS files explicitly |
