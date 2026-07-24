# Spark → Federated GraphQL Migration — Program Overview

> 🏷️ **Tags:** `dgs-migration` · `program-overview` — **Confluence:** *Federation Graph Migration* (space home)
> **Generated:** 2026-07-24 · **Scope:** 8 domains (phase 1) · `spark-internal-graphql` → Netflix DGS via Hive Schema Registry
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
| **Total backend stories** | **211** build stories (Phase-0 spikes tracked separately: 7 program spikes + their domain stubs) |
| **Total frontend stories** | **41** (platform enablement complete — waves 1–4) |
| Complexity (backend) | 🔴 6 Very High · 🟠 13 High · 🟡 74 Medium · 🟢 118 Low |
| Open decisions | 34 |
| **Backend effort (buffered +20%)** | **432–733 engineer-days** |
| **Frontend effort (single-engineer)** | **165–256 engineer-days** |

---

## Domains at a glance

| Domain | Target DGS | BE Stories | T-Shirt | 🔴 | 🟠 | 🟡 | 🟢 | BE effort (buffered) | FE Stories | FE effort | Top risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Product](./product/FederatedGqlBreakDown-product.md) | `plm-product (host)` | **69** | XXL | 5 | 4 | 27 | 33 | 194–326d | 13 | 68–104d | 🔴 High TechPack aggregation + partner drop/undrop orchestration |
| [BOM](./bom/FederatedGqlBreakDown-bom.md) | `plm-product (co-located)` | **37** | XL | 1 | 2 | 13 | 21 | 68–114d | 7 | 29–46d | 🔴 High `updateBom` 3-step write — no rollback path today |
| [Packaging](./packaging/FederatedGqlBreakDown-packaging.md) | `plm-product (co-located)` | **23** | L | 0 | 2 | 8 | 13 | 42–72d | 5 | 21–33d | 🟡 Medium `updatePackaging` multi-step write + elastic search cutover |
| [Measurement](./measurement/FederatedGqlBreakDown-measurement.md) | `plm-product (co-located)` | **30** | L | 0 | 1 | 5 | 24 | 32–55d | 4 | 12–19d | 🟡 Medium `updateMeasurement` 2-step write + master-data cache |
| [Claims](./claims/FederatedGqlBreakDown-claims.md) | `spark-claims (separate)` | **20** | L | 0 | 2 | 8 | 10 | 36–62d | 4 | 17–27d | 🟡 Medium `updateClaim` proxy-ACL multi-step + camelCase response bug |
| [Impression](./impression/FederatedGqlBreakDown-impression.md) | `plm-product (co-located)` | **7** | XS | 0 | 0 | 2 | 5 | 11–18d | 2 | 3–5d | 🟢 Low Impression sub-type polymorphism (5 types) |
| [Product Details](./productDetails/FederatedGqlBreakDown-productDetails.md) | `plm-product (co-located)` | **12** | M | 0 | 1 | 6 | 5 | 24–42d | 3 | 8–12d | 🟡 Medium `updateProductDetailsSet` multi-step + elastic search |
| [Watchlist](./watchlist/FederatedGqlBreakDown-watchlist.md) | `plm-product (co-located)` | **13** | M | 0 | 1 | 5 | 7 | 25–44d | 3 | 7–10d | 🟡 Medium `updateWatchlistEntries` multi-step write |
| **TOTAL** | — | **211** | — | **6** | **13** | **74** | **118** | **432–733d** | **41** | **165–256d** | — |

> BE counts + complexity are computed live from each domain's `be-04-stories.md`; FE counts + effort from `fe-08-frontend-stories.md` (same parsers as the breakdowns + Jira CSVs), so these totals always reconcile. BE effort is buffered +20%; FE effort is single-engineer, unbuffered. Each domain's FE stories live in `summary/{domain}/FederatedGqlBreakDown-{domain}.md` (Frontend section).

---

## Backend stories by phase

> Phases: 🧱 **A** Foundation & Type Resolvers · 📖 **B** Core Reads · 🔍 **C** Search & Listing · ✏️ **D** Mutations · ⚙️ **E** Complex Operations · 🔗 **F** Federation & Stitching · 🧪 **G** Field Resolvers & Tests · 🧬 **H** Entity Resolution. Phase-0 spikes are tracked separately (program spike register). Frontend stories are staged by **wave**, not phase — see `analysis/program/fe-10-migration-sequencing.md`.

| Domain | 🧱 A | 📖 B | 🔍 C | ✏️ D | ⚙️ E | 🔗 F | 🧪 G | 🧬 H | Total |
|---|---|---|---|---|---|---|---|---|---|
| [Product](./product/FederatedGqlBreakDown-product.md) | 0 | 11 | 5 | 18 | 5 | 8 | 16 | 6 | **69** |
| [BOM](./bom/FederatedGqlBreakDown-bom.md) | 2 | 7 | 5 | 5 | 1 | 2 | 15 | 0 | **37** |
| [Packaging](./packaging/FederatedGqlBreakDown-packaging.md) | 0 | 6 | 1 | 9 | 1 | 1 | 5 | 0 | **23** |
| [Measurement](./measurement/FederatedGqlBreakDown-measurement.md) | 0 | 9 | 2 | 10 | 1 | 1 | 5 | 2 | **30** |
| [Claims](./claims/FederatedGqlBreakDown-claims.md) | 0 | 5 | 2 | 5 | 1 | 0 | 5 | 2 | **20** |
| [Impression](./impression/FederatedGqlBreakDown-impression.md) | 0 | 2 | 0 | 1 | 0 | 1 | 3 | 0 | **7** |
| [Product Details](./productDetails/FederatedGqlBreakDown-productDetails.md) | 0 | 1 | 1 | 5 | 1 | 1 | 3 | 0 | **12** |
| [Watchlist](./watchlist/FederatedGqlBreakDown-watchlist.md) | 0 | 3 | 1 | 2 | 1 | 2 | 4 | 0 | **13** |
| **TOTAL** | **2** | **44** | **17** | **55** | **11** | **16** | **56** | **10** | **211** |

---

## DGS service groupings

| DGS Service | Phase | Domains | Combined stories |
|---|---|---|---|
| `plm-product` | 1 | Product · BOM · Measurement · Packaging · Impression · Product Details · Watchlist | 191 |
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
Tier 4 — Federation:  all Phase H entity-resolution stories, once the owning subgraph is live
```

## Cross-domain blockers (true federation — a separate DGS must migrate first)

| Blocked story | Domain | Waits on |
|---|---|---|
| `PRODUCT-BE-H-01` (attachments) | product | **attachment** (`plm-attachment`, later phase) |
| `PRODUCT-BE-H-02` (discussions) | product | **discussion** (`plm-discussion`, later phase) |
| `PRODUCT-BE-H-03` (sample) | product | **sample** (`plm-sample`, later phase) |
| `PRODUCT-BE-H-04` (claims) | product | **claims** (`spark-claims`, phase 1) |
| `PRODUCT-BE-H-05` (constructions) | product | **construction** (no subgraph scheduled yet — `H-05` stays blocked until one exists) |
| `MST-BE-H-01` (sampleMeasurement) | measurement | **sample** (`plm-sample`, later phase) |

> Internal (NOT blockers, same `plm-product` subgraph): `BOM-BE-F-01/F-02`, `PRODUCT-BE-F-04/F-06/F-08`, `MST-BE-F-01`, `IMPRESSION-BE-F-01`, `PDTL-BE-F-01`, `PKG-BE-F-01`. Cross-subgraph entity resolution (Phase H) is now split out from platform/gateway work that stays Phase F — see `PRODUCT-BE-H-06` (the `Product` entity fetcher) for the one Phase H story with no later-phase blocker.

---

## How to consume

- **Per domain (backend + frontend):** open `summary/{domain}/FederatedGqlBreakDown-{domain}.md` (or the `.docx` for Confluence/Word) — one merged page: `## Backend` then `## Frontend` (the Frontend section is generated by `generate_frontend.py`'s `build_fe_section()`).
- **Federation schema review:** `analysis/federation-review/` (hand-authored) — schema validation, cross-domain identifier inventory, required contract fixes (R1–R6), recommended entity references, entity-resolver analysis, and the risks/open-questions register. Required-fix stories: `PRODUCT-BE-F-13/F-14`, `CLAIM-BE-G-06`, `PRODUCT-FE-013`.
- **Cross-domain field analysis:** `analysis/schemaAnalysis/00-cross-domain-field-inventory.md` (program roll-up of each domain's `be-06-cross-domain-field-analysis.md`) — which fields hydrate another domain, real client usage, complexity, federation recommendation.
- **ACL research:** `analysis/aclResearch/00-acl-usage-inventory.md` (program roll-up of each domain's `be-07-acl-usage-analysis.md`) — classifies every ACL call site and proposes Mid-Request ACL Update for downstream-token cases; **supersedes** the "ACL is context-only, ignored" note in be-03/be-04 pending review (not yet applied to those docs).
- **Jira:** import `jira/{domain}.csv` (or `jira/all-stories.csv`). See `PUSH-TO-JIRA-CONFLUENCE.md`.
- **Read order by role + regeneration:** see `README.md`.

---
*Program overview · generated 2026-07-24 from `output/analysis/*/04-*.md`.*