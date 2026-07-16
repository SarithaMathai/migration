# Skill 06 — Consumption artifacts (Confluence + Jira)  *(new in Pipeline 2.0)*

> **Runs after** skills 01–05 have produced `finalOutput/{domain}/01..05`.
> **Outputs:** `finalOutput/confluence/{domain}.md` (PO page) + the Jira artifacts
> (`finalOutput/jira/{domain}.csv`, `{domain}-stories.md`, refreshed `all-stories.csv`).
> **Purpose:** turn the per-domain analysis into **copy-paste-ready** outputs for the three audiences.

The `01..05` files are the **source of truth / implementation layer**. This skill adds a thin
**consumption layer** on top — it does not change the analysis, it reformats it per audience.

| Audience | Artifact | Format |
|----------|----------|--------|
| Product Owner / stakeholders | `confluence/{domain}.md` + `confluence/00-portfolio.md` | Markdown (paste into Confluence) |
| Engineer creating tickets | `jira/{domain}.csv` (bulk) + `jira/{domain}-stories.md` (per-issue) | CSV + Markdown |
| Implementing engineer | `{domain}/be-04-stories.md` + `{domain}/be-02-resolver-analysis.md` | Markdown (already produced by 02/04) |

## A. Jira artifacts — just run the generator

`finalOutput/jira/generate.py` is **domain-agnostic**: it auto-discovers every
`finalOutput/*/be-04-stories-index.yaml`. After a new domain's `01..05` exist, run:

```
python finalOutput/jira/generate.py
```

It (re)writes `{domain}.csv`, `{domain}-stories.md`, and the combined `all-stories.csv`. No code change
per domain. The CSV column contract (do not change without updating `jira/README.md`):

`Issue Type, Story ID, Summary, Epic Name, Epic Link, Phase, Complexity, Story point estimate,
Labels, Labels, Labels, Depends On, Description`

- One **Epic** row per domain (from the index `epic:`), then one **Story** row per `stories[]` entry.
- `Description` is pulled from the matching `### {id}` block in `be-04-stories.md` (so write good story
  bodies in skill 04); stories with no dedicated block fall back to their summary + a pointer.
- `Labels` = `dgs-migration`, `{domain}`, `{type}`. `Story point estimate` maps complexity
  (Low 2 / Medium 3 / High 5 / Very High 8) — flagged "confirm in refinement".

**Prereq for clean output:** the domain's `be-04-stories-index.yaml` must list **every** story with
`id, summary, phase, category, complexity, depends_on`, and `totals.story_count` must equal the number
of `stories[]` entries (skill 04 completion check). The generator counts the entries, not the totals.

## B. Confluence page — assemble, don't re-derive

Create `confluence/{domain}.md` by **copying** the already-written PO content so facts can't drift.
Required outline (same for every domain — see `confluence/product.md` as the template):

1. Title + "paste into Confluence" note + links to the deep-dive files and the Jira CSV.
2. **What are we building?** ← `{domain}/be-04-po-summary.md §What Are We Building` (+ the ACL note).
3. **Scope** table ← `be-04-po-summary.md §Migration Scope`.
4. **Effort by phase** table ← `be-04-po-summary.md §Story Summary by Phase` (label AI-estimated).
5. **Key risks** ← `be-04-po-summary.md §Key Risk Areas`.
6. **Decisions required** (with owners) ← `be-04-po-summary.md §Decisions Required`.
7. **Migration approach (summary)** — 3–5 lines distilled from `be-03-schema-analysis.md §Migration Approach`,
   with a link to the full section.
8. **Field-inventory signal** ← `be-05-attribute-inventory.md §Table 3` summary (1 short paragraph).
9. **Sequencing & capacity** ← `be-04-po-summary.md`.

Then add the domain's row to `confluence/00-portfolio.md` (program totals + sequencing).

## C. Refresh the program rollups

After adding a domain, update the program-level counts so they stay consistent:
`STORIES-INDEX.md` §1 table, `index.yaml` (`domains:` + `totals:`), `README.md` §3 table, and
`confluence/00-portfolio.md`. **Counts must equal the enumerated `stories[]` entries**, not a separately
maintained tally (a past undercount put `by_complexity`/`story_count` out of sync with `by_phase`).

## Completion criteria
- [ ] `python finalOutput/jira/generate.py` runs clean; `{domain}.csv` row count = stories + 1 (epic).
- [ ] Every story row has a non-empty `Description` and an `Epic Link`.
- [ ] `{domain}-stories.md` `##`-block count = the domain's story count.
- [ ] `confluence/{domain}.md` follows the outline; numbers match `be-04-po-summary.md`.
- [ ] Program rollups (STORIES-INDEX / index.yaml / README / portfolio) updated and internally consistent.
