# Product — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [product/be-04-stories.md](../../../output/analysis/product/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

One box per **phase** (reads, search, mutations, complex ops, federation, field resolvers, entity resolution) — not one box per story, which stops being readable past a couple dozen stories. An arrow between two phase boxes means at least one story in the target phase directly depends on a story in the source phase; the label is how many story-level dependencies that represents. 🔬/⛔ on a box means at least one story in that phase is spike- or cross-subgraph-gated — see the table below for exactly which one.

```mermaid
flowchart TD
  PHB["📖 Phase B<br/>Core Reads<br/>(11 stories) 🔬"]
  PHC["🔍 Phase C<br/>Search & Listing<br/>(5 stories) 🔬"]
  PHD["✏️ Phase D<br/>Mutations<br/>(18 stories) 🔬"]
  PHE["⚙️ Phase E<br/>Complex Operations<br/>(5 stories) 🔬"]
  PHF["🔗 Phase F<br/>Federation & Stitching<br/>(8 stories)"]
  PHG["🧪 Phase G<br/>Field Resolvers & Tests<br/>(16 stories) 🔬"]
  PHH["🧬 Phase H<br/>Entity Resolution<br/>(6 stories) ⛔"]
  PHE -->|4 deps| PHF
  PHE -->|5 deps| PHH
  PHH -->|6 deps| PHF
  PHB -->|1 dep| PHH
```

**Story-level detail** (every story in this domain, its phase, its direct `Depends on:`, and any gate):

| Story | Phase | Depends on | Gate |
|---|---|---|---|
| `B-01` — getProduct(id) | B | — | — |
| `B-02` — getProductsByIds(ids) | B | — | — |
| `B-03` — getProductStatus (cacheable) | B | — | — |
| `B-04` — getProductVersions(id) | B | — | — |
| `B-05` — getCopyStatus(id) | B | — | — |
| `B-06` — getProductTemplateById(id) | B | — | — |
| `B-07` — getProductRules | B | — | — |
| `B-08` — getProductRulesById(id) | B | — | — |
| `B-09` — getAllAvailableRules | B | — | — |
| `B-10` — getProductDeptRules(productIds, departmentIds, activeOnly) | B | — | 🔬 SPIKE-07 |
| `B-11` — getProductBPRules(productIds, businessPartnerIds, activeOnly) | B | — | 🔬 SPIKE-07 |
| `C-01` — getProducts(...) two-stage hydration | C | — | 🔬 SPIKE-06a |
| `C-02` — getProductTemplates(...) | C | — | — |
| `C-03` — getCategories(...) | C | — | — |
| `C-04` — getRatingByTcin(tcin) (external rating) | C | — | — |
| `C-05` — searchProductRules(...) | C | — | 🔬 SPIKE-07 |
| `D-01` — addProduct | D | — | 🔬 SPIKE-06b |
| `D-02` — addProducts (bulk) | D | — | 🔬 SPIKE-06b |
| `D-03` — bulkUpdateProducts | D | — | — |
| `D-04` — updateProduct | D | — | 🔬 SPIKE-06b |
| `D-05` — carryForwardProduct | D | — | — |
| `D-06` — addTeamsToProduct 🔀 Collab Canvas | D | — | — |
| `D-07` — addBusinessPartnersToProductWithType 🔀 Collab Canvas | D | — | — |
| `D-08` — removeProductResources | D | — | — |
| `D-09` — updateBusinessPartnerStatuses | D | — | — |
| `D-10` — updateViewToggle | D | — | — |
| `D-11` — updateWorkspaceAttributes 🔀 Collab Canvas | D | — | — |
| `D-12` — updateProductTeamsWorkspaceContext | D | — | — |
| `D-13` — linkProduct | D | — | — |
| `D-14` — unlinkProduct | D | — | — |
| `D-15` — addProductRule | D | — | — |
| `D-16` — updateProductRule | D | — | — |
| `D-17` — deleteProductRule | D | — | — |
| `D-18` — updateComponentStatus (bulk) | D | — | — |
| `E-00` — WriteSaga shared module (Sprint 0, critical path) | E | — | 🔬 SPIKE-01 |
| `E-01` — productBusinessPartnerActions (REMOVE/DROP/UNDROP) | E | `E-00` | 🔬 SPIKE-03 |
| `E-02` — updateComponentStatuses (5-loader fan-out) | E | `E-00` | 🔬 SPIKE-01 |
| `E-03` — getProductTechPackCountV1 stub + aggregation facade (facade-then-federate, Phase 1) | E | — | 🔬 SPIKE-02 |
| `E-04` — getProductTechPackBulkCountV1 (bulk wrapper, ordering fix) | E | `E-03` | 🔬 SPIKE-02 |
| `F-04` — ResourcesCount.measurementSets (internal, from Measurement) | F | `E-03` | — |
| `F-06` — ResourcesCount.productBoms + packagingBoms + boms (internal, from BOM) | F | `E-03` | — |
| `F-08` — ResourcesCount.watchlists (internal, from Watchlist) | F | `E-03` | — |
| `F-09` — Retire the TechPack aggregation facade | F | `F-04`, `F-06`, `F-08`, `H-01`, `H-02`, `H-03`, `H-04`, `H-05` | — |
| `F-10` — Hive Gateway supergraph composition | F | `F-14`, `H-06` | — |
| `F-11` — Platform stub verification (VMM/IG/Doppler/CORONA/APEX) | F | `F-10` | — |
| `F-12` — Deferred partner-wrapper decision (drift mutations) | F | `E-01` | — |
| `F-14` — Cross-subgraph contract alignment (keys, type names, paged wrappers) | F | — | — |
| `G-01` — Product.attachmentsWithMetaData | G | — | — |
| `G-02` — Product.components | G | — | — |
| `G-03` — Product.attachments + attachmentsV3 + attachmentSummary + ProductTemplate.attachmentsData | G | `G-01` | — |
| `G-04` — ProductsCategories.categories (12-case) + DopplerDepartment fields | G | — | — |
| `G-05` — Product.samples + sampleIds + elasticSamplesList | G | — | — |
| `G-06` — Product.teams + discussionsV2 + discussionsCount + workspaces | G | — | — |
| `G-07` — Product.vendorAttributes + businessPartners + droppedPartners + unDroppablePartners + status | G | — | 🔬 SPIKE-04 |
| `G-08` — Product.measurementSets + claims + bom + productBom + packagingBom + productDetails + variations + associateProductsAsks | G | — | — |
| `G-09` — Product.productWorkspaceAttributes + productWorkspaceInfo | G | — | — |
| `G-10` — Product.ancestryProducts + rating + reservedDpcis | G | — | — |
| `G-11-1` — Product.notRemovablePartnerIds + notRemovableWorkspaceIds | G | — | 🔬 SPIKE-04 |
| `G-11-2` — Product.associateProductsAsks + Product.variations | G | — | — |
| `G-13` — IG/tag/tcin/spg + template trivial-field group | G | — | — |
| `G-14` — Simple user/status fields + trivial pass-throughs (bundle) | G | — | — |
| `G-15` — Port product utils to Kotlin | G | — | — |
| `G-17` — Entity references on partner/lineage value types (recommended, PO-gated) | G | `G-01` | — |
| `H-01` — ResourcesCount.productAttachments + discussionAttachments (federated, from Attachment) | H | `E-03` | ⛔ BLOCKED-BY attachment domain (⛔ cross-subgraph — does not ship until plm-attachment is live) |
| `H-02` — ResourcesCount.discussions (federated, from Discussion) | H | `E-03` | ⛔ BLOCKED-BY discussion domain (⛔ cross-subgraph) |
| `H-03` — ResourcesCount.sample (federated, from Sample) | H | `E-03` | ⛔ BLOCKED-BY sample domain (⛔ cross-subgraph) |
| `H-04` — ResourcesCount.claims (federated, from Claim) | H | `E-03` | ⛔ BLOCKED-BY claim domain (⛔ cross-subgraph) |
| `H-05` — ResourcesCount.constructions (federated, from Construction) | H | `E-03` | ⛔ BLOCKED-BY construction domain (⛔ cross-subgraph) |
| `H-06` — Product entity fetcher (@DgsEntityFetcher) for cross-subgraph references | H | `B-01` | — |

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

### PRODUCT-FE-001 · Migrate all `getProduct` documents (single root query, 17 flavors)

```mermaid
flowchart LR
  NB_01["B-01<br/>getProduct(id)"]
  NB_04["B-04<br/>getProductVersions(id)"]
  NF_10["F-10<br/>Hive Gateway supergraph com…"]
  NG_01["G-01<br/>Product.attachmentsWithMeta…"]
  NG_02["G-02<br/>Product.components"]
  NG_03["G-03<br/>Product.attachments + attac…"]
  NG_06["G-06<br/>Product.teams + discussions…"]
  NG_07["G-07<br/>Product.vendorAttributes +…"]
  NG_08["G-08<br/>Product.measurementSets + c…"]
  NG_09["G-09<br/>Product.productWorkspaceAtt…"]
  NG_10["G-10<br/>Product.ancestryProducts +…"]
  NG_13["G-13<br/>IG/tag/tcin/spg + template…"]
  NG_14["G-14<br/>Simple user/status fields +…"]
  NPRODUCT_FE_001(["PRODUCT-FE-001"])
  NB_01 ==> NPRODUCT_FE_001
  NF_10 ==> NPRODUCT_FE_001
  NG_01 ==> NPRODUCT_FE_001
  NG_02 ==> NPRODUCT_FE_001
  NG_03 ==> NPRODUCT_FE_001
  NG_06 ==> NPRODUCT_FE_001
  NG_07 ==> NPRODUCT_FE_001
  NG_08 ==> NPRODUCT_FE_001
  NG_09 ==> NPRODUCT_FE_001
  NG_10 ==> NPRODUCT_FE_001
  NG_13 ==> NPRODUCT_FE_001
  NG_14 ==> NPRODUCT_FE_001
  NB_04 ==> NPRODUCT_FE_001
```

### PRODUCT-FE-002 · Migrate `getProducts` documents (list/search/bulk-create)

```mermaid
flowchart LR
  NB_02["B-02<br/>getProductsByIds(ids)"]
  NG_13["G-13<br/>IG/tag/tcin/spg + template…"]
  NPRODUCT_FE_002(["PRODUCT-FE-002"])
  NB_02 ==> NPRODUCT_FE_002
  NG_13 ==> NPRODUCT_FE_002
```

### PRODUCT-FE-003 · Migrate `getProductsByIds` documents (bulk-by-id reads)

```mermaid
flowchart LR
  NB_03["B-03<br/>getProductStatus (cacheable)"]
  NPRODUCT_FE_003(["PRODUCT-FE-003"])
  NB_03 ==> NPRODUCT_FE_003
```

### PRODUCT-FE-004 · Migrate `getProductStatus` documents

```mermaid
flowchart LR
  NB_01["B-01<br/>getProduct(id)"]
  NB_02["B-02<br/>getProductsByIds(ids)"]
  NB_03["B-03<br/>getProductStatus (cacheable)"]
  NF_10["F-10<br/>Hive Gateway supergraph com…"]
  NG_06["G-06<br/>Product.teams + discussions…"]
  NG_07["G-07<br/>Product.vendorAttributes +…"]
  NG_09["G-09<br/>Product.productWorkspaceAtt…"]
  NG_13["G-13<br/>IG/tag/tcin/spg + template…"]
  NPRODUCT_FE_004(["PRODUCT-FE-004"])
  NB_01 ==> NPRODUCT_FE_004
  NB_02 ==> NPRODUCT_FE_004
  NB_03 ==> NPRODUCT_FE_004
  NF_10 ==> NPRODUCT_FE_004
  NG_06 ==> NPRODUCT_FE_004
  NG_07 ==> NPRODUCT_FE_004
  NG_09 ==> NPRODUCT_FE_004
  NG_13 ==> NPRODUCT_FE_004
```

### PRODUCT-FE-005 · Migrate `getProductTemplates` documents

```mermaid
flowchart LR
  NB_03["B-03<br/>getProductStatus (cacheable)"]
  NC_02["C-02<br/>getProductTemplates(...)"]
  NC_03["C-03<br/>getCategories(...)"]
  NG_03["G-03<br/>Product.attachments + attac…"]
  NG_04["G-04<br/>ProductsCategories.categori…"]
  NG_06["G-06<br/>Product.teams + discussions…"]
  NG_07["G-07<br/>Product.vendorAttributes +…"]
  NG_08["G-08<br/>Product.measurementSets + c…"]
  NG_13["G-13<br/>IG/tag/tcin/spg + template…"]
  NG_14["G-14<br/>Simple user/status fields +…"]
  NPRODUCT_FE_005(["PRODUCT-FE-005"])
  NB_03 ==> NPRODUCT_FE_005
  NC_02 ==> NPRODUCT_FE_005
  NC_03 ==> NPRODUCT_FE_005
  NG_03 ==> NPRODUCT_FE_005
  NG_04 ==> NPRODUCT_FE_005
  NG_06 ==> NPRODUCT_FE_005
  NG_07 ==> NPRODUCT_FE_005
  NG_08 ==> NPRODUCT_FE_005
  NG_13 ==> NPRODUCT_FE_005
  NG_14 ==> NPRODUCT_FE_005
```

### PRODUCT-FE-006 · Migrate `getCategories` documents

```mermaid
flowchart LR
  NG_03["G-03<br/>Product.attachments + attac…"]
  NG_13["G-13<br/>IG/tag/tcin/spg + template…"]
  NPRODUCT_FE_006(["PRODUCT-FE-006"])
  NG_03 ==> NPRODUCT_FE_006
  NG_13 ==> NPRODUCT_FE_006
```

### PRODUCT-FE-007 · Migrate product rules administration

```mermaid
flowchart LR
  NB_07["B-07<br/>getProductRules"]
  NB_08["B-08<br/>getProductRulesById(id)"]
  NB_09["B-09<br/>getAllAvailableRules"]
  NB_10["B-10<br/>getProductDeptRules(product…"]
  NB_11["B-11<br/>getProductBPRules(productId…"]
  NC_05["C-05<br/>searchProductRules(...)"]
  ND_15["D-15<br/>addProductRule"]
  ND_16["D-16<br/>updateProductRule"]
  ND_17["D-17<br/>deleteProductRule"]
  NG_07["G-07<br/>Product.vendorAttributes +…"]
  NG_13["G-13<br/>IG/tag/tcin/spg + template…"]
  NPRODUCT_FE_007(["PRODUCT-FE-007"])
  NB_07 ==> NPRODUCT_FE_007
  NB_08 ==> NPRODUCT_FE_007
  NB_09 ==> NPRODUCT_FE_007
  NB_10 ==> NPRODUCT_FE_007
  NB_11 ==> NPRODUCT_FE_007
  NC_05 ==> NPRODUCT_FE_007
  ND_15 ==> NPRODUCT_FE_007
  ND_16 ==> NPRODUCT_FE_007
  ND_17 ==> NPRODUCT_FE_007
  NG_07 ==> NPRODUCT_FE_007
  NG_13 ==> NPRODUCT_FE_007
```

### PRODUCT-FE-008 · Migrate simple product mutations

```mermaid
flowchart LR
  ND_01["D-01<br/>addProduct"]
  ND_02["D-02<br/>addProducts (bulk)"]
  ND_03["D-03<br/>bulkUpdateProducts"]
  ND_04["D-04<br/>updateProduct"]
  ND_05["D-05<br/>carryForwardProduct"]
  ND_10["D-10<br/>updateViewToggle"]
  ND_13["D-13<br/>linkProduct"]
  ND_14["D-14<br/>unlinkProduct"]
  NPRODUCT_FE_008(["PRODUCT-FE-008"])
  ND_01 ==> NPRODUCT_FE_008
  ND_02 ==> NPRODUCT_FE_008
  ND_03 ==> NPRODUCT_FE_008
  ND_04 ==> NPRODUCT_FE_008
  ND_05 ==> NPRODUCT_FE_008
  ND_10 ==> NPRODUCT_FE_008
  ND_13 ==> NPRODUCT_FE_008
  ND_14 ==> NPRODUCT_FE_008
```

### PRODUCT-FE-009 · Migrate team and partner assignment mutations

```mermaid
flowchart LR
  ND_06["D-06<br/>addTeamsToProduct 🔀 Collab…"]
  ND_07["D-07<br/>addBusinessPartnersToProduc…"]
  ND_12["D-12<br/>updateProductTeamsWorkspace…"]
  NPRODUCT_FE_009(["PRODUCT-FE-009"])
  ND_06 ==> NPRODUCT_FE_009
  ND_07 ==> NPRODUCT_FE_009
  ND_12 ==> NPRODUCT_FE_009
```

### PRODUCT-FE-010 · Migrate partner drop/undrop orchestration

```mermaid
flowchart LR
  ND_09["D-09<br/>updateBusinessPartnerStatus…"]
  NPRODUCT_FE_010(["PRODUCT-FE-010"])
  ND_09 ==> NPRODUCT_FE_010
```

### PRODUCT-FE-011 · Migrate TechPack count queries (facade-then-federate)

```mermaid
flowchart LR
  NE_03["E-03<br/>getProductTechPackCountV1 s…"]
  NE_04["E-04<br/>getProductTechPackBulkCount…"]
  NF_06["F-06<br/>ResourcesCount.productBoms…"]
  NF_08["F-08<br/>ResourcesCount.watchlists (…"]
  NG_08["G-08<br/>Product.measurementSets + c…"]
  NH_01["H-01<br/>ResourcesCount.productAttac…"]
  NH_02["H-02<br/>ResourcesCount.discussions…"]
  NH_03["H-03<br/>ResourcesCount.sample (fede…"]
  NH_04["H-04<br/>ResourcesCount.claims (fede…"]
  NH_05["H-05<br/>ResourcesCount.construction…"]
  NPRODUCT_FE_011(["PRODUCT-FE-011"])
  NE_03 ==> NPRODUCT_FE_011
  NE_04 ==> NPRODUCT_FE_011
  NF_06 ==> NPRODUCT_FE_011
  NF_08 ==> NPRODUCT_FE_011
  NG_08 ==> NPRODUCT_FE_011
  NH_01 ==> NPRODUCT_FE_011
  NH_02 ==> NPRODUCT_FE_011
  NH_03 ==> NPRODUCT_FE_011
  NH_04 ==> NPRODUCT_FE_011
  NH_05 ==> NPRODUCT_FE_011
```

### PRODUCT-FE-012 · Migrate component status mutations and rollup counts

```mermaid
flowchart LR
  ND_18["D-18<br/>updateComponentStatus (bulk)"]
  NE_02["E-02<br/>updateComponentStatuses (5-…"]
  NPRODUCT_FE_012(["PRODUCT-FE-012"])
  ND_18 ==> NPRODUCT_FE_012
  NE_02 ==> NPRODUCT_FE_012
```

### PRODUCT-FE-013 · Verify fragment type-conditions, `__typename` logic and cache keys against federated type names

```mermaid
flowchart LR
  NF_14["F-14<br/>Cross-subgraph contract ali…"]
  NPRODUCT_FE_013(["PRODUCT-FE-013"])
  NF_14 ==> NPRODUCT_FE_013
```

---
*Story dependency graphs · product · generated 2026-07-21.*