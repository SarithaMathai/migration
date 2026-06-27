# Skill 02 — Resolver Dependency Analysis (Pipeline 2.0)

> **Output:** `output/{domain}/02-resolver-analysis.md` · **Audience:** Engineers (the implementation spec)
> **Depends on:** `01-schema-inventory.md`. **Source of truth:** the `.txt` resolver/service/utils.

Produce plain-English **pseudo-logic** for every operation so a junior implements without reading JS.
This artifact is later embedded into each Jira story's "Current Behaviour". If it is vague here, the
story is vague — so **no forbidden phrases** ("various transformations", "standard error handling").

## What to document, per operation

For each `Query`, `Mutation`, and **non-trivial** field resolver:

- **Schema signature** (read from `code/schemas/SPARK_{Domain}.txt`; confirm args/return against the resolver).
- **Resolver location** `file.txt:start-end`.
- **Complexity** Low / Medium / High / Very High (+1 tier for `__resolveType`; +1 for `isExternal` branch).
- **Pseudo-logic** — numbered steps; sub-bullets for each branch (internal/external, 404, empty, etc.).
- **Service calls** table — method · HTTP · endpoint (from the service file) · purpose.
- **EXT Service calls** — every `ctx.loaders.{otherKey}` tagged `key · url · repo · severity 🔴/🟡/🔵`.
- **Pagination**, **error handling** (one line per path), **side effects** (workspace assoc, perms),
  **user bifurcation** (document BOTH paths when the resolver branches on `ctx.currentUser.internal`).

For **service classes**: base URL + each method's verb/path/headers/request-body/response-transform.
For **utils**: each used function's steps + its DGS equivalent.

## Trivial field resolvers
Group pass-throughs (`field: (p) => p.field`, no service call) in one table at the end — do **not** give
them pseudo-logic blocks. They still appear in `05-attribute-inventory.md` as `Direct`.

## Section order (mandatory)
Header → Summary Statistics → Helper Functions (only if shared by ≥2) → Query Resolvers → Mutation
Resolvers → Field Resolvers (+ trivial table) → Service Classes → Referenced Utils → EXT Service Call
Inventory (master table + `{n} total — {n}🔴/{n}🟡/{n}🔵`) → Complexity Assessment → Key Findings
(highest-risk, migration blockers, refactor recommendations, quick wins, **latent bugs**).

ID prefixes: `H/Q/M/F/S/U` sequential.

## Completion criteria
- [ ] Every query/mutation has a pseudo-logic block with exact endpoint + every error/branch path.
- [ ] Every non-trivial field resolver documented; trivial ones tabled.
- [ ] Every `ctx.loaders.{otherKey}` appears once in the master EXT inventory with severity.
- [ ] Internal/external bifurcations documented as two explicit paths.
- [ ] No forbidden phrases. Latent bugs called out for the Key Findings + risk register.
