# Phase 4: PO Sprint Planning Summary — Sample

> **Domain:** `sample` · **Target DGS:** separate `plm-sample` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

We are moving the **Sample** domain — physical/virtual samples, their rounds, evaluations, RFID locations and
master-data — off the `spark-internal-graphql` gateway into its **own `plm-sample` DGS subgraph**. Sample is
referenced by **product** (`Product.samples`/`sampleIds`), **measurement** (`SampleV2.sampleMeasurement`) and
**workspace** (sample report + drop/undrop).

It is **large and mid-high risk**: 23 queries, 9 mutations **(+3 schema-drift)**, ~45 field resolvers on a
430-line resolver. The cost concentrates in the **wide `SampleV2` entity** with **prefix-gated polymorphic
parent hydration** (product / trim / color / fabric / artwork / asset), the **`SampleAsset` union**, and two
evaluation writes (`updateSamplesV2`, `bulkEvaluateSamples`). A long master-data tail (~13 cacheable lookups)
is cheap.

**ACL note:** reads/writes curry capability tokens; drop/undrop bookkeeping lives in the workspace dispatcher.
**ACL is ignored in the DGS implementation** (no ACL story) — context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 23 | ~13 cacheable master-data + by-id/parent + 2 RFID |
| Mutations | 9 (+3 deferred) | create/round/update/workspace-assoc/export/retry/clone + 2 evaluation writes |
| Field-resolver type blocks | ~7 | `SampleV2` (~35) + 6 sub-types |
| Polymorphism | 1 union (`SampleAsset`) | A04 |
| External dependencies | ~20 keys (all cross-subgraph) | search 🔴; product/workspace/measurement/material/… 🟡 |
| Federation role | provides `SampleV2` entity | product/measurement/workspace reference it |
| **Total stories** | **33** | green-field; separate subgraph |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 5 | 14–24d |
| B | Core Reads | 8 | 8–14d |
| C | RFID Reads | 2 | 4–7d |
| D | Mutations (simple) | 7 | 11–18d |
| E | Complex (evaluation writes) | 2 | 9–15d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 7 | 31–51d |
| **Total** | | **33** | **81–136d** (buffered) |

> One engineer ≈ **16–27 sprints**. Parallelizable after A; 2–3 engineers recommended.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| Wide entity + prefix-gated polymorphic parents (G02) | 🟡 Medium-High | The biggest field-resolver block; budget X-Large |
| Evaluation writes (`bulkEvaluateSamples`/`updateSamplesV2`) (E01/E02) | 🟡 Medium-High | Orchestration; needs a partial-failure decision |
| `SampleAsset` union correctness (A04) | 🟡 Medium | Type resolver + per-member tests |
| Schema-drift drop/undrop owned by workspace | 🟢 Low | Coordinate ownership; survey consumers |
| RFID latest-location perf | 🟢 Low | Batch tag queries; cache the reduce |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `bulkEvaluateSamples`/`updateSamplesV2` partial-failure strategy | E01/E02 | Tech Lead + PO |
| 2 | `SampleAsset` union members + prefix rules (beyond Color/Artwork?) | A04 | Architect |
| 3 | Delete or `@deprecated` the 3 drift mutations; drop/undrop ownership (sample vs workspace) | F02 | Architect |
| 4 | `createSamplesV2` file-relationship failure strategy | D01 | Tech Lead |

## Dependency Map
```
plm-sample (Sample subgraph) depends on (all cross-subgraph):
  search 🔴 (attachments, RFID latest locations)
  product, workspace, measurement, relationship, attachment, notification, user-profile/role/user-group,
  trim, color, colorArchroma, combination, fabric, artwork, material, tgtColorEvaluator 🟡
  Hive Gateway → VMM, Brand, IG, Tag, recentlyViewed
  provides → SampleV2 entity for product (samples/sampleIds), measurement (sampleMeasurement), workspace
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | A01–A05 + B01–B08 | schema, union resolver, service port, reads + master-data |
| 3 | C01/C02 + D02–D06 | RFID + simple mutations |
| 4 | D01/D07 + E01/E02 | create(+files), clone, evaluation writes |
| 5 | G01/G02 | users + the prefix-gated parents/union (X-Large) |
| 6 | G03–G06 | partners/assoc/attachments/participants |
| 7 | F01/F02 + G07 | entity fetcher + drift decision + tests |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~16–27 sprints | sequential |
| 2 engineers | ~10–16 sprints | reads + mutations parallel after A |
| 3 engineers | ~6–11 sprints | critical path A → G02 → G07; E in parallel |

---
*Pipeline 2.0 — Phase 4 complete. Sample artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Separate `plm-sample` subgraph.*
