# Prompt — Push ALL stories for one domain to Jira

> **Use when:** you want every backend + frontend story for one domain created (or updated) in Jira in
> one pass. Fill in `<DOMAIN>` and `<PROJECT_KEY>`, run the dry-run prompt first, review its output
> table, then run the second prompt to actually create/update and link dependencies.
> **Prerequisite:** a Jira MCP server connected (Atlassian MCP or your enterprise custom MCP). Confirm
> with: *"List the Jira MCP tools you currently have."*
> **Background reading (rules this prompt assumes):** [`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).

---

## Step 1 — dry run (no writes)

Replace `<DOMAIN>` with one of: `product, bom, claims, measurement, impression, productDetails,
packaging, watchlist`. Replace `<PROJECT_KEY>` with your Jira project key.

```
Using the Jira MCP tools, prepare (DO NOT CREATE YET) an import plan from
output/jira/<DOMAIN>.csv into Jira project <PROJECT_KEY>.

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
- Map fields: Summary→summary, Description→description, T-shirt size→label "size-XS" (etc.),
  the three Labels columns→labels, Phase→label "phase-B" (frontend rows: Phase=FE → "phase-FE").
- Include the FULL detail already in the CSV's Description column and don't drop any of it:
  Current Behaviour, Target, Acceptance Criteria (every numbered item), Test Cases, Depends On /
  Blocks (by story id AND name, never bare numbers), Parallelizable, Owner, Priority, Definition
  of Done. If the target Jira field for one of these doesn't exist, keep it inline in the
  description rather than dropping it, and tell me which fields you had to fold in this way.
- FORMATTING: the Description is multi-paragraph with light markup (*emphasis*, **bold**, `code`,
  "- " bullets, [ ] checklists). Preserve paragraph breaks and convert markup to this Jira's
  description format (wiki markup or rich text). Do NOT collapse to one line, strip emphasis/code
  marks, reword, or summarize anything.
- The "Depends On" column lists other Story IDs. Don't resolve them to Jira keys yet — flag
  cross-domain ones (targets not in this CSV) separately; we link everything in step 2.

Output a table: Story ID | create-or-update | proposed issue type | epic | summary | labels |
depends-on. Then STOP and wait for my approval.
```

## Step 2 — create/update, then link dependencies

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
5. Report: Story ID → Jira key table, links created, and any pending links.
```

---
*Jira prompt — push all stories for one domain · output/prompts/jira/push-domain-all-stories.md*
