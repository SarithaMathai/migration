# Prompt — Publish the Federated GraphQL Program Overview page to Confluence
# Model: Claude Sonnet (via org Copilot/Claude integration)

> **Use when:** publishing (or re-syncing) the **program-wide overview** page — what/why, program
> totals, the domain-at-a-glance table, DGS service groupings, and the phase legend. This is ONE page,
> not split per-domain — run this prompt once, not once per domain. For the fuller global page with
> the complete program spike register and per-spike detail sections, use
> [`publish-program-breakdown-full-claude-sonnet.md`](publish-program-breakdown-full-claude-sonnet.md)
> instead/in addition — they're two different pages at two different depths, see
> [`CONFLUENCE-INVENTORY.md`](../../../fedMigrationScripts/reference/CONFLUENCE-INVENTORY.md) §2.
>
> **Why Sonnet:** this task is mechanical transcription against an explicit rule list (keep every
> table a table, keep heading levels, no summarizing) — not a judgment-call task, so Sonnet's literal
> instruction-following is sufficient. The dry-run manifest and "Verifying no loss" pass below are the
> real safety net regardless of model.
>
> **Prerequisite:** your Copilot/Claude integration must have Confluence access (an MCP server, plugin,
> or connector configured by your org). Confirm before running this prompt — ask your assistant to list
> its available Confluence actions/tools. If none are available, this prompt still works as a **content
> preparation step**: the assistant produces the exact Confluence-ready structure and a human pastes it
> into Confluence's editor manually.
>
> **Relationship to the per-domain pages:** this overview page is expected to **link out** to each
> domain's own breakdown page (e.g. "BOM — Federated GraphQL Breakdown") and to the Migration
> Sequencing page. If those pages already exist in Confluence, prefer linking to the live Confluence
> page over a raw GitHub link when the assistant can resolve it (check
> `finalArtifacts/jira/confluence-page-map.csv` first) — otherwise keep the reference as a GitHub link
> rather than guessing a URL.

---

## Inputs you provide

Fill these in before running the prompt below:

| Placeholder | Meaning | Example |
|---|---|---|
| `<PARENT_PAGE>` | Exact title of the parent page this should nest under (used to locate the space too — no separate space key needed) | `Federation Graph Migration` |

Source file: `finalArtifacts/00-overview.md`

---

## Prompt

```
Publish the content of finalArtifacts/00-overview.md as a single Confluence page.

Target:
- Parent page: "<PARENT_PAGE>" (find by title; this also identifies the space — if it does not
  exist, ask me before creating it, and ask me which space to create it in)
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
  resolve it, otherwise to GitHub (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>).
  Never leave a bare local file path that won't resolve outside this machine, and never guess/fabricate
  a URL.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section list of
what you're about to convert (e.g. "6 tables, 8 heading sections") so I can sanity-check nothing is
being dropped. STOP and wait for my approval before writing anything.

After I approve, publish and report back the page URL and the new version number.
```

## Verifying no loss after publish

```
Open the page you just published/updated and compare it section-by-section against
finalArtifacts/00-overview.md. Confirm: same number of tables (with the same row counts each), same
headings in the same order (all H2 sections present), no section present in the source missing from
the page. Report any discrepancy before I consider this page done.
```

---
*Confluence publish prompt — program overview, zero-loss, model-agnostic input · works with any
Copilot/Claude model that has Confluence access; Sonnet is sufficient, Opus optional if verification
shows drift.*
