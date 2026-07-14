# ADR-018 (draft) — `attachmentsWithMetaData` enrichment (Product + Workspace)

> **Status:** 🔴 Proposed — draft for review
> **Spike:** — (read pattern applied at cutover, not a research spike)
> **Home stubs:** `SPARK-PROD-G01` (product enrichment) · `SPARK-PROD-G03` (thin variants) ·
> `SPARK-WS-G01` / `SPARK-WS-G03` (later phase, workspace twins)
> **Scope:** the one-feed attachments tab — direct files + discussion files + sample files, merged,
> permission-annotated, draft-filtered, ordered — on both `Product` and `WorkspaceV2`, plus the thin
> variants (`attachments` / `attachmentsV3` / `attachmentSummary`) over the same engine. Reads only.
> **Related:** ADR-014 (owner-computed rollups — same stance) · ADR-015 (facade-then-federate phasing) ·
> ADR-016 (consumes this read cross-resolver today — that coupling dies with ADR-016 §4) ·
> `SPARK-SPIKE-06a` (hydration).
> **Evidence:** `resolvers/SPARK_Product.js` + `resolvers/SPARK_WorkspaceV2.js` +
> `utils/Product/attachmentUtils.js` + `utils/discussionUtils.js` at `https://github.com/XXX`.

---

## 1. Today's behavior

### `Product.attachmentsWithMetaData` (`SPARK-PROD-G01`, ~150 ln)

1. **Relationship walk** — `relationship.searchByIds` (`GET ${relationship}/{productId}`,
   10 `includeBranches`, node types `attachments / sample / discussions / discussionThreads /
   attachments_v3`, no `maxDepth`) → partition ids into 5 buckets; no attachment ids → `[]`.
2. **Two ACL capability tokens** — `accessControl.getUserAccessByPost` for attachment ids, then again for
   sample ids — 🐞 sequential, and the samples token is fetched even when no sample bucket is consulted
   until step 5.
3. **Hydrate attachments** — `attachment.getAttachmentsV3(JWT)` —
   `GET ${attachment}/attachments/v3?humanIds={v2+v3 ids}`; empty → `[]`.
4. **Viewer permissions** — `accessControl.getUserAccessUnencoded` for the attachment ids →
   `currentUserPermissions` (annotated per attachment later).
5. **Related-resource fetches** — 🐞 three more sequential awaits: discussions
   (`getDiscussionsBatch`, chunked), threads (`getDiscussionThreadsBatch`), samples
   (`sampleV2.getSamplesByIdsV2(samplesJWT)`).
6. **Enrich per attachment** — find its discussion / thread / sample by `attachment.resource.id`:
   - thread hit → 🐞 `mainDisc = find(discussions, …)` then **`mainDisc.sampleDiscussion` unguarded** —
     a thread whose parent discussion fell outside the walk crashes the whole field (TypeError),
   - sample-discussion → `linkedResourceId` = `resources.mappings.sample[0]`, else the discussion id,
   - carry `resourceTitle`, `isResourceCritical`, `isResourceDraft`, `isSampleDiscussion`,
   - attach the viewer's `currentUserPermissions` entry.
7. **Draft filter** — drop `resource.type === 'discussion'` rows with no link or draft —
   the *"TODO: ACL should bbe doing this"* rule.
8. **Order** — `orderProductAttachments`: rank by `resource.type` via
   `['product','discussion','sample'].indexOf` **asc**, then `created_at` **desc**.

### `WorkspaceV2.attachmentsWithMetaData` (`SPARK-WS-G01`, ~75 ln) — same shape, different rules

- Walk with 3 branches / 4 node types; 🐞 **v2 `attachments` ids are requested from the walk but never
  collected** — only `attachments_v3` count (empty v3 → `[]` even if v2 files exist).
- No sample bucket at all.
- 🐞 **Ordering differs**: `_.orderBy(attachments, ['resource.type','created_at'], ['desc','desc'])` —
  raw type-string **desc** (alphabetical), applied **before** enrichment — not the product's rank order.
- Enrichment defaults differ: `relatedResource = {}` → `linkedResourceId`/`resourceTitle` come out
  `undefined` instead of the key being absent; draft flag = thread's `draft` else discussion's.
- Same draft filter, duplicated verbatim (same TODO).

### The thin variants (`SPARK-PROD-G03` / `SPARK-WS-G03`) — one engine, three doors

- `Product.attachmentsV3` → `getProductOrWorkSpaceAttachments` (`utils/Product/attachmentUtils.js`):
  1. **elastic, not the walk** — `search.searchAttachmentsByRelatedResource` —
     `GET ${search}/attachments/v1?relatedIds={id}…`,
  2. 🐞 discussions **by importing the discussion resolver directly** —
     `SPARK_Discussion.Query.getDiscussionsV2({}, {resourceId}, ctx)` — then a 🐞 **serial per-discussion
     `getDiscussionRepliesV2` loop** (N discussions = N sequential reply fetches),
  3. `accessControl.getPermissions` for the attachment ids,
  4. `createAttachmentPaged` → `filterAttachmentsOrComponents(args)` (workspace/partner/tags/type/
     archived/packet filters) — also the engine behind `components`' attachment sibling.
- `WorkspaceV2.attachmentsV3` — 🐞 **dual-mode**: `args` present → the elastic engine above; `args`
  absent → relationship walk + `resolveRelationIds`, which itself branches on
  🔥 `ctx.featureConfig.attachmentElasticResponseFeatureFlag` (service hydration vs one elastic query) —
  **three data paths for one field**.
- `Product.attachments` — walk at `maxDepth: 0` only; `Product.attachmentSummary` —
  elastic by related-resource + thumbnail match (`previewable`, `totalAttachmentCount`).
- Shared engine details (`createAttachmentPaged`):
  - missing ACL entry → **skip the row + `logger.error`** (graceful — the opposite of `components`'
    throw, ADR-014 pin-down 2),
  - 🐞 `relatedResources` precedence bug — `a.relatedResources || (cond) ? [] : [resourceId]` parses as
    `(a.relatedResources || cond) ? [] : [resourceId]`: any row with its own `relatedResources` returns
    `[]`, which is almost certainly not the written intent but **is** today's output,
  - a **third ordering** — `orderAttachmentsByType`: product-first binary rank + `createdAt` desc
    (camelCase field, vs the resolvers' snake_case `created_at`).

### Interaction grid

Homes: relationship → central service (**retiring**) · ACL → AccessControlService · attachment →
`plm-attachment` · discussion → `plm-discussion` · sample → `plm-sample` · elastic → `plm-elastic-search`.

| Field | Relationship | ACL (token / viewer / perms) | Attachment | Discussion | Sample | Elastic | Order rule | Paths |
|---|---|---|---|---|---|---|---|---|
| `Product.attachmentsWithMetaData` | ✅ full walk ① | ✅ ×3 ②④ (serial 🔥) | ✅ ③ | ✅ ⑤ batch ×2 | ✅ ⑤ | — | rank asc + date desc | 1 |
| `WorkspaceV2.attachmentsWithMetaData` | ✅ walk ① | ✅ ×2 | ✅ | ✅ batch ×2 | — | — | 🐞 type desc + date desc | 1 |
| `Product.attachmentsV3` (+ `components`' sibling) | — | ✅ perms | — | 🐞 resolver import + N+1 replies | — | ✅ ① | product-first + date desc | 1 |
| `WorkspaceV2.attachmentsV3` | ✅ (no-args mode) | ✅ | ✅ (flag off) | ✅ | — | ✅ (args mode / flag on) | product-first | **3** 🐞🔥 |
| `Product.attachments` / `attachmentSummary` | ✅ depth 0 / — | — | ✅ / — | — | — | — / ✅ | — | 1 |

> **Key findings:**
> - **True cross-subgraph read** — the enrichment genuinely joins four future subgraphs (attachment ×
>   discussion × sample × ACL); no single existing service can answer it today.
> - But the *sources* are already per-domain queries — the walk only discovers **ids**; the elastic
>   engine proves the same feed can be sourced without it (`relatedResources:{id}` is the replacement).
> - The duplication is worse than the fan-out: **two resolvers + one util = three orderings, two draft
>   filters, two enrichment shapes** for "the same" feed — that divergence, not the joins, is what a naive
>   port would fossilize.
> - ADR-016 consumes this field cross-resolver for ids only; once its lanes land, this read has exactly
>   one job: the user-facing tab.

---

## 2. Decision drivers

- Phase-1 goal is **behavioral parity per surface** — the product tab and workspace tab differ today
  (ordering, v2 handling, defaults) and the UIs are calibrated to their own surface; "unifying" them is a
  visible regression, not a cleanup.
- The Relationship-Service walk is retiring — this case must move to the by-related-resource sourcing the
  elastic engine already demonstrates.
- Interactive tab read — latency budget is one paint; the serial ACL/discussion/sample chain and the
  reply N+1 are the perf debt to pay down while we're in there (same stance as ADR-014's fixes).
- Product and workspace land in **different subgraphs** (`plm-product` now, `plm-workspace` later) — the
  engine must be shareable without a shared runtime (ADR-013's shared-library precedent).
- The draft-filter TODO is a security-adjacent rule living in the read path — it must survive the port
  verbatim, and the "ACL should do this" question must go somewhere real.
- Reads: no saga/outbox; the questions are **who computes the merge** and **where each slice comes from**
  (mirrors ADR-014/015/016).

---

## 3. Options

| | Option | Who computes the merge | Slices come from | Parity | Verdict |
|---|---|---|---|---|---|
| A | Owner-computed, shared enrichment library + per-surface policy | `plm-product` / `plm-workspace` field resolver | direct clients (attachment/discussion/sample/ACL) | exact per surface | **recommended** |
| B | `plm-attachment` computes the feed | attachment subgraph | it calls discussion/sample/ACL | risky | rejected — wrong owner for the rules |
| C | Federated per-domain lanes, owner merges | owning subgraph via `@requires` | each domain contributes its slice | exact | end-state, blocked on subgraphs |
| D | Elastic single-source (the feature-flag path) | owning subgraph, one query | `plm-elastic-search` | unproven | input to C; pin the flag first |

### A — Owner-computed enrichment over a shared library ⭐

- One **enrichment library** (extracted once from `createAttachmentPaged` + the two resolvers), consumed
  by both subgraphs; behavior differences become a declared **per-surface policy table** —
  source set (± samples, ± v2), ordering rule, enrichment defaults, draft filter, packet filter —
  instead of three accidental implementations.
- Sourcing: ids come **by related-resource** (attachment: `relatedResources:{id}`; discussions:
  `resourceId`; samples: by parent) — the walk survives phase 1 only where no replacement query exists
  yet, quarantined behind one enumeration seam (ADR-015 pin-down 7 stance).
- Mandatory fixes riding the port (each an accepted, documented deviation):
  1. parallelize the independent fetches (tokens ∥, discussions ∥ threads ∥ samples),
  2. guard the thread→parent-discussion lookup (skip + log, same semantics as the engine's missing-ACL
     path) instead of crashing the field,
  3. discussion data via a **direct discussion-service client** + batched replies — the resolver import
     and the reply N+1 both die,
  4. every surface keeps **its own** ordering + defaults, pinned by fixture.
- ➕ exact per-surface parity · one engine, policy-visible differences · workspace phase inherits library +
  fixtures · perf debt paid without changing any row's content.
- ➖ a shared library to version across two repos · the walk lingers (quarantined) until per-slice queries
  are confirmed for every bucket.

### B — `plm-attachment` computes the merged feed

- The attachment subgraph exposes `attachmentsFor(resourceId, surface)`; product/workspace delegate.
- ➕ most rows are attachment rows; one implementation.
- ➖ the *rules* aren't attachment rules — thread/draft semantics (discussion), sample linkage (sample),
  surface ordering (product/workspace UX) would all migrate into the wrong domain (same rejection as
  ADR-014 §3-B) · per-viewer ACL still fans out. Rejected for phase 1 and as end-state.

### C — Federated per-domain lanes, owner merges

- Each domain contributes its slice on the entity (`Product.directAttachments` from `plm-attachment`,
  `…discussionAttachments` from `plm-discussion`, `…sampleAttachments` from `plm-sample`); the owner's
  `attachmentsWithMetaData` merges/orders/filters via `@requires` — the ADR-016 mechanism applied to a
  list feed.
- ➕ true slice ownership; the enrichment library shrinks to merge + policy.
- ➖ blocked on `plm-discussion`/`plm-sample` being live · list-valued lanes are heavy `_entities`
  payloads — needs the gateway cost measured first. **Recorded as the end-state**, adopted per-slice
  (ship-on-green) exactly like ADR-015's F-phase.

### D — Elastic single-source

- The engine's flag path already answers the feed with one query
  (`_index:attachments AND relatedResources:{id}`) — no walk, no hydration.
- ➕ one hop; the code exists.
- ➖ 🔥 flag state per environment is **unknown at analysis time** — the two paths return differently
  shaped rows (snake vs camel handled by compatibility fallbacks in the engine) · thread draft/critical
  still needs discussion data · index staleness on a tab users refresh after uploading. Not a decision
  this ADR can take alone; **pinned below**, and recorded as the likely sourcing for C's attachment lane.

---

## 4. Proposed decision (to ratify)

- **Option A** — each owning subgraph computes its own feed through one shared enrichment library with an
  explicit per-surface policy table; fixes 1–3 as accepted deviations; sourcing moves by-related-resource,
  walk quarantined.
- **Option C recorded as the end-state**, adopted slice-by-slice as sibling subgraphs ship; Option D's
  elastic query is the candidate attachment-slice source, contingent on pin-down 5.
- The thin variants (`G03`) are doors onto the same library — no separate engine.

### Pin-downs at ratification

| # | Item | Choice to make | Draft recommendation |
|---|---|---|---|
| 1 | Three ordering rules 🐞 | unify vs preserve per surface | **preserve each exactly** (product rank-asc/date-desc · workspace type-desc/date-desc · engine product-first) — declared in the policy table, one fixture each; unification is a PO decision post-parity |
| 2 | Workspace ignores v2 attachments 🐞 | preserve vs include | **preserve** — treat as intentional post-v3 state (same stance as ADR-015 pin-down 5); note in fixture |
| 3 | Thread→parent crash 🐞 | preserve crash vs degrade | skip + log the row (accepted deviation) — a data-integrity gap shouldn't kill the tab |
| 4 | Resolver import + reply N+1 🐞 | — | direct discussion client + one batched replies call; deviation noted |
| 5 | `attachmentElasticResponseFeatureFlag` 🔥 | which path is truth | **survey every environment before fixtures are recorded**; port the active path as primary and keep the other behind the same config key; fixtures recorded against the active path |
| 6 | `WorkspaceV2.attachmentsV3` dual-mode 🐞 | keep both modes vs collapse | keep both in phase 1 (callers may rely on either); log mode usage; collapse is a v2-API question |
| 7 | Draft filter TODO | keep in read path vs push to ACL | keep verbatim in the library (single copy now); file the ACL enforcement item on the access-control backlog — removing the filter is **never** a migration-time change |
| 8 | Missing-ACL skip+log vs `components`' throw | align vs preserve both | preserve both (each surface's UI is calibrated); record the asymmetry beside ADR-014 pin-down 2 so nobody "fixes" one to match the other |
| 9 | `relatedResources` precedence bug 🐞 | preserve output vs fix intent | **preserve today's output** (fixture pins it); annotate the library code with the precedence note; fixing it changes visible payloads and needs a client survey |
| 10 | Sequential fetches 🐞 | — | parallelize (fix 1); deviation noted — same stance as ADR-014 pin-down 7 / ADR-015 pin-down 2 |

---

## 5. Consequences

- If accepted:
  - `G01` builds the library + the product policy row; `G03` becomes thin doors; the workspace phase
    (`WS-G01`/`G03`) adds a policy row and fixtures, not a design round,
  - ADR-016's lanes stop depending on this read's internals — the two cases decouple,
  - tab latency improves (parallel fetches, batched replies) with byte-identical content,
  - the three-way divergence becomes a reviewed table instead of archaeology.
- Risks:
  - pin-down 5 is the schedule risk: fixtures recorded against the wrong flag path invalidate the parity
    gate — survey first,
  - the policy table quietly growing per-surface *behavior* forks — every new row needs a PO sign-off,
  - fixture recording must include: a thread whose parent discussion is missing (crash path → skip path),
    a draft discussion attachment (filter), a row with its own `relatedResources` (precedence quirk),
    a workspace with v2-only attachments (empty-feed path), and both `attachmentsV3` modes — or the edge
    behavior ships unverified.

---

## 6. On acceptance

Per `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md` (adapted — no spike id; this case is
pattern-at-cutover):

1. Copy this write-up to `adrs/`; add a case block to `adrs/adr-index.yaml`
   (`status: Accepted`, `chosen: "A — …"`, all options preserved).
2. Flip `00-overview.md` §2 to **Decided**; add `01-stories.md` + implementation notes
   (incl. the per-surface policy table and the deviation list).
3. Update `output/initial-analysis/product/04-stories.md` (`G01`, `G03`) with the concrete pattern;
   workspace stories follow in their phase.
4. Regenerate domain + global docs; push to Jira/Confluence.
