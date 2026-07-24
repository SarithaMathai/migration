---
mode: agent
model: Claude Sonnet 4.5
description: "Push just one phase (A-H) of one domain's stories to Jira"
---

Import Phase **${input:phase:E}** of domain **${input:domain:bom}** from
`finalArtifacts/jira/${input:domain:bom}.csv` into Jira project `${input:projectKey:ENG}`.

Follow the full rules in `output/prompts/jira/push-domain-phase.md` — this prompt is the short form;
read that file's "How dependencies work" section for the same-domain-shorthand, spike, and
cross-domain dependency rules before linking anything.

**Content model:** Description = numbered Acceptance Criteria + a `Full story:` back-link only —
never enrich it with Current Behaviour/Target/Test Cases from `be-04-stories.md`.

1. Dry run: filter rows to `Phase = ${input:phase:E}` (backend letter, or `FE` for frontend). If
   zero rows, stop and say so. For each: create-or-update plan, rewrite the back-link to
   `https://github.com/${input:githubOrgRepo:target-corp/saritha-mathai-repositories-research}/blob/main/output/analysis/${input:domain:bom}/be-04-stories.md#<Story ID>`,
   add a `Domain overview:` link if `finalArtifacts/jira/confluence-page-map.csv` has this domain.
   Flag any Depends-On pointing at an earlier phase not yet pushed. STOP for my approval.
2. After approval: create/update, link in-batch and found-in-Jira dependencies, leave
   pending-earlier-phase ones for follow-up.
3. Report: Story ID → Jira key table, links created, anything pending.
