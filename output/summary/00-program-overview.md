# Spark → Federated GraphQL Migration — Program Overview

> 🏷️ **Tags:** `dgs-migration` · `program-overview` — **Confluence:** *Federation Graph Migration* (space home)
> **Generated:** 2026-07-16 · **Scope:** 8 domains (phase 1) · `spark-internal-graphql` → Netflix DGS via Hive Schema Registry
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
| **Total stories** | **200** build stories (Phase-0 spikes tracked separately: 7 program spikes + their domain stubs) |
| Complexity | 🔴 6 Very High · 🟠 13 High · 🟡 76 Medium · 🟢 105 Low |
| Open decisions | 34 |
| **Effort (buffered +20%)** | **432–733 engineer-days** |

---

## Domains at a glance

| Domain | Target DGS | Stories | T-Shirt | 🔴 | 🟠 | 🟡 | 🟢 | Effort (buffered) | Top risk |
|---|---|---|---|---|---|---|---|---|---|
| [Product](./FederatedGqlBrakDown-BE-product.md) | `plm-product (host)` | **67** | XXL | 5 | 4 | 25 | 33 | 194–326d | 🔴 High TechPack aggregation + partner drop/undrop orchestration |
| [BOM](./FederatedGqlBrakDown-BE-bom.md) | `plm-product (co-located)` | **36** | XL | 1 | 2 | 12 | 21 | 68–114d | 🔴 High `updateBom` 3-step write — no rollback path today |
| [Packaging](./FederatedGqlBrakDown-BE-packaging.md) | `plm-product (co-located)` | **24** | L | 0 | 2 | 9 | 13 | 42–72d | 🟡 Medium `updatePackaging` multi-step write + elastic search cutover |
| [Measurement](./FederatedGqlBrakDown-BE-measurement.md) | `plm-product (co-located)` | **20** | M | 0 | 1 | 6 | 13 | 32–55d | 🟡 Medium `updateMeasurement` 2-step write + master-data cache |
| [Claims](./FederatedGqlBrakDown-BE-claims.md) | `spark-claims (separate)` | **20** | L | 0 | 2 | 9 | 9 | 36–62d | 🟡 Medium `updateClaim` proxy-ACL multi-step + camelCase response bug |
| [Impression](./FederatedGqlBrakDown-BE-impression.md) | `plm-product (co-located)` | **7** | XS | 0 | 0 | 2 | 5 | 11–18d | 🟢 Low Impression sub-type polymorphism (5 types) |
| [Product Details](./FederatedGqlBrakDown-BE-productDetails.md) | `plm-product (co-located)` | **13** | M | 0 | 1 | 7 | 5 | 24–42d | 🟡 Medium `updateProductDetailsSet` multi-step + elastic search |
| [Watchlist](./FederatedGqlBrakDown-BE-watchlist.md) | `plm-product (co-located)` | **13** | M | 0 | 1 | 6 | 6 | 25–44d | 🟡 Medium `updateWatchlistEntries` multi-step write |
| **TOTAL** | — | **200** | — | **6** | **13** | **76** | **105** | **432–733d** | — |

> All counts + complexity are computed live from each domain's `be-04-stories.md` (same parser as the breakdown + Jira CSVs), so these totals always reconcile.

---

## DGS service groupings

| DGS Service | Phase | Domains | Combined stories |
|---|---|---|---|
| `plm-product` | 1 | Product · BOM · Measurement · Packaging · Impression · Product Details · Watchlist | 180 |
| `spark-claims` | 1 | Claims | 20 |
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

- **Per domain (backend):** open `summary/FederatedGqlBrakDown-BE-{domain}.md` (or the `.docx` for Confluence/Word).
- **Per domain (frontend):** open `summary/FederatedGqlBrakDown-FE-{domain}.md` (generated by `generate_frontend.py`).
- **Jira:** import `jira/{domain}.csv` (or `jira/all-stories.csv`). See `PUSH-TO-JIRA-CONFLUENCE.md`.
- **Read order by role + regeneration:** see `README.md`.

---
*Program overview · generated 2026-07-16 from `output/analysis/*/04-*.md`.*