# Output — Federated GraphQL Migration Deliverables

> Start here. One-page map of everything under `output/`, by audience.

## Start here, by role

- **Product Owner / Stakeholder** → [summary/00-program-overview.md](summary/00-program-overview.md), then the per-domain breakdown pages in [summary/](summary/) (`.docx` twins for sharing).
- **Engineer (backend)** → [analysis/](analysis/) for your domain (`be-*` files; the domain's frontend view is right there as `fe-{domain}-breakdown.md`), then your domain's `FederatedGqlBrakDown-BE-*.md` in [summary/](summary/).
- **Engineer (frontend)** → [analysis/program/fe-00-executive-summary.md](analysis/program/fe-00-executive-summary.md), stories in [analysis/program/fe-08-frontend-stories.md](analysis/program/fe-08-frontend-stories.md), order in [analysis/program/fe-10-migration-sequencing.md](analysis/program/fe-10-migration-sequencing.md).
- **Delivery (Jira / Confluence)** → import the combined per-domain CSVs from [jira/](jira/) (prompts: `fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`), publish pages from [confluence/](confluence/).

## Folder map

| Folder | Content | Audience |
|---|---|---|
| [summary/](summary/) | Program overview + per-domain breakdown pages: `FederatedGqlBrakDown-BE-{domain}` (backend) and `FederatedGqlBrakDown-FE-{domain}` (frontend), each as `.md` + `.docx`; global `Federated+Graphql+Stories+-+BreakDown` | PO, everyone |
| [analysis/](analysis/) | **Everything for one domain in one folder** (8 folders): backend `be-01-schema-inventory` → `be-02-resolver-analysis` → `be-03-schema-analysis` (+ `be-03-schema.graphql`) → `be-04-stories` / `be-04-po-summary` → `be-05-attribute-inventory`, plus the domain's frontend view `fe-{domain}-breakdown.md` | Engineers |
| [analysis/program/](analysis/program/) | Cross-domain frontend program docs `fe-00`–`fe-11` (numbered reading order; `fe-08` = story source of truth) + `frontend-inventory.json` (machine-readable master data) | Frontend engineers |
| [jira/](jira/) | **Combined** per-domain CSVs — `{domain}.csv` holds that domain's backend AND frontend stories (both epics); full-program files: `all-stories.csv` (backend) + `all-frontend-stories.csv` (frontend) | Delivery |
| [confluence/](confluence/) | Confluence-ready index pages: [backend](confluence/backend-confluence-documentation.md) · [frontend](confluence/frontend-confluence-documentation.md) | Delivery, everyone |
| [complexStories/](complexStories/) | Scenario deep-dives (saga writes, partner drop/undrop, rollups, techpack, …) — one folder per scenario, see its [README](complexStories/README.md) | Architects, engineers |

## Conventions

- Story ids: backend `<TOKEN>-BE-<phase>-<NN>`, frontend `<TOKEN>-FE-<NNN>`; tokens: PRODUCT, BOM, CLAIM, MST, PDTL, PKG, WATCHLIST, IMPRESSION.
- Platform enablement (former Wave 0) is **complete** — frontend waves run 1–4 (see [analysis/program/fe-10-migration-sequencing.md](analysis/program/fe-10-migration-sequencing.md)).
- A frontend story is Done only after every backend story it depends on has been delivered.

## Regeneration

- Backend docs + summary pages: `python fedMigrationScripts/generatescripts/generate_all.py` (run from inside `generatescripts/`).
- Frontend docs (00–04, 09–11, Jira CSVs, FE breakdown pages, frontend Confluence page): `python fedMigrationScripts/generatescripts/generate_frontend.py`.
- Hand-authored (never overwritten): frontend `05`–`08` (`fe-08-frontend-stories.md` is the parsed source of truth) and the backend Confluence page.
