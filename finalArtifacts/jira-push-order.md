# Jira Push Order — by domain

> 🏷️ **Tags:** `dgs-migration` · `jira` — **Assembled:** 2026-07-24 from the actual `Depends On`
> edges in `finalArtifacts/jira/*.csv`. Recommendation: **push by domain**, in the order below, so
> every cross-domain dependency link resolves with zero pending links.

## Recommendation: push by domain — yes

Pushing one domain at a time (via `output/prompts/jira/push-domain-all-stories.md`) is the right unit:
each push is independently reviewable, a failure on one domain doesn't block the rest, and the
create-then-link-dependencies flow works cleanly within a domain.

**The only thing that dictates *order* is cross-domain dependency links.** A `Depends On` id that
points at another domain becomes a Jira "is blocked by" link, which can only be created if the target
issue **already exists**. Push in an order where every target is already in Jira → no pending links.

## The dependency shape (from the CSVs)

Every cross-domain edge points at **product** — except impression, which also needs **bom**.
`product` itself has **no** cross-domain dependencies. That makes the order nearly linear:

| Cross-domain edge | Why |
|---|---|
| bom, claims, measurement, packaging, productDetails, watchlist → **product** | each domain's `E-01` write story is blocked by `PRODUCT-BE-E-00` (shared WriteSaga); claims also needs product F-14/E-03/H-06 |
| impression → **product** and **bom** | `IMPRESSION-FE-001` reads BOM data (`getBomDataAndImpressions`); both pairs read product |

## Recommended order

| # | Domain | Stories | Needs already-pushed | Pending links |
|---|---|---|---|---|
| **1** | **Product** | 79 | — (self-contained) | 0 |
| 2 | Watchlist | 16 | product ✓ | 0 |
| 3 | Product Details | 15 | product ✓ | 0 |
| 4 | Measurement | 34 | product ✓ | 0 |
| 5 | Packaging | 28 | product ✓ | 0 |
| 6 | Claims | 24 | product ✓ | 0 |
| 7 | BOM | 44 | product ✓ | 0 |
| **8** | **Impression** | 9 | product ✓ **and** bom ✓ | 0 |

- **Product first** — it is the target of every cross-domain edge and depends on nothing else. Push
  it and all downstream links have somewhere to land.
- **Impression last** — the only domain needing two others (product **and** bom). Both must precede it.
- **Steps 2–7 are order-free** among themselves (each only needs product). Listed smallest-first for
  quick early wins; reorder freely. **BOM before impression** is the one constraint in this middle band.

## ⚠ Spikes are not in the per-domain CSVs

`SPIKE-01`…`SPIKE-07` are referenced by many stories' `Depends On` (e.g. every `E-01` needs
`SPIKE-01`) but the **spike issues themselves live only in `finalArtifacts/jira/all-stories.csv`**, not
in any domain CSV. So if you push domain-by-domain, spike links will be **pending** until the spikes
exist.

**Fix — push spikes first (step 0):**

- **Step 0 — Spikes.** Create the 8 spike issues from `all-stories.csv` (rows with `Issue Type=Spike`:
  `SPIKE-01, 02, 03, 04, 05, 06a, 06b, 07`) before any domain. Then every domain's spike link resolves
  on push. Do this once, up front.

Full order becomes: **Spikes → Product → Watchlist → Product Details → Measurement → Packaging →
Claims → BOM → Impression.**

## Testing note

Validate the mechanism on **Product first** against a **test Jira project**: it's self-contained
(0 pending links), the largest domain (79 stories — the hardest to get right), and references the most
spikes. If Product pushes clean, every other domain is easier. Then repeat the order against the real
project.

## How to run each push

Use `output/prompts/jira/push-domain-all-stories.md` — **Step 1 (dry run) first**, review the plan
table, then Step 2 (create + link). Fill in `<DOMAIN>` and `<PROJECT_KEY>` (the GitHub repo is already
wired to `target-corp/saritha-mathai-repositories-research`). The dry run reports create-vs-update per
row and flags any cross-domain link so nothing surprises you.

---
*Jira push order · assembled 2026-07-24 from finalArtifacts/jira/*.csv cross-domain edges.*
