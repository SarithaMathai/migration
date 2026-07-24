Update the existing Confluence page below IN PLACE from its source file. Do not create a new page,
do not change the title, do not move it under a different parent.

Target page (update this exact page, by id — this is an UPDATE, new version on the same page id):
- URL: https://confluence.target.com/spaces/PPDE/pages/1313880343/Federated+Graphql+Migration+-+Product
- Page id: 1313880343  (space: PPDE)
- Keep the existing title as-is.

Source: finalArtifacts/00-overview.md
Replace the page body with the full, current content of this file, in the exact section order it
appears — do not split it into multiple pages and do not omit any section (what/why, program totals
table, domains-at-a-glance table, backend-stories-by-phase table, DGS service groupings table,
recommended sequencing, cross-domain blockers table, how-to-consume links). Confluence must hold ALL
of it; nothing summarized away.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3) — do not flatten heading levels,
  merge sections, or reorder them.
- Bold, italic, inline code, and emoji/icons (🔴🟠🟡🟢) are preserved exactly where they appear —
  do not strip or simplify emoji.
- "> " block quotes become quote/info panels, not indented plain text.
- Every row in every table ships exactly as written. Do NOT summarize, reword, reflow, paraphrase, or
  drop any row or section, including ones that look repetitive or verbose.
- IDs that look like codes or tickets (e.g. PRODUCT-BE-E-00, SPIKE-07) stay as plain text — do not
  auto-convert them into Confluence smart links.
- Any relative link to another file in this repo becomes a link — to the live Confluence page if it
  exists (check finalArtifacts/jira/confluence-page-map.csv; the domain breakdowns, the Breakdown
  Overview at page 1313880187, and Complex Scenarios at page 1313880475 are all live) and you can
  resolve it, otherwise a GitHub link (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>).
  Never leave a bare local path, never guess/fabricate a URL.

Before writing, do a DRY RUN: confirm you resolved page id 1313880343 and its current title, and give
a section-by-section manifest (e.g. "N tables with row counts, N heading sections"). STOP and wait for
my approval before updating the page.

After I approve, update the page and report the page URL and the NEW version number.

---

Open page id 1313880343 and compare it section-by-section against finalArtifacts/00-overview.md.
Confirm: same number of tables (with the same row counts each), same headings in the same order (all
H2 sections present), no section from the source missing from the page. Report any discrepancy before
I consider this page done.
