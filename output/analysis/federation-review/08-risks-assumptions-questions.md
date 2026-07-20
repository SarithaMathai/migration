# 08 · Risks, Assumptions & Open Questions

> Federation review · 2026-07-17 · Items needing human review are marked ⚠.

## 1. Risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|------|-----------|--------|------------|-------|
| RK-1 ⚠ | The key/name mismatches (R1–R5) existed across *reviewed, generated* schemas — other latent contract drift may exist in phase-2 domains | Medium | High | CI composition gate (PRODUCT-BE-F-10 AC); run `hive compose` on every schema PR | Platform |
| RK-2 | Synthesized ids (`id` = humanId on Measurement, Claims, Packaging, Watchlist, Dieline — program decision 2026-07-17) — if a backend later mints real ids, federation keys and Apollo cache identities silently split | Medium | High | Contract test pinning `id == humanId` per entity; any future real-id introduction must version through the gateway | Tech Lead |
| RK-3 | Claims is the only separate subgraph in phase 1 — every gateway-hop defect (auth propagation, partial `_entities` failures) surfaces there first with no prior art | Medium | Medium | Make CLAIM-FE-002 an explicit canary with rollback flag; PRODUCT-BE-F-13 ships DataLoader batching + null-tolerant hydration | BE-2 |
| RK-4 | Phase-2 stubs (workspace, user-profile, attachment, sample, team, search) stay gateway-stitched — a stitching regression breaks 8 domains' field resolvers at once | Medium | High | PRODUCT-BE-F-11 stub-verification suite runs per deploy, not once | Platform |
| RK-5 | Denormalized display pairs (`supplierName`, `facilityName`, `printer*`) may be authoring-time snapshots; converting to live entity refs (REC-1, facility/printer options) could change displayed history | Medium | Medium | OQ-3 answered before any REC adoption; RECs keep both fields | PO |
| RK-6 | `Categories` interface→union change (already in the product schema) breaks clients selecting `id`/`name` without inline fragments | High (if unverified) | Medium | Existing A-04/G-04 verification + PRODUCT-FE-012 `__typename` sweep | FE |
| RK-7 | Regeneration discipline: hand edits to `output/jira/*` or `output/summary/*` are silently lost on the next `generate_all.py` run | Low | Low | This review only edited sources; note reiterated in 07 §4 | All |

## 2. Assumptions

1. `plm-product` ships as **one** subgraph (monorepo decision holds); co-located references never traverse the gateway.
2. ✅ Claims ships as `spark-claims`, a separate subgraph, in phase 1 — **confirmed 2026-07-17 (OQ-6)**; the stale "co-located" comment in the product schema has been corrected.
3. ACL remains ignored in DGS implementations (stakeholder decision; unchanged by this review).
4. The completed platform FE enablement (router flag, codegen, cache remap, fragment sweep) is a stable baseline; only the R3/R4 names need re-verification (PRODUCT-FE-012).
5. Federation spec v2.3 across all subgraphs; no v1-style `extend` semantics at the gateway.
6. `code/schemas/core.txt` is canonical for platform type shapes (`VMM_*`).

## 3. Open questions (⚠ all require answers before the affected work starts)

| # | Question | Blocks | Suggested decider |
|---|---|---|---|
| OQ-1 | ✅ **RESOLVED (2026-07-17):** every entity federates on `id`; humanId-only entities (Claims, Packaging, Watchlist, Dieline) wrap the record with a synthesized `id` — the Measurement pattern — so stitching is uniform. `humanId` stays for the client contract. Residual risk tracked as RK-2 | — | decided |
| OQ-2 | ✅ **RESOLVED (2026-07-17):** `CORONA_ItemDetails` stays an **entity keyed `tcinId`** — where a tcin exists the record carries `tcinId`, and Corona inflates the item details from that key via the gateway | — | decided |
| OQ-3 | ⏸ **DEFERRED (2026-07-17):** snapshot-vs-live semantics of `supplierName`/`facilityName`/`printer*` left open for now; BOM-BE-G-17 and the facility/printer entity-ref options stay parked until this is picked up | BOM-BE-G-17, facility/printer options | PO + Backend Eng (later) |
| OQ-4 | ⏸ **DEFERRED (2026-07-17):** `relatedResources` stays `[ID]`; no resource union | nothing | — |
| OQ-5 | ⏸ **DEFERRED (2026-07-17):** the 6 recommended additive entity-reference changes are **not approved for now** — the 5 REC BE stories + BOM-FE-007 remain in the inventory as PO-gated backlog, unscheduled; clients keep their second fetches | the 5 REC BE stories + BOM-FE-007 | PO (revisit) |
| OQ-6 | ✅ **RESOLVED (2026-07-17): claims IS a separate subgraph** (`spark-claims`). PRODUCT-BE-F-13, CLAIM-BE-F-01/F-02 entity fetchers, and the R5 `@shareable` duplication stand as specified; CLAIM-FE-002 remains the first cross-subgraph cutover canary (RK-3) | — | decided |
