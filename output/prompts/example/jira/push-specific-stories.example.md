# Example — Push a specific LIST of stories to Jira

> Worked example of [`output/prompts/jira/push-specific-stories.md`](../../jira/push-specific-stories.md)
> using real data. Values used: a hand-picked cross-domain list (`WATCHLIST-BE-B-01`,
> `WATCHLIST-BE-E-01`, `BOM-BE-B-01`) to show the "search every domain's CSV" behavior,
> `<PROJECT_KEY>` = `PROJ`, `<GITHUB_ORG>/<GITHUB_REPO>` = `myorg/spark-migration`.

---

## Step 1 — dry run (filled in)

```
Using the Jira tools, prepare (DO NOT CREATE YET) an import plan for exactly these story ids:

WATCHLIST-BE-B-01, WATCHLIST-BE-E-01, BOM-BE-B-01

For each id:
1. Find its row — search finalArtifacts/jira/{domain}.csv across all 8 domains (product, bom, claims,
   measurement, impression, productDetails, packaging, watchlist) for a matching Story ID; if not
   found there, check output/complexStories/*/*.csv, then
   output/analysis/out-of-scope-backlog.md §"Excluded from Jira" (deliberately not imported — a
   different team owns it). Tell me which file (or exclusion) each id came from.
2. Search Jira project PROJ for an existing issue carrying that Story ID — if found, plan
   an UPDATE; if not, plan a CREATE.
3. Find-or-create the epic named in the row's "Epic Link" column (reuse if it already exists from
   an earlier import).

Rules:
- The Description column is ALREADY minimal (Acceptance Criteria + a "Full story:" back-link) — pass
  it through as-is; do NOT add Current Behaviour, Target, or Test Cases from be-04-stories.md.
- REWRITE each id's "Full story:" line into a real URL:
  "Full story: https://github.com/myorg/spark-migration/blob/main/output/analysis/<domain>/be-04-stories.md#<id>"
  (derive <domain> from which CSV the row came from).
- ADD "Domain overview: <URL>" per id if finalArtifacts/jira/confluence-page-map.csv has a row for
  that id's domain; otherwise skip and tell me.
- FORMATTING: preserve the numbered Acceptance Criteria list and paragraph breaks, converting to this
  Jira's format — never flatten or strip it.
- For each id's "Depends On" list: if the target is also in THIS list, note the link to create
  after both exist. If the target is outside this list, search Jira for it by [bracket] id first
  (it may already exist from an earlier push); if not found, list as pending.

Output a table: Story ID | source file | create-or-update | epic | depends-on (in-list / found-in-
jira / pending). Then STOP and wait for my approval.
```

## Sample agent response

```
Resolved all 3 ids:
- WATCHLIST-BE-B-01 → finalArtifacts/jira/watchlist.csv
- WATCHLIST-BE-E-01 → finalArtifacts/jira/watchlist.csv
- BOM-BE-B-01 → finalArtifacts/jira/bom.csv

Searched Jira project PROJ — WATCHLIST-BE-B-01 already exists as PROJ-403 (imported earlier).
WATCHLIST-BE-E-01 and BOM-BE-B-01 are new.

| Story ID | source file | create/update | epic | depends-on |
|---|---|---|---|---|
| WATCHLIST-BE-B-01 | watchlist.csv | update | Federate BreakDown Product (PROJ-401) | — |
| WATCHLIST-BE-E-01 | watchlist.csv | create | Federate BreakDown Product (PROJ-401) | SPIKE-01 (pending — program spike, not a story); B-01 → WATCHLIST-BE-B-01 (found-in-jira: PROJ-403); PRODUCT-BE-E-00 (pending — cross-domain, not found in Jira) |
| BOM-BE-B-01 | bom.csv | create | Federate BreakDown Product (PROJ-401, reused) | — |

Confluence links: watchlist has a row in confluence-page-map.csv (link added to both watchlist
stories); bom does not yet (skipping the Domain overview line for BOM-BE-B-01, noting Confluence
hasn't been published for bom).

STOP — waiting for your approval before creating/updating anything.
```

## Step 2 — create/update, then link (filled in)

```
Looks good. Now create the new issues and update the existing ones per the plan, build a Story ID →
Jira key map for everything in this batch (including any matched-existing issues), create the
in-list dependency links, attempt the "found-in-jira" links, and report: the key map, links created,
and anything still pending.
```

## Sample agent response

```
Updated PROJ-403 (WATCHLIST-BE-B-01) — no field changes (already current).
Created PROJ-409 (WATCHLIST-BE-E-01) and PROJ-501 (BOM-BE-B-01).

Key map for this batch:
| Story ID | Jira key |
|---|---|
| WATCHLIST-BE-B-01 | PROJ-403 |
| WATCHLIST-BE-E-01 | PROJ-409 |
| BOM-BE-B-01 | PROJ-501 |

Links created (1): PROJ-403 blocks PROJ-409 (found-in-jira link).

Pending (2): PROJ-409's dependency on SPIKE-01 (program spike — not a Jira-linkable story in this
model; noted in the description's "Requires spike" line instead) and on PRODUCT-BE-E-00 (cross-domain,
product domain not yet imported).
```

---
*Worked example · output/prompts/example/jira/push-specific-stories.example.md*
