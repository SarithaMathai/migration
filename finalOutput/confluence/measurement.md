# Measurement — Migration to the `plm-product` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../measurement/03-schema-analysis.md) ·
> [field inventory](../measurement/05-attribute-inventory.md) · [engineering stories](../measurement/04-stories.md).
> Create tickets from [`../jira/measurement.csv`](../jira/measurement.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Measurement** domain — measurement sets (the size / point-of-measure specs for a
product), their sample measurements, and the master-data unit lists — off the `spark-internal-graphql`
gateway into the **`plm-product`** DGS. It is **mid-sized and mid-low risk**: 7 queries, 8 mutations, 15
field resolvers on a 175-line resolver, with **no polymorphism**. The one genuinely harder piece is
**`updateMeasurement`**, a 2-step write (workspace association, then body) with no rollback today.

`getMeasurements` depends on the **relationship** service to find a product's measurement-set ids, and the
template / size / tight-fit references are **separate sibling domains** we only reference (not migrate here).

**ACL note:** the current code obtains per-resource capability tokens via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 3 cacheable master-data |
| Mutations | 8 | 6 simple + `updateMeasurement` (2-step) + add |
| Field-resolver type blocks | 2 | `Measurement` (13), `SampleMeasurementSet` (2) |
| External dependencies | 11 keys (2 🔴 · 6 🟡 · 3 🔵) | relationship / search 🔴; templates 🟡 |
| Federation contributions | 2 (Product, SampleV2) | BLOCKED-BY product / sample |
| **Total stories** | **24** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 8–13d |
| B | Core Reads | 5 | 5–9d |
| C | Listing | 2 | 4–7d |
| D | Mutations (simple) | 7 | 8–14d |
| E | Complex (`updateMeasurement`) | 1 | 4–7d |
| F | Federation | 2 | 3–5d (BLOCKED-BY product / sample) |
| G | Field Resolvers & Tests | 3 | 8–13d |
| **Total** | | **24** | **40–68d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updateMeasurement` 2-step write | 🟡 Medium | Needs a decision (E01) on recovering from a mid-write failure |
| `getMeasurements` needs the relationship service | 🟡 Medium | Sequence relationship federation, or call its service directly |
| Template / size / tight-fit are separate domains | 🟢 Low | Field resolvers return stubs until those subgraphs federate |
| Federation contributions wait on product / sample | 🟢 Low | Not on the critical path |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updateMeasurement` failure strategy | E01 | Tech Lead + PO |
| 2 | `updateMeasurementComponentStatus` no auth token — backend-enforced? | D05 | PO |
| 3 | Adopt tagged `MeasurementAccessInput`? | D02 | Architect |
| 4 | Push `getMeasurements` / `getMeasurementsElastic` sort to backend? | C01/C02 | Backend Eng |

## Migration approach (summary)

Phase **A** schema + `MeasurementService` port; **B** the reads (3 cacheable); **C** listing; **D** simple
mutations; **E** the `updateMeasurement` 2-step write; **F** the contributions to Product (internal) and
SampleV2 (federation, blocked by sample); **G** field resolvers + tests. Full detail:
[03-schema-analysis.md §Migration Approach](../measurement/03-schema-analysis.md).

## Sequencing & capacity

Reads + mutations parallelize after A. One engineer ≈ 8–14 sprints; 3 engineers ≈ 4–6 (critical path
A → E01 → G01 → G03). Full plan: [04-po-summary.md](../measurement/04-po-summary.md).

---
*PO page assembled from the measurement analysis. Tickets:
[`../jira/measurement.csv`](../jira/measurement.csv) · [`../jira/measurement-stories.md`](../jira/measurement-stories.md).*
