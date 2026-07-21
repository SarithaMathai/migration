# 05 · Backend Impact Assessment

> Phase 5 of the federation review · 2026-07-17
> Method: the proposed schema (03) was compared story-by-story against the 8 domain `be-04-stories.md` inventories (206 BE stories).

## 1. Existing coverage — verdict per work category

| Work category | Covered today? | Where |
|---|---|---|
| Schema updates (owned types, stubs, directives) | ✅ | Per-domain Phase A/B skeleton stories (BOM-BE-A-04 etc.; product Phase A dissolved into the B-01 checklist) |
| Federation directives (`@key`/`@extends`/`@external`/`@shareable`) | ✅ | Baked into each schema + Phase A stories |
| Entity resolvers | ⚠ partial | `ResourcesCount` ✅ (product TechPack story), claims-side ✅ (CLAIM-BE-F-01/02) — **`Product` entity fetcher missing → new PRODUCT-BE-F-13** |
| Field resolver changes | ✅ | Phase G per domain (e.g. BOM G-01…G-16, CLAIM G-01…G-05) |
| Service layer / Kotlin ports | ✅ | Phase A/B foundation stories per domain |
| DataLoader changes | ✅ | e.g. BOM-BE-G-10 `MaterialDataLoader`; batching ACs in G stories |
| Query resolver migration | ✅ | Phase B/C — one story per query, all 63 phase-1 queries mapped |
| Mutation resolver migration | ✅ | Phase D/E — all 57 mutations mapped, sagas isolated in Phase E |
| Integration testing | ✅ | Per-domain G "tests + parity harness" stories |
| Federation/composition testing | ⚠ partial | PRODUCT-BE-F-10 composes the supergraph — **but had no CI gate and no contract-alignment AC → ACs added** |

## 2. Gaps found → new stories

### Required

| Story | Title | Order | Depends on | Blocks | Why |
|---|---|---|---|---|---|
| PRODUCT-BE-F-13 | `Product` `@DgsEntityFetcher` (cross-subgraph reference resolver) | with Phase F, before claims cutover | product Phase B foundation (`getProduct` service path) | CLAIM-BE-G-03 (E2E), PRODUCT-BE-F-10 | Only path for a separate subgraph to hydrate `Claims.product` via `_entities` |
| PRODUCT-BE-F-14 | Cross-subgraph contract alignment (R1–R4, R6 + undeclared paged wrappers) | before PRODUCT-BE-F-10 | — | PRODUCT-BE-F-10, CLAIM-BE-F-01/02 | Composition fails on key/name mismatches; see [03 §1](./03-proposed-schema-changes.md) |
| CLAIM-BE-G-06 | Shared value-type alignment (`@shareable` `ProductComponentStatus`/`ResourcePermissions`/`TeamPaged`) | with claims Phase G | CLAIM-BE-B-01 | CLAIM-BE-G-01/03 correctness | R5 — entity stubs can't carry locally-resolved data |
| PRODUCT-BE-F-10 (modified) | + ACs: CI composition gate; zero key/name mismatch check | unchanged | + PRODUCT-BE-F-13/F-14 | unchanged | Turns composition from a one-off into a regression gate |

### Recommended (PO-gated — do not schedule until OQ-3 & the REC list in 03 §2 are approved)

| Story | Title | Depends on | Notes |
|---|---|---|---|
| BOM-BE-G-17 | `BomMaterialInterface.supplier` entity ref (+7 impls) | BOM-BE-G-01, R1 | Snapshot-semantics answer (OQ-3) first |
| IMPRESSION-BE-G-04 | `Impression.attachment` entity ref | impression Phase B | Emits `@key` stub only — no resolver logic |
| WATCHLIST-BE-G-05 | `WatchlistPartner.partner` entity ref | WATCHLIST-BE-G-02 | Replaces nothing; `partnerName` stays |
| MST-BE-H-02 | `SampleMeasurementSet.sample` forward ref | MST-BE-B-05 | Pairs with MST-BE-H-01 |
| PRODUCT-BE-G-17 | Partner/lineage entity refs on product value types (REC-5/6) | PRODUCT-BE-G-01 | — |

## 3. Blocked-story map (delta only)

- CLAIM-BE-F-01, CLAIM-BE-F-02, CLAIM-BE-G-03 → now additionally blocked by **PRODUCT-BE-F-14** (and G-03's E2E by **PRODUCT-BE-F-13**).
- PRODUCT-BE-F-10 → now additionally blocked by **PRODUCT-BE-F-13 + F-14**.
- All 5 recommended stories → blocked by **PO approval** (tracked as OQ-5).
- No existing story becomes unblocked, obsolete, or resequenced by this review.

## 4. Effort delta

- Required: F-13 (M — entity fetcher + DataLoader + tests), F-14 (S — schema edits already applied; story is the verification + wrapper declarations), CLAIM-BE-G-06 (S).
- Recommended: 5 stories, S–M each; all parallelizable within their domain lanes after their G-phase prerequisites.
- Net: **+3 required stories (~1 sprint across BE-1/BE-2 lanes), +5 PO-gated stories**.
