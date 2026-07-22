# Example — Push ALL stories for one domain to Jira

> Worked example of [`output/prompts/jira/push-domain-all-stories.md`](../../jira/push-domain-all-stories.md)
> using real data. Values used throughout: `<DOMAIN>` = `watchlist`, `<PROJECT_KEY>` = `PROJ`,
> `<GITHUB_ORG>/<GITHUB_REPO>` = `myorg/spark-migration`. Watchlist is the smallest domain (16 rows:
> 13 backend + 3 frontend), so the full dry-run table fits without truncation.

---

## Step 1 — dry run (filled in)

```
Using the Jira tools, prepare (DO NOT CREATE YET) an import plan from
finalArtifacts/jira/watchlist.csv into Jira project PROJ.

This CSV holds ONE domain, in two blocks:
- backend stories (Story IDs like WATCHLIST-BE-B-01) under the epic "Federate BreakDown Product";
- frontend stories (Story IDs like WATCHLIST-FE-001) under the epic
  "Federate BreakDown Product — Frontend".

For EACH row, before you plan a create, check whether a Jira issue already exists carrying that
Story ID (search summary/description for the id in [brackets], or a custom field/label if your
project has one). If it exists: plan an UPDATE (new description/fields), not a duplicate create.
If it doesn't: plan a create.

Rules:
- The CSV contains TWO Issue Type=Epic rows (backend + frontend). Reuse an existing epic with that
  exact Summary if one exists; otherwise plan to create it.
- Each Issue Type=Story row → a Story; each Issue Type=Spike row → a Spike (or a Story labelled
  "spike" if Spike isn't an available issue type — tell me which).
- Attach every Story to the epic named in ITS OWN "Epic Link" column.
- Map fields: Summary→summary, Description→description, T-shirt size→label "size-XS" (etc.),
  the three Labels columns→labels, Phase→label "phase-B" (frontend rows: Phase=FE → "phase-FE").
- The Description column is ALREADY minimal (Acceptance Criteria + a "Full story:" back-link) — pass
  it through as-is. Do NOT enrich it with Current Behaviour, Target implementation, or Test Cases
  pulled from be-04-stories.md; that content stays on GitHub, linked not duplicated.
- REWRITE the "Full story:" line into a real URL:
  "Full story: https://github.com/myorg/spark-migration/blob/main/output/analysis/watchlist/be-04-stories.md#<Story ID>"
- ADD a second link line if finalArtifacts/jira/confluence-page-map.csv has a row for watchlist:
  "Domain overview: <that row's Breakdown Page URL>". If the map file or the row doesn't exist yet,
  skip this line and tell me Confluence hasn't been published for this domain.
- FORMATTING: the Description's numbered Acceptance Criteria list must stay a numbered list —
  preserve paragraph breaks and convert markup to this Jira's description format. Do NOT collapse to
  one line, strip numbering, reword, or summarize anything.
- The "Depends On" column lists other Story IDs. Don't resolve them to Jira keys yet — flag
  cross-domain ones (targets not in this CSV) separately; we link everything in step 2.

Output a table: Story ID | create-or-update | proposed issue type | epic | summary | labels |
depends-on | confluence-link-added(y/n). Then STOP and wait for my approval.
```

## Sample agent response

```
I've read finalArtifacts/jira/watchlist.csv (16 rows: 2 epics, 13 backend stories, 3 frontend
stories). I checked Jira project PROJ and found no existing issues labeled with any of these Story
IDs — this looks like a first import for this domain.

finalArtifacts/jira/confluence-page-map.csv exists with a row for watchlist, so I've added the
Confluence link to every row below.

| Story ID | create/update | type | epic | summary | labels | depends-on | confluence-link |
|---|---|---|---|---|---|---|---|
| WATCHLIST-BE-B-01 | create | Story | Federate BreakDown Product | (Watchlist) getWatchlistByIds(ids) | dgs-migration, watchlist, query, size-XS, phase-B | — | y |
| WATCHLIST-BE-B-02 | create | Story | Federate BreakDown Product | (Watchlist) getWatchlistReasons (cacheable) | dgs-migration, watchlist, query, size-XS, phase-B | B-01 | y |
| WATCHLIST-BE-B-03 | create | Story | Federate BreakDown Product | (Watchlist) getWatchlistInspectionActions (cacheable) | dgs-migration, watchlist, query, size-XS, phase-B | B-01 | y |
| WATCHLIST-BE-C-01 | create | Story | Federate BreakDown Product | (Watchlist) getWatchlistByFilter(...) (4-step read) | dgs-migration, watchlist, search, size-M, phase-C | B-01 | y |
| WATCHLIST-BE-D-01 | create | Story | Federate BreakDown Product | (Watchlist) createWatchlistEntries | dgs-migration, watchlist, mutation, size-S, phase-D | B-01 | y |
| WATCHLIST-BE-D-02 | create | Story | Federate BreakDown Product | (Watchlist) cloneFilesForWatchlist | dgs-migration, watchlist, mutation, size-S, phase-D | B-01 | y |
| WATCHLIST-BE-E-01 | create | Story | Federate BreakDown Product | (Watchlist) updateWatchlistEntries (multi-step write) | dgs-migration, watchlist, complex, size-L, phase-E | SPIKE-01, B-01, PRODUCT-BE-E-00 (cross-domain) | y |
| WATCHLIST-BE-F-01 | create | Story | Federate BreakDown Product | (Watchlist) Product.watchlists (internal) | dgs-migration, watchlist, field-resolver, size-XS, phase-F | B-01 | y |
| WATCHLIST-BE-F-02 | create | Story | Federate BreakDown Product | (Watchlist) ResourcesCount.watchlists (internal — TechPack) | dgs-migration, watchlist, field-resolver, size-XS, phase-F | B-01 | y |
| WATCHLIST-BE-G-01 | create | Story | Federate BreakDown Product | (Watchlist) Computed flatteners | dgs-migration, watchlist, field-resolver, size-S, phase-G | B-01 | y |
| WATCHLIST-BE-G-02 | create | Story | Federate BreakDown Product | (Watchlist) createdBy + updatedBy + workspaces + participantDetails + partnerName | dgs-migration, watchlist, field-resolver, size-M, phase-G | B-01 | y |
| WATCHLIST-BE-G-03 | create | Story | Federate BreakDown Product | (Watchlist) attachments + product | dgs-migration, watchlist, field-resolver, size-S, phase-G | B-01 | y |
| WATCHLIST-BE-G-05 | create | Story | Federate BreakDown Product | (Watchlist) WatchlistPartner.partner entity reference (recommended) | dgs-migration, watchlist, field-resolver, size-S, phase-G | G-02 | y |
| WATCHLIST-FE-001 | create | Story | Federate BreakDown Product — Frontend | [Watchlist FE] Migrate watchlist reads | dgs-migration-fe, watchlist, query-migration, size-M | B-01, C-01, G-01, G-02, G-03, G-05 | y |
| WATCHLIST-FE-002 | create | Story | Federate BreakDown Product — Frontend | [Watchlist FE] Migrate watchlist create and clone mutations | dgs-migration-fe, watchlist, mutation-migration, size-S | D-01, D-02 | y |
| WATCHLIST-FE-003 | create | Story | Federate BreakDown Product — Frontend | [Watchlist FE] Migrate `updateWatchlistEntries` saga handling | dgs-migration-fe, watchlist, mutation-migration, size-M | E-01 | y |

Notes:
- WATCHLIST-BE-E-01 depends on SPIKE-01 (a program spike, not a story — I'll flag it as a gate rather
  than a normal link) and on PRODUCT-BE-E-00, which is cross-domain (not in this CSV) — I'll search
  for it by [bracket] id in step 2.
- All 16 rows will get the GitHub back-link and the Confluence "Domain overview" link.

STOP — waiting for your approval before creating anything.
```

## Step 2 — create/update, then link dependencies (filled in)

```
Looks good. Now:
1. Find-or-create the two Epics for watchlist, then create NEW stories/spikes and UPDATE existing
   ones (per the plan), in Jira project PROJ. Do not touch fields I didn't ask you to change
   on an existing issue beyond what the plan specified.
2. Keep a map of Story ID → Jira key (created or matched-existing).
3. For each row's "Depends On" ids, create a Jira issue link (Blocks / is blocked by; blocker =
   the dependency) using that map.
4. If a "Depends On" id is NOT in this CSV (cross-domain dependency), search Jira for an issue
   whose summary/description contains that id in [brackets]. Link it if found; if not found, list
   it under "pending links — import that domain, then rerun step 4."
5. Report: Story ID → Jira key table, links created, GitHub/Confluence links added, and any pending
   links.
```

## Sample agent response

```
Created epic "Federate BreakDown Product" as PROJ-401 and "Federate BreakDown Product — Frontend"
as PROJ-402. Created 16 issues:

| Story ID | Jira key |
|---|---|
| WATCHLIST-BE-B-01 | PROJ-403 |
| WATCHLIST-BE-B-02 | PROJ-404 |
| WATCHLIST-BE-B-03 | PROJ-405 |
| WATCHLIST-BE-C-01 | PROJ-406 |
| WATCHLIST-BE-D-01 | PROJ-407 |
| WATCHLIST-BE-D-02 | PROJ-408 |
| WATCHLIST-BE-E-01 | PROJ-409 |
| WATCHLIST-BE-F-01 | PROJ-410 |
| WATCHLIST-BE-F-02 | PROJ-411 |
| WATCHLIST-BE-G-01 | PROJ-412 |
| WATCHLIST-BE-G-02 | PROJ-413 |
| WATCHLIST-BE-G-03 | PROJ-414 |
| WATCHLIST-BE-G-05 | PROJ-415 |
| WATCHLIST-FE-001 | PROJ-416 |
| WATCHLIST-FE-002 | PROJ-417 |
| WATCHLIST-FE-003 | PROJ-418 |

Links created (12): PROJ-403 blocks PROJ-404/405/406/407/408/410/411/412/413/414;
PROJ-413 blocks PROJ-415; PROJ-407+408 block PROJ-417; PROJ-406+412+413+414+415 block PROJ-416;
PROJ-409 blocks PROJ-418.

GitHub links added to all 16 descriptions (blob URL to be-04-stories.md#<id>). Confluence "Domain
overview" link added to all 16 (found a row for watchlist in confluence-page-map.csv →
https://confluence.com/Breakdown/Watchlist-Federated-GraphQL-Breakdown).

Pending links (1): WATCHLIST-BE-E-01 (PROJ-409) depends on PRODUCT-BE-E-00 — no Jira issue found
with that id in [brackets]. The product domain hasn't been imported yet. Re-run step 4 after
importing product.
```

---
*Worked example · output/prompts/example/jira/push-domain-all-stories.example.md*
