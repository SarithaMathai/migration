# Complex Story — Product Tech Pack (`getProductTechPack`)

> **Summary —** One panel, eight domains, zero owners — give the TechPack aggregate a federated home so each domain owns its own badge count instead of one 200-line function walking the whole graph.
> **Spike:** `SPIKE-02` · **Status:** 🟠 Draft ADR-015 proposed — ratification pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domain:** product (`plm-product`) · **Stub story:** `PRODUCT-BE-E-03` / `E-04`

> **Migrates (source resolvers → this case):** product **Q8 `getProductTechPackCountV1`** + **Q9
> `getProductTechPackBulkCountV1`** + helper **`getTechPackResourceCountMap`** (`product/be-02-resolver-analysis.md`),
> fanning out to the per-domain ID-list reads (attachment, discussion, sample, claims; co-located bom/measurement/
> construction/watchlist). Home stub **`PRODUCT-BE-E-03/E-04`**.

## 1. The problem

### 1.1 Problem statement

- One query, `getProductTechPackCountV1`, must render the Tech Pack panel's 11 badge counts for a
  `(productId, partnerId)` pair — data owned by ~8 domains — yet all of it is computed today by a single
  ~200-line, 14-step gateway helper that no domain team owns.
- Under federation that aggregate has no home: the helper cannot be lifted into any one subgraph without
  re-freezing the 8-domain coupling the migration exists to remove.

### 1.2 Current state & root cause

**What this read does.** The Tech Pack panel shows, for one product and partner, how much related material
- exists — how many attachments, discussions, samples, claims, BOMs, measurement sets, constructions and watchlists — as badge counts the user clicks through.
- Every one of those numbers is owned by a different domain, so a single screen load is a read across 8 domains' data (4 physical services: Relationship, ACL, Attachment, Elastic).

`getProductTechPackCountV1` → `getTechPackResourceCountMap` returns, for a `(productId, partnerId,
workspaceContext, parentProductId)`, **ID lists grouped by resource type** that the Tech Pack panel renders as
badge counts + nav links:

```
productAttachments  discussionAttachments  discussions  samples
measurementSets  claims  productBoms  packagingBoms  constructions  watchlists
```

**Root cause.** The monolithic gateway let one resolver call every domain's backend directly, so the
aggregate was built as one cross-domain function instead of per-domain contributions:
- **Full graph traversal** — `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission` with
  `maxDepth=null` loads the **entire** product subtree from the Relationship Service into memory —
  machinery that exists only because no domain exposes "my slice for product X" as an operation.
- **Serial ACL checks** — every node gets its own ACL permission call (N nodes = N calls).
- **Double traversal** — when `parentProductId` is set the whole thing repeats for the parent.
- **8 domain types in one 200-line function**; **mixed data sources** (Relationship graph + Elastic + ACL);
  **tight coupling** — no domain team can own or deploy a slice independently.

### 1.3 Impact if not addressed

- **Performance** — every panel paint pays a full subtree walk (×2 with a parent), chunked-serial ACL
  calls, and 7 sequential elastic queries; the bulk variant multiplies this per input product.
- **Reliability** — any one of the ~12 downstream calls throwing fails the whole field; there is no
  per-slice degradation.
- **Migration risk** — a naive lift-and-shift re-freezes the 8-domain coupling inside `plm-product` and
  gives the retiring Relationship-Service walk a new home; `PRODUCT-BE-E-03`/`E-04` and the `H-01–H-05`/`F-09`
  federation chain stay blocked until an assembly pattern is ratified.
- **Ownership** — badge-count defects have no owning team; every change is a cross-team negotiation.

### 1.4 Objectives

The spike is done when all of the following are recorded and ratified:
- An assembly pattern for the `ProductTechPack` aggregate under federation, with day-1 **behavioral
  parity** provable by recorded fixtures (including packet-critical filter, parent double-walk, and
  per-index statusId quirks).
- A slice-ownership map: which domain contributes each of the 11 fields, and how each slice ships
  independently (ship-on-green) as its subgraph goes live.
- The Relationship-Service dependency quarantined behind one seam with a defined deletion point.
- An explicit decision on the `E-04` bulk-ordering defect (fix vs preserve), recorded as a parity deviation.

## 2. What the spike must decide

- How the `ProductTechPack` aggregate is assembled under federation — which pattern serves it.
- Which domain contributes each slice (attachments, discussions, samples, claims, BOMs, measurements, constructions, watchlists).
- **Proposal so far (light, to validate):** each owning domain contributes its slice to one shared entity, instead of one helper calling every service.
- **Draft decision:** [ADR-015 (draft)](./01-adr-techpack.md) proposes **facade-then-federate**
  (ADR-015 §3 Option B; the pattern `techpack-migration-options.md` calls "Option D (hybrid)") — status
  🔴 Proposed, pending ratification. ACL is out of scope for this case (ADR-019 — see ADR-015's ACL note).

---

*This folder holds the problem brief (this file) + the draft decision ([01-adr-techpack.md](./01-adr-techpack.md)) + the story breakdown implementing it ([01-stories.md](./01-stories.md)) — the concrete story ids in each affected domain's be-04-stories.md, cross-referenced by pin-down.*
