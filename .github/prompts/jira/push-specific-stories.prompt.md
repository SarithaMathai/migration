---
mode: agent
model: Claude Sonnet 4.5
description: "Push a hand-picked list of story ids (any domain mix) to Jira"
---

Import exactly these story ids into Jira project `${input:projectKey:ENG}`:
**${input:storyIds:PRODUCT-BE-D-01, BOM-BE-B-01}**

Follow the full rules in `output/prompts/jira/push-specific-stories.md` — this prompt is the short
form.

**Content model:** Description = numbered Acceptance Criteria + a `Full story:` back-link only —
never enrich it with Current Behaviour/Target/Test Cases from `be-04-stories.md`.

1. Dry run: for each id, find its row across `finalArtifacts/jira/{domain}.csv` (all 8 phase-1
   domains), or `output/complexStories/*/*.csv`, or flag it as excluded per
   `output/analysis/out-of-scope-backlog.md` §"Excluded from Jira". Plan create-or-update. Rewrite
   each `Full story:` line into a GitHub URL
   (`https://github.com/${input:githubOrgRepo:<GITHUB_ORG>/<GITHUB_REPO>}/blob/main/output/analysis/<domain>/be-04-stories.md#<id>`)
   and add a `Domain overview:` link where `finalArtifacts/jira/confluence-page-map.csv` has a row
   for that domain. Output a table: Story ID | source file | create-or-update | epic | depends-on.
   STOP for my approval.
2. After approval: create/update, build the Story ID → Jira key map, create in-list links, attempt
   found-in-Jira links for out-of-list dependencies, report pending ones.
