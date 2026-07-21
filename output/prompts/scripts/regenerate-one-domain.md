# Prompt — Regenerate all artifacts for one domain

> **Use when:** you edited a domain's `be-04-stories.md` (or any upstream `be-0N` file) and need every
> downstream artifact (breakdown page, PO summary roll-up, Jira CSV, cross-domain field analysis, ACL
> usage analysis) to reflect the change.
> **What this does NOT do:** it does not touch `be-01`–`be-05` themselves (those are hand/AI-authored
> source, not generated) — it only regenerates the roll-ups that read them.

---

## Prompt

Replace `<DOMAIN>` with one of: `product, bom, claims, measurement, impression, productDetails,
packaging, watchlist`.

```
Run the regeneration pipeline for exactly one domain, then verify the result:

1. From the migration repo root, run:
   python fedMigrationScripts/generatescripts/generate_all.py <DOMAIN>

2. Confirm the run printed "OK" (not "FAIL") for every step: word doc, breakdown markdown, jira CSV,
   cross-domain field analysis (be-06), ACL usage analysis (be-07). If any step FAILed, show me the
   error before doing anything else — don't proceed to step 3 on a partial failure.

3. Spot-check the output actually changed where expected:
   - output/summary/<DOMAIN>/FederatedGqlBreakDown-<DOMAIN>.md reflects the story edit
   - output/jira/<DOMAIN>.csv has the updated row(s)
   - output/analysis/<DOMAIN>/be-04-po-summary.md's story counts/phase table match the new state

4. Note: this single-domain run does NOT refresh the program-wide roll-ups (output/summary/00-program-
   overview.md, output/analysis/program/cross-domain-dependencies.md, all-stories.csv) — those only
   regenerate on a full (no-argument) run. If your edit changed a cross-domain Blocked-by/Depends-on
   field or a story count, tell me and I'll also run the full regeneration (see
   output/prompts/scripts/regenerate-multiple-domains.md) — a single-domain run alone would leave those
   program-wide files stale.

Report what changed (file list + brief diff summary), and flag anything that failed.
```

---
*Scripts prompt — regenerate one domain · output/prompts/scripts/regenerate-one-domain.md*
