# Phase 3: Federation Schema Analysis — Sample

> **Domain:** `sample` · **Target DGS:** separate `plm-sample` subgraph
> **Pipeline Version:** 2.0 · **Generated:** 2026-06-27
> **Schema:** [03-schema.graphql](./03-schema.graphql) · **Depends on:** [02-resolver-analysis.md](./02-resolver-analysis.md)
> **DGS Target Status:** Green-field · Gap: **0 ✅ | 32 🔜 | 3 ⏭ — 35 operations**

- The target schema is translated from the source SDL (`schemas/SPARK_SampleV2.graphqls`), verified against the resolver.
- **Sample is its own subgraph** (`plm-sample`) — every reference is cross-subgraph.

## 1. Type Classification
| Bucket | Count | Examples |
|---|---|---|
| Owned entities (`@key`) | 1 | `SampleV2` (key `id`) |
| Owned value types | ~24 | rounds/aesthetics/colors/library-color, participants, department, rfid, formats, exports |
| Union (`@DgsTypeResolver`) | 1 | `SampleAsset` (`Color` \| `Artwork`) |
| `@shareable` | 3 | `CodeDescription`, `SampleCodeDescriptionV2`, `Participants` |
| External stub — platform | 4 | `VMM_BusinessPartner`, `VMM_Brand`, `IG_Department`, `Tag` |
| External stub — other DGS | ~12 | `Product`, `WorkspaceV2`, `SampleMeasurementSet`, `Attachment`, `Trim`, `ColorArchroma`, `Color`, `Artwork`, `FabricSpecCombo`, `FabricSpecification`, `Material`, `Role`, `Spark_AsapEvaluation` |
| Inputs | ~10 | `CreateSamplesInputV2`, `UpdateSamplesInputV2`, `Sample_RoundV2`, `BulkSampleRound`, `SampleUpdateSampleEvaluationInput`, … |

## 2. Polymorphism — `SampleAsset` union (`@DgsTypeResolver`)
- 2 members: `Color` (when `isColorId(humanId)`), `Artwork` (Artworks prefix); else null.
- **+1 complexity tier.** The `SampleV2.asset` field is the union; many `parent*` fields are concrete (product/trim/colorArchroma/…) resolved by prefix.

## 3. Client Contract Verification
- 23 queries + 9 mutations preserved (`0 ✅ | 32 🔜`); **3 schema-drift mutations deferred ⏭** (`updateSampleEvaluations`, `dropSamples`, `undropSamples` — no top-level resolver; drop/undrop run inside `workspaceBusinessPartnerActionsV2`).
- `SPARK_`/`V2` naming preserved (client contract); `VMM_`/`IG_` kept.
**Entity key:** `SampleV2.id`.

## 4. Federation Boundaries

> **Separate subgraph:** `sample` is its own DGS. Conversely, **`SampleV2` is referenced as an entity** by
> product (`Product.samples`, `sampleIds`), measurement (`SampleV2.sampleMeasurement` — `SPARK-MEAS-F02`),
> and workspace (drop/undrop + `sampleReport`).

- **Owns** `SampleV2` + ~24 value types + the `SampleAsset` union.
- **External (federation):** `product`, `workspace`, `measurement` (sample-measurement set), `search`
  (attachments + rfid), `relationship`, `attachment`, `notification`, `user-profile`/`role`/`user-group`,
  `trim`/`color`/`colorArchroma`/`combination`/`fabric`/`artwork`/`material`/`tgtColorEvaluator`;
  **gateway stitch:** `VMM`, `Brand`, `IG`, `Tag`, `recentlyViewed`.
- **Provides** `SampleV2` for the product-family + measurement subgraphs.

## 5. Migration Approach  *(Confluence approach page)*

Sample is a **large, mid-high-risk** standalone subgraph — a wide entity with prefix-gated polymorphic parent
hydration, a union, two evaluation writes, and a long master-data tail.

1. **Phase A:** schema (~25 types + the `SampleAsset` `@DgsTypeResolver` + ~10 inputs) + `SampleServiceV2`
   port (`samples/v2`). Preserve the `systemGenerated`/`systemUser` branch and the batched `getSamplesByIdsV2`
   + recentlyViewed side-effect.
2. **Phase B:** by-id/parent reads + the ~13 **cacheable master-data** queries (one bundled story).
3. **Phase C:** the RFID location reads (🔴 search).
4. **Phase D:** the simpler writes — create (+file relationship), round, workspace-assoc, exports, notification
   retries, bulk-clone.
5. **Phase E:** `updateSamplesV2` and `bulkEvaluateSamples` (the evaluation orchestration).
6. **Phase F:** expose `SampleV2` as a federated entity for product/measurement/workspace; decide the 3
   deferred drift mutations.
7. **Phase G:** the wide `SampleV2` field resolvers (users, prefix-gated parents/union, partners, workspace/
   measurement/tag, attachments/rfid, participants + sub-types) + the test/parity harness.

## 6. Risks & Recommendations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Wide entity + prefix-gated parent hydration (G02) | Medium | High | DataLoader batch; centralize the prefix→loader table | Backend Eng |
| `SampleAsset` union correctness (A04) | Medium | Medium | `@DgsTypeResolver` + per-member tests | Backend Eng |
| `bulkEvaluateSamples` / `updateSamplesV2` orchestration (E01/E02) | Medium | High | Port `bulkEvaluateSampleUtil` carefully; failure strategy | Tech Lead |
| `createSamplesV2` file-relationship side-effect (no rollback) (D01) | Low | Medium | Compensation/best-effort decision | Tech Lead |
| Schema-drift drop/undrop owned by workspace dispatcher | Medium | Low | Coordinate ownership with workspace (F) | Product Owner |
| RFID `searchLatestRfidLocations` perf (C01/G) | Low | Medium | Batch tag queries; cache latest-location reduce | Backend Eng |

## 7. ACL Handling
Reads/writes curry capability tokens; drop/undrop bookkeeping lives in the workspace dispatcher. **ACL is
ignored in the DGS implementation** (no ACL story) — context only.

## 8. Open Questions
1. `SampleAsset` — confirm the union members + prefix rules (any beyond Color/Artwork)?
2. Delete or `@deprecated` the 3 drift mutations; where do drop/undrop live (sample vs workspace)?
3. `createSamplesV2` file-relationship failure strategy?

---
**Phase Completed:** Phase 3 · **Domain:** `sample`.
