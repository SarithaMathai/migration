# Complex Story — Cross-domain association & hydration (`SPARK-SPIKE-06`)

> **Summary —** Decide how one domain references another’s entity — a federated `@key` reference vs a direct call — plus two-stage hydration and the sibling-DGS rollout order.
> **Spike:** `SPARK-SPIKE-06` · **Status:** 🔴 Open — decision pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`), workspace (`plm-workspace`), search (`plm-elastic-search`), bom (`plm-product`)
> **Stub stories:** `SPARK-PROD-C01` (two-stage hydration) · `SPARK-WS-D04` (later phase)/`G04` (workspace↔product) · `SPARK-SRCH-F01` (later phase) (read-hub) · bom material rollout

## 1. The problem (it recurs wherever one domain needs another's data)

- One domain constantly needs an object that **another** domain owns — a `product` on a `bom`, the `products` in a `workspace`, the canonical record behind a search hit.
- Today that happens in three messy ways, all of which federation is meant to replace:

| Symptom | Where it shows up today | Why it hurts |
|---|---|---|
| **Relationship-Service graph walk** to find related ids | `getMeasurements`, workspace resource lists, sample parents | a slow, central traversal bottleneck |
| **Reaching into another domain's resolver** to borrow data | `searchMaterialsBom` fabric-supplier import, `Workspace.products` | brittle cross-resolver coupling, not a clean contract |
| **Two-stage hydration** (index → canonical) done ad-hoc | `getProducts` (search flags → canonical body) | ordering/staleness handled per-caller, inconsistently |

There is also a **sequencing** question: a consumer subgraph must not go live before the provider it references
is federated, or the field returns a bare `{id}`.

## 2. What the spike must decide

- Per edge: federated reference vs direct service call.
- The rollout order across sibling subgraphs so nothing ships half-wired.
- **Proposal so far (light, to validate):** prefer a federated reference when the other domain has a subgraph; a direct call only where it does not yet.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
