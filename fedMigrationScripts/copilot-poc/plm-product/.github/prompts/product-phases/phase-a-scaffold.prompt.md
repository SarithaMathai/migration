---
mode: agent
model: Claude Sonnet 4.5
description: "Phase A — module scaffold or a type-resolver story (e.g. BOM-BE-A-04) in apps/app"
---

Implement Phase-A story **${input:storyId:BOM-BE-A-04}** in `apps/app`.

Phase A is the **Foundation & Type Resolvers** phase. It's either:
- the **one-time DGS module scaffold** for a domain (usually folded into that domain's `B-01` story as a "DGS Module Init" note — `product.graphqls` header/scalars/external stubs, `ScalarConfig.kt`, service + Feign wiring), or
- a **standalone type-resolver story** for a polymorphic interface/union (e.g. `BOM-BE-A-04`'s `@DgsTypeResolver` for `BomMaterialInterface`/`BomImpressionDetailsInterface`).

Steps:

1. Read the story's *Current Behaviour* (the legacy switch/dispatch logic — e.g. category-code → concrete-type mapping) and *Target DGS Implementation* from the Jira ticket or `output/initial-analysis/{domain}/04-stories.md` at https://github.com/XXX.
2. If it's a type resolver: mirror the legacy switch **exactly**, including the default/fallback branch — do not "clean up" or reorder the mapping. Source magic codes into a constants file if the story asks (e.g. `BomConstants.kt`) rather than leaving literals inline.
3. If it's a module scaffold: create the domain's `.graphqls` file (federation v2.3 header, scalars, `@key` owned types, external stubs per `.github/instructions/graphql/schema.instructions.md`), register scalars, wire the service + Feign client. This unblocks every later B/C/D/G story in the domain — do not add any query/mutation logic here, only the shell.
4. Implement per `.github/instructions/kotlin/datafetcher.instructions.md` (`@DgsTypeResolver(name = "...")`) and write tests per `.github/instructions/kotlin/testing.instructions.md`: **one test per concrete type + one for the unknown-code fallback**.
5. Report acceptance criteria one by one with evidence — for a type resolver, show the full code→type table you verified against, not just "tests pass."

No spike gating applies to Phase A. No ACL logic.
