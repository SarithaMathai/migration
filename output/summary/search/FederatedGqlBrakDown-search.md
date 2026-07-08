# Federated GraphQL Breakdown — Search

| | |
|---|---|
| **Target DGS** | `plm-elastic-search (separate)` |
| **T-Shirt Size** | **L** |
| **Total Stories** | 25 |
| **Complexity** | 🔴 0 Very High · 🟠 7 High · 🟡 11 Medium · 🟢 7 Low |
| **Phase Coverage** | 🧱 A · 📖 B · 🔍 C · ✏️ D · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Search** domain — the elastic-backed read layer that powers every search box, listing, suggestion, count and report across the PLM app — off the `spark-internal-graphql` gateway into its **own `plm-elastic-search` DGS subgraph**.
- Search is the **read hub**: nearly every other domain calls it (the 🔴 `search` dependency you see throughout product/bom/measurement/packaging/productDetails/claims/watchlist/ workspace).

- It is **breadth-dominated**: ~48 mostly-thin elastic-wrapper queries + 1 mutation, but a **large result-type surface** (~50 types) and heavy **enrichment field resolvers** that re-hydrate hits from product, vmm, ig, tag, brand, workspace, user, attachment, fabric and color.
- Low orchestration risk; the cost is surface area.

**ACL note:** a few proxy reads curry capability tokens; **ACL is ignored in the DGS implementation** — context only.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | ~48 | grouped into 10 search-family stories (Phase C) |
| Mutations | 1 | `sendBulkCombinationUpdates` |
| Result/value types | ~50 | the biggest single task (A02) |
| Field-resolver type blocks | ~12 | `SearchAttachment`, `Material`, combination/palette/watchlist/component, access/report/paging |
| External dependencies | ~14 keys | all cross-subgraph enrichment |
| Federation role | the program **read hub** | every domain calls it |
| **Total stories** | **25** | green-field; separate subgraph |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `SPARK-SRCH-A02` — Owned result types + inputs (the big surface) | `SPARK-SPIKE-05` | Polymorphic Type Resolution |

> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 4 | 14–24d |
| B | Core Reads | 3 | 3–6d |
| C | Search & Listing (by family) | 10 | 24–40d |
| D | Mutations | 1 | 1–2d |
| F | Federation & ownership | 1 | 3–5d |
| G | Field Resolvers & Tests | 6 | 28–46d |
| **Total** | | **25** | **73–123d** (buffered) |

> One engineer ≈ **15–25 sprints**. Parallelizable by family after A.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~15–25 sprints | sequential |
| 2 engineers | ~9–15 sprints | families parallel after A |
| 3 engineers | ~6–10 sprints | A02/A04 → families → enrichment in parallel |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | A01–A04 | schema (type surface) + service port |
| 3 | B01–B03 + C01 | by-id/counts + attachments |
| 4 | C02/C03 | material + sample families |
| 5 | C04–C06 | team/template/product families |
| 6 | C07–C10 + D01 | combination/palette/misc/suggestions/reports + mutation |
| 7 | G01/G02 | the two heavy enrichment blocks |
| 8 | G03–G05 + F01 | remaining enrichment + gateway/ownership |
| 9 | G06 | tests, parity, conformance CI |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 🧱 Phase A — Foundation & Type Resolvers (4 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 📄 `SPARK-SRCH-A01`<br>Schema skeleton + DateTime/JSON scalars | 🟢 Low `XS` | Story | — | **Intent —** Stand up the search subgraph's schema shell and custom scalars.<br>**Today —** green-field; schema translated from schemas/SPARK_Search.graphqls | — |
| 🔴🔬 📄 `SPARK-SRCH-A02`<br>Owned result types + inputs (the big surface)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-05` (Polymorphic Type Resolution) — see global Spike Detail_ | 🟠 High `L` | Story | SPARK-SPIKE-05 | **Intent —** Define all the search result types and input shapes (the big surface).<br>**Today —** all ~50 owned result/value types (SearchAttachment, Material, SearchCombination | — |
| 📄 `SPARK-SRCH-A03`<br>External stubs (platform + other DGS) | 🟡 Medium `M` | Story | — | **Intent —** Declare the external (other-DGS / platform) types search references.<br>**Today —** @extends @external stubs for Product(sPaged), WorkspaceV2, Bom, SampleV2, Attachment | — |
| 🔷 `SPARK-SRCH-A04`<br>`SearchService` Kotlin port (plm-elastic-search) | 🟠 High `L` | Query | — | **Intent —** Port the ~80 elastic query-builder methods to Kotlin.<br>**Today —** ~80 elastic query-builder methods on the plm-elastic-search base | — |


### 📖 Phase B — Core Reads (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-SRCH-B01`<br>`searchMaterialsById(id)` | 🟢 Low `XS` | Query | — | **Intent —** Fetch materials by id.<br>**Today —** getMaterialByIds |
| 🔷 `SPARK-SRCH-B02`<br>`getElasticSamplesByIds(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Fetch elastic sample docs by ids.<br>**Today —** getElasticSamplesByIds |
| 🔷 `SPARK-SRCH-B03`<br>`getAttachmentsCounts` + `getSampleCount` | 🟢 Low `XS` | Query | — | **Intent —** Count attachments / samples per resource.<br>**Today —** getAttachmentsCounts(resourceIds); getSampleCount(resourceId) → [ResourceCount] |


### 🔍 Phase C — Search & Listing (10 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔷 `SPARK-SRCH-C01`<br>`searchAttachments` | 🟡 Medium `M` | Query | — | **Intent —** Search attachments by query and filters.<br>**Today —** (own elastic) searchAttachments({q,parentIds,relatedIds,partnerId,asset3D,proxyIds,page,size,sort}) | — |
| 🔷 `SPARK-SRCH-C02`<br>Material search family | 🟠 High `L` | Query | — | **Intent —** Search materials (incl. RGB colour and nested filters).<br>**Today —** build elastic bodies (V2 = query+sort+options+searchArguments incl. - RGB color criteria + nested filters) → post → MaterialsPaged | — |
| 🔷 `SPARK-SRCH-C03`<br>Sample search family | 🟠 High `L` | Query | — | **Intent —** Search samples.<br>**Today —** elastic sample queries + group-by aggregates | — |
| 🔷 `SPARK-SRCH-C04`<br>Team search family | 🟡 Medium `M` | Query | — | **Intent —** Search teams. | — |
| 🔷 `SPARK-SRCH-C05`<br>Template search family | 🟡 Medium `M` | Query | — | **Intent —** Search templates. | — |
| 🔷 `SPARK-SRCH-C06`<br>Product search family | 🟡 Medium `M` | Query | — | **Intent —** Search products. | — |
| 🔷 `SPARK-SRCH-C07`<br>`searchCombinations` + `searchPalettes` | 🟢 Low `XS` | Query | — | **Intent —** Search combinations and colour palettes. | — |
| 🔷 `SPARK-SRCH-C08`<br>`searchWatchlist` + `searchClaimsByProxyIds` + `searchRfidLocations` | 🟢 Low `XS` | Query | — | **Intent —** Search watchlists, proxied claims and RFID locations. | — |
| 🔷 `SPARK-SRCH-C09`<br>Suggestions family | 🟡 Medium `M` | Query | — | **Intent —** Provide type-ahead suggestions. | — |
| 🔷 `SPARK-SRCH-C10`<br>Reports | 🟡 Medium `M` | Query | — | **Intent —** Run the search-backed reports. | — |


### ✏️ Phase D — Mutations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `SPARK-SRCH-D01`<br>`sendBulkCombinationUpdates` | 🟢 Low `XS` | Mutation | — | **Intent —** Queue bulk combination updates for indexing.<br>**Today —** sendBulkCombinationUpdates(combinationUpdates) → {requestId} |


### 🔗 Phase F — Federation & Stitching (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-SRCH-F01`<br>Gateway composition + ownership reconciliation | 🟡 Medium `M` | Field Resolver | — | **Intent —** Wire search into the federated graph and settle who owns which fields.<br>**Today —** add plm-elastic-search to the supergraph; reconcile drift/ownership: searchProducts |


### 🧪 Phase G — Field Resolvers & Tests (6 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔷 `SPARK-SRCH-G01`<br>`SearchAttachment` enrichment | 🟠 High `L` | Query | — | **Intent —** Enrich search-attachment results with related data. | — |
| 🔸 `SPARK-SRCH-G02`<br>`Material` enrichment (incl. `colorLinks`) | 🟠 High `L` | Field Resolver | — | **Intent —** Enrich material results (incl. colour links). | — |
| 🔷 `SPARK-SRCH-G03`<br>`SearchCombination` + `SearchPalette` field resolvers | 🟡 Medium `M` | Query | — | **Intent —** Resolve combination / palette result fields. | — |
| 🔷 `SPARK-SRCH-G04`<br>`SearchWatchlist` + `SearchComponent` field resolvers | 🟡 Medium `M` | Query | — | **Intent —** Resolve watchlist / component result fields. | — |
| 🔸 `SPARK-SRCH-G05`<br>Access + report-group + paging field resolvers | 🟡 Medium `M` | Field Resolver | — | **Intent —** Resolve access, report-group and paging fields. | — |
| 🔸 `SPARK-SRCH-G06`<br>Tests, parity harness, schema-conformance CI | 🟠 High `L` | Field Resolver | — | **Intent —** Prove the search subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity harness across the search families + enriched result types; **schema- | — |

