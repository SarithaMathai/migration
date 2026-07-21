# GraphQL Migration Investigation — Start Here

Everything you need to run a domain investigation in 5 steps.

---

## What You Need Before Starting

- [ ] `spark-internal-graphql` repository cloned locally
- [ ] VS Code open with GitHub Copilot enabled (or Claude Code active)
- [ ] This `fedMigrationScripts/` folder copied into your workspace root

You do **not** need:
- The target DGS microservice repository
- Any running services or databases
- Any environment variables configured

---

## Step 1 — Set Up Your Workspace

Your workspace should look like this:

```
{your-workspace}/
├── spark-internal-graphql/                     ← Clone this repo locally
│   └── packages/
│       └── data-source-spark/
│           └── src/
│               ├── schemas/           ← .graphql schema files
│               ├── resolvers/         ← .js resolver files
│               ├── services/          ← .js service files
│               ├── utils/             ← shared utility files
│               ├── config/            ← constants and flags
│               └── context.js         ← service wiring (loader keys + URLs)
├── fedMigrationScripts/                      ← These investigation assets
└── output/                            ← Pipeline writes artifacts here (auto-created)
    └── {domain}/
        ├── be-01-schema-inventory.md
        ├── be-02-resolver-analysis.md
        ├── be-03-schema.graphql
        ├── be-03-schema-analysis.md
        ├── be-04-stories.md
        └── be-04-po-summary.md
```

If `spark-internal-graphql` is at a different path, tell the agent at the start:
> "spark-internal-graphql is at `/Users/me/projects/spark-internal-graphql`"

---

## Step 2 — Confirm Your Domain

Check that your domain is in the catalog:

> **Type:** `What domains are in the catalog?`

The agent will list all 37+ available domains. Find yours. If your domain is missing:

> **Type:** `Add {loaderKey} to the catalog with URL {url} and target DGS {ServiceName}`

---

## Step 3 — Run Pre-Flight Checks

Before starting analysis, run the workspace validation:

> **Type:** `Set up for {domain} domain investigation — confirm paths and output folder`

The agent will confirm:
- Domain loader key found in catalog
- Source files located (schema, resolver, service)
- Output folder ready
- Any large files flagged (>1000 lines → will use chunked reading)

---

## Step 4 — Run Your Investigation

Choose your entry point based on what you need:

### Full Domain Analysis (all 6 artifacts, 20–60 min)
```
Analyze the {domain} domain for DGS migration — run all phases.
```

### Quick Scope Check (complexity estimate, ~5 min)
```
Give me a quick scan of the {domain} domain — top operations only.
```

### File Inventory Only (understand what exists, ~3 min)
```
Run the schema inventory for the {domain} domain.
```

### Federation Boundaries Only (entity decisions, ~10 min)
```
Assess federation readiness for the {domain} domain.
```

### Schema and Entity Ownership Only (~15 min)
```
Analyze schema ownership for the {domain} domain — inventory and type classification.
```

---

## Step 5 — Use the Artifacts

| Artifact | Use It To |
|---------|----------|
| `be-01-schema-inventory.md` | Scope the migration, brief the team, identify EXT dependencies |
| `be-02-resolver-analysis.md` | Implement DGS without reading JavaScript. Write acceptance criteria. |
| `be-03-schema.graphql` | Start building the DGS schema. Define federation contracts. |
| `be-03-schema-analysis.md` | Brief the architecture team. Identify type ownership. |
| `be-04-stories.md` | Create Jira tickets. Assign to engineers. |
| `be-04-po-summary.md` | Sprint planning. Stakeholder communication. Capacity planning. |

---

## Quick Reference — Common Prompts

| What You Want | What to Type |
|---|---|
| Full analysis, all phases | `Analyze the {domain} domain — all phases` |
| Just file inventory | `Run the schema inventory for {domain}` |
| Pseudo-logic only | `Run schema inventory and resolver analysis for {domain}` |
| Schema + federation | `Run Phases 1, 2, and 3 for {domain}` |
| Just stories (prior phases done) | `Generate migration stories for {domain} — prior analysis in output/{domain}/` |
| Check available domains | `What domains are in the catalog?` |
| Check analysis status | `What phases are complete for {domain}?` |
| Explain one resolver | `Explain {functionName} in SPARK_{Domain}.js` |
| Find EXT service calls | `What external services does the {domain} domain call?` |
| Sprint plan only | `Give me the PO sprint plan for {domain} — all phases done` |

---

## Pre-Flight Checklist

Run this mentally before every investigation:

- [ ] Domain confirmed in the service catalog
- [ ] spark-internal-graphql is accessible from VS Code
- [ ] Output folder exists or will be auto-created
- [ ] You know which phases you need (full / partial / targeted)
- [ ] If the domain is large (product: 2600+ lines), you've planned for chunked reading

---

## Domain Size Reference

| Domain | Resolver Lines | Operations | Est. Full Pipeline Time |
|--------|--------------|-----------|------------------------|
| bom | ~600 | 10–15 | 15–25 min |
| measurement | ~400 | 10–12 | 10–20 min |
| attachment | ~800 | 15–20 | 20–35 min |
| discussion | ~500 | 10–15 | 15–25 min |
| product | ~2,629 | 40+ | 45–60 min |

For large domains, consider running phases individually and reviewing between each.

---

## If Something Goes Wrong

**"I can't find the domain in the catalog"**
Type: `What domains are available?` — lists all 37+ loader keys.

**"The resolver file is too large and analysis is slow"**
Type: `Give me a quick scan of {domain} — top-level operations only, skip field resolvers`

**"I only have some output files"**
Tell the agent which phases are done: `Run Phase 3 for bom — Phases 1 and 2 are in output/bom/`

**"Output folder doesn't exist"**
The agent creates it during workspace setup, or create manually: `mkdir output/{domain}`

**"I need just one resolver explained"**
You don't need the full pipeline: `Explain what getProducts does in SPARK_Product.js`
