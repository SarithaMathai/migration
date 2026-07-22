# Example — Publish the Federated GraphQL Program Overview page to Confluence

> Worked example of [`output/prompts/confluence/publish-program-overview-claude-sonnet.md`](../../confluence/publish-program-overview-claude-sonnet.md)
> using real data. Value used: `<PARENT_PAGE>` = `https://confluence.com/Breakdown`. Source file
> `finalArtifacts/00-overview.md` is 124 lines, 5 tables, 8 headings — real counts.

---

## Prompt (filled in)

```
Publish the content of finalArtifacts/00-overview.md as a single Confluence page.

Target:
- Parent page: "https://confluence.com/Breakdown" (find by title; this also identifies the space —
  if it does not exist, ask me before creating it, and ask me which space to create it in)
- Title: "Spark → Federated GraphQL Migration — Program Overview"

Publish it as a single page in the exact section order it appears in the source — do not split it
into multiple pages, and do not omit any section (what/why, program totals table, domains-at-a-glance
table, backend-stories-by-phase table, DGS service groupings table, recommended sequencing, cross-domain
blockers table, how-to-consume links).

Create-or-update semantics: if a page with this exact title already exists under that parent, UPDATE
it in place (new version, same page id) — do not create a duplicate. If it does not exist, create it
under the parent.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3) — do not flatten heading levels,
  merge sections, or reorder them.
- Bold, italic, inline code, and emoji/icons (🔴🟠🟡🟢) are preserved exactly where they appear in
  the source — do not strip or simplify emoji.
- "> " block quotes become quote/info panels, not indented plain text.
- Every row in every table ships on the page exactly as written. Do NOT summarize, reword, reflow,
  paraphrase, or drop any row or section, including ones that look repetitive or verbose.
- IDs that look like codes or tickets (e.g. PRODUCT-BE-E-00) stay as plain text — do not try to
  auto-convert them into Confluence smart links.
- Any relative link to another file in this repo should become a link — to the live Confluence page
  if it already exists (check finalArtifacts/jira/confluence-page-map.csv) and the assistant can
  resolve it, otherwise to GitHub (https://github.com/myorg/spark-migration/blob/main/<path>).
  Never leave a bare local file path that won't resolve outside this machine, and never guess/fabricate
  a URL.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section list of
what you're about to convert (e.g. "6 tables, 8 heading sections") so I can sanity-check nothing is
being dropped. STOP and wait for my approval before writing anything.

After I approve, publish and report back the page URL and the new version number.
```

## Sample agent response

```
Read finalArtifacts/00-overview.md (124 lines).

Manifest:
- 8 headings: "What & why", "Program totals", "Domains at a glance", "Backend stories by phase",
  "DGS service groupings", "Recommended sequencing", "Cross-domain blockers", "How to consume".
- 5 tables: Program totals, Domains-at-a-glance (8 rows, one per phase-1 domain), Backend
  stories-by-phase, DGS service groupings, Cross-domain blockers.
- No mermaid blocks in this file.
- 3 relative links found (to per-domain breakdown pages and finalArtifacts/00-sequencing.md) — I
  checked finalArtifacts/jira/confluence-page-map.csv: watchlist has a live Confluence page
  (https://confluence.com/Breakdown/Watchlist-Federated-GraphQL-Breakdown), so that link resolves to
  the live page; the other 7 domains don't have a row yet, so those links become GitHub blob URLs
  instead.

Searched under "https://confluence.com/Breakdown" for a page titled "Spark → Federated GraphQL
Migration — Program Overview" — none found. This will be a CREATE.

STOP — waiting for your approval before publishing.
```

**After approval:**

```
Published "Spark → Federated GraphQL Migration — Program Overview" under
https://confluence.com/Breakdown as page ID 884699, version 1.
URL: https://confluence.com/Breakdown/Program-Overview
```

## Verifying no loss after publish (filled in)

```
Open the page you just published/updated and compare it section-by-section against
finalArtifacts/00-overview.md. Confirm: same number of tables (with the same row counts each), same
headings in the same order (all H2 sections present), no section present in the source missing from
the page. Report any discrepancy before I consider this page done.
```

## Sample agent response

```
5/5 tables present with matching row counts, 8/8 headings present in the same order. No
discrepancies found.
```

---
*Worked example · output/prompts/example/confluence/publish-program-overview.example.md*
