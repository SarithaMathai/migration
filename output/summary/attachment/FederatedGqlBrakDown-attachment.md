# Federated GraphQL Breakdown — Attachment

| | |
|---|---|
| **Target DGS** | `plm-attachment (separate)` |
| **T-Shirt Size** | **L** |
| **Total Stories** | 24 |
| **Complexity** | 🔴 0 Very High · 🟠 2 High · 🟡 14 Medium · 🟢 8 Low |
| **Phase Coverage** | 📖 B · ✏️ D · 🔗 F · 🧪 G |
| **Generated** | 2026-07-07 |

> **Icons:** 🔷 Query · 🔶 Mutation · 🔸 Field Resolver  · 🔴 Very High · 🟠 High · 🟡 Medium · 🟢 Low  · 🔬 Spike · 🔴🔬 spike-gated story · 🧱 A · 📖 B · 🔍 C · ✏️ D · ⚙️ E · 🔗 F · 🧪 G

---

## What Are We Building?

- We are moving the **Attachment** domain — files/documents, their gallery renders, tags, ACL permissions and resource associations — off the `spark-internal-graphql` gateway into its **own `plm-attachment` DGS subgraph**.
- Attachment is referenced by **product** (`attachments`, `attachmentsWithMetaData`, copy flows),
**productDetails**, **packaging**, **workspace**, **sample**, and **claims**.

- It is **mid-sized**: 8 queries (+1 deprecated drift), 15 mutations, ~32 field resolvers on a 318-line resolver, with **no polymorphism**.
- The defining wrinkle is the **dual record shape** — the backend serves attachments in both elastic `snake_case` and api `camelCase`, so ~18 field resolvers coalesce today; the DGS port should normalize that at the DTO boundary.

**ACL note:** read tokens are context-only, **but** `updateAttachmentsACLPermissions` and the permissions arm
of `bulkUpdateAttachments` are **ACL *writes*** (granting ADMIN/READ to partners) — that IS build work.

---

## Migration Scope

| Surface | Count | Notes |
|---|---|---|
| Queries | 8 (+1 deprecated drift) | V3 reads, by-resource (relationship+ACL), renders, from-related (🔴 search) |
| Mutations | 15 | archive/delete/copy/associate, tags, attributes/bulk, gallery publish, ACL writes, teams |
| Field-resolver type blocks | ~5 | `Attachment` (~25) + gallery/3d/packet sub-types |
| External dependencies | 6 keys | search 🔴; relationship/tag/user-profile 🟡; vmm/gallery 🔵 |
| Federation role | provides `Attachment` entity | product/productDetails/packaging/workspace/sample/claims |
| **Total stories** | **26** | green-field; separate subgraph |

---

## Spikes & Complex Cases

> This domain's complex, cross-cutting problems are tracked once as **program spikes** in the global breakdown — see **Phase 0 — Program Spikes** (the table) and **Spike Detail** (the brief, the decision, intended cross-domain steps, and every affected resolver's external deps + current logic) in the "Federated+Graphql+Stories+-+BreakDown" overview. Nothing from there is repeated here; the stories below just **link** to it.

> _No spike-gated stories in this domain._

> Simple, intuitive decisions (drift-op cleanup, dead-method audits, auth-token parity, sort/DTO shape) are resolved inline in the owning story — they are **not** spikes.

---

## Effort Snapshot

| Phase | Name | Stories | Effort (est., +20%) |
|---|---|---|---|
| B | Core Reads | 5 | 6–11d |
| D | Mutations | 14 | 20–33d |
| F | Federation & decisions | 2 | 4–7d |
| G | Field Resolvers & Tests | 3 | 12–20d |
| **Total** | | **26** | **42–71d** (buffered) |

> One engineer ≈ **9–15 sprints**. Parallelizable after B01.


> **Self-contained story model.** The DGS-on-REST framework already exists; every operation story is **end-to-end in one PR** — schema (query/mutation + the GraphQL types it returns) + DGS data fetcher + Kotlin REST service method (read/write) + push the schema change to **Hive**. The standalone `*Service` Kotlin-port story has been dissolved into the operation stories.


**Capacity Planning**

| Team size | Calendar | Notes |
|---|---|---|
| 1 engineer | ~10–17 sprints | sequential |
| 2 engineers | ~6–10 sprints | reads + mutations parallel after B01 |

---

## Recommended Sprint Sequencing

| Sprint | Stories | Focus |
|---|---|---|
| 1–2 | B01 (DGS module init + service wiring + first resolver) | schema (canonical DTO), service port, reads |
| 3 | D01–D07 | single-resource + tag/associate mutations |
| 4 | D08–D14 | bulk updates, ACL writes, gallery, teams |
| 5 | F01/F02 + G01 | entity fetcher + drift + core field resolvers |
| 6 | G02 + G03 | gallery/tags resolvers + tests |

---

## Jira Stories by Phase

> Each row is one Jira story. Complexity drives T-shirt sizing in refinement. `Depends On` lists blocking story IDs within this domain — including Phase 0 spikes where a story's implementation is gated on a spike's outcome.

### 📖 Phase B — Core Reads (5 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔷 `SPARK-ATCH-B01`<br>`getAttachmentsV3(ids)` | 🟢 Low `XS` | Query | — | **Intent —** Fetch full attachment records for a set of ids.<br>**Today —** empty ids → []; token → GET …<br>**Done when:**<br>• returns attachments; empty ids → [] |
| 🔷 `SPARK-ATCH-B02`<br>`getAttachmentsByResource(resourceId)` | 🟡 Medium `M` | Query<br>Calls: `relationship` | B01 | **Intent —** List the attachments hanging off a given resource (product, sample, etc.).<br>**Today —** (relationship) searchByIds({id, includeNodeTypes:['attachments','attachments_v3'], maxDepth:0}) → ids → (accessControl) getUserAccessByPost → getAttachmentsByPostV3<br>**Done when:**<br>• relationship→ids→attachments chain |
| 🔷 `SPARK-ATCH-B03`<br>`getAttachmentsByResourceAndOwner(resourceId)` | 🟡 Medium `M` | Query<br>Calls: `relationship` | B01 | **Intent —** List a resource's attachments, filtered to a specific owner/author.<br>**Today —** (relationship) ids → getAttachmentsByIdsAndAuthorByPostV3<br>**Done when:**<br>• returns attachments incl. author |
| 🔷 `SPARK-ATCH-B04`<br>Renders queries (`getRendersForAttachmentIds`/`V3Ids`/`byPost`) | 🟡 Medium `M` | Query | B01 | **Intent —** Get the generated render/preview images for attachments.<br>**Today —** map each id → renders loader (betaMode), compact; byPost uses an ACL token<br>**Done when:**<br>• each variant returns renders; betaMode honored |
| 🔷 `SPARK-ATCH-B05`<br>`getAttachmentsfromRelatedResource(s)` | 🟡 Medium `M` | Query<br>Calls: `search` | B01 | **Intent —** Find attachments reachable through a resource's related resources.<br>**Today —** (search) searchAttachmentsByParentAndRelatedResource / …ByRelatedResource(s) → content or []<br>**Done when:**<br>• parent+related vs related-only branches |

> **`SPARK-ATCH-B01`** — **Note — DGS Module Init (this PR only):** Creates `attachment.graphqls` (federation v2.3 header, scalars, owned types with `@key`, external stubs), registers scalars in `ScalarConfig.kt`, and wires the service and Feign client. Full type list: 03-schema.graphql.


### ✏️ Phase D — Mutations (14 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔶 `SPARK-ATCH-D01`<br>`archiveAttachmentV3` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Archive (soft-remove) an attachment.<br>**Today —** token → archiveAttachmentV3(id)<br>**Done when:**<br>• archives |
| 🔶 `SPARK-ATCH-D02`<br>`deleteAttachmentV3` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Permanently delete an attachment.<br>**Today —** token → deleteAttachmentV3(humanId) → String<br>**Done when:**<br>• deletes; returns status |
| 🔶 `SPARK-ATCH-D03`<br>`copyAttachmentsV3` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Copy attachments onto another resource.<br>**Today —** token for humanIds → copyAttachmentsV3<br>**Done when:**<br>• copies; returns thumbnail + copies |
| 🔶 `SPARK-ATCH-D04`<br>`associateResourcesV3` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Link an attachment to additional resources.<br>**Today —** token → associateResourcesV3<br>**Done when:**<br>• associates resources |
| 🔶 `SPARK-ATCH-D05`<br>`removeResourcesV3` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Unlink an attachment from resources.<br>**Today —** token → removeResourcesV3<br>**Done when:**<br>• removes resources |
| 🔶 `SPARK-ATCH-D06`<br>`updateAttachmentsACLPermissions` | 🟡 Medium `M` | Mutation<br>Calls: `accessControl` | B01 | **Intent —** Change who can view/administer an attachment (a permissions write).<br>**Today —** build bulk {resourceId, dps:[{permissionLevel:ADMIN/READ, grantees:[partnerId]}]} for admin/read id lists → (accessControl) updateAccessControl. Note: this is an ACL…<br>**Done when:**<br>• ADMIN/READ DTOs built correctly per id list |
| 🔶 `SPARK-ATCH-D07`<br>`updateAttachmentTags` + `updateAttachmentTagsV3` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Update the tags on an attachment.<br>**Today —** identical impl — token → updateTagsV3({attachmentId, tags})<br>**Done when:**<br>• updates tags; both fields delegate |
| 🔶 `SPARK-ATCH-D08`<br>`bulkUpdateAttachments` | 🟡 Medium `M` | Mutation<br>Calls: `accessControl` | B01 | **Intent —** Update many attachments at once (tags and/or permissions).<br>**Today —** if tags → bulkUpdateTags; if permissions → (accessControl) bulkUpdateAttachmentPermissions. Latent: fire-and-forget; returns undefined (confirm contract)<br>**Done when:**<br>• tags + permissions applied<br>• returns updated attachments (fix the undefined) |
| 🔶 `SPARK-ATCH-D09`<br>`updateAttributes` | 🟢 Low `XS` | Mutation | B01 | **Intent —** Update a single attachment's metadata attributes.<br>**Today —** token for documentId → updateAttributes<br>**Done when:**<br>• updates attributes |
| 🔶 `SPARK-ATCH-D10`<br>`bulkUpdateAttributes` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Update metadata attributes on many attachments at once.<br>**Today —** token for documentId\\|\\|humanId → bulkUpdateAttributes<br>**Done when:**<br>• bulk-updates attributes |
| 🔶 `SPARK-ATCH-D11`<br>`bulkUpdateAttachmentsV2` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Bulk-update a batch of attachments.<br>**Today —** token for documentId → bulkUpdateAttachmentsV2({attachments})<br>**Done when:**<br>• bulk-updates (tags/packet/perms/related) |
| 🔶 `SPARK-ATCH-D12`<br>`publishAttachmentToGallery` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Publish an attachment to the shared gallery.<br>**Today —** branch on ATC- prefix → V3 (publishAttachmentToGalleryV3) or legacy (publishAttachmentToGallery); api returns void → return true<br>**Done when:**<br>• ATC- → V3, else legacy<br>• returns true on no-error |
| 🔶 `SPARK-ATCH-D13`<br>`unpublishAttachmentToGallery` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Remove an attachment from the shared gallery.<br>**Today —** as D12, unpublish (V3/legacy by ATC-)<br>**Done when:**<br>• ATC- → V3, else legacy |
| 🔶 `SPARK-ATCH-D14`<br>`associateAttachmentTeams` | 🟡 Medium `M` | Mutation | B01 | **Intent —** Share attachments with teams (grant team access).<br>**Today —** build {teamsToUpdateDto, parentId, humanIds:files, relatedResourceIds} → token for files → associateAttachmentTeams<br>**Done when:**<br>• associates teams to files |


### 🔗 Phase F — Federation & Stitching (2 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria |
|---|---|---|---|---|
| 🔸 `SPARK-ATCH-F01`<br>`Attachment` federated entity fetcher | 🟡 Medium `M` | Field Resolver | B01 | **Intent —** Let other subgraphs resolve an Attachment by its key (the federation entry point).<br>**Today —** @DgsEntityFetcher(name="Attachment") resolving by id, so product (attachments<br>**Done when:**<br>• entity resolves by key<br>• `Product { attachments { id } }` smoke test |
| 📄 `SPARK-ATCH-F02`<br>Deferred `getAttachments` drift query decision | 🟢 Low `XS` | Schema | B01 | **Intent —** Decide whether to keep or drop the deprecated `getAttachments` query.<br>**Today —** getAttachments(resourceId, resourceType) is @deprecated("Use v3") with no resolver<br>**Done when:**<br>• decision + traffic survey |


### 🧪 Phase G — Field Resolvers & Tests (3 stories)

| Story | Complexity | Type | Depends On | Acceptance Criteria | Key Tests |
|---|---|---|---|---|---|
| 🔸 `SPARK-ATCH-G01`<br>`Attachment` core field resolvers (snake/camel + access/users/businessPartnersFull) | 🟠 High `L` | Field Resolver<br>Calls: `accessControl`, `vmm`, `userAttributes` | B01 | **Intent —** Resolve the everyday Attachment fields (names, dates, access, author, partners).<br>**Today —** ~18 coalescing fields (snake/camel) + Date parse + id derivation; access (accessControl getPermissionsForResource), businessPartnersFull (vmm), createdBy/updatedBy (user)<br>**Done when:**<br>• coalescing correct (both shapes)<br>• access/users/bps resolve | ☐ snake shape<br>☐ camel shape<br>☐ access<br>☐ users |
| 🔸 `SPARK-ATCH-G02`<br>`tags` + `modelFile` + gallery sub-types | 🟡 Medium `M` | Field Resolver<br>Calls: `tag`, `gallery`, `userAttributes` | B01 | **Intent —** Resolve the tag, 3D-model-file and gallery sub-fields.<br>**Done when:**<br>• each resolves; gallery fileTypes via asset id | — |
| 📄 `SPARK-ATCH-G03`<br>Tests, parity harness | 🟠 High `L` | Tests | B01, D08, G01 | **Intent —** Prove the new attachment subgraph matches the old gateway (tests + parity).<br>**Today —** ≥80% unit coverage; parity harness (incl<br>**Done when:**<br>• unit ≥80%<br>• parity green (both shapes)<br>• schema-diff intentional | ☐ Parity: DGS response matches spark-internal-graphql baseline<br>☐ contract |

