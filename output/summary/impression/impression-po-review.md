# Impression — Migration to the `plm-product` DGS (PO view)

> 🏷️ **Tags:** `dgs-migration` · `po-page` · `domain-impression` · `pipeline-v2`  —  **Confluence location:** *Federation Graph Migration ▸ Domains ▸ impression*

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.  
> Deep dives: migration approach & schema · field inventory · engineering stories.  
> Create tickets from `../finalOutput/jira/impression.csv`. Effort is **AI-estimated — confirm in refinement.**

---

## What are we building?

- We are moving the **Impression** domain (the product's printed/embellished artwork "impressions" and their per-partner counts) off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is the
**smallest and lowest-risk** of the thirteen domains: 2 queries, 1 mutation, and 6 field resolvers across a
66-line resolver — no polymorphism, no orchestration. We recommend migrating it **first** as a team warm-up
that proves the pipeline end-to-end.

- The only mild wrinkle is the counts query: today it returns the impressions **list** and a field resolver aggregates per-partner counts (re-fetching the product).
- We recommend a cleaner typed result as a fast-follow, but the existing contract can be preserved exactly.

**ACL note:** the current code obtains a per-product capability token via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites use **Mid-Request ACL Update** before the downstream call. Impression has zero downstream-token sites.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one reuses the other's REST call |
| Mutations | 1 | delete + update sets in one PUT |
| Field-resolver type blocks | 2 | `Impression` (5), `ImpressionCount` (1) |
| External dependencies | 4 keys (0 🔴 · 1 🟡 · 3 🔵) | workspace, VMM, user-profile |
| Federation contributions | 1 (Product extension) | BLOCKED-BY product |
| **Total stories** | **7** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads (incl. DGS module init + ImpressionService wiring) | 2 | 4–6d |
| D | Mutations | 1 | 2–3d |
| F | Federation (Product) | 1 | 1–2d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 3 | 4–7d |
| **Total** | | **7** | **11–18d** (buffered) |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Preserve `ImpressionCount` contract or adopt `ImpressionCountResult`? | B-02/G-02 | Product Owner |
| 2 | Should `enableWorkspaceContextFiltering` filter at the backend? | B-01 | Backend Eng |

## Migration approach (summary)

**B** Core Reads (incl. DGS module init + ImpressionService wiring); **D** Mutations; **F** Federation (Product); **G** Field Resolvers & Tests. Full detail: `be-03-schema-analysis.md §Migration Approach`.

## Sequencing & capacity

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~3–5 sprints | sequential |
| 2 engineers | ~2–3 sprints | reads + field resolvers parallel |

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 + B-02 | **B-01:** DGS module init (schema/types/stubs/scalars) + ImpressionService wiring + `searchImpressionsByProductId`; **B-02:** counts query |
| 2 | D-01 + G-01 + G-02 | mutation + field resolvers + counts aggregation |
| 3 | G-04 | `attachment` entity reference (recommended, PO-gated). Test coverage/parity tracked outside this Jira pipeline, created manually. |
| post-launch | F-01 | Product extension (unblocked by product) |

---
*PO review assembled from the `impression` analysis. Jira tickets: `finalOutput/jira/impression.csv`. Full engineering detail: `impression-comprehensive.md` (same folder).*