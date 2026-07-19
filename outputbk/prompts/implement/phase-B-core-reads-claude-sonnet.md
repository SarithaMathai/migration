# Prompt — Implement a Phase B story (Core Reads)
# Model: Claude Sonnet (GitHub Copilot)

> **Phase B** = `@DgsQuery` reads, thin wrappers over an existing REST/service call. Worked example:
> **`PRODUCT-BE-B-01`** — `getProduct(id)`, which also lands the one-time DGS module scaffold every
> other story in the domain depends on implicitly. Full story text:
> [`output/analysis/product/be-04-stories.md`](../../analysis/product/be-04-stories.md) (search `### PRODUCT-BE-B-01`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>`.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo. Read the full story section first — Current Behaviour, Target, Files/Dependencies,
Acceptance Criteria.

For PRODUCT-BE-B-01 specifically:
1. If this is the domain's first story (check whether the domain's DGS module scaffold already
   exists): add the one-time scaffold — the domain's .graphqls schema file, scalar registration in
   ScalarConfig.kt, and the service + Feign client wiring. This is a prerequisite every other story
   in the domain silently depends on, even though it won't appear in their own "Depends On" column
   (per the domain doc's own note on why B-01 isn't listed as a dependency elsewhere).
2. Add the getProduct(id: ID!): Product query to the schema.
3. Add a @DgsQuery data fetcher that calls the EXISTING Kotlin service method / REST controller —
   do not write a new service layer; this program's model is "thin DGS wrapper over what already
   exists," not a service-layer rewrite.
4. Push the schema change to the Hive registry as part of this same PR (per the self-contained-story
   model — schema + fetcher + service call + Hive push, one PR, no separate service-layer story).

Implement against every numbered Acceptance Criterion — typically parity with the existing REST
response shape, not a redesign of the response.
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) for this query's data fetcher — required for every Phase B story:

- File: src/test/groovy/<package>/GetProductDataFetcherSpec.groovy (name after your actual fetcher class).
- Structure: given/when/then blocks, not JUnit-style assertions — this is a Spock convention, keep to it.
- Mock the underlying service/REST client with Spock's `Mock()` — verify the data fetcher calls it with
  the right arguments (`1 * productService.getById(id)`), then asserts the DGS response shape maps the
  service's return value field-for-field.
- Add a **parity test**: given a fixture representing the CURRENT REST response for a known id, assert
  the new DGS query returns the same field values — every Phase B story's real acceptance bar is "same
  answer as before," so this test is not optional polish, it's the actual spec.
- Cover the not-found case (nonexistent id) and confirm the DGS-appropriate null/error shape, matching
  whatever the story's Acceptance Criteria says about that case (if the story is silent on it, ask
  before inventing behavior — don't guess).
- Do NOT write a Spock test for the one-time scaffold itself (ScalarConfig.kt wiring, Feign client
  registration) — that's infrastructure, not business logic; test the query behavior it enables.

Report the finished spec's file path and which Acceptance Criteria each test method covers.
```

---
*Implement prompt — Phase B · output/prompts/implement/phase-B-core-reads-claude-sonnet.md*
