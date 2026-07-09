# Phase 3: Federation Schema Analysis — Packaging

> **Domain:** `packaging` · **Target DGS:** `PackagingService` → `plm-product`
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 17 🔜 | 0 ⏭ — 17 operations**

The target schema is translated from the source SDL (`schemas/SPARK_Packaging.graphqls`), verified against
the resolver. Wide SDL (~24 object types, ~20 inputs), but **no polymorphism**.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 2 | `Packaging` (key `humanId`), `Dieline` (key `humanId`) |
| Owned value types | ~20 | `PrinterDieline`, `PackagingElement`, `PrintingProcess`, `WarningsAndCautions`, `ContactInformation`, `SuggestedRetailPriceByDPCI`, `PackagingFieldValues`, … |
| `@shareable` | 3 | `CodeDescription`, `Paging`, `Pageable` |
| External stub — platform | 1 | `VMM_BusinessPartner` |
| External stub — sibling DGS | 6 | `Attachment`, `SearchAttachment`, `WorkspaceV2`, `UserProfileAttributes`, `UserGroup_Participants`, `AccessControl` |
| Internal (same subgraph) | 3 | `Product`, `ProductComponentStatus`, `SpgFileLibrary` (fileLibrary) |
| Inputs | ~20 | `PackagingInput`, `PackagingBulkInput`, `PrinterDielineInput`, `DielineEvaluationInput`, … |

No interfaces / unions — no `@DgsTypeResolver` needed.

## 2. Client Contract Verification
7 queries + 10 mutations preserved (`0 ✅ | 17 🔜 | 0 ⏭`). `SPARK_` prefixes dropped; `VMM_` kept.
**Entity keys:** `Packaging` and `Dieline` are keyed on **`humanId`** (the SDL exposes no `id`). Several
- `@deprecated` fields/inputs (`retailPrice`, `creativePath`, `resourceType`, `fileDeliveryEmail`, `Dieline.attachments`) are carried across with the directive.
- **Claims pass-through:** `PackagingInput` carries `claimId`/`claimDetails` — confirm whether this stays here or moves with the claims subgraph.

## 3. Federation Boundaries

> **Monorepo:** `packaging` is the **same `plm-product` subgraph** as product/bom/measurement/productDetails.
> References among them are **internal types**, not federation. See
> [reference-federation-patterns.md §0](../../../fedMigrationScripts/reference/reference-federation-patterns.md).

- **Owns** `Packaging`, `Dieline` + ~20 value types.
- **Internal (same subgraph — NOT federation):** `Product` (`product` field), `fileLibrary`
  (`PackagingElement.packagingLibrary`), `ProductComponentStatus`, `packaging` (own dieline lookups).
- **External (true federation stubs):** `attachment` (clone/archive/getV3 + bulk attributes),
  `search` (elastic packaging/workspaces/attachments), `workspace`, `user-profile`
  (`createdBy`/`updatedBy`/evaluators/participants), `relationship` (attachment add/remove on update),
  `tag` (`waveDescription`), `access-control`; **gateway stitch:** `VMM`, **apex/pricing** (suggested price).
- **Contributes back** to `Product` → **internal** field resolvers (co-located, Phase F).

## 4. Migration Approach  *(Confluence approach page)*

Packaging is a **mid-size, mid risk** domain — wide schema, no polymorphism, one multi-step write and one
multi-hop pricing field.

1. **Phase A:** schema (~24 types, ~20 inputs) + `PackagingService` port. Preserve the create/bulk
   throw-on-error contracts and the `{content}` status wrap; carry `@deprecated` directives.
2. **Phase B:** the 6 simple reads (incl. 2 cacheable: dieline-evaluation-statuses, countries).
3. **Phase C:** `getPackagingElastic` (🔴 search).
4. **Phase D:** simple mutations — add, evaluate-dieline, bulk add/update, export, lock/unlock,
   clone-files (🔴 attachment), component-status.
5. **Phase E:** `updatePackaging` — the **multi-step** write (body → attachment remove [archive +
   relationship] → attachment add [relationship + attribute update]). Choose a failure strategy; note the
   add branch rejects on `relationship.status>=400` while the remove branch does not.
6. **Phase F:** `Product` packaging links — **internal** field resolvers (co-located), not gateway federation.
7. **Phase G:** field resolvers — ACL/partner/participants, users/evaluators, product/workspaces/attachments,
   the **`suggestedRetailPriceByDPCI`** pricing chain + `waveDescription` (tag), the `Dieline`/`PrinterDieline`/
   `PackagingElement` resolvers — + the test/parity harness.

## 5. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `updatePackaging` multi-step partial failure (E01) | Medium | High | Saga / compensation; align add/remove error handling | Tech Lead + PO |
| `suggestedRetailPriceByDPCI` multi-hop (dielines→dpcis→pricing) (G04) | Medium | Medium | Cache/batch; guard on `requiresSuggestedRetailPrice` | Backend Eng |
| `updatePackagingComponentStatus` has no auth token (D09) | Low | Medium | Confirm backend enforces; document | PO |
| Attachment-by-search field resolvers (perf) | Low | Medium | Shared search helper; batch | Backend Eng |
| Claims pass-through fields on `PackagingInput` | Low | Low | Confirm ownership (packaging vs claims subgraph) | Product Owner |

## 6. ACL Handling
Reads/writes curry capability tokens via `getUserPermissionsJWT` (resource-scoped). **ACL is ignored in the
DGS implementation** (no ACL story) — context only.

## 7. Open Questions
1. `updatePackaging` failure strategy (and align add/remove error handling)?
2. `updatePackagingComponentStatus` — backend-enforced without a token?
3. `suggestedRetailPriceByDPCI` — cache the dieline→dpci→pricing chain?
4. Claims pass-through (`claimId`/`claimDetails`) — keep on packaging or route to claims?

---
**Phase Completed:** Phase 3 · **Domain:** `packaging`.
