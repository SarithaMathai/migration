# Copilot walkthrough — Phase A through G, `product` domain

Seven worked sessions, one per migration phase, each using a real story from `output/analysis/product/be-04-stories.md` (Phase A example is from `bom`, since `product`'s own scaffold is folded into `B-01`). Each section shows: which prompt/chat mode to use, what the Engineer types, what Copilot does step by step, and where it stops to ask vs proceeds on its own.

Phase-specific prompts live in `.github/prompts/product-phases/`:

| Phase | Prompt | What it's for |
|---|---|---|
| A | `/phase-a-scaffold` | module scaffold or a type-resolver story |
| B | `/phase-b-reads` | simple query reads |
| C | `/phase-c-search` | search/listing, two-stage hydration |
| D | `/phase-d-mutations` | simple writes with side-effect associations |
| E | `/phase-e-complex` | multi-step orchestrated writes |
| F | `/phase-f-federation` | cross-subgraph federation contributions |
| G | `/phase-g-field-resolvers` | field resolvers, bug fixes, parity harness |

All seven build on the same base layer (`copilot-instructions.md`, the `story-implementer` chat mode, the `.github/instructions/**` rules) — they just add phase-specific judgment the generic `/implement-story` prompt doesn't encode (when to stop for a spike, when a block is a deployment order rather than a spike, when to preserve a legacy quirk instead of "fixing" it).

---

## Phase A — Foundation & Type Resolvers (`BOM-BE-A-04`)

**Story:** `@DgsTypeResolver` for the 2 BOM interfaces — routes each material/impression row to its concrete type by category code (`materialCategory.code`: 4→Trim, 6→Wash, 2→Fabric, …, default→BomMaterial).

**Engineer types:**
```
/phase-a-scaffold BOM-BE-A-04
```

**Copilot does:**
1. Reads *Current Behaviour*: the legacy switch on `material.materialCategory.code` and `impression.type`, including the two default branches (HUB code 9 → `BomMaterial`; unknown impression type → `BomBaseImpressionDetails`).
2. Confirms this is a **standalone type-resolver story**, not a module scaffold (no "DGS Module Init" note on this one) — proceeds directly to implementation, no gate check needed (Phase A isn't spike-gated).
3. Creates `model/BomConstants.kt` with all 21 material category codes + 5 impression codes, mirroring the switch exactly — flags that it's sourcing this from the story's table rather than inventing values, and asks the Engineer to verify the codes against the backend (the story's AC explicitly says "verify values against backend").
4. Writes `dataFetcher/BomTypeResolvers.kt`: two `@DgsTypeResolver` functions, default branches preserved literally.
5. Writes tests: one per concrete type in each interface (7 material + 5 impression), plus one unmapped-code fallback test per interface.
6. Reports:
   ```
   ✅ AC1 — each materialCategory.code maps correctly; unknown → BomMaterial  (12 mapping tests + 1 fallback)
   ✅ AC2 — each impression type maps correctly; unknown → BomBaseImpressionDetails (5 mapping tests + 1 fallback)
   ⚠️  AC3 — BomConstants holds all 21+5 codes: please verify these against the live backend before merge, I sourced them from the story text only.
   ```

**What the Engineer does:** confirms the codes against the backend (Copilot flagged this instead of silently assuming), then approves the PR draft.

---

## Phase B — Core Reads (`PRODUCT-BE-B-01`)

**Story:** `getProduct(id)` — the core single-product read; this PR also lands the one-time `product.graphqls` module scaffold.

**Engineer types:**
```
/phase-b-reads PRODUCT-BE-B-01
```

**Copilot does:**
1. Reads *Current Behaviour*: `getByID.load(id)` → `GET ${v1}?productId={id}` → camelCase or null, DataLoader-batched.
2. Notices this is the domain's `B-01` and its "DGS Module Init" note — builds the scaffold first: `product.graphqls` header + scalars + `@key` types + external stubs, `ScalarConfig.kt`, service/Feign wiring.
3. Adds `@DgsQuery getProduct(id): Product` backed by a `ProductDataLoader` keyed on id.
4. Writes tests for both AC lines: "returns product; 404→null" and "batches N ids in 1 call."
5. Reports pass/fail per AC, no open questions — Phase B stories rarely have anything to flag.

**What's different from Phase A:** no verification-needed flag, no gate check narrative — Phase B is the "just build it" phase. This is deliberately the first story most Engineers implement; it's also where they get comfortable with the diff-confirm → implement → verify loop before hitting a phase that pauses for a decision.

---

## Phase C — Search & Listing (`PRODUCT-BE-C-01`)

**Story:** `getProducts(...)` — two-stage hydration: search index (flags) → canonical DB (records) → merge. Depends on `S-02`. `🔴 search` EXT.

**Engineer types:**
```
/phase-c-search PRODUCT-BE-C-01
```

**Copilot does:**
1. **Gate check first** (the prompt requires it before touching code): runs the equivalent of `/check-spike-gate PRODUCT-BE-C-01` → gated on `SPIKE-06a` (Hydration) via `PRODUCT-BE-S-02`, status Open.
2. Reports the gate result and, because the story itself names a safe interim ("until S-02 concludes, preserve today's shape"), proposes proceeding with that fallback rather than stopping entirely:
   ```
   PRODUCT-BE-C-01 depends on the open SPIKE-06a decision (federated @key vs
   direct call for hydration). The story specifies a safe default to build against
   in the meantime: preserve today's two-call shape (ProductElasticService.
   getFilteredProductsListing → ProductReadService.getPage → merge). I'll implement
   that default and flag AC4 (which explicitly depends on S-02's outcome) as
   not-yet-final. Proceed?
   ```
3. Engineer confirms. Copilot implements the two-stage call exactly as described, preserving all truthy defaults (`includeBoms ?? true`, etc.) and the 🔴-severity search call's position in the sequence.
4. Tests: the 4 arg-combination parity tests, a default-truthiness test, a merge-correctness test.
5. Reports:
   ```
   ✅ AC1 — parity for 4 arg combos
   ✅ AC2 — truthy defaults preserved
   ✅ AC3 — elastic flags merged onto canonical
   ⏳ AC4 — workspace-filter placement/staleness per SPIKE-06a: NOT final, built
            against today's shape per the story's documented fallback. Re-open once
            S-02 concludes.
   ```

**What the Engineer does:** ships this now (it's not blocked, just provisional on one AC), and knows exactly what to revisit once the spike closes — Copilot didn't silently guess at the final hydration design.

---

## Phase D — Mutations, simple (`PRODUCT-BE-D-01`)

**Story:** `addProduct` — create a product, optional copy-from-another, optional workspace association. Depends on `S-01`. `🔴 workspaceV2` · `🔴 attachment` EXT.

**Engineer types:**
```
/phase-d-mutations PRODUCT-BE-D-01
```

**Copilot does:**
1. Gate check: `PRODUCT-BE-D-01` depends on `S-01` (`SPIKE-06b`, cross-domain association pattern), status Open.
2. Same pattern as Phase C: the story says "orchestrate create→copy→assoc per S-01's chosen pattern" but doesn't give an explicit fallback the way C-01 did — so Copilot reports the gate and asks rather than assuming a fallback exists:
   ```
   PRODUCT-BE-D-01 is gated on SPIKE-06b (association pattern: sync vs
   event-driven vs shared AssociationService — see PRODUCT-BE-S-01's three
   candidates). The story doesn't name an explicit interim shape the way C-01 did.
   I can implement today's ad-hoc sequence (POST → optional copy → workspace assoc,
   inline/synchronous, matching current gateway behaviour) as a clearly-marked
   interim, OR wait for the spike. Which do you want?
   ```
3. Engineer says "implement the interim, mark it clearly." Copilot builds `@DgsMutation addProduct(...)`, preserving the legacy call order, and adds a `// TODO(SPIKE-06b): revisit once association pattern is decided` marker at the orchestration point.
4. Tests per AC: creates product, optional copy runs when present, workspace assoc applied.
5. Reports AC line by line, restates the TODO marker location in the PR description so reviewers see it without reading the diff line-by-line.

**Contrast with Phase C:** here Copilot explicitly asks instead of assuming a fallback, because the story text didn't hand it one — this is the judgment call the phase-specific prompt is there to encode (stop-and-ask vs proceed-with-documented-fallback), rather than a blanket "always ask" or "always proceed."

---

## Phase E — Complex Operations (`PRODUCT-BE-E-01`)

**Story:** `productBusinessPartnerActions` (REMOVE/DROP/UNDROP) — ~220-line dispatcher, fans out to 4 cleanup services, no rollback today. Depends on `S-03`. Very High complexity.

**Engineer types:**
```
/phase-e-complex PRODUCT-BE-E-01
```

**Copilot does:**
1. **Mandatory gate check, no exceptions** — this is the one phase where the prompt refuses to look at implementation before this step. Result: gated on `SPIKE-03` (Partner Drop/Undrop + Ownership), status Open, decision pending: "ownership (domain subgraph vs workspace) + write-saga/rollback for the drop/undrop fan-out."
2. Copilot **stops completely** — no interim, no fallback, because unlike C-01/D-01 this story has no safe-default language, only "Failure strategy is whatever S-03 concludes":
   ```
   PRODUCT-BE-E-01 cannot be implemented yet. SPIKE-03 is Open — both
   ownership and the write-saga/rollback strategy are undecided, and the story
   gives no interim shape to build against (unlike C-01/D-01). Implementing any
   orchestration now risks building the wrong saga structure.

   What I can do now: scaffold the ProductBusinessPartnerActionService shell with
   the 3 action-case dispatch (REMOVE/DROP/UNDROP) stubbed to throw
   NotYetImplementedException, so the schema/fetcher plumbing exists and compiles.
   Want that, or wait entirely?
   ```
3. Engineer says "do the shell." Copilot builds the schema + fetcher + service class skeleton, with the fan-out steps named but each stubbed, matching the story's own pseudocode shape (`saga.step("partner-status-update", …)`, then 4 cleanup steps).
4. No tests beyond "throws NotYetImplementedException for all 3 actions" — real tests wait for the real logic.
5. Reports: what was scaffolded, what remains blocked, and the exact spike id + decision to watch for.

**Weeks later, after `SPIKE-03` resolves:** Engineer re-runs `/phase-e-complex PRODUCT-BE-E-01`. Copilot re-checks the gate, finds it resolved, reads the recorded decision, replaces the stubs with the real saga steps and compensation logic, and only now writes the REMOVE/DROP/UNDROP/partial-failure/parity tests from the *Test Cases* checklist.

**This is the phase where the pattern differs most from B/C/D:** Phase E never proceeds on an assumed interim — at most it scaffolds inert plumbing.

---

## Phase F — Federation & Stitching (`PRODUCT-BE-F-01`)

**Story:** `ResourcesCount.productAttachments` + `discussionAttachments`, contributed by the **Attachment** subgraph. Blocked by `plm-attachment` being live — not a spike.

**Engineer types:**
```
/phase-f-federation PRODUCT-BE-F-01
```

**Copilot does:**
1. Reads *Blocked by*: "attachment domain (⛔ cross-subgraph — does not ship until `plm-attachment` is live)." Recognizes this is a **deployment-order block**, distinct from spike gating — does not run `/check-spike-gate` for this, since there's no `SPIKE-0x` involved.
2. Asks the Engineer directly:
   ```
   PRODUCT-BE-F-01 is blocked by plm-attachment being deployed, not by a spike.
   Is plm-attachment live yet? If not, I can prepare the schema extension +
   entity fetcher against the story's example code (this is a well-defined
   shape, safe to build ahead of time) but it should not merge/deploy until
   attachment is confirmed live.
   ```
3. Say the Engineer confirms `plm-attachment` is live. Copilot implements exactly the shape the story provides — `extend type ResourcesCount @key(fields: "productId partnerId") { productAttachments: [ID!]! @requires(fields: "parentProductId") ... }` plus the `@DgsEntityFetcher` and two `@DgsData` field resolvers, calling `attachmentService.getIdsByProductAndPartner(...)` directly — no relationship-graph walk, since federation replaces that.
4. Notes explicitly: "this replaces the `E-03` TechPack facade's computation of these two fields — that facade should stop populating them once this ships."
5. Tests: entity-resolution given a `{productId, partnerId}` representation, parity vs. the facade's old output, and a ship-gate test if the repo has a feature-flag mechanism.
6. Recommends running the **schema-steward** chat mode on the `.graphqls` diff before opening the PR — federation shape mistakes here break every consumer, not just this field.

**What's distinct here:** the blocking check is about *another team's deployment*, and Copilot is explicit that it's a different kind of "stop" than a spike — it can still build ahead of the block (the shape is fully specified), just can't ship ahead of it.

---

## Phase G — Field Resolvers, Bug Fixes, Tests (`PRODUCT-BE-G-01`)

**Story:** `Product.attachmentsWithMetaData` — mixed attachments/discussions/samples feed, 5-source merge + sort, ~150 lines of legacy logic to port. Very High complexity.

**Engineer types:**
```
/phase-g-field-resolvers PRODUCT-BE-G-01
```

**Copilot does:**
1. No spike gating on this one (`Depends on: —`) — proceeds straight to implementation.
2. Reads the story's **literal pseudocode block** (`AttachmentEnrichmentService`: `relationshipClient.searchByIds` → 5-bucket partition → per-bucket hydration via 3 clients → flatten → draft filter → sort by `typeRank()` then `createdAt` descending) and ports it directly rather than redesigning — the ordering and tiebreak are exactly what the AC and parity tests check.
3. Notices the story explicitly preserves a known gap: `.filterNot { it.isDraft }` with the comment "ACL should eventually own this — tracked as follow-up." Copilot keeps this as-is, adds `// TODO(PRODUCT-BE-G-01): draft filter should move to ACL layer — see story` rather than either silently fixing it or silently leaving it unexplained.
4. Implements the 4 client calls (`relationshipClient`, `attachmentClient` v2+v3, `discussionClient` ×2, `sampleClient`), the merge, and the sort exactly as specified.
5. Tests per AC: parity across the mixed attachment/discussion/thread/sample sources, and an explicit ordering test — product=0, discussion=1, sample=2, `createdAt` descending tiebreak — asserting on actual sorted output, not just count.
6. Reports AC line by line, showing the sorted test output as evidence (per the phase-G prompt's instruction not to just say "tests pass" for ordering-sensitive stories), and calls out the TODO it left.

**What's distinct here:** Phase G is where "port the legacy logic faithfully, including its documented rough edges" matters most — the temptation to "improve" a 150-line merge while porting it is exactly what the prompt is written to suppress.

---

## What's common across all seven

- Every phase starts from the same `copilot-instructions.md` (repo shape, story-id scheme, ACL-is-context-only, no-invented-rollback).
- Every phase ends the same way: AC walked line by line with evidence, PR description drafted in bullets.
- The phases differ only in **when Copilot stops to ask vs proceeds**:
  - **A, B, G (no gating):** proceed straight through; G additionally preserves documented legacy quirks instead of fixing them.
  - **C, D (spike-gated, story gives or omits a fallback):** proceeds with a clearly-marked interim if the story provides one (C), otherwise asks which interim the Engineer wants (D).
  - **E (spike-gated, no fallback at all):** stops completely; offers only inert scaffolding until the spike resolves.
  - **F (deployment-blocked, not spike-gated):** asks whether the *other team's* subgraph is live; can prepare code ahead of the block but flags it must not ship ahead of it.
