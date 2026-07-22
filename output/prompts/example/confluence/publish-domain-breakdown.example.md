# Example — Publish one domain's Federated GraphQL Breakdown page to Confluence

> Worked example of [`output/prompts/confluence/publish-domain-breakdown-claude-sonnet.md`](../../confluence/publish-domain-breakdown-claude-sonnet.md)
> using real data. Values used: `<DOMAIN>` = `watchlist`, `<DOMAIN_DISPLAY_NAME>` = `Watchlist`,
> `<PARENT_PAGE>` = `https://confluence.com/Breakdown`. Source file
> `finalArtifacts/summary/watchlist/FederatedGqlBreakDown-watchlist.md` is 264 lines, 18 tables, 23
> headings, `## Backend` + `## Frontend` sections — real counts, not placeholders.

---

## Prompt (filled in)

```
Publish the content of finalArtifacts/summary/watchlist/FederatedGqlBreakDown-watchlist.md as a
Confluence page.

Target:
- Parent page: "https://confluence.com/Breakdown" (find by title; this also identifies the space —
  if it does not exist, ask me before creating it, and ask me which space to create it in)
- Title: "Watchlist — Federated GraphQL Breakdown"

Create-or-update semantics: if a page with this exact title already exists under that parent,
UPDATE it in place (new version, same page id) — do not create a duplicate. If it does not exist,
create it under the parent.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3, H4 stays H4, etc.) — do not
  flatten heading levels, merge sections, or reorder them.
- Bold, italic, inline code, and emoji/icons are preserved exactly where they appear in the source.
- "- [ ]" checklist items become native Confluence task lists, not plain bullets.
- "> " block quotes become quote/info panels, not indented plain text.
- Fenced code blocks become Confluence code macros with the same language hint. A ```mermaid block
  becomes a code macro labeled "mermaid (render externally)" — keep the full diagram source; do not
  drop it or replace it with a prose description of the diagram.
- Every acceptance-criteria list, every test case, every dependency/blocks reference, every table row
  in a risk register or story list — all of it ships on the page exactly as written. Do NOT summarize,
  reword, reflow, paraphrase, or drop any section, including ones that look repetitive or verbose.
- IDs that look like codes or tickets (e.g. WATCHLIST-BE-B-01) and references to other pages stay as
  plain text — do not try to auto-convert them into Confluence smart links.
- Any relative link to another file in this repo (be-04-stories.md, another domain's page, a
  complex-case brief) should become a GitHub link:
  https://github.com/myorg/spark-migration/blob/main/<path> — never a local file path.
- If the source file has more than one top-level section (e.g. a "## Backend" and a "## Frontend"
  section), publish ALL of them onto the SAME page, in the same order they appear in the source.
  Do not split sections into separate pages and do not omit any section.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section list of
what you're about to convert (e.g. "6 tables, 3 mermaid blocks, 2 checklists, 12 heading sections")
so I can sanity-check nothing is being dropped. STOP and wait for my approval before writing anything.

After I approve, publish and report back the page URL and the new version number.

Then APPEND a row to finalArtifacts/jira/confluence-page-map.csv (create it with header
"Domain,Breakdown Page URL,FE Readiness Page URL" if it doesn't exist yet — if a row for watchlist
already exists, update its Breakdown Page URL column in place rather than adding a duplicate row):
watchlist,<the page URL you just published>,
This file is what the Jira publish prompts read to link each story back to this page — don't skip it.
```

## Sample agent response

```
Read finalArtifacts/summary/watchlist/FederatedGqlBreakDown-watchlist.md (264 lines).

Manifest:
- 2 top-level sections: "## Backend" (line 1) and "## Frontend" (line 196) — both will publish on
  the same page, in this order.
- 23 headings total (2×H2, plus H3/H4 story and phase headers under each).
- 18 tables (story-summary tables, phase tables, dependency tables, migration-scope tables — full
  list on request).
- 0 mermaid blocks, 0 checklists in this particular file (the dependency graph is a separate page).
- No relative links found that need rewriting to GitHub.

Searched Confluence under parent "https://confluence.com/Breakdown" for a page titled "Watchlist —
Federated GraphQL Breakdown" — none found. This will be a CREATE, not an update.

STOP — waiting for your approval before publishing.
```

**After approval:**

```
Published "Watchlist — Federated GraphQL Breakdown" under
https://confluence.com/Breakdown as page ID 884737, version 1.
URL: https://confluence.com/Breakdown/Watchlist-Federated-GraphQL-Breakdown

Appended to finalArtifacts/jira/confluence-page-map.csv:
watchlist,https://confluence.com/Breakdown/Watchlist-Federated-GraphQL-Breakdown,
```

## Verifying no loss after publish (filled in)

```
Open the page you just published/updated and compare it section-by-section against
finalArtifacts/summary/watchlist/FederatedGqlBreakDown-watchlist.md. Confirm: same number of tables
(with the same row counts each), same number of code/mermaid blocks, same headings in the same order,
no section present in the source missing from the page. Report any discrepancy before I consider this
page done.
```

## Sample agent response

```
Compared the published page to the source: 18/18 tables present with matching row counts, 23/23
headings present in the same order, both "## Backend" and "## Frontend" sections intact, no mermaid
blocks in either (consistent with the source). No discrepancies found.
```

---
*Worked example · output/prompts/example/confluence/publish-domain-breakdown.example.md*
