# Sample — Migration to a dedicated `plm-sample` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../sample/03-schema-analysis.md) ·
> [field inventory](../sample/05-attribute-inventory.md) · [engineering stories](../sample/04-stories.md).
> Create tickets from [`../jira/sample.csv`](../jira/sample.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Sample** domain — physical/virtual samples, their rounds, evaluations, RFID locations and
master-data — off the `spark-internal-graphql` gateway into its **own `plm-sample` DGS subgraph**. Sample is
referenced by **product** (`Product.samples`/`sampleIds`), **measurement** (`SampleV2.sampleMeasurement`) and
**workspace** (sample report + drop/undrop).

It is **large and mid-high risk**: 23 queries, 9 mutations **(+3 schema-drift)**, ~45 field resolvers on a
430-line resolver. Cost concentrates in the **wide `SampleV2` entity** with **prefix-gated polymorphic parent
hydration** (product / trim / color / fabric / artwork / asset), the **`SampleAsset` union**, and two
evaluation writes. A long master-data tail (~13 cacheable lookups) is cheap.

**ACL note:** reads/writes curry capability tokens; drop/undrop bookkeeping lives in the workspace dispatcher.
**ACL is ignored in the DGS implementation** (no ACL story) — context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 23 | ~13 cacheable master-data + by-id/parent + 2 RFID |
| Mutations | 9 (+3 deferred) | create/round/update/workspace-assoc/export/retry/clone + 2 evaluation writes |
| Field-resolver type blocks | ~7 | `SampleV2` (~35) + 6 sub-types |
| Polymorphism | 1 union (`SampleAsset`) | A04 |
| External dependencies | ~20 keys (all cross-subgraph) | search 🔴; product/workspace/measurement/material/… 🟡 |
| Federation role | provides `SampleV2` entity | product/measurement/workspace reference it |
| **Total stories** | **33** | green-field; separate subgraph |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 5 | 14–24d |
| B | Core Reads | 8 | 8–14d |
| C | RFID Reads | 2 | 4–7d |
| D | Mutations (simple) | 7 | 11–18d |
| E | Complex (evaluation writes) | 2 | 9–15d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 7 | 31–51d |
| **Total** | | **33** | **81–136d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| Wide entity + prefix-gated polymorphic parents (G02) | 🟡 Medium-High | Biggest field-resolver block; budget X-Large |
| Evaluation writes (`bulkEvaluateSamples`/`updateSamplesV2`) (E01/E02) | 🟡 Medium-High | Orchestration; needs a partial-failure decision |
| `SampleAsset` union correctness (A04) | 🟡 Medium | Type resolver + per-member tests |
| Schema-drift drop/undrop owned by workspace | 🟢 Low | Coordinate ownership; survey consumers |
| RFID latest-location perf | 🟢 Low | Batch tag queries; cache the reduce |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `bulkEvaluateSamples`/`updateSamplesV2` partial-failure strategy | E01/E02 | Tech Lead + PO |
| 2 | `SampleAsset` union members + prefix rules (beyond Color/Artwork?) | A04 | Architect |
| 3 | Delete or `@deprecated` the 3 drift mutations; drop/undrop ownership (sample vs workspace) | F02 | Architect |
| 4 | `createSamplesV2` file-relationship failure strategy | D01 | Tech Lead |

## Migration approach (summary)

Phase **A** schema (wide `SampleV2` + the `SampleAsset` `@DgsTypeResolver` + ~10 inputs) + `SampleServiceV2`
port (`samples/v2`); **B** by-id/parent reads + the ~13 cacheable master-data queries; **C** the RFID reads;
**D** the simpler writes (create+files, round, workspace-assoc, exports, notification retries, bulk-clone);
**E** `updateSamplesV2` + `bulkEvaluateSamples`; **F** expose `SampleV2` as a federated entity + drift
decision; **G** the wide field-resolver surface (G02 = prefix-gated parents/union is X-Large) + tests. Full
detail: [03-schema-analysis.md §Migration Approach](../sample/03-schema-analysis.md).

## Sequencing & capacity

Parallelizable after A; **2–3 engineers recommended** (~6–11 sprints for 3 vs ~16–27 for one). Full plan:
[04-po-summary.md](../sample/04-po-summary.md).

---
*PO page assembled from the sample analysis. Tickets:
[`../jira/sample.csv`](../jira/sample.csv) · [`../jira/sample-stories.md`](../jira/sample-stories.md).*
