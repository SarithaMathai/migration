# Getting started — spark-claims + Copilot POC

For an Engineer setting this up **for the first time**, from an empty machine to implementing their first story. Follow in order.

---

## 1. Prerequisites

- [ ] GitHub Copilot access on your account, assigned to the `spark-claims` repo's org.
- [ ] VS Code (or your JetBrains IDE) with the **GitHub Copilot** and **GitHub Copilot Chat** extensions installed and signed in.
- [ ] Git configured locally (`git config --global user.name/user.email`).
- [ ] JDK + the Kotlin/Gradle toolchain this repo needs (see the real `spark-claims` repo's own `README.md`/`CONTRIBUTING.md` once cloned — versions aren't part of this POC).

## 2. Clone the target repo

Clone the **actual `spark-claims` service repo** — not this migration/analysis repo. This POC's files get copied *into* that clone. Unlike `plm-product`, this is a standalone repo — there's no monorepo module to navigate into.

```bash
git clone https://github.com/XXX/spark-claims.git
cd spark-claims
```

If you're setting this up as a new contribution to `spark-claims` itself, create a branch first:

```bash
git checkout -b chore/add-copilot-instructions
```

## 3. Copy the Copilot files into the clone

From this migration repo, copy `AGENTS.md`, `README.md`, `EXAMPLE-USAGE.md` and the whole `.github/` subtree into the `spark-claims` clone's **root**:

```bash
# run from the migration repo root (this repo)
SRC="fedMigrationScripts/copilot-poc/spark-claims"
DEST="../spark-claims"     # path to your spark-claims clone from step 2

cp "$SRC/AGENTS.md"           "$DEST/"
cp "$SRC/README.md"           "$DEST/COPILOT-README.md"      # rename if spark-claims already has a README.md — don't overwrite it
cp "$SRC/EXAMPLE-USAGE.md"    "$DEST/"
cp -r "$SRC/.github/instructions" "$DEST/.github/"
cp -r "$SRC/.github/prompts"      "$DEST/.github/"
cp -r "$SRC/.github/chatmodes"    "$DEST/.github/"
cp "$SRC/.github/copilot-instructions.md" "$DEST/.github/"   # see step 3a if spark-claims already has one
```

(PowerShell equivalent: `Copy-Item -Recurse` for the folders, `Copy-Item` for the files.)

### 3a. If `spark-claims/.github/` already has content

Almost certainly true — CI workflows, `PULL_REQUEST_TEMPLATE.md`, issue templates, maybe an existing `copilot-instructions.md`. **Do not blindly overwrite:**

- `.github/instructions/`, `.github/prompts/`, `.github/chatmodes/` are new folders in most repos — copying them in is additive and safe.
- `.github/copilot-instructions.md`: if one already exists, **merge** — keep whatever's already there (org-wide conventions, security rules) and append this POC's migration-specific sections (engineering model, story-id scheme, hard rules, the federation-contribution note about `Product`/`ResourcesCount`). Don't replace wholesale.
- `AGENTS.md` at repo root: same — merge if one exists.

### 3b. Verify what landed

```bash
git status
```

You should see new/modified files only under `.github/instructions/`, `.github/prompts/`, `.github/chatmodes/`, `.github/copilot-instructions.md`, `AGENTS.md`, plus the two doc files. Nothing else in the repo should have changed.

## 4. Open in VS Code and confirm Copilot sees it

```bash
code .
```

Then, in the editor:

1. Open **Copilot Chat** (sidebar icon or `Ctrl+Alt+I` / `Cmd+Alt+I`).
2. Check the **chat mode dropdown** at the top of the chat panel — you should see **story-implementer**, **parity-checker**, and **schema-steward** listed alongside the default modes. If they don't appear, confirm the files are at `.github/chatmodes/*.chatmode.md` (exact suffix, exact folder) and reload the VS Code window (`Ctrl+Shift+P` → "Developer: Reload Window").
3. Type `/` in the chat box — you should see `/implement-story`, `/check-spike-gate`, `/derive-dgs-schema`, `/write-parity-tests` in the autocomplete list. Same reload trick if missing.
4. Open the `claims.graphqls` schema file (or any Kotlin fetcher once one exists) and ask Copilot Chat a question about it (e.g. "what conventions apply to this file?") — it should reference `copilot-instructions.md` and, since the file matches an `applyTo` glob, the matching scoped instruction file too. This confirms the repo-wide and path-scoped instructions are both being picked up.

If nothing above shows up: confirm you're on a Copilot plan/IDE version that supports custom instructions, prompt files, and chat modes (these are newer Copilot features — check your extension version is current), and that the files are committed or at least saved on disk (some IDE integrations only pick up saved files).

## 5. Implement your first story

Now follow **[EXAMPLE-USAGE.md](./EXAMPLE-USAGE.md)** — it walks `CLAIM-BE-B-01` end-to-end using exactly the setup you just created. Short version:

1. Get your assigned story id from Jira (e.g. `CLAIM-BE-B-02`).
2. In Copilot Chat, switch to the **story-implementer** chat mode.
3. Type `Implement {story-id}` and paste the Jira ticket text if asked.
4. Follow along — gate check (including the `CLAIM-BE-F-01`/`F-02` federation-blocked check, distinct from spike gating), contract read, diff plan (confirm before it writes anything), implementation, verification, PR draft.
5. Before opening the PR, run the **parity-checker** chat mode to confirm response-shape parity with the legacy resolver, and **schema-steward** if you touched `claims.graphqls`.

## 6. Commit and push the Copilot setup itself (if you're the one introducing it)

```bash
git add AGENTS.md .github/copilot-instructions.md .github/instructions .github/prompts .github/chatmodes EXAMPLE-USAGE.md
git commit -m "Add GitHub Copilot instructions, prompts and chat modes for the DGS migration"
git push -u origin chore/add-copilot-instructions
```

Open a PR against `spark-claims`'s default branch so the whole team gets these files once it merges — after that, every Engineer just needs steps 1, 4 and 5 (clone, open, implement); the copy step is one-time.
