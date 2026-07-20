# Prompt — Implement a Phase G story (Field Resolvers & Utils)
# Model: Claude Sonnet (GitHub Copilot)

> **Phase G** = field-level resolvers and small utility work, often involving a multi-source merge or a
> shared enrichment pattern from a ratified ADR. Worked example: **`PRODUCT-BE-G-01`** —
> `Product.attachmentsWithMetaData`, a 5-source merge (files + discussions + threads + samples) behind
> a shared enrichment library (ADR-018). Full story text:
> [`output/analysis/product/be-04-stories.md`](../../analysis/product/be-04-stories.md) (search `### PRODUCT-BE-G-01`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>`.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo. Read the full story section first. If the story references a "Pattern (draft ADR-NNN...)"
or similar, read that ADR before writing code — several Phase G stories are the FIRST implementation of
a shared library other stories will later plug into as "thin doors," so getting the shared piece right
here matters beyond just this one story.

For PRODUCT-BE-G-01 specifically:
1. Implement AttachmentEnrichmentService as a Kotlin port of the existing ~150-line resolver logic:
   one relationshipClient.searchByIds call (replacing the old N+1 graph walk — this is an explicit,
   accepted behavior CHANGE, not a bug to avoid), partition into 5 buckets, hydrate each bucket via its
   own client (parallel independent fetches per ADR-018's accepted deviations), merge, filter drafts,
   sort by type-rank then recency-descending.
2. Build this as the shared library + the product policy row per ADR-018 (see
   output/complexStories/attachments-enrichment/01-adr-attachments-enrichment.md §4) — not a
   product-only one-off — since the story explicitly says other domains' equivalent stories become
   "thin doors" onto this same library.
3. Keep the "ACL should own draft filtering" TODO as a documented follow-up, not something to solve
   inline in this story — the story explicitly scopes that out.
4. The mandatory fixes (parallel independent fetches, guarded thread→parent-discussion lookup, direct
   discussion client) are ACCEPTED DEVIATIONS from current behavior per the ADR — implement them, don't
   preserve the old sequential/indirect behavior "for safety."

Implement against every numbered Acceptance Criterion.
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) for this field resolver — required for every Phase G story:

- File: src/test/groovy/<package>/AttachmentEnrichmentServiceSpec.groovy.
- Mock each of the 4 hydration clients (attachmentClient, discussionClient, sampleClient, and the
  relationshipClient for the initial searchByIds) individually with Spock `Mock()`.
- A merge-and-sort test: given fixtures for all 5 buckets with deliberately interleaved createdAt
  timestamps and types, assert the final list is sorted by type-rank first, then by createdAt
  descending within the same rank — this is the actual behavior parity tests need to check, not just
  "the list is non-empty."
- A draft-filter test: given a fixture item with isDraft = true, assert it's excluded from the result.
- A test for the ACCEPTED DEVIATION explicitly: assert the 4 hydration calls happen independently
  (e.g. via Spock's interaction verification showing they're not sequentially dependent on each other's
  results) rather than asserting the OLD sequential-graph-walk shape — a test written against the old
  behavior would be actively wrong for this story.
- Do not write a test asserting ACL performs draft filtering — that's explicitly out of scope, tracked
  as a follow-up, not this story's behavior.

Report the finished spec's file path and confirm the merge/sort test and the parallel-fetch test both
exist as their own named test methods.
```

---
*Implement prompt — Phase G · output/prompts/implement/phase-G-field-resolvers-utils-claude-sonnet.md*
