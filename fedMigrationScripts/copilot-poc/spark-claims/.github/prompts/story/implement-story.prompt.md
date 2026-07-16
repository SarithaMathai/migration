---
mode: agent
model: Claude Sonnet 4.5
description: "Implement one CLAIM-BE-* migration story end-to-end (schema + Kotlin fetcher + service + tests)"
---

Implement the migration story **${input:storyId:CLAIM-BE-B-01}**.

Follow the `story-implementer` workflow (`.github/chatmodes/story-implementer.chatmode.md`):

1. Gate check — if the story is `CLAIM-BE-E-01` (or any future Phase-E story) or depends on a `SPIKE-0x`, stop and report the open spike instead of coding (use `/check-spike-gate` logic). If the story is `CLAIM-BE-F-01` or `CLAIM-BE-F-02`, confirm the owning type (`Product` / `ResourcesCount`) already exists in `plm-product` before proceeding — they are BLOCKED-BY that.
2. Read the story's *Current Behaviour → Target → Files → Acceptance Criteria → Test Cases* (I will paste the Jira ticket if you don't have it; otherwise use `output/initial-analysis/claims/04-stories.md` at https://github.com/XXX).
3. Read the operation's pseudo-logic in `02-resolver-analysis.md` and the target slice of `03-schema.graphql`.
4. Show me the planned file diff list and wait for my confirmation.
5. Implement: schema addition, Kotlin DGS data fetcher, service method (only if missing), tests — per the path-scoped instruction files.
6. Build, run the tests, then report acceptance criteria one by one with pass/fail evidence.
7. Draft the PR description (bullets: what changed, criteria → evidence, Hive push note).

Constraints: one story only, thin DGS wrapper, no ACL/proxy-ACL logic, no invented rollback, parity with the legacy resolver's response shape, federation hop only (no in-process shortcuts to other domains).
