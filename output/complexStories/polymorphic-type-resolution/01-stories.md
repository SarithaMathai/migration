# Polymorphic Type Resolution — Story Breakdown

> **Decision:** [ADR-017 (draft)](./01-adr-polymorphic-type-resolution.md) — per-site ports + one shared
> playbook + a CI conformance gate (Option B).
> **Status:** 🟠 Draft proposed — ratification pending (`SPIKE-05`).
> **This file lists which concrete stories implement the decision — full story text lives in
> `output/analysis/bom/be-04-stories.md`, linked below.**

## The shared playbook + gate (build once, referenced by every dispatch site)

| Story | Domain | What it builds |
|---|---|---|
| [`BOM-BE-A-05`](../../analysis/bom/be-04-stories.md#bom-be-a-05-shared-ci-conformance-gate-code-type-registry-spike-05) | bom | the shared conformance-check library (SDL↔enum↔golden-fixture, the 3 checks) + the `code → type` registry seeded from ADR-017 §1 and ADR-014 pin-down 6 |

## Bom's two dispatch sites (phase 1)

| Story | Dispatch site | Pin-downs closed |
|---|---|---|
| [`BOM-BE-A-04`](../../analysis/bom/be-04-stories.md#bom-be-a-04-dgstyperesolver-for-the-2-bom-interfaces) | `BomMaterialInterface` (7 impls) + `BomImpressionDetailsInterface` (5 impls) | pin-down 1 (backend-verify the tables), pin-down 2 (HUB/COMPONENT/OTHER default kept exact) |
| `BOM-BE-G-08`–`G-13` | per-variant field resolvers (trim/wash/fabric/fabricSpec/combination + impression variants) | not yet enriched with pin-down 9 (Mid-Request ACL Update inside the 6 downstream-token loaders — wash/fabric/search-targeting) — **flagged gap**, see program backlog doc |

## Out-of-scope sites (adopt the playbook in their own stories, no new decision)

| Site | Home story | Status |
|---|---|---|
| `SampleAsset` union | `SAMPLE-BE-A-04` (later phase) | not yet written; inherits pin-downs 3 (typed `DgsException` for the `null` path) and 6 (cross-resolver import removal) when authored |
| `SampleV2.parent*` prefix gates | `SAMPLE-BE-G-02` (later phase) | not yet written; inherits pin-down 4 (preserve the un-gated `trim` call-through, log non-trim prefixes) |
| Materials search (`HubMaterialInterface`, `BaseMaterialCommonFields`) | `SEARCH-BE-B-01`/`SEARCH-BE-C-02` (later phase) | not yet written; inherits pin-down 5 (preserve the exact string-typed dispatch) and Option D's federation-native end-state |
| Discussion `Resource` union | discussion domain (later phase) | not yet written; adopts the playbook, no bespoke design |
| Product `SPARK_Categories` (12-case union) | [`PRODUCT-BE-G-04`](../../analysis/product/be-04-stories.md#product-be-g-04-productscategoriescategories-12-case-dopplerdepartment-fields) | already exists as a dispatcher/field-resolver port; not yet cross-referenced to the shared gate — flagged gap |

## Relationship to ADR-014 (components-and-counts-rollups)

The `type 2 → packagingBom` tagging rule (ADR-014 pin-down 6) is recorded in `BOM-BE-A-05`'s registry, not
duplicated — `PRODUCT-BE-G-02`'s own AC cites it independently since the rule is exercised in the `Product`
domain's rollup, not in bom's dispatch tables.

---
*Story ids and links regenerate from `output/analysis/bom/be-04-stories.md` and `output/analysis/product/be-04-stories.md`
— this index is hand-maintained alongside the ADR.*
