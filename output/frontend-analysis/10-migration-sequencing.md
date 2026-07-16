# Frontend Migration Sequencing Plan — Phase-1 Domains

> Hand-authored deliverable · 2026-07-16
> Inputs: [08-frontend-stories.md](./08-frontend-stories.md), [09-story-dependency-matrix.md](./09-story-dependency-matrix.md)
> Backend sequencing reference: `output/summary/00-program-overview.md`

## 1. Sequencing principles

- Platform stories land first — every domain cutover reuses the flag, codegen, cache and fragment work.
- Cut over the smallest isolated domain first to validate the platform stack in production before high-risk domains move.
- A domain's frontend cutover follows its backend phase-B/C delivery; complex writes follow their ADR ratification.
- Cross-domain documents migrate with the **later** of their two domains — no interim document splits unless a wave gap forces one.
- Dual-run (flag off/on comparison) precedes every domain's flag flip.

## 2. Waves

### Wave 0 — Platform enablement (parallel with backend phase B)

- PLATFORM-FE-001 (router flag) → PLATFORM-FE-002 (codegen) → PLATFORM-FE-003 (cache) — sequential.
- PLATFORM-FE-004 (fragment sweep) and PLATFORM-FE-005 (dynamic-gql expansion) — parallel once 002 lands; 005 has no upstream dependency and can start immediately.
- Exit criterion: a pilot document validates, builds and dual-runs end-to-end.

### Wave 1 — Pilot: Watchlist 🟢

- WATCHLIST-FE-001 → WATCHLIST-FE-002 → WATCHLIST-FE-003 (003 gated on ADR-013 ratification).
- Smallest isolated surface (5 operations, 1 library, 4 components) — proves entity caching, flag flip and rollback.
- Exit criterion: watchlist runs on the router in production for one full sprint without regression.

### Wave 2 — Low/medium isolated domains

- Product Details: PDTL-FE-001 → PDTL-FE-002 → PDTL-FE-003.
- Measurement: MST-FE-003 → MST-FE-001 → MST-FE-004 → MST-FE-002 (002 gated on search cutover).
- Packaging: PKG-FE-002 → PKG-FE-001 → PKG-FE-003 → PKG-FE-004 → PKG-FE-005.
- These three domains are parallelizable across engineers; no shared blocking dependencies between them.

### Wave 3 — High-complexity domains

- BOM: BOM-FE-001 (early, no gate) → BOM-FE-004 → BOM-FE-005 → BOM-FE-002 → BOM-FE-003 (search gate) → BOM-FE-006 (ADR-013 gate).
- Claims: CLAIM-FE-001 (early) → CLAIM-FE-002 (first cross-subgraph cutover — schedule when `spark-claims` subgraph is stable) → CLAIM-FE-003 → CLAIM-FE-004.

### Wave 4 — Product (largest surface, incremental)

- Independent slices first: PRODUCT-FE-006 (rules admin) and PRODUCT-FE-005 (templates) — low coupling, early wins.
- Core reads: PRODUCT-FE-001 → PRODUCT-FE-002 → PRODUCT-FE-004.
- Lists/search: PRODUCT-FE-003 (search gate, aligns with BOM-FE-003 / MST-FE-002).
- Writes: PRODUCT-FE-007 → PRODUCT-FE-008 → PRODUCT-FE-011 (ADR-014 gate) → PRODUCT-FE-009 (ADR-012/016 gate).
- Staged: PRODUCT-FE-010 step 1 (facade) can ride with PRODUCT-FE-001; step 2 lands after counts federate.
- Impression riders: IMPRESSION-FE-001 flips with BOM-FE-002; IMPRESSION-FE-002 flips with PRODUCT-FE-001.

## 3. External gates

| Gate | Blocks | Status convention |
|---|---|---|
| Search / elastic read-hub decision (S-phase stories) | PRODUCT-FE-003, BOM-FE-003, MST-FE-002 | carried by the corresponding `*-BE-S-*` stories |
| ADR-012 partner drop/undrop + ADR-016 not-removable | PRODUCT-FE-009 | 🟠 draft — ratification pending |
| ADR-013 non-atomic write saga | BOM-FE-006, PKG-FE-005, PDTL-FE-003, WATCHLIST-FE-003, CLAIM-FE-004, MST-FE-004 (partial) | 🟠 draft — ratification pending |
| ADR-014 components & counts rollups | PRODUCT-FE-011 | 🟠 draft — ratification pending |
| ADR-015 TechPack facade-then-federate | PRODUCT-FE-010 step 2 | 🟠 draft — ratification pending |
| ADR-017 polymorphic type resolution | IMPRESSION-FE-001/002 (`possibleTypes`) | 🟠 draft — ratification pending |
| `spark-claims` subgraph production stability | CLAIM-FE-002 | first cross-subgraph cutover |

## 4. Effort summary

| Wave | Stories | Estimated effort |
|---|---|---|
| 0 — Platform | 5 | 20–32 days |
| 1 — Watchlist pilot | 3 | 7–10 days |
| 2 — PDTL + MST + PKG | 12 | 40–63 days |
| 3 — BOM + Claims | 10 | 44–69 days |
| 4 — Product + Impression | 13 | 66–102 days |
| **Total** | **43** | **177–276 days** (single-engineer days; waves 2–4 parallelize across domains) |

## 5. Rollback posture

- Every wave keeps the legacy path alive behind the flag until the exit criterion holds.
- Cache reset on every flag transition (both directions) — no mixed-typename cache state.
- Cross-domain documents are the only places where rollback granularity is coarser than one domain — their stories carry an explicit rollback note.
