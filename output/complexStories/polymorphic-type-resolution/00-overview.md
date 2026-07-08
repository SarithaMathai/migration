# Complex Story — Polymorphic type resolution (`@DgsTypeResolver` + per-variant + prefix-gated parents)

> **Summary —** Same shape-shifting problem in three domains — a category code decides the real type, and today's dispatch tables drift silently. One `@DgsTypeResolver` playbook, enforced by CI, ends the drift.
> **Spike:** `SPARK-SPIKE-05` · **Status:** 🔴 Open — decision pending
> **⚠ Map authority:** the legacy resolver source is the authority for every dispatch table — do not port a dispatch map from drafted pseudo-code.
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** bom (`plm-product`), sample (`plm-sample`), search (`plm-elastic-search`)
> **Stub stories:** `SPARK-BOM-G08`/material interface, `SPARK-SMPL-G02` (later phase)/`A04`, `SPARK-SRCH-G01` (later phase)/`G02`

> **Migrates (source resolvers → this case):** bom **TR `BomMaterialInterface.__resolveType`** +
> **`BomImpressionDetailsInterface.__resolveType`** (`SPARK-BOM-A04`, material FRs `SPARK-BOM-G08`); sample
> **TR `SampleAsset` union** (`SPARK-SMPL-A04` (later phase)) + **FR `SampleV2.parent*`** (`SPARK-SMPL-G02` (later phase)); search
> **Q `materialsSearch`** polymorphic stubs (`SPARK-SRCH-C02` (later phase)/`B01`).
> **Note:** two further `__resolveType` sites (discussion `Resource` union, product `SPARK_Categories`) are not
> yet in this case — see `../REVIEW-findings.md` §2.

## 1. The problem (it recurs in three domains)

| Polymorphic point | Domain | Shape |
|---|---|---|
| `BomMaterialInterface` | bom | **7 impls**, a **21-case dispatcher** keyed on `materialCategory.code` (default 1 COMPONENT, 5 OTHER, **9 HUB → `BomMaterial`** falls through) |
| `BomImpressionDetailsInterface` | bom | **5 impls**, internal/external branch |
| `SampleAsset` union | sample | `Color \| Artwork` via `SampleV2.asset`, by id prefix |
| `SampleV2.parent*` | sample | **prefix-gated** concrete parents (product/trim/colorArchroma/fabric/artwork/asset) |
| `materialsSearch` results | search | polymorphic `Material` results (stubbed entities, `__typename` + id) |

**Why it's complex:** each needs an exact `__resolveType` / type-resolver, **per-variant field resolvers**, and
- it **silently drifts** as fields are added to one impl but not the others.
- Prior research shows the federation- native version: a `Material` interface with `@key`, polymorphic search returning stubs, fields resolved on the concrete type.
- Getting the dispatcher mapping **exactly** right (esp. the HUB fall-through default) is the risk.

## 2. What the spike must decide

- The confirmed `code → type` mapping for every dispatcher (legacy resolver source is the authority).
- How each resolver dispatches rows to the right variant, and how CI keeps schema and mapping in sync.
- **Proposal so far (light, to validate):** one dispatcher per interface/union + per-variant resolvers, with a CI conformance check.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
