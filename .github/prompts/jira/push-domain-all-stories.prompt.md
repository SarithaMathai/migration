---
mode: agent
model: Claude Sonnet 4.5
description: "Push every backend + frontend story for one domain to Jira (dry-run then create/update + link)"
---

Import `finalArtifacts/jira/${input:domain:bom}.csv` (backend + frontend, two epics) into Jira project
`${input:projectKey:ENG}`.

Follow the full rules in `output/prompts/jira/push-domain-all-stories.md` and the content model in
`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md` — this prompt is the short form; read those for
the complete field-mapping and link-rewrite contract if anything here is ambiguous.

**Content model — do not violate this:** the CSV's Description column is already minimal (numbered
Acceptance Criteria + a `Full story:` back-link). Pass it through as-is; do NOT enrich it with
Current Behaviour, Target implementation, or Test Cases pulled from `be-04-stories.md` — that detail
stays on GitHub, linked not duplicated.

1. Dry run (no writes): for every row, check whether a Jira issue already carries that Story ID
   (search `[<Story ID>]` in summary/description or a label). Plan create-or-update accordingly.
   Rewrite each row's `Full story:` line into
   `https://github.com/${input:githubOrgRepo:target-corp/saritha-mathai-repositories-research}/blob/main/output/analysis/${input:domain:bom}/be-04-stories.md#<Story ID>`.
   Add a `Domain overview:` line from `finalArtifacts/jira/confluence-page-map.csv` if a row exists
   for this domain. Output a table: Story ID | create-or-update | epic | labels | depends-on |
   confluence-link-added. STOP for my approval.
2. After approval: find-or-create the two epics, create/update every Story/Spike row, build a Story
   ID → Jira key map, then create dependency links (Blocks/is-blocked-by) from the Depends On column
   — cross-domain targets not in this file get searched by `[bracket]` id; unresolved ones go on a
   pending list.
3. Report: Story ID → Jira key table, links created, GitHub/Confluence links added, pending links.
