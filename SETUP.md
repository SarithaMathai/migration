# Creating the `migration` repo and pushing the code

This document records the exact steps used to create the private GitHub
repository **`XXX`** and push this folder's code to it.

---

## Prerequisites

- **Git** — check with `git --version`
- **GitHub CLI (`gh`)** — used to authenticate and create the repo

### Installing GitHub CLI (Windows)

```powershell
winget install --id GitHub.cli --source winget --accept-package-agreements
```

> After installing, open a **new** terminal so `gh` is on your PATH.
> If it still isn't recognized, use the full path:
> `& "C:\Program Files\GitHub CLI\gh.exe"`

---

## Step 1 — Authenticate with GitHub

Run this **in your own terminal** (it is interactive):

```powershell
gh auth login
```

Answer the prompts:

| Prompt | Answer |
| --- | --- |
| What account do you want to log into? | **GitHub.com** |
| Preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate? | **Login with a web browser** |

Copy the one-time code shown (e.g. `XXXX-XXXX`), press **Enter** to open the
browser, paste the code, and authorize as **SarithaMathai**.

Verify:

```powershell
gh auth status
```

---

## Step 2 — Create the private repository

```powershell
gh repo create migration --private
```

This creates an **empty private repo** at:

```
https://github.com/XXX
```

Useful variations:

```powershell
# Create AND push the current folder in one go
gh repo create migration --private --source=. --remote=origin --push

# Create with a description
gh repo create migration --private --description "Migration scripts and output"
```

---

## Step 3 — Push this folder's code

Run these from the project root (`c:\Saritha\test\migration`):

```powershell
git init                       # initialize a local git repo
git add .                      # stage all files
git commit -m "Initial commit" # create the first commit
git branch -M main             # name the default branch 'main'
git remote add origin https://github.com/XXX
git push -u origin main        # push and set upstream
```

After this, the code is live on GitHub and future pushes are just:

```powershell
git add .
git commit -m "your message"
git push
```

---

## Notes

- `.gitignore` controls which files are **excluded** from the repo. Add one if
  there are build artifacts, secrets, or large outputs you don't want pushed.
- To see what will be committed before pushing: `git status`.
