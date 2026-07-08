---
applyTo: "**/service/**/*.kt, **/client/**/*.kt"
description: "Kotlin REST service / client rules for spark-claims"
---

# Kotlin service and REST client rules

## Scope of a story's service change

- The REST controllers and core services **already exist** — a migration story adds at most a thin service method that the new data fetcher needs (a missing read variant, a param mapping), never a re-implementation.
- **Before writing any service method, find the existing REST controller/service that already serves the same resource** (the endpoint the story's *Current Behaviour* line names). Reuse that method from the fetcher; only add a new one when no existing method covers the read/write variant, modeled on the sibling methods around it.
- Use the existing HTTP client wiring (declared clients per backend service, e.g. the `workspaceV2` client `updateClaim` calls); do not introduce a second HTTP stack.
- Backend endpoints, verbs and payloads come from the story's *Current Behaviour* and the operation's pseudo-logic in `output/initial-analysis/claims/02-resolver-analysis.md` at https://github.com/XXX — copy the legacy call sequence, do not redesign it.

## Parity traps (verified in analysis — preserve them)

- `updateClaim` today: 1) proxy-ACL permission check (context-only, not built) → 2) `workspaceAssociationHelper(CLAIM, humanId, add, remove)` only if `workspaceContext.{add,remove}` is non-empty → 3) `PUT {base}/{humanId}` → 4) **throw on `validationErrors`/`message`**, no rollback. Keep this exact step order and throw behaviour until `SPARK-SPIKE-01` decides the saga strategy.
- `getClaimByIds` uses an ACL-context token in its call; `getClaims` explicitly has **no ACL token** — do not add one.
- The legacy gateway converts snake_case backend payloads to camelCase — replicate that conversion exactly where the story notes it.

## Style

- Constructor injection, immutable `data class` DTOs, no `!!`.
- Suspend/reactive style must follow what the module already uses — match surrounding code, do not mix paradigms.
- Log the backend call target and story id at debug level in new methods; no payload logging.
