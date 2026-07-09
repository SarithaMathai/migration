# AGENTS.md — plm-product

Instructions for the GitHub Copilot coding agent (and any other AGENTS.md-reading agent) working autonomously in this repo — e.g. from a Jira/GitHub issue assignment.

## Repo shape

- Monorepo. **`apps/app`** is the main API-hosting module and the only module migration stories touch, unless a story explicitly needs a missing method from a shared module.
- `apps/app` hosts the **plm-product** Netflix DGS subgraph: seven co-located domains — `product` (host), `bom`, `measurement`, `packaging`, `impression`, `productDetails`, `watchlist`.
- Language: **Kotlin** (Spring Boot + Netflix DGS). Data fetchers, services and tests are all Kotlin.

## Before making a change

1. Read `.github/copilot-instructions.md` for the migration model and hard rules.
2. Identify the story id in the assigned issue (`SPARK-{PROD|BOM|MEAS|PKG|IMP|PDTL|WL}-{phase}{n}`, e.g. `SPARK-PROD-B02`).
3. Check spike gating: if the story is Phase E or names a `SPARK-SPIKE-0x`, stop and comment on the issue with the open decision instead of coding — do not guess at a rollback/orchestration strategy yourself.
4. Read the story's *Current Behaviour → Target → Files → Acceptance Criteria → Test Cases* and the operation's pseudo-logic in `output/initial-analysis/{domain}/02-resolver-analysis.md` (companion analysis repo, linked from the issue).

## How to implement

- One story per PR/branch. Branch name `feature/{story-id-lowercase}`; commits start with the story id.
- Add only: schema (`apps/app/**/*.graphqls`), the Kotlin `@DgsComponent` data fetcher, a Kotlin service method (only if genuinely missing), and Kotlin tests — per the scoped rules in `.github/instructions/graphql/` and `.github/instructions/kotlin/`.
- Preserve legacy response shape/behaviour (parity) unless the story's *Target* says otherwise.
- Never add ACL logic or invented rollback/compensation logic.

## Validating a change

- Build the module and run its test suite before opening the PR.
- Run DGS codegen if a `.graphqls` file changed; confirm generated types compile.
- Walk the story's Acceptance Criteria one by one in the PR description with pass/fail evidence.

## PR description format

- Bullets, not paragraphs.
- Sections: *What changed*, *Acceptance criteria → evidence*, *Hive schema push note*, *Divergence from target schema (if any)*.
