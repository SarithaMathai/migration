---
applyTo: "**/datafetcher*/**/*.kt, **/fetchers/**/*.kt, **/graphql/**/*.kt"
description: "Netflix DGS data fetcher rules for spark-claims (Kotlin)"
---

# DGS data fetcher rules (Kotlin)

- **All data fetchers are written in Kotlin** — never Java — as `@DgsComponent` classes.

## Annotations — pick by story phase

- Phase B/C read story → `@DgsQuery`.
- Phase D/E write story → `@DgsMutation`.
- Phase F federation-contribution story → `@DgsEntityFetcher(name = "Product")` / `@DgsEntityFetcher(name = "ResourcesCount")` resolving only the contributed field, or `@DgsData(parentType = "Product", field = "claims")` depending on the chosen pattern — match whichever `SPARK-CLM-F01` established first.
- Phase G field-resolver story → `@DgsData(parentType = "Claims", field = "…")`.

## Implementation shape

- A data fetcher is a **thin wrapper**: validate/shape input → call the existing Kotlin service method → map to the schema type. No business logic in the fetcher.
- Fan-out reads (a field resolved for N parents, e.g. `Claims.businessPartner` across a list) use a **DataLoader** — never a per-parent service call in a loop.
- Every cross-subgraph reference (to `Product`, `Workspace`, etc.) is a genuine federation hop — there is no in-process shortcut in this repo. Do not call another domain's REST service directly from here; extend the type via federation instead.
- Nullability and list shape must match the schema exactly; map backend `null`/missing to the schema's declared nullability, matching the legacy resolver's behaviour (see `02-resolver-analysis.md` for the operation at https://github.com/XXX).
- Errors: translate backend failures to typed GraphQL errors; never leak raw REST bodies or stack traces into the response.
- DGS applies the federation transform automatically — do not add manual federation config.

## Hard limits

- No ACL or proxy-ACL logic (`getUserPermissionsJWTByProxy` and similar are context-only, never implemented here).
- No compensation/rollback logic in `updateClaim` (`SPARK-CLM-E01`) until `SPARK-SPIKE-01` records its decision.
- Keep the DGS layer free of caching unless the story's acceptance criteria ask for it (`getCommunicationChannels`/`getAllClaimsAbout` are marked cacheable — only cache where the story says so).
