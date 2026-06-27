# Evidence Collection — What to Capture and Where

**Purpose:** Guide engineers on what investigation artifacts to produce, where to store them, and what makes a finding useful for downstream teams.
**Audience:** Engineers who have completed a domain investigation and need to document findings.

---

## The Six Required Artifacts

Every domain investigation must produce all six artifacts before handing off to engineering or PO. Partial handoffs create downstream confusion.

| Artifact | File Name | Produced By | Must Have Before |
|---------|----------|------------|-----------------|
| Schema inventory | `01-schema-inventory.md` | Phase 1 | — |
| Resolver analysis | `02-resolver-analysis.md` | Phase 2 | Phase 1 |
| DGS schema | `03-schema.graphql` | Phase 3 | Phase 2 |
| Schema gap analysis | `03-schema-analysis.md` | Phase 3 | Phase 2 |
| Engineering stories | `04-stories.md` | Phase 4 | Phases 1+2+3 |
| PO sprint plan | `04-po-summary.md` | Phase 4 | Phases 1+2+3 |

---

## Where to Store Output

All output goes under `output/{domain}/` using the loader key as the directory name.

**Naming convention:** Use the catalog loader key (kebab-case):

| Domain | Loader Key | Output Folder |
|--------|-----------|--------------|
| Product | `product` | `output/product/` |
| BOM | `bom` | `output/bom/` |
| ProductPlan | `productPlan` | `output/productPlan/` |
| Access Control | `accessControl` | `output/accessControl/` |

**Do not use** display names as folder names. Always use the catalog loader key.

---

## What Makes a Finding Useful

### In `02-resolver-analysis.md` (Pseudo-Logic)

Each resolver block is evidence. For it to be useful to an engineer implementing the DGS service, it must include:

**Must have:**
- Numbered steps (not prose)
- REST endpoint details: HTTP verb + URL pattern + headers
- Every EXT service call tagged with severity
- Specific error handling per error path (not "handles errors")
- Specific transformation rules (not "transforms the response")

**Must not have:**
- Vague language: "various transformations", "standard error handling", "handles the typical cases"
- Missing REST endpoint details
- EXT calls without severity tags

**Test:** Can a backend engineer implement the DGS data fetcher from this pseudo-logic alone, without looking at the JavaScript source? If yes, the evidence is sufficient.

---

### In `03-schema-analysis.md` (Gap Analysis)

The gap analysis is evidence of what needs to be built. For it to drive CAT-4 stories, it must include:

**Must have:**
- Type Classification table with all types classified (no missing rows)
- External Type Stubs table with the stub pattern for each
- Client Contract Verification (is every query/mutation preserved?)
- Gap analysis summary line: `{n} ✅ | {n} 🔜 | {n} ⏭ — {total} total`

**Must not have:**
- Types classified as "unknown" or "TBD"
- Missing cross-domain references

---

### In `04-stories.md` (Engineering Stories)

Each story is evidence of what to build. For it to be Jira-ready, it must include:

**Must have:**
- Current Behavior section with Phase 2 pseudo-logic verbatim or lightly edited
- Target DGS Implementation with specific annotations (`@DgsQuery`, Feign client, Kotlin class)
- Files to Create/Modify with actual file paths
- Acceptance Criteria that are objectively verifiable (no vague language)
- Test Cases with specific test method names

**Must not have:**
- Vague acceptance criteria: "errors are handled properly", "data is returned correctly"
- Missing dependency chain
- Missing EXT service severity tags

---

## EXT Service Evidence (Critical)

EXT service calls are the highest-risk migration findings. Every EXT call must be recorded in:

1. The resolver's pseudo-logic block (inline)
2. The EXT Service Call Inventory master table
3. The Cross-Domain Reference Analysis (Phase 1)
4. The CAT-4 story (Phase 4)

**Evidence format (mandatory in all of the above):**
```
EXT Service → key: `{loaderKey}` · url: `{url}` · repo: `{repo}` · severity: 🔴/🟡/🔵
Purpose: {one-line description of why this call is made}
```

**Never omit severity.** An EXT call without severity is incomplete evidence.

---

## Audit Checklist

Before handing off domain findings, run this audit:

### Phase 1 (`01-schema-inventory.md`)
- [ ] Every source file is listed with path and line count
- [ ] `context.js` entry is a verbatim JS code block (not paraphrased)
- [ ] Co-located domains are listed
- [ ] Cross-domain reference table is present and classified (Internal / EXT / Gateway Stitch)
- [ ] Summary statistics block is filled in
- [ ] Large file warnings (⚠️) are noted if applicable

### Phase 2 (`02-resolver-analysis.md`)
- [ ] Every query resolver has a pseudo-logic block
- [ ] Every mutation resolver has a pseudo-logic block with input validation
- [ ] Non-trivial field resolvers are documented; trivial pass-throughs are grouped in a table
- [ ] Every EXT service call is tagged with severity
- [ ] Master EXT inventory table covers every EXT call
- [ ] Complexity Assessment table is complete
- [ ] Key Findings section covers: highest risk, migration blockers, refactor recommendations, quick wins
- [ ] No vague language in any pseudo-logic block

### Phase 3 (`03-schema.graphql` + `03-schema-analysis.md`)
- [ ] Schema file has mandatory comment header
- [ ] Schema body follows correct section ordering
- [ ] Every type is classified in the analysis document
- [ ] External stubs table is present with stub patterns
- [ ] Client Contract Verification covers every operation
- [ ] Gap analysis summary line is present
- [ ] DGS target status is explicitly stated

### Phase 4 (`04-stories.md` + `04-po-summary.md`)
- [ ] Every operation has at least one story
- [ ] Every story uses the mandatory template from `templates/story-format.md`
- [ ] Every story has objectively verifiable acceptance criteria
- [ ] Every story embeds Phase 2 pseudo-logic in Current Behavior
- [ ] Dependency graph (Mermaid) is present
- [ ] Risk Register has at least one entry per High/Very-High story
- [ ] All stories appear in the PO summary table
- [ ] PO summary has a Decisions Required table
- [ ] Effort totals include +20% buffer

---

## Reusing Findings Across Domains

Some findings apply beyond a single domain:

### Shared Utility Analysis
If you analyze a util like `commonLoaders.js` for the BOM domain, that analysis is reusable for other domains that import the same util. Note it in the Key Findings section:
> "Analysis of `commonLoaders.js` in this investigation is shared with: product, measurement, impression domains."

### EXT Service Patterns
If the attachment domain's EXT call to the relationship service is documented, other domains calling the same service can reference that finding without re-analyzing.

### Federation Boundary Decisions
If `federation-readiness` determined that `Product.bom` should be federated (not stitched), that decision applies to all domains that reference the BOM type.

Record these cross-domain findings in a `SHARED_FINDINGS.md` at the root of `output/`:

```markdown
# Shared Investigation Findings

## Shared Utils Analysis
- commonLoaders.js: Analyzed for BOM domain (output/bom/02-resolver-analysis.md §U3)
  Applies to: product, measurement, impression, packaging

## Cross-Domain EXT Patterns
- Attachment service calls: Documented in output/product/ and output/bom/
  Standard pattern established — all future domains calling `attachment` loader key can reference output/product/02-resolver-analysis.md §EXT1

## Federation Decisions
- Product type @key(fields: "id"): Decided in output/product/ federation analysis
  All other domains referencing Product type must use External stub pattern
```

---

## When Evidence Is Insufficient

If an investigation produces incomplete findings, do not hand it off. Common gaps and how to address them:

| Gap | Fix |
|-----|-----|
| EXT calls without severity | Re-read the resolver and classify each call using `reference/output-conventions.md` §5 |
| Vague pseudo-logic ("calls the service") | Re-read the service file and add HTTP verb, URL, headers |
| Missing field resolvers | Check if resolver file has field resolvers that were skipped as "trivial" — verify they are truly pass-throughs |
| Phase 4 stories without Phase 2 pseudo-logic | Re-run Phase 4 after verifying Phase 2 is in full mode |
| Type Classification missing entries | Re-run `federation-candidate-detection` skill |
