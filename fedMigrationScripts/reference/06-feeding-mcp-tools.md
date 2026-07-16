# Feeding these artifacts to MCP tools (Jira, Confluence)

These artifacts are structured so an MCP-enabled assistant can create Jira issues and Confluence pages
directly, with minimal prompting. This page maps each artifact to its destination and field mapping.

---

## Artifact → destination

| Artifact | MCP destination | Use |
|----------|-----------------|-----|
| `be-04-stories.md` (per story) | **Jira** create issue | One Jira Story per `###` story block |
| `be-04-stories-index.yaml` | **Jira** bulk create | Iterate the list; one issue per entry |
| `../STORIES-INDEX.md` + `../index.yaml` | **Jira** Epics + **Confluence** rollup | All stories, all domains, with complexity |
| `be-04-po-summary.md` | **Confluence** page | "Migration approach & sprint plan" |
| `be-03-schema-analysis.md` (§Migration Approach) | **Confluence** page | Architecture/approach doc |
| `be-05-attribute-inventory.md` | **Confluence** page (tables) | Field-level inventory & complexity |
| `be-02-resolver-analysis.md` | **Confluence** page | Engineering spec / appendix |

---

## Story → Jira field mapping

From each story's YAML front-matter + body:

| Jira field | Source |
|------------|--------|
| Summary | `title` (YAML) / the `###` heading |
| Issue type | Story |
| Epic link | `epic` (in `be-04-stories-index.yaml`) — one epic per domain |
| Description | Body sections: *Current Behaviour* + *Target DGS Implementation* + *Files to Create/Modify* |
| Acceptance Criteria | the *Acceptance Criteria* numbered list (paste as a checklist) |
| Story points / complexity | `complexity` (Low/Medium/High/Very High) → map to your point scale |
| Labels | `labels` (YAML): `dgs-migration`, `{domain}`, `{query|mutation|field}` |
| Links: "is blocked by" | `depends_on` (YAML) — each is another story ID |
| Component / subgraph | `target_dgs` (index) |
| Sub-tasks / test plan | the *Test Cases* checklist |

> **Do not** copy day-ranges into Jira from stories — stories carry complexity only. Day-ranges (for
> capacity planning) live in `be-04-po-summary.md` and are explicitly "AI-estimated, confirm in refinement".

## Confluence page composition (suggested)

A single domain Confluence space page can be assembled as:
1. **Approach** ← `be-03-schema-analysis.md` §Migration Approach + `be-04-po-summary.md` §What Are We Building.
2. **Field inventory** ← `be-05-attribute-inventory.md` (all three tables).
3. **Story inventory** ← `be-04-stories-index.yaml` rendered as a table (id, phase, complexity, deps).
4. **Risks & decisions** ← `be-04-po-summary.md` §Key Risk Areas + §Decisions Required.
5. **Sequencing** ← `be-04-po-summary.md` §Recommended Sprint Sequencing + Dependency Map.

## Cross-domain rollup
`../STORIES-INDEX.md` is the program-level view: every story across all domains with domain, phase,
category, complexity, deps, and blocked-by. Feed it to Confluence for a portfolio page, or to Jira to
create the four domain Epics and link stories.
