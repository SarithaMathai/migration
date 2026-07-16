# README (PO) — how to navigate the migration docs as a Product Owner

> For **Product Owners, Stakeholders, and Reviewers**. This is navigation only — what to open, in what order,
> and what you'll get. For the full file inventory + conventions see [`README.md`](./README.md).

---

## Your path

1. **Start — one domain's PO review:** `summary/{domain}/{domain}-po-review.md`
   - Scope, effort by phase, key risks, **the decisions you need to make**, sprint capacity, and the
     **ship-on-green** model. **No code.** This is your 1–2 page page (paste-ready for Confluence).

2. **Zoom out — the whole program:** `summary/00-program-overview.md`
   - All 13 domains: totals, per-domain table, target DGS groupings, top risks, open decisions, recommended
     sequencing, and cross-domain blockers.

3. **Approve the plan — the breakdown:** `summary/{domain}/FederatedGqlBrakDown-{domain}.md`
   - Every story in one table (ID, summary, size, dependencies, status), the **Phase-0 spikes**, the
     **§5b complex-story breakdowns**, risks, decisions, and the dependency map. This is the page you sign off.

---

## What to focus on

- **Decisions required** (in the po-review + breakdown): these gate a phase — resolve them before the sprint
  that needs them. Spikes (Phase 0) are the research that produces each decision.
- **Effort & capacity:** effort is **AI-estimated** — confirm in refinement. The phase table shows where the
  cost concentrates (usually Phase G field-resolvers + the complex Phase-E stories).
- **Ship model:** each story ships to prod once its own tests + parity pass. The exceptions are
  **BLOCKED-BY** stories (they wait for another subgraph to go live) — plan those last.
- **Complex stories:** the §5b table shows the few Very-High/High stories broken into ≤5-day sub-tasks and
  which cross-domain case (`complexStories/<case>/`) holds the detail.

## How to read a story row (scan, don't implement)

```
BOM-BE-B-04 · getBomByParentId · 🔷 Query · 🟢 Low [XS] · Depends On: — · ⬜ Not Started
```
- **Size:** 🟢 XS · 🟡 M · 🟠 L · 🔴 XL — drives sprint load.
- **Depends On:** only real story-to-story blockers (the one-time `B-01` scaffold is assumed, not shown).
- **Status:** ⬜ Not Started → update as work proceeds.

> Each story = **one `spark-internal-graphql` operation being migrated** (the title is that operation).

## Getting it into Jira / Confluence
Hand to delivery: `jira/{domain}.csv` imports the stories; the breakdown + po-review pages publish to
Confluence. Prompts: [`PUSH-TO-JIRA-CONFLUENCE.md`](./PUSH-TO-JIRA-CONFLUENCE.md).
