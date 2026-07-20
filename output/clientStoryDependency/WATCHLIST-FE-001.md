## WATCHLIST-FE-001 — Migrate watchlist reads
Queries in scope: getWatchlistByIds, getWatchlistByFilter · Mutations excluded: 0

**Must complete first:** BE — PRODUCT-BE-G-07, PRODUCT-BE-G-09, PRODUCT-BE-G-10, PRODUCT-BE-G-13, WATCHLIST-BE-B-01, WATCHLIST-BE-C-01, WATCHLIST-BE-G-01, WATCHLIST-BE-G-02, WATCHLIST-BE-G-03, WATCHLIST-BE-G-05 · Spikes — SPIKE-04 · New — NEW-WATCHLIST-BE-G-??

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| getWatchlistByFilter | WATCHLIST-BE-C-01 | — | — | No | getWatchlistByFilter |  |
| getWatchlistByIds | WATCHLIST-BE-B-01 | — | — | No | getWatchlistByIds |  |

### Fields

> Dependency-bearing fields only — a named External Dep service, or a genuine unresolved gap (`New?` = Yes) not yet attributed to one. Fields with no cross-team dependency (resolved internally by an existing same-DGS story) are omitted here but still counted in the readiness line below.

| Field/Entity | Story | External Dep | Ext-Story | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|---|
| droppedPartnerIds | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| editable | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| owningPartnerType | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| packagingAttributes | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| preferredStyle | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| primaryMaterial | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| productMaterials | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| secondaryMaterial | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| thumbnailId | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| vendorStyleNumber | NEW-WATCHLIST-BE-G-?? | — | — | Yes | getWatchlistByFilter, getWatchlistByIds | via `...ProductBaseInfoFragment` |
| attachments | WATCHLIST-BE-G-03 | search | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| brand | PRODUCT-BE-G-13 | ig | — | No | getWatchlistByFilter, getWatchlistByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| createdBy | WATCHLIST-BE-G-02 | user-profile | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| droppedPartners | PRODUCT-BE-G-07 | vmm | — | No | getWatchlistByFilter, getWatchlistByIds | 🔬 SPIKE-04 (gated); cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| participantDetails | WATCHLIST-BE-G-02 | user-group | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| reservedDpcis | PRODUCT-BE-G-10 | apex | — | No | getWatchlistByFilter, getWatchlistByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| tags | PRODUCT-BE-G-13 | tag | — | No | getWatchlistByFilter, getWatchlistByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| tcins | PRODUCT-BE-G-13 | corona | — | No | getWatchlistByFilter, getWatchlistByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment` |
| teams | WATCHLIST-BE-G-02 | user-group | — | No | getWatchlistByFilter, getWatchlistByIds | external via `participantDetails`; via `...ProductBaseInfoFragment`; via `...WatchlistParticipants` |
| updatedBy | WATCHLIST-BE-G-02 | user-profile | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| users | WATCHLIST-BE-G-02 | user-group | — | No | getWatchlistByFilter, getWatchlistByIds | external via `participantDetails`; via `...WatchlistParticipants` |
| workspaces | PRODUCT-BE-G-09 | workspaceV2 | — | No | getWatchlistByFilter, getWatchlistByIds | cross-domain: `Product` owned by `product`; via `...ProductBaseInfoFragment`; via `...WatchlistFields` |

## WATCHLIST-FE-001 — Readiness
22 of 32 distinct fields/entities resolve to existing backend stories. 10 field(s) have no covering story yet (see the `NEW-...-??` placeholders above) and block full readiness until a real story is authored. 1 field(s) sit behind an unresolved spike (SPIKE-04) and cannot be built past the spike's decision.
