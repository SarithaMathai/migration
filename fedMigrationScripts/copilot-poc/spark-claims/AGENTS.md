# AGENTS.md — spark-claims

Instructions for the GitHub Copilot coding agent (and any other AGENTS.md-reading agent) working autonomously in this repo — e.g. from a Jira/GitHub issue assignment.

## Repo shape

- Standalone repo — **not** part of the `plm-product` monorepo. Hosts exactly one Netflix DGS subgraph: **claims**.
- Language: **Kotlin** (Spring Boot + Netflix DGS). Data fetchers, services and tests are all Kotlin.
- Federates into the supergraph alongside `plm-product` (host) and, later, the other separate subgraphs.

## Before making a change

1. Read `.github/copilot-instructions.md` for the migration model and hard rules — especially the note that this subgraph *contributes into* `Product`/`ResourcesCount` rather than owning cross-domain data itself.
2. Identify the story id in the assigned issue (`SPARK-CLM-{phase}{n}`, e.g. `SPARK-CLM-B02`).
3. Check spike gating: `SPARK-CLM-E01` is gated on `SPARK-SPIKE-01`. If assigned that story, comment on the issue with the open decision instead of coding — do not guess at a rollback/failure strategy yourself.
4. Check federation blocking: `SPARK-CLM-F01` and `SPARK-CLM-F02` are **BLOCKED-BY** `plm-product` (the `Product` entity and the TechPack `ResourcesCount` facade must exist there first). If assigned one of these before that's confirmed live, comment and stop.
5. Read the story's *Current Behaviour → Target → Files → Acceptance Criteria → Test Cases* and the operation's pseudo-logic in `output/initial-analysis/claims/02-resolver-analysis.md` (companion analysis repo, linked from the issue).

## How to implement

- One story per PR/branch. Branch name `feature/{story-id-lowercase}`; commits start with the story id.
- Add only: schema (`**/*.graphqls`), the Kotlin `@DgsComponent` data fetcher (or `@DgsEntityFetcher`/`@DgsData` for F-phase federation contributions), a Kotlin service method (only if genuinely missing), and Kotlin tests — per the scoped rules in `.github/instructions/graphql/` and `.github/instructions/kotlin/`.
- Preserve legacy response shape/behaviour (parity) unless the story's *Target* says otherwise.
- Never add ACL/proxy-ACL logic or invented rollback/compensation logic.

## Validating a change

- Build the module and run its test suite before opening the PR.
- Run DGS codegen if a `.graphqls` file changed; confirm generated types compile.
- Walk the story's Acceptance Criteria one by one in the PR description with pass/fail evidence.
- For F-phase stories, confirm the federation hop resolves against a running `plm-product` subgraph (or its recorded schema) before claiming done.

## PR description format

- Bullets, not paragraphs.
- Sections: *What changed*, *Acceptance criteria → evidence*, *Hive schema push note*, *Divergence from target schema (if any)*.
