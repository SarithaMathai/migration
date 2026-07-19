# Federated GraphQL Migration — Program Overview

> **Very high level.** This is the top of the reading tree — read this first, regardless of role. It
> answers "what is this program, why, and what's the shape of the work" in one page, then points down
> into the detailed artifacts.
> **Generated:** 2026-07-18. Numbers are computed live from `output/analysis/*/be-04-stories.md` and
> `output/jira/all-stories.csv` — see [Regeneration](#regeneration) for how to refresh this doc.

---

## 1. What is this program

The PLM GraphQL API is moving off a monolithic Node.js gateway (`spark-internal-graphql`) onto
**Netflix DGS subgraphs**, federated through the **Hive Schema Registry**. Today one gateway resolver
often reaches directly into several domains' backends to answer one field (e.g. the TechPack panel's
badge counts, or a product's related claims/attachments). Federation gives each domain its own
subgraph that owns and serves its own data, with the gateway composing the graph instead of one team's
code doing it by hand.

**Why now:** the direct cross-domain reach-through is exactly the coupling that makes the monolith hard
to change safely — no domain team can deploy independently, and full-graph traversals (e.g. the
TechPack facade's relationship-graph walk) exist only because no domain exposes "my slice" as an
operation. Federation removes both problems at once.

## 2. Scope — 8 domains, phase 1

| Domain | Target subgraph | Role |
|---|---|---|
| Product | `plm-product` (host) | Largest surface; hosts the shared DGS scaffold everything else co-locates into |
| BOM | `plm-product` (co-located) | Bill-of-materials |
| Packaging | `plm-product` (co-located) | Packaging BOM |
| Measurement | `plm-product` (co-located) | Measurement sets |
| Product Details | `plm-product` (co-located) | Extended product attribute sets |
| Watchlist | `plm-product` (co-located) | Watchlist entries |
| Impression | `plm-product` (co-located) | Impression sub-types |
| Claims | `spark-claims` (separate subgraph) | Only phase-1 domain with its own subgraph, not co-located in `plm-product` |

Five domains federate in a **later phase** and are referenced only as *not-yet-live subgraphs* that
some phase-1 stories are blocked on: **attachment, discussion, sample, search, workspace**. See
[Cross-domain dependencies](#5-cross-domain-dependencies) below.

## 3. The phase-lettering scheme (how backend work is organized)

Every backend story belongs to one domain and one phase letter. The letter is what kind of work it is,
not when it happens in the roadmap — sequencing is a separate axis (§6).

| Phase | Name | What it covers |
|---|---|---|
| **0** | Spikes | Open design questions that gate real stories (e.g. write-saga strategy, TechPack assembly pattern) — tracked as `S-NN`, not counted in the 201 build-story total |
| **A** | Foundation & Type Resolvers | One-time scaffolding, shared registries, `@DgsTypeResolver` unions |
| **B** | Core Reads | `@DgsQuery` reads |
| **C** | Search & Listing | Search/listing operations |
| **D** | Mutations (simple) | Straightforward writes |
| **E** | Complex Operations | Multi-step writes, orchestration, partner actions, TechPack aggregation |
| **F** | Federation & Stitching | Platform/gateway work that stays *inside* one subgraph — facade retirement, schema composition, contract alignment |
| **G** | Field Resolvers & Utils | Field-level resolvers, small utility work |
| **H** | Entity Resolution *(new this program)* | Cross-subgraph `@DgsEntityFetcher`/`@key` fields — the actual federated contribution, resolved by a **separate** subgraph. Split out from Phase F so "still in my subgraph" (F) and "genuinely blocked on someone else's subgraph" (H) are never conflated. |

**Rule of thumb:** if a field's owner is a different subgraph than the one asking for it, it's Phase H
and it is `Blocked by:` that subgraph. If the owner is co-located in the same subgraph, it's Phase F and
ships on its own schedule.

## 4. Program totals

| Metric | Value |
|---|---|
| Domains (phase 1) | 8 |
| Target DGS services (phase 1) | 2 (`plm-product`, `spark-claims`) |
| Backend build stories | **201** (+ 7 program-level spikes, tracked separately) |
| Frontend stories | **40** (platform enablement — former "Wave 0" — already complete) |
| Complex-case ADRs (cross-domain design decisions) | **8** — see [complexStories/](../complexStories/) |
| Backend effort (buffered +20%) | 432–733 engineer-days |
| Frontend effort (single engineer) | 163–254 engineer-days |

Full per-domain breakdown (story counts, complexity mix, effort, top risk): [`output/summary/00-program-overview.md`](../summary/00-program-overview.md).

## 5. Cross-domain dependencies

Two different relationships exist between stories, and they are **not interchangeable**:

- **`Depends on:`** — an *intra-domain* build-order edge. The wave scheduler enforces this automatically
  when computing each domain's "Recommended Implementation Order." If `X` depends on `Y`, `Y` ships
  first, in the same domain.
- **`Blocked by:`** — a *cross-domain or cross-subgraph* constraint. Nothing in the generator pipeline
  schedules around this automatically — it's a documented fact a human (PO, tech lead) has to honor when
  sequencing sprints across domains.

The full, consolidated table of every `Blocked by:` in the program lives in
[`output/analysis/program/cross-domain-dependencies.md`](../analysis/program/cross-domain-dependencies.md).
As of this writing: **6** stories are blocked on shared infrastructure in another *phase-1* domain (all
six wait on `PRODUCT-BE-E-00`, the shared `WriteSaga` module), and **9** are blocked on a subgraph that
hasn't federated yet (5 of those are product's own Phase H TechPack contributions waiting on
attachment/discussion/sample/claims/construction).

## 6. Recommended sequencing (who builds what, in what order)

With the current team model (1 backend + 1 frontend engineer — see
[`team_config.py`](../../fedMigrationScripts/generatescripts/team_config.py)), the backend queue is:

```
product → watchlist → productDetails → measurement → packaging → bom → claims → impression
```

**Product must stay first.** `PRODUCT-BE-E-00` (the shared WriteSaga module) is a cross-domain
`Blocked by:` dependency for six other domains' own `E-01` write stories. Product's build finishes
`E-00` around day 16 of its own ~200-day build — long before any consumer domain's lane would start —
so this ordering is load-bearing, not a preference.

Full story-by-story order per domain, with dependency/blocks/parallelizable metadata: [`output/summary/02-project-plan.md`](../summary/02-project-plan.md).
Team lanes and sprint milestones: [`output/summary/01-implementation-plan-1BE-1FE.md`](../summary/01-implementation-plan-1BE-1FE.md).

## 7. Complex cases (cross-domain design decisions)

Eight areas of the system needed a ratified design decision *before* any story could be written safely,
because the "right" implementation spans multiple domains or subgraphs. Each has its own folder under
[`output/complexStories/`](../complexStories/):

| Case | Decision | Status |
|---|---|---|
| `non-atomic-write-saga` | Shared WriteSaga module (ADR-013) | Ratified |
| `techpack` | Facade-then-federate (ADR-015, draft) | 🟠 Ratification pending |
| `partner-drop-undrop-write` | Orchestrated fan-out + compensation (ADR-012) | Ratified |
| `notRemovable-undroppable-partners` | Owner `@requires` aggregation (ADR-014) | Ratified |
| `components-and-counts-rollups` | (ADR-014 twin) | Ratified |
| `attachments-enrichment` | (ADR-018) | Ratified |
| `polymorphic-type-resolution` | Shared code→type registry + CI conformance gate (ADR-017) | Ratified |
| `cross-domain-association` | Shared `associate()` component (ADR-011) | Ratified |

Each case folder's `00-overview.md` is the problem brief, `01-adr-*.md` is the decision record, and
`01-stories.md` is the index of concrete story ids (in each affected domain's `be-04-stories.md`) that
implement it.

## 8. Where to go next

- **Implementing a story?** → [`docs/instructions_engineer.md`](../../docs/instructions_engineer.md)
- **Prioritizing or reviewing the backlog?** → [`docs/instructions_po.md`](../../docs/instructions_po.md)
- **Architecture / domain map diagrams** → [`01-architecture-diagrams.md`](./01-architecture-diagrams.md)
- **Where every artifact lives, indexed** → [`02-story-domain-index.md`](./02-story-domain-index.md)
- **Full folder map by audience** → [`output/README.md`](../README.md)

## Regeneration

This doc is hand-authored (a curated top-level entry point), unlike `output/summary/00-program-overview.md`
which is generated live from source. If domain counts, phase totals, or the cross-domain-dependency
counts in §5 change, re-derive them from `output/summary/00-program-overview.md` and
`output/analysis/program/cross-domain-dependencies.md` (both regenerated by
`python fedMigrationScripts/generatescripts/generate_all.py`) and update this page's numbers to match.

---
*Program overview (high-level entry point) · output/overview/00-program-overview.md*
