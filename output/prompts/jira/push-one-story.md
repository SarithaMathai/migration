# Prompt — Create or update ONE story in Jira

> **Use when:** you only need a single story pushed or refreshed — e.g. a story changed after a
> staleness fix, or you're spot-checking the pipeline before a full domain push.
> **Prerequisite:** a Jira MCP server connected. Confirm with: *"List the Jira MCP tools you currently
> have."*
> **Background reading:** [`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).

---

## Prompt

Replace `<STORY_ID>` (e.g. `PRODUCT-BE-D-01`), `<DOMAIN>` (its domain, e.g. `product`), and
`<PROJECT_KEY>`.

```
Using the Jira MCP tools:

1. Open output/jira/<DOMAIN>.csv and find the row where Story ID = <STORY_ID>. If it isn't in that
   file, also check output/complexStories/*/*.csv (complex-case sub-tasks) and tell me which file
   it came from.

2. Search Jira project <PROJECT_KEY> for an existing issue carrying this Story ID (in its summary or
   description, e.g. "[<STORY_ID>]", or a custom field/label if this project has one).

3a. If it EXISTS: show me a diff — current Jira field values vs the CSV row's values (Summary,
    Description, all Labels, Phase, T-shirt size, Depends On) — and STOP for my approval before
    updating anything.

3b. If it does NOT exist: show me the fields you'd set (Issue Type, Summary, Description, Epic
    Link — find-or-create the epic named in the row's "Epic Link" column, Labels, Phase label,
    T-shirt-size label) and STOP for my approval before creating.

Rules:
- Include the FULL Description content: Current Behaviour, Target, every numbered Acceptance
  Criterion, Test Cases, Depends On / Blocks (story id + name), Parallelizable, Owner, Priority,
  Definition of Done. Don't drop or summarize any of it — fold anything with no matching Jira
  field into the description body and tell me which fields that was.
- FORMATTING: preserve paragraph breaks, bold/italic/inline-code/bullets/checklists — convert
  markup to this Jira's format, don't strip or flatten it.
- If the row's "Depends On" names another story, search for that story's existing Jira key too
  (same [bracket] search) and propose the link; if not found, note it as pending.

After my approval, make the change and report the Jira key + URL.
```

---
*Jira prompt — one story create/update · output/prompts/jira/push-one-story.md*
