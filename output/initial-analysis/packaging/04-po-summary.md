# Phase 4: PO Sprint Planning Summary — Packaging

> **Domain:** `packaging` · **Target DGS:** `plm-product` · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

- We are moving the **Packaging** domain — packaging records, their dielines (print artwork specs), printers, elements, and exports — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS.
- It is
**mid-sized with a wide schema** (24 object types, 20 inputs): 7 queries, 10 mutations, 17 field resolvers
on a 273-line resolver, but **no polymorphism**.

Two pieces carry the real work: **`updatePackaging`**, a multi-step write (body, then attachment
remove via archive + relationship, then attachment add via relationship + attribute update) with no
rollback; and **`suggestedRetailPriceByDPCI`**, a multi-hop pricing field (printers → dielines → DPCIs →
pricing service).

**ACL note:** the current code obtains per-resource capability tokens via ACL; Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs (`complexStories/*/02-adr-noacl-*.md`) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 10 | 9 simple + `updatePackaging` (multi-step) |
| Field-resolver type blocks | 4 | `Packaging` (12), `Dieline` (3), `PrinterDieline` (1), `PackagingElement` (1) |
| External dependencies | 7 keys (2 🔴 · 3 🟡 · 2 🔵) | search/attachment 🔴; relationship/user-profile/tag 🟡 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **24** | green-field |

## Story Summary by Phase (AI-estimated)
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

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B-01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updatePackaging` multi-step write | 🟡 Medium-High | Needs a decision (E-01) on mid-write failure; add/remove error handling is inconsistent today |
| `suggestedRetailPriceByDPCI` multi-hop pricing | 🟡 Medium | Performance-sensitive; cache/batch the dieline→DPCI→price chain |
| `updatePackagingComponentStatus` has no auth token | 🟢 Low | Confirm the backend enforces it |
| Attachment-by-search field resolvers | 🟢 Low | Shared search helper; batch |
| Claims pass-through fields on `PackagingInput` | 🟢 Low | Confirm ownership (packaging vs claims subgraph) |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updatePackaging` failure strategy + align add/remove error handling | E-01 | Tech Lead + PO |
| 2 | `suggestedRetailPriceByDPCI` — cache the dieline→DPCI→pricing chain? | G-04 | Backend Eng |
| 3 | `updatePackagingComponentStatus` no token — backend-enforced? | D-09 | PO |
| 4 | Claims pass-through (`claimId`/`claimDetails`) — keep on packaging or route to claims? | B-01 | Product Owner |

## Dependency Map
```
plm-product (Packaging subgraph) depends on:
 spark-product backend REST .../packaging/v1 + dielines + export
 sibling DGS (federation): attachment, search 🔴, workspace, user-profile, relationship, tag
 Hive Gateway → VMM (business partners), apex/pricing (suggested retail price)
 internal (same DGS): product, fileLibrary
 product domain F-01 Product packaging links (internal field resolvers)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, core reads |
| 2 | B-04–B-06 + C-01 + D-02/D-05–D-07 | master-data + search + simple mutations |
| 3 | D-01/D-03/D-04/D-08/D-09 | create/bulk/clone/component-status |
| 4 | E-01 + F-01 | multi-step update + Product links |
| 5 | G-01–G-03 | ACL/users/refs field resolvers |
| 6 | G-04/G-05 + G-06 | pricing + dieline resolvers + tests |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~10–17 sprints | sequential |
| 2 engineers | ~6–10 sprints | reads + mutations parallel after B-01 |
| 3 engineers | ~4–7 sprints | critical path A → E-01 → G-04 → G-06 |

---
*Pipeline 2.0 — Phase 4 complete. Packaging artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*
