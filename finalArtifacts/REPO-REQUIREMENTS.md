# What the repo needs — for Jira + Confluence push

> 🏷️ **Tags:** `dgs-migration` · `setup` — **Assembled:** 2026-07-24.
> **Target repo:** `https://github.com/target-corp/saritha-mathai-repositories-research`
> → `<GITHUB_ORG>` = `target-corp` · `<GITHUB_REPO>` = `saritha-mathai-repositories-research`

The push prompts don't just read the CSVs — they rewrite relative references into **GitHub blob URLs**
that must actually resolve. So the repo has to contain the source files those links point at, not only
the slim `finalArtifacts/`. This is the checklist.

## 1. Files/folders that MUST be in the repo

| Path | Why it's needed | Used by |
|---|---|---|
| `finalArtifacts/jira/spikes.csv` | Step-0 push unit — the 8 program spikes + shared epic | Jira |
| `finalArtifacts/jira/{domain}.csv` (×8) | Per-domain import (BE+FE stories, Acceptance Criteria + back-link) | Jira |
| `finalArtifacts/jira/all-stories.csv` | Whole-program import alternative | Jira |
| `output/analysis/{domain}/be-04-stories.md` (×8) | **Every Jira ticket's `Full story:` link points here** — the full story detail (Current Behaviour, Target, Test Cases) lives here, linked not copied | Jira |
| `finalArtifacts/summary/{domain}/FederatedGqlBreakDown-{domain}.md` (×8) | Source for each domain's Confluence breakdown page | Confluence |
| `finalArtifacts/summary/{domain}/story-dependency-graph-{domain}.md` (×8) | Source for each domain's FE-Readiness page | Confluence |
| `finalArtifacts/00-overview.md`, `00-sequencing.md`, `00-order-sequencing.md`, `00-external-dependencies.md`, `00-domain-rollout.md`, `00-dependency-map.md`, `00-cheatsheet.md`, `00-fe-unblock-plan.md` | Program-level Confluence pages | Confluence |
| `output/summary/Federated+Graphql+Stories+-+BreakDown.md` | Source for the "Breakdown — Overview" Confluence page | Confluence |
| `output/complexStories/{case}/00-overview.md` + `01-adr-*.md` (×9 cases) | Source for the "Complex Scenarios" Confluence page | Confluence |
| `finalArtifacts/jira/confluence-page-map.csv` | **Handoff file** — created by the Confluence prompts after publishing; the Jira prompts read it to add a "Domain overview:" link. Starts absent; publish Confluence first | both |

**Bottom line:** push the whole working tree, or at minimum **`finalArtifacts/` + `output/analysis/` +
`output/summary/` + `output/complexStories/` + `output/prompts/`**. The `output/analysis/**/be-04-stories.md`
files are the non-obvious must-have — Jira tickets are useless without them because the ticket body is
deliberately minimal and links out to that file for the full detail.

## 2. GitHub links — already wired to this repo

Every push prompt and runbook now hard-codes
`https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/...` (the old
`<GITHUB_ORG>/<GITHUB_REPO>` placeholder was replaced on 2026-07-24). Nothing to substitute at run time.

> **Check the default branch.** The links assume `blob/main/`. If this repo's default branch is
> `master` (or anything else), do a find-replace of `blob/main/` → `blob/<branch>/` across the prompts,
> or the links will 404.

## 3. Order of operations (end to end)

1. **Push the repo** with the folders in §1 (so the GitHub links resolve).
2. **Publish Confluence first** (so the Jira tickets can link back to domain pages):
   - Program pages (overview, sequencing, order-sequencing, external-dependencies) — run once each.
   - Per-domain breakdown + FE-readiness pages — one prompt per domain.
   - Each Confluence prompt appends a row to `finalArtifacts/jira/confluence-page-map.csv`.
3. **Push Jira**, in this order (see `jira-push-order.md`):
   - **Step 0 — `spikes.csv`** (the 8 program spikes) — so every `SPIKE-xx` dependency link resolves.
   - **Product** → Watchlist → Product Details → Measurement → Packaging → Claims → **BOM** →
     **Impression**. Product first (everyone depends on it), Impression last (needs product + bom).
   - Each domain: run the dry-run step, review, then create + link.

## 4. Prerequisites (integrations, not files)

- **Jira MCP** connection (Atlassian MCP / enterprise MCP / Copilot's Jira tools) with create + link
  permissions on the target project. Confirm with *"List the Jira tools you have."*
- **Confluence** write access to the **PPDE** space (MCP / plugin / connector). Confirm before running.
- If either is read-only, the prompts still work as **content-preparation** steps (they emit
  import-ready CSV / Confluence-ready structure for a manual paste).

---
*Repo requirements · assembled 2026-07-24 · target-corp/saritha-mathai-repositories-research.*
