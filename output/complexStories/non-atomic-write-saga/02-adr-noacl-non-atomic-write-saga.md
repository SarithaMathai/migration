# ADR-013-noACL (draft) — Non-Atomic Multi-Step Writes / WriteSaga under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-non-atomic-write-saga.md` (ADR-013) — read that first; this ADR re-scores it under
> one changed premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The DGS / orchestration layer makes **no**
> ACL calls: no capability JWTs, no proxy JWTs, no permission writes.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option B (shared `WriteSaga`, per-step declared policy) remains the proposal.
> The saga survives because the *steps that can strand a resource* — assoc vs body vs attachments vs
> fan-out — are domain writes, not ACL calls. Only the policy table shrinks.

---

## 1. What the assumption removes, write by write

| Mutation | ACL today | Under domain-ACL |
|---|---|---|
| `updateBom` | capability JWT ① · `bom.updatePermissions(permissionJWT)` ④ ✗? | JWT **gone**; the permissions update is a **bom-service write** — the bom service does its own ACL write when it processes `businessPartners`; ideally folds into the body PUT (see pin-down N2) |
| `updateMeasurement` | capability JWT ① | **gone** — pure 2-step saga remains (assoc → body) |
| `updatePackaging` | JWTs before archive / attrs | **gone** — steps and their broken ordering 🐞 remain |
| `updateProductDetailsSet` | capability JWT ① | **gone** — destructive-before-body 🐞 remains |
| `updateWatchlistEntries` | 🐞 JWT fetched even when archive list empty | **gone** (the wasted fetch with it) — the unawaited map race 🐞 remains |
| `updateClaim` | **proxy JWT** ① — permissions borrowed from the parent product | **verify, then drop** — proxy authorization ("claim inherits parent product's permissions") is the **claim service's** concern; confirm its existing ACL integration applies the rule, then the resolver's proxy JWT drops as duplication (pin-down N1) |
| `updateComponentStatuses` | none in the resolver | unaffected — 5-domain parallel fan-out 🐞s remain |

- Net effect on the grid: the **ACL column empties**, every sequence loses its JWT prelude — but every row
  keeps ≥ 2 ordered cross-service writes. The disease of the 01 ADR (early step commits, later step fails,
  nothing detects it) is completely unaffected by who calls ACL.

## 2. Impact on decision drivers

- Unchanged: multi-backend steps, interactive save clicks, cheap-inverse asymmetry, ADR-012's dependency
  on a shared `WriteSaga`.
- New: the **claim proxy-permission rule** is the one place to verify rather than assume — see pin-down N1.
- Clarification: every domain service **already integrates with ACL** — the assumption removes the
  orchestrator's *duplicate* ACL layer (JWT preludes minted on top of authorization the services perform
  anyway). No ACL capability is being added to any backend.

## 3. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Full compensating saga | unchanged — inverses still don't exist for the hard steps | over-engineered | unchanged |
| B | Shared `WriteSaga`, per-step policy | policy table loses its "ACL / permissions after body → RETRY" row; steps get simpler (no JWT preludes); everything else identical | **recommended** | **recommended — unchanged** |
| C | Best-effort | unchanged — still fails the stories' own AC | rejected | unchanged |
| D | Backend-composed atomic endpoints | unchanged in substance — composing assoc + body + permissions into one transactional endpoint is still per-edge backend work the assumption does not schedule (domains already have their ACL integration; nothing new rides along); for bom/measurement/claim/productDetails (all product-family backend) it would collapse the saga to one call, but it still does nothing for cross-backend steps (attachment archive, relationship links) | per-edge refinement, later | unchanged — per-edge refinement, later |

## 4. Proposed decision — no change

- **Option B** stands: one shared `WriteSaga`, per-step declared policy, legacy step order preserved.
- Revised default policy table (delta from 01 §4-B):

| Step kind | Policy | Change |
|---|---|---|
| workspace associate / dissociate | `COMPENSATE` | unchanged |
| relationship add / remove | `COMPENSATE` | unchanged |
| body PUT | point of no return | unchanged — and where the domain folds its ACL write into the body (pin-down N2), stale-ACL states become **impossible by construction** for that edge |
| ~~ACL / permissions after body~~ | ~~RETRY then PARTIAL_FAILURE~~ | **row deleted** — no orchestrator-level ACL step exists; a separate `updatePermissions`-style domain call, where it survives, is just another domain write: `RETRY` then `PARTIAL_FAILURE` |
| attachment archive / attrs | `RECORD` + reconcile | unchanged |
| parallel fan-out branches | isolate + aggregate | unchanged |

- **Option D stays a recorded per-edge refinement** (unchanged from 01): every edge that becomes
  single-backend-composable replaces its saga steps with one call.
- Build order unchanged: `WriteSaga` in Sprint 0, `updateMeasurement` pilots.

## 5. Pin-downs affected (vs 01 §5)

| 01 # | Item | Under domain-ACL |
|---|---|---|
| 1 | Compensation inventory | unchanged, minus ACL inverses (no longer the saga's problem) |
| 2–4 | watchlist race · packaging late check · componentStatuses DTO | unchanged |
| 5 | Unchecked responses | `bom.updatePermissions` check moves inside the bom service; claim-assoc and pdtl-body checks unchanged |
| 6–8 | result surface · parallel fan-out · sample mutations | unchanged |
| new N1 | **Claim proxy permissions** | verify the claim service's **existing** ACL integration already applies the parent-product proxy rule (the `getUserPermissionsJWTByProxy` semantics); if it does, the resolver's proxy JWT was pure duplication and drops cleanly — if not, that single gap is closed before cutover |
| new N2 | Permission-update folding | per product-family endpoint, decide: separate permissions call (saga step) vs folded into the body write (preferred — atomic); record per edge |

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes.*
