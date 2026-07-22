# Prompt — Update an existing story by Epic + Story ID (Jira key unknown)

> **Use when:** you know the Story ID (e.g. `BOM-BE-E-01`) and which epic it lives under, but you do
> NOT know its Jira issue key/number — e.g. it was imported a while ago, or by someone else, and you
> just need to refresh its content from the current `.md`/CSV source. This is UPDATE-ONLY: if no
> matching issue is found in that epic, this prompt stops and asks you rather than creating one (use
> `push-one-story.md` instead if you actually want create-or-update behavior).
> **Prerequisite:** a Jira MCP server connected. Confirm with: *"List the Jira tools you currently
> have."*
> **Background reading:** [`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).
> **Content model:** the Jira description is Acceptance Criteria + a back-link, nothing else — full
> story detail stays on GitHub, linked not duplicated.

---

## Inputs you provide

| Placeholder | Meaning | Example |
|---|---|---|
| `<STORY_ID>` | The story's id as it appears in the source docs | `BOM-BE-E-01` |
| `<EPIC_NAME>` | Exact epic name/summary this story should be under | `Federate BreakDown Product` (backend) or `Federate BreakDown Product — Frontend` (FE) |
| `<PROJECT_KEY>` | Jira project key | `ENG` |
| `<GITHUB_ORG>/<GITHUB_REPO>` | This repo's GitHub org/name | `myorg/spark-migration` |

> **Note on epic names:** both epics are shared across ALL 8 domains — there is no per-domain epic.
> The domain is instead carried on the issue's Labels (e.g. `bom`, `product`) and in the Story ID's
> own prefix. Don't search for a domain-specific epic name; it won't exist.

---

## Prompt

```
Using the Jira tools, find and UPDATE (do not create) the Jira issue for <STORY_ID>.

1. Find the epic in <PROJECT_KEY> whose name/summary is exactly "<EPIC_NAME>". If more than one issue
   matches that name, list them and ask me which one before continuing.
2. Within that epic's children ONLY (issues linked to it via Epic Link/parent), search for one whose
   summary or description contains "<STORY_ID>" (typically in the form "[<STORY_ID>]" per this
   project's summary convention, e.g. "(BOM) @DgsTypeResolver for the 2 BOM interfaces [BOM-BE-A-04]").
3. If found: that is the target issue. Report its Jira key + current URL before changing anything.
4. If NOT found within that epic: STOP. Do not search other epics, do not create a new issue. Tell me
   the epic had no matching child and ask whether the story hasn't been imported yet (in which case
   use push-one-story.md to create it) or whether I have the wrong epic name.

Once the target issue is confirmed, pull the CURRENT source content for <STORY_ID>:
- Find its row in finalArtifacts/jira/<DOMAIN>.csv (derive <DOMAIN> from the Story ID's prefix — e.g.
  BOM-BE-E-01 → bom.csv; a FE id like BOM-FE-002 → the same domain's csv, frontend block). If the id
  isn't in that domain's CSV, also check output/complexStories/*/*.csv and
  output/analysis/out-of-scope-backlog.md §"Excluded from Jira" (may be deliberately excluded).
- Cross-check the Acceptance Criteria against output/analysis/<DOMAIN>/be-04-stories.md (search
  "### <STORY_ID>") — this is the fuller source; if the CSV's AC list and the .md's numbered AC list
  disagree (e.g. reworded since the CSV was last generated), the .md file wins and you should flag
  the discrepancy to me. Do NOT pull Current Behaviour/Target/Test Cases from the .md into the Jira
  description — those stay on GitHub, linked not duplicated; only the Acceptance Criteria and the
  back-link belong in the ticket.

Show me a diff: current Jira field values vs. the source content — Summary, Description (Acceptance
Criteria list + the "Full story:" link, rewritten as
"https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/output/analysis/<DOMAIN>/be-04-stories.md#<STORY_ID>",
plus "Domain overview: <URL>" if finalArtifacts/jira/confluence-page-map.csv has a row for <DOMAIN>),
Labels, Phase label, T-shirt-size label. STOP and wait for my approval before changing anything.

FORMATTING (same contract as every other Jira/Confluence prompt in this repo): preserve the numbered
Acceptance Criteria list and paragraph breaks, converted to this Jira's format — never flatten, strip,
reword, or drop any criterion.

After my approval, apply the update and report the Jira key, URL, and a short list of what changed
(e.g. "Description: 1 Acceptance Criterion reworded, GitHub link added; Labels: no change").
```

---
*Jira prompt — update-only, epic-scoped, Jira key unknown · output/prompts/jira/update-story-in-epic.md*
