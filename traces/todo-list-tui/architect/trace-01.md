# Trace 01 (Architect)

### Design notes
- Separate storage from CLI: `storage.py` handles read/write; `cli.py` handles argparse.
- File format: JSON list of objects `{"id": 1, "title": "...", "done": false}` to allow future metadata.
- Error model: validation errors exit 1 with concise message; normal ops exit 0.

### Step 1 — Storage contract
- Sketched `load(path)` and `save(path, todos)` signatures; default file `todos.json`.
- Added invariant: IDs must be unique and increasing; `save` sorts by id before writing.
- Wrote docstring examples for both helpers to anchor serialization format.

### Step 2 — CLI scaffolding
- Built `argparse` with subcommands and shared `--file`; wired to stub handlers that call storage helpers.
- Added `--format` flag placeholder to allow switching to plain text later.
- Verified `python todo.py --help` shows subcommands with short summaries.

### Step 3 — Implement add/list/done
- `add`: loads todos, assigns `max_id + 1`, appends, saves; prints `added #<id> <title>`.
- `list`: prints `[ ]`/`[x]` rows with id and title; exits 0 if none.
- `done`: validates id exists, toggles flag, saves; prints confirmation.
- Added guard that disallows marking already-complete item twice; exits with explanation.

### Step 4 — Validation and resilience
- Added check that JSON file with malformed data raises clear message and exits 1.
- Noted potential race on concurrent writes; documented in code comments as out of scope.
- Added TODO to introduce lockfile later.

### Step 5 — Dry run
- Simulated flow using temporary file; ran add -> list -> done -> list, outputs matched acceptance criteria.
- Kept debug logging optional behind `--verbose` flag to avoid noisy traces.
