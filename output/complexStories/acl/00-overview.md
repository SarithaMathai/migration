# Complex Story — ACL Capability-Token Handling Across Domain Boundaries

> **Summary —** Every domain's schema/story docs currently say ACL is "context-only, ignored in DGS." The be-07 ACL usage research found 31 call sites across 8 domains where a capability token is minted specifically to call ANOTHER domain's API — that claim is false for those sites.
> **Spike:** — (cutover pattern, not a numbered program spike — same category as ADR-014/ADR-018) · **Status:** 🔴 Proposed — draft ADR-019 for review
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** program-wide — all 8 phase-1 domains (`product`, `bom`, `measurement`, `productDetails`, `packaging`, `watchlist`, `impression`, `claims`); heaviest in `product` (9 sites) and `bom` (6 sites).

> **Migrates (source resolvers → this case):** every `getUserPermissionsJWT(...)` call site across `code/resolvers/**/*.txt` classified as **downstream-token** in
> [`output/analysis/aclResearch/00-acl-usage-inventory.md`](../../analysis/aclResearch/00-acl-usage-inventory.md)
> (program roll-up) and each domain's `output/analysis/{domain}/be-07-acl-usage-analysis.md`.

## 1. The problem (grounded in the legacy code)

### 1.1 Problem statement

- Every domain's `be-03-schema.graphql` header and `be-04-stories.md` state: *"capability-token (JWT)
  usage in source is context-only; ACL is IGNORED in the DGS implementation (no ACL plumbing story)."*
- That claim is only true for two of the three ACL usage shapes found in the legacy resolvers. The third
  shape — a token minted in one domain's resolver and hand-carried into **another** domain's loader call
  (`ctx.loaders.<otherDomain>.<method>(token)`) — means ACL is load-bearing at a domain boundary, not
  ignorable.

### 1.2 Current state & root cause

The be-07 research (`generate_acl_analysis.py`) classified every `getUserPermissionsJWT` /
`ctx.loaders.accessControl.*` call site in all 8 domains' resolver files into three kinds:

| Kind | Count | What it means | Is "context-only, ignored" true here? |
|---|---|---|---|
| `permission-check` | 15 | `accessControl.getPermissions`/`getUserAccessUnencoded` or a bulk ACL-filtered tree read for the CURRENT resource | Yes — resolver-local, no token leaves the domain |
| `own-domain-token` | 35 | Token minted then used only by the SAME domain's own loader (e.g. `bom` resolver → `ctx.loaders.bom(token)`) | Yes — resolver-local write/read gate |
| **`downstream-token`** | **31** | Token minted then handed to a **DIFFERENT** domain's loader (`ctx.loaders.<otherDomain>(token)`) | **No** — the token is the caller's authorization to read/write another domain's resource |

Example (`code/resolvers/product/SPARK_Bom.txt`, `SPARK_BomWashMaterial.libraryResource`):
```
const permissionJWT = await getUserPermissionsJWT(washId, ctx)
const wash = await ctx.loaders.wash.getWash(permissionJWT).load(washId)
```
`bom`'s resolver mints a token scoped to `washId` and hands it to the `wash` domain's loader. If the DGS
port drops this token (per the current "ACL ignored" instruction), the `wash` service either has no
authorization context for the call, or must fall back to a service-account/ambient credential that loses
the calling user's actual permission scope — a silent authorization regression, not a no-op.

**Root cause:** the "ACL is context-only" note was written against the *dominant* pattern (permission-check
+ own-domain-token = 67% of sites) without isolating the minority downstream-token pattern, which behaves
differently and cannot be dropped the same way.

### 1.3 Impact if not addressed

- **Authorization regression risk** — 31 call sites across every domain would silently lose per-request,
  per-user authorization scope on a cross-domain call if the DGS port follows the current "ignore ACL"
  instruction literally.
- **Inconsistent doc trail** — `be-03-schema.graphql` and `be-04-stories.md` in all 8 domains carry a
  blanket claim that is field-level false for 31 named resolvers; anyone implementing from those docs
  alone will drop the token.
- **No sanctioned mechanism recorded** — `SparkSecurityService.updateCurrentUserPermissions
  (capabilityToken)` (Mid-Request ACL Update) exists as a callable mechanism today but has no story or ADR
  wiring it to these 31 sites.

### 1.4 Objectives

This case is done when:
- Every downstream-token call site has an explicit resolution recorded (Mid-Request ACL Update, or a
  named alternative) instead of being silently dropped.
- The "ACL is context-only, ignored" language in be-03/be-04 is corrected to distinguish the three kinds,
  once this ADR is ratified (doc edit is a **separate, later** pass — not bundled into this research).
- A story exists per domain for the domain's downstream-token sites (or the sites are folded into the
  entity-resolver/federation stories that already touch that call, if the ADR decides that's sufficient).

## 2. What must be decided

- Whether the DGS port refreshes security context via **Mid-Request ACL Update**
  (`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)`) before every downstream-token
  cross-domain call, or via a different mechanism (e.g. gateway-forwarded auth header, per-domain
  re-authentication).
- Whether the resolution is uniform across all 31 sites or differs by target-domain shape (phase-1
  co-located domain vs. separate sibling DGS vs. external platform stub).
- **Draft decision:** [ADR-019 (draft)](./01-adr-acl-mid-request-update.md) proposes Mid-Request ACL
  Update for every downstream-token site whose target is a phase-1 or sibling-DGS domain, and gateway
  auth passthrough for sites whose target is an external platform stub — status 🔴 Proposed, pending
  ratification. This is a **single decided version**, not a scenario pair — it does not need a
  `02-adr-noacl-*.md` variant because it does not depend on the program's general domain-ACL assumption;
  it is itself the ACL-handling decision for cross-domain resolver calls.

---

*This folder holds the problem brief (this file) + the decided ADR ([01-adr-acl-mid-request-update.md](./01-adr-acl-mid-request-update.md)). Unlike the other complex cases, this decision has no
`01-stories.md` of its own — per ADR-019 §5, it's implemented as one line added to each of the 31
downstream-token call sites' existing migration story (across bom, product, productDetails, packaging,
watchlist), not as new dedicated stories.*
