# Measurement — Migration to the `plm-product` DGS (PO view)

> 🏷️ **Tags:** `dgs-migration` · `po-page` · `domain-measurement` · `pipeline-v2`  —  **Confluence location:** *Federation Graph Migration ▸ Domains ▸ measurement*

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.  
> Deep dives: migration approach & schema · field inventory · engineering stories.  
> Create tickets from `../finalOutput/jira/measurement.csv`. Effort is **AI-estimated — confirm in refinement.**

---

## What are we building?

- We are moving the **Measurement** domain — measurement sets (the size/point-of-measure specs for a product), their sample measurements, and the master-data unit lists — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is **mid-sized and mid-low risk**: 7 queries, 8 mutations, 15 field resolvers on a 175-line resolver, with **no polymorphism**.
- The one genuinely harder piece is `updateMeasurement`, a 2-step write (workspace association, then body) with no rollback today.

`getMeasurements` depends on the **relationship** service to find a product's measurement-set ids, and the
template/size/tight-fit references are **separate sibling domains** we only reference (not migrate here).

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); measurement has zero downstream-token sites.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 3 cacheable master-data |
| Mutations | 8 | 6 simple + `updateMeasurement` (2-step) + add |
| Field-resolver type blocks | 2 | `Measurement` (13), `SampleMeasurementSet` (2) |
| External dependencies | 11 keys (2 🔴 · 6 🟡 · 3 🔵) | relationship/search 🔴; templates 🟡 |
| Federation contributions | 2 (Product, SampleV2) | BLOCKED-BY product/sample |
| **Total stories** | **20** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 5 | 5–9d |
| C | Listing | 2 | 4–7d |
| D | Mutations (simple) | 7 | 8–14d |
| E | Complex (`updateMeasurement`) | 1 | 4–7d |
| F | Federation | 2 | 3–5d (BLOCKED-BY product/sample) |
| G | Field Resolvers & Tests | 3 | 8–13d |
| **Total** | | **20** | **32–55d** (buffered) |

> One engineer ≈ **7–11 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateMeasurement` failure strategy | E-01 | Tech Lead + PO |
| 2 | `updateMeasurementComponentStatus` no auth token — backend-enforced? | D-05 | PO |
| 3 | Adopt tagged `MeasurementAccessInput`? | D-02 | Product Owner |
| 4 | Push `getMeasurements`/`getMeasurementsElastic` sort to backend? | C-01/C-02 | Backend Eng |
| 5 | Are the 2 unused version service methods needed cross-domain? | B-01 | Tech Lead |

## Migration approach (summary)

**B** Core Reads; **C** Listing; **D** Mutations (simple); **E** Complex (`updateMeasurement`); **F** Federation; **G** Field Resolvers & Tests. Full detail: `be-03-schema-analysis.md §Migration Approach`.

## Sequencing & capacity

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~8–14 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel |
| 3 engineers | ~4–6 sprints | critical path A → E-01 → G-01 → G-04 |

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-04 | listing + simple mutations |
| 3 | D-05–D-07 + E-01 | remaining mutations + `updateMeasurement` |
| 4 | G-01–G-02, G-04 | field resolvers (G-04 recommended, PO-gated). Test coverage/parity tracked outside this Jira pipeline, created manually. |
| post-launch | F-01, H-01 | federation contributions |

---
*PO review assembled from the `measurement` analysis. Jira tickets: `finalOutput/jira/measurement.csv`. Full engineering detail: `measurement-comprehensive.md` (same folder).*