# ADR-012-noACL (draft) — Partner Drop/Undrop + Ownership under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-partner-drop-undrop.md` (ADR-012) — read that first; this ADR re-scores it under
> one changed premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The orchestrator makes **no** ACL calls:
> no `filterResourcesByPartner` batch reads, no permission maps, no capability JWTs, no
> `dropPartnerFromResources` bulk call.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option B (owner-orchestrated saga + participant contract) remains the
> proposal. The assumption *tightens* B's constraints (revocation is now distributed) and makes
> A and D strictly worse — it does not open space for a different option.

---

## 1. What the assumption removes — and what it redistributes

| Today (DGS layer) | Under domain-ACL |
|---|---|
| `filterResourcesByPartner` — ACL batch read (chunks of 100) over every walked id | **gone** — each participant filters to "children the partner is actually on" itself, inside its drop endpoint |
| `getPermissionMapForBulkACLCall` — per-resource dropped-permission map (`Bps`/`Dps`/`MerchVendor`/`FabricSupplier`/`Ids`) | **moves** — each domain builds and applies the permission delta for **its own** resources |
| capability JWT for product + surviving ids + `SAMPLE_EVALUTION` | **gone** |
| `accessControl.dropPartnerFromResources` / `unDropPartnerFromResources` — **one bulk call revoking everything** | **redistributed** — becomes N per-participant revocations (sample service revokes sample ACLs, attachment service attachment ACLs, …) |
| `REMOVE_PARTNER` step 5 ACL token | **gone** |

- ⚠ **The critical consequence:** today, access revocation has a single choke point — one bulk ACL call
  either happened or didn't. Under domain-ACL, revocation is **inherently partial-state**: sample ACLs may
  be revoked while attachment ACLs still grant. This is not a reason to reject the assumption — it is the
  reason the saga's per-step visibility and the ordering constraint below become **mandatory**, not
  nice-to-have.
- Unaffected: the retiring relationship walk (replaced by per-participant enumeration, as in 01),
  the `UserProfileAttributes` resolver import kill, activity cleanup, the design-partner branch,
  `REMOVE_TEAM` staying a plain mutation.

## 2. Impact on decision drivers

- *"Access revocation is synchronous today"* — still the governing driver, now stricter: success may only
  be returned when **every participant** (hence every ACL slice) has revoked, because there is no single
  bulk call to anchor the guarantee on.
- The participant contract (01's core idea) and the domain-ACL decision are the **same obligation stated
  twice**: "enumerate your children, apply the partner change to them *including their ACL*". The global
  decision effectively pre-ratifies half of Option B.
- Every participant already integrates with ACL — the per-domain build is the **drop/undrop endpoint**
  (enumeration + applying the partner delta through its existing ACL integration), not new ACL capability.
- The workspace twin inherits identically.

## 3. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Lift-and-shift dispatcher | **strictly worse** — the dispatcher can no longer even do the fan-out as written (its ACL steps are forbidden); invisible mid-flight failure now means invisible *partial access revocation* | viable | no longer viable — the invisible-failure problem is now a security problem |
| B | Owner-orchestrated saga + participant contract | participant endpoints absorb their own enumeration + ACL delta; the orchestrator loses steps 2–4 and the bulk ACL calls; per-step `PARTIAL_FAILURE` visibility becomes the *only* way to know revocation completed everywhere | **recommended** | **recommended — unchanged, now effectively forced** |
| C | Central partner-lifecycle service | **contradicts the assumption outright** — a central service doing everyone's revocation is exactly the cross-domain ACL handling the global decision abolishes | rejected | rejected — now by construction |
| D | Event choreography | worse on **every dimension that disqualified it in 01**, even if median revocation latency might improve (N small parallel revocations vs one bulk call): the worst-case window is now bounded by the *slowest* of N consumers instead of one · a half-dropped partner (samples revoked, attachments still visible) becomes the normal in-flight state on every drop, not a failure mode · verifying "fully revoked" requires a cross-domain audit instead of one consumer's lag metric | disqualified for drop | disqualified — more firmly |

## 4. Proposed decision — no change

- **Option B** stands, with the participant contract upgraded:
  - each participant's drop/undrop endpoint = **enumerate own children of X the partner is on → apply the
    partner change → apply the ACL delta for those children** — one atomic-as-possible unit per domain,
  - the orchestrator (`plm-product` / `plm-workspace`) runs participants through `SPIKE-01`'s
    `WriteSaga` and returns success **only when all participants report revoked**,
  - **ordering constraint (revised from 01 §4):** on drop, *all participant drop steps* must complete
    before the mutation returns success (there is no longer a single ACL step to sequence); on undrop,
    participants restore before their resources become visible — each participant owns that ordering
    internally (restore ACL last... i.e. resource first, grant second),
  - `REMOVE_TEAM` still excluded; `REMOVE_PARTNER`'s activity cleanups (recentlyViewed/todo/favorite)
    are unchanged participants.
- **Option D** stays recorded for the non-security cleanup steps only (activity, profile) — unchanged.

## 5. Pin-downs affected (vs 01 §4)

| 01 # | Item | Under domain-ACL |
|---|---|---|
| 1 | Relationship traversal replacement | unchanged in direction, stronger in force — per-participant enumeration is now the only ACL-consistent source |
| 2 | `UserProfileAttributes` import | unchanged — client call as a saga step |
| 3 | Per-step failure policy | revised: partner-status write — compensate · **each participant drop (incl. its ACL delta) — retry then fail the mutation** · activity/profile — retry + reconcile, never fail |
| 4 | Async refinement scope | unchanged — never partner status; "never ACL" now reads "never any participant's drop step" |
| 5–6 | design-partner branch · dispatcher shape | unchanged |
| 7 | Error convention | unchanged, more important — `PARTIAL_FAILURE` per-step detail is now the audit trail for partially-revoked access |
| new N1 | Participant revocation atomicity | each domain must apply "resource change + ACL delta" as one unit (or ACL-first on drop / ACL-last on undrop); specify in the participant contract and test per domain |
| new N2 | Revocation completeness audit | a reconcile job (or fixture-backed check) that verifies no ACL grant survives for a dropped partner across all participants — replaces the implicit guarantee the single bulk call used to give |

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes. The participant contract here and ADR-016-noACL's lane contract are the
write and read faces of one per-domain obligation — agree them as one contract per domain team.*
