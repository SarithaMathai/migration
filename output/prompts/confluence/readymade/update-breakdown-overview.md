Update the existing Confluence page below IN PLACE from its source file. Do not create a new page,
do not change the title, do not move it under a different parent.

Target page (update this exact page, by id — this is an UPDATE, new version on the same page id):
- URL: https://confluence.target.com/spaces/PPDE/pages/1313880187/Federated+GraphQL+Stories+Breakdown%E2%80%94+Overview
- Page id: 1313880187  (space: PPDE)
- Keep the existing title as-is.

Source: output/summary/Federated+Graphql+Stories+-+BreakDown.md
Replace the page body with the full, current content of this file, as a SINGLE page in the exact
section order it appears — the program-wide spike register, T-shirt sizing rules, the domain index,
and every per-spike detail section (one H3 sub-section per spike, each with its own table). Do not
split it into multiple pages and do not omit any section. Confluence must hold ALL of it.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
  This includes the program spike register, the domain index, and every per-spike table.
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3) — do not flatten heading levels,
  merge sections, or reorder them. Each spike (SPIKE-01 … the highest-numbered one registered) stays
  its own H3 sub-section, in the source's order.
- Bold, italic, inline code, and emoji/icons (including the legend line, e.g. 🔴🟠🟡🟢🔬⛔) are
  preserved exactly — do not strip or simplify emoji.
- "> " block quotes become quote/info panels, not indented plain text.
- Fenced code blocks become Confluence code macros with the same language hint. A ```mermaid block
  becomes a code macro labeled "mermaid (render externally)" — keep the FULL diagram source.
- Every row in the spike register, the domain index, and each spike's detail table ships exactly as
  written. Do NOT summarize, reword, reflow, paraphrase, or drop any row or section.
- IDs that look like codes or tickets (e.g. SPIKE-07, PRODUCT-BE-E-02) stay as plain text — do not
  auto-convert them into Confluence smart links.
- Any relative link to another file in this repo (a per-domain breakdown page, a complex-case brief)
  becomes a link — to the live Confluence page if it exists (check
  finalArtifacts/jira/confluence-page-map.csv; the 8 domain breakdowns and Complex Scenarios at page
  1313880475 are live) and you can resolve it, otherwise a GitHub link
  (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>). Never leave a bare local path,
  never guess/fabricate a URL.

Before writing, do a DRY RUN: confirm you resolved page id 1313880187 and its current title, and give
a section-by-section manifest (e.g. "N tables incl. per-spike detail tables, N heading sections, 1
icon legend line"). STOP and wait for my approval before updating the page.

After I approve, update the page and report the page URL and the NEW version number.

---

Open page id 1313880187 and compare it section-by-section against
output/summary/Federated+Graphql+Stories+-+BreakDown.md. Confirm: same number of tables (with the same
row counts each, including every spike-detail table), same headings in the same order (all H2 and H3
sections present), the icon legend line intact, no section from the source missing from the page.
Report any discrepancy before I consider this page done.
