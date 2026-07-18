# Cross-Domain Association — Story Breakdown

> **Decision:** [ADR-011 (draft)](./01-adr-cross-domain-association.md) — synchronous orchestration + a
> shared internal `associate(...)` component (Option B).
> **Status:** 🟠 Draft proposed — ratification pending (`SPIKE-06b`; `SPIKE-06a` hydration concludes via
> `PRODUCT-BE-S-02`, separately).
> **This file lists which concrete stories implement the decision — full story text lives in
> `output/analysis/product/be-04-stories.md`, linked below.**

## Gated mutations — route through the shared `associate(...)` component

| Story | What it builds | Pin-downs already reflected in its AC |
|---|---|---|
| [`PRODUCT-BE-D-01`](../../analysis/product/be-04-stories.md#product-be-d-01-addproduct) | `addProduct` — workspace link via the shared component | routing made explicit in AC |
| [`PRODUCT-BE-D-02`](../../analysis/product/be-04-stories.md#product-be-d-02-addproducts-bulk) | `addProducts` (bulk) — workspace link + attachment-metadata + relationship-graph calls via the component | pin-down 1 (await `bulkUpdateResource`), pin-down 3 (replace the `bulkUpdateAttachmentsV2` cross-resolver import with an attachment-service client call, carrying Mid-Request ACL Update per ADR-019) |
| [`PRODUCT-BE-D-04`](../../analysis/product/be-04-stories.md#product-be-d-04-updateproduct) | `updateProduct` — template-attachment archiving via the shared component | routing made explicit in AC |

## Excluded from the component — plain mutations, no fan-out

| Story | Why excluded |
|---|---|
| `PRODUCT-BE-D-03` (`bulkUpdateProducts`) | pure passthrough, no cross-domain call |
| [`PRODUCT-BE-D-06`](../../analysis/product/be-04-stories.md#product-be-d-06-addteamstoproduct-collab-canvas) | single-backend write; already cites pin-down 4 (typed `DgsException` instead of `return new Error(...)`) verbatim |
| [`PRODUCT-BE-D-07`](../../analysis/product/be-04-stories.md#product-be-d-07-addbusinesspartnerstoproductwithtype-collab-canvas) | single-backend write; already cites pin-down 4 verbatim |
| `PRODUCT-BE-D-11` (`updateWorkspaceAttributes`) | single-backend write |

## Not yet built — the shared component itself

No story in `output/analysis/product/be-04-stories.md` builds `associate(sourceRef, targetDomain, targetRef,
props)` as its own deliverable today; D-01/D-02/D-04 each reference routing through it but the component's
own construction (the internal module, its Mid-Request ACL Update wiring for the 5 downstream-token calls it
wraps, its declared per-mutation failure-policy parameter) is implicitly bundled into whichever consumer
story lands first. **Flagged as a gap** — if a dedicated build story is wanted, it should land in
`output/analysis/product/be-04-stories.md` as a Phase-D or Phase-A infrastructure story analogous to
`PRODUCT-BE-E-00` (the `WriteSaga` module), landing before D-01/D-02/D-04. Not authored in this pass — see
the program backlog doc.

## Relationship to ADR-013 (WriteSaga)

D-02's pin-down 2 (accept non-atomic + document, defer compensation) explicitly defers to `SPIKE-01`
(ADR-013) — now `PRODUCT-BE-E-00`, the shared `WriteSaga` module. D-01/D-02/D-04 do not currently declare
`PRODUCT-BE-E-00` as a dependency in their own `Depends on:` line (unlike the E-phase multi-step writes,
these D-phase mutations may not need full saga machinery — a lighter compensating call may suffice per the
component's own declared policy). Not changed in this pass; flagged for review when the shared component is
actually built.

---
*Story ids and links regenerate from `output/analysis/product/be-04-stories.md` — this index is
hand-maintained alongside the ADR.*
