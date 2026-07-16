---
mode: agent
model: Claude Sonnet 4.5
description: "Derive/extend claims.graphqls (or a federation contribution) from the analysis target schema"
---

Add the schema for story **${input:storyId:CLAIM-BE-B-01}** (or the operation/type I name).

Steps:

1. Locate the target definition in `output/initial-analysis/claims/03-schema.graphql` at https://github.com/XXX — that file is the derived target for this subgraph; copy its intent, don't re-derive from the legacy SDL.
2. Decide which shape applies, per `.github/instructions/graphql/schema.instructions.md`:
   - owned type/operation on `Claims` → add directly to `claims.graphqls`
   - reference to another subgraph's entity → id-only `@extends @key @external` stub
   - **federation contribution into `plm-product`** (`CLAIM-BE-F-01`/`F-02`) → `extend type Product`/`extend type ResourcesCount`, contributing only the `claims` field, with `@DgsEntityFetcher` on that key — confirm the owning type already exists there first.
3. Apply the federation checklist: no `@key` unless another subgraph references the type; new scalars registered before use; no custom directives relied on surviving `_service { sdl }`.
4. Run DGS codegen; confirm the generated Kotlin types compile.
5. Report: the schema diff, any divergence from `03-schema.graphql` (with reason), and which story's data fetcher must ship with it (schema never merges alone).
