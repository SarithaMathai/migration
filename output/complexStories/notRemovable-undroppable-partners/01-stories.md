# Not-Removable / Undroppable Partners — Story Breakdown

> **Decision:** [ADR-016 (draft)](./01-adr-notremovable-undroppable-partners.md) — owner-computed union over
> direct service calls (phase 1), per-domain lanes at federation (Option B).
> **Status:** 🟠 Draft proposed — ratification pending (`SPIKE-04`).
> **This file lists which concrete stories implement the decision — full story text lives in
> `output/analysis/product/be-04-stories.md`, linked below.**

## Product-side (phase 1)

| Story | What it builds | Pin-downs closed |
|---|---|---|
| [`PRODUCT-BE-G-11-1`](../../analysis/product/be-04-stories.md#product-be-g-11-1-productnotremovablepartnerids-notremovableworkspaceids) | `notRemovablePartnerIds`/`notRemovableWorkspaceIds` — reflective resolver invocation replaced with direct scoped-lane calls | pin-down 1 (reflection removal), pin-down 2 (samples-lane `variableValues` blocker, contract-checked before cutover), pin-down 3 (parallelize 5 source fetches), pin-down 4 (parallelize ACL chunk loop), pin-down 8 (watchlist first-workspace-only scope preserved), pin-down 9 (Relationship-Service walk quarantined inside `unDroppablePartners`'s enumeration client), pin-down 10 (schema-diff gate on lane visibility) |
| [`PRODUCT-BE-G-07`](../../analysis/product/be-04-stories.md#product-be-g-07-productvendorattributes-businesspartners-droppedpartners-undroppablepartners-status) | `unDroppablePartners` semantics | pin-down 5 (`isDesignPartner`-only gate preserved), pin-down 6 (dps whole-resource exclusion preserved), pin-down 7 (`.filter(Number)` numeric-grantee semantics preserved) |

## Workspace-side (later phase — not yet written)

| Story | Status |
|---|---|
| `WORKSPACE-BE-G-05` | named in the ADR as the twin; not yet written — inherits the same 10-pin-down contract unchanged when authored |

## Relationship to ADR-018 / ADR-014 (the 6 cross-resolver invocations this case removes)

The aggregator previously called into `discussionsV2`, `attachmentsV3` (the full ADR-018 pipeline),
`components` (the full ADR-014 pipeline), and `samples` cross-resolver — all 6 are replaced by scoped lane
client calls per pin-down 1; ADR-014/ADR-018's own pipelines are no longer dependencies of these fields
(confirmed in `PRODUCT-BE-G-11-1`'s AC-2).

---
*Story ids and links regenerate from `output/analysis/product/be-04-stories.md` — this index is
hand-maintained alongside the ADR.*
