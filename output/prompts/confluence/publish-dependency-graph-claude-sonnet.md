# Prompt — Publish one domain's FE-Readiness dependency graph to Confluence
# Model: Claude Sonnet (via org Copilot/Claude integration)

> **Use when:** publishing (or re-syncing) one domain's FE-readiness page — one small mermaid diagram
> per frontend story, showing exactly which backend stories must ship before that FE story can start.
> Repeat once per domain, right after publishing that same domain's breakdown page (they're meant to
> be sibling child pages under the domain parent — see
> [`CONFLUENCE-INVENTORY.md`](../../../fedMigrationScripts/reference/CONFLUENCE-INVENTORY.md) §3).
>
> **Why Sonnet:** mechanical transcription — the file is mostly mermaid code blocks with short prose
> between them, not prose requiring judgment. The real risk on this file type isn't summarization,
> it's **mermaid diagrams silently rendering as plain text or images instead of an editable/re-
> renderable diagram** — the "Verifying no loss" pass below checks specifically for that.
>
> **Prerequisite:** your Copilot/Claude integration must have Confluence access, AND your Confluence
> instance must support a mermaid renderer (a marketplace app, or native mermaid support) for the
> diagrams to actually render — if it doesn't, this prompt still preserves the diagram *source* in a
> code macro (labeled "mermaid (render externally)") so nothing is lost, it just won't render inline
> until a renderer is available.

---

## Inputs you provide

| Placeholder | Meaning | Example |
|---|---|---|
| `<DOMAIN>` | Domain key (matches the folder under `finalArtifacts/summary/`) | `watchlist` |
| `<DOMAIN_DISPLAY_NAME>` | Human-readable domain name for the page title | `Watchlist` |
| `<PARENT_PAGE>` | Exact title of the parent page this should nest under — the SAME parent as that domain's breakdown page | `Federation Graph Migration ▸ Domains ▸ Watchlist` |

Source file: `finalArtifacts/summary/<DOMAIN>/story-dependency-graph-<DOMAIN>.md`

---

## Prompt

```
Publish the content of finalArtifacts/summary/<DOMAIN>/story-dependency-graph-<DOMAIN>.md as a
Confluence page.

Target:
- Parent page: "<PARENT_PAGE>" (find by title — same parent as "<DOMAIN_DISPLAY_NAME> — Federated
  GraphQL Breakdown", so this becomes its sibling page)
- Title: "<DOMAIN_DISPLAY_NAME> — FE Readiness"

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
  https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/<DOMAIN>/be-04-stories.md
  and the 00-sequencing.md reference becomes a link to the live "Migration Sequencing & Roadmap"
  Confluence page if you can resolve it, otherwise a GitHub link to finalArtifacts/00-sequencing.md.
- FE/BE story ids inside the diagrams (e.g. WATCHLIST-FE-001, B-01) stay as plain text inside the
  diagram source — do not try to convert them to Confluence smart links.

Before publishing, do a dry run: tell me the target title, parent, and how many "### <FE-STORY-ID>"
sections / mermaid blocks you found (they should match 1:1) so I can sanity-check nothing is being
dropped. STOP and wait for my approval before writing anything.

After I approve, publish and report back the page URL and the new version number.

Then UPDATE finalArtifacts/jira/confluence-page-map.csv: find the existing row for <DOMAIN> (created
when its breakdown page was published) and fill in its "FE Readiness Page URL" column with the page
you just published. If no row exists yet for <DOMAIN>, create one with the Breakdown Page URL column
left blank and a note to fill it in when that page is published.
```

## Verifying no loss after publish

```
Open the page you just published/updated. Count the number of H3 sections and the number of mermaid
diagrams/code macros — they should be equal, and should match the count of "### <FE-STORY-ID>"
headings in finalArtifacts/summary/<DOMAIN>/story-dependency-graph-<DOMAIN>.md. Spot-check 2 diagrams
against the source: same node count, same edges, same labels. Report any discrepancy — especially a
diagram that rendered as a flat image with no accessible source, or one where nodes/edges were
silently dropped — before I consider this page done.
```

---
*Confluence publish prompt — FE-readiness dependency graphs, zero-loss, model-agnostic input · works
with any Copilot/Claude model that has Confluence access; Sonnet is sufficient.*
