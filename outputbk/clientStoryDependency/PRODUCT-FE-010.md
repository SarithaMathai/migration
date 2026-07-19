## PRODUCT-FE-010 — Migrate TechPack count queries (facade-then-federate)
Queries in scope: getProductTechPackCountV1, getProductTechPackBulkCountV1 · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-E-03, PRODUCT-BE-E-04, PRODUCT-BE-F-06, PRODUCT-BE-F-08, PRODUCT-BE-G-08, PRODUCT-BE-H-01, PRODUCT-BE-H-02, PRODUCT-BE-H-03, PRODUCT-BE-H-05

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getProductTechPackBulkCountV1 | PRODUCT-BE-E-04 | — | No | getProductTechPackBulkCountV1 |  |
| getProductTechPackCountV1 | PRODUCT-BE-E-03 | — | No | getProductTechPackCountV1 |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| claims | PRODUCT-BE-G-08 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| constructions | PRODUCT-BE-H-05 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| discussionAttachments | PRODUCT-BE-H-01 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| discussions | PRODUCT-BE-H-02 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| measurementSets | PRODUCT-BE-G-08 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| packagingBoms | PRODUCT-BE-F-06 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| productAttachments | PRODUCT-BE-H-01 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| productBoms | PRODUCT-BE-F-06 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| sample | PRODUCT-BE-H-03 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |
| watchlists | PRODUCT-BE-F-08 | — | No | getProductTechPackBulkCountV1, getProductTechPackCountV1 |  |

## PRODUCT-FE-010 — Readiness
All 12 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
