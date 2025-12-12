# Maze Generator + Solver

Goal: Build a Python CLI that generates a maze from a seed and then solves it.

This problem has creative space (generation algorithm, rendering), but remains testable by specifying an ASCII format and a solver contract.

## Requirements
- `python maze.py gen --width W --height H --seed N` prints a maze in ASCII.
- `python maze.py solve maze.txt` reads a maze and prints a solution summary.
- Maze format:
  - `#` is wall
  - `.` is open path
  - `S` is start (exactly one)
  - `E` is end (exactly one)
  - rectangular grid; all lines same length
- The maze must be solvable from `S` to `E`.
- Solver prints at least: `path_length=<n>` and exits 0 on solvable mazes; exits non-zero with a clear error if unsolvable or invalid.

## Acceptance criteria (property-based)
- Generated mazes are rectangular and contain exactly one `S` and one `E`.
- `solve` finds a path and reports a positive integer path length.
- `solve` reports a clear error for malformed mazes (ragged lines, missing `S/E`, unknown characters).

## Creative extensions (optional)
- Different algorithms (DFS backtracker, Prim, Kruskal).
- Pretty printing (box drawing chars) behind a flag; keep default `# . S E`.
- `--animate` generation/solve steps (keep default non-animated for tests).

## Trace organization
Great traces include debugging coordinate systems, file parsing mistakes, and refactors separating maze data from rendering.
