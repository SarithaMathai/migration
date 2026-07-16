---
mode: agent
model: Claude Sonnet 4.5
description: "Implement one Spark→DGS migration story end-to-end in apps/app (schema + fetcher + service + tests)"
---

Implement the migration story **${input:storyId:PRODUCT-BE-B-02}** in the `apps/app` module.

Follow the `story-implementer` workflow (`.github/chatmodes/story-implementer.chatmode.md`):

1. Gate check — if the story is Phase E or depends on a `SPIKE-0x`, stop and report the open spike instead of coding (use `/check-spike-gate` logic).
2. Read the story's *Current Behaviour → Target → Files → Acceptance Criteria → Test Cases* (I will paste the Jira ticket if you don't have it; otherwise use `output/analysis/{domain}/be-04-stories.md` at https://github.com/XXX).
3. Read the operation's pseudo-logic in `be-02-resolver-analysis.md` and the target slice of `be-03-schema.graphql`.
4. Show me the planned file diff list and wait for my confirmation.
5. Implement: schema addition, DGS data fetcher, service method (only if missing), tests — per the path-scoped instruction files.
6. Build, run the tests, then report acceptance criteria one by one with pass/fail evidence.
7. Draft the PR description (bullets: what changed, criteria → evidence, Hive push note).

Constraints: one story only, thin DGS wrapper, no ACL logic, no invented rollback, parity with the legacy resolver's response shape.
