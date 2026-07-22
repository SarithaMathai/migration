---
mode: agent
model: Claude Sonnet 4.5
description: "Publish the program-wide overview page (what/why, totals, domain-at-a-glance) to Confluence"
---

Publish `finalArtifacts/00-overview.md` as a single Confluence page — ONE page, not per-domain.

Follow the full rules in `output/prompts/confluence/publish-program-overview-claude-sonnet.md` — this
prompt is the short form; read that file for the complete formatting contract if anything here is
ambiguous.

Target: parent page `${input:parentPage:Federation Graph Migration}`, title
`Spark → Federated GraphQL Migration — Program Overview`.

1. Dry run: report a section manifest (table count, heading count). STOP for my approval.
2. Publish (create-or-update by exact title, never duplicate). Every table, heading level, and
   status icon (🔴🟠🟡🟢) preserved verbatim. Rewrite relative repo links as GitHub links
   (`https://github.com/${input:githubOrgRepo:<GITHUB_ORG>/<GITHUB_REPO>}/blob/main/<path>`) or, if
   the target page already exists in Confluence (check `finalArtifacts/jira/confluence-page-map.csv`),
   link to the live page instead.
3. Verify: re-open the page, confirm table/heading counts match the source.

Report the page URL and version number.
