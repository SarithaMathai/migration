# generatescripts — the generators

This folder holds **only the Python generators** (`generate_*.py`). Run them from the repo root:

```bash
python fedMigrationScripts/generatescripts/generate_all.py        # all domains → output/summary + output/jira
python fedMigrationScripts/generatescripts/generate_breakdown.py --global
```

📖 **All documentation moved to [`../docs/`](../docs/):**
- [`README.md`](../docs/README.md) — file inventory + script-runner + navigate-by-role
- [`README-PO.md`](../docs/README-PO.md) · [`README-ARCHITECT.md`](../docs/README-ARCHITECT.md) · [`README-ENGINEER.md`](../docs/README-ENGINEER.md) — role guides
- [`PUSH-TO-JIRA-CONFLUENCE.md`](../docs/PUSH-TO-JIRA-CONFLUENCE.md) · [`PUSH-TO-JIRA-HAIKU.md`](../docs/PUSH-TO-JIRA-HAIKU.md) — publishing prompts

Repo-wide "how to use" entry point: [`/README.md`](../../README.md).
