# Example usage — chat modes, prompts, and instructions in action

Two worked sessions: a simple story that goes straight through, and a complex story that gets blocked at the spike gate. Both use real content from `output/initial-analysis/product/04-stories.md`.

---

## Walkthrough 1 — implementing a simple story (`PRODUCT-BE-B-01`)

**Setup:** in VS Code, open Copilot Chat, pick **story-implementer** from the chat mode dropdown (top of the chat panel — loads `.github/chatmodes/story-implementer.chatmode.md`).

**Engineer types:**

```
Implement PRODUCT-BE-B-01
```

(equivalently, without switching modes: `/implement-story PRODUCT-BE-B-01` from `.github/prompts/story/implement-story.prompt.md`)

**What fires, in order:**

1. **`copilot-instructions.md`** is already loaded for every request in this repo — Copilot knows this is `apps/app` of the `plm-product` monorepo, that stories are self-contained one-PR units, and that ACL is context-only.
2. The chat mode's workflow step 1 (**gate check**) runs: `PRODUCT-BE-B-01` is Phase B, not Phase E, no `SPIKE-0x` in *Depends on* → not gated → proceeds.
3. Step 2 (**read the contract**) — the Engineer pastes the Jira ticket text (or Copilot is pointed at `output/initial-analysis/product/04-stories.md#PRODUCT-BE-B-01` in the linked analysis repo):

   > **`getProduct(id)`** · Type: Query · Phase: B · Complexity: Low · Depends on: —
   > **Current Behaviour:** `getByID.load(id)` → `GET ${v1}?productId={id}` → camelCase or null; DataLoader-batched.
   > **Target:** `@DgsQuery getProduct(id): Product` via `ProductDataLoader` keyed on id.
   > **Note:** this PR also creates the one-time `product.graphqls` module scaffold (federation v2.3 header, scalars, `@key` types, external stubs) + `ScalarConfig.kt` + service/Feign wiring — every later B/C/D/G story assumes it.
   > **Acceptance Criteria:** 1) returns product, 404→null. 2) batches N ids in 1 call.

4. Step 3 (**plan the diff**) — Copilot lists the files it intends to touch and waits:

   ```
   Planned diff for PRODUCT-BE-B-01:
   - apps/app/.../product/product.graphqls        (new: Product @key type, Query.getProduct, scalar registration)
   - apps/app/.../product/ScalarConfig.kt          (new: scalar wiring)
   - apps/app/.../product/ProductDataFetcher.kt    (new: @DgsQuery getProduct)
   - apps/app/.../product/ProductDataLoader.kt     (new: batched loader keyed on id)
   - apps/app/.../product/ProductClient.kt         (Feign client wiring, if not already present)
   - apps/app/src/test/.../ProductDataFetcherTest.kt

   Confirm to proceed?
   ```

5. Engineer replies `yes`. Step 4 (**implement**) now pulls in the **path-scoped instructions** automatically, because the files Copilot is about to write match their `applyTo` globs:
   - writing `product.graphqls` → `.github/instructions/graphql/schema.instructions.md` applies (body order: header → `@key` types → external stubs → Query/Mutation extensions; co-located refs are plain types, no `@extends`).
   - writing `ProductDataFetcher.kt` → `.github/instructions/kotlin/datafetcher.instructions.md` applies (`@DgsQuery` in a `@DgsComponent`, DataLoader for fan-out, no business logic in the fetcher, no ACL).
   - writing `ProductClient.kt` → `.github/instructions/kotlin/service.instructions.md` applies (reuse existing HTTP client wiring, replicate the `GET ${v1}?productId={id}` call and camelCase conversion exactly).
   - writing the test → `.github/instructions/kotlin/testing.instructions.md` applies (`DgsQueryExecutor` + mocked REST layer, Low complexity → happy path + one error path, plus the batching test the AC explicitly asks for).
6. Step 5 (**verify**) — Copilot runs the build and the new test, then reports against the AC:

   ```
   ✅ AC1 — returns product; 404 → null  (ProductDataFetcherTest.returns product by id, ...returns null on 404)
   ✅ AC2 — batches N ids in 1 call      (ProductDataLoaderTest.batches three ids into a single GET)
   ```
7. Step 6 (**PR**) — Copilot proposes branch `feature/spark-prod-b01` and drafts the PR description (bullets: what changed / AC → evidence / Hive push note).

**Optional follow-up**, still in chat: switch to the **parity-checker** chat mode (or run `/write-parity-tests getProduct PRODUCT-BE-B-01`) to get the legacy-vs-DGS parity table before merging, and the **schema-steward** chat mode to review the new `.graphqls` for federation safety.

---

## Walkthrough 2 — a story that's spike-gated (`PRODUCT-BE-E-01`)

**Engineer types**, without switching modes:

```
/check-spike-gate PRODUCT-BE-E-01
```

This loads `.github/prompts/story/check-spike-gate.prompt.md`, which carries the override table inline (no need to re-derive it). `PRODUCT-BE-E-01` matches the table row directly:

**Copilot responds:**

```
Gated — SPIKE-03 (Partner Drop/Undrop + Ownership).

Decision to make: decide ownership (domain subgraph vs workspace) and the
write-saga/rollback for the drop/undrop fan-out. Status: Open.

Blocked: the orchestration/rollback part of productBusinessPartnerActions.
Not blocked: schema scaffolding for the read-only parts, if the story's
Files list separates them — check with the Product Owner before starting
those in isolation.

See Phase 0 — Program Spikes / Spike Detail on the global Confluence
overview for the brief + intended cross-domain steps, and
output/complexStories/partner-drop-undrop-write/ for research so far.
```

Now if the Engineer tries `/implement-story PRODUCT-BE-E-01` anyway, the **story-implementer** chat mode's own step 1 (gate check) catches it independently and refuses to write the orchestration code, asking for confirmation that the spike decision is recorded first — the two layers agree because they read the same override table.

---

## Quick reference — what to invoke when

| Situation | Use |
|---|---|
| Starting any story | chat mode **story-implementer**, or `/implement-story {id}` |
| Not sure if a story is blocked | `/check-spike-gate {id}` |
| Adding/extending a schema type before code exists | `/derive-dgs-schema` |
| Verifying a finished operation matches legacy behaviour | chat mode **parity-checker**, or `/write-parity-tests {operation} {id}` |
| Reviewing a PR that touches `.graphqls` | chat mode **schema-steward** |
| Copilot coding agent working an assigned GitHub issue autonomously | reads `AGENTS.md` + `copilot-instructions.md` on its own, no manual invocation |
