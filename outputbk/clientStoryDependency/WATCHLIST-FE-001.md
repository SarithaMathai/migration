## WATCHLIST-FE-001 — Migrate watchlist reads
Queries in scope: getWatchlistByIds, getWatchlistByFilter · Mutations excluded: 0

**Must complete first:** BE — WATCHLIST-BE-B-01, WATCHLIST-BE-C-01, WATCHLIST-BE-G-01, WATCHLIST-BE-G-02, WATCHLIST-BE-G-03

### Queries

> The root GraphQL operations this story ships. Readiness is driven from this table plus any genuine gap fields below (`New?` = Yes) — a plain pass-through field with no resolver of its own is not a distinct story and does not appear in either table.

| Query | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| getWatchlistByFilter | WATCHLIST-BE-C-01 | — | No | getWatchlistByFilter |  |
| getWatchlistByIds | WATCHLIST-BE-B-01 | — | No | getWatchlistByIds |  |

### Fields

> Field/entity-level detail behind the queries above, for traceability — not part of the readiness count except where `New?` = Yes (a genuine gap).

| Field/Entity | Story | External Dep | New? | Impacts (queries) | Notes |
|---|---|---|---|---|---|
| attachments | WATCHLIST-BE-G-03 | search | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| createdBy | WATCHLIST-BE-G-02 | user-profile | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| description | WATCHLIST-BE-G-01 | — | No | getWatchlistByFilter |  |
| participantDetails | WATCHLIST-BE-G-02 | user-group | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| product | WATCHLIST-BE-G-03 | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| products | WATCHLIST-BE-C-01 | — | No | getWatchlistByFilter |  |
| reasonIds | WATCHLIST-BE-G-01 | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| reasons | WATCHLIST-BE-G-01 | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| statusId | WATCHLIST-BE-G-01 | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| statusName | WATCHLIST-BE-G-01 | — | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| updatedBy | WATCHLIST-BE-G-02 | user-profile | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |
| workspaces | WATCHLIST-BE-G-02 | workspaceV2 | No | getWatchlistByFilter, getWatchlistByIds | via `...WatchlistFields` |

## WATCHLIST-FE-001 — Readiness
All 14 distinct fields/entities this story's queries touch resolve to existing, real backend stories — no gaps, no spike gates. This story is ready to sequence as soon as its listed BE stories are delivered.
