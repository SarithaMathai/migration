# Prompt — Publish the Federated GraphQL Program Overview page to Confluence
# Model: Claude Sonnet (via org Copilot/Claude integration)

> **Use when:** publishing (or re-syncing) the single **program-wide overview** page — the one page
> that sits above all per-domain breakdown pages: summary stats, glossary, migration phases, the
> cross-domain spike register, T-shirt sizing rules, the domain index, and full spike detail sections.
> This is ONE page, not split per-domain — run this prompt once, not once per domain.
>
> **Why Sonnet:** this task is mechanical transcription against an explicit rule list (keep every
> table a table, keep heading levels, no summarizing) — not a judgment-call task, so Sonnet's literal
> instruction-following is sufficient. The dry-run manifest and "Verifying no loss" pass below are the
> real safety net regardless of model. This page is long (300+ lines, 14 tables) — if you see any
> drift on the verification pass, re-run with Opus for extra margin.
>
> **Prerequisite:** your Copilot/Claude integration must have Confluence access (an MCP server, plugin,
> or connector configured by your org). Confirm before running this prompt — ask your assistant to list
> its available Confluence actions/tools. If none are available, this prompt still works as a **content
> preparation step**: the assistant produces the exact Confluence-ready structure and a human pastes it
> into Confluence's editor manually.
>
> **Relationship to the per-domain pages:** this overview page is expected to **link out** to each
> domain's own breakdown page (e.g. "FederatedGqlBreakDown-bom") and to spike research briefs. If those
> pages already exist in Confluence, prefer linking to the live Confluence page over a raw repo link
> when the assistant can resolve it — otherwise keep the reference as-is (see the link-handling rule
> below) rather than guessing a URL.

---

## Inputs you provide

Fill these in before running the prompt below:

| Placeholder | Meaning | Example |
|---|---|---|
| `<SOURCE_FILE>` | Path (or pasted content) of the overview Markdown file | `Federated+Graphql+Stories+-+BreakDown.md` |
| `<PAGE_TITLE>` | Exact Confluence page title | `Federated GraphQL — Migration Overview · All Domains` |
| `<PARENT_PAGE>` | Exact title of the parent page this should nest under (used to locate the space too — no separate space key needed) | `Federation Graph Migration` |

---

## Prompt

```
Publish the content of <SOURCE_FILE> as a single Confluence page.

Target:
- Parent page: "<PARENT_PAGE>" (find by title; this also identifies the space — if it does not
  exist, ask me before creating it, and ask me which space to create it in)
- Title: "<PAGE_TITLE>"

This is ONE page covering the whole program: overview, glossary, migration phases, the program-wide
spike register, T-shirt sizing rules, the domain index, and full spike-detail sections (one sub-section
per spike, each with its own table). Publish it as a single page in the exact section order it appears
in the source — do not split it into multiple pages, and do not omit any section.

Create-or-update semantics: if a page with this exact title already exists under that parent, UPDATE
it in place (new version, same page id) — do not create a duplicate. If it does not exist, create it
under the parent.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
  This includes the opening summary/stats table, the domain index table, and every per-spike table.
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3) — do not flatten heading levels,
  merge sections, or reorder them. Each spike (`SPIKE-01` … `SPIKE-06b`) must remain its own H3
  sub-section under the "Spike Detail" H2, in the same order as the source.
- Bold, italic, inline code, and emoji/icons (including the icon legend line, e.g. 🔴🟠🟡🟢🔬) are
  preserved exactly where they appear in the source — do not strip or simplify emoji.
- "> " block quotes become quote/info panels, not indented plain text.
- Fenced code blocks become Confluence code macros with the same language hint. A ```mermaid block
  becomes a code macro labeled "mermaid (render externally)" — keep the full diagram source; do not
  drop it or replace it with a prose description of the diagram.
- Every row in the Program Spikes table, every row in the Domain Index table, and every row in each
  spike's resolver-detail table ships on the page exactly as written. Do NOT summarize, reword,
  reflow, paraphrase, or drop any row or section, including ones that look repetitive or verbose.
- IDs that look like codes or tickets (e.g. SPIKE-01, PRODUCT-BE-E-02, ADR-013) stay as plain text —
  do not try to auto-convert them into Confluence smart links.
- Any relative link to another file in this repo (a per-domain breakdown page, a complexStories brief,
  an ADR) should become a proper absolute link — to the live Confluence page if it already exists and
  the assistant can resolve it, otherwise to GitHub, otherwise left as the original reference. Never
  leave a bare local file path that won't resolve outside this machine, and never guess/fabricate a URL.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section list of
what you're about to convert (e.g. "14 tables incl. 7 spike-detail tables, 15 heading sections, 1 icon
legend line") so I can sanity-check nothing is being dropped. STOP and wait for my approval before
writing anything.

After I approve, publish and report back the page URL and the new version number.
```

## Verifying no loss after publish

```
Open the page you just published/updated and compare it section-by-section against <SOURCE_FILE>.
Confirm: same number of tables (with the same row counts each, including all 7 spike-detail tables),
same headings in the same order (all H2 and H3 sections present), the icon legend line intact, no
section present in the source missing from the page. Report any discrepancy before I consider this
page done.
```

---
*Confluence publish prompt — program overview, zero-loss, model-agnostic input · works with any
Copilot/Claude model that has Confluence access; Sonnet is sufficient, Opus optional if verification
shows drift.*
