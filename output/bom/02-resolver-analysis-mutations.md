# Bom — Resolver Analysis: Mutations

> **Domain:** `bom` · **Source:** [resolvers/product/SPARK_Bom.js](spark-internal-graphql/packages/data-source-spark/src/resolvers/product/SPARK_Bom.js) (lines 226–315)
> **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

6 mutation resolvers.

---

## M1 · `addBom(sparkBom: SPARK_BomInput) : SPARK_Bom` — CAT-2 · Medium (3–5d)

**Pseudocode:**
```
bom = await ctx.loaders.bom.addBom(sparkBom)
if (bom.validationErrors || bom.message) throw new Error('Error creating bom\n' + JSON.stringify(bom))
return bom
```
**Service:** `POST /enterprise_product_development_products/bom/v1` (`postOne` with `transformRequest: deepToSnakeCase`, `transform: deepToCamelCase`, `primeKey: bom.humanId`).
**Notes:**
- **No JWT** on create (new resource, no ACL yet).
- Error surface is shape-sniffed (`validationErrors` or `message` keys) — port as typed `ValidationException` / `ServiceException` in Kotlin.
- `getDataLoader` primes the bom into the read loader cache.

---

## M2 · `updateBom(sparkBom: SPARK_UpdateBomInput) : SPARK_Bom` — CAT-2 · Large (5–8d)

**Pseudocode:**
```
permissionJWT = await getUserPermissionsJWT(sparkBom.humanId, ctx)
if (workspaceContext && (addWorkspaces.length || removeWorkspaces.length))
  await workspaceAssociationHelper(BOM, humanId, add, remove, ctx)   // mutates workspaces FIRST
bom = await ctx.loaders.bom.updateBom(permissionJWT, sparkBom)
if (bom.validationErrors || bom.message) throw new Error(...)
if (sparkBom.businessPartners)
  await ctx.loaders.bom.updatePermissions(permissionJWT).load(sparkBom)   // SECOND service call
return bom
```
**Services:**
1. `workspaceAssociationHelper(BOM, ...)` — calls `manageWorkspaceAssociations` (PUT `/{bomId}/associate_workspace` or `/dissociate_workspace`)
2. `PUT /enterprise_product_development_products/bom/v1/{humanId}` (main update)
3. Optional `PUT /{humanId}/permission` if `businessPartners` present

**Finding 🔴 atomicity:** Three sequential service calls with no rollback. If step 2 fails, workspace changes from step 1 are already committed. If step 3 fails, the bom is updated but ACL is stale. **Decision required:** saga/compensation or accept best-effort.

**Finding 🟡:** `omitParamsInBody: true` on the PUT — request body should not include the `{humanId}` path param. Confirm DGS request builder does the same.

---

## M3 · `manageBomWorkspaces(bomId, workspacesToAdd, workspacesToRemove) : SPARK_Bom` — CAT-2 · Small (1–2d)

**Pseudocode:**
```
result = undefined
if (toAdd.length || toRemove.length)
  result = await workspaceAssociationHelper(BOM, bomId, toAdd, toRemove, ctx)
return result
```
**Finding 🟡:** Returns `undefined` if both arrays empty. GraphQL nullable return covers this, but client may rely on a defined value. Document.

---

## M4 · `lockBom(bomId: String!) : SPARK_Bom` — CAT-2 · Small (<1d)

```
permissionJWT = await getUserPermissionsJWT(bomId, ctx)
return ctx.loaders.bom.lockBom(permissionJWT, bomId)   // PUT /{bomId}/lock
```

---

## M5 · `unlockBom(bomId: String!) : SPARK_Bom` — CAT-2 · Small (<1d)

Identical pattern, `PUT /{bomId}/unlock`.

---

## M6 · `updateBomComponentStatus(productId: String!, ids: [String], status: SPARK_ComponentStatusInput) : SPARK_BomPaged` — CAT-2 · Small (1–2d)

**Pseudocode:**
```
return ctx.loaders.bom.updateBomComponentStatus({productId, ids, status})
```
**Service:** `PUT /enterprise_product_development_products/bom/v1/component_status_update` with body `{productId, ids, status}`.
**Finding 🟡:** **No JWT.** Every other write mutation requires one. Confirm with backend whether ACL is enforced server-side or whether this is a gap. Same pattern observed in `Product.updateBomComponentStatuses` fan-out from Phase 2B of the product domain.

---

## Cross-Cutting Findings

| # | Finding | Severity |
|---|---|---|
| 1 | M2 has **3-step non-atomic write** (workspace, body, permissions) — rollback decision required | 🔴 |
| 2 | M6 missing JWT vs M2/M4/M5 — confirm intentional | 🟡 |
| 3 | Error detection by shape-sniffing (`validationErrors || message`) — replace with typed exceptions | 🟡 |
| 4 | `omitParamsInBody: true` quirk on M2 — verify DGS port matches | 🟢 |
| 5 | M1/M2 prime the read loader (`getDataLoader`/`primeKey`) — preserve via DGS DataLoader `prime()` after successful write | 🟡 |
| 6 | No bulk-mutation APIs in this domain (single-bom CRUD only) — simpler than product domain | 🟢 |

---

## Effort Summary

| Tier | Mutations | Days |
|---|---|---|
| Small | M3, M4, M5, M6 (4) | 3–6 |
| Medium | M1 (1) | 3–5 |
| Large | M2 (1) | 5–8 |
| **Subtotal mutations** | **6** | **11–19** |

---

**Phase Completed:** Phase 2B — Mutation Resolvers
**Output:** [output/bom/02-resolver-analysis-mutations.md](output/bom/02-resolver-analysis-mutations.md)
