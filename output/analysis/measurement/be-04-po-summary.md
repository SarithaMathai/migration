# Phase 4: PO Sprint Planning Summary — Measurement

> **Domain:** `measurement` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Stories:** [be-04-stories.md](./be-04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

- We are moving the **Measurement** domain — measurement sets (the size/point-of-measure specs for a product), their sample measurements, and the master-data unit lists — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **mid-sized and mid-low risk**: 7 queries, 8 mutations, 15 field resolvers on a 175-line resolver, with **no polymorphism**.
- The one genuinely harder piece is `updateMeasurement`, a 2-step write (workspace association, then body) with no rollback today.

`getMeasurements` depends on the **relationship** service to find a product's measurement-set ids, and the
template/size/tight-fit references are **separate sibling domains** we only reference (not migrate here).

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); measurement has zero downstream-token sites.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 3 cacheable master-data |
| Mutations | 8 | 6 simple + `updateMeasurement` (2-step) + add |
| Field-resolver type blocks | 2 | `Measurement` (13), `SampleMeasurementSet` (2) |
| External dependencies | 11 keys (2 🔴 · 6 🟡 · 3 🔵) | relationship/search 🔴; templates 🟡 |
| Federation contributions | 2 (Product, SampleV2) | BLOCKED-BY product/sample |
| **Total stories** | **30** | green-field (20 core + 10 sub-domain: measurement-template, size-template, tight-fit) |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 9 | 9–16d |
| C | Listing | 2 | 4–7d |
| D | Mutations (simple) | 10 | 12–20d |
| E | Complex (`updateMeasurement`) | 1 | 4–7d |
| F | Federation (internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 5 | 10–17d |
| H | Entity Resolution (cross-subgraph) | 2 | 2–4d (BLOCKED-BY product/sample deploy) |
| **Total** | | **30** | **42–73d** (buffered) |

> **Sub-domain note (2026-07-19).** B-06–B-09 (measurement-template, size-template, tight-fit reads),
> D-08–D-10 (their mutations), and G-05–G-07 (their field resolvers) are included above. Original
> core-measurement stories: 20; sub-domain additions: 10; total: 30.

> **Phase H note.** H-01 (`SampleV2.sampleMeasurement`) and H-02 (`SampleMeasurementSet.sample`) are
> cross-subgraph contributions — they cannot ship until the sample subgraph is deployed. Sequenced post-launch.

> One engineer ≈ **7–11 sprints**.

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B-01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateMeasurement` 2-step write | 🟡 Medium | Needs a decision (E-01) on recovering from a mid-write failure |
| `getMeasurements` needs the relationship service | 🟡 Medium | Sequence relationship federation, or call its service directly |
| Template/size/tight-fit are separate domains | 🟢 Low | Field resolvers return stubs until those subgraphs federate |
| Federation contributions wait on product/sample | 🟢 Low | Not on critical path |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateMeasurement` failure strategy | E-01 | Tech Lead + PO |
| 2 | `updateMeasurementComponentStatus` no auth token — backend-enforced? | D-05 | PO |
| 3 | Adopt tagged `MeasurementAccessInput`? | D-02 | Product Owner |
| 4 | Push `getMeasurements`/`getMeasurementsElastic` sort to backend? | C-01/C-02 | Backend Eng |
| 5 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Dependency Map
```
plm-product (Measurement subgraph) depends on:
 spark-product backend REST .../measurements/v1 + /masterData ; elastic measurement search
 relationship service (getMeasurements id resolution) 🔴
 sibling DGS (federation): workspace, sample, measurement-template, size-template, tight-fit, user-profile
 Hive Gateway → VMM (business partners)
 cross-domain blockers:
   E-01 (updateMeasurement) depends on PRODUCT-BE-E-00 (WriteSaga shared module)
   H-01/H-02 BLOCKED-BY sample subgraph deploy
 product domain F-01 Product.measurementSets (internal) ; sample domain H-01 SampleV2.sampleMeasurement
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-04 | listing + simple mutations |
| 3 | D-05–D-07 + E-01 | remaining mutations + `updateMeasurement` |
| 4 | G-01–G-02, G-04 | field resolvers (G-04 recommended, PO-gated). Test coverage/parity tracked outside this Jira pipeline, created manually. |
| post-launch | F-01, H-01 | federation contributions |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~8–14 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel |
| 3 engineers | ~4–6 sprints | critical path A → E-01 → G-01 → G-04 |

---
*Pipeline 2.0 — Phase 4 complete. Measurement artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*
