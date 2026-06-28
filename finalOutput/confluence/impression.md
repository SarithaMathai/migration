# Impression — Migration to the `plm-product` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../impression/03-schema-analysis.md) ·
> [field inventory](../impression/05-attribute-inventory.md) · [engineering stories](../impression/04-stories.md).
> Create tickets from [`../jira/impression.csv`](../jira/impression.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Impression** domain (the product's printed / embellished artwork "impressions" and their
per-partner counts) off the `spark-internal-graphql` gateway into the **`plm-product`** DGS. It is the
**smallest and lowest-risk** of the thirteen domains: 2 queries, 1 mutation, and 6 field resolvers across a
66-line resolver — no polymorphism, no orchestration. We recommend migrating it **first** as a team warm-up
that proves the pipeline end-to-end.

The only mild wrinkle is the counts query: today it returns the impressions **list** and a field resolver
aggregates per-partner counts (re-fetching the product). A cleaner typed result is a possible fast-follow,
but the existing contract can be preserved exactly.

**ACL note:** the current code obtains a per-product capability token via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one reuses the other's REST call |
| Mutations | 1 | delete + update sets in one PUT |
| Field-resolver type blocks | 2 | `Impression` (5), `ImpressionCount` (1) |
| External dependencies | 4 keys (0 🔴 · 1 🟡 · 3 🔵) | workspace, VMM, user-profile |
| Federation contributions | 1 (Product extension) | BLOCKED-BY product |
| **Total stories** | **11** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 5–8d |
| B | Core Reads | 2 | 2–4d |
| D | Mutations | 1 | 2–3d |
| F | Federation (Product) | 1 | 1–2d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 3 | 4–7d |
| **Total** | | **11** | **14–24d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| Awkward counts contract | 🟢 Low | Optional cleanup to a typed result; safe to defer |
| `enableWorkspaceContextFiltering` not forwarded today | 🟢 Low | Confirm whether it should filter |
| Federation contribution waits on product | 🟢 Low | Not on the critical path |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Preserve `ImpressionCount` contract or adopt `ImpressionCountResult`? | B02/G02 | Architect |
| 2 | Should `enableWorkspaceContextFiltering` filter at the backend? | B01 | Backend Eng |

## Migration approach (summary)

Phase **A** schema + `ImpressionService` port (one GET, one PUT — no interfaces); **B** the 2 reads;
**D** `updateImpressions`; **G** the `Impression` field resolvers + the counts aggregation; **F** the Product
extension (post-launch, internal). Full detail:
[03-schema-analysis.md §Migration Approach](../impression/03-schema-analysis.md).

## Sequencing & capacity

One engineer ≈ 3–5 sprints; 2 engineers ≈ 2–3. Recommended **first** domain. Full plan:
[04-po-summary.md](../impression/04-po-summary.md).

---
*PO page assembled from the impression analysis. Tickets:
[`../jira/impression.csv`](../jira/impression.csv) · [`../jira/impression-stories.md`](../jira/impression-stories.md).*
