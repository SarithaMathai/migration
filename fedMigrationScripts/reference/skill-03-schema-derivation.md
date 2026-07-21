# Skill 03 — Federation Target-Schema Derivation (Pipeline 2.0)

> **Outputs:** `output/{domain}/be-03-schema.graphql` + `output/{domain}/be-03-schema-analysis.md`
> **Audience:** Architects (schema), plus the **Confluence "approach" page** (analysis).
> **Source of truth:** the **source SDL** at `code/schemas/SPARK_{Domain}.txt` (now present in the
> snapshot). The `be-03-schema.graphql` is the **federated target** schema you *translate* from that SDL —
> renamed/restructured for Netflix DGS — verified against the resolver for behaviour. (It is still
> "derived" in the sense that it is a transform of the source; it is no longer guessed from resolver shapes.)

## be-03-schema.graphql — translate the source SDL into the federated target

Start from `code/schemas/SPARK_{Domain}.txt` (the real SDL: it already gives you operations, args,
nullability, types, inputs, `union`/`interface`, and `@deprecated`). Then transform for federation:

1. **Operations:** keep every `Query`/`Mutation` field from the SDL verbatim (names, args, nullability).
   Use the resolver only to confirm each has a top-level resolver — mark any **schema-drift** op
   (declared in SDL, no resolver) as ⏭ with a note.
2. **Owned types:** carry each `SPARK_{Domain}*` type across; **drop the `SPARK_` prefix** (convention).
   Apply `@key(fields: "id")` (or the real key) to top-level entities; embedded value types get no `@key`.
3. **Interfaces/unions:** carry the SDL `union`/`interface` across; the resolver's `__resolveType` block
   gives you the concrete-type mapping for the analysis doc.
4. **External stubs:** every type owned elsewhere (VMM_*, sibling DGS types) → `@extends @external` stub.
5. **Shared types** (`Paging`, `CodeDescription`, `UnitsOfMeasure`, …) → `@shareable`.
6. Header comment block + status legend (🔜 default green-field). Every field/op preceded by a `#`
   comment with status + one-line purpose. Body order per `output-conventions-condensed` §8.
7. Header note: `# TARGET schema translated from code/schemas/SPARK_{Domain}.txt — nullability from SDL`.
   Where the SDL and resolver disagree on behaviour, the resolver wins; note the discrepancy.

## be-03-schema-analysis.md — sections (mandatory)

1. Header block.
2. **Type Classification** table — every type → Owned / Embedded / External-stub / Shared / Input / Enum.
3. **External Type Stubs** table — stub · owning DGS · federation strategy · severity.
4. **Federation Boundaries** — which types this domain owns vs. extends; composite-key entities.
5. **Client Contract Verification** — every query+mutation confirmed preserved (`{n} ✅ | {n} 🔜 | {n} ⏭`).
6. **Migration Approach** *(this section is the Confluence approach page)* — recommended sequencing,
   the chosen federation pattern per cross-domain boundary, and any Option A/B/C/D facade decisions.
7. **Risks & Recommendations** (table per `output-conventions-condensed` §6).

## Completion criteria
- [ ] Every operation and type from the source SDL appears in the target schema (nullability preserved).
- [ ] `@key` only on real entities; `@shareable`/`@extends` applied correctly.
- [ ] Interfaces + every concrete variant present; `__resolveType` mapping captured in analysis.
- [ ] Header cites `code/schemas/SPARK_{Domain}.txt` as the source; any SDL-vs-resolver discrepancy noted.
- [ ] Analysis has a **Migration Approach** section suitable for a Confluence page.
