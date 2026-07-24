Using the Jira tools, prepare (DO NOT CREATE YET) an import plan from
finalArtifacts/jira/packaging.csv. Attach every story to this epic: <EPIC_LINK>.

This CSV holds the Packaging domain: backend stories (Story IDs like PKG-BE-B-01) and frontend
stories (Story IDs like PKG-FE-001). Ignore the two Issue Type=Epic rows in the CSV — use the
epic <EPIC_LINK> I gave above for ALL stories instead.

For EACH story row, before you plan a create, check whether a Jira issue already exists carrying that
Story ID (search summary/description for the id in [brackets]). If it exists: plan an UPDATE, not a
duplicate create. If it doesn't: plan a create.

Rules:
- Each Issue Type=Story row -> a Story under the epic <EPIC_LINK>. Skip the Issue Type=Epic rows.
- Map fields: Summary->summary, Description->description, T-shirt size->label "size-XS" (etc.),
  the three Labels columns->labels, Phase->label "phase-B" (frontend rows: Phase=FE -> "phase-FE").
- The Description column is ALREADY minimal (Acceptance Criteria + a "Full story:" back-link) — pass
  it through as-is. Do NOT enrich it with Current Behaviour, Target, or Test Cases from be-04-stories.md.
- REWRITE the "Full story:" line from a relative path into a real URL:
  "Full story: https://github.com/target-corp/saritha-mathai-repositories-research/blob/main/output/analysis/packaging/be-04-stories.md#<Story ID>"
- ADD a "Domain overview:" link if finalArtifacts/jira/confluence-page-map.csv has a row for packaging;
  otherwise skip it and tell me Confluence hasn't been published for this domain.
- FORMATTING: keep the Description's numbered Acceptance Criteria a numbered list; preserve paragraph
  breaks; convert markup to this Jira's description format. Do NOT collapse, strip, reword, or summarize.
- The "Depends On" column lists other Story IDs. Don't resolve them to Jira keys yet — flag any that
  target another domain or a SPIKE-xx (not in this CSV) separately; we link everything in step 2.

Output a table: Story ID | create-or-update | summary | labels | depends-on |
confluence-link-added(y/n). Then STOP and wait for my approval.

---

Looks good. Now:
1. Create NEW stories and UPDATE existing ones (per the plan), each under the epic <EPIC_LINK>. Do not
   touch fields I didn't ask you to change on an existing issue beyond what the plan specified.
2. Keep a map of Story ID -> Jira key (created or matched-existing).
3. For each row's "Depends On" ids, create a Jira issue link (Blocks / is blocked by; blocker = the
   dependency) using that map.
4. If a "Depends On" id is NOT in this CSV (cross-domain like PRODUCT-BE-E-00, or a SPIKE-xx), search
   Jira for an issue whose summary/description contains that id in [brackets]. Link it if found; if
   not, list it under "pending links — import that domain (or spikes.csv) first, then rerun step 4".
5. Report: Story ID -> Jira key table, links created, GitHub/Confluence links added, pending links.
