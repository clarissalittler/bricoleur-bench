# Trace 01 – Architect (Conway’s Game of Life)

Separates parsing, simulation, and rendering so later features (wrap mode, viewport) don’t infect core logic.

## Step 1: Core module

Snapshot: patterns/blinker.txt
```text
.....
..#..
..#..
..#..
.....
```

Snapshot: life_core.py
```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Grid:
    cells: list[list[bool]]

    @property
    def height(self) -> int:
        return len(self.cells)

    @property
    def width(self) -> int:
        return len(self.cells[0]) if self.cells else 0


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def step(grid: Grid) -> Grid:
    h = grid.height
    w = grid.width
    out = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and grid.cells[ny][nx]:
                    n += 1
            alive = grid.cells[y][x]
            out[y][x] = (alive and n in (2, 3)) or ((not alive) and n == 3)
    return Grid(out)
```

## Step 2: Parser + renderer

Snapshot: life_io.py
```python
from __future__ import annotations

from pathlib import Path

from life_core import Grid


def parse_grid(path: Path) -> Grid:
    raw = [l.rstrip("\n") for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not raw:
        raise ValueError("empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise ValueError("ragged grid")
    for l in raw:
        for ch in l:
            if ch not in (".", "#"):
                raise ValueError("grid must contain only . and #")
    return Grid([[ch == "#" for ch in l] for l in raw])


def render(grid: Grid) -> str:
    return "\n".join("".join("#" if c else "." for c in row) for row in grid.cells)
```

## Step 3: CLI wiring

Snapshot: life.py
```python
import argparse
import sys
from pathlib import Path

from life_core import step
from life_io import parse_grid, render


def main() -> int:
    p = argparse.ArgumentParser(prog="life.py")
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("pattern", type=Path)
    args = p.parse_args()
    if args.steps < 0:
        print("error: --steps must be >= 0", file=sys.stderr)
        return 1

    try:
        grid = parse_grid(args.pattern)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(render(grid))
    for _ in range(args.steps):
        print()
        grid = step(grid)
        print(render(grid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
