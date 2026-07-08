---
mode: ask
model: Claude Sonnet 4.5
description: "Check whether a story is gated on a program spike before starting it"
---

Check whether story **${input:storyId:SPARK-PROD-E01}** is spike-gated, using these program rules:

- **Default rule:** every **Phase E** story is gated on `SPARK-SPIKE-01` unless overridden below.
- **Overrides / non-E gated stories** — phase-1 domains only (product, bom, measurement, packaging, impression, productDetails, watchlist, claims). Later-phase domains (workspace, sample, search, discussion, attachment) have their own overrides once they're in scope — see `SPIKE_OVERRIDES` in `generate_breakdown.py` for the full map:

| Story | Spike | Bucket |
|---|---|---|
| `SPARK-PROD-E01` | `SPARK-SPIKE-03` | Partner Drop/Undrop + Ownership |
| `SPARK-PROD-E03`, `SPARK-PROD-E04` | `SPARK-SPIKE-02` | TechPack Aggregate |
| `SPARK-PROD-G07` | `SPARK-SPIKE-04` | Not-Removable / Undroppable Partners |
| `SPARK-BOM-A04` | `SPARK-SPIKE-05` | Polymorphic Type Resolution |
| `SPARK-PROD-C01`, `SPARK-BOM-B05` | `SPARK-SPIKE-06a` | Hydration (read: federated `@key` ref vs REST; via `SPARK-PROD-S02`) |
| `SPARK-PROD-D01`–`D04`, `D06`, `D07`, `D11` | `SPARK-SPIKE-06b` | Cross-Domain Association (write links a sibling domain; via `SPARK-PROD-S01`) |

- Spike briefs, decision-to-make and intended steps: **Phase 0 — Program Spikes** + **Spike Detail** on the global Confluence overview (`Federated+Graphql+Stories+-+BreakDown`); research so far in `output/complexStories/<case>/` at https://github.com/XXX.

Answer with:
1. **Gated / Not gated**, and by which spike.
2. If gated: the spike's decision-to-make (status reads "Open — … to decide" until recorded) and what part of the story is blocked (usually only the complex step — scaffold/read parts may proceed if the story says so).
3. If not gated: confirm the story can proceed straight from its Acceptance Criteria.
