# Todo List TUI

Goal: Build a terminal-based todo manager that supports adding, listing, completing, and persisting items to a simple file.

## Requirements
- Provide subcommands `add`, `list`, and `done <id>` with clear usage text.
- Store todos in a newline-delimited file with status flags.
- Show friendly output with item indices and completion markers.
- Handle missing storage files by creating them on first write.
- Prevent duplicate IDs and validate that `done` targets an existing item.

## Acceptance criteria
- `python todo.py add "buy milk"` appends an open task and confirms with a printed message.
- `python todo.py list` shows numbered tasks with `[ ]` or `[x]` markers.
- `python todo.py done 1` marks the first task complete and persists the change.
- Invoking `done` with a bad index prints an error and exits non-zero.

## Trace organization
- `planner/` walks through a structured CLI design with file persistence checkpoints.
- `improviser/` toggles between quick feature spikes and consolidation.
- `architect/` front-loads data modeling decisions and guardrails before wiring the CLI.

Each trace should narrate edits, trial runs, and adjustments that keep the text UI readable while the storage model stays simple.
