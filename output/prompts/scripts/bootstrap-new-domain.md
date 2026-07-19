# Prompt — Bootstrap a brand-new domain (e.g. `sample`) from scratch

> **Use when:** a later-phase domain (sample, discussion, attachment, workspace, search) is starting its
> own migration analysis for the first time. **Read this before running anything** — unlike the other
> two prompts in this folder, this is NOT a single mechanical regeneration. `generate_all.py` and its
> sibling scripts only regenerate roll-ups (breakdown pages, Jira CSVs, PO summaries) from an
> ALREADY-AUTHORED `be-04-stories.md`; they do not invent a new domain's story content from nothing.
> Creating a new domain is a two-stage process: (1) author the upstream analysis, (2) wire the domain
> into the generator scripts' domain lists, (3) run the regeneration pipeline.

---

## Stage 1 — author the upstream analysis (the real work, not a script)

This stage produces the same 5 files every existing domain has under `output/analysis/{domain}/`. There
is no generator for this stage — it requires reading the domain's actual current resolver code and
writing the analysis by hand (with AI assistance), the same way the 8 phase-1 domains were originally
authored.

```
I'm starting the migration analysis for a new domain: <NEW_DOMAIN> (e.g. "sample").

Help me produce, in output/analysis/<NEW_DOMAIN>/, the same 5 files every existing domain has —
use output/analysis/measurement/ as your structural reference (it's a mid-complexity domain, a good
template) for format and section headings, but derive the actual CONTENT from <NEW_DOMAIN>'s real
current code, not by copying measurement's content:

1. be-01-schema-inventory.md — the domain's current (pre-migration) schema/API surface: every query,
   mutation, and field this domain currently exposes, as-is.
2. be-02-resolver-analysis.md — pseudo-logic for every existing resolver: what it calls, in what order,
   what it merges, any quirks (defaults, null-handling, N+1 patterns) worth flagging now because
   they'll matter for parity later.
3. be-03-schema.graphql + be-03-schema-analysis.md — the TARGET federated schema for this domain, and a
   field-by-field classification (internal field resolver vs true cross-subgraph federation — this is
   where you'd identify this domain's own Phase F vs Phase H split, if any).
4. be-04-stories.md — the actual stories (this is what an engineer implements against) — Current
   Behaviour, Target, Acceptance Criteria, Test Cases per story, phase-lettered A-H per
   output/overview/00-program-overview.md §3's scheme. Also produce be-04-stories-index.yaml
   (machine-readable) and be-04-po-summary.md (PO-facing summary) alongside it.
5. be-05-attribute-inventory.md — field-level attribute detail.

Before writing be-04-stories.md, check output/analysis/program/cross-domain-dependencies.md and every
complex-case ADR in output/complexStories/ for existing references to <NEW_DOMAIN> — several complex
cases already list a "<NEW_DOMAIN>-twin" item in output/analysis/out-of-scope-backlog.md (later-phase
domain deferrals) with a specific pin-down/decision this domain's stories should inherit rather than
re-litigate. Cross-reference those, don't design from scratch where a decision already exists.

Flag every open decision as a Phase-0 spike story, the same way existing domains do (see product's
S-01/S-02/S-03 for the pattern), rather than guessing an answer inline in a build story.
```

## Stage 2 — wire the new domain into the generator scripts

Once stage 1's files exist, several scripts need the new domain added to their own `ALL_DOMAINS`
list/dict before they'll recognize it:

```
Now that output/analysis/<NEW_DOMAIN>/be-04-stories.md and its siblings exist, wire <NEW_DOMAIN> into
the generator pipeline:

1. Find every ALL_DOMAINS definition across fedMigrationScripts/generatescripts/*.py (grep for
   "^ALL_DOMAINS" — there are several, not one shared constant) and add <NEW_DOMAIN> to each, in the
   same style as the existing entries (domain key, display name, target DGS service).
2. If <NEW_DOMAIN> is co-located in an existing subgraph, add it there; if it needs a new subgraph
   entry (e.g. "plm-sample"), add that too, matching how existing later-phase estimates reference it in
   output/summary/00-program-overview.md's "DGS service groupings" table.
3. If team_config.py's BE_QUEUE/FE_WAVES should include this domain now (only if it's moving from
   later-phase into active build scope — check with me first), add it in the position we agree on.
4. Do NOT add <NEW_DOMAIN> to any complex-case's "ratified" story list — if a complex case's ADR
   named this domain as a later-phase twin, that item now graduates from
   output/analysis/out-of-scope-backlog.md into a real story in be-04-stories.md (done in stage 1),
   but the case's own 01-stories.md should be updated to include it explicitly, not left implicit.

Show me a diff of every file changed before I approve.
```

## Stage 3 — regenerate

```
Now run the full regeneration pipeline so <NEW_DOMAIN> appears in every roll-up:

python fedMigrationScripts/generatescripts/generate_all.py

Confirm <NEW_DOMAIN> now appears in: output/summary/00-program-overview.md's domain table,
output/jira/<NEW_DOMAIN>.csv, output/summary/<NEW_DOMAIN>/FederatedGqlBreakDown-<NEW_DOMAIN>.md, and
(if applicable) output/analysis/program/cross-domain-dependencies.md. Report the new program totals
(domain count, story count) and confirm they reconcile with a live count from all-stories.csv.
```

---
*Scripts prompt — bootstrap a new domain · output/prompts/scripts/bootstrap-new-domain.md*
