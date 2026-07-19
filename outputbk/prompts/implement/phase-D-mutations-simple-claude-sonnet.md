# Prompt — Implement a Phase D story (Mutations, simple)
# Model: Claude Sonnet (GitHub Copilot)

> **Phase D** = straightforward writes — create/update/delete, sometimes with an optional copy or a
> cross-domain association step. Worked example: **`PRODUCT-BE-D-01`** — `addProduct` (create, optional
> copy, workspace association via the shared `associate()` component from ADR-011). Full story text:
> [`output/analysis/product/be-04-stories.md`](../../analysis/product/be-04-stories.md) (search `### PRODUCT-BE-D-01`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>`.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo. Read the full story section first. If the story's body references a complex-case ADR
(look for a markdown link into output/complexStories/<case>/01-adr-*.md), read that ADR BEFORE writing
any code — Phase D stories very often point at a shared component (association, saga) that already has
a ratified shape; writing your own bespoke version of it is the single most common mistake here.

For PRODUCT-BE-D-01 specifically:
1. Implement @DgsMutation addProduct(workspaceId, sparkProduct, copyProduct): Product.
2. Orchestrate create → optional copy → workspace association using the SHARED association component
   from ADR-011 Option B (see output/complexStories/cross-domain-association/01-adr-cross-domain-association.md)
   — do not write bespoke per-mutation fan-out code; call the shared component.
3. Failure-after-create (link or copy fails) surfaces per the mutation's declared failure policy —
   ADR-011 §4 default is fail-fast, no rollback. This is a DELIBERATE accepted behavior, not a gap to
   silently "fix" with a rollback you invent — implementing automatic rollback here would fail the
   story's actual intent even though it looks like an improvement.

Implement against every numbered Acceptance Criterion.
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) for this mutation — required for every Phase D story:

- File: src/test/groovy/<package>/AddProductDataFetcherSpec.groovy.
- Mock the shared association component (not a hand-rolled fan-out) with Spock `Mock()` — assert the
  mutation calls INTO the shared component with the right arguments, rather than re-testing the
  component's own internals here (that belongs to the component's own spec).
- Cover: (a) create only, no copy, no workspace assoc; (b) create + copy; (c) create + workspace assoc
  via the shared component; (d) all three combined — a `where:` table works well for this AC.
- Add the failure-policy test the story's AC explicitly asks for: given the association/copy call
  throws, assert the mutation surfaces the failure per the DECLARED policy (fail-fast, no silent
  swallow, and — per ADR-011 — no rollback attempted). A test that expects a rollback here would be
  testing the wrong behavior; write the test the ADR actually specifies, not what "feels safer."
- Add a parity check for the "create only" path against the pre-migration REST response shape.

Report the finished spec's file path, and explicitly confirm the failure-policy test matches the ADR's
documented behavior rather than an invented rollback.
```

---
*Implement prompt — Phase D · output/prompts/implement/phase-D-mutations-simple-claude-sonnet.md*
