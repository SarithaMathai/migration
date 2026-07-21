## Backend

### Federated GraphQL Breakdown — Bill of Materials (BOM)

| | |
|---|---|
| **Target DGS** | `plm-product (co-located)` |
| **T-Shirt Size** | **XL** |
| **Total Stories** | 37 |
| **Complexity** | 🔴 1 Very High · 🟠 2 High · 🟡 13 Medium · 🟢 21 Low |
| **Phase Coverage** | 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-19 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H

---

#### What Are We Building?

- We are moving the **Bill of Materials (BOM)** domain off the shared Node.js `spark-internal-graphql` gateway and into the **`plm-product`** Netflix DGS service, where it lives next to Product, Measurement, Impression and Packaging.
- BOM is the structured record of every material, supplier and impression that makes up a product, and it is referenced by many sibling domains.

- BOM is **mid-sized**: 13 queries, 6 mutations, and ~46 field resolvers across 18 type blocks, on a 735-line resolver.
- Its defining challenge is **material polymorphism** — 7 concrete material types (Trim, Wash, Fabric, FabricSpec, Combination, Packaging, plus the base) resolved by a category dispatcher, and 5 impression sub-types.
- The single hardest piece of work is `updateBom`, a 3-step write (workspace → body → permissions) that today has no rollback.

- The schema is **wide but shallow**: the large majority of attributes are direct pass-throughs (cheap to migrate).
- Risk concentrates in ~38 cross-domain field resolvers (material-library and color lookups) and the 2 polymorphic interfaces.
- See be-05-attribute-inventory.md.

**Note on ACL:** the current gateway uses ACL to obtain a per-resource capability token. Per decision,
Per **ADR-019** ([`complexStories/acl/01-adr-acl-mid-request-update.md`](https://github.com/XXX/blob/main/output/complexStories/acl/01-adr-acl-mid-request-update.md)), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites — where a resolver hands its token to a *different* domain's loader — use **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before the downstream call.

---

#### Migration Scope

| Surface | Count | Notes |
|---------|-------|-------|
| Queries | 12 | 4 are cacheable master-data lookups. `getBomDataV2` removed (`Bom_Unified` deprecated) |
| Mutations | 6 | 5 simple + `updateBom` (complex) |
| Field-resolver type blocks | 17 | one story each. `BomMaterial_Unified` removed; impression branch (`G-10`) rescoped, not removed |
| Material polymorphism | 7 types + interface + type resolver | B-01 |
| Impression polymorphism | 5 types + interface | B-01 |
| External dependencies | 12 loader keys (2 🔴 · 6 🟡 · 4 🔵) | sibling DGS + VMM platform |
| Federation contributions | 2 (Product extension, ResourcesCount.bomsCount) | BLOCKED-BY product |
| **Total stories** | **36** | green-field build stories. The 3 Phase-0 spike stubs are tracked as **program spikes** in the global breakdown and Jira, not as rows here (see global Phase 0) |

---

#### Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `BOM-BE-A-04` — `@DgsTypeResolver` for the 2 BOM interfaces | `SPIKE-05` | Polymorphic Type Resolution |
| 🔴🔬 `BOM-BE-B-05` — `getBomMaterialTypes` (merge with Material Hub) | `SPIKE-06a` | Hydration |
| 🔴🔬 `BOM-BE-E-01` — `updateBom` — 3-step orchestrated write | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

#### Deployment Model — Ship on Green, Per Story

Each story is **end-to-end in one PR** (schema + DGS data fetcher + Kotlin service method + Hive push) and is
**independently deployable to production the moment its own tests and parity pass** — you don't wait for the
rest of the phase to finish.

- The **one exception** is a story whose field is produced by **composing another subgraph's data** — a cross-subgraph **entity extension** (`extend type … @key`, resolved by a *different* DGS).
- Those can only go live once the **owning subgraph is deployed**, so they are held and marked **BLOCKED-BY `<domain>`**.

- ✅ **Ships on green** — every BOM story here, including `F-01`/`F-02`. Those two contribute fields to
  `Product`/`ResourcesCount`, but **within the same `plm-product` subgraph** (internal `@DgsData`, not
  cross-subgraph federation), so they are *not* gated on a separate deployment — they ship as soon as the
  Product types exist in the shared schema.
- ⛔ **Waits for an owning subgraph** — **none in BOM.** BOM consumes sibling material subgraphs
  (hub/trim/wash/fabric/combination) for *enrichment*, but a material field simply returns `{id}` until its
  sibling is federated (rolled out per program spike `SPIKE-06a`), so the story still ships; it just shows partial enrichment until then.

---

#### Effort Snapshot

| Phase | Name | Stories | Effort (est., +20% buffer) |
|-------|------|---------|----------------------------|
| A | Foundation & Type Resolvers | 2 | 5–10d |
| B | Core Reads | 7 | 10–19d |
| C | Search & Listing | 5 | 8–17d |
| D | Mutations | 5 | 7–14d |
| E | Complex Operations | 1 | 8–14d |
| F | Federation & Stitching | 2 | 4–7d |
| G | Field Resolvers & Tests | 15 | 32–62d |
| **Total** | | **37** | **74–143d** (buffered) |

> Computed live from `be-04-stories.md` (phase + complexity per story) — always reconciles with the story tables below and the program overview. Effort = sum of per-story nominal day-ranges (Low 1–2 · Medium 2–4 · High 4–7 · Very High 7–12) × 1.2 buffer, AI-estimated — confirm in refinement. See each story's **Depends On** column for real sequencing.


**Capacity Planning**

| Team size | Calendar (5d sprints) | Notes |
|-----------|----------------------|-------|
| 1 engineer | ~15–25 sprints | sequential |
| 2 engineers | ~9–15 sprints | B/C/D + most of G parallel |
| 3 engineers | ~6–10 sprints | critical path A → E-01 → G-08/G-10 → G-15 |

> Phase G (field resolvers) dominates the calendar; G-08 (trim) and G-10 (impression branch) are the two
> biggest field-resolver stories.

---

#### Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|--------|---------|-------|
| 0 | Program spikes | run in Sprint 0 (see global Phase 0 — Program Spikes) so E-01/rollout-order aren't waiting |
| 1 | B-01 (DGS module init + service wiring + first resolver), A-05 (shared CI conformance gate) | schema, stubs, type resolvers, service port, drift guard |
| 2 | B-01, B-03–B-08 + D-03/D-04 | reads (incl. 4 cacheable) + lock/unlock |
| 3 | C-01–C-05 + D-01/D-02/D-05 | search/supplier + simple mutations |
| 4 | E-01 | `updateBom` 3-step write (focused; needs `SPIKE-01` concluded) |
| 5 | G-01, G-03–G-07 | entity + simple material field resolvers |
| 6 | G-08 + G-09 | trim (large) + wash |
| 7 | G-10–G-15 | impression branches + search-result enrichment + trivial bundle |
| post-launch | F-01, F-02 | federation contributions (unblocked by product) |

> Test-coverage/parity-harness work (formerly `G-16`) is tracked outside this Jira pipeline, created
> manually. `G-15` (`BomMaterialSearchResult` field resolvers) is real field-resolver scope and stays in
> the sprint plan above (sprint 7).

---

#### Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟡 `A-04`, 🟢 `B-03`, 🟢 `B-04`, 🟡 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟢 `C-04`, 🟢 `C-05`, 🟡 `D-01`, 🟢 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟡 `G-03`, 🟢 `G-04`, 🟢 `G-05`, 🟢 `G-06`, 🟢 `G-07`, 🟠 `G-08`, 🟢 `G-09`, 🟠 `G-10`, 🟢 `G-14` | `A-04` → 🔬 SPIKE-05<br>`B-05` → 🔬 SPIKE-06a | Fan-out — 🧱 Foundation & Type Resolvers · 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests |
| 3 | 🟡 `A-05`, 🔴 `E-01`, 🟡 `G-11`, 🟡 `G-12`, 🟢 `G-13`, 🟡 `G-15`, 🟡 `G-17` | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module) | 🧱 Foundation & Type Resolvers · ⚙️ Complex Operations · 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `A-04` → `A-05` — 3 sequential stories; everything else hangs off this chain in parallel.

---

#### Recommended Story Graph — 1 Backend Engineer

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 1 backend engineer** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 |
|---|---|
| 1 | 🟢 `B-01` (1–2d) |
| 2 | 🟢 `D-02` (1–2d) |
| 3 | 🔴 `E-01` (7–12d) 🔬 ⛔ |
| 4 | 🟠 `G-10` (4–7d) |
| 5 | 🟡 `A-04` (2–4d) 🔬 |
| 6 | 🟡 `C-02` (2–4d) |
| 7 | 🟡 `G-01` (2–4d) |
| 8 | 🟠 `G-08` (4–7d) |
| 9 | 🟡 `A-05` (2–4d) |
| 10 | 🟡 `B-05` (2–4d) 🔬 |
| 11 | 🟡 `C-03` (2–4d) |
| 12 | 🟡 `D-01` (2–4d) |
| 13 | 🟡 `F-01` (2–4d) |
| 14 | 🟡 `G-03` (2–4d) |
| 15 | 🟡 `G-11` (2–4d) |
| 16 | 🟡 `G-12` (2–4d) |
| 17 | 🟡 `G-15` (2–4d) |
| 18 | 🟡 `G-17` (2–4d) |
| 19 | 🟢 `B-03` (1–2d) |
| 20 | 🟢 `B-04` (1–2d) |
| 21 | 🟢 `B-06` (1–2d) |
| 22 | 🟢 `B-07` (1–2d) |
| 23 | 🟢 `B-08` (1–2d) |
| 24 | 🟢 `C-01` (1–2d) |
| 25 | 🟢 `C-04` (1–2d) |
| 26 | 🟢 `C-05` (1–2d) |
| 27 | 🟢 `D-03` (1–2d) |
| 28 | 🟢 `D-04` (1–2d) |
| 29 | 🟢 `D-05` (1–2d) |
| 30 | 🟢 `F-02` (1–2d) |
| 31 | 🟢 `G-04` (1–2d) |
| 32 | 🟢 `G-05` (1–2d) |
| 33 | 🟢 `G-06` (1–2d) |
| 34 | 🟢 `G-07` (1–2d) |
| 35 | 🟢 `G-09` (1–2d) |
| 36 | 🟢 `G-13` (1–2d) |
| 37 | 🟢 `G-14` (1–2d) |

**BE-1:** `B-01` → `D-02` → `E-01` → `G-10` → `A-04` → `C-02` → `G-01` → `G-08` → `A-05` → `B-05` → `C-03` → `D-01` → `F-01` → `G-03` → `G-11` → `G-12` → `G-15` → `G-17` → `B-03` → `B-04` → `B-06` → `B-07` → `B-08` → `C-01` → `C-04` → `C-05` → `D-03` → `D-04` → `D-05` → `F-02` → `G-04` → `G-05` → `G-06` → `G-07` → `G-09` → `G-13` → `G-14`

**Elapsed (nominal midpoints):** ~91 working days.

---

#### Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

##### 🧱 Phase A — Foundation & Type Resolvers (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔴🔬 🔸 `BOM-BE-A-04`<br>`@DgsTypeResolver` for the 2 BOM interfaces<br>🔴🔬 _Spike-gated on `SPIKE-05` (Polymorphic Type Resolution) — see global Spike Detail_ | 🟡 Medium `M` | Field Resolver | SPIKE-05 | **Intent —** Route each material/impression row to the right concrete type by its category code.<br>**Today —** - Material: switch on material.materialCategory.code → 4→Trim, 6→Wash, 2→Fabric, 15→Combination, 16→FabricSpec, {10,11,12,13,14,17–24}→Packaging, default…<br>**Done when:**<br>• Each `materialCategory.code` maps to the type in the table above; unknown codes → `BomMaterial`<br>• Each impression `type` maps correctly; unknown → `BomBaseImpressionDetails`<br>• `BomConstants` holds all 21 category codes + 5 impression codes (verify values against backend, ADR-017 pin-down 1) |
| 📄 `BOM-BE-A-05`<br>Shared CI conformance gate + `code → type` registry (`SPIKE-05`) | 🟡 Medium `M` | Service | A-04 | **Intent —** Build the one shared test library that fails a PR when a schema type, a dispatch enum, and a golden fixture disagree — so the next added material/impression variant can't silently drift the way today's five hand-maintained switch tables can.<br>**Done when:**<br>• The conformance library's three checks (SDL↔enum, explicit-default, golden-fixture-diff) run against `BomConstants.kt` + `bom.graphqls` in bom's CI build and pass on the current (correct) mapping<br>• Demonstrably fails on each drift direction, proven by a negative test per direction: an SDL member with no enum row; an enum row with no SDL type; an undeclared/implicit default; a mapping change with no fixture change in the same commit<br>• Golden-table fixtures exist for both of bom's dispatch sites (`BomMaterialInterface`, `BomImpressionDetailsInterface`), seeded from ADR-017 §1 and backend-verified per `A-04` AC-3 — including a HUB (code 9) material row and an unknown/missing category-code row (ADR-017 §5 fixture list)<br>• The `code → type` registry (`CodeToTypeRegistry.md`) is a standalone, human-readable page covering all five dispatch sites named in ADR-017 §1 (the three not yet built — `SampleAsset`, `SampleV2.parent*`, materials search — are recorded as later-phase rows so `SAMPLE-BE-A-04`/`SAMPLE-BE-G-02` and `SEARCH-BE-B-01`/`SEARCH-BE-C-02` inherit the table rather than re-deriving it), and includes ADR-014's `type 2 → packagingBom` row<br>• The library is versioned with the schema-registry tooling and documented as a single shared artifact — no domain forks its own copy (ADR-017 pin-down 7)<br>• This story does not touch any per-variant field resolver or dispatch table itself — those are `A-04`'s and each per-variant `G-0x` story's own scope; this story only builds and wires the shared gate + registry |


##### 📖 Phase B — Core Reads (7 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `BOM-BE-B-01`<br>`getBomByIds` data fetcher | 🟢 Low `XS` | Query | — | **Intent —** Looks up full BOM records for a set of BOM ids (the core 'give me these BOMs' read).<br>**Today —** if ids empty → []; else GET … → camelCase. - ACL ignored in DGS<br>**Done when:**<br>• `getBomByIds(["B1","B2"])` returns mapped `Bom` objects from the REST list endpoint<br>• Empty `ids` → returns `[]` with **no** REST call<br>• Response snake_case → camelCase per schema |
| 🔷 `BOM-BE-B-03`<br>`getBomStatus` (cacheable master data) | 🟢 Low `XS` | Query | — | **Intent —** Returns the list of possible BOM statuses — the options you'd see in a status dropdown.<br>**Today —** GET …; transform {key:value} map → [{code,description}]. No ACL<br>**Done when:**<br>• Returns `[{code,description}]` from the status map<br>• Second call served from cache (no REST)<br>• Map key→`code`, value→`description` |
| 🔷 `BOM-BE-B-04`<br>`getBomByParentId` data fetcher | 🟢 Low `XS` | Query | — | **Intent —** Lists all the BOMs that belong to one product, newest first.<br>**Today —** today, the gateway fetches boms for a product and sorts them by createdAt DESC itself, in application code — the backend returns them unsorted. ignored in DGS. -…<br>**Done when:**<br>• Returns boms for `parentId` sorted `createdAt` DESC, sorted by the **backend**, not client code<br>• Empty → `{content: []}`<br>• No `sortedByDescending` (or equivalent) remains in the Kotlin data fetcher — sorting happens once, server-side |
| 🔴🔬 🔷 `BOM-BE-B-05`<br>`getBomMaterialTypes` (merge with Material Hub)<br>🔴🔬 _Spike-gated on `SPIKE-06a` (Hydration) — see global Spike Detail_ | 🟡 Medium `M` | Query<br>Calls: `materialHub` | SPIKE-06a | **Intent —** Returns the catalog of material types, combined with the shared material-hub types.<br>**Today —** load bom material types (GET …/master_data/bom_material_types[?ids]) and materialHub.getHubMaterialTypes (today sequential), concat; map each hub type → {code:9…<br>**Done when:**<br>• Returns bom types + synthesized hub types<br>• Hub rows carry `code=9, libraryLink=true, freeText=true, bomType={1,'Product'}`<br>• The two fetches run concurrently<br>• EXT hub failure → return bom types only (partial), logged |
| 🔷 `BOM-BE-B-06`<br>`getBomPackagingMaterialTypes` (cacheable) | 🟢 Low `XS` | Query | — | **Intent —** Returns the packaging material-type lookup list (cached, rarely changes).<br>**Today —** GET …/master_data/packaging_bom_material_types → camelCase. No ACL<br>**Done when:**<br>• Returns packaging material types<br>• Cached on second call |
| 🔷 `BOM-BE-B-07`<br>`getBomPackagingSubstrates` (cacheable) | 🟢 Low `XS` | Query | — | **Intent —** Returns the packaging substrate lookup list (cached).<br>**Today —** GET …/master_data/packaging_bom_substrate_types → camelCase<br>**Done when:**<br>• Returns substrate list<br>• Cached |
| 🔷 `BOM-BE-B-08`<br>`getBomPackagingUnitOfMeasure` (cacheable) | 🟢 Low `XS` | Query | — | **Intent —** Returns the packaging unit-of-measure lookup list (cached).<br>**Today —** GET …/master_data/packaging_unit_of_measure → camelCase (units_of_measure)<br>**Done when:**<br>• Returns UoM list<br>• Cached |

> **`BOM-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `bom.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql. **This scaffold is a prerequisite for every B/C/D/G story** — they need the module + schema file to compile their DGS wrapper — so it is assumed globally (shown once in the dependency graph) and **not repeated** in each story's `Depends On`. After it lands, the wrappers parallelize.


##### 🔍 Phase C — Search & Listing (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `BOM-BE-C-01`<br>`getBomElastic` data fetcher | 🟢 Low `XS` | Query<br>Calls: `search` | — | **Intent —** Runs a BOM search and returns the BOMs that match.<br>**Today —** {content} = search.getBomElastic; return content. The entire query object is passed to elastic — document the exact field set. - EXT Service Calls: EXT → key: search ·…<br>**Done when:**<br>• Returns `content` boms for a query<br>• Query DTO field set documented + matches backend<br>• Empty → `[]` |
| 🔷 `BOM-BE-C-02`<br>`searchMaterialsBom` data fetcher | 🟡 Medium `M` | Query<br>Calls: `search`, `vmm` | — | **Intent —** Searches for materials inside BOMs, with filters and paging.<br>**Today —** in plain terms — before hitting the search backend, this resolver (1) looks up fabric suppliers by calling straight into another domain's resolver code (not a clean…<br>**Done when:**<br>• Returns `BomMaterialSearch{content,paging}`<br>• With `nestedSearchFilters`, the request serializes to the same `nestedSearchFilters[i].*` keys as today (or the agreed structured DTO, once the search-request-shape decision has landed)<br>• `size` defaults to 20<br>• Fabric-supplier prefetch via service/federation, not a resolver import |
| 🔷 `BOM-BE-C-03`<br>`getComboSupplierForBom` data fetcher | 🟡 Medium `M` | Query<br>Calls: `combination`, `vmm` | — | **Intent —** Finds which suppliers are available for a BOM's combination materials.<br>**Today —** fabricSpecCombos = SPARK_Combination.searchFabricSpecCombos({q:parentComboId:${comboId}, page:0, size:100}) (cross-resolver import). 2. Filter combos: keep where fsId…<br>**Done when:**<br>• Returns suppliers only for combos with a resolvable `fsId` and `bpName`<br>• Filter logic matches the rule above (document the `mvIds.length===1` behaviour)<br>• VMM lookups run concurrently |
| 🔷 `BOM-BE-C-04`<br>`getValidTrimSuppliersForBom` data fetcher | 🟢 Low `XS` | Query<br>Calls: `vmm` | — | **Intent —** Lists the valid trim suppliers for a BOM.<br>**Today —** getRelatedSuppliersForMVs(ctx, merchVendorIds, [TRIM_SUPPLIER.code]) → [Int] partner ids. - EXT Service Calls: EXT → key: vmm ·<br>**Done when:**<br>• Returns related trim-supplier partner ids<br>• Role filter = TRIM_SUPPLIER only<br>• Empty input → `[]` |
| 🔷 `BOM-BE-C-05`<br>`getValidRawMaterialSuppliersForBom` data fetcher | 🟢 Low `XS` | Query<br>Calls: `vmm` | — | **Intent —** Lists the valid raw-material suppliers for a BOM.<br>**Today —** same as C-04 with roles [RAW_MATERIAL_SUPPLIER, FABRIC_SUPPLIER, TRIM_SUPPLIER]<br>**Done when:**<br>• Returns ids matching the 3 roles<br>• Empty input → `[]` |


##### ✏️ Phase D — Mutations (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `BOM-BE-D-01`<br>`addBom` mutation | 🟡 Medium `M` | Mutation | — | **Intent —** Creates a new BOM.<br>**Today —** bom = bomService.addBom(sparkBom) → POST … (transformRequest: deepToSnakeCase, primeKey: humanId); if bom.validationErrors \\|\\| bom.message → throw. No ACL (new…<br>**Done when:**<br>• POST creates a bom and returns it mapped to `Bom`<br>• Backend `validationErrors`/`message` → `BomValidationException` (not a silent return)<br>• Request body is snake_case<br>• Read cache primed with `humanId` |
| 🔶 `BOM-BE-D-02`<br>`manageBomWorkspaces` mutation | 🟢 Low `XS` | Mutation<br>Calls: `workspaceV2` | — | **Intent —** Adds or removes which workspaces a BOM belongs to.<br>**Today —** if toAdd/toRemove non-empty → workspaceAssociationHelper(BOM, bomId, toAdd, toRemove) → PUT …/{bomId}/{associate\\|dissociate}_workspace; else returns undefined. - EXT…<br>**Done when:**<br>• Adds/removes workspace associations via the correct endpoint<br>• Both lists empty → `null`, no REST call<br>• Returns the updated bom |
| 🔶 `BOM-BE-D-03`<br>`lockBom` mutation | 🟢 Low `XS` | Mutation | — | **Intent —** Locks a BOM so others can't edit it.<br>**Today —** PUT …/{bomId}/lock. ignored in DGS<br>**Done when:**<br>• PUT to `/lock` returns the locked bom<br>• 404 → null |
| 🔶 `BOM-BE-D-04`<br>`unlockBom` mutation | 🟢 Low `XS` | Mutation | — | **Intent —** Unlocks a BOM so it can be edited again.<br>**Today —** PUT …/{bomId}/unlock<br>**Done when:**<br>• PUT to `/unlock` returns the unlocked bom<br>• 404 → null |
| 🔶 `BOM-BE-D-05`<br>`updateBomComponentStatus` mutation | 🟢 Low `XS` | Mutation | — | **Intent —** Updates the status of one or more components on a BOM.<br>**Today —** PUT …/bom/v1/component_status_update body {productId, ids, status}. No ACL token — the only write without one (every other BOM write obtains one)<br>**Done when:**<br>• PUT sends `{productId, ids, status}` (snake_case)<br>• Returns `BomPaged{content}` |


##### ⚙️ Phase E — Complex Operations (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `BOM-BE-E-01`<br>`updateBom` — 3-step orchestrated write<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🔴 Very High `XL` | Mutation<br>Calls: `workspaceV2` | SPIKE-01, D-02 | **Intent —** Edit a BOM — a 3-step write (workspace + body + permissions) that has no rollback today.<br>**Today —** editing a bom today is really three separate backend calls made one - after another, with no undo button: (1) if the caller changed which workspaces the bom belongs…<br>**Done when:**<br>• Parity for 5 fixtures: body-only; body+workspace-add; body+workspace-remove; body+partners; body+workspace+partners<br>• Workspace step runs **before** the body PUT; permissions step only when `businessPartners` present<br>• Body PUT omits `humanId` from the body<br>• Failure strategy per ADR-013 §4-B implemented: a workspace-step failure after the body PUT compensates (dissociate/re-associate); a permissions-step failure retries then surfaces `PARTIAL_FAILURE` with per-step detail (stale ACL made visible, not silently swallowed)<br>• Backend `validationErrors`/`message` → `BomValidationException`<br>• Read cache updated with the returned bom | ☐ Unit: order workspace→body→perms<br>☐ Unit: no-workspace skip<br>☐ Unit: no-partners skip<br>☐ Unit: step-3 (permissions) failure path yields `PARTIAL_FAILURE` with per-step detail<br>☐ Parity: 5 fixtures |


##### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `BOM-BE-F-01`<br>Implement `Product.productBoms` / `boms` / `packagingBoms` (internal) | 🟡 Medium `M` | Field Resolver | — | **Intent —** Serve a product's BOM lists from BOM's own service instead of product reaching across.<br>**Today —** when a client asks a Product for its boms today, that resolver lives - in product's code and reaches across to BOM's data loader. - After migration, product and bom…<br>**Done when:**<br>• `Product.productBoms/boms/packagingBoms` resolve via `bomService` internally<br>• the equivalent product-side resolvers are removed<br>• `boms(types)` filters by bom type<br>• no gateway hop |
| 🔸 `BOM-BE-F-02`<br>Fill `ResourcesCount.bomsCount` (internal) | 🟢 Low `XS` | Field Resolver<br>Calls: `search` | — | **Intent —** Let BOM own the 'how many boms' count shown on the TechPack panel.<br>**Today —** the TechPack summary panel shows "12 boms" for a product today by having product's orchestration code run an elastic count query. Once BOM owns this field, BOM's own…<br>**Done when:**<br>• `bomsCount` resolves internally on `ResourcesCount`<br>• count matches current elastic semantics<br>• no gateway hop for this field |


##### 🧪 Phase G — Field Resolvers & Tests (15 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `BOM-BE-G-01`<br>`Bom` field resolvers (9 shared fields) | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `tag` | — | **Intent —** Resolve the 9 shared Bom fields (people, product, workspaces, partners, participants).<br>**Today —** 9 fields — humanId, access, currentUserPermissions, businessPartners, createdBy, updatedBy, product, workspaces, participantDetails — that all need a little lookup…<br>**Done when:**<br>• All 9 fields resolve on `Bom` from one impl<br>• `product` null when `parentId` not `PID*` (defensive guard; in practice always `PID*`, per the confirmed decision)<br>• Sibling fields emit correct `@key`s for federation<br>• No ACL plumbing introduced | — |
| 🔸 `BOM-BE-G-03`<br>`BomMaterial` field resolvers (8 fields) | 🟡 Medium `M` | Field Resolver<br>Calls: `materialHub`, `tag` | — | **Intent —** Resolve the generic material row's fields (library lookup, origins, weight).<br>**Today —** BomMaterial is the generic ("hub") material row. Two of its fields — - libraryResource and genericMaterialType — both need the same lookup from the Material Hub…<br>**Done when:**<br>• `genericMaterialType` returns hub value when `relatedMaterialType` differs from local, else local<br>• `origins`/`certifications` filtered to known codes and enriched to `{code,description}`<br>• `weight` uses UoM fallback code 23 (grams)<br>• Hub fetched once per material | — |
| 🔸 `BOM-BE-G-04`<br>`BomPackagingMaterial` field resolvers (2 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `tag` | — | **Intent —** Resolve a packaging material's impressions and country-of-origin.<br>**Today —** impressionDetails (material.impressions), countryOfOrigin (tag)<br>**Done when:**<br>• `impressionDetails` = parent impressions<br>• `countryOfOrigin` resolves from `countryOfOriginIds` (empty → `[]`) | — |
| 🔸 `BOM-BE-G-05`<br>`BomFabricMaterial` field resolvers (4 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `search`, `tag`, `materialHub` | — | **Intent —** Resolve a fabric material's spec/combo, weight and origin.<br>**Today —** libraryResource = search.searchFabricSpecCombos({q:id:${fscId},page:0,size:1}) → content[0] ?? {id:fscId}; weight (H1), countryOfOrigin, impressionDetails…<br>**Done when:**<br>• Returns the matched fabricSpecCombo or `{id}`<br>• `weight`/`countryOfOrigin` as G-03 | — |
| 🔸 `BOM-BE-G-06`<br>`BomFabricSpecMaterial` field resolvers (4 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `fabric`, `tag`, `materialHub` | — | **Intent —** Resolve a fabric-spec material's fields.<br>**Today —** libraryResource = fabric.getSpecificationByID ?? {id}; weight, countryOfOrigin, impressionDetails. - EXT: fabric, materialHub; tag<br>**Done when:**<br>• Returns fabric spec or `{id}`<br>• weight/countryOfOrigin as G-03 | — |
| 🔸 `BOM-BE-G-07`<br>`BomCombinationMaterial` field resolvers (4 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `combination`, `tag`, `materialHub` | — | **Intent —** Resolve a combination material's fields.<br>**Today —** libraryResource = combination.getById ?? {id}; weight, countryOfOrigin<br>**Done when:**<br>• Returns combination or `{id}`<br>• weight/countryOfOrigin as G-03 | — |
| 🔸 `BOM-BE-G-08`<br>`BomTrimMaterial` field resolvers (7 fields) — trim size dispatchers | 🟠 High `L` | Field Resolver<br>Calls: `trim`, `location`, `tag` | — | **Intent —** Resolve a trim material's fields, including the per-trim-type size dispatch.<br>**Today —** - libraryResource = trim.getTrimBatch. - materialLibraryUom = trim UoMs, find by materialLibraryUomId.toString() (preserve int→string coercion). - sizeValue = reload…<br>**Done when:**<br>• `sizeValue` matches `getTrimSizeValue` for all 15 trim types (parity table) incl. THREAD/LABEL subtype branches<br>• `sizeCaption` returns the correct `{edit,view}` per type incl. compatible-size and finished-size cases<br>• `materialLibraryUom` matches via string-coerced code<br>• `facilityName` returns the pre-set value if present, else the resolved VMM facility name<br>• Trim is fetched once per material (one REST call) | ☐ Unit: 15 trim-type `sizeValue` cases<br>☐ Unit: caption edit/view per type<br>☐ Unit: UoM string coercion<br>☐ Unit: facilityName pre-set vs resolved<br>☐ Unit: single trim fetch<br>☐ Parity: recorded trim fixtures |
| 🔸 `BOM-BE-G-09`<br>`BomWashMaterial` field resolvers (4 fields) | 🟢 Low `XS` | Field Resolver<br>Calls: `wash`, `tag`, `materialHub` | — | **Intent —** Resolve a wash material's fields.<br>**Today —** libraryResource = wash.getWash(jwt) ?? {id}; weight, countryOfOrigin, impressionDetails. ACL context: wash uses a capability token; ignore in impl<br>**Done when:**<br>• Returns wash or `{id}`<br>• weight/countryOfOrigin as G-03 | — |
| 🔸 `BOM-BE-G-10`<br>Impression library-resource resolution (shared internal/external branch + `MaterialDataLoader`) | 🟠 High `L` | Field Resolver<br>Calls: `search` | — | **Intent —** Resolve an impression's colour/library links, branching on internal vs external caller.<br>**Today —** resolving "what material does this impression's color/library field - point to" needs to behave differently depending on who's asking. - An internal user gets the…<br>**Done when:**<br>• Internal path resolves `libraryResource` via material-by-id; external path via proxy-id search<br>• `bomIds` come from DGS local context, not field args (the fragile `args.ids` contract is removed)<br>• Missing `libraryResource.id` → null<br>• 5 color fields resolve via batched material loader<br>• `G-11`/`G-12`/`G-13` call this shared service rather than re-implementing the branch | ☐ Unit: internal branch<br>☐ Unit: external branch (proxyIds)<br>☐ Unit: null id<br>☐ Unit: color batch<br>☐ Parity: internal vs external |
| 🔸 `BOM-BE-G-11`<br>`BomFabricLibraryImpressionDetails.libraryResource` | 🟡 Medium `M` | Field Resolver<br>Calls: `search` | G-10 | **Intent —** Resolve this impression type's library link (shares G-10's branch).<br>**Today —** single libraryResource field with the same internal/external branch as G-10<br>**Done when:**<br>• Same behaviour as `G-10`'s `libraryResource` for this type<br>• Uses local-context `bomIds` | — |
| 🔸 `BOM-BE-G-12`<br>`BomTrimLibraryImpressionDetails` field resolvers (3 fields) | 🟡 Medium `M` | Field Resolver<br>Calls: `search` | G-10 | **Intent —** Resolve this trim-impression's library link and two colours.<br>**Today —** libraryResource (G-10 branch) + groundColor, textColor via searchMaterialById<br>**Done when:**<br>• `libraryResource` behaves as `G-10`<br>• `groundColor`/`textColor` resolve via material loader | — |
| 🔸 `BOM-BE-G-13`<br>`BomTrimZipperLibraryImpressionDetails` field resolvers (3 colors) | 🟢 Low `XS` | Field Resolver<br>Calls: `search` | G-10 | **Intent —** Resolve a zipper impression's three colours.<br>**Today —** sliderColor, tapeColor, teethColor via searchMaterialById. Unlike G-11/G-12, this type has no libraryResource field at all — just three colors — so it only needs…<br>**Done when:**<br>• Three color fields resolve by id<br>• Missing id → null | — |
| 🔸 `BOM-BE-G-14`<br>Trivial pass-through fields (bundle) | 🟢 Low `XS` | Field Resolver | — | **Intent —** Resolve the trivial computed / pass-through fields (no service call).<br>**Today —** the only allowed bundle — fields that return a parent value with no service call: BomMaterialType.id = ` ${code}_${description} (computed); BomMaterialSearch.paging =…<br>**Done when:**<br>• `BomMaterialType.id` = `code_description`<br>• `impressionDetails` maps from `impressions`<br>• `libraryResourceId` from nested id<br>• No EXT calls | — |
| 🔸 `BOM-BE-G-15`<br>`BomMaterialSearchResult` field resolvers (5 fields) | 🟡 Medium `M` | Field Resolver<br>Calls: `fabric`, `search` | C-02 | **Intent —** Resolve the material-search-result fields (tolerant of both response shapes).<br>**Today —** description (description ?? name), status (status?.description ?? status), - fabricSpec (if type==='fabric_spec_combo' & fabricSpecId → fabric.getSpecificationByID)…<br>**Done when:**<br>• `description`/`status` handle both shapes<br>• `fabricSpec`/`fabric`/`fabricId` gated by `type`<br>• `relatedMaterials` buckets `intentLineIds` correctly<br>• `proxyIds` not mutated (copy used) | — |
| 🔸 `BOM-BE-G-17`<br>`supplier` entity references on material rows (recommended, PO-gated) | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm` | G-01 | **Intent —** Adds a `supplier { … }` object next to `supplierId`/`supplierName` on every material row,<br>**Today —** add supplier: VMM_BusinessPartner to BomMaterialInterface and all 7<br>**Done when:**<br>• PO approval recorded (OQ-5) and OQ-3 answered before implementation starts<br>• `supplier` present on the interface + all 7 impls<br>• `supplierId`/`supplierName` continue to return unchanged values (parity)<br>• Stub emission only — no direct VMM calls from the BOM subgraph | — |



---

## Frontend

### Federated GraphQL Breakdown — BOM · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (co-located)` |
| **Total FE Stories** | 7 |
| **Impact** | 🔴 4 High · 🟡 1 Medium · 🟢 2 Low |
| **Estimated effort** | 29–46 days (single-engineer) |
| **Phase-1 surface** | 21 operation-to-root-field rows · 4 client files · 7 components |
| **Generated** | 2026-07-19 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

#### What Are We Changing?

- Point the **BOM** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (co-located)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

#### Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `BOM-FE-001` | Statically expand BOM fragment factories (pre-cutover) | Refactor | 🔴 High | 3–4 days | — | — |
| `BOM-FE-002` | Migrate BOM core reads | Query migration | 🔴 High | 6–10 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-17`, `BOM-FE-001` | `getBomByIds`, `getBomByParentId`, `getBomStatus`, `getBomComponentStatus` |
| `BOM-FE-003` | Migrate BOM search and elastic reads | Query migration | 🔴 High | 5–8 days | `BOM-BE-C-01`, `BOM-BE-G-01`, `BOM-BE-G-14`, `BOM-BE-S-03` | `getBomElastic`, `searchMaterialsBom` |
| `BOM-FE-004` | Migrate BOM master-data reads | Query migration | 🟢 Low | 2–3 days | `BOM-BE-B-05`, `BOM-BE-B-06`, `BOM-BE-B-07`, `BOM-BE-B-08`, `BOM-BE-G-14` | `getBomMaterialTypes`, `getBomPackagingMaterialTypes`, `getBomPackagingSubstrates`, `getBomPackagingUnitOfMeasure` |
| `BOM-FE-005` | Migrate BOM supplier reads | Query migration | 🟡 Medium | 3–5 days | `BOM-BE-C-03`, `BOM-BE-C-04`, `BOM-BE-C-05` | `getComboSupplierForBom`, `getValidTrimSuppliersForBom`, `getValidRawMaterialSuppliersForBom` |
| `BOM-FE-006` | Migrate BOM mutations including `updateBom` saga handling | Mutation migration (complex) | 🔴 High | 8–12 days | `BOM-BE-D-01`, `BOM-BE-D-03`, `BOM-BE-D-04`, `BOM-BE-D-05`, `BOM-BE-S-01` | `addBom`, `lockBom`, `unlockBom`, `updateBom`, `updateBomComponentStatus` |
| `BOM-FE-007` | Adopt BOM `supplier` entity references (optional, PO-gated) | Query enhancement | 🟢 Low | 2–4 days | `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04`, `BOM-BE-G-01`, `BOM-BE-G-03`, `BOM-BE-G-08`, `BOM-BE-G-12`, `BOM-BE-G-13`, `BOM-BE-G-14`, `BOM-BE-G-17`, `BOM-BE-S-03`, `BOM-FE-002` | `getBomByIds`, `getBomByParentId`, `searchMaterialsBom` |

---

#### Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🔴 `BOM-FE-001` | — | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `BOM-FE-005` | `BOM-FE-005` → `BOM-BE-C-03`, `BOM-BE-C-04`, `BOM-BE-C-05` | Search & listing — needs backend phase C |
| 4 | 🔴 `BOM-FE-002`, 🟢 `BOM-FE-004` | `BOM-FE-002` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04` (+6)<br>`BOM-FE-004` → `BOM-BE-B-05`, `BOM-BE-B-06`, `BOM-BE-B-07`, `BOM-BE-B-08` (+1) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `BOM-FE-003`, 🔴 `BOM-FE-006`, 🟢 `BOM-FE-007` | `BOM-FE-003` → `BOM-BE-C-01`, `BOM-BE-G-01`, `BOM-BE-G-14`, `BOM-BE-S-03`<br>`BOM-FE-006` → `BOM-BE-D-01`, `BOM-BE-D-03`, `BOM-BE-D-04`, `BOM-BE-D-05` (+1)<br>`BOM-FE-007` → `BOM-BE-A-04`, `BOM-BE-B-01`, `BOM-BE-B-03`, `BOM-BE-B-04` (+8) | Externally gated — search/read-hub decision |

**Cutover flow:** `BOM-FE-001` → `BOM-FE-005` → `BOM-FE-002` → `BOM-FE-004` → `BOM-FE-003` → `BOM-FE-006` → `BOM-FE-007`.

---

#### Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 1 | 🔴 `BOM-FE-001` (3–4d) | Reads cutover — needs backend phase A/B reads live |
| 2 | 🟡 `BOM-FE-005` (3–5d) | Search & listing — needs backend phase C |
| 4 | 🔴 `BOM-FE-002` (6–10d)<br>🟢 `BOM-FE-004` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `BOM-FE-006` (8–12d)<br>🔴 `BOM-FE-003` (5–8d)<br>🟢 `BOM-FE-007` (2–4d) | Externally gated — search/read-hub decision |

**Elapsed (nominal midpoints):** ~38 FE build days — calendar time is set by the backend gates, not FE capacity.

---

#### References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-bom.md — the combined Backend + Frontend breakdown this section lives in.

