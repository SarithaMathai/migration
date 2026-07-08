# spark-claims — GitHub Copilot POC

Starter GitHub Copilot configuration for the **spark-claims** DGS subgraph repo — a **standalone repo**, not a module in the `plm-product` monorepo. Drop this `.github/`, `AGENTS.md` and this `README.md` into the actual `spark-claims` repo root.

Same layer structure as the `plm-product` POC (see [`../plm-product/README.md`](../plm-product/README.md) for the general rationale), adapted for what's different about this repo: single domain, no co-located siblings, and it **contributes fields into `plm-product`'s types** instead of owning cross-domain data itself.

```
spark-claims/
├── AGENTS.md                                    ← read by Copilot's autonomous coding agent (issue → PR)
└── .github/
    ├── copilot-instructions.md                  ← repo-wide instructions, always applied
    ├── instructions/                             ← path-scoped rules (applyTo: glob)
    │   ├── graphql/schema.instructions.md         (**/*.graphqls)
    │   └── kotlin/
    │       ├── datafetcher.instructions.md        (Kotlin @DgsComponent fetchers)
    │       ├── service.instructions.md            (Kotlin services/clients)
    │       └── testing.instructions.md            (Kotlin tests)
    ├── prompts/                                   ← reusable /slash prompts (Copilot Chat)
    │   ├── story/
    │   │   ├── implement-story.prompt.md          /implement-story
    │   │   └── check-spike-gate.prompt.md          /check-spike-gate
    │   ├── schema/derive-dgs-schema.prompt.md      /derive-dgs-schema
    │   └── testing/write-parity-tests.prompt.md    /write-parity-tests
    └── chatmodes/                                 ← custom chat modes (VS Code mode picker)
        ├── story-implementer.chatmode.md
        ├── parity-checker.chatmode.md
        └── schema-steward.chatmode.md
```

## What's different from plm-product here

| | plm-product | spark-claims |
|---|---|---|
| Repo shape | monorepo, stories land in `apps/app` | standalone repo, one subgraph |
| Domains hosted | 7 co-located (product, bom, measurement, packaging, impression, productDetails, watchlist) | 1 (claims) |
| Story id prefix | `SPARK-PROD-*`, `SPARK-BOM-*`, … | `SPARK-CLM-*` |
| Cross-domain reference | co-located → plain type reference (in-process) | **always** a federation hop — no in-process shortcut |
| Federation direction | mostly hosts entities others extend | **contributes into** `plm-product`'s `Product`/`ResourcesCount` (`SPARK-CLM-F01`/`F02`) |
| Spike gating | 6 buckets across many stories | only `SPARK-CLM-E01` → `SPARK-SPIKE-01` |

## Source of truth this POC assumes

- Jira stories generated from `output/initial-analysis/claims/04-stories.md`, pushed from the migration repo.
- Confluence page `FederatedGqlBrakDown-claims` + the global overview (Phase 0 — Program Spikes).
- `fedMigrationScripts/` and `output/` are checked in at `https://github.com/XXX` — instructions/prompts link there for the legacy pseudo-logic and target schema an Engineer needs mid-story.

## Try it

1. `/check-spike-gate SPARK-CLM-E01` — confirm the one spike-gated story's status before starting.
2. `/implement-story SPARK-CLM-B01` (or switch to the **story-implementer** chat mode) — schema + Kotlin fetcher + service + tests in one pass.
3. `/write-parity-tests getClaims SPARK-CLM-B01` or the **parity-checker** chat mode — after implementing, verify response-shape parity with the legacy resolver.
4. **schema-steward** chat mode on any PR touching `.graphqls` — federation-safety review before the Hive push, including the `SPARK-CLM-F01`/`F02` contributions into `plm-product`.

See **[EXAMPLE-USAGE.md](./EXAMPLE-USAGE.md)** for two full worked sessions.
