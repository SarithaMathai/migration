# Spark GraphQL → Federated GraphQL — Migration Analysis (Final)

> **What this folder is:** the reviewed, corrected, and junior-engineer-ready output of the
> Spark-internal-GraphQL → Netflix DGS federation migration investigation.
> **Generated:** 2026-06-26 · **Pipeline Version:** 2.0 (supersedes the draft in `../output`)

---

## 1. Read this first — pick your audience

The same analysis is published in three layers. **Go to the one for your job:**

| If you are… | Go to | What you get |
|-------------|-------|--------------|
| A **Product Owner** / stakeholder | [`confluence/`](./confluence/) | One PO page per domain + a [program portfolio](./confluence/00-portfolio.md) — paste into Confluence |
| **Creating Jira tickets** | [`jira/`](./jira/) | `all-stories.csv` / per-domain CSV for **bulk import**, plus per-issue Markdown — see [`jira/README.md`](./jira/README.md) |
| **Implementing a story** | `<domain>/04-stories.md` + `<domain>/02-resolver-analysis.md` | The self-contained spec: current behaviour, endpoints, files, acceptance, tests |
| Analyzing a **new** domain | [`scripts/`](./scripts/) | The investigation framework + [`RUN-NEW-DOMAIN.md`](./scripts/RUN-NEW-DOMAIN.md) |

Underneath, the per-domain folders (`product/`, `bom/`, `measurement/`, `impression/`) hold the **8 source
analysis files** (the source of truth); `confluence/` and `jira/` are the **consumption layer** generated
from them. Program rollup: [`STORIES-INDEX.md`](./STORIES-INDEX.md) + [`index.yaml`](./index.yaml) — all
**325** stories across the 11 domains.

If you are a **junior engineer assigned a story**, you do **not** need to read the scripts.
Go straight to your domain folder and open `04-stories.md`. Every story is self-contained:
it tells you the current behaviour, the exact REST endpoints, the files to create, the
acceptance criteria, and the test cases. See [§4](#4-junior-engineer-quick-start).

---

## 2. What changed from the draft (`../output`) — and why

This `finalOutput/` corrects three concrete problems found while reviewing `../output` against the
actual source code in `../code`.

### 2.1 The schema source of truth (updated 2026-06-27)
The original draft framework told the analyst to *"open `context.js`"* and *"read
`schemas/SPARK_{Domain}.graphql`"* against the full `spark-internal-graphql` checkout. The `code/`
snapshot is smaller: there is **still no `context.js`** (endpoint/auth facts come from each service's
constructor — e.g. `BomService` builds its URL there). **The `.graphql` schemas, however, are now
included** under `code/schemas/` as `.txt` (e.g. `code/schemas/SPARK_Product.txt` is the real Product
SDL). `code/schemas/index.txt` is the stitch-order manifest; `core.txt` holds shared scalars.

**Fix:** the updated scripts in [`scripts/`](./scripts/) read endpoint/auth facts from the **service
files** instead of `context.js`, and treat **`code/schemas/SPARK_{Domain}.txt` as the schema source of
truth** — cross-checked against the resolver for behaviour (e.g. a field declared in the SDL with no
top-level resolver is a "schema-drift" op). The per-domain `03-schema.graphql` is the *federated target*
schema translated from that SDL. See [`scripts/00-adapting-to-this-repo.md`](./scripts/00-adapting-to-this-repo.md).

### 2.2 The stories were too terse for a junior engineer
The draft `04-stories.md` collapsed most operations into one-liners such as
*"SPARK-BOM-B02 — getBomStatus (cacheable master data)."* A junior engineer cannot start from that:
there is no current-behaviour spec, no endpoint, no acceptance criteria, no tests.

**Fix:** every story here uses the **full junior-ready template**
([`scripts/story-template-junior.md`](./scripts/story-template-junior.md)). The migrated domains'
own `04-stories.md` (e.g. [`product/04-stories.md`](./product/04-stories.md)) are the gold-standard examples.
Each story now embeds: Current Behaviour (pseudo-logic), EXT-service calls with severity, Target DGS
implementation, Files to create/modify, Dependencies, **objectively verifiable** Acceptance Criteria,
and a Test-case checklist. The rule is encoded in
[`scripts/skill-04-story-generation.md`](./scripts/skill-04-story-generation.md) §"Definition of Ready
for a junior engineer".

### 2.3 Facts were re-verified against the real code
Line counts, endpoint paths, JWT/ACL behaviour, the 7 polymorphic `BomMaterial` variants, the
internal-vs-external user branch, and the latent bugs were all re-checked against the actual
`.txt` source. Where the draft and the code disagreed, the **code wins** and the discrepancy is noted.

---

## 3. The eleven domains in this folder

Seven compile into the **same `plm-product` DGS — a monorepo / single federation subgraph**. Because they
are co-located, their references to each other (`Bom.product`, `Product.measurementSets`,
`ResourcesCount.bomsCount`, …) are **plain internal GraphQL types and in-process calls — not gateway
federation**. **`claims` (`spark-claims`), `workspace` (`plm-workspace`), `search` (`plm-elastic-search`),
and `sample` (`plm-sample`) are separate subgraphs** that federate with the rest (workspace/sample provide
the `WorkspaceV2`/`SampleV2` entities; search is the read hub).
True federation (`@extends @external`, CAT-4) applies only to **separate** DGS subgraphs
(attachment, workspace, discussion, sample, claim, tag, access-control, user-profile, search, and the material
DGSs hub/trim/wash/fabric/combination) and platforms (VMM/IG/Doppler/CORONA/APEX). See
[scripts/reference-federation-patterns.md §0](./scripts/reference-federation-patterns.md).

| Domain | Source resolver | Lines | Queries | Mutations | Stories | Headline complexity |
|--------|-----------------|-------|---------|-----------|---------|---------------------|
| [`impression`](./impression/) | `resolvers/product/SPARK_Impression.txt` | 66 | 2 | 1 | 11 | smallest; lowest-risk — **recommended first** |
| [`productDetails`](./productDetails/) | `resolvers/product/SPARK_ProductDetail.txt` | 129 | 2 | 6 | 17 | "construction" sets; one multi-step write |
| [`watchlist`](./watchlist/) | `resolvers/product/SPARK_Watchlist.txt` | 129 | 4 | 3 | 17 | co-located; multi-step write (await-race fix) |
| [`measurement`](./measurement/) | `resolvers/product/SPARK_Measurement.txt` | 175 | 7 | 8 | 24 | one 2-step write; relationship dependency |
| [`claims`](./claims/) | `resolvers/product/SPARK_Claims.txt` | 164 | 7 | 6 | 24 | **separate subgraph**; proxy-ACL update |
| [`search`](./search/) | `resolvers/SPARK_Search.txt` | 507 | ~48 | 1 | 25 | **separate subgraph**; elastic read hub; wide type surface |
| [`packaging`](./packaging/) | `resolvers/product/SPARK_Packaging.txt` | 273 | 7 | 10 | 28 | wide schema; multi-step write + pricing chain |
| [`workspace`](./workspace/) | `resolvers/SPARK_WorkspaceV2.txt` | 1,060 | 8 | 10(+2) | 32 | **separate subgraph**; 5-case partner dispatcher; hub entity |
| [`sample`](./sample/) | `resolvers/SPARK_SampleV2.txt` | 430 | 23 | 9(+3) | 33 | **separate subgraph**; `SampleAsset` union; prefix-gated parents |
| [`bom`](./bom/) | `resolvers/product/SPARK_Bom.txt` | 735 | 13 | 6 | 42 | 7-variant polymorphic `BomMaterial`; 3-step write |
| [`product`](./product/) | `resolvers/SPARK_Product.txt` | 2,629 | 18 | 20(+3) | 72 | TechPack aggregation; `components`; host DGS |
| **Total** | | | | | **325** | |

Each domain folder contains **eight** artifacts:

| File | What it answers | Primary audience |
|------|-----------------|------------------|
| `01-schema-inventory.md` | What files exist, how big, what they reference | Tech Lead |
| `02-resolver-analysis.md` | What every operation *does*, in plain English + REST detail | Engineers |
| `03-schema.graphql` | The target DGS schema to drop into `resources/schema/` (derived) | Architects |
| `03-schema-analysis.md` | Type ownership, federation boundaries, **Migration Approach** | Architects / Confluence |
| `04-stories.md` | Jira-ready, junior-executable engineering stories (one op each, YAML front-matter) | Engineering team |
| `04-stories-index.yaml` | Machine-readable story list for Jira MCP bulk-create | Copilot / agents |
| `04-po-summary.md` | Sprint plan, effort, risks, decisions | Product Owner / Confluence |
| `05-attribute-inventory.md` | Every schema field → resolution kind / EXT / complexity / story | Engineers, POs, Confluence |

---

## 4. Junior-engineer quick start

1. Open your domain folder (e.g. [`bom/`](./bom/)).
2. Open `04-stories.md`. Find your story ID (e.g. `SPARK-BOM-B02`).
3. Read these sections of your story, in order:
   - **Current Behaviour** — what the existing Node.js code does (you do *not* need to read the JS).
   - **Target DGS Implementation** — the Kotlin/DGS shape you are building.
   - **Files to Create / Modify** — exact paths.
   - **Acceptance Criteria** — your definition of done; each item is checkable.
   - **Test Cases** — write these.
4. Check **Dependencies** — do not start until the listed stories are merged.
5. If a step mentions an **EXT Service** with a 🔴/🟡/🔵 tag, that is a cross-domain call —
   read [`scripts/reference-federation-patterns.md`](./scripts/reference-federation-patterns.md)
   or ask your tech lead which CAT-4 story covers it.

You should never have to open the original `.txt` resolver to do your story. If you do, that is a
bug in the story — tell your tech lead so the analysis can be corrected.

---

## 5. Provenance

- **Source of truth:** `../code` — schema SDL (`code/schemas/SPARK_{Domain}.txt`), resolvers, services,
  utils (`.txt` snapshot; no `context.js` config).
- **Reviewed against:** `../output` (the earlier draft artifacts).
- **Framework:** [`scripts/`](./scripts/) is the self-contained investigation framework (it supersedes
  the earlier `fedMigrationScripts` draft). Conventions and amendments are described in
  [§2](#2-what-changed-from-the-draft-output--and-why).
