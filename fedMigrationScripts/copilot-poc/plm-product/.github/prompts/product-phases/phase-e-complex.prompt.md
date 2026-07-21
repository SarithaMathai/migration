---
mode: agent
model: Claude Sonnet 4.5
description: "Phase E — a complex multi-step write story (e.g. PRODUCT-BE-E-01) in apps/app"
---

Implement Phase-E story **${input:storyId:PRODUCT-BE-E-01}** in `apps/app`.

Phase E is **Complex Operations** — multi-step orchestrated writes, aggregations, or facades. **Every Phase-E story is spike-gated by default** (`SPIKE-01`, non-atomic write saga, unless overridden to `02`/`03`/`04` — see the override table).

Steps:

1. **Gate check is mandatory, not optional — run `/check-spike-gate ${input:storyId}` before reading further.** If the spike's decision is not recorded, **stop here**: report the open decision, the story's fan-out/step list from its pseudocode, and wait for the Engineer/PO to confirm the decision before writing any orchestration or compensation code.
2. Once unblocked: read the story's pseudocode block literally — it names the exact steps (e.g. `productBusinessPartnerActions`: partner-status-update → fan-out cleanup across `recentlyViewed`/`todo`/`favorite`/`sampleV2`, each as its own saga step) and the **shape only** — "the exact fan-out compensation depends on the spike's answer."
3. Implement the chosen saga strategy from the spike's recorded decision (compensating saga / compensation-log + best-effort / best-effort) using the shared pattern in `output/complexStories/<case>/` if the story references a shared `WriteSaga`.
4. Preserve **per-target failure isolation** where the story asks for it — one cleanup step failing must be visible and must not silently swallow the others.
5. Implement per `.github/instructions/kotlin/datafetcher.instructions.md` / `service.instructions.md`. If the story is large (Very High complexity), expect it to be split into sub-tasks in Jira (`E-01-1`, `E-01-2`, …) — implement and PR one sub-task at a time, not the whole story in one diff.
6. Tests per `.github/instructions/kotlin/testing.instructions.md`: every path in the *Test Cases* checklist becomes one named test — for a dispatcher, that means one test per action case (e.g. REMOVE/DROP/UNDROP) plus a partial-failure test plus the parity test.
7. Report: which spike decision you implemented against (cite it), AC line by line, and the sub-task boundary if this is part of a larger split.

This is the highest-risk phase — never invent a failure strategy, never skip the gate check, never merge without the parity test green.
