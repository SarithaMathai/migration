# Techpack — Story Breakdown

> **Decision:** [ADR-015 (draft)](./01-adr-techpack.md) — facade-then-federate (Option B).
> **Status:** 🟠 Draft proposed — ratification pending.
> **This file lists which concrete stories implement the decision — full story text (Current Behaviour,
> Target, Acceptance Criteria, Test Cases) lives in each domain's `be-04-stories.md`, linked below. This
> file is the case's own index, not a duplicate of that text.**

## Phase 1 — facade (ships day 1, before any sibling subgraph federates)

| Story | Domain | What it builds |
|---|---|---|
| [`PRODUCT-BE-E-03`](../../analysis/product/be-04-stories.md#product-be-e-03-getproducttechpackcountv1-stub-aggregation-facade-facade-then-federate-phase-1) | product | thin `@DgsQuery` stub + the aggregation facade extracted from `getTechPackResourceCountMap`, behavior-frozen except the pinned deviations |
| [`PRODUCT-BE-E-04`](../../analysis/product/be-04-stories.md#product-be-e-04-getproducttechpackbulkcountv1-bulk-wrapper-ordering-fix) | product | bulk wrapper over the same facade, input-ordered (fixes the completion-order bug) |

## Phase 2 — per-domain federation (each ships independently, on its owning subgraph's own schedule)

| Story | Domain | `ResourcesCount` field | Owning subgraph |
|---|---|---|---|
| [`PRODUCT-BE-H-01`](../../analysis/product/be-04-stories.md#product-be-h-01-resourcescountproductattachments-discussionattachments-federated-from-attachment) | product | `productAttachments` + `discussionAttachments` | plm-attachment |
| [`PRODUCT-BE-H-02`](../../analysis/product/be-04-stories.md#product-be-h-02-resourcescountdiscussions-federated-from-discussion) | product | `discussions` | plm-discussion |
| [`PRODUCT-BE-H-03`](../../analysis/product/be-04-stories.md#product-be-h-03-resourcescountsample-federated-from-sample) | product | `sample` | plm-sample |
| [`PRODUCT-BE-H-04`](../../analysis/product/be-04-stories.md#product-be-h-04-resourcescountclaims-federated-from-claim) | product | `claims` (product side) | spark-claims |
| [`CLAIM-BE-H-02`](../../analysis/claims/be-04-stories.md#claim-be-h-02-resourcescountclaims-techpack-claims-side-of-product-be-h-04) | claims | `claims` (claims side, paired with `PRODUCT-BE-H-04`) | spark-claims |
| [`PRODUCT-BE-H-05`](../../analysis/product/be-04-stories.md#product-be-h-05-resourcescountconstructions-federated-from-construction) | product | `constructions` | construction (later phase) |
| `PRODUCT-BE-F-04` / `F-06` / `F-08` | product | `measurementSets` · `productBoms`/`packagingBoms`/`boms` · `watchlists` | co-located in `plm-product` — no entity fetcher, stays Phase F |

## Cross-cutting — needed by any external subgraph referencing `Product`, not techpack-specific

| Story | Domain | What it builds |
|---|---|---|
| [`PRODUCT-BE-H-06`](../../analysis/product/be-04-stories.md#product-be-h-06-product-entity-fetcher-dgsentityfetcher-for-cross-subgraph-references) | product | `@DgsEntityFetcher(name="Product")` — required before `Claims.product`/any external `Product` reference resolves; blocks `CLAIM-BE-H-01`/`H-02` end-to-end, not just this case |

## Phase 3 — retirement (only once all Phase 2 slices report green on both facade and owner paths)

| Story | Domain | What it builds |
|---|---|---|
| [`PRODUCT-BE-F-09`](../../analysis/product/be-04-stories.md#product-be-f-09-retire-the-techpack-aggregation-facade) | product | deletes the facade; zero references remain (Feign beans, flags, health checks); all 11 fields resolve via federation |

## ACL

Out of scope for this case — see [ADR-019](../acl/01-adr-acl-mid-request-update.md) and `01-adr-techpack.md`'s
own ACL note; the walk's partner-permission filter and the attachment-hydration capability token are both
permission-check shaped, not downstream-token, so nothing here changes under ADR-019.

---
*Story ids and links regenerate from each domain's `be-04-stories.md` — this index is hand-maintained
alongside the ADR; if a domain file's story is renamed, update the link here in the same PR.*
