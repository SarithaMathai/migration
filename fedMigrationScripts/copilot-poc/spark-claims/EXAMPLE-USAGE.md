# Example usage — chat modes, prompts, and instructions in action

Two worked sessions: a simple story that goes straight through, and the one complex story in this domain that gets blocked at the spike gate. Both use real content from `output/analysis/claims/be-04-stories.md`.

---

## Walkthrough 1 — implementing a simple story (`CLAIM-BE-B-01`)

**Setup:** in VS Code, open Copilot Chat, pick **story-implementer** from the chat mode dropdown.

**Engineer types:**

```
Implement CLAIM-BE-B-01
```

**What fires, in order:**

1. **`copilot-instructions.md`** is already loaded — Copilot knows this is a standalone claims subgraph, that stories are self-contained one-PR units, and that ACL/proxy-ACL is context-only.
2. Gate check: `CLAIM-BE-B-01` is Phase B, not `E-01`, no `SPIKE-0x` → not gated → proceeds.
3. Read the contract — the Engineer pastes the Jira ticket text:

   > **`getClaims(parentHumanId, claimHumanIds, partnerIds)`** · Type: Query · Phase: B · Complexity: Low · Depends on: —
   > **Current Behaviour:** (own) `claim.getClaims.load({parentHumanId, claimHumanIds, partnerIds})` → `GET {base}` (filtered) → camelCase. No ACL token.
   > **Target:** `@DgsQuery → [Claims]`.
   > **Note:** this PR also creates the one-time `claims.graphqls` module scaffold + `ScalarConfig.kt` + service/Feign wiring — every later B/C/D/G story assumes it.
   > **Acceptance Criteria:** 1) filters by the 3 args.

4. Plan the diff — Copilot lists files and waits:

   ```
   Planned diff for CLAIM-BE-B-01:
   - claims.graphqls                        (new: Claims @key type, Query.getClaims, scalar registration)
   - ScalarConfig.kt                        (new: scalar wiring)
   - ClaimsDataFetcher.kt                   (new: @DgsQuery getClaims)
   - ClaimsClient.kt                        (Feign client wiring, if not already present)
   - src/test/.../ClaimsDataFetcherTest.kt

   Confirm to proceed?
   ```

5. Engineer replies `yes`. Implementation pulls in the path-scoped instructions automatically:
   - `claims.graphqls` → `.github/instructions/graphql/schema.instructions.md` (single schema file, `Claims` is owned here).
   - `ClaimsDataFetcher.kt` → `.github/instructions/kotlin/datafetcher.instructions.md` (`@DgsQuery` in a `@DgsComponent`, no ACL token — the story explicitly says none).
   - `ClaimsClient.kt` → `.github/instructions/kotlin/service.instructions.md` (reuse the existing `GET {base}` call, filtered by the 3 args, no ACL wiring added).
   - the test → `.github/instructions/kotlin/testing.instructions.md` (Low complexity → happy path + one error path).
6. Verify — Copilot runs the build and test, then reports:

   ```
   ✅ AC1 — filters by parentHumanId / claimHumanIds / partnerIds  (ClaimsDataFetcherTest.filters claims by all three params)
   ```
7. PR — branch `feature/spark-clm-b01`, description drafted with the Hive push note.

**Optional follow-up:** switch to **parity-checker** (or `/write-parity-tests getClaims CLAIM-BE-B-01`) to confirm the response shape matches the legacy gateway exactly, then **schema-steward** to review `claims.graphqls` before the Hive push.

---

## Walkthrough 2 — the spike-gated story (`CLAIM-BE-E-01`)

**Engineer types:**

```
/check-spike-gate CLAIM-BE-E-01
```

**Copilot responds** (from `.github/prompts/story/check-spike-gate.prompt.md`, which has the spike table inline):

```
Gated — SPIKE-01 (Non-Atomic Write Saga).

Decision to make: pick (a) compensating saga, (b) compensation-log +
best-effort, or (c) best-effort — and write down how to undo each step.
Status: Open.

updateClaim's current 3-step sequence (proxy-ACL check → conditional
workspace association → body PUT, throw on validation error, no
rollback) stays as-is until this spike concludes — do not add
compensation logic yourself.

See Phase 0 — Program Spikes / Spike Detail on the global Confluence
overview, and output/complexStories/non-atomic-write-saga/ for
research so far.
```

If the Engineer then tries `/implement-story CLAIM-BE-E-01` anyway, the **story-implementer** chat mode's own gate check catches it independently and refuses to write the failure-strategy code, asking for confirmation the spike decision is recorded first.

**Separately — federation blocking, not a spike:** if the Engineer instead asks about `CLAIM-BE-F-01` (`Product.claims`), the same prompt reports it as **Blocked by `plm-product`** (the `Product` entity must exist there first) rather than spike-gated — a different kind of hold that the prompt and chat mode both distinguish from `SPIKE-0x` gating.

---

## Quick reference — what to invoke when

| Situation | Use |
|---|---|
| Starting any story | chat mode **story-implementer**, or `/implement-story {id}` |
| Not sure if a story is blocked (spike or federation) | `/check-spike-gate {id}` |
| Adding/extending schema, incl. F-01/F-02 contributions into `plm-product` | `/derive-dgs-schema` |
| Verifying a finished operation matches legacy behaviour | chat mode **parity-checker**, or `/write-parity-tests {operation} {id}` |
| Reviewing a PR that touches `.graphqls` | chat mode **schema-steward** |
| Copilot coding agent working an assigned GitHub issue autonomously | reads `AGENTS.md` + `copilot-instructions.md` on its own, no manual invocation |
