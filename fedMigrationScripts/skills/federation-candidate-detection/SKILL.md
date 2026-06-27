---
name: federation-candidate-detection
description: "Identifies federation entity candidates in a domain — which types should be @key federated, which are external stubs, which are gateway-only, and which cross-domain fields need CAT-4 stitching stories. Can be invoked standalone for architecture Q&A or as part of the federation-schema-derivation skill. Produces a Cross-Domain Reference Analysis table and entity candidate list."
argument-hint: "Provide the domain. Example: 'Detect federation candidates for the bom domain' or 'What types in product should have @key directives?'"
---

# Skill: Federation Candidate Detection

## Purpose

Analyze a domain's types and cross-domain field references to determine:
- Which types are **owned** by this domain and should have `@key` federation directives
- Which types are **extended** (another domain's entity this domain adds fields to)
- Which types are **external stubs** (referenced but not extended)
- Which types are **gateway-only** (external platforms that never migrate to DGS)
- Which cross-domain fields need CAT-4 federation or stitching stories

This skill answers the architecture question: **"Where are the federation boundaries in this domain?"**

## When to Use

- Standalone: When an architect needs entity boundary decisions without a full pipeline run
- As part of `federation-schema-derivation`: Feeds type classification into schema file
- As part of `federation-readiness` agent: Provides candidate list before stitching analysis

## Cannot Run Without

- `output/{domain}/01-schema-inventory.md` (for the type list and cross-domain ref table)
- `output/{domain}/02-resolver-analysis.md` (for EXT call details — preferred but not blocking)

If Phase 2 is not complete, this skill can derive candidates from Phase 1 alone, with reduced accuracy on EXT severity.

## Reference Files to Read First

| For… | Read |
|------|------|
| External platform services (always gateway, never DGS) | `reference/stitching-patterns.md` §1 |
| Federation patterns (@key, @extends, @external, @requires) | `reference/federation-patterns.md` |
| Type classification categories and decision tree | `reference/federation-patterns.md` §2 |

---

## Federation Strategy Decision Tree

For each cross-domain reference, apply this decision tree:

```
Is the referenced service an external platform?
(VMM, IG/Item Groups, Doppler, LDAP, APEX, Corona, Nexus,
 Assortment, Negotiator, Brand Compliance)
│
├── YES → GATEWAY STITCH
│         DGS returns stub key only.
│         Hive Gateway resolves the full type.
│         No DGS entity fetcher needed.
│         Severity: 🔵 BLUE (unless business-critical)
│
└── NO → Is it a co-located domain (same backend URL)?
          │
          ├── YES → DIRECT RESOLUTION
          │         Same Feign client, same REST API.
          │         No federation boundary.
          │
          └── NO → Is the referenced service already migrated to DGS?
                    │
                    ├── YES → FEDERATION (@key + entity fetcher)
                    │         This DGS returns only the key field(s).
                    │         The owning DGS resolves the rest.
                    │
                    └── NO → EXT SERVICE (pending migration)
                              Treat as Gateway stitch for now.
                              Create a CAT-4 story to revisit when
                              the owning service migrates.
```

---

## Type Classification Categories

For each type in the source schema, assign exactly one category:

| Category | When to Use | Schema Pattern |
|----------|-------------|---------------|
| **Owned** | Data originates from this domain's backend | `type X @key(fields: "id") { ... }` |
| **Extended** | Type owned by another DGS; this domain adds fields | `extend type X @key(fields: "id") { newField: Type }` |
| **External stub** | Type owned by another DGS; referenced but not extended | `type X @key(fields: "id") @extends { id: ID! @external }` |
| **Gateway-only** | Resolved entirely by Hive Gateway (VMM, IG, Doppler, etc.) | Same as External stub — Hive handles resolution |
| **Shared** | Utility types (Paging, CodeDescription, etc.) | `type X @shareable { ... }` |
| **Input** | Mutation input types | `input X { ... }` |
| **Enum** | Enumeration types | `enum X { ... }` |

---

## Federation Key Rules

For every Owned type, determine the right `@key` directive:

| Type Role | Key Directive | When |
|-----------|--------------|------|
| Primary entity | `@key(fields: "id")` | Default — covers 90% of cases |
| Dual-key entity | `@key(fields: "id humanId")` | When BOTH are used as independent lookup keys |
| Response wrapper / embedded | No `@key` | Not independently fetchable |
| Composite context | `@key(fields: "productId partnerId")` | When identity is a tuple (e.g., ResourcesCount pattern) |
| Input type | No `@key` | Inputs are never federated |
| Shared utility | `@shareable`, no `@key` | Paging, CodeDescription, etc. |

---

## Step-by-Step Procedure

### Step 1: Load Type List from Phase 1

From `output/{domain}/01-schema-inventory.md`, collect every type defined in the source schema.

### Step 2: Load EXT Service References

From either:
- `output/{domain}/01-schema-inventory.md` Cross-Domain Reference table (if Phase 2 not done)
- `output/{domain}/02-resolver-analysis.md` EXT Service Call Inventory (preferred — more accurate severity)

### Step 3: Classify Each Type

Apply the type classification table above to every type. Note:
- Gateway-only services from `reference/stitching-patterns.md` §1 are always External stub / Gateway-only
- Types with `__resolveType` in resolvers (polymorphic interfaces/unions) need special handling

### Step 4: Determine Federation Keys

For each Owned type, apply the key rules above. Record the `@key` directive for each.

### Step 5: Handle Cross-Domain References

For each field referencing another domain's type, apply the federation strategy decision tree. Record:
- Strategy (Gateway Stitch / Direct Resolution / Federation / EXT Service pending)
- Severity for EXT calls (🔴 / 🟡 / 🔵)
- Whether a CAT-4 story is needed

### Step 6: Produce Cross-Domain Reference Analysis Table

```markdown
## Cross-Domain Reference Analysis — {Domain}

| Field | Referenced Type | Domain | Loader Key | Strategy | Severity | CAT-4 Story? |
|-------|----------------|--------|------------|----------|----------|-------------|
| {ParentType}.{field} | {Type} | {domain} | {key} | {strategy} | 🔴/🟡/🔵 | Yes/No |
```

### Step 7: Produce Entity Candidate Summary

```markdown
## Federation Entity Candidates

| Type | Classification | @key Directive | Notes |
|------|---------------|---------------|-------|
| {Type} | Owned | @key(fields: "id") | Primary entity |
| {Type} | External stub | — | Owned by {domain} |
| {Type} | Gateway-only | — | Hive resolves via {loader-key} |
```

---

## Output

When invoked **standalone** (no Phase 3 running):
- Produces Cross-Domain Reference Analysis table and Entity Candidate Summary in chat
- No file written (unless engineer requests one)

When invoked **as part of** `federation-schema-derivation`:
- Feeds type classification and @key decisions into `03-schema.graphql`
- Feeds cross-domain decisions into `03-schema-analysis.md` Type Classification table

When invoked **as part of** `federation-readiness` agent:
- Combined with stitching-pattern-analysis output
- Produces a focused federation design report

---

## Completion Criteria

- [ ] Every type in the source schema is assigned exactly one classification category
- [ ] Federation `@key` directives are determined for all Owned types
- [ ] All cross-domain references resolved via the decision tree
- [ ] CAT-4 story requirement noted for each EXT Service boundary
- [ ] Cross-Domain Reference Analysis table is complete
- [ ] Entity Candidate Summary is complete
- [ ] Gateway-only services are correctly identified and never marked for DGS migration
