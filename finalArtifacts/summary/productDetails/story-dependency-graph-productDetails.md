# Product Details — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [productDetails/be-04-stories.md](../../../output/analysis/productDetails/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

One box per **phase** (reads, search, mutations, complex ops, federation, field resolvers, entity resolution) — not one box per story, which stops being readable past a couple dozen stories. An arrow between two phase boxes means at least one story in the target phase directly depends on a story in the source phase; the label is how many story-level dependencies that represents. 🔬/⛔ on a box means at least one story in that phase is spike- or cross-subgraph-gated — see the table below for exactly which one.

```mermaid
flowchart TD
  PHB["📖 Phase B<br/>Core Reads<br/>(1 story)"]
  PHC["🔍 Phase C<br/>Search & Listing<br/>(1 story)"]
  PHD["✏️ Phase D<br/>Mutations<br/>(5 stories)"]
  PHE["⚙️ Phase E<br/>Complex Operations<br/>(1 story) 🔬 ⛔"]
  PHF["🔗 Phase F<br/>Federation & Stitching<br/>(1 story)"]
  PHG["🧪 Phase G<br/>Field Resolvers & Tests<br/>(3 stories)"]
  PHB -->|1 dep| PHC
  PHB -->|5 deps| PHD
  PHB -->|1 dep| PHE
  PHB -->|1 dep| PHF
  PHB -->|3 deps| PHG
```

**Story-level detail** (every story in this domain, its phase, its direct `Depends on:`, and any gate):

| Story | Phase | Depends on | Gate |
|---|---|---|---|
| `B-01` — getProductDetailsById(ids) | B | — | — |
| `C-01` — getProductDetailsElastic(resourceId) | C | `B-01` | — |
| `D-01` — createProductDetailsSet | D | `B-01` | — |
| `D-02` — updateProductDetailAccess | D | `B-01` | — |
| `D-03` — productDetailLockUnlock | D | `B-01` | — |
| `D-04` — cloneFilesForProductDetails | D | `B-01` | — |
| `D-05` — updateProductDetailComponentStatus | D | `B-01` | — |
| `E-01` — updateProductDetailsSet (multi-step write) | E | `B-01` | ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module), 🔬 SPIKE-01 |
| `F-01` — Product.productDetails (internal, same subgraph) | F | `B-01` | — |
| `G-01` — access + currentUserPermissions + participantDetails | G | `B-01` | — |
| `G-02` — product + createdBy + updatedBy + businessPartners + workspaces | G | `B-01` | — |
| `G-03` — attachment + item attachment/constructionSetAttachments + category subCategories | G | `B-01` | — |

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

### PDTL-FE-001 · Migrate product-details reads

```mermaid
flowchart LR
  NB_01["B-01<br/>getProductDetailsById(ids)"]
  NG_01["G-01<br/>access + currentUserPermiss…"]
  NG_02["G-02<br/>product + createdBy + updat…"]
  NG_03["G-03<br/>attachment + item attachmen…"]
  NPDTL_FE_001(["PDTL-FE-001"])
  NB_01 ==> NPDTL_FE_001
  NG_01 ==> NPDTL_FE_001
  NG_02 ==> NPDTL_FE_001
  NG_03 ==> NPDTL_FE_001
```

### PDTL-FE-002 · Migrate product-details simple mutations

```mermaid
flowchart LR
  ND_01["D-01<br/>createProductDetailsSet"]
  ND_03["D-03<br/>productDetailLockUnlock"]
  ND_04["D-04<br/>cloneFilesForProductDetails"]
  ND_05["D-05<br/>updateProductDetailComponen…"]
  NPDTL_FE_002(["PDTL-FE-002"])
  ND_01 ==> NPDTL_FE_002
  ND_03 ==> NPDTL_FE_002
  ND_04 ==> NPDTL_FE_002
  ND_05 ==> NPDTL_FE_002
```

### PDTL-FE-003 · Migrate `updateProductDetailsSet` saga handling

```mermaid
flowchart LR
  NE_01["E-01<br/>updateProductDetailsSet (mu…"]
  NPDTL_FE_003(["PDTL-FE-003"])
  NE_01 ==> NPDTL_FE_003
```

---
*Story dependency graphs · productDetails · generated 2026-07-21.*