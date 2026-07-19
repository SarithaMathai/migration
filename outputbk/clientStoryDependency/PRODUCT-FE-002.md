## PRODUCT-FE-002 — Migrate shared-library `getProduct` consumers
Queries in scope: getProduct, getProductVersions · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-B-01, PRODUCT-BE-B-04, PRODUCT-BE-G-01, PRODUCT-BE-G-02, PRODUCT-BE-G-03, PRODUCT-BE-G-06, PRODUCT-BE-G-07, PRODUCT-BE-G-08, PRODUCT-BE-G-09, PRODUCT-BE-G-10, PRODUCT-BE-G-13, PRODUCT-BE-G-14 · Spikes — SPIKE-04, SPIKE-05 · New — NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getProduct | PRODUCT-BE-B-01 | — | No | getProduct |  |
| getProductVersions | PRODUCT-BE-B-04 | — | No | getProductVersions |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| resourcePermissions | NEW-PRODUCT-BE-G-?? | — | Yes | getProduct |  |
| ancestryProducts | PRODUCT-BE-G-10 | relationship | No | getProduct |  |
| attachments | PRODUCT-BE-G-03 | attachment | No | getProduct |  |
| attachmentsV3 | PRODUCT-BE-G-03 | attachment | No | getProduct |  |
| attachmentsWithMetaData | PRODUCT-BE-G-01 | attachment | No | getProduct |  |
| brand | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| businessPartners | PRODUCT-BE-G-07 | vmm | No | getProduct | 🔬 SPIKE-04 (gated) |
| childProducts | PRODUCT-BE-G-10 | relationship | No | getProduct |  |
| claims | PRODUCT-BE-G-08 | — | No | getProduct |  |
| clazz | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| components | PRODUCT-BE-G-02 | search | No | getProduct | 🔬 SPIKE-05 (gated) |
| createdBy | PRODUCT-BE-G-14 | user-profile | No | getProduct |  |
| department | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| departments | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| discussionsV2 | PRODUCT-BE-G-06 | discussion | No | getProduct |  |
| division | PRODUCT-BE-G-13 | ig | No | getProduct |  |
| droppedPartners | PRODUCT-BE-G-07 | vmm | No | getProduct | 🔬 SPIKE-04 (gated) |
| productWorkspaceInfo | PRODUCT-BE-G-09 | workspaceV2 | No | getProduct |  |
| status | PRODUCT-BE-G-07 | vmm | No | getProduct | 🔬 SPIKE-04 (gated) |
| tags | PRODUCT-BE-G-13 | tag | No | getProduct |  |
| workspaces | PRODUCT-BE-G-09 | workspaceV2 | No | getProduct |  |

## PRODUCT-FE-002 — Readiness
22 of 23 distinct fields/entities resolve to existing backend stories. 1 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored. 2 field(s) sit behind an unresolved spike (SPIKE-04, SPIKE-05) and cannot be built past the spike's decision.
