# Example — Create or update ONE story in Jira

> Worked example of [`output/prompts/jira/push-one-story.md`](../../jira/push-one-story.md) using
> real data. Values used: `<STORY_ID>` = `WATCHLIST-BE-B-01`, `<DOMAIN>` = `watchlist`,
> `<PROJECT_KEY>` = `PROJ`, `target-corp/saritha-mathai-repositories-research` = `target-corp/saritha-mathai-repositories-research`. This shows the
> CREATE path (issue doesn't exist yet) — the smallest, simplest real story in the CSV.

---

## Prompt (filled in)

```
Using the Jira tools:

1. Open finalArtifacts/jira/watchlist.csv and find the row where Story ID = WATCHLIST-BE-B-01. If it
   isn't in that file, also check output/complexStories/*/*.csv (complex-case sub-tasks) and
   output/analysis/out-of-scope-backlog.md §"Excluded from Jira" (it may be deliberately excluded —
   different team owns the work) and tell me which applies.

2. Search Jira project PROJ for an existing issue carrying this Story ID (in its summary or
   description, e.g. "[WATCHLIST-BE-B-01]", or a custom field/label if this project has one).

3a. If it EXISTS: show me a diff — current Jira field values vs the CSV row's values (Summary,
    Description, all Labels, Phase, T-shirt size, Depends On) — and STOP for my approval before
    updating anything.

3b. If it does NOT exist: show me the fields you'd set (Issue Type, Summary, Description, Epic
    Link — find-or-create the epic named in the row's "Epic Link" column, Labels, Phase label,
    T-shirt-size label) and STOP for my approval before creating.

Rules:
- The Description column is ALREADY minimal (Acceptance Criteria + a "Full story:" back-link) — pass
  it through as-is. Do NOT enrich it with Current Behaviour, Target implementation, or Test Cases from
  be-04-stories.md; that content stays on GitHub, linked not duplicated.
- REWRITE the "Full story:" line into a real URL:
  "Full story: https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/watchlist/be-04-stories.md#WATCHLIST-BE-B-01"
- ADD "Domain overview: <URL>" if finalArtifacts/jira/confluence-page-map.csv has a row for
  watchlist; otherwise skip and tell me Confluence hasn't been published for this domain yet.
- FORMATTING: preserve the numbered Acceptance Criteria list and paragraph breaks — convert markup to
  this Jira's format, don't strip or flatten it.
- If the row's "Depends On" names another story, search for that story's existing Jira key too
  (same [bracket] search) and propose the link; if not found, note it as pending.

After my approval, make the change and report the Jira key + URL.
```

## Sample agent response

```
Found WATCHLIST-BE-B-01 in finalArtifacts/jira/watchlist.csv, row 2 (backend block).

Searched Jira project PROJ for an issue carrying "WATCHLIST-BE-B-01" — none found. This is a CREATE.

Depends On column is empty for this row — no dependency link to propose.

Proposed fields:
- Issue Type: Story
- Summary: (Watchlist) getWatchlistByIds(ids) [WATCHLIST-BE-B-01]
- Epic Link: "Federate BreakDown Product" (searching Jira... found as PROJ-401, will attach directly)
- Labels: dgs-migration, watchlist, query, size-XS, phase-B
- Description:
  ---
  *Acceptance Criteria:*
  1. returns entries for ids; empty → []

  Full story: https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/watchlist/be-04-stories.md#WATCHLIST-BE-B-01
  Domain overview: https://confluence.com/Breakdown/Watchlist-Federated-GraphQL-Breakdown
  ---
  (found a row for watchlist in confluence-page-map.csv, added the Domain overview line)

STOP — waiting for your approval before creating.
```

**After approval:**

```
Created WATCHLIST-BE-B-01 as PROJ-403 (https://your-instance.atlassian.net/browse/PROJ-403), attached
to epic PROJ-401.
```

---
*Worked example · output/prompts/example/jira/push-one-story.example.md*
