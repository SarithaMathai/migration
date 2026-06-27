# Impression — Federation Schema Analysis

> **Domain:** `impression` · **Pipeline Version:** 1.1 · **Generated:** 2026-05-18

---

## 1. Naming Decisions

| Source | Target | Rationale |
|---|---|---|
| `SPARK_Impression` | `Impression` | Drop prefix |
| `SPARK_ImpressionCount` | `ImpressionCount` (deprecated) + new `ImpressionCountResult` | **Restructure** — see §3 |
| `SPARK_CountsByBp` | `CountsByBp` | `@shareable` (legacy compat) |
| `SPARK_ProductImpressionInput` / `SPARK_ImpressionInput` | unprefixed | |
| `SPARK_WorkspaceV2` | `WorkspaceV2` | External stub |
| `SPARK_UserProfileAttributes` | `UserProfileAttributes` | External stub |

---

## 2. Gap Analysis

| Surface | Source | Status |
|---|---|---|
| Q1 `searchImpressionsByProductId` | 4 args | 🔜 + 🔧 (honor `enableWorkspaceContextFiltering`) |
| Q2 `getImpressionCountsByProductId` | returns count wrapper | 🔜 + 🔧 (restructure shape) |
| M1 `updateImpressions` | bulk delete+update | 🔜 |
| Types | Impression, ImpressionCount | 🔜 (+ new `ImpressionCountResult`) |
| Inputs | 2 | 🔜 |
| Field resolvers | 5 on Impression + 1 on count | 🔜 |

---

## 3. `ImpressionCount` Restructure

**Source contract** (per [02-resolver-analysis.md Q2](output/impression/02-resolver-analysis.md)):
- Query declared to return `SPARK_ImpressionCount` (object with single `counts: [SPARK_CountsByBp]` field)
- Resolver returns `[SPARK_Impression]` (an array) — relies on `SPARK_ImpressionCount.counts` field resolver receiving the array as parent
- `counts` resolver bucketizes per partner and appends `{bpType: 'totalCount', counts: N}` sentinel row

**Target contract:**
```graphql
type ImpressionCountResult {
  productId: ID!
  totalCount: Int!
  countsByPartner: [PartnerImpressionCount!]!
}
type PartnerImpressionCount { partnerId: ID!, count: Int! }
```
- Total surfaced as a typed field (no string `'totalCount'` sentinel)
- Per-partner counts have proper `ID` partner key
- `ImpressionCount` (old shape) kept `@deprecated` for one release for client migration

PO decision required (#3 below).

---

## 4. Federation Contribution

Per [federation-patterns.md §9](fedMigrationScripts/reference/federation-patterns.md), Impression should also contribute to the `Product` entity:

```graphql
extend type Product @key(fields: "id") {
  id: ID! @external
  impressions(partnerIds: [ID], workspaceIds: [ID]): [Impression]
  impressionCounts: ImpressionCountResult
}
```

These two fields are currently exposed as top-level queries `searchImpressionsByProductId` / `getImpressionCountsByProductId` rather than as resolvers on a `Product` shape. **Recommendation:** publish both surfaces in DGS — top-level queries (back-compat) + Product entity-extension (federation-native). Top-level queries can be `@deprecated` after gateway clients migrate.

---

## 5. Domain-Sizing / Co-location

Total source: **169 LOC**, 2 queries + 1 mutation + 2 types. Below the threshold where a dedicated DGS subgraph is justified.

**Options:**
- **A: Stand-alone `plm-impression` DGS** — Pure separation, but operational overhead for a 169-LOC domain is high.
- **B: Co-locate in `plm-product`** ⭐ recommended — Impressions are conceptually a sub-resource of Product (endpoint path `/impressions/product/{productId}` makes this explicit). Same Kotlin module, same DataLoader registry. Schema can still expose `Impression @key("id")` for cross-subgraph references.
- **C: Co-locate in `plm-bom`** — Impressions are referenced from bom impression details, but the data ownership is at product level (`parentId` references a product, not a bom).

PO decision required (#2 below).

---

## 6. Risks

| # | Risk | Severity |
|---|---|---|
| 1 | `enableWorkspaceContextFiltering` silently dropped — backend may have separate behavior expected | 🔴 |
| 2 | `SPARK_ImpressionCount` shape mismatch (array passed as object parent) — client-visible restructure | 🔴 |
| 3 | `counts` resolver TypeError on empty `impressions[0]` — masked by try/catch | 🟡 |
| 4 | `bpType: 'totalCount'` string-vs-ID type mixing | 🟡 |
| 5 | Silent error → dummy `[{totalCount, 0}]` — observability gap | 🟡 |
| 6 | Decision: stand-alone DGS vs co-locate in plm-product | 🟡 |
| 7 | Cross-resolver call into `SPARK_WorkspaceV2` | 🟢 |

---

## 7. Open Questions

1. **Co-location decision** — separate DGS or fold into `plm-product`?
2. **`ImpressionCountResult` schema restructure** — proceed with deprecation cycle?
3. **`enableWorkspaceContextFiltering`** — wire to backend or remove from schema after client survey?
4. **Top-level queries vs Product entity-extension** — keep both or migrate to entity-only?

---

**Phase Completed:** Phase 3 — Federation Schema Derivation
**Outputs:** [03-schema.graphql](output/impression/03-schema.graphql), [03-schema-analysis.md](output/impression/03-schema-analysis.md)
