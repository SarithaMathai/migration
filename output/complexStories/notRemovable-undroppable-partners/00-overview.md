# Complex Story — `notRemovablePartnerIds` & `unDroppablePartners`

> **Summary —** Work out which partners can’t be removed yet by asking each domain “do you still reference this partner?” and unioning the answers (a cross-domain read).
> **Spike:** `SPIKE-04` · **Status:** 🟠 Draft ADR-016 proposed — ratification pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub stories:** `PRODUCT-BE-G-11-1` (notRemovable) + `PRODUCT-BE-G-07` (unDroppable) + `WORKSPACE-BE-G-05` (later phase, workspace twins). The drop/undrop **writes** are `SPIKE-03`, not this case.

> **Migrates (source resolvers → this case):** product **FR `notRemovablePartnerIds`** (`PRODUCT-BE-G-11-1`) +
> **FR `unDroppablePartners`** (`PRODUCT-BE-G-07`) + helpers `getProductPartnersNotRemovable` /
> `getUnDroppablePartners`; workspace **FR `notRemovablePartnerIds`/`unDroppablePartners`** (`WORKSPACE-BE-G-05` (later phase)).

## 1. The problem (grounded in the legacy code)

### 1.1 Problem statement

- Two fields on `Product` and `Workspace` must answer "which partners can the user **not** remove / **not**
  drop, because a child resource still references them?" — a union across five domains' data.
- Today that union is computed by **invoking sibling field resolvers reflectively** (four cross-resolver
  calls, including two entire complex-case pipelines) and a retiring Relationship-Service graph walk, only
  to discard everything but partner ids.

### 1.2 Current state & root cause

**What this read does:**
- Before an admin removes or drops a partner, the UI must grey out the ones still in use — a partner who still owns samples, participates in discussions, holds claims, or is named on attachments cannot simply be taken off.
- Answering "is this partner still in use anywhere?" means asking each of those domains and combining the answers.

Two fields on **Product** and **Workspace** answer "which partners can the user **not** remove / **not** drop
from this resource, because they're still referenced by a child?" Both are **cross-domain aggregations** today.

### `Product.notRemovablePartnerIds` — `getProductPartnersNotRemovable` (utils/removePartnerUtils.js:57)
Unions partner IDs gathered from **five** sources:
| Source | How (legacy) | Owning subgraph (target) |
|---|---|---|
| discussions | `discussionsV2` (elastic) → `partnerId + droppedPartnerIds + designPartnerId` | plm-discussion |
| attachments **+ components** | `attachmentsV3` + `components` → `detailIds` → ACL batch → grantees | plm-attachment |
| samples | `samples` → `partnerId` | plm-sample |
| watchlists | search product watchlists in workspace → ACL batch → grantees | plm-product (watchlist, co-located) |
| owning | `product.owningPartnerId` | plm-product |

### `Workspace.notRemovablePartnerIds` — `getWorkspacePartnersNotRemovable` (utils/removePartnerUtils.js:38)
Same shape, fewer sources: `discussionsV2` + `attachmentsWithMetaData` (→ ACL grantees) + `workspace.owningPartnerId`.

### `Product`/`Workspace.unDroppablePartners(isDesignPartner)` — `getUnDroppablePartners` (utils/commonLoaders.js:836)
1. `getAssociatedChildrensFromResouceId` → **Relationship Service** returns every child id (discussions,
   attachments, BOMs, packaging BOMs, samples, measurement sets, claims, + the product itself).
2. `getChunkedPermissions` → ACL permissions for all of them.
3. Keep resources whose ACL group is **not** `dps` (design-partner-security), return the **unique grantees**.

**Root cause (same as TechPack):** "which partners do *you* still reference for resource X?" exists as an
operation in no domain, so the monolith gateway synthesized it — Relationship-Service full traversal +
chunked ACL across every child + reflective sibling-resolver invocation, all in one utility. No domain owns
its slice.

### 1.3 Impact if not addressed

- **Correctness/safety** — a missed source un-greys a partner who still owns data; an admin can then
  remove a partner who shouldn't be removable. Any single source throwing fails the whole field.
- **Coupling** — the fields silently depend on the full `components` and `attachmentsWithMetaData`
  pipelines (ADR-014/ADR-018 machinery) that they don't need; those cases cannot change internals without
  breaking partner removability.
- **Portability** — the `samples` source reads `info.variableValues` (the caller's GraphQL variable
  names); this coupling **cannot be ported** to DGS, so a decision is forced, not optional.
- **Performance** — five sequential source fetches plus serial ACL chunking on an interactive
  admin screen.

### 1.4 Objectives

The spike is done when all of the following are recorded and ratified:
- A per-domain contribution contract ("partner ids you still reference for X") for every source, with the
  union's owner fixed.
- Elimination of all reflective resolver invocation (`G-11-1` AC-2) — every source becomes a direct,
  statically-typed call or a federated lane.
- A replacement for the Relationship-Service walk in `unDroppablePartners` with a defined deletion point.
- Behavioral parity per source, proven by per-source recorded fixtures (so lane flips are individually
  gated), with quirks (dps exclusion, numeric-only grantees, first-workspace scope) consciously pinned.

## 2. What the spike must decide

- The contribution each domain exposes for the partner aggregation.
- Where the union is computed.
- **Proposal so far (light, to validate):** each domain contributes its own partner slice; the entity owner combines them.
- **Draft decision:** [ADR-016 (draft)](./01-adr-notremovable-undroppable-partners.md) proposes
  owner-`@requires` lane aggregation (Option B, phase 1 = direct calls behind the same aggregator field) —
  status 🔴 Proposed, pending ratification. ACL is out of scope for this case (ADR-019 — see ADR-016's
  ACL note).

---

*This folder holds the problem brief (this file) + the draft decision ([01-adr-notremovable-undroppable-partners.md](./01-adr-notremovable-undroppable-partners.md)) + the story breakdown implementing it ([01-stories.md](./01-stories.md)) — the concrete story ids in each affected domain's be-04-stories.md, cross-referenced by pin-down.*
