# Prompt — Implement a Phase C story (Search & Listing)
# Model: Claude Opus (GitHub Copilot)

> **Phase C** = search/listing operations, often combining two data sources (search index + canonical
> record). Worked example: **`PRODUCT-BE-C-01`** — `getProducts(...)` two-stage hydration (elastic search
> for ids/flags, then canonical DB for full records, then merge). Full story text:
> [`output/analysis/product/be-04-stories.md`](../../analysis/product/be-04-stories.md) (search `### PRODUCT-BE-C-01`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>`.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo. Read the full story section first, INCLUDING any "Depends on: S-NN" spike reference —
Phase C stories are frequently gated on an open design spike; check output/complexStories/ or the
domain's own Phase-0 note for that spike's ratified/pending status before assuming the "safe default"
described in the story is what to build.

For PRODUCT-BE-C-01 specifically:
1. Implement getProducts as a two-stage read: call the search/elastic service first for matching ids
   + flags (has-boms, has-claims, workspace membership, etc.), then call the canonical product read
   path for the full records, then merge the elastic flags onto the canonical records.
2. Preserve EVERY boolean default exactly as documented (?? true defaults) — the story explicitly
   flags these as easy to silently change; pin them in code AND in tests.
3. This story's "Target" is explicitly PROVISIONAL pending PRODUCT-BE-S-02's outcome — implement the
   documented safe-default shape now (preserves today's two-call behavior) so the story isn't blocked
   on the spike's timeline, but leave the workspace-filter placement and staleness handling as the one
   thing you'd revisit once S-02 concludes. Do not silently redesign this before that spike ratifies.

Implement against every numbered Acceptance Criterion, including the explicit "4 arg combos" parity
requirement — that's not filler, it's the actual regression surface for this kind of story.
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) for this listing query — required for every Phase C story:

- File: src/test/groovy/<package>/GetProductsDataFetcherSpec.groovy.
- Mock BOTH backing clients separately (search/elastic client AND canonical read client) with Spock
  `Mock()` — Phase C's defining risk is the merge logic between two sources, so the test must prove
  the merge, not just that either call happened.
- Use a `where:` table for the "4 arg combos" the story's AC calls out explicitly (no flags / all
  flags / resourceType=workspaces / filter array present) — one test method, four data rows, not four
  separate copy-pasted methods.
- Add an explicit boolean-default test: call the fetcher with the flag arguments OMITTED and assert
  the ?? true defaults were actually applied — this guards exactly the regression the story's prose
  warns about ("truthy defaults — pin in tests").
- Add a merge-correctness test: given a canonical record fixture and an elastic-flags fixture with
  DIFFERENT values for the same product id, assert the final result has the elastic flags merged onto
  the canonical fields (not overwritten, not dropped) — this is the two-stage-hydration behavior this
  whole story exists to implement.
- Add a parity fixture test against the CURRENT (pre-migration) response shape for at least one of the
  4 arg combos.

Report the finished spec's file path and confirm all 4 arg combos + the default-truthiness case have
their own test coverage.
```

---
*Implement prompt — Phase C · output/prompts/implement/phase-C-search-listing-claude-opus.md*
