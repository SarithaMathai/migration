---
applyTo: "apps/app/**/*.graphqls"
description: "Schema rules for the plm-product federated subgraph (Netflix DGS + Hive)"
---

# GraphQL schema rules — plm-product subgraph

## File layout

- All subgraph schema files live in the **`apps/app`** module (the API-hosting module of the monorepo).
- One schema file per co-located domain: `product.graphqls`, `bom.graphqls`, `measurement.graphqls`, `packaging.graphqls`, `impression.graphqls`, `productDetails.graphqls`, `watchlist.graphqls`.
- Body order inside a file: header comment → federated entity types (`@key`) → owned object types → interfaces/unions → input types → enums → `extend type Query` → `extend type Mutation`.
- Each type carries a one-line comment: status + purpose. No prose blocks.

## Ownership and federation

- Types owned by a co-located domain are **plain internal types** — cross-references between the seven co-located domains are direct type references, **not** `@extends` stubs (no gateway hop inside one subgraph).
- Only entities referenced by **separate** subgraphs get `@key` (e.g. `Product`, `ProductTechPack @key(fields: "productId partnerId")`).
- Stub types for entities owned by a separate subgraph: id-only `@extends @key(fields: "id")` + `@external`, and the Kotlin stub class **must use the entity's simple class name** (`Product`, not `ProductRef`) — DGS resolves `_Entity` by simple class name.
- Do not rely on custom directives surviving federation SDL — the federation-jvm SDL printer strips them from `_service { sdl }`. Hide plumbing structurally (naming/externals), not with directives.

## Evolution rules

- Never delete or rename a field a client may still query — mark `@deprecated(reason: "…")` and record the removal in the story.
- Match the target schema in `output/initial-analysis/{domain}/03-schema.graphql` at https://github.com/XXX; if the implementation must diverge, call it out in the PR description.
- New scalars must be registered in the scalar config before use.
- Every schema change ships with its story's data fetcher in the same PR and must pass the Hive composition check before merge.
