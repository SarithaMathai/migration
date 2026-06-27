# Packaging — Migration to the `plm-product` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../packaging/03-schema-analysis.md) ·
> [field inventory](../packaging/05-attribute-inventory.md) · [engineering stories](../packaging/04-stories.md).
> Create tickets from [`../jira/packaging.csv`](../jira/packaging.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Packaging** domain — packaging records, their dielines (print-artwork specs), printers,
elements, and exports — off the `spark-internal-graphql` gateway into the **`plm-product`** DGS. It is
**mid-sized with a wide schema** (24 object types, 20 inputs): 7 queries, 10 mutations, 17 field resolvers
on a 273-line resolver, but **no polymorphism**.

Two pieces carry the real work: **`updatePackaging`**, a multi-step write (body, then attachment remove via
archive + relationship, then attachment add via relationship + attribute update) with no rollback; and
**`suggestedRetailPriceByDPCI`**, a multi-hop pricing field (printers → dielines → DPCIs → pricing service).

**ACL note:** the current code obtains per-resource capability tokens via ACL; **ACL is ignored in the DGS
implementation** (no ACL story) — noted for context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 10 | 9 simple + `updatePackaging` (multi-step) |
| Field-resolver type blocks | 4 | `Packaging` (12), `Dieline` (3), `PrinterDieline` (1), `PackagingElement` (1) |
| External dependencies | 7 keys (2 🔴 · 3 🟡 · 2 🔵) | search/attachment 🔴; relationship/user-profile/tag 🟡 |
| Federation contributions | 1 (Product) | **internal** (co-located) |
| **Total stories** | **28** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 9–15d |
| B | Core Reads | 6 | 6–11d |
| C | Search & Listing | 1 | 2–4d |
| D | Mutations (simple) | 9 | 13–22d |
| E | Complex (`updatePackaging`) | 1 | 5–8d |
| F | Federation (Product, internal) | 1 | 1–2d |
| G | Field Resolvers & Tests | 6 | 15–25d |
| **Total** | | **28** | **51–87d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| `updatePackaging` multi-step write | 🟡 Medium-High | Needs a decision (E01); add/remove error handling is inconsistent today |
| `suggestedRetailPriceByDPCI` multi-hop pricing | 🟡 Medium | Performance-sensitive; cache/batch the dieline→DPCI→price chain |
| `updatePackagingComponentStatus` has no auth token | 🟢 Low | Confirm the backend enforces it |
| Attachment-by-search field resolvers | 🟢 Low | Shared search helper; batch |
| Claims pass-through fields on `PackagingInput` | 🟢 Low | Confirm ownership (packaging vs claims subgraph) |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `updatePackaging` failure strategy + align add/remove error handling | E01 | Tech Lead + PO |
| 2 | `suggestedRetailPriceByDPCI` — cache the dieline→DPCI→pricing chain? | G04 | Backend Eng |
| 3 | `updatePackagingComponentStatus` no token — backend-enforced? | D09 | PO |
| 4 | Claims pass-through (`claimId`/`claimDetails`) — keep on packaging or route to claims? | A02 | Architect |

## Migration approach (summary)

Phase **A** schema (~24 types, ~20 inputs) + `PackagingService` port; **B** the 6 simple reads (2 cacheable);
**C** elastic search; **D** the 9 simple mutations; **E** the multi-step `updatePackaging`; **F** Product
packaging links (internal); **G** field resolvers incl. the `suggestedRetailPriceByDPCI` pricing chain and
the dieline/printer/element resolvers + tests. Full detail:
[03-schema-analysis.md §Migration Approach](../packaging/03-schema-analysis.md).

## Sequencing & capacity

One engineer ≈ 10–17 sprints; 3 engineers ≈ 4–7 (critical path A → E01 → G04 → G06). Phase G + the wide
schema (A02) dominate. Full plan: [04-po-summary.md](../packaging/04-po-summary.md).

---
*PO page assembled from the packaging analysis. Tickets:
[`../jira/packaging.csv`](../jira/packaging.csv) · [`../jira/packaging-stories.md`](../jira/packaging-stories.md).*
