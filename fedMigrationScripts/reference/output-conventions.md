---
name: Output Conventions
description: "Universal conventions for every artifact produced by the migration pipeline. Apply when writing or editing any file under output/. Enforces header metadata, status symbols, effort scale, EXT severity, section ordering, and response footer format so all 37+ domains produce identical-shaped artifacts."
applyTo: "**/output/**/*.md,**/output/**/*.graphql,**/output/**/*.graphqls"
---

# Output Conventions — Universal Reference

Single source of truth for cross-cutting format rules used in every output artifact.
All skills reference this file. Do not invent alternative formats.

---

## 1. Output File Naming (Mandatory)

Every domain produces these files under `output/{domain}/`:

| Phase | File | Generator Skill |
|-------|------|----------------|
| 1 | `be-01-schema-inventory.md` | `skills/graphql-schema-inventory/SKILL.md` |
| 2 | `be-02-resolver-analysis.md` | `skills/resolver-dependency-analysis/SKILL.md` |
| 3 | `be-03-schema.graphql` | `skills/federation-schema-derivation/SKILL.md` |
| 3 | `be-03-schema-analysis.md` | `skills/federation-schema-derivation/SKILL.md` |
| 4 | `be-04-stories.md` | `skills/migration-story-generation/SKILL.md` |
| 4 | `be-04-po-summary.md` | `skills/migration-story-generation/SKILL.md` |

**Domain directory naming:** kebab-case matching the loader key (e.g., `product`, `bom`, `product-details`).

---

## 2. Mandatory Header Block (Every `.md` Output)

Every `.md` output file MUST start with this exact metadata block:

```markdown
# Phase {N}: {Phase Name} — {Domain Display Name}

> **Domain:** `{loader-key}`
> **Target DGS:** `{ServiceClassName}` (repo: `{repo-name}`, url: `{base-url}`)
> **Pipeline Version:** 1.1
> **Generated:** {YYYY-MM-DD}
> **Depends on:** {relative link list, or "None (entry phase)"}
> **DGS Target Status:** {Green-field (no existing DGS schema) | Existing schema found at {path}}
```

Rules:
- Use blockquote (`>`) for metadata — never a table, never a code block
- `Depends on` uses relative file links (e.g., `[be-01-schema-inventory.md](./be-01-schema-inventory.md)`)
- Phase 1's `Depends on` is `None (entry phase)`
- **Always include `DGS Target Status`** — tracks whether a green-field or gap analysis was done
- Include `Pipeline Version: 1.1` so future re-runs can be diffed

---

## 3. Status Symbols (Universal)

Use **only** these three symbols:

| Symbol | Meaning | When to Use |
|--------|---------|-------------|
| ✅ | **Exists in DGS** | Already implemented in target DGS repo (only if DGS files were provided) |
| 🔜 | **Needs migration** | Not yet in DGS — the default for green-field migrations |
| ⏭ | **Deferred** | Explicitly excluded from current cutover (admin-only, deprecated, or PO decision) |

Do not use ❌, ⚠️, ❓, 🚧, or any other glyph for status. Risk and complexity have their own scales.

**Required summary line** at the top of every gap analysis table:
```
{n} ✅ | {n} 🔜 | {n} ⏭ — {total} total
```

For green-field migrations (no DGS repo): always `0 ✅ | {n} 🔜 | {n} ⏭`.

---

## 4. Effort & Complexity Scale (Story-Level)

| Complexity | Effort | Day Range | Use When |
|-----------|--------|-----------|----------|
| **Low** | Small | 1–2d | Single REST call, no transformation, no EXT, < 20 lines of pseudo-logic |
| **Medium** | Medium | 3–5d | 2–3 service calls, modest transformation, ≤ 1 EXT, 20–60 lines |
| **High** | Large | 5–8d | 4+ service calls or 2+ EXT calls, multi-step orchestration, 60–150 lines |
| **Very High** | X-Large | 8–13d | Cross-domain aggregation, ≥ 8 EXT calls, polymorphic resolution, or bifurcation, > 150 lines |

Rules:
- **Complexity** label goes in story metadata; **Effort** label goes in PO summary
- Always add a **+20% buffer** to all domain-level totals
- Complexity bumps: +1 tier for `__resolveType` polymorphism; +1 tier for `isExternal` bifurcation

---

## 5. EXT Service Call Tagging (Mandatory)

Every cross-domain HTTP call must be tagged with this format wherever it appears:

```
**EXT Service** → key: `{loaderKey}` · url: `{url}` · repo: `{repo}` · severity: 🔴/🟡/🔵
Purpose: {one-line description of why this call is made}
```

### Severity Scale

| Severity | Criteria | Migration Treatment |
|----------|----------|---------------------|
| 🔴 **RED** | Critical to business logic; sequential EXT calls; data from multiple services merged | Full CAT-4 federation/stitching design required |
| 🟡 **YELLOW** | Important enrichment; single EXT call; partial response acceptable | Standard CAT-4 stub story |
| 🔵 **BLUE** | Optional enrichment; gateway can resolve | Pure gateway stitch; minimal CAT-4 effort |

Severity is mandatory on every EXT call — never omit.

---

## 6. Risk Register Format (Phases 3 and 4)

```markdown
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
```

- `Likelihood` and `Impact`: `Low` / `Medium` / `High`
- `Owner`: `PO`, `Tech Lead`, `Backend Eng`, `Platform`, `Gateway Team` — never leave blank

---

## 7. Section Ordering (Phase 2 — `be-02-resolver-analysis.md`)

Sections MUST appear in this exact order:

1. Header block
2. `## Summary Statistics`
3. `## Helper Functions` — **only if** resolver file defines helpers used by ≥ 2 resolvers; otherwise omit
4. `## Query Resolvers ({n})`
5. `## Mutation Resolvers ({n})`
6. `## Field Resolvers ({n})` — omit section if zero; include trivial pass-throughs table at end
7. `## Service Classes ({n})`
8. `## Referenced Utils ({n})`
9. `## EXT Service Call Inventory`
10. `## Complexity Assessment`
11. `## Key Findings`

ID prefixes: `H{n}` helpers, `Q{n}` queries, `M{n}` mutations, `F{n}` field resolvers, `S{n}` services, `U{n}` utils. Always sequential.

---

## 8. Schema File Conventions (`be-03-schema.graphql`)

Every schema file MUST begin with:

```graphql
# =============================================================================
# {Domain Name} Domain — Derived DGS Schema (Target State)
# Pipeline Version: 1.1
# Generated: {YYYY-MM-DD}
# DGS Target: Green-field (no existing schema) | Existing schema from {path}
# Source:    spark-internal-graphql/.../schemas/{file}.graphql
# Target:    {target-repo}/apps/app/src/main/resources/schema/{file}.graphqls
#
# Status Legend:
#   ✅  Exists in DGS  |  🔜  Needs migration  |  ⏭  Deferred
# =============================================================================
```

Schema body order (mandatory):
1. `extend schema @link(...)` (federation header, if needed)
2. Scalar declarations
3. External type stubs — `# --- External stubs (Gateway-only) ---`
4. Owned entity types with `@key` — `# --- Owned types ---`
5. Embedded/nested types — `# --- Embedded types ---`
6. Shared types (`@shareable`) — `# --- Shared types ---`
7. Input types — `# --- Inputs ---`
8. Enum types — `# --- Enums ---`
9. `extend type Query` — `# --- Queries ---`
10. `extend type Mutation` — `# --- Mutations ---`

Every query, mutation, and field MUST be preceded by a `#` comment with status symbol and one-line description.

---

## 9. Link Conventions

- All inter-output links use **relative paths** with `./` (e.g., `[be-02-resolver-analysis.md](./be-02-resolver-analysis.md)`)
- Story IDs in PO summary are bold text, not links (`**PRODUCT-BE-A-01**`)
- Story IDs in `be-04-stories.md` are headings (`### PRODUCT-BE-A-01 · {title}`) so anchor links work

---

## 10. Response Footer (Mandatory at End of Every Phase Run)

After completing any phase, the chat response MUST end with this block:

```markdown
---
**Phase Completed:** Phase {N} — {Phase Name}
**Domain:** `{loader-key}`
**Analysis Mode:** {Full | Quick Scan}
**DGS Target:** {Green-field | Existing schema found}
**Skills Applied:** {comma-separated list}
**Files Analyzed:** {n} files, {n} lines
**Target Service:** `{ServiceClassName}` ({repo})
**EXT Service Calls Found:** {n} total ({n} 🔴 RED / {n} 🟡 YELLOW / {n} 🔵 BLUE)
**Output Files Written:**
- `output/{domain}/{file}` ({n} lines)
**Next Phase:** {Phase N+1 description, or "Pipeline complete — all 6 artifacts ready"}
**Open Questions:** {bullet list, or "None"}
```

This footer makes the pipeline auditable across 37+ domains. Never skip it.

---

## 11. Trivial Field Resolver Grouping

In Phase 2, group trivial pass-through field resolvers at the end of the Field Resolvers section:

```markdown
### Trivial Pass-Through Resolvers

| Resolver | Returns |
|---------|---------|
| `{ParentType}.{field}` | `parent.{field}` |
| `{ParentType}.{field}` | `parent.{camelCaseVariant}` (field rename only) |
```

Do NOT give trivial pass-throughs individual pseudo-logic blocks.

---

## 12. Forbidden Phrases in Phase 2 Output

These phrases indicate incomplete analysis and must never appear:

| Forbidden | Replace With |
|---------|-------------|
| "various transformations" | Specific field mappings: "`partner_id` → `partnerId` via deepToCamelCase" |
| "standard error handling" | Specific behavior: "404 → return null; 500 → throw as GraphQL error" |
| "handles the typical cases" | Enumerate each case explicitly |
| "calls the appropriate service" | "Calls `ServiceClass.methodName` via GET `{base-url}/{endpoint}`" |
| "returns the expected fields" | List the specific fields or reference the schema |

---

## 13. Quick Scan Mode Output Marker

When Phase 2 runs in Quick Scan mode, add this banner to the output file:

```markdown
> ⚡ **Quick Scan Mode** — This analysis covers top-level queries and mutations only.
> Field resolvers, utils, and service methods are not fully documented.
> Run full mode before generating stories (Phase 4).
```
