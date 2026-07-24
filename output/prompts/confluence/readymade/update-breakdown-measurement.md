Update the existing Confluence page below IN PLACE from its source file. Do not create a new page,
do not change the title, do not move it under a different parent.

Target page (update this exact page, by id — this is an UPDATE, new version on the same page id):
- URL: https://confluence.target.com/spaces/PPDE/pages/1313880256/Federated+GraphQL+Breakdown+%E2%80%94+Measurement
- Page id: 1313880256  (space: PPDE)
- Keep the existing title as-is.

Source: finalArtifacts/summary/measurement/FederatedGqlBreakDown-measurement.md
Replace the page body with the full, current content of this file (all top-level sections — e.g.
"## Backend" and "## Frontend" — on THIS one page, in the source's order). Confluence must hold ALL of
it; nothing is left out or shortened.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3, H4 stays H4, etc.) — do not
  flatten heading levels, merge sections, or reorder them.
- Bold, italic, inline code, and emoji/icons (🔴🟠🟡🟢🔬⛔) are preserved exactly where they appear.
- "- [ ]" checklist items become native Confluence task lists, not plain bullets.
- "> " block quotes become quote/info panels, not indented plain text.
- Fenced code blocks become Confluence code macros with the same language hint. A ```mermaid block
  becomes a code macro labeled "mermaid (render externally)" — keep the FULL diagram source; do not
  drop it or replace it with a prose description of the diagram.
- Every acceptance-criteria list, every test case, every dependency/blocks reference, every risk-
  register row, every story-list row — all of it ships exactly as written. Do NOT summarize, reword,
  reflow, paraphrase, or drop any section, including ones that look repetitive or verbose.
- IDs that look like codes or tickets (e.g. MST-BE-B-01, SPIKE-04) stay as plain text —
  do not auto-convert them into Confluence smart links.
- Any relative link to another file in this repo (be-04-stories.md, another domain's page, a complex-
  case brief) becomes a link — to the live Confluence page if one exists (check
  finalArtifacts/jira/confluence-page-map.csv) and you can resolve it, otherwise a GitHub link
  (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>). Never leave a bare local path,
  never guess/fabricate a URL.

Before writing, do a DRY RUN: confirm you resolved page id 1313880256 and its current title, and give a
section-by-section manifest of what you're about to publish (e.g. "N tables with their row counts, N
mermaid blocks, N checklists, N heading sections, both Backend + Frontend sections present"). STOP and
wait for my approval before updating the page.

After I approve, update the page and report the page URL and the NEW version number.

Then ensure finalArtifacts/jira/confluence-page-map.csv has a row for measurement pointing at this page
(header "Domain,Breakdown Page URL,FE Readiness Page URL"; create the file if missing; update the
existing measurement row's Breakdown Page URL in place rather than adding a duplicate):
measurement,https://confluence.target.com/spaces/PPDE/pages/1313880256/Federated+GraphQL+Breakdown+%E2%80%94+Measurement,

---

Open page id 1313880256 and compare it section-by-section against
finalArtifacts/summary/measurement/FederatedGqlBreakDown-measurement.md. Confirm: same number of tables
(with the same row counts each), same number of code/mermaid blocks, same headings in the same order,
both top-level sections present, no section from the source missing from the page. Report any
discrepancy before I consider this page done.
