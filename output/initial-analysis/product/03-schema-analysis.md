# Phase 3: Federation Schema Analysis — Product

> **Domain:** `product` · **Target DGS:** `ProductService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 38 🔜 | 3 ⏭ — 41 operations**

This is the design view + the **Confluence approach page** for the flagship domain.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 3 | `Product` (`id`), `ProductRules` (`id`), `ResourcesCount` (`productId partnerId` composite) |
| Owned value types | ~40 | status/workspace/attachment/component/category/doppler/rules/copy/template types |
| Union (`@DgsTypeResolver`) | 1 | `Categories` (12 members, default `IG_Clazz_Filter`) |
| `@shareable` | ~10 | `Paging`, `Pageable`, `CodeDescription`, `CodeDescriptionOrder`, `AccessV3`, `WorkspaceStatus`, `ResourcePermissions`, `PermissionEntry`, `SpgFileLibrary` |
| External stub — platform | 6 | `VMM_*`, `IG_*`, `DopplerCapacityType`, `CORONA_ItemDetails` |
| External stub — sibling DGS | ~16 | `Attachment`, `SampleV2`, `Tag`, `WorkspaceV2`, `TeamV2`, `UserProfileAttributes`, `Discussion`, `DiscussionThread`, `FileLibrary`, `Bom`, `Claim`, `Measurement`, `ProductDetail`, `Packaging`, `ProductAsk`, `ProductVariation` |
| Inputs | ~30 | `ProductInput`, `ProductUpdateInput`, `CarryForwardProductInput`, … |

> **Co-location note:** many "external stubs" (`Bom`, `Measurement`, `Claim`, `ProductDetail`, `Packaging`,
> `ProductAsk`, `ProductVariation`, `FileLibrary`) are **co-located in the same `plm-product` DGS** — they
> appear as stubs in the schema but resolve via internal service calls at runtime, not cross-subgraph hops.

## 2. Polymorphism — `Categories` (`@DgsTypeResolver`)
**Source SDL:** `interface SPARK_Categories { id, name }` (`schemas/core.graphqls:116`), with 13
- implementers.
- **Target:** modeled as a **union** of the **12** concrete types the resolver's `__resolveType` actually returns (`resolvers/SPARK_Product.js:2470-2511`): `VMM_Brand`, `IG_Department`, `IG_Division`, `IG_Clazz_Filter`, `ProductStatus`, `VMM_BusinessPartnerCategory`, `Tag_Elastic`, `Filter_SetDates`, `Status`, `FilterSampleType`, `FilterSampleFormat`, `Packaging_Field`.
**Default branch → `IG_Clazz_Filter`** (preserve).
- `IG_MerchType` implements the interface in the SDL but is **never returned** by this resolver — omitted.
- **Union vs interface is deliberate:** four members are platform/external stubs that can't `implements`
- a local interface across subgraphs.
- **⚠ Client-contract caveat:** an interface lets clients select `id`/`name` directly on `[Categories]`; a union requires inline fragments.
- Survey consumers before cutover.

## 3. Composite-key Aggregate — `ResourcesCount` (TechPack)
- `@key(fields:"productId partnerId")` with 11 stub fields, each annotated with its owning subgraph (attachment/discussion/sample/measurement/claim/bom/construction/watchlist).
- Migration uses **Option D** (facade-then-federate) — see [reference-federation-patterns.md §3](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

## 4. Client Contract Verification
18 queries + 20 mutations preserved (`0 ✅ | 38 🔜`). 3 schema-drift partner wrappers are **deferred ⏭**
(traffic routes through `productBusinessPartnerActions`) — confirm consumers before deleting.

## 5. Federation Boundaries
- **Product owns** `Product`, `ProductRules`, `ResourcesCount` + ~40 value types.
- **Internal (same DGS)** resolution: bom/claims/measurementSets/productBom/packagingBom/productDetails/variations/associateProductsAsks.
- **Cross-subgraph EXT:** attachment, workspace, search/elastic, discussion, sample, tag, team, user-profile, relationship, claim.
- **Platform (gateway):** VMM, IG, Doppler, CORONA, APEX, Brand Compliance.
- **Contributes/owns** the TechPack `ResourcesCount` type that 8 sibling subgraphs extend (Phase F).

## 6. Migration Approach  *(Confluence approach page)*

Product is the **largest and highest-risk** domain and the **host DGS** for the whole product family.
Recommended sequence:

1. **Phase A:** schema skeleton, ~40 owned types + 30 inputs, external stubs, the `Categories`
   `@DgsTypeResolver`, the `ResourcesCount` composite-key type, and the `ProductService` Kotlin port
   (42 methods → grouped service interfaces; co-located methods are internal, only rating/rules-flag stay Feign).
2. **Phase B:** simple reads (`getProduct`, `getProductsByIds`, `getProductStatus`, versions, copy status, rules CRUD reads).
3. **Phase C:** search/listing (`getProducts` two-stage hydration, `getProductTemplates`, `getCategories`, `getRatingByTcin`).
4. **Phase D:** core mutations (add/update/bulk/teams/partners/resources/toggles/rules).
5. **Phase E:** the hard ones — `productBusinessPartnerActions` (M10), `updateComponentStatuses` (M20),
   and **TechPack** (`getProductTechPackCountV1`/Bulk) via the **Option D facade**.
6. **Phase F:** TechPack `ResourcesCount` field ownership. **Monorepo split:** `measurementSets` (measurement),
- `productBoms`/`packagingBoms`/`boms` (bom), and `watchlists` (watchlist) are filled by **internal** `@DgsData` (co-located, F04/F06/F08); the other **5** fields (attachment/discussion/sample/claim/construction) use **true federation** `extend type ResourcesCount` placeholders BLOCKED-BY each separate domain.
- Then facade retirement, gateway composition, platform stub verification, deferred-wrapper decision.
7. **Phase G:** ~14 field-resolver stories (incl. the two X-Large: `attachmentsWithMetaData`, `components`),
   the `division` bug fix, utils ports, and the test/parity harness.

**TechPack — recommended Option D (hybrid):** ship a thin `@DgsQuery` over a temporary aggregation facade
(extract `getTechPackResourceCountMap`) so the query works day 1; then federate each stub field to its owning
subgraph; then retire the facade. Fix the **bulk ordering bug** during the port.

## 7. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| TechPack composite-key aggregate (Q8/Q9) | High | High | Option D facade-then-federate; bulk-order fix | Tech Lead + Platform |
| `productBusinessPartnerActions` partial failure (M10) | Medium | High | Saga / compensation log — decision required | Tech Lead |
| `components` N+1 ACL regression (G02) | Medium | Medium | Batch ACL on port | Backend Eng |
| `attachmentsWithMetaData` perf (G01) | Medium | High | Parallel fetch + cached relationship walk | Backend Eng |
| `Product.division` bug fix changes shape (G12) | Medium | Medium | Feature-flag during cutover; client survey | PO |
| `USE_NEW_RULES_API` legacy delete | Low | High | Verify all envs `true`; staged rollout | PO |
| Deferred partner wrappers may have live consumers | Medium | Medium | Traffic survey before delete (Phase F) | PO |
| External rating secret handling | Low | Medium | Move `SPARK_GATEWAY_API_KEY` to Vault | Platform |

## 8. ACL Handling
The source curries capability tokens via `getUserPermissionsJWT`/`getAccessControlBatch` on nearly every
read/write because product resources are partner/workspace-scoped and the backend authorizes per resource.
**Per decision, ACL is ignored in the DGS implementation** — there is **no ACL plumbing story**. Each
affected operation carries a one-line context note; the `accessControl` loader is marked **context-only**,
not a 🔴 build dependency.

## 9. Open Questions
1. TechPack facade: Node extract vs Kotlin aggregation service?
2. `productBusinessPartnerActions` rollback strategy?
3. Delete or `@deprecated` the 3 drift wrappers?
4. `USE_NEW_RULES_API` — does rules stay in `plm-product` or move to its own subgraph?
5. `Product.division` bug — feature-flag the fix during cutover?

---
**Phase Completed:** Phase 3 · **Domain:** `product`.
