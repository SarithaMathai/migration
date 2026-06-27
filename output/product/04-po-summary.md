# Product — PO Sprint Planning Summary

> **Domain:** `product`
> **Target DGS:** `ProductService` (repo: `plm-product`, url: `https://spark-product.dev.target.com`)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18
> **Stories:** [04-stories.md](output/product/04-stories.md)

---

## What Are We Building?

The Product domain is the heart of the Spark platform — it connects business partners, teams, workspaces, attachments, samples, BOMs, measurements, claims, and rules into a single product-development view. This migration moves Product from the centralized **Node.js spark-internal-graphql gateway** to a dedicated **Kotlin / Netflix DGS** service called **`plm-product`**.

This is the **single largest domain** in the system:
- 800-line GraphQL schema
- 2,629-line resolver file
- 589-line service class (42 REST methods)
- 16 utility modules
- 29 distinct external service dependencies

Because Product is so central, this migration unlocks downstream work for 15+ sibling domains (BOM, claim, measurement, sample, attachment, etc.) and clears the way for Hive Gateway federation across the platform.

---

## Migration Scope

| Surface | Count | Status |
|---|---|---|
| Queries | 18 | 🔜 all to build |
| Mutations | 22 implemented + 3 schema-drift wrappers | 🔜 / ⏭ (3 deferred for delete-vs-deprecate decision) |
| Field resolvers | ~61 across 16 GraphQL types | 🔜 all to build |
| TechPack cross-domain sub-stories | 8 placeholders | One per owning subgraph; full stories written in each domain's file |
| External service dependencies | 29 | 11 platform (🔵 stay stitched), 18 critical / important |
| Hardcoded "must-be-removed" status tables | 3 | Cleanup during port |
| Latent bugs flagged for fix-during-port | 4 | `division` resolver, M17 shadow var, `incrementAllContextCounter`, M18 inverted logic (Phase 2B) |

This is a **green-field** migration — no existing DGS code to inherit.

> **TechPack note:** `getProductTechPackCountV1` and `getProductTechPackBulkCountV1` return a `ResourcesCount` composite-key entity whose 10 fields are owned by **8 different subgraphs** (Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist). Product owns only the query stub and type definition. **Option D (facade now → federate per-subgraph as each domain comes online)** is recommended — see [techpack-migration-options.md](fedMigrationScripts/reference/techpack-migration-options.md).

---

## Story Summary by Phase

| Phase | Description | Stories | Raw days | +20% buffer |
|---|---|---|---|---|
| A | Foundation & Schema | 7 | 14–22 | 17–27 |
| B | Core CRUD Queries (6 simple) | 6 | 7–13 | 9–16 |
| C | Search & Listing | 4 | 14–24 | 17–29 |
| D | Core Mutations (9) | 9 | 16–28 | 20–34 |
| E | Complex Mutations + TechPack stub + facade | 6 | 27–46 | 33–56 |
| F | Federation / Stitching (incl. 8 TechPack placeholders) | 13 | 22–39 | 27–47 |
| G | Field Resolvers (3 X-Large + 11 others) | 14 | 71–119 | 86–143 |
| H | Services + Utils + cleanup | 6 | 18–30 | 22–36 |
| I | Test Coverage (parity / load / contract / cutover) | 5 | 16–24 | 20–29 |
| **Total** | | **70** | **205–345** | **246–414** |

> One engineer ≈ **49–83 sprints** (5d/sprint). Phases B/C/D/F-placeholders/G are highly parallelizable.

---

## Key Risk Areas

| Risk | Severity | Story |
|---|---|---|
| `productBusinessPartnerActions` partial-failure rollback strategy | 🔴 Critical | SPARK-PROD-E01 |
| TechPack 8-subgraph sub-story coordination across 8 domain teams | 🔴 Critical | SPARK-PROD-F01–F08 |
| `attachmentsWithMetaData` — 150-line, multi-source merge + 2× ACL JWT | 🔴 Critical | SPARK-PROD-G01 |
| `components` — 190-line, 4 parallel elastic + N+1 ACL refactor | 🔴 Critical | SPARK-PROD-G02 |
| `updateComponentStatuses` 5-loader fan-out + shadow-var bug | 🟡 High | SPARK-PROD-E02 |
| `division` field resolver BUG (calls department loader) | 🟡 High | SPARK-PROD-G12 |
| `USE_NEW_RULES_API` legacy deletion needs all-env confirmation | 🟡 High | SPARK-PROD-H06 |
| Schema-drift mutations (M21–M23) may have live consumers | 🟡 High | SPARK-PROD-F13 |
| Aggregation facade becoming permanent if F01–F08 stall | 🟡 High | SPARK-PROD-F09 |
| `samples` resolver reads `info.variableValues` — fragile contract | 🟡 High | SPARK-PROD-G05 |
| Green-field: no DGS to validate naming against | 🟡 High | SPARK-PROD-A01 |

---

## Decisions Required from PO / Architecture

| # | Decision | Due Before | Impact |
|---|---|---|---|
| 1 | Confirm TechPack approach is **Option D** (facade now, federate per-subgraph). See [techpack-migration-options.md](fedMigrationScripts/reference/techpack-migration-options.md). | E kickoff | E05 design; blocks F01–F08 |
| 2 | Rollback strategy for `productBusinessPartnerActions` (saga vs best-effort log) | E kickoff | E01 design |
| 3 | Delete or `@deprecated`-keep the 3 schema-drift mutations (M21–M23)? Survey current traffic first. | F kickoff | F13 |
| 4 | Is `USE_NEW_RULES_API` `true` in **all** environments? Can the legacy branch be deleted? | F kickoff | H06; Q15/Q16/Q17 fate |
| 5 | Should the `division` resolver bug fix be feature-flagged during cutover? Survey clients first. | G kickoff | G12 |
| 6 | Where does the `spark_rules` service live in DGS — co-located in `plm-product` or its own subgraph? | A kickoff | A06 service split |
| 7 | Which 8 domain teams own the per-subgraph CAT-4 stories (Attachment, Discussion, Sample, Measurement, Claims, BOM, Construction, Watchlist)? Each needs a migration sprint slot. | F planning | F01–F08 |
| 8 | Hive Gateway federation v2.3 — confirmed supported? | F kickoff | All federation stories |
| 9 | Source bug-fix policy: fix in DGS only, or back-port to source first? Applies to `division`, M17 shadow var, M18 inversion, `incrementAllContextCounter`. | A kickoff | G12, E02, multiple |
| 10 | `samples` field-resolver contract change (stop reading `info.variableValues`) — communicate to clients in advance? | G kickoff | G05 |

---

## Dependency Map

```
plm-product depends on:
  spark-product backend                  (primary REST API for Product + spark_rules)
  spark-product search (Elasticsearch)   (product listing, categories facets)
  spark-attachment                       (bulk update, archive, relationship-linked)
  spark-relationship                     (resource tree traversal)
  spark-access-control                   (ACL JWT, permissions, drop/undrop)
  spark-sample-v2                        (drop/undrop, hydrate samples)
  spark-claim                            (claims listing + status updates)
  spark-bom                              (BOM listing + types)
  spark-measurement                      (measurement set listing)
  spark-packaging                        (packaging listing + field values)
  spark-product-detail                   (productDetail listing)
  spark-discussion                       (discussions + threads + replies)
  spark-tag                              (tags + categories)
  spark-workspace-v2                     (workspace membership + dates)
  spark-team-v2                          (teams for product)
  spark-user-profile                     (createdBy/updatedBy)
  spark-product-ask                      (associate-product-asks)
  spark-product-variation                (variations)
  spark-file-library                     (SPG file library for packaging)
  Hive Gateway → VMM                     (VMM_BusinessPartner, VMM_Brand stubs)
  Hive Gateway → IG                      (IG_Department, IG_Division, IG_Clazz)
  Hive Gateway → Doppler                 (capacity types)
  Hive Gateway → Corona                  (TCIN item details)
  Hive Gateway → APEX                    (reserved DPCIs)
  Hive Gateway → Brand Compliance        (compliance records)
  External → Bazaarvoice / Rating        (product ratings)
```

---

## Recommended Sprint Sequencing

| Sprint | Phases | Focus |
|---|---|---|
| S1 | A01–A07 | Schema skeleton, owned types, external stubs, Categories union, `ResourcesCount @key`, ProductService Kotlin port, ACL JWT plumbing |
| S2 | B01–B06 + D05–D09 | Simple queries + thin mutation wrappers (highly parallel; 2 engineers ideal) |
| S3 | C01–C04 + D01–D04 | Search/listing + core mutations |
| S4 | E01 | `productBusinessPartnerActions` — concentrated focus |
| S5 | E02–E04 + E05 | `updateComponentStatuses`, `updateComponentStatus`, `carryForwardProduct`, TechPack stub + facade (Day-1 working `getProductTechPackCountV1`) |
| S6 | E06 + F10–F13 | TechPack bulk + Hive Gateway composition + drift-mutation decision |
| S7 | G01 | `attachmentsWithMetaData` (X-Large) — concentrated focus |
| S8 | G02 | `components` (X-Large) — concentrated focus |
| S9 | G03–G07 | Attachments cluster, categories+Doppler, samples, teams/discussions, partners |
| S10 | G08–G14 + H05 + H06 | Remaining field resolvers + status-enum cleanup + USE_NEW_RULES_API delete |
| S11 | H01–H04 | Util/service ports (attachmentUtils, vmm, accessControl, partner/team/product utils) |
| S12 | I01–I04 | Unit + integration + parity + load + contract tests |
| S13 | I05 | Cut-over rehearsal + shadow traffic |
| Ongoing | F01–F08 + F09 | TechPack subgraph stories — each unblocked when owning domain migrates; F09 retires facade when all 8 are live |

---

## Capacity Planning

| Team size | Calendar (5d sprints) | Notes |
|---|---|---|
| 1 engineer | ~49–83 sprints | Sequential; no parallelism |
| 2 engineers | ~26–42 sprints | B/C/D parallelizable; G has internal parallelism |
| 3 engineers | ~18–28 sprints | Critical path = A → E05 → G01 → G02 → I05 |
| 4 engineers | ~14–22 sprints | Diminishing returns past 4 — A and I are not parallelizable |

> Phase G (Field Resolvers, 86–143 buffered days) is the **critical-path bottleneck** because of G01 + G02. Either staff these two X-Large stories with senior engineers concurrently or accept they will dominate calendar time.

---

## Cross-Domain Coordination

Because of the 8 TechPack CAT-4 placeholder stories, this migration **cannot be fully retired** until 8 sibling domains have completed their own Phase 3 + Phase F. Recommendation:

1. **Ship Option D Phase 1 (E05 + E06) early** to unblock product traffic to plm-product.
2. **Run the facade indefinitely** until all 8 owning domains have migrated.
3. **Track aggregation-facade retirement (F09)** as an epic-level success metric — it is the signal that the federation graph is fully native.

---

## Phase 2 Estimate Reconciliation

Phase 2 (Resolvers + Services + Utils) totalled **267–463 raw days / 320–555 buffered** (see [02-resolver-analysis-services.md §D5](output/product/02-resolver-analysis-services.md)). The story-level total here (**205–345 raw / 246–414 buffered**) is **lower** because:

1. `ProductService` REST methods (42) collapse into internal Kotlin calls in plm-product — no new HTTP layer (~30 days saved)
2. Shared utility modules (`discussionUtils`, parts of `commonLoaders`) are owned by sibling subgraphs and tracked in their files (~20 days)
3. Some Phase 2C/2D items are bundled into related field-resolver stories vs counted as separate items (~10 days)

This is consistent with the framework's guidance that Phase 2 estimates the *full implementation surface* while Phase 4 estimates only the *new work for this domain*.

---

*Generated by spark-migration pipeline v1.1 — Phase 4 complete. All 6 artifacts ready under `output/product/`.*
