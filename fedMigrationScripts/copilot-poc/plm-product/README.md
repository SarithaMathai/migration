# plm-product — GitHub Copilot POC

Starter GitHub Copilot configuration for the **plm-product** DGS subgraph repo (monorepo, `apps/app` = the API-hosting module: product · bom · measurement · packaging · impression · productDetails · watchlist). Drop this `.github/`, `AGENTS.md` and this `README.md` into the actual `plm-product` repo root.

**New to this? Start with [GETTING-STARTED.md](./GETTING-STARTED.md)** — clone → copy these files into your `plm-product` clone → verify Copilot picked them up → implement your first story. This README is the reference; that file is the walkthrough.

Uses GitHub Copilot's standard file conventions — no invented formats:

```
plm-product/
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
    │   ├── testing/write-parity-tests.prompt.md    /write-parity-tests
    │   └── product-phases/                         one prompt per migration phase (A–G)
    │       ├── phase-a-scaffold.prompt.md          /phase-a-scaffold
    │       ├── phase-b-reads.prompt.md             /phase-b-reads
    │       ├── phase-c-search.prompt.md            /phase-c-search
    │       ├── phase-d-mutations.prompt.md         /phase-d-mutations
    │       ├── phase-e-complex.prompt.md           /phase-e-complex
    │       ├── phase-f-federation.prompt.md        /phase-f-federation
    │       └── phase-g-field-resolvers.prompt.md   /phase-g-field-resolvers
    └── chatmodes/                                 ← custom chat modes (VS Code mode picker)
        ├── story-implementer.chatmode.md
        ├── parity-checker.chatmode.md
        └── schema-steward.chatmode.md
```

## What each layer is for

| Layer | Applies | Use for |
|---|---|---|
| `copilot-instructions.md` | every Copilot request in this repo | migration model, story-id scheme, hard rules (ACL, spike gating, parity) |
| `instructions/**/*.instructions.md` | files matching `applyTo` | schema/Kotlin-specific conventions, scoped so they don't pollute unrelated edits |
| `prompts/**/*.prompt.md` | invoked with `/name` in Copilot Chat | repeatable multi-step tasks with inputs (`${input:storyId}`) |
| `chatmodes/*.chatmode.md` | selected from the chat mode picker | a persistent persona + toolset for a whole session (implement / verify parity / review schema) |

## Source of truth this POC assumes

- Jira stories generated from `output/initial-analysis/{domain}/04-stories.md`, pushed from this migration repo.
- Confluence pages `FederatedGqlBrakDown-{domain}` + the global overview (Phase 0 — Program Spikes).
- `fedMigrationScripts/` and `output/` are checked in at `https://github.com/XXX` — instructions/prompts link there for the legacy pseudo-logic and target schema an Engineer needs mid-story.

## Try it

1. `/check-spike-gate PRODUCT-BE-E-01` — confirm a Phase-E story's spike status before starting.
2. `/implement-story PRODUCT-BE-B-02` (or switch to the **story-implementer** chat mode) — schema + Kotlin fetcher + service + tests in one pass.
3. `/write-parity-tests getProduct PRODUCT-BE-B-02` or the **parity-checker** chat mode — after implementing, verify response-shape parity with the legacy resolver.
4. **schema-steward** chat mode on any PR touching `.graphqls` — federation-safety review before the Hive push.

See **[EXAMPLE-USAGE.md](./EXAMPLE-USAGE.md)** for two full worked sessions — a simple story implemented start-to-finish (`PRODUCT-BE-B-01`) and a complex story caught by the spike gate (`PRODUCT-BE-E-01`) — showing exactly which chat mode, prompt, and instruction file fires at each step.

## Phase A–G, one prompt each

Each migration phase has a different shape and a different amount of Copilot judgment involved — a Phase-B read just gets implemented, a Phase-E write stops dead until a spike resolves. **[copilotExample.md](./copilotExample.md)** walks all seven phases end-to-end with real `product`-domain stories, showing exactly what the Engineer types and how Copilot responds differently in each phase (proceed / propose-a-fallback / ask / refuse-and-scaffold-only / check-deployment-order-not-spike).
