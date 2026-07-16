# Skill 04 — Migration Story Generation (Pipeline 2.0)

> **Outputs:** `output/{domain}/be-04-stories.md` (Jira-ready) + `output/{domain}/be-04-po-summary.md`
> (Confluence-ready) + `output/{domain}/be-04-stories-index.yaml` (machine-readable for MCP bulk-create).
> **Depends on:** 02, 03, and 05. **Template:** [`story-template-engineer.md`](./story-template-engineer.md).

## The three Pipeline-2.0 rules (enforced)

1. **One operation per story** — no "and" in titles. Only allowed bundle: a single *trivial
   pass-through* table at the end of Phase G.
2. **Junior Definition of Ready** — a story isn't done until a junior could implement it with zero
   questions. Run the checklist in `story-template-engineer.md` against every story.
3. **YAML front-matter** on every story; **complexity tiers only** (no day-ranges in stories).

## Procedure

1. **One story per query** (Phase B/C), **per mutation** (Phase D), **per complex field resolver**
   (Phase G). Embed the Phase-2 pseudo-logic verbatim into Current Behaviour.
2. **CAT-3 service / CAT-1 schema** prerequisites become Phase-A stories (schema skeleton, owned types,
   external stubs, interface `@DgsTypeResolver`, service Kotlin port, ACL/JWT plumbing).
3. **CAT-4 federation** stories (Phase F) — one per cross-domain boundary from the EXT inventory. For a
   composite-key aggregate (e.g. TechPack `ResourcesCount`), use the facade-then-federate pattern in
   [`reference-federation-patterns.md`](./reference-federation-patterns.md): one Phase-E stub+facade
   story, one Phase-F placeholder per owning subgraph (`BLOCKED-BY: {domain}`), one retirement story.
4. **Tests** — fold unit/integration/parity test cases into each story's Test Cases (not separate
   stories), plus one domain-level parity-harness story in Phase G.
5. **Build the artifacts** (below).

## `be-04-stories.md` structure
Header → §1 Phases Overview (story counts per phase; **no day totals** — point to PO summary) →
§2 Dependency Graph (Mermaid) → §3 Stories (Phase A→G, full junior template each) → §4 Risk Register.

## `be-04-stories-index.yaml` (machine-readable — for Jira MCP)
A list of every story with the fields a Jira MCP needs to create a ticket:

```yaml
domain: bom
target_dgs: plm-product
stories:
  - id: BOM-BE-B-01
    summary: "Implement getBomByIds query data fetcher"
    epic: "BOM → plm-product migration"
    phase: B
    category: CAT-2
    complexity: Low
    labels: [dgs-migration, bom, query]
    depends_on: []
    ext_services: []
    acceptance_criteria_count: 6
```

## `be-04-po-summary.md` (Confluence-ready) — sections
What Are We Building (plain English) → Migration Scope (counts) → Story Summary by Phase
(**rough day-ranges allowed here, labeled "AI-estimated, confirm in refinement"**) → Key Risk Areas →
Decisions Required (with owners) → Dependency Map → Recommended Sprint Sequencing → Capacity Planning
(1/2/3 engineers). No pseudo-logic.

## Completion criteria
- [ ] Exactly one story per operation; titles have no "and".
- [ ] Every story passes the junior Definition-of-Ready checklist.
- [ ] Every story has parsable YAML front-matter consistent with its body.
- [ ] `be-04-stories-index.yaml` lists every story in `be-04-stories.md` (counts match).
- [ ] Every EXT boundary has a CAT-4 story; composite-key aggregates use the facade pattern.
- [ ] Risk register has ≥1 entry per High/Very-High story, with an owner.
- [ ] PO summary lists every story and its rough effort; no story is missing.
