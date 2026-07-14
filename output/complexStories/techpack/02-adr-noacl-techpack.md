# ADR-015-noACL (draft) — Product TechPack aggregate under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-techpack.md` (ADR-015) — read that first; this ADR re-scores it under one changed
> premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The DGS / facade layer makes **no** ACL
> calls: no partner-permission batch filters, no capability tokens.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option B (facade-then-federate) remains the proposal. The facade's most
> expensive machinery (walk + serial ACL filter) shrinks dramatically, but the phase-1 blocker —
> 7 of 8 owning subgraphs not live — is untouched by who calls ACL.

---

## 1. What the assumption removes from this case

| Today (facade steps, per 01 §1) | Under domain-ACL |
|---|---|
| Step 1–2: walk ×1–2 + `getAccessControlBatch(ids, 100)` — 🐞 serial chunks — partner-filtering every walked id | **redistributed** — "which of your children under X can partner P see" is each owning service's question; the attachment service answers it directly for attachments (it queries by `relatedResources` and applies ACL itself) |
| Step 4: capability token before `getAttachmentsV3` hydration | **gone** — the attachment service authorizes and returns `product_packet_props` / `media_type` for the caller's context |
| Steps 5–11: elastic partner clauses (`partnerId`, `security.merchVendors\|bps`) | **unchanged** — these are index-embedded query filters, not ACL-service calls; they stay verbatim for parity (the search DGS is itself a domain service and owns their correctness under the global decision) |

- The 01 key finding gets stronger: the walk + ACL filter existed **only to find partner-visible attachment
  ids** — under domain-ACL that is a single attachment-service query, so the facade's heaviest and most
  fragile section collapses to one call even in phase 1.
- Unaffected: the 7 sequential elastic queries 🐞, the parent double-walk semantics, `parentId: undefined`
  🐞, the constructions paren splice 🐞, the v2-at-depth≥1 discard 🐞, the packet-critical filter (data
  logic over `product_packet_props`, not ACL), the bulk ordering bug 🐞.

## 2. Impact on decision drivers

- The retiring relationship walk loses its main remaining job in this flow — its quarantine gets smaller
  and its deletion (`F09`) gets easier.
- Parity nuance: today's semantics are "walk everything, then keep ids where the partner holds *any*
  surviving permission". The attachment service's ACL-scoped query must reproduce **that** visibility rule
  — record per-slice fixtures against today's output before swapping the source (new pin-down N1).
- The phase-1 constraint that decides the case — only `plm-product` live on day 1 — is completely
  independent of ACL placement.

## 3. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Lift-and-shift into `plm-product` | **can't even lift as-is** — the ported helper's ACL-filter section is forbidden; A becomes "port minus ACL", inheriting the same contract work as B's facade with none of its exit path | viable | weaker — still re-freezes the 8-domain coupling |
| B | Facade-then-federate | the facade thins (walk+ACL section → one attachment-service call); each `F0x` re-homing gets simpler because slices already arrive ACL-complete; `F09` gets closer | **recommended** | **recommended — unchanged** |
| C | Federation-native day 1 | unchanged — still blocked on 7 subgraphs not being live; ACL was never its blocker | disqualified | unchanged |
| D | Search-DGS / materialized counts | its "per-viewer ACL can't be precomputed" con technically softens (viewer scoping is the domains' job now) — but packet-critical needs attachment hydration, staleness is user-visible, and the business rules still land in the wrong owner | later refinement | unchanged — viewer-independent counts only |

## 4. Proposed decision — no change

- **Option B** stands: thin `@DgsQuery` stub → frozen aggregation facade (`E03`), per-domain re-homing
  (`F01–F08`), facade retirement (`F09`) — with the facade now built **without an ACL client**:
  - attachment ids + packet props come from one ACL-scoped attachment-service query (replacing walk +
    batch filter + token + hydrate),
  - the seven elastic slice queries stay verbatim (quirks and all, per 01 pin-downs 4–8),
  - bulk (`E04`) unchanged: same core, input-ordered.
- The F-phase gets cheaper: each owner already answers ACL-scoped questions, so re-homing a slice is
  purely a transport flip.

## 5. Pin-downs affected (vs 01 §4)

| 01 # | Item | Under domain-ACL |
|---|---|---|
| 3 | Serial ACL chunk loop | **moot** — no facade-side ACL calls exist |
| 7 | Parent double-walk | mostly subsumed — the attachment service queries `relatedResources IN (product, parent)` directly; preserve the *result* semantics via fixtures, not the mechanism |
| 1, 2, 4, 5, 6, 8, 9, 10 | bulk ordering · 7 serial queries · `undefined` literal · v2-depth discard · paren splice · statusId quirks · facade placement · critical-union semantics | unchanged |
| new N1 | Visibility-rule equivalence | prove the attachment service's ACL-scoped query returns the same id set as today's walk+filter ("any surviving permission" semantics) — a semantics check on its **existing** ACL integration, not new capability; per-slice fixture recorded against production-shaped data **before** the source swap |

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes.*
