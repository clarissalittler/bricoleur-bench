# ASCII Art Poster

Goal: Build a Python CLI that renders a short message as an ASCII “poster”.

This problem has room for creativity (borders, typography, layout) while remaining testable by defining a default style with deterministic output.

## Requirements
- Accept a message (positional) and print a poster to stdout.
- Provide a fixed default style that is deterministic for a given input.
- Support at least:
  - `--width N` (min width; wraps words)
  - `--align left|center|right`
  - `--border ascii|none` (default `ascii`)
- Validate inputs and emit clear errors for invalid flags or widths that are too small.

## Acceptance criteria (default style)
- `python poster.py "hi"` prints a bordered poster (exact format defined in the trace snapshots) and exits 0.
- `python poster.py --border none "hi"` prints just the wrapped/aligned text without a border and exits 0.
- `python poster.py --align center --width 10 "one two three"` wraps deterministically and exits 0.
- Invalid width (e.g., `--width 1`) exits non-zero with a clear error.

## Creative extensions (optional)
- Alternate border styles (double-line, rounded, “speech bubble”).
- Themes (e.g., `--theme neon|minimal|retro`) that change padding/border/typography.
- Simple banner fonts (block letters) behind a flag (keep default plain text).

## Trace organization
Create persona subdirectories (e.g., `bricoleur/`, `planner/`) and traces that show the poster evolving toward the acceptance criteria, including dead-ends in wrapping/alignment logic.
