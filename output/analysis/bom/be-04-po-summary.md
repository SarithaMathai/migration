# Phase 4: PO Sprint Planning Summary — BOM

> **Domain:** `bom` · **Target DGS:** `plm-product` (co-located) · **Generated:** 2026-06-26
> **Stories:** [be-04-stories.md](./be-04-stories.md)
> Day-ranges below are **AI-estimated — confirm in refinement.** Stories themselves carry complexity only.

---

## What Are We Building?

- We are moving the **Bill of Materials (BOM)** domain off the shared Node.js `spark-internal-graphql` gateway and into the **`plm-product`** Netflix DGS service, where it lives next to Product, Measurement, Impression and Packaging.
- BOM is the structured record of every material, supplier and impression that makes up a product, and it is referenced by many sibling domains.

- BOM is **mid-sized**: 13 queries, 6 mutations, and ~46 field resolvers across 18 type blocks, on a 735-line resolver.
- Its defining challenge is **material polymorphism** — 7 concrete material types (Trim, Wash, Fabric, FabricSpec, Combination, Packaging, plus the base) resolved by a category dispatcher, and 5 impression sub-types.
- The single hardest piece of work is `updateBom`, a 3-step write (workspace → body → permissions) that today has no rollback.

- The schema is **wide but shallow**: the large majority of attributes are direct pass-throughs (cheap to migrate).
- Risk concentrates in ~38 cross-domain field resolvers (material-library and color lookups) and the 2 polymorphic interfaces.
- See [be-05-attribute-inventory.md](./be-05-attribute-inventory.md).

**Note on ACL:** the current gateway uses ACL to obtain a per-resource capability token. Per decision,
Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites — where a resolver hands its token to a *different* domain's loader — use **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before the downstream call.

---

## Deployment model — ship on green, per story

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

## Migration Scope

| Surface | Count | Notes |
|---------|-------|-------|
| Queries | 12 | 4 are cacheable master-data lookups. `getBomDataV2` removed (`Bom_Unified` deprecated) |
| Mutations | 6 | 5 simple + `updateBom` (complex) |
| Field-resolver type blocks | 17 | one story each. `BomMaterial_Unified` removed; impression branch (`G-10`) rescoped, not removed |
| Material polymorphism | 7 types + interface + type resolver | B-01 |
| Impression polymorphism | 5 types + interface | B-01 |
| External dependencies | 12 loader keys (2 🔴 · 6 🟡 · 4 🔵) | sibling DGS + VMM platform |
| Federation contributions | 2 (Product extension, ResourcesCount.bomsCount) | BLOCKED-BY product |
| **Total stories** | **37** | green-field build stories. The 3 Phase-0 spike stubs are tracked as **program spikes** in the global breakdown and Jira, not as rows here (see global Phase 0) |

## Story Summary by Phase (AI-estimated)

| Phase | Name | Stories | Effort (est., +20% buffer) | Ready when |
|-------|------|---------|----------------------------|-----------|
| A | BOM material `@DgsTypeResolver` + CI conformance gate | 2 | 3–5d | |
| B | Core Reads | 7 | 7–12d | after B-01. (`B-02` removed) |
| C | Search & Listing | 5 | 9–15d | after B-01 |
| D | Mutations (simple) | 5 | 5–10d | after B-01 |
| E | Complex (`updateBom`) | 1 | 6–10d | after B-01, D-02 · gated on `SPIKE-01` + `PRODUCT-BE-E-00` |
| F | Federation Contributions | 2 | 4–7d | BLOCKED-BY product |
| G | Field Resolvers & Tests | 15 | 32–52d | after B-01. (`G-02` removed, `G-10` rescoped) |
| **Total** | | **37** | **69–115d** (buffered) | |

> One engineer ≈ **14–23 sprints** (5d). Phases B/C/D/G parallelize heavily after B-01.

> **Phase A is two stories** — `BOM-BE-A-04` (material/impression `@DgsTypeResolver`) and `BOM-BE-A-05` (shared CI conformance gate, depends on A-04). All *other* former Phase-A scaffolding (schema skeleton, service wiring, external stubs) is folded into the **B-01** checklist, done in the same PR.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories; the BOM material `@DgsTypeResolver` remains a dedicated story.

> **Thin DGS wrappers — parallel after B-01.** The model, REST controller (GET/POST/PUT) and service already exist; each story only adds the Netflix-DGS layer so the federated graph can stitch this subgraph. The **one-time DGS module scaffold** B-01 lands (schema file + scalar registration + service/Feign wiring) is a prerequisite for every operation story, so it is **assumed — not repeated in each story's `Depends On`** (rows list only genuine story-to-story dependencies). After B-01, phases B/C/D/G run fully in parallel.

## Key Risk Areas (plain English)

| Risk | Severity | What the PO needs to know |
|------|----------|---------------------------|
| `updateBom` 3-step write can leave data half-updated | 🔴 High | `S-01` (Phase 0 spike) picks the recovery strategy before `E-01` starts |
| Material field resolvers depend on 5 sibling domains | 🟡 Medium | `S-02` (Phase 0 spike) sets the rollout order; BOM can ship reads/writes meanwhile with partial enrichment |
| 7-variant polymorphism is easy to break when fields are added | 🟡 Medium | A shared CI conformance gate (`A-05`) guards this |
| Trim size logic is intricate (15 cases × 2) | 🟡 Medium | One larger story (G-08) with a parity table |
| Federation contributions wait on the product domain | 🟡 Low | F-01/F-02 are post-launch; not on the critical path |

## Decisions Required from Product Owner

> Reviewed and updated. Open items that need real research are now **Phase 0 spike stories** (estimable,
> assignable, trackable) rather than a flat decision list — see *Phase 0 — Spikes* in
> [`be-04-stories.md`](./be-04-stories.md) for the full write-up of each. The rest were resolved directly.

| # | Decision | Status | Detail |
|---|----------|--------|--------|
| 1 | `updateBom` failure strategy: saga / compensation log / best-effort | 🔬 **Spike** `BOM-BE-S-01` | Blocks `E-01`. Prior art: `complexStories/non-atomic-write-saga/`. |
| 2 | `updateBomComponentStatus` has no auth token — is the backend enforcing it? | ✅ Resolved — removed | Reviewer: not worth blocking on; dropped from `D-05`. |
| 3 | Keep `Bom_Unified` as a type or replace with field selection on `Bom`? | ✅ Resolved — deprecate `Bom_Unified` | `B-02`/`G-02` deleted; `G-01` rescoped to `Bom` only; `G-10` kept but rescoped to its shared impression-resolution logic (still needed by `G-11`/`G-12`/`G-13`). |
| 4 | Are the 3 unused service methods called by other domains? Confirm before delete | ✅ Resolved — removed | Reviewer: not a live concern; row dropped. |
| 5 | Federation rollout order for hub/trim/wash/fabric/combination | 🔬 **Spike** `BOM-BE-S-02` | Blocks `B-01`/`G`. |
| 6 | `getBomByParentId` — push sort to backend? | ✅ Resolved — yes | `B-04` updated: backend now sorts; client-side `sortedByDescending` shim removed. |
| 7 | `searchMaterialsBom` — keep query-string flatten or structured DTO? | 🔬 **Spike** `BOM-BE-S-03` | Blocks `C-02`. |
| 8 | `Bom.product` — does `parentId` only start with `PID`? | ✅ Resolved — yes | `G-01` updated: no longer an open question, kept as a defensive guard only. |

## Dependency Map

```
plm-product (BOM subgraph) depends on:
 spark-product backend REST .../bom/v1 + /masterData ; elastic bom/material search
 sibling DGS (federation): material-hub, trim, wash, fabric, combination, workspace, tag, user-profile
 Hive Gateway → VMM platform (business partners, supplier roles, facility location)
 cross-domain blockers:
   E-01 (updateBom) depends on PRODUCT-BE-E-00 (WriteSaga shared module)
 product domain F-01 Product entity extension ; F-02 TechPack ResourcesCount.bomsCount
```

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|--------|---------|-------|
| 0 | Program spikes | run in Sprint 0 (see global Phase 0 — Program Spikes) so E-01/rollout-order aren't waiting |
| 1 | A-04 (TypeResolver), A-05 (CI gate), B-01 (DGS module init + service wiring + first resolver) | schema, stubs, type resolvers, service port, drift guard |
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

## Capacity Planning

| Team size | Calendar (5d sprints) | Notes |
|-----------|----------------------|-------|
| 1 engineer | ~15–25 sprints | sequential |
| 2 engineers | ~9–15 sprints | B/C/D + most of G parallel |
| 3 engineers | ~6–10 sprints | critical path A → E-01 → G-08/G-10 → G-15 |

> Phase G (field resolvers) dominates the calendar; G-08 (trim) and G-10 (impression branch) are the two
> biggest field-resolver stories.
