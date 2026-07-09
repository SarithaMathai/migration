# spark-claims — GitHub Copilot instructions

## What this repository is

- `spark-claims` is a **standalone Netflix DGS subgraph** (Kotlin / Spring Boot) in the Spark → Federated GraphQL migration — its own repo, not a module in the `plm-product` monorepo.
- It hosts exactly **one domain: claims** (`ClaimService` → `spark-claims`).
- The subgraph is federated through the **Hive Schema Registry**; the supergraph gateway stitches it with `plm-product` (host) and the other subgraphs.
- We are replacing resolvers that today live in the `spark-internal-graphql` Node.js gateway (legacy paths: `resolvers/SPARK_...`, `services/Claim.js`, `utils/…`, `schemas/SPARK_Claim.graphqls`).

## The engineering model — one story, one PR

- Work items are Jira stories with the id prefix `SPARK-CLM-*` (e.g. `SPARK-CLM-B01`, `SPARK-CLM-E01`).
- Every story is **self-contained in a single PR**: schema addition (`.graphqls`) + Kotlin DGS data fetcher + Kotlin REST service method + Hive registry push.
- The domain model, REST controllers (GET/POST/PUT) and services **already exist** — a story only adds the thin DGS layer. Do not port business logic that the backing REST service already implements.
- `SPARK-CLM-B01` lands the one-time module scaffold (`claims.graphqls`, scalar registration, service + Feign client wiring). All later B/C/D/G stories assume it and are mutually parallelizable.

## This subgraph's shape is different from plm-product

- Claims is **not** co-located with product/bom/measurement/etc. — there is no in-process call option here. Anything claims needs from another domain is a **federation hop**, always.
- Claims **contributes into `Product`** rather than the other way around: `SPARK-CLM-F01` (`Product.claims`) and `SPARK-CLM-F02` (`ResourcesCount.claims`, the TechPack rollup) both `extend type Product`/`extend type ResourcesCount` owned by `plm-product`, and are **BLOCKED-BY** those types existing there first (`plm-product` Phase A / `SPARK-PROD-E03`/`F05`). Do not implement F01/F02 before confirming the owning type is live in `plm-product`.
- `updateClaim` (`SPARK-CLM-E01`) uses a **proxy-ACL** JWT path (`getUserPermissionsJWTByProxy`) that is context-only — never build it, just note it.

## Sources of truth (read before implementing)

- Story text: the Jira ticket, generated from `output/initial-analysis/claims/04-stories.md` at https://github.com/XXX.
- Per-operation pseudo-logic of the legacy resolver: `output/initial-analysis/claims/02-resolver-analysis.md`.
- Target subgraph schema: `output/initial-analysis/claims/03-schema.graphql`.
- Confluence: `FederatedGqlBrakDown-claims` page + the global overview holding **Phase 0 — Program Spikes**.

## Hard rules

- **Spike gating:** `SPARK-CLM-E01` (`updateClaim`) is gated on `SPARK-SPIKE-01` (non-atomic write saga) — the same generic multi-step-write spike every domain's Phase-E story shares. Do not implement its failure strategy until that spike's decision is recorded; run `/check-spike-gate` first.
- **ACL is context-only.** Never re-implement ACL/permission-token or proxy-ACL logic in the DGS layer — decided at program level.
- **Parity first.** The GraphQL response shape must match the legacy gateway byte-for-byte where the story says parity (field names, camelCase conversion, nullability, list vs single).
- **No invented rollback.** `updateClaim`'s three-step write (permissions check → workspace association → body PUT) keeps today's behaviour and its "throw on validation error, no rollback" until `SPARK-SPIKE-01` concludes.
- Do not edit generated code (DGS codegen output) by hand.

## Conventions

- Kotlin + Spring Boot + Netflix DGS; follow the path-scoped instruction files in `.github/instructions/` for schema, data fetcher, service and test rules.
- Write documentation and PR descriptions **point by point — bullets, never paragraphs**. Personas are **Engineer** and **Product Owner**.
- Reference legacy code with source-repo paths (`services/Claim.js`), never local copies.
- Commit messages: `SPARK-CLM-B01: <what changed>` — story id first.
