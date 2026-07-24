# Example — Publish one domain's FE-Readiness dependency graph to Confluence

> Worked example of [`output/prompts/confluence/publish-dependency-graph-claude-sonnet.md`](../../confluence/publish-dependency-graph-claude-sonnet.md)
> using real data. Values used: `<DOMAIN>` = `watchlist`, `<DOMAIN_DISPLAY_NAME>` = `Watchlist`,
> `<PARENT_PAGE>` = `https://confluence.com/Breakdown/Watchlist` (the same parent as the breakdown
> page, so this becomes its sibling — see the domain-breakdown example, published first). Source
> file `finalArtifacts/summary/watchlist/story-dependency-graph-watchlist.md` has exactly 3
> `### <FE-STORY-ID>` headings and 3 mermaid blocks (one per Watchlist frontend story).

---

## Prompt (filled in)

```
Publish the content of finalArtifacts/summary/watchlist/story-dependency-graph-watchlist.md as a
Confluence page.

Target:
- Parent page: "https://confluence.com/Breakdown/Watchlist" (find by title — same parent as
  "Watchlist — Federated GraphQL Breakdown", so this becomes its sibling page)
- Title: "Watchlist — FE Readiness"

Create-or-update semantics: if a page with this exact title already exists under that parent, UPDATE
it in place (new version, same page id) — do not create a duplicate. If it does not exist, create it
under the parent.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- This file is a series of "### <FE-STORY-ID> · <title>" headings, each immediately followed by ONE
  fenced ```mermaid code block. There are NO other sections to summarize — every heading and every
  mermaid block must appear on the page, in the same order, one after another, none dropped, none
  merged, none abbreviated.
- Each mermaid block becomes either (a) a live mermaid diagram if your Confluence has a mermaid
  renderer available, or (b) a code macro labeled "mermaid (render externally)" carrying the FULL,
  UNMODIFIED diagram source if it doesn't. Either way, the complete diagram source text must be
  preserved verbatim — do not simplify the diagram, drop nodes/edges, or replace it with a text
  description of what the diagram shows.
- Every H3 heading keeps its level and its exact text (including the FE story id and title).
- The intro paragraph above the diagrams (explaining what "one small diagram per frontend story"
  means) stays as regular text at the top of the page, unchanged.
- The back-link at the top of the source file (to be-04-stories.md and to 00-sequencing.md) becomes
  GitHub/Confluence links: the be-04-stories.md reference becomes
  https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/watchlist/be-04-stories.md
  and the 00-sequencing.md reference becomes a link to the live "Migration Sequencing & Roadmap"
  Confluence page if you can resolve it, otherwise a GitHub link to finalArtifacts/00-sequencing.md.
- FE/BE story ids inside the diagrams (e.g. WATCHLIST-FE-001, B-01) stay as plain text inside the
  diagram source — do not try to convert them to Confluence smart links.

Before publishing, do a dry run: tell me the target title, parent, and how many "### <FE-STORY-ID>"
sections / mermaid blocks you found (they should match 1:1) so I can sanity-check nothing is being
dropped. STOP and wait for my approval before writing anything.

After I approve, publish and report back the page URL and the new version number.

Then UPDATE finalArtifacts/jira/confluence-page-map.csv: find the existing row for watchlist
(created when its breakdown page was published) and fill in its "FE Readiness Page URL" column with
the page you just published. If no row exists yet for watchlist, create one with the Breakdown Page
URL column left blank and a note to fill it in when that page is published.
```

## Sample agent response

```
Read finalArtifacts/summary/watchlist/story-dependency-graph-watchlist.md.

Manifest: found 3 "### <FE-STORY-ID>" headings (WATCHLIST-FE-001, WATCHLIST-FE-002,
WATCHLIST-FE-003), each followed by exactly one mermaid block — 3 headings, 3 mermaid blocks, 1:1 as
expected. Plus one intro paragraph and one back-link line at the top.

Your Confluence instance doesn't expose a mermaid-renderer tool in this session, so all 3 diagrams
will publish as code macros labeled "mermaid (render externally)" carrying the full diagram source —
nothing is lost, they just won't render inline until a renderer is added.

Searched under "https://confluence.com/Breakdown/Watchlist" for a page titled "Watchlist — FE
Readiness" — none found. This will be a CREATE.

STOP — waiting for your approval before publishing.
```

**After approval:**

```
Published "Watchlist — FE Readiness" under https://confluence.com/Breakdown/Watchlist as page ID
884741, version 1.
URL: https://confluence.com/Breakdown/Watchlist-FE-Readiness

Updated finalArtifacts/jira/confluence-page-map.csv: found the existing watchlist row (Breakdown
Page URL already filled in from the earlier publish) and set its FE Readiness Page URL column to
https://confluence.com/Breakdown/Watchlist-FE-Readiness.
```

## Verifying no loss after publish (filled in)

```
Open the page you just published/updated. Count the number of H3 sections and the number of mermaid
diagrams/code macros — they should be equal, and should match the count of "### <FE-STORY-ID>"
headings in finalArtifacts/summary/watchlist/story-dependency-graph-watchlist.md. Spot-check 2
diagrams against the source: same node count, same edges, same labels. Report any discrepancy —
especially a diagram that rendered as a flat image with no accessible source, or one where
nodes/edges were silently dropped — before I consider this page done.
```

## Sample agent response

```
3 H3 sections, 3 code macros — matches the source's 3/3. Spot-checked WATCHLIST-FE-001 (6 backend
gate nodes: B-01, C-01, G-01, G-02, G-03, G-05) and WATCHLIST-FE-003 (1 backend gate node: E-01) —
both match the source diagram exactly, node-for-node. No discrepancies found.
```

---
*Worked example · output/prompts/example/confluence/publish-dependency-graph.example.md*
