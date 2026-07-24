# Example — Push one PHASE of one domain to Jira

> Worked example of [`output/prompts/jira/push-domain-phase.md`](../../jira/push-domain-phase.md)
> using real data. Values used: `<DOMAIN>` = `watchlist`, `<PHASE>` = `G` (field resolvers — the
> phase with the most rows for this small domain, 4 stories, good for showing a mid-size batch),
> `<PROJECT_KEY>` = `PROJ`, `target-corp/saritha-mathai-repositories-research` = `target-corp/saritha-mathai-repositories-research`.

---

## Step 1 — dry run (filled in)

```
Using the Jira tools, prepare (DO NOT CREATE YET) an import plan for Phase G of the
watchlist domain only, from finalArtifacts/jira/watchlist.csv.

Filter: only rows where the "Phase" column = G (backend rows use the letter directly, e.g.
"E"; there is no frontend-specific phase letter — frontend rows are Phase="FE" and are OUT of scope
for this prompt unless <PHASE> is literally "FE"). If Phase G has zero rows for this domain,
tell me that and stop rather than silently proceeding with an empty plan.

For EACH matching row, before you plan a create, check whether a Jira issue already exists carrying
that Story ID (search summary/description for the id in [brackets], or a custom field/label if your
project has one). If it exists: plan an UPDATE, not a duplicate create. If it doesn't: plan a create.

Rules:
- Attach every Story to the epic named in ITS OWN "Epic Link" column ("Federate BreakDown Product"
  for backend rows — this epic is shared across ALL domains, so also apply the domain label from the
  row's Labels column; do not create a per-domain epic).
- Map fields: Summary→summary, Description→description, T-shirt size→label "size-XS" (etc.), the
  three Labels columns→labels, Phase→label "phase-G".
- The Description column is ALREADY minimal (Acceptance Criteria + a "Full story:" back-link) — pass
  it through as-is. Do NOT pull in Current Behaviour, Target implementation, or Test Cases from
  be-04-stories.md; that content stays on GitHub, linked not duplicated.
- REWRITE the "Full story:" line into a real URL:
  "Full story: https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/watchlist/be-04-stories.md#<Story ID>"
- ADD "Domain overview: <URL>" if finalArtifacts/jira/confluence-page-map.csv has a row for
  watchlist; otherwise skip and tell me.
- FORMATTING: preserve the numbered Acceptance Criteria list and paragraph breaks, converting to this
  Jira's description format — never flatten, strip, or reword.
- This phase's stories may depend on an EARLIER phase in the SAME domain that hasn't been pushed yet
  (e.g. a Phase E story's "Depends On" naming a Phase B story). Check each "Depends On" id against
  this batch first; if it's not in this batch, search Jira for it (already-pushed earlier phase); if
  not found there either, list it as "pending — push Phase <earlier-letter> first."

Output a table: Story ID | create-or-update | epic | labels | depends-on (in-batch / found-in-jira /
pending-earlier-phase). Then STOP and wait for my approval.
```

## Sample agent response

```
Found 4 rows with Phase=G in finalArtifacts/jira/watchlist.csv: WATCHLIST-BE-G-01, G-02, G-03, G-05.

Searched Jira project PROJ — no existing issues found for any of these 4 ids. All plan as creates.

| Story ID | create/update | epic | labels | depends-on |
|---|---|---|---|---|
| WATCHLIST-BE-G-01 | create | Federate BreakDown Product | dgs-migration, watchlist, field-resolver, size-S, phase-G | B-01 (found-in-jira: PROJ-403, already pushed) |
| WATCHLIST-BE-G-02 | create | Federate BreakDown Product | dgs-migration, watchlist, field-resolver, size-M, phase-G | B-01 (found-in-jira: PROJ-403) |
| WATCHLIST-BE-G-03 | create | Federate BreakDown Product | dgs-migration, watchlist, field-resolver, size-S, phase-G | B-01 (found-in-jira: PROJ-403) |
| WATCHLIST-BE-G-05 | create | Federate BreakDown Product | dgs-migration, watchlist, field-resolver, size-S, phase-G | G-02 (in-batch) |

All 4 will get the GitHub back-link. finalArtifacts/jira/confluence-page-map.csv has a row for
watchlist, so all 4 also get the "Domain overview" link.

STOP — waiting for your approval before creating anything.
```

## Step 2 — create/update, then link dependencies (filled in)

```
Looks good. Now:
1. Create the new stories/spikes and update the existing ones per the plan, in Jira project
   PROJ. Do not touch fields I didn't ask you to change on an existing issue.
2. Keep a map of Story ID → Jira key (created or matched-existing) for this batch.
3. For each row's "Depends On" ids: link in-batch ones directly; for found-in-jira ones, create the
   link (Blocks / is blocked by — the dependency is the blocker); leave pending-earlier-phase ones
   unlinked and listed for follow-up.
4. Report: Story ID → Jira key table, links created, and anything still pending (with which earlier
   phase unblocks it).
```

## Sample agent response

```
Created 4 issues:

| Story ID | Jira key |
|---|---|
| WATCHLIST-BE-G-01 | PROJ-412 |
| WATCHLIST-BE-G-02 | PROJ-413 |
| WATCHLIST-BE-G-03 | PROJ-414 |
| WATCHLIST-BE-G-05 | PROJ-415 |

Links created (4): PROJ-403 (WATCHLIST-BE-B-01, already in Jira) blocks PROJ-412, PROJ-413, and
PROJ-414; PROJ-413 (WATCHLIST-BE-G-02) blocks PROJ-415 (in-batch link).

Nothing pending — all dependencies for this phase resolved (Phase B was already pushed).
```

---
*Worked example · output/prompts/example/jira/push-domain-phase.example.md*
