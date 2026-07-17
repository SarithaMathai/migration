# 03 · Proposed Federated Schema Changes + Diff Report

> Phase 3 of the federation review · 2026-07-17
> Changes are classified **REQUIRED** (composition breaks without them — applied to the `be-03-schema.graphql` files in this change), **RECOMMENDED** (additive, PO-gated — *not* applied, staged as stories), and **OPTIONAL** (documented only).
> Guiding principles: minimize schema change; never remove a primitive id a client selects today; additive object fields only.

## 1. REQUIRED — cross-subgraph contract fixes (applied)

### R1 · `VMM_BusinessPartner` key: `bpId` → `id`

- **Affected domain:** product (all other 7 domains + the source SDL already use `id`).
- **Evidence:** `code/schemas/core.txt:57` — `type VMM_BusinessPartner { id: ID … }`; no `bpId` field exists. PRODUCT-BE-F-11's own example resolves a "bare `VMM_BusinessPartner{id}`".
- **Impact:** High — with two different `@key` field sets on the same platform entity, Hive composition fails (or produces an unresolvable entity).

```graphql
# current (product/be-03-schema.graphql)
type VMM_BusinessPartner @key(fields: "bpId") @extends { bpId: ID! @external }
# proposed
type VMM_BusinessPartner @key(fields: "id") @extends { id: ID! @external }
```

### R2 · `VMM_Brand` key: `brandId` → `id`

- Same rationale as R1: `code/schemas/core.txt:135` — `VMM_Brand { name, id: ID, … }`; no `brandId` field. Product is the only referencing domain.
- **Impact:** Medium (single referencing subgraph, but same composition failure at the gateway).

### R3 · Claims entity: type name `Claims`, key = synthesized `id`

- **Affected domains:** product ↔ claims (a *real* cross-subgraph pair — claims is its own `spark-claims` DGS).
- **Problem:** product stubbed a type named `Claim` keyed on `id`; the owning subgraph's type is `Claims`, and the SDL exposes no `id` at all. As originally written, `Claim` had no owning subgraph and `Product.claims: [Claim]` could never resolve.
- **✅ DECIDED (2026-07-17):** all entities federate on **`id`**. Owners whose SDL lacks an id — `Claims`, `Packaging`, `Watchlist`, `Dieline` — **synthesize `id` from `humanId`** (the established `Measurement.id` pattern), wrapping the entity so gateway stitching is uniform on `id`. `humanId` stays on each type for the client contract.
- **Client contract:** the current SDL type is `SPARK_Claims` → federated name `Claims` (prefix-drop convention). Fragments/`__typename` checks must target `Claims` (see [06 §3](./06-frontend-impact.md)).

```graphql
# current (product/be-03-schema.graphql)
type Claim @key(fields: "id") @extends { id: ID! @external }
…  claims(partnerIds: [String], includeClaims: Boolean): [Claim]
# decided
type Claims @key(fields: "id") @extends { id: ID! @external }   # owner synthesizes id from humanId
…  claims(partnerIds: [String], includeClaims: Boolean): [Claims]

# owner side (claims/be-03-schema.graphql)
type Claims @key(fields: "id") {
  id: ID!            # synthesized from humanId (Measurement pattern)
  humanId: String    # kept for the client contract
  …
}
```

### R4 · Packaging / Watchlist / Dieline keys + ProductDetails naming

- Per the same decision: `Packaging`, `Watchlist` and `Dieline` gain a synthesized `id: ID!` (from `humanId`) and key on `id`; product's stubs stay keyed `id`.
- Product stubs `ProductDetail` — owner type is `ProductDetails` (key `id` ✓). → rename stub to `ProductDetails`.
- Product references `MeasurementsPaged` — measurement declares `MeasurementPaged`. → align to `MeasurementPaged`.
- **Impact:** Medium — packaging/watchlist are co-located in `plm-product` (merged-schema build-stopper); the id-synthesis itself is one mapper line per entity in the Phase A/B skeleton stories.

### R5 · Claims subgraph: entity stubs that must be `@shareable` value types

- **Problem:** claims declares `ProductComponentStatus`, `ResourcePermissions`, and `TeamPaged` as `@extends @key(fields:"id")` entity stubs. But:
  - claims resolves these fields **locally with full data** (statuses from the claim record; `systemTeams` from its own elastic call) — an `@external` stub cannot carry resolved fields;
  - the owners model them as **value types**: product's `ResourcePermissions` is `@shareable` with no key; `ProductComponentStatus` has no key *and no `id` field*; `TeamPaged` is a paged wrapper (`content`+`paging`) with no identity.
- **Fix (applied to claims/be-03-schema.graphql):** declare all three as `@shareable` value types with the owner's field shape (+ `TeamV2` entity stub keyed `teamId` inside `TeamPaged.content`, matching product's stub); mark product's `ProductComponentStatus` `@shareable` so the duplicate definitions compose.
- **Impact:** High for claims (its `statuses`/`currentUserPermissions`/`systemTeams` fields simply cannot ship as modelled); nil for clients (same shapes on the wire).

### R6 · `CORONA_ItemDetails` key — ✅ DECIDED (2026-07-17)

- Product stubs `CORONA_ItemDetails @key(fields:"tcinId")`; the SDL type (`code/schemas/SPARK_Product.txt:336`) has no key field — it is an embedded projection resolved from `Tcin.tcinId`.
- **Decision (OQ-2):** it **stays an entity keyed `tcinId`** — where a tcin exists, the record carries `tcinId`, and **Corona inflates the item details from that key via the gateway** (the same wrap-with-key pattern as the humanId-only entities). Implemented in PRODUCT-BE-F-14.

## 2. RECOMMENDED — additive entity references (PO-gated, staged as stories, NOT yet in the schemas)

For each: id/name fields stay (backward compatible); the object field is additive; impact = clients *may* simplify second fetches, nothing breaks.

| # | Change | Rationale | Affected domain(s) | Impact | Story |
|---|--------|-----------|--------------------|--------|-------|
| REC-1 | `BomMaterialInterface.supplier: VMM_BusinessPartner` (+ 7 impls) | today's `supplierId`+`supplierName` force clients to re-query VMM for any further partner data; BOM rows are the heaviest partner consumers (18 client selections) | bom → business-partner | Medium (schema-conformance across 7 impls) | BOM-BE-G-17 |
| REC-2 | `Impression.attachment: Attachment` | client selects `attachmentId` (`product-queries__ProductQueries.txt:309`) then resolves the file via the attachment API separately; emitting a `@key` stub costs one field | impression → attachment | Low | IMPRESSION-BE-G-04 |
| REC-3 | `WatchlistPartner.partner: VMM_BusinessPartner` | `partnerName` is *already* a live VMM `getByID(partnerId).bpName` lookup (WATCHLIST-BE-G-02) — same call, full entity instead of one field | watchlist → business-partner | Low | WATCHLIST-BE-G-05 |
| REC-4 | `SampleMeasurementSet.sample: SampleV2` | forward ref pairs with the existing reverse extension (`SampleV2.sampleMeasurement`, MST-BE-F-04); zero extra backend calls (emit `{id: sampleId}`) | measurement → sample | Low | MST-BE-G-04 |
| REC-5 | `ProductVendorAttributes.partner` + `WorkspaceInfoPartner.partner: VMM_BusinessPartner` | removes the client-side join of per-partner rows against the `businessPartners` list | product → business-partner | Medium | PRODUCT-BE-G-17 |
| REC-6 | Mark `Product.parentProductId`-adjacent projections (`AncestryProducts`, `ChildProducts`) with optional `product: Product` | one-hop lineage detail without a second `getProductsByIds` | product (self) | Low | PRODUCT-BE-G-17 |

## 3. OPTIONAL / DEFERRED (documented only — revisit at phase-2 kickoff)

- `Bom.selectedProductImpressions: [Impression]`, `Impression.associatedBoms: [Bom]` — internal co-located resolvers; wait for a UI need.
- Attachment-list object fields (`Bom*Material.attachments`, `PackagingInternalData.attachments`, `Product.thumbnail`) — blocked on the phase-2 attachment subgraph; ids are the working contract today.
- Workspace refs on per-workspace value rows (`ProductWorkspaceAttributes.workspace`, …) — blocked on the phase-2 workspace subgraph.
- `ProductDetailsItem.template` — blocked on spec-template types joining the merged schema.
- `facility`/`laundry`/`printer` → `VMM_Location` refs — needs the VMM location stub *and* the snapshot-semantics answer (OQ-3).
- `relatedResources: [ID]` polymorphic lists (impression, productDetails, watchlist inputs) — would need a resource union; no consumer asks for it (OQ-4).

## 4. Diff summary (applied in this change)

| File | Change |
|---|---|
| `product/be-03-schema.graphql` | R1 `VMM_BusinessPartner` key → `id` · R2 `VMM_Brand` key → `id` · R3 `Claim`→`Claims` stub (key `id`) + `Product.claims` return type · R4 `ProductDetail`→`ProductDetails`, `MeasurementsPaged`→`MeasurementPaged` · `ProductComponentStatus` marked `@shareable` (R5) · R6 comment on `CORONA_ItemDetails` |
| `claims/be-03-schema.graphql` | R3: `Claims.id` synthesized from humanId, `@key(fields:"id")` · R5: `ProductComponentStatus`/`ResourcePermissions`(+`PermissionEntry`)/`TeamPaged`(+`Team` stub, `Paging`) re-declared as `@shareable` value types / proper stubs |
| `packaging/be-03-schema.graphql` | R4: `Packaging.id` + `Dieline.id` synthesized from humanId, keys → `id` |
| `watchlist/be-03-schema.graphql` | R4: `Watchlist.id` synthesized from humanId, key → `id` |
| `measurement/be-03-schema.graphql` | Key note updated: synthesized-id wrap is now the program-wide standard (OQ-1 resolved) |
| bom, impression, productDetails schemas | **no changes** — verified consistent |

Everything in §2–3 ships only as stories awaiting PO approval; the generated Jira CSVs mark them `Recommended (PO-gated)`.
