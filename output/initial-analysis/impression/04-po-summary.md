# Phase 4: PO Sprint Planning Summary — Impression

> **Domain:** `impression` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Stories:** [04-stories.md](./04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

- We are moving the **Impression** domain (the product's printed/embellished artwork "impressions" and their per-partner counts) off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is the
**smallest and lowest-risk** of the thirteen domains: 2 queries, 1 mutation, and 6 field resolvers across a
66-line resolver — no polymorphism, no orchestration. We recommend migrating it **first** as a team warm-up
that proves the pipeline end-to-end.

- The only mild wrinkle is the counts query: today it returns the impressions **list** and a field resolver aggregates per-partner counts (re-fetching the product).
- We recommend a cleaner typed result as a fast-follow, but the existing contract can be preserved exactly.

**ACL note:** the current code obtains a per-product capability token via ACL; Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs (`complexStories/*/02-adr-noacl-*.md`) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 2 | one reuses the other's REST call |
| Mutations | 1 | delete + update sets in one PUT |
| Field-resolver type blocks | 2 | `Impression` (5), `ImpressionCount` (1) |
| External dependencies | 4 keys (0 🔴 · 1 🟡 · 3 🔵) | workspace, VMM, user-profile |
| Federation contributions | 1 (Product extension) | BLOCKED-BY product |
| **Total stories** | **7** | green-field |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads (incl. DGS module init + ImpressionService wiring) | 2 | 4–6d |
| D | Mutations | 1 | 2–3d |
| F | Federation (Product) | 1 | 1–2d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 3 | 4–7d |
| **Total** | | **7** | **11–18d** (buffered) |

> Phase A dissolved — schema skeleton, owned types, external stubs, and `ImpressionService` (2 methods) are a one-time checklist preamble in **B-01**. One engineer ≈ **2–4 sprints**.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| Awkward counts contract | 🟢 Low | Optional cleanup to a typed result; safe to defer |
| `enableWorkspaceContextFiltering` not forwarded today | 🟢 Low | Confirm whether it should filter |
| Federation contribution waits on product | 🟢 Low | Not on critical path |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | Preserve `ImpressionCount` contract or adopt `ImpressionCountResult`? | B-02/G-02 | Product Owner |
| 2 | Should `enableWorkspaceContextFiltering` filter at the backend? | B-01 | Backend Eng |

## Dependency Map
```
plm-product (Impression subgraph) depends on:
 spark-product backend REST .../impressions/product
 sibling DGS (federation): workspace, user-profile ; Hive Gateway → VMM
 product domain F-01 Product entity extension (impressions + impressionCounts)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 + B-02 | **B-01:** DGS module init (schema/types/stubs/scalars) + ImpressionService wiring + `searchImpressionsByProductId`; **B-02:** counts query |
| 2 | D-01 + G-01 + G-02 | mutation + field resolvers + counts aggregation |
| 3 | G-03 | tests & parity |
| post-launch | F-01 | Product extension (unblocked by product) |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~3–5 sprints | sequential |
| 2 engineers | ~2–3 sprints | reads + field resolvers parallel |

---
*Pipeline 2.0 — Phase 4 complete. Impression artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Lowest-risk domain — recommended first migration.*
