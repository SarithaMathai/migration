# Non-Atomic Write Saga (`WriteSaga`) — Story Breakdown

> **Decision:** [ADR-013 (draft)](./01-adr-non-atomic-write-saga.md) — one shared `WriteSaga` module,
> per-step declared policy (Option B).
> **Status:** 🟠 Draft proposed — ratification pending (`SPIKE-01`, Sprint-0 critical path).
> **This file lists which concrete stories implement the decision — full story text lives in each domain's
> `be-04-stories.md`, linked below.**

## The shared module (build once, blocks every consumer below)

| Story | Domain | What it builds |
|---|---|---|
| [`PRODUCT-BE-E-00`](../../analysis/product/be-04-stories.md#product-be-e-00-writesaga-shared-module-sprint-0-critical-path) | product | the `WriteSaga` module itself — ordered steps, per-step policy (`COMPENSATE`/`RETRY`/`RECORD`), the default policy table, the compensation inventory (pin-down 1) |

## Pilot adoption

| Story | Domain | Steps |
|---|---|---|
| [`MST-BE-E-01`](../../analysis/measurement/be-04-stories.md#mst-be-e-01-updatemeasurement-2-step-orchestrated-write) | measurement | workspace assoc `COMPENSATE` → body PUT = point of no return — the smallest real case, designated pilot per ADR-013 §5 build order |

## Remaining consumers (adopt story-by-story once the pilot proves the API)

| Story | Domain | Steps | Pin-downs closed |
|---|---|---|---|
| [`BOM-BE-E-01`](../../analysis/bom/be-04-stories.md#bom-be-e-01-updatebom-3-step-orchestrated-write) | bom | workspace assoc `COMPENSATE` → body PUT → permissions `RETRY` then `PARTIAL_FAILURE` | pin-down 5 (unchecked permissions response now checked) |
| [`PKG-BE-E-01`](../../analysis/packaging/be-04-stories.md#pkg-be-e-01-updatepackaging-multi-step-write) | packaging | body PUT (checked before side-effects) → attachment archive/attrs `RECORD` → relationship add/remove `COMPENSATE` | pin-down 3 (late validation-check bug fixed) |
| [`PDTL-BE-E-01`](../../analysis/productDetails/be-04-stories.md#pdtl-be-e-01-updateproductdetailsset-multi-step-write) | productDetails | workspace assoc `COMPENSATE` → attachment archive `RECORD` (order preserved) → body PUT checked | pin-down 5 (unchecked body response now checked); copy-paste error text fixed |
| [`WATCHLIST-BE-E-01`](../../analysis/watchlist/be-04-stories.md#watchlist-be-e-01-updatewatchlistentries-multi-step-write) | watchlist | user-group map awaited + ordered before body → body PUT → attachment archive `RECORD` | pin-down 2 (unawaited map race fixed) |
| [`CLAIM-BE-E-01`](../../analysis/claims/be-04-stories.md#claim-be-e-01-updateclaim-proxy-acl-multi-step-write) | claims | proxy-ACL context → workspace assoc `COMPENSATE` → body PUT | pin-down 5 (unchecked workspace-association response now checked) |
| [`PRODUCT-BE-E-02`](../../analysis/product/be-04-stories.md#product-be-e-02-updatecomponentstatuses-5-loader-fan-out) | product | 5-domain parallel fan-out, isolated per branch, aggregated result | pin-down 4 (duplicated `claimIds` DTO bug fixed, void return replaced), pin-down 7 (parallel fan-out kept, isolated) |

## Later phase

| Story | Status |
|---|---|
| `SAMPLE-BE-E-01`/`E-02` | named in the ADR header as later-phase home stubs; adopt the same module + policy table unchanged when the sample domain migrates (pin-down 8 — no new decision) |

## Superseded

`BOM-BE-S-01` (`updateBom` failure-strategy spike) predates this ADR and asked the same three questions
this ADR answers at the program level. Not deleted — flagged in its own body as superseded, kept as the
historical record. See the program backlog doc for the spike-closure housekeeping decision.

---
*Story ids and links regenerate from each domain's `be-04-stories.md` — this index is hand-maintained
alongside the ADR.*
