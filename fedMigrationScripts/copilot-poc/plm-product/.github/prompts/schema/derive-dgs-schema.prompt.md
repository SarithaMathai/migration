---
mode: agent
model: Claude Sonnet 4.5
description: "Derive/extend a domain's .graphqls file in apps/app from the analysis target schema"
---

Add the schema for story **${input:storyId:PRODUCT-BE-B-02}** (or the operation/type I name) to the owning domain's `.graphqls` file in `apps/app`.

Steps:

1. Locate the target definition in `output/initial-analysis/{domain}/03-schema.graphql` at https://github.com/XXX — that file is the derived target for this subgraph; copy its intent, don't re-derive from the legacy SDL.
2. Place it in the right domain file (`product.graphqls`, `bom.graphqls`, `measurement.graphqls`, `packaging.graphqls`, `impression.graphqls`, `productDetails.graphqls`, `watchlist.graphqls`) following `.github/instructions/graphql/schema.instructions.md` — body order, ownership rules, federation directives.
3. Apply the federation checklist:
   - co-located cross-reference → plain type reference (no `@extends`)
   - separate-subgraph entity → id-only `@extends @key @external` stub
   - only add `@key` where a separate subgraph references the type
   - new scalars registered before use
4. Run DGS codegen; confirm the generated Kotlin types compile.
5. Report: the schema diff, any divergence from `03-schema.graphql` (with reason), and which story's data fetcher must ship with it (schema never merges alone).
