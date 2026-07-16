# ADR-017 (draft) — Polymorphic type resolution (`SPIKE-05`)

> **Status:** 🔴 Proposed — draft for review
> **Spike:** `SPIKE-05` · **Home stubs:** `BOM-BE-A-04` + material FRs `BOM-BE-G-08` ·
> `SAMPLE-BE-A-04`/`SAMPLE-BE-G-02` (later phase) · `SEARCH-BE-B-01`/`SEARCH-BE-C-02` (later phase)
> **Scope:** how every `__resolveType` / prefix-gated dispatch is ported and **kept from drifting** —
> the dispatch tables, the per-variant field resolvers around them, and the conformance guard.
> **⚠ Map authority:** the legacy resolver source is the authority for every table below — these were
> read from the code, not from drafted pseudo-code.
> **Related:** ADR-014 pin-down 6 (`bom.type 2 → packagingBom` lands in this spike's `code → type`
> registry) · ADR-015/016 (federation end-states that consume the same entity keys).
> **Evidence:** `resolvers/product/SPARK_Bom.js` + `resolvers/SPARK_SampleV2.js` +
> `resolvers/SPARK_MaterialHub.js` + `resolvers/material/SPARK_BaseMaterialCommonFields.js` +
> `utils/materials/colorUtils.js` + `resolvers/SPARK_Search.js` at `https://github.com/XXX`.

---

## 1. Today's behavior — the five dispatch sites, table by table

### 1 · `SPARK_BomMaterialInterface.__resolveType` (bom, 7 impls)

- Discriminator: `material.materialCategory?.code || ''` against `MATERIAL_CATEGORY_ID`
  (`resolvers/product/SPARK_Bom.js` — 24 named codes, 18 cased):

| `materialCategory.code` | Concrete type |
|---|---|
| 4 TRIM | `SPARK_BomTrimMaterial` |
| 6 WASH | `SPARK_BomWashMaterial` |
| 2 FABRIC | `SPARK_BomFabricMaterial` |
| 15 COMBINATION | `SPARK_BomCombinationMaterial` |
| 16 FABRIC_SPEC | `SPARK_BomFabricSpecMaterial` |
| 10–14 packaging (paper/plastic/glass/metal/unspecified) · 17 acrylic · 18 rubber · 19 wood · 20 ceramic · 21 synthetic · 22 organic · 23 packaging-trim · 24 stick — **13 codes** | `SPARK_BomPackagingMaterial` |
| **default** — incl. 1 COMPONENT · 5 OTHER · **9 HUB** · missing/unknown | `SPARK_BomMaterial` |

- The risk named in the brief: the **HUB (9) fall-through is load-bearing** — hub-library materials render
  through the generic `SPARK_BomMaterial`, whose `libraryResource` resolves via
  `materialHub.getHubMaterial(JWT)`. Casing 9 "properly" would break them.
- Per-variant drift surface — each concrete type re-implements `libraryResource` against a different
  sibling: trim → `trim.getTrimBatch` (🟡) · wash → `wash.getWash(JWT)` (🟡) · fabric →
  `search.searchFabricSpecCombos` (🔴 search) · fabricSpec → `fabric.getSpecificationByID` (🟡) ·
  combination → `combination.getById` (🟡) · base → `materialHub.getHubMaterial(JWT)` (🟡) —
  plus per-variant `weight` / `countryOfOrigin` / trim-only `sizeValue`/`sizeCaption`/`facilityName`.
  🐞 fields added to one impl and not the others is exactly the "silent drift" the brief describes.

### 2 · `SPARK_BomImpressionDetailsInterface.__resolveType` (bom, 5 impls)

- Discriminator: `impression.type` against `IMPRESSION_TYPE`:

| `impression.type` | Concrete type |
|---|---|
| 603 TRIM | `SPARK_BomTrimLibraryImpressionDetails` |
| 605 TRIM_ZIPPER | `SPARK_BomTrimZipperLibraryImpressionDetails` |
| 604 WASH | `SPARK_BomWashLibraryImpressionDetails` |
| 602 FABRIC | `SPARK_BomFabricLibraryImpressionDetails` |
| **default** (601 BASE + unknown) | `SPARK_BomBaseImpressionDetails` |

- Internal/external branch rides along: `SPARK_BomImpressionDetails_Unified.libraryResource` picks
  `search.getMaterialByIds` for internal users vs a JWT-scoped path for external.

### 3 · `SPARK_SampleAsset` union (sample, `Color | Artwork`)

- Fed by `SampleV2.asset` — 🐞 which calls `SPARK_Material.Query.getMaterialByIdFromService(...)`
  **by importing the material resolver directly** (the ADR-011/012 anti-pattern again).
- Dispatch on `humanId` prefix: `isColorId(humanId)` (the **8 color-prefix family** — Colors, ColorColoro,
  ColorPantone, TargetColors, TargetColorColoro, TargetColorPantone, ReferenceColors, … per
  `utils/materials/colorUtils.js`) → `SPARK_Color`; `Artworks` prefix → `SPARK_Artwork`;
  🐞 **else `return null`** — an unmatched asset id makes the whole field error with GraphQL's generic
  "abstract type must resolve" failure.

### 4 · `SampleV2.parent*` — prefix-gated concrete parents (sample)

| Field | Gate on `sample.parentId` | Loader (owning domain) |
|---|---|---|
| `product` | `PID` prefix | `product.getByID` (plm-product) |
| `colorArchroma` | `ARCCLR` \| `TARARCCLR` \| `REFARCCLR` | `colorArchroma.getByID(JWT)` |
| `fabricSpecCombo` | `FSC` | `combination.getFabricSpecComboById(JWT)` |
| `fabricSpec` | `FAS` | `fabric.getSpecificationByID` |
| `trim` | 🐞 **no gate** — any non-empty `parentId` | `trim.getTrim(JWT)` (plm-trim) |

- 🐞 the `trim` hole means a product-parented sample that queries `trim` sends `PID-…` to the trim
  service — today it survives on the trim backend's 404 behavior, not on the resolver.

### 5 · Materials search results (search / material-hub)

- `searchMaterials` / `searchMaterialsV2` — `GET ${search}/materials/v1` — return mixed-type rows;
  two resolvers type them:
  - `SPARK_HubMaterialInterface.__resolveType` = `resolveMaterialType` — 🐞 **string-typed** dispatch:
    `material.type === 'Paper Based Substrate'` → `SPARK_Paper` · `'Wood'` → `SPARK_Wood` ·
    else `SPARK_UserDefinedMaterial` (a renamed display string silently reroutes every row to the default),
  - `SPARK_BaseMaterialCommonFields.__resolveType` — structural: `material.baseMaterial` present →
    `SPARK_BaseMaterial`, else `SPARK_BaseMaterialResource`.

### Out of scope (tracked, not decided here)

- Two further sites stay with their own domain stories, adopting whatever this ADR ratifies:
  discussion `Resource` union (`resolvers/SPARK_Discussion.js`) and product `SPARK_Categories`
  (12-case union, product `G-phase` story) — per the case brief's note.

### Interaction grid

| Dispatch site | Home subgraph | Discriminator | Impls | Default branch | Per-variant EXT calls | True cross-subgraph? |
|---|---|---|---|---|---|---|
| `BomMaterialInterface` | `plm-product` (co-located bom) | `materialCategory.code` (int) | 7 | ✅ load-bearing (1/5/**9**→`BomMaterial`) | trim 🟡 · wash 🟡 · fabric 🟡 · combination 🟡 · search 🔴 · materialHub 🟡 | resolution **local**; variant fields cross |
| `BomImpressionDetailsInterface` | `plm-product` | `impression.type` (int) | 5 | ✅ (601+unknown→Base) | search 🔴 (materials) | resolution local |
| `SampleAsset` union | `plm-sample` | id prefix | 2 | 🐞 `null` → field error | material/artwork loaders + 🐞 cross-resolver import | resolution local; **asset fetch crosses** |
| `SampleV2.parent*` | `plm-sample` | id prefix per field | 6 fields | n/a (per-field `null`) | product · trim · colorArchroma · combination · fabric | each gate targets a different subgraph |
| Materials search | `plm-elastic-search` rows, typed by material domain | `type` (string) + shape | 3 + 2 | ✅ (`UserDefinedMaterial`) | — | **yes at end-state** — stubs must resolve on owners |

> **Key findings:**
> - `__resolveType` itself is always **subgraph-local** — every dispatcher runs in the subgraph that
>   produced the row. No dispatch table needs federation to be ported.
> - The real cross-subgraph pressure is (a) the **per-variant field resolvers** calling five sibling
>   services, and (b) **polymorphic search results**, where the concrete fields belong to other subgraphs —
>   the only site where the federation-native stub pattern (`__typename` + `@key` id) applies.
> - The migration risk is therefore not architecture but **fidelity + drift**: five hand-maintained tables
>   in three domains, two load-bearing defaults, one `null` hole, one missing gate, one string-typed match.

---

## 2. Decision drivers

- Phase-1 goal is **behavioral parity** — a wrong dispatch renders the wrong fragment silently; nothing
  throws. Fixtures must pin every row of every table, including the defaults.
- The brief's named risk: getting the mapping **exactly** right, especially the HUB fall-through — the
  tables in §1 are read from the resolver source (the declared authority), and `BOM-BE-A-04` already
  encodes the same bom tables; this ADR must not contradict it.
- **Drift is the disease**: schema impls, dispatch tables, and per-variant resolvers are maintained by
  hand in 3 domains; today nothing fails when they diverge.
- DGS specifics: a `@DgsTypeResolver` must return a valid concrete type name — the `SampleAsset` `null`
  needs a conscious equivalent; Kotlin enums replace the resolver-local constant objects
  (`A-04` already moves `MATERIAL_CATEGORY_ID` to `BomConstants.kt`, fixing a circular import).
- Search's polymorphic lane lands **later phase** — the pattern must be decided now so `plm-sample` and
  `plm-elastic-search` inherit a playbook, not a per-team reinvention.
- Consistency: no cross-resolver imports survive (ADR-011/012/016 stance).

### Assumptions, constraints & success criteria

**Assumptions**
- The §1 tables, read from the resolver source, are correct pending one backend verification pass per
  domain (`A-04` AC-3) before fixtures freeze.
- The load-bearing defaults (HUB code 9 → `BomMaterial`, 601 → base impression) are intentional
  behavior, not bugs; the UI depends on them.
- Sample and search dispatch sites migrate in later phases and inherit this playbook unchanged.

**Constraints**
- A DGS `@DgsTypeResolver` must return a valid concrete type name — the legacy `null` return needs an
  explicit, decided equivalent (pin-down 3).
- Phase-1 parity: every dispatch outcome, including defaults and the un-gated `trim` call-through, must
  match the legacy resolver (deviations only via pin-downs 3/6).
- The conformance gate is a shared test library — it must not require new runtime infrastructure.

**Success criteria (measurable)**
- Golden-table fixtures exist for all five dispatch sites, seeded from §1 and backend-verified; every row
  (including defaults, unknown codes, the `null` path, a `PID`-parented trim query, an unrecognized hub
  `type` string) passes parity.
- The CI gate demonstrably fails on each drift direction: an SDL member with no enum row, an enum row
  with no SDL type, an undeclared default, and a mapping change without its fixture change in the same PR.
- Zero inline `when`/`if` dispatch ladders remain — every mapping is a constants-enum lookup.
- The two out-of-scope sites (discussion `Resource`, `SPARK_Categories`) have stories referencing the
  playbook, not bespoke designs.

---

## 3. Options

| | Option | Mapping lives | Drift guard | Parity | Verdict |
|---|---|---|---|---|---|
| A | Per-site ports | each `@DgsTypeResolver`, ad hoc | none — review only | exact | viable, keeps the disease |
| B | A + shared playbook + CI conformance gate | one constants enum per domain, one convention | schema↔table↔enum checked in CI | exact | **recommended** |
| C | Backend-supplied discriminator | data producers return `__typename` | producer contract | risky | rejected for phase 1 |
| D | Federation-native `Material` interface for search | `@key`-ed concrete types, stubs from search | composition check | n/a phase 1 | recorded end-state for the search lane only |

### A — Per-site ports (mirror every switch)

- Each domain writes its `@DgsTypeResolver` mirroring §1; per-variant field resolvers become service calls.
- ➕ smallest possible change · exactly what `BOM-BE-A-04` describes for bom.
- ➖ five tables in three repos with **no guard** — the next added impl or renamed type string drifts
  silently, which is the case's stated problem, unsolved.

### B — Option A + one playbook + CI conformance check ⭐

- **The playbook** (one page, referenced by every affected story):
  1. every dispatch table is a **domain constants enum** (`BomConstants.kt` pattern) — codes/prefixes/
     strings + target type name, one row per mapping, defaults explicit,
  2. the `@DgsTypeResolver` is a dumb lookup over that enum — no inline `when` ladders,
  3. prefix gates (`SampleV2.parent*`) use the same enum of `RESOURCE_TYPE_PREFIXES` — one source for
     `isColorId`-style families,
  4. per-variant field resolvers live one-file-per-concrete-type, named after it (drift is then visible
     in the file tree).
- **The CI conformance gate** (a shared test utility, run in each subgraph's build):
  - parse the subgraph SDL: every member of every interface/union **must** have ≥ 1 enum row targeting
    it, and every enum row's target **must** exist in the SDL (catches both add-and-forget directions),
  - the default branch must be declared explicitly in the enum (no implicit fall-through),
  - a **golden-table fixture** per site: `code/prefix → type` snapshot diffed on every build; changing a
    mapping requires changing the fixture in the same PR (mapping changes become reviewable events).
- ➕ ends silent drift by construction · one decision, five sites + the two out-of-scope ones reuse it ·
  zero runtime difference from A (parity untouched) · cheap — a test library, not infrastructure.
- ➖ the conformance test is one more shared artifact to own (home it with the schema-registry/CI stories) ·
  golden fixtures add PR friction on genuine mapping changes (that friction is the feature).

### C — Backend-supplied discriminator

- Each backend/index returns an explicit type tag; resolvers just trust it.
- ➕ one authority for typing.
- ➖ requires coordinated backend changes across product/sample/search for a parity phase · the hub
  materials case shows the failure mode already (`'Paper Based Substrate'` **is** a backend-supplied
  string, and it's the most fragile row in §1) · mapping bugs move somewhere the DGS can't test. Rejected.

### D — Federation-native polymorphic search (the search lane's end-state)

- `Material` as a federated interface with `@key`; `materialsSearch` returns **stubs**
  (`__typename` + id); concrete fields resolve on the owning subgraph via `_entities`.
- ➕ concrete types owned by their domains; search stops needing hydrated rows.
- ➖ needs the material-owning subgraphs live + gateway interface-entity support — a later-phase shape,
  and irrelevant to bom/sample (their variants are co-located; resolution is already local).
- **Recorded as the target** for `SEARCH-BE-C-02`/`B-01`; the enum + conformance gate from B carries over
  unchanged (the stub still needs the same `type → __typename` table on the search side).

---

## 4. Proposed decision (to ratify)

- **Option B** — port every dispatcher per-site (Option A runtime), with:
  - one constants-enum-per-domain as the single mapping source,
  - the shared **CI conformance gate** (SDL ↔ enum ↔ golden fixture) wired into each affected subgraph,
  - `SPIKE-05`'s **`code → type` registry** as the human-readable master table — §1 of this ADR
    seeds it, ADR-014's `type 2 → packagingBom` row included.
- **Option D recorded** as the search lane's end-state; no phase-1 work.
- The two out-of-scope sites (discussion `Resource`, `SPARK_Categories`) adopt the playbook in their own
  stories — no new decision.

### Pin-downs at ratification

| # | Item | Choice to make | Draft recommendation |
|---|---|---|---|
| 1 | Table fidelity | — | §1 tables (from resolver source) seed the registry; `A-04` AC-3's "verify values against backend" runs once per domain before fixtures freeze |
| 2 | HUB (9) / COMPONENT (1) / OTHER (5) fall-through | case them vs keep default | **keep the default branch exactly** — casing 9 breaks hub-material rendering; enum marks them `DEFAULT` explicitly |
| 3 | `SampleAsset` `null` return 🐞 | preserve generic error vs typed error | resolve to a typed `DgsException` with the offending prefix in the message — same observable failure (field errors), better diagnosis; accepted deviation |
| 4 | `SampleV2.trim` missing prefix gate 🐞 | preserve call-through vs add gate | **preserve** in phase 1 (parity — behavior currently defined by the trim backend's 404); log non-trim prefixes; add the gate as a documented post-parity fix |
| 5 | String-typed hub dispatch 🐞 | preserve strings vs backend code | preserve the exact strings in the enum (with source-of-string comment); pin both strings + default in the golden fixture |
| 6 | `SampleV2.asset` cross-resolver import 🐞 | — | replace with a material-service client call (ADR-011 stance); the union dispatch itself is unchanged |
| 7 | Conformance gate ownership | per-team copies vs shared library | one shared test library, versioned with the schema-registry tooling; each subgraph pins it in CI |
| 8 | Internal/external impression branch | fold into dispatch vs keep field-level | keep field-level (it selects a *data path*, not a *type*); document so nobody "simplifies" it into the type resolver |

---

## 5. Consequences

- If accepted:
  - `BOM-BE-A-04`/`G-08` proceed exactly as written, plus the enum + conformance wiring,
  - sample and search stories (later phase) inherit a playbook + a working gate, not a blank page,
  - every future "add an impl" PR fails CI until schema, enum, and golden fixture agree — silent drift
    becomes structurally impossible,
  - the `code → type` registry gives the PO/QA one page to validate against real data.
- Risks:
  - the golden fixtures are only as good as their seed — pin-down 1's backend verification must actually
    run, or the gate enshrines a wrong table,
  - fixture recording must include: a HUB (code 9) material · an unknown/missing category code · a
    non-color non-artwork `assetHumanId` (the `null` path) · a trim-field query on a `PID`-parented sample
    (pin-down 4's logged path) · a hub-material row with an unrecognized `type` string — or the defaults
    ship unverified,
  - the conformance library becoming a kitchen sink — keep it to the three checks in §3-B.

---

## 6. On acceptance

Per `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md`:

1. Copy this write-up to `adrs/`; add the `SPIKE-05` block to `adrs/adr-index.yaml`
   (`status: Accepted`, `chosen: "B — …"`, all options preserved).
2. Flip `00-overview.md` §2 to **Decided**; add `01-stories.md` + implementation notes
   (incl. the seeded `code → type` registry as its own artifact).
3. Replace the *"per `SPIKE-05`"* placeholders in the affected
   `output/analysis/{bom,product}/be-04-stories.md` stories (`A-04`, `G-08`); sample/search follow in
   their phases.
4. Regenerate domain + global docs; push to Jira/Confluence.
