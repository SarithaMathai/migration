# plm-product — GitHub Copilot instructions

## What this repository is

- `plm-product` is the **host Netflix DGS subgraph** (Kotlin / Spring Boot) in the Spark → Federated GraphQL migration.
- It is a **monorepo**; **`apps/app` is the main API-hosting module** and is where all migration stories land.
- `apps/app` contains the **seven co-located domains** compiled into one subgraph: **product** (host), **bom**, **measurement**, **packaging**, **impression**, **productDetails**, **watchlist** — one package/schema file per domain.
- Other modules in the monorepo (shared libs, clients, models) are consumed by `apps/app`; a story touches them only when it needs a missing service method, never to restructure them.
- The subgraph is federated through the **Hive Schema Registry**; the supergraph gateway stitches it with the separate subgraphs (`spark-claims`, and later `plm-attachment`, `plm-discussion`, `plm-sample`, `plm-elastic-search`, `plm-workspace`).
- We are replacing resolvers that today live in the `spark-internal-graphql` Node.js gateway (legacy paths: `resolvers/…`, `services/…`, `utils/…`, `schemas/….graphqls`).

## The engineering model — one story, one PR

- Work items are Jira stories with ids like `PRODUCT-BE-B-02`, `BOM-BE-D-03`, `WATCHLIST-BE-G-01` (prefixes: `PROD`, `BOM`, `MEAS`, `PKG`, `IMP`, `PDTL`, `WL`).
- Every story is **self-contained in a single PR**: schema addition (`.graphqls`) + DGS data fetcher + Kotlin REST service method + Hive registry push.
- The domain model, REST controllers (GET/POST/PUT) and services **already exist** — a story only adds the thin DGS layer. Do not port business logic that the backing REST service already implements.
- `B-01` of each domain lands the one-time module scaffold (`{domain}.graphqls`, scalar registration, service + client wiring). All later B/C/D/G stories assume it and are mutually parallelizable.

## Sources of truth (read before implementing)

- Story text: the Jira ticket, generated from `output/analysis/{domain}/be-04-stories.md` at https://github.com/XXX.
- Per-operation pseudo-logic of the legacy resolver: `output/analysis/{domain}/be-02-resolver-analysis.md`.
- Target subgraph schema: `output/analysis/{domain}/be-03-schema.graphql`.
- Complex-case research briefs: `output/complexStories/<case>/`.
- Confluence: `FederatedGqlBreakDown-BE-{domain}` pages + the global overview holding **Phase 0 — Program Spikes**.

## Hard rules

- **Spike gating:** a story flagged 🔴🔬 or listing `SPIKE-0x` in *Depends On* must not have its complex part implemented until that spike's decision is recorded. Every Phase-E story is gated on `SPIKE-01` (non-atomic write saga) unless stated otherwise. When in doubt run the `check-spike-gate` prompt.
- **ACL is context-only.** Never re-implement ACL/permission-token logic in the DGS layer — decided at program level.
- **Parity first.** The GraphQL response shape must match the legacy gateway byte-for-byte where the story says parity (field names, camelCase conversion, nullability, list vs single).
- **No invented rollback.** Multi-step writes keep today's behaviour until `SPIKE-01` concludes; do not add compensation logic on your own.
- Do not edit generated code (DGS codegen output) by hand.

## Conventions

- Kotlin + Spring Boot + Netflix DGS; follow the path-scoped instruction files in `.github/instructions/` for schema, data fetcher, service and test rules.
- Write documentation and PR descriptions **point by point — bullets, never paragraphs**. Personas are **Engineer** and **Product Owner**.
- Reference legacy code with source-repo paths (`resolvers/SPARK_Product.js`), never local copies.
- Commit messages: `PRODUCT-BE-B-02: <what changed>` — story id first.
