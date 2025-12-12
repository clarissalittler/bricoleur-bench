# SVG Logo Generator

Goal: Build a Python CLI that generates a simple SVG “logo” for a phrase.

This problem is creativity-friendly (layout, colors, shapes) while remaining testable by requiring valid SVG output and a default deterministic theme.

## Requirements
- `python logo.py "Hello"` prints an SVG document to stdout and exits 0.
- Default output is deterministic for the same input text.
- Provide:
  - `--width` and `--height`
  - `--theme` (at least `default`, optionally more)
- Validate dimensions and error clearly on invalid args.

## Acceptance criteria (default theme)
- Output starts with `<svg` (or an XML header then `<svg`) and ends with `</svg>`.
- Output includes the input phrase as an SVG `<text>` element (exact styling is free).
- Invalid sizes (e.g., negative width) exit non-zero with a clear error.

## Creative extensions (optional)
- Randomized palettes behind `--seed` (default stays deterministic without `--seed`).
- Decorative shapes (circles, paths) and text effects.
- Export background transparency flag.

## Trace organization
Good traces include iterations on coordinate systems, escaping XML, and refactors to a tiny layout engine.
