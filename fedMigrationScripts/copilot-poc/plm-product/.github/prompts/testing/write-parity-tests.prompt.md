---
mode: agent
model: Claude Sonnet 4.5
description: "Generate Kotlin parity tests for a migrated operation (DgsQueryExecutor + mocked REST)"
---

Write the parity tests for **${input:operation:getProduct}** (story ${input:storyId:PRODUCT-BE-B-02}) in the `apps/app` test tree.

Steps:

1. Pull the legacy contract from the operation's section in `output/initial-analysis/{domain}/02-resolver-analysis.md` at https://github.com/XXX: backend call sequence, response mapping (camelCase conversions), null/empty handling, error behaviour.
2. Pull the story's *Test Cases* checklist — for High / Very High stories every checklist item becomes one named test; Medium / Low get happy path + one backend-error path.
3. Write Kotlin tests per `.github/instructions/kotlin/testing.instructions.md`:
   - execute through `DgsQueryExecutor` (`@SpringBootTest`), mock the REST layer
   - assert response **shape** (field names, casing, nullability, list vs single), not just values
   - field resolvers: add the N-parents DataLoader batching test
   - type resolvers: one test per variant + unknown-code fallback
4. Run the tests and report results test-by-test against the story's checklist.

Do not loosen assertions to make a test pass — a failing parity test is a finding; report it.
