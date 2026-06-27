# Skill 05 — Attribute (Field) Inventory  *(new in Pipeline 2.0)*

> **Output:** `output/{domain}/05-attribute-inventory.md`
> **Purpose:** a flat, sortable, machine-parseable table of **every field on every type and every
> input object** in the domain, classified by how it is resolved and how hard it is to migrate.
> **Audience:** junior engineers (find your field fast), Copilot/agents (parse the table), POs
> (count of "special resolvers" = effort signal).

This artifact answers the question *"for this schema, which attributes are free, which need a special
resolver, which call another service, and how complex is each one?"* — in one screen, per domain.

---

## Why this exists

`01-schema-inventory.md` lists files. `03-schema.graphql` lists types. Neither lets a junior or PO see,
at a glance, **which individual attributes carry migration risk**. Most fields are free
(direct pass-through). A minority need a field resolver, and a smaller minority call an external
service. This table makes that distribution explicit and ties each non-trivial field to its story.

---

## How to build it

Enumerate every type and field from the source SDL (`code/schemas/SPARK_{Domain}.txt`) — that gives you
the exact field set and nullability. Then, for each field, use the resolver (`SPARK_Bom`,
`SPARK_BomMaterial`, … keys) to classify it into one **Resolution** kind:

| Resolution | Meaning | How to spot it in the resolver |
|------------|---------|--------------------------------|
| **Direct** | Pass-through; value comes straight from the parent object | No resolver entry, **or** `field: (p) => p.field` / `get(p,'x')` with no service call |
| **Computed** | Derived from parent fields only (no I/O) | Arrow fn that maps/filters parent data, no `ctx.loaders` |
| **Field-resolver** | Needs a same-backend service/loader call | Calls `ctx.loaders.{ownDomain}` or a util that does |
| **EXT** | Calls another domain/platform backend | Calls `ctx.loaders.{otherKey}` — tag severity 🔴/🟡/🔵 |
| **Polymorphic** | The field's type is an interface/union resolved by `__resolveType` | Field returns an interface; see the `__resolveType` block |

Then fill the table.

### Table 1 — Object-type attributes (mandatory)

```markdown
| Type | Attribute | GraphQL Type | Resolution | Resolver Loc | EXT (sev) | Complexity | Story |
|------|-----------|--------------|------------|--------------|-----------|------------|-------|
| `Bom` | `humanId` | `ID!` | Computed | `SPARK_Bom.txt:281` | — | Low | A02 |
| `Bom` | `access` | `AccessV3` | Field-resolver | `SPARK_Bom.txt:282` | — | Medium | G01 |
| `BomMaterial` | `libraryResource` | `HubMaterial` | EXT | `SPARK_Bom.txt:351` | 🟡 materialHub | High | G03 |
| `BomMaterial` | `materials` | `BomMaterialInterface` | Polymorphic | `SPARK_Bom.txt:315` | — | Very High | A04 |
```

Columns:
- **GraphQL Type** — copy from the SDL (`code/schemas/SPARK_{Domain}.txt`), including `!`/`[]` nullability.
- **Resolution** — one of the five kinds above.
- **Resolver Loc** — `file.txt:line` or `— (direct from parent)` for Direct.
- **EXT (sev)** — loader key + glyph, or `—`.
- **Complexity** — Low/Medium/High/Very High for the *field's* migration, not the whole op.
- **Story** — the `04-stories.md` ID that delivers this field.

### Table 2 — Input-object attributes (mandatory)

```markdown
| Input Object | Attribute | GraphQL Type | Required | Notes |
|--------------|-----------|--------------|----------|-------|
| `SparkBomInput` | `humanId` | `ID` | No | primeKey for update; absent on create |
| `SparkBomInput` | `workspaceContext` | `WorkspaceContextInput` | No | drives `manageBomWorkspaces` side-effect |
```

### Table 3 — Summary roll-up (mandatory)

```markdown
| Resolution kind | # fields | % | Migration signal |
|-----------------|----------|---|------------------|
| Direct | {n} | {x}% | Free — covered by schema story only |
| Computed | {n} | {x}% | Cheap — port the small mapping |
| Field-resolver | {n} | {x}% | Needs a fetcher + service method |
| EXT | {n} | {x}% | Needs CAT-4 federation/stitch |
| Polymorphic | {n} | {x}% | Needs `@DgsTypeResolver` + per-variant tests |
| **Total** | **{n}** | 100% | |
```

---

## Conventions

- Sort Table 1 by Type, then by Resolution severity (Polymorphic/EXT first, Direct last) so the risky
  rows are at the top of each type group.
- One row per field. Never collapse multiple fields into one row.
- Every non-Direct row must have a **Story** value (it is a bug if a field resolver has no story).
- Keep the same status/severity glyphs as `reference-output-conventions` (🔴/🟡/🔵).

## Completion criteria

- [ ] Every field of every object type is present exactly once.
- [ ] Every field of every input object is present exactly once.
- [ ] Each non-Direct field maps to a story ID that exists in `04-stories.md`.
- [ ] Summary roll-up percentages sum to 100%.
- [ ] Polymorphic interface fields and all their concrete-variant fields are represented.
