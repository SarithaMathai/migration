---
mode: agent
model: Claude Sonnet 4.5
description: "Phase C — a search/listing query story (e.g. PRODUCT-BE-C-01) in apps/app"
---

Implement Phase-C story **${input:storyId:PRODUCT-BE-C-01}** in `apps/app`.

Phase C is **Search & Listing** — queries that call the search/elastic EXT service, sometimes combined with a second canonical-data fetch ("two-stage hydration"). These often carry a `🔴 search` EXT severity marker and truthy-default booleans that must be preserved exactly.

Steps:

1. **Gate check first** — if *Depends on* names a `SPIKE-0x` or an `S0x` spike (e.g. `PRODUCT-BE-C-01` depends on `S-02`, the `getProducts` hydration spike), run `/check-spike-gate` before implementing the hydration/merge logic. If the spike is still open, the story's own text usually names a **safe default** ("until S-02 concludes, preserve today's shape") — implement that default, not a guess at the eventual design.
2. Read *Current Behaviour, in plain terms* carefully — Phase C stories often chain two calls (e.g. search index → ids → canonical DB → merge flags onto records). Reproduce the call order and the merge exactly.
3. **Preserve truthy defaults literally** — args like `includeBoms ?? true` must default to `true` in the DGS layer too; a story that says "Boolean defaults are truthy — pin in tests" means write a test that asserts this, not just implement it.
4. Implement per `.github/instructions/kotlin/datafetcher.instructions.md` / `service.instructions.md`. The EXT call severity (`🔴`/`🟡`/`🔵`) tells you how critical/sequential the call is — a 🔴 call on the critical path shouldn't be reordered or parallelized away without the story asking for it.
5. Tests per `.github/instructions/kotlin/testing.instructions.md`: cover every arg-combination the AC lists (e.g. "4 arg combos: no flags / all flags / resourceType=X / filter array"), plus a default-truthiness test, plus a merge-correctness test.
6. Report AC line by line, calling out explicitly which behaviour is "safe default pending spike" vs "final."

Most Phase-C stories in `product` are gated on `SPIKE-06a` (hydration) via `PRODUCT-BE-S-02` — always check.
