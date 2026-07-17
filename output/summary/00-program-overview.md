# Spark → Federated GraphQL Migration — Program Overview

> 🏷️ **Tags:** `dgs-migration` · `program-overview` — **Confluence:** *Federation Graph Migration* (space home)
> **Generated:** 2026-07-17 · **Scope:** 8 domains (phase 1) · `spark-internal-graphql` → Netflix DGS via Hive Schema Registry
> Effort is **AI-estimated — confirm in refinement.**

---

## What & why

- We are moving the PLM GraphQL API off the monolithic `spark-internal-graphql` Node.js gateway onto **Netflix DGS** subgraphs, federated via the **Hive Schema Registry**.
- Phase 1 covers 8 domains: seven compile into the **same `plm-product` subgraph** (their cross-references resolve internally); **claims** is its own subgraph.
- The remaining domains (attachment, discussion, sample, search, workspace) federate in a later phase.

**Engineering model:**
- Every story is self-contained in one PR — schema + DGS data fetcher + Kotlin REST service method + Hive push.
- The model, REST controllers (GET/POST/PUT) and services already exist; each story only adds the thin DGS wrapper.
- **Ship on green, per story** — except cross-subgraph entity extensions, which wait for their owning subgraph.

---

## Program totals

| Metric | Value |
|---|---|
| Total domains | 8 |
| Target DGS services | 2 |
| **Total backend stories** | **148** build stories (Phase-0 spikes tracked separately: 7 program spikes + their domain stubs) |
| **Total frontend stories** | **38** (platform enablement complete — waves 1–4) |
| Complexity (backend) | 🔴 6 Very High · 🟠 13 High · 🟡 93 Medium · 🟢 36 Low |
| Open decisions | 34 |
| **Backend effort (buffered +20%)** | **432–733 engineer-days** |
| **Frontend effort (single-engineer)** | **158–245 engineer-days** |

---

## Domains at a glance

| Domain | Target DGS | BE Stories | T-Shirt | 🔴 | 🟠 | 🟡 | 🟢 | BE effort (buffered) | FE Stories | FE effort | Top risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Product](./product/FederatedGqlBreakDown-BE-product.md) | `plm-product (host)` | **48** | XXL | 5 | 4 | 31 | 8 | 194–326d | 11 | 63–97d | 🔴 High TechPack aggregation + partner drop/undrop orchestration |
| [BOM](./bom/FederatedGqlBreakDown-BE-bom.md) | `plm-product (co-located)` | **24** | XL | 1 | 2 | 16 | 5 | 68–114d | 6 | 27–42d | 🔴 High `updateBom` 3-step write — no rollback path today |
| [Packaging](./packaging/FederatedGqlBreakDown-BE-packaging.md) | `plm-product (co-located)` | **18** | L | 0 | 2 | 11 | 5 | 42–72d | 5 | 21–33d | 🟡 Medium `updatePackaging` multi-step write + elastic search cutover |
| [Measurement](./measurement/FederatedGqlBreakDown-BE-measurement.md) | `plm-product (co-located)` | **14** | M | 0 | 1 | 8 | 5 | 32–55d | 4 | 12–19d | 🟡 Medium `updateMeasurement` 2-step write + master-data cache |
| [Claims](./claims/FederatedGqlBreakDown-BE-claims.md) | `spark-claims (separate)` | **15** | L | 0 | 2 | 11 | 2 | 36–62d | 4 | 17–27d | 🟡 Medium `updateClaim` proxy-ACL multi-step + camelCase response bug |
| [Impression](./impression/FederatedGqlBreakDown-BE-impression.md) | `plm-product (co-located)` | **7** | XS | 0 | 0 | 2 | 5 | 11–18d | 2 | 3–5d | 🟢 Low Impression sub-type polymorphism (5 types) |
| [Product Details](./productDetails/FederatedGqlBreakDown-BE-productDetails.md) | `plm-product (co-located)` | **11** | M | 0 | 1 | 8 | 2 | 24–42d | 3 | 8–12d | 🟡 Medium `updateProductDetailsSet` multi-step + elastic search |
| [Watchlist](./watchlist/FederatedGqlBreakDown-BE-watchlist.md) | `plm-product (co-located)` | **11** | M | 0 | 1 | 6 | 4 | 25–44d | 3 | 7–10d | 🟡 Medium `updateWatchlistEntries` multi-step write |
| **TOTAL** | — | **148** | — | **6** | **13** | **93** | **36** | **432–733d** | **38** | **158–245d** | — |

> BE counts + complexity are computed live from each domain's `be-04-stories.md`; FE counts + effort from `fe-08-frontend-stories.md` (same parsers as the breakdowns + Jira CSVs), so these totals always reconcile. BE effort is buffered +20%; FE effort is single-engineer, unbuffered. Each domain's FE stories live in `summary/{domain}/FederatedGqlBreakDown-FE-{domain}.md`.

---

## Backend stories by phase

> Phases: 🧱 **A** Foundation & Type Resolvers · 📖 **B** Core Reads · 🔍 **C** Search & Listing · ✏️ **D** Mutations · ⚙️ **E** Complex Operations · 🔗 **F** Federation & Stitching · 🧪 **G** Field Resolvers & Tests. Phase-0 spikes are tracked separately (program spike register). Frontend stories are staged by **wave**, not phase — see `analysis/program/fe-10-migration-sequencing.md`.

| Domain | 🧱 A | 📖 B | 🔍 C | ✏️ D | ⚙️ E | 🔗 F | 🧪 G | Total |
|---|---|---|---|---|---|---|---|---|
| [Product](./product/FederatedGqlBreakDown-BE-product.md) | 0 | 4 | 5 | 9 | 4 | 10 | 16 | **48** |
| [BOM](./bom/FederatedGqlBreakDown-BE-bom.md) | 1 | 4 | 3 | 2 | 1 | 2 | 11 | **24** |
| [Packaging](./packaging/FederatedGqlBreakDown-BE-packaging.md) | 0 | 3 | 1 | 6 | 1 | 1 | 6 | **18** |
| [Measurement](./measurement/FederatedGqlBreakDown-BE-measurement.md) | 0 | 2 | 2 | 4 | 1 | 2 | 3 | **14** |
| [Claims](./claims/FederatedGqlBreakDown-BE-claims.md) | 0 | 2 | 2 | 3 | 1 | 2 | 5 | **15** |
| [Impression](./impression/FederatedGqlBreakDown-BE-impression.md) | 0 | 2 | 0 | 1 | 0 | 1 | 3 | **7** |
| [Product Details](./productDetails/FederatedGqlBreakDown-BE-productDetails.md) | 0 | 1 | 1 | 3 | 1 | 1 | 4 | **11** |
| [Watchlist](./watchlist/FederatedGqlBreakDown-BE-watchlist.md) | 0 | 2 | 1 | 2 | 1 | 1 | 4 | **11** |
| **TOTAL** | **1** | **20** | **15** | **30** | **10** | **20** | **52** | **148** |

---

## DGS service groupings

| DGS Service | Phase | Domains | Combined stories |
|---|---|---|---|
| `plm-product` | 1 | Product · BOM · Measurement · Packaging · Impression · Product Details · Watchlist | 133 |
| `spark-claims` | 1 | Claims | 15 |
| `plm-sample` | later | Sample | ~33 (estimate — analysis not yet regenerated) |
| `plm-discussion` | later | Discussion | ~37 (estimate) |
| `plm-workspace` | later | Workspace | ~32 (estimate) |
| `plm-attachment` | later | Attachment | ~26 (estimate) |
| `plm-elastic-search` | later | Search | ~21 (estimate) |

> Phase-1 rows are computed live from `be-04-stories.md`; later-phase rows are earlier-pass estimates,
> re-baselined when those domains' analyses are regenerated.

---

## Recommended sequencing

```
Tier 1 — Foundation:  Product (host DGS, shared wiring; phase 1) · Search (read hub — later-phase domain,
                      sequenced first among them because every domain reads through it)
Tier 2 — Co-located:  Impression → Measurement → ProductDetails → Watchlist → BOM → Packaging  (phase 1)
Tier 3 — Separate:    Claims (phase 1) · Attachment · Discussion · Sample · Workspace  (later phase)
Tier 4 — Federation:  all F-phase stories, once the owning subgraph is live
```

## Cross-domain blockers (true federation — a separate DGS must migrate first)

| Blocked story | Domain | Waits on |
|---|---|---|
| `PRODUCT-BE-F-01` (attachments) | product | **attachment** (`plm-attachment`, later phase) |
| `PRODUCT-BE-F-02` (discussions) | product | **discussion** (`plm-discussion`, later phase) |
| `PRODUCT-BE-F-03` (sample) | product | **sample** (`plm-sample`, later phase) |
| `PRODUCT-BE-F-05` (claims) | product | **claims** (`spark-claims`, phase 1) |
| `PRODUCT-BE-F-07` (constructions) | product | **construction** (no subgraph scheduled yet — `F-07` stays blocked until one exists) |
| `MST-BE-F-02` (sampleMeasurement) | measurement | **sample** (`plm-sample`, later phase) |

> Internal (NOT blockers, same `plm-product` subgraph): `BOM-BE-F-01/F-02`, `PRODUCT-BE-F-04/F-06/F-08`, `MST-BE-F-01`, `IMPRESSION-BE-F-01`, `PDTL-BE-F-01`, `PKG-BE-F-01`.

---

## How to consume

- **Per domain (backend):** open `summary/{domain}/FederatedGqlBreakDown-BE-{domain}.md` (or the `.docx` for Confluence/Word).
- **Per domain (frontend):** open `summary/{domain}/FederatedGqlBreakDown-FE-{domain}.md` (generated by `generate_frontend.py`).
- **Jira:** import `jira/{domain}.csv` (or `jira/all-stories.csv`). See `PUSH-TO-JIRA-CONFLUENCE.md`.
- **Read order by role + regeneration:** see `README.md`.

---
*Program overview · generated 2026-07-17 from `output/analysis/*/04-*.md`.*