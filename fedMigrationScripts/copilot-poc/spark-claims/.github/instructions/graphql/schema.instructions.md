---
applyTo: "**/*.graphqls"
description: "Schema rules for the spark-claims federated subgraph (Netflix DGS + Hive)"
---

# GraphQL schema rules — spark-claims subgraph

## File layout

- Single schema file for the domain: `claims.graphqls`.
- Body order: header comment → owned entity types (`@key`) → federated stub types (`@extends @external`) → interfaces/unions → input types → enums → `extend type Query` → `extend type Mutation` → federation contributions into other subgraphs' types.
- Each type carries a one-line comment: status + purpose. No prose blocks.

## Ownership and federation — this subgraph is a contributor, not a host

- `Claims` (and its nested types) are **owned here** — this is the entity's home subgraph.
- Everything this subgraph needs from elsewhere is a **federation hop**, always — there is no co-located/in-process shortcut like in `plm-product`. Reference other subgraphs' entities as id-only `@extends @key @external` stubs; the Kotlin stub class **must use the entity's simple class name** (`Product`, not `ProductRef`) — DGS resolves `_Entity` by simple class name.
- This subgraph also **contributes fields into `plm-product`'s types**:
  - `extend type Product @key(fields: "id") { claims(...): [Claims] }` (`SPARK-CLM-F01`)
  - `extend type ResourcesCount @key(fields: "productId partnerId") { claims: [ID] }` (`SPARK-CLM-F02`, the TechPack rollup)
  - Both use `@DgsEntityFetcher` on the *`Product`*/`ResourcesCount` key, resolving only the `claims` field — do not attempt to own or redefine the rest of those types here.
  - Both are **BLOCKED-BY** the owning type existing in `plm-product` first — confirm before implementing, don't stub around it.
- Do not rely on custom directives surviving federation SDL — the federation-jvm SDL printer strips them from `_service { sdl }`. Hide plumbing structurally (naming/externals), not with directives.

## Evolution rules

- Never delete or rename a field a client may still query — mark `@deprecated(reason: "…")` and record the removal in the story.
- Match the target schema in `output/initial-analysis/claims/03-schema.graphql` at https://github.com/XXX; if the implementation must diverge, call it out in the PR description.
- New scalars must be registered in the scalar config before use.
- Every schema change ships with its story's data fetcher in the same PR and must pass the Hive composition check before merge.
