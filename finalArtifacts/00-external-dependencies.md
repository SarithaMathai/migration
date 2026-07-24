# External & Cross-Domain Dependencies

> 🏷️ **Tags:** `dgs-migration` · `dependencies` — **Assembled:** 2026-07-24 from
> `output/analysis/program/cross-domain-dependencies.md`, `ext-dependency-stories.md`, the `EXT:` tags
> in every `output/analysis/*/be-04-stories.md`, and `fedMigrationScripts/reference/domain-service-catalog.md`.
> **Validated against the codebase**, not just docs: external-service tags come from the story sources;
> entity-resolver gaps were confirmed against the federated target schemas (`*/be-03-schema.graphql`).
>
> **Companion page:** *Migration Order & Sequencing* — how the build order honors these blockers.

---

## 1. What "external dependency" means here

Three distinct kinds — they gate work differently:

| Kind | What it is | Blocks development? | Blocks FE? |
|---|---|---|---|
| **A. Cross-domain (same subgraph)** | One phase-1 domain's story waits on another phase-1 domain's story (e.g. every `E-01` needs Product's `WriteSaga`) | Yes — build order must honor it | Indirectly (via the BE story) |
| **B. Cross-subgraph (later-phase domain)** | A story waits on a domain that isn't live yet (attachment, discussion, sample, construction) | **Yes — cannot ship until that subgraph exists** | Only the specific federated field |
| **C. Externally-owned service/entity** | A field resolves data owned by an external platform/team (VMM, IG, search, etc.) via gateway stitch or a `@DgsEntityFetcher` | Usually no (stub/loader exists) — but the **entity resolver may be missing** | Only if the field is missing entirely |

---

## 2. Cross-domain blockers (Kind A) — honored by build order

Every one of these is a phase-1-to-phase-1 dependency. The sequencing plan builds the producer first.

| Blocked story | Domain | Waits on | Why |
|---|---|---|---|
| `IMPRESSION-BE-F-01` — `Product.impressions` / `impressionCounts` | impression | `PRODUCT-BE-B-01` | reads a field Product exposes |
| `BOM-BE-E-01` — `updateBom` (3-step write) | bom | `PRODUCT-BE-E-00` | shared `WriteSaga` module |
| `CLAIM-BE-E-01` — `updateClaim` | claims | `PRODUCT-BE-E-00` | shared `WriteSaga` module |
| `MST-BE-E-01` — `updateMeasurement` | measurement | `PRODUCT-BE-E-00` | shared `WriteSaga` module |
| `PKG-BE-E-01` — `updatePackaging` | packaging | `PRODUCT-BE-E-00` | shared `WriteSaga` module |
| `PDTL-BE-E-01` — `updateProductDetailsSet` | productDetails | `PRODUCT-BE-E-00` | shared `WriteSaga` module |
| `WATCHLIST-BE-E-01` — `updateWatchlistEntries` | watchlist | `PRODUCT-BE-E-00` | shared `WriteSaga` module |
| `CLAIM-BE-H-02` — `ResourcesCount.claims` (TechPack) | claims | `PRODUCT-BE-E-03` (+ `F-14`) | TechPack facade + contract alignment |
| `CLAIM-BE-H-01` — `Product.claims` (federation) | claims | `PRODUCT-BE-F-14` | product-side stub + `Product` entity (plm-product Phase A) |

**The dominant blocker is `PRODUCT-BE-E-00` — the shared `WriteSaga` module — which gates 6 domains'
write stories.** This is the single most important thing to build early; it's why Product is first in
the backend queue. It lands ≈ **day 16** of Product's build, before any consumer's `E-01` is reached.

---

## 3. Cross-subgraph blockers (Kind B) — cannot ship until the domain is live

These wait on a domain that federates in a **later phase**. They are **excluded from the phase-1
critical path** and land post-launch when the owning subgraph exists.

| Blocked story | Domain | Waits on (not-yet-live subgraph) |
|---|---|---|
| `MST-BE-H-01` — contribute `sampleMeasurement` to `SampleV2` | measurement | **sample** |
| `MST-BE-H-02` — `SampleMeasurementSet.sample` forward ref (PO-gated) | measurement | **sample** |
| `PRODUCT-BE-H-01` — `ResourcesCount.productAttachments` + `discussionAttachments` | product | **attachment** (⛔ `plm-attachment` not live) |
| `PRODUCT-BE-H-02` — `ResourcesCount.discussions` | product | **discussion** |
| `PRODUCT-BE-H-03` — `ResourcesCount.sample` | product | **sample** |
| `PRODUCT-BE-H-04` — `ResourcesCount.claims` | product | **claim** |
| `PRODUCT-BE-H-05` — `ResourcesCount.constructions` | product | **construction** |

> **Do not let these gate the phase-1 flips.** They are `ResourcesCount`/forward-ref fields that
> resolve to a safe stub until the owning subgraph is live. Ship the domain, backfill these later.

---

## 4. Externally-owned services (Kind C) — the platform/team dependencies

Fields that resolve data owned by an **external platform or sibling service**, via gateway stitch
(🔵), a sibling DGS (🟡), or a business-critical call (🔴). Counted from the `EXT:` tags across all
`be-04-stories.md`. **Most do not block development** — a loader or `@extends` stub already exists —
but they define the external-team surface the migration touches.

| External service | # story refs | Severity | Owner (per domain-service-catalog) | Notes |
|---|---|---|---|---|
| `search` | 30 | 🔴 when business-critical | SearchService (elastic, sibling DGS) | list/search views; also gated by the search read-hub decision |
| `vmm` | 16 | 🔵 | VMM platform | business-partner lookups (`VmmBusinessPartner`) |
| `workspaceV2` | 15 | 🔵 | WorkspaceV2 | workspace context on most reads |
| `attachment` | 15 | 🔴 (writes) | Attachment (later-phase subgraph) | file attach/clone; write path is 🔴 |
| `userAttributes` | 12 | 🔵 | User platform | created/updated-by hydration |
| `tag` | 11 | 🔵 | Tag / NEXUS | size + tag lookups |
| `userGroup` | 6 | 🔵 | User-group platform | ACL / permissions |
| `materialHub` | 6 | 🟡 | MaterialHubService (sibling) | BOM material master data |
| `relationship` | 5 | 🟡 | Relationship service | entity associations |
| `ig` | 3 | 🔵 | Insights (IG) platform | **entity resolvers missing — see §5** |
| `ruleLibrary`, `sampleV2`, `rating`, `apex`, `corona`, `doppler`, `location`, `favorite`, `todo`, `recentlyViewed`, `relationship`, `fabric`/`trim`/`wash`/`combination` (BOM material siblings) | 1–3 each | mixed | various | mostly 🔵 read stitches |

**EXT dependency load by domain** (stories carrying an `EXT:` tag):

| Domain | product | bom | measurement | packaging | watchlist | productDetails | claims | impression |
|---|---|---|---|---|---|---|---|---|
| EXT stories | 30 | 30 | 12 | 11 | 11 | 9 | 8 | 1 |

> **Severity legend:** 🔵 gateway-stitched read (low risk — stub exists) · 🟡 sibling DGS (migrates
> alongside) · 🔴 business-critical read or a write path (verify carefully). See
> `fedMigrationScripts/reference/domain-service-catalog.md` for the full service→owner catalogue.

---

## 5. Entity-resolver gaps (Kind C, blocking) — the real external blockers

Most external references resolve via an existing stub. **Two** externally-owned entities have **no
covering resolver anywhere** — today they silently resolve to a bare `{id}` key stub, which means the
consuming FE story would render incomplete data. These were auto-identified by the field-by-field
drill-down (`output/clientStoryDependency/`) and confirmed against the federated schema
(`product/be-03-schema.graphql`, where they are `@extends`-stubbed).

| New BE story | External entity | Owner | Blocks FE | Fix |
|---|---|---|---|---|
| `PRODUCT-BE-H-07` — `IG_Clazz_Filter` entity fetcher | `IG_Clazz_Filter` | Insights (IG) | `PRODUCT-FE-006` | `@DgsEntityFetcher(name = "IG_Clazz_Filter")` → IG client behind a batched `DataLoader`, null-tolerant |
| `PRODUCT-BE-H-08` — `IG_Clazz` entity fetcher | `IG_Clazz` (`insightsClassExclusion`) | Insights (IG) | `PRODUCT-FE-007` | `@DgsEntityFetcher(name = "IG_Clazz")` → IG client behind a batched `DataLoader`, null-tolerant |

> **Priority:** medium. Each unblocks one Product FE story (`FE-006`, `FE-007`). Neither is on the
> program critical path, but both must exist before those two Product frontend stories can render the
> IG fields fully. Source: `output/analysis/program/ext-dependency-stories.md`.

---

## 6. What actually blocks the frontend

Pulling it together — the FE-blocking dependencies, in priority order:

1. **`PRODUCT-BE-E-00` (WriteSaga)** — indirectly gates every domain's write/saga FE story. Build first. *(Highest leverage.)*
2. **Each domain's own B + G (field-resolver) stories** — gate that domain's reads FE. In-domain, not external.
3. **`IG_Clazz` / `IG_Clazz_Filter` entity fetchers** (`PRODUCT-BE-H-07/08`) — gate `PRODUCT-FE-006/007`.
4. **Cross-subgraph `ResourcesCount` fields** (attachment/discussion/sample/claim/construction) — do **not** block the flip; resolve to stubs until those subgraphs are live.

**Not a blocker (verified 2026-07-24):** `IMPRESSION-FE-002` was previously listed as depending on 9
BOM stories — a copy-paste error from its sibling `IMPRESSION-FE-001`. The actual query
(`getCarryForwardFormData`) selects only `getProduct` + `searchImpressionsByProductId`, no BOM. Fixed
at source; `IMPRESSION-FE-002` now depends on Product + Impression only.

---
*External Dependencies · assembled 2026-07-24 · validated against be-04-stories.md, be-03-schema.graphql, ClientCallingGqlQueries/, and domain-service-catalog.md.*
