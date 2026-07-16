# Skill 01 — Schema Inventory (Pipeline 2.0, snapshot-adapted)

> **Output:** `output/{domain}/be-01-schema-inventory.md` · **Audience:** Tech Lead
> **Reads from:** `code/schemas`, `code/resolvers`, `code/services`, `code/utils` (the `.txt` snapshot).
> See [`00-adapting-to-this-repo.md`](./00-adapting-to-this-repo.md) — there is **no** `context.js`
> (read endpoint/auth facts from the service constructor), but the **schema SDL is now present** at
> `code/schemas/SPARK_{Domain}.txt`; use it as the schema source of truth, cross-checked with the resolver.

## Procedure

1. **Look up the domain** in [`domain-service-catalog.md`](./domain-service-catalog.md): loader key,
   service class, schema file, resolver path, target DGS.
2. **Read the schema file** (`code/schemas/SPARK_{Domain}.txt`). Record line count, every `Query`/
   `Mutation` field, every object/input/`union`/`interface` type, and every `@key`/`@deprecated`
   directive. This is the authoritative contract.
3. **Read the resolver file** (`resolvers/.../SPARK_{Domain}.txt`). Record line count and reconcile it
   against the schema: confirm each operation has a top-level resolver (flag any **schema-drift** op
   that is declared in the SDL but has no resolver), note `__resolveType` blocks, and all `import`s.
4. **Read the service file** (`services/.../{Domain}.txt`). Record line count, the base endpoint built
   in the constructor, and every method with its HTTP verb, path, and auth header.
5. **Read referenced utils** (from the resolver's imports). Record each util file, line count, and the
   exported functions this domain uses. Map each to its DGS equivalent (catalog §3).
6. **Cross-domain references:** every `ctx.loaders.{otherKey}.*` call is an EXT dependency. Build the
   cross-domain table (Field/Operation · Referenced loader key · Owning DGS · Strategy · Severity).
7. **Co-located siblings:** other resolvers in the same folder (`resolvers/product/*`) targeting the
   same `enterprise_product_development_products` base — list them; they share `plm-product`.
8. **Schema status:** `From SDL (code/schemas/SPARK_{Domain}.txt, {n} lines) — cross-checked with resolver`.

## Mandatory sections (in order)

1. Header block (per `reference-output-conventions`).
2. Context Registration — service class, base endpoint (quote the constructor line), auth pattern.
3. Source File Manifest — schema / resolver / service / utils tables with line counts.
4. Import Graph — which files import which utils.
5. Cross-Domain Reference table (with severity).
6. Co-located siblings.
7. Hot Spots — polymorphic resolvers, internal/external branches, JWT-curried hot paths, latent bugs.
8. Summary Statistics.

## Completion criteria
- [ ] Schema, resolver, service, and every referenced util are line-counted.
- [ ] Base endpoint quoted verbatim from the service constructor.
- [ ] Every `ctx.loaders.{otherKey}` classified Internal / EXT / Gateway-stitch with severity.
- [ ] Large-file warning (⚠️) if any file > 1000 lines.
- [ ] Schema sourced from `code/schemas/SPARK_{Domain}.txt`; any schema-drift op (declared, no resolver) flagged.
