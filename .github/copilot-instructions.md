# Migration docs repo — GitHub Copilot instructions

## What this repository is

This is the **documentation and artifact-generation repo** for the Spark → Federated GraphQL
migration (8 phase-1 domains: product, bom, measurement, packaging, impression, productDetails,
watchlist, claims). It is not the application codebase — the actual DGS subgraph implementations live
in separate repos (see `fedMigrationScripts/copilot-poc/` for per-subgraph Copilot setups used there).

## The three-tier documentation model

```
GitHub (source of truth)       →  Confluence (curated planning docs)  →  Jira (actionable stories)
output/analysis/                  finalArtifacts/summary/                finalArtifacts/jira/
be-04-stories.md (full detail:    FederatedGqlBreakDown-*.md             {domain}.csv
Current Behaviour, Target,        story-dependency-graph-*.md            (Acceptance Criteria + a
every AC, Test Cases)             00-overview.md, 00-sequencing.md        back-link, nothing else)
```

- **GitHub is the source of truth.** Never duplicate full story detail into Confluence or Jira —
  every published artifact links back to `output/analysis/{domain}/be-04-stories.md` instead.
- **Confluence is the curated layer.** `finalArtifacts/` is the already-trimmed publishing set — the
  complete page list is [`fedMigrationScripts/reference/CONFLUENCE-INVENTORY.md`](../fedMigrationScripts/reference/CONFLUENCE-INVENTORY.md).
- **Jira is the actionable layer.** One ticket per story, description = Acceptance Criteria + links
  back to GitHub and Confluence — never Current Behaviour/Target/Test Cases.

## Publishing — use the prompts, don't improvise the rules

Every publish task (Confluence or Jira) has a ready-made prompt under `.github/prompts/confluence/`
or `.github/prompts/jira/` — invoke with `/prompt-name` in Copilot Chat. Each short Copilot prompt
points at a fuller reference in `output/prompts/{confluence,jira}/` and
[`fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md`](../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md)
— read the fuller version if a rule is ambiguous rather than guessing.

**Hard rules that apply to every publish, Confluence or Jira:**
- **Formatting is the contract.** Tables stay tables, headings keep their level, mermaid diagrams
  keep their full source — never summarize, flatten, reword, or drop a section "for brevity."
- **Create-or-update by exact title/label — never duplicate.** Search first, always.
- **Dry run, then stop for approval, then write.** No publish prompt writes without an explicit human
  confirmation of the dry-run plan.
- **Relative repo links become real links** — GitHub blob URLs
  (`https://github.com/<GITHUB_ORG>/<GITHUB_REPO>/blob/main/<path>` — replace the placeholder with
  the real org/repo) or, where a Confluence page already exists for the target, a link to that live
  page. Never leave a local file path in a published artifact.
- **Never fabricate a URL.** If you don't have the real GitHub org/repo or a Confluence page doesn't
  exist yet, say so and leave the placeholder rather than guessing.

## Regenerating the artifacts (before publishing)

The `finalArtifacts/` and `output/` trees are generated, not hand-authored — if you edit
`output/analysis/{domain}/be-04-stories.md` or `output/analysis/program/fe-08-frontend-stories.md`,
regenerate before publishing:

```
python fedMigrationScripts/generatescripts/generate_all.py            # everything
python fedMigrationScripts/generatescripts/generate_all.py bom        # one domain
```

Never hand-edit a generated file (`finalArtifacts/**`, `output/summary/**`, `output/jira/**`,
`output/analysis/program/fe-0[0-9,1]*.md`) — the next regeneration will silently overwrite it. Fix
the source instead (`be-04-stories.md`, `fe-08-frontend-stories.md`, or the generator script itself).

## Conventions

- Write documentation **point by point — bullets, never paragraphs**.
- Story ids: `<TOKEN>-BE-<PHASE>-<NN>` (backend, phase A–H) or `<TOKEN>-FE-<NNN>` (frontend).
- Domain tokens: PRODUCT, BOM, MST (measurement), PKG (packaging), IMPRESSION, PDTL (productDetails),
  WATCHLIST, CLAIM.
