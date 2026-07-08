# Spark → Federated GraphQL Migration — Program Overview

> 🏷️ **Tags:** `dgs-migration` · `program-overview` — **Confluence:** *Federation Graph Migration* (space home)
> **Generated:** 2026-07-07 · **Scope:** 13 domains · `spark-internal-graphql` → Netflix DGS via Hive Schema Registry
> Effort is **AI-estimated — confirm in refinement.**

---

## What & why

- We are moving the PLM GraphQL API off the monolithic `spark-internal-graphql` Node.js gateway onto **Netflix DGS** subgraphs, federated via the **Hive Schema Registry**.
- Seven domains compile into the **same `plm-product` subgraph** (their cross-references resolve internally); **claims, search, workspace, sample, attachment, discussion** are separate subgraphs that federate back in.

**Engineering model:**
- Every story is self-contained in one PR — schema + DGS data fetcher + Kotlin REST service method + Hive push.
- The model, REST controllers (GET/POST/PUT) and services already exist; each story only adds the thin DGS wrapper.
- **Ship on green, per story** — except cross-subgraph entity extensions, which wait for their owning subgraph.

---

## Program totals

| Metric | Value |
|---|---|
| Total domains | 13 |
| Target DGS services | 7 |
| **Total stories** | **343** |
| Complexity | 🔴 9 Very High · 🟠 35 High · 🟡 143 Medium · 🟢 156 Low |
| Open decisions | 51 |
| **Effort (buffered +20%)** | **742–1251 engineer-days** |

---

## Domains at a glance

| Domain | Target DGS | Stories | T-Shirt | 🔴 | 🟠 | 🟡 | 🟢 | Effort (buffered) | Top risk |
|---|---|---|---|---|---|---|---|---|---|
| [Product](./product/FederatedGqlBrakDown-product.md) | `plm-product (host)` | **70** | XXL | 5 | 5 | 27 | 33 | 197–330d | 🔴 High TechPack aggregation + partner drop/undrop orchestration |
| [BOM](./bom/FederatedGqlBrakDown-bom.md) | `plm-product (co-located)` | **39** | XL | 1 | 2 | 13 | 23 | 68–114d | 🔴 High `updateBom` 3-step write — no rollback path today |
| [Workspace](./workspace/FederatedGqlBrakDown-workspace.md) | `plm-workspace (separate)` | **28** | XL | 3 | 3 | 13 | 9 | 75–126d | 🔴 High Partner-action dispatcher with un-awaited promise chains |
| [Sample](./sample/FederatedGqlBrakDown-sample.md) | `plm-sample (separate)` | **28** | XL | 0 | 5 | 11 | 12 | 70–116d | 🟡 Medium RFID ops + clone + multi-round write orchestration |
| [Discussion](./discussion/FederatedGqlBrakDown-discussion.md) | `plm-discussion (separate)` | **32** | XL | 0 | 4 | 15 | 13 | 61–102d | 🟡 Medium Three API versions (v1/v2/V3) + core* twins to consolidate |
| [Search](./search/FederatedGqlBrakDown-search.md) | `plm-elastic-search (sep.)` | **25** | L | 0 | 7 | 11 | 7 | 59–99d | 🔴 High Read-hub cutover — every domain depends on search |
| [Packaging](./packaging/FederatedGqlBrakDown-packaging.md) | `plm-product (co-located)` | **24** | L | 0 | 2 | 9 | 13 | 42–72d | 🟡 Medium `updatePackaging` multi-step write + elastic search cutover |
| [Attachment](./attachment/FederatedGqlBrakDown-attachment.md) | `plm-attachment (separate)` | **24** | L | 0 | 2 | 14 | 8 | 42–71d | 🟡 Medium Dual record shape (snake/camel) + ACL-permission writes |
| [Measurement](./measurement/FederatedGqlBrakDown-measurement.md) | `plm-product (co-located)` | **20** | M | 0 | 1 | 6 | 13 | 32–55d | 🟡 Medium `updateMeasurement` 2-step write + master-data cache |
| [Claims](./claims/FederatedGqlBrakDown-claims.md) | `spark-claims (separate)` | **20** | L | 0 | 2 | 9 | 9 | 36–62d | 🟡 Medium `updateClaim` proxy-ACL multi-step + camelCase response bug |
| [Impression](./impression/FederatedGqlBrakDown-impression.md) | `plm-product (co-located)` | **7** | XS | 0 | 0 | 2 | 5 | 11–18d | 🟢 Low Impression sub-type polymorphism (5 types) |
| [Product Details](./productDetails/FederatedGqlBrakDown-productDetails.md) | `plm-product (co-located)` | **13** | M | 0 | 1 | 7 | 5 | 24–42d | 🟡 Medium `updateProductDetailsSet` multi-step + elastic search |
| [Watchlist](./watchlist/FederatedGqlBrakDown-watchlist.md) | `plm-product (co-located)` | **13** | M | 0 | 1 | 6 | 6 | 25–44d | 🟡 Medium `updateWatchlistEntries` multi-step write |
| **TOTAL** | — | **343** | — | **9** | **35** | **143** | **156** | **742–1251d** | — |

> All counts + complexity are computed live from each domain's `04-stories.md` (same parser as the breakdown + Jira CSVs), so these totals always reconcile.

---

## DGS service groupings

| DGS Service | Domains | Combined stories |
|---|---|---|
| `plm-product` | Product · BOM · Measurement · Packaging · Impression · Product Details · Watchlist | 186 |
| `plm-sample` | Sample | 33 |
| `plm-discussion` | Discussion | 37 |
| `plm-workspace` | Workspace | 32 |
| `plm-attachment` | Attachment | 26 |
| `plm-elastic-search` | Search | 21 |
| `spark-claims` | Claims | 22 |

---

## Recommended sequencing

```
Tier 1 — Foundation:  Search (read hub) · Product (host DGS, shared wiring)
Tier 2 — Co-located:  Impression → Measurement → ProductDetails → Watchlist → BOM → Packaging
Tier 3 — Separate:    Attachment · Claims · Discussion · Sample · Workspace
Tier 4 — Federation:  all F-phase stories, once the owning subgraph is live
```

## Cross-domain blockers (true federation — a separate DGS must migrate first)

| Blocked story | Domain | Waits on |
|---|---|---|
| `SPARK-PROD-F01` (attachments) | product | **attachment** |
| `SPARK-PROD-F02` (discussions) | product | **discussion** |
| `SPARK-PROD-F03` (sample) | product | **sample** |
| `SPARK-PROD-F05` (claims) | product | **claim** |
| `SPARK-PROD-F07` (constructions) | product | **construction** |
| `SPARK-MEAS-F02` (sampleMeasurement) | measurement | **sample** |

> Internal (NOT blockers, same `plm-product` subgraph): `SPARK-BOM-F01/F02`, `SPARK-PROD-F04/F06/F08`, `SPARK-MEAS-F01`, `SPARK-IMP-F01`, `SPARK-PDTL-F01`, `SPARK-PKG-F01`.

---

## How to consume

- **Per domain:** open `summary/{domain}/FederatedGqlBrakDown-{domain}.md` (or the `.docx` for Confluence/Word).
- **Jira:** import `jira/{domain}.csv` (or `jira/all-stories.csv`). See `PUSH-TO-JIRA-CONFLUENCE.md`.
- **Read order by role + regeneration:** see `README.md`.

---
*Program overview · generated 2026-07-07 from `output/initial-analysis/*/04-*.md`.*