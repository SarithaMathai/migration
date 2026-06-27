# Phase 4: PO Sprint Planning Summary — BOM

> **Domain:** `bom` · **Target DGS:** `plm-product` (co-located) · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges below are **AI-estimated — confirm in refinement.** Stories themselves carry complexity only.

---

## What Are We Building?

We are moving the **Bill of Materials (BOM)** domain off the shared Node.js `spark-internal-graphql`
gateway and into the **`plm-product`** Netflix DGS service, where it lives next to Product, Measurement,
Impression and Packaging. BOM is the structured record of every material, supplier and impression that
makes up a product, and it is referenced by many sibling domains.

BOM is **mid-sized**: 13 queries, 6 mutations, and ~46 field resolvers across 18 type blocks, on a
735-line resolver. Its defining challenge is **material polymorphism** — 7 concrete material types
(Trim, Wash, Fabric, FabricSpec, Combination, Packaging, plus the base) resolved by a category dispatcher,
and 5 impression sub-types. The single hardest piece of work is `updateBom`, a 3-step write (workspace →
body → permissions) that today has no rollback.

The schema is **wide but shallow**: the large majority of attributes are direct pass-throughs (cheap to
migrate). Risk concentrates in ~38 cross-domain field resolvers (material-library and color lookups) and
the 2 polymorphic interfaces. See [05-attribute-inventory.md](./05-attribute-inventory.md).

**Note on ACL:** the current gateway uses ACL to obtain a per-resource capability token. Per decision,
**ACL is ignored in the DGS implementation** — there is no ACL story; we only note where/why it's used today.

---

## Migration Scope

| Surface | Count | Notes |
|---------|-------|-------|
| Queries | 13 | 4 are cacheable master-data lookups |
| Mutations | 6 | 5 simple + `updateBom` (complex) |
| Field-resolver type blocks | 18 | one story each (G01–G15) |
| Material polymorphism | 7 types + interface + type resolver | A04 |
| Impression polymorphism | 5 types + interface | A04 |
| External dependencies | 12 loader keys (2 🔴 · 6 🟡 · 4 🔵) | sibling DGS + VMM platform |
| Federation contributions | 2 (Product extension, ResourcesCount.bomsCount) | BLOCKED-BY product |
| **Total stories** | **42** | green-field |

## Story Summary by Phase (AI-estimated)

| Phase | Name | Stories | Effort (est., +20% buffer) | Ready when |
|-------|------|---------|----------------------------|-----------|
| A | Foundation & Schema | 5 | 10–16d | Sprint 1 |
| B | Core Reads | 8 | 8–14d | after A02+A05 |
| C | Search & Listing | 5 | 9–15d | after A05 |
| D | Mutations (simple) | 5 | 5–10d | after A05 |
| E | Complex (`updateBom`) | 1 | 6–10d | after A05 |
| F | Federation Contributions | 2 | 4–7d | BLOCKED-BY product |
| G | Field Resolvers & Tests | 16 | 34–55d | after A04+A05 |
| **Total** | | **42** | **76–127d** (buffered) | |

> One engineer ≈ **15–25 sprints** (5d). Phases B/C/D/G parallelize heavily after A.

## Key Risk Areas (plain English)

| Risk | Severity | What the PO needs to know |
|------|----------|---------------------------|
| `updateBom` 3-step write can leave data half-updated | 🔴 High | Needs an architecture decision (E01) on how to recover from a mid-write failure |
| Material field resolvers depend on 5 sibling domains | 🟡 Medium | BOM can ship reads/writes; full material enrichment needs hub/trim/wash/fabric/combination federated |
| 7-variant polymorphism is easy to break when fields are added | 🟡 Medium | A CI check (G16) guards this |
| Trim size logic is intricate (15 cases × 2) | 🟡 Medium | One larger story (G08) with a parity table |
| Federation contributions wait on the product domain | 🟡 Low | F01/F02 are post-launch; not on the critical path |

## Decisions Required from PO / Architecture

| # | Decision | Blocks | Owner |
|---|----------|--------|-------|
| 1 | `updateBom` failure strategy: saga / compensation log / best-effort | E01 | Tech Lead + PO |
| 2 | `updateBomComponentStatus` has no auth token — is the backend enforcing it? | D05 | PO |
| 3 | Keep `Bom_Unified` as a type or replace with field selection on `Bom`? | A02/G01 | Architect |
| 4 | Are the 3 unused service methods called by other domains? Confirm before delete | A05 | Tech Lead |
| 5 | Federation rollout order for hub/trim/wash/fabric/combination | A03/G | Architect + Platform |
| 6 | `getBomByParentId` — push sort to backend? | B04 | Backend Eng |
| 7 | `searchMaterialsBom` — keep query-string flatten or structured DTO? | C02 | Backend Eng |
| 8 | `Bom.product` — does `parentId` only start with `PID`? | G01 | Backend Eng |

## Dependency Map

```
plm-product (BOM subgraph) depends on:
  spark-product backend   REST .../bom/v1 + /masterData ; elastic bom/material search
  sibling DGS (federation): material-hub, trim, wash, fabric, combination, workspace, tag, user-profile
  Hive Gateway → VMM platform (business partners, supplier roles, facility location)
  product domain          F01 Product entity extension ; F02 TechPack ResourcesCount.bomsCount
```

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|--------|---------|-------|
| 1 | A01–A05 | schema, stubs, type resolvers, service port |
| 2 | B01–B08 + D03/D04 | reads (incl. 4 cacheable) + lock/unlock |
| 3 | C01–C05 + D01/D02/D05 | search/supplier + simple mutations |
| 4 | E01 | `updateBom` 3-step write (focused) |
| 5 | G01–G07 | entity + simple material field resolvers |
| 6 | G08 + G09 | trim (large) + wash |
| 7 | G10–G15 | impression branches + search-result enrichment + trivial bundle |
| 8 | G16 | tests, parity harness, load test |
| post-launch | F01, F02 | federation contributions (unblocked by product) |

## Capacity Planning

| Team size | Calendar (5d sprints) | Notes |
|-----------|----------------------|-------|
| 1 engineer | ~15–25 sprints | sequential |
| 2 engineers | ~9–15 sprints | B/C/D + most of G parallel |
| 3 engineers | ~6–10 sprints | critical path A → E01 → G08/G10 → G16 |

> Phase G (field resolvers) dominates the calendar; G08 (trim) and G10 (impression branch) are the two
> biggest field-resolver stories.

---
*Pipeline 2.0 — Phase 4 complete. BOM artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*
