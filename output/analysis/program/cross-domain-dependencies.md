# Cross-Domain Dependencies

> **Generated:** 2026-07-18 · by `generate_cross_domain_deps.py` — collects every `**Blocked by:**` line already declared in each domain's `be-04-stories.md`; adds nothing new. Regenerate after any story's `Blocked by:` field changes.
> **`Depends on:` vs `Blocked by:`** — `Depends on:` is an intra-domain build-order edge the wave scheduler enforces (see each domain's "Recommended Implementation Order"). `Blocked by:` is documentation only: nothing in the generator pipeline currently treats it as a hard scheduling gate — it's the human-readable record of a cross-domain or cross-subgraph constraint the *program plan* (sprint sequencing, not the wave scheduler) has to honor by hand.

---

## Blocked on shared infrastructure in another domain

| Blocked story | Domain | Waits on | Target story |
|---|---|---|---|
| `BOM-BE-E-01` — `updateBom` — 3-step orchestrated write | bom | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) | `PRODUCT-BE-E-00` |
| `CLAIM-BE-E-01` — `updateClaim` (proxy ACL + multi-step write) | claims | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) | `PRODUCT-BE-E-00` |
| `MST-BE-E-01` — `updateMeasurement` — 2-step orchestrated write | measurement | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) | `PRODUCT-BE-E-00` |
| `PKG-BE-E-01` — `updatePackaging` (multi-step write) | packaging | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) | `PRODUCT-BE-E-00` |
| `PDTL-BE-E-01` — `updateProductDetailsSet` (multi-step write) | productDetails | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) | `PRODUCT-BE-E-00` |
| `WATCHLIST-BE-E-01` — `updateWatchlistEntries` (multi-step write) | watchlist | product (`PRODUCT-BE-E-00`, the shared `WriteSaga` module) | `PRODUCT-BE-E-00` |

---

## Blocked on a not-yet-live subgraph (later-phase domain)

| Blocked story | Domain | Waits on |
|---|---|---|
| `CLAIM-BE-H-01` — `Product.claims` (federation contribution) | claims | product |
| `CLAIM-BE-H-02` — `ResourcesCount.claims` (TechPack — claims side of PRODUCT-BE-H-04) | claims | product |
| `IMPRESSION-BE-F-01` — `Product.impressions` / `impressionCounts` (internal field resolver) | impression | product B-01 |
| `MST-BE-H-01` — Contribute `sampleMeasurement` to the `SampleV2` entity | measurement | sample |
| `PRODUCT-BE-H-01` — `ResourcesCount.productAttachments` + `discussionAttachments` (federated, from Attachment) | product | attachment domain (⛔ cross-subgraph — does not ship until `plm-attachment` is live) |
| `PRODUCT-BE-H-02` — `ResourcesCount.discussions` (federated, from Discussion) | product | discussion domain (⛔ cross-subgraph) |
| `PRODUCT-BE-H-03` — `ResourcesCount.sample` (federated, from Sample) | product | sample domain (⛔ cross-subgraph) |
| `PRODUCT-BE-H-04` — `ResourcesCount.claims` (federated, from Claim) | product | claim domain (⛔ cross-subgraph) |
| `PRODUCT-BE-H-05` — `ResourcesCount.constructions` (federated, from Construction) | product | construction domain (⛔ cross-subgraph) |

---
*6 infrastructure gate(s) · 9 later-phase-subgraph gate(s).*