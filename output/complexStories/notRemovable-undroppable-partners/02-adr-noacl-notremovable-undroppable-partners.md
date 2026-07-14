# ADR-016-noACL (draft) — `notRemovablePartnerIds` / `unDroppablePartners` under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-notremovable-undroppable-partners.md` (ADR-016) — read that first; this ADR
> re-scores it under one changed premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The DGS / orchestration layer makes **no**
> ACL calls: no `getAccessControlBatch`, no `getPermissions`, no owner-side grantee joins.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option B (owner-`@requires` lane aggregation) remains the proposal.
> This is the most ACL-heavy case of the eight — the assumption reshapes the **lane contract**
> substantially, but it *strengthens* the recommended option rather than displacing it.

---

## 1. What the assumption removes from this case

| Today (DGS layer) | Under domain-ACL |
|---|---|
| `notRemovable`: `getAccessControlBatch(detailIds, 250)` — 🐞 serial chunks — joining component + attachment ids to grantees | **gone** — each lane returns partner ids directly; the domain resolved its own grantees via ACL |
| `notRemovable`: watchlist ids → ACL batch → grantees | **gone** — the watchlist lane (co-located `plm-product`) returns partner ids itself |
| grantee-group parsing (`bps` / `dps` / `MerchVendor`-style) in the owner | **moves** — group semantics are resolved where the ACL read happens: inside each domain |
| `unDroppable`: `getChunkedPermissions` over the whole relationship subtree | **gone** — replaced by per-domain lanes answering "grantees on my children of X" |
| `unDroppable`: 🐞 `dps`-group whole-resource exclusion, owner-side | **splits** — see pin-down N1: group *retrieval* is the domain's; the exclusion *rule* stays with the owner |
| 🐞 `.filter(Number)` numeric-only grantees, owner-side | **moves** into the lane contract (each lane returns numeric partner ids; logs dropped non-numeric) |

- What survives: the union/`uniq`/`owningPartnerId` aggregation, the `isDesignPartner` gate, the
  first-workspace-only watchlist scope, the retirement of both the cross-resolver imports and the
  relationship walk. The case's shape — "each domain answers for its own slice, owner unions" — is
  exactly what the domain-ACL decision mandates globally.

## 2. Impact on decision drivers

- No domain gains new ACL plumbing — every domain service already integrates with ACL; the lanes only
  **expose** an answer each domain can already compute with its existing integration.
- The 01 ADR's key finding gets sharper: the lanes are no longer "cheap domain queries + owner ACL join" —
  they are **complete answers**. "Which partners do *you* still reference for X?" is now answerable only by
  the domain (it alone may read ACL), so lane-shaped decomposition stops being a choice and becomes the
  only architecture consistent with the global decision.
- `unDroppablePartners` loses its last owner-side data dependency (the ACL join) — the owner keeps only
  business rules (union, dps exclusion, design-partner gate).
- New parity risk: the union was previously computed against **one** ACL snapshot (one batched read);
  under lanes it is computed against **N per-domain ACL reads at slightly different instants** — a
  partner being granted/revoked mid-flight can produce a union no single snapshot would. Acceptable for a
  grey-out read; note it in the fixtures (pin-down N2).

## 3. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Owner-computed union over direct service calls | its residual role (phase-1 interim of B) survives, but the owner may **no longer do the ACL join itself** — each direct call must already return partner ids, i.e. A is forced into B's lane contract anyway | viable interim | still the phase-1 interim — now indistinguishable from B's phase 1 |
| B | Owner-`@requires` lane aggregation | **strengthened** — lanes become fully self-contained (domain query + domain ACL read inside one service); the owner-side ACL client disappears even in phase 1; the validated `removablePartner/` clone mechanics apply unchanged | **recommended** | **recommended — unchanged, stronger** |
| C | Central partner-reference service | **weaker** — a central service would now need to *be* an ACL-calling domain over everyone's data; doubly inverted ownership | rejected | still rejected |
| D | Materialized partner-reference index | unchanged blockers — and its "ACL grantee changes don't flow through domain events" objection gets worse: grantee changes now happen inside N domains, so N event sources would be needed | later refinement | unchanged — cache only, never source of truth |

## 4. Proposed decision — no change

- **Option B** stands, with the lane contract upgraded from "ids/partners slice" to a **complete,
  ACL-resolved partner answer** per domain:
  - `notRemovable` lanes: *"partner ids referenced by my children of X"* — discussion, attachment, sample
    lanes on their subgraphs; watchlist/bom/measurement in-process; each performs its own ACL read,
  - `unDroppable` lanes: *"grantees (with group tags) on my children of X"* — the owner applies the
    `dps` exclusion + `uniq` + `.filter(Number)` semantics **without calling ACL** (group tags ride in on
    the lane payload),
  - phase 1 = the same aggregator over direct service calls returning the same lane payloads; federation
    flips transport, not contract (unchanged from 01).
- The relationship walk's quarantine (01 pin-down 9) still applies where a domain can't yet enumerate its
  children — but the walked ids must then be passed **to the domain** for its ACL-scoped answer, never
  joined to ACL by the owner.

## 5. Pin-downs affected (vs 01 §4)

| 01 # | Item | Under domain-ACL |
|---|---|---|
| 4 | Serial ACL chunk loop | **moot** — no owner-side ACL calls exist |
| 6 | `dps` whole-resource exclusion | re-homed as pin-down N1: lanes return grantees **with group tags**; owner keeps the exclusion rule (it is removability UX, not ACL mechanics); mixed dps+bps fixture still required |
| 7 | `.filter(Number)` | moves into the lane contract — each lane filters + logs |
| 1–3, 5, 8, 10 | cross-resolver kills · samples `variableValues` · parallel sources · design-partner gate · first-workspace scope · lane hiding | unchanged |
| new N1 | Grantee-group tags in the lane payload | define one shared `{partnerId, groups[]}` lane fragment; every domain already resolves this via its existing ACL integration — the work is exposing it uniformly; contract-test all lanes before fixtures freeze |
| new N2 | Multi-snapshot union skew | document that the union is now assembled from N per-domain ACL reads; fixtures assert set-equality under a quiesced dataset |

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes. The lane-contract upgrade (N1) must be agreed jointly with ADR-012-noACL's
participant contract — they are the read and write faces of the same per-domain obligation.*
