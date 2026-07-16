# Run the migration pipeline for a NEW domain

Copy one of the ready-to-run blocks below (or the generic template) into Claude Code / Copilot to analyze
a new domain end-to-end and produce all audience artifacts. The framework lives in this `scripts/` folder.

## What a run produces

For domain `{X}` it creates `finalOutput/{x}/` with the 8 analysis files
(`01-schema-inventory`, `02-resolver-analysis`, `03-schema.graphql`, `03-schema-analysis`,
`04-stories`, `04-stories-index.yaml`, `04-po-summary`, `05-attribute-inventory`), then the consumption
layer (`confluence/{x}.md`, refreshed `jira/` via `generate.py`), and refreshes the program rollups.

## Generic prompt (template)

```
Analyze the GraphQL domain "{DOMAIN}" for the Spark → plm-product DGS migration, following the
framework in finalOutput/scripts/ (skills 01 → 02 → 03 → 04 → 05 → 06, reference-output-conventions,
reference-federation-patterns, domain-service-catalog).

Sources (the SDL is the schema source of truth; cross-check behaviour against the resolver):
- schema  : code/schemas/{SPARK_Domain}.txt
- resolver: {resolver path}
- service : {service path}
- utils   : whatever the resolver imports

Produce finalOutput/{domain}/01..05 per the skills, then run skill-06 (consumption):
- write confluence/{domain}.md (PO page, per skill-06 outline)
- run: python finalOutput/jira/generate.py   (regenerates {domain}.csv, {domain}-stories.md, all-stories.csv)
- update the program rollups: STORIES-INDEX.md, index.yaml, README.md §3, confluence/00-portfolio.md

Apply these review rules (learned on the first four domains):
- The SDL is authoritative for fields, return types, and nullability — do NOT tighten args to `!`
  beyond the SDL.
- Flag any SCHEMA-DRIFT op (declared in the SDL but with no top-level resolver) as ⏭ with a note.
- Do NOT expose record-only properties (read internally by field resolvers) as schema fields.
- If you synthesize an entity @key not present in the SDL type, say so and flag it to confirm.
- Counts must equal the enumerated stories (totals.story_count == number of stories[] entries).
- ACL is context-only — note where the source curries a capability token; create no ACL story.
```

Then `add a catalog row` for the domain in [`domain-service-catalog.md`](./domain-service-catalog.md).

---

## Ready-to-run blocks (the four next domains)

> **Subgraph note:** `productDetails` and `watchlist` are **co-located in the `plm-product` monorepo**
> (their service uses the `enterprise_product_development_products` base; links to/from Product are internal
> types). `claims` and `search` are **separate DGS subgraphs** — model their cross-references to
> Product/others as true federation (`@extends @external`) and say so in their `03-schema-analysis`.
> (Decide co-located vs separate from the **service base path**, not assumptions.)

### claims
```
Analyze the GraphQL domain "claims" per finalOutput/scripts/ (skills 01→06).
- schema  : code/schemas/SPARK_Claims.txt          (157 lines, SDL — source of truth)
- resolver: code/resolvers/product/SPARK_Claims.txt
- service : code/services/Claim.txt
Separate DGS subgraph (not the plm-product monorepo). Output finalOutput/claims/01..05 + confluence/claims.md,
run python finalOutput/jira/generate.py, and refresh STORIES-INDEX.md / index.yaml / README.md / portfolio.
Follow the review rules in RUN-NEW-DOMAIN.md (SDL authoritative; flag schema-drift; no record-only fields;
confirm synthesized @key; counts == enumerated stories; ACL context-only).
```

### productDetails
```
Analyze the GraphQL domain "productDetails" per finalOutput/scripts/ (skills 01→06).
- schema  : code/schemas/SPARK_ProductDetail.txt    (139 lines, SDL — source of truth)
- resolver: code/resolvers/product/SPARK_ProductDetail.txt
- service : code/services/product/ProductDetails.txt
Co-located in the plm-product monorepo (links to/from Product are internal types, not federation).
Output finalOutput/productDetails/01..05 + confluence/productDetails.md, run python finalOutput/jira/generate.py,
and refresh the program rollups. Follow the review rules in RUN-NEW-DOMAIN.md.
```

### watchlist
```
Analyze the GraphQL domain "watchlist" per finalOutput/scripts/ (skills 01→06).
- schema  : code/schemas/SPARK_Watchlist.txt        (98 lines, SDL — source of truth)
- resolver: code/resolvers/product/SPARK_Watchlist.txt
- service : code/services/product/Watchlist.txt
Co-located in the plm-product monorepo (service uses the enterprise_product_development_products base);
it contributes ResourcesCount.watchlists to Product TechPack INTERNALLY (CAT-2, like bom/measurement —
see PRODUCT-BE-F-08). Output finalOutput/watchlist/01..05 + confluence/watchlist.md, run
python finalOutput/jira/generate.py, and refresh the program rollups. Follow the RUN-NEW-DOMAIN.md rules.
```

### search
```
Analyze the GraphQL domain "search" per finalOutput/scripts/ (skills 01→06).
- schema  : code/schemas/SPARK_Search.txt           (655 lines, SDL — source of truth; large)
- resolver: code/resolvers/SPARK_Search.txt
- service : code/services/Search.txt
Separate DGS subgraph (elastic-backed); many product-family domains depend on it (🔴). Read the large
files in windows. Output finalOutput/search/01..05 + confluence/search.md, run
python finalOutput/jira/generate.py, and refresh the program rollups. Follow the RUN-NEW-DOMAIN.md rules.
```

---
*After any run, `jira/generate.py` auto-discovers the new `finalOutput/{domain}/04-stories-index.yaml` —
no generator change needed. See [`skill-06-consumption-artifacts.md`](./skill-06-consumption-artifacts.md).*
