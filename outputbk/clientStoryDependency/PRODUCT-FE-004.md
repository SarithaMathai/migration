## PRODUCT-FE-004 — Migrate product status and workspace-context reads
Queries in scope: getProductStatus · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-B-01, PRODUCT-BE-B-02, PRODUCT-BE-B-03, PRODUCT-BE-G-06, PRODUCT-BE-G-07, PRODUCT-BE-G-09, PRODUCT-BE-G-13, PRODUCT-BE-S-01 · Spikes — SPIKE-04 · New — NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getProduct | PRODUCT-BE-B-01 | — | No | getProductStatus |  |
| getProductsByIds | PRODUCT-BE-B-02 | — | No | getProductStatus |  |
| getProductStatus | PRODUCT-BE-B-03 | — | No | getProductStatus |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| firstRoundSampleReceivedBySampleFormat | NEW-PRODUCT-BE-G-?? | — | Yes | getProductStatus |  |
| firstRoundSampleReceivedBySampleType | NEW-PRODUCT-BE-G-?? | — | Yes | getProductStatus |  |
| productSamplesReceivedBySampleFormat | NEW-PRODUCT-BE-G-?? | — | Yes | getProductStatus |  |
| productSamplesReceivedBySampleType | NEW-PRODUCT-BE-G-?? | — | Yes | getProductStatus |  |
| totalProducts | NEW-PRODUCT-BE-G-?? | — | Yes | getProductStatus |  |
| totalProductsRequested | NEW-PRODUCT-BE-G-?? | — | Yes | getProductStatus |  |
| totalProductsWithBp | NEW-PRODUCT-BE-G-?? | — | Yes | getProductStatus |  |
| businessPartners | PRODUCT-BE-G-07 | vmm | No | getProductStatus | 🔬 SPIKE-04 (gated) |
| code | PRODUCT-BE-S-01 | — | No | getProductStatus |  |
| departments | PRODUCT-BE-G-13 | ig | No | getProductStatus |  |
| productWorkspaceInfo | PRODUCT-BE-G-09 | workspaceV2 | No | getProductStatus |  |
| teams | PRODUCT-BE-G-06 | teamV2 | No | getProductStatus |  |
| vendorAttributes | PRODUCT-BE-G-07 | vmm | No | getProductStatus | 🔬 SPIKE-04 (gated) |

## PRODUCT-FE-004 — Readiness
9 of 16 distinct fields/entities resolve to existing backend stories. 7 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored. 1 field(s) sit behind an unresolved spike (SPIKE-04) and cannot be built past the spike's decision.
