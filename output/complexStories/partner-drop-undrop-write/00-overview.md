# Complex Story — Partner DROP / UNDROP / REMOVE write (`productBusinessPartnerActions` / `workspaceBusinessPartnerActionsV2`)

> **Summary —** Drop / undrop / remove a business partner across every referencing child domain as one orchestrated, compensatable write.
> **Spike:** `SPARK-SPIKE-03` · **Status:** 🔴 Open — decision pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub story:** `SPARK-PROD-E01` + `SPARK-WS-E01` (later phase)

> **Migrates (source resolvers → this case):** product **M10 `productBusinessPartnerActions`** (`SPARK-PROD-E01`)
> + workspace **M7 `workspaceBusinessPartnerActionsV2`** (`SPARK-WS-E01` (later phase), 5-case dispatcher), fanning out to
> per-domain drop/undrop participants (sample, discussion, claims, attachment, ACL, user-profile). Full per-task
> mapping: 

## 1. The problem (grounded in the legacy code)

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

**Why it is hard:** Relationship-Service full traversal (being retired) + a multi-service, **non-atomic,
no-rollback** fan-out + ACL bulk drop/undrop + a design-partner branch. Today no domain owns its slice of the cleanup.

## 2. What the spike must decide

- Who owns and orchestrates the drop/undrop fan-out — domain subgraph vs workspace.
- How a mid-flight failure is detected and recovered.
- **Proposal so far (light, to validate):** the resource owner orchestrates the fan-out; each domain exposes its own drop/undrop step.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
