# Prompts

> Copy-paste prompt templates for the four recurring actions in this migration: pushing stories to
> Jira, publishing curated planning docs to Confluence, implementing a story with its required test
> coverage, and regenerating artifacts. Each prompt names its prerequisites and what to replace before
> running it.
>
> **Using GitHub Copilot?** Every prompt below has a native `.prompt.md` counterpart under
> [`.github/prompts/`](../../.github/prompts/) (repo root) — invoke with `/prompt-name` in Copilot
> Chat instead of copy-pasting from here. [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md)
> has the repo-wide publishing context (the three-tier model, formatting contract, hard rules) that
> every Copilot prompt assumes.

## [jira/](jira/) — push stories to Jira

| Prompt | Use when |
|---|---|
| [push-domain-all-stories.md](jira/push-domain-all-stories.md) | Every story (BE+FE) for one domain, dry-run first |
| [push-domain-phase.md](jira/push-domain-phase.md) | Just one phase letter (A–H) of one domain, e.g. "BOM's Phase E only" |
| [push-one-story.md](jira/push-one-story.md) | A single story, create-or-update |
| [push-specific-stories.md](jira/push-specific-stories.md) | A hand-picked list of story ids across domains |
| [update-story-in-epic.md](jira/update-story-in-epic.md) | Update-only: you know the Story ID + epic name but not the Jira key — finds the issue within that epic and refreshes it from source, never creates |

All five assume a Jira MCP connection (or Copilot's own Jira tools) and follow the field-mapping,
GitHub-link, and Confluence-cross-link rules in
[`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).
Source: `finalArtifacts/jira/{domain}.csv` / `all-stories.csv` — **8 phase-1 domains** (product, bom,
claims, measurement, impression, productDetails, packaging, watchlist).

**Content model:** every prompt's Jira description is **Acceptance Criteria + a back-link, nothing
else** — Current Behaviour, Target implementation, and Test Cases stay on GitHub in
`be-04-stories.md` and are linked to, never copied into the ticket. Each prompt rewrites the CSV's
relative `Full story:` reference into a real GitHub blob URL, and adds a `Domain overview:` link to
that domain's Confluence page if `finalArtifacts/jira/confluence-page-map.csv` has one.

**Copilot-native versions** (with `${input:}` placeholders, invoke via `/prompt-name`) live under
[`.github/prompts/jira/`](../../.github/prompts/jira/). A lighter-model variant (smaller batches,
explicit ID→key bookkeeping) is in [`fedMigrationScripts/docs/PUSH-TO-JIRA-HAIKU.md`](../../fedMigrationScripts/docs/PUSH-TO-JIRA-HAIKU.md).

**How dependencies work (read once, applies to all 5):** each story's real dependency data lives in
`output/analysis/<domain>/be-04-stories.md` as a `Depends on:` / `Blocked by:` line; the Jira CSV's
"Depends On" column is a flattened copy of the same thing. A bare id like `A-04` means "same domain";
a full id like `BOM-BE-A-04` in another domain's CSV is cross-domain; an id like `SPIKE-07` is a
program-wide research spike (not a story) and isn't safely startable until its decision is ratified —
see [`finalArtifacts/00-overview.md`](../../finalArtifacts/00-overview.md) and
[`output/summary/Federated+Graphql+Stories+-+BreakDown.md`](../summary/Federated+Graphql+Stories+-+BreakDown.md)
§"Phase 0 — Program Spikes" for status. The full pre-compiled cross-domain edge list is
[`output/analysis/program/cross-domain-dependencies.md`](../analysis/program/cross-domain-dependencies.md)
— check there before re-deriving an edge by hand. A domain's
`finalArtifacts/summary/{domain}/story-dependency-graph-{domain}.md` shows the same picture visually
for what gates each FE story. `push-domain-phase.md` has the fullest version of the dependency
explanation if you want the detail inline in a prompt.

**Excluded stories:** a few stories are documented in `be-04-stories.md` but deliberately not
imported to Jira (different team owns the work) — see `JIRA_EXCLUDED_STORIES` in `generate_jira.py`
and `output/analysis/out-of-scope-backlog.md` §"Excluded from Jira" before assuming a missing story
is a generation bug.

## [confluence/](confluence/) — publish curated planning docs

Source root is `finalArtifacts/` (repo root, already-trimmed for publishing), not `output/summary/`
directly. Full page list, titles, and parent structure:
[`CONFLUENCE-INVENTORY.md`](../../fedMigrationScripts/reference/CONFLUENCE-INVENTORY.md).

| Prompt | Use when |
|---|---|
| [publish-program-overview-claude-sonnet.md](confluence/publish-program-overview-claude-sonnet.md) | Publish the program overview page (`finalArtifacts/00-overview.md`) — what/why, totals, domain-at-a-glance — run once |
| [publish-sequencing-claude-sonnet.md](confluence/publish-sequencing-claude-sonnet.md) | Publish the Migration Sequencing & Roadmap page (`finalArtifacts/00-sequencing.md`) — build order, per-domain step + story-sequence tables — run once |
| [publish-program-breakdown-full-claude-sonnet.md](confluence/publish-program-breakdown-full-claude-sonnet.md) | Publish the fuller global page with the full program spike register + per-spike detail (`output/summary/Federated+Graphql+Stories+-+BreakDown.md`) — companion to the overview, run once |
| [publish-domain-breakdown-claude-sonnet.md](confluence/publish-domain-breakdown-claude-sonnet.md) | Publish or re-sync one domain's merged BE+FE breakdown page, zero data/format loss — repeat once per domain |
| [publish-dependency-graph-claude-sonnet.md](confluence/publish-dependency-graph-claude-sonnet.md) | Publish one domain's FE-Readiness dependency graph (mermaid, one diagram per FE story) — repeat once per domain, right after that domain's breakdown page |

All five are model-agnostic content-preparation prompts (Sonnet named as the tested default; Opus
optional for the longest pages) — usable via Copilot + org Claude, or any Copilot/Claude integration
with Confluence access. **Copilot-native versions** (with `${input:}` placeholders, invoke via
`/prompt-name`) live under [`.github/prompts/confluence/`](../../.github/prompts/confluence/).

**Confluence → Jira handoff:** the domain breakdown and dependency-graph prompts write/update a row in
`finalArtifacts/jira/confluence-page-map.csv` after publishing — the Jira prompts read this file to
link each story ticket back to its domain's Confluence page. Publish Confluence before Jira for a
first import, or the Jira prompts will note the link is missing and proceed without it.

## [implement/](implement/) — implement a story, phase by phase

One prompt per phase letter, each anchored to one real story as a worked example, and each ending
with a required Spock (Groovy) test-writing instruction specific to that phase's risk shape. Model
picked per phase: Sonnet where the story is mechanical/explicit, Opus where it's spike/ADR-gated or
has an ordering/correctness invariant (see Model column).

| Phase | Prompt | Model | Worked example |
|---|---|---|---|
| A — Foundation & Type Resolvers | [phase-A-foundation-type-resolvers-claude-sonnet.md](implement/phase-A-foundation-type-resolvers-claude-sonnet.md) | Sonnet | `BOM-BE-A-04` |
| B — Core Reads | [phase-B-core-reads-claude-sonnet.md](implement/phase-B-core-reads-claude-sonnet.md) | Sonnet | `PRODUCT-BE-B-01` |
| C — Search & Listing | [phase-C-search-listing-claude-opus.md](implement/phase-C-search-listing-claude-opus.md) | Opus (spike-provisional) | `PRODUCT-BE-C-01` |
| D — Mutations (simple) | [phase-D-mutations-simple-claude-sonnet.md](implement/phase-D-mutations-simple-claude-sonnet.md) | Sonnet | `PRODUCT-BE-D-01` |
| E — Complex Operations | [phase-E-complex-operations-claude-opus.md](implement/phase-E-complex-operations-claude-opus.md) | Opus (saga/ordering) | `PRODUCT-BE-E-01` |
| F — Federation & Stitching | [phase-F-federation-stitching-claude-opus.md](implement/phase-F-federation-stitching-claude-opus.md) | Opus (supergraph-safety) | `PRODUCT-BE-F-10` |
| G — Field Resolvers & Utils | [phase-G-field-resolvers-utils-claude-sonnet.md](implement/phase-G-field-resolvers-utils-claude-sonnet.md) | Sonnet | `PRODUCT-BE-G-01` |
| H — Entity Resolution | [phase-H-entity-resolution-claude-sonnet.md](implement/phase-H-entity-resolution-claude-sonnet.md) | Sonnet | `PRODUCT-BE-H-06` |

Swap in your own `<STORY_ID>`/`<DOMAIN>` — the worked example shows the pattern, not a fixed target.

## [scripts/](scripts/) — regenerate artifacts

| Prompt | Use when |
|---|---|
| [regenerate-one-domain.md](scripts/regenerate-one-domain.md) | You edited one domain's stories; refresh its own roll-ups |
| [regenerate-multiple-domains.md](scripts/regenerate-multiple-domains.md) | A named subset of domains, or the whole program (all domains + program-wide roll-ups) |
| [bootstrap-new-domain.md](scripts/bootstrap-new-domain.md) | Starting a brand-new domain (e.g. `sample`) from scratch — **not** a one-shot script; authors the upstream analysis first, then wires it in, then regenerates |
| [per-client-file-story-view.md](scripts/per-client-file-story-view.md) | One Markdown report per `ClientCallingGqlQueries/*.txt` file — operations, existing BE/FE story ids, field diffs, dependency graph. A VIEW over `fe-03`/`fe-11`, reuses existing story ids — does not renumber or invent new ones |

---
*Prompts index · output/prompts/README.md*
