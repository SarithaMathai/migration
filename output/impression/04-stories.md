# Impression — Migration Plan & Stories

> **Domain:** `impression` · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18
> **Target:** TBD per PO decision (`plm-impression` stand-alone vs co-located in `plm-product`)
> **Depends on:** [02-resolver-analysis.md](output/impression/02-resolver-analysis.md), [02-resolver-analysis-mutations.md](output/impression/02-resolver-analysis-mutations.md), [02-resolver-analysis-fields.md](output/impression/02-resolver-analysis-fields.md), [02-resolver-analysis-services.md](output/impression/02-resolver-analysis-services.md), [03-schema.graphql](output/impression/03-schema.graphql), [03-schema-analysis.md](output/impression/03-schema-analysis.md)

---

## 1. Phases Overview

| Phase | Stories | Effort (raw d) | +20% buffer |
|---|---|---|---|
| A | Foundation & Schema (assumes co-location in plm-product; subtract A-skeleton effort if stand-alone) | 2 | 2–3 | 3–4 |
| B | Queries | 2 | 2–4 | 3–5 |
| D | Mutation | 1 | 1–2 | 2–3 |
| G | Field resolvers | 2 | 2–4 | 3–5 |
| F | Federation: Product entity extension | 1 | 2–3 | 3–4 |
| H | Schema restructure + bug fixes | 2 | 3–5 | 4–6 |
| I | Test coverage | 2 | 3–5 | 4–6 |
| **Total** | **12** | **15–26** | **22–33** |

---

## 2. Stories

### Phase A — Foundation

**SPARK-IMP-A01 · CAT-1 · Small (1d)** — Add `Impression`, `ImpressionCountResult`, `PartnerImpressionCount`, deprecated `ImpressionCount`, `CountsByBp` `@shareable`, 2 input types, external stubs (`VMM_BusinessPartner`, `Product`, `WorkspaceV2`, `UserProfileAttributes`) to schema per [03-schema.graphql](output/impression/03-schema.graphql).

**SPARK-IMP-A02 · CAT-3 · Small (1–2d)** — `ImpressionService` Kotlin port (2 methods). Replace manual query-string assembly with Feign `@QueryParam(...) List<ID>`. **Honor `enableWorkspaceContextFiltering`** in service signature (fix Phase 2A 🔴 finding).

### Phase B — Queries

**SPARK-IMP-B01 · CAT-2 · Small (1–2d)** — `searchImpressionsByProductId` data fetcher. Plumb `enableWorkspaceContextFiltering`.

**SPARK-IMP-B02 · CAT-2 · Small (1–2d)** — `getImpressionCountsByProductId`. Returns properly-typed `ImpressionCountResult` per H01 restructure.

### Phase D — Mutation

**SPARK-IMP-D01 · CAT-2 · Small (1–2d)** — `updateImpressions`. Typed `ValidationException` replaces shape-sniff.

### Phase G — Field Resolvers

**SPARK-IMP-G01 · CAT-2 · Small (1–2d)** — `Impression` 5 fields (businessPartners, owningBusinessPartner, workspaces, createdBy, updatedBy). All become federation entity stubs.

**SPARK-IMP-G02 · CAT-2 · Small (1–2d)** — `ImpressionCountResult` count fields (totalCount + countsByPartner). Pure projection from internal carrier — no I/O.

### Phase F — Federation

**SPARK-IMP-F01 · CAT-4 · Small (1–2d) · BLOCKED-BY product domain Phase 3** — Contribute `impressions(partnerIds, workspaceIds)` and `impressionCounts` fields to `Product` entity per [03-schema-analysis.md §4](output/impression/03-schema-analysis.md).

### Phase H — Schema Restructure + Bug Fixes

**SPARK-IMP-H01 · CAT-1 + CAT-2 · Small (1–2d)** — `ImpressionCount` → `ImpressionCountResult` restructure (per [03-schema-analysis.md §3](output/impression/03-schema-analysis.md)). Keep old shape `@deprecated` for one release. Add `productId` carrier so internal `counts` resolver doesn't depend on `impressions[0].parentId`.

**SPARK-IMP-H02 · CAT-3 · Small (1d)** — Fix latent bugs: empty-array guard on count resolver; replace silent dummy-counts error with structured exception + null propagation; honor `enableWorkspaceContextFiltering`.

### Phase I — Tests

**SPARK-IMP-I01 · CAT-5 · Small (1–2d)** — Unit + integration tests (≥ 80% coverage).

**SPARK-IMP-I02 · CAT-5 · Small (1–2d)** — Parity fixture set (~10 fixtures: empty impressions, multi-partner, workspace filter on/off, validation error path).

---

## 3. Risk Register

| # | Risk | Severity | Story |
|---|---|---|---|
| 1 | `enableWorkspaceContextFiltering` arg silently dropped (latent bug) | 🔴 | A02, B01, H02 |
| 2 | `ImpressionCount` schema-shape mismatch — client-visible restructure | 🔴 | H01 |
| 3 | Co-location decision (stand-alone DGS vs fold into plm-product) | 🟡 | A01 |
| 4 | Empty-array TypeError masked by try/catch | 🟡 | H02 |
| 5 | `bpType` string-vs-ID type mix | 🟡 | H01 |
| 6 | Silent error → dummy counts (observability gap) | 🟡 | H02 |
| 7 | F01 BLOCKED-BY product domain Phase 3 | 🟡 | F01 |
| 8 | `enableWorkspaceContextFiltering` semantic — what should backend do? Confirm | 🔴 | A02 |

---

## 4. Summary

- **Total stories:** 12
- **Total effort:** 22–33 days (+20% buffer) ≈ **4–7 sprints** for one engineer
- **Critical path:** A → A02 → H01/H02 → B/D/G → F01
- **Tiny domain** — fully migratable by a single engineer in ~1 month including all bug fixes and schema restructure
- **3 🔴 risks** all stem from latent bugs in source; all fixable during port

---

**Phase Completed:** Phase 4 — Migration Story Generation
**Outputs:** [04-stories.md](output/impression/04-stories.md), [04-po-summary.md](output/impression/04-po-summary.md)
