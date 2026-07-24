# Domain-by-Domain Rollout — 1 BE + 1 FE

> 🏷️ **Tags:** `dgs-migration` · `rollout-plan` — **Generated:** 2026-07-24 by `generate_domain_rollout.py` (runs inside `generate_all.py`). The same team and the same day math as [01-implementation-plan-1BE-1FE.md](01-implementation-plan-1BE-1FE.md), reorganized **one block per domain** in cutover order: what the **backend engineer** builds first → the exact **frontend start gate** → the **FE cutover** → domain done. Day figures are AI-estimated midpoints — confirm in refinement. 1 sprint = 10 days, d0 = start.

## Operating model (1 BE + 1 FE)

- **One backend engineer, one frontend engineer, working in parallel**, completing the program **domain by domain**.
- The backend engineer runs the domains in `team_config.BE_QUEUE` order — **Product first** (host DGS + the shared `WriteSaga` module `PRODUCT-BE-E-00` that every other domain's write story is blocked on), then the rest.
- For each domain the backend engineer builds its **phases A–E** (reads → search → writes). Once the specific A–E stories the FE stories depend on are live, the **frontend engineer starts the cutover for that domain** while the backend engineer moves on to the next domain.
- Backend **F/G** stories (federation stitches, field-resolver parity) trail *behind* the flip — they don't gate it.
- **Reads flip before writes before the multi-step saga** — the FE stage order inside each domain.
- **Spikes (SPIKE-01…07)** run in the first 1–2 sprints alongside Product scaffold work; E-phase (saga) stories are gated on their outcomes.

> **⚠ Priority reorder (2026-07-24):** an **external team is waiting on `watchlist` + `impression`**, so those are prioritized. Impression's **backend** is pulled far forward (A–E gate ≈ d297, vs ~d520 in the pilot-first order) — that is what unblocks the external consumer of the federated impression data. Impression's **frontend**, though, is fused with BOM + Product screens (`getBomDataAndImpressions`, `getCarryForwardFormData`), so its FE flip can only happen in the same wave as BOM/Product, not before them — which is why `bom` and `product` core also move up and the smaller domains shift later. If the external team only needs the backend data, impression is effectively unblocked at its BE gate above, well before its FE cutover row. Order lives in `team_config.py` with a revert note.

**Bottom line:** ≈ **55 sprints (~28 months)** end-to-end with this 1 BE + 1 FE team; buffered (+20%) ≈ 66 sprints. The backend lane is the long pole — the frontend engineer is gate-bound (waiting on backend), not capacity-bound, so between flips they run parity dashboards, dual-run monitoring, rollback drills, and pre-pull the next domain's prep.

---

## Domain 1 — Watchlist

> **13 BE + 3 FE stories** · Wave 1 pilot — smallest isolated surface; proves flag flip + rollback

**① Backend builds first** — window **d304–d336 (spr 31–34)** (≈ 31 days, 21–41).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d324** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `G-02` → `G-05`.
- **Starts with** `B-01` — getWatchlistByIds(ids) (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d324):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟢 `B-01` | getWatchlistByIds(ids) | `WATCHLIST-FE-001` |
| 🟡 `C-01` | getWatchlistByFilter(...) (4-step read) | `WATCHLIST-FE-001` |
| 🟡 `D-01` | createWatchlistEntries | `WATCHLIST-FE-002` |
| 🟡 `D-02` | cloneFilesForWatchlist | `WATCHLIST-FE-002` |
| 🟠 `E-01` | updateWatchlistEntries (multi-step write) | `WATCHLIST-FE-003` |
| 🟢 `G-01` | Computed flatteners (status/reasons/inspectio… | `WATCHLIST-FE-001` |
| 🟡 `G-02` | createdBy + updatedBy + workspaces + particip… | `WATCHLIST-FE-001` |
| 🟡 `G-03` | attachments + product | `WATCHLIST-FE-001` |
| 🟢 `G-05` | WatchlistPartner.partner entity reference (re… | `WATCHLIST-FE-001` |

**③ Frontend cutover** — window **d324–d332 (spr 33–34)**, gated by: BE Watchlist A–E done (d324).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 3 | 🟢 `WATCHLIST-FE-002` — Migrate watchlist create and clone muta… | `D-01`, `D-02` |
| 4 | 🟢 `WATCHLIST-FE-001` — Migrate watchlist reads | `B-01`, `C-01`, `G-01`, `G-02`, `G-03`, `G-05` |
| 4 | 🟡 `WATCHLIST-FE-003` — Migrate updateWatchlistEntries saga han… | `E-01` |

- **FE cutover flow:** `WATCHLIST-FE-002` → `WATCHLIST-FE-001` → `WATCHLIST-FE-003`.

**④ Domain done ≈ d332 (sprint 34)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## Domain 2 — Product

> **69 BE + 13 FE stories** · Largest surface + host DGS — pulled up (feeds impression/BOM FE); writes last

**① Backend builds first** — window **d0–d200 (spr 1–20)** (≈ 200 days, 138–262).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d108** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `E-03` → `F-04` → `F-09`.
- **Starts with** `B-01` — getProduct(id) (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d108):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟢 `B-01` | getProduct(id) | `PRODUCT-FE-001`, `PRODUCT-FE-004` |
| 🟢 `B-02` | getProductsByIds(ids) | `PRODUCT-FE-002`, `PRODUCT-FE-004` |
| 🟢 `B-03` | getProductStatus (cacheable) | `PRODUCT-FE-003`, `PRODUCT-FE-004`, `PRODUCT-FE-005` |
| 🟢 `B-04` | getProductVersions(id) | `PRODUCT-FE-001` |
| 🟢 `B-07` | getProductRules | `PRODUCT-FE-007` |
| 🟢 `B-08` | getProductRulesById(id) | `PRODUCT-FE-007` |
| 🟢 `B-09` | getAllAvailableRules | `PRODUCT-FE-007` |
| 🟢 `B-10` | getProductDeptRules(productIds, departmentIds… | `PRODUCT-FE-007` |
| 🟢 `B-11` | getProductBPRules(productIds, businessPartner… | `PRODUCT-FE-007` |
| 🟡 `C-02` | getProductTemplates(...) | `PRODUCT-FE-005` |
| 🟡 `C-03` | getCategories(...) | `PRODUCT-FE-005` |
| 🟡 `C-05` | searchProductRules(...) | `PRODUCT-FE-007` |
| 🟡 `D-01` | addProduct | `PRODUCT-FE-008` |
| 🟡 `D-02` | addProducts (bulk) | `PRODUCT-FE-008` |
| 🟡 `D-03` | bulkUpdateProducts | `PRODUCT-FE-008` |
| 🟡 `D-04` | updateProduct | `PRODUCT-FE-008` |
| 🟡 `D-05` | carryForwardProduct | `PRODUCT-FE-008` |
| 🟢 `D-06` | addTeamsToProduct 🔀 Collab Canvas | `PRODUCT-FE-009` |
| 🟢 `D-07` | addBusinessPartnersToProductWithType 🔀 Collab… | `PRODUCT-FE-009` |
| 🟢 `D-09` | updateBusinessPartnerStatuses | `PRODUCT-FE-010` |
| 🟢 `D-10` | updateViewToggle | `PRODUCT-FE-008` |
| 🟢 `D-12` | updateProductTeamsWorkspaceContext | `PRODUCT-FE-009` |
| 🟢 `D-13` | linkProduct | `PRODUCT-FE-008` |
| 🟢 `D-14` | unlinkProduct | `PRODUCT-FE-008` |
| 🟢 `D-15` | addProductRule | `PRODUCT-FE-007` |
| 🟢 `D-16` | updateProductRule | `PRODUCT-FE-007` |
| 🟢 `D-17` | deleteProductRule | `PRODUCT-FE-007` |
| 🟢 `D-18` | updateComponentStatus (bulk) | `PRODUCT-FE-012` |
| 🟠 `E-02` | updateComponentStatuses (5-loader fan-out) | `PRODUCT-FE-012` |
| 🔴 `E-03` | getProductTechPackCountV1 stub + aggregation … | `PRODUCT-FE-011` |
| 🔴 `E-04` | getProductTechPackBulkCountV1 (bulk wrapper, … | `PRODUCT-FE-011` |
| 🟢 `F-06` | ResourcesCount.productBoms + packagingBoms + … | `PRODUCT-FE-011` |
| 🟢 `F-08` | ResourcesCount.watchlists (internal, from Wat… | `PRODUCT-FE-011` |
| 🟢 `F-10` | Hive Gateway supergraph composition | `PRODUCT-FE-001`, `PRODUCT-FE-004` |
| 🟢 `F-14` | Cross-subgraph contract alignment (keys, type… | `PRODUCT-FE-013` |
| 🔴 `G-01` | Product.attachmentsWithMetaData | `PRODUCT-FE-001` |
| 🔴 `G-02` | Product.components | `PRODUCT-FE-001` |
| 🟠 `G-03` | Product.attachments + attachmentsV3 + attachm… | `PRODUCT-FE-001`, `PRODUCT-FE-005`, `PRODUCT-FE-006` |
| 🟡 `G-04` | ProductsCategories.categories (12-case) + Dop… | `PRODUCT-FE-005` |
| 🟡 `G-06` | Product.teams + discussionsV2 + discussionsCo… | `PRODUCT-FE-001`, `PRODUCT-FE-004`, `PRODUCT-FE-005` |
| 🟡 `G-07` | Product.vendorAttributes + businessPartners +… | `PRODUCT-FE-001`, `PRODUCT-FE-004`, `PRODUCT-FE-005`, `PRODUCT-FE-007` |
| 🟡 `G-08` | Product.measurementSets + claims + bom + prod… | `PRODUCT-FE-001`, `PRODUCT-FE-005`, `PRODUCT-FE-011` |
| 🟡 `G-09` | Product.productWorkspaceAttributes + productW… | `PRODUCT-FE-001`, `PRODUCT-FE-004` |
| 🟡 `G-10` | Product.ancestryProducts + rating + reservedD… | `PRODUCT-FE-001` |
| 🟡 `G-13` | IG/tag/tcin/spg + template trivial-field group | `PRODUCT-FE-001`, `PRODUCT-FE-002`, `PRODUCT-FE-004`, `PRODUCT-FE-005`, `PRODUCT-FE-006`, `PRODUCT-FE-007` |
| 🟢 `G-14` | Simple user/status fields + trivial pass-thro… | `PRODUCT-FE-001`, `PRODUCT-FE-005` |
| 🟡 `H-01` | ResourcesCount.productAttachments + discussio… | `PRODUCT-FE-011` |
| 🟡 `H-02` | ResourcesCount.discussions (federated, from D… | `PRODUCT-FE-011` |
| 🟡 `H-03` | ResourcesCount.sample (federated, from Sample) | `PRODUCT-FE-011` |
| 🟡 `H-04` | ResourcesCount.claims (federated, from Claim) | `PRODUCT-FE-011` |
| 🟡 `H-05` | ResourcesCount.constructions (federated, from… | `PRODUCT-FE-011` |

**③ Frontend cutover** — window **d342–d428 (spr 35–43)**, gated by: BE Product A–E done (d108) + pilot soak (d342).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 3 | 🟡 `PRODUCT-FE-003` — Migrate getProductsByIds documents (bul… | `B-03` |
| 4 | 🟡 `PRODUCT-FE-008` — Migrate simple product mutations | `D-01`, `D-02`, `D-03`, `D-04`, `D-05`, `D-10`, `D-13`, `D-14` |
| 5 | 🟢 `PRODUCT-FE-006` — Migrate getCategories documents | `G-03`, `G-13` |
| 5 | 🟡 `PRODUCT-FE-007` — Migrate product rules administration | `B-07`, `B-08`, `B-09`, `B-10`, `B-11`, `C-05`, `D-15`, `D-16`, `D-17`, `G-07`, `G-13` |
| 5 | 🟡 `PRODUCT-FE-011` — Migrate TechPack count queries (facade-… | `E-03`, `E-04`, `F-06`, `F-08`, `G-08`, `H-01`, `H-02`, `H-03`, `H-04`, `H-05` |
| 5 | 🟡 `PRODUCT-FE-013` — Verify fragment type-conditions, __type… | `F-14` |
| 6 | 🔴 `PRODUCT-FE-001` — Migrate all getProduct documents (singl… | `B-01`, `B-04`, `F-10`, `G-01`, `G-02`, `G-03`, `G-06`, `G-07`, `G-08`, `G-09`, `G-10`, `G-13`, `G-14` |
| 6 | 🔴 `PRODUCT-FE-002` — Migrate getProducts documents (list/sea… | `B-02`, `G-13` |
| 6 | 🟡 `PRODUCT-FE-004` — Migrate getProductStatus documents | `B-01`, `B-02`, `B-03`, `F-10`, `G-06`, `G-07`, `G-09`, `G-13` |
| 6 | 🟡 `PRODUCT-FE-005` — Migrate getProductTemplates documents | `B-03`, `C-02`, `C-03`, `G-03`, `G-04`, `G-06`, `G-07`, `G-08`, `G-13`, `G-14` |
| 6 | 🔴 `PRODUCT-FE-010` — Migrate partner drop/undrop orchestrati… | `D-09` |
| 7 | 🟡 `PRODUCT-FE-009` — Migrate team and partner assignment mut… | `D-06`, `D-07`, `D-12` |
| 7 | 🟡 `PRODUCT-FE-012` — Migrate component status mutations and … | `D-18`, `E-02` |

- **FE cutover flow:** `PRODUCT-FE-003` → `PRODUCT-FE-008` → `PRODUCT-FE-006` → `PRODUCT-FE-007` → `PRODUCT-FE-011` → `PRODUCT-FE-013` → `PRODUCT-FE-001` → `PRODUCT-FE-002` → `PRODUCT-FE-004` → `PRODUCT-FE-005` → `PRODUCT-FE-010` → `PRODUCT-FE-009` → `PRODUCT-FE-012`.

**④ Domain done ≈ d428 (sprint 43)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## Domain 3 — BOM

> **37 BE + 7 FE stories** · High complexity, search-gated list views — pulled up to feed impression FE

**① Backend builds first** — window **d200–d291 (spr 21–30)** (≈ 91 days, 62–120).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d247** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `A-04` → `A-05`.
- **Starts with** `B-01` — getBomByIds data fetcher (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d247):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟡 `A-04` | @DgsTypeResolver for the 2 BOM interfaces | `BOM-FE-002`, `BOM-FE-007` |
| 🟢 `B-01` | getBomByIds data fetcher | `BOM-FE-002`, `BOM-FE-007` |
| 🟢 `B-03` | getBomStatus (cacheable master data) | `BOM-FE-002`, `BOM-FE-007` |
| 🟢 `B-04` | getBomByParentId data fetcher | `BOM-FE-002`, `BOM-FE-007` |
| 🟡 `B-05` | getBomMaterialTypes (merge with Material Hub) | `BOM-FE-004` |
| 🟢 `B-06` | getBomPackagingMaterialTypes (cacheable) | `BOM-FE-004` |
| 🟢 `B-07` | getBomPackagingSubstrates (cacheable) | `BOM-FE-004` |
| 🟢 `B-08` | getBomPackagingUnitOfMeasure (cacheable) | `BOM-FE-004` |
| 🟢 `C-01` | getBomElastic data fetcher | `BOM-FE-003` |
| 🟡 `C-03` | getComboSupplierForBom data fetcher | `BOM-FE-005` |
| 🟢 `C-04` | getValidTrimSuppliersForBom data fetcher | `BOM-FE-005` |
| 🟢 `C-05` | getValidRawMaterialSuppliersForBom data fetch… | `BOM-FE-005` |
| 🟡 `D-01` | addBom mutation | `BOM-FE-006` |
| 🟢 `D-03` | lockBom mutation | `BOM-FE-006` |
| 🟢 `D-04` | unlockBom mutation | `BOM-FE-006` |
| 🟢 `D-05` | updateBomComponentStatus mutation | `BOM-FE-006` |
| 🟡 `G-01` | Bom field resolvers (9 shared fields) | `BOM-FE-002`, `BOM-FE-003`, `BOM-FE-007` |
| 🟡 `G-03` | BomMaterial field resolvers (8 fields) | `BOM-FE-002`, `BOM-FE-007` |
| 🟠 `G-08` | BomTrimMaterial field resolvers (7 fields) — … | `BOM-FE-002`, `BOM-FE-007` |
| 🟡 `G-12` | BomTrimLibraryImpressionDetails field resolve… | `BOM-FE-002`, `BOM-FE-007` |
| 🟢 `G-13` | BomTrimZipperLibraryImpressionDetails field r… | `BOM-FE-002`, `BOM-FE-007` |
| 🟢 `G-14` | Trivial pass-through fields (bundle) | `BOM-FE-003`, `BOM-FE-004`, `BOM-FE-007` |
| 🟡 `G-17` | supplier entity references on material rows (… | `BOM-FE-002`, `BOM-FE-007` |

**③ Frontend cutover** — window **d428–d466 (spr 43–47)**, gated by: BE BOM A–E done (d247) + pilot soak (d342).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 1 | 🔴 `BOM-FE-001` — Statically expand BOM fragment factorie… | — |
| 3 | 🟡 `BOM-FE-005` — Migrate BOM supplier reads | `C-03`, `C-04`, `C-05` |
| 4 | 🔴 `BOM-FE-002` — Migrate BOM core reads | `A-04`, `B-01`, `B-03`, `B-04`, `G-01`, `G-03`, `G-08`, `G-12`, `G-13`, `G-17` |
| 4 | 🟢 `BOM-FE-004` — Migrate BOM master-data reads | `B-05`, `B-06`, `B-07`, `B-08`, `G-14` |
| 5 | 🔴 `BOM-FE-003` — Migrate BOM search and elastic reads | `C-01`, `G-01`, `G-14` |
| 5 | 🔴 `BOM-FE-006` — Migrate BOM mutations including updateB… | `D-01`, `D-03`, `D-04`, `D-05` |
| 5 | 🟢 `BOM-FE-007` — Adopt BOM supplier entity references (o… | `A-04`, `B-01`, `B-03`, `B-04`, `G-01`, `G-03`, `G-08`, `G-12`, `G-13`, `G-14`, `G-17` |

- **FE cutover flow:** `BOM-FE-001` → `BOM-FE-005` → `BOM-FE-002` → `BOM-FE-004` → `BOM-FE-003` → `BOM-FE-006` → `BOM-FE-007`.

**④ Domain done ≈ d466 (sprint 47)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## Domain 4 — Impression

> **7 BE + 2 FE stories** · Prioritized for an external team; FE flips with its BOM / Product partners

**① Backend builds first** — window **d291–d304 (spr 30–31)** (≈ 14 days, 9–18).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d297** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `B-02`.
- **Starts with** `B-01` — searchImpressionsByProductId data fetcher (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d297):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟢 `B-01` | searchImpressionsByProductId data fetcher | `IMPRESSION-FE-001`, `IMPRESSION-FE-002` |
| 🟢 `G-01` | Impression field resolvers (5 fields) | `IMPRESSION-FE-001`, `IMPRESSION-FE-002` |
| 🟡 `G-02` | ImpressionCount.counts aggregation | `IMPRESSION-FE-002` |

**③ Frontend cutover** — window **d466–d470 (spr 47–47)**, gated by: BE Impression A–E done (d297) + pilot soak (d342).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 3 | 🟢 `IMPRESSION-FE-001` — Migrate getBomDataAndImpressions (with … | `B-01`, `G-01` |
| 4 | 🟢 `IMPRESSION-FE-002` — Migrate getCarryForwardFormData (with P… | `B-01`, `G-01`, `G-02` |

- **FE cutover flow:** `IMPRESSION-FE-001` → `IMPRESSION-FE-002`.

**④ Domain done ≈ d470 (sprint 47)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## Domain 5 — Product Details

> **12 BE + 3 FE stories** · Small, isolated, no shared blockers

**① Backend builds first** — window **d336–d366 (spr 34–37)** (≈ 31 days, 21–41).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d356** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `C-01`.
- **Starts with** `B-01` — getProductDetailsById(ids) (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d356):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟢 `B-01` | getProductDetailsById(ids) | `PDTL-FE-001` |
| 🟡 `D-01` | createProductDetailsSet | `PDTL-FE-002` |
| 🟢 `D-03` | productDetailLockUnlock | `PDTL-FE-002` |
| 🟡 `D-04` | cloneFilesForProductDetails | `PDTL-FE-002` |
| 🟢 `D-05` | updateProductDetailComponentStatus | `PDTL-FE-002` |
| 🟠 `E-01` | updateProductDetailsSet (multi-step write) | `PDTL-FE-003` |
| 🟡 `G-01` | access + currentUserPermissions + participant… | `PDTL-FE-001` |
| 🟡 `G-02` | product + createdBy + updatedBy + businessPar… | `PDTL-FE-001` |
| 🟡 `G-03` | attachment + item attachment/constructionSetA… | `PDTL-FE-001` |

**③ Frontend cutover** — window **d470–d480 (spr 47–48)**, gated by: BE Product Details A–E done (d356).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 3 | 🟡 `PDTL-FE-002` — Migrate product-details simple mutations | `D-01`, `D-03`, `D-04`, `D-05` |
| 4 | 🟢 `PDTL-FE-001` — Migrate product-details reads | `B-01`, `G-01`, `G-02`, `G-03` |
| 4 | 🟡 `PDTL-FE-003` — Migrate updateProductDetailsSet saga ha… | `E-01` |

- **FE cutover flow:** `PDTL-FE-002` → `PDTL-FE-001` → `PDTL-FE-003`.

**④ Domain done ≈ d480 (sprint 48)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## Domain 6 — Measurement

> **30 BE + 4 FE stories** · Parallel with the other small domains

**① Backend builds first** — window **d366–d423 (spr 37–43)** (≈ 56 days, 38–75).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d408** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `B-06` → `D-08`.
- **Starts with** `B-01` — getMeasurementByIds data fetcher (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d408):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟢 `B-01` | getMeasurementByIds data fetcher | `MST-FE-001`, `MST-FE-002` |
| 🟢 `B-02` | getUnitsOfMeasure (cacheable) | `MST-FE-003` |
| 🟢 `B-03` | getThicknessUnitsOfMeasure (cacheable) | `MST-FE-003` |
| 🟢 `B-04` | getMeasurementSetStatus (cacheable) | `MST-FE-001`, `MST-FE-003` |
| 🟡 `C-01` | getMeasurements data fetcher (relationship + … | `MST-FE-002` |
| 🟢 `C-02` | getMeasurementsElastic data fetcher | `MST-FE-002` |
| 🟢 `D-03` | lockMeasurementSet mutation | `MST-FE-004` |
| 🟢 `D-04` | unlockMeasurementSet mutation | `MST-FE-004` |
| 🟡 `D-06` | putSampleMeasurementSet mutation | `MST-FE-004` |
| 🟢 `D-07` | deleteSampleMeasurementSet mutation | `MST-FE-004` |
| 🟡 `G-01` | Measurement field resolvers (13 fields) | `MST-FE-001`, `MST-FE-002` |
| 🟢 `G-07` | TightFit field resolvers (5 fields) | `MST-FE-001`, `MST-FE-002` |

**③ Frontend cutover** — window **d480–d495 (spr 48–50)**, gated by: BE Measurement A–E done (d408).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 3 | 🟢 `MST-FE-003` — Migrate measurement master-data reads | `B-02`, `B-03`, `B-04` |
| 4 | 🟡 `MST-FE-004` — Migrate measurement mutations | `D-03`, `D-04`, `D-06`, `D-07` |
| 5 | 🟡 `MST-FE-001` — Migrate measurement reads and retire hu… | `B-01`, `B-04`, `G-01`, `G-07` |
| 5 | 🟡 `MST-FE-002` — Migrate measurement list/search reads | `B-01`, `C-01`, `C-02`, `G-01`, `G-07` |

- **FE cutover flow:** `MST-FE-003` → `MST-FE-004` → `MST-FE-001` → `MST-FE-002`.

**④ Domain done ≈ d495 (sprint 50)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## Domain 7 — Packaging

> **23 BE + 5 FE stories** · Parallel with the other small domains

**① Backend builds first** — window **d423–d478 (spr 43–48)** (≈ 54 days, 37–72).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d460** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `B-02`.
- **Starts with** `B-01` — getPackagings(...) (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d460):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟢 `B-01` | getPackagings(...) | `PKG-FE-001` |
| 🟢 `B-02` | getPackagingById(packagingId) | `PKG-FE-001` |
| 🟢 `B-03` | getDielines(...) | `PKG-FE-003` |
| 🟢 `B-04` | getPackagingFieldValuesByType(type, ids) | `PKG-FE-002` |
| 🟢 `B-05` | getDielineEvaluationStatuses (cacheable) | `PKG-FE-003` |
| 🟢 `B-06` | getCountries(codes) (cacheable) | `PKG-FE-002` |
| 🟡 `D-01` | addPackaging | `PKG-FE-004` |
| 🟢 `D-02` | evaluateDieline | `PKG-FE-003` |
| 🟡 `D-03` | bulkAddPackagings | `PKG-FE-004` |
| 🟡 `D-04` | bulkUpdatePackagings | `PKG-FE-004` |
| 🟢 `D-05` | exportPackaging | `PKG-FE-004` |
| 🟢 `D-06` | lockPackaging | `PKG-FE-004` |
| 🟢 `D-07` | unlockPackaging | `PKG-FE-004` |
| 🟢 `D-09` | updatePackagingComponentStatus | `PKG-FE-004` |
| 🟠 `E-01` | updatePackaging (multi-step write) | `PKG-FE-005` |
| 🟡 `G-01` | access + businessPartner + participantDetails | `PKG-FE-001` |
| 🟢 `G-02` | createdBy + updatedBy + dielineEvaluators | `PKG-FE-001` |
| 🟠 `G-04` | suggestedRetailPriceByDPCI + waveDescription … | `PKG-FE-001` |
| 🟡 `G-05` | Dieline + PrinterDieline + PackagingElement f… | `PKG-FE-003` |

**③ Frontend cutover** — window **d495–d522 (spr 50–53)**, gated by: BE Packaging A–E done (d460).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 3 | 🟢 `PKG-FE-002` — Migrate packaging master-data reads and… | `B-04`, `B-06` |
| 4 | 🟡 `PKG-FE-004` — Migrate packaging simple mutations and … | `D-01`, `D-03`, `D-04`, `D-05`, `D-06`, `D-07`, `D-09` |
| 5 | 🟡 `PKG-FE-001` — Migrate packaging reads | `B-01`, `B-02`, `G-01`, `G-02`, `G-04` |
| 5 | 🟡 `PKG-FE-003` — Migrate dieline flows | `B-03`, `B-05`, `D-02`, `G-05` |
| 5 | 🔴 `PKG-FE-005` — Migrate updatePackaging saga handling a… | `E-01` |

- **FE cutover flow:** `PKG-FE-002` → `PKG-FE-004` → `PKG-FE-001` → `PKG-FE-003` → `PKG-FE-005`.

**④ Domain done ≈ d522 (sprint 53)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## Domain 8 — Claims

> **20 BE + 4 FE stories** · First cross-subgraph cutover (`spark-claims`)

**① Backend builds first** — window **d478–d528 (spr 48–53)** (≈ 50 days, 34–66).

The backend engineer works this domain's phases in dependency steps. The frontend flip can begin once the **A–E** stories the FE stories depend on are live (≈ **d507** — reads, search, writes); the trailing **F/G** federation stitches and field-resolver parity land after the flip and don't block it.

- **Backend critical path (longest chain):** `B-01` → `G-06` → `G-03`.
- **Starts with** `B-01` — getClaims(parentHumanId, claimHumanIds, partn… (the module scaffold every other story waits on).

**② Frontend can start after these backend stories ship** (the FE gate, ≈ d507):

| BE story | What it delivers | Unlocks FE |
|---|---|---|
| 🟢 `B-01` | getClaims(parentHumanId, claimHumanIds, partn… | `CLAIM-FE-002` |
| 🟢 `B-02` | getClaimByIds(claimHumanIds) | `CLAIM-FE-002` |
| 🟢 `B-03` | getCommunicationChannels (cacheable) | `CLAIM-FE-002` |
| 🟢 `B-04` | getAllClaimsAbout (cacheable) | `CLAIM-FE-002` |
| 🟡 `D-01` | createClaim | `CLAIM-FE-003` |
| 🟡 `D-02` | bulkUpdateClaim | `CLAIM-FE-003` |
| 🟢 `D-03` | requestClaimExport | `CLAIM-FE-003` |
| 🟢 `D-04` | lockClaim | `CLAIM-FE-003` |
| 🟢 `D-05` | unlockClaim | `CLAIM-FE-003` |
| 🟠 `E-01` | updateClaim (proxy ACL + multi-step write) | `CLAIM-FE-004` |
| 🟡 `G-01` | access + currentUserPermissions + participant… | `CLAIM-FE-002` |
| 🟡 `G-02` | createdBy + updatedBy + businessPartner + des… | `CLAIM-FE-002` |
| 🟠 `G-03` | product + parentDetails (otherClaimBps / syst… | `CLAIM-FE-002` |

**③ Frontend cutover** — window **d522–d544 (spr 53–55)**, gated by: BE Claims A–E done (d507).

Reads flip first, then writes, then the multi-step saga — one FE story per stage:

| Stage | FE story | Waits on (BE) |
|---|---|---|
| 1 | 🟡 `CLAIM-FE-001` — Split the claim fragment factory and re… | — |
| 3 | 🟡 `CLAIM-FE-003` — Migrate claim simple mutations and expo… | `D-01`, `D-02`, `D-03`, `D-04`, `D-05` |
| 4 | 🔴 `CLAIM-FE-002` — Migrate claim reads (first cross-subgra… | `B-01`, `B-02`, `B-03`, `B-04`, `G-01`, `G-02`, `G-03` |
| 4 | 🔴 `CLAIM-FE-004` — Migrate updateClaim multi-step write ha… | `E-01` |

- **FE cutover flow:** `CLAIM-FE-001` → `CLAIM-FE-003` → `CLAIM-FE-002` → `CLAIM-FE-004`.

**④ Domain done ≈ d544 (sprint 55)** — the last FE story is flipped and stable. Backend F/G parity leftovers for this domain may trail post-flip while the backend engineer is already on the next domain.

---

## How this reconciles with the other docs

- Same numbers, two-lane view: [01-implementation-plan-1BE-1FE.md](01-implementation-plan-1BE-1FE.md) (backend lane + frontend lane tables).
- Step/edge detail per story: [00-sequencing.md](00-sequencing.md) and the compact [00-dependency-map.md](00-dependency-map.md) / [03-linear-dependency-map.md](03-linear-dependency-map.md).
- Cross-domain gates (the ⛔ blockers, e.g. every domain's `E-01` waiting on `PRODUCT-BE-E-00`): [cross-domain-dependencies.md](../analysis/program/cross-domain-dependencies.md).
- Team size + domain order: `team_config.py` — change there and regenerate.

---
*Domain rollout plan · generated 2026-07-24 by generate_domain_rollout.py.*