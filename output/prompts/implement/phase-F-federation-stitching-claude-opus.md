# Prompt — Implement a Phase F story (Federation & Stitching)
# Model: Claude Opus (GitHub Copilot)

> **Phase F** = platform/gateway work that stays INSIDE one subgraph — schema composition, contract
> alignment, facade retirement, platform stub verification. Not cross-subgraph entity resolution (that's
> Phase H — see that prompt instead if your story is a `@DgsEntityFetcher`/`@key` extension owned by a
> *different* subgraph). Worked example: **`PRODUCT-BE-F-10`** — Hive Gateway supergraph composition.
> Full story text: [`output/analysis/product/be-04-stories.md`](../../analysis/product/be-04-stories.md)
> (search `### PRODUCT-BE-F-10`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>`.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo (or the gateway/composition repo, if this story is gateway-level rather than
subgraph-level — check the story's "Type" field). Read the full story section first, and confirm every
story it "Depends on" (often other F-phase contract-alignment stories) has actually landed — Phase F
stories are frequently the last-mile gate before a subgraph can serve any federated query at all, so
starting one out of order can silently produce a broken supergraph, not just an incomplete feature.

For PRODUCT-BE-F-10 specifically:
1. Register the plm-product subgraph URL with the Hive Gateway.
2. Verify composition succeeds with no conflicting type definitions and no missing @key fields against
   every already-registered subgraph (VMM/IG/CORONA/Doppler stubs named in the story).
3. Run a cross-subgraph smoke query end-to-end (the story gives a concrete example query) and confirm
   it resolves cleanly.
4. Wire composition into CI as a standing gate on every schema change — this is explicit in the AC
   ("runs as a CI gate... not a one-off") — a manual one-time compose check does not satisfy this story.
5. Confirm the specific contract alignments the story calls out by name (e.g. entity key field names,
   type name alignment across domains) are actually zero — don't approximate this, enumerate each one
   named in the AC and check it individually.

Implement against every numbered Acceptance Criterion.
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) for this composition/contract-alignment story — required for every
Phase F story, adapted to what's actually testable at this layer:

- File: src/test/groovy/<package>/SupergraphCompositionSpec.groovy (or wherever your CI-gate test
  harness lives — Phase F stories often test schema/contract properties, not runtime business logic).
- If the story is CI-gate-shaped (like F-10): write a Spock spec that invokes the actual composition
  check programmatically (not just "runs the CLI and checks exit code" — call into the composition
  library/tool's API if one exists) and asserts on the structured error list it returns, so a future
  regression produces a readable Spock failure, not just a red CI job.
- Include one test per specific contract mismatch the story's AC calls out by name (e.g. "every entity
  keyed by id" — assert this against the actual schema definitions, not a hardcoded fixture that could
  drift from the real schema).
- Include a smoke-query test: given the composed schema (or a representative stub), execute the exact
  cross-subgraph query example from the story and assert it resolves without composition errors.
- If the story is genuinely CI-infrastructure with no unit-testable business logic (e.g. "stub
  verification" stories), say so explicitly rather than writing a hollow test — propose an integration-
  test or contract-test approach instead and flag it for review rather than forcing a Spock spec where
  it doesn't fit.

Report the finished spec's file path, or, if you determined Spock doesn't fit this particular story,
explain why and what you're proposing instead.
```

---
*Implement prompt — Phase F · output/prompts/implement/phase-F-federation-stitching-claude-opus.md*
