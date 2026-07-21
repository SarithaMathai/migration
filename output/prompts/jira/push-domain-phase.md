# Prompt — Push one PHASE of one domain to Jira

> **Use when:** you want just one phase letter (A–H) of one domain — e.g. "just BOM's Phase E stories"
> — instead of the whole domain (`push-domain-all-stories.md`) or a hand-picked id list
> (`push-specific-stories.md`). Useful for sprint-by-sprint import matching the phase build order
> (A→H), or re-pushing one phase after its stories changed.
> **Prerequisite:** a Jira MCP server connected. Confirm with: *"List the Jira MCP tools you currently
> have."*
> **Background reading:** [`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).
> **Phase reference:** [`output/summary/Federated+Graphql+Stories+-+BreakDown.md`](../../summary/Federated+Graphql+Stories+-+BreakDown.md)
> §"The migration phases (A→H)" — A=foundation/type-resolvers, B/C=reads, D=mutations, E=complex ops,
> F=federation, G=field-resolvers, H=entity-resolution. Per-domain phase counts:
> [`output/overview/02-story-domain-index.md`](../../overview/02-story-domain-index.md).

---

## Step 1 — dry run (no writes)

Replace `<DOMAIN>` (one of: `product, bom, claims, measurement, impression, productDetails, packaging,
watchlist`), `<PHASE>` (one letter, `A`–`H`), and `<PROJECT_KEY>`.

```
Using the Jira MCP tools, prepare (DO NOT CREATE YET) an import plan for Phase <PHASE> of the
<DOMAIN> domain only, from output/jira/<DOMAIN>.csv.

Filter: only rows where the "Phase" column = <PHASE> (backend rows use the letter directly, e.g.
"E"; there is no frontend-specific phase letter — frontend rows are Phase="FE" and are OUT of scope
for this prompt unless <PHASE> is literally "FE"). If Phase <PHASE> has zero rows for this domain
(check output/overview/02-story-domain-index.md's per-domain phase-count column first), tell me that
and stop rather than silently proceeding with an empty plan.

For EACH matching row, before you plan a create, check whether a Jira issue already exists carrying
that Story ID (search summary/description for the id in [brackets], or a custom field/label if your
project has one). If it exists: plan an UPDATE, not a duplicate create. If it doesn't: plan a create.

Rules:
- Attach every Story to the epic named in ITS OWN "Epic Link" column ("Federate BreakDown Product"
  for backend rows — this epic is shared across ALL domains, so also apply the domain label from the
  row's Labels column; do not create a per-domain epic).
- Map fields: Summary→summary, Description→description, T-shirt size→label "size-XS" (etc.), the
  three Labels columns→labels, Phase→label "phase-<PHASE>".
- Include the FULL detail in the CSV's Description column: Current Behaviour, Target, every numbered
  Acceptance Criterion, Test Cases, Depends On / Blocks (by story id AND name, never bare numbers),
  Parallelizable, Owner, Priority, Definition of Done. Don't drop or summarize any of it — fold
  anything with no matching Jira field into the description body and tell me which fields that was.
- FORMATTING: preserve paragraph breaks and markup (*emphasis*, **bold**, `code`, "- " bullets, "[ ]"
  checklists), converting to this Jira's description format — never flatten, strip, or reword.
- This phase's stories may depend on an EARLIER phase in the SAME domain that hasn't been pushed yet
  (e.g. a Phase E story's "Depends On" naming a Phase B story). Check each "Depends On" id against
  this batch first; if it's not in this batch, search Jira for it (already-pushed earlier phase); if
  not found there either, list it as "pending — push Phase <earlier-letter> first."
- See "How dependencies work" below if any of this is unclear before you plan the links.

Output a table: Story ID | create-or-update | epic | labels | depends-on (in-batch / found-in-jira /
pending-earlier-phase). Then STOP and wait for my approval.
```

## Step 2 — create/update, then link dependencies

```
Looks good. Now:
1. Create the new stories/spikes and update the existing ones per the plan, in Jira project
   <PROJECT_KEY>. Do not touch fields I didn't ask you to change on an existing issue.
2. Keep a map of Story ID → Jira key (created or matched-existing) for this batch.
3. For each row's "Depends On" ids: link in-batch ones directly; for found-in-jira ones, create the
   link (Blocks / is blocked by — the dependency is the blocker); leave pending-earlier-phase ones
   unlinked and listed for follow-up.
4. Report: Story ID → Jira key table, links created, and anything still pending (with which earlier
   phase unblocks it).
```

## How dependencies work (read this if the "Depends On" column is unclear)

- **Source of truth:** each domain's `output/analysis/<domain>/be-04-stories.md` has, per story, an
  explicit **`Depends on:`** line (what must land first) and sometimes a **`Blocks:`** line (what
  this one gates). The Jira CSV's "Depends On" column is a flattened copy of the same information —
  if the CSV value looks ambiguous, the `.md` file's prose next to that story is the tie-breaker.
- **Same-domain shorthand:** a bare id like `A-04` or `G-10` (no domain prefix) means "the story with
  that phase-letter+number in THIS SAME domain" (e.g. inside `bom.csv`, `A-04` means `BOM-BE-A-04`).
  A full id like `BOM-BE-A-04` appearing in another domain's CSV is a genuine cross-domain dependency.
- **Spike dependencies:** an id like `SPIKE-01` or `SPIKE-06a` is NOT a story — it's a program-wide
  research spike tracked in [`output/summary/Federated+Graphql+Stories+-+BreakDown.md`](../../summary/Federated+Graphql+Stories+-+BreakDown.md)
  §"Phase 0 — Program Spikes." A story depending on one is marked 🔴🔬 and is genuinely NOT startable
  until that spike's decision is ratified — check the spike's Status column before importing it as
  "ready," and say so in your dry-run output rather than treating it like a normal story dependency.
- **Cross-domain dependencies (the full list):** every cross-domain "Blocked by" edge in the whole
  program is pre-compiled in [`output/analysis/program/cross-domain-dependencies.md`](../../analysis/program/cross-domain-dependencies.md)
  — check there first instead of re-deriving it from scratch; it tells you which domain must federate
  first for an H-phase (entity resolution) or F-phase (federation) story to actually be startable.
- **Depends On vs. Blocks:** "Depends On" = what THIS story needs to exist/land first (an incoming
  edge). "Blocks" = what can't start until THIS story lands (an outgoing edge) — usually only noted
  on foundational stories (e.g. a domain's own `B-01` module scaffold, or `E-00` shared saga module)
  since almost every later story in that domain implicitly depends on it even when not listed row-by-
  row. When in doubt about an implicit dependency, check the domain's own breakdown page's "Migration
  Scope" or "Deployment Model" section for a note like "every story implicitly depends on B-01."

---
*Jira prompt — one phase of one domain · output/prompts/jira/push-domain-phase.md*
