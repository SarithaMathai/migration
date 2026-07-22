# Prompt — Push a specific LIST of stories to Jira

> **Use when:** you want a hand-picked subset — not a whole domain, not just one story. E.g. "just the
> stories in this sprint," or "just the stories one complex-case ADR unblocked."
> **Prerequisite:** a Jira MCP server connected. Confirm with: *"List the Jira tools you currently
> have."*
> **Background reading:** [`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).
> **Content model:** the Jira description is Acceptance Criteria + a back-link, nothing else — full
> story detail stays on GitHub, linked not duplicated.

---

## Step 1 — dry run (no writes)

Replace `<PROJECT_KEY>`, `<GITHUB_ORG>/<GITHUB_REPO>`, and the story-id list.

```
Using the Jira tools, prepare (DO NOT CREATE YET) an import plan for exactly these story ids:

<STORY_ID_1>, <STORY_ID_2>, <STORY_ID_3>, ...

For each id:
1. Find its row — search finalArtifacts/jira/{domain}.csv across all 8 domains (product, bom, claims,
   measurement, impression, productDetails, packaging, watchlist) for a matching Story ID; if not
   found there, check output/complexStories/*/*.csv, then
   output/analysis/out-of-scope-backlog.md §"Excluded from Jira" (deliberately not imported — a
   different team owns it). Tell me which file (or exclusion) each id came from.
2. Search Jira project <PROJECT_KEY> for an existing issue carrying that Story ID — if found, plan
   an UPDATE; if not, plan a CREATE.
3. Find-or-create the epic named in the row's "Epic Link" column (reuse if it already exists from
   an earlier import).

Rules:
- The Description column is ALREADY minimal (Acceptance Criteria + a "Full story:" back-link) — pass
  it through as-is; do NOT add Current Behaviour, Target, or Test Cases from be-04-stories.md.
- REWRITE each id's "Full story:" line into a real URL:
  "Full story: https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/output/analysis/<domain>/be-04-stories.md#<id>"
  (derive <domain> from which CSV the row came from).
- ADD "Domain overview: <URL>" per id if finalArtifacts/jira/confluence-page-map.csv has a row for
  that id's domain; otherwise skip and tell me.
- FORMATTING: preserve the numbered Acceptance Criteria list and paragraph breaks, converting to this
  Jira's format — never flatten or strip it.
- For each id's "Depends On" list: if the target is also in THIS list, note the link to create
  after both exist. If the target is outside this list, search Jira for it by [bracket] id first
  (it may already exist from an earlier push); if not found, list as pending.

Output a table: Story ID | source file | create-or-update | epic | depends-on (in-list / found-in-
jira / pending). Then STOP and wait for my approval.
```

## Step 2 — create/update, then link

```
Looks good. Now create the new issues and update the existing ones per the plan, build a Story ID →
Jira key map for everything in this batch (including any matched-existing issues), create the
in-list dependency links, attempt the "found-in-jira" links, and report: the key map, links created,
and anything still pending.
```

---
*Jira prompt — specific story list · output/prompts/jira/push-specific-stories.md*
