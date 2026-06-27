# claims — Jira stories (paste one block per issue)

> **Epic:** Claims → claims DGS migration  ·  **Labels:** `dgs-migration`, `claims`, `<type>`
> Create the Epic first, then paste each block below as a new Story's description.
> Story points are AI-derived from complexity (confirm in refinement). See [README.md](./README.md).

## SPARK-CLM-A01 · Schema skeleton + DateTime scalar
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** —
**Labels:** `dgs-migration`, `claims`, `schema`

**Current Behaviour:** green-field; schema translated from `code/schemas/SPARK_Claims.txt`.
**Target:** federation v2.3 header, `scalar DateTime → Instant`, empty `extend type Query`/`Mutation`.
**Acceptance:** 1. `./gradlew generateJava` passes. 2. `DateTime` round-trips. **Tests:** ☐ compiles ☐ scalar serde.

---

## SPARK-CLM-A02 · Owned types + inputs
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A01
**Labels:** `dgs-migration`, `claims`, `schema`

**Target:** `Claims` (**`@key(fields:"humanId")`** — SDL has no `id`), the 7 value types, the ~9 inputs,
`@shareable CodeDescription` — per [03-schema.graphql](./03-schema.graphql). **Note:** `workspaceContext`
is `[ID]` on create but `PartialWorkspaceAssociationsInput` on update (preserve). **Acceptance:** 1. all types+inputs present; `@key=humanId`; nullability matches SDL. 2. validates. **Tests:** ☐ validates ☐ entity stub.

---

## SPARK-CLM-A03 · External stubs (Product + platform + sibling DGS)
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A01
**Labels:** `dgs-migration`, `claims`, `schema`

**Target:** `@extends @external` stubs — `Product`, `WorkspaceV2`, `UserProfileAttributes`,
`UserGroup_Participants`, `AccessControl`, `ResourcePermissions`, `ProductComponentStatus`, `TeamPaged`,
`VMM_BusinessPartner`. (All cross-subgraph — claims is its own DGS.) **Acceptance:** 1. compiles; gateway composes. **Tests:** ☐ compiles ☐ stub resolves.

---

## SPARK-CLM-A04 · ClaimService Kotlin port
**Type:** Story  ·  **Phase:** A  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A01
**Labels:** `dgs-migration`, `claims`, `service`

**Current Behaviour (Phase 2 §Service):** 13 REST methods on the claim base (2 unused: versions).
**Target:** Kotlin service; preserve create/update throw-on-error and the `bulkUpdateClaim` `status_code`
contract; **fix** `bulkUpdateClaim` to camelCase the response (source snake-cases it). **Acceptance:** 1. used methods present (POST, GET listing, GET /search, PUT /{humanId}, PUT /bulk-update, GET /communication-channels, GET/POST /export, GET /search/guest_facing_claim, PUT /{id}/lock|unlock, GET /claims-about). 2. bulk response camelCased. **Tests:** ☐ endpoint build ☐ bulk transform ☐ error contracts.

---

### Phase B — Core Reads

---

## SPARK-CLM-B01 · getClaims
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A02, SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `query`

**Current Behaviour (Q1):** (own) `claim.getClaims.load({parentHumanId, claimHumanIds, partnerIds})` `GET {base}` (filtered) → camelCase. **No ACL token.** **Target:** `@DgsQuery → [Claims]`. **Acceptance:** 1. filters by the 3 args. **Tests:** ☐ happy ☐ empty ☐ integration.

---

## SPARK-CLM-B02 · getClaimByIds
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A02, SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `query`

**Current Behaviour (Q2):** (ACL context) token → `GET {base}/search?claimIds={csv}`. **Target:** `@DgsQuery → [Claims]`. **Acceptance:** 1. returns claims for ids. **Tests:** ☐ happy ☐ empty.

---

## SPARK-CLM-B03 · getCommunicationChannels (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `query`

**Current Behaviour (Q3):** (own) `GET {base}/communication-channels`. **Target:** `@DgsQuery` → `@Cacheable` → `[CommunicationChannel]`. **Acceptance:** 1. returns channels; cached. **Tests:** ☐ list ☐ cache hit.

---

## SPARK-CLM-B04 · getAllClaimsAbout (cacheable)
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `query`

**Current Behaviour (Q4):** (own) `GET {base}/claims-about`. **Target:** `@DgsQuery` → `@Cacheable` → `[CodeDescription]`. **Acceptance:** 1. returns list; cached. **Tests:** ☐ list ☐ cache hit.

---

## SPARK-CLM-B05 · getClaimExports
**Type:** Story  ·  **Phase:** B  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `query`

**Current Behaviour (Q5):** (own) `GET {base}/export`. **Target:** `@DgsQuery → [ClaimExport]`. **Acceptance:** 1. returns export records. **Tests:** ☐ list.

---

### Phase C — Search & Listing

---

## SPARK-CLM-C01 · searchGuestFacing
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `query`

**Current Behaviour (Q6):** (own) `GET {base}/search/guest_facing_claim?{qs(queryParam)}` → camelCase. **Target:** `@DgsQuery → [Guest_Facing]`. **Acceptance:** 1. query-string built from `queryParam`. **Tests:** ☐ search ☐ empty.

---

## SPARK-CLM-C02 · getClaimsElastic
**Type:** Story  ·  **Phase:** C  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `query`

**Current Behaviour (Q7):** (🔴 search) `search.getClaimsElastic.load({ q:"parentId: {parentHumanId}" })`. **EXT:** 🔴 search. **Target:** `@DgsQuery → [Claims]` via the search subgraph/client. **Acceptance:** 1. `parentId:` elastic query built. **Tests:** ☐ query build ☐ parity.

---

### Phase D — Mutations (simple)

---

## SPARK-CLM-D01 · createClaim (throws on validationErrors)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `mutation`

**Current Behaviour (M1):** (own) `POST {base}` (snake_case). **If `validationErrors`/`message` → throw.** **Target:** `@DgsMutation → [Claims]`; port throw-on-error. **Acceptance:** 1. creates claim(s). 2. validation error → exception. **Tests:** ☐ create ☐ validation-error→throw.

---

## SPARK-CLM-D02 · bulkUpdateClaim (status_code contract; fix snake-case response)
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `mutation`

**Current Behaviour (M3):** (own) `PUT {base}/bulk-update`. **Error contract:** result is array → return; `status_code>400` → throw; else throw "unhandled". **Latent:** source snake-cases the response — **fix to camelCase**. **Target:** `@DgsMutation → [Claims]`. **Acceptance:** 1. array result returned (camelCase). 2. error status → exception. **Tests:** ☐ bulk ☐ error status ☐ camelCase.

---

## SPARK-CLM-D03 · requestClaimExport
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `mutation`

**Current Behaviour (M4):** (own) `POST {base}/export` → `response.request_id`. **Target:** `@DgsMutation → String`. **Acceptance:** 1. returns the request id. **Tests:** ☐ request.

---

## SPARK-CLM-D04 · lockClaim
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `mutation`

**Current Behaviour (M5):** (ACL context) token → `PUT {base}/{claimId}/lock`. **Target:** `@DgsMutation → Claims`. **Acceptance:** 1. locks the claim. **Tests:** ☐ lock.

---

## SPARK-CLM-D05 · unlockClaim
**Type:** Story  ·  **Phase:** D  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `mutation`

**Current Behaviour (M6):** (ACL context) token → `PUT {base}/{claimId}/unlock`. **Target:** `@DgsMutation → Claims`. **Acceptance:** 1. unlocks the claim. **Tests:** ☐ unlock.

---

### Phase E — Complex Operations

---

## SPARK-CLM-E01 · updateClaim (proxy ACL + workspace + body, non-atomic)
**Type:** Story  ·  **Phase:** E  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `mutation`

**As a** DGS engineer **I want** the multi-step claim update with a failure strategy **so that** workspace
and body changes stay consistent.
**Current Behaviour (M2):** 1) `getUserPermissionsJWTByProxy({id:humanId, proxyIds:[parentId],
basePermissions:true})` (proxy/external ACL path — context only); 2) if `workspaceContext.{add,remove}`
non-empty → `workspaceAssociationHelper(CLAIM, humanId, add, remove)`; 3) `PUT {base}/{humanId}`;
4) **throw on `validationErrors`/`message`**. No rollback.
**EXT:** 🟡 workspaceV2. **Target:** ordered steps + chosen failure strategy (**PO decision**). The proxy
ACL is **context-only** (note it; build nothing). **Acceptance:** 1. workspace assoc runs when present. 2. body update + throw-on-error. 3. partial-failure strategy. **Tests:** ☐ body-only ☐ +workspace ☐ validation-error→throw ☐ partial-failure ☐ parity.

---

### Phase F — Federation Contributions (BLOCKED-BY product)

---

## SPARK-CLM-F01 · Product.claims (federation contribution)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `field-resolver`

**Target:** `extend type Product @key(fields:"id") { claims(partnerIds:[String], includeClaims:Boolean): [Claims] }` with a `@DgsEntityFetcher`; the claims subgraph fills `Product.claims` over the gateway. **BLOCKED-BY:** the `Product` entity existing (plm-product Phase A). **Acceptance:** 1. `Product.claims` resolves via federation. 2. parity vs the current in-gateway resolver. **Tests:** ☐ field resolves ☐ parity.

---

## SPARK-CLM-F02 · ResourcesCount.claims (TechPack — see SPARK-PROD-F05)
**Type:** Story  ·  **Phase:** F  ·  **Complexity:** Low  ·  **Points (est.):** 2  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `field-resolver`

**Target:** `extend type ResourcesCount @key(fields:"productId partnerId") { claims: [ID] }` with a
`@DgsEntityFetcher`; fills the TechPack `claims` count. **BLOCKED-BY:** product TechPack facade
(`SPARK-PROD-E03`/`F05`). **Acceptance:** 1. field resolves on the federated `ResourcesCount`; parity vs facade. **Tests:** ☐ field resolves ☐ parity.

---

### Phase G — Field Resolvers & Tests

---

## SPARK-CLM-G01 · access + currentUserPermissions + participantDetails
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A02, SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `field-resolver`

**Current Behaviour:** `access` → `accessControl.getPermissions([humanId])[0]`; `currentUserPermissions`
→ `getUserAccessUnencoded(humanId)[0]`; `participantDetails` → `getUserGroup(humanId)`. (ACL context.) **Acceptance:** 1. each resolves; null-safe. **Tests:** ☐ access ☐ perms ☐ participants.

---

## SPARK-CLM-G02 · createdBy + updatedBy + businessPartner + designPartner (3-way fallback)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `field-resolver`

**Current Behaviour:** users via 🟡 user-profile; `businessPartner` **3-way fallback** (`partnerId` ||
`{bpId:0,bpName:'Target'}` when no `dpPartnerId` || `dpPartnerId`); `designPartner` `dpPartnerId` or
`{bpId:null,bpName:null}`. **Target:** preserve every branch exactly. **Acceptance:** 1. all 3 BP branches correct (incl. `bpId:0` Target). 2. null id → null user. **Tests:** ☐ partnerId ☐ dp fallback ☐ Target(0) ☐ users.

---

## SPARK-CLM-G03 · product + parentDetails (otherClaimBps/systemTeams/droppedPartnerIds)
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** High  ·  **Points (est.):** 5  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `field-resolver`

**Current Behaviour:** `product` (🟡 product, only if `parentId` starts `'PID'`); `parentDetails` →
`product.getByID(parentId)` (the product feeds `ParentDetails`): `otherClaimBps` (🔴 search
`getClaimsElastic` → partner ids), `systemTeams` (🔴 search `searchTeams` from product BPs; empty→`{content:[]}`),
`droppedPartnerIds` (direct). **Target:** federated product reference + search. **Acceptance:** 1. `product` null when not `PID*`. 2. `otherClaimBps`/`systemTeams` elastic queries match source; empty-BP → `{content:[]}`. **Tests:** ☐ product branch ☐ otherClaimBps ☐ systemTeams ☐ empty BPs.

---

## SPARK-CLM-G04 · workspaces + substantiatedBy + claimDetails.claimName
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-A04
**Labels:** `dgs-migration`, `claims`, `field-resolver`

**Current Behaviour:** `workspaces` (🟡 workspaceV2 by `workspaceContext`); `substantiatedBy`
(🟡 user-profile); `ClaimDetails.claimName` = `guestFacingClaim` (computed). **Acceptance:** 1. each resolves; `workspaces` null when empty. 2. `claimName` mirrors `guestFacingClaim`. **Tests:** ☐ workspaces ☐ substantiatedBy ☐ claimName.

---

## SPARK-CLM-G05 · Tests, parity harness
**Type:** Story  ·  **Phase:** G  ·  **Complexity:** Medium  ·  **Points (est.):** 3  ·  **Depends on:** SPARK-CLM-B01, SPARK-CLM-E01, SPARK-CLM-G02, SPARK-CLM-G03
**Labels:** `dgs-migration`, `claims`, `tests`

**Target:** ≥80% unit coverage; parity fixtures (incl. `updateClaim` proxy path, `bulkUpdateClaim`
camelCase fix, the `businessPartner` 3-way fallback, `parentDetails` elastic lookups); contract test
(schema diff intentional-only). **Acceptance:** 1. unit ≥80%. 2. parity green. 3. schema-diff intentional. **Tests:** ☐ parity ☐ contract.

---

## 4. Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| `updateClaim` proxy-ACL multi-step partial failure (E01) | Medium | High | Saga / compensation — PO decision | Tech Lead + PO |
| `bulkUpdateClaim` snake-cased response (likely bug) (D02) | Medium | Medium | Fix to camelCase; parity test | Backend Eng |
| `businessPartner` 3-way fallback regressions (G02) | Low | Medium | Unit-test each branch incl. Target(0) | Backend Eng |
| `ParentDetails` elastic team/BP lookups (G03) | Low | Medium | Preserve empty handling; paginate | Backend Eng |
| Federation contributions wait on product (F01/F02) | Low | Low | Post-launch; not on critical path | Architect |

## 5. Summary
- **Stories:** 24 (A:4 · B:5 · C:2 · D:5 · E:1 · F:2 · G:5).
- **Critical path:** A01→A02/A04→E01→G02/G03→G05.
- **Highest risk:** `updateClaim` (E01); the `bulkUpdateClaim` transform bug (D02).
- **Separate subgraph:** claims contributes `Product.claims` + TechPack `ResourcesCount.claims` (Phase F).

---
**Phase Completed:** Phase 4 — Migration Stories · **Domain:** `claims` · **Outputs:** 04-stories.md, 04-stories-index.yaml, 04-po-summary.md.

---
