# Trace 01 (Planner)

### Plan
- Define data model: list of dicts with `id`, `title`, `done` persisted to `todos.txt`.
- Implement CLI scaffold with subparsers: `add`, `list`, `done`.
- Add persistence helpers `load_todos` and `save_todos` that tolerate missing files.
- Finish commands in order: add -> list -> done.
- Verify flows with sample runs.

### Step 1 — CLI and storage helpers
- Added argparse with `subparsers` and shared `--file todos.txt` option for overrides.
- Implemented `load_todos(path)` returning empty list when file missing; `save_todos` writes `id|status|title` lines.
- Ran `python todo.py list` and confirmed it prints nothing rather than throwing.

### Step 2 — Add command
- `add` creates incremental IDs via `max(ids)+1 if ids else 1`; appends to list then saves.
- Output format: `added [ ] 1: buy milk`.
- Smoke test: `python todo.py add "buy milk"` created file and message printed.

### Step 3 — List command
- Implemented pretty printer showing `[ ]` or `[x]` with numbering.
- Ensured list reads after write to confirm persistence.
- Verified `python todo.py list` after two adds shows sequential IDs and statuses.

### Step 4 — Done command with validation
- Added guard: if index not found, print error to stderr and `sys.exit(1)`.
- Marked task complete by toggling `done=True` and saving file.
- Tested `python todo.py done 1` followed by `list`; saw `[x]` marker.

### Step 5 — Cleanup and notes
- Added help examples in parser description for each subcommand.
- Left TODOs to add unit tests around malformed storage lines and concurrent writes.
