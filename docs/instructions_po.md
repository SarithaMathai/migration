# Product Owner Instructions — Reading, Prioritizing, and Sequencing the Backlog

> Audience: a Product Owner working with this migration's backlog for the first time. Goal: by the end
> of this doc you can read the backlog, understand what's sequenced and why, and know what you're being
> asked to review or ratify at each layer — without an engineer translating it for you each time.
>
> Start at [`output/overview/00-program-overview.md`](../output/overview/00-program-overview.md) if you
> haven't yet — it's the one-page "what and why."

---

## 1. How to read the backlog

You don't read `be-04-stories.md` (that's the engineer-facing full text with code samples). Your entry
points are:

| You want to know... | Read this |
|---|---|
| What's the program building, overall, and how much does it cost | [`output/summary/00-program-overview.md`](../output/summary/00-program-overview.md) |
| What's this domain building, in plain language, and what's risky | `output/analysis/{domain}/be-04-po-summary.md` — one per domain, written for you specifically |
| When will domain X be done | [`output/summary/01-implementation-plan-1BE-1FE.md`](../output/summary/01-implementation-plan-1BE-1FE.md) (§4 below) |
| What's the exact build order and why | [`output/summary/02-project-plan.md`](../output/summary/02-project-plan.md) |
| What decisions are still open / need my sign-off | Each domain's po-summary "Decisions Required" section, or a complex case's ADR status (§3 below) |

Every `be-04-po-summary.md` follows the same shape: **What Are We Building** (plain-language, no code),
**Deployment model** (which stories ship independently vs wait on something), **Migration Scope**
(counts), **Story Summary by Phase** (effort estimates with a "Ready when" column — this is your
prioritization signal, see §2).

**On the numbers:** every effort estimate in these docs is explicitly labeled AI-estimated, pending
refinement. Treat day-ranges as relative sizing signal (this domain is bigger than that one), not a
committed date, until the team has actually refined them.

## 2. Phases, categories, and what actually drives priority

Stories are grouped into **phases** (A–H, a *what kind of work* label — see program overview §3) and
**categories** `CAT-1`–`CAT-4` (a rough sizing/risk band). Neither of those, by itself, tells you what
order to prioritize in — sequencing comes from three other signals, and they're not interchangeable:

1. **`Depends on:`** (intra-domain) — the wave scheduler already sequences these for you inside a
   domain. You don't need to reason about this one; it's baked into "Ready when" and the project plan.
2. **`Blocked by:`** (cross-domain/cross-subgraph) — **this is the one that needs your judgment.** It's
   not scheduler-enforced, so if you prioritize a blocked story into an early sprint, it will sit
   un-startable until the thing it's blocked on lands. The full list is
   [`output/analysis/program/cross-domain-dependencies.md`](../output/analysis/program/cross-domain-dependencies.md)
   — read the two tables there (six stories waiting on product's shared WriteSaga module; nine waiting
   on a subgraph that isn't live yet) before you sequence anything that touches those domains.
3. **Complex-case ADR ratification status** (§3) — a story that implements an unratified draft ADR
   (currently: TechPack, `ADR-015`, 🟠 draft) shouldn't be prioritized into a near-term sprint even if
   nothing else blocks it, because the underlying design could still change.

**To read the dependency diagram visually instead of the table:**
[`output/overview/01-architecture-diagrams.md`](../output/overview/01-architecture-diagrams.md) §3 — every
arrow points at a blocked story, pointing from what it's waiting on. If you're deciding whether to pull
a story forward, check this diagram first.

## 3. Complex Stories (CS) — what you're actually being asked to approve

Eight areas of this migration needed a cross-domain design decision *before* any story could be written
safely — these are tracked as **Complex Stories** in
[`output/complexStories/`](../output/complexStories/), each with its own ADR (Architecture Decision
Record). This is a distinct review workflow from normal backlog grooming:

| What you're reviewing | Where | What "approve" means |
|---|---|---|
| The problem brief | `{case}/00-overview.md` | Confirm the framing is right — is this actually a cross-domain problem, and is the impact section accurate |
| The proposed decision | `{case}/01-adr-*.md` | This is the actual ratification ask — a status badge (🟠 Proposed / ✅ Ratified) tells you where it stands. Ratifying an ADR unblocks every story listed in that case's `01-stories.md` |
| Which stories implement it | `{case}/01-stories.md` | Confirms scope — these are the concrete, estimable stories your sprint plan will actually carry |

**Current status:** 7 of 8 cases are ratified. **TechPack (`ADR-015`) is still 🟠 draft** — this is the
single highest-leverage ratification decision in the backlog right now, since it gates Product's
`E-03`/`E-04` (the facade) plus five `H`-phase federation stories across multiple domains. If you only
review one ADR this sprint, review that one.

**Important:** these are **not** counted twice against your Phase A–G totals. A complex-case story
(e.g. `PRODUCT-BE-E-00`, the shared WriteSaga module) is a real row in its domain's `be-04-stories.md`
and its domain's story count — the case folder is a cross-reference index into stories that already
exist, not a separate backlog.

## 4. Reading the roadmap — "when will X be done"

[`output/summary/01-implementation-plan-1BE-1FE.md`](../output/summary/01-implementation-plan-1BE-1FE.md)
has two tables — Backend lane and Frontend lane — read them together, not separately, because frontend
work is **gated** on backend milestones, not scheduled independently:

- **Backend lane** — one row per domain, in build order (currently: product → watchlist →
  productDetails → measurement → packaging → bom → claims → impression). The **"FE gate (A–E done)"**
  column is the day backend reads/search/writes for that domain are live — that's the earliest the
  frontend cutover for that domain can start. Backend phases F (federation) and G (field-resolver
  parity) trail behind this gate and don't block the frontend flip.
- **Frontend lane** — organized by **wave**, not domain build order. A wave's entry gate is often "the
  previous wave's pilot has soaked in production for one sprint," not just "backend is ready" — check
  the "Waits for" column, it names the specific gate.
- **Milestones** table at the bottom is your at-a-glance checkpoint list (pilot live, first cross-subgraph
  cutover, etc.) — use this for status reporting rather than re-deriving dates from the lane tables each time.

For the exact story-by-story sequence within a domain (useful when a stakeholder asks "why is story X
not done yet"): [`output/summary/02-project-plan.md`](../output/summary/02-project-plan.md) — every story
carries its Depends On / Blocks / Parallelizable metadata inline.

**If the team size changes** (more engineers added/removed), the day-ranges in both lanes are
regenerated from [`team_config.py`](../../fedMigrationScripts/generatescripts/team_config.py) — ask an
engineer to bump `N_BE_ENGINEERS`/`N_FE_ENGINEERS` there and regenerate; don't hand-adjust the dates in
the plan doc, they'll drift from the underlying schedule.

## 5. What's deliberately not in Jira

[`output/analysis/out-of-scope-backlog.md`](../output/analysis/out-of-scope-backlog.md) tracks items
that are real, known gaps but are **not** imported to Jira and **not** counted in any story total —
later-phase domain twins (work that repeats once attachment/discussion/sample/workspace/search
federate), and a few genuine session-level gaps found during backlog authoring. Bug-fix and
test-coverage-shaped stories are also deliberately excluded from this pipeline — those are created
manually, outside this backlog, per standing program policy. Check this doc before assuming something
is "missing" from the story counts.

---

## Quick reference — doc map for this role

1. [`output/overview/00-program-overview.md`](../output/overview/00-program-overview.md) — what and why
2. `output/analysis/{domain}/be-04-po-summary.md` — per-domain, plain-language
3. [`output/analysis/program/cross-domain-dependencies.md`](../output/analysis/program/cross-domain-dependencies.md) — every cross-domain block, one table
4. [`output/overview/01-architecture-diagrams.md`](../output/overview/01-architecture-diagrams.md) — the same blocks, visually
5. [`output/complexStories/`](../output/complexStories/) — ADRs awaiting your ratification
6. [`output/summary/01-implementation-plan-1BE-1FE.md`](../output/summary/01-implementation-plan-1BE-1FE.md) + [`02-project-plan.md`](../output/summary/02-project-plan.md) — the roadmap
7. [`output/analysis/out-of-scope-backlog.md`](../output/analysis/out-of-scope-backlog.md) — what's deliberately not here

---
*Product Owner instructions · docs/instructions_po.md*
