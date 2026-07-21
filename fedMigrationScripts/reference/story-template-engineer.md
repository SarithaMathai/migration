# Story template — engineer-ready (Pipeline 2.0)

Every story in `be-04-stories.md` MUST use this exact template. It supersedes the draft
`templates/story-format.md`. Three rules changed for Pipeline 2.0:

1. **One operation per story.** A story covers exactly one query, one mutation, or one complex field
   resolver. No "and" in titles. The only allowed grouping is a single table of *trivial pass-through*
   field resolvers (no service call, no transform) — see the trivial-bundle story at the end of Phase G.
2. **YAML front-matter** opens every story so Copilot/agents can parse it. Human-readable body follows.
3. **Complexity tiers only — no day-ranges inside stories.** Use `Low | Medium | High | Very High`.
   (Rough day-ranges live only in `be-04-po-summary.md`, labeled "AI-estimated, confirm in refinement".)

---

## The template (copy verbatim per story)

````markdown
### {STORY-ID} · {one-operation title, no "and"}

```yaml
id: {STORY-ID}
title: {short title}
operation: {graphqlOperationName}
type: {query | mutation | field-resolver}
category: CAT-{1..5}
phase: {A|B|C|D|E|F|G}
complexity: {Low | Medium | High | Very High}
depends_on: [{STORY-ID}, ...]      # [] if none
ext_services:                       # [] if none
  - key: {loaderKey}
    severity: {RED | YELLOW | BLUE}
files:
  - {repo}/.../path.kt
blocked_by: {none | domain-name}
```

**As a** DGS migration engineer
**I want** {specific, single-operation goal}
**so that** {user/technical benefit}.

---

**Current Behaviour (from Phase 2 — {Q/M/F id}):**
{Copy the numbered pseudo-logic from be-02-resolver-analysis.md. This IS the spec — a junior implements
from this without opening the .txt resolver. Include the REST endpoint, headers, transform, and every
error/empty/branch path. Never write "standard error handling".}

---

**EXT Service Calls:**
{None — all calls are to this domain's own backend.}
OR
- **EXT Service** → key: `{loaderKey}` · url: `{url}` · repo: `{repo}` · severity: 🔴/🟡/🔵
  Purpose: {one line}. Handled by federation story {CAT-4 STORY-ID}.

---

**Target DGS Implementation:**
- Annotation: `{@DgsQuery | @DgsMutation | @DgsData | @DgsEntityFetcher}`
- Data fetcher: `{Name}DataFetcher.kt`
- Service method: `{Service.method}({params})` → `{HTTP} {base-url}{path}`
- Auth: `Authorization` only. **ACL note (context, not work):** if the source curries a permissionJWT
  via `getUserPermissionsJWT`, add one line — *"Current impl uses ACL to get a capability token because
  {reason}; ACL ignored in DGS implementation."* Do **not** create ACL plumbing tasks (see federation §4).
- Request mapping: {camelCase input → snake_case body via Jackson, or "none"}
- Response mapping: {snake_case → camelCase via Jackson `deepToCamelCase` equivalent}
- DataLoader: {None | `{Name}DataLoader` keyed on `{field}`}
- Pagination: {None | Spring `Pageable` page={n} size={n} matching source}

---

**Files to Create / Modify:**
- `plm-product/apps/app/src/main/resources/schema/{domain}.graphqls` — add `{operation}`
- `plm-product/.../dataFetcher/{Name}DataFetcher.kt` — create
- `plm-product/.../service/{Name}Service.kt` — add `{method}`
- `plm-product/.../model/{Type}.kt` — create DTO
- `plm-product/.../test/.../{Name}DataFetcherTest.kt` — create

---

**Dependencies:** {STORY-IDs with one-line reason each, or "None"}

---

**Acceptance Criteria:** (every item objectively verifiable by a reviewer who hasn't seen the story)
1. {e.g. "`{operation}` schema matches `be-03-schema.graphql`."}
2. {e.g. "Service calls `GET {base}/{path}` with `Authorization` + `SPARK-Capability-Token`."}
3. {request/response transform rule, specific}
4. {error path: "404 → returns null; 5xx → throws DgsEntityNotFoundException"}
5. {empty/branch path}
6. {EXT handling, if any}

---

**Test Cases:**
- [ ] Unit: `{testName}` — happy path
- [ ] Unit: `{testName}` — {error path}
- [ ] Unit: `{testName}` — {branch / empty path}
- [ ] Integration: `{testName}` — query via DGS test client returns expected shape
- [ ] Parity: `{testName}` — DGS == spark-internal-graphql for `{example input}`  *(High/Very-High only)*
````

---

## Definition of Ready for a Engineer (the quality bar)

A story is **not done** being written until a junior could implement it without asking a question.
Before publishing a story, verify all of these:

- [ ] Title names **one** operation; there is no "and".
- [ ] **Current Behaviour** has numbered steps, the **exact endpoint + HTTP verb**, and **every** branch
      (internal/external user, 404, empty list, polymorphic case). No forbidden phrases
      ("various transformations", "standard error handling", "handles typical cases").
- [ ] Every `ctx.loaders.X` cross-domain call appears as an **EXT Service** line with a severity glyph.
- [ ] **Files to Create / Modify** lists concrete paths.
- [ ] **Dependencies** are real story IDs (not prose).
- [ ] Acceptance criteria are **checkable** — a reviewer can mark each true/false.
- [ ] At least one **error-path** and one **happy-path** test case.
- [ ] YAML front-matter parses and matches the human-readable body.

## Story ID & phase convention (unchanged)

`SPARK-{DOMAIN_ABBREV}-{PHASE}{NN}` — e.g. `BOM-BE-B-02`.
Phases group by *what they deliver*: **A** Foundation/Schema · **B** Core Reads · **C** Search/Listing ·
**D** Mutations · **E** Complex/Orchestration · **F** Federation/Stitching · **G** Field Resolvers & Tests.
Category `CAT-1..5` is metadata, not the grouping key.
