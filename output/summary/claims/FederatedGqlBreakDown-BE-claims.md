# Federated GraphQL Breakdown — Claims

| | |
|---|---|
| **Target DGS** | `spark-claims (separate)` |
| **T-Shirt Size** | **L** |
| **Total Stories** | 15 |
| **Complexity** | 🔴 0 Very High · 🟠 2 High · 🟡 11 Medium · 🟢 2 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-17 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

We are moving the **Claims** domain — a product's marketing/technical claims (claim details, guest-facing
copy, substantiation, per-partner access, exports) — off the `spark-internal-graphql` gateway into its
**own `claims` DGS subgraph**. Unlike BOM/Measurement/ProductDetails, claims is **not** part of the
plm-product monorepo, so its links to Product, search, workspace, user-profile and VMM are all
**cross-subgraph** (federation / gateway stitch), and it **contributes** the `Product.claims` field and the
TechPack `ResourcesCount.claims` count back to plm-product.

It is **mid-sized and mid-risk**: 7 queries, 6 mutations, 17 field resolvers on a 164-line resolver, with
**no polymorphism**. The one genuinely harder piece is **`updateClaim`**, a multi-step write that uses the
**proxy/external ACL** path plus workspace association, with no rollback today.

**ACL note:** the current code obtains capability tokens via ACL (including the proxy variant for update);
Per the program-level working decision, **the DGS layer carries no ACL plumbing story** — each domain service performs its own access control; scenario ADRs ([`complexStories/*/02-adr-noacl-*.md`](https://github.com/XXX/blob/main/output/complexStories/*/02-adr-noacl-*.md)) record the assumption's impact and ratify with the global decision. ACL is noted in stories for context only.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateClaim` (proxy-ACL multi-step) |
| Field-resolver type blocks | 4 | `Claims` (11), `ParentDetails` (3), substantiate (1), claimDetails (1) |
| External dependencies | 6 keys (1 🔴 · 3 🟡 · 2 🔵) | search 🔴; product/user-profile/workspace 🟡 |
| Federation contributions | 2 (Product.claims, ResourcesCount.claims) | BLOCKED-BY product |
| **Total stories** | **20** | green-field; separate subgraph |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `CLAIM-BE-E-01` — `updateClaim` (proxy ACL + multi-step write) | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 5 | 5–9d |
| C | Search & Listing | 2 | 4–7d |
| D | Mutations (simple) | 5 | 7–12d |
| E | Complex (`updateClaim`) | 1 | 4–7d |
| F | Federation Contributions | 2 | 4–7d (BLOCKED-BY product) |
| G | Field Resolvers & Tests | 5 | 12–20d |
| **Total** | | **20** | **36–62d** (buffered) |

> One engineer ≈ **8–13 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~9–15 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel after B-01 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-05 | search + simple mutations |
| 3 | E-01 + G-01/G-02 | `updateClaim` + ACL/partner field resolvers |
| 4 | G-03/G-04 + G-05 | parent/elastic + misc fields + tests |
| post-launch | F-01, F-02 | federation contributions (unblocked by product) |

---

## Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟡 `B-02`, 🟡 `C-01`, 🟡 `C-02`, 🟡 `D-01`, 🟡 `D-02`, 🟡 `D-03`, 🟠 `E-01`, 🟡 `F-01`, 🟢 `F-02`, 🟡 `G-01`, 🟡 `G-02`, 🟠 `G-03`, 🟡 `G-04` | `E-01` → 🔬 SPIKE-01<br>`F-01` → ⛔ BLOCKED-BY product<br>`F-02` → ⛔ BLOCKED-BY product | Fan-out — 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🔗 Federation & Stitching · 🧪 Field Resolvers & Tests |
| 3 | 🟡 `G-05` | — | 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `G-03` → `G-05` — 3 sequential stories; everything else hangs off this chain in parallel.

---

## Recommended Story Graph — 2 Backend Engineers

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 2 backend engineers** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 | 👤 BE-2 |
|---|---|---|
| 1 | 🟢 `B-01` (1–2d) | ⏳ after `B-01` → 🟠 `G-03` (4–7d) |
| 2 | 🟠 `E-01` (4–7d) 🔬 | 🟡 `B-02` (2–4d) *(grouped XS: +`B-03`, `B-04`, `B-05`)* |
| 3 | 🟡 `G-02` (2–4d) | 🟡 `C-02` (2–4d) |
| 4 | 🟡 `C-01` (2–4d) | 🟡 `D-02` (2–4d) |
| 5 | 🟡 `D-01` (2–4d) | 🟡 `F-01` (2–4d) ⛔ |
| 6 | 🟡 `D-03` (2–4d) *(grouped XS: +`D-04`, `D-05`)* | 🟡 `G-04` (2–4d) |
| 7 | 🟡 `G-01` (2–4d) | 🟢 `F-02` (1–2d) ⛔ |
| 8 | 🟡 `G-05` (2–4d) | — |

**BE-1:** `B-01` → `E-01` → `G-02` → `C-01` → `D-01` → `D-03` → `G-01` → `G-05`<br>**BE-2:** `G-03` → `B-02` → `C-02` → `D-02` → `F-01` → `G-04` → `F-02`

**Elapsed (nominal midpoints):** ~25 working days with 2 engineers vs ~47 days sequential.

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `CLAIM-BE-B-01`<br>`getClaims(parentHumanId, claimHumanIds, partnerIds)` | 🟢 Low `XS` | Query | — | **Intent —** List claims for a product / set of partners.<br>**Today —** claim.getClaims GET … (filtered) → camelCase. No ACL token<br>**Done when:**<br>• filters by the 3 args |
| 🔷 `CLAIM-BE-B-02`<br>`getClaimByIds` · `getCommunicationChannels` · `getAllClaimsAbout` · `getClaimExports` | 🟡 Medium `M` | Query | B-01 | **Grouped XS story —** combines former `B-03`, `B-04`, `B-05` (one PR train)<br>**Intent —** Fetch specific claims by their ids; Return the communication-channel lookup list (cached); Return the 'claims about' lookup list (cached); List the claim export jobs<br>**Today —** token → GET … ; GET … ; GET … ; GET …<br>**Done when:**<br>• `getClaimByIds`: returns claims for ids<br>• `getCommunicationChannels`: returns channels; cached<br>• `getAllClaimsAbout`: returns list; cached<br>• `getClaimExports`: returns export records |

> **`CLAIM-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `claims.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.


### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `CLAIM-BE-C-01`<br>`searchGuestFacing(queryParam)` | 🟡 Medium `M` | Query | B-01 | **Intent —** Search the guest-facing (external-partner) claims view.<br>**Today —** GET … → camelCase<br>**Done when:**<br>• query-string built from `queryParam` |
| 🔷 `CLAIM-BE-C-02`<br>`getClaimsElastic(parentHumanId)` | 🟡 Medium `M` | Query<br>Calls: `search` | B-01 | **Intent —** Search a product's claims via elastic.<br>**Today —** (search) search.getClaimsElastic. EXT: search<br>**Done when:**<br>• `parentId:` elastic query built |


### ✏️ Phase D — Mutations (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `CLAIM-BE-D-01`<br>`createClaim` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create a new claim.<br>**Today —** POST … (snake_case). If validationErrors/message → throw<br>**Done when:**<br>• creates claim(s)<br>• validation error → exception |
| 🔶 `CLAIM-BE-D-02`<br>`bulkUpdateClaim` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Update many claims in one call.<br>**Today —** PUT … Error contract: result is array → return; status_code>400 → throw; else throw "unhandled". Latent: source snake-cases the response — fix to camelCase<br>**Done when:**<br>• array result returned (camelCase)<br>• error status → exception |
| 🔶 `CLAIM-BE-D-03`<br>`requestClaimExport` · `lockClaim` · `unlockClaim` | 🟡 Medium `M` | Mutation | B-01 | **Grouped XS story —** combines former `D-04`, `D-05` (one PR train)<br>**Intent —** Kick off a claim export job; Lock a claim from edits; Unlock a claim for edits<br>**Today —** POST … → response.request_id. ; token → PUT … ; token → PUT …<br>**Done when:**<br>• `requestClaimExport`: returns the request id<br>• `lockClaim`: locks the claim<br>• `unlockClaim`: unlocks the claim |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `CLAIM-BE-E-01`<br>`updateClaim` (proxy ACL + multi-step write)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `workspaceV2` | SPIKE-01, B-01 | **Intent —** Edit a claim — a multi-step write (permissions + workspace + body) that has no rollback today.<br>**Today —** getUserPermissionsJWTByProxy({id:humanId, proxyIds:[parentId], basePermissions:true}) (proxy/external ACL path — context only); 2) if workspaceContext.{add,remove}…<br>**Done when:**<br>• workspace assoc runs when present<br>• body update + throw-on-error<br>• partial-failure strategy | ☐ body-only<br>☐ +workspace<br>☐ validation-error→throw<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `CLAIM-BE-F-01`<br>`Product.claims` (federation contribution) | 🟡 Medium `M` | Field Resolver | B-01 | **Intent —** Expose a product's claims on the Product type (federation contribution).<br>**Today —** extend type Product @key(fields:"id") { claims(partnerIds:[String], includeClaims:Boolean): [Claims] } with a @DgsEntityFetcher; the claims subgraph fills `Product<br>**Done when:**<br>• `Product.claims` resolves via federation<br>• parity vs the current in-gateway resolver |
| 🔸 `CLAIM-BE-F-02`<br>`ResourcesCount.claims` (TechPack — claims side of PRODUCT-BE-F-05) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Contribute the claims count to the product TechPack rollup.<br>**Today —** extend type ResourcesCount @key(fields:"productId partnerId") { claims: [ID] } with a<br>**Done when:**<br>• field resolves on the federated `ResourcesCount`; parity vs facade |


### 🧪 Phase G — Field Resolvers & Tests (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `CLAIM-BE-G-01`<br>`access` + `currentUserPermissions` + `participantDetails` | 🟡 Medium `M` | Field Resolver<br>Calls: `userGroup` | B-01 | **Intent —** Resolve a claim's access / permission / participant fields.<br>**Done when:**<br>• each resolves; null-safe | — |
| 🔸 `CLAIM-BE-G-02`<br>`createdBy` + `updatedBy` + `businessPartner` + `designPartner` | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `vmm` | B-01 | **Intent —** Resolve the people and partner fields on a claim.<br>**Today —** users via user-profile; businessPartner 3-way fallback (partnerId \\|\\| {bpId:0,bpName:'Target'} when no dpPartnerId \\|\\| dpPartnerId); designPartner dpPartnerId or…<br>**Done when:**<br>• all 3 BP branches correct (incl. `bpId:0` Target)<br>• null id → null user | — |
| 🔸 `CLAIM-BE-G-03`<br>`product` + `parentDetails` (otherClaimBps / systemTeams / droppedPartnerIds) | 🟠 High `L` | Field Resolver<br>Calls: `product`, `search` | B-01 | **Intent —** Resolve the parent product and its related-partner context on a claim.<br>**Today —** product (product, only if parentId starts 'PID'); parentDetails → - product.getByID(parentId) (the product feeds ParentDetails): otherClaimBps (search getClaimsElastic…<br>**Done when:**<br>• `product` null when not `PID*`<br>• `otherClaimBps`/`systemTeams` elastic queries match source; empty-BP → `{content:[]}` | ☐ product branch<br>☐ otherClaimBps<br>☐ systemTeams<br>☐ empty BPs |
| 🔸 `CLAIM-BE-G-04`<br>`workspaces` + `ClaimSubstantiate.substantiatedBy` + `ClaimDetails.claimName` | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `userAttributes` | B-01 | **Intent —** Resolve workspace links and a few computed claim fields.<br>**Done when:**<br>• each resolves; `workspaces` null when empty<br>• `claimName` mirrors `guestFacingClaim` | — |
| 📄 `CLAIM-BE-G-05`<br>Tests, parity harness | 🟡 Medium `M` | Tests | B-01, E-01, G-02, G-03 | **Intent —** Prove the claims subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity fixtures (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green<br>• schema-diff intentional | — |

