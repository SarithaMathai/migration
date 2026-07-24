# Example — Update an existing story by Epic + Story ID (Jira key unknown)

> Worked example of [`output/prompts/jira/update-story-in-epic.md`](../../jira/update-story-in-epic.md)
> using real data. Values used: `<STORY_ID>` = `WATCHLIST-BE-E-01`, `<EPIC_NAME>` = `Federate
> BreakDown Product`, `<PROJECT_KEY>` = `PROJ`, `target-corp/saritha-mathai-repositories-research` = `target-corp/saritha-mathai-repositories-research`.
> Scenario: this story was imported a while ago; its Acceptance Criteria have since been reworded in
> `be-04-stories.md` (a spike note was added), and you want to refresh it without knowing its Jira key.

---

## Prompt (filled in)

```
Using the Jira tools, find and UPDATE (do not create) the Jira issue for WATCHLIST-BE-E-01.

1. Find the epic in PROJ whose name/summary is exactly "Federate BreakDown Product". If more than one
   issue matches that name, list them and ask me which one before continuing.
2. Within that epic's children ONLY (issues linked to it via Epic Link/parent), search for one whose
   summary or description contains "WATCHLIST-BE-E-01" (typically in the form "[WATCHLIST-BE-E-01]"
   per this project's summary convention, e.g. "(Watchlist) updateWatchlistEntries (multi-step write)
   [WATCHLIST-BE-E-01]").
3. If found: that is the target issue. Report its Jira key + current URL before changing anything.
4. If NOT found within that epic: STOP. Do not search other epics, do not create a new issue. Tell me
   the epic had no matching child and ask whether the story hasn't been imported yet (in which case
   use push-one-story.md to create it) or whether I have the wrong epic name.

Once the target issue is confirmed, pull the CURRENT source content for WATCHLIST-BE-E-01:
- Find its row in finalArtifacts/jira/watchlist.csv (derive <DOMAIN> from the Story ID's prefix — e.g.
  BOM-BE-E-01 → bom.csv; a FE id like BOM-FE-002 → the same domain's csv, frontend block). If the id
  isn't in that domain's CSV, also check output/complexStories/*/*.csv and
  output/analysis/out-of-scope-backlog.md §"Excluded from Jira" (may be deliberately excluded).
- Cross-check the Acceptance Criteria against output/analysis/watchlist/be-04-stories.md (search
  "### WATCHLIST-BE-E-01") — this is the fuller source; if the CSV's AC list and the .md's numbered AC
  list disagree (e.g. reworded since the CSV was last generated), the .md file wins and you should
  flag the discrepancy to me. Do NOT pull Current Behaviour/Target/Test Cases from the .md into the
  Jira description — those stay on GitHub, linked not duplicated; only the Acceptance Criteria and
  the back-link belong in the ticket.

Show me a diff: current Jira field values vs. the source content — Summary, Description (Acceptance
Criteria list + the "Full story:" link, rewritten as
"https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/watchlist/be-04-stories.md#WATCHLIST-BE-E-01",
plus "Domain overview: <URL>" if finalArtifacts/jira/confluence-page-map.csv has a row for watchlist),
Labels, Phase label, T-shirt-size label. STOP and wait for my approval before changing anything.

FORMATTING (same contract as every other Jira/Confluence prompt in this repo): preserve the numbered
Acceptance Criteria list and paragraph breaks, converted to this Jira's format — never flatten, strip,
reword, or drop any criterion.

After my approval, apply the update and report the Jira key, URL, and a short list of what changed
(e.g. "Description: 1 Acceptance Criterion reworded, GitHub link added; Labels: no change").
```

## Sample agent response

```
Found epic "Federate BreakDown Product" as PROJ-401 in project PROJ.

Searched PROJ-401's children for "WATCHLIST-BE-E-01" — found PROJ-409: "(Watchlist)
updateWatchlistEntries [WATCHLIST-BE-E-01]" (https://your-instance.atlassian.net/browse/PROJ-409).

Pulled current source: finalArtifacts/jira/watchlist.csv row for WATCHLIST-BE-E-01, cross-checked
against output/analysis/watchlist/be-04-stories.md §WATCHLIST-BE-E-01 — no discrepancy found between
the CSV's AC list and the .md's; both currently list the same 3 criteria.

Diff — current Jira vs. source:

| Field | Current (PROJ-409) | Source | Change |
|---|---|---|---|
| Summary | (Watchlist) updateWatchlistEntries (multi-step write) [WATCHLIST-BE-E-01] | same | none |
| Description | 3 AC items, no "Requires spike" line, back-link is a relative path "be-04-stories.md#WATCHLIST-BE-E-01" | 3 AC items (unchanged), NEW "Requires spike: SPIKE-01 (Non-Atomic Write Saga)" line added at top, back-link rewritten to full GitHub URL, Domain overview link added | spike line added, back-link upgraded to URL, Confluence link added |
| Labels | dgs-migration, watchlist, complex | same + size-L, phase-E (missing on the existing issue) | 2 labels added |
| T-shirt size | (not set) | L | added |

STOP — waiting for your approval before updating.
```

**After approval:**

```
Updated PROJ-409. Changed: Description (added the "Requires spike: SPIKE-01" line, rewrote the
back-link to a full GitHub URL, added a Domain overview link to Confluence); Labels (added size-L,
phase-E). Acceptance Criteria text itself: unchanged (already current).
```

---
*Worked example · output/prompts/example/jira/update-story-in-epic.example.md*
