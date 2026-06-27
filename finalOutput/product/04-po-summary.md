# Phase 4: PO Sprint Planning Summary — Product

> **Domain:** `product` · **Target DGS:** `plm-product` (host DGS) · **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Stories:** [04-stories.md](./04-stories.md) · **Index:** [04-stories-index.yaml](./04-stories-index.yaml)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

We are moving **Product** — the central entity of the PLM system — off the `spark-internal-graphql` gateway
into the **`plm-product`** Netflix DGS. Product is the **largest and highest-risk** domain (18 queries, 20
mutations, ~50 field resolvers on a 2,629-line resolver) and the **host service** for the whole product
family: BOM, Measurement, Impression, Packaging and others live in the same DGS, so their links from Product
resolve **internally** rather than across the federation gateway.

Most of the work is mechanical (the long tail of CRUD and simple field resolvers), but a handful of items
carry real risk: the **TechPack count** query (a 17-step aggregation across 9+ services that becomes a
federated composite-key entity), the **partner drop/undrop** orchestration, the cross-domain **components**
and **attachmentsWithMetaData** field resolvers, and a **latent `division` bug**. We recommend the **Option D**
approach for TechPack: ship a thin query over a temporary aggregation facade so it works on day 1, then
federate each piece to its owning domain, then retire the facade.

**ACL note:** the source obtains per-resource capability tokens via ACL on nearly every call; **ACL is
ignored in the DGS implementation** (no ACL story) — noted for context only.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 18 | incl. TechPack (Very High) and two-stage `getProducts` |
| Mutations | 20 (+3 deferred) | incl. partner actions + component fan-out |
| Field-resolver stories | ~16 | incl. 2 X-Large (attachmentsWithMetaData, components) |
| External dependencies | 12 EXT + 6 platform | search/attachment/workspace 🔴 |
| Composite-key aggregate | 1 (TechPack `ResourcesCount`) | 8 sibling subgraphs extend it |
| Federation contributions received | 8 | from sibling domains (Phase F placeholders) |
| **Total stories** | **72** | green-field |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| A | Foundation & Schema | 6 | 17–27d |
| B | Core Reads | 11 | 11–18d |
| C | Search & Listing | 5 | 17–29d |
| D | Mutations (simple) | 18 | 25–40d |
| E | Complex (partner/components/TechPack) | 4 | 33–56d |
| F | Federation & Stitching | 12 | 22–40d (most BLOCKED-BY siblings) |
| G | Field Resolvers, Bug-fixes, Utils, Tests | 16 | 86–143d |
| **Total** | | **72** | **211–353d** (buffered) |

> One engineer ≈ **42–71 sprints**. Heavily parallelizable after A; 2–3 engineers strongly recommended.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| TechPack aggregation (E03/E04) | 🔴 High | Biggest single cost; use the facade so it works on day 1, federate later |
| Partner drop/undrop (E01) | 🔴 High | Needs a decision on recovering from a mid-orchestration failure |
| `components` / `attachmentsWithMetaData` (G01/G02) | 🟡 Medium-High | Large, performance-sensitive; budget X-Large |
| `division` latent bug (G12) | 🟡 Medium | Fixing it changes the response shape — may need a cutover flag |
| 8 TechPack placeholders block on 8 domains | 🟡 Medium | Facade keeps it working; retire only when all siblings are live |
| Rules feature-flag + external rating secret | 🟢 Low | Verify flag everywhere; move the rating key to Vault |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | TechPack facade: Node extract vs Kotlin aggregation | E03 | Tech Lead + Architect |
| 2 | `productBusinessPartnerActions` failure strategy | E01 | Tech Lead + PO |
| 3 | Delete or `@deprecated` the 3 drift partner wrappers | F12 | PO |
| 4 | `USE_NEW_RULES_API` cutover (rules may move to spark-tag DGS) | B10/B11/C05 | Architect |
| 5 | `Product.division` bug fix — feature-flag during cutover? | G12 | PO |
| 6 | `components` ACL batching approach | G02 | Backend Eng |

## Dependency Map
```
plm-product (Product subgraph, the host DGS) depends on:
  spark-product backend   REST v1/v2 + elastic + spark_rules + external rating
  EXT (federation): attachment, workspace, discussion, sample, tag, team, user-profile, relationship, claim
  Platform (gateway): VMM, IG, Doppler, CORONA, APEX, Brand Compliance
  Internal (same DGS): bom, measurement, impression, packaging, productDetails, productAsk, productVariation, fileLibrary
  Sibling domains → contribute 8 ResourcesCount field sets (TechPack federation, Phase F)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | A01–A06 | schema, types, stubs, Categories resolver, ResourcesCount, service port |
| 3 | B01–B11 | all core reads (incl. rules reads) |
| 4 | C01–C05 | search/listing + rating + rules search |
| 5–6 | D01–D18 | all simple mutations (parallelizable) |
| 7–8 | E03/E04 | TechPack facade + bulk (focused) |
| 9 | E01/E02 | partner actions + component fan-out |
| 10–12 | G01–G14 | field resolvers (G01/G02 X-Large get their own sprint) |
| 13 | G15 + G16 | utils port + tests/parity/load/cut-over |
| post-launch | F01–F09 | TechPack federation (unblocked as siblings migrate) + facade retirement |
| any | F10–F12 | gateway composition + platform verify + drift decision |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~42–71 sprints | sequential — not recommended for this domain |
| 2 engineers | ~25–42 sprints | B/C/D parallel after A |
| 3–4 engineers | ~18–28 sprints | A done → B + C + D + most of G in parallel; E and the two X-Large fields on dedicated owners |

> Phase G dominates the calendar; the two X-Large field resolvers (`attachmentsWithMetaData`, `components`)
> and TechPack (E03/E04) are the cost-and-risk centre of the whole program.

---
*Pipeline 2.0 — Phase 4 complete. Product artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files).*
