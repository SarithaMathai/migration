# Federated GraphQL — Migration Overview · All Domains

> **Program overview** — the full `spark-internal-graphql` → Netflix DGS migration at a glance. Each domain's phase tables live in its own FederatedGqlBrakDown-<domain> breakdown page (see the Domain Index); the complex, cross-cutting problems are centralized here as **program spikes** (below).

| | |
|---|---|
| **Program** | `spark-internal-graphql` → Netflix DGS Federation (Hive Schema Registry) |
| **Domains** | 8 |
| **Target DGS services** | 2 |
| **Total Stories** | **200** |
| **Complexity** | 🔴 6 Very High · 🟠 13 High · 🟡 76 Medium · 🟢 105 Low |
| **Phase Coverage** | 🔬 7 Spikes · 🧱 A Foundation · 📖 B Reads · 🔍 C Search · ✏️ D Mutations · ⚙️ E Complex · 🔗 F Federation · 🧪 G Field-resolvers/Tests |
| **Cross-domain spikes** | 🔬 7 program-level research spikes (`SPARK-SPIKE-06` split into `06a` Hydration / `06b` Association) — see *Phase 0 — Program Spikes* below. Only genuinely **complex** problems that need a solve/migrate approach are spikes; straightforward decisions are resolved inline in the owning story. |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## Overview

We are migrating the entire Product Lifecycle Management (PLM) GraphQL API surface off the monolithic `spark-internal-graphql` Node.js gateway onto a set of independently owned **Netflix DGS** (Domain Graph Service) subgraphs, federated via the **Hive Schema Registry**.

Each DGS is a Kotlin/Spring Boot service that exposes its domain's schema as a federated subgraph. The supergraph stitches them together transparently for clients.

**Why?**

- The monolith is a ~15,000-line Node.js resolver with no clear ownership boundaries
- Federation gives each team autonomous schema ownership, independent deployability, and fine-grained caching
- Netflix DGS provides production-proven tooling (DataLoaders, code generation, Hive integration)
- Hive Schema Registry enforces schema contracts and enables safe rollout with schema checks

**Engineering model:** every story is self-contained in one PR — schema additions, DGS data fetcher, Kotlin REST service method, and Hive registry push. There are no separate service-layer stories.

**ACL note:** the current gateway obtains per-resource ACL capability tokens. ACL is **not** re-implemented in the DGS layer (decided at program level); it is noted in stories for context only.

---

## Glossary

| Term | Meaning |
|---|---|
| **DGS** | Netflix Domain Graph Service — a Spring/Kotlin GraphQL subgraph |
| **Hive Gateway / plm-gateway** | the federation gateway that composes the subgraphs into one supergraph |
| **subgraph** | one DGS (e.g. `plm-product`, `plm-sample`) |
| **co-located** | a domain compiling into `plm-product` (in-process call, not a gateway hop) |
| **CAT-1…5** | story categories: 1 schema · 2 resolver · 3 service · 4 federation · 5 tests |
| **Phase A–G** | the migration order within a domain (see the phases table below) |
| **EXT severity** | 🔴 critical/sequential · 🟡 single enrichment call · 🔵 optional/gateway |

---

## The migration phases (A→G) — the order of replacement

Stories are grouped into phases that encode the replacement order within a domain:

| Phase | Replaces / builds | Category |
|---|---|---|
| **A** | schema skeleton, owned types, external stubs, `@DgsTypeResolver`, service port, ACL/JWT plumbing | CAT-1/CAT-3 |
| **B / C** | query resolvers (reads) | CAT-2 |
| **D** | mutation resolvers (writes) | CAT-2 |
| **E** | complex operations (multi-step writes, aggregations) — often a stub + facade pointing at a complex case | CAT-2 |
| **F** | federation boundaries — one story per cross-domain edge (`@extends @external`) | CAT-4 |
| **G** | field resolvers (incl. the heavy ones) + the domain parity harness | CAT-2/CAT-5 |

> **Phase 0 = Spikes** — time-boxed research producing a recorded decision before the phase it blocks.

---

## How to read the spikes & related stories

> The `SPARK-SPIKE-0x` id is the join key between a **program spike** (here) and the **domain stories** it gates. Read **global → domain** to plan decisions, or **domain → global** to implement.

**👔 Product Owner:**

1. **Phase 0 — Program Spikes table** — what each spike blocks and its status. Nothing dependent starts until the spike's decision is recorded.
2. **Spike Detail** (per bucket) — the brief, the **Decision to make**, the **intended steps**, and the resolver table (blast radius).
3. **Sequencing** — `SPARK-SPIKE-01/02/03` are critical path (Sprint 0); `04/05/06a/06b` run in parallel. Assign an owner + timebox each.
4. In a **domain page**, the *Spikes & Complex Cases* map lists which of that domain's stories are 🔴🔬-blocked — plan the domain around them.

**🔧 Engineer:**

1. In the **domain A–G table**, find your story. If it's **🔴🔬 with `SPARK-SPIKE-0x` in Depends On**, the complex part is blocked until that spike concludes — check its status first.
2. **Follow the `SPARK-SPIKE-0x` id → Spike Detail**: the **intended cross-domain steps** (your target flow) + the resolver table (external services you'll call + what each resolver does today = your parity target).
3. **Research so far** — the **Phase 0 — Program Spikes** table links each spike to its `complexStories/<case>/` brief.
4. **Non-gated stories** (no 🔴🔬) — build straight from the story's Acceptance Criteria; no spike needed.
5. **In Jira/CSV** — the spike is a `Spike` issue (`SPARK-SPIKE-0x`) with the brief + steps in its description; your gated story lists it in **Depends On**.

> **One-line model —** *Product Owner:* "which decisions block work, who owns them, when?" → the spike table. *Engineer:* "is my story blocked, and once unblocked what's the flow + who do I call?" → follow the id to Spike Detail.

---

## 🔬 Phase 0 — Program Spikes (cross-domain research buckets)

> **Why this table lives here and not in the domain pages.** The same handful of hard problems recur across many domains under different operation names (e.g. every domain's multi-step `update*` write hits the *same* "no rollback" question). Rather than repeat a decision list on every domain page, each recurring problem is **generalized into one program spike bucket** below. A spike is **time-boxed research that produces a recorded decision** — not shipped code — and every domain story gated on one is marked **🔴🔬 in its domain page** with the spike id in `Depends On`.

> 🔬 **A spike is only for a genuinely complex problem that needs a solve/migrate approach.** Simple, intuitive, one-off decisions (delete-vs-`@deprecate` drift ops, dead service-method audits, auth-token parity, sort pushdown, DTO request-shape) are **not** spikes — they are resolved inline in the owning story's acceptance criteria and no longer appear anywhere as a decision table.

| Spike ID | Bucket / Generic Problem | Domains affected (home story) | Blocks | Research so far | Status |
|---|---|---|---|---|---|
| `SPARK-SPIKE-01` | 🔬 **Non-Atomic Write Saga** — a mutation fans out across ≥2 REST services (workspace-assoc · body · permissions · component-status) with no transaction; on partial failure state is left inconsistent. Choose the failure strategy: (a) compensating saga · (b) compensation-log + best-effort · (c) best-effort. | bom `E01` · claims `E01` · measurement `E01` · packaging `E01` · productDetails `E01` · watchlist `E01` · product `E02` | all `E`-phase writes | [`complexStories/non-atomic-write-saga`](https://github.com/XXX/tree/main/output/complexStories/non-atomic-write-saga) (shared `WriteSaga`) | 🔴 Open — failure strategy to decide |
| `SPARK-SPIKE-02` | 🔬 **TechPack Aggregate** — build a `ProductTechPack` entity where **every field is computed from a different microservice REST API**; pick the assembly pattern (A `extend type` · B elastic DGS · C orchestrator · D interface · E materialized). | product `E03/E04` | product techpack | [`complexStories/techpack`](https://github.com/XXX/tree/main/output/complexStories/techpack) | 🔴 Open — assembly pattern to decide |
| `SPARK-SPIKE-03` | 🔬 **Partner Drop/Undrop + Ownership** — orchestrated drop/undrop of a business partner across every referencing child domain; decide ownership (domain subgraph vs workspace) and the write saga. | product `E01` · workspace `E01` | partner-write `E`/`F` | [`complexStories/partner-drop-undrop-write`](https://github.com/XXX/tree/main/output/complexStories/partner-drop-undrop-write) | 🔴 Open — ownership + orchestration to decide |
| `SPARK-SPIKE-04` | 🔬 **Not-Removable / Undroppable Partners** — read aggregation computing which partners cannot be removed/dropped because still referenced (cross-domain `@requires` union). | product `E01` · workspace `E01` | partner-read fields | [`complexStories/notRemovable-undroppable-partners`](https://github.com/XXX/tree/main/output/complexStories/notRemovable-undroppable-partners) | 🔴 Open — contribution contract to agree |
| `SPARK-SPIKE-05` | 🔬 **Polymorphic Type Resolution** — interfaces/unions resolved by a category dispatcher; confirm the full `code → type` table + union membership, then `@DgsTypeResolver` + per-variant + CI schema-conformance. | bom `A04` | type-resolver + variant fields | [`complexStories/polymorphic-type-resolution`](https://github.com/XXX/tree/main/output/complexStories/polymorphic-type-resolution) | 🔴 Open — code→type table to confirm |
| `SPARK-SPIKE-06a` | 🔬 **Hydration** — how a domain *reads* another's entity (federated `@key` ref vs REST client); two-stage hydration; federation/read-hub rollout ordering across sibling DGS. | product `S02` (gates `C01`) · bom `B05` | hydration + rollout (reads) | [`complexStories/cross-domain-association`](https://github.com/XXX/tree/main/output/complexStories/cross-domain-association) | 🔴 Open — per-edge rule to decide |
| `SPARK-SPIKE-06b` | 🔬 **Cross-Domain Association** — one pattern for a mutation that also *links* its record into a sibling domain (workspace/attachment/team/partner), incl. sync-vs-async and partial-failure handling. | product `S01` (gates `D01`/`D02`/`D03`/`D04`/`D06`/`D07`/`D11`) | association-side writes | [`complexStories/cross-domain-association`](https://github.com/XXX/tree/main/output/complexStories/cross-domain-association) | 🔴 Open — pattern to choose |

> **Sequencing:** `SPARK-SPIKE-01/02/03` are on the critical path (they block `E`-phase writes and TechPack); run them in Sprint 0 alongside each domain's `B01` module scaffold. `04/05/06a/06b` block specific reads/writes and can run in parallel. Each spike concludes with the decision recorded back into the affected domain stories.
>
> **Note on `06a`/`06b`:** these were originally tracked as one `SPARK-SPIKE-06` id. They're split here because they answer different questions — 06a is "how do I *read* another domain's data," 06b is "how does my *write* also link into another domain" — and a story should only cite the one it actually needs.

### Non-spike complex cases (read pattern applied at cutover — no research decision needed)

> These recur across domains too, but the shape of the fix is already known (per-domain contribution + fan-out merge) — there's nothing to research, just build. They still get one `complexStories/` brief each so the pattern is documented once instead of per-domain.

| Bucket | Generic Problem | Domains affected (home story) | Research so far |
|---|---|---|---|
| `attachmentsWithMetaData` enrichment | 📎 **One attachments tab, three sources** — files, discussion files, and sample files must merge into one ordered, ACL-filtered feed without a Relationship-Service walk. | product `G01/G03` · workspace `G01/G03` (later phase) | [`complexStories/attachments-enrichment`](https://github.com/XXX/tree/main/output/complexStories/attachments-enrichment) |
| `components` + `counts` rollups | 🧮 **Five domains, one dashboard number** — a product's component list and a workspace's counts strip both roll up parallel per-domain fan-outs plus a batched ACL call into a single screen's worth of data. | product `G02` · workspace `G02/G04` (later phase) | [`complexStories/components-and-counts-rollups`](https://github.com/XXX/tree/main/output/complexStories/components-and-counts-rollups) |

---

## T-Shirt Size Classification

| T-Shirt | Story count | Effort (high est., eng-days) | Rule | Typical scope |
|---|---|---|---|---|
| 🔴 **XXL** | ≥ 60 | ≥ 200 | stories ≥ 60 OR effort_hi ≥ 200 | Very large, cross-domain initiative |
| 🔴 **XL** | 35–59 | 100–199 | stories ≥ 35 OR effort_hi ≥ 100 | Large feature or domain |
| 🟠 **L** | 25–34 | 60–99 | stories ≥ 25 OR effort_hi ≥ 60 | Medium-large project |
| 🟡 **M** | 15–24 | 40–59 | stories ≥ 15 OR effort_hi ≥ 40 | Medium-sized project |
| 🟢 **S** | 8–14 | 20–39 | stories ≥ 8 OR effort_hi ≥ 20 | Small project |
| 🟢 **XS** | < 8 | < 20 | otherwise | Minor enhancement or maintenance |

---

## Domain Index

> Each domain's full story detail is in its own breakdown page (named in the last column).

| # | Domain | Target DGS | T-Shirt | Stories | 🔴 VH | 🟠 High | 🟡 Med | 🟢 Low | Breakdown page |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Bill of Materials (BOM)** | `plm-product (co-located)` | **XL** | **36** | 1 | 2 | 12 | 21 | `FederatedGqlBrakDown-bom` |
| 2 | **Claims** | `spark-claims (separate)` | **L** | **20** | 0 | 2 | 9 | 9 | `FederatedGqlBrakDown-claims` |
| 3 | **Impression** | `plm-product (co-located)` | **XS** | **7** | 0 | 0 | 2 | 5 | `FederatedGqlBrakDown-impression` |
| 4 | **Measurement** | `plm-product (co-located)` | **M** | **20** | 0 | 1 | 6 | 13 | `FederatedGqlBrakDown-measurement` |
| 5 | **Packaging** | `plm-product (co-located)` | **L** | **24** | 0 | 2 | 9 | 13 | `FederatedGqlBrakDown-packaging` |
| 6 | **Product** | `plm-product (host)` | **XXL** | **67** | 5 | 4 | 25 | 33 | `FederatedGqlBrakDown-product` |
| 7 | **Product Details** | `plm-product (co-located)` | **M** | **13** | 0 | 1 | 7 | 5 | `FederatedGqlBrakDown-productDetails` |
| 8 | **Watchlist** | `plm-product (co-located)` | **M** | **13** | 0 | 1 | 6 | 6 | `FederatedGqlBrakDown-watchlist` |
| | **TOTAL** | — | — | **200** | **6** | **13** | **76** | **105** | — |

---

## 🔬 Spike Detail — the brief + the resolvers each spike touches

> For each spike: what it means, the decision to make, and the exact queries/mutations/field-resolvers it covers — with the **external services each one calls today** and a **one-line summary of its current logic**, so an engineer knows what to look at before starting.

### 🔬 `SPARK-SPIKE-01` · Non-Atomic Write Saga

- Some “save” buttons actually fire two or three separate backend calls in a row (e.g. first update which workspaces a record belongs to, then save the record body, then save its permissions).
- There is no database transaction across them, so if call 2 or 3 fails, call 1 is already committed and nothing undoes it — the record is left half-saved.
- This spike picks one consistent way to detect and recover from that partial failure for every write of this shape.

**Decision to make:** Pick (a) compensating saga, (b) compensation-log + best-effort, or (c) best-effort — and write down how to undo each step.

**Intended cross-domain steps:**

1. Open a **write-saga** and record each step so it can be undone
2. PUT **workspace-association** first (compensatable — remembers add/remove to reverse)
3. PUT the **record body** (typed validation exception on error)
4. PUT **permissions/partners** only if the input carries them
5. On any step failure → run the chosen strategy: compensate (saga) or log + best-effort

| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |
|---|---|---|---|---|
| 🔴🔬 `SPARK-BOM-E01` `updateBom` — 3-step orchestrated write | bom | Mutation | `workspaceV2` | editing a bom today is really three separate backend calls made one - after another, with no undo button: (1) if the caller changed which workspaces the bom belongs… |
| 🔴🔬 `SPARK-CLM-E01` `updateClaim` (proxy ACL + multi-step write) | claims | Mutation | `workspaceV2` | getUserPermissionsJWTByProxy({id:humanId, proxyIds:[parentId], basePermissions:true}) (proxy/external ACL path — context only); 2) if workspaceContext.{add,remove}… |
| 🔴🔬 `SPARK-MEAS-E01` `updateMeasurement` — 2-step orchestrated write | measurement | Mutation | `workspaceV2` | workspaceAssociations = sparkMeasurement.updateWorkspaceAssociations \|\| {}. token for [humanId]. 2. If add/remove workspaces → workspaceAssociationHelper(MEASUREMENT… |
| 🔴🔬 `SPARK-PKG-E01` `updatePackaging` (multi-step write) | packaging | Mutation | `attachment`, `relationship` | token; set humanId=packagingId; PUT packaging/v1 (body); 2) if attachmentsToRemove → (attachment) archiveAttachmentBulkV2 + (relationship) removeRelationship; 3) if… |
| 🔴🔬 `SPARK-PROD-E02` `updateComponentStatuses` (5-loader fan-out) | product | Mutation | `claim` | updating component statuses fans out to 5 places in parallel (bom, - measurement, productDetail, packaging — all internal — plus claim, external). - The bug: a loop… |
| 🔴🔬 `SPARK-PDTL-E01` `updateProductDetailsSet` (multi-step write) | productDetails | Mutation | `attachment`, `workspaceV2` | if workspaceContext.{add,remove}Workspaces non-empty → workspaceAssociationHelper(PRODUCT_DETAIL, id, add, remove) (throws on error); 2) null workspaceContext; 3) if… |
| 🔴🔬 `SPARK-WL-E01` `updateWatchlistEntries` (multi-step write) | watchlist | Mutation | `attachment`, `userGroup` | per-entry (currently NOT awaited — bug): getUserGroups([humanId]); if existing participants → updateUserGroup, else (user-group) addUserGroup (throw on error); 2)… |


---

### 🔬 `SPARK-SPIKE-02` · TechPack Aggregate

- A “TechPack” is one screen that shows counts and lists pulled from ~8 different backend services (attachments, discussions, samples, claims, BOMs, measurements, constructions, watchlists).
- Today a single gateway helper calls all of them and adds up the numbers.
- This spike decides how to assemble that one entity under federation so each service owns and contributes its own slice.

**Decision to make:** Confirm the assembly pattern (chosen: Option A, `extend type ProductTechPack`) and each domain’s contribution.

**Intended cross-domain steps:**

1. Gateway resolves the `ProductTechPack` **`@key`** (product id → shell entity)
2. Fans out **in parallel** to each contributing subgraph (attachments · discussions · samples · claims · BOMs · measurements · constructions · watchlists)
3. Each subgraph returns **only its own slice** (its count/list) — it owns that field
4. Gateway **stitches** the slices into one `ProductTechPack` response

| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |
|---|---|---|---|---|
| 🔴🔬 `SPARK-PROD-E03` `getProductTechPackCountV1` stub + aggregation facade (Option D Phase 1) | product | Query | `attachment`, `search` | the TechPack panel shows badge counts (attachments, discussions, - samples, boms, claims, etc.) for a product. - Getting those counts today means walking the entire… |
| 🔴🔬 `SPARK-PROD-E04` `getProductTechPackBulkCountV1` (bulk wrapper, ordering fix) | product | Query | `attachment`, `search` | the bulk version runs all N single-product lookups concurrently and - returns them in whatever order they happen to finish — not the order the caller asked for. - If a… |


---

### 🔬 `SPARK-SPIKE-03` · Partner Drop/Undrop + Ownership

- When a business partner is dropped or undropped from a product or workspace, every child domain that references that partner has to be updated too.
- This spike decides who orchestrates that fan-out write and how it recovers if one of the child updates fails midway.

**Decision to make:** Decide ownership (domain subgraph vs workspace) and the write-saga/rollback for the drop/undrop fan-out.

**Intended cross-domain steps:**

1. Owner (product/workspace) receives the **drop/undrop** request and starts the orchestration
2. **Fans out** the write to every child domain that references the partner
3. Each child applies its change with **per-target failure isolation** (one failure is visible, doesn't swallow the rest)
4. On partial failure → compensate/log per the SPIKE-01 saga

| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |
|---|---|---|---|---|
| 🔴🔬 `SPARK-PROD-E01` `productBusinessPartnerActions` (REMOVE/DROP/UNDROP) | product | Mutation | `sampleV2`, `recentlyViewed`, `todo`, `favorite` | removing, dropping, or un-dropping a business partner from a product - isn't one write — it's a ~220-line dispatcher that updates the partner's status and then fans… |


---

### 🔬 `SPARK-SPIKE-04` · Not-Removable / Undroppable Partners

- The UI needs to know which partners can’t be removed yet because something still references them.
- Answering that means asking several domains “do you still use this partner?” and combining the answers.
- This spike designs that cross-domain read.

**Decision to make:** Agree the `@requires` contribution each domain exposes and where the union is computed.

**Intended cross-domain steps:**

1. Owner exposes the public field (`notRemovablePartnerIds` / `unDroppablePartners`)
2. Each contributing domain declares its refs as **`@external`**; owner **`@requires`** them
3. Gateway fetches every domain's contribution and **batches** them
4. Owner resolver **unions + dedupes** into the final answer

| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |
|---|---|---|---|---|
| 🔴🔬 `SPARK-PROD-G07` `Product.vendorAttributes` + `businessPartners` + `droppedPartners` + `unDroppablePartners` + `status` | product | Field resolver | `vmm` | business-partner ids sometimes arrive as strings that need to be - parsed to ints before VMM will accept them (vmmUtils's int-parse normalization) — an easy detail to… |


---

### 🔬 `SPARK-SPIKE-05` · Polymorphic Type Resolution

- Some GraphQL types are interfaces or unions — one field can return one of several concrete shapes, chosen by a category code.
- This spike confirms the full code→type mapping and how the resolver dispatches each row to the right variant.

**Decision to make:** Confirm the `code → type` table + union membership, then wire `@DgsTypeResolver` + CI conformance.

**Intended cross-domain steps:**

1. Read the row's **category code** (or union discriminator)
2. `@DgsTypeResolver` maps code → **concrete type** (unknown → base type)
3. Resolve the **per-variant** field set for that concrete type
4. CI **schema-conformance** check fails the build if a variant misses an interface field

| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |
|---|---|---|---|---|
| 🔴🔬 `SPARK-BOM-A04` `@DgsTypeResolver` for the 2 BOM interfaces | bom | Field resolver | — (internal only) | - Material: switch on material.materialCategory.code → 4→Trim, 6→Wash, 2→Fabric, 15→Combination, 16→FabricSpec, {10,11,12,13,14,17–24}→Packaging, default… |


---

### 🔬 `SPARK-SPIKE-06a` · Hydration

- One domain often needs to **read** another domain’s object (e.g. a `product` on a `bom`).
- This spike decides whether to stitch it as a federated `@key` reference or call the other service directly, plus the order the services must ship so nothing launches half-wired.

**Decision to make:** Choose federated `@key` reference vs REST client per edge, and the cross-DGS rollout order.

**Intended cross-domain steps:**

1. Decide the edge shape: **federated `@key` reference** vs a direct **REST client** call
2. If `@key`: emit the key and let the **owning subgraph** hydrate it (gateway hop)
3. If REST: call the other service **in-process/directly** and map the result
4. Sequence the **rollout order** so no consumer launches before its provider is federated

| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |
|---|---|---|---|---|
| 🔴🔬 `SPARK-BOM-B05` `getBomMaterialTypes` (merge with Material Hub) | bom | Query | `materialHub` | load bom material types (GET …/master_data/bom_material_types[?ids]) and materialHub.getHubMaterialTypes (today sequential), concat; map each hub type → {code:9… |
| 🔴🔬 `SPARK-PROD-C01` `getProducts(...)` two-stage hydration | product | Query | `search` | listing products needs data from two places — the search index (which - knows flags like "has boms", "has claims", workspace membership) and the canonical product… |


---

### 🔬 `SPARK-SPIKE-06b` · Cross-Domain Association

- A mutation on one domain’s record often also has to **link** that record into a sibling domain — attach files, put it in a workspace, add teams, add partners.
- This spike decides the **one pattern** every such mutation should follow (sync direct call / event-driven / shared `AssociationService`), instead of each mutation inventing its own "write, then also link" logic.
- Unlike `06a`, there is no read-hydration or federated-reference question here — this is purely about how a *write* fans out to a sibling domain.

**Decision to make:** Pick the association pattern (see `SPARK-PROD-S01`’s three candidates) and how a mid-flight association failure is handled.

**Intended cross-domain steps:**

1. Primary mutation writes its own record (product create/update/bulk-update)
2. If the input carries a cross-domain link (`workspaceId`, `copyProduct`, template attachments, teams, partners) → build the association per the **chosen S01 pattern** (sync call / event / shared service)
3. Apply the link to the target domain (workspace, attachment, team, partner)
4. Record what happens if the link step fails after the primary write succeeded (today: mostly silent/undocumented)

| Resolver (home story) | Domain | Kind | Calls (external services) | What it does today (minimal) |
|---|---|---|---|---|
| 🔴🔬 `SPARK-PROD-D01` `addProduct` | product | Mutation | `workspaceV2`, `attachment` | POST ${v1} + optional copyProductToProduct(copyProduct) + workspace association |
| 🔴🔬 `SPARK-PROD-D02` `addProducts` (bulk) | product | Mutation | `attachment` | bulk POST ${v1}/bulk + attachment-link side-effects (no rollback — preserve, flag) |
| 🔴🔬 `SPARK-PROD-D03` `bulkUpdateProducts` | product | Mutation | — (internal only) | PUT ${v1}/mass_update |
| 🔴🔬 `SPARK-PROD-D04` `updateProduct` | product | Mutation | `attachment` | PUT ${v1}/{id} + optional copy + archive removed-template attachments (template branch) |
| 🔴🔬 `SPARK-PROD-D06` `addTeamsToProduct` 🔀 Collab Canvas | product | Mutation | — (internal only) | POST ${v1}/{productId}/resources/bulk + manage_workspace_teams |
| 🔴🔬 `SPARK-PROD-D07` `addBusinessPartnersToProductWithType` 🔀 Collab Canvas | product | Mutation | — (internal only) | POST ${v1}/{productId}/partners-add/bulk |
| 🔴🔬 `SPARK-PROD-D11` `updateWorkspaceAttributes` 🔀 Collab Canvas | product | Mutation | — (internal only) | PUT ${v1}/{productId} workspace attrs |
