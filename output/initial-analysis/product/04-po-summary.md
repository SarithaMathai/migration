# Phase 4: PO Sprint Planning Summary — Product

> **Domain:** `product` · **Target DGS:** `plm-product` (host DGS) · **Generated:** 2026-06-26
> **Stories:** [04-stories.md](./04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

- We are moving **Product** — the central entity of the PLM system — off the `spark-internal-graphql` gateway into the **`plm-product`** Netflix DGS.
- Product is the **largest and highest-risk** domain (18 queries, 20 mutations, ~50 field resolvers on a 2,629-line resolver) and the **host service** for the whole product family: BOM, Measurement, Impression, Packaging and others live in the same DGS, so their links from Product resolve **internally** rather than across the federation gateway.

- Most of the work is mechanical (the long tail of CRUD and simple field resolvers), but a handful of items carry real risk: the **TechPack count** query (a 17-step aggregation across 9+ services that becomes a federated composite-key entity), the **partner drop/undrop** orchestration, the cross-domain **components** and **attachmentsWithMetaData** field resolvers, and a **latent `division` bug**.
- We recommend the **Option D** approach for TechPack: ship a thin query over a temporary aggregation facade so it works on day 1, then federate each piece to its owning domain, then retire the facade.

**ACL note:** the source obtains per-resource capability tokens via ACL on nearly every call; **ACL is
ignored in the DGS implementation** (no ACL story) — noted for context only.

## Deployment model — ship on green, per story

- Every story is **end-to-end in one PR** and **independently deployable to production once its own tests and parity pass** — no waiting for the rest of the phase.
- The **one exception** is a story whose field is produced by **composing another subgraph's data** (a cross-subgraph **entity extension**, `extend type … @key` resolved by a different DGS): those go live only once the **owning subgraph is deployed**, and are marked
**BLOCKED-BY `<domain>`**.

- ✅ **Ships on green** — all B/C/D/E/G stories, the internal Phase-F contributions (`F04`, `F06`, `F08`), the
  gateway/platform stories (`F10`, `F11`), and the **TechPack facade** (`E03`/`E04`), which is *designed* to
  work day 1 before any sibling federates.
- ⛔ **Waits for an owning subgraph (the exception)** — the true cross-subgraph federation stories
  **`F01` (attachment), `F02` (discussion), `F03` (sample), `F05` (claim), `F07` (construction)**, plus
  **`F09`** (facade retirement, which needs all 8 contributions live). These are the only stories held back
  from per-story prod release.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 18 | incl. TechPack (Very High) and two-stage `getProducts` |
| Mutations | 20 (+3 deferred) | incl. partner actions + component fan-out |
| Field-resolver stories | ~16 | incl. 2 X-Large (attachmentsWithMetaData, components) |
| External dependencies | 12 EXT + 6 platform | search/attachment/workspace 🔴 |
| Composite-key aggregate | 1 (TechPack `ResourcesCount`) | 8 sibling subgraphs extend it |
| Federation contributions received | 8 | from sibling domains (Phase F placeholders) |
| **Total stories** | **67** | green-field build stories (3 complex problems centralized as program spikes; `G11` split into `G11-1`/`G11-2` = +1) |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) | Ready when |
|---|---|---|---|---|
| B | Core Reads | 11 | 11–18d | after B01 |
| C | Search & Listing | 5 | 17–29d | after B01; C01 gated on `SPARK-SPIKE-06a` (Hydration, via `SPARK-PROD-S02`) |
| D | Mutations (simple) | 18 | 25–40d | after B01; D01-D04/D06/D07/D11 gated on `SPARK-SPIKE-06b` (Association, via `SPARK-PROD-S01`) |
| E | Complex (partner/components/TechPack) | 4 | 33–56d | E01 gated on `SPARK-SPIKE-03` |
| F | Federation & Stitching | 12 | 22–40d (most BLOCKED-BY siblings) | after E03 / siblings |
| G | Field Resolvers, Bug-fixes, Utils, Tests | 17 | 86–143d | after B01. `G11` split into `G11-1`/`G11-2` (16 → 17) |
| **Total** | | **67** | **203–348d** (buffered) | |

> One engineer ≈ **40–66 sprints**. Heavily parallelizable after B01; 2–3 engineers strongly recommended.

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories; the `Categories` union `@DgsTypeResolver` remains a dedicated story.

> **Thin DGS wrappers — parallel after B01.** The model, REST controller (GET/POST/PUT) and service already exist; each story only adds the Netflix-DGS layer so the federated graph can stitch this subgraph. The **one-time DGS module scaffold** B01 lands (schema file + scalar registration + service/Feign wiring) is a prerequisite for every operation story, so it is **assumed — not repeated in each story's `Depends On`** (rows list only genuine story-to-story dependencies). E.g. `D08 removeProductResources` is a one-line wrapper over the existing REST `DELETE`/`PUT`, so its `Depends On` is **—**. After B01, phases B/C/D/G run fully in parallel.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| TechPack aggregation (E03/E04) | 🔴 High | Biggest single cost; facade-then-federate already decided (spike completed) — use it so it works on day 1 |
| Partner drop/undrop (E01) | 🔴 High | `S03` spike (run first) picks the recovery strategy before `E01` starts |
| `getProducts` two-stage hydration (C01) | 🟡 Medium-High | `S02` spike resolves workspace-filter placement + elastic/canonical staleness before `C01` starts |
| Cross-domain association pattern (D01-D04, D06/D07/D11) | 🟡 Medium | `S01` spike picks one pattern so 7 mutations stop each inventing their own |
| `components` / `attachmentsWithMetaData` (G01/G02) | 🟡 Medium-High | Large, performance-sensitive; budget X-Large |
| `division` latent bug (G12) | 🟡 Medium | Fixing it changes the response shape — client survey before rollout |
| 8 TechPack placeholders block on 8 domains | 🟡 Medium | Facade keeps it working; retire only when all siblings are live |
| Rules feature-flag + external rating secret | 🟢 Low | Verify flag everywhere; move the rating key to Vault |

## Decisions Required

> Reviewed and updated. Open items needing real research are now **Phase 0 spike stories** — see
> *Phase 0 — Spikes* in [`04-stories.md`](./04-stories.md) for the full write-up of each.

| # | Decision | Status | Detail |
|---|---|---|---|
| 1 | TechPack facade: Node extract vs Kotlin aggregation | ✅ Resolved — Option D Phase 1 | Facade now, federate per-domain later, retire facade (`F09`). See `E03`'s note + `complexStories/techpack/`. |
| 2 | `productBusinessPartnerActions` failure strategy | 🔬 **Spike** `SPARK-PROD-S03` (run first) | Blocks `E01`. Prior art: `complexStories/partner-drop-undrop-write/`. |
| 3 | Delete or `@deprecated` the 3 drift partner wrappers | ⬜ Open (not a spike — needs a traffic survey, not research) | Blocks `F12`. Owner: PO. |
| 4 | `USE_NEW_RULES_API` cutover (rules may move to spark-tag DGS) | ⬜ Open (not a spike) | Blocks `B10`/`B11`/`C05`. Owner: Product Owner. |
| 5 | `Product.division` bug fix — ship the response-shape change after a client survey | ✅ Resolved — ship straight, survey first | Blocks `G12`. Owner: PO. See `G12`'s write-up. |
| 6 | `components` ACL batching approach | ✅ Resolved — batch, no N+1 | See `G02`'s pseudocode; not an open question. |
| — | `getProducts` two-stage hydration design | 🔬 **Spike** `SPARK-PROD-S02` | Blocks `C01`. New item raised in review, not in the original 6. |
| — | Cross-domain association pattern (attachments/teams/partners/workspace) | 🔬 **Spike** `SPARK-PROD-S01` | Blocks `D01-D04`, `D06`, `D07`, `D11`. New item raised in review; prior teams↔domain research is directly on-topic. |

## Dependency Map
```
plm-product (Product subgraph, the host DGS) depends on:
 spark-product backend REST v1/v2 + elastic + spark_rules + external rating
 EXT (federation): attachment, workspace, discussion, sample, tag, team, user-profile, relationship, claim
 Platform (gateway): VMM, IG, Doppler, CORONA, APEX, Brand Compliance
 Internal (same DGS): bom, measurement, impression, packaging, productDetails, productAsk, productVariation, fileLibrary
 Sibling domains → contribute 8 ResourcesCount field sets (TechPack federation, Phase F)
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 0 | Program spikes | run in Sprint 0 (see global Phase 0 — Program Spikes) so D/C/E work isn't waiting |
| 1–2 | B01 (DGS module init + service wiring + first resolver) | schema, types, stubs, Categories resolver, ResourcesCount, service port |
| 3 | B01–B11 | all core reads (incl. rules reads) |
| 4 | C01–C05 | search/listing + rating + rules search (C01 needs `SPARK-SPIKE-06a` concluded) |
| 5–6 | D01–D18 | all simple mutations, parallelizable (D01-D04/D06/D07/D11 need `SPARK-SPIKE-06b` concluded) |
| 7–8 | E03/E04 | TechPack facade + bulk (focused; facade-vs-federate spike already resolved) |
| 9 | E01/E02 | partner actions (needs `SPARK-SPIKE-03` concluded) + component fan-out |
| 10–12 | G01–G10, G11-1, G11-2, G12–G14 | field resolvers (G01/G02 X-Large get their own sprint) |
| 13 | G15 + G16 | utils port + tests/parity/load/cut-over |
| post-launch | F01–F09 | TechPack federation (unblocked as siblings migrate) + facade retirement |
| any | F10–F12 | gateway composition + platform verify + drift decision |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~42–71 sprints | sequential — not recommended for this domain |
| 2 engineers | ~25–42 sprints | B/C/D parallel after B01 |
| 3–4 engineers | ~18–28 sprints | A done → B + C + D + most of G in parallel; E and the two X-Large fields on dedicated owners |

> Phase G dominates the calendar; the two X-Large field resolvers (`attachmentsWithMetaData`, `components`)
> and TechPack (E03/E04) are the cost-and-risk centre of the whole program.
