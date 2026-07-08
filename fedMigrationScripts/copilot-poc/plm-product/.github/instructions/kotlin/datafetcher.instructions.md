---
applyTo: "apps/app/**/datafetcher*/**/*.kt, apps/app/**/fetchers/**/*.kt, apps/app/**/graphql/**/*.kt"
description: "Netflix DGS data fetcher rules for plm-product (apps/app module)"
---

# DGS data fetcher rules (Kotlin)

- **All data fetchers are written in Kotlin** — never Java — as `@DgsComponent` classes in the **`apps/app`** module, in the domain's package (`product`, `bom`, `measurement`, `packaging`, `impression`, `productDetails`, `watchlist`).

## Annotations — pick by story phase

- Phase B/C read story → `@DgsQuery` in a `@DgsComponent` class, one class per domain area.
- Phase D/E write story → `@DgsMutation`.
- Phase F/G field-resolver story → `@DgsData(parentType = "…", field = "…")`.
- Entity resolution for a `@key` type → `@DgsEntityFetcher(name = "…")`.
- Interface/union dispatch → `@DgsTypeResolver`; unknown discriminator code falls back to the base type, never throws.

## Implementation shape

- A data fetcher is a **thin wrapper**: validate/shape input → call the existing Kotlin service method → map to the schema type. No business logic in the fetcher.
- Fan-out reads (a field resolved for N parents) use a **DataLoader** — never a per-parent service call in a loop.
- Co-located cross-domain fields (e.g. `Product.boms`) call the sibling domain's service **in-process**; do not add a REST hop or an `_entities` round-trip inside the subgraph.
- Nullability and list shape must match the schema exactly; map backend `null`/missing to the schema's declared nullability, matching the legacy resolver's behaviour (see `02-resolver-analysis.md` for the operation at https://github.com/XXX).
- Errors: translate backend failures to typed GraphQL errors; never leak raw REST bodies or stack traces into the response.
- DGS applies the federation transform automatically — do not add manual federation config.

## Hard limits

- No ACL/permission-token logic — ACL is context-only (program-level decision).
- No compensation/rollback logic in multi-step writes until `SPARK-SPIKE-01` records its decision.
- Keep the DGS layer free of caching unless the story's acceptance criteria ask for it.
