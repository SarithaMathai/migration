# Template: Schema Inventory (`be-01-schema-inventory.md`)

This template defines the format for Phase 1 schema inventory output.

---

## File Header Block

```markdown
# Phase 1: Schema Inventory — {Domain Display Name}

> **Domain:** `{loader-key}`
> **Target DGS:** `{ServiceClassName}` (repo: `{repo-name}`, url: `{base-url}`)
> **Pipeline Version:** 1.1
> **Generated:** {YYYY-MM-DD}
> **Depends on:** None (entry phase)
> **DGS Target Status:** {Green-field (no existing DGS schema) | Existing schema found at {path}}
```

---

## Context Registration

The verbatim `context.js` entry for this domain.

```markdown
## Context Registration

```js
// spark-internal-graphql/packages/data-source-spark/src/context.js
"{loader-key}": {
  "service": "{ServiceClassName}",
  "url": "{base-url}",
  "repo": "{repo-name}"
}
```

**Auth pattern:** {e.g., "Authorization: Bearer {token}" | "SPARK-Capability-Token: {token}" | "Both headers"}
```

---

## Co-Located Domain Siblings

Other domains sharing the same backend URL.

```markdown
## Co-Located Domain Siblings

The following domains share the same backend (`{base-url}`):

| Loader Key | Service Class | Schema File | Target DGS |
|-----------|--------------|------------|-----------|
| `{loader-key}` | `{ServiceClassName}` | `SPARK_{Domain}.graphql` | {DGS service} |
| `{this-domain}` | — | — | ← **This domain** |

**Note:** All co-located domains will share the `{target-repo}` DGS service.
{Or: "This domain has no co-located siblings."}
```

---

## Source File Manifest

### Schema Files

```markdown
## Source File Manifest

### Schema Files

| File | Path | Lines | Types | Inputs | Enums | Queries | Mutations |
|------|------|-------|-------|--------|-------|---------|-----------|
| `SPARK_{Domain}.graphql` | `spark-internal-graphql/.../schemas/SPARK_{Domain}.graphql` | {n} | {n} | {n} | {n} | {n} | {n} |
```

### Resolver Files

```markdown
### Resolver Files

| File | Path | Lines | Query Resolvers | Mutation Resolvers | Field Resolvers |
|------|------|-------|----------------|-------------------|----------------|
| `SPARK_{Domain}.js` | `spark-internal-graphql/.../resolvers/{path}/SPARK_{Domain}.js` | {n} | {n} | {n} | {n} |

{⚠️ Large file: {n} lines — Phase 2 will use chunked reading (500-line windows). If applicable.}
```

### Service Files

```markdown
### Service Files

| File | Path | Lines | Methods | Base URL |
|------|------|-------|---------|---------|
| `{Domain}.js` | `spark-internal-graphql/.../services/{Domain}.js` | {n} | {n} | `{base-url}` |
```

### Utils Files

```markdown
### Utils Files

| File | Path | Lines | Type | DGS Equivalent |
|------|------|-------|------|---------------|
| `loadOne.js` | `spark-internal-graphql/.../utils/loadOne.js` | {n} | Core util | `@DgsDataLoader` + `MappedBatchLoaderWithContext` |
| `{Domain}Utils.js` | `spark-internal-graphql/.../utils/{Domain}Utils.js` | {n} | Domain-specific | {custom analysis required} |
```

### Config Files

```markdown
### Config Files

| File | Path | Purpose |
|------|------|---------|
| `{config}.js` | `spark-internal-graphql/.../config/{config}.js` | {purpose — e.g., "Business partner constants", "Feature flags"} |
{Or: "None — no config files referenced by this domain."}
```

---

## Import Graph

```markdown
## Import Graph

```
SPARK_{Domain}.js (resolver)
├── imports: {ServiceClassName} from services/{Domain}
├── imports: loadOne from utils/loadOne
├── imports: loadListing from utils/loadListing
├── imports: commonLoaders from utils/commonLoaders
└── imports: {domainUtils} from utils/{Domain}Utils
    └── uses: {specificFunction}

{Domain}.js (service)
├── imports: axios (HTTP client)
└── imports: convertFunctions from utils/convertFunctions
```
```

---

## Target DGS Section

```markdown
## Target DGS: Green-Field

**Status:** No existing DGS schema found — green-field derivation.
**Target service:** `{ServiceClassName}` (repo: `{repo-name}`)
**Phase 3 approach:** All types and operations will be derived fresh and marked 🔜.

If you have DGS files to compare against, provide them when running Phase 3.
```

---

## Cross-Domain Reference Table

```markdown
## Cross-Domain Reference Table

| Field | Referenced Type | Domain | Loader Key | URL | Strategy | Severity |
|-------|----------------|--------|------------|-----|----------|----------|
| `{ParentType}.{field}` | `{RefType}` | {domain} | `{key}` | `{url}` | Internal | N/A |
| `{ParentType}.{field}` | `{RefType}` | {domain} | `{key}` | `{url}` | EXT Service | 🔴 RED |
| `{ParentType}.{field}` | `{RefType}` | {domain} | `{key}` | `{url}` | Gateway Stitch | 🔵 BLUE |

**Strategy definitions:**
- **Internal** — same backend (same `{base-url}`), no cross-service boundary needed
- **EXT Service** — different backend, requires federation or stitching design
- **Gateway Stitch** — external platform (VMM, IG, Doppler, etc.) — always Hive Gateway, never DGS
```

---

## Summary Statistics

```markdown
## Summary Statistics

| Metric | Count |
|--------|-------|
| Schema files | {n} |
| Total schema lines | {n} |
| Types defined | {n} |
| Input types | {n} |
| Enum types | {n} |
| Queries | {n} |
| Mutations | {n} |
| Resolver files | {n} |
| Total resolver lines | {n} |
| Service files | {n} |
| Total service lines | {n} |
| Service methods | {n} |
| Utils files | {n} |
| Co-located domain siblings | {n} |
| Cross-domain references (Internal) | {n} |
| Cross-domain references (EXT Service) | {n} |
| Cross-domain references (Gateway Stitch) | {n} |
| EXT Service calls (estimated) | {n} |
| Large files (>1000 lines) | {n} ⚠️ |
```

---

## Response Footer

```markdown
---
**Phase Completed:** Phase 1 — Schema Inventory
**Domain:** `{loader-key}`
**DGS Target:** Green-field
**Skills Applied:** graphql-schema-inventory
**Files Analyzed:** {n} files, {n} lines
**Target Service:** `{ServiceClassName}` ({repo})
**EXT Service Calls (estimated):** {n}
**Output Files Written:**
- `output/{domain}/be-01-schema-inventory.md` ({n} lines)
**Next Phase:** Phase 2 — Resolver Dependency Analysis
**Open Questions:** {list or "None"}
**Large File Warning:** {None | ⚠️ {file} is {n} lines — Phase 2 will use 500-line chunks}
```
