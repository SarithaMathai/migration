# Engineer Instructions — Implementing a Story

> Audience: an engineer (backend or frontend) picking up a story from this migration's backlog for the
> first time. Goal: by the end of this doc you can find your story, understand what it depends on and
> what depends on it, and know what "done" means — without needing someone to walk you through it.
>
> **Just need the sequencing, dependency graph, or the Jira ticket?** [`finalArtifacts/`](../finalArtifacts/)
> (repo root, sibling of `output/`) is the slim entry point — `00-sequencing.md` (backend build order,
> one table per domain), `summary/{domain}/FederatedGqlBreakDown-{domain}.md` (Confluence breakdown),
> `summary/{domain}/story-dependency-graph-{domain}.md` (visual: which backend stories must ship before
> each frontend story can start), `jira/{domain}.csv` (import-ready, Acceptance Criteria only). Everything
> below is for when you need the full story text to actually implement it.
>
> Start at [`output/overview/00-program-overview.md`](../output/overview/00-program-overview.md) if you
> haven't yet — it explains *why* this migration exists and the phase-lettering scheme (A–H) referenced
> throughout this doc.

---

## 1. Repo navigation — where things live

```
migration/
├── output/
│   ├── overview/              ← start here (program overview, diagrams, index)
│   ├── analysis/{domain}/     ← YOUR domain's full story text lives here
│   │   ├── be-01-schema-inventory.md         current schema, as-is
│   │   ├── be-02-resolver-analysis.md        pseudo-logic for every existing resolver
│   │   ├── be-03-schema.graphql              target federated schema
│   │   ├── be-03-schema-analysis.md          field-by-field federation classification
│   │   ├── be-04-stories.md                  ← THE STORIES (full AC + Test Cases) — this is what you implement
│   │   ├── be-04-stories-index.yaml          same stories, machine-readable
│   │   ├── be-04-po-summary.md               PO-facing summary of the same stories
│   │   └── be-05-attribute-inventory.md      field-level attribute detail
│   │   └── fe-{domain}-breakdown.md          frontend view of this domain
│   ├── analysis/program/       ← cross-domain frontend docs (fe-00 … fe-11)
│   ├── complexStories/{case}/  ← ratified cross-domain design decisions (ADRs) — read BEFORE implementing
│   │                             any story that names a complex case in its Current Behaviour/EXT notes
│   ├── summary/                ← generated roll-ups: program totals, team plan, project plan (build order)
│   └── jira/{domain}.csv       ← same stories, Jira-importable
├── fedMigrationScripts/        ← the Python generators that produce everything under output/
└── adrs/                       ← pre-migration planning docs (older, context only)
```

**Rule of thumb:** `be-04-stories.md` is the only place with the full story text you implement against.
Everything else is either upstream research (`be-01`–`be-03`, `be-05`), downstream roll-up
(`po-summary`, `summary/`, `jira/`), or cross-domain context (`complexStories/`).

## 2. Finding your story

1. Story ids look like `<TOKEN>-BE-<PHASE>-<NN>` (backend) or `<TOKEN>-FE-<NNN>` (frontend) — e.g.
   `PRODUCT-BE-D-01`, `BOM-BE-G-15`.
2. Map the token to a domain using the table in
   [`output/overview/02-story-domain-index.md`](../output/overview/02-story-domain-index.md) (`PRODUCT`
   → product, `BOM` → bom, `CLAIM` → claims, `MST` → measurement, `PKG` → packaging, `PDTL` →
   productDetails, `WATCHLIST` → watchlist, `IMPRESSION` → impression).
3. Open that domain's `output/analysis/{domain}/be-04-stories.md` and search for `### <ID>`.
4. If your assignment is a frontend story instead, its full text is in
   [`output/analysis/program/fe-08-frontend-stories.md`](../output/analysis/program/fe-08-frontend-stories.md)
   — that file is the source of truth, not any generated summary.

## 3. Reading a story's dependency fields — the distinction that matters most

Every story header line carries some subset of these fields. Getting this distinction wrong is the
single most common way to start a story before it's actually safe to start:

| Field | Scope | Who enforces it | What it means |
|---|---|---|---|
| **`Depends on:`** | Intra-domain — another story in the *same* `be-04-stories.md` | The wave scheduler, automatically, when computing that domain's "Recommended Implementation Order" | That story must ship first, in this domain, before you start |
| **`Blocked by:`** | Cross-domain or cross-subgraph | **Nobody, automatically** — this is documentation only | A fact a human (you, your tech lead, the PO) has to check by hand before starting |
| **`EXT:`** | External backend service this story's implementation calls | N/A (informational) | Which non-GraphQL systems you'll be touching (e.g. `workspaceV2`, `attachment`) — a heads-up, not a gate |

**Concretely:** if you're about to start a story with a `Blocked by:` line, go check whether the thing
it names is actually ready. The consolidated table of every `Blocked by:` in the whole program is
[`output/analysis/program/cross-domain-dependencies.md`](../output/analysis/program/cross-domain-dependencies.md)
— it tells you if you're blocked on shared infrastructure in another domain (e.g. six domains' `E-01`
stories wait on `PRODUCT-BE-E-00`, the shared WriteSaga module) or on a subgraph that hasn't federated
yet (e.g. Phase H stories waiting on attachment/discussion/sample).

## 4. Phase letters — what kind of work you're doing

See [`output/overview/00-program-overview.md`](../output/overview/00-program-overview.md) §3 for the
full table. The one distinction worth internalizing before you start: **Phase F vs Phase H are both
"federation" work, but they are not the same kind of story.**

- **Phase F** — the field you're adding stays inside your own subgraph. No cross-subgraph entity
  resolution involved; ships on its own schedule.
- **Phase H** — the field is genuinely owned by a *different* subgraph. Your story is a
  `@DgsEntityFetcher`/`@key` extension, and it is `Blocked by:` that other subgraph going live. Don't
  start a Phase H story assuming it behaves like a normal field resolver — read
  [`output/overview/01-architecture-diagrams.md`](../output/overview/01-architecture-diagrams.md) §2
  first for the request-time sequence diagram.

## 5. Complex-case stories — read the ADR first

If a story's **Current Behaviour** text or `EXT:`/prose mentions a shared component, a saga, an
aggregation facade, or a cross-domain union/rollup, it is very likely implementing a ratified design
decision from one of the 8 **complex cases** in
[`output/complexStories/`](../output/complexStories/). Before writing code:

1. Open that case's `00-overview.md` (the problem — why this couldn't just be a normal story).
2. Read `01-adr-*.md` (the ratified decision — what pattern was chosen and why, including any accepted
   deviations from current behavior — these are deliberate, not bugs to "fix").
3. Check `01-stories.md` for exactly which stories (across which domains) implement this decision, and
   in what order/phase.

Skipping this step is the most common way to reimplement a pattern the ADR already ruled out (e.g.
writing bespoke per-domain fan-out code where the ADR mandates a shared component).

## 6. Implementation workflow / definition of done

1. **Read the whole story** — Current Behaviour → Target → Acceptance Criteria → Test Cases, in that
   order. Current Behaviour tells you what exists today (don't break it silently); Target tells you the
   federated shape; AC is your literal checklist; Test Cases are what a reviewer will look for.
2. **Check `Depends on:`** — confirm the story(ies) named there have actually shipped in your domain.
3. **Check `Blocked by:`** — confirm the cross-domain/cross-subgraph thing it names is actually ready
   (see §3). If it isn't, this story isn't startable yet — flag it, don't route around it.
4. **If it's a complex-case story, read the ADR first** (§5).
5. **Implement** — per the program's self-contained-story model, most stories are one PR: schema change
   + DGS data fetcher + the Kotlin service-layer call + Hive schema push. There is no separate
   service-layer story in this program; if you think you need one, that's a signal to re-read the ADR or
   ask, not to add one unilaterally.
6. **Verify against every Acceptance Criterion**, not just the happy path — ACs often encode a specific
   accepted deviation from current behavior (see the worked example below) that's easy to silently
   "fix" back to the old behavior by accident.
7. **Done** means: schema + resolver + service call shipped in one PR, every AC verified, Test Cases
   pass, and — if this story is one of several implementing a complex-case decision — the case's
   `01-stories.md` still accurately reflects what shipped (flag your tech lead if it doesn't).

## 7. Worked example — `PRODUCT-BE-D-01` (`addProduct`)

Full text: [`output/analysis/product/be-04-stories.md`](../output/analysis/product/be-04-stories.md),
search `### PRODUCT-BE-D-01`.

```
### PRODUCT-BE-D-01 · addProduct
- Type: Mutation · Phase: D · Complexity: Medium · Category: CAT-2 · Depends on: S-01 · EXT: 🔴 workspaceV2 · 🔴 attachment
```

**Reading the header:**
- **Phase D** — a mutation, not a cross-subgraph entity resolution — this is normal work, not gated on
  another subgraph going live.
- **`Depends on: S-01`** — this is intra-domain: `PRODUCT-BE-S-01` is a *spike* (a design decision, not
  a build story) that must resolve first. Checking the phases-overview table at the top of the same
  file, `S-01` is "cross-domain association pattern... draft ADR-011." So before starting `D-01`, the
  actual gate is: **has ADR-011 been ratified**, not just "has some other story shipped."
- **`EXT: workspaceV2, attachment`** — this story's implementation will call those two external
  services. Informational, not a scheduling gate — but it tells you which service clients you'll need.
- **No `Blocked by:`** — nothing cross-domain/cross-subgraph is gating this one; it's safe to start as
  soon as `S-01`'s decision is ratified.

**Reading the body:**
> Target: `@DgsMutation addProduct(workspaceId, sparkProduct, copyProduct): Product`; orchestrate
> create→copy→assoc **per `PRODUCT-BE-S-01`'s chosen cross-domain association pattern** (draft ADR-011
> Option B: shared association component, sync, service-to-service REST).

This sentence is doing exactly what §5 above describes: the story text is pointing you at
`output/complexStories/cross-domain-association/01-adr-cross-domain-association.md` for the actual
"how." Implementing `D-01` without reading that ADR risks reinventing the fan-out logic the ADR
specifically centralizes into one shared `associate(...)` component.

**Reading the AC:**
```
1. creates product.
2. optional copy runs when copyProduct present.
3. workspace assoc applied via the shared association component (no bespoke fan-out code).
4. failure after create (link or copy fails) surfaces per the mutation's declared failure policy
   — default fail-fast, no rollback, documented (ADR-011 §4).
```
AC 3 and 4 are the ones that encode the ADR's decision directly — a naive implementation that writes
its own fan-out code (violates AC 3) or silently swallows a post-create failure (violates AC 4, which
*deliberately* wants fail-fast, not a rollback) would pass a superficial read of "creates a product" but
fail the story's actual intent.

---

## Regeneration note

If you're touching a generator script under `fedMigrationScripts/generatescripts/` rather than writing
application code, see that folder's own comments — `team_config.py` documents the single-source-of-truth
pattern for team size/sequencing, and `output/README.md` §Regeneration lists every entry point.

---
*Engineer instructions · docs/instructions_engineer.md*
