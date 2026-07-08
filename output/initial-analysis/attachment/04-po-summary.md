# Phase 4: PO Sprint Planning Summary — Attachment

> **Domain:** `attachment` · **Target DGS:** separate `plm-attachment` subgraph · **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Stories:** [04-stories.md](./04-stories.md)
> Day-ranges are **AI-estimated — confirm in refinement.** Stories carry complexity only.

## What Are We Building?

- We are moving the **Attachment** domain — files/documents, their gallery renders, tags, ACL permissions and resource associations — off the `spark-internal-graphql` gateway into its **own `plm-attachment` DGS subgraph**.
- Attachment is referenced by **product** (`attachments`, `attachmentsWithMetaData`, copy flows),
**productDetails**, **packaging**, **workspace**, **sample**, and **claims**.

- It is **mid-sized**: 8 queries (+1 deprecated drift), 15 mutations, ~32 field resolvers on a 318-line resolver, with **no polymorphism**.
- The defining wrinkle is the **dual record shape** — the backend serves attachments in both elastic `snake_case` and api `camelCase`, so ~18 field resolvers coalesce today; the DGS port should normalize that at the DTO boundary.

**ACL note:** read tokens are context-only, **but** `updateAttachmentsACLPermissions` and the permissions arm
of `bulkUpdateAttachments` are **ACL *writes*** (granting ADMIN/READ to partners) — that IS build work.

## Migration Scope
| Surface | Count | Notes |
|---|---|---|
| Queries | 8 (+1 deprecated drift) | V3 reads, by-resource (relationship+ACL), renders, from-related (🔴 search) |
| Mutations | 15 | archive/delete/copy/associate, tags, attributes/bulk, gallery publish, ACL writes, teams |
| Field-resolver type blocks | ~5 | `Attachment` (~25) + gallery/3d/packet sub-types |
| External dependencies | 6 keys | search 🔴; relationship/tag/user-profile 🟡; vmm/gallery 🔵 |
| Federation role | provides `Attachment` entity | product/productDetails/packaging/workspace/sample/claims |
| **Total stories** | **26** | green-field; separate subgraph |

## Story Summary by Phase (AI-estimated)
| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 5 | 6–11d |
| D | Mutations | 14 | 20–33d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 3 | 12–20d |
| **Total** | | **26** | **42–71d** (buffered) |

> One engineer ≈ **9–15 sprints**. Parallelizable after B01.

> **Phase A dissolved.** Schema skeleton, service wiring, and external stubs are a one-time checklist in **B01** (completed in the same PR). No separate Phase A stories.

> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.

## Key Risk Areas
| Risk | Severity | What the PO needs to know |
|---|---|---|
| Dual record shape (snake/camel) | 🟡 Medium | Normalize at the DTO boundary so it doesn't leak into the schema |
| `bulkUpdateAttachments` fire-and-forget (returns undefined) | 🟡 Medium | Confirm the contract; await + return updated |
| ACL-permission writes treated as "ignored" | 🟡 Medium | They ARE build work (grant data), not authorization — port them |
| Gallery publish/unpublish V3-vs-legacy branch | 🟢 Low | Preserve the `ATC-` prefix branch |
| `SearchAttachment` vs `Attachment` confusion | 🟢 Low | Keep the two shapes distinct in the supergraph |

## Decisions Required
| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `bulkUpdateAttachments` — await and return the updated attachments? | D08 | Backend Eng |
| 2 | Canonical DTO target for the dual record shape | B01 | Product Owner |
| 3 | Delete or `@deprecated`-keep `getAttachments` (drift) + the deprecated renders/tag ops | F02 | Product Owner |

## Dependency Map
```
plm-attachment (Attachment subgraph) depends on (all cross-subgraph):
 search 🔴 (related-resource lookups)
 relationship, tag, user-profile 🟡 ; access-control (perms + ACL writes)
 Hive Gateway → VMM ; gallery (asset files)
 provides → Attachment entity for product/productDetails/packaging/workspace/sample/claims
```

## Recommended Sprint Sequencing
| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | B01 (DGS module init + service wiring + first resolver) | schema (canonical DTO), service port, reads |
| 3 | D01–D07 | single-resource + tag/associate mutations |
| 4 | D08–D14 | bulk updates, ACL writes, gallery, teams |
| 5 | F01/F02 + G01 | entity fetcher + drift + core field resolvers |
| 6 | G02 + G03 | gallery/tags resolvers + tests |

## Capacity Planning
| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~10–17 sprints | sequential |
| 2 engineers | ~6–10 sprints | reads + mutations parallel after B01 |

---
*Pipeline 2.0 — Phase 4 complete. Attachment artifacts: 01, 02, 03×2, 04-stories, 04-stories-index, 04-po, 05 (8 files). Separate `plm-attachment` subgraph.*
