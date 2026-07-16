# Reference — Output Conventions (condensed, Pipeline 2.0)

Cross-cutting rules every artifact follows.

## Header block (every `.md`)
```
# Phase {N}: {Phase Name} — {Domain Display Name}
> **Domain:** `{loader-key}`
> **Target DGS:** `{ServiceClass}` (repo: `{repo}`, url: `{base-url}`)
> **Pipeline Version:** 2.0
> **Generated:** {YYYY-MM-DD}
> **Source of truth:** schema (`code/schemas/SPARK_{Domain}.txt`) + resolver + service + utils (`.txt` snapshot; no config)
> **Depends on:** {relative links or "None (entry phase)"}
```

## Status symbols (only these three)
✅ exists in DGS · 🔜 needs migration (default) · ⏭ deferred.
Gap summary line: `{n} ✅ | {n} 🔜 | {n} ⏭ — {total} total`. Green-field → `0 ✅ | n 🔜 | m ⏭`.

## Complexity tiers (stories carry these; no day-ranges in stories)
Low · Medium · High · Very High. +1 tier for `__resolveType` polymorphism; +1 for `isExternal` branch.
Day-ranges appear **only** in `be-04-po-summary.md`, labeled "AI-estimated, confirm in refinement".

## EXT severity
🔴 RED (critical/sequential/merged) · 🟡 YELLOW (single enrichment call) · 🔵 BLUE (optional / gateway).
Format: `**EXT Service** → key: \`{key}\` · url: \`{url}\` · repo: \`{repo}\` · severity: 🔴/🟡/🔵`.

## Risk register
`| Risk | Likelihood | Impact | Mitigation | Owner |` — owner ∈ {PO, Tech Lead, Backend Eng, Platform, Gateway Team}.

## Forbidden phrases (Phase 2 / story Current Behaviour)
"various transformations", "standard error handling", "handles typical cases", "calls the appropriate
service", "returns the expected fields" → always replace with the specific endpoint/field/branch.

## Per-domain artifact set (Pipeline 2.0)
**Analysis (source of truth):** `be-01-schema-inventory.md` · `be-02-resolver-analysis.md` ·
`be-03-schema.graphql` · `be-03-schema-analysis.md` · `be-04-stories.md` · `be-04-stories-index.yaml` ·
`be-04-po-summary.md` · `be-05-attribute-inventory.md`.
**Consumption (skill 06):** `../confluence/{domain}.md` (PO page) · `../jira/{domain}.csv` (bulk import) ·
`../jira/{domain}-stories.md` (per-issue). See [`skill-06-consumption-artifacts.md`](./skill-06-consumption-artifacts.md).
