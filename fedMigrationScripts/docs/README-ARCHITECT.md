# README (Architect) — how to navigate the migration docs as an Architect

> For **Architects and Tech Leads** owning the federation design and the cross-domain decisions.
> Navigation only — what to open, in what order. Full file inventory + conventions: [`README.md`](./README.md).

---

## Your path

1. **Shape of the migration — the domain breakdown:** `output/summary/{domain}/FederatedGqlBrakDown-{domain}.md`
   - Phase A–G structure, the **spike-gated stories** (🔴🔬), dependencies, and pointers to the complex cases.
     This is the map; use it to see boundaries and sequencing at a glance.

2. **The target design — the SDL + analysis:** `output/initial-analysis/{domain}/`
   - `03-schema.graphql` — the **target federated SDL** (the DGS schema you're approving).
   - `03-schema-analysis.md` — **type classification, federation boundaries, `@key` candidates, gap analysis**.
   - `01-schema-inventory.md` — the full type/field surface being migrated.

3. **The decisions you own — spikes & ADRs:** the 6 program spikes (`SPARK-SPIKE-01…06`, in the global
   breakdown's *Phase 0 — Program Spikes*).
   - You **approve the option**; that decision becomes an ADR and drives the case design.
   - Index of status + chosen option: [`adrs/adr-index.yaml`](../../adrs/adr-index.yaml).
   - The full flow (where the ADR goes, multi-option handling, what to update):
     [`fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md`](../reference/SPIKE-ADR-LIFECYCLE.md).

4. **The hard cross-domain cases — the design detail:** `output/complexStories/{case}/`
   - `00-overview.md` §2 (chosen approach + the ADR it came from) · `ARCHITECTURE.md` (C4 static view, NFR,
     consistency) · `implementation/` (per-service SDL + pseudo-code).

5. **Patterns:** `fedMigrationScripts/reference/federation-patterns.md` and `stitching-patterns.md`
   (`@key`, `@requires`, `@external`, `extend type`, entity fetchers, gateway stitch).

---

## What to focus on (architect lens)

- **Federation boundaries:** co-located (in-process, same `plm-product` JAR) vs separate DGS (true
  `_entities` hop). The `03-schema-analysis.md` calls each out; confirm the ones marked *synthesized `@key`*.
- **The spike decisions are yours to sign off** — edge rule (`@key`-ref vs client), non-atomic-write failure
  strategy, TechPack assembly pattern, polymorphic dispatch. Each lands in a `complexStories/<case>/`.
- **ACL is context-only** — not re-implemented in the DGS layer (per decision). Stories note where the gateway
  curries a token; there is **no ACL story**.
- **Schema-drift ops** (declared in SDL, no resolver) are flagged ⏭ — decide keep-vs-`@deprecate`.

## When to open `code/`
Reference the legacy `code/` only to **confirm an ambiguous boundary** or a **`@key` you're synthesizing**
that isn't explicit in the SDL. Otherwise `03-schema*` + the resolver analysis are your working set.

## How to read a story row
```
SPARK-BOM-B04 · getBomByParentId · 🔷 Query · 🟢 Low [XS] · Depends On: — · ⬜ Not Started
```
Phase 🔬0 🧱A 📖B 🔍C ✏️D ⚙️E 🔗F 🧪G · Type 🔷Query 🔶Mutation 🔸Resolver · Size 🟢XS 🟡M 🟠L 🔴XL.

> **Do not edit** the generated `summary/` docs — edit `initial-analysis/{domain}/03-*`/`04-*` and regenerate
> (see the Script Runner section in [`README.md`](./README.md)).
