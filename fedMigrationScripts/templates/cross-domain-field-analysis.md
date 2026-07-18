# Template: Cross-Domain Field Analysis (`be-06-cross-domain-field-analysis.md`)

This template defines the exact format for Phase 6 output, produced by
`generatescripts/generate_schema_analysis.py`. Regenerated, never hand-edited.

---

## File Header Block

```markdown
# Phase 6: Cross-Domain Field Analysis — {Domain Display Name}

> **Domain:** `{loader-key}`
> **Target DGS:** `{target-dgs-label}`
> **Pipeline Version:** 1.0
> **Generated:** {YYYY-MM-DD}
> **Depends on:** [be-02-resolver-analysis.md](./be-02-resolver-analysis.md) · [be-03-schema.graphql](./be-03-schema.graphql)
> **DGS Target Status:** Green-field
```

## Summary (Mandatory)

```markdown
## Summary

| Metric | Count |
|---|---|
| Total resolvers scanned | {n} |
| Resolvers with cross-domain/EXT dependency | {n} |
| Very High complexity | {n} |
| High complexity | {n} |
| Medium complexity | {n} |
| Low complexity | {n} |
| Cross-domain fields with no client usage found | {n} |
```

## Cross-Domain Field Dependencies Table (Mandatory)

```markdown
## Cross-Domain Field Dependencies

| Resolver | Requires (loader key → owner) | Client usage | Complexity | Recommendation |
|---|---|---|---|---|
| `{Type.field}` | `{loaderKey}` ({owner label}) | `{opName}` or ⏭ not found in ClientCallingGqlQueries | {complexity} | {recommendation} |
```

- `Resolver` uses `Query.{name}` / `Mutation.{name}` / `{TypeName}.{field}` — matches the
  resolver-map block name, not the GraphQL schema type where they differ.
- `Requires` lists every non-own, non-`accessControl` loader key referenced in that
  resolver's body, each with its catalog-resolved owner label. Multiple keys are
  comma-separated.
- `Client usage` lists up to 3 matching client operation names (from
  `ClientCallingGqlQueries/`), or the unused marker.
- `Recommendation` uses exactly one phrase from `output-conventions.md` §14.

## Recommendation Legend (Mandatory, fixed text)

```markdown
## Recommendation Legend

- **@requires field composition** — single co-located phase-1 domain (same `plm-product` subgraph); compose via Federation `@requires`, no gateway hop.
- **Co-locate + @requires** — multiple phase-1 domains feed one field; keep co-located, sequence the `@requires` chain, document ordering.
- **Entity resolver (@key + @DgsEntityFetcher)** — the dependency lives in a separate DGS subgraph; needs a federation entity fetcher on the owning side.
- **Gateway stitch (@extends stub)** — external platform (VMM/IG/Doppler/Corona/etc); no DGS migration, the gateway resolves the stub directly.
- **No cross-domain dependency** — resolves locally; no federation work needed.
```

## Response Footer (Mandatory)

```markdown
---
**Phase Completed:** Phase 6 — Cross-Domain Field Analysis · **Domain:** `{loader-key}` · **Cross-domain fields:** {n}/{total}
```

---

## Program Roll-Up (`schemaAnalysis/00-cross-domain-field-inventory.md`)

Sections, in order: Program Totals table, By Domain table (links to each domain's be-06),
Unused Cross-Domain Fields (grouped per domain — deferral candidates). See
`generate_schema_analysis.generate_rollup()` for the generator.
