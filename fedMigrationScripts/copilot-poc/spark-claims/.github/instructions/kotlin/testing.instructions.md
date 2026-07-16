---
applyTo: "src/test/**/*.kt"
description: "Test rules for spark-claims migration stories"
---

# Test rules — migration stories

## What every story must test

- Execute the new operation through `DgsQueryExecutor` (`@SpringBootTest`) — not by calling the fetcher method directly.
- Mock the backend REST layer (WireMock / MockWebServer / mocked client bean); never hit a live service in unit/CI tests.
- Assert the **response shape**, not just status: field names, camelCase conversion, nullability, list vs single — this is the parity contract with the legacy gateway.

## Complexity drives depth

- **High / Very High** stories (e.g. `CLAIM-BE-E-01`): implement every item in the story's *Test Cases* checklist. `E-01`'s checklist is explicit — body-only, +workspace, validation-error→throw, partial-failure, parity — each becomes one named test.
- **Medium / Low** stories: happy path + one backend-error path is enough.
- Field-resolver stories (Phase F/G): include an N-parents test proving the DataLoader batches (one backend call, not N).
- Federation-contribution stories (`CLAIM-BE-F-01`/`F-02`): test the `@DgsEntityFetcher`/`@DgsData` resolves given a representation for the owning type's key, plus a parity test against the current in-gateway resolver.

## Conventions

- Test class per story or per operation (`GetClaimsDataFetcherTest`) — match what the module already uses.
- Name tests after the acceptance criterion they prove, in backtick sentences.
- Keep fixture payloads minimal and inline; large JSON goes to `src/test/resources/claims/`.
- A red test that documents a legacy quirk being preserved is better than an assertion loosened to pass.
