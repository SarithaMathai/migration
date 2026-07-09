# Complex Story — Cross-domain association & hydration (`SPARK-SPIKE-06`)

> **Summary —** Every domain needs another domain's data, and today it's three brittle ways of reaching across. `SPARK-SPIKE-06` is an umbrella over two *separate* decisions — don't treat them as one:
> - **06a · Hydration** — pick one rule (federated `@key` vs direct call) for reading another domain's data, plus rollout order.
> - **06b · Association** — pick one pattern for a mutation that *also* links its record into a sibling domain (workspace/attachment/team/partner).
>
> **Status:** 🔴 Open — both decisions pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`), workspace (`plm-workspace`), search (`plm-elastic-search`), bom (`plm-product`)
> **06a (Hydration) stub stories:** `SPARK-PROD-S02` (two-stage hydration spike; gates `C01`) · `SPARK-BOM-B05` (`getBomMaterialTypes` merge with Material Hub) · workspace/search read-hub stories (not yet broken down — later-phase domains)
> **06b (Association) stub stories:** `SPARK-PROD-S01` (association-pattern spike; gates `D01`/`D02`/`D03`/`D04`/`D06`/`D07`/`D11`)

## 1. The problem (it recurs wherever one domain needs another's data)

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

## 2. What each half must decide

### 06a · Hydration
- Per edge: federated reference vs direct service call.
- The rollout order across sibling subgraphs so nothing ships half-wired.
- **Proposal so far (light, to validate):** prefer a federated reference when the other domain has a subgraph; a direct call only where it does not yet.

### 06b · Association
- Whether association-building is inline/synchronous, event-driven/async, or routed through one shared `AssociationService`.
- What happens if the primary write succeeds but the association call fails.
- Whether the three "Collab Canvas" mutations (`D06`/`D07`/`D11` — pure association mutations) follow the same pattern as the mutations that incidentally associate (`D01`–`D04`).
- **Proposal so far (light, to validate):** see `SPARK-PROD-S01`'s three candidate patterns (synchronous direct call, event-driven, shared `AssociationService`).

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
