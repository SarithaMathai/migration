# ADR-018-noACL (draft) — `attachmentsWithMetaData` enrichment under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-attachments-enrichment.md` (ADR-018) — read that first; this ADR re-scores it under one changed premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The DGS / orchestration layer makes **no**
> ACL calls: no capability tokens, no viewer-permission lookups, no grantee joins.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option A (owner-computed enrichment over a shared library) remains the proposal.

---

## 1. What the assumption removes from this case

ACL touchpoints in today's flow (per 01 §1) and where they go:

| Today (DGS layer) | Under domain-ACL |
|---|---|
| 2 capability tokens (`getUserAccessByPost` for attachment ids, again for sample ids) — 🐞 serial | **gone** — `plm-attachment` / `plm-sample` authorize internally; hydration calls carry user context only |
| `getUserAccessUnencoded` → `currentUserPermissions` per attachment | **moves** — the attachment service returns rows already annotated with the viewer's permissions (it reads ACL itself) |
| Thin-variant engine `accessControl.getPermissions` + missing-ACL **skip + log** | **moves** — permission annotation and the missing-entry behavior become attachment-service contract, not library code |
| JWT plumbing on `getAttachmentsV3(JWT)` / `getSamplesByIdsV2(samplesJWT)` | **gone** — plain service calls |

- What does **not** change: the relationship walk, the discussion/thread/sample enrichment joins, the three
  ordering rules, the draft filter, the `relatedResources` precedence quirk — the case's real complexity is
  the merge policy, and it was never ACL's.
- One long-standing question gets an answer for free: the *"TODO: ACL should bbe doing this"* draft filter
  finally has a natural home — the attachment/discussion **domain read path** (which now owns access
  filtering). Still not a migration-time change (01 pin-down 7 stance holds), but the backlog item now has
  an owner instead of "the access-control backlog".

## 2. Impact on decision drivers

- The serial ACL-token chain drops out of the latency budget — the remaining perf debt is the
  discussion/sample fetch chain and the reply N+1 (01 fixes 1 & 3 still apply).
- The library shrinks: enrichment = merge + per-surface policy; permission annotation arrives on the rows.
- New driver: the per-row permission shape (`currentUserPermissions`) becomes a **domain-service contract
  field** — parity now depends on the attachment service reproducing it byte-identically.

## 3. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Owner-computed, shared enrichment library | slimmer — loses all ACL clients; policy table unchanged | **recommended** | **recommended — unchanged** |
| B | `plm-attachment` computes the feed | its "per-viewer ACL still fans out" con **disappears** — but the decisive objection (thread/draft/ordering rules are not attachment rules) is untouched | rejected | still rejected — the ownership argument alone decides |
| C | Federated per-domain lanes, owner merges | slightly **stronger** — each lane is now ACL-complete inside its own domain, no owner-side permission join needed | end-state | still end-state, blocked on subgraphs — unchanged |
| D | Elastic single-source | unchanged — its blockers (flag state, thread data, index staleness) were never ACL | pinned input to C | unchanged |

## 4. Proposed decision — no change

- **Option A** stands, minus every ACL responsibility:
  - the enrichment library performs **no ACL calls**; viewer permissions and access filtering ride in on
    the domain services' responses,
  - 01 fixes 1–3 still apply, except fix 1 shrinks (nothing left to parallelize on the token side),
  - the per-surface policy table is unchanged — ordering, defaults, draft filter, source sets.
- Option C stays the recorded end-state; it gets marginally cheaper (lanes need no ACL representation in
  `@requires` payloads).

## 5. Pin-downs affected (vs 01 §4)

| 01 # | Item | Under domain-ACL |
|---|---|---|
| 7 | Draft-filter TODO | keep verbatim in the library phase 1; the enforcement item is now filed on the **attachment/discussion domain** backlog (real owner exists) |
| 8 | Missing-ACL skip+log vs `components`' throw | no longer library code — becomes a **domain-service contract question**; record the required behavior (skip + annotate) in the attachment-service contract and pin it with a fixture |
| 10 | Sequential fetches | token part **moot** (no tokens); discussions ∥ threads ∥ samples parallelization still applies |
| new | Permission-annotation contract | the attachment service already integrates with ACL — the ask is only that its responses **expose** `currentUserPermissions` in today's exact shape (a response-shape check, not new ACL work); verify before fixtures are recorded |

All other pin-downs (orderings, workspace v2 gap, thread→parent crash, flag survey, dual-mode,
`relatedResources` precedence) are unaffected.

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes.*
