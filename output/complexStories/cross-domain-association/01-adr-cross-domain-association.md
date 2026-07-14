# ADR-011 (draft) — Cross-Domain Association writes (`SPARK-SPIKE-06b`)

> **Status:** 🔴 Proposed — draft for review
> **Spike:** `SPARK-SPIKE-06b` · **Home stub:** `SPARK-PROD-S01` · **Gates:** `D01 D02 D03 D04 D06 D07 D11`
> **Scope:** the *write* half of cross-domain — a mutation that also links its record into a sibling domain.
> Hydration (reads) is `SPARK-SPIKE-06a`, **not** decided here.
> **Prior art:** ADR-010 (Teams ↔ Domain association) — must stay consistent with it.
> **Evidence:** `resolvers/SPARK_Product.js` + `services/Product.js` at `https://github.com/XXX`.

---

## 1. Today's behavior, mutation by mutation

### D01 · `addProduct(workspaceId, sparkProduct, copyProduct)`

1. Create product — `POST ${v1}`.
2. `workspaceId`? → ACL token for the workspace, then `workspaceV2.addResourcesToWorkspaceV2` links the new id.
3. `copyProduct`? → set `targetProductId` = new id, ACL token, `POST ${v2}/copy-details`;
   graft `copyId` / `copyProductRequest` / `copyProductResources` onto the result.
4. Return product.

- **Failure:** sequential, no rollback — a failed link or copy errors the mutation *after* the product exists.

### D02 · `addProducts(workspaceId, products[])` — one create, four association fan-outs

1. ACL token for the workspace, up front.
2. Bulk create — `POST ${v1}/bulk` (input `attachmentId` → `thumbnailId`).
3. Per input with an `attachmentId` (created product matched back by `thumbnailId`), build:
   - attachment re-point — `{documentId, resource: {id: productId, type: 'product'}}`,
   - relationship node — root `productId` (`product`) → node `attachmentId` (`attachments_v3`),
   - attachment attributes — `relatedResources: [productId]`; with `businessPartners` also
     `productPacketProps` (each partner `critical: true`) + `managePermissionsRequest.partnersToAdd`.
4. Attachment metadata — calls `SPARK_Attachment.Mutation.bulkUpdateAttachmentsV2(...)`
   **by importing the attachment resolver directly**. ← the coupling this spike exists to remove.
5. Relationship graph — `relationship.createBulkRelationship`; status ≥ 400 **rejects the whole mutation**,
   though products were created in step 2.
6. Attachment re-point — `attachment.bulkUpdateResource` — **not awaited** (fire-and-forget).
7. Workspace — `addResourcesToWorkspaceV2` for all created ids.
8. Return the bulk-create result.

- **Failure:** no rollback anywhere; one call never even checked.

### D03 · `bulkUpdateProducts(products)`

- Pure passthrough — `PUT ${v1}/mass_update`.
- No cross-domain call in the resolver; "cross-domain" only in that the DTO can carry association-ish fields
  the backend fans out.

### D04 · `updateProduct(input, copyProduct)`

1. Update product (only if `input` has keys besides `id`) — `PUT ${v1}/{id}`.
2. `copyProduct`? → same copy helper as D01; merge copy metadata into the result.
3. `removedProductTemplateAttachments`? → split: `humanId` → v3, `documentId` → v2;
   per list: ACL token, then `archiveAttachmentBulkV2` / `archiveAttachmentBulkV3` (awaited).
4. Return product.

- **Failure:** sequential, no rollback — a failed archive errors the mutation after the update committed.

### D06 · `addTeamsToProduct(productId, workspaceIds, teamIds, newPartners)` 🔀 Collab Canvas

1. `newPartners`? → `POST ${v1}/{productId}/partners-add/bulk`; on error **return `new Error(...)`**
   (early exit — teams never added).
2. Add teams — `POST ${v1}/{productId}/resources/bulk`.
3. `workspaceIds`? → every `workspaceId × teamId` pair → `PUT ${v1}/{productId}/manage_workspace_teams`;
   return that. Else return the add-teams result.

- **Failure:** sequential; partners can land and teams fail; no compensation.
- All three endpoints are on the **product backend** — cross-domain in concept, single-service in execution.

### D07 · `addBusinessPartnersToProductWithType(productId, partners)` 🔀 Collab Canvas

- Single write — `POST ${v1}/{productId}/partners-add/bulk`.
- Success = response has `product_id`, no `status_code` → return it.
- Failure = log, then **`return new Error(...)`** (returned, not thrown — surfaces as a field error).

### D11 · `updateWorkspaceAttributes(productId, workspaceAttributesInput)` 🔀 Collab Canvas

- Pure passthrough — `PUT ${v1}/{productId}/workspaceAttributes/{humanId}`.
- Per-workspace attributes live **on the product record**; the workspace service is never called.

### Interaction matrix

Homes: product → `plm-product` · workspace → `plm-workspace` · attachment → `plm-attachment` ·
relationship → central platform service · ACL → AccessControlService.

| Mutation | Product | Workspace | Attachment | Relationship | ACL | Cross-subgraph write? |
|---|---|---|---|---|---|---|
| D01 `addProduct` | create + copy | ✅ | — | — | ✅ ×2 | **Yes** — workspace |
| D02 `addProducts` | bulk create | ✅ | ✅ metadata (cross-resolver) + re-point (unawaited) | ✅ | ✅ ×3 | **Yes** — 3 domains |
| D03 `bulkUpdateProducts` | mass_update | — | — | — | — | No |
| D04 `updateProduct` | update + copy | — | ✅ archive V2/V3 | — | ✅ | **Yes** — attachment |
| D06 `addTeamsToProduct` | 3 endpoints | — | — | — | — | No — single backend |
| D07 `addBusinessPartnersToProductWithType` | 1 endpoint | — | — | — | — | No — single backend |
| D11 `updateWorkspaceAttributes` | 1 endpoint | — | — | — | — | No — single backend |

> **Key finding:** only **D01, D02, D04** orchestrate across future subgraph boundaries.
> **D03, D06, D07, D11** hit the product backend only → plain `@DgsMutation`s, no orchestration decision.
> The spike's blast radius is three mutations, not seven.

---

## 2. Decision drivers

- Phase-1 goal is **behavioral parity** — same inputs, outputs, side-effects, proven by parity tests.
- Today's contract is synchronous: the mutation returns **after** links exist; the UI reads-after-write
  (e.g. navigates straight to the workspace listing after `addProduct`).
- Partial failure is real but undocumented: no rollback anywhere, one fire-and-forget call.
- A federated gateway does **not** orchestrate multi-subgraph mutations natively.
- ACL capability tokens must keep flowing (header forwarding via `@DgsContext` filter).
- Collab Canvas consumes D06/D07/D11 — its contract must not change in phase 1.
- Must stay consistent with ADR-010.

---

## 3. Options

| | Option | Semantics | Parity | Verdict |
|---|---|---|---|---|
| A | Sync in-subgraph orchestration | mutation → REST clients to siblings | exact | viable, but keeps ad-hoc fan-outs |
| B | A + shared association component | same, via one `associate(...)` API | exact | **recommended** |
| C | Client/gateway composition | split into per-subgraph mutations | breaks contract | disqualified for phase 1 |
| D | Event-driven (Kafka + transactional outbox) | write + outbox row in one txn, relay publishes, consumers link | breaks read-after-write | end-state, not phase 1 |

### A — Synchronous in-subgraph orchestration (lift-and-shift, formalized)

- The `plm-product` `@DgsMutation` does the primary write, then calls siblings **service-to-service**
  (Feign/REST to workspace, attachment, relationship) — never subgraph-to-subgraph GraphQL.
- ➕ exact parity · no new infra · D02's resolver import becomes an honest client call.
- ➖ each mutation still hand-rolls its fan-out (the "five ad-hoc versions" survive) ·
  partial-failure behavior stays implicit.

### B — Option A + shared association component ⭐

- One internal component — `associate(sourceRef, targetDomain, targetRef, props)` — wraps the
  workspace / attachment / relationship link calls; every gated mutation uses it.
- Partial-failure policy (fail-fast · best-effort · compensate) is a **declared parameter** per mutation,
  not implicit resolver code.
- ➕ kills the duplicated fan-outs (`SPARK-PROD-S01`'s stated problem) · failure policy explicit and testable ·
  internals can later switch to events (D) without touching mutation signatures · same runtime behavior as A.
- ➖ one more abstraction to own · doesn't fix partial failure by itself — only makes the policy visible.

### C — Client/gateway-level composition

- Split: `addProduct` in `plm-product`, workspace link in `plm-workspace`, attachment link in
  `plm-attachment`; the UI (or a thin layer) calls them in sequence.
- ➕ purest domain boundaries.
- ➖ every Spark UI / Collab Canvas caller changes · gateway can't orchestrate it · failure handling
  re-implemented per client. **Disqualified for the parity phase**; revisit only as a v2 API shape.

### D — Event-driven associations

- `plm-product` commits, publishes `ProductCreated` / `ProductUpdated`; consumers create the links.
- ➕ full decoupling · retries + idempotency answer partial failure cleanly.
- ➖ mutation would return before links exist → UI read-after-write races · D02's "reject on relationship
  failure" contract inexpressible · needs event infra, idempotency keys, monitoring.
- **Reliability — transactional outbox required**, or D is worse than today:
  - naïve publish-after-commit is a dual-write: a crash between DB commit and Kafka publish silently
    drops the event → links never created, no visible error,
  - outbox: product row + `outbox_events` row commit in **one DB transaction**; a relay
    (Debezium CDC or poller) publishes to Kafka → event exists iff the write committed,
  - key messages by `productId` for per-product ordering; at-least-once delivery → consumers stay idempotent,
  - **placement caveat:** the outbox must live in the **product backend service** (it owns the DB
    transaction), not the DGS — the DGS orchestrates over REST and can't retrofit this. D is therefore
    a backend-team dependency,
  - outbox makes async *reliable*, not *synchronous* — the read-after-write race remains, so it does not
    rescue D for phase 1.
- **Recorded as the target end-state** for edges that don't need synchronous confirmation.

---

## 4. Proposed decision (to ratify)

- **Option B** for phase 1:
  - synchronous orchestration through one shared association component in `plm-product`,
  - per-mutation failure policy declared explicitly; default = today's fail-fast / no-rollback, documented.
- **Option D recorded as end-state** — with the **transactional outbox as a stated precondition**
  (outbox in the product backend's DB transaction, CDC/poller relay, idempotent consumers);
  revisit after `SPARK-SPIKE-06a` + read federation land.
- **Scope exclusions** (satisfies `SPARK-PROD-S01` AC-3):
  - D03, D06, D07, D11 → plain `plm-product` mutations; component not required,
  - Collab Canvas trio = the documented exception — association *semantics*, but the product backend owns
    the write, so no cross-subgraph pattern applies.

### Pin-downs at ratification

| # | Item | Choice to make | Draft recommendation |
|---|---|---|---|
| 1 | D02 unawaited `bulkUpdateResource` | await vs preserve fire-and-forget | await; list as accepted parity deviation |
| 2 | D02 post-create reject on relationship failure | accept non-atomic vs compensate | accept + document; defer compensation to `SPARK-SPIKE-01` (saga) |
| 3 | D02 cross-resolver import of `bulkUpdateAttachmentsV2` | — | replace with attachment-service client call inside the component |
| 4 | D06/D07 `return new Error(...)` | keep vs standardize | thrown typed errors (`DgsException`); accepted parity deviation |

---

## 5. Consequences

- If accepted:
  - D01/D02/D04 stories reference one named component + one failure-policy table,
  - D03/D06/D07/D11 unblock immediately (no dependency on the component build),
  - the component is a new `plm-product` module with unit + parity tests,
  - a later move to Option D touches component internals only.
- Risks:
  - the component becomes a dumping ground — keep its contract to *associate / dissociate* only,
  - the accepted deviations (pin-downs 1 & 4) must be in the parity-test exception list up front,
    or the gate fails on known-good changes.

---

## 6. On acceptance

Per `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md`:

1. Copy this write-up to `adrs/`; add the `SPARK-SPIKE-06b` block to `adrs/adr-index.yaml`
   (`status: Accepted`, `chosen: "B — …"`, all options preserved).
2. Flip `00-overview.md` §2 (06b half) to **Decided**; add `01-stories.md` + implementation notes.
3. Replace the *"per `SPARK-PROD-S01`"* placeholders in `output/initial-analysis/product/04-stories.md`
   (D01–D04, D06, D07, D11) with the concrete pattern.
4. Regenerate domain + global docs; push to Jira/Confluence.
