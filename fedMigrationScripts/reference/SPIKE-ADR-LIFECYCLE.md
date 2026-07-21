# Spike → ADR → breakdown lifecycle

How a hard problem goes from *"we don't know the approach yet"* to *shipped stories*. Short and practical.

## The 6 program spikes

The genuinely complex, cross-cutting problems are **program spikes** `SPIKE-01…06` (listed in the
global breakdown, *Phase 0 — Program Spikes*). Each one:
- **blocks** the domain stories that depend on it (those stories are flagged 🔴🔬),
- **concludes with an ADR** (a decision),
- and its design **lands in a folder**: `output/complexStories/<case>/`.

The spike ↔ ADR ↔ case ↔ status mapping lives in one machine-readable file:
**[`adrs/adr-index.yaml`](../../adrs/adr-index.yaml)** — read it to see, per spike, the options and which is chosen.

## The lifecycle

```
SPIKE-0x        run the spike        record decision           build it
(Proposed)  ─────►   research options  ─────►  ADR + adr-index   ─────►  case folder
                                              status: Accepted          + stories + CSV
                                              chosen: <option>                │
                                                                             ▼
                                              regenerate ◄──── update sources ── import to Jira
                                              (.md/.docx/.csv)   (04-stories)    + Confluence
                                                                                     │
                                                                                     ▼
                                                                              build → parity gate → Done
```

## Where the ADR goes (so scripts/agents can read it)

1. **The write-up** (options + reasoning) → `adrs/<name>.pdf` (or `.md`). This is the human doc.
2. **The machine-readable entry** → add/update the spike's block in **`adrs/adr-index.yaml`**:
   ```yaml
   - spike:  SPIKE-0x
     case:   complexStories/<case>
     status: Accepted            # was Proposed
     adr_doc: adrs/<name>.pdf
     options: ["A …", "B …"]     # the options the ADR weighed
     chosen:  "A — …"            # the approved one (null while Proposed)
   ```
   > **Multiple options, one approved:** keep **all** options in `options:`; set `chosen:` to the approved one
   > and `status: Accepted`. That preserves the "why not B/C" trail and gives scripts one field to read.

`adr-index.yaml` is the single source for a decision's **status** and **chosen option**; the source PDFs stay
next to it for the full reasoning.

## Runbook — a spike just concluded, migrate the functionality

Do these in order:

1. **ADR** — save the write-up in `adrs/`; set the spike's `status: Accepted` + `chosen:` in
   [`adrs/adr-index.yaml`](../../adrs/adr-index.yaml).
2. **Case folder** — in `output/complexStories/<case>/`: fill `00-overview.md` §2 with the chosen approach,
   flip the banner **Status → Decided**, and complete `01-stories.md` + `01-stories-index.yaml` +
   `implementation/` (per-service pseudo-code). *(New spike with no folder yet? copy
   [`_TEMPLATE/`](../complexStories/_TEMPLATE/).)*
3. **Domain sources** — in each affected `output/analysis/{domain}/be-04-stories.md`, replace the story's
   *"per `SPIKE-0x`"* placeholder with the concrete choice (e.g. the failure strategy).
4. **Regenerate**:
   ```bash
   python output/complexStories/generate.py                                  # <case>.csv + <case>-stories.md
   python fedMigrationScripts/generatescripts/generate_all.py {domains}      # refresh domain .md/.docx/.csv
   python fedMigrationScripts/generatescripts/generate_breakdown.py --global # refresh the global page
   ```
5. **Jira / Confluence** — push per
   [`PUSH-TO-JIRA-CONFLUENCE.md`](../../fedMigrationScripts/docs/PUSH-TO-JIRA-CONFLUENCE.md).

## How the Jira / Confluence stories get created

| What | Source CSV / page | Import as |
|---|---|---|
| The 6 spikes themselves | `output/jira/all-stories.csv` (rows `Issue Type=Spike`) | Spikes (or Story labelled `spike`) |
| Domain stories | `output/jira/{domain}.csv` / `all-stories.csv` | Story per row, under the domain Epic |
| **Complex-case sub-tasks** | `output/complexStories/<case>/<case>.csv` | **imported separately, nested under the case's home stub** (e.g. techpack sub-tasks under `PRODUCT-BE-E-03`) |
| Confluence pages | `output/summary/{domain}/FederatedGqlBreakDown-BE-{domain}.md` + `{domain}-po-review.md` | create/update by title |

> **Why complex cases import separately:** they are kept **out** of `all-stories.csv` so they aren't
> double-counted against the 337-story program total — the **home stub** story is what the rollup tracks.

## Which cases are decided vs open (today)

| Spike | Case | Status |
|---|---|---|
| `SPIKE-02/03/04/05` | techpack · partner-drop-undrop · notRemovable-partners · polymorphic | **Accepted** |
| `SPIKE-01` | non-atomic-write-saga | **Proposed** — failure strategy open |
| `SPIKE-06` | cross-domain-association | **Proposed** — edge rule open |

See [`output/complexStories/README.md`](../complexStories/README.md) for how to *use* a case folder by role.
