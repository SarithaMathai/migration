# Program Story Inventory — All Domains

> **Pipeline Version:** 2.0 · **Generated:** 2026-06-26
> Program-level rollup of every migration story across the thirteen analyzed domains. Feed this (or
> [index.yaml](./index.yaml)) to a Jira MCP to create the thirteen epics + link stories, or to Confluence for a
> portfolio page. Per-domain detail: each domain's `04-stories.md` + `04-stories-index.yaml`.

## 1. Program totals

| Domain | Target DGS | Stories | Very High | High | Medium | Low | Est. effort (buffered) |
|--------|-----------|---------|-----------|------|--------|-----|------------------------|
| [impression](./impression/04-stories.md) | plm-product | 11 | 0 | 0 | 2 | 9 | 14–24d |
| [productDetails](./productDetails/04-stories.md) | plm-product | 17 | 0 | 1 | 9 | 7 | 31–53d |
| [watchlist](./watchlist/04-stories.md) | plm-product | 17 | 0 | 1 | 8 | 8 | 32–55d |
| [measurement](./measurement/04-stories.md) | plm-product | 24 | 0 | 1 | 8 | 15 | 40–68d |
| [claims](./claims/04-stories.md) | claims (separate) | 24 | 0 | 2 | 11 | 11 | 44–75d |
| [search](./search/04-stories.md) | plm-elastic-search (separate) | 25 | 0 | 7 | 11 | 7 | 73–123d |
| [packaging](./packaging/04-stories.md) | plm-product | 28 | 0 | 2 | 11 | 15 | 51–87d |
| [attachment](./attachment/04-stories.md) | plm-attachment (separate) | 28 | 0 | 3 | 15 | 10 | 51–86d |
| [workspace](./workspace/04-stories.md) | plm-workspace (separate) | 32 | 3 | 3 | 15 | 11 | 87–146d |
| [sample](./sample/04-stories.md) | plm-sample (separate) | 33 | 0 | 7 | 13 | 13 | 81–136d |
| [discussion](./discussion/04-stories.md) | plm-discussion (separate) | 37 | 0 | 6 | 17 | 14 | 70–118d |
| [bom](./bom/04-stories.md) | plm-product | 42 | 1 | 2 | 15 | 24 | 76–127d |
| [product](./product/04-stories.md) | plm-product | 72 | 5 | 5 | 22 | 40 | 211–353d |
| **Total** | | **390** | **9** | **40** | **157** | **184** | **861–1451d** |

> Effort is AI-estimated (confirm in refinement). Seven domains target the same **`plm-product`** DGS (shared
> Feign base URLs + some federation stories); **claims, search, workspace, sample, attachment** and
> **discussion** are separate subgraphs that federate back into Product.

## 2. Recommended program sequencing

1. **Impression first** — smallest, lowest-risk; proves the pipeline + DGS scaffolding end-to-end.
2. **Measurement** — mid-size, one 2-step write; reuses the scaffolding.
3. **BOM** — polymorphism (7 material types) + one 3-step write; the first genuinely complex domain.
4. **Product** — largest and the host DGS; the others' federation contributions land into it.
   Product's TechPack federation (Phase F) is **unblocked incrementally** as each sibling migrates.

> **Monorepo:** `product`, `bom`, `measurement`, `impression` (and the rest of the product family) are the
> **same `plm-product` subgraph**. Their references to each other are **internal types**, so the Phase-F
> "contributions to Product / ResourcesCount" among them (`bom F01/F02`, `measurement F01`, `impression F01`,
> `product F04/F06`) are **internal field resolvers (CAT-2), not gateway federation** — they only depend on the
> `Product`/`ResourcesCount` types existing in the merged schema (ordering), and **block nothing across services**.

## 3. Cross-domain blockers (TRUE federation only — separate DGS subgraphs)

These are the only genuinely cross-service blockers (a separate DGS must migrate first):

| Blocked story | In domain | Waits on (separate DGS) |
|---|---|---|
| `SPARK-MEAS-F02` (SampleV2.sampleMeasurement) | measurement | **sample** DGS |
| `SPARK-PROD-F01` (productAttachments, discussionAttachments) | product | **attachment** DGS |
| `SPARK-PROD-F02` (discussions) | product | **discussion** DGS |
| `SPARK-PROD-F03` (sample) | product | **sample** DGS |
| `SPARK-PROD-F05` (claims) | product | **claim** DGS |
| `SPARK-PROD-F07` (constructions) | product | **construction** DGS |

Also true (not co-located) federation **within** a domain's own stories: BOM's material field resolvers wait on
the **material-hub / trim / wash / fabric / combination** DGSs being stubbed in the gateway.

**Internal (NOT blockers — same `plm-product` subgraph):** `SPARK-BOM-F01`, `SPARK-BOM-F02`,
`SPARK-MEAS-F01`, `SPARK-IMP-F01`, `SPARK-PROD-F04` (measurement), `SPARK-PROD-F06` (bom),
`SPARK-PROD-F08` (watchlist — co-located; **corrected** from a prior separate-DGS mislabel),
`SPARK-PDTL-F01` (productDetails), `SPARK-PKG-F01` (packaging).

## 4. Highest-risk stories across the program (Very High)

| Story | Domain | Why |
|---|---|---|
| `SPARK-PROD-E03` / `E04` | product | TechPack 17-step aggregation → composite-key federation (Option D) |
| `SPARK-PROD-E01` | product | partner drop/undrop orchestration across 4+ cleanup services, no rollback |
| `SPARK-PROD-G01` / `G02` | product | `attachmentsWithMetaData` / `components` — large, perf-sensitive, N+1 ACL |
| `SPARK-BOM-E01` | bom | `updateBom` 3-step non-atomic write |

## 5. Program-wide decisions (roll-up of PO decisions)

| Decision | Domains | Owner |
|---|---|---|
| Non-atomic write failure strategy (saga / compensation / best-effort) | bom (E01), measurement (E01), product (E01) | Tech Lead + PO |
| `updateComponentStatus*` has no auth token — backend-enforced? | bom (D05), measurement (D05), product (E02) | PO |
| Federation rollout order for sibling subgraphs | all | Architect + Platform |
| TechPack facade approach (Node vs Kotlin) | product (E03) | Architect |
| `Product.division` bug fix cutover flag | product (G12) | PO |
| Feature-flag / drift-wrapper cleanups | product (B10/B11/C05/F12) | PO |

## 6. How to consume this

- **Jira MCP:** read [index.yaml](./index.yaml) → create 13 epics (one per domain) → create a Story per entry
  (map `complexity`→points, `depends_on`→"is blocked by" links, `labels`, `blocked_by`→a blocking note).
- **Confluence MCP:** render this file as the portfolio page; render each domain's `05-attribute-inventory.md`
  + `03-schema-analysis.md §Migration Approach` + `04-po-summary.md` as the per-domain space pages.
- See [scripts/06-feeding-mcp-tools.md](./scripts/06-feeding-mcp-tools.md) for the field-by-field mapping.

---
*Pipeline 2.0 — 13 domains, 390 stories. Source of truth: `../code` (schema SDL + resolver + service + utils).*
