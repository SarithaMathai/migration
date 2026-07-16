# Complex Story — Polymorphic type resolution (`@DgsTypeResolver` + per-variant + prefix-gated parents)

> **Summary —** Same shape-shifting problem in three domains — a category code decides the real type, and today's dispatch tables drift silently. One `@DgsTypeResolver` playbook, enforced by CI, ends the drift.
> **Spike:** `SPIKE-05` · **Status:** 🟠 Draft ADR-017 proposed — ratification pending
> **⚠ Map authority:** the legacy resolver source is the authority for every dispatch table — do not port a dispatch map from drafted pseudo-code.
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** bom (`plm-product`), sample (`plm-sample`), search (`plm-elastic-search`)
> **Stub stories:** `BOM-BE-A-04` (type resolvers) + material FRs `BOM-BE-G-08`; `SAMPLE-BE-A-04`/`SAMPLE-BE-G-02` (later phase); `SEARCH-BE-B-01`/`SEARCH-BE-C-02` (later phase)

> **Migrates (source resolvers → this case):** bom **TR `BomMaterialInterface.__resolveType`** +
> **`BomImpressionDetailsInterface.__resolveType`** (`BOM-BE-A-04`, material FRs `BOM-BE-G-08`); sample
> **TR `SampleAsset` union** (`SAMPLE-BE-A-04` (later phase)) + **FR `SampleV2.parent*`** (`SAMPLE-BE-G-02` (later phase)); search
> **Q `materialsSearch`** polymorphic stubs (`SEARCH-BE-B-01`/`SEARCH-BE-C-02` (later phase)).
> **Note:** two further `__resolveType` sites (discussion `Resource` union — `resolvers/SPARK_Discussion.js`,
> product `SPARK_Categories` 12-case union — product `G-04`) are **tracked but not decided here**; they adopt
> whatever this spike ratifies in their own domain stories (see [ADR-017 §1 "Out of scope"](./01-adr-polymorphic-type-resolution.md)).

## 1. The problem (it recurs in three domains)

### 1.1 Problem statement

- Five GraphQL polymorphic points (interfaces, unions, prefix-gated fields) across three domains each need
  an exact type-resolution table ported to `@DgsTypeResolver` — and each table is hand-maintained today,
  with nothing failing when schema, dispatch table and per-variant resolvers diverge.
- The migration risk is **fidelity + drift**, not architecture: a wrong dispatch renders the wrong
  fragment silently.

### 1.2 Current state & root cause

| Polymorphic point | Domain | Shape |
|---|---|---|
| `BomMaterialInterface` | bom | **7 impls**, a **21-case dispatcher** keyed on `materialCategory.code` (default 1 COMPONENT, 5 OTHER, **9 HUB → `BomMaterial`** falls through) |
| `BomImpressionDetailsInterface` | bom | **5 impls**, internal/external branch |
| `SampleAsset` union | sample | `Color \| Artwork` via `SampleV2.asset`, by id prefix |
| `SampleV2.parent*` | sample | **prefix-gated** concrete parents (product/trim/colorArchroma/fabric/artwork/asset) |
| `materialsSearch` results | search | polymorphic `Material` results (stubbed entities, `__typename` + id) |

**Root cause:** each polymorphic point needs an exact `__resolveType` / type-resolver **and** per-variant
field resolvers, but the mappings live as hand-written switch/if ladders local to each resolver —
- there is no single mapping source, so tables **silently drift** as fields are added to one impl but not the others;
- some defaults are **load-bearing** (HUB code 9 must fall through to the generic type) and some are defects
  (a `null` return, a missing prefix gate, a display-string match) — none distinguishable without reading the code.
- Prior research shows the federation-native version: a `Material` interface with `@key`, polymorphic search returning stubs, fields resolved on the concrete type.

### 1.3 Impact if not addressed

- **Silent wrong rendering** — a mis-ported code→type row renders the wrong fragment with no error;
  casing the HUB fall-through "properly" breaks hub-material rendering outright.
- **Recurring drift** — five hand-maintained tables in three repos keep diverging after migration; every
  added impl or renamed backend string is a latent production bug.
- **Per-team reinvention** — sample and search (later phase) redesign the same dispatch problem without a
  playbook.

### 1.4 Objectives

The spike is done when all of the following are recorded and ratified:
- A confirmed `code → type` registry for every dispatcher, read from the legacy resolver source (the
  declared authority) and verified against backend data once per domain.
- A dispatch playbook (constants enum + dumb-lookup resolver + one-file-per-variant) reusable by the two
  out-of-scope sites and later-phase domains.
- A CI conformance gate that fails the build when schema, enum, or golden fixture disagree — making
  silent drift structurally impossible.
- Behavioral parity for every row of every table, including the defaults, pinned by fixtures.

## 2. What the spike must decide

- The confirmed `code → type` mapping for every dispatcher (legacy resolver source is the authority).
- How each resolver dispatches rows to the right variant, and how CI keeps schema and mapping in sync.
- **Proposal so far (light, to validate):** one dispatcher per interface/union + per-variant resolvers, with a CI conformance check.
- **Draft decision:** [ADR-017 (draft)](./01-adr-polymorphic-type-resolution.md) proposes per-site ports +
  shared playbook + CI conformance gate (Option B) — status 🔴 Proposed, pending ratification. Scenario
  variant under the domain-ACL assumption: [ADR-017-noACL](./02-adr-noacl-polymorphic-type-resolution.md).

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
