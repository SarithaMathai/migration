# Pushing the migration stories to Jira & Confluence (via MCP)

These are **copy-paste prompts** for an agent (Claude Code / Claude Desktop) with a Jira/Confluence MCP
server connected — the **Atlassian MCP or your enterprise custom MCP**; the prompts only assume
create/search/update/link capabilities, not specific tool names. Run them one at a time, review the dry-run
output, then let it write.

> **Formatting is part of the contract.** The generated artifacts carry deliberate structure — multi-paragraph
> descriptions, tables, bold/italic emphasis, inline code, checklists, block quotes, status emoji. Every prompt
> below instructs the agent to **convert that structure to the target system's format, never to strip, flatten,
> or summarize it**. If your MCP accepts only plain text for a field, the markup is passed through as-is
> (readable), not removed.

> **Repo:** `https://github.com/XXX`. In the **published Jira/Confluence** content, any
> reference to a repo article (a domain page, a `complexStories/<case>`, an ADR) must be a **GitHub link into
> that repo** — never a local file path (readers can't open your filesystem). The generated breakdown pages
> already emit GitHub links; keep them, and add the repo URL when you cite a source.

> **Prerequisite:** an Atlassian MCP server is configured and authenticated to your site
> (e.g. `atlassian` / `mcp-atlassian`, exposing `jira_create_issue`, `jira_search`, `jira_link_issues`,
> `confluence_create_page`, `confluence_update_page`, or their equivalents). Confirm with:
> *"List the Jira and Confluence MCP tools you currently have."*

---

## 1. Jira — create the epics + stories from the CSV

**Source of truth:** `output/jira/{domain}.csv` — one file per domain, **combined**: the domain's
**backend** stories (epic "Federate BreakDown Product", ids `*-BE-*`) followed by its **frontend**
stories (epic "Federate BreakDown Product — Frontend", ids `*-FE-*`). Program-wide files:
`output/jira/all-stories.csv` (all backend + the program spikes) and
`output/jira/all-frontend-stories.csv` (all frontend). Columns everywhere:
`Issue Type, Story ID, Summary, Epic Name, Epic Link, Phase, T-shirt size,
Labels, Labels, Labels, Parent Link, Depends On, Status, Description`.

### Prompt — push ONE domain (backend + frontend), dry run first

Replace `<DOMAIN>` with one of: `product, bom, claims, measurement, impression, productDetails,
packaging, watchlist` — then repeat the same prompt for the next domain.

```
Using the Jira MCP tools, prepare (DO NOT CREATE YET) an import plan from
output/jira/<DOMAIN>.csv into Jira project <PROJECT_KEY>.

This CSV holds ONE domain, in two blocks:
- backend stories (Story IDs like <TOKEN>-BE-B-01) under the epic "Federate BreakDown Product";
- frontend stories (Story IDs like <TOKEN>-FE-001) under the epic
  "Federate BreakDown Product — Frontend".

Rules:
- The CSV contains TWO Issue Type=Epic rows (backend + frontend). For each: if an epic with that
  exact Summary already exists in <PROJECT_KEY> (created by an earlier domain's import), REUSE it —
  do not create a duplicate. Otherwise plan to create it.
- Each Issue Type=Story row → a Story; each Issue Type=Spike row → a Spike (or a Story labelled
  "spike" if Spike isn't an available issue type in this project — tell me which).
- Attach every Story to the epic named in ITS OWN "Epic Link" column (backend stories → backend
  epic, frontend stories → frontend epic).
- Map fields: Summary→summary, Description→description, T-shirt size→a label like "size-XS",
  the three Labels columns→labels, Phase→a label like "phase-B" (frontend rows have Phase=FE →
  label "phase-FE").
- FORMATTING: the Description is multi-paragraph (blank-line separated sections such as *Current
  Behaviour:*, *Target:*, *Acceptance Criteria:*) with light markup (*emphasis*, **bold**, `code`,
  "- " bullets, [ ] checklist items). Preserve the paragraph breaks and convert the markup to this
  Jira's description format (wiki markup or rich text). Do NOT collapse it to one line, strip
  emphasis/code marks, or reword anything.
- Do NOT invent fields the project doesn't have; list any you had to drop.
- The "Depends On" column lists other Story IDs (e.g. "B-01" or "PRODUCT-BE-B-01").
  Don't resolve them yet — we'll link after creation. Most targets are in THIS csv; a few
  frontend stories depend on ANOTHER domain's stories (e.g. IMPRESSION-FE-001 → BOM-BE-B-01) —
  flag those rows in the plan.

Output a table: Story ID | proposed issue type | epic | summary | labels | depends-on.
Then STOP and wait for my approval.
```

### Prompt — create, then link dependencies

```
Looks good. Now:
1. Find-or-create the two Epics, then create all Stories/Spikes, in Jira project <PROJECT_KEY>.
2. Keep a map of Story ID (e.g. BOM-BE-B-04, BOM-FE-002) → created Jira key (e.g. PROJ-123).
3. For each row's "Depends On" IDs, create a Jira issue link of type "Blocks"/"is blocked by"
   (blocker = the dependency, blocked = the dependent) using that map.
4. If a "Depends On" id is NOT in this CSV (cross-domain dependency), jira_search for an issue
   whose summary contains that id in [brackets] — it was imported with its own domain. Link it if
   found; if not found (that domain not yet imported), list it under "pending links — import
   <that domain> then rerun step 4".
5. Report the Story ID → Jira key table, the links created, and any pending links.
```

> **Why link after creation:** the CSV references stories by **our IDs** (`BOM-BE-B-04`), not Jira keys —
> Jira keys don't exist until the issue is created. The agent builds the ID→key map on creation, then wires
> the "Depends On" links. This is also why the docs cross-reference by ID, not URL.

> **Domain-by-domain order tip:** import in the frontend wave order — watchlist → productDetails →
> measurement → packaging → bom → claims → product → impression — and the cross-domain "pending links"
> list stays near-empty (each domain's dependencies are mostly already imported).

Repeat both prompts per domain, or point at `output/jira/all-stories.csv` + `output/jira/all-frontend-stories.csv`
for a single whole-program import.

> **Complex cross-domain cases import SEPARATELY.** Each `output/complexStories/<case>/<case>.csv` holds that
> case's sub-tasks; import it **under its home stub story** (e.g. the techpack sub-tasks nest under
> `PRODUCT-BE-E-03`). These are deliberately **not** in `all-stories.csv` to avoid double-counting — see
> [`fedMigrationScripts/reference/SPIKE-ADR-LIFECYCLE.md`](../reference/SPIKE-ADR-LIFECYCLE.md).

---

## 2. Confluence — publish the breakdown & PO pages

**Source:** `output/summary/{domain}/FederatedGqlBreakDown-BE-{domain}.md` (backend breakdown) and
`output/summary/{domain}/FederatedGqlBreakDown-FE-{domain}.md` (frontend breakdown), one folder per domain under `output/summary/`.
They are already Confluence-safe (no relative links). (PO-review deep-dives exist only after a
`generate_all.py --full` run, under `output/summary/{domain}/`.)

### Prompt — create/update pages by name

```
Using the Confluence MCP tools, publish these pages into space <SPACE_KEY> under the parent page
"Federation Graph Migration ▸ Domains" (find the parent by title; create it if missing):

- Title: "BOM — Federated GraphQL Breakdown (Backend)"
  Body: the markdown in output/summary/bom/FederatedGqlBreakDown-BE-bom.md
- Title: "BOM — Federated GraphQL Breakdown (Frontend)"
  Body: the markdown in output/summary/bom/FederatedGqlBreakDown-FE-bom.md
- Title: "Product — Federated GraphQL Breakdown (Backend)"
  Body: output/summary/product/FederatedGqlBreakDown-BE-product.md
- Title: "Product — Federated GraphQL Breakdown (Frontend)"
  Body: output/summary/product/FederatedGqlBreakDown-FE-product.md

Rules:
- FORMATTING — convert Markdown to Confluence storage format faithfully and completely:
  - tables stay tables (same columns/rows — never flattened to text), headings keep their levels,
    bold/italic/inline-code/links/emoji are preserved, "- [ ]" checklists become task lists,
    "> " block quotes become quote/info panels.
  - fenced code blocks become code macros; a ```mermaid block becomes a code macro labelled
    "mermaid (render externally)" — do not drop the diagram source.
  - do NOT summarize, reword, reflow, or omit any section; the page must read exactly like the file.
- If a page with that exact title already exists in the space, UPDATE it (new version) instead of
  creating a duplicate; otherwise create it under the parent.
- These docs reference stories by ID (e.g. PRODUCT-BE-F-01) and other pages by name — leave those as text.
  Do NOT try to convert them to links.
- After publishing, give me the page URLs.
```

### Prompt — scoped first load: the 8 selected modules + their overview breakdown (custom MCP)

The **first wave**: the Selected Modules overview breakdown plus the eight module breakdown pages —
no PO reviews, ADRs, or complex cases yet. Written for a **custom enterprise MCP**: it names no tool;
the agent discovers and uses whatever Confluence create/search/update capability it has.

```
You are publishing the first wave of our migration documentation to Confluence space <SPACE_KEY>
using the Confluence tools you have (list them first; then proceed autonomously).

PAGES (9) — create under a parent page "Federation Graph Migration" (find by title; create if missing):

1. Title: "Federated GraphQL Stories — Breakdown (Selected Modules)"
   Body: output/summary/Federated+Graphql+Stories+-+BreakDown_custom.md
   (the overview breakdown for the 8 modules below — make it the parent's first child)
2–9. One page per module, under a child parent "Domains", titled
   "<Domain> — Federated GraphQL Breakdown", from
   output/summary/<domain>/FederatedGqlBreakDown-BE-<domain>.md, for exactly these 8:
   product, bom, claims, productDetails, packaging, watchlist, measurement, impression
   (display names: Product, BOM, Claims, Product Details, Packaging, Watchlist,
   Measurement, Impression).

RULES
- FORMATTING IS THE CONTRACT: convert Markdown to Confluence storage format faithfully —
  tables stay tables (same rows/columns), headings keep levels, bold/italic/inline-code/emoji
  preserved, "- [ ]" checklists become task lists, "> " quotes become quote panels, fenced code
  blocks become code macros (a ```mermaid block becomes a code macro — keep the source).
  Never summarize, reword, reflow, or drop a section.
- Update by EXACT title if the page exists (new version); never create a duplicate.
- Story IDs (SPARK-…) stay plain text. Repository file references become GitHub links into
  https://github.com/XXX — never a local path.
- Dry-run first: list title → source → parent → create-or-update, then STOP for my approval.
  After I approve, publish and report each page's URL and version number.

Not in scope for this run: the remaining 5 domains, PO reviews, ADRs, complex-case pages, and the
All Domains page (output/summary/Federated+Graphql+Stories+-+BreakDown.md — add it alongside #1,
titled "Federated GraphQL Stories — Breakdown (All Domains)", if I say so; the program overview
output/summary/00-program-overview.md joins in a later wave the same way).
```

### Prompt — publish the architecture decision records and complex-case designs

```
Using the Confluence MCP tools, publish these under the parent page
"Federation Graph Migration ▸ Architecture" in space <SPACE_KEY> (create the parent if missing),
with the same formatting rules as above (tables stay tables; nothing summarized or reworded):

- Title: "ADR-012 — Non-Atomic Write Failure Strategy"            Body: adrs/ADR-012-non-atomic-write-failure-strategy.md
- Title: "ADR-013 — Partner Drop/Undrop Write Orchestration"      Body: adrs/ADR-013-partner-drop-undrop-write-orchestration.md
- Title: "ADR-014 — Cross-Domain Association & Hydration"         Body: adrs/ADR-014-cross-domain-association-hydration.md
- Title: "ADR-015 — Polymorphic Type Resolution Playbook"         Body: adrs/ADR-015-polymorphic-type-resolution-playbook.md
- One page per complex case: title from the case's 00-overview.md H1, body = that file
  (output/complexStories/<case>/00-overview.md), under a "Complex Cases" child parent.

Relative links inside these files point at repo files — rewrite them as GitHub links into the repo
(see the repo note at the top of this document); never leave a local relative path in a published page.
Update by exact title if the page exists. Report the page URLs.
```

> **Optional — link Confluence ↔ Jira:** once both exist, *"On each domain's breakdown page, add a Jira
> issues macro (or a link) filtered to label `dgs-migration` AND label `{domain}` so the live story status
> shows on the page."*

---

## 3. Handy variations

- **One domain only:** replace the file list with just that domain's two breakdown pages (BE + FE).
- **All stories at once:** point the Jira prompt at `output/jira/all-stories.csv` (all backend + program
  spikes) plus `output/jira/all-frontend-stories.csv` (all frontend) and tell it to create one Epic per
  `Epic Name` value.
- **Re-sync after edits:** re-run the generators
  (`python fedMigrationScripts/generatescripts/generate_all.py bom product`), then re-run the Confluence
  prompt — it UPDATES existing pages by title. For Jira, only push *new/changed* rows (ask the agent to
  `jira_search` by our ID label first and skip issues that already exist).

> **Tip:** keep a persistent mapping (our Story ID ↔ Jira key ↔ Confluence page URL) somewhere durable so
> re-syncs update instead of duplicate. The agent can maintain it in a small `jira-confluence-map.csv`.
