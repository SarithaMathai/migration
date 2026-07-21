---
mode: agent
model: Claude Sonnet 4.5
description: "Phase B — a core read query story (e.g. PRODUCT-BE-B-01) in apps/app"
---

Implement Phase-B story **${input:storyId:PRODUCT-BE-B-01}** in `apps/app`.

Phase B is **Core Reads** — simple query wrappers, usually Low/Medium complexity, `Depends on: —`. These are the easiest stories and the best ones to start with.

Steps:

1. Read the story's *Current Behaviour* (the legacy loader call — e.g. `getByID.load(id)` → `GET {v1}?productId={id}`) and *Target* (`@DgsQuery` signature) from the Jira ticket or `output/analysis/{domain}/be-04-stories.md` at https://github.com/XXX.
2. If this is the domain's `B-01`, it also carries the **one-time module scaffold** note — build that first (see the `phase-a-scaffold` prompt), it's a prerequisite for this and every later story in the domain.
3. Add the query to the domain's `.graphqls` file, the `@DgsQuery` fetcher, and a `DataLoader` if the story's AC mentions batching (most B-phase reads are DataLoader-batched — check for "batches N ids in 1 call" in the AC).
4. Implement per `.github/instructions/kotlin/datafetcher.instructions.md` and `.github/instructions/kotlin/service.instructions.md` — this is a thin wrapper over an existing REST call, do not add logic beyond what the legacy loader does.
5. Tests per `.github/instructions/kotlin/testing.instructions.md`: Low complexity → happy path + one error path (e.g. "404 → null"); if the AC mentions batching, add the N-parents-in-1-call test.
6. Report each AC line with pass/fail evidence.

No spike gating applies to Phase B (Depends on is almost always `—`). No ACL logic.
