# Impression — Resolver Analysis: Field Resolvers

> **Domain:** `impression` · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

6 field resolvers across 2 types.

---

## C1 · `SPARK_Impression` (5 fields) — CAT-2 · Small (1–2d)

| Field | Implementation |
|---|---|
| `businessPartners` | `impression.partnerIds && loadBpsWithType(partnerIds.map(id => ({partnerId: id})), ctx)` (VMM) |
| `owningBusinessPartner` | `impression.owningPartnerId && loadBp(ctx, impression.owningPartnerId)` (VMM) |
| `workspaces` | If `workspaceContext.length > 0` → `SPARK_WorkspaceV2.Query.getWorkspacesByIdsV2({}, {ids}, ctx)`; else `[]` |
| `createdBy` | `impression.createdBy && userAttributes.getUserByID.load(createdBy)` |
| `updatedBy` | `impression.updatedBy && userAttributes.getUserByID.load(updatedBy)` |

**Findings:**
- 🟢 All 5 fields become federation entity-fetcher stubs in DGS (VMM, workspace, user-profile).
- 🟡 `partnerIds.map(id => ({partnerId: id}))` — re-wrap to match `loadBpsWithType` shape. Verify util signature when porting.
- 🟡 Cross-resolver call `SPARK_WorkspaceV2.Query.getWorkspacesByIdsV2` — replace with native service-method or federation entity call.

---

## C2 · `SPARK_ImpressionCount.counts` — CAT-2 · Small (1–2d)

```
try {
  parentId = impressions[0].parentId          // !!! TypeError on empty array
  product = await product.getByID.load(parentId)
  partners = (product.businessPartners || []).map(p => p.partnerId)
  partnerCounts = partners.map(partnerId => ({
    bpType: partnerId,
    counts: impressions.filter(imp => imp.partnerIds.includes(partnerId)).length
  }))
  return partnerCounts.concat({bpType: 'totalCount', counts: impressions.length})
} catch (error) {
  logger.error('error fetching product impression counts - returning dummy counts', ctx.logContext, {error})
  return [{bpType: 'totalCount', counts: 0}]
}
```

**Findings:**
- 🔴 Receives array-from-Q2-resolver as parent — schema-shape mismatch (see Q2). Restructure to typed wrapper in port.
- 🟡 `impressions[0].parentId` — TypeError on empty array (caught by try/catch but masks the bug).
- 🟡 `bpType` field is `ID`-ish but uses literal `'totalCount'` string — type-tag the sum entry differently (e.g. separate `totalCount: Int!` field on the wrapper type).
- 🟡 Silent error → `[{bpType: 'totalCount', counts: 0}]` dummy. Replace with `null` propagation + structured error.

---

## Effort

| Block | Days |
|---|---|
| C1 (5 field resolvers, all cross-DGS stubs) | 1–2 |
| C2 (counts bucketizer + restructure) | 1–2 |
| **Subtotal field resolvers** | **2–4** |

---

**Phase Completed:** Phase 2C — Field Resolvers
