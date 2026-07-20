# ADR-019 (draft) — Capability-Token Handling for Cross-Domain Resolver Calls

> **Status:** 🔴 Proposed — draft for review
> **Scope:** the 31 **downstream-token** ACL call sites found across all 8 phase-1 domains — where a
> resolver mints a capability token (`getUserPermissionsJWT`) and hands it to a **different** domain's
> loader call. Permission-check (15 sites) and own-domain-token (35 sites) call sites are unaffected by
> this ADR — they stay resolver-local, exactly as the existing "ACL is context-only" note already says.
> **Related:** every domain's `be-03-schema.graphql` ACL header note and `be-04-stories.md` ACL note
> (this ADR **supersedes** those, pending ratification — doc edits are a separate follow-up, not bundled
> here) · `output/analysis/aclResearch/00-acl-usage-inventory.md` (the full findings this ADR is built on)
> · each domain's `be-07-acl-usage-analysis.md`.
> **Evidence:** `code/utils/commonLoaders.txt` (`getUserPermissionsJWT`), `code/utils/accessControlUtils.txt`
> (`getToken`, `getAccessControlBatch`), `code/resolvers/**/*.txt` (31 downstream-token sites, enumerated
> below) at `https://github.com/XXX`.

---

## 1. Today's behavior, evidence

### How the legacy gateway does it

`code/utils/accessControlUtils.txt` mints a capability token per request:
```
export const getToken = async (ids, headers, logContext) => {
  const serviceUrl = `${process.env.ACCESS_CONTROL_ENDPOINT}/.../permissions/user/current`
  const response = await fetch(serviceUrl, { method: 'POST', body: JSON.stringify(ids), headers })
  return response.text()   // <- the capability token
}
```
`commonLoaders.getUserPermissionsJWT(ids, ctx)` wraps this per-resolver. The 31 downstream-token sites
follow one shape: mint a token scoped to the current resource's ids, then pass it as an argument into
**another** domain's `ctx.loaders.<key>` call, so the downstream domain's own REST call carries the
caller's actual permission scope (the `SPARK-Capability-Token` header), not a service-account credential.

### Every downstream-token site (from be-07, by domain)

| Domain | Resolver | Target domain/service | Target kind |
|---|---|---|---|
| product | `Mutation.addProduct` | `workspaceV2` | sibling-dgs |
| product | `Mutation.addProducts` | `workspaceV2` | sibling-dgs |
| product | `Mutation.addProducts` | `attachment` | sibling-dgs (`plm-attachment`) |
| product | `Mutation.updateProduct` ×2 | `attachment` | sibling-dgs (`plm-attachment`) |
| product | `Mutation.productBusinessPartnerActions` | `sampleV2` | sibling-dgs |
| product | `SPARK_Product.associateProductsAsks` | `productAsk` | sibling-dgs (co-located) |
| product | `SPARK_Product.teams` | `teamV2` | sibling-dgs |
| product | `SPARK_Product.variations` | `productVariation` | sibling-dgs (co-located) |
| bom | `SPARK_BomWashMaterial.libraryResource` | `wash` | sibling-dgs |
| bom | `SPARK_BomImpressionDetails_Unified.libraryResource` | `search` | sibling-dgs (elastic) |
| bom | `SPARK_BomFabricLibraryImpressionDetails.libraryResource` | `search` | sibling-dgs (elastic) |
| bom | `SPARK_BomTrimLibraryImpressionDetails.libraryResource` | `search` | sibling-dgs (elastic) |
| bom | `SPARK_BomMaterialSearchResult.fabric` | `fabric` | sibling-dgs |
| bom | `SPARK_BomMaterialSearchResult.relatedMaterials` | `search` | sibling-dgs (elastic) |
| productDetails | `Mutation.updateProductDetailsSet` | `attachment` | sibling-dgs (`plm-attachment`) |
| productDetails | `Mutation.cloneFilesForProductDetails` | `attachment` | sibling-dgs (`plm-attachment`) |
| packaging | `Mutation.updatePackaging` ×2 | `attachment` | sibling-dgs (`plm-attachment`) |
| packaging | `Mutation.cloneFilesForDielines` | `attachment` | sibling-dgs (`plm-attachment`) |
| packaging | `SPARK_Dieline.attachment` | `attachment` | sibling-dgs (`plm-attachment`) |
| watchlist | `Mutation.updateWatchlistEntries` | `attachment` | sibling-dgs (`plm-attachment`) |
| watchlist | `Mutation.cloneFilesForWatchlist` | `attachment` | sibling-dgs (`plm-attachment`) |

Full table with per-site recommendation: `output/analysis/aclResearch/00-acl-usage-inventory.md` §"All
Downstream-Token Call Sites". `measurement`, `impression`, and `claims` had 0 downstream-token sites
(their ACL usage is entirely permission-check / own-domain-token — the existing "context-only" note
already holds for them).

### The mechanism available today

`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)` can be called from within the
application (e.g. after fetching a new capability token during request processing) to refresh the
current thread's security context **without re-authenticating**. It is not currently wired to any of
the 31 sites, and no story references it.

---

## 2. Decision drivers

- The existing "ACL is context-only, ignored" note is a **program-level working decision** already baked
  into every domain's be-03/be-04 docs — this ADR does not overturn it wholesale, it **narrows its scope**
  to the two kinds where it's actually true (permission-check, own-domain-token) and supplies the missing
  decision for the third kind (downstream-token).
- `plm-product` hosts 7 of the 8 phase-1 domains as one subgraph (product, bom, measurement,
  productDetails, watchlist, packaging, impression); `claims` is its own subgraph (`spark-claims`).
  Domain stitching happens in the federated gateway, not inside any one domain's service — so a
  downstream-token call in the legacy monolith becomes, post-migration, either (a) an in-process call
  within the same `plm-product` JVM (if the target is also co-located) or (b) a real cross-subgraph
  network call resolved by the gateway (if the target is `spark-claims`, a later-phase sibling DGS, or an
  external platform). The resolution must hold for both shapes.
- Correctness: dropping the token on a downstream-token call is an authorization regression, not a no-op
  — the target domain's REST call today validates against the calling user's actual permission scope.
- Consistency with the existing complex-case pattern: other ADRs (011–018) already record where ACL
  responsibility sits per case; this ADR is the first to give the **general** cross-domain-token answer
  the others deferred to "context-only, ignored."

### Assumptions, constraints & success criteria

**Assumptions**
- `SparkSecurityService.updateCurrentUserPermissions(capabilityToken)` is available to call from any DGS
  service in the `plm-product`/`spark-claims` estate (not gateway-only) — confirm with the platform team
  before ratification; this is the one unverified premise the whole recommendation rests on.
- The capability token minted for the current resource's ids (`getUserPermissionsJWT` equivalent) is
  sufficient scope for the downstream call — the legacy code already assumes this (same token, same ids,
  passed straight through); no widening of scope is being proposed.
- External-platform-stub targets (none among the 31 sites currently, all resolve to sibling DGS domains)
  would use gateway auth passthrough instead — recorded for completeness, not exercised by today's
  21-row table above.

**Constraints**
- Must not require re-authenticating the user (no login round-trip mid-request) — Mid-Request ACL Update
  exists specifically to avoid this.
- Must not silently drop the token (the failure mode this ADR is written to prevent).
- Must not widen or narrow the permission scope the legacy code already grants — parity first, any
  scope change is a separate product decision.

**Success criteria (measurable)**
- Every one of the 31 downstream-token sites has a named resolution (Mid-Request ACL Update or the
  gateway-passthrough alternative) recorded in its domain's migration story, not just in this ADR.
- A fixture/integration test proves the downstream call carries the refreshed capability token (not a
  service-account credential) for at least one sibling-DGS case (`attachment`, the most common target —
  9 of the 31 sites) and one co-located case (`workspaceV2`/`productAsk`/`productVariation`/`teamV2`).
- be-03/be-04 ACL language is corrected (separate follow-up pass) to read: *"ACL is context-only for
  permission-check and own-domain-token call sites (see ADR-019); downstream-token call sites use
  Mid-Request ACL Update — see ADR-019 for the full list."*

---

## 3. Options

| | Option | Mechanism | Re-auth needed? | Verdict |
|---|---|---|---|---|
| A | Drop the token (current instruction, literal) | none | — | rejected — authorization regression, this ADR exists because A is wrong for these 31 sites |
| B | Mid-Request ACL Update | `SparkSecurityService.updateCurrentUserPermissions(capabilityToken)` refreshes the thread's security context before the downstream call | No | **recommended** for sibling-DGS/phase-1-domain targets (all 31 current sites) |
| C | Gateway auth header passthrough | the gateway forwards the original request's auth header to every subgraph; no per-call token minting | No | recommended only for external-platform-stub targets (none today, kept for completeness/future sites) |
| D | Per-call re-authentication | downstream domain independently re-validates the caller against the access-control endpoint | Yes (implicit — a fresh permission check per call) | rejected — duplicates the token-mint the legacy code already does once per resolver; adds latency with no parity benefit |

### A — Drop the token (current instruction, literal)

- What every domain's be-03/be-04 currently implies: capability-token usage is context-only, port nothing.
- ➕ simplest possible port — zero ACL plumbing.
- ➖ **wrong for downstream-token sites** — the target domain's REST call validates against the caller's
  permission scope today; dropping the token either fails the call (401/403) or falls back to an
  over-privileged service-account credential. This is the defect this ADR exists to close.

### B — Mid-Request ACL Update ⭐ (recommended for the 31 sites found)

- After the resolver mints/receives the capability token for the current resource's ids, call
  `SparkSecurityService.updateCurrentUserPermissions(capabilityToken)` to refresh the current thread's
  security context, then make the downstream call (in-process for co-located targets, over the wire for
  sibling DGS/`spark-claims`) — the downstream service reads the refreshed context exactly as it does
  today when a request arrives with a valid capability token.
- ➕ no re-authentication round-trip · matches the legacy token-scoping exactly (same ids, same token) ·
  works identically whether the target ends up co-located in `plm-product` or federated to a separate
  subgraph — the mechanism doesn't change when a lane flips from in-process to gateway-routed (same
  facade-then-federate phasing other ADRs already use, applied to auth instead of data).
- ➖ unverified premise: needs platform-team confirmation that `SparkSecurityService` is callable from
  DGS services, not gateway-only (pin-down 1) · adds one call per downstream-token resolver (31 sites) —
  acceptable, it replaces work the legacy code already did via `getUserPermissionsJWT`.

### C — Gateway auth header passthrough

- The federated gateway forwards the original request's auth header to every subgraph it calls; no
  domain mints or refreshes a token itself.
- ➕ zero per-domain ACL code · simplest for external-platform-stub targets, which don't participate in
  Mid-Request ACL Update at all.
- ➖ doesn't match today's shape for the 31 sites, where the token is scoped to specific **ids**
  (`getUserPermissionsJWT(ids, ctx)`), not just "the calling user" — a bare header passthrough loses that
  id-scoping unless the downstream service re-derives it, which is extra work C doesn't actually save.
  Recorded as the answer for platform-stub targets (VMM/IG/Doppler/etc.) if any future downstream-token
  site targets one — none do today.

### D — Per-call re-authentication

- Downstream domain calls the access-control endpoint itself on every incoming request, ignoring any
  token the caller supplies.
- ➕ downstream domain owns its own authorization decision fully.
- ➖ duplicates the mint the caller already did · adds a network round-trip per call on top of the actual
  business call · no evidence the legacy code needs this (it works today with token passthrough) —
  rejected as unnecessary complexity.

---

## 4. Proposed decision (to ratify)

- **Option B — Mid-Request ACL Update** for all 31 downstream-token sites, since every one targets a
  phase-1 co-located domain or a sibling DGS (`plm-attachment`, `plm-sample`, or a later-phase
  `plm-*`/`team` subgraph) — never today an external platform stub.
- **Option C recorded** as the answer if a future downstream-token site ever targets an external platform
  stub (VMM/IG/Doppler/etc.) — not exercised by any of today's 31 sites, kept for completeness.
- **Option A (drop the token) is explicitly rejected** for these 31 sites — it remains correct only for
  the 50 permission-check/own-domain-token sites, where the existing "context-only, ignored" note stays
  true and unchanged.

### Pin-downs at ratification

| # | Item | Choice to make | Draft recommendation |
|---|---|---|---|
| 1 | `SparkSecurityService` callable from DGS services? | confirm with platform team | blocking — Option B's premise; if false, fall back to Option D for the affected targets only |
| 2 | Token scope on refresh | same ids as the legacy `getUserPermissionsJWT(ids, ctx)` call, or the full-resource scope | preserve exactly — same ids, no widening (parity first) |
| 3 | Per-story wiring | one story per domain's downstream-token sites, or fold into each site's existing entity-resolver/federation story | fold into the existing story for that resolver — avoids a second story touching the same code; add "Mid-Request ACL Update before the downstream call" as an explicit acceptance-criteria line |
| 4 | `attachment` concentration | 9 of 31 sites target `attachment` (`plm-attachment`) — worth a shared helper? | yes — one `refreshAndCallAttachment(...)` helper in `plm-product`/`plm-productDetails`/`plm-packaging`/`plm-watchlist` avoids 9 copies of the same refresh-then-call pattern |
| 5 | Doc supersession | when does be-03/be-04 ACL language get corrected? | separate follow-up pass, after this ADR ratifies — do not bundle into the ADR acceptance itself (per program decision, 2026-07-17) |

---

## 5. Consequences

- If accepted:
  - 31 resolvers across 6 domains (product, bom, productDetails, packaging, watchlist — measurement/
    impression/claims have zero downstream-token sites) gain one line each: a
    `SparkSecurityService.updateCurrentUserPermissions(capabilityToken)` call before the downstream
    domain call, wired into each site's existing migration story rather than a new story per site.
  - The "ACL is context-only, ignored" note in every domain's be-03/be-04 is corrected to name the
    exception explicitly, with a link to this ADR and the aclResearch roll-up.
  - Future domains added to the program get the same three-way classification (permission-check /
    own-domain-token / downstream-token) via `generate_acl_analysis.py` — no new judgment call needed,
    the generator already does this.
- Risks:
  - Pin-down 1 (platform-team confirmation) is a hard blocker — if `SparkSecurityService` turns out to be
    gateway-only, Option B needs re-scoping to Option D for the affected call paths before this ADR can
    ratify as written.
  - The `attachment`-domain concentration (9/31 sites) means any change to the shared refresh helper
    (pin-down 4) touches product, productDetails, packaging, and watchlist simultaneously — coordinate
    the helper's contract before any one domain starts its story.

---

## 6. On acceptance

Per `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md`:

1. Confirm pin-down 1 with the platform team; adjust the decision if `SparkSecurityService` is gateway-only.
2. Save the write-up in `adrs/`; record the decision (status, chosen option) alongside the other ADRs.
3. Flip `00-overview.md` §2 to **Decided**.
4. In each affected domain's `output/analysis/{domain}/be-04-stories.md`, add the Mid-Request ACL Update
   acceptance-criteria line to the story that already touches each downstream-token resolver (pin-down 3)
   — do not create 31 new stories.
5. Correct the "ACL is context-only, ignored" note in every domain's `be-03-schema.graphql` header and
   `be-04-stories.md` ACL note (separate pass, per pin-down 5) — link to this ADR.
6. Regenerate: `python fedMigrationScripts/generatescripts/generate_all.py` (refreshes domain docs, Jira
   CSVs, program overview) and re-run `generate_acl_analysis.py` to confirm the downstream-token count
   in the roll-up now matches stories with the acceptance-criteria line added.
