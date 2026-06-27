# Measurement — Resolver Analysis: Queries

> **Domain:** `measurement` (+ `measurementTemplate`) · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

9 queries total (7 measurement + 2 template).

---

## Q1 · `getMeasurementByIds(ids, calculated) : SPARK_MeasurementsPaged` — CAT-2 · Small (1–2d)

```
permissionJWT = await getUserPermissionsJWT(ids, ctx)
return ctx.loaders.measurement.getMeasurementByIds(permissionJWT, ids, calculated)
```
**Service:** `GET /measurements/v1?ids=&calculated=&businessPartnerIds=&mustHaveRows=` (qs.stringify).

---

## Q2 · `getMeasurements(resourceId, calculated, businessPartnerIds, mustHaveRows) : SPARK_MeasurementsPaged` — CAT-2 · Medium (3–5d)

```
relationships = await relationship.findRelationships(resourceId, {includeNodeTypes:['measurement_set'], maxDepth:0})
ids = relationships.map(n => n.id)
if (!ids.length) return []                          // !!! returns [] but schema expects MeasurementsPaged
permissionJWT = await getUserPermissionsJWT(ids, ctx)
{content} = await measurement.getMeasurementByIds(permissionJWT, ids, calculated, businessPartnerIds, mustHaveRows)
return { content: orderBy(content, c -> new Date(c.createdAt), 'desc') }
```

**Findings:**
- 🟡 **Empty-result type mismatch:** `return []` from a query typed `SPARK_MeasurementsPaged` (object). Tolerated by JS but should return `{content: []}` in DGS port.
- 🟡 Relationship-tree pre-walk couples this query to `plm-relationship` availability.
- 🟢 Client-side sort — could move backend-side.

---

## Q3 · `getMeasurementsElastic(resourceId) : SPARK_MeasurementsPaged` — CAT-2 · Small (1–2d)

```
{content} = await search.getMeasurementSets.load({q: `parentId: ${resourceId}`})
return {content: orderBy(content, c -> new Date(c.createdAt), 'desc')}
```
String interpolation into elastic query — **injection risk if resourceId is user-supplied.** Confirm input validation.

---

## Q4 · `getUnitsOfMeasure(ids: [String]) : [SPARK_UnitsOfMeasure]` — CAT-2 · Small (<1d)

Master data; `GET /master_data/unit_of_measure[?ids=]`. Cacheable.

---

## Q5 · `getThicknessUnitsOfMeasure : [SPARK_UnitsOfMeasure]` — CAT-2 · Small (<1d)

Master data; cacheable.

---

## Q6 · `getMeasurementSetStatus : [SPARK_CodeDescription]` — CAT-2 · Small (<1d)

Master data; `GET /masterData?name=MeasurementSetStatus`. Cacheable.

---

## Q7 · `getSampleMeasurement(sampleId) : SPARK_SampleMeasurementSet` — CAT-2 · Small (1–2d)

`GET /measurements/v1/sample/{sampleId}` — **no JWT in resolver call** but service signature accepts one and uses it. Resolver inconsistency: caller passes `(sampleId)`, service expects `(permissionJWT, sampleId)`.

**Finding 🔴:** Resolver invocation `ctx.loaders.measurement.getSampleMeasurement(sampleId)` does **not** include `permissionJWT`. The service treats first arg as JWT — so the literal `sampleId` is sent as the SPARK-Capability-Token header. **Latent bug.**

---

## Q8 · `getMeasurementTemplates(page, size) : SPARK_MeasurementTemplatesPaged` — CAT-2 · Small (1–2d)

```
formattedParams = {...searchParams}
_.without(Object.keys(searchParams), 'size','page','q').forEach(key => {
  if (searchParams[key]) formattedParams[key] = searchParams[key].join(',')
})
return measurementTemplate.getMeasurementTemplates.load(_.omitBy(formattedParams, p => !p && p !== 0))
```

**Finding 🟡:** The array-join logic is dead code — `searchParams` only ever contains `page`/`size` (per schema). Either the schema is missing filter fields or this code is leftover. Decision required.

---

## Q9 · `getMeasurementTemplatesByIds(ids) : SPARK_MeasurementTemplatesPaged` — CAT-2 · Small (<1d)

`GET /measurement/templates/v1?ids=`. **No JWT** (master template data).

---

## Cross-Cutting Findings

| # | Finding | Severity |
|---|---|---|
| 1 | Q7 `getSampleMeasurement` passes `sampleId` where JWT is expected — latent bug | 🔴 |
| 2 | Q2 empty-result type mismatch (`[]` vs `MeasurementsPaged`) | 🟡 |
| 3 | Q3 elastic query string interpolation — input validation needed | 🟡 |
| 4 | Q8 dead array-join logic | 🟡 |
| 5 | Q4/Q5/Q6 master-data — cacheable | 🟢 perf |
| 6 | Q2 client-side sort — move to backend | 🟢 |

---

## Effort

| Tier | Queries | Days |
|---|---|---|
| Small | Q1, Q3, Q4, Q5, Q6, Q7, Q8, Q9 (8) | 6–11 |
| Medium | Q2 (1) | 3–5 |
| **Subtotal queries** | **9** | **9–16** |

---

**Phase Completed:** Phase 2A — Query Resolvers
