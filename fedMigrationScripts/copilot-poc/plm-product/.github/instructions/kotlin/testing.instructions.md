---
applyTo: "apps/app/src/test/**/*.kt"
description: "Test rules for plm-product migration stories (apps/app module)"
---

# Test rules — migration stories

## What every story must test

- Execute the new operation through `DgsQueryExecutor` (`@SpringBootTest`) — not by calling the fetcher method directly.
- Mock the backend REST layer (WireMock / MockWebServer / mocked client bean); never hit a live service in unit/CI tests.
- Assert the **response shape**, not just status: field names, camelCase conversion, nullability, list vs single — this is the parity contract with the legacy gateway.

## Complexity drives depth

- **High / Very High** stories: implement every item in the story's *Test Cases* checklist (the Jira ticket lists them). Each checklist item becomes one named test.
- **Medium / Low** stories: happy path + one backend-error path is enough.
- Field-resolver stories (Phase F/G): include an N-parents test proving the DataLoader batches (one backend call, not N).
- Type-resolver stories: one test per concrete variant + one unknown-code fallback test.

## Conventions

- Test class per story: `Spark{Prod|Bom|Meas|Pkg|Imp|Pdtl|Wl}{StoryId}Test` or per operation (`GetProductDataFetcherTest`) — match what the module already uses.
- Name tests after the acceptance criterion they prove, in backtick sentences.
- Keep fixture payloads minimal and inline; large JSON goes to `src/test/resources/{domain}/`.
- A red test that documents a legacy quirk being preserved is better than an assertion loosened to pass.
