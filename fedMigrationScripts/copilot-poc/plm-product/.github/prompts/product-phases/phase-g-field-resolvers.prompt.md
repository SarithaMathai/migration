---
mode: agent
model: Claude Sonnet 4.5
description: "Phase G — a field resolver / bug-fix / test-coverage story (e.g. PRODUCT-BE-G-01) in apps/app"
---

Implement Phase-G story **${input:storyId:PRODUCT-BE-G-01}** in `apps/app`.

Phase G covers **field resolvers, bug fixes, utility ports, and the domain's parity test harness**. Complexity ranges widely — some are one-line field wrappers, others (like `PRODUCT-BE-G-01`) are Very High: multi-source merges ported near-verbatim from ~150 lines of legacy logic.

Steps:

1. Read the story's *Current Behaviour, in plain terms* and, if present, its **pseudocode block** — Phase-G stories for complex fields ship a literal Kotlin sketch (e.g. `AttachmentEnrichmentService`: 1 relationship call → 5-bucket partition → per-bucket hydration → merge → draft filter → sort). Port this structure directly; do not redesign the merge/sort order even if a "cleaner" approach seems obvious — the ordering rank and tiebreak are exactly what parity tests check.
2. If the story explicitly preserves a known gap as a **follow-up** (e.g. "keep the 'ACL should do draft filter' TODO as a follow-up"), leave it as a TODO comment referencing the story — do not silently fix it, and do not silently leave it undocumented either.
3. For simple field resolvers (single field, no merge): implement per `.github/instructions/kotlin/datafetcher.instructions.md` as a `@DgsData(parentType = "...", field = "...")`, with a `DataLoader` if it resolves per-parent across a list.
4. If this is the domain's designated **parity harness / tests story** (commonly the last G-numbered story, e.g. `G-16`), its job is a shared test suite proving every earlier story's DGS response matches the legacy gateway — build fixtures once, reuse across the domain's operations, not per-story duplication.
5. Tests per `.github/instructions/kotlin/testing.instructions.md`: for a multi-source merge, one test per source combination plus the exact ordering/tiebreak the pseudocode specifies; for a simple field, happy path + null-source path; for a fan-out field, the N-parents batching test.
6. Report AC line by line — for ordering-sensitive stories, show the actual sorted output in your evidence, not just "tests pass."

No spike gating applies to most Phase-G stories (`Depends on: —` is typical) — check anyway, since a few field resolvers surfacing partner data are gated on `SPIKE-04`.
