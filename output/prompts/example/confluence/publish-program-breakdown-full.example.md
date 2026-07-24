# Example — Publish the full Federated GraphQL Stories Breakdown (All Domains) page to Confluence

> Worked example of [`output/prompts/confluence/publish-program-breakdown-full-claude-sonnet.md`](../../confluence/publish-program-breakdown-full-claude-sonnet.md)
> using real data. Value used: `<PARENT_PAGE>` = `https://confluence.com/Breakdown`. Source file
> `output/summary/Federated+Graphql+Stories+-+BreakDown.md` is 346 lines, 17 headings, 15 tables, and
> 8 spike-detail sub-sections (SPIKE-01 through SPIKE-07, with 06a/06b as two separate buckets) —
> real counts.

---

## Prompt (filled in)

```
Publish the content of output/summary/Federated+Graphql+Stories+-+BreakDown.md as a single
Confluence page.

Target:
- Parent page: "https://confluence.com/Breakdown" (find by title; this also identifies the space —
  if it does not exist, ask me before creating it, and ask me which space to create it in)
- Title: "Federated GraphQL Stories — Breakdown (All Domains)"

This is ONE page covering the whole program: the program-wide spike register, T-shirt sizing rules,
the domain index, and full spike-detail sections (one sub-section per spike, each with its own
table). Publish it as a single page in the exact section order it appears in the source — do not
split it into multiple pages, and do not omit any section.

Create-or-update semantics: if a page with this exact title already exists under that parent, UPDATE
it in place (new version, same page id) — do not create a duplicate. If it does not exist, create it
under the parent.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
  This includes the program spike register table, the domain index table, and every per-spike table.
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3) — do not flatten heading levels,
  merge sections, or reorder them. Each spike (`SPIKE-01` … `SPIKE-07`) must remain its own H3
  sub-section, in the same order as the source.
- Bold, italic, inline code, and emoji/icons (including the icon legend line, e.g. 🔴🟠🟡🟢🔬⛔) are
  preserved exactly where they appear in the source — do not strip or simplify emoji.
- "> " block quotes become quote/info panels, not indented plain text.
- Fenced code blocks become Confluence code macros with the same language hint. A ```mermaid block
  becomes a code macro labeled "mermaid (render externally)" — keep the full diagram source; do not
  drop it or replace it with a prose description of the diagram.
- Every row in the spike register, every row in the domain index, and every row in each spike's
  detail table ships on the page exactly as written. Do NOT summarize, reword, reflow, paraphrase,
  or drop any row or section, including ones that look repetitive or verbose.
- IDs that look like codes or tickets (e.g. SPIKE-07, PRODUCT-BE-E-02) stay as plain text — do not
  try to auto-convert them into Confluence smart links.
- Any relative link to another file in this repo (a per-domain breakdown page, a complexStories
  brief) should become a link — to the live Confluence page if it already exists (check
  finalArtifacts/jira/confluence-page-map.csv) and the assistant can resolve it, otherwise to GitHub
  (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>). Never leave a bare local file path,
  and never guess/fabricate a URL.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section list of
what you're about to convert (e.g. "N tables incl. per-spike detail tables, N heading sections, 1
icon legend line") so I can sanity-check nothing is being dropped. STOP and wait for my approval
before writing anything.

After I approve, publish and report back the page URL and the new version number.
```

## Sample agent response

```
Read output/summary/Federated+Graphql+Stories+-+BreakDown.md (346 lines).

Manifest:
- 17 headings: Overview, Glossary, The migration phases (A→H), How to read the spikes, Phase 0 —
  Program Spikes, Non-spike complex cases, T-Shirt Size Classification, Domain Index, Spike Detail,
  and 8 per-spike H3 sub-sections (SPIKE-01, SPIKE-02, SPIKE-03, SPIKE-04, SPIKE-05, SPIKE-06a,
  SPIKE-06b, SPIKE-07).
- 15 tables: the program spike register, the domain index (8 rows, phase-1 domains), and one
  resolver-detail table per spike (8 tables).
- 1 icon legend line (🔴🟠🟡🟢 risk levels, 🔬 spike marker) near the top — will preserve as-is.
- No mermaid blocks in this file.
- 8 relative links to per-domain breakdown pages — checked finalArtifacts/jira/confluence-page-map.csv:
  watchlist resolves to its live Confluence page; the other 7 domains don't have a row yet, so those
  become GitHub blob URLs.

Searched under "https://confluence.com/Breakdown" for a page titled "Federated GraphQL Stories —
Breakdown (All Domains)" — none found. This will be a CREATE.

STOP — waiting for your approval before publishing.
```

**After approval:**

```
Published "Federated GraphQL Stories — Breakdown (All Domains)" under
https://confluence.com/Breakdown as page ID 884712, version 1.
URL: https://confluence.com/Breakdown/Stories-Breakdown-All-Domains
```

## Verifying no loss after publish (filled in)

```
Open the page you just published/updated and compare it section-by-section against
output/summary/Federated+Graphql+Stories+-+BreakDown.md. Confirm: same number of tables (with the
same row counts each, including every spike-detail table), same headings in the same order (all H2
and H3 sections present), the icon legend line intact, no section present in the source missing from
the page. Report any discrepancy before I consider this page done.
```

## Sample agent response

```
15/15 tables present with matching row counts, 17/17 headings present in the same order, all 8 spike
sub-sections present (SPIKE-01 through SPIKE-07, in the same order including 06a/06b), icon legend
line intact. No discrepancies found.
```

---
*Worked example · output/prompts/example/confluence/publish-program-breakdown-full.example.md*
