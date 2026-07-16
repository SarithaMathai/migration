# Story Dependency Matrix — Frontend × Backend

> Generated from 08-frontend-stories.md · 2026-07-16
> A frontend story is not Done until every backend story it depends on has been delivered.

| FE story | Title | Impact | Depends on (BE / FE) | Domain |
|---|---|---|---|---|
| BOM-FE-001 | Statically expand BOM fragment factories (pre-cutover) | High | PLATFORM-FE-005 | BOM |
| BOM-FE-002 | Migrate BOM core reads | High | BOM-BE-B-01, BOM-BE-B-03, BOM-BE-B-04, BOM-FE-001, PLATFORM-FE-003 | BOM |
| BOM-FE-003 | Migrate BOM search and elastic reads | High | BOM-BE-C-01, BOM-BE-S-03, PLATFORM-FE-003 | BOM |
| BOM-FE-004 | Migrate BOM master-data reads | Low | BOM-BE-B-05, BOM-BE-B-06, BOM-BE-B-07, BOM-BE-B-08 | BOM |
| BOM-FE-005 | Migrate BOM supplier reads | Medium | BOM-BE-C-03, BOM-BE-C-04, BOM-BE-C-05 | BOM |
| BOM-FE-006 | Migrate BOM mutations including `updateBom` saga handling | High | BOM-BE-D-01, BOM-BE-D-03, BOM-BE-D-04, BOM-BE-D-05, BOM-BE-S-01, PLATFORM-FE-003 | BOM |
| CLAIM-FE-001 | Split the claim fragment factory and re-target claim fragments | Medium | PLATFORM-FE-005 | Claims |
| CLAIM-FE-002 | Migrate claim reads (first cross-subgraph cutover) | High | CLAIM-BE-B-01, CLAIM-BE-B-02, CLAIM-BE-B-03, CLAIM-BE-B-04, CLAIM-FE-001, PLATFORM-FE-003 | Claims |
| CLAIM-FE-003 | Migrate claim simple mutations and export | Medium | CLAIM-BE-D-01, CLAIM-BE-D-02, CLAIM-BE-D-03, CLAIM-BE-D-04, CLAIM-BE-D-05 | Claims |
| CLAIM-FE-004 | Migrate `updateClaim` multi-step write handling | High | CLAIM-BE-E-01, PLATFORM-FE-003 | Claims |
| IMPRESSION-FE-001 | Migrate `getBomDataAndImpressions` (with BOM wave) | Low | IMPRESSION-BE-B-01, BOM-BE-B-01, BOM-FE-002, PLATFORM-FE-003 | Impression |
| IMPRESSION-FE-002 | Migrate `getCarryForwardFormData` (with Product wave) | Low | IMPRESSION-BE-B-01, PRODUCT-BE-B-01, PRODUCT-FE-001 | Impression |
| MST-FE-001 | Migrate measurement reads and retire `humanId` | Medium | MST-BE-B-01, MST-BE-B-04, PLATFORM-FE-004 | Measurement |
| MST-FE-002 | Migrate measurement list/search reads | Medium | MST-BE-C-01, MST-BE-C-02 | Measurement |
| MST-FE-003 | Migrate measurement master-data reads | Low | MST-BE-B-02, MST-BE-B-03 | Measurement |
| MST-FE-004 | Migrate measurement mutations | Medium | MST-BE-D-03, MST-BE-D-04, MST-BE-D-06, MST-BE-D-07, PLATFORM-FE-003 | Measurement |
| PDTL-FE-001 | Migrate product-details reads | Low | PDTL-BE-B-01, PLATFORM-FE-004 | Product Details |
| PDTL-FE-002 | Migrate product-details simple mutations | Medium | PDTL-BE-D-01, PDTL-BE-D-03, PDTL-BE-D-04, PDTL-BE-D-05 | Product Details |
| PDTL-FE-003 | Migrate `updateProductDetailsSet` saga handling | Medium | PDTL-BE-E-01, PLATFORM-FE-003 | Product Details |
| PKG-FE-001 | Migrate packaging reads | Medium | PKG-BE-B-01, PKG-BE-B-02, PLATFORM-FE-004 | Packaging |
| PKG-FE-002 | Migrate packaging master-data reads and retire deprecated fields | Low | PKG-BE-B-04, PKG-BE-B-06 | Packaging |
| PKG-FE-003 | Migrate dieline flows | Medium | PKG-BE-B-03, PKG-BE-B-05, PKG-BE-D-02 | Packaging |
| PKG-FE-004 | Migrate packaging simple mutations and export | Medium | PKG-BE-D-01, PKG-BE-D-03, PKG-BE-D-04, PKG-BE-D-05, PKG-BE-D-06, PKG-BE-D-07, PKG-BE-D-09 | Packaging |
| PKG-FE-005 | Migrate `updatePackaging` saga handling and packet information | High | PKG-BE-E-01, PLATFORM-FE-003 | Packaging |
| PLATFORM-FE-001 | Federated router endpoint behind a feature flag | High | — | Platform |
| PLATFORM-FE-002 | Codegen against the federated schema | High | PLATFORM-FE-001 | Platform |
| PLATFORM-FE-003 | Apollo cache identity remap and cutover reset | High | PLATFORM-FE-002 | Platform |
| PLATFORM-FE-004 | Phase-1 fragment rename sweep (`on SPARK_*` → federated types) | Medium | PLATFORM-FE-002 | Platform |
| PLATFORM-FE-005 | Statically expand runtime-composed gql factories | High | — | Platform |
| PRODUCT-FE-001 | Migrate `getProduct` documents in product-queries | High | PRODUCT-BE-B-01, PLATFORM-FE-003, PLATFORM-FE-004 | Product |
| PRODUCT-FE-002 | Migrate shared-library `getProduct` consumers | Medium | PRODUCT-BE-B-01, PRODUCT-BE-B-04, PRODUCT-FE-001 | Product |
| PRODUCT-FE-003 | Migrate product list and bulk reads | High | PRODUCT-BE-S-02, PRODUCT-BE-B-02, PLATFORM-FE-003 | Product |
| PRODUCT-FE-004 | Migrate product status and workspace-context reads | Medium | PRODUCT-BE-B-03, PLATFORM-FE-003 | Product |
| PRODUCT-FE-005 | Migrate template library and categories reads | Medium | PRODUCT-BE-C-02, PRODUCT-BE-C-03, PLATFORM-FE-004 | Product |
| PRODUCT-FE-006 | Migrate product rules administration | Medium | PRODUCT-BE-B-07, PRODUCT-BE-B-08, PRODUCT-BE-B-09, PRODUCT-BE-B-10, PRODUCT-BE-B-11, PRODUCT-BE-C-05, PRODUCT-BE-D-15, PRODUCT-BE-D-16, PRODUCT-BE-D-17 | Product |
| PRODUCT-FE-007 | Migrate simple product mutations | Medium | PRODUCT-BE-D-01, PRODUCT-BE-D-02, PRODUCT-BE-D-03, PRODUCT-BE-D-04, PRODUCT-BE-D-05, PRODUCT-BE-D-10, PRODUCT-BE-D-13, PRODUCT-BE-D-14 | Product |
| PRODUCT-FE-008 | Migrate team and partner assignment mutations | Medium | PRODUCT-BE-D-06, PRODUCT-BE-D-07, PRODUCT-BE-D-12, PRODUCT-FE-001 | Product |
| PRODUCT-FE-009 | Migrate partner drop/undrop orchestration | High | PRODUCT-BE-S-03, PRODUCT-BE-D-09, PLATFORM-FE-003 | Product |
| PRODUCT-FE-010 | Migrate TechPack count queries (facade-then-federate) | Medium | PRODUCT-BE-E-03, PRODUCT-BE-E-04 | Product |
| PRODUCT-FE-011 | Migrate component status rollups | Medium | PRODUCT-BE-B-01, PRODUCT-BE-D-18, PRODUCT-BE-E-02 | Product |
| WATCHLIST-FE-001 | Migrate watchlist reads | Low | WATCHLIST-BE-B-01, WATCHLIST-BE-C-01, PLATFORM-FE-004 | Watchlist |
| WATCHLIST-FE-002 | Migrate watchlist create and clone mutations | Low | WATCHLIST-BE-D-01, WATCHLIST-BE-D-02 | Watchlist |
| WATCHLIST-FE-003 | Migrate `updateWatchlistEntries` saga handling | Medium | WATCHLIST-BE-E-01, PLATFORM-FE-003 | Watchlist |

## Reverse index — backend story → blocked frontend stories

| BE story | Blocks FE stories |
|---|---|
| BOM-BE-B-01 | BOM-FE-002, IMPRESSION-FE-001 |
| BOM-BE-B-03 | BOM-FE-002 |
| BOM-BE-B-04 | BOM-FE-002 |
| BOM-BE-B-05 | BOM-FE-004 |
| BOM-BE-B-06 | BOM-FE-004 |
| BOM-BE-B-07 | BOM-FE-004 |
| BOM-BE-B-08 | BOM-FE-004 |
| BOM-BE-C-01 | BOM-FE-003 |
| BOM-BE-C-03 | BOM-FE-005 |
| BOM-BE-C-04 | BOM-FE-005 |
| BOM-BE-C-05 | BOM-FE-005 |
| BOM-BE-D-01 | BOM-FE-006 |
| BOM-BE-D-03 | BOM-FE-006 |
| BOM-BE-D-04 | BOM-FE-006 |
| BOM-BE-D-05 | BOM-FE-006 |
| BOM-BE-S-01 | BOM-FE-006 |
| BOM-BE-S-03 | BOM-FE-003 |
| CLAIM-BE-B-01 | CLAIM-FE-002 |
| CLAIM-BE-B-02 | CLAIM-FE-002 |
| CLAIM-BE-B-03 | CLAIM-FE-002 |
| CLAIM-BE-B-04 | CLAIM-FE-002 |
| CLAIM-BE-D-01 | CLAIM-FE-003 |
| CLAIM-BE-D-02 | CLAIM-FE-003 |
| CLAIM-BE-D-03 | CLAIM-FE-003 |
| CLAIM-BE-D-04 | CLAIM-FE-003 |
| CLAIM-BE-D-05 | CLAIM-FE-003 |
| CLAIM-BE-E-01 | CLAIM-FE-004 |
| IMPRESSION-BE-B-01 | IMPRESSION-FE-001, IMPRESSION-FE-002 |
| MST-BE-B-01 | MST-FE-001 |
| MST-BE-B-02 | MST-FE-003 |
| MST-BE-B-03 | MST-FE-003 |
| MST-BE-B-04 | MST-FE-001 |
| MST-BE-C-01 | MST-FE-002 |
| MST-BE-C-02 | MST-FE-002 |
| MST-BE-D-03 | MST-FE-004 |
| MST-BE-D-04 | MST-FE-004 |
| MST-BE-D-06 | MST-FE-004 |
| MST-BE-D-07 | MST-FE-004 |
| PDTL-BE-B-01 | PDTL-FE-001 |
| PDTL-BE-D-01 | PDTL-FE-002 |
| PDTL-BE-D-03 | PDTL-FE-002 |
| PDTL-BE-D-04 | PDTL-FE-002 |
| PDTL-BE-D-05 | PDTL-FE-002 |
| PDTL-BE-E-01 | PDTL-FE-003 |
| PKG-BE-B-01 | PKG-FE-001 |
| PKG-BE-B-02 | PKG-FE-001 |
| PKG-BE-B-03 | PKG-FE-003 |
| PKG-BE-B-04 | PKG-FE-002 |
| PKG-BE-B-05 | PKG-FE-003 |
| PKG-BE-B-06 | PKG-FE-002 |
| PKG-BE-D-01 | PKG-FE-004 |
| PKG-BE-D-02 | PKG-FE-003 |
| PKG-BE-D-03 | PKG-FE-004 |
| PKG-BE-D-04 | PKG-FE-004 |
| PKG-BE-D-05 | PKG-FE-004 |
| PKG-BE-D-06 | PKG-FE-004 |
| PKG-BE-D-07 | PKG-FE-004 |
| PKG-BE-D-09 | PKG-FE-004 |
| PKG-BE-E-01 | PKG-FE-005 |
| PRODUCT-BE-B-01 | IMPRESSION-FE-002, PRODUCT-FE-001, PRODUCT-FE-002, PRODUCT-FE-011 |
| PRODUCT-BE-B-02 | PRODUCT-FE-003 |
| PRODUCT-BE-B-03 | PRODUCT-FE-004 |
| PRODUCT-BE-B-04 | PRODUCT-FE-002 |
| PRODUCT-BE-B-07 | PRODUCT-FE-006 |
| PRODUCT-BE-B-08 | PRODUCT-FE-006 |
| PRODUCT-BE-B-09 | PRODUCT-FE-006 |
| PRODUCT-BE-B-10 | PRODUCT-FE-006 |
| PRODUCT-BE-B-11 | PRODUCT-FE-006 |
| PRODUCT-BE-C-02 | PRODUCT-FE-005 |
| PRODUCT-BE-C-03 | PRODUCT-FE-005 |
| PRODUCT-BE-C-05 | PRODUCT-FE-006 |
| PRODUCT-BE-D-01 | PRODUCT-FE-007 |
| PRODUCT-BE-D-02 | PRODUCT-FE-007 |
| PRODUCT-BE-D-03 | PRODUCT-FE-007 |
| PRODUCT-BE-D-04 | PRODUCT-FE-007 |
| PRODUCT-BE-D-05 | PRODUCT-FE-007 |
| PRODUCT-BE-D-06 | PRODUCT-FE-008 |
| PRODUCT-BE-D-07 | PRODUCT-FE-008 |
| PRODUCT-BE-D-09 | PRODUCT-FE-009 |
| PRODUCT-BE-D-10 | PRODUCT-FE-007 |
| PRODUCT-BE-D-12 | PRODUCT-FE-008 |
| PRODUCT-BE-D-13 | PRODUCT-FE-007 |
| PRODUCT-BE-D-14 | PRODUCT-FE-007 |
| PRODUCT-BE-D-15 | PRODUCT-FE-006 |
| PRODUCT-BE-D-16 | PRODUCT-FE-006 |
| PRODUCT-BE-D-17 | PRODUCT-FE-006 |
| PRODUCT-BE-D-18 | PRODUCT-FE-011 |
| PRODUCT-BE-E-02 | PRODUCT-FE-011 |
| PRODUCT-BE-E-03 | PRODUCT-FE-010 |
| PRODUCT-BE-E-04 | PRODUCT-FE-010 |
| PRODUCT-BE-S-02 | PRODUCT-FE-003 |
| PRODUCT-BE-S-03 | PRODUCT-FE-009 |
| WATCHLIST-BE-B-01 | WATCHLIST-FE-001 |
| WATCHLIST-BE-C-01 | WATCHLIST-FE-001 |
| WATCHLIST-BE-D-01 | WATCHLIST-FE-002 |
| WATCHLIST-BE-D-02 | WATCHLIST-FE-002 |
| WATCHLIST-BE-E-01 | WATCHLIST-FE-003 |
