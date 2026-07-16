# ADR-011-noACL (draft) — Cross-Domain Association writes under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-cross-domain-association.md` (ADR-011) — read that first; this ADR re-scores it
> under one changed premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The DGS / orchestration layer makes **no**
> ACL calls: no capability tokens fetched, none forwarded.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option B (sync orchestration + shared association component) remains the proposal.

---

## 1. What the assumption removes from this case

ACL in this case is pure **token plumbing** — capability JWTs fetched before calling a sibling service:

| Mutation | ACL today | Under domain-ACL |
|---|---|---|
| D-01 `addProduct` | token before workspace link · token before copy-details (✅ ×2) | **gone** — workspace / product services authorize the calls themselves |
| D-02 `addProducts` | tokens ×3 (workspace, attachment metadata, re-point) | **gone** |
| D-04 `updateProduct` | token per archive list (V2/V3) | **gone** — attachment service authorizes its own archive |
| D-03 / D-06 / D-07 / D-11 | none | unaffected |

- The interaction matrix loses its ACL column; nothing else moves. The case's substance — who orchestrates
  the multi-subgraph fan-out, and what happens on partial failure — is untouched, because ACL was never a
  step that could fail the association semantics; it was a precondition fetch.
- Decision driver *"ACL capability tokens must keep flowing (header forwarding via `@DgsContext`)"*
  simplifies to: **user identity/context forwarding only** — each domain service resolves its own
  permissions from that.

## 2. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Sync in-subgraph orchestration | loses token plumbing; still leaves five ad-hoc fan-outs | viable | unchanged |
| B | A + shared association component | the component's `associate(...)` API gets simpler (no token acquisition inside it); everything that made it recommended — one fan-out implementation, declared failure policy — is untouched | **recommended** | **recommended — unchanged** |
| C | Client/gateway composition | unchanged — still breaks every caller's contract | disqualified | unchanged |
| D | Event-driven + transactional outbox | marginally **stronger** as end-state: consumers creating links no longer need capability tokens minted for an absent user context (a classic async-ACL headache) — each consumer's domain service authorizes with the event's principal. The disqualifier (read-after-write contract) is untouched | end-state | unchanged — end-state, slightly de-risked |

## 3. Proposed decision — no change

- **Option B** stands: synchronous orchestration through one shared association component in
  `plm-product`, per-mutation failure policy declared; the component now contains **no ACL logic at all** —
  it is purely link-call sequencing + policy.
- **Option D** remains the recorded end-state; note in the end-state record that the domain-ACL decision
  removes one of its practical frictions (token minting in consumers).

## 4. Pin-downs affected (vs 01 §4)

| 01 # | Item | Under domain-ACL |
|---|---|---|
| 1 | D-02 unawaited `bulkUpdateResource` | unchanged — await it |
| 2 | D-02 reject-after-create | unchanged — accept + document, defer to `SPIKE-01` |
| 3 | D-02 cross-resolver import | unchanged — attachment-service client call (now without a token argument) |
| 4 | D-06/D-07 `return new Error(...)` | unchanged — thrown typed errors |
| new | Context forwarding contract | replace the capability-token forwarding requirement with a single **user-context propagation** convention (headers) shared by all service clients; the domain services' own ACL calls depend on it — one contract test |

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes.*
