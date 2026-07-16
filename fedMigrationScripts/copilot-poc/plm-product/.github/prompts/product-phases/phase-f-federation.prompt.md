---
mode: agent
model: Claude Sonnet 4.5
description: "Phase F — a federation/stitching contribution story (e.g. PRODUCT-BE-F-01) in apps/app"
---

Implement Phase-F story **${input:storyId:PRODUCT-BE-F-01}** in `apps/app`.

Phase F is **Federation & Stitching** — one story per cross-domain edge, almost always **BLOCKED-BY another subgraph being live**, not by a program spike. Do not confuse the two: a Phase-F story stays in "do not implement" state until the owning/contributing subgraph is deployed, regardless of spike status.

Steps:

1. **Blocking check first.** Read the story's *Blocked by* line (e.g. `PRODUCT-BE-F-01`: "attachment domain (⛔ cross-subgraph — does not ship until `plm-attachment` is live)"). If the blocking subgraph isn't confirmed live, **stop and report** — do not scaffold speculative code for it. This is a deployment-order block, not a `/check-spike-gate` spike.
2. Read the story's example block literally — F-phase stories in this repo ship a **complete `extend type` + `@DgsEntityFetcher`/`@DgsData` example** in the story text; match its shape exactly rather than re-deriving the federation pattern from scratch.
3. Apply `.github/instructions/graphql/schema.instructions.md`'s federation rules: this story's schema change is an `extend type` on an entity **owned by another subgraph** (e.g. `ResourcesCount @key(fields: "productId partnerId")` owned by `plm-product`, extended here or extended *by* another domain into `plm-product` depending on direction) — never redefine the owning type, only add the field(s) this story is responsible for.
4. Implement the `@DgsEntityFetcher` resolving the key, and the field resolver(s) calling **this domain's own store/service directly** — the whole point of federation is that the graph walk / facade computation the legacy code did is replaced by a direct, local answer.
5. Tests per `.github/instructions/kotlin/testing.instructions.md`: an entity-resolution test given a representation for the key, a parity test against whatever facade/aggregation this replaces, and (if the AC says so) a "field is live only after the other subgraph is deployed" ship-gate test or feature-flag check.
6. Report: confirm the blocking subgraph's status, AC line by line, and explicitly note the facade/story this replaces (e.g. "E-03 TechPack facade stops populating this field").

Run **schema-steward** chat mode on the resulting `.graphqls` diff before opening the PR — federation-shape mistakes here break composition for every consumer.
