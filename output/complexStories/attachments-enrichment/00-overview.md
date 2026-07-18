# Complex Story — `attachmentsWithMetaData` enrichment (Product + Workspace)

> **Summary —** One attachments tab, three hidden sources — files, discussion files, sample files — merged and ordered today by a Relationship-Service walk we're retiring; make each domain contribute its own slice instead.
> **Spike:** — *(read pattern applied at cutover, not a research spike)* · **Status:** 🟠 Draft ADR-018 proposed — ratification pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub story:** `PRODUCT-BE-G-01`/`G-03` + `WORKSPACE-BE-G-01` (later phase)/`G-03`

> **Migrates (source resolvers → this case):** product **FR `attachmentsWithMetaData`** (`PRODUCT-BE-G-01`) +
> the thin variants `attachments`/`attachmentsV3`/`attachmentSummary` (`PRODUCT-BE-G-03`); workspace
> **FR `attachmentsWithMetaData`** (`WORKSPACE-BE-G-01` (later phase)) + `attachmentsV3` (`WORKSPACE-BE-G-03` (later phase)). Fans out to per-domain
> attachment buckets (attachment, discussion, sample).

## 1. The problem (grounded in the code)

### 1.1 Problem statement

- The attachments tab on `Product` and `WorkspaceV2` is one merged, permission-annotated, ordered feed
  built from three domains (attachment, discussion, sample) plus access control — implemented **three
  different ways** (two resolvers + one shared util) with three ordering rules and two draft filters.
- Sourcing depends on the retiring Relationship-Service walk; a naive port fossilizes both the walk and
  the three-way divergence.

### 1.2 Current state & root cause

**What this read does.** The attachments tab on a product or workspace lists every file in one feed —
- files attached directly, files shared inside discussions, and files on samples — each enriched with who may see it and where it came from.
- Building that one list means reading three domains plus access control.

`Product.attachmentsWithMetaData` (~150 ln, `PRODUCT-BE-G-01`) and `WorkspaceV2.attachmentsWithMetaData`
(~75 ln, `WORKSPACE-BE-G-01` (later phase)) both do the **same shape** of work:

1. **Relationship Service** `searchByIds` → the resource subtree (attachments_v3, discussions, discussionThreads, samples).
2. partition into buckets → **hydrate attachments** (`getAttachmentsV3`, with ACL) per bucket.
3. batch **discussion / thread** attachments; product also folds in **sample** attachments.
4. **merge** the 5 (product) / 3 (workspace) sources.
5. **order** by `resource.type` rank (product=0, discussion=1, sample=2) then `createdAt DESC`.
6. **draft filter** — drop discussion attachments with no link / draft (carries a *"ACL should do this"* TODO).

- `PRODUCT-BE-G-03` / `WORKSPACE-BE-G-03` (later phase) (`attachments`, `attachmentsV3`, `attachmentSummary`) are thin variants over the same enrichment.

**Root cause:** the feed's rules (thread/draft semantics, sample linkage, surface ordering) belong to
three different domains, so the monolith gateway assembled them inline — twice in resolvers, once in a
util — and the copies drifted (three ordering rules, differing v2 handling, differing enrichment
defaults). The Relationship-Service walk exists only to discover ids that per-domain
by-related-resource queries can already supply.

### 1.3 Impact if not addressed

- **Divergence fossilized** — a naive port carries three accidental implementations of "the same" feed
  into two subgraphs; unifying later becomes a visible UI regression on two calibrated surfaces.
- **Reliability** — a thread whose parent discussion falls outside the walk crashes the whole product
  tab today (unguarded lookup); the walk's retirement breaks sourcing entirely if not replaced.
- **Performance** — serial ACL/discussion/sample fetches and an N+1 per-discussion reply loop on an
  interactive tab.
- **Security-adjacent** — the draft filter (an "ACL should do this" TODO) lives in the read path; losing
  or "fixing" it during port silently exposes draft discussion attachments.

### 1.4 Objectives

The cutover pattern is done when the following are recorded:
- One enrichment engine with an explicit per-surface policy table (source set, ordering, defaults, draft
  filter) replacing the three accidental implementations — behavioral parity **per surface**, pinned by
  fixtures.
- Sourcing moved to by-related-resource queries; any remaining walk usage quarantined behind one seam
  with a deletion point.
- The mandatory fixes (parallel fetches, guarded thread lookup, direct discussion client + batched
  replies) each recorded as accepted parity deviations.

## 2. What must be decided before build

- How each domain contributes its attachment set and where the metadata enrichment/rollup is computed.
- The parity target against the legacy `attachmentsWithMetaData` behaviour.
- **Draft decision:** [ADR-018 (draft)](./01-adr-attachments-enrichment.md) proposes owner-computed
  enrichment over a shared library with a per-surface policy table (Option A; federated per-domain lanes
  recorded as end-state) — status 🔴 Proposed, pending ratification. ACL is out of scope for this case
  (ADR-019 — see ADR-018's ACL note).

---

*This folder holds the problem brief (this file) + the draft decision ([01-adr-attachments-enrichment.md](./01-adr-attachments-enrichment.md)) + the story breakdown implementing it ([01-stories.md](./01-stories.md)) — the concrete story ids in each affected domain's be-04-stories.md, cross-referenced by pin-down.*
