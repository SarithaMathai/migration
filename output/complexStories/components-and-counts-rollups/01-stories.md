# Components + Counts Rollups — Story Breakdown

> **Decision:** [ADR-014 (draft)](./01-adr-components-counts-rollups.md) — owner-computed rollup (lift-and-shift,
> formalized) with four named fixes (Option A).
> **Status:** 🟠 Draft proposed — ratification pending.
> **This file lists which concrete stories implement the decision — full story text lives in each domain's
> `be-04-stories.md`, linked below.**

## Product-side (phase 1)

| Story | What it builds | Pin-downs closed |
|---|---|---|
| [`PRODUCT-BE-G-02`](../../analysis/product/be-04-stories.md#product-be-g-02-productcomponents) | `Product.components` — N+1→batched ACL fix, `type 2 → packagingBom` tagging, no `info.variableValues` coupling | pin-down 1 (batched ACL), pin-down 2 (missing-ACL throw preserved), pin-down 4 (sample→discussion **+1** rollup quirk preserved), pin-down 5 (explicit field args + contract test), pin-down 6 (`type 2 → packagingBom`), pin-down 7 (packaging query joins the parallel group) |

`PRODUCT-BE-G-02`'s own body notes pin-downs 3 (`counts` scalar-`0`→zeros-object) and 8 (`WorkspaceV2.products`
include-flags delegation) belong to the workspace-side twin, not here.

## Workspace-side (later phase — not yet written)

| Story | Status |
|---|---|
| `WORKSPACE-BE-G-02` | named in the ADR as the `WorkspaceV2.counts` twin; not yet written — owes pin-down 3 (zeros-object fix) and the sequential-reads parallelization when authored |
| `WORKSPACE-BE-G-04` | named in the ADR for `WorkspaceV2.products`; not yet written — owes pin-down 8 (keep the include-flags hydration short-circuit) when authored |

## Relationship to ADR-017 (polymorphic-type-resolution)

Pin-down 6 (`type 2 → packagingBom`) is recorded once in `BOM-BE-A-05`'s shared `code → type` registry
(`SPIKE-05`) — `PRODUCT-BE-G-02`'s own AC cites the rule independently since it's exercised inside the
`Product` domain's rollup logic, not bom's dispatch tables. No duplicate decision.

---
*Story ids and links regenerate from each domain's `be-04-stories.md` — this index is hand-maintained
alongside the ADR.*
