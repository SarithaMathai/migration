# Prompts

> Copy-paste prompt templates for the four recurring actions in this migration: pushing stories to
> Jira, publishing breakdown pages to Confluence, implementing a story with its required test coverage,
> and regenerating artifacts. Each prompt names its prerequisites and what to replace before running it.

## [jira/](jira/) — push stories to Jira

| Prompt | Use when |
|---|---|
| [push-domain-all-stories.md](jira/push-domain-all-stories.md) | Every story (BE+FE) for one domain, dry-run first |
| [push-domain-phase.md](jira/push-domain-phase.md) | Just one phase letter (A–H) of one domain, e.g. "BOM's Phase E only" |
| [push-one-story.md](jira/push-one-story.md) | A single story, create-or-update |
| [push-specific-stories.md](jira/push-specific-stories.md) | A hand-picked list of story ids across domains |
| [update-story-in-epic.md](jira/update-story-in-epic.md) | Update-only: you know the Story ID + epic name but not the Jira key — finds the issue within that epic and refreshes it from source, never creates |

All five assume a Jira MCP connection and follow the field-mapping/formatting rules in
[`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).

**How dependencies work (read once, applies to all 5):** each story's real dependency data lives in
`output/analysis/<domain>/be-04-stories.md` as a `Depends on:` / `Blocks:` line; the Jira CSV's
"Depends On" column is a flattened copy of the same thing. A bare id like `A-04` means "same domain";
a full id like `BOM-BE-A-04` in another domain's CSV is cross-domain; an id like `SPIKE-01` is a
program-wide research spike (not a story) and isn't safely startable until its decision is ratified —
see [`output/summary/Federated+Graphql+Stories+-+BreakDown.md`](../summary/Federated+Graphql+Stories+-+BreakDown.md)
§"Phase 0 — Program Spikes" for status. The full pre-compiled cross-domain edge list is
[`output/analysis/program/cross-domain-dependencies.md`](../analysis/program/cross-domain-dependencies.md)
— check there before re-deriving an edge by hand. `push-domain-phase.md` has the fullest version of
this explanation if you want the detail inline in a prompt.

## [confluence/](confluence/) — publish breakdown pages

| Prompt | Use when |
|---|---|
| [publish-domain-breakdown-claude-sonnet.md](confluence/publish-domain-breakdown-claude-sonnet.md) | Publish or re-sync one domain's merged BE+FE breakdown page, zero data/format loss — repeat once per domain (standalone version for exporting to a repo with no Claude Code — Copilot + org Claude, Sonnet; transcription task, not judgment-call) |
| [publish-program-overview-claude-sonnet.md](confluence/publish-program-overview-claude-sonnet.md) | Publish the single program-wide overview page (`Federated+Graphql+Stories+-+BreakDown.md`) — zero data/format loss, Sonnet, standalone |

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
