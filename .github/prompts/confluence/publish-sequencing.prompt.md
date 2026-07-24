---
mode: agent
model: Claude Sonnet 4.5
description: "Publish the Migration Sequencing & Roadmap page (build order, per-domain step tables) to Confluence"
---

Publish `finalArtifacts/00-sequencing.md` as a single Confluence page — ONE page covering every
domain's build order, not split per-domain.

Follow the full rules in `output/prompts/confluence/publish-sequencing-claude-sonnet.md` — this
prompt is the short form; read that file for the complete formatting contract if anything here is
ambiguous. **This file has the most tabular data of any page in this program** — the per-domain
story-sequence tables run 15–80 rows each; verifying exact row counts matters more here than
anywhere else.

Target: parent page `${input:parentPage:Federation Graph Migration ▸ Program}`, title
`Migration Sequencing & Roadmap`.

1. Dry run: report a manifest — number of domain sections, total row count across ALL story-sequence
   tables, heading count. STOP for my approval.
2. Publish (create-or-update by exact title, never duplicate). Every domain section, every table row
   (including the long story-sequence tables), every status/gate icon (🟢🟡🟠🔴🔬⛔) preserved
   verbatim — no sampling, no truncating, no summarizing a long table. Rewrite relative repo links as
   GitHub links (`https://github.com/${input:githubOrgRepo:target-corp/saritha-mathai-repositories-research}/blob/main/<path>`).
3. Verify: re-open the page, confirm the row count of EVERY story-sequence table matches the source
   exactly — this is where silent truncation is most likely to hide on this page specifically.

Report the page URL and version number.
