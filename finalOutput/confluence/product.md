# Product — Migration to the `plm-product` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../product/03-schema-analysis.md) ·
> [field inventory](../product/05-attribute-inventory.md) · [engineering stories](../product/04-stories.md).
> Create tickets from [`../jira/product.csv`](../jira/product.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving **Product** — the central entity of the PLM system — off the `spark-internal-graphql`
gateway into the **`plm-product`** DGS. Product is the **largest and highest-risk** domain (18 queries,
20 mutations, ~50 field resolvers on a 2,629-line resolver) and the **host service** for the whole product
family: BOM, Measurement, Impression and others live in the same DGS, so their links from Product resolve
**internally** rather than across the federation gateway.

Most of the work is mechanical CRUD and simple field resolvers, but a handful carry real risk: the
**TechPack count** query (a 17-step aggregation that becomes a federated composite-key entity), the
**partner drop/undrop** orchestration, the cross-domain **components** and **attachmentsWithMetaData**
field resolvers, and a **latent `division` bug**. For TechPack we recommend **Option D**: ship a thin query
over a temporary aggregation facade so it works on day 1, then federate each piece, then retire the facade.

**ACL note:** the source obtains per-resource capability tokens via ACL on nearly every call; **ACL is
ignored in the DGS implementation** (no ACL story) — noted for context only.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 18 | incl. TechPack (Very High) and two-stage `getProducts` |
| Mutations | 20 (+3 deferred) | incl. partner actions + component fan-out |
| Field-resolver stories | ~16 | incl. 2 X-Large (`attachmentsWithMetaData`, `components`) |
| External dependencies | 12 EXT + 6 platform | search / attachment / workspace 🔴 |
| Composite-key aggregate | 1 (TechPack `ResourcesCount`) | 8 sibling subgraphs extend it |
| **Total stories** | **72** | green-field |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 6 | 17–27d |
| B | Core Reads | 11 | 11–18d |
| C | Search & Listing | 5 | 17–29d |
| D | Mutations (simple) | 18 | 25–40d |
| E | Complex (partner / components / TechPack) | 4 | 33–56d |
| F | Federation & Stitching | 12 | 22–40d (most BLOCKED-BY siblings) |
| G | Field Resolvers, Bug-fixes, Utils, Tests | 16 | 86–143d |
| **Total** | | **72** | **211–353d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| TechPack aggregation (E03/E04) | 🔴 High | Biggest single cost; use the facade so it works day 1, federate later |
| Partner drop/undrop (E01) | 🔴 High | Needs a decision on recovering from a mid-orchestration failure |
| `components` / `attachmentsWithMetaData` (G01/G02) | 🟡 Medium-High | Large, performance-sensitive; budget X-Large |
| `division` latent bug (G12) | 🟡 Medium | Fixing it changes the response shape — may need a cutover flag |
| 8 TechPack placeholders block on 8 domains | 🟡 Medium | Facade keeps it working; retire only when all siblings are live |
| Rules feature-flag + external rating secret | 🟢 Low | Verify flag everywhere; move the rating key to Vault |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | TechPack facade: Node extract vs Kotlin aggregation | E03 | Tech Lead + Architect |
| 2 | `productBusinessPartnerActions` failure strategy | E01 | Tech Lead + PO |
| 3 | Delete or `@deprecated` the 3 drift partner wrappers | F12 | PO |
| 4 | `USE_NEW_RULES_API` cutover (rules may move to spark-tag DGS) | B10/B11/C05 | Architect |
| 5 | `Product.division` bug fix — feature-flag during cutover? | G12 | PO |
| 6 | `components` ACL batching approach | G02 | Backend Eng |

## Migration approach (summary)

Phase **A** lays the schema + `ProductService` Kotlin port; **B/C** the reads; **D** the simple mutations;
**E** the hard ones (partner actions, component fan-out, TechPack facade); **F** federates the TechPack
`ResourcesCount` fields + gateway composition; **G** the ~16 field-resolver stories (incl. the two X-Large)
and the `division` bug fix. Co-located siblings (bom/measurement/impression/…) resolve **internally**.
Full detail: [03-schema-analysis.md §Migration Approach](../product/03-schema-analysis.md).

## Field-inventory signal

Product is **wide and deep** (~90 fields on `Product`). The bulk are direct pass-throughs (cheap), but the
long tail of **~30 EXT field resolvers**, the **two X-Large** (`attachmentsWithMetaData`, `components`), and
the **TechPack composite-key aggregate** are where cost and risk concentrate. Detail:
[05-attribute-inventory.md](../product/05-attribute-inventory.md).

## Sequencing & capacity

Parallelizable after Phase A; **2–3 engineers strongly recommended** (~18–28 sprints for 3–4 engineers vs
~42–71 for one). Phase G dominates the calendar. Post-launch: F01–F09 TechPack federation unblocks as each
sibling migrates. Full sprint plan: [04-po-summary.md](../product/04-po-summary.md).

---
*PO page assembled from the product analysis. Tickets: [`../jira/product.csv`](../jira/product.csv) ·
[`../jira/product-stories.md`](../jira/product-stories.md).*
