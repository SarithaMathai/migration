# Impression — Resolver Analysis: Mutations

> **Domain:** `impression` · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

1 mutation.

---

## M1 · `updateImpressions(productId, productImpression) : [SPARK_Impression]` — CAT-2 · Small (1–2d)

```
permissionJWT = await getUserPermissionsJWT(productId, ctx)
impression = await ctx.loaders.impression.updateImpressions(permissionJWT, productId, productImpression)
if (impression.validationErrors || impression.message) throw Error('Error updating impression set\n' + JSON.stringify(impression))
return impression
```

**Service:** `PUT /enterprise_product_development_products/impressions/product/{productId}` with body `{impressionsToDelete, impressionsToUpdate}`. Both `transform` and `transformRequest` for camelCase ↔ snake_case.

**Findings:**
- 🟢 Single-call atomic write (backend handles delete + update batch).
- 🟢 Error detection by shape-sniffing — replace with typed exception.
- 🟡 Input `SPARK_ImpressionInput.businessPartners: [SPARK_ProductPartnerInput]` exists but the resolver doesn't process it locally — backend handles. Confirm contract.

---

## Effort

| Tier | Mutations | Days |
|---|---|---|
| Small | M1 | 1–2 |

---

**Phase Completed:** Phase 2B — Mutation Resolvers
