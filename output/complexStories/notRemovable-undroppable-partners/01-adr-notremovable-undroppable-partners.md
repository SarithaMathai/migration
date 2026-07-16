# ADR-016 (draft) — `notRemovablePartnerIds` / `unDroppablePartners` reads (`SPIKE-04`)

> **Status:** 🔴 Proposed — draft for review
> **Spike:** `SPIKE-04` · **Home stubs:** `PRODUCT-BE-G-11-1` (notRemovable) · `PRODUCT-BE-G-07`
> (unDroppable) · `WORKSPACE-BE-G-05` (later phase, workspace twins)
> **Scope:** the two **read** aggregations that answer "which partners can the user *not* remove / *not*
> drop, because a child still references them". The drop/undrop **writes** are ADR-012 (`SPIKE-03`),
> not decided here.
> **Related:** ADR-014 (owner-computed rollups) · ADR-015 (facade-then-federate — same lane decomposition) ·
> ADR-018 (`attachmentsWithMetaData` — a direct dependency of the workspace twin) ·
> the `removablePartner/` spike clone validated the owner-`@requires` lane aggregation E2E.
> **Evidence:** `utils/removePartnerUtils.js` + `utils/commonLoaders.js` + `resolvers/SPARK_Product.js` +
> `resolvers/SPARK_WorkspaceV2.js` at `https://github.com/XXX`.

---

## 1. Today's behavior, field by field

### `Product.notRemovablePartnerIds` — `getProductPartnersNotRemovable` (`utils/removePartnerUtils.js`)

Unions partner ids from five sources — every source fetched **by invoking a sibling field resolver
directly**, then discarding almost everything but the ids:

1. **Discussions** — `Product.SPARK_Product.discussionsV2(product, {}, ctx)` 🐞 cross-resolver →
   elastic `GET ${search}/discussion/v1/search/v2` (`relatedResources:{productId}`);
   keep `partnerId + droppedPartnerIds + designPartnerId` per discussion (`getDiscussionPartners`).
2. **Attachments** — `Product.SPARK_Product.attachmentsV3(product, {}, ctx)` 🐞 cross-resolver →
   the **full ADR-018 enrichment pipeline** (elastic + discussions + replies + ACL + counts), used here
   only for `content[].documentId`.
3. **Components** — `Product.SPARK_Product.components(product, {}, ctx)` 🐞 cross-resolver →
   the **full ADR-014 rollup** (~190 ln: 5 elastic queries + N+1 claim ACL + batched ACL + type tagging),
   used here only for `content[].id`.
4. **Samples** — `Product.SPARK_Product.samples(product, {}, ctx, info)` 🐞 cross-resolver — and the
   samples resolver reads **`info.variableValues.id/q/filter`** 🐞, so this aggregation silently inherits
   the caller's-variable-names coupling (cannot be ported — same as ADR-014 pin-down 5);
   used only for `samples[].partnerId`.
5. **Watchlists** — `workspaceId` = 🐞 **first entry only** of `productWorkspaceInfo[0].humanId` (fallback
   `productWorkspaceAttributes[0].humanId`); if present: elastic `searchWatchlist`
   (`parentId + workspaceContext + statusId:501`) → watchlist ids → `getAccessControlBatch(ids, 250)` →
   grantees (`getPartnersFromAccess`).
6. **ACL join for 2+3** — `detailIds` = component ids + attachment documentIds →
   `getAccessControlBatch(detailIds, 250)` — 🐞 chunks awaited **serially** (`accessControlUtils.js`) —
   → grantees of `bps`/`dps`/`MerchVendor`-style groups.
7. Union all five + `product.owningPartnerId`; `uniq`; return.

- 🐞 Steps 1–5 are **sequential awaits** for five independent sources.
- **Failure:** any source throwing fails the whole field — including failures in the heavyweight
  `components`/`attachmentsV3` machinery this field doesn't actually need.

### `Workspace.notRemovablePartnerIds` — `getWorkspacePartnersNotRemovable`

- Same shape, three sources: `WorkspaceV2.SPARK_WorkspaceV2.discussionsV2` 🐞 +
  `WorkspaceV2.SPARK_WorkspaceV2.attachmentsWithMetaData` 🐞 (the **ADR-018 read**, invoked cross-resolver
  for its `attachment.document_id`s) → `getAccessControlBatch(ids, 250)` → grantees +
  `workspace.owningPartnerId`.

### `Product.unDroppablePartners(isDesignPartner)` / `Workspace.unDroppablePartners` — `getUnDroppablePartners` (`utils/commonLoaders.js`)

1. Resolver gate: 🐞 computed **only when `args.isDesignPartner` is true**; otherwise returns `[]` —
   the field name promises more than the field delivers (UI asks it only for the design-partner flow).
2. `getAssociatedChildrensFromResouceId` — `relationship.searchByIds` with **no filters, no maxDepth**
   (`GET ${relationship}/{id}`) → full subtree → group by type → discussions, attachments, boms,
   packaging boms, samples, measurement sets, claims, **+ the product id itself**.
   ← the retiring Relationship-Service walk again (same root as ADR-015).
3. `getChunkedPermissions` — `accessControl.getPermissions` per chunk (`chunkArray`, parallel
   `Promise.all` — this one *is* parallel; carries a `TODO: fix getPermissions attaching "resourceIds"`).
4. Drop every resource whose permission list contains **any** `dps` group 🐞 — the whole resource is
   excluded even if other partners are also granted on it.
5. Return `uniq` of remaining grantees, 🐞 `.filter(Number)` — **numeric grantee ids only**, string ids
   silently dropped (the spike clone reproduced this with numeric seed ids 1001–1006).
- Workspace twin: identical, keyed on `workspace.workspaceHumanId || workspace.humanId`.

### Interaction grid

Homes: discussions → `plm-discussion` (via `plm-elastic-search`) · attachments → `plm-attachment` ·
samples → `plm-sample` · claims → spark-claims · bom/measurement/watchlist → co-located `plm-product` ·
ACL → AccessControlService · relationship → central service (**retiring**).

| Field | Relationship | Elastic | Discussion data | Attachment data | Sample data | Components (5-type) | ACL | Cross-resolver imports |
|---|---|---|---|---|---|---|---|---|
| `Product.notRemovablePartnerIds` | — (hidden inside siblings) | ✅ ×3+ | ✅ ① | ✅ ② (full ADR-018 pipeline) | ✅ ④ (`variableValues` 🐞) | ✅ ③ (full ADR-014 rollup) | ✅ ×2–3 batch(250) serial 🔥 | **4** 🐞 |
| `Workspace.notRemovablePartnerIds` | — (inside `attachmentsWithMetaData`) | ✅ | ✅ ① | ✅ ② | — | — | ✅ batch(250) | **2** 🐞 |
| `Product/Workspace.unDroppablePartners` | ✅ full walk ① | — | ids only | ids only | ids only | — | ✅ chunked ∥ ② | 0 |

> **Key findings:**
> - Neither field needs what it fetches — every source is reduced to **partner ids**. The five heavyweight
>   sibling invocations (incl. two entire complex-case pipelines) exist because "get me just the partner
>   slice" doesn't exist as an operation anywhere.
> - That makes this the cleanest **lane decomposition** case of all: each domain can answer
>   "which partners do *you* still reference for resource X?" with one cheap query it already owns.
> - `unDroppablePartners` is the same shape with the union computed from ACL grantees instead of domain
>   fields — its only structural dependency is the retiring relationship walk.
> - The `variableValues` coupling (via `samples`) **cannot be ported** — a decision is forced, not optional.

---

## 2. Decision drivers

- Phase-1 goal is **behavioral parity** — the UI greys out partner rows from these exact unions; a missed
  source un-greys a partner who still owns data (an admin then removes a partner who shouldn't be).
- Security-adjacent read, but a **read** — staleness risk is a wrong grey-out, not an access leak;
  still: async/materialized options must clear a higher bar than dashboard counts.
- `G-11-1` AC-2 is explicit: **no reflective resolver invocation remains** — every source becomes a direct,
  statically-typed call. The pattern chosen here decides what those calls are.
- The Relationship-Service walk (unDroppable) is retiring — per-domain enumeration must replace it
  (same conclusion as ADR-012 pin-down 1: each participant enumerates its own children).
- The workspace twins (`WORKSPACE-BE-G-05`, later phase) must inherit the pattern, not a redesign.
- The `removablePartner/` spike clone already **validated the end-state E2E**: owner-computed aggregation
  via `@requires` over per-domain lane fields, gateway resolving lanes first then `_entities` back to the
  owner — including the stand-in trick for not-yet-live subgraphs.
- Consistency: owner-computed reads (ADR-014), facade-then-federate phasing (ADR-015), async never for
  ACL/security edges (ADR-012).

### Assumptions, constraints & success criteria

**Assumptions**
- The five legacy sources (discussions, attachments+components, samples, watchlists, owning partner) are
  the complete set; per-source fixtures diffed against production samples confirm no source is reached
  only via ad-hoc ACL grants before cutover.
- Each referencing domain can answer "which partners do you still reference for X?" with one query it
  already owns (validated E2E in the `removablePartner/` spike clone).
- The UI's usage pattern holds: `unDroppablePartners` is queried only in the design-partner flow.

**Constraints**
- `G-11-1` AC-2: no reflective resolver invocation may remain — every source becomes a direct,
  statically-typed call or a federated lane.
- The `info.variableValues` coupling via the `samples` resolver cannot be ported — the lane contract must
  be settled with the UI team before cutover (hard blocker, pin-down 2).
- Lane fields must not leak into client-facing schemas (structural hiding until `@inaccessible` is usable).
- The Relationship-Service walk may survive phase 1 only quarantined inside the owner's enumeration client.

**Success criteria (measurable)**
- Per-source recorded fixtures match legacy output for both fields on product and workspace (union per
  source, plus the final union), with quirks (dps exclusion, `.filter(Number)`, first-workspace watchlist
  scope, `isDesignPartner` gate) each pinned by a dedicated fixture.
- Each lane flip (direct call → federated contribution) is individually gated on its per-source fixture
  staying green; the aggregator field's contract and fixtures never change.
- A schema-diff gate proves no lane field is exposed to clients.
- Zero cross-resolver invocations remain (statically verifiable); the ADR-014/ADR-018 pipelines are no
  longer dependencies of these fields.

---

## 3. Options

| | Option | Who computes the union | Sources come from | Parity | Verdict |
|---|---|---|---|---|---|
| A | Owner-computed, direct service calls | `plm-product` / `plm-workspace` field resolver | REST/Feign to each domain service | exact | viable — is also B's phase-1 interim |
| B | Owner-`@requires` lane aggregation (A now, lanes as subgraphs ship) | owning subgraph aggregator field | per-domain **lane fields** on the entity | exact | **recommended** |
| C | Central "partner references" service | new shared service | it queries every domain | exact | rejected — same inversion as ADR-012 §3-C |
| D | Materialized partner-reference index | indexer precomputes per resource | events/outbox pipeline | stale between updates | later refinement only |

### A — Owner-computed union over direct service calls (lift-and-shift, de-reflected)

- Port both utils into the owning subgraph; each source becomes a **client call scoped to ids/partners**
  (elastic discussions query, attachment-by-relatedResource query, sample-by-parent query, watchlist
  search, batched ACL) — never the sibling resolvers' full pipelines.
- ➕ exact parity · satisfies `G-11-1` AC-2 · kills the two accidental complex-case dependencies
  (components/attachmentsWithMetaData no longer invoked for ids).
- ➖ the owner keeps a client for every domain, forever · each new referencing domain = an owner change ·
  the "which partners do you reference?" question still has no owner-side contract.

### B — Option A now, per-domain lanes at federation ⭐ (the validated pattern)

- **The contract:** each referencing domain exposes a lane on the shared entity —
  `Product.discussionPartnerIds`, `Product.attachmentPartnerIds`, `Product.samplePartnerIds`, … (and the
  `Workspace.*` twins). Co-located domains (watchlist, bom, measurement) contribute in-process.
- **The aggregator:** `notRemovablePartnerIds` stays **owned by the entity's home subgraph** and is
  declared `@requires(fields: "discussionPartnerIds attachmentPartnerIds samplePartnerIds …")` — the
  gateway resolves the lanes first, then hands them back to the owner, which unions + `uniq`s + appends
  `owningPartnerId`. Exactly the mechanism the `removablePartner/` clone proved (gateway mechanism 3:
  lanes as synthetic jobs → `_entities` back to the owner with lane values in the representation).
- **Phasing:** phase 1 ships Option A's direct calls *behind the same aggregator field*; each lane flips
  from "owner queries the domain" to "domain contributes the lane" as its subgraph goes live — the field's
  contract and fixtures never change (facade-then-federate, applied to a field instead of a query).
- `unDroppablePartners`: same skeleton — each domain's lane is "ids of my children for X" (replacing the
  relationship walk, per ADR-012 pin-down 1); the owner keeps the ACL join + `dps` exclusion, which is
  ACL-service logic, not domain logic.
- ➕ every domain owns its slice (the case's stated goal) · new referencing domain = new lane, no owner
  change · relationship walk retired by construction · prototype-validated, incl. not-yet-live subgraph
  stand-ins · same runtime behavior as A in phase 1.
- ➖ lane fields are schema surface — they must be hidden from clients (the clone hit the fed-1
  `@inaccessible`-stripping gotcha; hiding is structural: externals + lane-suffix naming convention) ·
  `@requires` fan-out latency at the gateway once federated (bounded by the slowest lane — today it's
  serial, so this is still a win).

### C — Central partner-lifecycle/reference service

- One service answers "is partner P still referenced by anything under X?" for all resource types.
- ➕ one place to reason about removability.
- ➖ must know every domain's reference semantics (dropped ids, design partners, packet criticality) ·
  new always-on deployment nobody owns · rejected for the same reasons as ADR-012 §3-C — and here there
  isn't even a write to orchestrate.

### D — Materialized partner-reference index

- An indexer maintains `resource → referencing partners`; the field reads one document.
- ➕ one hop; no fan-out.
- ➖ needs the outbox/event pipeline (ADR-011 §3-D precondition) from **every** referencing domain ·
  stale grey-outs on exactly the screen where an admin is about to remove a partner · ACL grantee changes
  (unDroppable) don't flow through domain events at all. **Recorded as a later refinement**, only ever as
  a cache in front of B's lanes, never the source of truth.

---

## 4. Proposed decision (to ratify)

- **Option B** — the aggregation is **owned by the entity's home subgraph** (`plm-product` /
  `plm-workspace`), computed over **per-domain partner lanes**:
  - phase 1: the aggregator resolves lanes via direct service calls (Option A runtime, satisfying
    `G-11-1` AC-2), never via sibling resolver pipelines,
  - per lane, as the owning subgraph ships: the lane becomes a federated contribution
    (`extend type Product … @external/@requires` wiring per the `removablePartner/` clone), aggregator
    unchanged,
  - `unDroppablePartners` uses the same lanes for child enumeration + owner-side ACL join.
- **Option D recorded as a possible cache refinement** after all lanes federate; never for phase 1.
- Workspace twins (`WORKSPACE-BE-G-05`) inherit the contract — no second decision round.

### Pin-downs at ratification

| # | Item | Choice to make | Draft recommendation |
|---|---|---|---|
| 1 | 6 cross-resolver invocations 🐞 | — | replaced by scoped client calls / lanes by construction; the two complex-case pipelines (components, attachmentsWithMetaData) are **not** dependencies of these fields anymore |
| 2 | `samples` `variableValues` coupling 🐞 | which sample set is "the" source | **cannot port** — define the lane as "samples under this product (+ workspace context arg if the UI passes one)"; contract-check the UI queries before cutover (same as ADR-014 pin-down 5) |
| 3 | Sequential source fetches 🐞 | keep vs parallelize | parallelize (independent sources); accepted deviation — union output is order-insensitive so fixtures are unaffected |
| 4 | Serial ACL chunk loop (`getAccessControlBatch`) 🐞 | — | parallelize chunks; deviation noted (shared fix with ADR-015 pin-down 3) |
| 5 | `isDesignPartner`-only gate on `unDroppablePartners` 🐞 | preserve vs widen | **preserve exactly** — the UI only asks in the design-partner flow; widening is a product decision, not a migration one |
| 6 | `dps`-group whole-resource exclusion 🐞 | preserve vs per-group filter | **preserve** — encode a fixture with a mixed dps+bps resource so the quirk is pinned intentionally |
| 7 | `.filter(Number)` numeric-only grantees 🐞 | preserve vs include string ids | preserve (grantee ids are numeric partner ids in practice); log dropped non-numeric grantees so drift becomes visible |
| 8 | First-workspace-only watchlist scope 🐞 | preserve vs all workspaces | preserve `productWorkspaceInfo[0]` semantics; document in the lane contract; revisit with the PO post-parity |
| 9 | Relationship walk in `unDroppablePartners` | interim source before lanes exist | phase 1 may keep the walk **inside the owner's enumeration client only** (quarantined, per ADR-015 pin-down 7); each lane's arrival deletes its share |
| 10 | Lane visibility | how lanes are hidden from clients | structural hiding (externals + `…PartnerIds` lane naming convention) until fed-2/`@inaccessible` is available — the clone's D3 fallback |

---

## 5. Consequences

- If accepted:
  - `G-11-1` and `G-07` implement one aggregator + a lane-client seam each; parity fixtures record the
    union per source so lane flips are individually gated,
  - the accidental coupling to ADR-014/ADR-018 pipelines disappears — those cases can now change their
    internals without breaking partner removability,
  - ADR-012's participant contract and this ADR's lanes are two views of one per-domain obligation
    ("enumerate/answer for your children") — agree them as **one** contract with each domain team,
  - the workspace phase inherits contract + fixtures wholesale.
- Risks:
  - a referencing domain the legacy union silently covered via ACL grantees (e.g. ad-hoc grants) but no
    lane covers — the per-source fixtures must be diffed against production samples before cutover,
  - lane fields leaking into client schemas (pin-down 10) — add a schema-diff gate,
  - pin-down 2's contract check is the only hard blocker: if UI queries rely on differently-named
    variables, the samples lane definition must be settled with the UI team first.

---

## 6. On acceptance

Per `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md`:

1. Copy this write-up to `adrs/`; add the `SPIKE-04` block to `adrs/adr-index.yaml`
   (`status: Accepted`, `chosen: "B — …"`, all options preserved).
2. Flip `00-overview.md` §2 to **Decided**; add `01-stories.md` + implementation notes
   (incl. the lane contract table: lane field · owning domain · phase-1 client call · federation trigger).
3. Replace the *"per `SPIKE-04`"* placeholders in `output/initial-analysis/product/04-stories.md`
   (`G-07`, `G-11-1`); workspace stories follow in their phase.
4. Regenerate domain + global docs; push to Jira/Confluence.
