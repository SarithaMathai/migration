# Complex Story — Non-atomic multi-step writes (the saga / compensation pattern)

> **Summary —** Make every multi-step “save” recover cleanly when a middle step fails — using one shared saga/compensation framework instead of nine hand-rolled guesses.
> **Spike:** `SPIKE-01` · **Status:** 🟠 Draft ADR-013 proposed — ratification pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** bom, measurement, packaging, productDetails, watchlist, claims, sample, product
> **Stub stories:** `BOM-BE-E-01`, `MST-BE-E-01`, `PKG-BE-E-01`, `PDTL-BE-E-01`, `WATCHLIST-BE-E-01`, `CLAIM-BE-E-01`, `SAMPLE-BE-E-01/E-02` (later phase), `PRODUCT-BE-E-02`

> **Migrates (source resolvers → this case):** nine multi-step mutations — `updateBom` (`BOM-BE-E-01`),
> `updateMeasurement` (`MST-BE-E-01`), `updatePackaging` (`PKG-BE-E-01`), `updateProductDetailsSet`
> (`PDTL-BE-E-01`), `updateWatchlistEntries` (`WATCHLIST-BE-E-01`), `updateClaim` (`CLAIM-BE-E-01`), `updateSamplesV2`
> (`SAMPLE-BE-E-01` (later phase)), `bulkEvaluateSamples` (`SAMPLE-BE-E-02` (later phase)), `updateComponentStatuses` (`PRODUCT-BE-E-02`/M20).

## 1. The problem (it recurs in 8+ places)

### 1.1 Problem statement

- Across the program, **every "update" mutation is a multi-step, non-atomic, no-rollback write** spanning
  two or more REST services with no transaction boundary.
- They all share the same failure mode: an early step commits, a later step fails, and the resource is left
  inconsistent — and nothing detects it.

### 1.2 Current state & root cause

**Root cause.** The steps of each "save" span **different backends** (workspace association, resource body,
permissions, attachments, relationship links), so no single database transaction can cover them; the legacy
gateway simply sequenced the calls and hoped, and each of the nine mutations hand-rolled its own ordering —
four never check a response, one never awaits a write.

| Mutation | What the user is doing | Steps (legacy) | Risk |
|---|---|---|---|
| `updateBom` (`BOM-E-01`) | Saving a bill of materials: move it between workspaces, save its content, update which partners may see it | workspace assoc **(commits first)** → body PUT → permissions PUT | step-2 persists if step-3 fails; ACL left stale |
| `updateMeasurement` (`MEAS-E-01`) | Saving a measurement set: move it between workspaces, then save its content | workspace assoc **(commits first)** → body PUT | 2-step, no rollback |
| `updatePackaging` (`PKG-E-01`) | Saving packaging details and adding/removing its attachments | body → attachment add/remove | partial attachment state |
| `updateProductDetailsSet` (`PDTL-E-01`) | Saving a set of product-detail records in one action | multi-step set update | partial set |
| `updateWatchlistEntries` (`WL-E-01`) | Updating a watchlist's entries, the user groups who follow it, and archiving attachments removed from it | **un-awaited user-group add/update** (latent bug) → entries → archive removed attachments | race + partial |
| `updateClaim` (`CLM-E-01`) | Saving a claim: update access on the partner's behalf, its workspace, and its content | proxy ACL → workspace → body | proxy-ACL/body divergence |
| `updateSamplesV2` (`SMPL-E-01`) | Saving a sample together with its evaluation results | sample body + evaluation | partial evaluation |
| `bulkEvaluateSamples` (`SMPL-E-02`) | Recording evaluations for many samples at once and opening new review rounds | evaluation + new-rounds util (bulk) | partial bulk |
| `updateComponentStatuses` (`PROD-E-02`) | Setting a status across all of a product's components (BOMs, measurements, details, packaging, claims) | 5-loader fan-out (+ shadow-var bug) | partial status fan-out |

> Step sequences above are taken from each domain's `be-02-resolver-analysis.md` code deep-dive (e.g.
> [bom M2](../../analysis/bom/be-02-resolver-analysis.md), [measurement M3](../../analysis/measurement/be-02-resolver-analysis.md),
> [watchlist M2](../../analysis/watchlist/be-02-resolver-analysis.md), [product M20](../../analysis/product/be-02-resolver-analysis.md));
> the descriptions summarize the same source.

- The program already lists *"Non-atomic write failure strategy (saga / compensation / best-effort)"* as a cross-domain decision.
- **This case turns that decision into one shared mechanism** so each write isn't a bespoke guess.

### 1.3 Impact if not addressed

- **Data integrity** — a resource can be moved between workspaces with its content unsaved, have stale
  ACLs after a body save, or have attachments archived for a write that already failed validation —
  invisible to the caller and to operations.
- **Migration blockage** — every `E`-phase story's acceptance criteria demand a partial-failure strategy;
  without one shared decision, nine teams re-decide (differently) per mutation.
- **Support cost** — inconsistent state is discovered by users, not systems; there is no per-step record
  to reconcile from.

### 1.4 Objectives

The spike is done when all of the following are recorded and ratified:
- One failure strategy for all nine multi-step writes, with a per-step policy (compensate / retry /
  record) declared rather than implied.
- A compensation inventory: which steps have a real inverse, which are explicitly not-undoable.
- A result contract that makes partial failure **visible** to the caller (satisfying every `E`-story AC).
- A disposition for each latent defect (unawaited map, late validation check, duplicated-ids DTO):
  fixed or consciously preserved, each recorded as a parity deviation.

## 2. What the spike must decide

- The failure strategy for multi-step writes — compensate, compensation-log + best-effort, or best-effort.
- How each write step can be undone (or explicitly declared not-undoable).
- **Proposal so far (light, to validate):** one shared write-step recorder reused by every multi-step mutation, so the failure handling is decided once.
- **Draft decision:** [ADR-013 (draft)](./01-adr-non-atomic-write-saga.md) proposes a shared `WriteSaga`
  with per-step declared policy (Option B) — status 🔴 Proposed, pending ratification. Scenario variant
  under the domain-ACL assumption: [ADR-013-noACL](./02-adr-noacl-non-atomic-write-saga.md) (verdict: no change).

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
