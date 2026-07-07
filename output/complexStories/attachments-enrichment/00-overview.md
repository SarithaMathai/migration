# Complex Story — `attachmentsWithMetaData` enrichment (Product + Workspace)

> **Summary —** Build the Product / Workspace “attachments-with-metadata” feed from per-domain attachment contributions — no Relationship-Service walk.
> **Spike:** — *(read pattern applied at cutover, not a research spike)* · **Status:** Problem brief
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub story:** `SPARK-PROD-G01`/`G03` + `SPARK-WS-G01` (later phase)/`G03`

> **Migrates (source resolvers → this case):** product **FR `attachmentsWithMetaData`** (`SPARK-PROD-G01`) +
> the thin variants `attachments`/`attachmentsV3`/`attachmentSummary` (`SPARK-PROD-G03`); workspace
> **FR `attachmentsWithMetaData`** (`SPARK-WS-G01` (later phase)) + `attachmentsV3` (`SPARK-WS-G03` (later phase)). Fans out to per-domain
> attachment buckets (attachment, discussion, sample).

## 1. The problem (grounded in the code)

**What this read does.** The attachments tab on a product or workspace lists every file in one feed —
- files attached directly, files shared inside discussions, and files on samples — each enriched with who may see it and where it came from.
- Building that one list means reading three domains plus access control.

`Product.attachmentsWithMetaData` (~150 ln, `SPARK-PROD-G01`) and `WorkspaceV2.attachmentsWithMetaData`
(~75 ln, `SPARK-WS-G01` (later phase)) both do the **same shape** of work:

1. **Relationship Service** `searchByIds` → the resource subtree (attachments_v3, discussions, discussionThreads, samples).
2. partition into buckets → **hydrate attachments** (`getAttachmentsV3`, with ACL) per bucket.
3. batch **discussion / thread** attachments; product also folds in **sample** attachments.
4. **merge** the 5 (product) / 3 (workspace) sources.
5. **order** by `resource.type` rank (product=0, discussion=1, sample=2) then `createdAt DESC`.
6. **draft filter** — drop discussion attachments with no link / draft (carries a *"ACL should do this"* TODO).

- `SPARK-PROD-G03` / `SPARK-WS-G03` (later phase) (`attachments`, `attachmentsV3`, `attachmentSummary`) are thin variants over the same enrichment.
- **Why it's complex:** Relationship-Service traversal (being retired) + a multi-source merge + ordering + a draft-filter rule duplicated across two subgraphs.

## 2. What must be decided before build

- How each domain contributes its attachment set and where the metadata enrichment/rollup is computed.
- The parity target against the legacy `attachmentsWithMetaData` behaviour.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
