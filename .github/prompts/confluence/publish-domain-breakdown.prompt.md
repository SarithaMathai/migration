---
mode: agent
model: Claude Sonnet 4.5
description: "Publish one domain's Federated GraphQL Breakdown page to Confluence, zero data/format loss"
---

Publish `finalArtifacts/summary/${input:domain:bom}/FederatedGqlBreakDown-${input:domain:bom}.md` as
a Confluence page.

Follow the full rules in `output/prompts/confluence/publish-domain-breakdown-claude-sonnet.md`
(field mapping, dry-run manifest, GitHub-link rule, `confluence-page-map.csv` write-back) — this
prompt is the short form; read that file for the complete formatting contract if anything here is
ambiguous.

Target: parent page `${input:parentPage:Federation Graph Migration ▸ Domains}`, title
`${input:domainDisplayName:BOM} — Federated GraphQL Breakdown`.

1. Dry run: report the target title/parent and a section manifest (table count, mermaid count,
   heading count). STOP for my approval.
2. Publish (create-or-update by exact title, never duplicate). Preserve every table, heading level,
   checklist, and mermaid block verbatim — no summarizing, no flattening. Rewrite relative repo links
   as `https://github.com/${input:githubOrgRepo:target-corp/saritha-mathai-repositories-research}/blob/main/<path>`.
3. Verify: re-open the page and confirm table/heading/mermaid counts match the source.
4. Append a row to `finalArtifacts/jira/confluence-page-map.csv` (Domain, Breakdown Page URL, FE
   Readiness Page URL) with this page's URL.

Report the page URL and version number.
