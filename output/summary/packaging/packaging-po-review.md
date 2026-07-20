# Packaging — Migration to the `plm-product` DGS (PO view)

> 🏷️ **Tags:** `dgs-migration` · `po-page` · `domain-packaging` · `pipeline-v2`  —  **Confluence location:** *Federation Graph Migration ▸ Domains ▸ packaging*

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.  
> Deep dives: migration approach & schema · field inventory · engineering stories.  
> Create tickets from `../finalOutput/jira/packaging.csv`. Effort is **AI-estimated — confirm in refinement.**

---

## What are we building?

- We are moving the **Packaging** domain — packaging records, their dielines (print artwork specs), printers, elements, and exports — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is
**mid-sized with a wide schema** (24 object types, 20 inputs): 7 queries, 10 mutations, 17 field resolvers
on a 273-line resolver, but **no polymorphism**.

Two pieces carry the real work: **`updatePackaging`**, a multi-step write (body, then attachment
remove via archive + relationship, then attachment add via relationship + attribute update) with no
rollback; and **`suggestedRetailPriceByDPCI`**, a multi-hop pricing field (printers → dielines → DPCIs →
pricing service).

**ACL note:** the current code obtains per-resource capability tokens via ACL. Per **ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites (e.g. the attachment-archive steps in `updatePackaging`) use **Mid-Request ACL Update** before the downstream call.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 10 | 9 simple + `updatePackaging` (multi-step) |
| Field-resolver type blocks | 4 | `Packaging` (12), `Dieline` (3), `PrinterDieline` (1), `PackagingElement` (1) |
| External dependencies | 7 keys (2 🔴 · 3 🟡 · 2 🔵) | search/attachment 🔴; relationship/user-profile/tag 🟡 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **24** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 6 | 6–11d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 9 | 13–22d |
| E | Complex (`updatePackaging`) | 1 | 5–8d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 6 | 15–25d |
| **Total** | | **24** | **42–72d** (buffered) |

> One engineer ≈ **9–15 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updatePackaging` failure strategy + align add/remove error handling | E-01 | Tech Lead + PO |
| 2 | `suggestedRetailPriceByDPCI` — cache the dieline→DPCI→pricing chain? | G-04 | Backend Eng |
| 3 | `updatePackagingComponentStatus` no token — backend-enforced? | D-09 | PO |
| 4 | Claims pass-through (`claimId`/`claimDetails`) — keep on packaging or route to claims? | B-01 | Product Owner |

## Migration approach (summary)

**B** Core Reads; **C** Search & Listing; **D** Mutations (simple); **E** Complex (`updatePackaging`); **F** Federation (Product, internal); **G** Field Resolvers & Tests. Full detail: `be-03-schema-analysis.md §Migration Approach`.

## Sequencing & capacity

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~10–17 sprints | sequential |
| 2 engineers | ~6–10 sprints | reads + mutations parallel after B-01 |
| 3 engineers | ~4–7 sprints | critical path A → E-01 → G-04 → G-05 |

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, core reads |
| 2 | B-04–B-06 + C-01 + D-02/D-05–D-07 | master-data + search + simple mutations |
| 3 | D-01/D-03/D-04/D-08/D-09 | create/bulk/clone/component-status |
| 4 | E-01 + F-01 | multi-step update + Product links |
| 5 | G-01–G-03 | ACL/users/refs field resolvers |
| 6 | G-04/G-05 | pricing + dieline resolvers. Test coverage/parity tracked outside this Jira pipeline, created manually. |

## Phase 2 Story Breakdowns

One story in this domain was broken into **M-size (≤5 day) sub-tasks** in Jira.

| Parent milestone | Original size | Sub-tasks |
|---|---|---|
| `PKG-BE-E-01` updatePackaging (body + attachment add/remove, branching) | High | E-01-1 body + attachment add · E-01-2 attachment remove + pricing |

> In Jira, sub-tasks appear **nested under** their parent story. Sprint capacity: each sub-task = M (3–5 days).

---
*PO review assembled from the `packaging` analysis. Jira tickets: `finalOutput/jira/packaging.csv`. Full engineering detail: `packaging-comprehensive.md` (same folder).*