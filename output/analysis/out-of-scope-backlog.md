# Out-of-Scope Backlog

> **Generated:** 2026-07-18 · **Purpose:** one place listing every item deliberately deferred while doing
> the Phase-H split, complex-case story authoring, and dependency/sequencing verification — so nothing
> flagged along the way gets silently lost. Not imported to Jira; not counted against any story total.
> Each row names why it's deferred, what it depends on, and a rough priority hint.

## Already known — later-phase domains (not phase-1 scope)

| Item | Source | Why out of scope | Depends on | Priority hint |
|---|---|---|---|---|
| Discussion domain slice (TechPack `H-02`) | techpack | `plm-discussion` subgraph not in phase-1 scope | plm-discussion | P2 — revisit when discussion domain is scheduled |
| Attachment domain slice (TechPack `H-01`) | techpack | `plm-attachment` subgraph not in phase-1 scope | plm-attachment | P2 |
| Sample domain slice (TechPack `H-03`) | techpack | `plm-sample` subgraph not in phase-1 scope | plm-sample | P2 |
| Construction domain slice (TechPack `H-05`) | techpack | no construction subgraph scheduled yet | construction subgraph (none exists) | P3 — stays blocked until one exists |
| `WORKSPACE-BE-G-02`/`G-04` (components-and-counts-rollups twin) | components-and-counts-rollups | workspace domain later-phase | plm-workspace | P2 — owes ADR-014 pin-downs 3, 8 when authored |
| `WORKSPACE-BE-G-05` (notRemovable-undroppable-partners twin) | notRemovable-undroppable-partners | workspace domain later-phase | plm-workspace | P2 — inherits the 10-pin-down contract unchanged |
| `WORKSPACE-BE-E-01` (partner-drop-undrop-write twin) | partner-drop-undrop-write | workspace domain later-phase | plm-workspace, `PRODUCT-BE-E-00` | P2 — reuses the participant contract + WriteSaga, no second design round |
| `WORKSPACE-BE-G-01`/`G-03` (attachments-enrichment twin) | attachments-enrichment | workspace domain later-phase | plm-workspace | P2 — owes ADR-018 pin-down 6 |
| `SAMPLE-BE-A-04`/`SAMPLE-BE-G-02` (polymorphic-type-resolution) | polymorphic-type-resolution | sample domain later-phase | plm-sample | P2 — inherits pin-downs 3, 4, 6 |
| `SEARCH-BE-B-01`/`SEARCH-BE-C-02` (polymorphic-type-resolution) | polymorphic-type-resolution | search domain later-phase | plm-elastic-search | P2 — inherits pin-down 5 + Option D end-state |
| `SAMPLE-BE-E-01`/`E-02` (non-atomic-write-saga) | non-atomic-write-saga | sample domain later-phase | plm-sample, `PRODUCT-BE-E-00` | P2 — adopts WriteSaga unchanged, no new decision (pin-down 8) |
| Discussion `Resource` union, product `SPARK_Categories` cross-ref (polymorphic-type-resolution) | polymorphic-type-resolution | out-of-scope dispatch sites, adopt playbook in their own stories | `BOM-BE-A-05`'s conformance gate | P3 — `PRODUCT-BE-G-04` exists but isn't yet cross-referenced to the shared gate |

## Found during this session — genuine gaps, not yet authored

| Item | Source | Why out of scope | Depends on | Priority hint |
|---|---|---|---|---|
| Shared `associate(...)` component build story (cross-domain-association) | cross-domain-association (ADR-011) | `PRODUCT-BE-D-01`/`D-02`/`D-04` each reference routing through the shared component, but no story builds the component itself as its own deliverable | none — could land now | P1 — same shape as `PRODUCT-BE-E-00`; recommend authoring before/alongside whichever of D-01/D-02/D-04 ships first |
| ADR-019 (Mid-Request ACL Update) wiring into `BOM-BE-G-08`–`G-13` | polymorphic-type-resolution (ADR-017 pin-down 9) | the 6 downstream-token material/impression loaders (trim/wash/fabric/fabricSpec/combination/search-targeting) haven't had their per-variant stories' ACs updated with the Mid-Request ACL Update line, unlike product's stories which got this treatment | `BOM-BE-A-05` (conformance gate, done) | P1 — mechanical, same pattern already applied across 6 product/domain files this session |
| `PRODUCT-BE-G-04` (`SPARK_Categories` 12-case union) not cross-referenced to `BOM-BE-A-05`'s shared conformance gate | polymorphic-type-resolution | exists as a normal dispatcher story, ADR-017 names it as an out-of-scope site that should adopt the playbook, but no AC yet ties it to the gate | `BOM-BE-A-05` | P2 |
| `BOM-BE-S-01` spike-closure decision | non-atomic-write-saga | the spike's three open questions are now answered by ADR-013 + `PRODUCT-BE-E-00`; the spike story is flagged superseded in its own body but not formally closed/removed — same question applies to any other now-redundant per-domain spike stories not audited in this pass | none | P3 — housekeeping, not blocking; a program-level decision on whether superseded spikes get removed or just flagged |
| `PRODUCT-BE-D-01`/`D-02`/`D-04`'s (cross-domain-association) `Depends on:` not wired to `PRODUCT-BE-E-00` | cross-domain-association | D-02's pin-down 2 defers non-atomicity/compensation to `SPIKE-01` (now `PRODUCT-BE-E-00`), but none of D-01/D-02/D-04 declare it as a `Depends on:` — may be correct (a lighter compensating call inside `associate(...)` may not need full saga machinery) or may be an oversight | `PRODUCT-BE-E-00` | P2 — needs a judgment call once the shared component (above) is actually designed |

## Excluded from Jira — different team owns the work

> Unlike the sections above, these stories are **fully documented and remain in their domain's
> `be-04-stories.md`** — they are real, estimable, phase-1-scoped work, just not this program's Jira import.
> Excluded via `JIRA_EXCLUDED_STORIES` in `generate_jira.py`, so the exclusion is enforced by the generator,
> not a manual CSV edit — re-running `generate_jira.py` will never accidentally re-include them.

| Item | Source | Why out of scope | Depends on | Priority hint |
|---|---|---|---|---|
| `PRODUCT-BE-D-15` `addProductRule` | product rules admin | Rules-**write** ownership sits with a different team; only the `get*`/`search*` rules reads (`B-10`, `B-11`, `C-05`, `getProductRules`, `getProductRulesById`, `getAllAvailableRules`) are in this program's Jira scope for product | none | P3 — informational; pick up in the owning team's own backlog |
| `PRODUCT-BE-D-16` `updateProductRule` | product rules admin | Same rules-write ownership exclusion as `D-15` | none | P3 |
| `PRODUCT-BE-D-17` `deleteProductRule` | product rules admin | Same rules-write ownership exclusion as `D-15` | none | P3 |

## Generated-output staleness

> **Regenerated and verified current** (as of this doc's last edit) — `output/summary/*` (all merged
> `FederatedGqlBreakDown-{domain}.md`/`.docx` pages, `01-implementation-plan-1BE-1FE.*`,
> `02-project-plan.md`), `output/jira/*.csv` (all domain CSVs + `all-stories.csv`), and all 8
> `output/complexStories/<case>/<case>.csv` files have been generated for real via
> `python fedMigrationScripts/generatescripts/generate_all.py` — not dry-run tested, actually run — and the
> old orphaned `FederatedGqlBreakDown-BE-*`/`-FE-*` and `01-implementation-plan-2BE-2FE.*` files were
> removed. `output/analysis/*/fe-{domain}-breakdown.md` co-located copies were refreshed in the same run.
> **Two independent review passes** (separate from the authoring work) caught and fixed several real
> defects post-regeneration: a wrong `Parent Link` in `non-atomic-write-saga.csv` (the shared-module case's
> CSV nested every domain's rows under one domain's stub instead of each domain's own —
> `output/complexStories/generate.py`'s `home_stub()` logic — plus a follow-on bug in the fix itself, a
> malformed `SAMPLE-BE-E-E-02` id from an incorrect shorthand-expansion regex, caught and fixed in the same
> pass), stale `F-01`–`F-08`/`MST-BE-F-02` prose references left over from the Phase H rename — found across
> three separate waves as each pass's own fix surfaced the next: `generate_all.py`'s hardcoded
> cross-domain-blockers table (wave 1), 5 lines of prose in `product/be-04-stories.md` — a Phases-Overview
> table missing its Phase H row, an ownership map, and 2 other lines (wave 2, caught by the second review
> pass), and finally a manual full sweep of every domain's `be-04-po-summary.md` (wave 3, not covered by
> either automated review) which found 4 more stale `product/be-04-po-summary.md`/`claims/`/`measurement/`
> references to the same renamed ids, plus separately **11 references across 7 domains' po-summary files
> to G-phase stories removed earlier in the session** (`G-16`/`G-12`/`G-05`/`G-03`/`G-04`/`G-06`, each
> domain's own now-manually-tracked bug-fix/test-coverage story) — all now corrected. Every domain's own
> genuinely-still-internal `F-01`/`F-02` (bom, impression, measurement, packaging, productDetails,
> watchlist all have their own unrenamed internal Phase-F stories, distinct from product's renamed ones)
> was deliberately left untouched. `claims`'s and `measurement`'s own phase-header tables and mermaid
> diagrams (which genuinely did have renamed ids — `CLAIM-BE-F-01/F-02` → `H-01/H-02`, `MST-BE-F-02` →
> `MST-BE-H-01`) and `output/complexStories/techpack/00-overview.md` + `01-adr-techpack.md` (8 locations
> describing the pre-rename `F-01`–`F-09` chain) were also found and fixed in this same wave — the ADR is
> a primary, actively-linked reference doc, worth keeping current. **Deliberately left un-fixed** (an
> earlier, separate task's own explicit scope decision, not re-opened here):
> `output/analysis/federation-review/05-backend-impact.md`, `07-story-validation-and-sequencing.md`,
> `08-risks-assumptions-questions.md` still cite `PRODUCT-BE-F-13`/`CLAIM-BE-F-01`/`CLAIM-BE-F-02` by their
> pre-rename ids — flagged then, still flagged now, still not fixed; a future pass should decide whether to
> update them or archive them as historical review artifacts. A merged-page heading-level
> bug (`## Backend`/`## Frontend` colliding with the nested page's own demoted title instead of nesting
> under it), Phase H missing from the phases glossary/table, a nondeterministic "Critical path" line
> (unsorted set iteration — now sorted at both call sites, verified stable across separate process runs and
> multiple `PYTHONHASHSEED` values), and one story (`BOM-BE-G-15`) that was miscategorized as a bug-fix/test
> story and wrongly deleted alongside a genuinely test-shaped story — restored, including its risk-register
> and summary-count references. **Regeneration was re-run after all fixes** — `output/summary/`,
> `output/jira/`, and `output/complexStories/*/*.csv` on disk now reflect every fix above.

| Item | Where | Status |
|---|---|---|
| `fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md` | reference docs | still describes `02-adr-noacl-*.md` as an artifact type (retired) and doesn't mention `01-stories.md`/`generate.py` (both now real) — needs a manual doc pass, not auto-fixed by regeneration |
| `fedMigrationScripts/skills/oneStopDoc-generation/SKILL.md` | skills doc | still references the old `FederatedGqlBreakDown-BE-{domain}` filename pattern (pre-merge) — needs a manual doc pass |
| `fedMigrationScripts/generatescripts/generate_breakdown.py`'s `DOMAIN_OWNERS` dict | generate_breakdown.py | still labeled `BE-1`/`BE-2`/`FE-1`/`FE-2` per-domain, describing the retired 2BE+2FE model; feeds `generate_jira.py` Owner metadata and `generate_project_plan.py` — reassigning it to the 1BE+1FE (or future N-engineer) model is a real decision, not a mechanical rename — flagged inline in the file's own comment |

## Notes on severity

Nothing above blocks regeneration — every item is either a later-phase domain (correctly deferred by the
program's own phasing) or a scoped, nameable gap that can be picked up as its own follow-up without
touching what's already built. The two P1 items (the `associate(...)` component build story, and the
6-site ADR-019 wiring in bom's material stories) are the closest to "should probably happen soon" since
they're mechanical, low-risk, and directly analogous to work already done elsewhere this session.
