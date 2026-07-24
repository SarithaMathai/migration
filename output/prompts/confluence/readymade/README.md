# Confluence — ready-made update prompts (pre-wired to the live pages)

> **What these are:** one prompt per Confluence page that **already exists** in the PPDE space, each
> pre-filled with that page's exact URL/id so it **updates the existing page in place** — you don't
> supply a `<DOMAIN>`, `<PARENT_PAGE>`, or search-by-title. Copy the prompt, run it, approve the
> dry-run, done. These are the "I already published once, now re-sync the content" prompts.
>
> **How they differ from [`../` (the generalized prompts)](../):** the parent `confluence/` prompts
> take placeholders and *find or create* a page by title under a parent. The prompts here hard-code a
> specific target page id (from the live-page list below) and only ever **update** it — never create,
> never duplicate. Use these for re-syncs; use the generalized ones to stand up a page that doesn't
> exist yet.
>
> **The contract is the same:** zero data loss, zero format loss. Every table stays a table, every
> heading keeps its level, every row/AC/test-case/ADR-option ships exactly as written, mermaid stays
> as full diagram source in a code macro. Confluence must hold **all** the data — nothing summarized
> away "for brevity." Each prompt does a **dry-run manifest first and waits for your approval** before
> writing.

## The live pages these target (from `output/prompts/example/confluence/scrap.txt`)

| Prompt | Confluence page | Page id | Source in repo |
|---|---|---|---|
| [update-program-overview-main.md](update-program-overview-main.md) | Federated Graphql Migration — Product (main/landing) | `1313880343` | `finalArtifacts/00-overview.md` |
| [update-complex-scenarios.md](update-complex-scenarios.md) | Federated GraphQL Migration — Product — Complex Scenarios | `1313880475` | 9× `output/complexStories/<case>/00-overview.md` + `01-adr-*.md` |
| [update-breakdown-overview.md](update-breakdown-overview.md) | Federated GraphQL Stories Breakdown — Overview | `1313880187` | `output/summary/Federated+Graphql+Stories+-+BreakDown.md` |
| [update-breakdown-bom.md](update-breakdown-bom.md) | Federated GraphQL Breakdown — Bill of Materials (BOM) | `1313880240` | `finalArtifacts/summary/bom/FederatedGqlBreakDown-bom.md` |
| [update-breakdown-claims.md](update-breakdown-claims.md) | Federated GraphQL Breakdown — Claims | `1313880249` | `finalArtifacts/summary/claims/FederatedGqlBreakDown-claims.md` |
| [update-breakdown-impression.md](update-breakdown-impression.md) | Federated GraphQL Breakdown — Impression | `1313880252` | `finalArtifacts/summary/impression/FederatedGqlBreakDown-impression.md` |
| [update-breakdown-measurement.md](update-breakdown-measurement.md) | Federated GraphQL Breakdown — Measurement | `1313880256` | `finalArtifacts/summary/measurement/FederatedGqlBreakDown-measurement.md` |
| [update-breakdown-packaging.md](update-breakdown-packaging.md) | Federated GraphQL Breakdown — Packaging | `1313880264` | `finalArtifacts/summary/packaging/FederatedGqlBreakDown-packaging.md` |
| [update-breakdown-product.md](update-breakdown-product.md) | Federated GraphQL Breakdown — Product | `1313880281` | `finalArtifacts/summary/product/FederatedGqlBreakDown-product.md` |
| [update-breakdown-product-details.md](update-breakdown-product-details.md) | Federated GraphQL Breakdown — Product Details | `1313880287` | `finalArtifacts/summary/productDetails/FederatedGqlBreakDown-productDetails.md` |
| [update-breakdown-watchlist.md](update-breakdown-watchlist.md) | Federated GraphQL Breakdown — Watchlist | `1313880299` | `finalArtifacts/summary/watchlist/FederatedGqlBreakDown-watchlist.md` |

### New pages (create first time, then update-in-place by title — no id yet)

| Prompt | Confluence page | Source in repo |
|---|---|---|
| [publish-order-sequencing.md](publish-order-sequencing.md) | Migration Order & Sequencing — Backend + Frontend | `finalArtifacts/00-order-sequencing.md` |
| [publish-external-dependencies.md](publish-external-dependencies.md) | External & Cross-Domain Dependencies | `finalArtifacts/00-external-dependencies.md` |

These two are assembled from the generated plan docs + the codebase-validated dependency data; they
nest under the same program landing page (`1313880343`) and cross-link each other. Publish them
together.

All pages live in the **PPDE** space: `https://confluence.target.com/spaces/PPDE/...`.

## Order to run (matches the parent-child structure)

1. **Main / overview** — `update-program-overview-main.md` (the landing page).
2. **Breakdown overview** — `update-breakdown-overview.md` (the "followed by domain breakdown" parent).
3. **Each domain breakdown** — the 8 `update-breakdown-<domain>.md` prompts (independent of each other;
   run in any order, one at a time so each is individually reviewable).
4. **Complex scenarios** — `update-complex-scenarios.md` (the deep architectural page).

Nothing here depends on running the others first — but keeping this order means a reader following the
overview's outbound links always lands on an already-refreshed child.

## Prerequisite (same as the generalized prompts)

Your Copilot/Claude integration must have **Confluence write access** to the PPDE space (an MCP server,
plugin, or connector). Confirm before running — ask your assistant to list its Confluence actions. If
it can only read, each prompt still works as a **content-preparation step**: it produces the exact
Confluence-ready structure for you to paste into the page editor by hand.

---
*Ready-made Confluence update prompts · output/prompts/confluence/readymade/README.md*
