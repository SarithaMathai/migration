# Example — Publish the Migration Sequencing & Roadmap page to Confluence

> Worked example of [`output/prompts/confluence/publish-sequencing-claude-sonnet.md`](../../confluence/publish-sequencing-claude-sonnet.md)
> using real data. Value used: `<PARENT_PAGE>` = `https://confluence.com/Breakdown`. Source file
> `finalArtifacts/00-sequencing.md` is 530 lines, 17 tables (332 total rows across all of them, most
> of that in the per-domain story-sequence tables), 17 headings — real counts, and this is the
> largest page in the whole publish set, which is why the example leans on the row-count
> verification step.

---

## Prompt (filled in)

```
Publish the content of finalArtifacts/00-sequencing.md as a single Confluence page.

Target:
- Parent page: "https://confluence.com/Breakdown" (find by title; this also identifies the space —
  if it does not exist, ask me before creating it, and ask me which space to create it in)
- Title: "Migration Sequencing & Roadmap"

This is ONE page covering the whole program's build order: the domain-order table (why each domain
is sequenced where), then one section per domain with its roadmap summary, step table, and full
story-sequence table (Order | Step | Story | Team/Owner | Depends On | Blocks | Parallelizable).
Publish it as a single page in the exact section order it appears in the source — do not split it
into multiple pages (e.g. one page per domain), and do not omit any domain's section or any row of
any story-sequence table, even the long ones.

Create-or-update semantics: if a page with this exact title already exists under that parent, UPDATE
it in place (new version, same page id) — do not create a duplicate. If it does not exist, create it
under the parent.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
  The per-domain story-sequence tables are often 15-80 rows long — publish every row, none dropped or
  sampled.
- Every heading keeps its level exactly — do not flatten heading levels, merge domain sections, or
  reorder them from the source's domain-build order.
- Bold, italic, inline code, and status/gate icons (🟢🟡🟠🔴🔬⛔) are preserved exactly where they
  appear — do not strip or simplify them; they carry real meaning (risk level, gate type).
- "> " block quotes become quote/info panels, not indented plain text.
- Story IDs (e.g. PRODUCT-BE-B-01) and FE story IDs (e.g. WATCHLIST-FE-001) stay as plain text — do
  not try to auto-convert them into Confluence smart links.
- Any relative link to another file in this repo should become a GitHub link:
  https://github.com/myorg/spark-migration/blob/main/<path> — never a local file path.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section manifest
(number of domain sections, total table row count across all story-sequence tables, heading count) so
I can sanity-check nothing is being dropped — this file has the most tabular data of any page in this
program, so the row-count check matters more here than elsewhere. STOP and wait for my approval
before writing anything.

After I approve, publish and report back the page URL and the new version number.
```

## Sample agent response

```
Read finalArtifacts/00-sequencing.md (530 lines).

Manifest:
- 17 headings: 1 "## Domain order" section, then 8 per-domain "## <Domain>" sections (product, bom,
  measurement, packaging, impression, productDetails, watchlist, claims), each with a "Roadmap"
  sub-heading, a step table, and a "Story sequence" sub-heading with its own table.
- 17 tables, 332 total rows across all of them. The largest single table is Product's story-sequence
  table (79 rows — Product is the biggest domain). The smallest is Watchlist's (13 rows).
- Status/gate icons found: 🟢 (ready), 🟡 (medium risk), 🟠 (higher risk), 🔴 (blocked/high risk),
  🔬 (spike-gated), ⛔ (cross-subgraph blocked) — all will be preserved as-is.
- No mermaid blocks in this file.

Searched under "https://confluence.com/Breakdown" for a page titled "Migration Sequencing &
Roadmap" — none found. This will be a CREATE.

STOP — waiting for your approval before publishing (given the size of this page, let me know if
you'd like me to publish domain-by-domain sections for review instead of the whole page at once —
otherwise I'll publish it as one page per the instructions).
```

**After approval:**

```
Published "Migration Sequencing & Roadmap" under https://confluence.com/Breakdown as page ID
884705, version 1.
URL: https://confluence.com/Breakdown/Migration-Sequencing-Roadmap
```

## Verifying no loss after publish (filled in)

```
Open the page you just published/updated and compare it section-by-section against
finalArtifacts/00-sequencing.md. Confirm: same number of domain sections in the same order, same
number of tables with the SAME ROW COUNT each (count rows in every story-sequence table specifically
— this is where silent truncation is most likely to hide), same headings in the same order, no
section missing. Report any discrepancy, especially a row-count mismatch on any story-sequence table,
before I consider this page done.
```

## Sample agent response

```
8/8 domain sections present, in the same build order (watchlist, productDetails, measurement,
packaging, bom, claims, product, impression). 17/17 tables present. Row-count check on every
story-sequence table:

| Domain | Source rows | Published rows | Match |
|---|---|---|---|
| watchlist | 13 | 13 | ✓ |
| productDetails | 15 | 15 | ✓ |
| measurement | 34 | 34 | ✓ |
| packaging | 28 | 28 | ✓ |
| bom | 44 | 44 | ✓ |
| claims | 24 | 24 | ✓ |
| product | 79 | 79 | ✓ |
| impression | 9 | 9 | ✓ |

All story-sequence tables match exactly. All status/gate icons intact. No discrepancies found.
```

---
*Worked example · output/prompts/example/confluence/publish-sequencing.example.md*
