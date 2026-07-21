## PKG-FE-001 — Migrate packaging reads
Queries in scope: getPackagings, getPackagingById, getPackagingComponentStatus · Mutations excluded: 0

**Must complete first:** BE — PKG-BE-B-01, PKG-BE-B-02, PKG-BE-G-01, PKG-BE-G-02, PKG-BE-G-04

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getPackagingById | PKG-BE-B-02 | — | — | No | getPackagingById, getPackagingComponentStatus |  |
| getPackagings | PKG-BE-B-01 | — | — | No | getPackagings |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| businessPartner | PKG-BE-G-01 | vmm | — | No | getPackagingById, getPackagings | via `...PackagingDetailsBaseFragment`; via `...PackagingDetailsFragment` |
| createdBy | PKG-BE-G-02 | user-profile | — | No | getPackagingById, getPackagings | via `...PackagingDetailsBaseFragment`; via `...PackagingDetailsFragment` |
| dielineEvaluators | PKG-BE-G-02 | user-profile | — | No | getPackagingById, getPackagings | via `...PackagingDetailsBaseFragment`; via `...PackagingDetailsFragment` |
| suggestedRetailPriceByDPCI | PKG-BE-G-04 | apex | — | No | getPackagingById, getPackagings | via `...PackagingDetailsBaseFragment`; via `...PackagingDetailsFragment` |
| updatedBy | PKG-BE-G-02 | user-profile | — | No | getPackagingById, getPackagings | via `...PackagingDetailsBaseFragment`; via `...PackagingDetailsFragment` |
| waveDescription | PKG-BE-G-04 | tag | — | No | getPackagingById, getPackagings | via `...PackagingDetailsBaseFragment`; via `...PackagingDetailsFragment` |

## PKG-FE-001 — Readiness
All 10 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
