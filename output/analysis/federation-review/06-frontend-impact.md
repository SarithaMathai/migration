# 06 · Frontend Impact Assessment

> Phase 6 of the federation review · 2026-07-17
> Baseline: the program FE analysis ([fe-05-federation-impact.md](../program/fe-05-federation-impact.md)) already covers the migration-wide impacts (gateway endpoint, `SPARK_` renames, flattened→entity selections). This document covers only the **delta** introduced by this review (required fixes R1–R6 + recommended fields REC-1…6).

## 1. Required fixes (R1–R6) — client-visible impact

| Fix | Client impact | Action |
|---|---|---|
| R1/R2 (VMM key `id`) | None — keys are server-side; clients already select `id` | none |
| R3 (`Claim`→`Claims`; entity keys uniformly `id`, synthesized from humanId where absent) | **Fragment type-conditions and `__typename` logic** must target `Claims` (the prefix-drop of `SPARK_Claims`); with `id` now present, Apollo's default id normalization applies — documents must **select `id`** on `Claims` | PRODUCT-FE-012 (new verification story) |
| R4 (`ProductDetails` name; `Packaging`/`Watchlist`/`Dieline` synthesized `id`) | Same class of risk: `__typename`-driven code must use `ProductDetails`; select `id` on packaging/watchlist/dieline documents for default cache normalization | PRODUCT-FE-012 |
| R5 (claims shareable value types) | None — wire shapes unchanged | none |
| R6 (CORONA key) | None either way — `itemDetails` stays an embedded selection | none |

## 2. Recommended fields (REC-1…6) — operation-level impact when adopted

All are additive: **no existing operation breaks**; adoption is optional per screen. Representative selection-set updates:

### REC-1 · BOM supplier (queries in `src/libs/product-queries/src/queries/BomQueries.tsx` — 18 selections of `supplierId`/`supplierName`)

```graphql
# current                          # updated (adoption optional)
materials {                        materials {
  supplierId                         supplierId          # kept — row identity & edit flows
  supplierName                       supplier { id name role { bpRoleName } }
}                                  }
```

- Generated TS: `BomMaterialInterface` gains `supplier?: VmmBusinessPartner` (codegen re-run; union of 7 impls all gain it).
- Apollo cache: `VMM_BusinessPartner` already normalizes by `id` — rows now link to the shared partner entity instead of carrying copies.
- Hooks/components: supplier pickers in the BOM grid can drop their secondary `getBusinessPartnersByIds` fetch.
- Tests: BOM grid snapshots regenerate; MSW mocks add `supplier`.

### REC-2 · Impression attachment (`searchImpressionsByProductId` in `product-queries__ProductQueries.txt:306`)

```graphql
# current                          # updated
impressions { id name              impressions { id name
  attachmentId                       attachmentId        # kept — thumbnail URL building
}                                    attachment { id }   # entity-stitched metadata when needed
                                   }
```

### REC-3 · Watchlist partner

```graphql
businessPartners {                 businessPartners {
  partnerId partnerName              partnerId partnerName
}                                    partner { id name }
                                   }
```

### REC-4/5/6 · Measurement sample ref / product partner rows / lineage

- `sampleMeasurement { sample { id } }` becomes available from the sample screens (`samples__SampleBulkEvaluateQueries.txt`).
- `vendorAttributes { partner { id name } }` removes the client-side join against `businessPartners` in the vendor-status rail.
- `ancestryProducts { product { id description } }` replaces follow-up `getProductsByIds` calls in lineage views.

## 3. Cross-cutting FE workstreams (delta)

- **Generated TypeScript:** one codegen run per adopted REC; no type removals, so no forced compile breaks.
- **Apollo cache:** with the program id-key decision (2026-07-17), `Claims`/`Packaging`/`Watchlist`/`Dieline` expose a synthesized `id` and normalize by Apollo's default — no `keyFields` needed, but every cached document must select `id`. Explicit `keyFields` remain only for `SampleMeasurementSet: ["sampleId"]` and `ResourcesCount: ["productId","partnerId"]` (verify against the platform cache-remap done in the completed PLATFORM-FE-003).
- **UI components / hooks:** only on REC adoption (listed above); none for R-fixes.
- **Fragments:** sweep for type-conditions on `Claim`/`ProductDetail` legacy names (PRODUCT-FE-012); the completed platform fragment sweep predates R3/R4 and must be re-verified for these two names.
- **Testing:** federated-vs-legacy JSON parity diffs (existing per-story pattern) remain the acceptance mechanism; PRODUCT-FE-012 adds a `__typename` assertion pass.

## 4. New / updated FE stories

| Story | Type | Status |
|---|---|---|
| PRODUCT-FE-012 · Verify fragment type-conditions, `__typename` logic and cache `keyFields` against federated type names/keys | Required verification | added to fe-08 |
| BOM-FE-007 · Adopt BOM `supplier` entity references (REC-1) | Optional, PO-gated | added to fe-08 |
| Other REC adoptions | Optional | documented here; stories to be cut per screen only after PO approval (avoid inventory noise) |
