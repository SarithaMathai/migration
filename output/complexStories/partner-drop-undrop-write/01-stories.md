# Partner Drop/Undrop + Ownership — Story Breakdown

> **Decision:** [ADR-012 (draft)](./01-adr-partner-drop-undrop.md) — owner-orchestrated saga (via the shared
> `WriteSaga` module, ADR-013) + a per-domain participant contract (Option B).
> **Status:** 🟠 Draft proposed — ratification pending (`SPIKE-03` — do this one first, blocks `E-01`).
> **This file lists which concrete stories implement the decision — full story text lives in
> `output/analysis/product/be-04-stories.md`, linked below.**

## Product-side (phase 1)

| Story | What it builds |
|---|---|
| [`PRODUCT-BE-S-03`](../../analysis/product/be-04-stories.md#product-be-s-03-productbusinesspartneractions-failure-strategy-spike-do-this-one-first) | the fan-out-shape-specific failure-strategy spike (which of `REMOVE`/`DROP`/`UNDROP` need which policy) |
| [`PRODUCT-BE-E-01`](../../analysis/product/be-04-stories.md#product-be-e-01-productbusinesspartneractions-removedropundrop) | `ProductBusinessPartnerActionService` — all 3 action paths, orchestrated via the shared `WriteSaga` module (`PRODUCT-BE-E-00`) over the per-domain participant contract; the ACL-ordering security invariant (drop/undrop) as an automated test |

`PRODUCT-BE-E-01` already cites this ADR's pin-downs 1, 2, 3, 5, 7 verbatim in its own Acceptance Criteria
(Relationship-Service traversal removed, `UserProfileAttributes` resolver import removed, per-step failure
policy, ACL-before-return ordering test, `PARTIAL_FAILURE` per-step detail). Pin-downs 4 (async-refinement
scope) and 6 (keep dispatcher shape) are recorded as a note in `E-01`'s body, not a testable AC — see that
story.

## Workspace-side (later phase — inherits the contract, no second design round)

| Story | Status |
|---|---|
| `WORKSPACE-BE-E-01` | named as home stub in the ADR header; not yet written — net-new when the workspace domain's phase starts, reusing `PRODUCT-BE-E-01`'s participant contract and `PRODUCT-BE-E-00`'s `WriteSaga` module unchanged |

## Dependency on ADR-013 (WriteSaga)

`PRODUCT-BE-E-01`'s `Depends on:` line already lists `S-03, E-00` — the shared `WriteSaga` module built in
`PRODUCT-BE-E-00` is a hard prerequisite, consistent with ADR-013 §6 ("ADR-012's partner actions get their
saga for free (same module)").

## ACL

Per-domain participant call sites reviewed against ADR-019: only the sample-domain call
(`sampleV2.dropSamples`/`unDropSamples` inside `DROP_UNDROP_PARTNER`) is downstream-token and carries
Mid-Request ACL Update; the batched permission-filter read and the bulk ACL drop/undrop calls are
permission-check / own-domain-token and stay resolver-local — see `01-adr-partner-drop-undrop.md`'s own ACL
note.

---
*Story ids and links regenerate from `output/analysis/product/be-04-stories.md` — this index is
hand-maintained alongside the ADR.*
