# Complex Stories — problem briefs

One folder per genuinely complex, cross-domain case found during the resolver analysis.
Each folder holds a single `00-overview.md`:

- **§1 The problem** — grounded in the legacy code: which resolvers, what they do today, why it is hard.
- **§2 What must be decided** — the open questions the owning spike answers.

These briefs are the research so far. The decision and the detailed design/task
breakdown are produced by the spike and land here when it concludes.

| Case | Spike | Home domains |
|---|---|---|
| [non-atomic-write-saga](non-atomic-write-saga/00-overview.md) | `SPARK-SPIKE-01` | all `E`-phase writes |
| [techpack](techpack/00-overview.md) | `SPARK-SPIKE-02` | product |
| [partner-drop-undrop-write](partner-drop-undrop-write/00-overview.md) | `SPARK-SPIKE-03` | product · workspace |
| [notRemovable-undroppable-partners](notRemovable-undroppable-partners/00-overview.md) | `SPARK-SPIKE-04` | product · workspace |
| [polymorphic-type-resolution](polymorphic-type-resolution/00-overview.md) | `SPARK-SPIKE-05` | bom |
| [cross-domain-association](cross-domain-association/00-overview.md) | `SPARK-SPIKE-06a` (Hydration) / `SPARK-SPIKE-06b` (Association) | product · bom |
| [attachments-enrichment](attachments-enrichment/00-overview.md) | — (cutover pattern) | product · workspace |
| [components-and-counts-rollups](components-and-counts-rollups/00-overview.md) | — (cutover pattern) | product · workspace |

Stories gated on a spike are marked 🔴🔬 in their domain page with the spike id in
**Depends On** — see the Phase 0 table in the program breakdown
(`output/summary/Federated+Graphql+Stories+-+BreakDown.md`).
