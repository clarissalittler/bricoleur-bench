# Trace 01 (Improviser)

### Step 1 — Spike add/list in one go
- Skipped subparsers; quick `if cmd == "add"` branching based on `sys.argv[1]`.
- Stored todos as lines `0|buy milk` in `todos.txt`; `list` just reads and prints raw lines.
- Ran `python todo.py add "buy milk"`; worked but list output ugly.

### Step 2 — Rework to argparse
- Friction reading positional args -> introduced `argparse` with subcommands.
- Migrated storage format to `id|status|title` and added helper `parse_line` that tolerates missing status by defaulting to `[ ]`.
- Quick manual fix-up: rewrote existing file contents to match new format.

### Step 3 — Improve list readability
- Added pretty printer: `[ ] 1: buy milk` and `[x]` when done.
- Added padding to align IDs; tested with three items.
- Left a `print("DEBUG", todos)` accidentally, caught during rerun and removed.

### Step 4 — Implement done with guardrails
- `done` marks by ID; if ID absent, prints `no such todo` and exits 1.
- Added small helper to avoid reusing IDs: compute `max` then increment.
- Confirmed `python todo.py done 2` flips marker and persists.

### Step 5 — Small quality tweaks
- Added `--file` override for ad-hoc testing; defaults to `todos.txt`.
- Wrote README snippet inside script for future help message; TODO: wire to `--help`.
- Noted follow-up: factor storage helpers into module to share with tests.
