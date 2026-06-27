# Template: Federation Entity Analysis (`03-schema-analysis.md`)

This template defines the format for Phase 3 schema analysis output.
Skills producing this artifact must follow this structure exactly.

---

## File Header Block

```markdown
# Phase 3: Federation Schema Analysis — {Domain Display Name}

> **Domain:** `{loader-key}`
> **Target DGS:** `{ServiceClassName}` (repo: `{repo-name}`)
> **Pipeline Version:** 1.1
> **Generated:** {YYYY-MM-DD}
> **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** {Green-field (no existing DGS schema) | Existing schema found at {path}}
```

---

## Type Classification Table (Mandatory)

One row per type. No missing rows.

```markdown
## Type Classification

| Type | Category | @key Directive | Owned By | Notes |
|------|---------|---------------|---------|-------|
| `{TypeName}` | Owned | `@key(fields: "id")` | This domain | Primary entity |
| `{TypeName}` | Owned | `@key(fields: "id humanId")` | This domain | Dual-key entity |
| `{TypeName}` | Owned | None | This domain | Response wrapper — not independently fetchable |
| `{TypeName}` | Extended | `@key(fields: "id")` | {other-domain} | This domain adds {fieldName} field |
| `{TypeName}` | External stub | None | {other-domain} | Referenced, not extended |
| `{TypeName}` | Gateway-only | None | {loader-key} gateway | Hive resolves via {strategy} |
| `{TypeName}` | Shared | `@shareable` | All domains | Utility type (Paging, CodeDescription, etc.) |
| `{InputTypeName}` | Input | None | This domain | Mutation input — never federated |
| `{EnumName}` | Enum | None | This domain | |

**Summary:** {n} Owned · {n} Extended · {n} External stubs · {n} Gateway-only · {n} Shared · {n} Input · {n} Enum
```

---

## External Type Stubs Table

One row per external or gateway-only type reference.

```markdown
## External Type Stubs

| Type | Owned By | Strategy | DGS Returns | Hive Resolves |
|------|---------|---------|------------|--------------|
| `{TypeName}` | {domain} DGS | Federation | `{ id: "..." }` stub | No — DGS entity fetcher |
| `{TypeName}` | VMM gateway | Gateway Stitch | `{ {keyField}: "..." }` stub | Yes — `{loaderKey}` |
| `{TypeName}` | IG gateway | Gateway Stitch | `{ id: "..." }` stub | Yes — `department` |

**Schema pattern for each stub:**
```graphql
# Gateway-stitched type
type {TypeName} @key(fields: "{keyField}") @extends {
  {keyField}: {KeyType}! @external
}

# Federation-referenced type (DGS-to-DGS)
type {TypeName} @key(fields: "id") @extends {
  id: ID! @external
}
```
```

---

## Client Contract Verification (Mandatory)

Every query and mutation must be verified. No missing rows.

```markdown
## Client Contract Verification

**Principle:** Every client-facing operation must be preserved with the same name, arguments, and return type structure.

| Operation | Type | Args Preserved? | Return Type Preserved? | Breaking Change? | Notes |
|-----------|------|----------------|----------------------|-----------------|-------|
| `{queryName}` | Query | ✅ Yes | ✅ Yes | No | |
| `{mutationName}` | Mutation | ✅ Yes | ✅ Yes | No | |
| `{deprecated}` | Query | ✅ Yes | ✅ Yes | No | Kept with @deprecated |

**Breaking changes:** {0 breaking changes | List any breaking changes}
```

---

## Query Gap Analysis (Mandatory)

```markdown
## Query Gap Analysis

**{n} ✅ | {n} 🔜 | {n} ⏭ — {total} total**

| Query | Status | Notes |
|-------|--------|-------|
| `{queryName}` | 🔜 Needs migration | Green-field |
| `{queryName}` | ✅ Exists in DGS | (only if DGS files were provided) |
| `{queryName}` | ⏭ Deferred | {reason: deprecated / admin-only / PO decision} |
```

---

## Mutation Gap Analysis (Mandatory)

```markdown
## Mutation Gap Analysis

**{n} ✅ | {n} 🔜 | {n} ⏭ — {total} total**

| Mutation | Status | Notes |
|---------|--------|-------|
| `{mutationName}` | 🔜 Needs migration | Green-field |
```

---

## Schema Analysis Summary Block (Mandatory)

```markdown
## Schema Analysis Summary

| Category | Count |
|---------|-------|
| Owned types (this domain) | {n} |
| Extended types (add fields to another domain) | {n} |
| External stubs (referenced, not owned) | {n} |
| Gateway-only stubs (Hive resolves) | {n} |
| Shared utility types | {n} |
| Input types | {n} |
| Enums | {n} |
| **Total types** | **{n}** |
| Queries requiring migration | {n} |
| Mutations requiring migration | {n} |
| Breaking changes | {0} |
| CAT-4 stories required | {n} |
```

---

## Risks and Recommendations

```markdown
## Risks and Recommendations

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| {risk description} | Low/Medium/High | Low/Medium/High | {mitigation} | Tech Lead/PO/Platform/Gateway Team |

### Recommendations
- {Recommendation 1 — e.g., "Define Product entity fetcher before BOM migration starts"}
- {Recommendation 2}
```

---

## Schema File Header (For `03-schema.graphql`)

Every schema file must begin with this comment block:

```graphql
# =============================================================================
# {Domain Name} Domain — Derived DGS Schema (Target State)
# Pipeline Version: 1.1
# Generated: {YYYY-MM-DD}
# DGS Target: Green-field (no existing schema) | Existing schema from {path}
# Source:    spark-internal-graphql/.../schemas/{file}.graphql
# Target:    {target-repo}/apps/app/src/main/resources/schema/{domain}.graphqls
#
# Status Legend:
#   ✅  Exists in DGS  |  🔜  Needs migration  |  ⏭  Deferred
# =============================================================================
```

---

## Schema File Body Order (For `03-schema.graphql`)

```graphql
# Federation header (if federation v2)
extend schema @link(url: "...", import: ["@key", "@external", "@shareable", "@extends"])

# Scalar declarations (if any)
scalar DateTime

# --- External stubs (Gateway-only) ---
# Types resolved by Hive Gateway — DGS returns only the key field
# 🔵 BLUE: Optional gateway stitch
type {GatewayType} @key(fields: "{keyField}") @extends {
  {keyField}: {KeyType}! @external
}

# --- Owned types ---
# 🔜 Needs migration
type {OwnedType} @key(fields: "id") {
  id: ID!
  # {field}: {Type}  # 🔜 description
}

# --- Embedded types ---
# No @key — not independently fetchable
type {EmbeddedType} {
  # fields
}

# --- Shared types ---
type Paging @shareable {
  # fields
}

# --- Inputs ---
input {InputType} {
  # fields
}

# --- Enums ---
enum {EnumType} {
  # values
}

# --- Queries ---
extend type Query {
  # 🔜 Needs migration
  # {queryName}: {description}
  {queryName}({args}): {ReturnType}
}

# --- Mutations ---
extend type Mutation {
  # 🔜 Needs migration
  # {mutationName}: {description}
  {mutationName}(input: {InputType}!): {ReturnType}
}
```

---

## Response Footer

```markdown
---
**Phase Completed:** Phase 3 — Federation Schema Derivation
**Domain:** `{loader-key}`
**DGS Target:** {Green-field | Existing schema found}
**Skills Applied:** federation-candidate-detection, federation-schema-derivation
**Types Classified:** {n} total ({n} Owned · {n} External stubs · {n} Gateway-only)
**Breaking Changes:** {0}
**CAT-4 Stories Required:** {n}
**Output Files Written:**
- `output/{domain}/03-schema.graphql` ({n} lines)
- `output/{domain}/03-schema-analysis.md` ({n} lines)
**Next Phase:** Phase 4 — Migration Story Generation
**Open Questions:** {list or "None"}
```
