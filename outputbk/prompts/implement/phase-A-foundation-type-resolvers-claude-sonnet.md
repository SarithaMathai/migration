# Prompt — Implement a Phase A story (Foundation & Type Resolvers)
# Model: Claude Sonnet (GitHub Copilot)

> **Phase A** = one-time scaffolding, shared registries, `@DgsTypeResolver` unions/interfaces. Worked
> example: **`BOM-BE-A-04`** — `@DgsTypeResolver` for the 2 BOM interfaces (material category code → concrete
> type, impression type code → concrete type). Full story text:
> [`output/analysis/bom/be-04-stories.md`](../../analysis/bom/be-04-stories.md) (search `### BOM-BE-A-04`).

---

## Prompt

Replace `<STORY_ID>` and `<DOMAIN>` for the story you're actually implementing — the instructions below
use `BOM-BE-A-04` concretely so you can see the pattern; swap in your own story's specifics.

```
You are implementing <STORY_ID> from output/analysis/<DOMAIN>/be-04-stories.md in the target DGS
service repo (not this planning repo). Read the full story section first (search "### <STORY_ID>") —
Current Behaviour, Target DGS Implementation, Files to Create/Modify, Acceptance Criteria.

For BOM-BE-A-04 specifically, that means:
1. Create model/BomConstants.kt — a Kotlin object/enum holding all 21 material-category codes and 5
   impression-type codes, replacing the legacy resolver's inline MATERIAL_CATEGORY_ID constant (this
   also fixes the circular import the story calls out).
2. Create dataFetcher/BomTypeResolvers.kt with two @DgsTypeResolver(name = "...") functions:
   - one for BomMaterialInterface: switch on material.materialCategory.code using BomConstants,
     mapping 4→Trim, 6→Wash, 2→Fabric, 15→Combination, 16→FabricSpec, {10,11,12,13,14,17-24}→Packaging,
     default (including 1,5,9)→BomMaterial.
   - one for BomImpressionDetailsInterface: switch on impression.type, 603→Trim, 605→TrimZipper,
     604→Wash, 602→Fabric, default (601)→Base.
3. Preserve the default-branch fallthrough EXACTLY as specified — this is an explicit Acceptance
   Criterion (HUB code 9 must fall through to BomMaterial, not throw or return null).

Implement against every numbered Acceptance Criterion in the story — do not mark this done until each
one is independently verifiable, not just "the happy path works."
```

## Spock/Groovy test requirement

```
Write a Spock specification (Groovy) covering this story's type-resolver logic — this is required for
every Phase A story, not optional test coverage:

- File: src/test/groovy/<package>/BomTypeResolversSpec.groovy (mirror your source package layout).
- Use a `where:` data table to cover EVERY category/type code named in the Acceptance Criteria as its
  own row — not just a representative sample. For BOM-BE-A-04 that's all 21 material codes + 5
  impression codes + the two documented defaults (materialCategory code 9 → BomMaterial, impression
  code 601 → BomBaseImpressionDetails).
- One `def "resolves material category code #code to #expectedType"()` -style parameterized test for
  the material resolver, one equivalent for the impression resolver.
- Assert on the exact returned type (e.g. `result == "Trim"` or `result instanceof BomTrimMaterial`,
  matching whatever your @DgsTypeResolver actually returns — a type name String per the DGS contract).
- Include one explicit "unknown/unmapped code" case per resolver asserting the default-branch fallback,
  since the story's AC calls this out as a specific must-not-regress behavior, not an edge case to skip.
- Do not mock BomConstants — reference the real object, since the story's AC #3 says to "verify values
  against backend" and a mocked constants table would hide a real mismatch.

Report the finished spec's file path and confirm every AC-named code path has its own test row.
```

---
*Implement prompt — Phase A · output/prompts/implement/phase-A-foundation-type-resolvers-claude-sonnet.md*
