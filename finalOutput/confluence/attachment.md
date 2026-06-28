# Attachment — Migration to a dedicated `plm-attachment` DGS (PO view)

> **Paste this page into Confluence.** Audience: Product Owner / stakeholders.
> Deep dives: [migration approach & schema](../attachment/03-schema-analysis.md) ·
> [field inventory](../attachment/05-attribute-inventory.md) · [engineering stories](../attachment/04-stories.md).
> Create tickets from [`../jira/attachment.csv`](../jira/attachment.csv). Effort is **AI-estimated — confirm in refinement.**

## What are we building?

We are moving the **Attachment** domain — files/documents, their gallery renders, tags, ACL permissions and
resource associations — off the `spark-internal-graphql` gateway into its **own `plm-attachment` DGS
subgraph**. Attachment is referenced by **product** (`attachments`, `attachmentsWithMetaData`, copy flows),
**productDetails**, **packaging**, **workspace**, **sample**, **claims** and **discussion**.

It is **mid-sized**: 8 queries (+1 deprecated drift), 15 mutations, ~32 field resolvers on a 318-line resolver,
with **no polymorphism**. The defining wrinkle is the **dual record shape** — the backend serves attachments in
both elastic `snake_case` and api `camelCase`, so ~18 field resolvers coalesce today; the DGS port should
normalize that at the DTO boundary.

**ACL note:** read tokens are context-only, **but** `updateAttachmentsACLPermissions` and the permissions arm
of `bulkUpdateAttachments` are **ACL *writes*** (granting ADMIN/READ to partners) — that IS build work.

## Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 8 (+1 deprecated drift) | V3 reads, by-resource (relationship+ACL), renders, from-related (🔴 search) |
| Mutations | 15 | archive/delete/copy/associate, tags, attributes/bulk, gallery publish, ACL writes, teams |
| Field-resolver type blocks | ~5 | `Attachment` (~25) + gallery/3d/packet sub-types |
| Polymorphism | none | — |
| External dependencies | 6 keys | search 🔴; relationship/tag/user-profile 🟡; vmm/gallery 🔵 |
| Federation role | provides `Attachment` entity | product/productDetails/packaging/workspace/sample/claims/discussion |
| **Total stories** | **28** | green-field; separate subgraph |

## Effort by phase (AI-estimated, +20% buffer)

| Phase | Name | Stories | Effort |
|---|---|---|---|
| A | Foundation & Schema | 4 | 9–15d |
| B | Core Reads | 5 | 6–11d |
| D | Mutations | 14 | 20–33d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 3 | 12–20d |
| **Total** | | **28** | **51–86d** (buffered) |

## Key risks

| Risk | Severity | What the PO needs to know |
|---|---|---|
| Dual record shape (snake/camel) | 🟡 Medium | Normalize at the DTO boundary so it doesn't leak into the schema |
| `bulkUpdateAttachments` fire-and-forget (returns undefined) | 🟡 Medium | Confirm the contract; await + return updated |
| ACL-permission writes treated as "ignored" | 🟡 Medium | They ARE build work (grant data), not authorization — port them |
| Gallery publish/unpublish V3-vs-legacy branch | 🟢 Low | Preserve the `ATC-` prefix branch |
| `SearchAttachment` vs `Attachment` confusion | 🟢 Low | Keep the two shapes distinct in the supergraph |

## Decisions required

| # | Decision | Blocks | Owner |
|---|---|---|---|
| 1 | `bulkUpdateAttachments` — await and return the updated attachments? | D08 | Backend Eng |
| 2 | Canonical DTO target for the dual record shape | A02 | Architect |
| 3 | Delete or `@deprecated`-keep `getAttachments` (drift) + the deprecated renders/tag ops | F02 | Architect |

## Migration approach (summary)

Phase **A** schema (canonical DTO that collapses the dual record shape + ~external stubs) + the service port;
**B** the V3/by-resource/renders/from-related reads; **D** the single-resource then bulk writes (archive/
delete/copy/associate, tags, attributes, gallery publish, **ACL writes**, teams); **F** expose `Attachment` as
a federated entity + the drift decision; **G** the field-resolver surface (`Attachment` + gallery/3d/packet) +
tests. Full detail: [03-schema-analysis.md §Migration Approach](../attachment/03-schema-analysis.md).

## Sequencing & capacity

Parallelizable after A; **1–2 engineers** (~6–10 sprints for two vs ~10–17 for one). Reads and mutations run in
parallel after the canonical DTO lands. Full plan: [04-po-summary.md](../attachment/04-po-summary.md).

---
*PO page assembled from the attachment analysis. Tickets:
[`../jira/attachment.csv`](../jira/attachment.csv) · [`../jira/attachment-stories.md`](../jira/attachment-stories.md).*
