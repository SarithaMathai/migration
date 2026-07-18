# Domain Service Catalog (snapshot-adapted)

Single source of truth for per-domain facts. Adapted for the `code/` `.txt` snapshot: endpoints come
from **service constructors**, not `context.js`.

## Backend base (product family)
- **URL:** `https://spark-product.dev.target.com` · **Repo:** `spark-product` · **Target DGS:** `plm-product`
- All product-family services build `this.endpoint = \`${endpoint}/enterprise_product_development_products/...\``
  where `${endpoint}` is this base.

> **Schema location:** the source SDL for every domain lives in `code/schemas/SPARK_{Domain}.txt`
> (e.g. `code/schemas/SPARK_Product.txt`). `code/schemas/core.txt` holds shared scalars/base types and
> `code/schemas/index.txt` is the stitch-order manifest. These are the schema source of truth.

> **`plm-product` is a monorepo / single subgraph.** Every product-family domain below compiles into the
> **same** DGS subgraph. Their cross-references are **internal GraphQL types** (no federation). Only the
> EXT keys further down (separate DGSs + platforms) use `@extends @external` / gateway stitch. See
> [reference-federation-patterns.md §0](./reference-federation-patterns.md).

## Product-family domains (co-located on `plm-product`)

| Loader key | Service class | Schema (`code/schemas/`) | Resolver (`code/`) | Service (`code/`) |
|-----------|--------------|--------------------------|--------------------|-------------------|
| `product` | `ProductService` | `SPARK_Product.txt` | `resolvers/SPARK_Product.txt` | `services/Product.txt` |
| `bom` | `BomService` | `SPARK_Bom.txt` | `resolvers/product/SPARK_Bom.txt` | `services/product/Bom.txt` |
| `impression` | `ImpressionService` | `SPARK_Impression.txt` | `resolvers/product/SPARK_Impression.txt` | `services/product/Impression.txt` |
| `measurement` | `MeasurementService` | `SPARK_Measurement.txt` | `resolvers/product/SPARK_Measurement.txt` | `services/product/Measurement.txt` |
| `packaging` | `PackagingService` | `SPARK_Packaging.txt` | `resolvers/product/SPARK_Packaging.txt` | `services/product/Packaging.txt` |
| `productDetails` | `ProductDetailsService` | `SPARK_ProductDetail.txt` | `resolvers/product/SPARK_ProductDetail.txt` | `services/product/ProductDetails.txt` |

## EXT loader keys seen in the product family (tag with severity)

| Loader key | Owning DGS / platform | Migrate to DGS? | Default severity |
|-----------|-----------------------|-----------------|------------------|
| `materialHub` | MaterialHubService | Yes (sibling) | 🟡 |
| `trim` | TrimService | Yes (sibling) | 🟡 |
| `wash` | WashService | Yes (sibling) | 🟡 |
| `fabric` | FabricService | Yes (sibling) | 🟡 |
| `combination` | CombinationService | Yes (sibling) | 🟡 |
| `search` | SearchService (elastic) | Yes (sibling) | 🔴 when business-critical |
| `accessControl` | AccessControlService | Yes (sibling) | 🔴 (ACL/JWT) |
| `tag` | TagService | Yes (sibling) | 🔵 |
| `product` | ProductService | same DGS (internal call) | — internal |
| `workspaceV2` | WorkspaceService | Yes (sibling) | 🟡 |
| `vmm` / `location` / `brand` | VMM platform | **No — Gateway stitch** | 🔵 |
| `clazz`/`department`/`division` / `ig` | Item Groups (IG) | **No — Gateway stitch** | 🔵 |
| `doppler`/`apex`/`nexusAttributes`/`ldap`/`corona`/`coronaItems` | External platforms | **No — Gateway stitch** | 🔵 |
| `relationship` | RelationshipService | Yes (sibling) | 🟡 |
| `userAttributes` | UserProfileService | Yes (sibling) | 🟡 |
| `teamV2` | TeamService | Yes (sibling — later-phase `team` subgraph) | 🟡 |
| `sampleV2` | SampleService | Yes (sibling — separate DGS `plm-sample`) | 🟡 |
| `recentlyViewed` / `todo` / `favorite` | Dashboard services | Yes (sibling) | 🔵 |
| `ruleLibrary` | RuleLibraryService | Yes (sibling) | 🔵 |
| `fileLibrary` | FileLibraryService | Yes (sibling) | 🔵 |
| `productAsk` | ProductAskService | Yes (sibling — co-located, product-family) | 🔵 |
| `productVariation` | ProductVariationService | Yes (sibling — co-located, product-family) | 🔵 |
| `userGroup` | UserGroupService | Yes (sibling) | 🔵 |
| `specificationsTemplate` | SpecificationsTemplateService | Yes (sibling) | 🟡 |
| `measurementTemplate` / `sizeTemplate` / `tightFit` | Measurement (templates) services | Yes (sibling) | 🟡 |

## Core utils → DGS equivalents

| Util | Purpose | DGS equivalent |
|------|---------|----------------|
| `loadOne` / `loadListing` | DataLoader GET with ACL + transform | `@DgsDataLoader` + `MappedBatchLoaderWithContext` / Feign |
| `postOne` / `putOne` / `deleteOne` | write + transform + primeKey | Service method + Feign write |
| `convertFunctions` (`deepToCamelCase`/`deepToSnakeCase`) | case conversion | Jackson `PropertyNamingStrategies.SnakeCaseStrategy` |
| `commonLoaders.getUserPermissionsJWT` | ACL capability token | header forwarding via `@DgsContext` filter |
| `workspaceAssociationHelper` | workspace assoc/dissoc | service method calling associate/dissociate endpoints |
| `accessControlUtils` | chunked permission load | batched ACL service call |

## Adding a new domain
Look up its three sources and add a catalog row (above). Then run the pipeline via
[`RUN-NEW-DOMAIN.md`](./RUN-NEW-DOMAIN.md). The four candidate domains below are **all done**; plus
`workspace` (`plm-workspace`), `sample` (`plm-sample`), `attachment` (`plm-attachment`) and `discussion`
(`plm-discussion`) were analyzed on request:

| Loader key | Schema (`code/schemas/`) | Resolver (`code/`) | Service (`code/`) | Subgraph | Status |
|-----------|--------------------------|--------------------|-------------------|----------|--------|
| `claims` | `SPARK_Claims.txt` | `resolvers/product/SPARK_Claims.txt` | `services/Claim.txt` | **separate DGS** | ✅ done |
| `productDetails` | `SPARK_ProductDetail.txt` | `resolvers/product/SPARK_ProductDetail.txt` | `services/product/ProductDetails.txt` | plm-product (co-located) | ✅ done |
| `watchlist` | `SPARK_Watchlist.txt` | `resolvers/product/SPARK_Watchlist.txt` | `services/product/Watchlist.txt` | **plm-product (co-located)** | ✅ done |
| `search` | `SPARK_Search.txt` | `resolvers/SPARK_Search.txt` | `services/Search.txt` | separate DGS (elastic) | ✅ done |
| `workspace` | `SPARK_WorkspaceV2.txt` | `resolvers/SPARK_WorkspaceV2.txt` | `services/WorkspaceV2.txt` | **separate DGS (plm-workspace)** | ✅ done |
| `sample` | `SPARK_SampleV2.txt` | `resolvers/SPARK_SampleV2.txt` | `services/SampleV2.txt` | **separate DGS (plm-sample)** | ✅ done |
| `attachment` | `SPARK_Attachment.txt` | `resolvers/SPARK_Attachment.txt` | `services/Attachment.txt` | **separate DGS (plm-attachment)** | ✅ done |
| `discussion` | `SPARK_Discussion.txt` + `SPARK_DiscussionV3.txt` | `resolvers/SPARK_Discussion.txt` (+V3) | `services/Discussion.txt` (+V3) | **separate DGS (plm-discussion)** | ✅ done |

## Effort calibration (PO summary only — AI-estimated, confirm in refinement)
Low/Small 1–2d · Medium 3–5d · High/Large 5–8d · Very-High/X-Large 8–13d · +20% buffer on domain totals.
