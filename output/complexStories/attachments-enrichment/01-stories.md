# Attachments Enrichment — Story Breakdown

> **Decision:** [ADR-018 (draft)](./01-adr-attachments-enrichment.md) — owner-computed enrichment via one
> shared library + a per-surface policy table (Option A; federated per-domain lanes recorded as end-state,
> Option C).
> **Status:** 🟠 Draft proposed — ratification pending.
> **This file lists which concrete stories implement the decision — full story text lives in
> `output/analysis/product/be-04-stories.md`, linked below.**

## Product-side (phase 1)

| Story | What it builds | Pin-downs closed |
|---|---|---|
| [`PRODUCT-BE-G-01`](../../analysis/product/be-04-stories.md#product-be-g-01-productattachmentswithmetadata) | `Product.attachmentsWithMetaData` — the shared enrichment library + product's policy-table row | pin-down 2 (v2-ignoring note, product-side has no gap), pin-down 3 (thread→parent crash becomes skip+log), pin-down 4 (direct discussion client + batched replies, replacing the cross-resolver import + N+1 loop), pin-down 5 (feature-flag environment survey, blocking pre-condition on fixtures), pin-down 7 (draft-filter TODO preserved verbatim), pin-down 9 (`relatedResources` precedence bug preserved), pin-down 10 (parallelize independent fetches) |
| [`PRODUCT-BE-G-03`](../../analysis/product/be-04-stories.md#product-be-g-03-productattachments-attachmentsv3-attachmentsummary-producttemplateattachmentsdata) | thin `attachments`/`attachmentsV3`/`attachmentSummary` doors over G-01's library | inherits all of G-01's fixtures/pin-downs by construction |

`PRODUCT-BE-G-01`'s own body flags pin-down 8 (missing-ACL skip+log vs `PRODUCT-BE-G-02`'s throw) as an
intentional, by-design asymmetry — not something to "fix" for consistency.

## Not yet built — the shared library as its own artifact

The shared enrichment library (extracted from `createAttachmentPaged` + the two legacy resolvers) is
currently bundled inside `PRODUCT-BE-G-01`'s own scope rather than built as a separate, explicitly
library-shaped story. **Flagged as a gap** — if the workspace twin (below) needs the library before
`PRODUCT-BE-G-01` ships, extracting it into its own story first is worth reconsidering; not done in this
pass.

## Workspace-side (later phase — not yet written)

| Story | Status |
|---|---|
| `WORKSPACE-BE-G-01` | named in the ADR as the twin for `WorkspaceV2.attachmentsWithMetaData`; not yet written — owes pin-down 6 (`attachmentsV3` dual-mode preserved) when authored |
| `WORKSPACE-BE-G-03` | named in the ADR as the thin-variant doors twin; not yet written |

## Relationship to ADR-016 (notRemovable-undroppable-partners)

This case's static-check/CI-gate item (verifying ADR-016's `notRemovablePartnerIds`/`unDroppablePartners`
no longer invoke this read cross-resolver) is recorded in ADR-016's own pin-down 1 and
`PRODUCT-BE-G-11-1`'s AC — not duplicated here.

## ACL

Elastic single-source candidate (Option D, pin-down 5) requires a per-environment
`attachmentElasticResponseFeatureFlag` survey **before** fixtures are recorded — this is a blocking
pre-condition on `PRODUCT-BE-G-01`, not a separate story.

---
*Story ids and links regenerate from `output/analysis/product/be-04-stories.md` — this index is
hand-maintained alongside the ADR.*
