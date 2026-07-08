# Complex Story — Non-atomic multi-step writes (the saga / compensation pattern)

> **Summary —** Make every multi-step “save” recover cleanly when a middle step fails — using one shared saga/compensation framework instead of nine hand-rolled guesses.
> **Spike:** `SPARK-SPIKE-01` · **Status:** 🔴 Open — decision pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** bom, measurement, packaging, productDetails, watchlist, claims, sample, product
> **Stub stories:** `SPARK-BOM-E01`, `SPARK-MEAS-E01`, `SPARK-PKG-E01`, `SPARK-PDTL-E01`, `SPARK-WL-E01`, `SPARK-CLM-E01`, `SPARK-SMPL-E01/E02`, `SPARK-PROD-E02`

> **Migrates (source resolvers → this case):** nine multi-step mutations — `updateBom` (`SPARK-BOM-E01`),
> `updateMeasurement` (`SPARK-MEAS-E01`), `updatePackaging` (`SPARK-PKG-E01`), `updateProductDetailsSet`
> (`SPARK-PDTL-E01`), `updateWatchlistEntries` (`SPARK-WL-E01`), `updateClaim` (`SPARK-CLM-E01`), `updateSamplesV2`
> (`SPARK-SMPL-E01`), `bulkEvaluateSamples` (`SPARK-SMPL-E02`), `updateComponentStatuses` (`SPARK-PROD-E02`/M20).
>.

## 1. The problem (it recurs in 8+ places)

- Across the program, **every "update" mutation is a multi-step, non-atomic, no-rollback write**.
- They all share the same failure mode: an early step commits, a later step fails, and the resource is left inconsistent.

| Mutation | What the user is doing | Steps (legacy) | Risk |
|---|---|---|---|
| `updateBom` (`BOM-E01`) | Saving a bill of materials: move it between workspaces, save its content, update which partners may see it | workspace assoc **(commits first)** → body PUT → permissions PUT | step-2 persists if step-3 fails; ACL left stale |
| `updateMeasurement` (`MEAS-E01`) | Saving a measurement set: move it between workspaces, then save its content | workspace assoc **(commits first)** → body PUT | 2-step, no rollback |
| `updatePackaging` (`PKG-E01`) | Saving packaging details and adding/removing its attachments | body → attachment add/remove | partial attachment state |
| `updateProductDetailsSet` (`PDTL-E01`) | Saving a set of product-detail records in one action | multi-step set update | partial set |
| `updateWatchlistEntries` (`WL-E01`) | Updating a watchlist's entries, the user groups who follow it, and archiving attachments removed from it | **un-awaited user-group add/update** (latent bug) → entries → archive removed attachments | race + partial |
| `updateClaim` (`CLM-E01`) | Saving a claim: update access on the partner's behalf, its workspace, and its content | proxy ACL → workspace → body | proxy-ACL/body divergence |
| `updateSamplesV2` (`SMPL-E01`) | Saving a sample together with its evaluation results | sample body + evaluation | partial evaluation |
| `bulkEvaluateSamples` (`SMPL-E02`) | Recording evaluations for many samples at once and opening new review rounds | evaluation + new-rounds util (bulk) | partial bulk |
| `updateComponentStatuses` (`PROD-E02`) | Setting a status across all of a product's components (BOMs, measurements, details, packaging, claims) | 5-loader fan-out (+ shadow-var bug) | partial status fan-out |

> Step sequences above are taken from each domain's `02-resolver-analysis.md` code deep-dive (e.g.
> [bom M2](../../initial-analysis/bom/02-resolver-analysis.md), [measurement M3](../../initial-analysis/measurement/02-resolver-analysis.md),
> [watchlist M2](../../initial-analysis/watchlist/02-resolver-analysis.md), [product M20](../../initial-analysis/product/02-resolver-analysis.md));
> the descriptions summarize the same source.

- The program already lists *"Non-atomic write failure strategy (saga / compensation / best-effort)"* as a cross-domain decision.
- **This case turns that decision into one shared mechanism** so each write isn't a bespoke guess.

## 2. What the spike must decide

- The failure strategy for multi-step writes — compensate, compensation-log + best-effort, or best-effort.
- How each write step can be undone (or explicitly declared not-undoable).
- **Proposal so far (light, to validate):** one shared write-step recorder reused by every multi-step mutation, so the failure handling is decided once.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
