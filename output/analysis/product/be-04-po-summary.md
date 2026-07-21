# Phase 4: PO Sprint Planning Summary — Product

> **Domain:** `product` · **Target DGS:** `plm-product` (host DGS) · **Generated:** 2026-06-26
> **Stories:** [be-04-stories.md](./be-04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

- We are moving **Product** — the central entity of the PLM system — off the `spark-internal-graphql` gateway into the **`plm-product`** Netflix DGS.
- Product is the **largest and highest-risk** domain (18 queries, 20 mutations, ~50 field resolvers on a 2,629-line resolver) and the **host service** for the whole product family: BOM, Measurement, Impression, Packaging and others live in the same DGS, so their links from Product resolve **internally** rather than across the federation gateway.

- Most of the work is mechanical (the long tail of CRUD and simple field resolvers), but a handful of items carry real risk: the **TechPack count** query (a ~200-line, 14-step aggregation spanning 8 domains' data via 4 physical services, which becomes a federated composite-key entity), the **partner drop/undrop** orchestration, the cross-domain **components** and **attachmentsWithMetaData** field resolvers, and a **latent `division` bug**.
- We recommend the **facade-then-federate** approach for TechPack (draft **ADR-015** Option B; the pattern `techpack-migration-options.md` labels "Option D (hybrid)"): ship a thin query over a temporary aggregation facade so it works on day 1, then federate each piece to its owning domain, then retire the facade (`F-09`).

**ACL note:** the legacy gateway obtains per-resource capability tokens via ACL on nearly every call. Per
**ADR-019** (`complexStories/acl/01-adr-acl-mid-request-update.md`), permission-check and own-domain-token
call sites stay resolver-local (context-only, unchanged); downstream-token call sites — where a resolver
hands its token to a *different* domain's loader — use **Mid-Request ACL Update**
(`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before the downstream call.

## Deployment model — ship on green, per story

- Every story is **end-to-end in one PR** and **independently deployable to production once its own tests and parity pass** — no waiting for the rest of the phase.
- The **one exception** is a story whose field is produced by **composing another subgraph's data** (a cross-subgraph **entity extension**, `extend type … @key` resolved by a different DGS): those go live only once the **owning subgraph is deployed**, and are marked
**BLOCKED-BY `<domain>`**.

- ✅ **Ships on green** — all B/C/D/E/G stories, the internal Phase-F contributions (`F-04`, `F-06`, `F-08`), the
  gateway/platform stories (`F-10`, `F-11`), and the **TechPack facade** (`E-03`/`E-04`), which is *designed* to
  work day 1 before any sibling federates.
- ⛔ **Waits for an owning subgraph (the exception)** — the true cross-subgraph federation stories
  **`H-01` (attachment), `H-02` (discussion), `H-03` (sample), `H-04` (claim), `H-05` (construction)**, plus
  **`F-09`** (facade retirement, which needs all 8 contributions live). These are the only stories held back
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
| **Total stories** | **67** | green-field build stories (`G-11` split into `G-11-1`/`G-11-2` = +1). The 3 Phase-0 spike stubs (`S-01`–`S-03`) are tracked as **program spikes** in the global breakdown and Jira, not as rows here |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) | Ready when |
|---|---|---|---|---|
| B | Core Reads | 11 | 11–18d | after B-01 |
| C | Search & Listing | 5 | 17–29d | after B-01; C-01 gated on `SPIKE-06a` (Hydration, via `PRODUCT-BE-S-02`) |
| D | Mutations (simple) | 18 | 25–40d | after B-01; D-01/D-02/D-04 gated on `SPIKE-06b` (Association, via `PRODUCT-BE-S-01`); D-03/D-06/D-07/D-11 unblocked (single-backend, per ADR-011 scope) |
| E | Complex (partner/components/TechPack) | 4 | 33–56d | E-01 gated on `SPIKE-03` |
| F | Federation & Stitching (ships on green) | 8 | 14–24d | after E-03; F-04/F-06/F-08 internal (co-located); F-09 waits for all H |
| H | Entity Resolution (cross-subgraph, BLOCKED) | 6 | 10–18d | BLOCKED-BY sibling subgraph deploys (attachment/discussion/sample/claim/construction) |
| G | Field Resolvers, Bug-fixes, Utils, Tests | 17 | 86–143d | after B-01. `G-11` split into `G-11-1`/`G-11-2` (16 → 17) |
| **Total** | | **69** | **196–328d** (buffered; sum of phase rows) | |

> One engineer ≈ **39–66 sprints**. Heavily parallelizable after B-01; 2–3 engineers strongly recommended.

> **Phase F vs H clarification.** Phase F stories resolve **internally** (co-located domains in the same DGS
> process) or handle schema/composition infrastructure — they **ship on green**. Phase H stories require a
> **separate subgraph's deployment** at runtime (`@DgsEntityFetcher` cross-subgraph resolution) — they are
> **BLOCKED-BY** that subgraph and sequenced post-launch. See
> [federation-review/04-entity-analysis.md](../federation-review/04-entity-analysis.md) for the full distinction.

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B-01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories; the `Categories` union `@DgsTypeResolver` remains a dedicated story.

> **Thin DGS wrappers — parallel after B-01.** The model, REST controller (GET/POST/PUT) and service already exist; each story only adds the Netflix-DGS layer so the federated graph can stitch this subgraph. The **one-time DGS module scaffold** B-01 lands (schema file + scalar registration + service/Feign wiring) is a prerequisite for every operation story, so it is **assumed — not repeated in each story's `Depends On`** (rows list only genuine story-to-story dependencies). E.g. `D-08 removeProductResources` is a one-line wrapper over the existing REST `DELETE`/`PUT`, so its `Depends On` is **—**. After B-01, phases B/C/D/G run fully in parallel.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| TechPack aggregation (E-03/E-04) | 🔴 High | Biggest single cost; direction pre-resolved as facade-then-federate (draft ADR-015, ratification pending) — the facade works on day 1 |
| Partner drop/undrop (E-01) | 🔴 High | `S-03` spike (program id `SPIKE-03`, run first) picks ownership + recovery strategy before `E-01` starts — draft ADR-012 |
| `getProducts` two-stage hydration (C-01) | 🟡 Medium-High | `S-02` spike (program id `SPIKE-06a`) resolves workspace-filter placement + elastic/canonical staleness before `C-01` starts |
| Cross-domain association pattern (D-01/D-02/D-04) | 🟡 Medium | `S-01` spike (program id `SPIKE-06b`, draft ADR-011) picks one pattern for the 3 cross-subgraph mutations; D-03/D-06/D-07/D-11 descoped (single-backend) |
| `components` / `attachmentsWithMetaData` (G-01/G-02) | 🟡 Medium-High | Large, performance-sensitive; budget X-Large |
| `G-13` FE chokepoint (IG/tag/tcin/spg + template fields) | 🟡 Medium | Blocks **8 FE stories** — prioritize early in G phase |
| `division` latent bug (`Product.division`/`DopplerDepartment.division` wrong-loader bug, tracked outside this Jira pipeline) | 🟡 Medium | Fixing it changes the response shape — client survey before rollout |
| 8 TechPack placeholders block on 8 domains | 🟡 Medium | Facade keeps it working; retire only when all siblings are live |
| Rules feature-flag + external rating secret | 🟢 Low | Verify flag everywhere; move the rating key to Vault |

## Decisions Required

> Reviewed and updated. Open items needing real research are now **Phase 0 spike stories** — see
> *Phase 0 — Spikes* in [`be-04-stories.md`](./be-04-stories.md) for the full write-up of each.

| # | Decision | Status | Detail |
|---|---|---|---|
| 1 | TechPack facade: Node extract vs Kotlin aggregation | ✅ Direction resolved — facade-then-federate (draft ADR-015 Option B; catalogue "Option D Phase 1"); ADR ratification pending | Facade now, federate per-domain later, retire facade (`F-09`). See `E-03`'s note + `complexStories/techpack/`. |
| 2 | `productBusinessPartnerActions` failure strategy | 🔬 **Spike** `PRODUCT-BE-S-03` (program id `SPIKE-03`, run first) | Blocks `E-01`. Draft ADR-012 in `complexStories/partner-drop-undrop-write/`. |
| 3 | Delete or `@deprecated` the 3 drift partner wrappers | ⬜ Open (not a spike — needs a traffic survey, not research) | Blocks `F-12`. Owner: PO. |
| 4 | `USE_NEW_RULES_API` cutover (rules may move to spark-tag DGS) | ⬜ Open (not a spike) | Blocks `B-10`/`B-11`/`C-05`. Owner: Product Owner. |
| 5 | `Product.division` bug fix — ship the response-shape change after a client survey | ✅ Resolved — ship straight, survey first | Tracked outside this Jira pipeline, created manually — see `be-04-stories.md` Phase G's `G-13` note. Owner: PO. |
| 6 | `components` ACL batching approach | ✅ Resolved — batch, no N+1 | See `G-02`'s pseudocode; not an open question. |
| — | `getProducts` two-stage hydration design | 🔬 **Spike** `PRODUCT-BE-S-02` | Blocks `C-01`. New item raised in review, not in the original 6. |
| — | Cross-domain association pattern (attachments/teams/partners/workspace) | 🔬 **Spike** `PRODUCT-BE-S-01` (program id `SPIKE-06b`) | Blocks `D-01`/`D-02`/`D-04` only — draft ADR-011 descopes `D-03` (pure passthrough) and `D-06`/`D-07`/`D-11` (single-backend writes). Prior teams↔domain research (ADR-010) is directly on-topic. |

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
| 1–2 | B-01 (DGS module init + service wiring + first resolver) | schema, types, stubs, Categories resolver, ResourcesCount, service port |
| 3 | B-01–B-11 | all core reads (incl. rules reads) |
| 4 | C-01–C-05 | search/listing + rating + rules search (C-01 needs `SPIKE-06a` concluded) |
| 5–6 | D-01–D-18 | all simple mutations, parallelizable (D-01/D-02/D-04 need `SPIKE-06b` concluded; D-03/D-06/D-07/D-11 unblocked) |
| 7–8 | E-03/E-04 | TechPack facade + bulk (focused; facade-then-federate direction already resolved, draft ADR-015) |
| 9 | E-00 (shared `WriteSaga` module, Sprint-0 critical path) + E-01/E-02 | partner actions (needs `SPIKE-03` concluded) + component fan-out |
| 10–12 | G-01–G-10, G-11-1, G-11-2, G-13–G-14 | field resolvers (G-01/G-02 X-Large get their own sprint) |
| 13 | G-15 | utils port (Kotlin). Test coverage/parity/load/cut-over rehearsal tracked outside this Jira pipeline, created manually. |
| post-launch | H-01–H-06, F-09 | TechPack federation (unblocked as siblings migrate) + facade retirement |
| any | F-10–F-12 | gateway composition + platform verify + drift decision |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~39–66 sprints | sequential — not recommended for this domain |
| 2 engineers | ~25–42 sprints | B/C/D parallel after B-01 |
| 3–4 engineers | ~18–28 sprints | A done → B + C + D + most of G in parallel; E and the two X-Large fields on dedicated owners |

> Phase G dominates the calendar; the two X-Large field resolvers (`attachmentsWithMetaData`, `components`)
> and TechPack (E-03/E-04) are the cost-and-risk centre of the whole program.
