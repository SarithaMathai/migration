# Output — Federated GraphQL Migration Deliverables

> Start here. One-page map of everything under `output/`, by audience.

## Start here, by role

- **Anyone, first time here** → [overview/00-program-overview.md](overview/00-program-overview.md) — the one-page what-and-why, plus [overview/01-architecture-diagrams.md](overview/01-architecture-diagrams.md) (visuals) and [overview/02-story-domain-index.md](overview/02-story-domain-index.md) (where everything lives).
- **Engineer implementing a story** → [../docs/instructions_engineer.md](../docs/instructions_engineer.md) — repo navigation, how to read a story's `Depends on:`/`Blocked by:` fields, implementation workflow, and a worked example.
- **Product Owner prioritizing/reviewing** → [../docs/instructions_po.md](../docs/instructions_po.md) — how to read the backlog and dependency diagrams, the Complex-Story/ADR ratification workflow, and how to read the roadmap.
- **Product Owner / Stakeholder** → [summary/00-program-overview.md](summary/00-program-overview.md), then the per-domain breakdown pages in [summary/{domain}/](summary/) (`.docx` twins for sharing).
- **Tech Lead / Planning** → [summary/01-implementation-plan-1BE-1FE.md](summary/01-implementation-plan-1BE-1FE.md) (who does what, when — lanes, gates, sprint milestones for the 1 backend + 1 frontend team), then [summary/02-project-plan.md](summary/02-project-plan.md) (the exact story-by-story implementation order per domain, with Depends On / Blocks / Parallelizable per story and a roadmap per domain).
- **Engineer (backend)** → [analysis/](analysis/) for your domain (`be-*` files; the domain's frontend view is right there as `fe-{domain}-breakdown.md`), then your domain's `summary/{domain}/FederatedGqlBreakDown-{domain}.md` (`## Backend` section) — its **Recommended Implementation Order** (dependency map) and **Recommended Story Graph** (your lane) sections are the build order.
- **Engineer (frontend)** → [analysis/program/fe-00-executive-summary.md](analysis/program/fe-00-executive-summary.md), stories in [analysis/program/fe-08-frontend-stories.md](analysis/program/fe-08-frontend-stories.md), order in [analysis/program/fe-10-migration-sequencing.md](analysis/program/fe-10-migration-sequencing.md); your domain's cutover lane is the **Recommended Story Graph** section of the `## Frontend` section of `summary/{domain}/FederatedGqlBreakDown-{domain}.md`.
- **Delivery (Jira / Confluence)** → import the combined per-domain CSVs from [jira/](jira/) (prompts: `fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`), publish pages from [confluence/](confluence/). Every story's description carries the sequencing metadata (Implementation Order, Owner, Priority, Depends On / Blocks by story id + name, Parallelizable, Definition of Done).
- **Ready-to-run prompts (Jira push, Confluence publish, implement-a-story, regenerate)** → [prompts/](prompts/) — copy-paste templates, one per recurring action.

## Folder map

| Folder | Content | Audience |
|---|---|---|
| [overview/](overview/) | Hand-authored high-level entry point: program overview (`00`), architecture diagrams (`01`), story/domain index (`02`) | Everyone, first stop |
| [summary/](summary/) | Program overview (`00`), team plan (`01-implementation-plan-1BE-1FE`), story-order project plan (`02-project-plan`) + per-domain breakdown folders: `{domain}/FederatedGqlBreakDown-{domain}` (merged `## Backend` + `## Frontend`), as `.md` + `.docx`; global `Federated+Graphql+Stories+-+BreakDown` at the root | PO, everyone |
| [analysis/](analysis/) | **Everything for one domain in one folder** (8 folders): backend `be-01-schema-inventory` → `be-02-resolver-analysis` → `be-03-schema-analysis` (+ `be-03-schema.graphql`) → `be-04-stories` / `be-04-po-summary` → `be-05-attribute-inventory`, plus the domain's frontend view `fe-{domain}-breakdown.md` | Engineers |
| [analysis/program/](analysis/program/) | Cross-domain frontend program docs `fe-00`–`fe-11` (numbered reading order; `fe-08` = story source of truth) + `frontend-inventory.json` (machine-readable master data) | Frontend engineers |
| [jira/](jira/) | **Combined** per-domain CSVs — `{domain}.csv` holds that domain's backend AND frontend stories (both epics); full-program files: `all-stories.csv` (backend) + `all-frontend-stories.csv` (frontend) | Delivery |
| [confluence/](confluence/) | Confluence-ready index pages: [backend](confluence/backend-confluence-documentation.md) · [frontend](confluence/frontend-confluence-documentation.md) | Delivery, everyone |
| [complexStories/](complexStories/) | Scenario deep-dives (saga writes, partner drop/undrop, rollups, techpack, …) — one folder per scenario, see its [README](complexStories/README.md) | Architects, engineers |
| [prompts/](prompts/) | Copy-paste prompt templates: `jira/` (push stories), `confluence/` (publish pages), `implement/` (one per phase A–H, with required Spock test instructions), `scripts/` (regenerate artifacts) — see its [README](prompts/README.md) | Everyone |

## Conventions

- Story ids: backend `<TOKEN>-BE-<phase>-<NN>`, frontend `<TOKEN>-FE-<NNN>`; tokens: PRODUCT, BOM, CLAIM, MST, PDTL, PKG, WATCHLIST, IMPRESSION.
- **Grouped XS stories:** logically-related XS stories (same phase + type + dependencies) are merged into one story at generation time (`MERGE_XS` in `generate_breakdown.py`); the surviving id absorbs the others (e.g. `CLAIM-BE-B-02` combines former `B-03`, `B-04`, `B-05`) and every generated reference follows the survivor. `be-04-stories.md` still lists the originals.
- **Story sequencing metadata:** every Jira story description carries Implementation Order, Domain, Team, Owner (BE-1/BE-2/FE-1/FE-2 per the team plan's domain ownership), Priority, Depends On / Blocks (story ids + names, never order numbers), Parallelizable, and a Definition of Done.
- Platform enablement (former Wave 0) is **complete** — frontend waves run 1–4 (see [analysis/program/fe-10-migration-sequencing.md](analysis/program/fe-10-migration-sequencing.md)).
- A frontend story is Done only after every backend story it depends on has been delivered.

## Regeneration

- Everything (backend + frontend docs, Jira CSVs, team plan `01`, project plan `02`): `python fedMigrationScripts/generatescripts/generate_all.py`.
- Frontend only (fe-00–04, 09–11, Jira CSVs, FE breakdown pages, frontend Confluence page): `python fedMigrationScripts/generatescripts/generate_frontend.py`.
- Plans only: `generate_team_plan.py` (01) · `generate_project_plan.py` (02).
- Hand-authored (never overwritten): frontend `05`–`08` (`fe-08-frontend-stories.md` is the parsed source of truth) and the backend Confluence page.
