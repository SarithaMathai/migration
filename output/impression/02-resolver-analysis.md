# Impression — Resolver Analysis: Queries

> **Domain:** `impression` · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

2 queries.

---

## Q1 · `searchImpressionsByProductId(id, partnerIds, workspaceIds, enableWorkspaceContextFiltering) : [SPARK_Impression]` — CAT-2 · Small (1–2d)

```
permissionJWT = await getUserPermissionsJWT(id, ctx)
return ctx.loaders.impression.searchImpressionsByProductId(permissionJWT, id, partnerIds, workspaceIds, enableWorkspaceContextFiltering)
```

**Service:** `GET /enterprise_product_development_products/impressions/product/{productId}?workspaceIds=&partnerIds=` with JWT header. Manual query-string assembly per array element.

**Findings:**
- 🔴 **`enableWorkspaceContextFiltering` is silently dropped** — service signature only takes `(jwt, productId, partnerIds, workspaceIds)`. Fix during port (either honor it or remove from schema after confirming clients don't rely on it).
- 🟢 Manual query-string assembly → replace with Feign multi-param.

---

## Q2 · `getImpressionCountsByProductId(id) : SPARK_ImpressionCount` — CAT-2 · Small (1–2d)

```
permissionJWT = await getUserPermissionsJWT(id, ctx)
return ctx.loaders.impression.searchImpressionsByProductId(permissionJWT, id)   // returns ARRAY
// counts field resolver then receives the array as parent and bucketizes per partner
```

**Finding 🔴 schema-shape mismatch:** Returns `[SPARK_Impression]` from a field typed `SPARK_ImpressionCount`. Works because the `counts` field resolver treats the parent as an array. **Port strategy:** return a typed `ImpressionCountResult` wrapper containing the impressions internally; field resolver reads `parent.impressions`.

---

## Effort

| Tier | Queries | Days |
|---|---|---|
| Small | Q1, Q2 | 2–4 |

---

**Phase Completed:** Phase 2A — Query Resolvers
