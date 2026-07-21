---
mode: ask
model: Claude Sonnet 4.5
description: "Check whether a claims story is gated on a program spike, or blocked on plm-product, before starting it"
---

Check whether story **${input:storyId:CLAIM-BE-E-01}** is gated, using these program rules:

- **Spike gating:**

| Story | Spike | Bucket | Decision to make |
|---|---|---|---|
| `CLAIM-BE-E-01` (`updateClaim`) | `SPIKE-01` | Non-Atomic Write Saga | Pick (a) compensating saga, (b) compensation-log + best-effort, or (c) best-effort — and write down how to undo each step. |

  All other claims stories (B/C/D/G phases) are **not** spike-gated.

- **Federation blocking (not a spike, but must be checked before F-phase work):**

| Story | Blocked by | What must exist first |
|---|---|---|
| `CLAIM-BE-F-01` (`Product.claims`) | `plm-product` | The `Product` entity (`plm-product` Phase A) |
| `CLAIM-BE-F-02` (`ResourcesCount.claims`) | `plm-product` | The TechPack facade (`PRODUCT-BE-E-03`/`F-05`) |

- Spike briefs, decision-to-make and intended steps: **Phase 0 — Program Spikes** + **Spike Detail** on the global Confluence overview (`Federated+Graphql+Stories+-+BreakDown`); research so far in `output/complexStories/non-atomic-write-saga/` at https://github.com/XXX.

Answer with:
1. **Gated / Blocked / Neither**, and by which spike or dependency.
2. If spike-gated: the decision-to-make (status reads "Open — … to decide" until recorded) and what part of the story is blocked.
3. If federation-blocked: whether the owning type is confirmed live in `plm-product` yet — ask if unknown, don't assume.
4. If neither: confirm the story can proceed straight from its Acceptance Criteria.
