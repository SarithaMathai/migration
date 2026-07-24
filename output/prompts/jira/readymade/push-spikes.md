Using the Jira tools, prepare (DO NOT CREATE YET) an import plan from
finalArtifacts/jira/spikes.csv. Attach every spike to this epic: <EPIC_LINK>.

This CSV holds the program-wide research SPIKES: 8 Spike rows (Story IDs SPIKE-01, SPIKE-02, SPIKE-03,
SPIKE-04, SPIKE-05, SPIKE-06a, SPIKE-06b, SPIKE-07). Push this FIRST, before any domain, so every
domain story that depends on a SPIKE-xx can link to it. Ignore the Issue Type=Epic row in the CSV —
use the epic <EPIC_LINK> I gave above.

For EACH spike row, before you plan a create, check whether a Jira issue already exists carrying that
Story ID (search summary/description for the id in [brackets]). If it exists: plan an UPDATE. If not: a create.

Rules:
- Each Issue Type=Spike row -> a Spike issue under the epic <EPIC_LINK> (or a Story labelled "spike" if
  your project has no Spike issue type — tell me which it is before creating). Skip the Epic row.
- Map fields: Summary->summary, Description->description, T-shirt size->label "size-M",
  the Labels columns->labels (dgs-migration, all-domains, spike).
- Pass the Description through as-is (Summary / Decision to make / Intended steps). Do NOT summarize.
- Spikes have no "Depends On" — nothing to link here.

Output a table: Story ID | create-or-update | summary. Then STOP and wait for my approval.

---

Looks good. Now:
1. Create NEW spikes and UPDATE existing ones (per the plan), each under the epic <EPIC_LINK>.
2. Keep and report a map of Story ID -> Jira key for all 8 spikes — the domain pushes link to these
   keys, so I need them recorded.
3. Report: Story ID -> Jira key table, and confirm each spike is attached to the epic.
