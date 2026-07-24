Publish the content of finalArtifacts/00-order-sequencing.md as a Confluence page.

Target:
- Parent page: "Federated Graphql Migration - Product" (id 1313880343, PPDE space) — nest this under
  the program landing page. If you cannot resolve that parent, ask me before creating anywhere else.
- Title: "Migration Order & Sequencing — Backend + Frontend"

Create-or-update semantics: if a page with this exact title already exists under that parent, UPDATE
it in place (new version, same page id) — do not create a duplicate. Otherwise create it.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, rows, cell content and order — never flattened to bullets
  or prose, never truncated, never summarized "for brevity."
- Every heading keeps its level exactly (H2/H3/H4). Do not merge, reorder, or flatten sections.
- Bold, italic, inline code, and emoji/icons (🔴🟠🟡🟢🔵▶⚠) are preserved exactly.
- "> " block quotes become quote/info panels, not indented plain text.
- IDs like PRODUCT-BE-E-00, WATCHLIST-FE-001, d108 stay as plain text — do not auto-link them.
- Any relative link to another repo file (00-cheatsheet.md, 00-domain-rollout.md, the External
  Dependencies page, etc.) becomes a link to the live Confluence page if it exists (check
  finalArtifacts/jira/confluence-page-map.csv) else a GitHub link
  (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>). Never a bare local path, never a
  guessed URL.

Before writing, do a DRY RUN: give the target title, parent, and a section-by-section manifest
(e.g. "6 tables with row counts, 6 H2 sections"). STOP and wait for my approval before publishing.

After I approve, publish and report the page URL and version number. Then record the URL in
finalArtifacts/jira/confluence-page-map.csv (add a row "order-sequencing,<url>," — create the file
with a header if missing; update in place if a row already exists).

---

Open the page you just published and compare section-by-section against
finalArtifacts/00-order-sequencing.md. Confirm: same number of tables (same row counts each), same
headings in the same order, no section missing, emoji intact. Report any discrepancy.
