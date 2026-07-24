# Prompt — Publish the Migration Sequencing & Roadmap page to Confluence
# Model: Claude Sonnet (via org Copilot/Claude integration)

> **Use when:** publishing (or re-syncing) the **migration sequencing** page — domain build order and
> why, per-domain BE/FE roadmap and step tables, the full story implementation sequence, external
> gates, and the effort summary. This answers "what's building, and in what order" for an architect,
> tech lead, or PO — see [`CONFLUENCE-INVENTORY.md`](../../../fedMigrationScripts/reference/CONFLUENCE-INVENTORY.md)
> §2. ONE page, run once, not once per domain.
>
> **Why Sonnet:** mechanical transcription against an explicit rule list, not a judgment-call task.
> **This page is long** (500+ lines, a full story-order table per domain) — if the verification pass
> shows drift, re-run with Opus.
>
> **Prerequisite:** your Copilot/Claude integration must have Confluence access. Confirm before
> running this prompt. If no Confluence access is available, this still works as a **content
> preparation step** — the assistant produces the Confluence-ready structure for manual paste.

---

## Inputs you provide

| Placeholder | Meaning | Example |
|---|---|---|
| `<PARENT_PAGE>` | Exact title of the parent page this should nest under | `Federation Graph Migration ▸ Program` |

Source file: `finalArtifacts/00-sequencing.md`

---

## Prompt

```
Publish the content of finalArtifacts/00-sequencing.md as a single Confluence page.

Target:
- Parent page: "<PARENT_PAGE>" (find by title; this also identifies the space — if it does not
  exist, ask me before creating it, and ask me which space to create it in)
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
  https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path> — never a local file path.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section manifest
(number of domain sections, total table row count across all story-sequence tables, heading count) so
I can sanity-check nothing is being dropped — this file has the most tabular data of any page in this
program, so the row-count check matters more here than elsewhere. STOP and wait for my approval
before writing anything.

After I approve, publish and report back the page URL and the new version number.
```

## Verifying no loss after publish

```
Open the page you just published/updated and compare it section-by-section against
finalArtifacts/00-sequencing.md. Confirm: same number of domain sections in the same order, same
number of tables with the SAME ROW COUNT each (count rows in every story-sequence table specifically
— this is where silent truncation is most likely to hide), same headings in the same order, no
section missing. Report any discrepancy, especially a row-count mismatch on any story-sequence table,
before I consider this page done.
```

---
*Confluence publish prompt — migration sequencing, zero-loss, model-agnostic input · works with any
Copilot/Claude model that has Confluence access; Sonnet is sufficient, Opus optional if verification
shows drift.*
