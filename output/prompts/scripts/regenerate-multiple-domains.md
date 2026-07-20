# Prompt — Regenerate artifacts for multiple domains (or the whole program)

> **Use when:** you changed something that spans domains — a cross-domain `Blocked by:`/`Depends on:`
> field, a shared complex-case ADR, a generator script itself (e.g. `team_config.py`,
> `generate_breakdown.py`) — or you just want to be sure everything is current before a review/commit.

---

## Prompt A — a named subset of domains

Replace `<DOMAIN_LIST>` with a space-separated list, e.g. `bom claims measurement`.

```
Run the regeneration pipeline for exactly these domains: <DOMAIN_LIST>

1. From the migration repo root, run:
   python fedMigrationScripts/generatescripts/generate_all.py <DOMAIN_LIST>

2. Confirm every domain's steps printed OK, not FAIL. Show me any failure before proceeding.

3. Note: naming specific domains (as opposed to no arguments) skips the PROGRAM-WIDE roll-ups
   (00-program-overview.md, cross-domain-dependencies.md, all-stories.csv, the team/project plans).
   If any of the domains you just regenerated has a cross-domain Depends-on/Blocked-by relationship
   with a domain NOT in this list, or if story counts changed, run Prompt B below afterward so the
   program-wide files reconcile with what you just changed.

Report what changed per domain, and flag anything that failed.
```

## Prompt B — the whole program (every domain + all program-wide roll-ups)

```
Run the FULL regeneration pipeline (all 8 domains + every program-wide roll-up):

1. From the migration repo root, run:
   python fedMigrationScripts/generatescripts/generate_all.py

2. Confirm every domain's steps printed OK. Then confirm these program-wide artifacts were also
   regenerated (their generation is only wired into the no-argument, full-program run):
   - output/summary/00-program-overview.md
   - output/summary/01-implementation-plan-1BE-1FE.md + 02-project-plan.md
   - output/analysis/program/cross-domain-dependencies.md
   - output/jira/all-stories.csv + all-frontend-stories.csv
   - every output/complexStories/<case>/<case>.csv

3. Cross-check: output/summary/00-program-overview.md's "Program totals" table should reconcile with
   a live count from output/jira/all-stories.csv (Story rows only) — if you want, verify with:
   python3 -c "import csv; rows=list(csv.DictReader(open('output/jira/all-stories.csv',encoding='utf-8')));
   print(sum(1 for r in rows if r['Issue Type']=='Story'))"
   and confirm it matches the "Total backend stories" figure in the program overview.

4. If this run follows a batch of source edits across several domains (e.g. a staleness-fix pass),
   also grep the regenerated output for anything that still looks stale (an id or phase letter that
   should have changed but didn't) before considering the run complete.

Report: OK/FAIL per domain and per program-wide step, plus the reconciliation check result.
```

---
*Scripts prompt — regenerate multiple domains / full program · output/prompts/scripts/regenerate-multiple-domains.md*
