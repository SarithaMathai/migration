# Complex Story — Cross-domain association & hydration (`SPIKE-06`)

> **Summary —** Every domain needs another domain's data, and today it's three brittle ways of reaching across. `SPIKE-06` is an umbrella over two *separate* decisions — don't treat them as one:
> - **06a · Hydration** — pick one rule (federated `@key` vs direct call) for reading another domain's data, plus rollout order.
> - **06b · Association** — pick one pattern for a mutation that *also* links its record into a sibling domain (workspace/attachment/team/partner).
>
> **Status:** 06a 🔴 Open — decision pending · 06b 🟠 Draft ADR-011 proposed — ratification pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`), workspace (`plm-workspace`), search (`plm-elastic-search`), bom (`plm-product`)
> **06a (Hydration) stub stories:** `PRODUCT-BE-S-02` (two-stage hydration spike; gates `C-01`) · `BOM-BE-B-05` (`getBomMaterialTypes` merge with Material Hub) · workspace/search read-hub stories (not yet broken down — later-phase domains)
> **06b (Association) stub stories:** `PRODUCT-BE-S-01` (association-pattern spike; gates `D-01`/`D-02`/`D-03`/`D-04`/`D-06`/`D-07`/`D-11`)

## 1. The problem (it recurs wherever one domain needs another's data)

### 1.1 Problem statement

- Cross-domain data access in the monolith happens three brittle ways — Relationship-Service graph walks,
  reaching into another domain's resolver, and ad-hoc two-stage index→canonical reads — and cross-domain
  *link-building* after a write happens five slightly different ad-hoc ways.
- Federation replaces all of them, but only if two separate rules are decided once: how a domain **reads**
  another's entity (06a), and how a mutation **links** its record into a sibling domain (06b).

### 1.2 Current state & root cause

- One domain constantly needs an object that **another** domain owns — a `product` on a `bom`, the `products` in a `workspace`, the canonical record behind a search hit. That's **hydration** (06a): a *read*.
- Separately, a mutation on one domain's record often also has to **create a link** into a sibling domain — attach files, put a product in a workspace, add teams, add partners. That's **association** (06b): a *write side-effect*. It is not the same problem as hydration even though both are "cross-domain" — 06b never needs to decide "federated ref vs REST read," it needs to decide "sync vs async vs shared-service call."
- Today both happen in messy, ad-hoc ways that federation is meant to replace:

| Symptom | Sub-problem | Where it shows up today | Why it hurts |
|---|---|---|---|
| **Relationship-Service graph walk** to find related ids | 06a Hydration | `getMeasurements`, workspace resource lists, sample parents | a slow, central traversal bottleneck |
| **Reaching into another domain's resolver** to borrow data | 06a Hydration | `searchMaterialsBom` fabric-supplier import, `Workspace.products` | brittle cross-resolver coupling, not a clean contract |
| **Two-stage hydration** (index → canonical) done ad-hoc | 06a Hydration | `getProducts` (search flags → canonical body) | ordering/staleness handled per-caller, inconsistently |
| **Inline call-out to link a sibling record** after a mutation | 06b Association | `addProduct` → workspace assoc, `updateProduct` → attachment cleanup, `addTeamsToProduct` | five near-duplicate ad-hoc versions of "write, then also link" |

There is also a **sequencing** question on the hydration side: a consumer subgraph must not go live before the provider it references is federated, or the field returns a bare `{id}`.

**Root cause:** the monolith had no boundary between domains — any resolver could walk the relationship
graph, import a sibling resolver, or call any backend — so every team solved "I need another domain's
data/link" locally; federation introduces boundaries, and the ad-hoc reaches become either broken
(resolver imports, `variableValues`) or architectural decisions (ref vs REST, sync vs async).

### 1.3 Impact if not addressed

- **06a (reads)** — per-edge improvisation: inconsistent staleness/ordering semantics, consumers shipping
  before providers (fields degrade to bare `{id}` stubs), and the retiring Relationship-Service walk
  surviving inside individual resolvers.
- **06b (writes)** — the five "write, then also link" variants get ported as five variants; partial
  failure after the primary write stays silent/undocumented; `D-01`/`D-02`/`D-04` stay blocked.
- **Program-wide** — every later-phase domain re-litigates both questions without a recorded rule.

### 1.4 Objectives

The spikes are done when the following are recorded and ratified:
- **06a:** a per-edge rule (federated `@key` reference vs direct service call), the two-stage hydration
  contract (index → canonical, staleness semantics), and a rollout order in which no consumer ships
  before its provider.
- **06b:** one association pattern (sync / async / shared service) with an explicit partial-failure
  policy per mutation, the resolver-import coupling removed, and the Collab Canvas trio's scope
  (in or out) documented with reasons.
- Behavioral parity for the gated stories (`C-01`, `D-01`/`D-02`/`D-04`), proven by recorded fixtures.

## 2. What each half must decide

### 06a · Hydration
- Per edge: federated reference vs direct service call.
- The rollout order across sibling subgraphs so nothing ships half-wired.
- **Proposal so far (light, to validate):** prefer a federated reference when the other domain has a subgraph; a direct call only where it does not yet.

### 06b · Association
- Whether association-building is inline/synchronous, event-driven/async, or routed through one shared `AssociationService`.
- What happens if the primary write succeeds but the association call fails.
- Whether the three "Collab Canvas" mutations (`D-06`/`D-07`/`D-11` — pure association mutations) follow the same pattern as the mutations that incidentally associate (`D-01`–`D-04`).
- **Proposal so far (light, to validate):** see `PRODUCT-BE-S-01`'s three candidate patterns (synchronous direct call, event-driven, shared `AssociationService`).
- **Draft decision (06b):** [ADR-011 (draft)](./01-adr-cross-domain-association.md) proposes synchronous
  in-subgraph orchestration through one shared association component (Option B), with the event-driven
  pattern recorded as end-state behind a transactional-outbox precondition — status 🔴 Proposed, pending
  ratification. It also **descopes** `D-03`/`D-06`/`D-07`/`D-11` (no cross-subgraph write). Scenario variant
  under the domain-ACL assumption: [ADR-011-noACL](./02-adr-noacl-cross-domain-association.md).
  06a has no draft ADR yet — it concludes via `PRODUCT-BE-S-02`.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
