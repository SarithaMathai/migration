# FE-Unblock Plan — build blockers first so frontend can start earliest

> 🏷️ `dgs-migration` · `fe-unblock` — **Generated:** 2026-07-24 by `generate_fe_unblock_plan.py` (in `generate_all.py`). A **dependency-only** view of what to build so frontend can start as early as possible. **Domain-first** — 38 of 41 FE stories stay inside their own domain, so keep building domain by domain; this doc just shows, within that, that FE starts on its own deps (not the whole domain) and that ready FE stories can run in parallel. Shows what CAN run in parallel, not a fixed-team schedule — for the capacity-bound calendar see [01-implementation-plan-1BE-1FE.md](01-implementation-plan-1BE-1FE.md) and [00-domain-rollout.md](00-domain-rollout.md).

**Do domains as coherent units — this view refines *within* that, it doesn't replace it.** Of the 41 frontend stories, **38 depend only on their OWN domain's backend**; only **3** reach across domains (the impression pair fused with BOM/Product screens, chiefly). So keep building domain by domain — the point here is the two refinements below, not a cross-domain free-for-all:

1. **You don't need a whole domain's backend done before its frontend starts** — each FE story starts when *its own* deps land (reads need B+G, writes need D, saga needs E).
2. **FE stories that are ready together can run in parallel** (capacity permitting) — nothing orders them beyond their backend deps.
3. **A handful of cross-domain blockers are worth pulling forward** — mainly Product/BOM field resolvers that unblock impression's fused FE; those are the only reason to look past one domain at a time.

**Supporting facts:**

- **145 of 211 backend stories** gate at least one frontend story (directly or via a BE prerequisite). Build these first.
- **66 backend stories gate NO frontend story** — federation stitches, parity, later-phase counts. They can **trail after the flips** (§3).
- Frontend stories are grouped into **readiness waves**: a wave holds every FE story whose backend deps are all satisfied by that point — **FE stories in the same wave have no dependency on each other and can run in parallel** (limited only by FE capacity, not order).
- **Not all of a domain's backend must finish before its FE starts** — an FE reads story needs only that entity's B + field-resolver (G) stories, not its writes (D/E); a writes story needs only its D stories; the saga FE needs only E. Each starts when *its own* deps land.

---

## 1. Backend unblocker sequence (build these first)

Only the frontend-blocking backend stories, in dependency order (level = longest dependency chain). Grouped across domains only so you can see the earliest unblock — in practice most of a level belongs to whichever domain you're building. Everything in a level is independent (parallel if you have the backend capacity). **Frontend stories unblocked** lists exactly which FE stories name this backend story as a dependency (grouped by FE domain; the number in parens is the count). More = more leverage → do first within its level. A story shown '— (prereq only)' unblocks no FE story directly; it's here because another blocker needs it.

### Backend level 1

| BE story | Domain | Story | Frontend stories unblocked (by domain) |
|---|---|---|---|
| 🟢 `B-01` | Product | getProduct(id) | Impression: `IMPRESSION-FE-001`, `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001`, `PRODUCT-FE-004` **(4)** |
| 🟢 `B-01` | BOM | getBomByIds data fetcher | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟢 `B-01` | Impression | searchImpressionsByProductId data fetcher | Impression: `IMPRESSION-FE-001`, `IMPRESSION-FE-002` **(2)** |
| 🟢 `B-01` | Measurement | getMeasurementByIds data fetcher | Measurement: `MST-FE-001`, `MST-FE-002` **(2)** |
| 🟢 `B-01` | Claims | getClaims(parentHumanId, claimHumanIds, part… | Claims: `CLAIM-FE-002` **(1)** |
| 🟢 `B-01` | Packaging | getPackagings(...) | Packaging: `PKG-FE-001` **(1)** |
| 🟢 `B-01` | Product Details | getProductDetailsById(ids) | Product Details: `PDTL-FE-001` **(1)** |
| 🟢 `B-01` | Watchlist | getWatchlistByIds(ids) | Watchlist: `WATCHLIST-FE-001` **(1)** |

### Backend level 2

| BE story | Domain | Story | Frontend stories unblocked (by domain) |
|---|---|---|---|
| 🟡 `G-13` | Product | IG/tag/tcin/spg + template trivial-field gro… | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001`, `PRODUCT-FE-002`, `PRODUCT-FE-004`, `PRODUCT-FE-005`, `PRODUCT-FE-006`, `PRODUCT-FE-007` **(7)** |
| 🟡 `G-07` | Product | Product.vendorAttributes + businessPartners … | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001`, `PRODUCT-FE-004`, `PRODUCT-FE-005`, `PRODUCT-FE-007` **(5)** |
| 🟡 `G-01` | BOM | Bom field resolvers (9 shared fields) | BOM: `BOM-FE-002`, `BOM-FE-003`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(4)** |
| 🟡 `G-06` | Product | Product.teams + discussionsV2 + discussionsC… | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001`, `PRODUCT-FE-004`, `PRODUCT-FE-005` **(4)** |
| 🟡 `G-08` | Product | Product.measurementSets + claims + bom + pro… | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001`, `PRODUCT-FE-005`, `PRODUCT-FE-011` **(4)** |
| 🟡 `A-04` | BOM | @DgsTypeResolver for the 2 BOM interfaces | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟢 `B-03` | BOM | getBomStatus (cacheable master data) | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟡 `G-03` | BOM | BomMaterial field resolvers (8 fields) | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟠 `G-08` | BOM | BomTrimMaterial field resolvers (7 fields) —… | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟢 `G-14` | BOM | Trivial pass-through fields (bundle) | BOM: `BOM-FE-003`, `BOM-FE-004`, `BOM-FE-007` **(3)** |
| 🟢 `B-03` | Product | getProductStatus (cacheable) | Product: `PRODUCT-FE-003`, `PRODUCT-FE-004`, `PRODUCT-FE-005` **(3)** |
| 🟡 `G-09` | Product | Product.productWorkspaceAttributes + product… | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001`, `PRODUCT-FE-004` **(3)** |
| 🟢 `B-04` | BOM | getBomByParentId data fetcher | BOM: `BOM-FE-002`, `BOM-FE-007` **(2)** |
| 🟢 `G-01` | Impression | Impression field resolvers (5 fields) | Impression: `IMPRESSION-FE-001`, `IMPRESSION-FE-002` **(2)** |
| 🟢 `B-04` | Measurement | getMeasurementSetStatus (cacheable) | Measurement: `MST-FE-001`, `MST-FE-003` **(2)** |
| 🟢 `B-02` | Product | getProductsByIds(ids) | Product: `PRODUCT-FE-002`, `PRODUCT-FE-004` **(2)** |
| 🔴 `G-01` | Product | Product.attachmentsWithMetaData | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001` **(2)** |
| 🔴 `G-02` | Product | Product.components | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001` **(2)** |
| 🟡 `G-10` | Product | Product.ancestryProducts + rating + reserved… | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001` **(2)** |
| 🟢 `G-14` | Product | Simple user/status fields + trivial pass-thr… | Product: `PRODUCT-FE-001`, `PRODUCT-FE-005` **(2)** |
| 🟡 `B-05` | BOM | getBomMaterialTypes (merge with Material Hub) | BOM: `BOM-FE-004` **(1)** |
| 🟢 `B-06` | BOM | getBomPackagingMaterialTypes (cacheable) | BOM: `BOM-FE-004` **(1)** |
| 🟢 `B-07` | BOM | getBomPackagingSubstrates (cacheable) | BOM: `BOM-FE-004` **(1)** |
| 🟢 `B-08` | BOM | getBomPackagingUnitOfMeasure (cacheable) | BOM: `BOM-FE-004` **(1)** |
| 🟢 `C-01` | BOM | getBomElastic data fetcher | BOM: `BOM-FE-003` **(1)** |
| 🟡 `C-03` | BOM | getComboSupplierForBom data fetcher | BOM: `BOM-FE-005` **(1)** |
| 🟢 `C-04` | BOM | getValidTrimSuppliersForBom data fetcher | BOM: `BOM-FE-005` **(1)** |
| 🟢 `C-05` | BOM | getValidRawMaterialSuppliersForBom data fetc… | BOM: `BOM-FE-005` **(1)** |
| 🟡 `D-01` | BOM | addBom mutation | BOM: `BOM-FE-006` **(1)** |
| 🟢 `D-03` | BOM | lockBom mutation | BOM: `BOM-FE-006` **(1)** |
| 🟢 `D-04` | BOM | unlockBom mutation | BOM: `BOM-FE-006` **(1)** |
| 🟢 `D-05` | BOM | updateBomComponentStatus mutation | BOM: `BOM-FE-006` **(1)** |
| 🟢 `B-02` | Claims | getClaimByIds(claimHumanIds) | Claims: `CLAIM-FE-002` **(1)** |
| 🟢 `B-03` | Claims | getCommunicationChannels (cacheable) | Claims: `CLAIM-FE-002` **(1)** |
| 🟢 `B-04` | Claims | getAllClaimsAbout (cacheable) | Claims: `CLAIM-FE-002` **(1)** |
| 🟡 `D-01` | Claims | createClaim | Claims: `CLAIM-FE-003` **(1)** |
| 🟡 `D-02` | Claims | bulkUpdateClaim | Claims: `CLAIM-FE-003` **(1)** |
| 🟢 `D-03` | Claims | requestClaimExport | Claims: `CLAIM-FE-003` **(1)** |
| 🟢 `D-04` | Claims | lockClaim | Claims: `CLAIM-FE-003` **(1)** |
| 🟢 `D-05` | Claims | unlockClaim | Claims: `CLAIM-FE-003` **(1)** |
| 🟠 `E-01` | Claims | updateClaim (proxy ACL + multi-step write) | Claims: `CLAIM-FE-004` **(1)** |
| 🟡 `G-01` | Claims | access + currentUserPermissions + participan… | Claims: `CLAIM-FE-002` **(1)** |
| 🟡 `G-02` | Claims | createdBy + updatedBy + businessPartner + de… | Claims: `CLAIM-FE-002` **(1)** |
| 🟢 `B-02` | Measurement | getUnitsOfMeasure (cacheable) | Measurement: `MST-FE-003` **(1)** |
| 🟢 `B-03` | Measurement | getThicknessUnitsOfMeasure (cacheable) | Measurement: `MST-FE-003` **(1)** |
| 🟡 `C-01` | Measurement | getMeasurements data fetcher (relationship +… | Measurement: `MST-FE-002` **(1)** |
| 🟢 `C-02` | Measurement | getMeasurementsElastic data fetcher | Measurement: `MST-FE-002` **(1)** |
| 🟢 `D-03` | Measurement | lockMeasurementSet mutation | Measurement: `MST-FE-004` **(1)** |
| 🟢 `D-04` | Measurement | unlockMeasurementSet mutation | Measurement: `MST-FE-004` **(1)** |
| 🟡 `D-06` | Measurement | putSampleMeasurementSet mutation | Measurement: `MST-FE-004` **(1)** |
| 🟢 `D-07` | Measurement | deleteSampleMeasurementSet mutation | Measurement: `MST-FE-004` **(1)** |
| 🟢 `B-02` | Packaging | getPackagingById(packagingId) | Packaging: `PKG-FE-001` **(1)** |
| 🟢 `B-03` | Packaging | getDielines(...) | Packaging: `PKG-FE-003` **(1)** |
| 🟢 `B-04` | Packaging | getPackagingFieldValuesByType(type, ids) | Packaging: `PKG-FE-002` **(1)** |
| 🟢 `B-05` | Packaging | getDielineEvaluationStatuses (cacheable) | Packaging: `PKG-FE-003` **(1)** |
| 🟢 `B-06` | Packaging | getCountries(codes) (cacheable) | Packaging: `PKG-FE-002` **(1)** |
| 🟡 `D-01` | Packaging | addPackaging | Packaging: `PKG-FE-004` **(1)** |
| 🟢 `D-02` | Packaging | evaluateDieline | Packaging: `PKG-FE-003` **(1)** |
| 🟡 `D-03` | Packaging | bulkAddPackagings | Packaging: `PKG-FE-004` **(1)** |
| 🟡 `D-04` | Packaging | bulkUpdatePackagings | Packaging: `PKG-FE-004` **(1)** |
| 🟢 `D-05` | Packaging | exportPackaging | Packaging: `PKG-FE-004` **(1)** |
| 🟢 `D-06` | Packaging | lockPackaging | Packaging: `PKG-FE-004` **(1)** |
| 🟢 `D-07` | Packaging | unlockPackaging | Packaging: `PKG-FE-004` **(1)** |
| 🟢 `D-09` | Packaging | updatePackagingComponentStatus | Packaging: `PKG-FE-004` **(1)** |
| 🟠 `E-01` | Packaging | updatePackaging (multi-step write) | Packaging: `PKG-FE-005` **(1)** |
| 🟡 `G-01` | Packaging | access + businessPartner + participantDetails | Packaging: `PKG-FE-001` **(1)** |
| 🟢 `G-02` | Packaging | createdBy + updatedBy + dielineEvaluators | Packaging: `PKG-FE-001` **(1)** |
| 🟠 `G-04` | Packaging | suggestedRetailPriceByDPCI + waveDescription… | Packaging: `PKG-FE-001` **(1)** |
| 🟡 `G-05` | Packaging | Dieline + PrinterDieline + PackagingElement … | Packaging: `PKG-FE-003` **(1)** |
| 🟢 `B-04` | Product | getProductVersions(id) | Product: `PRODUCT-FE-001` **(1)** |
| 🟢 `B-07` | Product | getProductRules | Product: `PRODUCT-FE-007` **(1)** |
| 🟢 `B-08` | Product | getProductRulesById(id) | Product: `PRODUCT-FE-007` **(1)** |
| 🟢 `B-09` | Product | getAllAvailableRules | Product: `PRODUCT-FE-007` **(1)** |
| 🟢 `B-10` | Product | getProductDeptRules(productIds, departmentId… | Product: `PRODUCT-FE-007` **(1)** |
| 🟢 `B-11` | Product | getProductBPRules(productIds, businessPartne… | Product: `PRODUCT-FE-007` **(1)** |
| 🟡 `C-02` | Product | getProductTemplates(...) | Product: `PRODUCT-FE-005` **(1)** |
| 🟡 `C-03` | Product | getCategories(...) | Product: `PRODUCT-FE-005` **(1)** |
| 🟡 `C-05` | Product | searchProductRules(...) | Product: `PRODUCT-FE-007` **(1)** |
| 🟡 `D-01` | Product | addProduct | Product: `PRODUCT-FE-008` **(1)** |
| 🟡 `D-02` | Product | addProducts (bulk) | Product: `PRODUCT-FE-008` **(1)** |
| 🟡 `D-03` | Product | bulkUpdateProducts | Product: `PRODUCT-FE-008` **(1)** |
| 🟡 `D-04` | Product | updateProduct | Product: `PRODUCT-FE-008` **(1)** |
| 🟡 `D-05` | Product | carryForwardProduct | Product: `PRODUCT-FE-008` **(1)** |
| 🟢 `D-06` | Product | addTeamsToProduct 🔀 Collab Canvas | Product: `PRODUCT-FE-009` **(1)** |
| 🟢 `D-07` | Product | addBusinessPartnersToProductWithType 🔀 Colla… | Product: `PRODUCT-FE-009` **(1)** |
| 🟢 `D-09` | Product | updateBusinessPartnerStatuses | Product: `PRODUCT-FE-010` **(1)** |
| 🟢 `D-10` | Product | updateViewToggle | Product: `PRODUCT-FE-008` **(1)** |
| 🟢 `D-12` | Product | updateProductTeamsWorkspaceContext | Product: `PRODUCT-FE-009` **(1)** |
| 🟢 `D-13` | Product | linkProduct | Product: `PRODUCT-FE-008` **(1)** |
| 🟢 `D-14` | Product | unlinkProduct | Product: `PRODUCT-FE-008` **(1)** |
| 🟢 `D-15` | Product | addProductRule | Product: `PRODUCT-FE-007` **(1)** |
| 🟢 `D-16` | Product | updateProductRule | Product: `PRODUCT-FE-007` **(1)** |
| 🟢 `D-17` | Product | deleteProductRule | Product: `PRODUCT-FE-007` **(1)** |
| 🟢 `D-18` | Product | updateComponentStatus (bulk) | Product: `PRODUCT-FE-012` **(1)** |
| 🔴 `E-03` | Product | getProductTechPackCountV1 stub + aggregation… | Product: `PRODUCT-FE-011` **(1)** |
| 🟢 `F-14` | Product | Cross-subgraph contract alignment (keys, typ… | Product: `PRODUCT-FE-013` **(1)** |
| 🟡 `G-04` | Product | ProductsCategories.categories (12-case) + Do… | Product: `PRODUCT-FE-005` **(1)** |
| 🟡 `H-06` | Product | Product entity fetcher (@DgsEntityFetcher) f… | Claims: `CLAIM-FE-002` **(1)** |
| 🟡 `D-01` | Product Details | createProductDetailsSet | Product Details: `PDTL-FE-002` **(1)** |
| 🟢 `D-03` | Product Details | productDetailLockUnlock | Product Details: `PDTL-FE-002` **(1)** |
| 🟡 `D-04` | Product Details | cloneFilesForProductDetails | Product Details: `PDTL-FE-002` **(1)** |
| 🟢 `D-05` | Product Details | updateProductDetailComponentStatus | Product Details: `PDTL-FE-002` **(1)** |
| 🟠 `E-01` | Product Details | updateProductDetailsSet (multi-step write) | Product Details: `PDTL-FE-003` **(1)** |
| 🟡 `G-01` | Product Details | access + currentUserPermissions + participan… | Product Details: `PDTL-FE-001` **(1)** |
| 🟡 `G-02` | Product Details | product + createdBy + updatedBy + businessPa… | Product Details: `PDTL-FE-001` **(1)** |
| 🟡 `G-03` | Product Details | attachment + item attachment/constructionSet… | Product Details: `PDTL-FE-001` **(1)** |
| 🟡 `C-01` | Watchlist | getWatchlistByFilter(...) (4-step read) | Watchlist: `WATCHLIST-FE-001` **(1)** |
| 🟡 `D-01` | Watchlist | createWatchlistEntries | Watchlist: `WATCHLIST-FE-002` **(1)** |
| 🟡 `D-02` | Watchlist | cloneFilesForWatchlist | Watchlist: `WATCHLIST-FE-002` **(1)** |
| 🟠 `E-01` | Watchlist | updateWatchlistEntries (multi-step write) | Watchlist: `WATCHLIST-FE-003` **(1)** |
| 🟢 `G-01` | Watchlist | Computed flatteners (status/reasons/inspecti… | Watchlist: `WATCHLIST-FE-001` **(1)** |
| 🟡 `G-02` | Watchlist | createdBy + updatedBy + workspaces + partici… | Watchlist: `WATCHLIST-FE-001` **(1)** |
| 🟡 `G-03` | Watchlist | attachments + product | Watchlist: `WATCHLIST-FE-001` **(1)** |
| 🟠 `G-10` | BOM | Impression library-resource resolution (shar… | — (prereq only) |
| 🟢 `G-06` | Claims | Shared value-type alignment (@shareable inst… | — (prereq only) |
| 🟢 `B-06` | Measurement | getMeasurementTemplates + getMeasurementTemp… | — (prereq only) |
| 🟢 `B-07` | Measurement | getSizeTemplates + getSizeCategories + getMa… | — (prereq only) |
| 🟢 `B-08` | Measurement | getTightFits + getTightFitByIdAndVersion dat… | — (prereq only) |
| 🟠 `E-00` | Product | WriteSaga shared module (Sprint 0, critical … | — (prereq only) |

### Backend level 3

| BE story | Domain | Story | Frontend stories unblocked (by domain) |
|---|---|---|---|
| 🟠 `G-03` | Product | Product.attachments + attachmentsV3 + attach… | Impression: `IMPRESSION-FE-002` ‖ Product: `PRODUCT-FE-001`, `PRODUCT-FE-005`, `PRODUCT-FE-006` **(4)** |
| 🟡 `G-12` | BOM | BomTrimLibraryImpressionDetails field resolv… | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟢 `G-13` | BOM | BomTrimZipperLibraryImpressionDetails field … | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟡 `G-17` | BOM | supplier entity references on material rows … | BOM: `BOM-FE-002`, `BOM-FE-007` ‖ Impression: `IMPRESSION-FE-001` **(3)** |
| 🟡 `G-01` | Measurement | Measurement field resolvers (13 fields) | Measurement: `MST-FE-001`, `MST-FE-002` **(2)** |
| 🟢 `G-07` | Measurement | TightFit field resolvers (5 fields) | Measurement: `MST-FE-001`, `MST-FE-002` **(2)** |
| 🟢 `F-10` | Product | Hive Gateway supergraph composition | Product: `PRODUCT-FE-001`, `PRODUCT-FE-004` **(2)** |
| 🟠 `G-03` | Claims | product + parentDetails (otherClaimBps / sys… | Claims: `CLAIM-FE-002` **(1)** |
| 🟠 `E-02` | Product | updateComponentStatuses (5-loader fan-out) | Product: `PRODUCT-FE-012` **(1)** |
| 🔴 `E-04` | Product | getProductTechPackBulkCountV1 (bulk wrapper,… | Product: `PRODUCT-FE-011` **(1)** |
| 🟢 `F-06` | Product | ResourcesCount.productBoms + packagingBoms +… | Product: `PRODUCT-FE-011` **(1)** |
| 🟢 `F-08` | Product | ResourcesCount.watchlists (internal, from Wa… | Product: `PRODUCT-FE-011` **(1)** |
| 🟡 `H-01` | Product | ResourcesCount.productAttachments + discussi… | Product: `PRODUCT-FE-011` **(1)** |
| 🟡 `H-02` | Product | ResourcesCount.discussions (federated, from … | Product: `PRODUCT-FE-011` **(1)** |
| 🟡 `H-03` | Product | ResourcesCount.sample (federated, from Sampl… | Product: `PRODUCT-FE-011` **(1)** |
| 🟡 `H-04` | Product | ResourcesCount.claims (federated, from Claim) | Product: `PRODUCT-FE-011` **(1)** |
| 🟡 `H-05` | Product | ResourcesCount.constructions (federated, fro… | Product: `PRODUCT-FE-011` **(1)** |
| 🟢 `G-05` | Watchlist | WatchlistPartner.partner entity reference (r… | Watchlist: `WATCHLIST-FE-001` **(1)** |

---

## 2. Frontend readiness waves (parallel within a wave)

Each frontend story appears in the wave where **all its backend deps are done** (wave n = after backend level n above). **Everything in one wave can be built in parallel** — no dependency between them. With one FE engineer you'd still do them one at a time (take a whole domain as a unit if you prefer); with more capacity, anything in a wave can go at once.

Grouped by domain within each wave, so you can still take a domain's frontend as one unit — the wave just tells you the earliest point each becomes startable.

| Ready after | Frontend stories, grouped by domain (‖ = parallel-eligible) |
|---|---|
| immediately (no BE dep) | **BOM:** `BOM-FE-001` · **Claims:** `CLAIM-FE-001` |
| backend level 2 | **BOM:** `BOM-FE-003` ‖ `BOM-FE-004` ‖ `BOM-FE-005` ‖ `BOM-FE-006` · **Claims:** `CLAIM-FE-003` ‖ `CLAIM-FE-004` · **Measurement:** `MST-FE-003` ‖ `MST-FE-004` · **Packaging:** `PKG-FE-001` ‖ `PKG-FE-002` ‖ `PKG-FE-003` ‖ `PKG-FE-004` ‖ `PKG-FE-005` · **Product:** `PRODUCT-FE-002` ‖ `PRODUCT-FE-003` ‖ `PRODUCT-FE-007` ‖ `PRODUCT-FE-008` ‖ `PRODUCT-FE-009` ‖ `PRODUCT-FE-010` ‖ `PRODUCT-FE-013` · **Product Details:** `PDTL-FE-001` ‖ `PDTL-FE-002` ‖ `PDTL-FE-003` · **Watchlist:** `WATCHLIST-FE-002` ‖ `WATCHLIST-FE-003` |
| backend level 3 | **BOM:** `BOM-FE-002` ‖ `BOM-FE-007` · **Claims:** `CLAIM-FE-002` · **Impression:** `IMPRESSION-FE-001` ‖ `IMPRESSION-FE-002` · **Measurement:** `MST-FE-001` ‖ `MST-FE-002` · **Product:** `PRODUCT-FE-001` ‖ `PRODUCT-FE-004` ‖ `PRODUCT-FE-005` ‖ `PRODUCT-FE-006` ‖ `PRODUCT-FE-011` ‖ `PRODUCT-FE-012` · **Watchlist:** `WATCHLIST-FE-001` |

> Earliest frontend work can begin after **backend level 2** — you do not have to wait for a whole domain, or for the backend queue to drain.

---

## 3. Trailing backend (gates no frontend — can land after the flips)

These **66** backend stories are not on any frontend story's critical path. Ship them in the background after the cutovers — they're federation stitches, field-resolver parity, and later-phase counts.

| BE story | Domain | Story |
|---|---|---|
| 🟡 `A-05` | BOM | Shared CI conformance gate + code → type registry (SPIKE… |
| 🟡 `C-02` | BOM | searchMaterialsBom data fetcher |
| 🟢 `D-02` | BOM | manageBomWorkspaces mutation |
| 🔴 `E-01` | BOM | updateBom — 3-step orchestrated write |
| 🟡 `F-01` | BOM | Implement Product.productBoms / boms / packagingBoms (in… |
| 🟢 `F-02` | BOM | Fill ResourcesCount.bomsCount (internal) |
| 🟢 `G-04` | BOM | BomPackagingMaterial field resolvers (2 fields) |
| 🟢 `G-05` | BOM | BomFabricMaterial field resolvers (4 fields) |
| 🟢 `G-06` | BOM | BomFabricSpecMaterial field resolvers (4 fields) |
| 🟢 `G-07` | BOM | BomCombinationMaterial field resolvers (4 fields) |
| 🟢 `G-09` | BOM | BomWashMaterial field resolvers (4 fields) |
| 🟡 `G-11` | BOM | BomFabricLibraryImpressionDetails.libraryResource |
| 🟡 `G-15` | BOM | BomMaterialSearchResult field resolvers (5 fields) |
| 🟢 `B-05` | Claims | getClaimExports |
| 🟡 `C-01` | Claims | searchGuestFacing(queryParam) |
| 🟡 `C-02` | Claims | getClaimsElastic(parentHumanId) |
| 🟡 `G-04` | Claims | workspaces + ClaimSubstantiate.substantiatedBy + ClaimDe… |
| 🟡 `H-01` | Claims | Product.claims (federation contribution) |
| 🟢 `H-02` | Claims | ResourcesCount.claims (TechPack — claims side of PRODUCT… |
| 🟢 `B-02` | Impression | getImpressionCountsByProductId data fetcher |
| 🟡 `D-01` | Impression | updateImpressions mutation |
| 🟢 `F-01` | Impression | Product.impressions / impressionCounts (internal field r… |
| 🟡 `G-02` | Impression | ImpressionCount.counts aggregation |
| 🟢 `G-04` | Impression | attachment entity reference (recommended, PO-gated) |
| 🟢 `B-05` | Measurement | getSampleMeasurement data fetcher |
| 🟢 `B-09` | Measurement | searchSparkSizes data fetcher (NEXUS + Tag fan-out) |
| 🟡 `D-01` | Measurement | addMeasurement mutation |
| 🟢 `D-02` | Measurement | updateMeasurementAccess mutation |
| 🟢 `D-05` | Measurement | updateMeasurementComponentStatus mutation |
| 🟢 `D-08` | Measurement | addMeasurementTemplate + updateMeasurementTemplate + del… |
| 🟢 `D-09` | Measurement | addSizeTemplate + updateSizeTemplate mutations |
| 🟢 `D-10` | Measurement | addTightFit + updateTightFit mutations |
| 🟠 `E-01` | Measurement | updateMeasurement — 2-step orchestrated write |
| 🟡 `F-01` | Measurement | Implement Product.measurementSets (internal) |
| 🟢 `G-02` | Measurement | SampleMeasurementSet field resolvers (2 fields) |
| 🟢 `G-05` | Measurement | MeasurementTemplate field resolvers (5 fields) |
| 🟢 `G-06` | Measurement | SizeTemplate field resolvers (3 fields) |
| 🟢 `H-01` | Measurement | Contribute sampleMeasurement to the SampleV2 entity |
| 🟢 `H-02` | Measurement | SampleMeasurementSet.sample forward reference (recommend… |
| 🟡 `C-01` | Packaging | getPackagingElastic(parentHumanId) |
| 🟡 `D-08` | Packaging | cloneFilesForDielines |
| 🟢 `F-01` | Packaging | Product packaging links (internal, same subgraph) |
| 🟡 `G-03` | Packaging | product + workspaces + attachments |
| 🟢 `B-05` | Product | getCopyStatus(id) |
| 🟢 `B-06` | Product | getProductTemplateById(id) |
| 🟠 `C-01` | Product | getProducts(...) two-stage hydration |
| 🟡 `C-04` | Product | getRatingByTcin(tcin) (external rating) |
| 🟢 `D-08` | Product | removeProductResources |
| 🟢 `D-11` | Product | updateWorkspaceAttributes 🔀 Collab Canvas |
| 🔴 `E-01` | Product | productBusinessPartnerActions (REMOVE/DROP/UNDROP) |
| 🟢 `F-04` | Product | ResourcesCount.measurementSets (internal, from Measureme… |
| 🟢 `F-09` | Product | Retire the TechPack aggregation facade |
| 🟢 `F-11` | Product | Platform stub verification (VMM/IG/Doppler/CORONA/APEX) |
| 🟢 `F-12` | Product | Deferred partner-wrapper decision (drift mutations) |
| 🟡 `G-05` | Product | Product.samples + sampleIds + elasticSamplesList |
| 🟡 `G-11-1` | Product | Product.notRemovablePartnerIds + notRemovableWorkspaceIds |
| 🟡 `G-11-2` | Product | Product.associateProductsAsks + Product.variations |
| 🟡 `G-15` | Product | Port product utils to Kotlin |
| 🟡 `G-17` | Product | Entity references on partner/lineage value types (recomm… |
| 🟡 `C-01` | Product Details | getProductDetailsElastic(resourceId) |
| 🟢 `D-02` | Product Details | updateProductDetailAccess |
| 🟢 `F-01` | Product Details | Product.productDetails (internal, same subgraph) |
| 🟢 `B-02` | Watchlist | getWatchlistReasons (cacheable) |
| 🟢 `B-03` | Watchlist | getWatchlistInspectionActions (cacheable) |
| 🟢 `F-01` | Watchlist | Product.watchlists (internal) |
| 🟢 `F-02` | Watchlist | ResourcesCount.watchlists (internal — TechPack) |

---
*FE-unblock plan · generated 2026-07-24 by generate_fe_unblock_plan.py.*