# Trace 01 – Architect (Maze Generator + Solver)

Separates concerns: format validation, generation, solving, and CLI.

## Step 1: Maze model + parser module

Snapshot: maze_io.py
```python
from __future__ import annotations

from dataclasses import dataclass


ALLOWED = {"#", ".", "S", "E"}


@dataclass(frozen=True)
class Maze:
    grid: list[list[str]]

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self) -> int:
        return len(self.grid)


def parse(path: str) -> Maze:
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        raise ValueError("empty maze")
    w = len(lines[0])
    if any(len(l) != w for l in lines):
        raise ValueError("ragged maze")
    grid = [list(l) for l in lines]
    for row in grid:
        for ch in row:
            if ch not in ALLOWED:
                raise ValueError("unknown character in maze")
    if sum(ch == "S" for row in grid for ch in row) != 1:
        raise ValueError("maze must contain exactly one S")
    if sum(ch == "E" for row in grid for ch in row) != 1:
        raise ValueError("maze must contain exactly one E")
    return Maze(grid)


def render(maze: Maze) -> str:
    return "\n".join("".join(row) for row in maze.grid) + "\n"
```

## Step 2: Generator + solver modules

Snapshot: maze_core.py
```python
from __future__ import annotations

import random
from collections import deque

from maze_io import Maze


def gen(width: int, height: int, seed: int) -> Maze:
    if width < 3 or height < 3:
        raise ValueError("width/height must be >= 3")
    rng = random.Random(seed)
    grid = [["#"] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            grid[y][x] = "."

    sx, sy = 1, 1
    ex, ey = width - 2, height - 2
    path = {(sx, sy)}
    x, y = sx, sy
    while (x, y) != (ex, ey):
        if rng.random() < 0.5 and x < ex:
            x += 1
        elif y < ey:
            y += 1
        path.add((x, y))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x, y) in path:
                continue
            if rng.random() < 0.30:
                grid[y][x] = "#"

    grid[sy][sx] = "S"
    grid[ey][ex] = "E"
    return Maze(grid)


def solve_length(maze: Maze) -> int | None:
    w = maze.width
    h = maze.height
    start = next((x, y) for y in range(h) for x in range(w) if maze.grid[y][x] == "S")
    end = next((x, y) for y in range(h) for x in range(w) if maze.grid[y][x] == "E")

    q = deque([(start[0], start[1], 0)])
    visited = [[False] * w for _ in range(h)]
    visited[start[1]][start[0]] = True
    while q:
        x, y, d = q.popleft()
        if (x, y) == end:
            return d
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                if maze.grid[ny][nx] in (".", "E"):
                    visited[ny][nx] = True
                    q.append((nx, ny, d + 1))
    return None
```

## Step 3: CLI wiring with clear errors

Snapshot: maze.py
```python
import argparse
import sys

from maze_core import gen, solve_length
from maze_io import parse, render


def main() -> int:
    p = argparse.ArgumentParser(prog="maze.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("--width", type=int, required=True)
    g.add_argument("--height", type=int, required=True)
    g.add_argument("--seed", type=int, required=True)
    s = sub.add_parser("solve")
    s.add_argument("maze")
    args = p.parse_args()

    try:
        if args.cmd == "gen":
            maze = gen(args.width, args.height, args.seed)
            print(render(maze), end="")
            return 0

        maze = parse(args.maze)
        dist = solve_length(maze)
        if dist is None:
            print("error: unsolvable", file=sys.stderr)
            return 1
        print(f"path_length={dist}")
        return 0
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```
