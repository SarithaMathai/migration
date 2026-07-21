## PRODUCT-FE-006 — Migrate product rules administration
Queries in scope: getProductRules, getProductRulesById, getAllAvailableRules, getProductDeptRules, getProductBPRules, searchProductRules · Mutations excluded: 3

**Must complete first:** BE — PRODUCT-BE-B-07, PRODUCT-BE-B-08, PRODUCT-BE-B-09, PRODUCT-BE-B-10, PRODUCT-BE-B-11, PRODUCT-BE-C-05, PRODUCT-BE-G-07, PRODUCT-BE-G-13, PRODUCT-BE-H-08 · Spikes — SPIKE-04

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getAllAvailableRules | PRODUCT-BE-B-09 | — | — | No | getAllAvailableRules |  |
| getProductBPRules | PRODUCT-BE-B-11 | — | — | No | getProductBPRules |  |
| getProductDeptRules | PRODUCT-BE-B-10 | — | — | No | getProductDeptRules |  |
| getProductRules | PRODUCT-BE-B-07 | — | — | No | getProductRules |  |
| getProductRulesById | PRODUCT-BE-B-08 | — | — | No | getProductRulesById |  |
| searchProductRules | PRODUCT-BE-C-05 | — | — | No | searchProductRules |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| businessPartners | PRODUCT-BE-G-07 | vmm | PRODUCT-BE-F-11 | No | getProductBPRules, getProductDeptRules, getProductRules, getProductRulesById, searchProductRules | 🔬 SPIKE-04 (gated); via `...ProductRules` |
| departments | PRODUCT-BE-G-13 | ig | — | No | getProductBPRules, getProductDeptRules, getProductRules, getProductRulesById, searchProductRules | via `...ProductRules` |
| insightsClassExclusion | PRODUCT-BE-H-08 | ig | PRODUCT-BE-H-08 | No | getProductBPRules, getProductDeptRules, getProductRules, getProductRulesById, searchProductRules | newly authored — PRODUCT-BE-H-08; via `...ProductRules` |

## PRODUCT-FE-006 — Readiness
9 of 9 distinct fields/entities resolve to existing backend stories. 1 field(s) sit behind an unresolved spike (SPIKE-04) and cannot be built past the spike's decision.
