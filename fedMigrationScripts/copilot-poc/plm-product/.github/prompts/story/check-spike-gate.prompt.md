---
mode: ask
model: Claude Sonnet 4.5
description: "Check whether a story is gated on a program spike before starting it"
---

Check whether story **${input:storyId:PRODUCT-BE-E-01}** is spike-gated, using these program rules:

- **Default rule:** every **Phase E** story is gated on `SPIKE-01` unless overridden below.
- **Overrides / non-E gated stories** — phase-1 domains only (product, bom, measurement, packaging, impression, productDetails, watchlist, claims). Later-phase domains (workspace, sample, search, discussion, attachment) have their own overrides once they're in scope — see `SPIKE_OVERRIDES` in `generate_breakdown.py` for the full map:

| Story | Spike | Bucket |
|---|---|---|
| `PRODUCT-BE-E-01` | `SPIKE-03` | Partner Drop/Undrop + Ownership |
| `PRODUCT-BE-E-03`, `PRODUCT-BE-E-04` | `SPIKE-02` | TechPack Aggregate |
| `PRODUCT-BE-G-07` | `SPIKE-04` | Not-Removable / Undroppable Partners |
| `BOM-BE-A-04` | `SPIKE-05` | Polymorphic Type Resolution |
| `PRODUCT-BE-C-01`, `BOM-BE-B-05` | `SPIKE-06a` | Hydration (read: federated `@key` ref vs REST; via `PRODUCT-BE-S-02`) |
| `PRODUCT-BE-D-01`–`D-04`, `D-06`, `D-07`, `D-11` | `SPIKE-06b` | Cross-Domain Association (write links a sibling domain; via `PRODUCT-BE-S-01`) |

- Spike briefs, decision-to-make and intended steps: **Phase 0 — Program Spikes** + **Spike Detail** on the global Confluence overview (`Federated+Graphql+Stories+-+BreakDown`); research so far in `output/complexStories/<case>/` at https://github.com/XXX.

Answer with:
1. **Gated / Not gated**, and by which spike.
2. If gated: the spike's decision-to-make (status reads "Open — … to decide" until recorded) and what part of the story is blocked (usually only the complex step — scaffold/read parts may proceed if the story says so).
3. If not gated: confirm the story can proceed straight from its Acceptance Criteria.
