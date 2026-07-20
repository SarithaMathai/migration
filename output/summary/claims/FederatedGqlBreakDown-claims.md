## Backend

### Federated GraphQL Breakdown — Claims

| | |
|---|---|
| **Target DGS** | `spark-claims (separate)` |
| **T-Shirt Size** | **L** |
| **Total Stories** | 20 |
| **Complexity** | 🔴 0 Very High · 🟠 2 High · 🟡 8 Medium · 🟢 10 Low |
| **Phase Coverage** | 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🧪 G · 🧬 H |
| **Generated** | 2026-07-19 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G · 🧬 H

---

#### What Are We Building?

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
Per **ADR-019** ([`complexStories/acl/01-adr-acl-mid-request-update.md`](https://github.com/XXX/blob/main/output/complexStories/acl/01-adr-acl-mid-request-update.md)), permission-check and own-domain-token call sites stay resolver-local (context-only, unchanged); downstream-token call sites — where a resolver hands its token to a *different* domain's loader — use **Mid-Request ACL Update** (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before the downstream call.

---

#### Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 7 | 2 cacheable master-data; 1 elastic (🔴 search) |
| Mutations | 6 | 5 simple + `updateClaim` (proxy-ACL multi-step) |
| Field-resolver type blocks | 4 | `Claims` (11), `ParentDetails` (3), substantiate (1), claimDetails (1) |
| External dependencies | 6 keys (1 🔴 · 3 🟡 · 2 🔵) | search 🔴; product/user-profile/workspace 🟡 |
| Federation contributions | 2 (Product.claims, ResourcesCount.claims) | BLOCKED-BY product |
| **Total stories** | **20** | green-field; separate subgraph |

---

#### Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

**Spike-gated stories in this domain** — each is flagged 🔴🔬 in its phase table with the same id in `Depends On`. *(Engineer: follow the id to the global **Spike Detail** for the target flow + the external services each resolver calls. See **How to read the spikes & related stories** in the global doc.)*

| Story | Program spike | Bucket |
|---|---|---|
| 🔴🔬 `CLAIM-BE-E-01` — `updateClaim` (proxy ACL + multi-step write) | `SPIKE-01` | Non-Atomic Write Saga |

> Follow a story's `SPIKE-0x` id to the global **Spike Detail** for its brief, steps and cross-service resolver breakdown.

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

#### Effort Snapshot

| Phase | Name | Stories | Effort (est., +20% buffer) |
|-------|------|---------|----------------------------|
| B | Core Reads | 5 | 6–12d |
| C | Search & Listing | 2 | 5–10d |
| D | Mutations | 5 | 8–17d |
| E | Complex Operations | 1 | 5–8d |
| G | Field Resolvers & Tests | 5 | 13–25d |
| H | Entity Resolution | 2 | 4–7d |
| **Total** | | **20** | **41–79d** (buffered) |

> Computed live from `be-04-stories.md` (phase + complexity per story) — always reconciles with the story tables below and the program overview. Effort = sum of per-story nominal day-ranges (Low 1–2 · Medium 2–4 · High 4–7 · Very High 7–12) × 1.2 buffer, AI-estimated — confirm in refinement. See each story's **Depends On** column for real sequencing.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~9–15 sprints | sequential |
| 2 engineers | ~5–8 sprints | reads + mutations parallel after B-01 |

---

#### Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1 | B-01 (DGS module init + service wiring + first resolver) | schema, service port, reads |
| 2 | C-01/C-02 + D-01–D-05 | search + simple mutations |
| 3 | E-01 + G-01/G-02 | `updateClaim` + ACL/partner field resolvers |
| 4 | G-03/G-04 + G-06 | parent/elastic + misc fields + shared value-type alignment |
| post-launch | H-01, H-02 | federation contributions (unblocked by product) |

---

#### Recommended Implementation Order

> Derived from each story's `Depends On` edges (plus the module-init scaffold as the implicit first step). A story appears in the earliest step where everything it depends on is already done; **stories in the same step are independent of each other and parallelize across engineers**. **Focus** names the phase category each step advances — same convention as the frontend order map.

> 🔬 spike gates and ⛔ cross-subgraph blocks are *entry criteria*, not ordering edges — a gated story slides later without reshuffling the map.

| Step | Stories (parallel set) | Entry gates in this step | Focus |
|---|---|---|---|
| 1 | 🟢 `B-01` | — | 🧱 Module init — schema skeleton, service wiring (unblocks everything) |
| 2 | 🟢 `B-02`, 🟢 `B-03`, 🟢 `B-04`, 🟢 `B-05`, 🟡 `C-01`, 🟡 `C-02`, 🟡 `D-01`, 🟡 `D-02`, 🟢 `D-03`, 🟢 `D-04`, 🟢 `D-05`, 🟠 `E-01`, 🟡 `G-01`, 🟡 `G-02`, 🟡 `G-04`, 🟢 `G-06`, 🟡 `H-01`, 🟢 `H-02` | `E-01` → 🔬 SPIKE-01 · ⛔ BLOCKED-BY product (PRODUCT-BE-E-00, the shared WriteSaga module)<br>`H-01` → ⛔ BLOCKED-BY product (PRODUCT-BE-F-14, product-side stub alignment; also waits on the Product entity existing, plm-product Phase A)<br>`H-02` → ⛔ BLOCKED-BY product (PRODUCT-BE-E-03, TechPack facade; also PRODUCT-BE-F-14 contract alignment) | Fan-out — 📖 Core Reads · 🔍 Search & Listing · ✏️ Mutations · ⚙️ Complex Operations · 🧪 Field Resolvers & Tests · 🧬 Entity Resolution |
| 3 | 🟠 `G-03` | — | 🧪 Field Resolvers & Tests |

**Critical path:** `B-01` → `G-06` → `G-03` — 3 sequential stories; everything else hangs off this chain in parallel.

---

#### Recommended Story Graph — 1 Backend Engineer

> The order map above assumes unlimited parallelism; this packs the **same dependency graph onto 1 backend engineer** (greedy critical-chain scheduling, nominal day-ranges from complexity — confirm in refinement). Read each column top-to-bottom as one engineer's queue; ⏳ marks a slot that waits on a dependency, 🔬/⛔ are entry gates that slide a slot without reshuffling the lanes.

| Slot | 👤 BE-1 |
|---|---|
| 1 | 🟢 `B-01` (1–2d) |
| 2 | 🟢 `G-06` (1–2d) |
| 3 | 🟠 `E-01` (4–7d) 🔬 ⛔ |
| 4 | 🟠 `G-03` (4–7d) |
| 5 | 🟡 `C-01` (2–4d) |
| 6 | 🟡 `C-02` (2–4d) |
| 7 | 🟡 `D-01` (2–4d) |
| 8 | 🟡 `D-02` (2–4d) |
| 9 | 🟡 `G-01` (2–4d) |
| 10 | 🟡 `G-02` (2–4d) |
| 11 | 🟡 `G-04` (2–4d) |
| 12 | 🟡 `H-01` (2–4d) ⛔ |
| 13 | 🟢 `B-02` (1–2d) |
| 14 | 🟢 `B-03` (1–2d) |
| 15 | 🟢 `B-04` (1–2d) |
| 16 | 🟢 `B-05` (1–2d) |
| 17 | 🟢 `D-03` (1–2d) |
| 18 | 🟢 `D-04` (1–2d) |
| 19 | 🟢 `D-05` (1–2d) |
| 20 | 🟢 `H-02` (1–2d) ⛔ |

**BE-1:** `B-01` → `G-06` → `E-01` → `G-03` → `C-01` → `C-02` → `D-01` → `D-02` → `G-01` → `G-02` → `G-04` → `H-01` → `B-02` → `B-03` → `B-04` → `B-05` → `D-03` → `D-04` → `D-05` → `H-02`

**Elapsed (nominal midpoints):** ~50 working days.

---

#### Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

##### 📖 Phase B — Core Reads (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `CLAIM-BE-B-01`<br>`getClaims(parentHumanId, claimHumanIds, partnerIds)` | 🟢 Low `XS` | Query | — | **Intent —** List claims for a product / set of partners.<br>**Today —** claim.getClaims GET … (filtered) → camelCase. No ACL token<br>**Done when:**<br>• filters by the 3 args |
| 🔷 `CLAIM-BE-B-02`<br>`getClaimByIds(claimHumanIds)` | 🟢 Low `XS` | Query | B-01 | **Intent —** Fetch specific claims by their ids.<br>**Today —** token → GET …<br>**Done when:**<br>• returns claims for ids |
| 🔷 `CLAIM-BE-B-03`<br>`getCommunicationChannels` (cacheable) | 🟢 Low `XS` | Query | B-01 | **Intent —** Return the communication-channel lookup list (cached).<br>**Today —** GET …<br>**Done when:**<br>• returns channels; cached |
| 🔷 `CLAIM-BE-B-04`<br>`getAllClaimsAbout` (cacheable) | 🟢 Low `XS` | Query | B-01 | **Intent —** Return the 'claims about' lookup list (cached).<br>**Today —** GET …<br>**Done when:**<br>• returns list; cached |
| 🔷 `CLAIM-BE-B-05`<br>`getClaimExports` | 🟢 Low `XS` | Query | B-01 | **Intent —** List the claim export jobs.<br>**Today —** GET …<br>**Done when:**<br>• returns export records |

> **`CLAIM-BE-B-01`** — **Note — DGS Module Init (this PR only):** Creates `claims.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: be-03-schema.graphql.


##### 🔍 Phase C — Search & Listing (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `CLAIM-BE-C-01`<br>`searchGuestFacing(queryParam)` | 🟡 Medium `M` | Query | B-01 | **Intent —** Search the guest-facing (external-partner) claims view.<br>**Today —** GET … → camelCase<br>**Done when:**<br>• query-string built from `queryParam` |
| 🔷 `CLAIM-BE-C-02`<br>`getClaimsElastic(parentHumanId)` | 🟡 Medium `M` | Query<br>Calls: `search` | B-01 | **Intent —** Search a product's claims via elastic.<br>**Today —** (search) search.getClaimsElastic. EXT: search<br>**Done when:**<br>• `parentId:` elastic query built |


##### ✏️ Phase D — Mutations (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `CLAIM-BE-D-01`<br>`createClaim` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Create a new claim.<br>**Today —** POST … (snake_case). If validationErrors/message → throw<br>**Done when:**<br>• creates claim(s)<br>• validation error → exception |
| 🔶 `CLAIM-BE-D-02`<br>`bulkUpdateClaim` | 🟡 Medium `M` | Mutation | B-01 | **Intent —** Update many claims in one call.<br>**Today —** PUT … Error contract: result is array → return; status_code>400 → throw; else throw "unhandled". Latent: source snake-cases the response — fix to camelCase<br>**Done when:**<br>• array result returned (camelCase)<br>• error status → exception |
| 🔶 `CLAIM-BE-D-03`<br>`requestClaimExport` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Kick off a claim export job.<br>**Today —** POST … → response.request_id<br>**Done when:**<br>• returns the request id |
| 🔶 `CLAIM-BE-D-04`<br>`lockClaim` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Lock a claim from edits.<br>**Today —** token → PUT …<br>**Done when:**<br>• locks the claim |
| 🔶 `CLAIM-BE-D-05`<br>`unlockClaim` | 🟢 Low `XS` | Mutation | B-01 | **Intent —** Unlock a claim for edits.<br>**Today —** token → PUT …<br>**Done when:**<br>• unlocks the claim |


##### ⚙️ Phase E — Complex Operations (1 story)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔴🔬 🔶 `CLAIM-BE-E-01`<br>`updateClaim` (proxy ACL + multi-step write)<br>🔴🔬 _Spike-gated on `SPIKE-01` (Non-Atomic Write Saga) — see global Spike Detail_ | 🟠 High `L` | Mutation<br>Calls: `workspaceV2` | SPIKE-01, B-01 | **Intent —** Edit a claim — a multi-step write (permissions + workspace + body) that has no rollback today.<br>**Today —** getUserPermissionsJWTByProxy({id:humanId, proxyIds:[parentId], basePermissions:true}) (proxy/external ACL path — context only); 2) if workspaceContext.{add,remove}…<br>**Done when:**<br>• workspace assoc runs when present<br>• body update + throw-on-error<br>• partial-failure strategy | ☐ body-only<br>☐ +workspace<br>☐ validation-error→throw<br>☐ partial-failure<br>☐ Parity: DGS response matches spark-internal-graphql baseline |


##### 🧪 Phase G — Field Resolvers & Tests (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `CLAIM-BE-G-01`<br>`access` + `currentUserPermissions` + `participantDetails` | 🟡 Medium `M` | Field Resolver<br>Calls: `userGroup` | B-01 | **Intent —** Resolve a claim's access / permission / participant fields.<br>**Done when:**<br>• each resolves; null-safe | — |
| 🔸 `CLAIM-BE-G-02`<br>`createdBy` + `updatedBy` + `businessPartner` + `designPartner` | 🟡 Medium `M` | Field Resolver<br>Calls: `userAttributes`, `vmm` | B-01 | **Intent —** Resolve the people and partner fields on a claim.<br>**Today —** users via user-profile; businessPartner 3-way fallback (partnerId \\|\\| {bpId:0,bpName:'Target'} when no dpPartnerId \\|\\| dpPartnerId); designPartner dpPartnerId or…<br>**Done when:**<br>• all 3 BP branches correct (incl. `bpId:0` Target)<br>• null id → null user | — |
| 🔸 `CLAIM-BE-G-03`<br>`product` + `parentDetails` (otherClaimBps / systemTeams / droppedPartnerIds) | 🟠 High `L` | Field Resolver<br>Calls: `product`, `search` | B-01, G-06 | **Intent —** Resolve the parent product and its related-partner context on a claim.<br>**Today —** product (product, only if parentId starts 'PID'); parentDetails → - product.getByID(parentId) (the product feeds ParentDetails): otherClaimBps (search getClaimsElastic…<br>**Done when:**<br>• `product` null when not `PID*`<br>• `otherClaimBps`/`systemTeams` elastic queries match source; empty-BP → `{content:[]}` | ☐ product branch<br>☐ otherClaimBps<br>☐ systemTeams<br>☐ empty BPs |
| 🔸 `CLAIM-BE-G-04`<br>`workspaces` + `ClaimSubstantiate.substantiatedBy` + `ClaimDetails.claimName` | 🟡 Medium `M` | Field Resolver<br>Calls: `workspaceV2`, `userAttributes` | B-01 | **Intent —** Resolve workspace links and a few computed claim fields.<br>**Done when:**<br>• each resolves; `workspaces` null when empty<br>• `claimName` mirrors `guestFacingClaim` | — |
| 📄 `CLAIM-BE-G-06`<br>Shared value-type alignment (`@shareable` instead of entity stubs) | 🟢 Low `XS` | Schema | B-01 | **Intent —** Models `ProductComponentStatus`, `ResourcePermissions` and `TeamPaged` as shared value<br>**Today —** duplicate the value types @shareable in the claims schema<br>**Done when:**<br>• Claims subgraph composes with plm-product with zero `INVALID_FIELD_SHARING`/value-type conflicts<br>• `statuses` / `currentUserPermissions` / `systemTeams` return locally-resolved data (parity vs the old gateway)<br>• `TeamPaged.content: [TeamV2]` resolves against the claims elastic response (map result rows to `{teamId}` stubs); documented<br>• Revisit note recorded for the phase-2 team subgraph (TeamV2 becomes its full entity then; today it is a stitched stub) | — |


##### 🧬 Phase H — Entity Resolution (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `CLAIM-BE-H-01`<br>`Product.claims` (federation contribution) | 🟡 Medium `M` | Field Resolver | B-01 | **Intent —** Expose a product's claims on the Product type (federation contribution).<br>**Today —** extend type Product @key(fields:"id") { claims(partnerIds:[String], includeClaims:Boolean): [Claims] } with a @DgsEntityFetcher; the claims subgraph fills `Product<br>**Done when:**<br>• `Product.claims` resolves via federation<br>• parity vs the current in-gateway resolver |
| 🔸 `CLAIM-BE-H-02`<br>`ResourcesCount.claims` (TechPack — claims side of PRODUCT-BE-H-04) | 🟢 Low `XS` | Field Resolver | B-01 | **Intent —** Contribute the claims count to the product TechPack rollup.<br>**Today —** extend type ResourcesCount @key(fields:"productId partnerId") { claims: [ID] } with a<br>**Done when:**<br>• field resolves on the federated `ResourcesCount`; parity vs facade |



---

## Frontend

### Federated GraphQL Breakdown — Claims · Frontend

| | |
|---|---|
| **Client** | `pdex-ui-react` (Apollo Client) |
| **Backend subgraph** | `spark-claims (separate)` |
| **Total FE Stories** | 4 |
| **Impact** | 🔴 2 High · 🟡 2 Medium · 🟢 0 Low |
| **Estimated effort** | 17–27 days (single-engineer) |
| **Phase-1 surface** | 18 operation-to-root-field rows · 6 client files · 8 components |
| **Generated** | 2026-07-19 |

> A frontend story is **Done only after every backend story it depends on has been delivered**. Full story text (objectives, required changes, AC, testing) lives in fe-08-frontend-stories.md — the hand-authored source of truth; this page is the per-domain planning view.

---

#### What Are We Changing?

- Point the **Claims** GraphQL operations in `pdex-ui-react` at the federated router (subgraph `spark-claims (separate)`) behind the platform feature flag, then remove legacy-gateway assumptions (typenames, cache keys, fragments).
- Cutover is per-domain and reversible: dual-run first, flag flip after parity, legacy path kept until the exit criterion holds.

---

#### Stories

| Story | Title | Type | Impact | Effort | Depends on | Operations |
|---|---|---|---|---|---|---|
| `CLAIM-FE-001` | Split the claim fragment factory and re-target claim fragments | Refactor | 🟡 Medium | 2–3 days | — | — |
| `CLAIM-FE-002` | Migrate claim reads (first cross-subgraph cutover) | Query migration | 🔴 High | 6–10 days | `CLAIM-BE-B-01`, `CLAIM-BE-B-02`, `CLAIM-BE-B-03`, `CLAIM-BE-B-04`, `CLAIM-FE-001`, `PRODUCT-BE-H-06` | `getClaims`, `getClaimByIds`, `getCommunicationChannels`, `getAllClaimsAbout`, `getClaimComponentStatus` |
| `CLAIM-FE-003` | Migrate claim simple mutations and export | Mutation migration | 🟡 Medium | 4–6 days | `CLAIM-BE-D-01`, `CLAIM-BE-D-02`, `CLAIM-BE-D-03`, `CLAIM-BE-D-04`, `CLAIM-BE-D-05` | `createClaim`, `bulkUpdateClaim`, `lockClaim`, `unlockClaim`, `requestClaimExport` |
| `CLAIM-FE-004` | Migrate `updateClaim` multi-step write handling | Mutation migration (complex) | 🔴 High | 5–8 days | `CLAIM-BE-E-01` | `updateClaim` |

---

#### Recommended Implementation Order

> Staged from each story's dependencies: the backend phase its BE stories sit in (reads → search → writes → sagas) plus in-domain FE→FE chains. **Stories in the same step are independent of each other and parallelize.** ADR ratifications are entry gates, not ordering edges.

| Step | Stories (parallel set) | Waits for | Focus |
|---|---|---|---|
| 1 | 🟡 `CLAIM-FE-001` | — | Reads cutover — needs backend phase A/B reads live |
| 2 | 🔴 `CLAIM-FE-002` | `CLAIM-FE-002` → `CLAIM-BE-B-01`, `CLAIM-BE-B-02`, `CLAIM-BE-B-03`, `CLAIM-BE-B-04` (+1) | Search & listing — needs backend phase C |
| 3 | 🟡 `CLAIM-FE-003` | `CLAIM-FE-003` → `CLAIM-BE-D-01`, `CLAIM-BE-D-02`, `CLAIM-BE-D-03`, `CLAIM-BE-D-04` (+1) | Writes — needs backend phase D mutations |
| 4 | 🔴 `CLAIM-FE-004` | `CLAIM-FE-004` → `CLAIM-BE-E-01` | Complex writes / sagas — needs backend phase E + ADR ratification |

**Cutover flow:** `CLAIM-FE-001` → `CLAIM-FE-002` → `CLAIM-FE-003` → `CLAIM-FE-004`.

---

#### Recommended Story Graph — 1 Frontend Engineer

> The staged order map above, run by **one frontend engineer**. Steps re-sync at each stage because the stage's **backend gate** — not engineer availability — is the limiter.

| Step | 👤 FE-1 | Backend gate (focus) |
|---|---|---|
| 1 | 🟡 `CLAIM-FE-001` (2–3d) | Reads cutover — needs backend phase A/B reads live |
| 2 | 🔴 `CLAIM-FE-002` (6–10d) | Search & listing — needs backend phase C |
| 3 | 🟡 `CLAIM-FE-003` (4–6d) | Writes — needs backend phase D mutations |
| 4 | 🔴 `CLAIM-FE-004` (5–8d) | Complex writes / sagas — needs backend phase E + ADR ratification |

**Elapsed (nominal midpoints):** ~22 FE build days — calendar time is set by the backend gates, not FE capacity.

---

#### References

- fe-08-frontend-stories.md — full story text (source of truth).
- fe-09-story-dependency-matrix.md — FE ↔ BE dependency matrix.
- fe-10-migration-sequencing.md — program-level waves and external gates.
- fe-03-merged-inventory.md — every operation × backend root field for this domain.
- FederatedGqlBreakDown-claims.md — the combined Backend + Frontend breakdown this section lives in.

