# Prompt — Implement a Phase H story (Entity Resolution — cross-subgraph)
# Model: Claude Sonnet (GitHub Copilot)

> **Phase H** = a field genuinely owned by a DIFFERENT subgraph — `@DgsEntityFetcher`/`@key` extensions.
> Always check for a `Blocked by:` line before starting (see
> [`output/analysis/program/cross-domain-dependencies.md`](../../analysis/program/cross-domain-dependencies.md)).
> Worked example: **`PRODUCT-BE-H-06`** — the `Product` entity fetcher, required before ANY external
> subgraph (today: claims) can turn a bare `Product{id}` reference into a full product. Full story text:
> [`output/analysis/product/be-04-stories.md`](../../analysis/product/be-04-stories.md) (search `### PRODUCT-BE-H-06`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>`.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo. BEFORE starting: check this story's "Blocked by:" line (if present) against
output/analysis/program/cross-domain-dependencies.md — if it names a subgraph that isn't live yet,
this story is not startable regardless of how ready the code looks; flag it and stop, don't implement
speculatively against an unstable external schema.

Read output/overview/01-architecture-diagrams.md §2 for the general request-time sequence every Phase H
story follows (gateway resolves the @key shell in the defining subgraph, then calls _entities on the
OWNING subgraph) before writing code — this shape is the same across every Phase H story; only the
owning subgraph and field name change.

For PRODUCT-BE-H-06 specifically:
1. Implement @DgsEntityFetcher(name = "Product") -> productService.getById(id), reusing the EXISTING
   B-01 service path (this story explicitly reuses infrastructure, not building new lookup logic).
2. Put it behind a DataLoader so multiple representations in one _entities call become ONE batched
   backend call, not N — this is an explicit Acceptance Criterion, not an optimization nice-to-have.
3. Null-tolerant per the federation spec: an unknown id yields a null entry in the result list, and
   does NOT throw or fail the whole _entities response — a single bad reference must not break every
   other entity in the same batch.
4. No ACL plumbing — the story explicitly scopes this out; don't add a permission check here.

Implement against every numbered Acceptance Criterion.
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) for this entity fetcher — required for every Phase H story:

- File: src/test/groovy/<package>/ProductEntityFetcherSpec.groovy.
- Mock productService (or its DataLoader wrapper) with Spock `Mock()`.
- A BATCHING test: given a representations list with 2+ ids, assert productService is called EXACTLY
  ONCE (`1 * productService.getByIds(...)`, or however your DataLoader batches) — not once per id. This
  is the single most important behavior this story adds; a test that only checks single-id correctness
  would miss the actual point of the story.
- A NULL-TOLERANCE test: given a representations list where one id doesn't exist, assert the result
  list has a null entry AT THAT POSITION and valid Product entries at the others — and that no
  exception propagates out of the fetcher for the whole batch.
- An END-TO-END shape test: given a fixture representations list matching the story's own example
  (`_entities(representations: [{__typename:"Product", id:"PID1"}, ...])`), assert the returned shape
  matches what the federation spec expects (ordered list, same length as input, each entry either the
  hydrated type or null).
- Do not add an ACL/permission-check test — the story explicitly says none is introduced; a test
  asserting ACL behavior here would be testing something this story deliberately doesn't do.

Report the finished spec's file path and confirm the batching test explicitly asserts a single
downstream call for a multi-id batch (not just "it returns the right data").
```

---
*Implement prompt — Phase H · output/prompts/implement/phase-H-entity-resolution-claude-sonnet.md*
