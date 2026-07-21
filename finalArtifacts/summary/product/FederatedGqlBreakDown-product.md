## Backend

### Federated GraphQL Breakdown — Product

| | |
|---|---|
| **Target DGS** | `plm-product (host)` |
| **T-Shirt Size** | **XXL** |
| **Total Stories** | 69 |
| **Complexity** | 🔴 5 Very High · 🟠 4 High · 🟡 27 Medium · 🟢 33 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H |
| **Generated** | 2026-07-21 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H

---

#### What Are We Building?

- We are moving **Product** — the central entity of the PLM system — off the `spark-internal-graphql` gateway into the **`plm-product`** Netflix DGS.
- Product is the **largest and highest-risk** domain (18 queries, 20 mutations, ~50 field resolvers on a 2,629-line resolver) and the **host service** for the whole product family: BOM, Measurement, Impression, Packaging and others live in the same DGS, so their links from Product resolve **internally** rather than across the federation gateway.

- Most of the work is mechanical (the long tail of CRUD and simple field resolvers), but a handful of items carry real risk: the **TechPack count** query (a ~200-line, 14-step aggregation spanning 8 domains' data via 4 physical services, which becomes a federated composite-key entity), the **partner drop/undrop** orchestration, the cross-domain **components** and **attachmentsWithMetaData** field resolvers, and a **latent `division` bug**.
- We recommend the **facade-then-federate** approach for TechPack (draft **ADR-015** Option B; the pattern `techpack-migration-options.md` labels "Option D (hybrid)"): ship a thin query over a temporary aggregation facade so it works on day 1, then federate each piece to its owning domain, then retire the facade (`F-09`).

**ACL note:** the legacy gateway obtains per-resource capability tokens via ACL on nearly every call. Per
**ADR-019** ([`complexStories/acl/01-adr-acl-mid-request-update.md`](https://github.com/XXX/blob/main/output/complexStories/acl/01-adr-acl-mid-request-update.md)), permission-check and own-domain-token
call sites stay resolver-local (context-only, unchanged); downstream-token call sites — where a resolver
hands its token to a *different* domain's loader — use **Mid-Request ACL Update**
(`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before the downstream call.

---

#### Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 18 | incl. TechPack (Very High) and two-stage `getProducts` |
| Mutations | 20 (+3 deferred) | incl. partner actions + component fan-out |
| Field-resolver stories | ~16 | incl. 2 X-Large (attachmentsWithMetaData, components) |
| External dependencies | 12 EXT + 6 platform | search/attachment/workspace 🔴 |
| Composite-key aggregate | 1 (TechPack `ResourcesCount`) | 8 sibling subgraphs extend it |
| Federation contributions received | 8 | from sibling domains (Phase F placeholders) |
| **Total stories** | **67** | green-field build stories (`G-11` split into `G-11-1`/`G-11-2` = +1). The 3 Phase-0 spike stubs (`S-01`–`S-03`) are tracked as **program spikes** in the global breakdown and Jira, not as rows here |

---

#### Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `PRODUCT-BE-B-10` — `getProductDeptRules(productIds, departmentIds, activeOnly)` | `SPIKE-07` | Product Rules API Ownership |
| 🔴🔬 `PRODUCT-BE-B-11` — `getProductBPRules(productIds, businessPartnerIds, activeOnly)` | `SPIKE-07` | Product Rules API Ownership |
| 🔴🔬 `PRODUCT-BE-C-01` — `getProducts(...)` two-stage hydration | `SPIKE-06a` | Hydration |
| 🔴🔬 `PRODUCT-BE-C-05` — `searchProductRules(...)` | `SPIKE-07` | Product Rules API Ownership |
| 🔴🔬 `PRODUCT-BE-D-01` — `addProduct` | `SPIKE-06b` | Cross-Domain Association |
| 🔴🔬 `PRODUCT-BE-D-02` — `addProducts` (bulk) | `SPIKE-06b` | Cross-Domain Association |
| 🔴🔬 `PRODUCT-BE-D-04` — `updateProduct` | `SPIKE-06b` | Cross-Domain Association |
| 🔴🔬 `PRODUCT-BE-E-00` — `WriteSaga` shared module (Sprint 0, critical path) | `SPIKE-01` | Non-Atomic Write Saga |
| 🔴🔬 `PRODUCT-BE-E-01` — `productBusinessPartnerActions` (REMOVE/DROP/UNDROP) | `SPIKE-03` | Partner Drop/Undrop + Ownership |
| 🔴🔬 `PRODUCT-BE-E-02` — `updateComponentStatuses` (5-loader fan-out) | `SPIKE-01` | Non-Atomic Write Saga |
| 🔴🔬 `PRODUCT-BE-E-03` — `getProductTechPackCountV1` stub + aggregation facade (facade-then-federate, Phase 1) | `SPIKE-02` | TechPack Aggregate |
| 🔴🔬 `PRODUCT-BE-E-04` — `getProductTechPackBulkCountV1` (bulk wrapper, ordering fix) | `SPIKE-02` | TechPack Aggregate |
| 🔴🔬 `PRODUCT-BE-G-07` — `Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status` | `SPIKE-04` | Not-Removable / Undroppable Partners |
| 🔴🔬 `PRODUCT-BE-G-11-1` — `Product.notRemovablePartnerIds` + `notRemovableWorkspaceIds` | `SPIKE-04` | Not-Removable / Undroppable Partners |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

#### Deployment Model — Ship on Green, Per Story

- Every story is **end-to-end in one PR** and **independently deployable to production once its own tests and parity pass** — no waiting for the rest of the phase.
- The **one exception** is a story whose field is produced by **composing another subgraph's data** (a cross-subgraph **entity extension**, `extend type … @key` resolved by a different DGS): those go live only once the **owning subgraph is deployed**, and are marked
**BLOCKED-BY `<domain>`**.

- ✅ **Ships on green** — all B/C/D/E/G stories, the internal Phase-F contributions (`F-04`, `F-06`, `F-08`), the
  gateway/platform stories (`F-10`, `F-11`), and the **TechPack facade** (`E-03`/`E-04`), which is *designed* to
  work day 1 before any sibling federates.
- ⛔ **Waits for an owning subgraph (the exception)** — the true cross-subgraph federation stories
  **`H-01` (attachment), `H-02` (discussion), `H-03` (sample), `H-04` (claim), `H-05` (construction)**, plus
  **`F-09`** (facade retirement, which needs all 8 contributions live). These are the only stories held back
  from per-story prod release.

---

#### Effort Snapshot

| Phase | Name | Stories | Effort (est., +20% buffer) |
|-------|------|---------|----------------------------|
| B | Core Reads | 11 | 13–26d |
| C | Search & Listing | 5 | 14–28d |
| D | Mutations | 18 | 28–55d |
| E | Complex Operations | 5 | 35–60d |
| F | Federation & Stitching | 8 | 10–19d |
| G | Field Resolvers & Tests | 16 | 52–97d |
| H | Entity Resolution | 6 | 14–29d |
| **Total** | | **69** | **166–314d** (buffered) |

> Computed live from `be-04-stories.md` (phase + complexity per story) — always reconciles with the story tables below and the program overview. Effort = sum of per-story nominal day-ranges (Low 1–2 · Medium 2–4 · High 4–7 · Very High 7–12) × 1.2 buffer, AI-estimated — confirm in refinement. See each story's **Depends On** column for real sequencing.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~39–66 sprints | sequential — not recommended for this domain |
| 2 engineers | ~25–42 sprints | B/C/D parallel after B-01 |
| 3–4 engineers | ~18–28 sprints | A done → B + C + D + most of G in parallel; E and the two X-Large fields on dedicated owners |

> Phase G dominates the calendar; the two X-Large field resolvers (`attachmentsWithMetaData`, `components`)
> and TechPack (E-03/E-04) are the cost-and-risk centre of the whole program.

---

#### Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 0 | Program spikes | run in Sprint 0 (see global Phase 0 — Program Spikes) so D/C/E work isn't waiting |
| 1–2 | B-01 (DGS module init + service wiring + first resolver) | schema, types, stubs, Categories resolver, ResourcesCount, service port |
| 3 | B-01–B-11 | all core reads (incl. rules reads) |
| 4 | C-01–C-05 | search/listing + rating + rules search (C-01 needs `SPIKE-06a` concluded) |
| 5–6 | D-01–D-18 | all simple mutations, parallelizable (D-01/D-02/D-04 need `SPIKE-06b` concluded; D-03/D-06/D-07/D-11 unblocked) |
| 7–8 | E-03/E-04 | TechPack facade + bulk (focused; facade-then-federate direction already resolved, draft ADR-015) |
| 9 | E-00 (shared `WriteSaga` module, Sprint-0 critical path) + E-01/E-02 | partner actions (needs `SPIKE-03` concluded) + component fan-out |
| 10–12 | G-01–G-10, G-11-1, G-11-2, G-13–G-14 | field resolvers (G-01/G-02 X-Large get their own sprint) |
| 13 | G-15 | utils port (Kotlin). Test coverage/parity/load/cut-over rehearsal tracked outside this Jira pipeline, created manually. |
| post-launch | H-01–H-06, F-09 | TechPack federation (unblocked as siblings migrate) + facade retirement |
| any | F-10–F-12 | gateway composition + platform verify + drift decision |

---

#### Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟢 `B-06`, 🟢 `B-07`, 🟢 `B-08`, 🟢 `B-09`, 🟢 `B-10`, 🟢 `B-11`, 🟠 `C-01`, 🟡 `C-02`, 🟡 `C-03`, 🟡 `C-04`, 🟡 `C-05`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-03`, 🟡 `D-04`, 🟡 `D-05`, 🟢 `D-06`, 🟢 `D-07`, 🟢 `D-08`, 🟢 `D-09`, 🟢 `D-10`, 🟢 `D-11`, 🟢 `D-12`, 🟢 `D-13`, 🟢 `D-14`, 🟢 `D-15`, 🟢 `D-16`, 🟢 `D-17`, 🟢 `D-18`, 🟠 `E-00`, 🔴 `E-03`, 🟢 `F-14`, 🔴 `G-01`, 🔴 `G-02`, 🟡 `G-04`, 🟡 `G-05`, 🟡 `G-06`, 🟡 `G-07`, 🟡 `G-08`, 🟡 `G-09`, 🟡 `G-10`, 🟡 `G-11-1`, 🟡 `G-11-2`, 🟡 `G-13`, 🟢 `G-14`, 🟡 `G-15`, 🟡 `H-06` | `B-10` → 🔬 SPIKE-07<br>`B-11` → 🔬 SPIKE-07<br>`C-01` → 🔬 SPIKE-06a<br>`C-05` → 🔬 SPIKE-07<br>`D-01` → 🔬 SPIKE-06b<br>`D-02` → 🔬 SPIKE-06b<br>`D-04` → 🔬 SPIKE-06b<br>`E-00` → 🔬 SPIKE-01<br>`E-03` → 🔬 SPIKE-02<br>`G-07` → 🔬 SPIKE-04<br>`G-11-1` → 🔬 SPIKE-04 | Fan-out — 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests · 🧬 Entity Resolution |
| 3 | 🔴 `E-01`, 🟠 `E-02`, 🔴 `E-04`, 🟢 `F-04`, 🟢 `F-06`, 🟢 `F-08`, 🟢 `F-10`, 🟠 `G-03`, 🟡 `G-17`, 🟡 `H-01`, 🟡 `H-02`, 🟡 `H-03`, 🟡 `H-04`, 🟡 `H-05` | `E-01` → 🔬 SPIKE-03<br>`E-02` → 🔬 SPIKE-01<br>`E-04` → 🔬 SPIKE-02<br>`H-01` → ⛔ BLOCKED-BY attachment domain (⛔ cross-subgraph — does not ship until plm-attachment is live)<br>`H-02` → ⛔ BLOCKED-BY discussion domain (⛔ cross-subgraph)<br>`H-03` → ⛔ BLOCKED-BY sample domain (⛔ cross-subgraph)<br>`H-04` → ⛔ BLOCKED-BY claim domain (⛔ cross-subgraph)<br>`H-05` → ⛔ BLOCKED-BY construction domain (⛔ cross-subgraph) | Fan-out — ⚙️ Complex Operations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests · 🧬 Entity Resolution |
| 4 | 🟢 `F-09`, 🟢 `F-11`, 🟢 `F-12` | — | 🔗 Federation & Stitching |

**Critical path:** `B-01` → `E-03` → `F-04` → `F-09` — 4 sequential stories; everything else hangs off this chain in parallel.

---

#### Recommended Story Graph — 1 Backend Engineer

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 1 backend engineer** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 |
|---|---|
| 1 | 🟢 `B-01` (1–2d) |
| 2 | 🔴 `E-03` (7–12d) 🔬 |
| 3 | 🟠 `E-00` (4–7d) 🔬 |
| 4 | 🔴 `G-01` (7–12d) |
| 5 | 🔴 `E-01` (7–12d) 🔬 |
| 6 | 🔴 `E-04` (7–12d) 🔬 |
| 7 | 🔴 `G-02` (7–12d) |
| 8 | 🟡 `H-06` (2–4d) |
| 9 | 🟠 `C-01` (4–7d) 🔬 |
| 10 | 🟠 `E-02` (4–7d) 🔬 |
| 11 | 🟠 `G-03` (4–7d) |
| 12 | 🟢 `F-14` (1–2d) |
| 13 | 🟡 `H-01` (2–4d) ⛔ |
| 14 | 🟡 `H-02` (2–4d) ⛔ |
| 15 | 🟡 `H-03` (2–4d) ⛔ |
| 16 | 🟡 `H-04` (2–4d) ⛔ |
| 17 | 🟡 `H-05` (2–4d) ⛔ |
| 18 | 🟡 `C-02` (2–4d) |
| 19 | 🟡 `C-03` (2–4d) |
| 20 | 🟡 `C-04` (2–4d) |
| 21 | 🟡 `C-05` (2–4d) 🔬 |
| 22 | 🟡 `D-01` (2–4d) 🔬 |
| 23 | 🟡 `D-02` (2–4d) 🔬 |
| 24 | 🟡 `D-03` (2–4d) |
| 25 | 🟡 `D-04` (2–4d) 🔬 |
| 26 | 🟡 `D-05` (2–4d) |
| 27 | 🟢 `F-04` (1–2d) |
| 28 | 🟢 `F-06` (1–2d) |
| 29 | 🟢 `F-08` (1–2d) |
| 30 | 🟢 `F-10` (1–2d) |
| 31 | 🟡 `G-04` (2–4d) |
| 32 | 🟡 `G-05` (2–4d) |
| 33 | 🟡 `G-06` (2–4d) |
| 34 | 🟡 `G-07` (2–4d) 🔬 |
| 35 | 🟡 `G-08` (2–4d) |
| 36 | 🟡 `G-09` (2–4d) |
| 37 | 🟡 `G-10` (2–4d) |
| 38 | 🟡 `G-11-1` (2–4d) 🔬 |
| 39 | 🟡 `G-11-2` (2–4d) |
| 40 | 🟡 `G-13` (2–4d) |
| 41 | 🟡 `G-15` (2–4d) |
| 42 | 🟡 `G-17` (2–4d) |
| 43 | 🟢 `B-02` (1–2d) |
| 44 | 🟢 `B-03` (1–2d) |
| 45 | 🟢 `B-04` (1–2d) |
| 46 | 🟢 `B-05` (1–2d) |
| 47 | 🟢 `B-06` (1–2d) |
| 48 | 🟢 `B-07` (1–2d) |
| 49 | 🟢 `B-08` (1–2d) |
| 50 | 🟢 `B-09` (1–2d) |
| 51 | 🟢 `B-10` (1–2d) 🔬 |
| 52 | 🟢 `B-11` (1–2d) 🔬 |
| 53 | 🟢 `D-06` (1–2d) |
| 54 | 🟢 `D-07` (1–2d) |
| 55 | 🟢 `D-08` (1–2d) |
| 56 | 🟢 `D-09` (1–2d) |
| 57 | 🟢 `D-10` (1–2d) |
| 58 | 🟢 `D-11` (1–2d) |
| 59 | 🟢 `D-12` (1–2d) |
| 60 | 🟢 `D-13` (1–2d) |
| 61 | 🟢 `D-14` (1–2d) |
| 62 | 🟢 `D-15` (1–2d) |
| 63 | 🟢 `D-16` (1–2d) |
| 64 | 🟢 `D-17` (1–2d) |
| 65 | 🟢 `D-18` (1–2d) |
| 66 | 🟢 `F-09` (1–2d) |
| 67 | 🟢 `F-11` (1–2d) |
| 68 | 🟢 `F-12` (1–2d) |
| 69 | 🟢 `G-14` (1–2d) |

**BE-1:** `B-01` → `E-03` → `E-00` → `G-01` → `E-01` → `E-04` → `G-02` → `H-06` → `C-01` → `E-02` → `G-03` → `F-14` → `H-01` → `H-02` → `H-03` → `H-04` → `H-05` → `C-02` → `C-03` → `C-04` → `C-05` → `D-01` → `D-02` → `D-03` → `D-04` → `D-05` → `F-04` → `F-06` → `F-08` → `F-10` → `G-04` → `G-05` → `G-06` → `G-07` → `G-08` → `G-09` → `G-10` → `G-11-1` → `G-11-2` → `G-13` → `G-15` → `G-17` → `B-02` → `B-03` → `B-04` → `B-05` → `B-06` → `B-07` → `B-08` → `B-09` → `B-10` → `B-11` → `D-06` → `D-07` → `D-08` → `D-09` → `D-10` → `D-11` → `D-12` → `D-13` → `D-14` → `D-15` → `D-16` → `D-17` → `D-18` → `F-09` → `F-11` → `F-12` → `G-14`

**Elapsed (nominal midpoints):** ~200 working days.

---

#### Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

##### 📖 Phase B — Core Reads (11 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `PRODUCT-BE-B-01`<br>`getProduct(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up a single product by id (the core product read everything else builds on).<br>**Today —** getByID GET ${v1}?productId={id} → camelCase or null; DataLoader-batched<br>**Done when:**<br>• returns product; 404→null<br>• batches N ids in 1 call |
| 🔷 `PRODUCT-BE-B-02`<br>`getProductsByIds(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up several products at once by their ids.<br>**Today —** getByIdList GET ${v1}?productId={csv}&page=0&size=10000&sort=createdDate,desc; primes getByID<br>**Done when:**<br>• returns paged products for ids<br>• primes single-id loader |
| 🔷 `PRODUCT-BE-B-03`<br>`getProductStatus` (cacheable) | 🟢 Low `XS` | Query | — | **Intent —** Returns the list of possible product statuses (dropdown options).<br>**Today —** getStatus master status list<br>**Done when:**<br>• returns statuses<br>• cached |
| 🔷 `PRODUCT-BE-B-04`<br>`getProductVersions(id)` | 🟢 Low `XS` | Query | — | **Intent —** Lists the saved versions of a product.<br>**Today —** getVersions GET ${v1}/{id}/versions?page=0&size=10000<br>**Done when:**<br>• returns versions |
| 🔷 `PRODUCT-BE-B-05`<br>`getCopyStatus(id)` | 🟢 Low `XS` | Query | — | **Intent —** Tells you whether a product copy is still in progress or done.<br>**Today —** getCopyStatus GET ${v2}/count/resource-type?copyId={id}<br>**Done when:**<br>• returns copy status |
| 🔷 `PRODUCT-BE-B-06`<br>`getProductTemplateById(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up a product template by id.<br>**Today —** getByID → response \\|\\| {} (empty object on miss — preserve)<br>**Done when:**<br>• returns product or empty object (not null) |
| 🔷 `PRODUCT-BE-B-07`<br>`getProductRules` | 🟢 Low `XS` | Query | — | **Intent —** Returns the product business rules.<br>**Today —** getAllRules GET $… → content<br>**Done when:**<br>• returns rules content |
| 🔷 `PRODUCT-BE-B-08`<br>`getProductRulesById(id)` | 🟢 Low `XS` | Query | — | **Intent —** Looks up one business rule by id.<br>**Today —** getRuleById GET $…<br>**Done when:**<br>• returns rule |
| 🔷 `PRODUCT-BE-B-09`<br>`getAllAvailableRules` | 🟢 Low `XS` | Query | — | **Intent —** Lists all the rules that are available to apply.<br>**Today —** getAvailableRules GET …/spark_rules/v1/rules<br>**Done when:**<br>• returns available rules |
| 🔴🔬 🔷 `PRODUCT-BE-B-10`<br>`getProductDeptRules(productIds, departmentIds, activeOnly)`<br>🔴🔬 _Spike-gated on `SPIKE-07` (Product Rules API Ownership) — see global Spike Detail_ | 🟢 Low `XS` | Query<br>Calls: `ruleLibrary` | SPIKE-07 | **Intent —** Returns the department-level rules for given products.<br>**Today —** flag fork USE_NEW_RULES_API ? ruleLibrary.searchRuleLibrary : product.searchProductDeptRules GET …/spark_rules/v1/search?productIds=&departmentIds=&activeOnly=. PO…<br>**Done when:**<br>• default `activeOnly=true`<br>• flag selects the correct backend<br>• Scope reconfirmed against `S-04`'s decision before implementation starts |
| 🔴🔬 🔷 `PRODUCT-BE-B-11`<br>`getProductBPRules(productIds, businessPartnerIds, activeOnly)`<br>🔴🔬 _Spike-gated on `SPIKE-07` (Product Rules API Ownership) — see global Spike Detail_ | 🟢 Low `XS` | Query<br>Calls: `ruleLibrary` | SPIKE-07 | **Intent —** Returns the business-partner-level rules for given products.<br>**Today —** same as B-10 with businessPartnerIds<br>**Done when:**<br>• flag fork honored; BP filter applied<br>• Scope reconfirmed against `S-04`'s decision before implementation starts |

> **`PRODUCT-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `product.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql. **This scaffold is a prerequisite for every B/C/D/G story** — they need the module + schema file to compile their DGS wrapper — so it is assumed globally (shown once in the dependency graph) and **not repeated** in each story's `Depends On`. After it lands, the wrappers parallelize.


##### 🔍 Phase C — Search & Listing (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔷 `PRODUCT-BE-C-01`<br>`getProducts(...)` two-stage hydration<br>🔴🔬 _Spike-gated on `SPIKE-06a` (Hydration) — see global Spike Detail_ | 🟠 High `L` | Query<br>Calls: `search` | SPIKE-06a | **Intent —** List products by combining the search index with the canonical record (two-stage hydration).<br>**Today —** listing products needs data from two places — the search index (which - knows flags like "has boms", "has claims", workspace membership) and the canonical product…<br>**Done when:**<br>• parity for 4 arg combos (no flags / all flags / resourceType=workspaces / filter array)<br>• truthy defaults preserved<br>• elastic flags merged onto canonical<br>• Workspace-filter placement and elastic/canonical staleness handling match `SPIKE-06a`'s decision | ☐ 4 combos<br>☐ default truthiness<br>☐ merge<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔷 `PRODUCT-BE-C-02`<br>`getProductTemplates(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | — | **Intent —** Lists product templates, with optional filters on what to include.<br>**Today —** (search) getFilteredProductsListing({resourceType:'product', includeBoms:false, ...7 includeXxxTemplates flags, types}) → return elastic response (no 2nd hydration)<br>**Done when:**<br>• all 7 template-include flags forwarded<br>• `types:[Int]` filter applied | — |
| 🔷 `PRODUCT-BE-C-03`<br>`getCategories(...)` | 🟡 Medium `M` | Query<br>Calls: `search` | — | **Intent —** Returns the category tree for products.<br>**Today —** default productType ?? 100; (search) getProductCategories GET ${elastic}/search/${snake_case(type)}?resourceType=&resourceId=&productType= → ProductsCategories…<br>**Done when:**<br>• `snake_case(type)` path exact<br>• wires to `Categories` union | — |
| 🔷 `PRODUCT-BE-C-04`<br>`getRatingByTcin(tcin)` (external rating) | 🟡 Medium `M` | Query<br>Calls: `rating` | — | **Intent —** Gets the customer rating for a product (from an external ratings service).<br>**Today —** (external) GET ${RATING_ENDPOINT}?reviewType=product&includes=statistics&reviewedId={tcin}&key={API_KEY} (skipJsonParse) → JSON.parse → {averageRating, reviewCount}…<br>**Done when:**<br>• parses statistics to `Rating`<br>• any error → null<br>• API key from config/Vault, not source | — |
| 🔴🔬 🔷 `PRODUCT-BE-C-05`<br>`searchProductRules(...)`<br>🔴🔬 _Spike-gated on `SPIKE-07` (Product Rules API Ownership) — see global Spike Detail_ | 🟡 Medium `M` | Query<br>Calls: `ruleLibrary` | SPIKE-07 | **Intent —** Searches product rules.<br>**Today —** flag fork; legacy GET …/spark_rules/v1/search_mapped?... → productRuleResponseTransformer → camelCase<br>**Done when:**<br>• flag fork honored<br>• legacy response transformed correctly<br>• Scope reconfirmed against `S-04`'s decision before implementation starts | — |


##### ✏️ Phase D — Mutations (18 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔴🔬 🔶 `PRODUCT-BE-D-01`<br>`addProduct`<br>🔴🔬 _Spike-gated on `SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `workspaceV2`, `attachment` | SPIKE-06b | **Intent —** Create a product (optionally copy from another + associate a workspace).<br>**Today —** POST ${v1} + optional copyProductToProduct(copyProduct) + workspace association<br>**Done when:**<br>• creates product<br>• optional copy runs when `copyProduct` present<br>• workspace assoc applied via the shared association component (no bespoke fan-out code)<br>• failure after create (link or copy fails) surfaces per the mutation's declared failure policy — default fail-fast, no rollback, documented (ADR-011 §4) |
| 🔴🔬 🔶 `PRODUCT-BE-D-02`<br>`addProducts` (bulk)<br>🔴🔬 _Spike-gated on `SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | SPIKE-06b | **Intent —** Create many products at once (plus attachment links).<br>**Today —** bulk POST ${v1}/bulk + attachment-link side-effects (no rollback — preserve, flag)<br>**Done when:**<br>• bulk creates<br>• attachment links applied via the shared association component; no-rollback behaviour documented (compensation deferred to the shared `WriteSaga` module, `PRODUCT-BE-E-00`, per ADR-011 pin-down 2)<br>• no resolver import remains; the formerly fire-and-forget attachment re-point is awaited and its failure visible (accepted deviations per ADR-011 §4) |
| 🔶 `PRODUCT-BE-D-03`<br>`bulkUpdateProducts` | 🟡 Medium `M` | Mutation | — | **Intent —** Update many products in one call.<br>**Today —** PUT ${v1}/mass_update<br>**Done when:**<br>• mass-updates products |
| 🔴🔬 🔶 `PRODUCT-BE-D-04`<br>`updateProduct`<br>🔴🔬 _Spike-gated on `SPIKE-06b` (Cross-Domain Association) — see global Spike Detail_ | 🟡 Medium `M` | Mutation<br>Calls: `attachment` | SPIKE-06b | **Intent —** Edit a product (optional copy + template-attachment cleanup).<br>**Today —** PUT ${v1}/{id} + optional copy + archive removed-template attachments (template branch)<br>**Done when:**<br>• updates product<br>• optional copy<br>• removed-template attachments archived (template branch)<br>• attachment archiving applied via the shared association component (no bespoke fan-out code) |
| 🔶 `PRODUCT-BE-D-05`<br>`carryForwardProduct` | 🟡 Medium `M` | Mutation | — | **Intent —** Carries a product forward (creates the next season/version from it).<br>**Today —** PUT ${v1}/{productId}/carry_forward/{workspaceId} — uses every field on CarryForwardProductInput<br>**Done when:**<br>• all input fields mapped to the request |
| 🔶 `PRODUCT-BE-D-06`<br>`addTeamsToProduct` 🔀 Collab Canvas | 🟢 Low `XS` | Mutation | — | **Intent —** Adds teams (and their partners) to a product.<br>**Today —** POST ${v1}/{productId}/resources/bulk + manage_workspace_teams<br>**Done when:**<br>• adds teams + new partners + workspace links<br>• partner-add failure exits early with a thrown typed error (today `return new Error(...)` — standardized per ADR-011 §4 pin-down 4, accepted deviation); teams are not added after a failed partner add (legacy order preserved) |
| 🔶 `PRODUCT-BE-D-07`<br>`addBusinessPartnersToProductWithType` 🔀 Collab Canvas | 🟢 Low `XS` | Mutation | — | **Intent —** Adds business partners to a product with a given type.<br>**Today —** POST ${v1}/{productId}/partners-add/bulk; success = response has product_id and no status_code; failure = log + return new Error(...) (returned, not thrown — surfaces…<br>**Done when:**<br>• adds partners with type<br>• failure throws a typed `DgsException` instead of `return new Error(...)` (accepted parity deviation, ADR-011 §4 pin-down 4) |
| 🔶 `PRODUCT-BE-D-08`<br>`removeProductResources` | 🟢 Low `XS` | Mutation | — | **Intent —** Removes resources (links) from a product.<br>**Today —** DELETE ${v1}/{productId}/resources/bulk<br>**Done when:**<br>• removes resources |
| 🔶 `PRODUCT-BE-D-09`<br>`updateBusinessPartnerStatuses` | 🟢 Low `XS` | Mutation | — | **Intent —** Updates the status of business partners on a product.<br>**Today —** PUT ${v1}/{productId}/status_update/bulk<br>**Done when:**<br>• updates partner statuses |
| 🔶 `PRODUCT-BE-D-10`<br>`updateViewToggle` | 🟢 Low `XS` | Mutation | — | **Intent —** Toggles whether a product is hidden.<br>**Today —** PUT ${v1} view toggle<br>**Done when:**<br>• toggles hidden |
| 🔶 `PRODUCT-BE-D-11`<br>`updateWorkspaceAttributes` 🔀 Collab Canvas | 🟢 Low `XS` | Mutation | — | **Intent —** Updates a product's workspace attributes.<br>**Today —** PUT ${v1}/{productId} workspace attrs<br>**Done when:**<br>• updates workspace attrs |
| 🔶 `PRODUCT-BE-D-12`<br>`updateProductTeamsWorkspaceContext` | 🟢 Low `XS` | Mutation | — | **Intent —** Adds or removes team↔workspace pairings on a product.<br>**Today —** PUT team-workspace add/remove<br>**Done when:**<br>• adds/removes team-workspace pairs |
| 🔶 `PRODUCT-BE-D-13`<br>`linkProduct` | 🟢 Low `XS` | Mutation | — | **Intent —** Links a parent and child product together.<br>**Today —** PUT link — throws on backend error (only mutation that does)<br>**Done when:**<br>• links parent/child<br>• backend error → exception (not null) |
| 🔶 `PRODUCT-BE-D-14`<br>`unlinkProduct` | 🟢 Low `XS` | Mutation | — | **Intent —** Unlinks a parent and child product.<br>**Today —** PUT unlink<br>**Done when:**<br>• unlinks parent/child |
| 🔶 `PRODUCT-BE-D-15`<br>`addProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Creates a product rule.<br>**Today —** POST …/spark_rules/v1<br>**Done when:**<br>• creates rule |
| 🔶 `PRODUCT-BE-D-16`<br>`updateProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Updates a product rule.<br>**Today —** PUT …/spark_rules/v1/{id}<br>**Done when:**<br>• updates rule |
| 🔶 `PRODUCT-BE-D-17`<br>`deleteProductRule` | 🟢 Low `XS` | Mutation | — | **Intent —** Deletes a product rule.<br>**Today —** DELETE …/spark_rules/v1/{id} → Boolean<br>**Done when:**<br>• deletes; returns Boolean |
| 🔶 `PRODUCT-BE-D-18`<br>`updateComponentStatus` (bulk) | 🟢 Low `XS` | Mutation | — | **Intent —** Bulk-updates the status of many components at once.<br>**Today —** bulk PUT ${v1}/component_status_update/bulk<br>**Done when:**<br>• bulk-updates component statuses |


##### ⚙️ Phase E — Complex Operations (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 📄 `PRODUCT-BE-E-00`<br>`WriteSaga` shared module (Sprint 0, critical path)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Service | SPIKE-01 | **Intent —** Build the one shared "ordered steps + per-step failure policy" mechanism every multi-step write in the program will use, instead of nine domains each guessing their own.<br>**Done when:**<br>• `WriteSaga` executes ordered steps, stops at the first non-retryable failure, and runs declared compensations (in reverse order) for every already-completed step that has one<br>• Every step's response is checked by construction — there is no code path where a step's result is silently ignored (closes ADR-013 pin-down 5)<br>• `finish()` returns `COMMITTED` (all steps succeeded), `COMPENSATED` (a step failed, compensations ran, no net change), or `PARTIAL_FAILURE` (a step failed, some compensations don't exist or also failed) — always with per-step detail, never a bare generic error (ADR-013 pin-down 6; surfaced via GraphQL error extensions by each consumer)<br>• Parallel fan-out steps isolate per-branch failures and aggregate a per-branch result — a `Promise.all`-style first-rejection-wins is not possible through this API (ADR-013 pin-down 7)<br>• Compensation inventory completed and recorded before any consumer story starts: for every step kind in the §4-B policy table, confirm the declared inverse actually exists (workspace associate↔dissociate, relationship add↔remove); anything without a confirmed inverse defaults to `RECORD`, never assumed (ADR-013 pin-down 1 — this is a blocking pre-condition on every consumer story, not optional polish)<br>• Injected mid-sequence failures in unit tests yield `COMPENSATED` or `PARTIAL_FAILURE` with correct per-step detail for at least one `COMPENSATE`, one `RETRY`, and one `RECORD` step in the same saga run<br>• Zero consumer-facing API changes are needed if a later step kind's policy is refined (e.g. Option D's backend-composed atomic endpoints replace a saga step with one call) — the saga's public contract is step-name + action + compensation + policy, nothing consumer-specific leaks in<br>• This story ships alone — no domain's E-phase mutation story is modified here; `MST-BE-E-01` (`updateMeasurement`, the smallest real case) is the designated pilot adopter in its own story, followed by `BOM-BE-E-01`, `PKG-BE-E-01`, `PDTL-BE-E-01`, `WATCHLIST-BE-E-01`, `CLAIM-BE-E-01`, `PRODUCT-BE-E-02`, and the later-phase sample mutations, each per their own story's acceptance criteria | ☐ Unit: a 3-step saga where step 2 fails → step 1's compensation runs, step 3 never runs, result is `COMPENSATED`<br>☐ Unit: a step with `RETRY(n)` policy fails `n` times then still fails → result is `PARTIAL_FAILURE` with that step's detail<br>☐ Unit: a step with `RECORD` policy fails → saga continues past it (not a hard stop), failure recorded in per-step detail<br>☐ Unit: a step declares `COMPENSATE` but its own compensation call also fails → surfaced as `PARTIAL_FAILURE`, not silently swallowed<br>☐ Unit: a 5-branch parallel fan-out where 1 branch fails → the other 4 branches' results are still returned, aggregated<br>☐ Integration: compensation inventory checklist (pin-down 1) run and recorded against real backend endpoints before this story closes |
| 🔴🔬 🔶 `PRODUCT-BE-E-01`<br>`productBusinessPartnerActions` (REMOVE/DROP/UNDROP)<br>🔴🔬 _Spike-gated on `SPIKE-03` (Partner Drop/Undrop + Ownership) — see global Spike Detail_ | 🔴 Very High `XL` | Mutation<br>Calls: `sampleV2`, `recentlyViewed`, `todo`, `favorite` | SPIKE-03, E-00 | **Intent —** Remove / drop / undrop a business partner across a product — a ~220-line orchestrated write.<br>**Today —** removing, dropping, or un-dropping a business partner from a product - isn't one write — it's a ~220-line dispatcher that updates the partner's status and then fans…<br>**Done when:**<br>• all 3 paths reach REST parity (recorded fixtures), incl. the design-partner branch (`skipSamples` when `partnerType == DESIGN_PARTNER`)<br>• partial-failure compensation log/strategy implemented per `SPIKE-03`'s decision (draft ADR-012: per-step policy — partner-status compensate · ACL retry-then-fail · activity/profile retry+reconcile)<br>• cleanup fan-out runs per case, with per-target failure isolation (one cleanup failing is visible and doesn't silently swallow the others)<br>• on DROP, ACL revocation completes **before** the mutation returns success; on UNDROP, ACL restore precedes participant undrops — proven by an automated test, not convention (ADR-012 §4 ordering constraint)<br>• no Relationship-Service traversal and no `UserProfileAttributes` resolver import remain in the ported flow (replaced by participant enumeration + a user-profile client call). > **Note:** ADR-012 pin-down 4 (async-refinement scope — recentlyViewed/todo/favorite/user-profile only, never > ACL or partner status) and pin-down 6 (keep the `actionType` dispatcher shape for phase-1 parity; splitting > is a v2 API question) are scope/architecture statements, not independently testable behavior — no dedicated > AC needed; honored by construction in the service shape above | ☐ REMOVE<br>☐ DROP<br>☐ UNDROP<br>☐ design-partner branch (samples skipped)<br>☐ partial-failure per step<br>☐ ACL-before-return ordering invariant<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔴🔬 🔶 `PRODUCT-BE-E-02`<br>`updateComponentStatuses` (5-loader fan-out)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `claim` | SPIKE-01, E-00 | **Intent —** Update a product's component statuses, fanning out to 5 sibling loaders.<br>**Today —** updating component statuses fans out to 5 places in parallel (bom, - measurement, productDetail, packaging — all internal — plus claim, external). - The bug: a loop…<br>**Done when:**<br>• per-loader failures don't fail siblings<br>• shadow var fixed<br>• parity | ☐ 5-way fan-out<br>☐ partial failure isolation<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔴🔬 🔷 `PRODUCT-BE-E-03`<br>`getProductTechPackCountV1` stub + aggregation facade (facade-then-federate, Phase 1)<br>🔴🔬 _Spike-gated on `SPIKE-02` (TechPack Aggregate) — see global Spike Detail_ | 🔴 Very High `XL` | Query<br>Calls: `attachment`, `search` | SPIKE-02 | **Intent —** Build the TechPack panel's badge counts by aggregating across ~8 domains.<br>**Today —** the TechPack panel shows badge counts (attachments, discussions, - samples, boms, claims, etc.) for a product. - Getting those counts today means walking the entire…<br>**Done when:**<br>• Returns a fully populated 11-field `ResourcesCount` from the facade for a valid `(productId, partnerId, workspaceContext, parentProductId)` input<br>• `@DgsEntityFetcher(name="ResourcesCount")` reconstructs the entity from key + context on an `_entities` query (federation-ready shell)<br>• Recorded-fixture parity vs `spark-internal-graphql` for ≥ 5 pinned inputs, including: a product **with a parent** (double-walk), > 100 walked ids (chunked ACL), a 3D attachment, and a critical thread whose parent discussion is outside the walk — 100% field-value match modulo the ADR-015 §4 deviation list (parallelized elastic/ACL calls; counts unchanged)<br>• Facade is observable: per-slice latency + error metrics and a health endpoint exist (they gate the `H-01`–`H-05` re-homings and the `F-09` retirement check)<br>• Facade is behavior-frozen: deviations limited to ADR-015 §4 pin-downs; `CODEOWNERS` guard in place so new feature work lands in the owning domain's `F0x` story instead | ☐ facade call returns 11 populated fields<br>☐ entity fetcher via `_entities`<br>☐ parity ≥ 5 pinned inputs (incl. parent double-walk, >100 ids, 3D attachment, out-of-walk critical thread)<br>☐ per-slice metrics emitted<br>☐ Integration: full query via DGS test client returns expected shape |
| 🔴🔬 🔷 `PRODUCT-BE-E-04`<br>`getProductTechPackBulkCountV1` (bulk wrapper, ordering fix)<br>🔴🔬 _Spike-gated on `SPIKE-02` (TechPack Aggregate) — see global Spike Detail_ | 🔴 Very High `XL` | Query<br>Calls: `attachment`, `search` | SPIKE-02, E-03 | **Intent —** Return TechPack counts for many products at once, in the caller's order.<br>**Today —** the bulk version runs all N single-product lookups concurrently and - returns them in whatever order they happen to finish — not the order the caller asked for. - If a…<br>**Done when:**<br>• `bulk(P1..Pn) == [single(P1)..single(Pn)]` in input order<br>• empty list → [] | ☐ order preserved<br>☐ empty<br>☐ Parity: DGS response matches spark-internal-graphql baseline |

> **`PRODUCT-BE-E-01`** — **Note:** ADR-012 pin-down 4 (async-refinement scope — recentlyViewed/todo/favorite/user-profile only, never
> ACL or partner status) and pin-down 6 (keep the `actionType` dispatcher shape for phase-1 parity; splitting
> is a v2 API question) are scope/architecture statements, not independently testable behavior — no dedicated
> AC needed; honored by construction in the service shape above.


##### 🔗 Phase F — Federation & Stitching (8 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PRODUCT-BE-F-04`<br>`ResourcesCount.measurementSets` (internal, from Measurement) | 🟢 Low `XS` | Field Resolver | E-03 | **Intent —** Fills in the product's measurement-set count — answered in-process by the co-located Measurement code.<br>**Done when:**<br>• `measurementSets` resolves in-process; no gateway hop; parity vs facade |
| 🔸 `PRODUCT-BE-F-06`<br>`ResourcesCount.productBoms` + `packagingBoms` + `boms` (internal, from BOM) | 🟢 Low `XS` | Field Resolver | E-03 | **Intent —** Fills in the product's BOM counts — answered in-process by the co-located BOM code.<br>**Done when:**<br>• `productBoms`/`packagingBoms`/`boms` resolve in-process; no gateway hop; parity vs facade |
| 🔸 `PRODUCT-BE-F-08`<br>`ResourcesCount.watchlists` (internal, from Watchlist) | 🟢 Low `XS` | Field Resolver | E-03 | **Intent —** Fills in the product's watchlist count — answered in-process by the co-located Watchlist code.<br>**Done when:**<br>• `watchlists` resolves in-process; no gateway hop; parity vs facade |
| 🔸 `PRODUCT-BE-F-09`<br>Retire the TechPack aggregation facade | 🟢 Low `XS` | Field Resolver | H-01, H-02, H-03, F-04, H-04, F-06, H-05, F-08 | **Intent —** Removes the temporary TechPack 'facade' once every count is served by its real owner.<br>**Today —** remove TechPackAggregatorClient; TechPackDataFetcher returns key+context only; decommission the facade<br>**Done when:**<br>• all 11 `ResourcesCount` fields resolve via federation<br>• facade health-check endpoint returns 404 (decommissioned)<br>• no orphaned config (feature flags, Feign client beans, etc. referencing the retired facade) |
| 🔸 `PRODUCT-BE-F-10`<br>Hive Gateway supergraph composition | 🟢 Low `XS` | Field Resolver | H-06, F-14 | **Intent —** Composes all the subgraphs into one federated graph at the gateway.<br>**Today —** add plm-product subgraph URL; verify composition with VMM/IG/CORONA/Doppler stubs; smoke-test cross-subgraph query<br>**Done when:**<br>• supergraph composes<br>• cross-subgraph smoke test passes<br>• composition runs as a CI gate on every schema change (not a one-off) and fails on any `@key`/type-name mismatch between subgraphs (regression guard for federation-review/03 §R1–R5)<br>• zero remaining contract mismatches: `VMM_BusinessPartner`/`VMM_Brand` keyed `id`; every entity keyed `id` (Claims/Packaging/Watchlist/Dieline synthesize `id` from humanId — program decision 2026-07-17); `ProductDetails`/`MeasurementPaged` names aligned |
| 🔸 `PRODUCT-BE-F-11`<br>Platform stub verification (VMM/IG/Doppler/CORONA/APEX) | 🟢 Low `XS` | Field Resolver | F-10 | **Intent —** Verifies each external platform (VMM, IG, etc.) resolves through its stub.<br>**Today —** confirm the gateway resolves full platform types from product-emitted @key stubs<br>**Done when:**<br>• each platform type resolves via its stub key |
| 📄 `PRODUCT-BE-F-12`<br>Deferred partner-wrapper decision (drift mutations) | 🟢 Low `XS` | Schema | E-01 | **Intent —** Decide the fate of three drift partner mutations that have no resolvers.<br>**Today —** three old mutation names (removeProductBusinessPartner, - dropProductBusinessPartner, unDropProductBusinessPartner) still exist in the schema, but nothing calls them…<br>**Done when:**<br>• traffic survey complete<br>• decision implemented |
| 📄 `PRODUCT-BE-F-14`<br>Cross-subgraph contract alignment (keys, type names, paged wrappers) | 🟢 Low `XS` | Schema | — | **Intent —** Fixes the naming/key mismatches between product's stubs and the owning schemas so the supergraph can actually compose.<br>**Done when:**<br>• `plm-product` schema compiles standalone with every referenced type declared (including `TeamPaged`, `TeamPagedV2`, `WorkspacesPagedV2`, `DiscussionElastic`)<br>• `hive compose` over plm-product + spark-claims + platform stubs reports zero key/name conflicts, including zero `@shareable` field-shape conflicts on `TeamPaged` (must match claims' declaration exactly)<br>• `CORONA_ItemDetails` entity form implemented per the 2026-07-17 decision (keyed `tcinId`; Corona inflates via the gateway)<br>• Blocks released: F-10, CLAIM-BE-H-01, CLAIM-BE-H-02 |


##### 🧪 Phase G — Field Resolvers & Tests (16 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `PRODUCT-BE-G-01`<br>`Product.attachmentsWithMetaData` | 🔴 Very High `XL` | Field Resolver<br>Calls: `attachment`, `relationship` | — | **Intent —** Resolve a product's mixed attachments-with-metadata feed (files + discussions + samples).<br>**Today —** the attachments panel on a product shows a mixed feed — actual file - attachments, plus discussions and samples that are also surfaced as if they were attachments…<br>**Done when:**<br>• parity for mixed attachment/discussion/thread/sample<br>• ordering rank preserved (product=0, discussion=1, sample=2; createdAt DESC tiebreak)<br>• product side hydrates both v2 and v3 attachment ids (no v2-ignoring gap) — the workspace-side v2-ignoring behaviour (ADR-018 pin-down 2) does not apply here; confirmed by fixture<br>• thread→parent-discussion lookup guarded — a thread whose parent discussion falls outside the walk is skipped + logged, not a crash (accepted deviation, ADR-018 pin-down 3)<br>• discussion data sourced via a direct discussion-service client + one batched replies call — the cross-resolver import and the per-discussion reply N+1 are both gone (ADR-018 pin-down 4)<br>• `attachmentElasticResponseFeatureFlag` state surveyed across every environment BEFORE fixtures are recorded — blocking precondition on fixture recording (ADR-018 pin-down 5)<br>• draft-filter TODO ("ACL should be doing this") kept verbatim in the ported code — filter not removed; ACL-enforcement backlog item filed separately (ADR-018 pin-down 7)<br>• `createAttachmentPaged`'s `relatedResources` precedence bug preserved exactly as today's output — pinned by a fixture using a row with its own non-empty `relatedResources` (ADR-018 pin-down 9)<br>• independent fetches (token, discussions, threads, samples) run in parallel — accepted performance fix (ADR-018 pin-down 10). > **Note:** the missing-ACL skip+log behaviour here is intentionally asymmetric with `G-02`'s missing-ACL throw (ADR-014 pin-down 2) — each surface's UI is calibrated to its own behaviour; this asymmetry is by design (ADR-018 pin-down 8) and should not be "fixed" to match | ☐ merge<br>☐ ordering<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `PRODUCT-BE-G-02`<br>`Product.components` | 🔴 Very High `XL` | Field Resolver<br>Calls: `search` | — | **Intent —** List everything attached to a product, tagged by type, with counts.<br>**Today —** the components tab lists everything attached to a product — measurements, - claims, boms, product-details, packaging — tagged by type, with counts (how many are…<br>**Done when:**<br>• parity for 50+ components, incl. a product with > 100 components (chunked ACL) and a claim with a missing ACL record (throw path preserved, ADR-014 pin-down 2)<br>• `archivedCount`/`countByComponents` match source exactly (incl. name/status fallbacks and `type 2 → packagingBom`)<br>• ACL batched — exactly one `getAccessControlBatch` call per resolution (no N+1), asserted by a call-count test<br>• no `info.variableValues` read; explicit field args confirmed against UI queries (contract test, ADR-014 pin-down 5)<br>• sample→discussion **+1** roll-up quirk preserved exactly, not "fixed" to real counts — pinned by a dedicated fixture documenting the quirk as intentional (ADR-014 pin-down 4)<br>• packaging elastic query joins the 4-way `Promise.all` (5-way parallel) instead of running sequentially after — accepted performance fix, not a behaviour change (ADR-014 pin-down 7). > **Note:** ADR-014 pin-downs 3 (`counts` scalar-`0` → zeros-object fix) and 8 (`WorkspaceV2.products` include-flags delegation) are `WorkspaceV2`-side, not `Product`-side — they belong to the later-phase `WorkspaceV2` twin story (`WORKSPACE-BE-G-02`/`G-04`), not here | ☐ merge<br>☐ counts<br>☐ batched ACL<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `PRODUCT-BE-G-03`<br>`Product.attachments` + `attachmentsV3` + `attachmentSummary` + `ProductTemplate.attachmentsData` | 🟠 High `L` | Field Resolver<br>Calls: `attachment`, `search` | G-01 | **Intent —** Resolve the product's attachment views (via a shared enrichment service).<br>**Today —** four related resolvers sharing AttachmentEnrichmentService (G-01)<br>**Done when:**<br>• each field returns its shape<br>• shares G-01 service<br>• thin fields inherit all of `G-01`'s fixtures/pin-downs by construction (no separate fixture set) | ☐ each field<br>☐ draft discussion attachment fixture (draft filter)<br>☐ workspace-v2-only-attachments fixture<br>☐ both `attachmentsV3` modes (args-present elastic vs args-absent walk/flag) produce parity output<br>☐ Parity: DGS response matches spark-internal-graphql baseline |
| 🔸 `PRODUCT-BE-G-04`<br>`ProductsCategories.categories` (12-case) + `DopplerDepartment` fields | 🟡 Medium `M` | Field Resolver<br>Calls: `doppler` | — | **Intent —** Resolve the polymorphic categories union (12 branches) and department fields.<br>**Today —** categories is a polymorphic union — depending on which category type - the caller asked for, a different one of 12 branches builds the response shape. - Two of those…<br>**Done when:**<br>• each category type built correctly<br>• Doppler fetched once | — |
| 🔸 `PRODUCT-BE-G-05`<br>`Product.samples` + `sampleIds` + `elasticSamplesList` | 🟡 Medium `M` | Field Resolver<br>Calls: `sampleV2`, `search` | — | **Intent —** Resolve a product's samples from local context (removing the fragile args hack).<br>**Today —** today these fields reach into GraphQL's internal info.variableValues to read arguments that were passed to a different, parent query — a fragile, implicit way to pass…<br>**Done when:**<br>• samples/sampleIds/elastic resolve<br>• no `info.variableValues` read | — |
| 🔸 `PRODUCT-BE-G-06`<br>`Product.teams` + `discussionsV2` + `discussionsCount` + `workspaces` | 🟡 Medium `M` | Field Resolver<br>Calls: `teamV2`, `discussion`, `search`, `workspaceV2` | — | **Intent —** Resolve a product's team / discussion / workspace fields.<br>**Today —** team/discussion/workspace elastic lookups<br>**Done when:**<br>• each field resolves | — |
| 🔴🔬 🔸 `PRODUCT-BE-G-07`<br>`Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status`<br>🔴🔬 _Spike-gated on `SPIKE-04` (Not-Removable / Undroppable Partners) — see global Spike Detail_ | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm` | SPIKE-04 | **Intent —** Resolve a product's partner fields (with id normalization).<br>**Today —** business-partner ids sometimes arrive as strings that need to be - parsed to ints before VMM will accept them (vmmUtils's int-parse normalization) — an easy detail to…<br>**Done when:**<br>• partners resolve via VMM<br>• `status` merge correct | — |
| 🔸 `PRODUCT-BE-G-08`<br>`Product.measurementSets` + `claims` + `bom` + `productBom` + `packagingBom` + `productDetails` + `variations` + `associateProductsAsks` | 🟡 Medium `M` | Field Resolver | — | **Intent —** Resolve the 8 'ask a sibling domain' product fields (bom, measurement, …), each on demand.<br>**Today —** each of these 8 fields is "go ask a sibling domain (bom, measurement, - etc.) for this product's data" — but only if the caller asked for it (each has an includeXxx…<br>**Done when:**<br>• each sibling field resolves internally<br>• `includeXxx` branches honored | — |
| 🔸 `PRODUCT-BE-G-09`<br>`Product.productWorkspaceAttributes` + `productWorkspaceInfo` | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `search`, `tag` | — | **Intent —** Resolve a product's per-workspace attributes (incl. lazy designCycle).<br>**Today —** designCycle is computed lazily today — an inline async () => ... - closure attached to the value, evaluated only if a caller actually reads that sub-field. -…<br>**Done when:**<br>• both fields resolve<br>• `designCycle` is a nested fetcher | — |
| 🔸 `PRODUCT-BE-G-10`<br>`Product.ancestryProducts` + `rating` + `reservedDpcis` | 🟡 Medium `M` | Field Resolver<br>Calls: `relationship`, `rating`, `apex` | — | **Intent —** Resolve a product's ancestry, rating and reserved-DPCI fields.<br>**Today —** rating via RatingClient; reservedDpcis via getReservedDpcisFromApex<br>**Done when:**<br>• ancestry/rating/dpcis resolve<br>• rating null-on-error | — |
| 🔴🔬 🔸 `PRODUCT-BE-G-11-1`<br>`Product.notRemovablePartnerIds` + `notRemovableWorkspaceIds`<br>🔴🔬 _Spike-gated on `SPIKE-04` (Not-Removable / Undroppable Partners) — see global Spike Detail_ | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm`, `workspaceV2` | SPIKE-04 | **Intent —** Compute which partners/workspaces can't be removed (still referenced).<br>**Today —** to figure out which partners/workspaces can't be removed from a product (e.g. because they're the last remaining owner), today's code calls into 4-5 other field…<br>**Done when:**<br>• `notRemovablePartnerIds`/`notRemovableWorkspaceIds` return the same results as source (same logical union of the underlying sibling data)<br>• No reflective resolver invocation remains — every call is a direct, statically-typed service method call<br>• samples lane's `variableValues` coupling contract-checked against the UI's samples queries BEFORE cutover — this is a blocking pre-condition, not a nice-to-have (ADR-016 pin-down 2)<br>• the 5 sequential source fetches (discussions/attachments/components/samples/watchlists) parallelize — accepted deviation, union output is order-insensitive (ADR-016 pin-down 3)<br>• the serial ACL chunk loop (`getAccessControlBatch`) parallelizes — same fix family as ADR-015 pin-down 3 (ADR-016 pin-down 4)<br>• watchlist lane's `productWorkspaceInfo[0]`-only / first-workspace-only scope preserved exactly as today's semantics (ADR-016 pin-down 8)<br>• the Relationship-Service walk inside `unDroppablePartners`'s owner-enumeration client is a quarantined interim — each lane's future arrival deletes its own share of the walk (ADR-016 pin-down 9)<br>• schema-diff gate proves no lane field (`…PartnerIds` naming + externals until fed-2/`@inaccessible` is usable) is exposed to clients (ADR-016 pin-down 10) | — |
| 🔸 `PRODUCT-BE-G-11-2`<br>`Product.associateProductsAsks` + `Product.variations` | 🟡 Medium `M` | Field Resolver | — | **Intent —** Resolve two sibling passthroughs (product-asks and variations).<br>**Today —** two straightforward sibling passthroughs — associateProductsAsks - (the product-ask records tied to this product) and variations (sibling product variation records) —…<br>**Done when:**<br>• `associateProductsAsks` resolves the product's ask records<br>• `variations` resolves the product's variation records | — |
| 🔸 `PRODUCT-BE-G-13`<br>IG/tag/tcin/spg + template trivial-field group | 🟡 Medium `M` | Field Resolver<br>Calls: `ig`, `tag`, `corona` | — | **Intent —** Resolve a group of trivial IG / tag / TCIN / template fields.<br>**Today —** department/departments/clazz/brand/brands/divisions/productTemplateDepartments, tags, tcins, SPARK_Tcin.itemDetails (CORONA), SPARK_PackagingAttribute.spg (internal…<br>**Done when:**<br>• each field resolves to the right source | — |
| 🔸 `PRODUCT-BE-G-14`<br>Simple user/status fields + trivial pass-throughs (bundle) | 🟢 Low `XS` | Field Resolver<br>Calls: `userAttributes` | — | **Intent —** Resolve simple people / status fields and trivial pass-throughs.<br>**Today —** createdBy/updatedBy/versionCreatedBy (user-profile), ProductComponentStatus.updatedBy, SPARK_ResourcesCount.productThumbnailId (re-fetch product), plus ~60 direct…<br>**Done when:**<br>• user fields resolve (null id → null)<br>• `productThumbnailId` re-fetches<br>• scalars mapped | — |
| 📄 `PRODUCT-BE-G-15`<br>Port product utils to Kotlin | 🟡 Medium `M` | Service | — | **Intent —** Port the shared product utility helpers to Kotlin.<br>**Today —** attachmentUtils, partnerUtils, teamUtils, productUtils, componentStatusUtils, resolvePaging, vmmUtils, accessControlUtils, removePartnerUtils<br>**Done when:**<br>• utils ported with unit tests<br>• counter logic fixed/verified<br>• ACL batch parallel-chunked | — |
| 🔸 `PRODUCT-BE-G-17`<br>Entity references on partner/lineage value types (recommended, PO-gated) | 🟡 Medium `M` | Field Resolver<br>Calls: `vmm` | G-01 | **Intent —** Adds `partner { … }` / `product { … }` object fields next to the existing ids on the<br>**Today —** schema adds partner: VMM_BusinessPartner (emit {id} key stub — the gateway<br>**Done when:**<br>• PO approval recorded (OQ-5) before implementation starts<br>• New object fields resolve; all existing id fields unchanged<br>• `product` lineage refs batch via DataLoader (no N+1 on `ancestryProducts`)<br>• Codegen/contract parity suite passes with the additive fields present | — |

> **`PRODUCT-BE-G-01`** — **Note:** the missing-ACL skip+log behaviour here is intentionally asymmetric with `G-02`'s missing-ACL throw (ADR-014 pin-down 2) — each surface's UI is calibrated to its own behaviour; this asymmetry is by design (ADR-018 pin-down 8) and should not be "fixed" to match.

> **`PRODUCT-BE-G-02`** — **Note:** ADR-014 pin-downs 3 (`counts` scalar-`0` → zeros-object fix) and 8 (`WorkspaceV2.products` include-flags delegation) are `WorkspaceV2`-side, not `Product`-side — they belong to the later-phase `WorkspaceV2` twin story (`WORKSPACE-BE-G-02`/`G-04`), not here.


##### 🧬 Phase H — Entity Resolution (6 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `PRODUCT-BE-H-01`<br>`ResourcesCount.productAttachments` + `discussionAttachments` (federated, from Attachment) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Contribute attachment counts to the product's TechPack rollup (from Attachment).<br>**Done when:**<br>• `productAttachments`/`discussionAttachments` resolve on the federated `ResourcesCount`; the `E-03` facade stops populating them<br>• Parity vs the facade for the same inputs<br>• Field is live in prod only after `plm-attachment` is deployed (ship gate honored) |
| 🔸 `PRODUCT-BE-H-02`<br>`ResourcesCount.discussions` (federated, from Discussion) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's discussion count — answered by the Discussion service once it's live.<br>**Done when:**<br>• `discussions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `plm-discussion` is deployed |
| 🔸 `PRODUCT-BE-H-03`<br>`ResourcesCount.sample` (federated, from Sample) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's sample count — answered by the Sample service once it's live.<br>**Done when:**<br>• `sample` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `plm-sample` is deployed |
| 🔸 `PRODUCT-BE-H-04`<br>`ResourcesCount.claims` (federated, from Claim) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's claims count — answered by the Claims service once it's live.<br>**Done when:**<br>• `claims` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after `spark-claims` is deployed |
| 🔸 `PRODUCT-BE-H-05`<br>`ResourcesCount.constructions` (federated, from Construction) | 🟡 Medium `M` | Field Resolver | E-03 | **Intent —** Fills in the product's construction count — answered by the Construction service once it's live.<br>**Done when:**<br>• `constructions` resolves on the federated `ResourcesCount`; facade stops populating it; parity vs facade<br>• Live in prod only after the construction subgraph is deployed |
| 🔸 `PRODUCT-BE-H-06`<br>`Product` entity fetcher (`@DgsEntityFetcher`) for cross-subgraph references | 🟡 Medium `M` | Field Resolver | B-01 | **Intent —** Lets *other* subgraphs (today: claims) turn a bare `Product{id}` reference into a full product through the gateway.<br>**Today —** @DgsEntityFetcher(name = "Product") → `productService<br>**Done when:**<br>• `_entities` resolves `Product` representations with a single batched backend call<br>• Unknown ids yield `null` entries without failing the whole `_entities` response<br>• End-to-end: a claims-subgraph query `{ getClaims { product { description } } }` hydrates through the gateway (pairs with CLAIM-BE-G-03)<br>• No ACL plumbing introduced |



---

## Frontend

### Federated GraphQL Breakdown — Product · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `plm-product (host)` |
| **Total FE Stories** | 13 |
| **Impact** | 🔴 3 High · 🟡 9 Medium · 🟢 1 Low |
| **Estimated effort** | 68–104 days (single-engineer) |
| **Phase-1 surface** | 66 operation-to-root-field rows · 20 client files · 48 components |
| **Generated** | 2026-07-21 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

#### What Are We Changing?

- Point the **Product** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `plm-product (host)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

#### Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `PRODUCT-FE-001` | Migrate all `getProduct` documents (single root query, 17 flavors) | Query migration | 🔴 High | 13–19 days | `PRODUCT-BE-B-01`, `PRODUCT-BE-F-10`, `PRODUCT-BE-G-01`, `PRODUCT-BE-G-02`, `PRODUCT-BE-G-03`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-08`, `PRODUCT-BE-G-09`, `PRODUCT-BE-G-10`, `PRODUCT-BE-G-13`, `PRODUCT-BE-G-14`, `PRODUCT-BE-S-01`, `PRODUCT-BE-B-04` | `getProduct` |
| `PRODUCT-FE-002` | Migrate `getProducts` documents (list/search/bulk-create) | Query migration | 🔴 High | 6–9 days | `PRODUCT-BE-B-02`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-02` | `getProducts` |
| `PRODUCT-FE-003` | Migrate `getProductsByIds` documents (bulk-by-id reads) | Query migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-B-03` | `getProductsByIds` |
| `PRODUCT-FE-004` | Migrate `getProductStatus` documents | Query migration | 🟡 Medium | 5–8 days | `PRODUCT-BE-B-01`, `PRODUCT-BE-B-02`, `PRODUCT-BE-B-03`, `PRODUCT-BE-F-10`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-09`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-01` | `getProductStatus` |
| `PRODUCT-FE-005` | Migrate `getProductTemplates` documents | Query migration | 🟡 Medium | 6–9 days | `PRODUCT-BE-B-03`, `PRODUCT-BE-C-02`, `PRODUCT-BE-C-03`, `PRODUCT-BE-G-03`, `PRODUCT-BE-G-04`, `PRODUCT-BE-G-06`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-08`, `PRODUCT-BE-G-13`, `PRODUCT-BE-G-14`, `PRODUCT-BE-H-07`, `PRODUCT-BE-S-01`, `PRODUCT-BE-S-02` | `getProductTemplates` |
| `PRODUCT-FE-006` | Migrate `getCategories` documents | Query migration | 🟢 Low | 2–3 days | `PRODUCT-BE-G-03`, `PRODUCT-BE-G-13` | `getCategories` |
| `PRODUCT-FE-007` | Migrate product rules administration | Query + mutation migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-B-07`, `PRODUCT-BE-B-08`, `PRODUCT-BE-B-09`, `PRODUCT-BE-B-10`, `PRODUCT-BE-B-11`, `PRODUCT-BE-C-05`, `PRODUCT-BE-D-15`, `PRODUCT-BE-D-16`, `PRODUCT-BE-D-17`, `PRODUCT-BE-G-07`, `PRODUCT-BE-G-13`, `PRODUCT-BE-H-08` | `getProductRules`, `getProductRulesById`, `getAllAvailableRules`, `getProductDeptRules`, `getProductBPRules`, `searchProductRules`, `addProductRule`, `updateProductRule`, `deleteProductRule` |
| `PRODUCT-FE-008` | Migrate simple product mutations | Mutation migration | 🟡 Medium | 6–10 days | `PRODUCT-BE-D-01`, `PRODUCT-BE-D-02`, `PRODUCT-BE-D-03`, `PRODUCT-BE-D-04`, `PRODUCT-BE-D-05`, `PRODUCT-BE-D-10`, `PRODUCT-BE-D-13`, `PRODUCT-BE-D-14` | `addProduct`, `addProducts`, `updateProduct`, `bulkUpdateProducts`, `carryForwardProduct`, `updateViewToggle`, `linkProduct`, `unlinkProduct` |
| `PRODUCT-FE-009` | Migrate team and partner assignment mutations | Mutation migration | 🟡 Medium | 4–6 days | `PRODUCT-BE-D-06`, `PRODUCT-BE-D-07`, `PRODUCT-BE-D-12`, `PRODUCT-FE-001` | `addTeamsToProduct`, `addBusinessPartnersToProductWithType`, `updateProductTeamsWorkspaceContext` |
| `PRODUCT-FE-010` | Migrate partner drop/undrop orchestration | Mutation migration (complex) | 🔴 High | 8–12 days | `PRODUCT-BE-S-03`, `PRODUCT-BE-D-09` | `productBusinessPartnerActions`, `updateBusinessPartnerStatuses` |
| `PRODUCT-FE-011` | Migrate TechPack count queries (facade-then-federate) | Query migration (staged) | 🟡 Medium | 4–6 days (step 1) + 4–6 days (step 2) | `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-F-06`, `PRODUCT-BE-F-08`, `PRODUCT-BE-G-08`, `PRODUCT-BE-H-01`, `PRODUCT-BE-H-02`, `PRODUCT-BE-H-03`, `PRODUCT-BE-H-04`, `PRODUCT-BE-H-05` | `getProductTechPackCountV1`, `getProductTechPackBulkCountV1` |
| `PRODUCT-FE-012` | Migrate component status mutations and rollup counts | Mutation migration | 🟡 Medium | 3–5 days | `PRODUCT-BE-D-18`, `PRODUCT-BE-E-02`, `PRODUCT-FE-001` | `updateComponentStatus`, `updateComponentStatuses` |
| `PRODUCT-FE-013` | Verify fragment type-conditions, `__typename` logic and cache keys against federated type names | Verification / refactor | 🟡 Medium | 3–5 days | `PRODUCT-BE-F-14` | `cross-cutting (no single operation)` |

---

#### Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟡 `PRODUCT-FE-003` | `PRODUCT-FE-003` → `PRODUCT-BE-B-03` | Reads cutover — needs backend phase A/B reads live |
| 3 | 🟡 `PRODUCT-FE-008` | `PRODUCT-FE-008` → `PRODUCT-BE-D-01`, `PRODUCT-BE-D-02`, `PRODUCT-BE-D-03`, `PRODUCT-BE-D-04` (+4) | Writes — needs backend phase D mutations |
| 4 | 🟢 `PRODUCT-FE-006`, 🟡 `PRODUCT-FE-007`, 🟡 `PRODUCT-FE-011`, 🟡 `PRODUCT-FE-013` | `PRODUCT-FE-006` → `PRODUCT-BE-G-03`, `PRODUCT-BE-G-13`<br>`PRODUCT-FE-007` → `PRODUCT-BE-B-07`, `PRODUCT-BE-B-08`, `PRODUCT-BE-B-09`, `PRODUCT-BE-B-10` (+8)<br>`PRODUCT-FE-011` → `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04`, `PRODUCT-BE-F-06`, `PRODUCT-BE-F-08` (+6)<br>`PRODUCT-FE-013` → `PRODUCT-BE-F-14` | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `PRODUCT-FE-001`, 🔴 `PRODUCT-FE-002`, 🟡 `PRODUCT-FE-004`, 🟡 `PRODUCT-FE-005`, 🔴 `PRODUCT-FE-010` | `PRODUCT-FE-001` → `PRODUCT-BE-B-01`, `PRODUCT-BE-F-10`, `PRODUCT-BE-G-01`, `PRODUCT-BE-G-02` (+10)<br>`PRODUCT-FE-002` → `PRODUCT-BE-B-02`, `PRODUCT-BE-G-13`, `PRODUCT-BE-S-02`<br>`PRODUCT-FE-004` → `PRODUCT-BE-B-01`, `PRODUCT-BE-B-02`, `PRODUCT-BE-B-03`, `PRODUCT-BE-F-10` (+5)<br>`PRODUCT-FE-005` → `PRODUCT-BE-B-03`, `PRODUCT-BE-C-02`, `PRODUCT-BE-C-03`, `PRODUCT-BE-G-03` (+9)<br>`PRODUCT-FE-010` → `PRODUCT-BE-S-03`, `PRODUCT-BE-D-09` | Externally gated — search/read-hub decision |
| 6 | 🟡 `PRODUCT-FE-009`, 🟡 `PRODUCT-FE-012` | `PRODUCT-FE-009` → `PRODUCT-BE-D-06`, `PRODUCT-BE-D-07`, `PRODUCT-BE-D-12`<br>`PRODUCT-FE-012` → `PRODUCT-BE-D-18`, `PRODUCT-BE-E-02` | Follow-on cutover — after the stories it depends on |

**Cutover flow:** `PRODUCT-FE-003` → `PRODUCT-FE-008` → `PRODUCT-FE-006` → `PRODUCT-FE-007` → `PRODUCT-FE-011` → `PRODUCT-FE-013` → `PRODUCT-FE-001` → `PRODUCT-FE-002` → `PRODUCT-FE-004` → `PRODUCT-FE-005` → `PRODUCT-FE-010` → `PRODUCT-FE-009` → `PRODUCT-FE-012`.

---

#### Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 1 | 🟡 `PRODUCT-FE-003` (4–6d) | Reads cutover — needs backend phase A/B reads live |
| 3 | 🟡 `PRODUCT-FE-008` (6–10d) | Writes — needs backend phase D mutations |
| 4 | 🟡 `PRODUCT-FE-007` (4–6d)<br>🟡 `PRODUCT-FE-011` (4–6d)<br>🟡 `PRODUCT-FE-013` (3–5d)<br>🟢 `PRODUCT-FE-006` (2–3d) | Complex writes / sagas — needs backend phase E + ADR ratification |
| 5 | 🔴 `PRODUCT-FE-001` (13–19d)<br>🔴 `PRODUCT-FE-010` (8–12d)<br>🔴 `PRODUCT-FE-002` (6–9d)<br>🟡 `PRODUCT-FE-005` (6–9d)<br>🟡 `PRODUCT-FE-004` (5–8d) | Externally gated — search/read-hub decision |
| 6 | 🟡 `PRODUCT-FE-009` (4–6d)<br>🟡 `PRODUCT-FE-012` (3–5d) | Follow-on cutover — after the stories it depends on |

**Elapsed (nominal midpoints):** ~86 FE build days — calendar time is set by the backend gates, not FE capacity.

---

#### References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-product.md — the combined Backend + Frontend breakdown this section lives in.

