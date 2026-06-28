# Confluence — PO-ready pages

These are **Product-Owner-facing pages**, one per domain plus a program portfolio, written so they paste
cleanly into Confluence.

| Page | Use |
|------|-----|
| [`00-portfolio.md`](./00-portfolio.md) | Program rollup — all 13 domains, totals, sequencing, blockers, decisions |
| [`product.md`](./product.md) · [`bom.md`](./bom.md) · [`sample.md`](./sample.md) · [`workspace.md`](./workspace.md) · [`packaging.md`](./packaging.md) · [`search.md`](./search.md) · [`claims.md`](./claims.md) · [`measurement.md`](./measurement.md) · [`watchlist.md`](./watchlist.md) · [`productDetails.md`](./productDetails.md) · [`impression.md`](./impression.md) · [`attachment.md`](./attachment.md) · [`discussion.md`](./discussion.md) | One page per domain — what we're building, scope, effort, risks, decisions, sequencing |

## How to paste into Confluence (Cloud)

1. Create the page, click into the body, then use **`/Markdown`** (type slash → "Markdown") and paste the
   file's contents — Confluence converts headings, tables, and lists. (Or paste directly; the Cloud editor
   converts most Markdown on paste.)
2. Review tables (they render as Confluence tables) and fix any link targets — the relative links here
   (`../product/…`, `../jira/…`) point at repo files; in Confluence, replace them with links to the
   corresponding Confluence pages or the repo URL.

> Confluence **Server/DC** uses wiki markup, not Markdown. Use the *Insert → Markup → Markdown* dialog, or
> the Markdown macro, to convert on paste.

## Want a Word / Google Doc?

The same Markdown pastes into **Google Docs** and **Microsoft Word** (both accept Markdown-style content;
Word's *Open* also reads `.md`). A native `.docx`/`.html` export is not generated here because no converter
(`pandoc` / LibreOffice) is installed in this environment — if you want it, install `pandoc` and run e.g.
`pandoc product.md -o product.docx`, or ask and we can add an HTML export step.

## Keeping these current

These pages are **assembled from** the per-domain analysis (`../<domain>/04-po-summary.md`,
`03-schema-analysis.md §Migration Approach`, `05-attribute-inventory.md`). If a domain's analysis changes,
update its page here. New domains follow the same outline — see
[`../scripts/skill-06-consumption-artifacts.md`](../scripts/skill-06-consumption-artifacts.md).
