---
mode: agent
model: Claude Sonnet 4.5
description: "Create or update a single story in Jira from its generated CSV row"
---

Create or update the Jira issue for **${input:storyId:PRODUCT-BE-D-01}** (domain
`${input:domain:product}`) in project `${input:projectKey:ENG}`.

Follow the full rules in `output/prompts/jira/push-one-story.md` — this prompt is the short form.

1. Find the row in `finalArtifacts/jira/${input:domain:product}.csv`. If absent, check
   `output/complexStories/*/*.csv` and `output/analysis/out-of-scope-backlog.md` §"Excluded from
   Jira" (it may be deliberately not imported).
2. Search Jira for an existing issue carrying this Story ID.
3. Show a diff (if updating) or the fields you'd set (if creating) — Summary, Description (numbered
   Acceptance Criteria + rewritten GitHub back-link
   `https://github.com/${input:githubOrgRepo:target-corp/saritha-mathai-repositories-research}/blob/main/output/analysis/${input:domain:product}/be-04-stories.md#${input:storyId:PRODUCT-BE-D-01}`
   + a `Domain overview:` link from `finalArtifacts/jira/confluence-page-map.csv` if present), Labels,
   Phase, T-shirt size. Do NOT add Current Behaviour/Target/Test Cases — not in scope for this ticket.
   STOP for my approval.
4. After approval: apply the change, propose the Depends-On link if the target story's Jira key is
   findable, and report the Jira key + URL.
