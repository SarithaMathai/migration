# Template: Resolver Analysis (`be-02-resolver-analysis.md`)

This template defines the exact format for Phase 2 resolver analysis output.
Skills that produce this artifact must follow this structure exactly.

---

## File Header Block

```markdown
# Phase 2: Resolver Dependency Analysis — {Domain Display Name}

> **Domain:** `{loader-key}`
> **Target DGS:** `{ServiceClassName}` (repo: `{repo-name}`, url: `{base-url}`)
> **Pipeline Version:** 1.1
> **Generated:** {YYYY-MM-DD}
> **Depends on:** [be-01-schema-inventory.md](./be-01-schema-inventory.md)
> **DGS Target Status:** {Green-field (no existing DGS schema) | Existing schema found at {path}}
> **Analysis Mode:** {Full | Quick Scan}
```

---

## Summary Statistics (Mandatory)

```markdown
## Summary Statistics

| Metric | Count |
|--------|-------|
| Query resolvers | {n} |
| Mutation resolvers | {n} |
| Field resolvers (non-trivial) | {n} |
| Field resolvers (trivial pass-throughs) | {n} |
| Helper functions | {n} |
| Service classes | {n} |
| Service methods | {n} |
| Utils analyzed | {n} |
| EXT Service calls total | {n} |
| EXT 🔴 RED | {n} |
| EXT 🟡 YELLOW | {n} |
| EXT 🔵 BLUE | {n} |
| Very High complexity operations | {n} |
| High complexity operations | {n} |
| Medium complexity operations | {n} |
| Low complexity operations | {n} |
```

---

## Quick Scan Mode Banner (Add Only If Quick Scan)

```markdown
> ⚡ **Quick Scan Mode** — This analysis covers top-level queries and mutations only.
> Field resolvers, utils, and service methods are not fully documented.
> Run full mode before generating stories (Phase 4).
```

---

## Helper Functions (Omit Section If None)

Use H{n} prefix. Only include if the resolver file defines helpers shared by 2+ resolvers.

```markdown
## Helper Functions

### H1: `{helperFunctionName}({params})`

**Used by:** {list of resolver IDs that call this helper}
**Complexity contribution:** {what it adds to caller complexity}

**Logic:**
1. {step}
2. {step}
   - {sub-step if applicable}

**EXT Service calls:**
{None | EXT Service tags}

**Returns:** {description of return value}
```

---

## Query Resolver Block (Repeat for Each Query)

Use Q{n} prefix, sequential.

```markdown
## Query Resolvers ({n})

### Q{n}: `{queryName}`

**Schema signature:**
```graphql
{queryName}({argName}: {ArgType}!, {argName2}: {ArgType2}): {ReturnType}
```

**Resolver location:** `{relative/path/to/file.js}:{startLine}-{endLine}`
**Complexity:** {Low | Medium | High | Very High}

**Pseudo-logic:**
1. {First step — extract args, validate, setup context}
2. {Second step — primary service call or DataLoader}
   - {Sub-step: detail on conditional, transformation, or error path}
3. {Subsequent steps}
4. Return {return value description}

**Service calls:**
| Method | HTTP | Endpoint | Purpose |
|--------|------|---------|---------|
| `{ServiceClass.methodName}` | {GET/POST/PUT/DELETE} | `{base-url}/{path}` | {purpose} |

**EXT Service calls:**
{None — all calls are to this domain's own backend.}
OR
**EXT Service** → key: `{loaderKey}` · url: `{url}` · repo: `{repo}` · severity: 🔴/🟡/🔵
Purpose: {one-line description}

**Pagination:**
{None | Source defaults: page={n}, size={n}. DGS target: Spring Pageable with same defaults.}

**Error handling:**
- {404 from REST} → {return null | throw exception}
- {500 from REST} → {propagate as GraphQL error | log and return null}
- {Empty list} → {return [] | return null}

**Side effects:**
{None | Cache invalidation: {cache key} | Activity log: {event type} | ACL refresh: {condition}}

**User bifurcation:**
{None | Internal users: {code path A}. External users: {code path B}.}
```

---

## Mutation Resolver Block (Repeat for Each Mutation)

Use M{n} prefix, sequential.

```markdown
## Mutation Resolvers ({n})

### M{n}: `{mutationName}`

**Schema signature:**
```graphql
{mutationName}(input: {InputType}!): {ReturnType}
```

**Resolver location:** `{relative/path}:{startLine}-{endLine}`
**Complexity:** {Low | Medium | High | Very High}

**Input validation:**
- {Rule 1 — e.g., "productId must be non-null"}
- {Rule 2 — e.g., "partnerId must exist in the ACL context"}

**Pseudo-logic:**
1. {step}
2. {step}

**Orchestration steps (if multiple service calls):**
| Step | Service | Can Parallelize? |
|------|---------|----------------|
| 1 | {ServiceClass.method} | No — required before step 2 |
| 2 | {ServiceClass.method} | Yes — parallel with step 3 |

**Service calls:**
| Method | HTTP | Endpoint | Purpose |
|--------|------|---------|---------|

**EXT Service calls:**
{None | EXT Service tags with severity}

**Rollback / partial failure:**
{None | If step {n} fails: {rollback behavior}}

**Error handling:**
- {specific error} → {specific behavior}
```

---

## Field Resolver Block (Non-Trivial Only)

Use F{n} prefix, sequential.

```markdown
## Field Resolvers ({n})

### F{n}: `{ParentType}.{fieldName}`

**Resolver location:** `{path}:{startLine}-{endLine}`
**Trigger condition:** {When does this fire — e.g., "When the query includes the {fieldName} field"}
**Complexity:** {Low | Medium | High | Very High}

**Pseudo-logic:**
1. {step}

**Data source:** {Internal — same backend | EXT Service — {loaderKey}}
**EXT Service calls:** {None | EXT tags}
**Caching / batching:** {None | DataLoader: {dataLoaderName}, batch key: {key}, max batch size: {n}}

---

### Trivial Pass-Through Resolvers

The following field resolvers return a parent field directly with no transformation or service call:

| Resolver | Returns |
|---------|---------|
| `{ParentType}.{field}` | `parent.{field}` |
| `{ParentType}.{field}` | `parent.{camelCaseVariant}` (field rename only) |
```

---

## Service Class Block (Repeat for Each Service)

Use S{n} prefix.

```markdown
## Service Classes ({n})

### S{n}: `{ServiceClassName}`

**Base URL:** `{base-url-from-context.js}`
**File:** `{relative/path/to/Service.js}` ({n} lines)

#### Method: `{methodName}({params})`

**HTTP:** `{VERB} {URL-pattern}`
**Headers:** `Authorization: Bearer {token}` [+ `SPARK-Capability-Token: {token}` if applicable]
**Query params:** `{param}={source}` (e.g., `page={input.page}`, `size={input.size}`)
**Request body:** `{field}: {source}` (snake_case, e.g., `product_id: input.productId`)
**Response shape:** `{field}: {type}` (snake_case from REST)
**Transformations:** {e.g., "deepToCamelCase applied to response" or "productId field renamed from product_id"}
**Error handling:** {e.g., "404 returns null, other errors propagated"}
```

---

## Referenced Utils Block (Repeat for Each Util)

Use U{n} prefix.

```markdown
## Referenced Utils ({n})

### U{n}: `{utilFileName}.js` — `{functionName}({params})`

**Purpose:** {one-line description}
**Used by:** {list of resolver IDs}

**Logic:**
1. {step}

**DGS equivalent:** {e.g., "@DgsDataLoader + MappedBatchLoaderWithContext" | "Jackson ObjectMapper with deepToCamelCase" | etc.}
```

---

## EXT Service Call Inventory (Mandatory)

```markdown
## EXT Service Call Inventory

**{n} total — {n} 🔴 RED / {n} 🟡 YELLOW / {n} 🔵 BLUE**

| # | Called From | EXT Service | Loader Key | URL | Repo | HTTP | Endpoint | Severity | Purpose |
|---|-------------|-------------|------------|-----|------|------|----------|----------|---------|
| 1 | {Q3/M2/F5} | {ServiceName} | `{key}` | `{url}` | `{repo}` | {VERB} | `{/path}` | 🔴/🟡/🔵 | {purpose} |
```

---

## Complexity Assessment (Mandatory)

```markdown
## Complexity Assessment

| Operation | Type | Lines | Service Calls | EXT Calls | Orchestration Steps | Complexity |
|-----------|------|-------|---------------|-----------|---------------------|------------|
| {name} | Query | {n} | {n} | {n} | {n} | {Low/Medium/High/VH} |
```

**Complexity bump rules applied:**
- `__resolveType` polymorphism present: +1 tier to {list operations affected}
- Internal/external user bifurcation: +1 tier to {list operations affected}
- Parallel orchestration 5+ services: +1 tier to {list operations affected}

---

## Key Findings (Mandatory)

```markdown
## Key Findings

### Highest Risk Operations
1. **{operation}** ({Complexity}) — {one-line risk description}
2. **{operation}** ({Complexity}) — {one-line risk description}
3. **{operation}** ({Complexity}) — {one-line risk description}

### Migration Blockers
- {Operation} cannot migrate until {service} is migrated to DGS.
  Workaround: Gateway stitch with CAT-4 story.
- {Or: "None identified."}

### Refactor Recommendations
- {Pattern found} in {file}:{lines} — recommend {specific improvement}
- {Or: "None identified."}

### Quick Wins
1. **{operation}** (Low complexity) — {why it's a quick win}
2. **{operation}** (Low complexity) — {why it's a quick win}
```

---

## Response Footer (Mandatory at End of Chat Response)

```markdown
---
**Phase Completed:** Phase 2 — Resolver Dependency Analysis
**Domain:** `{loader-key}`
**Analysis Mode:** {Full | Quick Scan}
**DGS Target:** {Green-field | Existing schema found}
**Skills Applied:** resolver-dependency-analysis
**Files Analyzed:** {n} files, {n} lines
**Target Service:** `{ServiceClassName}` ({repo})
**EXT Service Calls Found:** {n} total ({n} 🔴 RED / {n} 🟡 YELLOW / {n} 🔵 BLUE)
**Output Files Written:**
- `output/{domain}/be-02-resolver-analysis.md` ({n} lines)
**Next Phase:** Phase 3 — Federation Schema Derivation
**Open Questions:** {bullet list or "None"}
```
