# Federated GraphQL Breakdown — Claims

| | |
|---|---|
| **Target DGS** | `spark-claims (separate)` |
| **T-Shirt Size** | **L** |
| **Total Stories** | 20 |
| **Complexity** | 🔴 0 Very High · 🟠 2 High · 🟡 9 Medium · 🟢 9 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

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
**ACL is ignored in the DGS implementation** (no ACL story) — noted for context only.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateClaim` (proxy-ACL multi-step) |
| Field-resolver type blocks | 4 | `Claims` (11), `ParentDetails` (3), substantiate (1), claimDetails (1) |
| External dependencies | 6 keys (1 🔴 · 3 🟡 · 2 🔵) | search 🔴; product/user-profile/workspace 🟡 |
| Federation contributions | 2 (Product.claims, ResourcesCount.claims) | BLOCKED-BY product |
| **Total stories** | **22** | green-field; separate subgraph |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `SPARK-CLM-E01` — `updateClaim` (proxy ACL + multi-step write) | `SPARK-SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPARK-SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

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
| **Total** | | **22** | **36–62d** (buffered) |

> One engineer ≈ **8–13 sprints**.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~9–15 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel after B01 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C01/C02 + D01–D05 | search + simple mutations |
| 3 | E01 + G01/G02 | `updateClaim` + ACL/partner field resolvers |
| 4 | G03/G04 + G05 | parent/elastic + misc fields + tests |
| post-launch | F01, F02 | federation contributions (unblocked by product) |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-CLM-B01`<br>`getClaims(parentHumanId, claimHumanIds, partnerIds)` | 🟢 Low `XS` | Query | — | **Intent —** List claims for a product / set of partners.<br>**Today —** claim.getClaims GET … (filtered) → camelCase. No ACL token<br>**Done when:**<br>• filters by the 3 args |
| 🔷 `SPARK-CLM-B02`<br>`getClaimByIds(claimHumanIds)` | 🟢 Low `XS` | Query | B01 | **Intent —** Fetch specific claims by their ids.<br>**Today —** token → GET …<br>**Done when:**<br>• returns claims for ids |
| 🔷 `SPARK-CLM-B03`<br>`getCommunicationChannels` (cacheable) | 🟢 Low `XS` | Query | B01 | **Intent —** Return the communication-channel lookup list (cached).<br>**Today —** GET …<br>**Done when:**<br>• returns channels; cached |
| 🔷 `SPARK-CLM-B04`<br>`getAllClaimsAbout` (cacheable) | 🟢 Low `XS` | Query | B01 | **Intent —** Return the 'claims about' lookup list (cached).<br>**Today —** GET …<br>**Done when:**<br>• returns list; cached |
| 🔷 `SPARK-CLM-B05`<br>`getClaimExports` | 🟢 Low `XS` | Query | B01 | **Intent —** List the claim export jobs.<br>**Today —** GET …<br>**Done when:**<br>• returns export records |

> **`SPARK-CLM-B01`** — **Note — DGS Module Init (this PR only):** Creates `claims.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql.


### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-CLM-C01`<br>`searchGuestFacing(queryParam)` | 🟡 Medium `M` | Query | B01 | **Intent —** Search the guest-facing (external-partner) claims view.<br>**Today —** GET … → camelCase<br>**Done when:**<br>• query-string built from `queryParam` |
| 🔷 `SPARK-CLM-C02`<br>`getClaimsElastic(parentHumanId)` | 🟡 Medium `M` | Query<br>Calls: `search` | B01 | **Intent —** Search a product's claims via elastic.<br>**Today —** (search) search.getClaimsElastic. EXT: search<br>**Done when:**<br>• `parentId:` elastic query built |


### ✏️ Phase D — Mutations (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `SPARK-CLM-D01`<br>`createClaim` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Create a new claim.<br>**Today —** POST … (snake_case). If validationErrors/message → throw<br>**Done when:**<br>• creates claim(s)<br>• validation error → exception |
| 🔶 `SPARK-CLM-D02`<br>`bulkUpdateClaim` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Update many claims in one call.<br>**Today —** PUT … Error contract: result is array → return; status_code>400 → throw; else throw "unhandled". Latent: source snake-cases the response — fix to camelCase<br>**Done when:**<br>• array result returned (camelCase)<br>• error status → exception |
| 🔶 `SPARK-CLM-D03`<br>`requestClaimExport` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Kick off a claim export job.<br>**Today —** POST … → response.request_id<br>**Done when:**<br>• returns the request id |
| 🔶 `SPARK-CLM-D04`<br>`lockClaim` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Lock a claim from edits.<br>**Today —** token → PUT …<br>**Done when:**<br>• locks the claim |
| 🔶 `SPARK-CLM-D05`<br>`unlockClaim` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Unlock a claim for edits.<br>**Today —** token → PUT …<br>**Done when:**<br>• unlocks the claim |


### ⚙️ Phase E — Complex Operations (1 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `SPARK-CLM-E01`<br>`updateClaim` (proxy ACL + multi-step write)<br>🔴🔬 _Spike-gated on `SPARK-SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `workspaceV2` | SPARK-SPIKE-01, B01 | **Intent —** Edit a claim — a multi-step write (permissions + workspace + body) that has no rollback today.<br>**Today —** getUserPermissionsJWTByProxy({id:humanId, proxyIds:[parentId], basePermissions:true}) (proxy/external ACL path — context only); 2) if workspaceContext.{add,remove}…<br>**Done when:**<br>• workspace assoc runs when present<br>• body update + throw-on-error<br>• partial-failure strategy | ☐ body-only<br>☐ +workspace<br>☐ validation-error→throw<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-CLM-F01`<br>`Product.claims` (federation contribution) | 🟡 Medium `M` | Field Resolver | B01 | **Intent —** Expose a product's claims on the Product type (federation contribution).<br>**Today —** extend type Product @key(fields:"id") { claims(partnerIds:[String], includeClaims:Boolean): [Claims] } with a @DgsEntityFetcher; the claims subgraph fills `Product<br>**Done when:**<br>• `Product.claims` resolves via federation<br>• parity vs the current in-gateway resolver |
| 🔸 `SPARK-CLM-F02`<br>`ResourcesCount.claims` (TechPack — claims side of SPARK-PROD-F05) | 🟢 Low `XS` | Field Resolver | B01 | **Intent —** Contribute the claims count to the product TechPack rollup.<br>**Today —** extend type ResourcesCount @key(fields:"productId partnerId") { claims: [ID] } with a<br>**Done when:**<br>• field resolves on the federated `ResourcesCount`; parity vs facade |


### 🧪 Phase G — Field Resolvers & Tests (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `SPARK-CLM-G01`<br>`access` + `currentUserPermissions` + `participantDetails` | 🟡 Medium `M` | Field Resolver<br>Calls: `userGroup` | B01 | **Intent —** Resolve a claim's access / permission / participant fields.<br>**Done when:**<br>• each resolves; null-safe | — |
| 🔸 `SPARK-CLM-G02`<br>`createdBy` + `updatedBy` + `businessPartner` + `designPartner` | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `vmm` | B01 | **Intent —** Resolve the people and partner fields on a claim.<br>**Today —** users via user-profile; businessPartner 3-way fallback (partnerId \\|\\| {bpId:0,bpName:'Target'} when no dpPartnerId \\|\\| dpPartnerId); designPartner dpPartnerId or…<br>**Done when:**<br>• all 3 BP branches correct (incl. `bpId:0` Target)<br>• null id → null user | — |
| 🔸 `SPARK-CLM-G03`<br>`product` + `parentDetails` (otherClaimBps / systemTeams / droppedPartnerIds) | 🟠 High `L` | Field Resolver<br>Calls: `product`, `search` | B01 | **Intent —** Resolve the parent product and its related-partner context on a claim.<br>**Today —** product (product, only if parentId starts 'PID'); parentDetails → - product.getByID(parentId) (the product feeds ParentDetails): otherClaimBps (search getClaimsElastic…<br>**Done when:**<br>• `product` null when not `PID*`<br>• `otherClaimBps`/`systemTeams` elastic queries match source; empty-BP → `{content:[]}` | ☐ product branch<br>☐ otherClaimBps<br>☐ systemTeams<br>☐ empty BPs |
| 🔸 `SPARK-CLM-G04`<br>`workspaces` + `ClaimSubstantiate.substantiatedBy` + `ClaimDetails.claimName` | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `userAttributes` | B01 | **Intent —** Resolve workspace links and a few computed claim fields.<br>**Done when:**<br>• each resolves; `workspaces` null when empty<br>• `claimName` mirrors `guestFacingClaim` | — |
| 📄 `SPARK-CLM-G05`<br>Tests, parity harness | 🟡 Medium `M` | Tests | B01, E01, G02, G03 | **Intent —** Prove the claims subgraph matches the old gateway.<br>**Today —** ≥80% unit coverage; parity fixtures (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green<br>• schema-diff intentional | — |

