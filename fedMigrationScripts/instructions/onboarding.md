# Onboarding: Setting Up for Domain Investigation

**Purpose:** Walk a new engineer through workspace setup and pre-flight validation before running any investigation.
**Audience:** Engineers who are new to this framework or investigating a domain for the first time.

---

## Prerequisites

Before you start, confirm you have:

- [ ] VS Code installed with GitHub Copilot (or Claude Code active in VS Code)
- [ ] Git access to clone `spark-internal-graphql`
- [ ] This `fedMigrationScripts/` folder available locally

You do **not** need:
- Target DGS microservice repositories (e.g., `plm-product`, `plm-bom`)
- Any running services or databases
- Any environment variables

---

## Step 1: Clone spark-internal-graphql

```bash
git clone {spark-internal-graphql-repo-url}
```

The expected source path structure:

```
spark-internal-graphql/
└── packages/
    └── data-source-spark/
        └── src/
            ├── schemas/        ← .graphql schema files (80 files)
            ├── resolvers/      ← .js resolver files (60+ files)
            ├── services/       ← .js service files (50+ files)
            ├── utils/          ← shared utility files (40+ files)
            ├── config/         ← constants, feature flags
            └── context.js      ← service wiring (ALL endpoints + auth)
```

If your clone is at a non-standard path, note it — you'll tell the agent at startup:
> "spark-internal-graphql is at `/Users/me/projects/spark-internal-graphql`"

---

## Step 2: Arrange Your Workspace

Place this framework folder alongside spark-internal-graphql:

```
{your-workspace}/
├── spark-internal-graphql/              ← cloned repo
├── fedMigrationScripts/               ← this framework
└── output/                     ← will be auto-created during investigation
    └── {domain}/
        ├── 01-schema-inventory.md
        ├── 02-resolver-analysis.md
        ├── 03-schema.graphql
        ├── 03-schema-analysis.md
        ├── 04-stories.md
        └── 04-po-summary.md
```

---

## Step 3: Find Your Domain in the Catalog

Open `reference/domain-service-catalog.md` §2 and find your domain.

You need to confirm:
- **Loader key** — the identifier used in `context.js` (e.g., `bom`, `measurement`)
- **Schema file** — the `.graphql` file (e.g., `SPARK_Bom.graphql`)
- **Resolver file** — the `.js` file (e.g., `product/SPARK_Bom.js`)
- **Target DGS** — the destination service (e.g., `plm-product`)

**Not sure of the loader key?** Type into the AI assistant:
> "What domains are in the service catalog?"

**Domain not in the catalog?** Tell the agent:
> "Add {loaderKey} to the catalog with URL {url} and target DGS {ServiceName}"

---

## Step 4: Run Pre-Flight Validation

Before any analysis, validate your workspace:

> **Type:** `Set up for {domain} domain investigation — confirm paths and output folder`

The AI assistant will:
1. Confirm the domain loader key maps to a valid catalog entry
2. Locate the schema, resolver, service, and utils files
3. Create the `output/{domain}/` folder if it doesn't exist
4. Flag any large files (>1000 lines) that will need chunked reading in Phase 2
5. Confirm DGS target availability (always green-field unless you provide DGS files)

**What a successful pre-flight looks like:**
```
✅ Domain: bom (loader key confirmed)
✅ Schema: spark-internal-graphql/.../schemas/SPARK_Bom.graphql (312 lines)
✅ Resolver: spark-internal-graphql/.../resolvers/product/SPARK_Bom.js (587 lines)
✅ Service: spark-internal-graphql/.../services/Bom.js (234 lines)
✅ Utils: bomUtils.js, commonLoaders.js, loadOne.js
✅ Output folder: output/bom/ (created)
✅ DGS target: green-field (plm-product — no existing schema)
⚠️ No large files detected — Phase 2 will not require chunked reading.
```

---

## Step 5: Choose Your Investigation Entry Point

Now that your workspace is validated, choose what to run:

| What You Need | Command to Type |
|---|---|
| Full analysis, all artifacts | `Analyze the {domain} domain — all phases` |
| Quick scope estimate | `Quick scope of the {domain} domain` |
| Schema ownership only | `Analyze schema ownership for the {domain} domain` |
| Federation boundaries only | `Assess federation readiness for the {domain} domain` |
| Just the file inventory | `Run schema inventory for the {domain} domain` |

For more options, see [investigation-workflow.md](./investigation-workflow.md).

---

## Domain Size Reference (Helps You Choose Mode)

| Domain | Resolver Lines | Est. Full Pipeline | Suggested Approach |
|--------|-------------|--------------------|--------------------|
| measurement | ~400 | 15–20 min | Full pipeline, one pass |
| bom | ~600 | 20–30 min | Full pipeline, one pass |
| discussion | ~500 | 15–25 min | Full pipeline, one pass |
| attachment | ~800 | 25–35 min | Full pipeline, consider phased |
| product | ~2,629 | 45–60 min | **Run phases individually and review** |

---

## Pre-Flight Checklist (Run Before Every Investigation)

- [ ] Domain confirmed in the service catalog
- [ ] spark-internal-graphql is accessible from VS Code
- [ ] Workspace layout confirmed (spark-internal-graphql and output folder in the right place)
- [ ] You know which phases you need (full / partial / targeted)
- [ ] If the domain is large (>1000 line resolver), you've planned for chunked reading
- [ ] If you have existing output/ files from a previous run, you know which phases are done

---

## Troubleshooting Setup Issues

### "I can't find the resolver file at the expected path"

Some domains have resolver files in subdirectories:
- `resolvers/product/SPARK_Bom.js` (not `resolvers/SPARK_Bom.js`)
- `resolvers/productplan/SPARK_ProductPlan.js`

Check the catalog entry's "Resolver File" column for the exact path.

### "context.js doesn't have an entry for my domain"

The loader key you used may differ from the domain name. Common mismatches:
- `discussionV3` not `discussion-v3`
- `sampleV2` not `sample-v2`
- `teamV2` not `team`

Check the catalog for the exact loader key.

### "The output folder already has files from a previous run"

Tell the agent which phases are done:
> "Run Phase 3 for bom — Phases 1 and 2 outputs are already in output/bom/"

The agent will load existing phase output without re-running.

### "I want to start fresh"

Move or rename the existing output folder:
```bash
mv output/bom output/bom-backup-{date}
```
Then run pre-flight again.
