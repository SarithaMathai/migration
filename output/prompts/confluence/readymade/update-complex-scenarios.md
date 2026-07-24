Update the existing Confluence page below IN PLACE, assembling it from the 9 complex-case sources.
Do not create a new page, do not change the title, do not move it under a different parent, and do NOT
split the cases into separate pages — this is ONE page with one section per case.

Target page (update this exact page, by id — this is an UPDATE, new version on the same page id):
- URL: https://confluence.target.com/spaces/PPDE/pages/1313880475/Federated+GraphQL+Migration+%E2%80%94+Product+%E2%80%94+Complex+Scenarios
- Page id: 1313880475  (space: PPDE)
- Keep the existing title as-is.

Build the page body as 9 top-level (H2) sections, one per case, in this exact order:
  1. output/complexStories/acl/00-overview.md            then acl/01-adr-acl-mid-request-update.md
  2. output/complexStories/non-atomic-write-saga/00-overview.md   then .../01-adr-non-atomic-write-saga.md
  3. output/complexStories/techpack/00-overview.md        then techpack/01-adr-techpack.md
  4. output/complexStories/partner-drop-undrop-write/00-overview.md   then .../01-adr-partner-drop-undrop.md
  5. output/complexStories/notRemovable-undroppable-partners/00-overview.md   then .../01-adr-notremovable-undroppable-partners.md
  6. output/complexStories/attachments-enrichment/00-overview.md   then .../01-adr-attachments-enrichment.md
  7. output/complexStories/components-and-counts-rollups/00-overview.md   then .../01-adr-components-counts-rollups.md
  8. output/complexStories/polymorphic-type-resolution/00-overview.md   then .../01-adr-polymorphic-type-resolution.md
  9. output/complexStories/cross-domain-association/00-overview.md   then .../01-adr-cross-domain-association.md
(If a newer case folder exists under output/complexStories/ that isn't listed, include it too, after
these, and flag it in the dry run.)

For EACH case, publish the full 00-overview.md (the problem brief) immediately followed by the full
01-adr-*.md (the draft ADR) — both complete, nothing summarized away. The case's own H1 becomes the
section's H2; every heading inside it shifts down one level accordingly (its H2 → H3, H3 → H4) so the
levels stay consistent and nested — do not flatten them into a single level. Confluence must hold ALL
the content of all 18 source files.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose, never truncated, never summarized "for brevity." This
  includes every options/trade-off table, decision-drivers table, and consequences table in each ADR.
- Heading levels stay consistent under the one-level shift described above — never merge or drop the
  ADR's own sub-sections (Today's behaviour / Decision drivers / Options / Decision / Consequences /
  On-acceptance lifecycle) or the brief's §1 problem / §2 what-must-be-decided.
- Bold, italic, inline code, and emoji/icons (🔴 Proposed status markers, 🟠🟡🟢🔬⛔, etc.) are
  preserved exactly — do not strip or simplify emoji, and do not change a 🔴 Proposed status.
- "> " block quotes become quote/info panels, not indented plain text.
- Fenced code blocks become Confluence code macros with the same language hint. A ```mermaid block
  becomes a code macro labeled "mermaid (render externally)" — keep the FULL diagram source; do not
  replace it with a prose description.
- Every decision driver, every option with its trade-offs, every pin-down, every consequence, every
  ACL note — all of it ships exactly as written. Do NOT summarize, reword, reflow, paraphrase, or drop
  any section, including ones that look repetitive or verbose.
- IDs and references (ADR-019, SPIKE-06b, PRODUCT-BE-S-02, ADR-015 Option B) stay as plain text — do
  not auto-convert them into Confluence smart links.
- Any relative link in a source (to be-04-stories.md, a domain breakdown, another case's ADR, an
  01-stories.md) becomes a link — to the live Confluence page if it exists (check
  finalArtifacts/jira/confluence-page-map.csv; the 8 domain breakdowns and the Breakdown Overview at
  page 1313880187 are live) and you can resolve it, otherwise a GitHub link
  (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>). Never leave a bare local path,
  never guess/fabricate a URL.

Optional but helpful: add a short table-of-contents / index table at the very top (Case | Spike |
Draft ADR | Home domains | Status) built from the case briefs — but this is IN ADDITION to the full
per-case content below it, never a replacement for it.

Before writing, do a DRY RUN: list the 9 (or more) cases in order, and for each give a manifest of what
it contributes (e.g. "ACL: brief = 4 headings 1 table; ADR-019 = 9 headings, 3 tables, 1 mermaid").
Give the page-wide totals too (total sections, tables, mermaid blocks). Confirm you resolved page id
1313880475 and its current title. STOP and wait for my approval before updating the page.

After I approve, update the page and report the page URL and the NEW version number.

---

Open page id 1313880475 and compare it against all 18 source files (each case's 00-overview.md and
01-adr-*.md). Confirm, per case: the brief and the full ADR are both present and complete; same number
of tables (with the same row counts each); same number of code/mermaid blocks; the ADR's sub-sections
(Today's behaviour, Decision drivers, Options, Decision, Consequences, lifecycle) all present; heading
nesting consistent; the 🔴/status markers unchanged. Report any case where anything is missing or
shortened before I consider this page done.
