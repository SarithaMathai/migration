# Complex Story — Product Tech Pack (`getProductTechPack`)

> **Summary —** Assemble the TechPack entity whose every field/count comes from a different microservice, via federation (`extend type ProductTechPack`) so each service owns its own slice.
> **Spike:** `SPARK-SPIKE-02` · **Status:** 🔴 Open — decision pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domain:** product (`plm-product`) · **Stub story:** `SPARK-PROD-E03` / `E04`

> **Migrates (source resolvers → this case):** product **Q8 `getProductTechPackCountV1`** + **Q9
> `getProductTechPackBulkCountV1`** + helper **`getTechPackResourceCountMap`** (`product/02-resolver-analysis.md`),
> fanning out to the per-domain ID-list reads (attachment, discussion, sample, claims; co-located bom/measurement/
> construction/watchlist). Home stub **`SPARK-PROD-E03/E04`**.

## 1. The problem

**What this read does.** The Tech Pack panel shows, for one product and partner, how much related material
- exists — how many attachments, discussions, samples, claims, BOMs, measurement sets, constructions and watchlists — as badge counts the user clicks through.
- Every one of those numbers is owned by a different domain, so a single screen load is a read across ~8 services.

`getProductTechPackCountV1` → `getTechPackResourceCountMap` returns, for a `(productId, partnerId,
workspaceContext, parentProductId)`, **ID lists grouped by resource type** that the Tech Pack panel renders as
badge counts + nav links:

```
productAttachments  discussionAttachments  discussions  samples
measurementSets  claims  productBoms  packagingBoms  constructions  watchlists
```

Why it is hard to migrate:
- **Full graph traversal** — `getFilteredResourceAndLevelWiseChildrenBasedOnPartnerACLPermission` with
  `maxDepth=null` loads the **entire** product subtree from the Relationship Service into memory.
- **Serial ACL checks** — every node gets its own ACL permission call (N nodes = N calls).
- **Double traversal** — when `parentProductId` is set the whole thing repeats for the parent.
- **8 domain types in one 200-line function**; **mixed data sources** (Relationship graph + Elastic + ACL);
  **tight coupling** — no domain team can own or deploy a slice independently.

## 2. What the spike must decide

- How the `ProductTechPack` aggregate is assembled under federation — which pattern serves it.
- Which domain contributes each slice (attachments, discussions, samples, claims, BOMs, measurements, constructions, watchlists).
- **Proposal so far (light, to validate):** each owning domain contributes its slice to one shared entity, instead of one helper calling every service.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
