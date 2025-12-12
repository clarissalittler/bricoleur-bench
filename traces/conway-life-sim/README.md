# Conway’s Game of Life

Goal: Build a Python CLI that simulates Conway’s Game of Life from an input pattern file and prints frames as ASCII.

This problem supports creative rendering (different characters, borders, viewport choices) while staying testable by pinning a default format.

## Requirements
- `python life.py --steps N pattern.txt` reads a pattern and prints N+1 frames (including step 0).
- Default rendering uses:
  - `#` for live cells
  - `.` for dead cells
- Provide a fixed bounding box output: the input pattern’s rectangular dimensions.
- Validate `--steps` (non-negative) and error clearly on invalid files.

## Pattern format (simple)
Plain text grid of `#` and `.` with no spaces.

See `patterns/glider.txt` for an example.

## Acceptance criteria (default mode)
- `python life.py --steps 1 patterns/blinker.txt` prints two frames where the blinker oscillates correctly.
- `python life.py --steps 0 patterns/glider.txt` prints exactly the input grid as the only frame.
- Missing file exits non-zero with a clear error.

## Creative extensions (optional)
- `--wrap` torus mode.
- `--viewport` cropping and panning.
- Alternate characters or ANSI color (keep default plain output for tests).

## Trace organization
Great traces include off-by-one frame bugs, neighbor-count errors, and refactors from nested loops to helper functions.
