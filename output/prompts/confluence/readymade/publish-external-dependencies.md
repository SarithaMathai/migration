Publish the content of finalArtifacts/00-external-dependencies.md as a Confluence page.

Target:
- Parent page: "Federated Graphql Migration - Product" (id 1313880343, PPDE space) — nest under the
  program landing page. If you cannot resolve that parent, ask me before creating anywhere else.
- Title: "External & Cross-Domain Dependencies"

Create-or-update semantics: if a page with this exact title already exists under that parent, UPDATE
it in place (new version, same page id) — do not create a duplicate. Otherwise create it.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, rows, cell content and order — never flattened to bullets
  or prose, never truncated, never summarized. This includes the cross-domain blocker table, the
  cross-subgraph table, the external-service inventory, the per-domain EXT-load table, and the
  entity-resolver gap table.
- Every heading keeps its level exactly (H2/H3). Do not merge, reorder, or flatten sections.
- Bold, italic, inline code, and emoji/icons (🔵🟡🟠🔴⛔▶) are preserved exactly — the 🔵/🟡/🔴
  severity markers carry meaning (see the legend), do not strip or normalize them.
- "> " block quotes become quote/info panels, not indented plain text.
- IDs and service names (PRODUCT-BE-E-00, IG_Clazz, VmmBusinessPartner, PRODUCT-FE-006) stay as
  plain text — do not auto-link them.
- Any relative link to another repo file (be-03-schema.graphql, domain-service-catalog.md, the Order
  & Sequencing page) becomes a link to the live Confluence page if it exists (check
  finalArtifacts/jira/confluence-page-map.csv) else a GitHub link
  (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>). Never a bare local path, never a
  guessed URL.

Before writing, do a DRY RUN: give the target title, parent, and a section-by-section manifest
(e.g. "5 tables with row counts, 6 H2 sections, 1 severity legend"). STOP and wait for my approval
before publishing.

After I approve, publish and report the page URL and version number. Then record the URL in
finalArtifacts/jira/confluence-page-map.csv (add a row "external-dependencies,<url>," — create the
file with a header if missing; update in place if a row already exists).

---

Open the page you just published and compare section-by-section against
finalArtifacts/00-external-dependencies.md. Confirm: same number of tables (same row counts each),
same headings in the same order, no section missing, the 🔵/🟡/🔴 severity markers intact. Report any
discrepancy.
