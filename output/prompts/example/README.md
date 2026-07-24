# Prompt examples

> Worked examples for every prompt in [`output/prompts/jira/`](../jira/) and
> [`output/prompts/confluence/`](../confluence/) — the prompt text with placeholders filled in, plus
> a realistic sample of the agent's dry-run and post-publish/post-push response, so you can see the
> whole expected interaction before running the real prompt.

## Shared example values

Every example uses the same consistent scenario, so they read as one coherent worked run rather than
10 unrelated fill-ins:

| Placeholder | Value | Why |
|---|---|---|
| `<DOMAIN>` | `watchlist` | Smallest phase-1 domain (13 backend + 3 frontend stories) — full output fits without truncation |
| `<PROJECT_KEY>` | `PROJ` | Example Jira project key |
| `target-corp/saritha-mathai-repositories-research` | `target-corp/saritha-mathai-repositories-research` | Example GitHub org/repo — replace with the real one in actual use |
| `<PARENT_PAGE>` | `https://confluence.com/Breakdown` | Example Confluence parent page |
| `<STORY_ID>` | `WATCHLIST-BE-B-01` (simple, no deps) or `WATCHLIST-BE-E-01` (has a spike gate + cross-domain dependency) | Used where a single-story example is needed — picked to show both the trivial and the interesting case |

All story data, row counts, table counts, and heading counts in these examples are taken from the
**real generated files** as of 2026-07-21 (`finalArtifacts/jira/watchlist.csv`,
`finalArtifacts/summary/watchlist/*.md`, `finalArtifacts/00-overview.md`,
`finalArtifacts/00-sequencing.md`, `output/summary/Federated+Graphql+Stories+-+BreakDown.md`) — not
fabricated placeholder numbers. If you regenerate the pipeline, these counts may drift slightly; the
*shape* of the interaction (dry-run manifest → approval → publish/push → verification) stays the same.

**What's fabricated vs. real:** the prompt text, source-file structure, and manifest counts are real.
The Jira keys (`PROJ-403`, etc.), Confluence page IDs/URLs, and version numbers in the "sample agent
response" sections are illustrative — your actual run will get different keys/URLs from your own
Jira/Confluence instance.

## [jira/](jira/) — 5 examples

| Example | Scenario |
|---|---|
| [push-domain-all-stories.example.md](jira/push-domain-all-stories.example.md) | First-time import of all 16 watchlist rows (13 BE + 3 FE) |
| [push-domain-phase.example.md](jira/push-domain-phase.example.md) | Just Phase G (4 field-resolver stories) of watchlist |
| [push-one-story.example.md](jira/push-one-story.example.md) | Create WATCHLIST-BE-B-01 (simplest real story — no dependencies) |
| [push-specific-stories.example.md](jira/push-specific-stories.example.md) | A hand-picked cross-domain list (2 watchlist + 1 bom story) |
| [update-story-in-epic.example.md](jira/update-story-in-epic.example.md) | Refresh WATCHLIST-BE-E-01 (Jira key unknown) after its Acceptance Criteria changed upstream |

## [confluence/](confluence/) — 5 examples

| Example | Scenario |
|---|---|
| [publish-program-overview.example.md](confluence/publish-program-overview.example.md) | First-time publish of the program overview page |
| [publish-sequencing.example.md](confluence/publish-sequencing.example.md) | First-time publish of the Migration Sequencing & Roadmap page (the largest page — 17 tables, 332 total rows) |
| [publish-program-breakdown-full.example.md](confluence/publish-program-breakdown-full.example.md) | First-time publish of the full program spike-register page |
| [publish-domain-breakdown.example.md](confluence/publish-domain-breakdown.example.md) | First-time publish of Watchlist's breakdown page (publish this before the FE-readiness one below) |
| [publish-dependency-graph.example.md](confluence/publish-dependency-graph.example.md) | Publish Watchlist's FE-Readiness page as the breakdown page's sibling, updating `confluence-page-map.csv` |

---
*Prompt examples index · output/prompts/example/README.md*
