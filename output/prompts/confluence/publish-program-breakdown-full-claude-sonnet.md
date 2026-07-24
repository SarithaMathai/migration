# Prompt — Publish the full Federated GraphQL Stories Breakdown (All Domains) page to Confluence
# Model: Claude Sonnet (via org Copilot/Claude integration)

> **Use when:** publishing (or re-syncing) the **full global breakdown** page — the program spike
> register (with ADR status per spike), full per-spike detail sections, and the all-domain story
> roll-up. This is the deeper companion to
> [`publish-program-overview-claude-sonnet.md`](publish-program-overview-claude-sonnet.md) — publish
> both; the overview page is the one-page orientation, this one is where "what's SPIKE-07 about and
> what does the PO need to decide" actually lives. This is ONE page — run once, not once per domain.
>
> **Why Sonnet:** mechanical transcription against an explicit rule list, not a judgment-call task.
> The dry-run manifest and "Verifying no loss" pass are the real safety net. **This page is long**
> (300+ lines, multiple spike-detail tables) — if the verification pass shows any drift, re-run with
> Opus for extra margin against silent truncation.
>
> **Prerequisite:** your Copilot/Claude integration must have Confluence access. Confirm before
> running this prompt. If no Confluence access is available, this still works as a **content
> preparation step** — the assistant produces the Confluence-ready structure for manual paste.

---

## Inputs you provide

| Placeholder | Meaning | Example |
|---|---|---|
| `<PARENT_PAGE>` | Exact title of the parent page this should nest under | `Federation Graph Migration ▸ Program` |

Source file: `output/summary/Federated+Graphql+Stories+-+BreakDown.md`

---

## Prompt

```
Publish the content of output/summary/Federated+Graphql+Stories+-+BreakDown.md as a single
Confluence page.

Target:
- Parent page: "<PARENT_PAGE>" (find by title; this also identifies the space — if it does not
  exist, ask me before creating it, and ask me which space to create it in)
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
  merge sections, or reorder them. Each spike (`SPIKE-01` … the highest-numbered one currently
  registered) must remain its own H3 sub-section, in the same order as the source.
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
  (https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path>). Never leave a bare local file
  path, and never guess/fabricate a URL.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section list of
what you're about to convert (e.g. "N tables incl. per-spike detail tables, N heading sections, 1
icon legend line") so I can sanity-check nothing is being dropped. STOP and wait for my approval
before writing anything.

After I approve, publish and report back the page URL and the new version number.
```

## Verifying no loss after publish

```
Open the page you just published/updated and compare it section-by-section against
output/summary/Federated+Graphql+Stories+-+BreakDown.md. Confirm: same number of tables (with the
same row counts each, including every spike-detail table), same headings in the same order (all H2
and H3 sections present), the icon legend line intact, no section present in the source missing from
the page. Report any discrepancy before I consider this page done.
```

---
*Confluence publish prompt — full program breakdown, zero-loss, model-agnostic input · works with any
Copilot/Claude model that has Confluence access; Sonnet is sufficient, Opus optional if verification
shows drift.*
