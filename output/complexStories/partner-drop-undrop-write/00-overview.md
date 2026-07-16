# Complex Story — Partner DROP / UNDROP / REMOVE write (`productBusinessPartnerActions` / `workspaceBusinessPartnerActionsV2`)

> **Summary —** One click, five services, no rollback — today a mid-flight failure leaves a partner half-dropped; orchestrate drop/undrop/remove as one compensatable write instead.
> **Spike:** `SPIKE-03` · **Status:** 🟠 Draft ADR-012 proposed — ratification pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub story:** `PRODUCT-BE-E-01` + `WORKSPACE-BE-E-01` (later phase)

> **Migrates (source resolvers → this case):** product **M10 `productBusinessPartnerActions`** (`PRODUCT-BE-E-01`)
> + workspace **M7 `workspaceBusinessPartnerActionsV2`** (`WORKSPACE-BE-E-01` (later phase), 5-case dispatcher), fanning out to
> per-domain drop/undrop participants (sample, discussion, claims, attachment, ACL, user-profile). Full per-case
> call sequences: [ADR-012 §1](./01-adr-partner-drop-undrop.md).

## 1. The problem (grounded in the legacy code)

### 1.1 Problem statement

- Three partner-lifecycle actions (drop, undrop, remove) must each take effect **atomically across every
  service that references the partner** — but today each is a sequential, no-rollback fan-out across 5+
  services, so a mid-flight failure leaves a partner half-dropped with access rules out of sync.
- Drop/undrop is **security-relevant**: the UI (and the partner) assume access is revoked the moment the
  mutation returns.

### 1.2 Current state & root cause

**What these operations do.** A business partner (a supplier or vendor) collaborates on products and
workspaces — they see samples, discussions, claims, and attachments. Three administrative actions manage that
relationship, and each must take effect **everywhere the partner is referenced**:

- **Drop** — suspend the partner's access to a product or workspace and to everything under it (samples,
  discussions, claims, attachments). The association is kept, so the action is reversible.
- **Undrop** — reverse a drop: restore the partner's access across the same set of domains.
- **Remove** — take the partner off the product entirely: team membership, access rights, and their saved
  activity (recently viewed, to-dos, favorites) are all cleaned up.

One click in the UI therefore fans out to five or more services — which is why a mid-flight failure today
leaves a partner half-dropped, and why this case exists.

`productBusinessPartnerActions(actionType, values)` (resolvers/SPARK_Product.js:825) is a ~220-line dispatcher with **no rollback**:

### `REMOVE_PARTNER`
- `removeProductResources` (teams) → `deleteRecentlyViewedByPartner` → `deleteToDoByBusinessPartner` → `deleteFavoritesByBusinessPartner` → `removeProductBusinessPartner` (ACL via capability token).
- **5 sequential side-effecting calls across 5 services.**

### `DROP_UNDROP_PARTNER` (the hard one)
1. **Relationship Service** `searchByIds(includeBranches:[product,sample,discussions,discussionThreads,claim])` → all child ids.
2. `filterResourcesByPartner` → ACL permissions for the partner across those ids; drop the ones the partner isn't on.
3. `getPermissionMapForBulkACLCall` → `toBePermissionsMap`.
4. capability JWT for all resources.
5. if **not** a design partner and samples exist → `sampleV2.dropSamples` / `unDropSamples`.
6. `Promise.all([ dropUndropProductBusinessPartner, sampleCall ])` **then** `accessControl.dropPartnerFromResources` /
   `unDropPartnerFromResources(toBePermissionsMap)` **+** (if dropped) `deleteAllUserProfileDataForAPartner`.

`workspaceBusinessPartnerActionsV2` (resolvers/SPARK_WorkspaceV2.js) is the analogous **5-case dispatcher** for workspaces (+ `discussion`, `favorite`, `sampleV2`).

**Root cause:** the monolithic gateway let one dispatcher call every service directly, so partner cleanup
was written as one function instead of per-domain contracts — on top of a Relationship-Service full
traversal (being retired) for child discovery, ACL bulk drop/undrop, and a design-partner branch. Today no
domain owns its slice of the cleanup, and no step records enough to recover from.

### 1.3 Impact if not addressed

- **Security** — a failure after the partner-status write but before the ACL bulk-drop leaves the UI
  saying "dropped" while the partner can still read samples, discussions and claims.
- **Data integrity** — remove can wipe recently-viewed and to-dos yet leave the partner on the product
  (failure at step 3 of 5); nothing detects or reconciles it.
- **Migration blockage** — `PRODUCT-BE-E-01` cannot meet its own AC-3 (visible, isolated cleanup failures)
  without an orchestration decision; the workspace twin would re-implement the same fan-out ad hoc.
- **Structural debt** — the retiring Relationship-Service traversal and the cross-resolver
  `UserProfileAttributes` import both survive any naive port.

### 1.4 Objectives

The spike is done when all of the following are recorded and ratified:
- An ownership decision: who orchestrates product vs workspace partner actions, generalizable to both.
- A per-step failure policy (compensate / retry / record) with the ACL-before-return ordering constraint
  for drop stated as a testable invariant, not a convention.
- A participant contract per affected domain (drop/undrop/remove step + own-children enumeration) that
  replaces the Relationship-Service traversal.
- Behavioral parity for all three action paths, proven by recorded fixtures, with any new
  partial-failure visibility listed as an accepted deviation.

## 2. What the spike must decide

- Who owns and orchestrates the drop/undrop fan-out — domain subgraph vs workspace.
- How a mid-flight failure is detected and recovered.
- **Proposal so far (light, to validate):** the resource owner orchestrates the fan-out; each domain exposes its own drop/undrop step.
- **Draft decision:** [ADR-012 (draft)](./01-adr-partner-drop-undrop.md) proposes an owner-orchestrated
  saga over a per-domain participant contract (Option B) — status 🔴 Proposed, pending ratification.
  Scenario variant under the domain-ACL assumption: [ADR-012-noACL](./02-adr-noacl-partner-drop-undrop.md).

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
