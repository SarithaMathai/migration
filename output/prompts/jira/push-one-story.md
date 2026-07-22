# Prompt — Create or update ONE story in Jira

> **Use when:** you only need a single story pushed or refreshed — e.g. a story changed after a
> staleness fix, or you're spot-checking the pipeline before a full domain push.
> **Prerequisite:** a Jira MCP server connected. Confirm with: *"List the Jira tools you currently
> have."*
> **Background reading:** [`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).
> **Content model:** the Jira description is Acceptance Criteria + a back-link, nothing else — full
> story detail stays on GitHub, linked not duplicated.

---

## Prompt

Replace `<STORY_ID>` (e.g. `PRODUCT-BE-D-01`), `<DOMAIN>` (its domain, e.g. `product`),
`<PROJECT_KEY>`, and `<GITHUB_ORG>/<GITHUB_REPO>`.

```
Using the Jira tools:

1. Open finalArtifacts/jira/<DOMAIN>.csv and find the row where Story ID = <STORY_ID>. If it isn't in
   that file, also check output/complexStories/*/*.csv (complex-case sub-tasks) and
   output/analysis/out-of-scope-backlog.md §"Excluded from Jira" (it may be deliberately excluded —
   different team owns the work) and tell me which applies.

2. Search Jira project <PROJECT_KEY> for an existing issue carrying this Story ID (in its summary or
   description, e.g. "[<STORY_ID>]", or a custom field/label if this project has one).

3a. If it EXISTS: show me a diff — current Jira field values vs the CSV row's values (Summary,
    Description, all Labels, Phase, T-shirt size, Depends On) — and STOP for my approval before
    updating anything.

3b. If it does NOT exist: show me the fields you'd set (Issue Type, Summary, Description, Epic
    Link — find-or-create the epic named in the row's "Epic Link" column, Labels, Phase label,
    T-shirt-size label) and STOP for my approval before creating.

Rules:
- The Description column is ALREADY minimal (Acceptance Criteria + a "Full story:" back-link) — pass
  it through as-is. Do NOT enrich it with Current Behaviour, Target implementation, or Test Cases from
  be-04-stories.md; that content stays on GitHub, linked not duplicated.
- REWRITE the "Full story:" line into a real URL:
  "Full story: https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/output/analysis/<DOMAIN>/be-04-stories.md#<STORY_ID>"
- ADD "Domain overview: <URL>" if finalArtifacts/jira/confluence-page-map.csv has a row for <DOMAIN>;
  otherwise skip and tell me Confluence hasn't been published for this domain yet.
- FORMATTING: preserve the numbered Acceptance Criteria list and paragraph breaks — convert markup to
  this Jira's format, don't strip or flatten it.
- If the row's "Depends On" names another story, search for that story's existing Jira key too
  (same [bracket] search) and propose the link; if not found, note it as pending.

After my approval, make the change and report the Jira key + URL.
```

---
*Jira prompt — one story create/update · output/prompts/jira/push-one-story.md*
