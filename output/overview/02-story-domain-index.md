# Story / Domain Index

> One map: every domain, its story count and phase mix, and a direct link into every artifact that
> domain has — analysis, complex-case involvement, Jira CSV, PO summary. Use this to find "where does
> X live" without hunting through folders.
> **Counts verified against `output/jira/all-stories.csv` (209 rows: 201 Story + 7 Spike + 1 Epic) on 2026-07-18 — reconciles with `output/summary/00-program-overview.md`.**

---

## Per-domain artifact map

| Domain | Stories | Phases (A·B·C·D·E·F·G·H) | Analysis folder | Jira CSV | PO summary |
|---|---|---|---|---|---|
| **Product** | 69 | 0·11·5·18·5·8·16·6 | [analysis/product/](../analysis/product/) | [jira/product.csv](../jira/product.csv) | [be-04-po-summary.md](../analysis/product/be-04-po-summary.md) |
| **BOM** | 37 | 2·7·5·5·1·2·15·0 | [analysis/bom/](../analysis/bom/) | [jira/bom.csv](../jira/bom.csv) | [be-04-po-summary.md](../analysis/bom/be-04-po-summary.md) |
| **Packaging** | 23 | 0·6·1·9·1·1·5·0 | [analysis/packaging/](../analysis/packaging/) | [jira/packaging.csv](../jira/packaging.csv) | [be-04-po-summary.md](../analysis/packaging/be-04-po-summary.md) |
| **Measurement** | 20 | 0·5·2·7·1·1·3·1 | [analysis/measurement/](../analysis/measurement/) | [jira/measurement.csv](../jira/measurement.csv) | [be-04-po-summary.md](../analysis/measurement/be-04-po-summary.md) |
| **Claims** | 20 | 0·5·2·5·1·0·5·2 | [analysis/claims/](../analysis/claims/) | [jira/claims.csv](../jira/claims.csv) | [be-04-po-summary.md](../analysis/claims/be-04-po-summary.md) |
| **Product Details** | 12 | 0·1·1·5·1·1·3·0 | [analysis/productDetails/](../analysis/productDetails/) | [jira/productDetails.csv](../jira/productDetails.csv) | [be-04-po-summary.md](../analysis/productDetails/be-04-po-summary.md) |
| **Watchlist** | 13 | 0·3·1·2·1·2·4·0 | [analysis/watchlist/](../analysis/watchlist/) | [jira/watchlist.csv](../jira/watchlist.csv) | [be-04-po-summary.md](../analysis/watchlist/be-04-po-summary.md) |
| **Impression** | 7 | 0·2·0·1·0·1·3·0 | [analysis/impression/](../analysis/impression/) | [jira/impression.csv](../jira/impression.csv) | [be-04-po-summary.md](../analysis/impression/be-04-po-summary.md) |
| **TOTAL** | **201** | 2·40·17·52·11·16·54·9 | — | [jira/all-stories.csv](../jira/all-stories.csv) | — |

Each domain folder also has: `be-01-schema-inventory.md` → `be-02-resolver-analysis.md` →
`be-03-schema-analysis.md` (+ `be-03-schema.graphql`) → `be-04-stories.md` (the stories themselves,
full AC + Test Cases) → `be-04-stories-index.yaml` (machine-readable) → `be-05-attribute-inventory.md`.

## Complex cases — which domains each one touches

| Case | Domains involved | Folder |
|---|---|---|
| `non-atomic-write-saga` | product (builds it) · bom, claims, measurement, packaging, productDetails, watchlist (consume it) | [complexStories/non-atomic-write-saga/](../complexStories/non-atomic-write-saga/) |
| `techpack` | product (host, facade) · claims (H-02 pairing) · attachment/discussion/sample/construction (later-phase contributors) | [complexStories/techpack/](../complexStories/techpack/) |
| `partner-drop-undrop-write` | product | [complexStories/partner-drop-undrop-write/](../complexStories/partner-drop-undrop-write/) |
| `notRemovable-undroppable-partners` | product · workspace (later phase) | [complexStories/notRemovable-undroppable-partners/](../complexStories/notRemovable-undroppable-partners/) |
| `components-and-counts-rollups` | product · workspace (later phase) | [complexStories/components-and-counts-rollups/](../complexStories/components-and-counts-rollups/) |
| `attachments-enrichment` | bom · workspace (later phase) | [complexStories/attachments-enrichment/](../complexStories/attachments-enrichment/) |
| `polymorphic-type-resolution` | bom, product · sample, search (later phase) | [complexStories/polymorphic-type-resolution/](../complexStories/polymorphic-type-resolution/) |
| `cross-domain-association` | product | [complexStories/cross-domain-association/](../complexStories/cross-domain-association/) |

## Program-wide (cross-domain) artifacts

| Artifact | What it is |
|---|---|
| [analysis/program/cross-domain-dependencies.md](../analysis/program/cross-domain-dependencies.md) | Every `Blocked by:` edge in the program, one table |
| [analysis/program/fe-00-executive-summary.md](../analysis/program/fe-00-executive-summary.md) … `fe-11` | Frontend program docs, numbered reading order (`fe-08` = frontend story source of truth) |
| [analysis/schemaAnalysis/00-cross-domain-field-inventory.md](../analysis/schemaAnalysis/00-cross-domain-field-inventory.md) | Which fields hydrate across domains, federation recommendation per field |
| [analysis/aclResearch/00-acl-usage-inventory.md](../analysis/aclResearch/00-acl-usage-inventory.md) | Every ACL call site, Mid-Request ACL Update (ADR-019) classification |
| [analysis/out-of-scope-backlog.md](../analysis/out-of-scope-backlog.md) | Deferred items — later-phase domain twins, session gaps — tracked outside Jira |
| [summary/00-program-overview.md](../summary/00-program-overview.md) | Generated program totals/effort/risk table (this index's numeric source) |
| [summary/01-implementation-plan-1BE-1FE.md](../summary/01-implementation-plan-1BE-1FE.md) | Team lanes, sprint milestones |
| [summary/02-project-plan.md](../summary/02-project-plan.md) | Story-by-story build order per domain |

## Reverse lookup — "I have a story id, where's its full text"

Story ids follow `<TOKEN>-BE-<phase>-<NN>`. Map the token to a domain folder, then search that domain's
`be-04-stories.md` for a `### <ID>` heading:

| Token | Domain |
|---|---|
| `PRODUCT` | product |
| `BOM` | bom |
| `CLAIM` | claims |
| `MST` | measurement |
| `PKG` | packaging |
| `PDTL` | productDetails |
| `WATCHLIST` | watchlist |
| `IMPRESSION` | impression |

Frontend story ids are `<TOKEN>-FE-<NNN>` — full text lives in
[analysis/program/fe-08-frontend-stories.md](../analysis/program/fe-08-frontend-stories.md), not in the
per-domain folders.

---

## Regeneration

Re-derive the counts table above with:
```bash
python3 -c "
import csv, re
from collections import defaultdict
with open('output/jira/all-stories.csv', encoding='utf-8') as f:
    rows = [r for r in csv.DictReader(f) if r['Issue Type']=='Story']
by_domain = defaultdict(list)
for r in rows:
    m = re.match(r'([A-Z]+)-BE-', r['Story ID'])
    if m: by_domain[m.group(1)].append(r['Story ID'])
for tok, ids in sorted(by_domain.items()):
    phases = defaultdict(int)
    for sid in ids:
        pm = re.search(r'-BE-([A-H])-', sid)
        if pm: phases[pm.group(1)] += 1
    print(tok, len(ids), dict(sorted(phases.items())))
"
```
Run after any `generate_all.py` pass that changes story counts.

---
*Story/domain index · output/overview/02-story-domain-index.md*
