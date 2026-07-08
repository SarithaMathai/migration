---
mode: agent
model: Claude Sonnet 4.5
description: "Phase D — a simple mutation story (e.g. SPARK-PROD-D01) in apps/app"
---

Implement Phase-D story **${input:storyId:SPARK-PROD-D01}** in `apps/app`.

Phase D is **Mutations (simple)** — single-purpose writes. Many co-located `product` D-stories also perform a side-effect association (workspace link, attachment link) and are gated on the cross-domain association spike.

Steps:

1. **Gate check first** — run `/check-spike-gate ${input:storyId}`. Most `product` D-stories (`D01`–`D04`, `D06`, `D07`, `D11`) depend on `S01`/`SPARK-SPIKE-06b` (cross-domain association pattern). If open, the story names a fallback ("orchestrate create→copy→assoc per S01's chosen pattern" — implement today's ad-hoc sequence as the interim, don't invent a saga).
2. Read *Current Behaviour* for the exact backend call sequence (e.g. `POST {v1}` + optional copy + workspace association) and reproduce the order.
3. If the story flags a **no-rollback behaviour to preserve** (e.g. "attachment-link side-effects — no rollback — preserve, flag"), implement it as-is and add a code comment/test name that makes the gap visible — do not add rollback yourself; that's the spike's call.
4. Implement per `.github/instructions/kotlin/datafetcher.instructions.md` (`@DgsMutation`) / `service.instructions.md`. If the story is a bulk variant (`addProducts`, `bulkUpdateProducts`), match the response shape's bulk type (e.g. `ProductBulkType`), not a plain list.
5. Tests per `.github/instructions/kotlin/testing.instructions.md`: one test per AC line (create, optional-copy-when-present, association-applied), plus one explicitly asserting the preserved no-rollback behaviour if flagged.
6. Report AC line by line with evidence, and separately confirm you did **not** implement any failure-strategy logic the gate check flagged as pending.

No ACL logic. Never guess at the association pattern — implement only what the story's fallback text specifies.
