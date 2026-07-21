# Product — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [product/be-04-stories.md](../../../output/analysis/product/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

For the engineer implementing this domain's backend: which story unlocks which. Nodes are grouped into swimlanes by **phase** (reads, then search, then mutations, then complex/federation/field-resolver work) — arrows show only the direct `Depends on:` edges. A dashed arrow from a diamond is a **gate** (a Phase-0 spike or a cross-subgraph block) — read-only context, not something the scheduler enforces.

```mermaid
flowchart TD
  subgraph PHB["📖 Phase B — Core Reads"]
    NB_01["B-01<br/>getProduct(id)"]
    NB_02["B-02<br/>getProductsByIds(ids)"]
    NB_03["B-03<br/>getProductStatus (cacheable)"]
    NB_04["B-04<br/>getProductVersions(id)"]
    NB_05["B-05<br/>getCopyStatus(id)"]
    NB_06["B-06<br/>getProductTemplateById(id)"]
    NB_07["B-07<br/>getProductRules"]
    NB_08["B-08<br/>getProductRulesById(id)"]
    NB_09["B-09<br/>getAllAvailableRules"]
    NB_10["B-10<br/>getProductDeptRules(productIds, d…"]
    NB_11["B-11<br/>getProductBPRules(productIds, bus…"]
  end
  subgraph PHC["🔍 Phase C — Search & Listing"]
    NC_01["C-01<br/>getProducts(...) two-stage hydrat…"]
    NC_02["C-02<br/>getProductTemplates(...)"]
    NC_03["C-03<br/>getCategories(...)"]
    NC_04["C-04<br/>getRatingByTcin(tcin) (external r…"]
    NC_05["C-05<br/>searchProductRules(...)"]
  end
  subgraph PHD["✏️ Phase D — Mutations"]
    ND_01["D-01<br/>addProduct"]
    ND_02["D-02<br/>addProducts (bulk)"]
    ND_03["D-03<br/>bulkUpdateProducts"]
    ND_04["D-04<br/>updateProduct"]
    ND_05["D-05<br/>carryForwardProduct"]
    ND_06["D-06<br/>addTeamsToProduct 🔀 Collab Canvas"]
    ND_07["D-07<br/>addBusinessPartnersToProductWithT…"]
    ND_08["D-08<br/>removeProductResources"]
    ND_09["D-09<br/>updateBusinessPartnerStatuses"]
    ND_10["D-10<br/>updateViewToggle"]
    ND_11["D-11<br/>updateWorkspaceAttributes 🔀 Colla…"]
    ND_12["D-12<br/>updateProductTeamsWorkspaceContext"]
    ND_13["D-13<br/>linkProduct"]
    ND_14["D-14<br/>unlinkProduct"]
    ND_15["D-15<br/>addProductRule"]
    ND_16["D-16<br/>updateProductRule"]
    ND_17["D-17<br/>deleteProductRule"]
    ND_18["D-18<br/>updateComponentStatus (bulk)"]
  end
  subgraph PHE["⚙️ Phase E — Complex Operations"]
    NE_00["E-00<br/>WriteSaga shared module (Sprint 0…"]
    NE_01["E-01<br/>productBusinessPartnerActions (RE…"]
    NE_02["E-02<br/>updateComponentStatuses (5-loader…"]
    NE_03["E-03<br/>getProductTechPackCountV1 stub +…"]
    NE_04["E-04<br/>getProductTechPackBulkCountV1 (bu…"]
  end
  subgraph PHF["🔗 Phase F — Federation & Stitching"]
    NF_04["F-04<br/>ResourcesCount.measurementSets (i…"]
    NF_06["F-06<br/>ResourcesCount.productBoms + pack…"]
    NF_08["F-08<br/>ResourcesCount.watchlists (intern…"]
    NF_09["F-09<br/>Retire the TechPack aggregation f…"]
    NF_10["F-10<br/>Hive Gateway supergraph compositi…"]
    NF_11["F-11<br/>Platform stub verification (VMM/I…"]
    NF_12["F-12<br/>Deferred partner-wrapper decision…"]
    NF_14["F-14<br/>Cross-subgraph contract alignment…"]
  end
  subgraph PHG["🧪 Phase G — Field Resolvers & Tests"]
    NG_01["G-01<br/>Product.attachmentsWithMetaData"]
    NG_02["G-02<br/>Product.components"]
    NG_03["G-03<br/>Product.attachments + attachments…"]
    NG_04["G-04<br/>ProductsCategories.categories (12…"]
    NG_05["G-05<br/>Product.samples + sampleIds + ela…"]
    NG_06["G-06<br/>Product.teams + discussionsV2 + d…"]
    NG_07["G-07<br/>Product.vendorAttributes + busine…"]
    NG_08["G-08<br/>Product.measurementSets + claims…"]
    NG_09["G-09<br/>Product.productWorkspaceAttribute…"]
    NG_10["G-10<br/>Product.ancestryProducts + rating…"]
    NG_11_1["G-11-1<br/>Product.notRemovablePartnerIds +…"]
    NG_11_2["G-11-2<br/>Product.associateProductsAsks + P…"]
    NG_13["G-13<br/>IG/tag/tcin/spg + template trivia…"]
    NG_14["G-14<br/>Simple user/status fields + trivi…"]
    NG_15["G-15<br/>Port product utils to Kotlin"]
    NG_17["G-17<br/>Entity references on partner/line…"]
  end
  subgraph PHH["🧬 Phase H — Entity Resolution"]
    NH_01["H-01<br/>ResourcesCount.productAttachments…"]
    NH_02["H-02<br/>ResourcesCount.discussions (feder…"]
    NH_03["H-03<br/>ResourcesCount.sample (federated,…"]
    NH_04["H-04<br/>ResourcesCount.claims (federated,…"]
    NH_05["H-05<br/>ResourcesCount.constructions (fed…"]
    NH_06["H-06<br/>Product entity fetcher (@DgsEntit…"]
  end
  NE_00 --> NE_01
  NE_00 --> NE_02
  NE_03 --> NE_04
  NE_03 --> NF_04
  NE_03 --> NF_06
  NE_03 --> NF_08
  NH_01 --> NF_09
  NH_02 --> NF_09
  NH_03 --> NF_09
  NF_04 --> NF_09
  NH_04 --> NF_09
  NF_06 --> NF_09
  NH_05 --> NF_09
  NF_08 --> NF_09
  NH_06 --> NF_10
  NF_14 --> NF_10
  NF_10 --> NF_11
  NE_01 --> NF_12
  NE_03 --> NH_01
  NE_03 --> NH_02
  NE_03 --> NH_03
  NE_03 --> NH_04
  NE_03 --> NH_05
  NB_01 --> NH_06
  NG_01 --> NG_03
  NG_01 --> NG_17
  G__SPIKE_07{{"🔬 SPIKE-07"}}
  G__SPIKE_07 -.-> NB_10
  G__SPIKE_07 -.-> NB_11
  G__SPIKE_06a{{"🔬 SPIKE-06a"}}
  G__SPIKE_06a -.-> NC_01
  G__SPIKE_07 -.-> NC_05
  G__SPIKE_06b{{"🔬 SPIKE-06b"}}
  G__SPIKE_06b -.-> ND_01
  G__SPIKE_06b -.-> ND_02
  G__SPIKE_06b -.-> ND_04
  G__SPIKE_01{{"🔬 SPIKE-01"}}
  G__SPIKE_01 -.-> NE_00
  G__SPIKE_03{{"🔬 SPIKE-03"}}
  G__SPIKE_03 -.-> NE_01
  G__SPIKE_01 -.-> NE_02
  G__SPIKE_02{{"🔬 SPIKE-02"}}
  G__SPIKE_02 -.-> NE_03
  G__SPIKE_02 -.-> NE_04
  G__BLOCKED_BY_attachment_domain____cross_subgraph___does_not_ship_until_plm_attachment_is_live_{{"⛔ BLOCKED-BY attachment domain (⛔ cross-subgraph — does not ship until plm-attachment is live)"}}
  G__BLOCKED_BY_attachment_domain____cross_subgraph___does_not_ship_until_plm_attachment_is_live_ -.-> NH_01
  G__BLOCKED_BY_discussion_domain____cross_subgraph_{{"⛔ BLOCKED-BY discussion domain (⛔ cross-subgraph)"}}
  G__BLOCKED_BY_discussion_domain____cross_subgraph_ -.-> NH_02
  G__BLOCKED_BY_sample_domain____cross_subgraph_{{"⛔ BLOCKED-BY sample domain (⛔ cross-subgraph)"}}
  G__BLOCKED_BY_sample_domain____cross_subgraph_ -.-> NH_03
  G__BLOCKED_BY_claim_domain____cross_subgraph_{{"⛔ BLOCKED-BY claim domain (⛔ cross-subgraph)"}}
  G__BLOCKED_BY_claim_domain____cross_subgraph_ -.-> NH_04
  G__BLOCKED_BY_construction_domain____cross_subgraph_{{"⛔ BLOCKED-BY construction domain (⛔ cross-subgraph)"}}
  G__BLOCKED_BY_construction_domain____cross_subgraph_ -.-> NH_05
  G__SPIKE_04{{"🔬 SPIKE-04"}}
  G__SPIKE_04 -.-> NG_07
  G__SPIKE_04 -.-> NG_11_1
```

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