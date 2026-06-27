# BOM — Migration to the `plm-product` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../bom/03-schema-analysis.md) ·
> [field inventory](../bom/05-attribute-inventory.md) · [engineering stories](../bom/04-stories.md).
> Create tickets from [`../jira/bom.csv`](../jira/bom.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **BOM** (bill-of-materials) domain off the `spark-internal-graphql` gateway into the
**`plm-product`** DGS. BOM describes the materials that make up a product and is referenced by many sibling
domains. It is **mid-sized**: 13 queries, 6 mutations, ~46 field resolvers across 18 type blocks on a
735-line resolver. Its defining challenge is **material polymorphism** — 7 concrete material types (Trim,
Wash, Fabric, FabricSpec, Combination, Packaging, plus the base) resolved by a category dispatcher, and 5
impression sub-types. The single hardest piece of work is **`updateBom`**, a 3-step write (workspace → body
→ permissions) that today has no rollback.

The schema is **wide but shallow**: most attributes are direct pass-throughs (cheap). Risk concentrates in
~38 cross-domain field resolvers (material-library and color lookups) and the 2 polymorphic interfaces.

**ACL note:** the current gateway uses ACL to obtain a per-resource capability token. **ACL is ignored in
the DGS implementation** — no ACL story; we only note where/why it's used today.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 13 | 4 are cacheable master-data lookups |
| Mutations | 6 | 5 simple + `updateBom` (complex) |
| Field-resolver type blocks | 18 | one story each (G01–G15) |
| Material polymorphism | 7 types + interface + type resolver | A04 |
| External dependencies | 12 keys (2 🔴 · 6 🟡 · 4 🔵) | material-hub/trim/wash/fabric/combination 🟡; search 🔴 |
| **Total stories** | **42** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 5 | 10–16d |
| B | Core Reads | 8 | 8–14d |
| C | Search & Listing | 5 | 9–15d |
| D | Mutations (simple) | 5 | 5–10d |
| E | Complex (`updateBom`) | 1 | 6–10d |
| F | Federation Contributions | 2 | 4–7d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 16 | 34–55d |
| **Total** | | **42** | **76–127d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateBom` 3-step write can leave data half-updated | 🔴 High | Needs an architecture decision (E01) on recovering from a mid-write failure |
| Material field resolvers depend on 5 sibling domains | 🟡 Medium | BOM can ship reads/writes; full material enrichment needs hub/trim/wash/fabric/combination federated |
| 7-variant polymorphism is easy to break when fields change | 🟡 Medium | A CI conformance check (G16) guards this |
| Trim size logic is intricate (15 cases × 2) | 🟡 Medium | One larger story (G08) with a parity table |
| Federation contributions wait on product | 🟢 Low | F01/F02 post-launch; not on the critical path |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateBom` failure strategy: saga / compensation log / best-effort | E01 | Tech Lead + PO |
| 2 | `updateBomComponentStatus` has no auth token — is the backend enforcing it? | D05 | PO |
| 3 | Keep `Bom_Unified` as a type or replace with field selection on `Bom`? | A02/G01 | Architect |
| 4 | Are the 3 unused service methods called by other domains? Confirm before delete | A05 | Tech Lead |
| 5 | Federation rollout order for hub/trim/wash/fabric/combination | A03/G | Architect + Platform |

## Migration approach (summary)

Phase **A** lays the schema (incl. the 2 `@DgsTypeResolver` interfaces) + `BomService` port; **B/C** reads
and search; **D** simple mutations; **E** the `updateBom` 3-step write; **F** the (internal) contributions
to Product; **G** the material field resolvers (G08 trim and G10 impression branches are the largest) +
tests. Full detail: [03-schema-analysis.md §Migration Approach](../bom/03-schema-analysis.md).

## Sequencing & capacity

Phases B/C/D/G parallelize heavily after A. One engineer ≈ 15–25 sprints; 3 engineers ≈ 6–10 (critical path
A → E01 → G08/G10 → G16). Phase G (field resolvers) dominates the calendar. Full plan:
[04-po-summary.md](../bom/04-po-summary.md).

---
*PO page assembled from the BOM analysis. Tickets: [`../jira/bom.csv`](../jira/bom.csv) ·
[`../jira/bom-stories.md`](../jira/bom-stories.md).*
