## PRODUCT-FE-011 — Migrate component status rollups
Queries in scope: getProduct · Mutations excluded: 2

**Must complete first:** BE — PRODUCT-BE-B-01, PRODUCT-BE-F-10, PRODUCT-BE-G-01, PRODUCT-BE-G-02, PRODUCT-BE-G-03, PRODUCT-BE-G-06, PRODUCT-BE-G-07, PRODUCT-BE-G-08, PRODUCT-BE-G-09, PRODUCT-BE-G-10, PRODUCT-BE-G-13, PRODUCT-BE-G-14, PRODUCT-BE-S-01 · Spikes — SPIKE-04, SPIKE-05 · New — NEW-PRODUCT-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getProduct | PRODUCT-BE-B-01 | — | — | No | getProduct |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| currentUserPermissions | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct | via `...AttachmentsWithMetaData` |
| isResourceCritical | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct | via `...AttachmentsWithMetaData` |
| linkedResourceId | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct | via `...AttachmentsWithMetaData` |
| resourcePermissions | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct |  |
| resourceTitle | NEW-PRODUCT-BE-G-?? | — | — | Yes | getProduct | via `...AttachmentsWithMetaData` |
| ancestryProducts | PRODUCT-BE-G-10 | relationship | — | No | getProduct |  |
| attachments | PRODUCT-BE-G-03 | attachment | — | No | getProduct |  |
| attachmentsV3 | PRODUCT-BE-G-03 | attachment | — | No | getProduct |  |
| attachmentsWithMetaData | PRODUCT-BE-G-01 | attachment | — | No | getProduct |  |
| brand | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| businessPartners | PRODUCT-BE-G-07 | vmm | PRODUCT-BE-F-11 | No | getProduct | 🔬 SPIKE-04 (gated) |
| childProducts | PRODUCT-BE-G-10 | relationship | — | No | getProduct |  |
| clazz | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| components | PRODUCT-BE-G-02 | search | — | No | getProduct | 🔬 SPIKE-05 (gated) |
| createdBy | PRODUCT-BE-G-14 | user-profile | — | No | getProduct |  |
| department | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| departments | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| discussionsV2 | PRODUCT-BE-G-06 | discussion | — | No | getProduct |  |
| division | PRODUCT-BE-G-13 | ig | — | No | getProduct |  |
| droppedPartners | PRODUCT-BE-G-07 | vmm | PRODUCT-BE-F-11 | No | getProduct | 🔬 SPIKE-04 (gated) |
| productWorkspaceInfo | PRODUCT-BE-G-09 | workspaceV2 | — | No | getProduct |  |
| status | PRODUCT-BE-G-07 | vmm | — | No | getProduct | 🔬 SPIKE-04 (gated) |
| tags | PRODUCT-BE-G-13 | tag | — | No | getProduct |  |
| workspaces | PRODUCT-BE-G-09 | workspaceV2 | — | No | getProduct |  |

## PRODUCT-FE-011 — Readiness
23 of 28 distinct fields/entities resolve to existing backend stories. 5 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored. 2 field(s) sit behind an unresolved spike (SPIKE-04, SPIKE-05) and cannot be built past the spike's decision.
