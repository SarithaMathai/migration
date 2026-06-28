# Workspace — Migration to a dedicated `plm-workspace` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../workspace/03-schema-analysis.md) ·
> [field inventory](../workspace/05-attribute-inventory.md) · [engineering stories](../workspace/04-stories.md).
> Create tickets from [`../jira/workspace.csv`](../jira/workspace.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Workspace** domain — the seasonal/working containers that group products, samples, teams,
partners, attachments and discussions — off the `spark-internal-graphql` gateway into its **own
`plm-workspace` DGS subgraph**. Workspace is a **hub**: nearly every product-family domain references a
`WorkspaceV2`, and workspace itself reaches into product, search, discussion, sample, combination, attachment,
relationship and access-control.

It is **large and high-risk**: 8 queries, 10 mutations (+2 schema-drift wrappers), ~25 field resolvers on a
1,060-line resolver. Cost and risk concentrate in three places: the **`workspaceBusinessPartnerActionsV2`**
drop/undrop dispatcher (5 cases, manual compensation, and **un-awaited promise chains** to fix), and the two
heavy field resolvers **`attachmentsWithMetaData`** and **`counts`** (the workspace product dashboard).

**ACL note:** ACL authorization is ignored in the DGS; **but** the drop/undrop **resource bookkeeping** IS
real build work (data maintenance, not auth).

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 8 | 2 paged elastic; product/search-backed lookups |
| Mutations | 10 (+2 deferred) | partner-action dispatcher + 3 exports |
| Field-resolver type blocks | ~3 | `WorkspaceV2` (~22), `WorkspaceDepartmentV2`, paged |
| External dependencies | 14 keys (all cross-subgraph) | search/product/attachment 🔴 |
| Federation role | provides `WorkspaceV2` entity | every product-family domain references it |
| **Total stories** | **32** | green-field; separate subgraph |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 12–20d |
| B | Core Reads | 6 | 8–14d |
| C | Search & Listing | 2 | 5–9d |
| D | Mutations (simple) | 9 | 16–27d |
| E | Complex (partner-action dispatcher) | 1 | 8–13d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 8 | 34–56d |
| **Total** | | **32** | **87–146d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| Partner-action dispatcher (E01) | 🔴 High | 5-case drop/undrop with manual compensation + **un-awaited chains** (real bug); needs a failure strategy |
| `attachmentsWithMetaData` / `counts` (G01/G02) | 🟡 Medium-High | Large, performance-sensitive; budget X-Large |
| Cross-subgraph coupling to product | 🟡 Medium | `products`/`addResources` call product directly today; needs entity refs / a product client |
| Schema-drift drop/undrop wrappers | 🟢 Low | Survey live consumers before deleting |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `workspaceBusinessPartnerActionsV2` failure strategy + await the fire-and-forget chains | E01 | Tech Lead + PO |
| 2 | Delete or `@deprecated` the 2 drop/undrop drift wrappers | F02 | PO |
| 3 | `products`/`addResources` — federated entity reference vs a product client | D04/G04 | Architect |

## Migration approach (summary)

Phase **A** schema + `WorkspaceServiceV2` port (`plm-workspace`); **B** lookups; **C** paged search; **D** the
simpler mutations (incl. product side-effects + exports); **E** the Very-High partner-action dispatcher
(choose a failure strategy, fix the un-awaited chains); **F** expose `WorkspaceV2` as a federated entity +
drift decision; **G** the field resolvers (two X-Large) + tests. Full detail:
[03-schema-analysis.md §Migration Approach](../workspace/03-schema-analysis.md).

## Sequencing & capacity

Parallelizable after A; **2–3 engineers recommended** (~7–11 sprints for 3 vs ~17–29 for one). Full plan:
[04-po-summary.md](../workspace/04-po-summary.md).

---
*PO page assembled from the workspace analysis. Tickets:
[`../jira/workspace.csv`](../jira/workspace.csv) · [`../jira/workspace-stories.md`](../jira/workspace-stories.md).*
