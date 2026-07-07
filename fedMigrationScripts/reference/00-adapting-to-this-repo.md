# Adapting the framework to *this* repo (read before analyzing a new domain)

This framework was originally written for the **full** `spark-internal-graphql` checkout. The
snapshot we actually have (`../../code`) is smaller and differently shaped. This page lists every
assumption that changed, so you don't get blocked.

> **Update (2026-06-27):** the source `.graphql` schemas are now included in the snapshot under
> `code/schemas/` (as `.txt`). The earlier draft was produced before they were available and had to
> *derive* the schema from resolver shapes. **From now on, `code/schemas/SPARK_{Domain}.txt` is the
> primary schema source of truth** — cross-check it against the resolver, don't re-derive from scratch.

---

## 1. What the source snapshot actually contains

```
code/
├── resolvers/         # .txt — GraphQL resolvers (the behaviour)        ✅ source of truth
│   ├── product/       #         co-located product-family resolvers
│   ├── activityLogUtilities/
│   ├── commonResolvers/
│   └── material/ ...
├── services/          # .txt — REST client classes (endpoints + auth)  ✅ source of truth
├── utils/             # .txt — shared helpers (loaders, transforms)     ✅ source of truth
└── schemas/           # .txt — the actual GraphQL SDL, one file per type-bundle  ✅ source of truth
    ├── SPARK_Product.txt   #   e.g. the Product SDL (`extend type Query/Mutation`, types, inputs)
    ├── SPARK_Bom.txt       #   …one per domain, named SPARK_{Domain}.txt
    ├── core.txt            #   shared scalars / base types (core.graphql)
    └── index.txt           #   the loader manifest (lists every .graphql file, in stitch order)
```

**There is still no `context.js`** (endpoint/auth facts come from the service constructor — see §3).
The schema files, however, **are now present**: each `schemas/SPARK_{Domain}.txt` holds the real SDL
for that domain. Use it directly; only fall back to deriving from the resolver if a field is missing.

## 2. Rule changes vs. the original skills

| Original skill said | In this repo, do instead |
|---------------------|--------------------------|
| "Read `context.js` for url/repo/auth" | **Read the service file's constructor.** Each service builds its own endpoint, e.g. `BomService` sets `this.endpoint = \`${endpoint}/enterprise_product_development_products/bom/v1\``. The `${endpoint}` base is the `spark-product` backend (see catalog). Auth headers are visible inline (`SPARK-Capability-Token: permissionJWT`). |
| "Read `schemas/SPARK_{Domain}.graphql`" | **Read `code/schemas/SPARK_{Domain}.txt`** — it is that SDL, just with a `.txt` extension. It carries real **nullability** (`!`), arguments, and `@deprecated`/`@key` directives the resolver can't tell you. Cross-check it against the resolver for *behaviour* (a field declared in SDL may have no top-level resolver — a "schema-drift" op). Only derive a field from the resolver if it is genuinely absent from the SDL. |
| "Record schema line count" | Record **schema / resolver / service / utils** line counts. The schema line count is now real (e.g. `code/schemas/SPARK_Product.txt` = 802). |
| "Files use `.js` / `.graphql`" | Files are `.txt`. Cite them as `resolvers/product/SPARK_Bom.txt:84-90`. |
| "Co-located domains share a backend URL from `context.js`" | Co-located domains are inferred from the **folder** (`resolvers/product/*`, `services/product/*`) and the shared `${endpoint}/enterprise_product_development_products/...` base built in each service constructor. |

## 3. How to read endpoint + auth facts from a service file

Worked example — `services/product/Bom.txt`:

```js
this.endpoint = `${endpoint}/enterprise_product_development_products/bom/v1`   // base path
this.getBomByIds = (permissionJWT, ids) =>
  loadListing(`${this.endpoint}?ids=${ids}`,                                    // → GET .../bom/v1?ids=
    { ...this.headers, 'SPARK-Capability-Token': permissionJWT }, ...)          // → ACL token header
```

From that one method you can fill a whole story's REST section:
- **HTTP/endpoint:** `GET {spark-product}/enterprise_product_development_products/bom/v1?ids={ids}`
- **Auth:** `Authorization` (base header) **+** `SPARK-Capability-Token: {permissionJWT}` (per-call ACL)
- **Transform:** `deepToCamelCase(boms)` on the response → camelCase DTO in DGS (Jackson naming strategy).

## 4. How to spot an EXT (cross-domain) call

In a resolver, `ctx.loaders.{key}.{method}` is a call into the loader registry. If `{key}` is **not**
this domain's own key, it is an **EXT Service** call and must be tagged with severity. Examples from BOM:
`ctx.loaders.materialHub.*`, `ctx.loaders.trim.*`, `ctx.loaders.vmm.*`, `ctx.loaders.search.*`,
`ctx.loaders.tag.*`, `ctx.loaders.location.*`. The owning backend + DGS target for each key is in
[`domain-service-catalog.md`](./domain-service-catalog.md).

## 5. The backend base URL

Every product-family service is built with `${endpoint}` = the **`spark-product`** backend.
Use `https://spark-product.dev.target.com` (repo `spark-product`, target DGS `plm-product`) as the base
when you need a concrete URL. External platforms (VMM/IG/Doppler/…) keep their own bases — see catalog §2d.
