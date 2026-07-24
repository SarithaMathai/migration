# Prompt — Push ALL stories for one domain to Jira

> **Use when:** you want every backend + frontend story for one domain created (or updated) in Jira in
> one pass. Fill in `<DOMAIN>`, `<PROJECT_KEY>`, and `target-corp/saritha-mathai-repositories-research`, run the dry-run
> prompt first, review its output table, then run the second prompt to actually create/update and link
> dependencies.
> **Prerequisite:** a Jira MCP server connected (Atlassian MCP, your enterprise custom MCP, or
> Copilot's own Jira tools). Confirm with: *"List the Jira tools you currently have."*
> **Background reading (rules this prompt assumes):** [`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).
> **Content model:** the Jira description is Acceptance Criteria + a back-link, nothing else — full
> story detail (Current Behaviour, Target, Test Cases) stays on GitHub in `be-04-stories.md` and is
> linked to, never copied in. See the runbook above for why.

---

## Step 1 — dry run (no writes)

Replace `<DOMAIN>` with one of: `product, bom, claims, measurement, impression, productDetails,
packaging, watchlist`. Replace `<PROJECT_KEY>` and `target-corp/saritha-mathai-repositories-research`.

```
Using the Jira tools, prepare (DO NOT CREATE YET) an import plan from
finalArtifacts/jira/<DOMAIN>.csv into Jira project <PROJECT_KEY>.

This CSV holds ONE domain, in two blocks:
- backend stories (Story IDs like <TOKEN>-BE-B-01) under the epic "Federate BreakDown Product";
- frontend stories (Story IDs like <TOKEN>-FE-001) under the epic
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
  pulled from be-04-stories.md; that stays on GitHub, linked not duplicated.
- REWRITE the "Full story:" line from a relative path into a real URL:
  "Full story: https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/<DOMAIN>/be-04-stories.md#<Story ID>"
- ADD a second link line if finalArtifacts/jira/confluence-page-map.csv has a row for <DOMAIN>:
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

## Step 2 — create/update, then link dependencies

```
Looks good. Now:
1. Find-or-create the two Epics for <DOMAIN>, then create NEW stories/spikes and UPDATE existing
   ones (per the plan), in Jira project <PROJECT_KEY>. Do not touch fields I didn't ask you to change
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

---
*Jira prompt — push all stories for one domain · output/prompts/jira/push-domain-all-stories.md*
