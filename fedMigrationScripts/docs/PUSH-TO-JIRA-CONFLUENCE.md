# Pushing the migration artifacts to Jira & Confluence (via MCP)

These are **copy-paste prompts** for an agent (Claude Code, Claude Desktop, or GitHub Copilot) with a
Jira/Confluence MCP server or equivalent tool access — the **Atlassian MCP, your enterprise custom
MCP, or Copilot's own Jira/Confluence integrations**. The prompts only assume create/search/update/link
capabilities, not specific tool names. Run them one at a time, review the dry-run output, then let the
agent write.

**For Copilot users:** every prompt below has a matching `.prompt.md` file under `.github/prompts/`
(see [`output/prompts/README.md`](../../output/prompts/README.md)) written in Copilot's native
`${input:name:default}` format — use those directly with `/prompt-name` in Copilot Chat rather than
copy-pasting from here. This document is the shared reference both the Claude-flavored prompts
(`output/prompts/`) and the Copilot `.prompt.md` files are generated from.

## The three-tier model

```
GitHub (source of truth)  →  Confluence (curated planning docs)  →  Jira (actionable stories)
     output/analysis/            finalArtifacts/summary/               finalArtifacts/jira/
     be-04-stories.md            FederatedGqlBreakDown-*.md             {domain}.csv
     (full detail, never         story-dependency-graph-*.md            (Acceptance Criteria +
      published verbatim)        00-overview.md, 00-sequencing.md        back-links, never full detail)
```

- **GitHub is the source of truth.** `output/analysis/{domain}/be-04-stories.md` carries the complete
  story text — Current Behaviour, Target implementation, every Acceptance Criterion, Test Cases. Every
  other artifact (Confluence page, Jira ticket) **links back to it**, never re-copies it. If you find
  yourself pasting Current Behaviour or Target implementation prose into a Jira ticket or a Confluence
  page beyond what's already in the generated file, stop — that content belongs in GitHub, and the
  published artifact should link to it instead.
- **Confluence is the curated layer.** Program overview, sequencing, per-domain breakdowns, and the
  FE-readiness dependency graphs — see [`CONFLUENCE-INVENTORY.md`](../reference/CONFLUENCE-INVENTORY.md)
  for the complete page list. These pages are already trimmed for a human reader (that's the whole
  point of `finalArtifacts/` existing) — publish them as-is, formatting preserved exactly.
- **Jira is the actionable layer.** One ticket per story, description = **Acceptance Criteria only**
  plus links back to (a) the full story on GitHub and (b) that domain's Confluence breakdown page.
  Nothing else belongs in the ticket body — dependencies live in Jira's own link graph, not restated
  as prose.

> **Formatting is part of the contract.** The generated artifacts carry deliberate structure — tables,
> bold/italic emphasis, inline code, checklists, block quotes, mermaid diagrams. Every prompt below
> instructs the agent to **convert that structure to the target system's format, never to strip,
> flatten, or summarize it**. If your MCP accepts only plain text for a field, the markup is passed
> through as-is (readable), not removed.

> **Repo placeholder.** Every GitHub link in these prompts uses `https://github.com/<GITHUB_ORG>/<GITHUB_REPO>`.
> Replace `<GITHUB_ORG>/<GITHUB_REPO>` once, in your own copy of the prompt, with the real org/repo —
> never fabricate or guess a URL if you don't have the real one yet; leave the placeholder and flag it.

> **Prerequisite:** an Atlassian MCP server (or Copilot's built-in Jira/Confluence tools) is configured
> and authenticated to your site. Confirm with: *"List the Jira and Confluence tools you currently have."*

---

## 1. Confluence — publish the curated planning docs

**Full page list, titles, and parent structure:** [`CONFLUENCE-INVENTORY.md`](../reference/CONFLUENCE-INVENTORY.md).
**Source root:** `finalArtifacts/` (repo root, sibling of `output/`) — not `output/summary/` directly;
`finalArtifacts/` is the already-curated, already-trimmed copy meant for publishing.

Publish order: space home → program roll-ups (overview, then sequencing) → per-domain pages
(breakdown, then FE-readiness graph) → deep-dive tier and complex-case ADRs on request only.

### Prompt — publish the program overview + sequencing (2 pages, run once)

```
Using the Confluence tools you have, publish these two pages into space <SPACE_KEY> under the parent
page "Federation Graph Migration" (find by title; create if missing):

1. Title: "Spark → Federated GraphQL Migration — Program Overview"
   Body: finalArtifacts/00-overview.md
2. Title: "Migration Sequencing & Roadmap"
   Body: finalArtifacts/00-sequencing.md

FORMATTING AND CONTENT ARE THE CONTRACT — no data loss, no format loss:
- Every table stays a table (same columns/rows/cells, never flattened to a list or paragraph, never
  truncated or summarized "for brevity").
- Every heading keeps its exact level; sections stay in source order, none omitted.
- Bold, italic, inline code, and emoji/icons are preserved exactly where they appear.
- "- [ ]" checklist items become native task lists; "> " block quotes become quote/info panels.
- Fenced code blocks become code macros with the same language hint. A ```mermaid block becomes a
  code macro labeled "mermaid (render externally)" — keep the full diagram source, never replace it
  with a prose description.
- Story/domain IDs (e.g. PRODUCT-BE-B-01) stay as plain text — do not auto-convert to smart links.
- Any relative link to another repo file becomes a GitHub link:
  https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/<path> — never a local file path.

Create-or-update by exact title (update in place, new version, same page id — never duplicate).

Dry run first: title → parent → section-by-section manifest (table count, mermaid count, heading
count). STOP for my approval before writing. After I approve, publish and report each page's URL and
version number.
```

### Prompt — publish one domain's pages (breakdown + FE-readiness graph, repeat per domain)

```
Using the Confluence tools you have, publish these two pages for the <DOMAIN> domain into space
<SPACE_KEY>, under parent "Federation Graph Migration ▸ Domains ▸ <Domain Display Name>" (find or
create the domain parent under "Domains" first; this also identifies the space):

1. Title: "<Domain Display Name> — Federated GraphQL Breakdown"
   Body: finalArtifacts/summary/<DOMAIN>/FederatedGqlBreakDown-<DOMAIN>.md
2. Title: "<Domain Display Name> — FE Readiness"
   Body: finalArtifacts/summary/<DOMAIN>/story-dependency-graph-<DOMAIN>.md

Same formatting contract as the program-overview prompt above (tables stay tables, mermaid blocks
keep their source, GitHub links not local paths, no summarizing). The breakdown page has a
"## Backend" and a "## Frontend" section — publish BOTH on the SAME page, in source order; do not
split into separate pages.

Create-or-update by exact title. Dry run first (manifest of what you're about to convert), then STOP
for my approval before writing.

After publishing, APPEND a row to finalArtifacts/jira/confluence-page-map.csv (create it with header
"Domain,Breakdown Page URL,FE Readiness Page URL" if it doesn't exist yet):
<DOMAIN>,<breakdown page URL>,<FE readiness page URL>
This file is what the Jira publish prompts read to link each story back to its domain's Confluence
page — do not skip this step.
```

Domain display names: product→Product, bom→BOM, measurement→Measurement, packaging→Packaging,
impression→Impression, productDetails→Product Details, watchlist→Watchlist, claims→Claims.

### Prompt — publish a deep-dive page on request (PO review or comprehensive)

Only run this when a specific reader needs this depth — see
[`CONFLUENCE-INVENTORY.md`](../reference/CONFLUENCE-INVENTORY.md) §4 for when that is. These are
**not** part of the default publish set.

```
Using the Confluence tools you have, publish one page under "Federation Graph Migration ▸ Domains ▸
<Domain Display Name>" in space <SPACE_KEY>:

Title: "<Domain Display Name> — <PO Review|Comprehensive>"
Body: output/summary/<DOMAIN>/<DOMAIN>-<po-review|comprehensive>.md

Same formatting contract as above. Create-or-update by exact title. Dry run first, then STOP for my
approval.
```

### Prompt — publish a complex-case ADR on request

```
Using the Confluence tools you have, publish this page under "Federation Graph Migration ▸
Architecture ▸ Complex Cases" in space <SPACE_KEY>:

Title: (the ADR file's own H1 heading — read it first)
Body: output/complexStories/<CASE>/01-adr-<case>.md

Same formatting contract as above. Relative links inside this file to other repo files become GitHub
links (https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/<path>), never local paths. Create-or-
update by exact title. Dry run first, then STOP for my approval.
```

---

## 2. Jira — create the epics + stories from the CSV

**Source of truth for the import:** `finalArtifacts/jira/{domain}.csv` — one file per domain,
**combined**: the domain's **backend** stories (epic "Federate BreakDown Product", ids `*-BE-*`)
followed by its **frontend** stories (epic "Federate BreakDown Product — Frontend", ids `*-FE-*`).
Program-wide file: `finalArtifacts/jira/all-stories.csv` (all backend + the program spikes).

**Columns:** `Issue Type, Story ID, Summary, Epic Name, Epic Link, Phase, T-shirt size, Labels,
Labels, Labels, Parent Link, Depends On, External Dependency, Status, Description`.

**The Description column is intentionally minimal — Acceptance Criteria + a back-link, nothing else:**

```
*Acceptance Criteria:*
1. <criterion>
2. <criterion>

*Full story:* be-04-stories.md#<Story ID>
```

Do **not** try to pull in Current Behaviour, Target implementation, Test Cases, or Definition of Done
from anywhere else and paste them into the ticket — that detail is deliberately not in the CSV
because it lives on GitHub and would just go stale in two places at once. The ticket's job is "what
does done look like" (the AC) and "where do I go for the rest" (the links below), not a copy of the
implementation notes.

### Prompt — push ONE domain (backend + frontend), dry run first

Replace `<DOMAIN>` with one of: `product, bom, claims, measurement, impression, productDetails,
packaging, watchlist` — then repeat for the next domain.

```
Using the Jira tools you have, prepare (DO NOT CREATE YET) an import plan from
finalArtifacts/jira/<DOMAIN>.csv into Jira project <PROJECT_KEY>.

This CSV holds ONE domain, in two blocks:
- backend stories (Story IDs like <TOKEN>-BE-B-01) under the epic "Federate BreakDown Product";
- frontend stories (Story IDs like <TOKEN>-FE-001) under the epic
  "Federate BreakDown Product — Frontend".

For EACH row, before you plan a create, check whether a Jira issue already exists carrying that
Story ID (search summary/description for the id in [brackets], or a custom field/label if your
project has one). If it exists: plan an UPDATE (new description/fields), not a duplicate create.
If it doesn't: plan a create.

Rules:
- The CSV contains TWO Issue Type=Epic rows (backend + frontend). Reuse an existing epic with that
  exact Summary if one exists; otherwise plan to create it.
- Each Issue Type=Story row → a Story; each Issue Type=Spike row → a Spike (or a Story labelled
  "spike" if Spike isn't an available issue type — tell me which).
- Attach every Story to the epic named in ITS OWN "Epic Link" column.
- Map fields: Summary→summary, Description→description, T-shirt size→label "size-XS" (etc.), the
  three Labels columns→labels, Phase→label "phase-B" (frontend rows: Phase=FE → "phase-FE").
- The Description column is ALREADY minimal (Acceptance Criteria + a back-link) — pass it through
  as-is. Do NOT enrich it by pulling Current Behaviour, Target implementation, or Test Cases from
  be-04-stories.md; that content stays on GitHub, linked, not duplicated into the ticket.
- REWRITE the back-link before creating the issue: the CSV's "Full story:" line reads
  "be-04-stories.md#<Story ID>" (a relative path, correct inside the repo) — in the Jira description,
  expand it to a real URL:
  "Full story: https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/output/analysis/<DOMAIN>/be-04-stories.md#<Story ID>"
- ADD a second link line if finalArtifacts/jira/confluence-page-map.csv exists and has a row for
  <DOMAIN>: "Domain overview: <that row's Breakdown Page URL>". If the map file doesn't exist yet or
  has no row for this domain, skip this line and tell me Confluence hasn't been published for this
  domain yet (publish it first, or proceed without the cross-link and add it in a later re-sync).
- FORMATTING: the Description is multi-paragraph with light markup (*emphasis*, **bold**, `code`,
  numbered lists). Preserve paragraph breaks and convert markup to this Jira's description format
  (wiki markup or rich text). Do NOT collapse to one line, strip emphasis/code marks, reword, or
  summarize anything.
- The "Depends On" column lists other Story IDs. Don't resolve them to Jira keys yet — flag
  cross-domain ones (targets not in this CSV) separately; we link everything in step 2.

Output a table: Story ID | create-or-update | proposed issue type | epic | summary | labels |
depends-on | confluence-link-added(y/n). Then STOP and wait for my approval.
```

### Prompt — create/update, then link dependencies

```
Looks good. Now:
1. Find-or-create the two Epics for <DOMAIN>, then create NEW stories/spikes and UPDATE existing
   ones (per the plan), in Jira project <PROJECT_KEY>. Do not touch fields I didn't ask you to change
   on an existing issue beyond what the plan specified.
2. Keep a map of Story ID → Jira key (created or matched-existing).
3. For each row's "Depends On" ids, create a Jira issue link (Blocks / is blocked by; blocker =
   the dependency) using that map.
4. If a "Depends On" id is NOT in this CSV (cross-domain dependency), search Jira for an issue
   whose summary/description contains that id in [brackets]. Link it if found; if not found, list
   it under "pending links — import that domain, then rerun step 4."
5. Report: Story ID → Jira key table, links created, GitHub/Confluence links added, and any pending
   links.
```

> **Why link after creation:** the CSV references stories by **our IDs** (`BOM-BE-B-04`), not Jira
> keys — Jira keys don't exist until the issue is created. The agent builds the ID→key map on
> creation, then wires the "Depends On" links.

> **Domain-by-domain order tip:** import in the frontend wave order — watchlist → productDetails →
> measurement → packaging → bom → claims → product → impression — and the cross-domain "pending
> links" list stays near-empty (each domain's dependencies are mostly already imported).

Repeat both prompts per domain, or point at `finalArtifacts/jira/all-stories.csv` for a single
whole-program import (backend + program spikes only — frontend stories are per-domain-file only
today; there is no combined all-frontend file inside `finalArtifacts/`, only in `output/jira/`).

> **Complex cross-domain cases import SEPARATELY.** Each `output/complexStories/<case>/<case>.csv`
> holds that case's sub-tasks; import it **under its home stub story** (e.g. the techpack sub-tasks
> nest under `PRODUCT-BE-E-03`). These are deliberately **not** in `all-stories.csv` to avoid
> double-counting.

> **Excluded stories:** a small number of stories are documented in `be-04-stories.md` but
> deliberately **not** imported to Jira (different team owns the work — see
> `JIRA_EXCLUDED_STORIES` in `fedMigrationScripts/generatescripts/generate_jira.py` and
> `output/analysis/out-of-scope-backlog.md` §"Excluded from Jira" for the current list and reasons).
> If a story you expected to see in the CSV is missing, check there before assuming a generation bug.

---

## 3. Handy variations

- **All stories at once:** point the Jira prompt at `finalArtifacts/jira/all-stories.csv` (all
  backend + program spikes) and tell it to create one Epic per `Epic Name` value.
- **Re-sync after edits:** re-run the generators (`python fedMigrationScripts/generatescripts/generate_all.py
  bom product`), then re-run the Confluence prompt — it UPDATES existing pages by title. For Jira,
  only push *new/changed* rows (ask the agent to search by our ID label first and skip issues that
  already exist).
- **A specific story only, or a hand-picked list:** see the standalone prompts in
  [`output/prompts/jira/`](../../output/prompts/jira/) (`push-one-story.md`,
  `push-specific-stories.md`, `push-domain-phase.md`, `update-story-in-epic.md`) — same field-mapping
  and link contract as above, scoped narrower.

> **Tip:** keep `finalArtifacts/jira/confluence-page-map.csv` (Domain → Confluence page URLs) and a
> Story ID ↔ Jira key map somewhere durable so re-syncs update instead of duplicating. The agent can
> maintain the Jira key map as a small `jira-key-map.csv` alongside it.
