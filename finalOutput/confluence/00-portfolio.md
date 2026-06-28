# Spark → Federated GraphQL Migration — Program Portfolio

> **Audience:** Product Owners, Tech Leads, Architects. **Paste this page into Confluence** (it is the
> program-level rollup). Per-domain PO pages: [product](./product.md) · [bom](./bom.md) ·
> [measurement](./measurement.md) · [impression](./impression.md).
> Effort ranges are **AI-estimated — confirm in refinement**; stories themselves carry complexity only.

## What this program does

We are moving the PLM **GraphQL domains** off the `spark-internal-graphql` gateway into Netflix DGS
subgraphs. Eleven domains are analyzed and broken into engineering stories. Six compile into the **same
`plm-product` subgraph** (cross-references are internal types); **claims**, **search**, **workspace**, and
**sample** are **separate subgraphs** (`spark-claims`, `plm-elastic-search`, `plm-workspace`, `plm-sample`)
that federate with the rest.

## Program totals

| Domain | Target DGS | Stories | Very High | High | Medium | Low | Est. effort (buffered) |
|--------|-----------|---------|-----------|------|--------|-----|------------------------|
| [impression](./impression.md) | plm-product | 11 | 0 | 0 | 2 | 9 | 14–24d |
| [productDetails](./productDetails.md) | plm-product | 17 | 0 | 1 | 9 | 7 | 31–53d |
| [watchlist](./watchlist.md) | plm-product | 17 | 0 | 1 | 8 | 8 | 32–55d |
| [measurement](./measurement.md) | plm-product | 24 | 0 | 1 | 8 | 15 | 40–68d |
| [claims](./claims.md) | claims (separate) | 24 | 0 | 2 | 11 | 11 | 44–75d |
| [search](./search.md) | plm-elastic-search (separate) | 25 | 0 | 7 | 11 | 7 | 73–123d |
| [packaging](./packaging.md) | plm-product | 28 | 0 | 2 | 11 | 15 | 51–87d |
| [workspace](./workspace.md) | plm-workspace (separate) | 32 | 3 | 3 | 15 | 11 | 87–146d |
| [sample](./sample.md) | plm-sample (separate) | 33 | 0 | 7 | 13 | 13 | 81–136d |
| [bom](./bom.md) | plm-product | 42 | 1 | 2 | 15 | 24 | 76–127d |
| [product](./product.md) | plm-product | 72 | 5 | 5 | 22 | 40 | 211–353d |
| **Total** | | **325** | **9** | **31** | **125** | **160** | **740–1247d** |

## Recommended sequencing

1. **Impression** — smallest, lowest-risk; proves the pipeline + DGS scaffolding end-to-end.
2. **ProductDetails** / **Watchlist** — small, co-located; one multi-step write each. Good early wins.
3. **Measurement** — mid-size, one 2-step write; reuses the scaffolding.
4. **Claims** — mid-size, **separate subgraph**; proves cross-subgraph federation back into Product.
5. **Search** — the **read hub**; migrate early (or dual-run) since every domain calls it.
6. **Packaging** — wide schema, one multi-step write + a pricing chain.
7. **Workspace** — large standalone hub; 5-case partner-action dispatcher; provides the `WorkspaceV2` entity.
8. **Sample** — wide entity + prefix-gated polymorphic parents + a union; provides the `SampleV2` entity.
9. **BOM** — material polymorphism (7 types) + one 3-step write; first genuinely complex domain.
10. **Product** — largest and the host DGS; the others' federation contributions land into it.

## Cross-domain blockers (true federation — a separate DGS must migrate first)

| Blocked story | In domain | Waits on (separate DGS) |
|---|---|---|
| `SPARK-MEAS-F02` (SampleV2.sampleMeasurement) | measurement | **sample** |
| `SPARK-PROD-F01` (product/discussion attachments) | product | **attachment** |
| `SPARK-PROD-F02` (discussions) | product | **discussion** |
| `SPARK-PROD-F03` (sample) | product | **sample** |
| `SPARK-PROD-F05` (claims) | product | **claim** |
| `SPARK-PROD-F07` (constructions) | product | **construction** |

BOM's material field resolvers also wait on the **material-hub / trim / wash / fabric / combination** DGSs.
**Internal (NOT blockers — same `plm-product` subgraph):** `SPARK-BOM-F01/F02`, `SPARK-MEAS-F01`,
`SPARK-IMP-F01`, `SPARK-PROD-F04/F06/F08` (F08 watchlist — co-located), `SPARK-PDTL-F01`, `SPARK-PKG-F01`,
`SPARK-WL-F01/F02`.

**Separate subgraphs (federate, not blockers per se):** `claims` (`spark-claims`), `workspace`
(`plm-workspace` — provides the `WorkspaceV2` entity every product-family domain references), `search`
(`plm-elastic-search` — the **read hub** every domain calls; sequence its cutover first or dual-run), and
`sample` (`plm-sample` — provides the `SampleV2` entity; **unblocks `SPARK-MEAS-F02` + `SPARK-PROD-F03`** above).

## Highest-risk items (Very High)

| Item | Domain | Why |
|---|---|---|
| TechPack `getProductTechPackCountV1`/Bulk (`E03/E04`) | product | 17-step aggregation → composite-key federation |
| `productBusinessPartnerActions` (`E01`) | product | drop/undrop across 4+ cleanup services, no rollback |
| `attachmentsWithMetaData` / `components` (`G01/G02`) | product | large, perf-sensitive, N+1 ACL |
| `workspaceBusinessPartnerActionsV2` (`E01`) + `attachmentsWithMetaData`/`counts` (`G01/G02`) | workspace | 5-case drop/undrop dispatcher (un-awaited chains) + 2 heavy field resolvers |
| Prefix-gated polymorphic parents + `SampleAsset` union (`G02`/`A04`); evaluation writes (`E01/E02`) | sample | wide entity hydration + bulk-evaluate orchestration |
| `updateBom` (`E01`) | bom | 3-step non-atomic write |

## Program-wide decisions (PO / Architecture)

| Decision | Domains | Owner |
|---|---|---|
| Non-atomic write failure strategy (saga / compensation / best-effort) | bom, measurement, product, packaging, productDetails, claims, watchlist, workspace, sample | Tech Lead + PO |
| `update*ComponentStatus*` has no auth token — backend-enforced? | bom, measurement, product, packaging, productDetails | PO |
| Federation rollout order for sibling subgraphs | all | Architect + Platform |
| Search (read hub) cutover ordering — migrate early or dual-run | all (search) | Tech Lead + Platform |
| TechPack facade approach (Node vs Kotlin) | product | Architect |
| `Product.division` latent-bug fix cutover flag | product | PO |

## How to consume

- **Jira:** create the 11 epics + 325 stories from [`../jira/all-stories.csv`](../jira/all-stories.csv)
  (see [`../jira/README.md`](../jira/README.md)).
- **Confluence:** this page + each per-domain page.
- **Implementation:** engineers work from `../<domain>/04-stories.md` + `../<domain>/02-resolver-analysis.md`.

---
*Source of truth: `../../code` (schema SDL + resolver + service + utils). Generated from the per-domain
analysis in `finalOutput/`.*
