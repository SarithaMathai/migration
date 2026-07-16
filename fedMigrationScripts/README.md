# Spark GraphQL → Federated GraphQL Migration Investigation Framework

A reusable investigation toolkit for analyzing the `spark-internal-graphql` edge layer and producing migration-ready artifacts for each domain service.

---

## What This Is

`spark-internal-graphql` is a centralized Node.js GraphQL gateway that proxies 37+ backend microservices. This framework provides the tools to investigate every domain, understand its stitching logic, and produce structured migration artifacts — without needing to run any services or access any databases.

**Target architecture:** Federated GraphQL with Netflix DGS subgraphs stitched via Hive Gateway.

---

## Who It's For

| Role | Uses |
|------|------|
| Backend Engineers | Resolver pseudo-logic, Jira stories, implementation specs |
| Tech Leads | File inventories, cross-domain dependencies, scope estimates |
| Architects | Federation schema, entity boundaries, stitching strategies |
| Product Owners | Sprint plans, effort estimates, migration sequencing |

---

## Start Here

New to this framework? Read [ONBOARDING.md](./ONBOARDING.md) — it gets you running in 5 minutes.

Need detailed usage? Read [USAGE.md](./USAGE.md).

Want to understand how skills, agents, instructions, and templates work? Read [agentsMakeGuide.md](./agentsMakeGuide.md).

---

## Folder Structure

```
fedMigrationScripts/
├── README.md                          ← This file
├── ONBOARDING.md                      ← Start here (5 steps)
├── USAGE.md                           ← Full usage guide
├── agentsMakeGuide.md                 ← How skills/agents/instructions/templates work
├── threadDiscussion.md                ← Design rationale discussion
│
├── skills/                            ← Focused, reusable analysis capabilities
│   ├── graphql-schema-inventory/      ← Locate and catalog all domain source files
│   ├── resolver-dependency-analysis/  ← Document resolver logic and EXT service calls
│   ├── federation-schema-derivation/  ← Derive target DGS GraphQL schema
│   ├── federation-candidate-detection/← Identify entity boundaries and @key candidates
│   ├── stitching-pattern-analysis/    ← Analyze cross-domain joins and gateway stitching
│   ├── migration-story-generation/    ← Generate Jira-ready engineering stories
│   └── oneStopDoc-generation/         ← Regenerate all 4 publication artifacts per domain
│
├── agents/                            ← Multi-skill orchestrators for investigation goals
│   ├── full-migration-investigation.agent.md  ← Complete 4-phase domain analysis
│   ├── federation-readiness.agent.md          ← Entity boundaries + stitching analysis
│   ├── schema-ownership.agent.md              ← Schema inventory + type ownership
│   └── quick-scope.agent.md                   ← Fast complexity estimate
│
├── instructions/                      ← Human operational playbooks
│   ├── onboarding.md                  ← Workspace setup and pre-flight checklist
│   ├── investigation-workflow.md      ← Which agent/skill to run for which question
│   ├── evidence-collection.md         ← What artifacts to capture and where
│   └── migration-checklist.md         ← Pre/post migration validation
│
├── templates/                         ← Fill-in-the-blank output formats
│   ├── resolver-analysis.md           ← Resolver pseudo-logic block format
│   ├── federation-entity.md           ← Entity candidate and @key decision format
│   ├── migration-report.md            ← Full domain migration report structure
│   └── story-format.md                ← Jira story template with acceptance criteria
│
├── reference/                         ← Stable lookup data consumed by agents and skills
│   ├── domain-service-catalog.md      ← 37+ service mapping (loader key → DGS target)
│   ├── output-conventions.md          ← Universal artifact format rules
│   ├── federation-patterns.md         ← @key, @requires, entity resolution patterns
│   ├── stitching-patterns.md          ← Gateway stitch and cross-domain join patterns
│   └── techpack-migration-options.md  ← TechPack migration analysis (Options B/C/D)
│
└── examples/                          ← Sample output for reference
    ├── EXAMPLES.md                    ← Copy-paste invocation examples
    └── product-domain/                ← Full sample output for the product domain
```

---

## What You Get Per Domain

Running the full pipeline produces **six analysis artifacts** plus **two publication artifacts**:

### Analysis artifacts (source of truth — in `finalOutput/{domain}/`)

| File | Purpose | Audience |
|------|---------|---------|
| `be-01-schema-inventory.md` | Every source file, line counts, cross-domain refs | Tech Lead |
| `be-02-resolver-analysis.md` | Plain-English pseudo-logic for every operation | Engineers |
| `be-03-schema.graphql` | Target DGS GraphQL schema (green-field) | Architects |
| `be-03-schema-analysis.md` | Type classification, federation boundaries, gap analysis | Architects |
| `be-04-stories.md` | Jira-ready engineering tickets | Engineering Team |
| `be-04-po-summary.md` | Sprint planning table with effort estimates | Product Owner |

### Publication artifacts (generated — in `finalOutput/oneStopDoc/`)

Run `python finalOutput/oneStopDoc/generate_all.py` to produce all five for all 13 domains.
Each domain's artifacts are in their own subfolder: `finalOutput/oneStopDoc/{domain}/`.

| File | Purpose | Audience |
|------|---------|---------|
| `FederatedGqlBrakDown-BE-{domain}.docx` | **Primary — Word doc with full formatting**: navy blue headers, metrics banner, colored story tables, icons (🔷🔶🔸 🔴🟠🟡🟢) | PO + Engineers (open in Word or paste into Confluence) |
| `FederatedGqlBrakDown-BE-{domain}.md` | Markdown fallback — same content and table format as the Word doc | PO + Engineers (paste raw Markdown into Confluence) |
| `{domain}/{domain}-comprehensive.md` | Full engineering doc — all stories, AC, test cases (High/VH only), complex story callouts | Engineers + Tech Leads |
| `{domain}/{domain}-po-review.md` | Executive PO review — scope, risks, decisions, sprint capacity, Phase 2 breakdowns | Product Owner + Stakeholders |
| `{domain}/{domain}.csv` | Jira import CSV — Epic + stories; schema init excluded; tests for High/VH only | Jira admin |

Plus program-level docs at the `oneStopDoc/` root:
- `Federated+Graphql+Stories+-+BreakDown.docx` — All 325 stories in one Word doc: domain index table + per-domain story tables (primary)
- `Federated+Graphql+Stories+-+BreakDown.md` — Same content as Markdown (Confluence paste fallback)
- `fe-00-executive-summary.md` — Cross-domain scope, risks, migration sequence, per-domain quick reference
- `00-portfolio.md` — Program portfolio table for Confluence space home
- `jira/all-stories.csv` — All 325 stories in one Jira import file

See [`skills/oneStopDoc-generation/SKILL.md`](./skills/oneStopDoc-generation/SKILL.md) for full details.

---

## Key Principles

- **No target DGS repo required** — all output derived from spark-internal-graphql source alone
- **No running services required** — static analysis only
- **No databases or environment variables needed**
- **Green-field by default** — all schema output marked 🔜 (needs migration)
- **Deterministic outputs** — same input always produces same artifact shape
- **Auditable** — every artifact has a header showing what was analyzed and when
