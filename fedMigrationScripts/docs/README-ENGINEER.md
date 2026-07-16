# README (Engineer) — how to navigate the migration docs as an Engineer

> For **Engineers** implementing the migration. Navigation only — what to open, in what order.
> Architects/Tech Leads: see [`README-ARCHITECT.md`](./README-ARCHITECT.md). Full inventory + conventions:
> [`README.md`](./README.md).

---

## Your path

1. **Start — the domain's comprehensive doc:** `summary/{domain}/{domain}-comprehensive.md`
   - **Heavy detail, every story end-to-end:** metadata (type, size, depends-on), *In-plain-terms*,
     **Current Behaviour** (what the gateway does today), **examples + pseudocode**, target DGS
     implementation, files to touch, **Acceptance Criteria**, and tests (High/VH).

2. **Go to source when you implement:** `initial-analysis/{domain}/`
   - `04-stories.md` — the story specs (source of truth; the comprehensive doc is generated from this).
   - `02-resolver-analysis.md` — the **per-resolver logic of the current `spark-internal-graphql` gateway**
     (the `(Qn/Mn)` tag in a story's Current Behaviour points here).
   - `03-schema.graphql` — the **target federated SDL** you're building toward.
   - `01-schema-inventory.md` / `05-attribute-inventory.md` — the type/field surface + attribute mapping.

3. **For the hard cross-domain stories:** `output/complexStories/{case}/`
   - `00-overview.md` (banner: Summary · Spike/ADR · Status · who-reads-what) · `ARCHITECTURE.md`
     (design) · `01-stories.md` (sub-tasks) · `implementation/` (pseudo-code + SDL per cross-service op).
   - **8 cases** = the 6 program spikes (+ 2 read patterns). How a spike's ADR becomes these stories:
     `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md`.

4. **Patterns & how-to:** `reference/` (e.g. `reference-federation-patterns.md`, `RUN-NEW-DOMAIN.md`).

---

## What each story tells you

- **Traceability:** the story **title is the `spark-internal-graphql` operation** you're migrating; *Current
  Behaviour* is its exact gateway logic today (DataLoader + REST endpoint).
- **Thin wrapper:** the model, REST controller (GET/POST/PUT) and service already exist — you add only the
  Netflix-DGS layer (`@DgsQuery`/`@DgsMutation`/`@DgsData` + schema type + wiring).
- **`B-01` dependency = the module scaffold** (`{domain}.graphqls` + scalars + service/Feign wiring), landed once.
  It's assumed, not repeated per row — after `B-01`, B/C/D/G are parallel.
- **Ship on green:** merge + deploy a story once its own tests + parity pass. Exceptions are the
  cross-subgraph **BLOCKED-BY** field resolvers (wait for the owning subgraph).
- **Acceptance Criteria + tests** are the definition of done; parity (new DGS output == old gateway output) is
  the gate for cut-over.

## How to read a story row
```
BOM-BE-B-04 · getBomByParentId · 🔷 Query · 🟢 Low [XS] · Depends On: — · ⬜ Not Started
```
Phase 🔬0 🧱A 📖B 🔍C ✏️D ⚙️E 🔗F 🧪G · Type 🔷Query 🔶Mutation 🔸Resolver · Size 🟢XS 🟡M 🟠L 🔴XL.

> **Do not edit** the generated `summary/` docs — edit `initial-analysis/{domain}/04-*.md` and regenerate
> (see the Script Runner section in [`README.md`](./README.md)).
