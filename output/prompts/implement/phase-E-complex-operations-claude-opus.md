# Prompt — Implement a Phase E story (Complex Operations)
# Model: Claude Opus (GitHub Copilot)

> **Phase E** = multi-step orchestrated writes, partner actions, TechPack aggregation — the highest-risk
> phase, usually gated on a spike and/or built on the shared `WriteSaga` module. Worked example:
> **`PRODUCT-BE-E-01`** — `productBusinessPartnerActions` (REMOVE/DROP/UNDROP), a ~220-line dispatcher
> that fans out to 4 cleanup services with no rollback today, orchestrated via `WriteSaga` per ADR-013.
> Full story text: [`output/analysis/product/be-04-stories.md`](../../analysis/product/be-04-stories.md)
> (search `### PRODUCT-BE-E-01`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>`.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo. Phase E stories are usually gated on BOTH a spike's outcome AND the shared WriteSaga
module — read the story's "Depends on:" line carefully; if it names an "S-NN" spike, confirm that
spike's decision is actually ratified (check output/complexStories/<case>/01-adr-*.md's status badge)
before implementing the fan-out/compensation specifics. If it names "E-00" (or your domain's equivalent
shared-saga story), confirm that module already exists in the target repo — do not reimplement saga
machinery inline.

For PRODUCT-BE-E-01 specifically:
1. Implement ProductBusinessPartnerActionService with 3 strategy methods (REMOVE_PARTNER,
   DROP_PARTNER, UNDROP_PARTNER), each orchestrated as a WriteSaga (PRODUCT-BE-E-00) with one step for
   the partner-status update and one step PER cleanup target (recentlyViewed, todo, favorite,
   sampleV2) — each cleanup is its OWN saga step, not a single combined step, specifically so one
   cleanup failing doesn't silently skip the rest.
2. The exact compensation behavior per step is whatever PRODUCT-BE-S-03 concludes — implement against
   that spike's ratified decision, not an assumption. If S-03 hasn't ratified yet, flag this story as
   not-yet-startable rather than guessing at the compensation strategy.
3. Security ordering constraint (ADR-012 §4, testable invariant): on DROP, the ACL bulk-drop must
   complete before the mutation returns success — this is a hard ordering requirement, not a nice-to-
   have; get it wrong and you have a security gap, not just a test failure.

Implement against every numbered Acceptance Criterion.
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) for this orchestrated write — required for every Phase E story,
and the most important test suite in this program given the failure-mode risk:

- File: src/test/groovy/<package>/ProductBusinessPartnerActionServiceSpec.groovy.
- Mock the WriteSaga collaborator and each cleanup client (recentlyViewedClient, todoClient,
  favoriteClient, sampleV2Client) individually with Spock `Mock()`.
- One `where:`-driven test per action type (REMOVE/DROP/UNDROP) asserting the correct saga steps are
  registered in the correct order (partner-status-update first, then the 4 cleanup steps).
- A dedicated PARTIAL-FAILURE test: given one cleanup client throws, assert (a) the other cleanup steps
  still execute (this is the entire point of "each cleanup is its own saga step" — a test that shows
  one failure blocking the rest is testing the OLD, broken behavior), and (b) the saga result reflects
  PARTIAL_FAILURE with per-step detail, per whatever S-03 ratified.
- A dedicated ORDERING test for the DROP case: assert the ACL bulk-drop step completes (mocked call
  verified) BEFORE the mutation's return value is produced — use Spock's `Mock()` invocation-order
  verification (e.g. an explicit `1 * ... >> {...}` sequencing block or `MockingApi#interaction` /
  ordered `then:` blocks) to make this a real ordering assertion, not just "both were called."
- Do not test WriteSaga's own internals here — mock it and verify this service calls it correctly;
  WriteSaga has (or should have) its own spec.

Report the finished spec's file path and explicitly confirm the partial-failure and ACL-ordering tests
exist as their own named test methods (they're the two riskiest paths in this story).
```

---
*Implement prompt — Phase E · output/prompts/implement/phase-E-complex-operations-claude-opus.md*
