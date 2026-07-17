# 07 · Story Validation, Dependency Matrix Delta & Roadmap Update

> Phase 7 of the federation review · 2026-07-17
> All 206 BE stories (8 × `be-04-stories.md`) and 39 FE stories (`fe-08-frontend-stories.md`) were re-checked against the proposed schema.

## 1. Story disposition summary

| Disposition | Count | Stories |
|---|---|---|
| Still applies, unchanged | 236 | everything not listed below |
| Needs modification (ACs added) | 4 | PRODUCT-BE-F-10 (composition CI gate + alignment ACs) · CLAIM-BE-F-01/F-02 (depend on R3 alignment) · CLAIM-BE-G-03 (E2E depends on PRODUCT-BE-F-13) |
| New — required | 3 BE + 1 FE | PRODUCT-BE-F-13 · PRODUCT-BE-F-14 · CLAIM-BE-G-06 · PRODUCT-FE-012 |
| New — recommended (PO-gated) | 5 BE + 1 FE | BOM-BE-G-17 · IMPRESSION-BE-G-04 · WATCHLIST-BE-G-05 · MST-BE-G-04 · PRODUCT-BE-G-17 · BOM-FE-007 |
| Should be split | 0 | — |
| Can be removed | 0 | — (the 3 product schema-drift wrapper mutations are already ⏭-gated, not stories) |
| Reordered | 0 | new stories slot into existing phase lanes; no existing order changes |

Every new story carries the standard metadata block (Type / Phase / Complexity / Depends on / EXT) parsed by `generate_jira.py`; Domain, Team, Implementation Order, Parallelizable and Owner lanes are derived by the generator as for all existing stories.

## 2. Dependency matrix — delta rows

| Story | Depends on | Blocks | Parallelizable | Domain | Team |
|---|---|---|---|---|---|
| PRODUCT-BE-F-13 | PRODUCT-BE-B-01 (service path) | PRODUCT-BE-F-10 · CLAIM-BE-G-03 (E2E) | Yes (BE-1 lane) | product | BE |
| PRODUCT-BE-F-14 | — (schema edits applied; verification work) | PRODUCT-BE-F-10 · CLAIM-BE-F-01 · CLAIM-BE-F-02 | Yes | product | BE |
| CLAIM-BE-G-06 | CLAIM-BE-B-01 | CLAIM-BE-G-01 · CLAIM-BE-G-03 (correctness) | Yes (claims lane) | claims | BE |
| PRODUCT-FE-012 | PRODUCT-BE-F-14 | claims/packaging/productDetails FE cutovers (CLAIM-FE-002, PKG-FE-001, PDTL-FE-001) | Yes | product | FE |
| BOM-BE-G-17 | BOM-BE-G-01 · PO approval (OQ-3/OQ-5) | BOM-FE-007 | Yes | bom | BE |
| IMPRESSION-BE-G-04 | IMPRESSION-BE-B-01 · PO approval | — | Yes | impression | BE |
| WATCHLIST-BE-G-05 | WATCHLIST-BE-G-02 · PO approval | — | Yes | watchlist | BE |
| MST-BE-G-04 | MST-BE-B-05 · PO approval | — | Yes | measurement | BE |
| PRODUCT-BE-G-17 | PRODUCT-BE-G-01 · PO approval | — | Yes | product | BE |
| BOM-FE-007 | BOM-BE-G-17 · BOM-FE-002 | — | Yes | bom | FE |

## 3. Domain implementation roadmap — what changes

- **Wave order is unchanged** (per [01-implementation-plan-2BE-2FE.md](../program/01-implementation-plan-2BE-2FE.md) and [02-project-plan.md](../program/02-project-plan.md)).
- **Insertions:**
  - PRODUCT-BE-F-14 lands **before** PRODUCT-BE-F-10 (composition) — earliest free BE-1 slot in the product Phase-F window; it is small (schema verification + wrapper declarations) and unblocks the claims lane.
  - PRODUCT-BE-F-13 lands in the same window, before the claims FE cutover (CLAIM-FE-002 is the first cross-subgraph cutover and needs `Claims.product` to hydrate).
  - CLAIM-BE-G-06 folds into the existing claims Phase-G window (same sprint as G-01).
  - PRODUCT-FE-012 runs as a gate immediately before CLAIM-FE-002 / PKG-FE-001 / PDTL-FE-001.
  - The 5 recommended BE stories + BOM-FE-007 form a **post-cutover enhancement mini-wave** at the tail of each domain's lane, contingent on PO approval — they never block a cutover.
- **Critical path impact:** +0 days if F-13/F-14 are worked in parallel with the existing product Phase-F stories (both fit the BE-1/BE-2 split); worst case +3–4 days on the claims cutover if serialized.

## 4. Artifact synchronization

- Sources updated: 8 × `be-04-stories.md` deltas (product, claims, bom, impression, watchlist, measurement) · `fe-08-frontend-stories.md` (+2) · 2 × `be-03-schema.graphql` (product, claims).
- Regenerated from sources: `output/jira/*.csv` (per-domain + all-stories + all-frontend-stories) · program fe-derivative docs (fe-00…04, fe-09…11, per-domain `fe-*-breakdown.md`).
- Not touched (generated, would be overwritten): `output/summary/*`, `output/confluence/*`, `.docx` plans.
