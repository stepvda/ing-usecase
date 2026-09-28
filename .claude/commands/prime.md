---
description: Load the project's standing context - what this is, what was decided, and what is currently open
---

Read these, in this order, before doing anything else in this session:

1. `README.md` - what the project is, the scope as measured, and the open items.
2. `technical_deep_dive.md` - skim the module reference; read section 6 ("The
   lessons, extracted") and section 8 ("Open issues") in full.
3. `docs/decisions.md` - the last 150 lines. It is append-only, so the end is
   the current state and early entries may have been superseded.
4. `config/feature_dictionary.yaml` - do not read it all. Read the header and
   the `comparability`, `tiers` and `extraction_methods` blocks, and nothing
   else unless a task needs a specific feature.

Then run, and report the literal output of each:

```bash
git log --oneline -10
git status --short
python3 -m pytest tests/ -q 2>&1 | tail -1
python3 scripts/check_schema_freeze.py
```

Finally, tell me in at most ten lines:

- where the working tree stands (branch, anything uncommitted, anything that
  looks like it was left mid-task);
- the test count and whether the schema freeze passes;
- the open items from the README that still look open, checked against the repo
  rather than taken on trust;
- anything you noticed that contradicts the documentation.

Do not start work. Do not propose a plan. This command exists so the next
instruction lands on a loaded context, nothing more. If something in the
documentation turns out to be wrong, say so here rather than acting on it.
