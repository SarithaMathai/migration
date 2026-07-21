# Packaging — Story Dependency Graphs

> Generated 2026-07-21 from `be-04-stories.md` and `fe-08-frontend-stories.md` — regenerate via `generate_story_dependency_graphs.py` (also runs inside `generate_all.py`). Full story text (Current Behaviour, Target implementation, Acceptance Criteria): [packaging/be-04-stories.md](../../../output/analysis/packaging/be-04-stories.md).

---

## Graph A — Backend Story Dependency (build order)

One box per **phase** (reads, search, mutations, complex ops, federation, field resolvers, entity resolution) — not one box per story, which stops being readable past a couple dozen stories. An arrow between two phase boxes means at least one story in the target phase directly depends on a story in the source phase; the label is how many story-level dependencies that represents. 🔬/⛔ on a box means at least one story in that phase is spike- or cross-subgraph-gated — see the table below for exactly which one.

```mermaid
flowchart TD
  PHB["📖 Phase B<br/>Core Reads<br/>(6 stories)"]
  PHC["🔍 Phase C<br/>Search & Listing<br/>(1 story)"]
  PHD["✏️ Phase D<br/>Mutations<br/>(9 stories)"]
  PHE["⚙️ Phase E<br/>Complex Operations<br/>(1 story) 🔬 ⛔"]
  PHF["🔗 Phase F<br/>Federation & Stitching<br/>(1 story)"]
  PHG["🧪 Phase G<br/>Field Resolvers & Tests<br/>(5 stories)"]
  PHB -->|1 dep| PHC
  PHB -->|9 deps| PHD
  PHB -->|1 dep| PHE
  PHB -->|1 dep| PHF
  PHB -->|5 deps| PHG
```

**Story-level detail** (every story in this domain, its phase, its direct `Depends on:`, and any gate):

| Story | Phase | Depends on | Gate |
|---|---|---|---|
| `B-01` — getPackagings(...) | B | — | — |
| `B-02` — getPackagingById(packagingId) | B | `B-01` | — |
| `B-03` — getDielines(...) | B | `B-01` | — |
| `B-04` — getPackagingFieldValuesByType(type, ids) | B | `B-01` | — |
| `B-05` — getDielineEvaluationStatuses (cacheable) | B | `B-01` | — |
| `B-06` — getCountries(codes) (cacheable) | B | `B-01` | — |
| `C-01` — getPackagingElastic(parentHumanId) | C | `B-01` | — |
| `D-01` — addPackaging | D | `B-01` | — |
| `D-02` — evaluateDieline | D | `B-01` | — |
| `D-03` — bulkAddPackagings | D | `B-01` | — |
| `D-04` — bulkUpdatePackagings | D | `B-01` | — |
| `D-05` — exportPackaging | D | `B-01` | — |
| `D-06` — lockPackaging | D | `B-01` | — |
| `D-07` — unlockPackaging | D | `B-01` | — |
| `D-08` — cloneFilesForDielines | D | `B-01` | — |
| `D-09` — updatePackagingComponentStatus | D | `B-01` | — |
| `E-01` — updatePackaging (multi-step write) | E | `B-01` | ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module), 🔬 SPIKE-01 |
| `F-01` — Product packaging links (internal, same subgraph) | F | `B-01` | — |
| `G-01` — access + businessPartner + participantDetails | G | `B-01` | — |
| `G-02` — createdBy + updatedBy + dielineEvaluators | G | `B-01` | — |
| `G-03` — product + workspaces + attachments | G | `B-01` | — |
| `G-04` — suggestedRetailPriceByDPCI + waveDescription + retailPrice | G | `B-01` | — |
| `G-05` — Dieline + PrinterDieline + PackagingElement field resolvers | G | `B-01` | — |

---

## Graph B — Frontend Readiness (what must ship before FE can start)

For the frontend engineer or PO checking whether backend is far enough along: **one small diagram per frontend story**, showing only the backend stories it directly depends on. (Any dependency *those* backend stories have on each other is Graph A's job, not repeated here — that's what kept the old single combined diagram unreadable.) A frontend story cannot start until every backend story pointing at it has shipped.

### PKG-FE-001 · Migrate packaging reads

```mermaid
flowchart LR
  NB_01["B-01<br/>getPackagings(...)"]
  NB_02["B-02<br/>getPackagingById(packagingI…"]
  NG_01["G-01<br/>access + businessPartner +…"]
  NG_02["G-02<br/>createdBy + updatedBy + die…"]
  NG_04["G-04<br/>suggestedRetailPriceByDPCI…"]
  NPKG_FE_001(["PKG-FE-001"])
  NB_01 ==> NPKG_FE_001
  NB_02 ==> NPKG_FE_001
  NG_01 ==> NPKG_FE_001
  NG_02 ==> NPKG_FE_001
  NG_04 ==> NPKG_FE_001
```

### PKG-FE-002 · Migrate packaging master-data reads and retire deprecated fields

```mermaid
flowchart LR
  NB_04["B-04<br/>getPackagingFieldValuesByTy…"]
  NB_06["B-06<br/>getCountries(codes) (cachea…"]
  NPKG_FE_002(["PKG-FE-002"])
  NB_04 ==> NPKG_FE_002
  NB_06 ==> NPKG_FE_002
```

### PKG-FE-003 · Migrate dieline flows

```mermaid
flowchart LR
  NB_03["B-03<br/>getDielines(...)"]
  NB_05["B-05<br/>getDielineEvaluationStatuse…"]
  ND_02["D-02<br/>evaluateDieline"]
  NG_05["G-05<br/>Dieline + PrinterDieline +…"]
  NPKG_FE_003(["PKG-FE-003"])
  NB_03 ==> NPKG_FE_003
  NB_05 ==> NPKG_FE_003
  ND_02 ==> NPKG_FE_003
  NG_05 ==> NPKG_FE_003
```

### PKG-FE-004 · Migrate packaging simple mutations and export

```mermaid
flowchart LR
  ND_01["D-01<br/>addPackaging"]
  ND_03["D-03<br/>bulkAddPackagings"]
  ND_04["D-04<br/>bulkUpdatePackagings"]
  ND_05["D-05<br/>exportPackaging"]
  ND_06["D-06<br/>lockPackaging"]
  ND_07["D-07<br/>unlockPackaging"]
  ND_09["D-09<br/>updatePackagingComponentSta…"]
  NPKG_FE_004(["PKG-FE-004"])
  ND_01 ==> NPKG_FE_004
  ND_03 ==> NPKG_FE_004
  ND_04 ==> NPKG_FE_004
  ND_05 ==> NPKG_FE_004
  ND_06 ==> NPKG_FE_004
  ND_07 ==> NPKG_FE_004
  ND_09 ==> NPKG_FE_004
```

### PKG-FE-005 · Migrate `updatePackaging` saga handling and packet information

```mermaid
flowchart LR
  NE_01["E-01<br/>updatePackaging (multi-step…"]
  NPKG_FE_005(["PKG-FE-005"])
  NE_01 ==> NPKG_FE_005
```

---
*Story dependency graphs · packaging · generated 2026-07-21.*