---
name: cross-domain-field-analysis
description: "For every query, mutation, and field resolver in a domain, identifies which OTHER domains or services it must hydrate from, cross-checks whether the field is used by a real frontend client operation (ClientCallingGqlQueries), rates complexity, and recommends a federation resolution (entity resolver / @requires / gateway stitch / defer). Output: output/{domain}/be-06-cross-domain-field-analysis.md + program roll-up output/schemaAnalysis/00-cross-domain-field-inventory.md"
argument-hint: "Provide the domain whose resolver analysis (Phase 2) is complete. Example: 'Run cross-domain field analysis for bom' or 'Regenerate schema analysis for all domains'."
---

# Skill: Cross-Domain Field Analysis

## Purpose

Answer, for every resolver in a domain: *which other domain does this need to hydrate,
is anyone actually calling it from the frontend, how complex is it, and how should
federation resolve it?* This is Phase 6 — it runs after resolver analysis (Phase 2) and
schema derivation (Phase 3), and feeds migration-story prioritization by flagging fields
with no client usage as deferral candidates.

## When to Use

- After `be-02-resolver-analysis.md` and `be-03-schema.graphql` exist for a domain
- Before finalizing which cross-domain fields get a federation story vs. a defer/drop story
- When the PO asks "which fields actually need another team's subgraph to be ready first?"
- As a program-wide health check on client-usage coverage (the roll-up)

## Cannot Run Without

- `output/{domain}/be-02-resolver-analysis.md` (EXT Service Call Inventory — the source of
  truth for which loader keys a domain calls)
- `code/resolvers/**/*.txt` (the actual resolver source — parsed directly, not just the
  markdown summary, because be-02's EXT table format varies by domain and by author)
- `ClientCallingGqlQueries/*.txt` + `QUERY_INVENTORY.md` (client usage cross-check)
- `fedMigrationScripts/reference/domain-service-catalog.md` (loader key → owning domain /
  sibling DGS / external platform catalog — the single source of truth for classification;
  add missing loader keys here, never hardcode them in the generator)

## How It Works

This is a **generated artifact**, not a hand-authored analysis pass — run the generator:

```
python fedMigrationScripts/generatescripts/generate_schema_analysis.py            # all domains
python fedMigrationScripts/generatescripts/generate_schema_analysis.py bom        # one domain
```

The generator (`generate_schema_analysis.py`):
1. Parses each domain's `code/resolvers/**/*.txt` resolver map (`Query`/`Mutation`/`TypeName`
   blocks) and extracts every `ctx.loaders.<key>` reference per field, excluding the domain's
   own loader key and `accessControl` (ACL is analyzed separately — see
   `acl-usage-analysis` skill).
2. Classifies each loader key via `domain-service-catalog.md`: `phase1-domain` (co-located,
   same `plm-product` subgraph), `sibling-dgs` (separate DGS, needs a federation entity
   fetcher), or `platform` (external, gateway-stitched stub only).
3. Cross-references every cross-domain field against the client-operation index built by
   `generate_frontend.py`'s parser (imported directly — not reimplemented) to find real
   frontend usage, or flags the field as unused.
4. Rates complexity by EXT-key count + polymorphism bump, same Low/Medium/High/Very High
   scale as `output-conventions.md` §4.
5. Recommends a resolution per the vocabulary in `output-conventions.md` §14.

## When the Catalog Is Missing a Loader Key

If a resolver's loader key doesn't resolve to a real owner, the recommendation column reads
"Needs manual review — unclassified loader key" — this means `domain-service-catalog.md`
is missing that key, not that the field has no cross-domain dependency. Fix the catalog
(add a row to the "EXT loader keys" table with the correct owner/migrate-target/severity),
never patch around it in the generator — the catalog is the single source of truth other
skills (`resolver-dependency-analysis`) also read.

## Output Format

Per domain: `output/{domain}/be-06-cross-domain-field-analysis.md` — header block, summary
table, one row per cross-domain resolver (resolver id, loader keys → owners, client usage,
complexity, recommendation), recommendation legend, response footer.

Program roll-up: `output/schemaAnalysis/00-cross-domain-field-inventory.md` — totals by
domain, complexity breakdown, and a consolidated "unused cross-domain fields" list (deferral
candidates) grouped by domain.

⚠ Regeneration overwrites both — never hand-edit; fix the generator or the catalog instead.

## Next Skill

Findings here inform migration story prioritization (`migration-story-generation`) — fields
with no client usage are candidates for a defer/drop story instead of a federation story.
