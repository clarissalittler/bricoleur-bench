# Purpose
This directory is for building out (synthetic) traces of hypothetical student work from start to finish of a program.

It should have subdirectories for the different problems and each of those directories should in turn have subdirectories containing the traces for the student types.

In this directory there are two lists that should be maintained:

1. student-types.md
2. problem-list.md

These traces should represent a coherent sequence of potential edits, missteps, and in-progress programs in terms of meeting the goal.

We want to reflect an editing sequence that is coherent for the student type and reflects actual changes to a single program in service of getting it to a goal, mistakes and missteps and refactors all included.

The student types should reflect a spectrum from "bricoleur" to "planner", using different kinds of tinkering and planning and levels of abstraction vs. concrete thinking.

## Snapshot extraction (for automated feedback)

Trace files can optionally include explicit code snapshots that are extracted into standalone files for automated feedback systems.

Format inside a trace (`trace-*.md`):
- Add a line `Snapshot: relative/path.py` (or any relative path)
- Immediately follow it with a fenced code block containing the full file contents for that step

Example:

```text
Snapshot: todo.py
```python
print("hello")
```
```

To generate snapshot files:
- Full per-step workspace: `python3 traces/tools/extract_snapshots.py --traces-root traces`
- Only files that changed in each step: `python3 traces/tools/extract_snapshots.py --traces-root traces --changed-only`

Outputs are written next to each persona trace under `snapshots/<trace-stem>/{full-state,changed-only}/step-XX/...`, with a `manifest.json` for each mode and a top-level index at `traces/snapshots-summary.json`.
