---
mode: agent
model: Claude Sonnet 4.5
description: "Publish one domain's FE-Readiness dependency graph (mermaid, one diagram per FE story) to Confluence"
---

Publish `finalArtifacts/summary/${input:domain:bom}/story-dependency-graph-${input:domain:bom}.md`
as a Confluence page.

Follow the full rules in `output/prompts/confluence/publish-dependency-graph-claude-sonnet.md` — this
prompt is the short form; read that file for the complete formatting contract if anything here is
ambiguous, especially the mermaid-preservation rules.

Target: parent page `${input:parentPage:Federation Graph Migration ▸ Domains}` — the SAME parent as
that domain's breakdown page, so this becomes its sibling. Title:
`${input:domainDisplayName:BOM} — FE Readiness`.

1. Dry run: this file is a series of `### <FE-STORY-ID> · <title>` headings, each followed by one
   mermaid block. Report the heading count and confirm it equals the mermaid-block count. STOP for
   my approval.
2. Publish (create-or-update by exact title). Every heading and every mermaid diagram preserved
   verbatim, in source order — none dropped, none merged, none simplified. Each mermaid block becomes
   a live diagram if your Confluence has a renderer, otherwise a code macro carrying the full,
   unmodified diagram source (never a prose description of it).
3. Verify: re-open the page, confirm the H3 section count equals the mermaid count and matches the
   source; spot-check 2 diagrams for identical nodes/edges/labels against the source.
4. Update the existing row for this domain in `finalArtifacts/jira/confluence-page-map.csv` (fill in
   its FE Readiness Page URL column) — create the row if the breakdown page hasn't been published yet.

Report the page URL and version number.
