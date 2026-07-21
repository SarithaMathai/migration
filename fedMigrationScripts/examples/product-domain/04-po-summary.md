# Phase 4: PO Summary — Product

> **Domain:** `product`
> **Target DGS:** `ProductService` (repo: `plm-product`, url: `https://spark-product.dev.target.com`)
> **Pipeline Version:** 1.1
> **Generated:** 2026-05-01
> **Depends on:** [be-04-stories.md](./be-04-stories.md)
> **DGS Target Status:** Green-field (no existing DGS schema)

---

## What Are We Building?

The Product domain is the central entity in the Spark platform — it connects partners, teams, workspaces, attachments, samples, BOMs, measurements, and rules into a unified product development view. This migration moves the Product domain from the SPARK GraphQL gateway (Node.js) to a dedicated **Netflix DGS** (Spring Boot / Kotlin) service called `plm-product`.

The source codebase contains **781 lines of GraphQL schema** and **2,629 lines of resolver logic** — making this the most complex domain in the Spark ecosystem.

---

## Migration Scope

| Operation Type | Count | Status |
|---------------|-------|--------|
| Queries | 18 | 🔜 All to be built |
| Mutations | 23 | 🔜 All to be built (1 ⏭ deferred as internal sub-op) |
| Field Resolvers | 62 | 🔜 All to be built |
| External service dependencies | 29 | — |
| Source files migrated | 3 | schema, resolver, service |
| TechPack sub-stories (cross-domain CAT-4) | 8 placeholders | One per owning subgraph; full stories written in each domain's file |

This is a **green-field migration** — no existing DGS code exists for this domain.

> **TechPack note:** `getProductTechPackCountV1` and `getProductTechPackBulkCountV1` each return a `ResourcesCount` composite key entity whose 10 fields are owned by 8 different subgraphs (Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist). The Product subgraph owns only the query stub and the type definition. This decomposes into Phase E stories for the stub + aggregation facade (Day 1), and Phase F placeholder stories for each owning subgraph's federation extension (migrated as those domains come online). See `reference/techpack-migration-options.md` for full option analysis.

---

## Story Summary by Phase

| Phase | Description | Stories | Effort (days, raw) | Effort (+20% buffer) |
|-------|-------------|---------|---------------------|---------------------|
| Phase A | Foundation & Schema | 8 | 17–27 | 21–33 |
| Phase B | Core CRUD Queries | 3 | 4–6 | 5–8 |
| Phase C | Search & Listing | 3 | 11–16 | 14–20 |
| Phase D | Core Mutations | 4 | 12–18 | 15–22 |
| Phase E | Partner Management + TechPack Stub + Aggregation Facade | 7 | 29–48 | 35–58 |
| Phase F | Tech Pack Federation (per-subgraph) + Rules | 12 | 18–30 | 22–36 |
| Phase G | Complex Field Resolvers | 6 | 33–50 | 40–60 |
| Phase H | Federation & Stitching (remaining) | 4 | 9–14 | 11–17 |
| Phase I | Test Coverage | 4 | 14–20 | 17–24 |
| **Total** | | **51** | **147–229** | **180–278** |

> **Note:** All estimates are in engineering-days for one engineer. Parallelization with a team of 3–4 engineers can compress calendar time significantly.
>
> **Phase E expansion:** Now includes TechPack sub-stories: `ResourcesCount` schema (CAT-1), `getProductTechPackCountV1` stub+facade (CAT-2+CAT-3), and `getProductTechPackBulkCountV1` (CAT-2).
>
> **Phase F expansion:** Now includes 8 per-subgraph CAT-4 placeholder stories (Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist) + 1 aggregation facade retirement story + Rules routing story. The 8 placeholder stories are BLOCKED-BY each owning domain's migration and will be fully fleshed out in those domains' files.

---

## Key Risk Areas

| Risk | Severity | Relevant Stories |
|------|----------|-----------------|
| `attachmentsWithMetaData` — 6 external service calls, complex enrichment and sort | 🔴 Critical | PRODUCT-BE-G-01 |
| `productBusinessPartnerActions` DROP_UNDROP — relationship tree traversal + ACL update + sample side-effects | 🔴 Critical | PRODUCT-BE-E-04 |
| `getProductTechPackCountV1` — ACL tree traversal is 200+ lines of recursive graph logic shared across domains | 🔴 Critical | PRODUCT-BE-E-02 |
| TechPack sub-story coordination — 8 per-subgraph CAT-4 stories depend on 8 separate domain migrations being in scope | 🔴 Critical | PRODUCT-BE-F-01 through F-08 |
| `components` field resolver — 5 domain types unified with ACL mapping | 🔴 Critical | PRODUCT-BE-G-03 |
| `addProducts` bulk create — 4 external side-effects with no transaction rollback | 🟡 High | PRODUCT-BE-E-01 |
| `USE_NEW_RULES_API` feature flag — dual-path routing in DGS | 🟡 High | Phase F rules story |
| **`division` field resolver BUG in source** — calls `department` loader instead of `division` | 🟡 High | PRODUCT-BE-G-06 |
| Green-field: no existing DGS to validate naming against | 🟡 High | PRODUCT-BE-A-01, H04 |
| Aggregation facade becoming permanent if sub-story retirement is not actively governed | 🟡 High | PRODUCT-BE-F-09 |

---

## Decisions Required from PO / Architecture

| Decision | Due Before | Impact |
|----------|-----------|--------|
| Should `removeProductBusinessPartner` be exposed as a standalone mutation or remain internal to `productBusinessPartnerActions`? | Phase E kickoff | Schema design for M9 |
| What is the rollback strategy for `productBusinessPartnerActions` DROP_UNDROP partial failures? | Phase E kickoff | Saga vs best-effort |
| Is the `division` resolver bug already reported? Should it be fixed in the source before/during migration? | Phase D kickoff | Avoids dual-tracking |
| Should `USE_NEW_RULES_API` be ON or OFF by default in `plm-product`? | Phase F kickoff | RuleLibrary team coordination |
| Does the Hive Gateway supergraph support federation v2.3? | Phase H kickoff | Stitching approach for VMM/IG |
| Confirm TechPack migration option (B/C/D). Option D (facade now, federate per-subgraph) is recommended. See `reference/techpack-migration-options.md`. | Phase E kickoff | PRODUCT-BE-E-02 story design; blocks 8 downstream sub-stories |
| Which 8 domain teams own the per-subgraph CAT-4 stories (Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist)? Each needs a migration sprint. | Phase F planning | PRODUCT-BE-F-01–F-08 |

---

## Dependency Map

```
plm-product depends on:
  spark-product backend (primary REST API)
  elastic search cluster (product search index)
  spark-attachment (bulk update, archive, relationship-linked fetches)
  spark-relationship (resource tree traversal)
  spark-access-control (ACL JWT, permission maps, drop/undrop)
  spark-sample-v2 (drop/undrop, hydrate samples)
  stgapi-internal/VMM (business partner + brand data)
  stgapi-internal/IG (department / division / class data)
  stgapi-internal/APEX (reserved DPCI data)
  stgapi-internal/Corona (TCIN item details)
  Bazaarvoice (product ratings)
  spark-user-profile (createdBy/updatedBy, recently-viewed, todos, favorites, teams)
  spark-workspace-v2 (workspace membership)
  spark-tag (tags field)
  spark-claim (component status updates)
  spark-rule-library (feature-flagged rules routing)
```

---

## Recommended Sprint Sequencing

| Sprint | Phases | Focus |
|--------|--------|-------|
| S1 | A | Foundation, schema, DTOs, service skeleton; includes `ResourcesCount` @key schema (E-01) |
| S2 | B, D1–D3 | Core queries + simple mutations |
| S3 | C, D4 | Search queries + remaining mutations |
| S4 | E1–E3 | Partner management (non-complex) |
| S5 | E4 | `productBusinessPartnerActions` (complex orchestration) |
| S6 | E-TechPack | TechPack stub resolver + aggregation facade (E-02, E-03) — delivers working `getProductTechPackCountV1` on Day 1 via Option D Phase 1 |
| S7 | F-Rules | `USE_NEW_RULES_API` routing + remaining federation config |
| S8 | G1–G4 | Complex field resolvers: `attachmentsWithMetaData`, `attachmentsV3`, `components`, `reservedDpcis` |
| S9 | G5–G6, H | Remaining field resolvers + federation stitching |
| S-10 | I | Full test coverage pass |
| Ongoing | F-01–F-09 | Per-subgraph TechPack CAT-4 stories — each unblocked when owning domain migrates. Retire aggregation facade (F-09) when all 8 are done. |

---

## Capacity Planning

| Team Size | Estimated Calendar Time | Notes |
|-----------|------------------------|-------|
| 1 engineer | 35–51 sprints (5d/sprint) | Sequential; no parallelism |
| 2 engineers | 18–26 sprints | Phases B/C, D/E, G/H parallelizable |
| 3 engineers | 13–18 sprints | Phase A serializes all; G is the critical path |

> Phases A and I are not parallelizable (A is foundation; I is parity testing). All other phases have parallel opportunities. The critical path runs through Phase G (Complex Field Resolvers).

---

*Generated by spark-migration pipeline v1.1 — Phase 4 complete. All 6 artifacts ready.*
