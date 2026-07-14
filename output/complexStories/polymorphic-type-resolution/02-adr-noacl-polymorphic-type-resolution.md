# ADR-017-noACL (draft) — Polymorphic type resolution under the domain-ACL assumption

> **Status:** 🔴 Proposed — scenario draft for review
> **Baseline:** `01-adr-polymorphic-type-resolution.md` (ADR-017) — read that first; this ADR re-scores it
> under one changed premise.
> **Global assumption (given):** ACL is handled by **each domain service** — every domain service calls the
> access-control endpoint itself for its own reads and writes. The DGS / orchestration layer makes **no**
> ACL calls.
> **Convention:** if the proposed option differs from the 01 ADR, it is flagged with a red star ✴️.
>
> ## Verdict: **NO CHANGE** — Option B (per-site ports + playbook + CI conformance gate) remains the
> proposal. This is the least ACL-coupled case of the eight; the assumption touches only loader plumbing.

---

## 1. What the assumption removes from this case

- Type resolution itself — the five dispatch tables, discriminators, defaults, prefix gates — involves
  **zero ACL calls**. Nothing in §1 of the 01 ADR changes.
- The only ACL surface is **capability-JWT plumbing inside per-variant field loaders**:

| Loader | Today | Under domain-ACL |
|---|---|---|
| `wash.getWash(JWT)` · `materialHub.getHubMaterial(JWT)` · `colorArchroma.getByID(JWT)` · `combination.getFabricSpecComboById(JWT)` | resolver fetches/forwards a capability JWT | **gone** — plain service calls with user context; each material-family service authorizes internally |
| `SPARK_BomImpressionDetails_Unified.libraryResource` internal/external branch | selects a JWT-scoped path for external users | the *data-path* branch survives (it selects a source, per 01 pin-down 8) — only the JWT mechanics inside the external path disappear |

- The drift disease, the load-bearing defaults (HUB 9 fall-through), the `null` hole, the missing trim
  gate, the string-typed hub dispatch — all unaffected.

## 2. Options re-scored

| | Option | Change under domain-ACL | 01 verdict | Verdict now |
|---|---|---|---|---|
| A | Per-site ports | loaders lose JWT args; drift problem unsolved as before | viable | unchanged |
| B | A + playbook + CI conformance gate | identical value proposition; the enum/SDL/golden-fixture gate has no ACL dimension | **recommended** | **recommended — unchanged** |
| C | Backend-supplied discriminator | unchanged — still rejected on coordination cost + the `'Paper Based Substrate'` fragility | rejected | unchanged |
| D | Federation-native `Material` interface for search | unchanged — still the search lane's end-state | end-state | unchanged |

## 3. Proposed decision — no change

- **Option B** stands verbatim: constants-enum-per-domain, dumb `@DgsTypeResolver` lookups, shared CI
  conformance gate, `code → type` registry.
- The only scenario delta: per-variant loader clients are written **without capability-token plumbing** —
  slightly less code per variant, one less thing to drift.

## 4. Pin-downs affected (vs 01 §4)

- 1–8: **all unchanged.**
- No new pin-downs. (The internal/external branch — pin-down 8 — should note that "external" is a data-path
  selection surviving the ACL move, so nobody deletes it as "dead ACL code".)

---

*On acceptance: same lifecycle as the 01 ADR; this scenario ADR is ratified only together with the global
domain-ACL decision it assumes.*
