---
applyTo: "apps/app/**/service/**/*.kt, apps/app/**/client/**/*.kt"
description: "Kotlin REST service / client rules for plm-product (apps/app module)"
---

# Kotlin service and REST client rules

## Scope of a story's service change

- The REST controllers and core services **already exist** — a migration story adds at most a thin service method that the new data fetcher needs (a missing read variant, a param mapping), never a re-implementation.
- **Before writing any service method, find the existing REST controller/service in `apps/app` that already serves the same resource** (the endpoint the story's *Today* line names — each DGS repo hosts the REST endpoints its DGS layer wraps). Reuse that service method from the fetcher; only add a new method when no existing one covers the read/write variant, and model it on the sibling methods around it.
- Use the existing HTTP client wiring (declared clients per backend service); do not introduce a second HTTP stack.
- Backend endpoints, verbs and payloads come from the story's *Current Behaviour* and the operation's pseudo-logic in `output/initial-analysis/{domain}/02-resolver-analysis.md` at https://github.com/XXX — copy the legacy call sequence, do not redesign it.

## Parity traps (verified in analysis — preserve them)

- The legacy gateway converts snake_case backend payloads to camelCase in specific operations — replicate that conversion exactly where the story notes it.
- Some legacy operations tolerate partial backend failure per target (one failure is visible, the rest proceed) — keep that isolation.
- Multi-step writes (workspace-association PUT → body PUT → permissions PUT) keep today's step order and failure behaviour until `SPIKE-01` decides the saga strategy.

## Style

- Constructor injection, immutable `data class` DTOs, no `!!`.
- Suspend/reactive style must follow what the module already uses — match surrounding code, do not mix paradigms.
- Log the backend call target and story id at debug level in new methods; no payload logging.
