# Prompt — Publish one domain's Federated GraphQL Breakdown page to Confluence
# Model: Claude Sonnet (via org Copilot/Claude integration)

> **Use when:** publishing (or re-syncing) one domain's merged BE+FE breakdown page in Confluence,
> using its content as the source of truth. Repeat this same prompt once per domain — don't batch
> multiple domains into one call, so each publish is independently reviewable and a failure on one
> domain doesn't block the rest.
>
> **Why Sonnet:** this task is mechanical transcription against an explicit rule list (keep every
> table a table, keep heading levels, no summarizing) — not a judgment-call task, so Sonnet's literal
> instruction-following is sufficient. The dry-run manifest and "Verifying no loss" pass below are the
> real safety net regardless of model. **Exception:** for the largest page (`product` domain — 79 BE
> + 13 FE stories), consider Opus for extra margin against silent truncation on a single long page.
>
> **Prerequisite:** your Copilot/Claude integration must have Confluence access (an MCP server, plugin,
> or connector configured by your org). Confirm before running this prompt — ask your assistant to list
> its available Confluence actions/tools. If none are available, this prompt still works as a **content
> preparation step**: the assistant produces the exact Confluence-ready structure and a human pastes it
> into Confluence's editor manually.

---

## Inputs you provide

Fill these in before running the prompt below:

| Placeholder | Meaning | Example |
|---|---|---|
| `<DOMAIN>` | Domain key (matches the folder under `finalArtifacts/summary/`) | `bom` |
| `<DOMAIN_DISPLAY_NAME>` | Human-readable domain name for the page title | `Bill of Materials (BOM)` |
| `<PARENT_PAGE>` | Exact title of the parent page this should nest under (used to locate the space too — no separate space key needed) | `Federation Graph Migration ▸ Domains ▸ Bill of Materials (BOM)` |

Source file: `finalArtifacts/summary/<DOMAIN>/FederatedGqlBreakDown-<DOMAIN>.md`

---

## Prompt

```
Publish the content of finalArtifacts/summary/<DOMAIN>/FederatedGqlBreakDown-<DOMAIN>.md as a
Confluence page.

Target:
- Parent page: "<PARENT_PAGE>" (find by title; this also identifies the space — if it does not
  exist, ask me before creating it, and ask me which space to create it in)
- Title: "<DOMAIN_DISPLAY_NAME> — Federated GraphQL Breakdown"

Create-or-update semantics: if a page with this exact title already exists under that parent,
UPDATE it in place (new version, same page id) — do not create a duplicate. If it does not exist,
create it under the parent.

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss, full stop:
- Every table stays a table: same columns, same rows, same cell content, same cell order — never
  flattened into a bullet list or prose paragraph, never truncated, never summarized "for brevity."
- Every heading keeps its level exactly (H2 stays H2, H3 stays H3, H4 stays H4, etc.) — do not
  flatten heading levels, merge sections, or reorder them.
- Bold, italic, inline code, and emoji/icons are preserved exactly where they appear in the source.
- "- [ ]" checklist items become native Confluence task lists, not plain bullets.
- "> " block quotes become quote/info panels, not indented plain text.
- Fenced code blocks become Confluence code macros with the same language hint. A ```mermaid block
  becomes a code macro labeled "mermaid (render externally)" — keep the full diagram source; do not
  drop it or replace it with a prose description of the diagram.
- Every acceptance-criteria list, every test case, every dependency/blocks reference, every table row
  in a risk register or story list — all of it ships on the page exactly as written. Do NOT summarize,
  reword, reflow, paraphrase, or drop any section, including ones that look repetitive or verbose.
- IDs that look like codes or tickets (e.g. <TOKEN>-BE-B-01) and references to other pages stay as
  plain text — do not try to auto-convert them into Confluence smart links.
- Any relative link to another file in this repo (be-04-stories.md, another domain's page, a
  complex-case brief) should become a GitHub link:
  https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/<path> — never a local file path.
- If the source file has more than one top-level section (e.g. a "## Backend" and a "## Frontend"
  section), publish ALL of them onto the SAME page, in the same order they appear in the source.
  Do not split sections into separate pages and do not omit any section.

Before publishing, do a dry run: tell me the target title, parent, and a section-by-section list of
what you're about to convert (e.g. "6 tables, 3 mermaid blocks, 2 checklists, 12 heading sections")
so I can sanity-check nothing is being dropped. STOP and wait for my approval before writing anything.

After I approve, publish and report back the page URL and the new version number.

Then APPEND a row to finalArtifacts/jira/confluence-page-map.csv (create it with header
"Domain,Breakdown Page URL,FE Readiness Page URL" if it doesn't exist yet — if a row for <DOMAIN>
already exists, update its Breakdown Page URL column in place rather than adding a duplicate row):
<DOMAIN>,<the page URL you just published>,
This file is what the Jira publish prompts read to link each story back to this page — don't skip it.
```

## Verifying no loss after publish

```
Open the page you just published/updated and compare it section-by-section against
finalArtifacts/summary/<DOMAIN>/FederatedGqlBreakDown-<DOMAIN>.md. Confirm: same number of tables
(with the same row counts each), same number of code/mermaid blocks, same headings in the same order,
no section present in the source missing from the page. Report any discrepancy before I consider this
page done.
```

---
*Confluence publish prompt — zero-loss, model-agnostic input · works with any Copilot/Claude model
that has Confluence access; Sonnet is sufficient, Opus optional for the largest pages.*
